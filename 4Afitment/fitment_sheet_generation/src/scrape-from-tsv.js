import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { openBrowser } from "./browser.js";
import {
  chooseOptionIfNeeded,
  chooseOptionTextIfNeeded,
  findButton,
  findControl,
  findYearRangeControls,
  getOptions
} from "./dom.js";
import { appendJsonLine, readJson, writeJson } from "./io.js";

let restartCount = 0;
const maxRestarts = 5;

while (true) {
  try {
    await runPass();
    break;
  } catch (error) {
    if (isBrowserClosedError(error) && restartCount < maxRestarts) {
      restartCount += 1;
      console.log(`浏览器被关闭，自动重启继续，第 ${restartCount}/${maxRestarts} 次。`);
      continue;
    }
    throw error;
  }
}

async function runPass() {
  const { config, context, page } = await openBrowser();

  try {
    const input = parseInputTsv(config.inputTsvFile);
    const checkpoint = readJson(config.tsvCheckpointFile, {
      completed: [],
      failed: [],
      notFound: [],
      modelsByManufacturer: {}
    });
    const completed = new Set(checkpoint.completed ?? []);
    const failed = new Set(checkpoint.failed ?? []);
    const notFound = checkpoint.notFound ?? [];
    const modelsByManufacturer = checkpoint.modelsByManufacturer ?? {};

    if (fs.existsSync(config.requestLogFile)) fs.rmSync(config.requestLogFile);
    ensureMarkdownHeader(config, input);
    writeSummary(config, input, checkpoint);

    page.on("response", async (response) => {
      const url = response.url();
      if (!/4afitment|vehicle|year|make|model|manufacturer|vc/i.test(url)) return;

      const contentType = response.headers()["content-type"] || "";
      if (!contentType.includes("json")) return;

      try {
        appendJsonLine(config.requestLogFile, {
          status: response.status(),
          url,
          body: await response.json()
        });
      } catch {
        // Some JSON-looking responses are not readable after navigation; ignore them.
      }
    });

    await context.grantPermissions(["clipboard-read", "clipboard-write"], { origin: new URL(config.startUrl).origin }).catch(() => {});

    await page.goto(config.startUrl, { waitUntil: "domcontentloaded" });
    await page.waitForLoadState("networkidle").catch(() => {});

    const loginVisible = await page.locator("input[name='username'], input[name='password']").first().isVisible().catch(() => false);
    if (loginVisible) {
      throw new Error("当前还是登录页。请先运行 .\\run.ps1 src\\login.js，手动登录后再运行 TSV 抓取。");
    }

    const yearSelectors = await findYearRangeControls(page, config.selectors, config.labels);
    const manufacturerSelector = await findControl(page, config.selectors.manufacturer, config.labels.manufacturer);
    const modelSelector = await findControl(page, config.selectors.model, config.labels.model);
    const searchButton = await findButton(page, config.selectors.searchButton, config.labels.searchButton);

    console.log("识别到控件：");
    console.log(`yearFrom: ${yearSelectors.from}`);
    console.log(`yearTo: ${yearSelectors.to}`);
    console.log(`manufacturer: ${manufacturerSelector}`);
    console.log(`model: ${modelSelector}`);
    console.log(`TSV 输入：${config.inputTsvFile}`);

    const changedYearFrom = await chooseOptionTextIfNeeded(page, yearSelectors.from, config.yearRange.from);
    if (changedYearFrom) await page.waitForTimeout(config.timeouts.settleMs);
    const changedYearTo = await chooseOptionTextIfNeeded(page, yearSelectors.to, config.yearRange.to);
    if (changedYearTo) await page.waitForTimeout(config.timeouts.settleMs);

    const siteManufacturers = await getOptions(page, manufacturerSelector);
    console.log(`TSV 品牌数量：${input.entries.length}`);

    for (const entry of input.entries) {
      assertPageOpen(page);

      const manufacturer = findOption(siteManufacturers, entry.make);
      if (!manufacturer) {
        recordNotFound(notFound, {
          make: entry.make,
          model: entry.model,
          reason: "品牌在 4AFitment 制造商下拉列表中找不到"
        });
        saveCheckpoint(config, checkpoint, completed, failed, notFound);
        writeSummary(config, input, { ...checkpoint, notFound });
        console.log(`找不到品牌：${entry.make}`);
        continue;
      }

      let models = modelsByManufacturer[manufacturer.text] ?? [];
      const needsAllModels = !entry.model;
      const requestedModelsAlreadyDone = !needsAllModels
        && completed.has(rowKey(manufacturer.text, entry.model));
      if (requestedModelsAlreadyDone) continue;

      const changedManufacturer = await chooseOptionIfNeeded(page, manufacturerSelector, manufacturer);
      if (changedManufacturer) await page.waitForTimeout(config.timeouts.settleMs);

      if (!models.length) {
        models = await getOptions(page, modelSelector);
        modelsByManufacturer[manufacturer.text] = models;
        checkpoint.modelsByManufacturer = modelsByManufacturer;
        saveCheckpoint(config, checkpoint, completed, failed, notFound, { currentManufacturer: manufacturer.text });
      }

      const targetModels = needsAllModels
        ? models
        : [findOption(models, entry.model)].filter(Boolean);

      if (!targetModels.length) {
        recordNotFound(notFound, {
          make: entry.make,
          model: entry.model,
          reason: "车型在该品牌车型下拉列表中找不到"
        });
        saveCheckpoint(config, checkpoint, completed, failed, notFound);
        writeSummary(config, input, { ...checkpoint, notFound });
        console.log(`找不到车型：${entry.make} / ${entry.model}`);
        continue;
      }

      if (needsAllModels && targetModels.every((model) => completed.has(rowKey(manufacturer.text, model.text)))) {
        continue;
      }

      console.log(`${manufacturer.text}: 准备处理 ${targetModels.length} 个车型`);

      for (const model of targetModels) {
        assertPageOpen(page);
        const key = rowKey(manufacturer.text, model.text);
        if (completed.has(key)) continue;

        try {
          const changedModel = await chooseOptionIfNeeded(page, modelSelector, model);
          if (changedModel) await page.waitForTimeout(config.timeouts.settleMs);

          await searchButton.click();
          await page.waitForLoadState("networkidle").catch(() => {});
          await page.waitForTimeout(config.timeouts.settleMs);

          const copyButton = await findButton(page, config.selectors.copyButton, config.labels.copyButton);
          await copyButton.click();
          await page.waitForTimeout(300);

          const copied = await readClipboardText(page);
          appendMarkdownSection(config, {
            manufacturer: manufacturer.text,
            model: model.text,
            content: copied
          });

          completed.add(key);
          failed.delete(key);
          saveCheckpoint(config, checkpoint, completed, failed, notFound, {
            currentManufacturer: manufacturer.text,
            currentModel: model.text
          });
          writeSummary(config, input, { ...checkpoint, notFound, completed: [...completed], failed: [...failed] });

          console.log(`已复制：${manufacturer.text} / ${model.text}`);
        } catch (error) {
          if (isBrowserClosedError(error)) throw error;

          failed.add(key);
          saveCheckpoint(config, checkpoint, completed, failed, notFound, {
            currentManufacturer: manufacturer.text,
            currentModel: model.text,
            lastError: `${manufacturer.text} / ${model.text}: ${error.message}`
          });
          writeSummary(config, input, { ...checkpoint, notFound, completed: [...completed], failed: [...failed] });
          console.log(`跳过失败：${manufacturer.text} / ${model.text}，原因：${error.message}`);
        }
      }
    }

    saveCheckpoint(config, checkpoint, completed, failed, notFound, { completedAt: new Date().toISOString() });
    writeSummary(config, input, { ...checkpoint, notFound, completed: [...completed], failed: [...failed] });
    console.log(`完成：${completed.size} 个组合，输出 ${config.tsvMarkdownFile}`);
    console.log(`Summary：${config.tsvSummaryFile}`);
  } finally {
    await context.close().catch(() => {});
  }
}

