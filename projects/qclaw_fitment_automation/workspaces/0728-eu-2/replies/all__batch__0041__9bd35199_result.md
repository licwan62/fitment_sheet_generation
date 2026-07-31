# 任务：all 第 4001-4100 行
# 来源文件：all.tsv
# 任务 ID：all__batch__0041__9bd35199


--- 发送 / 首次任务 ---
【任务名称】
【全量表更新】all 第 4001-4100 行

【任务要求】
# EU Auto-Data Ktype 与尺寸组补全规则

本规则适用于以下 Tab 分隔的欧洲车型输入表。`Ktype` 是输入车型标识，但不保证唯一对应一个物理车身。输出必须包含两张互相解耦的全量 TSV：

1. `Ktype 映射表`：保存 Ktype、派生主键和尺寸组关系。
2. `DIMENSION_GROUP 表`：保存每个尺寸组唯一一套长宽高及其来源。

```tsv
Make	Model	VariantName	BodyStyle	DriveType	Energy	EngineOutputKW	EngineOutputHP	Product Start Month-Year	Product End Month-Year	LastProcessedDate	Ktype	LatestStatus
Opel	Corsa d	1.4	Schrägheck	Frontantrieb	Benzin	66	90	Jul 2006	Aug 2014	2024-03-01	1	NEW
```

<!-- fitment-data-contract
full_table:
  columns:
    - id
    - Ktype
    - NormalizedBodyStyle
    - Generation
    - BodyCode
    - Doors
    - DIMENSION_GROUP_ID
    - MatchConfidence
    - Notes
    - IterationStatus
  auto_empty_columns: []
dimension_group_table:
  enabled: true
  columns:
    - DIMENSION_GROUP_ID
    - LengthMM
    - WidthMM
    - HeightMM
    - DimensionSource
    - SourceURL
  auto_empty_columns: []
subseries_match:
  enabled: false
  columns: []
  auto_empty_columns: []
-->

## 一、输出模型与粒度

### 1. Ktype 映射表

Ktype 映射表只表达车型和物理尺寸组之间的关系，不重复输入表字段，也不保存具体尺寸值或抓取过程字段。

- `id`：映射表唯一主键，按文本处理。
- `Ktype`：指向输入表的外键，必须逐字保留；禁止转为浮点数、改写前导零或生成不存在的 Ktype。
- `DIMENSION_GROUP_ID`：指向 DIMENSION_GROUP 表的外键。
- 一个 Ktype 可以对应多个 `id` 和多个 `DIMENSION_GROUP_ID`。
- 多个 Ktype 也可以引用同一个 `DIMENSION_GROUP_ID`，因此业务关系允许多对多。
- 每个输入 Ktype 至少输出一行；不得因待处理或共用尺寸组而删除。
- 不输出 `Make`、`Model`、`VariantName`、生产年月等其他输入字段，需要时通过 Ktype 回查输入表。
- 不在映射表保存 `WheelbaseMM`、`LengthMM`、`WidthMM`、`HeightMM`、`WidthBasis`、`EndDateStatus`、`ResolutionStatus`、`CacheSourceKtype`、`MatchReason`、`DimensionSource` 或 `SourceURL`。

### 2. id 生成规则

- 当一个 Ktype 唯一对应一条物理尺寸记录时，`id` 直接等于 Ktype，例如 `2`。
- 当一个 Ktype 对应多个不同物理车身或尺寸时，分别输出多行，`id` 使用 `{Ktype}_{描述}`，例如 `1_3dr`、`1_5dr`。
- 后缀必须简短、稳定、可读，并表达造成物理外廓差异的特征。优先使用 `3dr`、`5dr`、`swb`、`lwb`、`lowroof`、`highroof`、`srw`、`drw`、`prefl`、`facelift` 等小写 ASCII 标记；必要时组合，例如 `12_5dr_facelift`。
- Ktype 拆成派生行后，不再保留无后缀的 `id=Ktype` 基础行。
- 不得使用无语义临时序号掩盖未确认差异。
- 已确认 Ktype 覆盖多个物理外廓时，必须输出全部派生行，不能任选一个，也不能仅因 Ktype 不唯一而保持 `PENDING`。
- 若证据只表明可能存在多个外廓，但尚不能确认具体分支，则暂时保留 `id=Ktype` 的一行并标记 `PENDING`，不得创建猜测性派生行。

### 3. DIMENSION_GROUP 表

DIMENSION_GROUP 表是尺寸事实的唯一落盘位置。

- 每个 `DIMENSION_GROUP_ID` 恰好出现一次。
- 每行必须完整填写 `LengthMM`、`WidthMM`、`HeightMM`、`DimensionSource` 和 `SourceURL`。
- Ktype 映射表中引用的每个 `DIMENSION_GROUP_ID` 都必须存在于本表。
- 本表不得包含当前 Ktype 映射表完全未引用的孤立尺寸组。
- 相同物理外廓只能复用同一个稳定 `DIMENSION_GROUP_ID`，不得因 Ktype、发动机或来源不同重复建组。
- 物理外廓不同必须使用不同 `DIMENSION_GROUP_ID`。
- 如果当前批次得到的三维与累计表中同名 `DIMENSION_GROUP_ID` 不同，禁止覆盖已有组；应使用同系列下一个可用序号创建新尺寸组，并将当前批次所有相关 Ktype 映射同步指向新组。
- 尺寸研究、来源冲突和缓存核验都在尺寸组层完成，不在 Ktype 映射表重复落盘。

### 4. 首次建组与后续复用

尺寸抓取以 `DIMENSION_GROUP_ID` 为单位，而不是以 Ktype 为单位：

1. 处理 Ktype 前先查询当前批次及历史缓存中已有的 `DIMENSION_GROUP_ID`，再决定是否需要外部抓取。
2. 首次创建一个 `DIMENSION_GROUP_ID` 时，完整核对一次物理车身边界、`LengthMM`、不含后视镜的 `WidthMM`、`HeightMM`、`DimensionSource` 和 `SourceURL`。
3. 尺寸和来源闭合后，将该组作为稳定缓存。相同组在当前批次和后续批次均直接复用。
4. 后续 Ktype 只判断它应该关联哪个现有尺寸组；不得为每个 Ktype 重复打开尺寸页面、重新抓取同一组三维或重复整理来源。
5. 一次尺寸组核对应尽可能同时解决所有候选相同外廓的 Ktype，避免串行逐条查询。
6. 后续关联不填写、不输出 `CacheSourceKtype`、`MatchReason`、`ResolutionStatus` 或重复来源说明。
7. 只有出现以下情况才允许重新打开尺寸核对：
   - 现有尺寸组缺字段或来源不可追溯；
   - 新证据表明代际、BodyStyle、门数外形、轴距、车顶、宽体、改款或外部套件不同；
   - 现有尺寸与可靠来源发生实质冲突；
   - 宽度不能确认是不含后视镜口径。
8. 发动机、功率、燃料、变速箱或普通配置不同，不能触发重复尺寸抓取。

处理顺序应优先按候选物理车身聚类：先创建并闭合一个尺寸组，再批量将所有匹配 Ktype 链接到该组，避免逐 Ktype 重复查询。

## 二、输入字段解释

| 字段 | 处理规则 |
| --- | --- |
| Make | 原始品牌。查询时允许使用标准品牌写法；输出表不重复此字段。 |
| Model | 原始车型/车系，可能包含代际提示，例如 `Corsa d`、`Megane iii`；输出表不重复此字段。 |
| VariantName | 发动机或版本名称，用于核验 Ktype，不等于物理车身；输出表不重复此字段。 |
| BodyStyle | 原始德语或欧洲市场车身形式；标准化结果写入 `NormalizedBodyStyle`。 |
| DriveType | 通常不单独决定尺寸组，但需注意特殊底盘是否改变外廓。 |
| Energy | 通常不单独决定尺寸组。 |
| EngineOutputKW / EngineOutputHP | 仅用于版本核验，不得作为尺寸组相同或不同的唯一依据。 |
| Product Start Month-Year | Ktype 的生产开始月，通常为 `MMM YYYY`。 |
| Product End Month-Year | Ktype 的生产结束月；`-`、空值或未知值不能解释为生产至今。 |
| LastProcessedDate | 上游处理日期，不是车型生产日期或资料发布日期。 |
| Ktype | 输入车型标识和输出外键，不保证唯一对应一套尺寸。按文本处理。 |
| LatestStatus | 上游状态；本轮状态写入 `IterationStatus`。 |

输入必须按 Tab 解析；字段内空格不是分隔符。

## 三、Ktype 映射字段

### 1. NormalizedBodyStyle

根据输入 `BodyStyle` 和可靠车型资料写入：

| 常见原值 | NormalizedBodyStyle |
| --- | --- |
| Schrägheck、Hatchback | Hatchback |
| Stufenheck、Limousine、Sedan | Sedan |
| Kombi、Touring、Estate | Wagon |
| Coupe、Coupé | Coupe |
| Cabriolet、Roadster | Convertible |
| SUV、Geländewagen | SUV |
| Van、Großraumlimousine、MPV | MPV |
| Kasten、Kastenwagen | Van |
| Pritsche、Pickup | Pickup |

无法可靠归类时保留最接近的来源写法，并在 `Notes` 说明，不得凭外观猜测。

### 2. Generation、BodyCode、Doors

- `Generation`：正式代际名称，例如 `Corsa D`，不能仅从生产年份推断。
- `BodyCode`：厂商平台或车身代码；一行只能填写一个明确代码，不能写 `L08/L68` 等组合值。无可靠证据时留空。
- `Doors`：只写整数，例如 `3`、`5`；一行只能表示一种门数。来源未明确时留空。
- 不抓取、不推断、不输出 `WheelbaseMM`。
- 不得把发动机代号、底盘配置或营销版本误写为 `BodyCode`。

若门数、车身代码、轴距、车顶、驾驶室、货斗、宽体、改款或特殊外部套件造成不同外廓，必须拆成不同 `id` 并链接不同尺寸组。轴距只作为判断线索，不需要落盘。

### 3. MatchConfidence、Notes、IterationStatus

`MatchConfidence` 只允许 `HIGH`、`MEDIUM`、`LOW`，表示 Ktype/派生 id 与尺寸组之间的映射置信度，不表示尺寸来源质量。

`Notes` 只记录映射层必要信息，例如派生原因、门数/车身代码边界或人工决定。具体尺寸、抓取来源、缓存来源、匹配理由和核验过程不得在这里重复落盘。能够由 `DIMENSION_GROUP_ID` 表达的内容不再写入 `Notes`。

`IterationStatus` 只允许：

- `READY`
- `PENDING: <具体原因>`

映射行只有同时满足以下条件才能写 `READY`：

- `id` 唯一，Ktype 能回查输入表。
- 必要的 Generation、NormalizedBodyStyle、BodyCode/Doors 物理边界已确认。
- 已链接一个确定的 `DIMENSION_GROUP_ID`。
- 被引用尺寸组存在于本轮完整 DIMENSION_GROUP 表中，且三维和来源完整。
- 映射没有未解决冲突。

`PENDING` 行的 `DIMENSION_GROUP_ID` 必须留空；候选组只能简要写入 `Notes`。

## 四、尺寸组与统一尺寸口径

### 1. DIMENSION_GROUP_ID

只有物理车身边界和同一配置的三维均确认后才能创建或命中尺寸组。ID 必须跨当前批次和后续缓存保持稳定，推荐格式：

```text
EU-{MAKE}-{MODEL}-{GENERATION}-{BODYSTYLE}-{SEQUENCE}
```

示例：

```text
EU-OPEL-CORSA-D-HATCHBACK-3D-01
```

