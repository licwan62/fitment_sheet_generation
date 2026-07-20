# MotorcycleSpecs 摩托车尺寸采集

这个项目根据输入的品牌和车型寻找可信的车型页面，再从页面中取得长、宽、高信息。核心流程分为三个连续阶段：

```text
输入车型 → match → fetch → parse → 尺寸结果
```

## 首次安装（venv + .env）

要求 Python 3.12+。在本项目目录中执行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

复制环境变量模板，并在 `.env` 中填写一次真实的 Qwen API Key：

```powershell
Copy-Item .env.example .env
notepad .env
```

`.env` 的内容格式如下：

```dotenv
QWEN_API_KEY=你的_Qwen_API_Key
```

程序启动时会自动读取项目根目录下的 `.env`，以后无需重复输入。`.env` 和 `.venv` 均已加入 `.gitignore`，不会提交到 Git；系统中已有的 `QWEN_API_KEY` 优先于 `.env`。如果两处都未设置，程序仍会临时提示输入。

以后每次打开新的 PowerShell，只需激活虚拟环境后运行命令：

```powershell
.\.venv\Scripts\Activate.ps1
python -m moto_dimension_crawler --help
```

## match：确定哪些页面属于输入车型

`match` 逐条处理输入车型，在各来源的页面目录中寻找候选，并判断候选页面是否足够可信。

这一阶段回答的是：**“哪个网页对应这条输入车型？”**

- 匹配成功：保留一个或多个可信页面，交给 `fetch`。
- 只有近似候选：保留为复核信息，不自动用作尺寸来源。
- 没有可信候选：该车型不会进入正常的网页抓取与解析流程。

`match` 不下载车型详情页，也不从网页中读取长宽高。实时结果写入 `match_progress.csv`；一行表示一条输入车型已经完成匹配，重点查看匹配状态、最佳页面和可信页面数量。

## fetch：取得匹配页面的原始内容

`fetch` 接收 `match` 选出的可信页面，取得页面 HTML；已有可用缓存时直接确认缓存，不重复下载。同一个 URL 被多个输入车型命中时，页面内容只需取得一次，后续关系可以复用。默认使用两路并发，但仍按域名维持配置的请求间隔。

默认的 `crawler.fetch_strategy: adaptive` 会优先处理高可信匹配和高优先级来源。页面下载后会立即做一次内部完整性检查；取得无异常的完整长宽高后，剩余候选标记为 `SKIPPED_ADAPTIVE`。同一来源、同一标题的大量年份页默认仅保留早期、中期和晚期三个代表页面。需要抓取全部可信页面时，可将该配置改为 `exhaustive`。

这一阶段回答的是：**“目标网页的原始内容是否已经拿到？”**

`fetch` 保存页面内容并记录抓取是否成功；自适应模式的内部完整性检查只用于决定是否继续抓取，正式字段仍由 `parse` 阶段写出。因此 `fetch_progress.csv` 只显示页面 URL、抓取状态、抓取时间和内容标识，**不会出现 `L_RAW`、`W_RAW`、`H_RAW`，也不会出现换算后的 `L-MM`、`W-MM`、`H-MM`**。

换句话说，fetch 取得的是“包含尺寸信息的整张网页”，而不是“已经识别出来的尺寸数据”。

## parse：从页面中识别尺寸

`parse` 读取 `fetch` 得到的页面内容，识别页面中的尺寸文字，并把它们整理成可用字段。

这一阶段回答的是：**“网页写了什么尺寸，这些尺寸分别对应长、宽、高多少毫米？”**

在这里程序才会：

- 找到页面中的长、宽、高原文；
- 区分单值、范围值和组合尺寸；
- 将页面单位统一换算为毫米；
- 判断长宽高是完整、部分缺失，还是页面没有尺寸；
- 保留来源页面和解析状态，供结果追溯。

因此，对于网页来源的数据，**长宽高是在 parse 阶段首次被识别成尺寸字段的**。`parse_progress.csv` 会实时显示 `L-MM`、`W-MM`、`H-MM` 和解析状态。

原始尺寸文字 `L_RAW`、`W_RAW`、`H_RAW` 也在 parse 阶段产生，但当前不会写进实时的 `parse_progress.csv`；完整运行到 `run` 或 `export` 后，可在 `logs/run_details.jsonl` 的 `DIMENSIONS_RAW` 记录中查看。

例外是明确标记的 AI 推断结果：它没有来源网页，不经过正常的 fetch/parse 提取，不能与网页实证尺寸混为一谈。

## 三个进度文件该看什么

| 文件 | 表示已经完成 | 用来检查 |
| --- | --- | --- |
| `match_progress.csv` | 输入车型与页面的匹配 | 找没找到可信页面、匹配到了哪些页面 |
| `fetch_progress.csv` | 页面下载或缓存确认 | 页面内容是否成功取得 |
| `parse_progress.csv` | 页面尺寸解析 | 是否得到长宽高、缺了哪些字段 |

三个文件对应三个不同问题，不能从 `fetch_progress.csv` 判断页面最终能否解析出尺寸；只有进入 `parse` 后才知道。

## 运行方式

完整执行三个阶段：

```powershell
python -m moto_dimension_crawler run --input data/input/motorcycles.xlsx --output output/production
```

也可以停在某个阶段检查结果：

```powershell
python -m moto_dimension_crawler match --input data/input/motorcycles.xlsx --output output/check
python -m moto_dimension_crawler fetch --input data/input/motorcycles.xlsx --output output/check
python -m moto_dimension_crawler parse --input data/input/motorcycles.xlsx --output output/check
```

这些命令表示“执行到该阶段为止”：`fetch` 会先完成或恢复 `match`，`parse` 会先完成或恢复 `match` 和 `fetch`。再次运行时，已经完成的匹配和已取得的页面可以继续使用。
