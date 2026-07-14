# Fitment Agent

车型全量表补强 Agent —— 非技术团队成员只需编辑两个 YAML 文件即可驱动 LLM 完成车辆数据补强。

## 快速开始

### 1. 安装依赖

```bash
pip install typer pydantic pyyaml rich openai httpx
```

### 2. 初始化配置文件

```bash
PYTHONPATH=src python -m fitment_agent init --template us_edmunds
```

这会在当前目录生成两个文件：

- `requirement.yaml` —— 控制 LLM **如何处理**数据（选模板 + 填参数）
- `input_list.yaml` —— 指定**处理哪些**车型（只需填品牌 + 车型名）

### 3. 编辑配置文件

**requirement.yaml**

```yaml
template: us_edmunds          # 或 eu_autodata

params:
  market: US
  data_sources: [Edmunds, KBB, NHTSA]
  focus_fields: [dimensions, year_range, generation]
  extra_instructions: []

  # 可选覆盖
  # max_rounds: 150
  # chunk_size: 50
  # model: gpt-4o
```

可选模板：

| 模板 | 市场 | 数据源 |
|------|------|--------|
| `us_edmunds` | 美国 | Edmunds / KBB / NHTSA |
| `eu_autodata` | 欧洲 | Auto-Data / Car.info / UltimateSpecs |

**input_list.yaml**

```yaml
vehicles:
  - make: Chevrolet
    model: Silverado 2500HD
  - make: Ford
    model: F-150
  - make: Toyota
    model: Tacoma

# 可选：限制展开范围
#   year_from: 2001
#   year_to: 2024
#   body_styles: [Pickup]
#   generations: [gen1, gen2]

# 或直接使用已有的 TSV 文件
# prebuilt_tsv: ./my_data.tsv
```

### 4. 设置 API Key

```bash
export OPENAI_API_KEY=sk-...
```

### 5. 运行

```bash
PYTHONPATH=src python -m fitment_agent run
```

## CLI 命令

```
fitment run        运行完整的补强流水线（展开 → 拆分 → 处理 → 合并）
fitment validate   仅校验 requirement.yaml 和 input_list.yaml
fitment init       生成示例配置文件
fitment expand     预览车辆展开结果（不调用 LLM）
```

### run

```bash
PYTHONPATH=src python -m fitment_agent run \
  --requirement requirement.yaml \
  --input input_list.yaml \
  --project-dir ./work \
  --backend openai \
  --chunk-size 50 \
  --max-rounds 150
```

常用参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-r / --requirement` | requirement.yaml 路径 | `./requirement.yaml` |
| `-i / --input` | input_list.yaml 路径 | `./input_list.yaml` |
| `-p / --project-dir` | 工作目录 | `./work` |
| `-b / --backend` | LLM 后端：`openai` 或 `browser` | `openai` |
| `--chunk-size` | 每个分片的行数 | `50` |
| `--max-rounds` | 每个分片最大对话轮数 | `150` |
| `--dry-run` | 仅显示执行计划，不实际运行 | `false` |
| `--resume` | 从上次断点继续 | `false` |

### validate

```bash
PYTHONPATH=src python -m fitment_agent validate
```

校验两个 YAML 文件是否合法，不执行任何处理。

### init

```bash
PYTHONPATH=src python -m fitment_agent init --template eu_autodata --output-dir ./my_project
```

生成指定模板的示例 `requirement.yaml` 和 `input_list.yaml`。

### expand

```bash
PYTHONPATH=src python -m fitment_agent expand --output expanded_preview.tsv
```

预览品牌 + 车型名会展开为哪些行（不调用 LLM）。

## 运行流水线

`fitment run` 会自动执行以下步骤：

1. **车辆展开** —— 将每个 `make + model` 通过 LLM 展开为所有代际、年份区间、车身形式
2. **TSV 拆分** —— 按 `chunk_size` 拆分为多个分片
3. **逐片处理** —— 每个分片启动独立 LLM 对话，多轮迭代直到完成
4. **结果合并** —— 从每个分片的最终轮次提取 TSV，合并为一张总表
5. **生成摘要** —— 输出 `summary.txt` 汇总成功/失败/偏离情况

处理过程中会生成 `checkpoint.json`，支持 `--resume` 断点续跑。

### 输出目录结构

```
work/
├── input/                  # 拆分后的 TSV 分片
│   ├── split_part_01.tsv
│   └── split_part_02.tsv
├── output/                 # 每个分片的多轮对话结果
│   ├── split_part_01_result.md
│   └── split_part_02_result.md
├── checkpoint.json         # 断点续跑状态
└── summary.txt             # 运行摘要
```

## 运行测试

```bash
PYTHONPATH=src python -m pytest tests/ -v
```

## 项目结构

```
src/fitment_agent/
├── cli.py                   # CLI 入口
├── config/
│   ├── models.py            # requirement.yaml + input_list.yaml 数据模型
│   └── loader.py            # YAML 加载与校验
├── templates/
│   ├── base.py              # 模板抽象基类
│   ├── registry.py          # 模板注册表
│   ├── us_edmunds.py        # US Edmunds 模板
│   ├── eu_autodata.py       # EU AutoData 模板
│   └── prompts/             # 内置 requirement 文档
├── vehicle/
│   ├── expander.py          # 品牌+车型 → 种子 TSV
│   └── tsv_splitter.py      # TSV 拆分
├── llm/
│   ├── protocol.py          # LLM 后端抽象接口
│   └── openai_api.py        # OpenAI API 实现
├── agent/
│   ├── orchestrator.py      # 流水线编排
│   ├── shard_worker.py      # 分片多轮 Agent 循环
│   ├── signals.py           # 完成/重复/偏离信号检测
│   ├── messages.py          # 上下文感知消息构建
│   └── state.py             # 分片状态机
├── merger/
│   └── result_merger.py     # 结果合并
└── io/
    └── project.py           # 项目目录管理
```

---

## Legacy: PowerShell 自动化

以下是基于 PowerShell + OpenClaw 浏览器自动化的旧版用法，仍然兼容。

### 使用 config.yaml 工作

默认入口是 `run_from_config.ps1`，读取同目录的 `config.yaml`。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\run_from_config.ps1"
```

只检查配置、目录和 OpenClaw 页面控制，不发送消息：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\run_from_config.ps1" -Mode check
```

只显示将要遍历的项目：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\run_from_config.ps1" -Mode dry_run
```

`config.yaml` 各部分说明：

- `mode`：`work`、`check` 或 `dry_run`，默认 `work`
- `workspace.traversal`：选择 `directories`、`glob` 或 `explicit` 遍历方式
- `project_layout`：定义 `input`、`output`、日志和汇总文件位置
- `runtime`：定义最大轮数、浏览器、失败后是否继续
- `data_contract.requirement`：requirement 文件地址
- `data_contract.full_table`：全量 TSV 列顺序和自动留空列
- `data_contract.subseries_match`：子车系匹配表列顺序和自动列

### 直接运行自动化脚本

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\qclaw_fitment_automation.ps1" -Project .\projects\0610 -MaxRounds 150
```

### 手动首轮后自动发送下一步

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\auto_next_until_done.ps1"
```

脚本打开 ChatGPT 后，手动发送初始 prompt，按 Enter 后脚本自动循环发送 `下一步`。

### 拆分原始 TSV

```powershell
python .\split_origin_tsv.py --origin .\full.tsv --output-dir .\input_sheets --prefix split --chunk-size 20 --write
```

### 合并最终 Round 结果

```powershell
python .\merge_final_round_results.py --project .\projects\0610
```