ID 只使用大写 ASCII、数字和连字符。不得把 `id` 或 Ktype 直接当作尺寸组 ID，也不得创建临时确认组。

以下差异通常不单独创建尺寸组：

- 发动机排量、功率、增压方式
- 燃料或能源类型
- 变速箱
- 不改变外部轮廓的驱动形式
- 普通配置等级

以下差异必须独立核对，外廓不同则使用不同尺寸组：

- 不同代际或车身代码
- 不同 BodyStyle 或门数外形
- 不同轴距、SWB/LWB
- 普通车身/宽体、SRW/DRW
- 普通顶/高顶
- facelift 前后尺寸变化
- 不同 CAB/BED
- 特殊悬架高度、保险杠或外部套件
- 同名车型停产后重新推出

不得仅凭 `Make + Model + VariantName` 相似复用尺寸组。

### 2. LengthMM、WidthMM、HeightMM

- `LengthMM`：量产标准状态下的最大车身外部长度，单位 mm。
- `WidthMM`：强制使用不含外后视镜的车身宽度，单位 mm。
- `HeightMM`：量产标准状态下的外部高度，单位 mm。
- 不输出 `WidthBasis`；所有落盘的 `WidthMM` 按规则即为 `WITHOUT_MIRRORS`。
- 如果只能获得含后视镜宽度或宽度口径未知，该尺寸组不得进入完整 DIMENSION_GROUP 表，对应映射保持 `PENDING`。
- 三个尺寸格只写正整数，不写单位、约数、范围或多个候选值。
- 同一尺寸组的长宽高必须属于同一物理配置，不能从不同版本拼接。
- 英寸换算使用 `1 in = 25.4 mm`，最终取整到 1 mm；厘米换算使用 `1 cm = 10 mm`。

## 五、尺寸来源

来源优先级：

1. 厂商官网、官方 brochure、technical specification、press kit、历史资料、homologation 或 type approval。
2. Auto-Data、Car.info、UltimateSpecs、Automobile-Catalog、Parkers。
3. 其他可信规格数据库，仅用于交叉验证。

二手车广告、论坛、搜索摘要、AI 摘要和无出处聚合页只能作为线索，不能单独支撑最终尺寸组。

- `DimensionSource`：填写直接支持该组三维或关键物理边界的来源名称。
- `SourceURL`：填写对应直接页面 URL，不得填写搜索结果页。
- 多个来源使用分号分隔，并保持名称和 URL 顺序对应。
- 来源冲突时核对市场、年份、代际、BodyStyle、门数、轴距、含镜口径和特殊版本；无法解决时不创建完整尺寸组，对应映射保持 `PENDING`。

## 六、每轮固定输出

为减少抓取频率和对话落盘体积，区分推进轮与最终轮。

### CONTINUE 推进轮

尚未完成时依次输出：

1. `更新点`
2. `当前批次进度`
3. `本轮新增/修改的 Ktype 映射 TSV`，仅输出本轮发生变化的行；没有变化时明确写“无”
4. `本轮新增/修改的 DIMENSION_GROUP TSV`，仅输出首次创建或本轮修正的尺寸组；复用既有组时不重复输出；没有变化时明确写“无”
5. `下一步优先处理`
6. 最后一行输出 `推进信号：CONTINUE`

推进轮不得为了形式完整而重复打印未变化的 Ktype 行或既有尺寸组。尺寸组一旦闭合，后续轮只通过 `DIMENSION_GROUP_ID` 引用。

### COMPLETE 最终轮

只有准备完成时，依次输出：

1. `更新点`
2. `当前批次进度`
3. `最终完整 Ktype 映射 TSV`
4. Ktype 映射 TSV 的可点击 sandbox 下载链接
5. `最终完整 DIMENSION_GROUP TSV`
6. DIMENSION_GROUP TSV 的可点击 sandbox 下载链接
7. 最后一行输出 `推进信号：COMPLETE`

最终轮的两张表必须是当前批次可直接落盘的完整快照，不能只输出变化行、引用上一轮或写“其余不变”。自动化只在同一条最终回复中检测到两张完整表时接受 `COMPLETE`。

下载文件名由当前任务提示明确给出，必须原样使用。分批任务示例：

```text
all_1-100_ktype_dimension_mapping_final.tsv
all_1-100_dimension_groups_final.tsv
```

链接必须是可点击的 Markdown sandbox 链接，例如：

```markdown
[下载 Ktype 映射表](sandbox:/mnt/data/all_1-100_ktype_dimension_mapping_final.tsv)
[下载 DIMENSION_GROUP 表](sandbox:/mnt/data/all_1-100_dimension_groups_final.tsv)
```

只有文字文件名、缺少链接、链接不是 `.tsv`、文件名与任务提示不一致，均不得输出 `COMPLETE`。

自动化在接受 COMPLETE 后会从同一回复的两张内嵌 TSV 生成本批本地文件。分批模式固定使用首批文件名维护两张累计总表：

```text
all_1-100_ktype_dimension_mapping_final.tsv
all_1-100_dimension_groups_final.tsv
```

第一批成功时创建这两张总表；此后每个批次成功都立即追加。累计合并以 `id` 和 `DIMENSION_GROUP_ID` 去重，可安全恢复或重复处理；尺寸组出现三维冲突时必须停止，不得静默覆盖首次确认的尺寸事实。首批文件名从第二批开始代表累计总表，不再是冻结的第一批快照。

### Ktype 映射表排序

1. 保持输入 Ktype 原始顺序。
2. 同一 Ktype 有多行时按稳定物理分支排序，例如 `3dr` 在 `5dr` 前、`swb` 在 `lwb` 前。
3. 后续轮次不得无故改变已确认 `id` 或行顺序。

### DIMENSION_GROUP 表排序

建议按各尺寸组第一次在 Ktype 映射表中被引用的顺序排列。一个组只出现一次。尺寸组顺序仅用于稳定输出，不得因非阻塞的排序差异延迟 `COMPLETE`。

### 第二阶段轻量收尾

1. 第一阶段只负责消除数据缺失；当进度达到 `PENDING=0`、`READY=全部输入行` 时，数据阶段结束。
2. 第二阶段最多只允许一轮轻量机械检查：两张表表头固定、`id` 与 `DIMENSION_GROUP_ID` 唯一、每个映射引用闭合、长宽高和来源非空、两个任务指定下载链接存在。
3. 第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复抓取，也不得重新验证已经首次确认并缓存的尺寸组。
4. `PENDING=0` 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以 `推进信号：COMPLETE` 结束；不得再输出 `CONTINUE`。
5. 非阻塞的排序、措辞、置信度微调或来源偏好不影响完成。只要既有尺寸组已按首次创建规则确认且映射闭合，应优先完成并给出链接。

### CONTINUE 输出示例

````text
更新点
- ……

当前批次进度
- READY 映射：……
- PENDING 映射：……
- 已确认尺寸组：……
- 当前批次尚未完成。

本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
1_3dr	1	Hatchback	Corsa D	L08	3	EU-OPEL-CORSA-D-HATCHBACK-3D-01	HIGH	L08三门物理外廓。	READY
1_5dr	1	Hatchback	Corsa D	L68	5	EU-OPEL-CORSA-D-HATCHBACK-5D-01	HIGH	L68五门物理外廓。	READY
```

本轮新增/修改的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-OPEL-CORSA-D-HATCHBACK-3D-01	3999	1713	1488	Vauxhall New Corsa official brochure	https://www.vauxhall.co.uk/content/dam/vauxhall/Home/PDFs/historical-brochures/discounted-models/corsa-d/CorsaD_February_2007.pdf
EU-OPEL-CORSA-D-HATCHBACK-5D-01	3999	1737	1488	Vauxhall New Corsa official brochure	https://www.vauxhall.co.uk/content/dam/vauxhall/Home/PDFs/historical-brochures/discounted-models/corsa-d/CorsaD_February_2007.pdf
```

下一步优先处理
1. ……

推进信号：CONTINUE
````

## 七、COMPLETE 条件

`PENDING=0` 后立即按以下机械条件组装最终产物；全部满足即可输出 `推进信号：COMPLETE`，无需再做第二轮外部核对：

1. 两张最终完整 TSV 均已在同一条当前回复中输出，表头和顺序严格正确。
2. 两个按任务指定文件名生成的 `.tsv` sandbox 下载链接均已提供。
3. Ktype 映射表覆盖每个输入 Ktype，所有派生物理分支均无遗漏。
4. 每个映射行都有唯一 `id`、有效 `DIMENSION_GROUP_ID`，且 `IterationStatus=READY`。
5. 每个映射引用都能在 DIMENSION_GROUP 表中找到恰好一行。
6. DIMENSION_GROUP 表中的每行都被当前映射表引用，不存在孤立组。
7. 每个尺寸组的长宽高均为完整正整数，`WidthMM` 明确是不含后视镜宽度。
8. 每个尺寸组的 `DimensionSource` 和 `SourceURL` 均完整、可追溯。
9. 不存在 `PENDING`、缺失尺寸、未知宽度口径、未解决来源冲突或候选尺寸组。
10. 同一物理尺寸组没有因多个 Ktype 而被重复建组或重复抓取。

任一机械条件不满足时，只修复该具体产物问题；不得重新展开逐车型研究。修复后立即输出两张完整 TSV、下载链接和 `COMPLETE`。

## 八、提交前强制检查

1. Ktype 映射表是否严格为 10 列，DIMENSION_GROUP 表是否严格为 6 列。
2. 映射表是否没有落盘已移除字段：`WheelbaseMM`、三维、`WidthBasis`、`EndDateStatus`、`ResolutionStatus`、`CacheSourceKtype`、`MatchReason`、来源字段。
3. `id` 是否每行有值且唯一；Ktype 是否逐字匹配输入表。
4. 每个输入 Ktype 是否至少出现一次；已确认多外廓 Ktype 是否完整派生且无基础重复行。
5. 多行是否确由物理外廓差异造成，而不是发动机、功率、燃料或普通配置差异造成。
6. 映射表的每个非空 `DIMENSION_GROUP_ID` 是否恰好命中尺寸组表一行。
7. 每个尺寸组是否只出现一次并被至少一个映射引用。
8. 长宽高是否来自同一配置、统一为 mm 且均为正整数。
9. `WidthMM` 是否明确为不含外后视镜口径。
10. 尺寸来源和 URL 是否完整对应且可追溯。
11. 是否保持映射顺序和尺寸组首次引用顺序。
12. 是否只有两张要求的 TSV，没有另建子车系表、缓存表或抓取明细表。
13. 输出 COMPLETE 前是否确认两张表均完整、所有映射 READY 且无 PENDING。
14. 是否仅在首次创建或纠错尺寸组时抓取三维和来源；后续 Ktype 是否只建立关联。
15. CONTINUE 轮是否避免重复输出未变化记录，COMPLETE 轮是否一次性输出两张完整快照。
16. COMPLETE 轮是否提供任务指定文件名的两个可点击 `.tsv` sandbox 下载链接。


【执行顺序】
执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。

【配置附加规则】


【当前文件名】
all.tsv

【当前独立任务】
all 第 4001-4100 行

【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_4001-4100_ktype_dimension_mapping_final.tsv
- all_4001-4100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。

【跨批次已有尺寸组索引】
以下 ID 已经存在于累计表。三维和物理外廓完全相同时才可复用；如果当前证据得到不同三维，禁止改写已有组，必须使用同系列下一个可用序号创建新 DIMENSION_GROUP_ID，并把当前批次相关 Ktype 全部指向新组。

DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM
EU-ALFA-ROMEO-147-937-HATCHBACK-FACELIFT-01	4223	1729	1442
EU-ALFA-ROMEO-147-937-HATCHBACK-PREFL-01	4170	1729	1442
EU-ALFA-ROMEO-MITO-955-HATCHBACK-3D-01	4060	1720	1440
EU-AUDI-Q5-8R-SUV-5D-PREFL-01	4629	1880	1653
EU-BENTLEY-ARNAGE-T-SEDAN-4D-01	5400	1900	1515
EU-BMW-1-SERIES-E81-HATCHBACK-3D-01	4239	1748	1421
EU-BMW-1-SERIES-E82-COUPE-2D-01	4360	1748	1423
EU-BMW-1-SERIES-E88-CONVERTIBLE-2D-01	4360	1748	1411
EU-BMW-X5-E70-SUV-01	4854	1933	1766
EU-BMW-X5-F15-SUV-01	4886	1938	1762
EU-CADILLAC-CTS-II-SEDAN-4D-01	4866	1842	1472
EU-CITROEN-C25-I-CHASSIS-CAB-LWB-1400-01	5442	1965	2108
EU-CITROEN-C25-I-CHASSIS-CAB-LWB-1800-01	5442	1965	2080
EU-CITROEN-C25-I-CHASSIS-CAB-SWB-MWB-01	4989	1965	2108
EU-CITROEN-C2-I-HATCHBACK-3D-01	3666	1659	1474
EU-CITROEN-C3-PICASSO-I-PHASE-I-MPV-5D-01	4078	1766	1669
EU-CITROEN-C4-GRAND-PICASSO-I-UA-MPV-AIRSUSP-01	4590	1830	1690
EU-CITROEN-C4-GRAND-PICASSO-I-UA-MPV-COIL-01	4590	1830	1710
EU-CITROEN-C4-PICASSO-I-UD-MPV-AIRSUSP-01	4470	1830	1660
EU-CITROEN-C4-PICASSO-I-UD-MPV-COIL-01	4470	1830	1680
EU-CITROEN-C5-II-X7-SEDAN-4D-01	4779	1860	1451
EU-CITROEN-C5-II-X7-TOURER-WAGON-5D-01	4829	1860	1479
EU-CITROEN-C5-I-PHASE-I-HATCHBACK-5D-01	4618	1770	1476
EU-CITROEN-C5-I-PHASE-II-HATCHBACK-01	4745	1780	1476
EU-CITROEN-C5-I-PHASE-II-HATCHBACK-02	4750	1770	1480
EU-CITROEN-C5-I-PHASE-II-WAGON-01	4839	1780	1511
EU-CITROEN-C5-I-PHASE-I-WAGON-5D-01	4760	1770	1520
EU-FIAT-CROMA-II-WAGON-5D-01	4756	1775	1597
EU-FIAT-DUCATO-I-280-VAN-L1H1-01	4760	1965	2100
EU-FIAT-DUCATO-I-280-VAN-L1H2-01	4760	1965	2419
EU-FIAT-DUCATO-I-280-VAN-L2H2-01	5495	1965	2450
EU-FIAT-DUCATO-II-CHASSIS-244-LWB-15-01	5681	1932	2100
EU-FIAT-DUCATO-II-CHASSIS-244-LWB-MAXI-01	5681	1932	2125
EU-FIAT-DUCATO-II-CHASSIS-244-MWB-15-01	5181	1932	2100
EU-FIAT-DUCATO-II-CHASSIS-244-MWB-MAXI-01	5181	1932	2125
EU-FIAT-DUCATO-II-CHASSIS-244-SWB-15-01	4831	1932	2100
EU-FIAT-DUCATO-II-CHASSIS-244-XLWB-15-01	5980	2040	2100
EU-FIAT-DUCATO-II-CHASSIS-244-XLWB-MAXI-01	5980	2040	2125
EU-FIAT-DUCATO-III-BUS-LWB-HIGHROOF-01	5998	2050	2524
EU-FIAT-DUCATO-III-BUS-MWB-HIGHROOF-01	5413	2050	2524
EU-FIAT-DUCATO-III-BUS-SWB-LOWROOF-01	4963	2050	2254
EU-FIAT-DUCATO-III-CHASSIS-LWB-01	5943	2050	2254
EU-FIAT-DUCATO-III-CHASSIS-MLWB-01	5708	2050	2254
EU-FIAT-DUCATO-III-CHASSIS-MWB-01	5358	2050	2254
EU-FIAT-DUCATO-III-CHASSIS-SWB-01	4908	2050	2254
EU-FIAT-DUCATO-III-CHASSIS-XLWB-01	6308	2050	2254
EU-FIAT-DUCATO-III-VAN-L1H1-01	4963	2050	2254
EU-FIAT-DUCATO-III-VAN-L1H2-01	4963	2050	2522
EU-FIAT-DUCATO-III-VAN-L2H1-01	5413	2050	2254
EU-FIAT-DUCATO-III-VAN-L2H2-01	5413	2050	2524
EU-FIAT-DUCATO-III-VAN-L3H2-01	5998	2050	2524
EU-FIAT-DUCATO-III-VAN-L3H3-01	5998	2050	2764
EU-FIAT-DUCATO-III-VAN-L4H2-01	6363	2050	2539
EU-FIAT-DUCATO-III-VAN-L4H3-01	6363	2050	2779
EU-FIAT-DUCATO-II-VAN-244-LWB-HIGHROOF-01	5599	2024	2470
EU-FIAT-DUCATO-II-VAN-244-LWB-SUPERHIGHROOF-01	5599	2024	2860
EU-FIAT-DUCATO-II-VAN-244-MWB-HIGHROOF-01	5099	2024	2470
EU-FIAT-DUCATO-II-VAN-244-MWB-LOWROOF-01	5099	2024	2150
EU-FIAT-DUCATO-II-VAN-244-MWB-MAXI-HIGHROOF-01	5099	2024	2480
EU-FIAT-DUCATO-II-VAN-244-MWB-MAXI-LOWROOF-01	5099	2024	2160
EU-FIAT-DUCATO-II-VAN-244-MWB-MAXI-SUPERHIGHROOF-01	5099	2024	2735
EU-FIAT-DUCATO-II-VAN-244-MWB-SUPERHIGHROOF-01	5099	2024	2725
EU-FIAT-DUCATO-II-VAN-244-SWB-HIGHROOF-01	4749	2024	2470
EU-FIAT-DUCATO-II-VAN-244-SWB-LOWROOF-01	4749	2024	2150
EU-FIAT-DUCATO-II-X230-BUS-LWB-STANDARD-01	5005	1998	2150
EU-FIAT-DUCATO-II-X230-BUS-SWB-PANORAMA-01	4655	1998	2104
EU-FIAT-DUCATO-II-X230-VAN-SWB-LOWROOF-01	4655	1998	2150
EU-FIAT-DUCATO-X230-TRUCK-LWB-01	5620	2000	2100
EU-FIAT-DUCATO-X230-TRUCK-MWB-01	5120	2000	2100
EU-FIAT-DUCATO-X230-TRUCK-SWB-01	4770	2000	2100
EU-FIAT-DUCATO-X244-BODY-11-SWB-LOWROOF-01	4749	2024	2154
EU-FIAT-DUCATO-X244-BODY-15-LWB-HIGHROOF-01	5599	2024	2850
EU-FIAT-DUCATO-X244-BODY-15-LWB-MIDROOF-01	5599	2024	2470
EU-FIAT-DUCATO-X244-BODY-15-SWB-LOWROOF-01	4749	2024	2150
EU-FIAT-DUCATO-X244-BODY-MAXI-LWB-HIGHROOF-01	5599	2024	2860
EU-FIAT-DUCATO-X244-BODY-MAXI-LWB-MIDROOF-01	5599	2024	2480
EU-FIAT-DUCATO-X244-BODY-MAXI-MWB-HIGHROOF-01	5099	2024	2735
EU-FIAT-DUCATO-X244-BODY-MAXI-MWB-LOWROOF-01	5099	2024	2160
EU-FIAT-DUCATO-X244-BODY-MAXI-SWB-HIGHROOF-01	4749	2024	2480
EU-FIAT-DUCATO-X244-BODY-MAXI-SWB-LOWROOF-01	4749	2024	2160
EU-FIAT-DUCATO-X244-BODY-MWB-HIGHROOF-01	5099	2024	2725
EU-FIAT-DUCATO-X244-BODY-MWB-LOWROOF-01	5099	2024	2150
EU-FIAT-DUCATO-X244-BODY-SWB-HIGHROOF-01	4749	2024	2470
EU-FIAT-DUCATO-X244-TRUCK-LWB-MAXI-01	5861	2024	2125
EU-FIAT-DUCATO-X244-TRUCK-LWB-STANDARD-01	5861	2024	2100
EU-FIAT-DUCATO-X244-TRUCK-MWB-MAXI-01	5181	2024	2125
EU-FIAT-DUCATO-X244-TRUCK-MWB-STANDARD-01	5181	2024	2100
EU-FIAT-DUCATO-X244-TRUCK-SWB-STANDARD-01	4831	2024	2100
EU-MAZDA-CX-7-ER-SUV-5D-01	4680	1870	1645
EU-MINI-MINI-R50-HATCHBACK-ONE-D-FACELIFT-01	3626	1688	1416
EU-MINI-MINI-R52-CONVERTIBLE-01	3660	1690	1420
EU-MINI-MINI-R52-CONVERTIBLE-JCW-01	3635	1688	1415
EU-MINI-MINI-R53-HATCHBACK-JCW-3D-01	3655	1688	1427
EU-MINI-MINI-R56-HATCHBACK-3D-01	3699	1683	1407
EU-MINI-MINI-R57-CONVERTIBLE-COOPER-01	3699	1683	1414
EU-MINI-MINI-R57-CONVERTIBLE-COOPER-S-01	3714	1683	1414
EU-OPEL-ASTRA-H-GTC-HATCHBACK-3D-FACELIFT-01	4290	1753	1435
EU-OPEL-ASTRA-H-GTC-HATCHBACK-3D-PREFL-01	4290	1753	1415
EU-OPEL-ASTRA-H-GTC-HATCHBACK-FACELIFT-01	4290	1753	1405
EU-OPEL-ASTRA-H-GTC-HATCHBACK-PREFL-01	4290	1753	1415
EU-OPEL-CORSA-D-HATCHBACK-3D-01	3999	1713	1488
EU-OPEL-CORSA-D-HATCHBACK-3D-OPC-01	4040	1713	1488
EU-OPEL-CORSA-D-HATCHBACK-5D-01	3999	1737	1488
EU-PEUGEOT-407-COUPE-2D-01	4815	1868	1399
EU-PEUGEOT-407-I-SEDAN-FACELIFT-01	4691	1811	1442
EU-PEUGEOT-407-I-SEDAN-PREFL-01	4676	1811	1447
EU-PEUGEOT-407-I-SW-WAGON-FACELIFT-01	4763	1811	1460
EU-PEUGEOT-407-I-SW-WAGON-PREFL-01	4763	1811	1486
EU-PEUGEOT-407-PHASE-II-SEDAN-01	4691	1811	1455
EU-PEUGEOT-407-PHASE-I-SEDAN-01	4676	1811	1455
EU-PEUGEOT-407-SW-PHASE-I-WAGON-01	4763	1811	1486
EU-PEUGEOT-5008-I-MPV-01	4529	1888	1647
EU-PORSCHE-911-997-CARRERA-4-CONVERTIBLE-01	4427	1852	1310
EU-PORSCHE-911-997-CARRERA-4S-CONVERTIBLE-01	4427	1852	1300
EU-PORSCHE-911-997-COUPE-AWD-WIDEBODY-01	4427	1852	1300
EU-PORSCHE-911-997-COUPE-GT3-01	4445	1808	1280
EU-PORSCHE-911-997-COUPE-RWD-01	4427	1808	1300
EU-PORSCHE-911-997-FACELIFT-CARRERA-4-CONVERTIBLE-01	4435	1852	1310
EU-PORSCHE-911-997-FACELIFT-CARRERA-4-COUPE-01	4435	1852	1310
EU-PORSCHE-911-997-FACELIFT-CARRERA-4S-CONVERTIBLE-01	4435	1852	1300
EU-PORSCHE-911-997-GT2-COUPE-01	4469	1852	1285
EU-PORSCHE-911-997-TARGA-4-01	4427	1852	1310
EU-PORSCHE-911-997-TARGA-4S-01	4427	1852	1300
EU-PORSCHE-911-997-TURBO-CONVERTIBLE-01	4450	1852	1300
EU-PORSCHE-911-997-TURBO-COUPE-01	4450	1852	1300
EU-RENAULT-CLIO-III-GRANDTOUR-WAGON-5D-01	4202	1707	1497
EU-RENAULT-MEGANE-III-COUPE-FACELIFT1-01	4299	1785	1423
EU-RENAULT-MEGANE-III-COUPE-FACELIFT2-01	4299	1848	1435
EU-RENAULT-MEGANE-III-COUPE-PREFL-01	4299	1804	1435
EU-RENAULT-MEGANE-III-GRANDTOUR-PHASE-III-01	4567	1804	1507
EU-RENAULT-MEGANE-III-GRANDTOUR-PHASE-I-II-01	4559	1804	1507
EU-RENAULT-MEGANE-III-HATCHBACK-FACELIFT-5D-01	4295	1808	1471
EU-RENAULT-MEGANE-III-HATCHBACK-PREFL-5D-01	4295	1808	1491
EU-RENAULT-TRAFIC-II-BUS-L1H1-01	4782	1904	1955
EU-RENAULT-TRAFIC-II-BUS-L2H1-01	5182	1904	1962
EU-RENAULT-TRAFIC-II-PH2-VAN-LWB-HIGHROOF-01	5182	1904	2464
EU-RENAULT-TRAFIC-II-PH2-VAN-LWB-LOWROOF-01	5182	1904	1969
EU-RENAULT-TRAFIC-II-PH2-VAN-SWB-LOWROOF-01	4782	1904	1960
EU-RENAULT-TRAFIC-II-PLATFORM-CAB-L2-01	5036	1904	1973
EU-RENAULT-TRAFIC-II-PLATFORM-CAB-LWB-01	5038	1904	1967
EU-RENAULT-TRAFIC-II-VAN-L1H1-01	4782	1904	1955
EU-RENAULT-TRAFIC-II-VAN-L1H2-01	4782	1904	2465
EU-RENAULT-TRAFIC-II-VAN-L2H1-01	5182	1904	1962
EU-RENAULT-TRAFIC-II-VAN-L2H2-01	5182	1904	2464
EU-SEAT-IBIZA-IV-6J5-HATCHBACK-5D-PREFL-01	4052	1693	1445
EU-SEAT-IBIZA-IV-6J-HATCHBACK-3D-FACELIFT-01	4043	1693	1428
EU-SEAT-IBIZA-IV-6J-HATCHBACK-3D-PREFL-01	4072	1693	1428
EU-SEAT-LEON-I-1M-HATCHBACK-01	4184	1742	1439
EU-SEAT-LEON-II-HATCHBACK-5D-01	4315	1768	1458
EU-SEAT-LEON-II-HATCHBACK-FACELIFT-01	4323	1768	1458
EU-SEAT-LEON-II-HATCHBACK-FR-01	4323	1768	1458
EU-SEAT-LEON-II-HATCHBACK-PREFL-01	4315	1768	1458
EU-SEAT-LEON-III-ST-WAGON-01	4535	1816	1454
EU-SKODA-OCTAVIA-I-1U2-HATCHBACK-FACELIFT-01	4507	1731	1431
EU-SKODA-OCTAVIA-I-1U5-WAGON-FACELIFT-01	4513	1731	1457
EU-SKODA-OCTAVIA-II-1Z5-WAGON-FACELIFT-01	4569	1769	1462
EU-SKODA-OCTAVIA-II-1Z5-WAGON-PREFL-01	4572	1769	1468
EU-SKODA-OCTAVIA-II-HATCHBACK-5D-01	4572	1769	1462
EU-SKODA-OCTAVIA-II-HATCHBACK-5D-FACELIFT-01	4569	1769	1462
EU-SKODA-OCTAVIA-II-HATCHBACK-5D-PREFL-01	4578	1769	1462
EU-SKODA-OCTAVIA-II-HATCHBACK-RS-FACELIFT-01	4569	1769	1462
EU-SKODA-OCTAVIA-II-HATCHBACK-RS-PREFL-01	4578	1769	1462
EU-SKODA-OCTAVIA-II-WAGON-5D-01	4572	1769	1468
EU-SKODA-OCTAVIA-II-WAGON-5D-FACELIFT-01	4569	1769	1462
EU-SKODA-OCTAVIA-II-WAGON-5D-PREFL-01	4572	1769	1468
EU-SKODA-OCTAVIA-II-WAGON-RS-FACELIFT-01	4599	1769	1451
EU-SKODA-OCTAVIA-II-WAGON-RS-PREFL-01	4572	1769	1468
EU-SUBARU-IMPREZA-II-FACELIFT-SEDAN-01	4465	1740	1440
EU-SUBARU-IMPREZA-II-GD-SEDAN-FACELIFT1-01	4415	1740	1440
EU-SUBARU-IMPREZA-II-GD-SEDAN-PREFL-01	4405	1730	1440
EU-SUBARU-IMPREZA-II-GG-WAGON-FACELIFT-STANDARD-01	4465	1695	1485
EU-SUBARU-IMPREZA-II-GG-WAGON-FACELIFT-WRX-01	4465	1695	1465
EU-SUBARU-IMPREZA-III-GH-HATCHBACK-5D-01	4415	1740	1475
EU-SUBARU-IMPREZA-II-SEDAN-FACELIFT-01	4465	1740	1440
EU-SUBARU-IMPREZA-II-WAGON-FACELIFT-01	4465	1695	1485
EU-VOLVO-S70-SEDAN-01	4720	1760	1400
EU-VOLVO-V70-II-FACELIFT-WAGON-01	4710	1804	1465
EU-VOLVO-V70-II-FACELIFT-WAGON-AWD-01	4710	1804	1514
EU-VOLVO-V70-III-FACELIFT-WAGON-5D-01	4814	1907	1547
EU-VOLVO-V70-III-WAGON-5D-PREFL-01	4823	1861	1547
EU-VOLVO-V70-II-WAGON-FACELIFT-01	4710	1804	1465
EU-VOLVO-V70-I-WAGON-5D-01	4730	1760	1430
EU-VW-GOLF-PLUS-V-HATCHBACK-5D-01	4206	1759	1580
EU-VW-GOLF-PLUS-VI-MPV-FACELIFT-01	4204	1759	1592
EU-VW-GOLF-PLUS-V-MPV-PREFL-01	4206	1759	1592
EU-VW-GOLF-VI-5K1-HATCHBACK-3D-01	4199	1779	1479
EU-VW-GOLF-VI-5K1-HATCHBACK-5D-01	4199	1786	1480
EU-VW-GOLF-VI-CABRIOLET-2D-01	4246	1782	1423
EU-VW-GOLF-VII-VARIANT-WAGON-5D-PREFL-01	4575	1799	1481
EU-VW-GOLF-VI-PLUS-MPV-5D-01	4204	1759	1592
EU-VW-PASSAT-B6-3C2-SEDAN-01	4765	1820	1472
EU-VW-PASSAT-B6-3C5-WAGON-01	4774	1820	1517
EU-VW-PASSAT-B6-R36-SEDAN-01	4806	1820	1447
EU-VW-PASSAT-B6-R36-WAGON-01	4820	1820	1456
EU-VW-PASSAT-B6-SEDAN-4D-01	4765	1820	1472
EU-VW-PASSAT-B6-VARIANT-WAGON-01	4774	1820	1517
EU-VW-PASSAT-B6-WAGON-5D-01	4774	1820	1517
EU-VW-POLO-9N3-HATCHBACK-3D-01	3916	1650	1467
EU-VW-POLO-9N3-HATCHBACK-5D-01	3916	1650	1467
EU-VW-POLO-III-6V2-CLASSIC-SEDAN-4D-01	4140	1640	1410
EU-VW-POLO-IV-FACELIFT-HATCHBACK-3D-01	3916	1650	1467
EU-VW-POLO-IV-FACELIFT-HATCHBACK-3D-02	3916	1650	1459
EU-VW-POLO-IV-FACELIFT-HATCHBACK-5D-01	3897	1650	1465
EU-VW-POLO-IV-FACELIFT-HATCHBACK-5D-02	3916	1650	1459
EU-VW-POLO-IV-HATCHBACK-3D-FACELIFT-GTI-01	3916	1650	1459
EU-VW-POLO-IV-HATCHBACK-5D-FACELIFT-GTI-01	3897	1650	1465

