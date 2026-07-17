# MotorcycleSpecs 摩托车尺寸定向采集

## 目录未收录页面与市场后缀

有些真实车型页没有出现在 MotorcycleSpecs 的品牌目录中，常规索引无法自动发现。将已确认的页面添加到 `config/manual_pages.yaml` 后，程序会在每次运行时把它合并进索引，并在 `candidate_pages.csv` 中将 `DISCOVERY_METHOD` 标记为 `MANUAL_CONFIG`。

输入中的市场或配置后缀可以加入 `config/config.yaml` 的 `matching.ignored_model_words`。例如 `equipada` 会在车型匹配时忽略，因此 `F900GS Adventure Equipada` 可以与 `BMW F 900 GS Adventure 2024` 严格匹配；原始输入值仍原样保留在所有输出中。

这两项配置只解决页面发现和名称匹配，不会补造页面没有提供的尺寸。缺少整体高度时，`H-MM` 保持为空，`PARSE_STATUS` 为 `PARTIAL`。

这是一个面向 `https://www.motorcyclespecs.co.za/` 的定向采集子项目。它按输入品牌/车型建立站内目录索引，保留同车型不同年份页面，提取长、宽、高及辅助尺寸，并输出可追溯的 CSV、Excel、SQLite 状态和运行报告。它不是整站镜像工具；匹配失败时不会自动采用“最相似”页面。

## 安装

要求 Python 3.12+。在本目录运行：

```powershell
python -m pip install -e ".[dev]"
```

Playwright 不是默认依赖。只有确认页面依赖 JavaScript 时才可另行安装 `.[browser]`；当前站点流程使用 `httpx + BeautifulSoup + lxml`。

## Python 文件说明

程序入口是 `python -m moto_dimension_crawler`，对应 `src/moto_dimension_crawler/__main__.py`。日常使用不需要逐个执行下面的 `.py` 文件，它们由 CLI 按流水线顺序调用。

| 文件 | 作用 |
| --- | --- |
| `__main__.py` | `python -m moto_dimension_crawler` 的模块入口。 |
| `cli.py` | 定义 `run`、`build-index`、`match`、`fetch`、`parse`、`summarize`、`export`、`report` 命令及参数。 |
| `pipeline.py` | 编排完整流程，连接输入、索引、匹配、抓取、解析、分组和导出。 |
| `config.py` | 读取主配置、品牌别名和车型别名 YAML。 |
| `models.py` | 定义输入记录、候选页面、尺寸结果等内部数据结构。 |
| `input_reader.py` | 读取 XLSX/CSV/TSV，处理编码、工作表、起始行和条数限制。 |
| `normalizer.py` | 车型名称标准化、紧凑名称、数字 token 和文字 token 提取。 |
| `index_builder.py` | 从站点首页和目标品牌目录建立并保存本地页面索引。 |
| `page_discovery.py` | 根据输入品牌和数字型号对本地索引进行定向预筛选。 |
| `matcher.py` | 对候选页面评分，执行品牌、数字型号和版本词硬约束。 |
| `robots.py` | 读取并执行站点 `robots.txt` 访问规则。 |
| `crawler.py` | HTTP 请求、限速、重试、robots 检查及缓存命中处理。 |
| `cache.py` | 以 URL 的 SHA-256 保存 HTML 和 JSON 元数据。 |
| `parser.py` | 清理 HTML、提取页面标题、正文、年份和尺寸区域。 |
| `dimension_parser.py` | 解析长宽高、范围值、组合尺寸、公英制和辅助尺寸。 |
| `year_parser.py` | 从标题、正文和 URL 中提取单年或明确年份范围。 |
| `scope_parser.py` | 识别后视镜、风挡、边箱等尺寸测量口径。 |
| `validator.py` | 检查合理范围及高度、座高、轴距等逻辑异常。 |
| `grouper.py` | 按车型、尺寸、口径和容差生成尺寸组。 |
| `database.py` | 管理 SQLite 任务状态、解析结果、缓存记录和错误。 |
| `exporter.py` | 生成字段顺序固定的 CSV 和多工作表 Excel。 |
| `reporter.py` | 生成 `run_report.json` 和运行数量统计。 |
| `utils.py` | UTC 时间、稳定哈希和项目路径等公共函数。 |

