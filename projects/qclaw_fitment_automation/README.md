# QClaw Fitment Automation

以下命令默认在 PowerShell 中执行。

## 项目结构

```text
qclaw_fitment_automation/
├── src/                         # Python 命令行工具与配置加载代码
├── tests/                       # 不依赖浏览器的 smoke tests
├── requirements/                # 不同数据源/任务的 requirement
├── workspaces/                  # 各批次输入、输出、检查点和运行记录
├── config.yaml                  # 默认运行配置
├── run_from_config.ps1          # 推荐启动入口
├── run_automation.bat           # Windows 快捷入口
├── qclaw_fitment_automation.ps1 # 核心自动化脚本（兼容直接调用）
└── playwright_browser_bridge.js # Playwright 浏览器桥接
```

`src` 中的 Python 文件都是可直接执行的 CLI，不要求安装为 Python 包。

## 推荐：使用 config.yaml 工作

默认入口是 `run_from_config.ps1`，不再要求每次传 `-Project`。它默认读取同目录的 `config.yaml`，且未指定模式时使用 `mode: work`。

正式工作：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\run_from_config.ps1"
```

只检查配置、目录和当前浏览器页面控制，不发送消息：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\run_from_config.ps1" -Mode check
```

只显示将要遍历的项目：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\run_from_config.ps1" -Mode dry_run
```

使用另一份配置：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\run_from_config.ps1" -ConfigPath ".\configs\production.yaml"
```

`config.yaml` 分为以下几部分：

- `mode`：`work`、`check` 或 `dry_run`，默认 `work`
- `workspace.traversal`：选择 `directories`、`glob` 或 `explicit` 遍历方式，并可设置包含、排除、排序及最大项目数
- `project_layout`：定义每个工作目录里的 `input`、`output`、日志和汇总文件位置
- `runtime`：定义最大轮数、最长回复等待时间、浏览器、失败后是否继续以及只处理哪些 TSV
- `runtime.max_reply_wait_seconds`：等待单轮回复完成的最长时间，单位为秒；默认 `900`
- `runtime.input_sources`：组合指定目录遍历与指定文件，合并后自动去重
- `runtime.processing`：选择 `row`（逐行独立对话）或 `file`（整文件独立对话）
- `runtime.input_files.skip_processed`：是否跳过日志中已成功的整文件任务
- `data_contract.requirement`：requirement 文件地址；相对路径按 config.yaml 所在目录解析，也可以写绝对路径

全量表固定字段、自动留空字段、附加提示约束及是否输出子车系匹配表，只在 requirement
文件的 `<!-- fitment-data-contract ... -->` 区块中配置，不要在
`config.yaml` 中重复设置。字段定义重复出现在 config 时会直接报错，防止两处配置漂移。

遍历示例：

```yaml
workspace:
  root: ./workspaces
  traversal:
    strategy: glob
    include: ["0610-*", "production-*"]
    exclude: ["*.disabled", "_*"]
    order: name_asc
    max_projects: 0
```

`run_automation.bat` 也已经改为使用 `config.yaml`。命令行直接运行旧的 `qclaw_fitment_automation.ps1 -Project ...` 仍然兼容。

## 配置输入遍历和对话粒度

`input_sources.directories` 与 `input_sources.files` 可以同时配置。目录条目支持独立
通配符和递归开关；文件条目用于精确加入单个 TSV。一个文件若同时由目录和文件条目
命中，只处理一次。相对路径以当前项目目录为基准。

```yaml
runtime:
  conversation:
    mode: new

  input_sources:
    directories:
      - path: input
        pattern: "*.tsv"
        recursive: false
      - path: imported
        pattern: "production-*.tsv"
        recursive: true
    files:
      - special/manual.tsv
      - D:\shared\one-off.tsv
    order: name_asc

  processing:
    mode: row
    row_label_columns: [MAKE, MODEL]
    checkpoint_dir: checkpoints
```

处理模式：

- `mode: row`：跳过表头和空行，每个数据行携带原表头，分别打开一个全新 ChatGPT
  对话。`row_label_columns` 只控制任务名称；不配置时使用“文件名 + 行号”。
- `mode: file`：每个最终选中的完整 TSV 文件打开一个全新 ChatGPT 对话。

两种模式都为每个独立任务保留输出文本和 checkpoint：

```text
<项目>/
├── output/
│   ├── list__row__chevrolet-astro__<稳定哈希>_result.md
│   └── full_result.md
├── checkpoints/
│   ├── list__row__chevrolet-astro__<稳定哈希>.json
│   └── full.json
├── log.csv
└── summary.txt
```