【TSV 数据】
Make	Model	VariantName	BodyStyle	DriveType	Energy	EngineOutputKW	EngineOutputHP	Product Start Month-Year	Product End Month-Year	LastProcessedDate	Ktype
Skoda	Octavia	1.8 TSI 4X4	Kombi	Allrad	Benzin	118	160	Nov 2008	Feb 2013	2024-03-01	31594
VW	Passat b6	1.6 TDI	Stufenheck	Frontantrieb	Diesel	77	105	Aug 2009	Jul 2010	2024-03-01	31595
VW	Passat b6 variant	1.6 TDI	Kombi	Frontantrieb	Diesel	77	105	Aug 2009	Nov 2010	2024-03-01	31596
Seat	Ibiza iv	1.4 TSI	Schrägheck	Frontantrieb	Benzin	110	150	Jun 2009	May 2015	2024-03-01	31599
Seat	Ibiza iv	1.6 TDI	Schrägheck	Frontantrieb	Diesel	66	90	May 2009	May 2015	2024-03-01	31600
Seat	Ibiza iv sc	1.2	Schrägheck	Frontantrieb	Benzin	44	60	Jul 2009	May 2015	2025-06-01	31601
Seat	Ibiza iv sc	1.4 TSI	Schrägheck	Frontantrieb	Benzin	110	150	Jan 2009	May 2015	2025-06-01	31602
Seat	Ibiza iv sc	1.4 TSI Cupra	Schrägheck	Frontantrieb	Benzin	132	180	Jun 2009	May 2015	2025-06-01	31603
Seat	Ibiza iv sc	1.6 TDI	Schrägheck	Frontantrieb	Diesel	66	90	May 2009	May 2015	2025-06-01	31604
VW	Golf plus v	1.6 TDI	Schrägheck	Frontantrieb	Diesel	77	105	Mar 2009	Dec 2013	2024-03-01	31605
VW	Polo	1.6 TDI	Schrägheck	Frontantrieb	Diesel	66	90	Jun 2009	May 2014	2024-03-01	31606
VW	Polo	1.6 TDI	Schrägheck	Frontantrieb	Diesel	77	105	Jun 2009	Aug 2015	2024-03-01	31607
Fiat	Ducato	140 Natural Power	Bus	Frontantrieb	CNG	100	136	Apr 2009	-	2024-03-01	31608
Fiat	Croma	1.9 D Multijet	Kombi	Frontantrieb	Diesel	85	115	Jun 2005	Dec 2011	2024-03-01	31616
Alfa Romeo	147	1.9 Jtdm 16V	Schrägheck	Frontantrieb	Diesel	125	170	Jun 2008	Mar 2010	2024-03-01	31643
Alfa Romeo	Gt	1.9 JTD	Coupe	Frontantrieb	Diesel	125	170	May 2008	Sep 2010	2024-03-01	31644
Alfa Romeo	Mito	1.4 Tjet	Schrägheck	Frontantrieb	Benzin	88	120	Aug 2008	Aug 2013	2024-03-01	31645
Alfa Romeo	Mito	1.3 Multijet	Schrägheck	Frontantrieb	Diesel	66	90	Aug 2008	Aug 2010	2024-03-01	31646
Hummer	Hummer h2	6.0 AWD	Geländewagen geschlossen	Allrad	Benzin	242	329	Oct 2004	Dec 2009	2024-03-01	31649
Subaru	Impreza	2.5 AWD	Stufenheck	Allrad	Benzin	169	230	Oct 2008	-	2024-03-01	31653
Mazda	Cx-7	2.3 Disi	SUV	Frontantrieb	Benzin	177	241	Jun 2006	Jun 2009	2024-03-01	31654
Porsche	911	3.6 Carrera	Coupe	Heckantrieb	Benzin	235	320	Aug 2004	Jul 2005	2024-03-01	31660
Porsche	911	3.6 Carrera	Cabriolet	Heckantrieb	Benzin	235	320	Apr 2005	Jul 2005	2024-03-01	31661
Volvo	V70 i	2.3	Kombi	Frontantrieb	Benzin	177	241	Nov 1996	Nov 2000	2024-03-01	31666
Bentley	Arnage	6.8 V8 T	Stufenheck	Heckantrieb	Benzin	373	507	Feb 2002	Oct 2009	2024-03-01	31669
BMW	1	116 I	Schrägheck	Heckantrieb	Benzin	90	122	Nov 2008	Dec 2011	2024-03-01	31671
BMW	1	116 D	Schrägheck	Heckantrieb	Diesel	85	116	Nov 2008	Dec 2011	2024-03-01	31672
BMW	1	130 I	Schrägheck	Heckantrieb	Benzin	190	258	Sep 2006	Dec 2011	2024-03-01	31673
Renault	Megane iii	1.6 16V Bifuel	Coupe	Frontantrieb	Benzin/Autogas (LPG)	81	110	Nov 2008	Aug 2015	2024-03-01	31692
Renault	Megane iii	1.6 16V Hi-flex	Schrägheck	Frontantrieb	Benzin/Ethanol	81	110	Nov 2008	Aug 2015	2024-03-01	31693
Renault	Megane iii grandtour	1.6 Bifuel	Kombi	Frontantrieb	Benzin/Autogas (LPG)	81	110	Nov 2008	Aug 2015	2024-03-01	31695
Seat	Leon	1.6 LPG	Schrägheck	Frontantrieb	Benzin/Autogas (LPG)	75	102	Dec 2009	Dec 2012	2024-03-01	31708
Lexus	Is c	250	Cabriolet	Heckantrieb	Benzin	153	208	Apr 2009	Jun 2015	2024-03-01	31715
Renault	Megane iii	2.0 DCI	Coupe	Frontantrieb	Diesel	110	150	Apr 2009	Aug 2015	2024-03-01	31717
Renault	Clio iii grandtour	1.6 16V	Kombi	Frontantrieb	Benzin	94	128	Nov 2007	Dec 2012	2026-05-01	31718
Renault	Fluence	1.6 16V	Stufenheck	Frontantrieb	Benzin	81	110	Feb 2010	-	2024-03-01	31722
Renault	Fluence	2.0 16V	Stufenheck	Frontantrieb	Benzin	103	140	Feb 2010	-	2024-03-01	31723
Renault	Fluence	1.5 DCI	Stufenheck	Frontantrieb	Diesel	66	90	Feb 2010	-	2024-03-01	31724
Renault	Fluence	1.5 DCI	Stufenheck	Frontantrieb	Diesel	81	110	Feb 2010	-	2024-03-01	31725
Peugeot	407	2.0 HDI	Coupe	Frontantrieb	Diesel	120	163	Jun 2009	-	2024-03-01	31727
Peugeot	407	3.0 HDI	Coupe	Frontantrieb	Diesel	177	241	Jun 2009	-	2024-03-01	31728
Peugeot	5008	1.6 16V	Großraumlimousine	Frontantrieb	Benzin	88	120	Sep 2009	Mar 2017	2024-03-01	31733
Peugeot	5008	1.6 16V	Großraumlimousine	Frontantrieb	Benzin	115	156	Sep 2009	Mar 2017	2024-03-01	31734
Peugeot	5008	1.6 HDI	Großraumlimousine	Frontantrieb	Diesel	80	110	Sep 2009	Mar 2017	2024-03-01	31737
Peugeot	5008	2.0 HDI 150 / Bluehdi 150	Großraumlimousine	Frontantrieb	Diesel	110	150	Jun 2009	Mar 2017	2024-03-01	31739
Peugeot	5008	2.0 HDI	Großraumlimousine	Frontantrieb	Diesel	120	163	Sep 2009	Mar 2017	2024-03-01	31740
Citroën	C3 picasso	1.6 HDI	Großraumlimousine	Frontantrieb	Diesel	66	90	Feb 2009	Mar 2015	2024-08-01	31742
Citroën	C4 picasso i	2.0 HDI 150	Großraumlimousine	Frontantrieb	Diesel	110	150	Jul 2009	Aug 2013	2024-03-01	31743
Citroën	C4 grand picasso i	2.0 HDI 150	Großraumlimousine	Frontantrieb	Diesel	110	150	Jul 2009	Aug 2013	2024-03-01	31745
Ford Australia	Mustang	4	Coupe	Heckantrieb	Benzin	157	214	Sep 2004	Jul 2014	2024-03-01	31819
Ford Australia	Mustang	4.6 V8	Coupe	Heckantrieb	Benzin	224	305	Sep 2004	Jul 2014	2024-03-01	31820
Audi	Q5	2.0 Tfsi Quattro	SUV	Allrad	Benzin	132	180	Aug 2009	May 2017	2024-03-01	31955
Audi	Q5	2.0 TDI Quattro	SUV	Allrad	Diesel	105	143	Aug 2009	May 2013	2024-03-01	31956
Audi	Q5	2.0 TDI Quattro	SUV	Allrad	Diesel	100	136	Aug 2009	May 2017	2024-03-01	31957
Cadillac	Cts	6.2	Stufenheck	Heckantrieb	Benzin	415	564	Jan 2009	-	2024-03-01	31958
Audi	Q5	2.0 TDI Quattro	SUV	Allrad	Diesel	120	163	Nov 2008	May 2017	2024-03-01	31959
BMW	X5	M	SUV	Allrad	Benzin	408	555	Jul 2009	Jul 2013	2024-03-01	31960
BMW	X6	M	SUV	Allrad	Benzin	408	555	Jul 2009	Jul 2014	2024-03-01	31961
Audi	Q5	3.0 TDI Quattro	SUV	Allrad	Diesel	155	211	Nov 2008	Sep 2012	2024-03-01	31962
Volvo	S70	2.3	Stufenheck	Frontantrieb	Benzin	177	241	Nov 1996	Nov 2000	2024-03-01	31963
Skoda	Superb ii	2.0 TDI 16V	Schrägheck	Frontantrieb	Diesel	103	140	Jan 2009	May 2015	2024-03-01	31965
Opel	Corsa d	1.2 LPG	Schrägheck	Frontantrieb	Benzin/Autogas (LPG)	59	80	Aug 2006	Aug 2014	2024-03-01	31968
Opel	Corsa d	1.4	Schrägheck	Frontantrieb	Benzin	64	87	Sep 2009	Aug 2014	2024-03-01	31969
VW	Passat cc b6	2.0 Bluetdi	Coupe	Frontantrieb	Diesel	105	143	May 2009	Nov 2010	2024-03-01	31972
VW	Passat cc b6	2.0 TDI 4motion	Coupe	Allrad	Diesel	103	140	Aug 2009	Jan 2012	2024-03-01	31974
VW	Golf vi	2.0 TDI 4motion	Schrägheck	Allrad	Diesel	103	140	May 2009	Nov 2012	2024-03-01	31992
Citroën	C2	1.4	Schrägheck	Frontantrieb	Benzin	55	75	Oct 2006	Dec 2009	2024-03-01	31995
Renault	Trafic ii	2.5 DCI	Kasten	Frontantrieb	Diesel	84	114	Aug 2007	-	2024-03-01	31996
Citroën	C5	2.0 HDI 140	Stufenheck	Frontantrieb	Diesel	103	140	Nov 2008	Jun 2015	2024-07-01	31997
Citroën	C5	2.0 HDI 140	Kombi	Frontantrieb	Diesel	103	140	Apr 2009	Jun 2015	2024-07-01	31998
Citroën	C5	3.0 HDI 240	Stufenheck	Frontantrieb	Diesel	177	241	Apr 2009	Oct 2014	2024-07-01	31999
Citroën	C5	3.0 HDI 240	Kombi	Frontantrieb	Diesel	177	241	Apr 2009	Oct 2014	2024-07-01	32000
Hyundai	ii	2.7 V6	Coupe	Frontantrieb	Benzin	121	165	Jan 2001	Aug 2009	2024-03-01	32001
Opel	Astra h gtc	1.7 Cdti	Schrägheck	Frontantrieb	Diesel	59	80	Mar 2005	Oct 2010	2024-03-01	32003
Opel	Corsa b caravan	1.4 I 16V	Kombi	Frontantrieb	Benzin	66	90	Jan 1999	Dec 2002	2024-03-01	32004
Opel	Corsa b caravan	1.7 D	Kombi	Frontantrieb	Diesel	44	60	Jan 1999	Dec 2002	2024-03-01	32005
Mini	Mini	John Cooper Works	Schrägheck	Frontantrieb	Benzin	155	211	Nov 2007	Nov 2013	2024-03-01	32009
Mini	Mini	John Cooper Works	Cabriolet	Frontantrieb	Benzin	155	211	Aug 2008	May 2015	2024-03-01	32010
Mini	Mini	John Cooper Works	Kombi	Frontantrieb	Benzin	155	211	Nov 2007	Jun 2014	2024-03-01	32012
Toyota	Urban cruiser	1.33	Schrägheck	Frontantrieb	Benzin	74	101	Apr 2009	Mar 2016	2024-03-01	32024
Toyota	Urban cruiser	1.4 D-4d	Schrägheck	Frontantrieb	Diesel	66	90	Jan 2009	Apr 2014	2024-03-01	32025
Toyota	Urban cruiser	1.4 D-4d 4WD	Schrägheck	Allrad	Diesel	66	90	Jan 2009	Apr 2014	2024-03-01	32026
Citroën	C3 ii	1.1 I	Schrägheck	Frontantrieb	Benzin	44	60	Sep 2009	Jan 2013	2024-03-01	32027
Citroën	C3 ii	1.4	Schrägheck	Frontantrieb	Benzin	54	73	Nov 2009	Sep 2016	2024-03-01	32028
Citroën	C3 ii	1.4 VTI 95	Schrägheck	Frontantrieb	Benzin	70	95	Nov 2009	Sep 2016	2024-07-01	32029
Citroën	C3 ii	1.6 VTI 120	Schrägheck	Frontantrieb	Benzin	88	120	Nov 2009	Sep 2016	2024-07-01	32030
Citroën	C3 ii	1.6 HDI	Schrägheck	Frontantrieb	Diesel	68	92	Nov 2009	Sep 2016	2024-03-01	32031
Citroën	C3 ii	1.6 HDI 110	Schrägheck	Frontantrieb	Diesel	82	112	Nov 2009	Sep 2016	2024-07-01	32032
Citroën	Ds3	1.4 VTI 95	Schrägheck	Frontantrieb	Benzin	70	95	Apr 2010	Jul 2015	2024-03-01	32033
Citroën	Ds3	1.6 VTI 120	Schrägheck	Frontantrieb	Benzin	88	120	Apr 2010	Jul 2015	2024-03-01	32034
Citroën	Ds3	1.6 THP 155	Schrägheck	Frontantrieb	Benzin	115	156	Apr 2010	Jul 2015	2024-03-01	32035
Citroën	Ds3	1.6 HDI 90	Schrägheck	Frontantrieb	Diesel	68	92	Nov 2009	Jul 2015	2024-03-01	32036
Citroën	Ds3	1.6 HDI 110	Schrägheck	Frontantrieb	Diesel	82	112	Nov 2009	Jul 2015	2024-03-01	32037
Peugeot	Rcz	1.6 16V	Coupe	Frontantrieb	Benzin	115	156	Mar 2010	Dec 2015	2024-03-01	32038
Peugeot	Rcz	1.6 16V	Coupe	Frontantrieb	Benzin	147	200	Jun 2010	Dec 2015	2024-03-01	32039
Peugeot	Rcz	2.0 HDI	Coupe	Frontantrieb	Diesel	120	163	Mar 2010	Dec 2015	2024-03-01	32040
KIA	Venga	1.4 Cvvt	Schrägheck	Frontantrieb	Benzin	66	90	Feb 2010	Mar 2019	2024-05-01	32041
KIA	Venga	1.6 Cvvt	Schrägheck	Frontantrieb	Benzin	92	125	Feb 2010	Mar 2019	2024-05-01	32042
KIA	Venga	1.4 Crdi 90	Schrägheck	Frontantrieb	Diesel	66	90	Feb 2010	Mar 2019	2024-05-01	32043
KIA	Venga	1.6 Crdi 128	Schrägheck	Frontantrieb	Diesel	94	128	Feb 2010	Mar 2019	2024-05-01	32044


