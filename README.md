# Fitment Sheet Generation

仓库按职责拆分为三个互相独立的子项目：

```text
projects/
├── motorcycle_specs/            # 摩托车规格抓取、标准化与导出
├── auto_next_until_done/         # 对话“下一步”自动续跑工具
└── qclaw_fitment_automation/     # QClaw/OpenClaw 适配表自动化主项目
    ├── workspaces/               # 各批次输入、输出和日志
    ├── requirements/             # 数据要求
    └── archive/                  # 历史备份
```

各子项目的安装、配置和运行方法见其自己的 README：

- [摩托车规格](projects/motorcycle_specs/README.md)
- [自动续跑](projects/auto_next_until_done/README.md)
- [QClaw 适配自动化](projects/qclaw_fitment_automation/README.md)

从仓库根目录进入对应项目后再执行命令。例如：

```powershell
Set-Location .\projects\qclaw_fitment_automation
.\run_automation.bat
```
