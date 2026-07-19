# Auto Next Until Done

这是独立的 ChatGPT 对话自动续跑工具。它等待当前回复稳定，在未发现完成信号时发送 `下一步`，直到任务完成或达到轮数上限。

本工具复用相邻 `qclaw_fitment_automation` 子项目中的 OpenClaw 浏览器控制函数，因此两个子项目必须保持当前的同级目录关系。

从本目录运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\auto_next_until_done.ps1"
```

脚本打开 ChatGPT 后，先在页面中手动发送初始 prompt，再回到 PowerShell 按 Enter。运行记录默认写入本目录的 `transcripts\auto_next_transcript_*.md`。

常用参数：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\auto_next_until_done.ps1" -MaxNextSteps 200
powershell -NoProfile -ExecutionPolicy Bypass -File ".\auto_next_until_done.ps1" -NextMessage "继续补强当前批次"
```