--- 脚本异常 ---
异常: 对话分支失败（已尝试 3 次）: 没有找到最后一条用户消息的【在新聊天中分支】入口


--- 发送 / checkpoint 续跑到 Round 2 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_4001-4100_ktype_dimension_mapping_final.tsv
- all_4001-4100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 2 / checkpoint 续跑 ---
## 更新点

* 本轮新增/修改 **44 条 Ktype 映射**，首次创建并闭合 **19 个尺寸组**。重点完成 BMW 1 Series E81/E87 门数拆分、Citroën C3 II 改款前后拆分、Superb II 和 Venga 改款拆分，以及 Q5 facelift、X5 M、X6 M、Passat CC、Urban Cruiser 前驱/四驱等尺寸组。BMW E87 页面同时明确区分五门车身及不含后视镜宽度。([汽车数据网][1])
* Alfa Romeo GT、Hummer H2、Porsche 911 Carrera Cabriolet、Lexus IS 250C、Hyundai Coupe II 等独立外廓已经闭合。([汽车数据网][2])
* RCZ 暂不落盘：厂商规格表只直接列出含后视镜宽度，而其他规格源虽给出不含后视镜宽度，但长度和高度存在市场口径差异，尚需一次组级冲突处理。([bluelightcars.co.uk][3])