每轮回复都会先追加到该任务的 Markdown 文本，再更新 JSON checkpoint。checkpoint
记录任务状态、轮次、发送次数、输出文件、当前 ChatGPT 对话 URL 和对话分支链。
脚本重启后会跳过已经成功的任务；未完成任务若已取得对话 URL，则自动打开当前分支，
从断点继续。全部任务遍历结束后，`summary.txt` 汇总最终状态。逐行模式下
`conversation.mode` 必须为 `new`，历史对话续跑由 checkpoint 负责。

### 对话长度上限与自动分支

检测到 ChatGPT 提示当前对话达到最大长度后，脚本会自动：

1. 从最后一条用户消息执行“在新聊天中分支”。
2. 等待 ChatGPT 生成不同于父对话的新 `/c/...` URL。
3. 立即把父对话、新分支、触发轮次和创建时间写入任务 checkpoint。
4. 在新分支继续等待当前轮回复；脚本重启后也会恢复最新分支。

checkpoint 使用 `version: 2`，其中 `conversation_url` 指向当前分支，
`conversation_lineage` 按顺序记录根对话和所有后续分支，
`conversation_branch_count` 记录已创建的分支数量。结果 Markdown 中也会追加
“对话分支”段落，便于人工审计。如果页面没有提供“在新聊天中分支”入口，脚本会
明确报错并保留原 checkpoint，不会静默创建一个丢失上下文的空白聊天。

只预览最终选中的文件和拆分后的任务，不打开浏览器：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\run_from_config.ps1" `
  -ConfigPath ".\workspaces\0723-chevyadd\config.yaml" -Mode dry_run
```

旧的 `runtime.input_files.pattern/order` 和 `runtime.vehicle_iteration` 仍兼容；新配置
建议使用 `input_sources + processing`。

## 同尺寸 key 复用代表年份

`data_contract.dimension_representative` 用于减少同一代际、同一物理配置的重复尺寸
查询。完整 key 中任一字段不同都视为不同尺寸组。只有跨年份证据通过离群检查后，
才允许选择一个资料充分的代表年份，将其真实尺寸用于已经验证的年份范围。

```yaml
data_contract:
  dimension_representative:
    enabled: true
    key_columns: [MAKE, MODEL, 版本, CAB, BED, 代际]
    year_column: YEAR
    dimension_columns: [L-IN, W-IN, H-IN]
    minimum_comparison_years: 2

    outlier:
      # absolute_or_relative：绝对差或相对差任一超限即为 outlier。
      comparison_rule: absolute_or_relative
      max_absolute_difference:
        L-IN: 4.0
        W-IN: 2.0
        H-IN: 2.0
      max_relative_difference_percent: 3.0

    representative_year:
      strategy: best_documented

    audit_columns: [参考车型, 备注]
```

启用后的强制流程：

1. 只在完整尺寸 key 相同且代际相同的记录之间比较。
2. 至少取得配置数量的不同年份证据，并尽量覆盖首年、末年和中期改款点。
3. 对每个尺寸计算可靠样本的 `max - min` spread。
4. 任一尺寸越过配置阈值，或存在车身、版本、CAB、BED、轴距/结构变化，就禁止
   整段复用，并按变化边界拆分或继续核实。
5. 无 outlier 时选择资料最完整、来源最可靠且容易查证的一年作为代表年。使用该年
   的真实尺寸，不对多个年份求平均。
6. 在 `audit_columns` 中记录尺寸 key、代表年份、验证范围、各尺寸 spread、阈值结论
   和来源。证据不足或来源冲突时禁止复用和完成。

示例中的 `4 / 2 / 2 英寸 + 3%` 是当前 US 批次采用的可配置阈值，不是写死在程序
中的全局标准。启用时，key、年份、尺寸和审计字段都必须存在于 requirement 定义的
全量表中，配置加载阶段会直接拦截拼写错误、缺失阈值和自动留空尺寸字段。

## 进入项目目录

```powershell
$ProjectRoot = "D:\Home\Scripts\fitment_sheet_generation\projects\qclaw_fitment_automation"
Set-Location $ProjectRoot
```

## 运行浏览器自动化

### 推荐：Playwright 测试 Chromium

DOM 读取默认改为 Playwright 持久化 Chromium。Playwright 会等待页面 DOM 挂载，并在
React 导航导致 execution context 重建时自动重试；登录状态保存在独立 profile 中。

首次安装：

```powershell
Set-Location .\projects\qclaw_fitment_automation
npm install
npx playwright install chromium
```

`config.yaml` 中使用：

```yaml
runtime:
  browser: playwright
  playwright_profile_path: ""
  playwright_executable_path: ""
```

留空时，profile 默认保存在
`%LOCALAPPDATA%\qclaw-fitment-automation\playwright-profile`，首次打开后需在该
Chromium 窗口登录 ChatGPT。`playwright_executable_path` 留空时使用 Playwright
配套 Chromium。若要临时切回原来的浏览器控制方式，将 `browser` 改为 `openclaw`。

先运行检查模式完成登录和 DOM 自检。未登录时脚本不会计时退出；完成登录后，
回到 PowerShell 按 Enter 重新验证：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\run_from_config.ps1" -Mode check
```

