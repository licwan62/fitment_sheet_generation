# Command Demo

以下命令默认在 PowerShell 中执行。

## 进入项目目录

```powershell
$ProjectRoot = "D:\Home\Scripts\fitment_sheet_generation"
Set-Location $ProjectRoot
```

## 运行 QClaw / xbrowser 自动化

设置当前版本使用的路径参数：

```powershell
$ScriptPath = Join-Path $ProjectRoot "qclaw_fitment_automation.ps1"
$WorkProject = Join-Path $ProjectRoot "projects\0610"
$RequirementPath = Join-Path $ProjectRoot "requirement.md"
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

# 只打开 ChatGPT 页面，不开始批量处理：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\qclaw_fitment_automation.ps1" -OpenOnly
```

# 直接运行当前版本进行批量处理

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\qclaw_fitment_automation.ps1"
```

# 指定更高的轮次上限

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\qclaw_fitment_automation.ps1" -MaxRounds 80
```

# 使用项目目录默认路径

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\qclaw_fitment_automation.ps1" -Project .\projects\0610 -MaxRounds 150
```

# 使用批处理并透传参数

```powershell
.\run_automation.bat -MaxRounds 80
```

# 直接使用 PowerShell 命令并透传参数 80 作为轮次上限

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\qclaw_fitment_automation.ps1" -MaxRounds 80
```

## 手动首轮后自动发送下一步

先打开脚本：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\auto_next_until_done.ps1"
```

脚本打开 ChatGPT 后，先在页面里手动写完并发送初始 prompt；确认已经发出后，回到 PowerShell 窗口按 Enter。之后脚本会等待每轮回复稳定，未检测到完成信号就继续发送 `下一步`，直到出现 `本批次完成`、`全部完成`、`可入库全量表` 等完成信号，或达到 `-MaxNextSteps` 上限。

自动下一步的记录文件默认保存在 `transcripts\auto_next_transcript_*.md`。

常用参数：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\auto_next_until_done.ps1" -MaxNextSteps 200
powershell -NoProfile -ExecutionPolicy Bypass -File ".\auto_next_until_done.ps1" -NextMessage "继续补强当前批次"
```

## 拆分原始 TSV

使用 `split_origin_tsv.py` 可以把一个 TSV 按固定行数拆成多个 `split` 文件。

例如，把项目根目录下的 `full.tsv` 按每份约 `20` 行拆到 `input_sheets` 目录：

```powershell
python .\split_origin_tsv.py --origin .\full.tsv --output-dir .\input_sheets --prefix split --chunk-size 20 --write
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
python .\split_origin_tsv.py --origin .\full.tsv --output-dir .\input_sheets --prefix split --chunk-size 20 --write --force
```

## 合并最终 Round 结果

使用 `merge_final_round_results.py` 可以从每个分片对应的最新结果 Markdown 中，提取最后一个包含 TSV 表格的 `--- Round N / 下一步 ---` 或 `--- Round N / 首次发送 ---` 段落，并合并成一个总 TSV。

最常用命令：

```powershell
python .\merge_final_round_results.py --project .\projects\0610
```

默认路径：

- 不带 `--project` 时保持旧默认：`.\input_sheets`、`.\output_sheets`、`.\output_merged`
- 带 `--project .\projects\0610` 时默认：
  - `--origin-dir`：`.\projects\0610\input`
  - `--results-dir`：`.\projects\0610\output`
  - `--output-dir`：`.\projects\0610`
  - `--log-dir`：`.\projects\0610`

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
python .\merge_final_round_results.py --project .\projects\0610

# 指定输入和输出目录
python .\merge_final_round_results.py `
  --project .\projects\0610 `
  --origin-dir .\input_sheets\my_batch `
  --results-dir .\output_sheets `
  --output-dir .\output_merged `
  --log-dir .\output_merged

# 显式指定输出文件路径
python .\merge_final_round_results.py `
  --output .\output_merged\my_batch_merged.tsv `
  --log .\output_merged\my_batch_merged.log

# 不写表头
python .\merge_final_round_results.py --no-header
```

powershell -NoProfile -ExecutionPolicy Bypass -File ".\qclaw_fitment_automation.ps1" -Project .\projects\0604补强 -MaxRounds 100