## 当前批次进度

* 当前派生映射总数：136
* READY 映射：111
* PENDING 映射：25
* 本轮首次创建尺寸组：19
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
31644	31644	Coupe	Alfa Romeo GT	937	2	EU-ALFA-ROMEO-GT-937-COUPE-2D-01	HIGH	937双门Coupe外廓。	READY
31649	31649	SUV	Hummer H2 I		5	EU-HUMMER-H2-I-SUV-5D-01	HIGH	封闭式五门SUV外廓。	READY
31661	31661	Convertible	911 997	997	2	EU-PORSCHE-911-997-CARRERA-CONVERTIBLE-RWD-01	HIGH	后驱Carrera Cabriolet外廓。	READY
31671_3dr	31671	Hatchback	1 Series E81	E81	3	EU-BMW-1-SERIES-E81-HATCHBACK-3D-01	MEDIUM	按E81三门物理分支拆分。	READY
31671_5dr	31671	Hatchback	1 Series E87	E87	5	EU-BMW-1-SERIES-E87-HATCHBACK-5D-01	MEDIUM	按E87五门物理分支拆分。	READY
31672_3dr	31672	Hatchback	1 Series E81	E81	3	EU-BMW-1-SERIES-E81-HATCHBACK-3D-01	MEDIUM	按E81三门物理分支拆分。	READY
31672_5dr	31672	Hatchback	1 Series E87	E87	5	EU-BMW-1-SERIES-E87-HATCHBACK-5D-01	MEDIUM	按E87五门物理分支拆分。	READY
31673_3dr	31673	Hatchback	1 Series E81	E81	3	EU-BMW-1-SERIES-E81-HATCHBACK-3D-01	MEDIUM	按E81三门物理分支拆分。	READY
31673_5dr	31673	Hatchback	1 Series E87	E87	5	EU-BMW-1-SERIES-E87-HATCHBACK-5D-01	MEDIUM	按E87五门物理分支拆分。	READY
31715	31715	Convertible	IS C	GSE20	2	EU-LEXUS-IS-C-GSE20-CONVERTIBLE-2D-01	HIGH	IS 250C双门硬顶敞篷外廓。	READY
31742_facelift	31742	MPV	C3 Picasso I Phase II		5	EU-CITROEN-C3-PICASSO-I-PHASE-II-MPV-5D-01	HIGH	2013改款外廓。	READY
31955_facelift	31955	SUV	Q5 8R	8R	5	EU-AUDI-Q5-8R-SUV-5D-FACELIFT-01	HIGH	2012改款外廓。	READY
31956_facelift	31956	SUV	Q5 8R	8R	5	EU-AUDI-Q5-8R-SUV-5D-FACELIFT-01	HIGH	2012改款外廓。	READY
31957_facelift	31957	SUV	Q5 8R	8R	5	EU-AUDI-Q5-8R-SUV-5D-FACELIFT-01	HIGH	2012改款外廓。	READY
31959_facelift	31959	SUV	Q5 8R	8R	5	EU-AUDI-Q5-8R-SUV-5D-FACELIFT-01	HIGH	2012改款外廓。	READY
31960	31960	SUV	X5 E70 M	E70	5	EU-BMW-X5-E70-M-SUV-5D-01	HIGH	X5 M专属外廓。	READY
31961	31961	SUV	X6 E71 M	E71	5	EU-BMW-X6-E71-M-SUV-5D-01	HIGH	X6 M专属外廓。	READY
31965_prefl	31965	Hatchback	Superb II	3T4	5	EU-SKODA-SUPERB-II-3T4-LIFTBACK-PREFL-01	HIGH	改款前TwinDoor外廓。	READY
31965_facelift	31965	Hatchback	Superb II	3T4	5	EU-SKODA-SUPERB-II-3T4-LIFTBACK-FACELIFT-01	HIGH	2013改款TwinDoor外廓。	READY
31972	31972	Coupe	Passat CC B6	357	4	EU-VW-PASSAT-CC-B6-357-COUPE-4D-01	HIGH	357四门Coupe外廓。	READY
31974	31974	Coupe	Passat CC B6	357	4	EU-VW-PASSAT-CC-B6-357-COUPE-4D-01	HIGH	357四门Coupe外廓。	READY
32001	32001	Coupe	Coupe II	GK	3	EU-HYUNDAI-COUPE-II-GK-COUPE-3D-01	HIGH	GK三门Coupe外廓。	READY
32024	32024	SUV	Urban Cruiser I	XP110	5	EU-TOYOTA-URBAN-CRUISER-XP110-SUV-FWD-01	HIGH	前驱标准高度外廓。	READY
32025	32025	SUV	Urban Cruiser I	XP110	5	EU-TOYOTA-URBAN-CRUISER-XP110-SUV-FWD-01	HIGH	前驱标准高度外廓。	READY
32026	32026	SUV	Urban Cruiser I	XP110	5	EU-TOYOTA-URBAN-CRUISER-XP110-SUV-AWD-01	HIGH	四驱增高外廓。	READY
32027	32027	Hatchback	C3 II Phase I		5	EU-CITROEN-C3-II-PHASE-I-HATCHBACK-5D-01	HIGH	改款前五门外廓。	READY
32028_prefl	32028	Hatchback	C3 II Phase I		5	EU-CITROEN-C3-II-PHASE-I-HATCHBACK-5D-01	HIGH	改款前五门外廓。	READY
32028_facelift	32028	Hatchback	C3 II Phase II		5	EU-CITROEN-C3-II-PHASE-II-HATCHBACK-5D-01	HIGH	2013改款五门外廓。	READY
32029_prefl	32029	Hatchback	C3 II Phase I		5	EU-CITROEN-C3-II-PHASE-I-HATCHBACK-5D-01	HIGH	改款前五门外廓。	READY
32029_facelift	32029	Hatchback	C3 II Phase II		5	EU-CITROEN-C3-II-PHASE-II-HATCHBACK-5D-01	HIGH	2013改款五门外廓。	READY
32030_prefl	32030	Hatchback	C3 II Phase I		5	EU-CITROEN-C3-II-PHASE-I-HATCHBACK-5D-01	HIGH	改款前五门外廓。	READY
32030_facelift	32030	Hatchback	C3 II Phase II		5	EU-CITROEN-C3-II-PHASE-II-HATCHBACK-5D-01	HIGH	2013改款五门外廓。	READY
32031_prefl	32031	Hatchback	C3 II Phase I		5	EU-CITROEN-C3-II-PHASE-I-HATCHBACK-5D-01	HIGH	改款前五门外廓。	READY
32031_facelift	32031	Hatchback	C3 II Phase II		5	EU-CITROEN-C3-II-PHASE-II-HATCHBACK-5D-01	HIGH	2013改款五门外廓。	READY
32032_prefl	32032	Hatchback	C3 II Phase I		5	EU-CITROEN-C3-II-PHASE-I-HATCHBACK-5D-01	HIGH	改款前五门外廓。	READY
32032_facelift	32032	Hatchback	C3 II Phase II		5	EU-CITROEN-C3-II-PHASE-II-HATCHBACK-5D-01	HIGH	2013改款五门外廓。	READY
32041_prefl	32041	MPV	Venga YN	YN	5	EU-KIA-VENGA-YN-MPV-PREFL-01	HIGH	改款前外廓。	READY
32041_facelift	32041	MPV	Venga YN	YN	5	EU-KIA-VENGA-YN-MPV-FACELIFT-01	HIGH	2014改款外廓。	READY
32042_prefl	32042	MPV	Venga YN	YN	5	EU-KIA-VENGA-YN-MPV-PREFL-01	HIGH	改款前外廓。	READY
32042_facelift	32042	MPV	Venga YN	YN	5	EU-KIA-VENGA-YN-MPV-FACELIFT-01	HIGH	2014改款外廓。	READY
32043_prefl	32043	MPV	Venga YN	YN	5	EU-KIA-VENGA-YN-MPV-PREFL-01	HIGH	改款前外廓。	READY
32043_facelift	32043	MPV	Venga YN	YN	5	EU-KIA-VENGA-YN-MPV-FACELIFT-01	HIGH	2014改款外廓。	READY
32044_prefl	32044	MPV	Venga YN	YN	5	EU-KIA-VENGA-YN-MPV-PREFL-01	HIGH	改款前外廓。	READY
32044_facelift	32044	MPV	Venga YN	YN	5	EU-KIA-VENGA-YN-MPV-FACELIFT-01	HIGH	2014改款外廓。	READY
```

## 本轮新增/修改的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-ALFA-ROMEO-GT-937-COUPE-2D-01	4480	1760	1390	Auto-Data	https://www.auto-data.net/ro/alfa-romeo-gt-coupe-937-2.0-i-16v-jts-165hp-1348
EU-HUMMER-H2-I-SUV-5D-01	4820	2063	2080	Auto-Data	https://www.auto-data.net/en/hummer-h2-gmt-840-6.0i-v8-329hp-29733
EU-PORSCHE-911-997-CARRERA-CONVERTIBLE-RWD-01	4427	1808	1310	Auto-Data	https://www.auto-data.net/en/porsche-911-cabriolet-997-carrera-3.6-325hp-6587
EU-BMW-1-SERIES-E87-HATCHBACK-5D-01	4239	1748	1421	Auto-Data	https://www.auto-data.net/en/bmw-1-series-hatchback-5dr-e87-lci-facelift-2007-116d-115hp-27369
EU-LEXUS-IS-C-GSE20-CONVERTIBLE-2D-01	4635	1800	1415	Automobile-Catalog	https://www.automobile-catalog.com/car/2012/1427615/lexus_is_250c.html
EU-CITROEN-C3-PICASSO-I-PHASE-II-MPV-5D-01	4101	1766	1631	Auto-Data	https://www.auto-data.net/en/citroen-c3-i-picasso-phase-ii-2013-1.6-hdi-92hp-21044
EU-AUDI-Q5-8R-SUV-5D-FACELIFT-01	4629	1898	1655	Auto-Data	https://www.auto-data.net/en/audi-q5-i-8r-facelift-2012-2.0-tdi-150hp-quattro-dpf-19165
EU-BMW-X5-E70-M-SUV-5D-01	4851	1994	1764	Auto-Data	https://www.auto-data.net/en/bmw-x5-m-e70-4.4-555hp-xdrive-steptronic-9771
EU-BMW-X6-E71-M-SUV-5D-01	4876	1983	1684	Auto-Data	https://www.auto-data.net/en/bmw-x6-m-e71-4.4-v8-555hp-steptronic-9762
EU-SKODA-SUPERB-II-3T4-LIFTBACK-PREFL-01	4838	1817	1462	Auto-Data	https://www.auto-data.net/en/skoda-superb-ii-2.0-tdi-pd-140hp-dpf-17424
EU-SKODA-SUPERB-II-3T4-LIFTBACK-FACELIFT-01	4833	1817	1462	Auto-Data	https://www.auto-data.net/en/skoda-superb-ii-facelift-2013-2.0-tdi-140hp-dpf-19295
EU-VW-PASSAT-CC-B6-357-COUPE-4D-01	4799	1855	1417	Auto-Data	https://www.auto-data.net/en/volkswagen-passat-cc-i-2.0-tdi-bmt-140hp-16846
EU-HYUNDAI-COUPE-II-GK-COUPE-3D-01	4395	1760	1330	Auto-Data	https://www.auto-data.net/en/hyundai-coupe-ii-gk-2.7-i-v6-24v-167hp-13841
EU-TOYOTA-URBAN-CRUISER-XP110-SUV-FWD-01	3930	1725	1525	Auto-Data	https://www.auto-data.net/en/toyota-urban-cruiser-i-1.4-d-4d-90hp-4x2-18511
EU-TOYOTA-URBAN-CRUISER-XP110-SUV-AWD-01	3930	1725	1540	Auto-Data	https://www.auto-data.net/en/toyota-urban-cruiser-i-1.4-d-4d-90hp-4x4-3755
EU-CITROEN-C3-II-PHASE-I-HATCHBACK-5D-01	3941	1728	1524	Auto-Data	https://www.auto-data.net/en/citroen-c3-ii-phase-i-2009-1.4-vti-95hp-27451
EU-CITROEN-C3-II-PHASE-II-HATCHBACK-5D-01	3941	1728	1538	Auto-Data	https://www.auto-data.net/en/citroen-c3-ii-phase-ii-2013-1.4-puretech-95hp-etg-start-stop-27458
EU-KIA-VENGA-YN-MPV-PREFL-01	4068	1765	1600	Auto-Data	https://www.auto-data.net/en/kia-venga-yn-1.4-16v-90hp-17089
EU-KIA-VENGA-YN-MPV-FACELIFT-01	4075	1765	1600	Auto-Data	https://www.auto-data.net/en/kia-venga-yn-facelift-2014-1.4-90hp-23781
```