function parseInputTsv(file) {
  if (!fs.existsSync(file)) {
    throw new Error(`找不到 TSV 文件：${file}`);
  }

  const raw = fs.readFileSync(file, "utf8").replace(/^\uFEFF/, "");
  const lines = raw.split(/\r?\n/).filter((line) => line.trim());
  if (!lines.length) throw new Error(`TSV 文件为空：${file}`);

  const first = splitTsvLine(lines[0]);
  const normalizedHeader = first.map(normalizeHeader);
  const hasHeader = normalizedHeader.some((name) => ["make", "model"].includes(name));

  const makeIndex = hasHeader ? normalizedHeader.findIndex((name) => name === "make") : 0;
  const modelIndex = hasHeader ? normalizedHeader.findIndex((name) => name === "model") : 1;
  if (makeIndex < 0) throw new Error("TSV 需要包含品牌列：make / brand / manufacturer / 品牌");

  const dataLines = hasHeader ? lines.slice(1) : lines;
  const entries = [];
  const seen = new Set();

  for (const line of dataLines) {
    const cells = splitTsvLine(line);
    const make = (cells[makeIndex] ?? "").trim();
    const model = modelIndex >= 0 ? (cells[modelIndex] ?? "").trim() : "";
    if (!make) continue;

    const key = `${normalizeText(make)}\t${normalizeText(model)}`;
    if (seen.has(key)) continue;
    seen.add(key);
    entries.push({ make, model });
  }

  return {
    file,
    hasModelColumn: modelIndex >= 0,
    entries
  };
}

