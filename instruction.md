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

只打开 ChatGPT 页面，不开始批量处理：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File $ScriptPath -OpenOnly
```

## 查看进度和结果

查看最近 20 条日志：

```powershell
Get-Content .\log.csv -Tail 20
```

查看汇总：

```powershell
Get-Content .\summary.txt
```

列出输出结果文件：

```powershell
Get-ChildItem .\output_sheets -Filter "*_result*.md" | Sort-Object LastWriteTime -Descending
```