## 下一步优先处理

1. 解决 RCZ、DS3 的不含后视镜宽度及版本高度口径。
2. 闭合 Mustang S197、Fluence、Ducato Bus、Trafic Van 的改款、轴距和车顶分支。
3. 处理 Ibiza/Polo 门数分支，以及 MINI JCW、Corsa B Caravan 的专属外廓。

推进信号：CONTINUE

[1]: https://www.auto-data.net/en/bmw-1-series-hatchback-5dr-e87-lci-facelift-2007-116d-115hp-27369 "https://www.auto-data.net/en/bmw-1-series-hatchback-5dr-e87-lci-facelift-2007-116d-115hp-27369"
[2]: https://www.auto-data.net/ro/alfa-romeo-gt-coupe-937-2.0-i-16v-jts-165hp-1348 "https://www.auto-data.net/ro/alfa-romeo-gt-coupe-937-2.0-i-16v-jts-165hp-1348"
[3]: https://www.bluelightcars.co.uk/wp-content/uploads/peugeot-rcz-prices-and-specifications-brochure.pdf "https://www.bluelightcars.co.uk/wp-content/uploads/peugeot-rcz-prices-and-specifications-brochure.pdf"


--- 发送 / 继续到 Round 3 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_4001-4100_ktype_dimension_mapping_final.tsv
- all_4001-4100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 3 / checkpoint 续跑 ---
## 更新点

* 本轮消除 14 个 Ktype 的阻塞，新增 24 条 READY 派生映射。
* 已闭合 Ibiza IV/SC 的改款及 FR、Cupra 外廓，Polo V 的三门/五门分支，Mustang S197 改款前后外廓，以及 MINI JCW Hatch、Convertible、Clubman。([汽车数据网][1])
* Golf VI Plus 与 MINI R57 JCW 直接关联已有尺寸组，本轮不重复输出其尺寸组。([汽车数据网][2])
* 本轮首次创建 14 个 DIMENSION_GROUP。

## 当前批次进度