function splitTsvLine(line) {
  return line.split("\t").map((cell) => cell.trim());
}

function normalizeHeader(value) {
  const text = String(value ?? "").trim().toLowerCase().replaceAll(" ", "").replaceAll("_", "");
  if (["make", "brand", "manufacturer", "manufacture", "品牌", "制造商", "厂商"].includes(text)) return "make";
  if (["model", "车型", "车系"].includes(text)) return "model";
  return text;
}

function findOption(options, expected) {
  const target = normalizeText(expected);
  return options.find((option) => normalizeText(option.text) === target)
    || options.find((option) => normalizeText(option.value) === target)
    || null;
}

function normalizeText(value) {
  return String(value ?? "").trim().replace(/\s+/g, " ").toLowerCase();
}

function recordNotFound(notFound, item) {
  const key = `${item.make}\t${item.model ?? ""}\t${item.reason}`;
  if (notFound.some((existing) => `${existing.make}\t${existing.model ?? ""}\t${existing.reason}` === key)) return;
  notFound.push({ ...item, at: new Date().toISOString() });
}

function rowKey(manufacturer, model) {
  return `${manufacturer}\t${model}`;
}

function saveCheckpoint(config, checkpoint, completed, failed, notFound, extra = {}) {
  writeJson(config.tsvCheckpointFile, {
    modelsByManufacturer: checkpoint.modelsByManufacturer ?? {},
    completed: [...completed],
    failed: [...failed],
    notFound,
    updatedAt: new Date().toISOString(),
    ...extra
  });
}

function ensureMarkdownHeader(config, input) {
  fs.mkdirSync(path.dirname(config.tsvMarkdownFile), { recursive: true });
  if (fs.existsSync(config.tsvMarkdownFile)) return;

  fs.writeFileSync(
    config.tsvMarkdownFile,
    [
      "# 4AFitment TSV Copied Vehicle Data",
      "",
      `Input: ${input.file}`,
      `Year range: ${config.yearRange.from} - ${config.yearRange.to}`,
      `Generated at: ${new Date().toISOString()}`,
      ""
    ].join("\n"),
    "utf8"
  );
}

function appendMarkdownSection(config, { manufacturer, model, content }) {
  const safeContent = String(content || "").replaceAll("```", "`\\`\\`");
  const block = [
    "",
    `## ${manufacturer} / ${model}`,
    "",
    `- Year range: ${config.yearRange.from} - ${config.yearRange.to}`,
    `- Copied at: ${new Date().toISOString()}`,
    "",
    "```text",
    safeContent.trim(),
    "```",
    ""
  ].join("\n");

  fs.appendFileSync(config.tsvMarkdownFile, block, "utf8");
}

function writeSummary(config, input, checkpoint) {
  fs.mkdirSync(path.dirname(config.tsvSummaryFile), { recursive: true });
  const notFound = checkpoint.notFound ?? [];
  const failed = checkpoint.failed ?? [];
  const completed = checkpoint.completed ?? [];

  const lines = [
    "# 4AFitment TSV Summary",
    "",
    `Input: ${input.file}`,
    `Input rows: ${input.entries.length}`,
    `Completed combinations: ${completed.length}`,
    `Failed combinations: ${failed.length}`,
    `Not found rows: ${notFound.length}`,
    `Updated at: ${new Date().toISOString()}`,
    ""
  ];

  if (notFound.length) {
    lines.push("## Not Found", "");
    for (const item of notFound) {
      lines.push(`- ${item.make}${item.model ? ` / ${item.model}` : ""}: ${item.reason}`);
    }
    lines.push("");
  }

  if (failed.length) {
    lines.push("## Failed", "");
    for (const item of failed) lines.push(`- ${item}`);
    lines.push("");
  }

  fs.writeFileSync(config.tsvSummaryFile, `${lines.join("\n")}\n`, "utf8");
}

async function readClipboardText(page) {
  const fromBrowser = await page.evaluate(async () => {
    try {
      return await navigator.clipboard.readText();
    } catch {
      return "";
    }
  }).catch(() => "");

  if (fromBrowser) return fromBrowser;

  return execFileSync("powershell.exe", ["-NoProfile", "-Command", "Get-Clipboard -Raw"], {
    encoding: "utf8"
  });
}

function assertPageOpen(page) {
  if (page.isClosed()) throw new Error("Target page, context or browser has been closed");
}

function isBrowserClosedError(error) {
  return /target page, context or browser has been closed|browser has been closed|page has been closed/i.test(error?.message ?? "");
}
