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
$InputDir = Join-Path $ProjectRoot "input_sheets"
$OutputDir = Join-Path $ProjectRoot "output_sheets"
$LogPath = Join-Path $ProjectRoot "log.csv"
$SummaryPath = Join-Path $ProjectRoot "summary.txt"
$RequirementPath = Join-Path $ProjectRoot "requirement.md"
```

运行当前版本：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File $ScriptPath `
  -InputDir $InputDir `
  -OutputDir $OutputDir `
  -LogPath $LogPath `
  -SummaryPath $SummaryPath `
  -RequirementPath $RequirementPath
```

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

# 使用批处理并透传参数
```powershell
.\run_automation.bat -MaxRounds 80
```

# 直接使用 PowerShell 命令并透传参数 80 作为轮次上限
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\qclaw_fitment_automation.ps1" -MaxRounds 80
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
- `--chunk-size`：每个拆分文件包含的行数
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
python .\merge_final_round_results.py
```

默认路径：

- `--origin-dir`：`.\input_sheets`
- `--results-dir`：`.\output_sheets`
- `--output-dir`：`.\output_merged`
- `--log-dir`：`.\output_merged`

脚本行为说明：

- 按 `origin-dir` 下的 `*.tsv` 分片顺序逐个处理
- 每个分片会在 `results-dir` 中查找同名结果文件，优先选择最新版本，例如 `xxx_result_2.md` 会覆盖 `xxx_result.md`
- 每个结果文件只提取最后一个有效 Round 里的 TSV 数据
- 默认输出文件名取 `origin-dir` 中第一个 TSV 的文件名，去掉结尾的 `_part_n` 后再拼接后缀
- 例如第一个输入文件是 `待补强_part_27.tsv`，则默认输出 `待补强_merged.tsv` 和 `待补强_merged.log`
- 输出 TSV 时会在每行前面补一列来源文件名
- 默认会写入表头；如果不需要表头，可以加 `--no-header`
- 同时生成 `.log` 文件，记录 `MERGED`、`MISSING`、`NO_ROUND`、`EMPTY_ROUND` 等状态

常用示例：

```powershell
# 使用默认目录合并
python .\merge_final_round_results.py

# 指定输入和输出目录
python .\merge_final_round_results.py `
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


powershell -NoProfile -ExecutionPolicy Bypass -File ".\qclaw_fitment_automation.ps1" -MaxRounds 100 --input_dir .\projects\0604补强\input\ -output_dir .\projects\0604补强\output 