* 当前派生映射总数：146
* READY 映射：135
* PENDING 映射：11
* 本轮首次创建尺寸组：14
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
31599_prefl	31599	Hatchback	Ibiza IV	6J5	5	EU-SEAT-IBIZA-IV-6J5-HATCHBACK-5D-FR-PREFL-01	HIGH	改款前FR五门外廓。	READY
31599_facelift	31599	Hatchback	Ibiza IV Facelift	6J5	5	EU-SEAT-IBIZA-IV-6J5-HATCHBACK-5D-FR-FACELIFT-01	HIGH	2012改款FR五门外廓。	READY
31600_prefl	31600	Hatchback	Ibiza IV	6J5	5	EU-SEAT-IBIZA-IV-6J5-HATCHBACK-5D-PREFL-01	HIGH	改款前五门外廓。	READY
31600_facelift	31600	Hatchback	Ibiza IV Facelift	6J5	5	EU-SEAT-IBIZA-IV-6J5-HATCHBACK-5D-FACELIFT-01	HIGH	2012改款五门外廓。	READY
31601_prefl	31601	Hatchback	Ibiza IV SC	6J	3	EU-SEAT-IBIZA-IV-6J-HATCHBACK-3D-STANDARD-PREFL-01	HIGH	改款前标准三门外廓。	READY
31601_facelift	31601	Hatchback	Ibiza IV SC Facelift	6J	3	EU-SEAT-IBIZA-IV-6J-HATCHBACK-3D-FACELIFT-01	HIGH	2012改款标准三门外廓。	READY
31602_prefl	31602	Hatchback	Ibiza IV SC	6J	3	EU-SEAT-IBIZA-IV-6J-HATCHBACK-3D-FR-PREFL-01	HIGH	改款前FR三门外廓。	READY
31602_facelift	31602	Hatchback	Ibiza IV SC Facelift	6J	3	EU-SEAT-IBIZA-IV-6J-HATCHBACK-3D-FR-FACELIFT-01	HIGH	2012改款FR三门外廓。	READY
31603_prefl	31603	Hatchback	Ibiza IV SC	6J	3	EU-SEAT-IBIZA-IV-6J-HATCHBACK-3D-CUPRA-PREFL-01	HIGH	改款前Cupra三门外廓。	READY
31603_facelift	31603	Hatchback	Ibiza IV SC Facelift	6J	3	EU-SEAT-IBIZA-IV-6J-HATCHBACK-3D-CUPRA-FACELIFT-01	HIGH	2012改款Cupra三门外廓。	READY
31604_prefl	31604	Hatchback	Ibiza IV SC	6J	3	EU-SEAT-IBIZA-IV-6J-HATCHBACK-3D-STANDARD-PREFL-01	HIGH	改款前标准三门外廓。	READY
31604_facelift	31604	Hatchback	Ibiza IV SC Facelift	6J	3	EU-SEAT-IBIZA-IV-6J-HATCHBACK-3D-FACELIFT-01	HIGH	2012改款标准三门外廓。	READY
31605	31605	MPV	Golf VI Plus	5M	5	EU-VW-GOLF-VI-PLUS-MPV-5D-01	HIGH	五门Golf Plus外廓。	READY
31606_3dr	31606	Hatchback	Polo V	6R	3	EU-VW-POLO-V-6R-HATCHBACK-3D-01	MEDIUM	Ktype覆盖三门物理分支。	READY
31606_5dr	31606	Hatchback	Polo V	6R	5	EU-VW-POLO-V-6R-HATCHBACK-5D-01	MEDIUM	Ktype覆盖五门物理分支。	READY
31607_3dr	31607	Hatchback	Polo V	6R	3	EU-VW-POLO-V-6R-HATCHBACK-3D-01	MEDIUM	Ktype覆盖三门物理分支。	READY
31607_5dr	31607	Hatchback	Polo V	6R	5	EU-VW-POLO-V-6R-HATCHBACK-5D-01	MEDIUM	Ktype覆盖五门物理分支。	READY
31819_prefl	31819	Coupe	Mustang V	S197	2	EU-FORD-MUSTANG-V-S197-COUPE-2D-PREFL-01	MEDIUM	改款前双门外廓。	READY
31819_facelift	31819	Coupe	Mustang V Facelift	S197	2	EU-FORD-MUSTANG-V-S197-COUPE-2D-FACELIFT-01	MEDIUM	2009改款双门外廓。	READY
31820_prefl	31820	Coupe	Mustang V	S197	2	EU-FORD-MUSTANG-V-S197-COUPE-2D-PREFL-01	MEDIUM	改款前GT双门外廓。	READY
31820_facelift	31820	Coupe	Mustang V Facelift	S197	2	EU-FORD-MUSTANG-V-S197-COUPE-2D-FACELIFT-01	MEDIUM	2009改款GT双门外廓。	READY
32009	32009	Hatchback	MINI R56	R56	3	EU-MINI-MINI-R56-HATCHBACK-JCW-3D-01	HIGH	JCW三门外廓。	READY
32010	32010	Convertible	MINI R57	R57	2	EU-MINI-MINI-R57-CONVERTIBLE-COOPER-S-01	HIGH	JCW双门敞篷外廓。	READY
32012	32012	Wagon	MINI Clubman R55	R55	5	EU-MINI-MINI-R55-CLUBMAN-WAGON-JCW-5D-01	HIGH	JCW Clubman五门外廓。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-SEAT-IBIZA-IV-6J5-HATCHBACK-5D-FR-PREFL-01	4088	1693	1441	Auto-Data	https://www.auto-data.net/en/seat-ibiza-iv-fr-1.4-tsi-150hp-dsg-16885
EU-SEAT-IBIZA-IV-6J5-HATCHBACK-5D-FR-FACELIFT-01	4082	1693	1441	Auto-Data	https://www.auto-data.net/en/seat-ibiza-iv-facelift-2012-fr-1.4-tsi-150hp-dsg-16876
EU-SEAT-IBIZA-IV-6J5-HATCHBACK-5D-FACELIFT-01	4061	1693	1445	Auto-Data	https://www.auto-data.net/en/seat-ibiza-iv-facelift-2012-1.6-tdi-90hp-16883
EU-SEAT-IBIZA-IV-6J-HATCHBACK-3D-STANDARD-PREFL-01	4034	1693	1428	Auto-Data; Automobile-Catalog	https://www.auto-data.net/en/seat-ibiza-iv-sc-1.2-60hp-44349; https://www.automobile-catalog.com/car/2009/3094805/seat_ibiza_sc_1_6_tdi_cr_90.html
EU-SEAT-IBIZA-IV-6J-HATCHBACK-3D-FR-PREFL-01	4072	1693	1424	Auto-Data	https://www.auto-data.net/en/seat-ibiza-iv-sc-fr-1.4-tsi-150hp-dsg-16887
EU-SEAT-IBIZA-IV-6J-HATCHBACK-3D-FR-FACELIFT-01	4066	1693	1424	Auto-Data	https://www.auto-data.net/en/seat-ibiza-iv-sc-facelift-2012-fr-1.4-tsi-150hp-dsg-16889
EU-SEAT-IBIZA-IV-6J-HATCHBACK-3D-CUPRA-PREFL-01	4063	1693	1420	Auto-Data	https://www.auto-data.net/en/seat-ibiza-iv-sc-cupra-1.4-tsi-180hp-13467
EU-SEAT-IBIZA-IV-6J-HATCHBACK-3D-CUPRA-FACELIFT-01	4055	1693	1420	Auto-Data	https://www.auto-data.net/en/seat-ibiza-iv-sc-facelift-2012-cupra-1.4-tsi-180hp-dsg-16888
EU-VW-POLO-V-6R-HATCHBACK-3D-01	3970	1682	1462	Auto-Data	https://www.auto-data.net/en/volkswagen-polo-v-3-door-1.6-tdi-90hp-52470
EU-VW-POLO-V-6R-HATCHBACK-5D-01	3970	1682	1462	Auto-Data	https://www.auto-data.net/en/volkswagen-polo-v-5-door-1.6-tdi-90hp-16815
EU-FORD-MUSTANG-V-S197-COUPE-2D-PREFL-01	4765	1875	1385	Auto-Data	https://www.auto-data.net/en/ford-mustang-v-gt-4.6i-v8-304hp-7775
EU-FORD-MUSTANG-V-S197-COUPE-2D-FACELIFT-01	4778	1877	1412	Auto-Data	https://www.auto-data.net/en/ford-mustang-v-facelift-2009-gt-4.6-v8-315hp-46035
EU-MINI-MINI-R56-HATCHBACK-JCW-3D-01	3714	1683	1407	Auto-Data	https://www.auto-data.net/en/mini-hatch-r56-jcw-1.6-211hp-21504
EU-MINI-MINI-R55-CLUBMAN-WAGON-JCW-5D-01	3958	1683	1432	Auto-Data	https://www.auto-data.net/en/mini-clubman-r55-jcw-1.6-211hp-automatic-21584
```

## 下一步优先处理

1. 闭合 DS3 与 RCZ 的不含后视镜宽度及版本高度口径。
2. 拆分 Ducato Bus 与 Trafic Van 的轴距、车顶高度分支。
3. 处理 Subaru Impreza 230 HP、Corsa B Caravan 及剩余车型边界。

推进信号：CONTINUE

[1]: https://www.auto-data.net/en/seat-ibiza-iv-fr-1.4-tsi-150hp-dsg-16885 "Seat Ibiza IV FR 1.4 TSI (150 Hp) DSG | Technical specs, data, fuel consumption, Dimensions"
[2]: https://www.auto-data.net/en/volkswagen-golf-vi-plus-1.6-tdi-105hp-17906 "Volkswagen Golf VI Plus 1.6 TDI (105 Hp) | Technical specs, data, fuel consumption, Dimensions"


--- 发送 / 继续到 Round 4 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_4001-4100_ktype_dimension_mapping_final.tsv
- all_4001-4100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 4 / checkpoint 续跑 ---
## 更新点

* 本轮新增/修改 **11 条 READY 映射**，首次创建 **3 个尺寸组**。
* 修正 Subaru Ktype 31653 的车身边界：该 Ktype 对应 GHE 五门掀背车，不按输入中的 `Stufenheck` 落盘，直接复用已有 Impreza III GH 尺寸组。
* 闭合 Corsa B Caravan F35、Citroën DS3 I 和 Peugeot RCZ I。DS3 各动力版本统一为 `3948 × 1715 × 1458 mm`；RCZ 改款前后核得相同的无镜宽度及三维，可共用稳定尺寸组。([汽车目录][1])

## 当前批次进度

* 按输入 Ktype 计：READY **98/100**
* PENDING **2/100**
* 剩余 PENDING：`31608`、`31996`
* 本轮新增/修改 READY 映射：11
* 本轮首次创建尺寸组：3
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
31653	31653	Hatchback	Impreza III	GHE	5	EU-SUBARU-IMPREZA-III-GH-HATCHBACK-5D-01	HIGH	输入车身形式与GHE实际车身不一致，按五门掀背修正。	READY
32004	32004	Wagon	Corsa B Caravan	F35	5	EU-OPEL-CORSA-B-F35-WAGON-5D-01	HIGH	F35五门Caravan外廓。	READY
32005	32005	Wagon	Corsa B Caravan	F35	5	EU-OPEL-CORSA-B-F35-WAGON-5D-01	HIGH	F35五门Caravan外廓。	READY
32033	32033	Hatchback	DS3 I		3	EU-CITROEN-DS3-I-HATCHBACK-3D-01	HIGH	三门掀背外廓。	READY
32034	32034	Hatchback	DS3 I		3	EU-CITROEN-DS3-I-HATCHBACK-3D-01	HIGH	三门掀背外廓。	READY
32035	32035	Hatchback	DS3 I		3	EU-CITROEN-DS3-I-HATCHBACK-3D-01	HIGH	三门掀背外廓。	READY
32036	32036	Hatchback	DS3 I		3	EU-CITROEN-DS3-I-HATCHBACK-3D-01	HIGH	三门掀背外廓。	READY
32037	32037	Hatchback	DS3 I		3	EU-CITROEN-DS3-I-HATCHBACK-3D-01	HIGH	三门掀背外廓。	READY
32038	32038	Coupe	RCZ I		2	EU-PEUGEOT-RCZ-I-COUPE-2D-01	HIGH	双门Coupe外廓。	READY
32039	32039	Coupe	RCZ I		2	EU-PEUGEOT-RCZ-I-COUPE-2D-01	HIGH	双门Coupe外廓。	READY
32040	32040	Coupe	RCZ I		2	EU-PEUGEOT-RCZ-I-COUPE-2D-01	HIGH	双门Coupe外廓。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-OPEL-CORSA-B-F35-WAGON-5D-01	4026	1610	1470	Auto-Data	https://www.auto-data.net/en/opel-corsa-b-kasten-generation-527
EU-CITROEN-DS3-I-HATCHBACK-3D-01	3948	1715	1458	Automobile-Catalog	https://www.automobile-catalog.com/car/2010/1214150/citroen_ds3_vti_120_sochic.html
EU-PEUGEOT-RCZ-I-COUPE-2D-01	4287	1845	1359	Automobile-Catalog (2010 RCZ THP 200); Automobile-Catalog (2013 RCZ THP 156)	https://www.automobile-catalog.com/car/2010/2623205/peugeot_rcz_1_6_thp_200.html; https://www.automobile-catalog.com/car/2013/2623115/peugeot_rcz_1_6_thp_156.html
```

## 下一步优先处理

1. 确认 `31608` Ducato Natural Power Minibus 实际覆盖的轴距和车顶分支。
2. 确认 `31996` Trafic II Van 的 `FL0R/FL0V` 是否覆盖 SWB/LWB、低顶/高顶多个物理外廓。
3. 两项闭合后立即执行一次机械检查并输出两张最终完整 TSV、指定下载链接及 `COMPLETE`。

推进信号：CONTINUE

[1]: https://www.automobile-catalog.com/car/2010/1214150/citroen_ds3_vti_120_sochic.html?utm_source=chatgpt.com "2010 Citroen DS3 VTi 120 SoChic (DStyle) (man. 5)"


--- 发送 / 继续到 Round 5 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_4001-4100_ktype_dimension_mapping_final.tsv
- all_4001-4100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 5 / checkpoint 续跑 ---
## 更新点

* `31996` 已按 Trafic II Phase II 的短轴低顶、长轴低顶两个物理分支拆分并闭合；该 84 kW 版本资料对应 L1H1 与 L2H1，未将高顶分支猜测性纳入。([Autodoc][1])
* `31608` 仍未闭合。Fiat 官方资料确认 140 Natural Power 同时提供 Combinato、Panorama、Minibus 等多种配置，但尚未获得能够把该 Bus Ktype 精确限定到具体轴距和车顶组合的配置矩阵，因此不能直接任选或全量套用已有三个 Bus 尺寸组。([Stellantis Media][2])

## 当前批次进度

* READY Ktype：99/100
* PENDING Ktype：1/100
* 剩余 PENDING：`31608`
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
31996_swb_lowroof	31996	Van	Trafic II Phase II	FL		EU-RENAULT-TRAFIC-II-PH2-VAN-SWB-LOWROOF-01	MEDIUM	Ktype覆盖短轴低顶物理分支。	READY
31996_lwb_lowroof	31996	Van	Trafic II Phase II	FL		EU-RENAULT-TRAFIC-II-PH2-VAN-LWB-LOWROOF-01	MEDIUM	Ktype覆盖长轴低顶物理分支。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

无

## 下一步优先处理

1. 仅核对 `31608` Fiat Ducato 250 Bus 140 Natural Power 的原厂配置矩阵或型式批准资料。
2. 确认其实际覆盖的轴距和车顶分支后，直接关联已有 Ducato III Bus 尺寸组；若三维不一致，则按规则创建下一序号新组。
3. `31608` 闭合后立即执行一次机械检查并输出两张最终完整 TSV及指定下载链接。

推进信号：CONTINUE

[1]: https://www.autodoc.parts/car-parts/battery-10142/renault/trafic/trafic-ii-box-fl/31996-2-5-dci?utm_source=chatgpt.com "Renault Trafic FL 2.5 dCi Battery (114 hp Diesel G9U 630)"
[2]: https://www.media.stellantis.com/it-it/fiat-professional/press/arriva-il-nuovo-fiat-ducato-alimentato-a-metano "Arriva il nuovo Fiat Ducato alimentato a metano | FIAT Professional | Stellantis Media"


--- 发送 / 继续到 Round 6 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_4001-4100_ktype_dimension_mapping_final.tsv
- all_4001-4100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- 脚本异常 ---
异常: 对话分支失败（已尝试 3 次）: 没有找到最后一条用户消息的【在新聊天中分支】入口