如果 Google 拒绝在受自动化控制的浏览器中登录，检查脚本会自动关闭 Playwright
窗口，并用普通 Chrome/Edge 打开同一个独立 profile。完成登录、确认 ChatGPT 输入框
可用并关闭普通浏览器后，回到 PowerShell 按 Enter；脚本会重新启动 Playwright 验证。

也可以手动执行同样的 profile 初始化。例如本机 Edge：

```powershell
$ProfilePath = Join-Path $env:LOCALAPPDATA "qclaw-fitment-automation\playwright-profile"
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" `
  "--user-data-dir=$ProfilePath" "https://chatgpt.com/"
```

Playwright 会复用该 profile 中已建立的 ChatGPT 会话，无需自动化 Google 登录。

### 手动选择旧对话并存档续跑

在项目配置的 `runtime` 下设置：

```yaml
conversation:
  mode: manual_resume
  archive_code: 0723-chevyadd
  archive_path: conversation_archives.json
```

正式运行后，脚本会暂停，请在 ChatGPT 历史记录中手动选中要继续的对话；
页面加载完成后回到 PowerShell 按 Enter。脚本会：

- 将当前对话 URL 记录到 `conversation_archives.json`
- 不新建对话，也不重发首轮 requirement 和原始 TSV
- 直接发送“继续补强当前批次”
- 将新结果以 `Round 1 / 存档续跑` 开始写入新的结果文件

以后不再手动选择时，将模式改成：

```yaml
conversation:
  mode: archive_resume
  archive_code: 0723-chevyadd
  archive_path: conversation_archives.json
```

脚本会按存档码自动打开已记录的对话。`mode: new` 保持原行为，每个 TSV
新建对话并发送完整首轮任务。

### 备选：OpenClaw browser control

若将 `runtime.browser` 改为 `openclaw`，当前版本不依赖 QClaw 安装目录中的
`xb.cjs`，而是使用本机已经部署的 OpenClaw。请先确认以下命令可用：

```powershell
openclaw --version
```

脚本会读取 `%USERPROFILE%\.openclaw\openclaw.json`，并在需要时自动启动本机 Gateway 和 browser control 服务。第一次使用前，OpenClaw 配置需要启用 `browser.enabled` 和 browser 插件；ChatGPT 登录状态保存在 OpenClaw 自己的浏览器配置中。

设置当前版本使用的路径参数：

```powershell
$ScriptPath = Join-Path $ProjectRoot "qclaw_fitment_automation.ps1"
$WorkProject = Join-Path $ProjectRoot "workspaces\0610"
$RequirementPath = Join-Path $ProjectRoot "requirements\eu_autodata.md"
```

运行当前版本：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File $ScriptPath `
  -Project $WorkProject `
  -RequirementPath $RequirementPath
```

`-Project` 会把未显式指定的路径默认到项目目录下：

- 输入目录：`<Project>\input`
- 输出目录：`<Project>\output`
- 日志文件：`<Project>\log.csv`
- 汇总文件：`<Project>\summary.txt`

也可以继续用 `-InputDir`、`-OutputDir`、`-LogPath`、`-SummaryPath` 单独覆盖。脚本同时兼容 `--input_dir`、`--output_dir`、`--log-path`、`--summary-path` 这类写法。

当前完成判定规则：

- 只要最后一轮回复明确出现 `本批次完成` 一类完成信号，就记为完成
- 如果同一轮同时带有更新后的完整 TSV，会在日志里额外记为“包含完整表”
- 不再因为年份参考覆盖不足、仍有 `待补强` / `待终核` 字样，或最后一步未附完整 TSV 而单独拦截完成判定

只打开 ChatGPT 页面，不开始批量处理：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File $ScriptPath -OpenOnly
```

成功时会显示当前后端的页面控制验证结果。如果 ChatGPT 尚未登录，在打开的浏览器中完成登录，再运行正式命令。

可选的 OpenClaw 连接参数：

- `-OpenClawCommand`：OpenClaw 命令路径，默认自动查找 `openclaw.cmd` / `openclaw`
- `-OpenClawConfigPath`：配置文件路径，默认 `%USERPROFILE%\.openclaw\openclaw.json`
- `-OpenClawGatewayUrl`：Gateway 地址，默认按配置端口使用本机地址
- `-OpenClawBrowserUrl`：browser control 地址，默认是 Gateway 端口加 2

### 只打开 ChatGPT 页面，不开始批量处理

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\qclaw_fitment_automation.ps1" -OpenOnly
```

### 直接运行当前版本进行批量处理

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\qclaw_fitment_automation.ps1"
```

### 指定更高的轮次上限

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\qclaw_fitment_automation.ps1" -MaxRounds 80
```