## 输入与运行

支持 `.xlsx`、`.csv`、`.tsv`。Excel 默认首个工作表，可用 `--sheet` 指定。分隔文件依次尝试 UTF-8-SIG、UTF-8、GB18030。默认字段为 `MAKE`、`MODEL`、`车辆类型`，可在 `config/config.yaml` 的 `input_columns` 中添加映射。原字段不被改写，`INPUT_ID` 按原数据行稳定生成。

```powershell
python -m moto_dimension_crawler run `
  --input data/input/sample.tsv `
  --output output/sample `
  --config config/config.yaml `
  --resume `
  --limit 2
```

分阶段命令为 `build-index`、`match`、`fetch`、`parse`、`summarize`、`export`、`report`。查看完整参数：

```powershell
python -m moto_dimension_crawler run --help
```

### 常用参数

| 参数 | 是否必需 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--input PATH` | `run` 必需 | 无 | 输入 XLSX、CSV 或 TSV 文件。 |
| `--output PATH` | 否 | `output/` | CSV、Excel 和运行报告输出目录。 |
| `--config PATH` | 否 | `config/config.yaml` | 主配置文件路径。别名文件从该文件所在目录读取。 |
| `--sheet NAME` | 否 | 第一个工作表 | Excel 工作表名称；CSV/TSV 忽略。 |
| `--resume / --no-resume` | 否 | `--resume` | 使用现有索引、缓存和 SQLite 进度；`--no-resume` 重新建立本次流程状态。 |
| `--force-refetch` | 否 | 关闭 | 忽略已有 HTML 缓存并重新请求页面。会增加站点访问量。 |
| `--force-reparse` | 否 | 关闭 | 重新解析页面；仍优先读取本地 HTML 缓存。解析规则修改后使用。 |
| `--limit N` | 否 | 全部 | 从起始位置最多处理 N 条，适合小批量验证。 |
| `--start-row N` | 否 | `1` | 从第 N 条数据开始，不计算表头。生成的 `INPUT_ID` 仍对应原始行位置。 |
| `--trusted-score-threshold N` | 否 | 配置值 `80` | 自动采用候选页面的匹配分数门槛，范围 0–100；严格大于门槛且通过硬约束时记为 `LIKELY` 并写入结果。 |
| `--max-concurrency N` | 否 | 配置值 `1` | 最大并发，程序强制限制为 1–2；正式运行建议 1。 |
| `--request-delay-min SEC` | 否 | 配置值 `2` | 两次请求之间随机等待的最小秒数。 |
| `--request-delay-max SEC` | 否 | 配置值 `5` | 随机等待的最大秒数，不能小于最小值。 |
| `--log-level LEVEL` | 否 | `INFO` | 控制台及日志级别，例如 `DEBUG`、`INFO`、`WARNING`、`ERROR`。 |

参数选择建议：

- 正常首次运行：使用 `--resume`，无需指定强制参数。
- 中断后继续：保持输入文件和行顺序不变，再次使用相同命令及 `--resume`。
- 修改了解析代码：添加 `--force-reparse`，避免重新下载网页。
- 怀疑缓存网页已过期：同时添加 `--force-refetch --force-reparse`。
- 先验证数据格式和匹配效果：使用 `--limit 10` 或 `--limit 50`。
- 分批运行：组合使用 `--start-row` 和 `--limit`，例如从第 501 条开始处理 500 条。

### 分阶段命令