### 使用项目目录默认路径

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\qclaw_fitment_automation.ps1" -Project .\workspaces\0610 -MaxRounds 150
```

### 使用批处理并透传参数

```powershell
.\run_automation.bat -MaxRounds 80
```

### 直接使用 PowerShell 命令并透传参数 80 作为轮次上限

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\qclaw_fitment_automation.ps1" -MaxRounds 80
```

## 对话自动续跑

手动首轮后持续发送“下一步”的工具已经拆分到相邻的 `..\auto_next_until_done` 子项目，使用方法见其 README。

## 拆分原始 TSV

使用 `src\split_origin_tsv.py` 可以把一个 TSV 按固定行数拆成多个 `split` 文件。

例如，把项目根目录下的 `full.tsv` 按每份约 `20` 行拆到 `input_sheets` 目录：

```powershell
python .\src\split_origin_tsv.py --origin .\full.tsv --output-dir .\input_sheets --prefix split --chunk-size 20 --write
```

生成的文件名类似：

```text
split_part_01.tsv
split_part_02.tsv
split_part_03.tsv
```

常用参数说明：

- `--origin`：原始 TSV 文件路径
- `--output-dir`：拆分后文件的输出目录
- `--prefix`：输出文件名前缀
- `--chunk-size`：每个拆分文件包含的数据行数，原表第一行表头会自动放入每个拆分文件且不计入该数量
- `--write`：执行写入
- `--force`：如果输出目录下已有同名前缀文件，则先覆盖

如果需要覆盖已有的 `split_part_*.tsv` 文件：

```powershell
python .\src\split_origin_tsv.py --origin .\full.tsv --output-dir .\input_sheets --prefix split --chunk-size 20 --write --force
```

## 合并最终 Round 结果

使用 `src\merge_final_round_results.py` 可以从每个分片对应的最新结果 Markdown 中，提取最后一个包含 TSV 表格的 `--- Round N / 下一步 ---` 或 `--- Round N / 首次发送 ---` 段落，并合并成一个总 TSV。

最常用命令：

```powershell
python .\src\merge_final_round_results.py --project .\workspaces\0610
```

默认路径：

- 不带 `--project` 时保持旧默认：`.\input_sheets`、`.\output_sheets`、`.\output_merged`
- 带 `--project .\workspaces\0610` 时默认：
  - `--origin-dir`：`.\workspaces\0610\input`
  - `--results-dir`：`.\workspaces\0610\output`
  - `--output-dir`：`.\workspaces\0610`
  - `--log-dir`：`.\workspaces\0610`

脚本行为说明：

- 按 `origin-dir` 下的 `*.tsv` 分片顺序逐个处理
- 每个分片会在 `results-dir` 中查找同名结果文件，优先选择最新版本，例如 `xxx_result_2.md` 会覆盖 `xxx_result.md`
- 每个结果文件只提取最后一个有效 Round 里的 TSV 数据
- 合并输出统一使用新版全量表头；`对应尺码`、`排序依据车型`、`子车系`、`区间最小年份`、`区间最大年份`、`max_length_cm`、`max_width_cm`、`max_height_cm`、`长度余量`、`无尺码原因` 会保留为空
- 如果结果中包含 `Year	主车型	结构	版本	候选车型	匹配数量` 子车系匹配表，合并时会额外生成 `*_subseries_match.tsv`，其中 `匹配数量` 会保留为空
- 默认输出文件名取 `origin-dir` 中第一个 TSV 的文件名，去掉结尾的 `_part_n` 后再拼接后缀
- 例如第一个输入文件是 `待补强_part_27.tsv`，则默认输出 `待补强_merged.tsv` 和 `待补强_merged.log`
- 输出 TSV 时会在每行前面补一列来源文件名
- 默认会写入表头；如果不需要表头，可以加 `--no-header`
- 同时生成 `.log` 文件，记录 `MERGED`、`MISSING`、`NO_ROUND`、`EMPTY_ROUND` 等状态

常用示例：

```powershell
# 使用项目目录默认路径合并
python .\src\merge_final_round_results.py --project .\workspaces\0610

# 指定输入和输出目录
python .\src\merge_final_round_results.py `
  --project .\workspaces\0610 `
  --origin-dir .\input_sheets\my_batch `
  --results-dir .\output_sheets `
  --output-dir .\output_merged `
  --log-dir .\output_merged

# 显式指定输出文件路径
python .\src\merge_final_round_results.py `
  --output .\output_merged\my_batch_merged.tsv `
  --log .\output_merged\my_batch_merged.log

# 不写表头
python .\src\merge_final_round_results.py --no-header
```

powershell -NoProfile -ExecutionPolicy Bypass -File ".\qclaw_fitment_automation.ps1" -Project .\workspaces\0604补强 -MaxRounds 100