| 命令 | 执行到的阶段 | 典型用途 |
| --- | --- | --- |
| `build-index` | 建立品牌页面索引 | 先检查站内目录能否正常访问。 |
| `match` | 输入规范化和候选评分 | 不抓车型详情页，先审查匹配质量。 |
| `fetch` | 下载可信候选页 | 预先填充 HTML 缓存。 |
| `parse` | 解析缓存或新下载页面 | 检查尺寸解析结果。 |
| `summarize` | 生成尺寸组 | 检查跨年份分组情况。 |
| `export` | 执行并导出全部结果 | 与完整流水线结果相同。 |
| `run` | 执行完整流水线 | 日常推荐入口，参数最完整。 |
| `report` | 读取已有运行报告 | 不抓取、不解析，仅显示 `run_report.json`。 |

示例：

```powershell
# 指定 Excel 工作表，只测试第 101～150 条
python -m moto_dimension_crawler run `
  --input data/input/motorcycles.xlsx `
  --sheet Sheet1 `
  --start-row 101 `
  --limit 50 `
  --output output/check_101_150

# 解析代码更新后，使用缓存重新解析并输出调试日志
python -m moto_dimension_crawler run `
  --input data/input/motorcycles.xlsx `
  --output output/production `
  --resume `
  --force-reparse `
  --log-level DEBUG

# 查看最近一次报告
python -m moto_dimension_crawler report --output output/production
```

常用控制：

```powershell
# 只运行前 50 条
python -m moto_dimension_crawler run --input data/input/motorcycles.xlsx --limit 50

# 从第 501 条数据开始（首条数据为 1，不含表头）
python -m moto_dimension_crawler run --input data/input/motorcycles.xlsx --start-row 501

# 不重新下载，只重新解析已缓存页面
python -m moto_dimension_crawler run --input data/input/motorcycles.xlsx --force-reparse

# 明确要求重新下载和重新解析
python -m moto_dimension_crawler run --input data/input/motorcycles.xlsx --force-refetch --force-reparse
```

正式运行约 3000 条数据：

```powershell
python -m moto_dimension_crawler run `
  --input data/input/motorcycles.xlsx `
  --output output/production `
  --config config/config.yaml `
  --resume `
  --max-concurrency 1
```

## 名称匹配

名称先做 Unicode NFKC、小写、标点统一、空白合并和字母/数字边界切分，并保留无空格比较值。匹配采用品牌、标准化车型、主要数字 token、关键词和版本词的组合评分。品牌不符最高 40 分；主要数字不符最高 65 分；`GT`/`X`、`Adventure Sports` 等版本冲突不得为 `EXACT`。多个高分候选差小于配置阈值时标记 `MULTIPLE` 并全部保留。`REVIEW` 页面只进入候选/复核数据，不会自动作为尺寸来源。

候选输出同时提供 `MODEL_SIMILARITY`（0–100 模糊相似度）、`MATCH_SCORE`（综合置信分）和 `MATCH_CONFIDENCE`（`HIGH`、`MEDIUM`、`LOW`）。`matching.trusted_score_threshold` 默认是 `80`，也可用 `--trusted-score-threshold` 临时覆盖；综合分严格大于门槛且通过硬约束的候选记为 `LIKELY`，可以自动写入长宽高结果。参数为 `80` 时采用 81–100 分，若要包含 80 分可传 `79`。`EXACT` 仍表示完全一致。品牌、主要数字、首段字母型号、字母 token 和版本 token 仍属于硬约束，不会仅凭模糊高分绕过。

品牌和市场别名分别维护在 `config/brand_aliases.yaml`、`config/model_aliases.yaml`。普通空格、连字符和字母数字边界差异无需配置；只为真实市场名、历史名或特殊别名增加条目。

## 尺寸解析与校验

解析器按字段语义读取表格、定义列表和普通文本，支持：单值、范围、`L x W x H`、公制与英制。标准单位为毫米：`1 cm = 10 mm`、`1 in = 25.4 mm`。换算值保留一位小数，不人为凑整。范围同时写入 MIN/MAX；兼容单值字段 `L-MM`、`W-MM`、`H-MM` 使用 MAX。原始文本保存在 `L_RAW`、`W_RAW`、`H_RAW`、`UNIT_RAW`、`DIMENSION_RAW`。

宽度/高度口径只依据页面明确文字写入，例如 `WITH_MIRRORS`、`WITHOUT_MIRRORS`、`ADJUSTABLE_WINDSCREEN`；未说明时必须为 `UNKNOWN`。异常值不删除、不自动修复，而是保留原值并写入 `ANOMALY_FLAGS` 和复核表。

`PARSE_STATUS` 使用 `COMPLETE`、`PARTIAL`、`NO_DIMENSION`、`MULTIPLE_DIMENSION_SETS`、`UNIT_CONFLICT`、`INVALID_VALUE`、`PARSE_FAILED`、`FETCH_FAILED`。缺字段保持为空。

## 缓存、断点续传与访问纪律

成功 HTML 和 JSON 元数据按 URL 的 SHA-256 分别写入 `data/cache/html`、`data/cache/metadata`；状态即时写入 `data/checkpoints/state.sqlite3`。默认 `--resume`：有效缓存不重新下载，已解析的输入/URL 对不重复解析。`--force-reparse` 只重解析缓存；`--force-refetch` 才重新访问页面。

程序读取并遵守 `robots.txt`，默认单并发、请求间隔 2–5 秒，最多允许并发 2。只对 429、500、502、503、504 和临时网络错误退避重试；不绕过验证码、登录或访问限制，不下载图片和视频。请在正式运行前把 `site.user_agent` 改为带真实联系方式的标识。

常见故障：持续 403/429 时停止任务并稍后恢复；网络失败会成为 `FETCH_FAILED`；站点结构变化导致尺寸区无法识别时进入 `PARSE_FAILED`/`NO_DIMENSION`；编码或字段错误会在输入阶段明确报错。详细日志见 `logs/crawler.log` 和 `logs/errors.log`。

## 输出

输出目录包含：

- `fitment_dimensions.csv`：与输入一一对应的一行一车型视图，优先展示最佳可信来源的 `L-MM`、`W-MM`、`H-MM`、匹配置信度和来源 URL。
- `input_normalized.csv`：原始输入与规范化 token。
- `candidate_pages.csv`：全部候选、评分、状态和发现方式。
- `dimensions_raw.csv`：每个可信输入/来源页的原始尺寸、毫米值、年份、URL、哈希和状态。
- `dimensions_summary.csv`：在车型、版本、口径、附件状态一致且尺寸容差内的尺寸组；非连续年份保留为 `YEARS` 列表，不伪造连续范围。
- `review_needed.csv`：不确定匹配、缺失尺寸、未知年份、抓取/解析失败和异常。
- `not_found.csv`：完全没有可信候选的输入。
- 默认只生成 CSV 和 `run_report.json`，不再生成 XLSX。`fitment_dimensions.csv` 用于按原始输入逐行查看可信长宽高；`dimensions_raw.csv` 保留全部可信年份来源。
- `run_report.json`：数量、缓存、匹配、解析、分组和错误统计。

## 测试与当前样例

测试只使用本地 HTML fixture，不访问真实站点：

```powershell
python -m pytest -q
```

2026-07-17 已完成真实站点样例验证：识别 `BMW C Evolution 2017`，并分别保留 `BMW C 400 GT` 的 2019、2021、2025 页面；`C 400 X` 仅保留为低分复核候选，没有进入尺寸结果。样例生成了 4 条可信页面明细、4 个严格口径尺寸组、全部 CSV 和 Excel。强制重解析的第二次运行下载数为 0、缓存命中 4。

## 已知限制

- 站点目录的链接标题可能只给车型而不含完整版本，低分候选仍需人工复核。
- 两位年份只在页面正文能找到明确四位年份时采用，不根据相邻页面推测。
- 当前不启用外部搜索 API，也不抓取搜索引擎结果；目录未收录的页面可能标记为 `NOT_FOUND`。
- 多个尺寸组合、同一字段多组公英制冲突的进一步语义消歧仍需人工复核。
- SQLite 状态库由本子项目共享；正式批次应使用稳定输入顺序，避免在同一状态库中并行启动多个进程。
