# 任务：all 第 2501-2600 行
# 来源文件：all.tsv
# 任务 ID：all__batch__0026__bf43a22a


--- 发送 / 首次任务 ---
【任务名称】
【全量表更新】all 第 2501-2600 行

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
all 第 2501-2600 行

【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2501-2600_ktype_dimension_mapping_final.tsv
- all_2501-2600_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。

【跨批次已有尺寸组索引】
以下 ID 已经存在于累计表。三维和物理外廓完全相同时才可复用；如果当前证据得到不同三维，禁止改写已有组，必须使用同系列下一个可用序号创建新 DIMENSION_GROUP_ID，并把当前批次相关 Ktype 全部指向新组。

DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM
EU-ALFA-ROMEO-156-932-FACELIFT-WAGON-01	4441	1743	1390
EU-ALFA-ROMEO-156-932-SEDAN-FACELIFT-01	4435	1743	1430
EU-ALFA-ROMEO-156-932-SEDAN-PREFL-01	4430	1745	1415
EU-AUDI-A3-8PA-HATCHBACK-5D-01	4286	1765	1423
EU-AUDI-A3-8P-HATCHBACK-3D-01	4214	1765	1421
EU-AUDI-A3-8P-HATCHBACK-3D-FACELIFT-01	4238	1765	1421
EU-AUDI-A3-8P-HATCHBACK-3D-PREFL-01	4214	1765	1421
EU-AUDI-A3-II-CABRIOLET-2D-01	4238	1765	1424
EU-AUDI-A3-II-HATCHBACK-3D-FACELIFT-01	4238	1765	1421
EU-AUDI-A3-II-HATCHBACK-3D-PREFL-01	4214	1765	1421
EU-AUDI-A3-II-HATCHBACK-5D-FACELIFT-01	4292	1765	1423
EU-AUDI-A3-II-HATCHBACK-5D-PREFL-01	4286	1765	1423
EU-AUDI-A4-B7-8E-AVANT-WAGON-5D-01	4586	1772	1427
EU-AUDI-A4-B7-CONVERTIBLE-01	4573	1777	1391
EU-AUDI-A4-B7-CONVERTIBLE-02	4570	1780	1390
EU-AUDI-A4-B7-SEDAN-01	4586	1772	1427
EU-AUDI-A4-B7-SEDAN-4D-01	4586	1772	1427
EU-AUDI-A4-B7-WAGON-01	4586	1772	1427
EU-AUDI-A4-B7-WAGON-5D-01	4586	1772	1453
EU-AUDI-A4-B7-WAGON-5D-02	4586	1772	1427
EU-BMW-3-E90-SEDAN-4D-FACELIFT-01	4531	1817	1421
EU-BMW-3-E90-SEDAN-4D-PREFL-01	4520	1817	1421
EU-BMW-3-E91-WAGON-5D-FACELIFT-01	4527	1817	1418
EU-BMW-3-E91-WAGON-5D-PREFL-01	4520	1817	1418
EU-BMW-3-E92-COUPE-2D-FACELIFT-01	4612	1782	1375
EU-BMW-3-E92-COUPE-2D-PREFL-01	4580	1782	1395
EU-BMW-3-E92-COUPE-FACELIFT-01	4612	1782	1395
EU-BMW-3-E92-COUPE-PREFL-01	4580	1782	1395
EU-BMW-3-E93-CONVERTIBLE-FACELIFT-01	4612	1782	1384
EU-BMW-3-E93-CONVERTIBLE-PREFL-01	4588	1782	1384
EU-BMW-3-SERIES-E46-CONVERTIBLE-FACELIFT-01	4488	1757	1372
EU-BMW-3-SERIES-E46-COUPE-FACELIFT-2D-01	4488	1757	1369
EU-BMW-3-SERIES-E46-SEDAN-FACELIFT-4D-01	4471	1739	1415
EU-BMW-3-SERIES-E46-WAGON-FACELIFT-5D-01	4480	1740	1410
EU-BMW-3-SERIES-E90-SEDAN-01	4520	1817	1421
EU-BMW-3-SERIES-E90-SEDAN-FACELIFT-4D-01	4531	1817	1421
EU-BMW-3-SERIES-E90-SEDAN-PREFL-4D-01	4520	1820	1420
EU-BMW-3-SERIES-E91-WAGON-FACELIFT-5D-01	4527	1817	1418
EU-BMW-3-SERIES-E91-WAGON-PREFL-01	4520	1817	1418
EU-BMW-3-SERIES-E91-WAGON-PREFL-5D-01	4520	1820	1440
EU-BMW-3-SERIES-E92-COUPE-2D-01	4580	1782	1395
EU-BMW-3-SERIES-E92-COUPE-FACELIFT-01	4612	1782	1395
EU-BMW-3-SERIES-E92-COUPE-PREFL-01	4580	1782	1395
EU-BMW-3-SERIES-E93-CONVERTIBLE-2D-PREFL-01	4580	1782	1384
EU-CHEVROLET-AVALANCHE-I-GMT800-PICKUP-4D-01	5629	2027	1869
EU-CHEVROLET-EXPRESS-I-CARGO-VAN-LWB-2500-01	6066	2012	2108
EU-CHEVROLET-EXPRESS-I-CARGO-VAN-SWB-1500-01	5558	2012	2068
EU-CHEVROLET-EXPRESS-I-CARGO-VAN-SWB-2500-01	5558	2012	2062
EU-CHEVROLET-TAHOE-I-SUV-2D-01	4788	1958	1839
EU-CHEVROLET-TAHOE-I-SUV-4D-01	5057	1941	1783
EU-CITROEN-C4-I-COUPE-3D-PHASE-I-01	4273	1769	1456
EU-DODGE-AVENGER-JS-SEDAN-01	4850	1843	1497
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
EU-FIAT-PUNTO-2012-HATCHBACK-01	4065	1687	1490
EU-FORD-FOCUS-II-CONVERTIBLE-01	4509	1834	1448
EU-FORD-FOCUS-II-HATCHBACK-FACELIFT-01	4337	1839	1500
EU-FORD-FOCUS-II-HATCHBACK-PREFL-01	4342	1840	1497
EU-FORD-FOCUS-II-SEDAN-01	4488	1840	1497
EU-FORD-FOCUS-II-ST-HATCHBACK-3D-01	4362	1840	1447
EU-FORD-FOCUS-II-ST-HATCHBACK-5D-01	4362	1840	1447
EU-FORD-FOCUS-II-WAGON-FACELIFT-01	4468	1839	1503
EU-FORD-FOCUS-II-WAGON-PREFL-01	4472	1840	1501
EU-FORD-USA-EXPLORER-III-U152-SUV-5D-01	4813	1831	1826
EU-KIA-SORENTO-I-FACELIFT-SUV-01	4590	1865	1811
EU-LAND-ROVER-DISCOVERY-III-L319-SUV-5D-01	4835	2009	1887
EU-LAND-ROVER-DISCOVERY-I-SUV-3D-01	4520	1795	1915
EU-LAND-ROVER-DISCOVERY-I-SUV-5D-01	4520	1795	1960
EU-LEXUS-GS-IV-SEDAN-01	4850	1840	1455
EU-MAZDA-626-V-GF-SEDAN-01	4575	1710	1430
EU-MAZDA-6-II-GH-HATCHBACK-01	4735	1795	1440
EU-MAZDA-6-II-GH-HATCHBACK-02	4755	1795	1440
EU-MAZDA-6-II-GH-HATCHBACK-03	4765	1795	1440
EU-MAZDA-6-II-GH-SEDAN-01	4755	1795	1440
EU-MAZDA-6-I-SEDAN-MPS-FACELIFT-01	4765	1780	1430
EU-MITSUBISHI-LANCER-VIII-CY0-SEDAN-4D-01	4570	1760	1490
EU-NISSAN-QUEST-III-V42-MPV-5D-01	5184	1971	1778
EU-OPEL-MOVANO-A-BUS-L1H1-01	4899	1990	2253
EU-OPEL-MOVANO-A-BUS-L2H2-01	5399	1990	2493
EU-OPEL-MOVANO-A-BUS-L3H3-01	5899	1990	2720
EU-OPEL-MOVANO-A-VAN-L1H1-01	4899	1990	2253
EU-OPEL-MOVANO-A-VAN-L1H2-01	4899	1990	2496
EU-OPEL-MOVANO-A-VAN-L2H2-01	5399	1990	2493
EU-OPEL-MOVANO-A-VAN-L3H2-01	5899	1990	2490
EU-OPEL-MOVANO-A-VAN-L3H3-01	5899	1990	2720
EU-OPEL-MOVANO-A-X70-CHASSIS-CAB-LWB-01	5869	1990	2195
EU-OPEL-MOVANO-A-X70-CHASSIS-CAB-MWB-01	5369	1990	2200
EU-OPEL-MOVANO-A-X70-CREW-CAB-LWB-01	5869	1990	2203
EU-OPEL-VIVARO-A-BUS-LWB-01	5182	1904	1960
EU-OPEL-VIVARO-A-BUS-SWB-01	4782	1904	1960
EU-OPEL-VIVARO-A-VAN-LWB-HIGHROOF-01	5182	1904	2492
EU-OPEL-VIVARO-A-VAN-LWB-LOWROOF-01	5182	1904	1960
EU-OPEL-VIVARO-A-VAN-SWB-HIGHROOF-01	4782	1904	2492
EU-OPEL-VIVARO-A-VAN-SWB-LOWROOF-01	4782	1904	1960
EU-PEUGEOT-4007-I-SUV-5D-01	4637	1808	1715
EU-PEUGEOT-807-MPV-01	4730	1850	1750
EU-RENAULT-CLIO-III-GRANDTOUR-WAGON-5D-01	4202	1707	1497
EU-RENAULT-CLIO-III-HATCHBACK-3D-01	3986	1707	1495
EU-RENAULT-CLIO-III-HATCHBACK-3D-02	3986	1719	1495
EU-RENAULT-CLIO-III-HATCHBACK-5D-01	3986	1707	1495
EU-RENAULT-CLIO-III-HATCHBACK-5D-02	3986	1719	1495
EU-RENAULT-CLIO-III-PHASE-I-HATCHBACK-3D-01	3986	1719	1495
EU-RENAULT-CLIO-III-PHASE-I-HATCHBACK-5D-01	3986	1719	1495
EU-RENAULT-CLIO-III-PHASE-II-HATCHBACK-3D-01	4032	1720	1497
EU-RENAULT-CLIO-III-PHASE-II-HATCHBACK-5D-01	4032	1720	1497
EU-RENAULT-CLIO-III-RS-HATCHBACK-3D-01	3991	1768	1477
EU-RENAULT-CLIO-II-PHASE-III-VAN-01	3811	1639	1417
EU-RENAULT-KOLEOS-I-SUV-PHASE-I-01	4520	1855	1695
EU-RENAULT-KOLEOS-I-SUV-PHASE-II-01	4520	1855	1695
EU-RENAULT-KOLEOS-I-SUV-PHASE-III-01	4520	1865	1695
EU-RENAULT-LAGUNA-II-FACELIFT-HATCHBACK-01	4576	1772	1429
EU-RENAULT-LAGUNA-II-GRANDTOUR-FACELIFT-WAGON-01	4695	1772	1443
EU-RENAULT-LAGUNA-II-GRANDTOUR-WAGON-FACELIFT-01	4695	1772	1443
EU-RENAULT-LAGUNA-III-HATCHBACK-5D-01	4695	1811	1445
EU-RENAULT-LAGUNA-III-WAGON-5D-01	4803	1811	1445
EU-RENAULT-LAGUNA-II-PHASE-I-HATCHBACK-01	4576	1772	1429
EU-RENAULT-LAGUNA-II-PHASE-I-WAGON-01	4695	1772	1443
EU-RENAULT-MEGANE-II-CC-PHASE-II-CONVERTIBLE-01	4355	1777	1404
EU-RENAULT-MEGANE-II-CC-PHASE-II-CONVERTIBLE-2D-01	4355	1777	1404
EU-RENAULT-MEGANE-II-CLASSIC-PHASE-II-SEDAN-4D-01	4498	1777	1460
EU-RENAULT-MEGANE-II-GRANDTOUR-PHASE-II-WAGON-5D-01	4500	1777	1467
EU-RENAULT-MEGANE-II-PHASE-II-CC-CONVERTIBLE-01	4355	1777	1404
EU-RENAULT-MEGANE-II-PHASE-II-GRANDTOUR-WAGON-01	4500	1777	1467
EU-RENAULT-MEGANE-II-PHASE-II-HATCHBACK-01	4228	1777	1458
EU-RENAULT-MEGANE-II-PHASE-II-HATCHBACK-3D-01	4209	1777	1458
EU-RENAULT-MEGANE-II-PHASE-II-HATCHBACK-5D-01	4209	1777	1458
EU-RENAULT-MEGANE-II-PHASE-II-SEDAN-01	4498	1777	1460
EU-SAAB-9-3-II-CONVERTIBLE-FACELIFT-01	4647	1780	1437
EU-SAAB-9-3-II-CONVERTIBLE-PREFL-01	4635	1762	1434
EU-SAAB-9-3-II-FACELIFT-SEDAN-4D-01	4647	1762	1450
EU-SAAB-9-3-II-FACELIFT-WAGON-5D-01	4670	1762	1496
EU-SAAB-9-3-II-SEDAN-01	4635	1762	1466
EU-SAAB-9-5-FACELIFT-2005-SEDAN-01	4836	1792	1448
EU-SAAB-9-5-FACELIFT-2005-WAGON-01	4841	1792	1459
EU-SEAT-LEON-I-1M-HATCHBACK-01	4184	1742	1439
EU-SEAT-LEON-II-HATCHBACK-5D-01	4315	1768	1458
EU-SEAT-LEON-II-HATCHBACK-FACELIFT-01	4323	1768	1458
EU-SEAT-LEON-II-HATCHBACK-FR-01	4323	1768	1458
EU-SEAT-LEON-II-HATCHBACK-PREFL-01	4315	1768	1458
EU-SEAT-LEON-III-ST-WAGON-01	4535	1816	1454
EU-SUZUKI-SWIFT-III-HATCHBACK-3D-01	3695	1690	1500
EU-SUZUKI-SWIFT-III-HATCHBACK-5D-01	3695	1690	1500
EU-TOYOTA-HIACE-IV-BUS-LWB-01	5240	1800	1995
EU-TOYOTA-HIACE-IV-BUS-SWB-01	4795	1800	2000
EU-TOYOTA-HIACE-IV-H100-VAN-LH102-SWB-01	4615	1690	1935
EU-TOYOTA-HIACE-IV-H100-VAN-LH112-LWB-01	4950	1690	1960
EU-TOYOTA-HIACE-IV-XH10-VAN-KLH18-01	4715	1800	1955
EU-TOYOTA-HIACE-IV-XH10-VAN-KLH28-01	5160	1800	1955
EU-VOLVO-C30-FACELIFT-HATCHBACK-3D-01	4266	1782	1447
EU-VOLVO-C30-I-HATCHBACK-3D-FACELIFT-01	4266	1782	1447
EU-VOLVO-C30-I-HATCHBACK-3D-PREFL-01	4252	1782	1447
EU-VOLVO-C30-PREFL-HATCHBACK-3D-01	4252	1782	1447
EU-VOLVO-S40-II-FACELIFT-SEDAN-4D-01	4476	1770	1454
EU-VOLVO-S40-II-SEDAN-01	4468	1770	1452
EU-VOLVO-S40-II-SEDAN-MS-01	4476	1770	1454
EU-VOLVO-S80-II-SEDAN-01	4851	1861	1493
EU-VOLVO-S80-II-SEDAN-4D-01	4851	1861	1493
EU-VOLVO-V50-FACELIFT-WAGON-5D-01	4522	1770	1457
EU-VOLVO-V50-I-WAGON-01	4510	1770	1450
EU-VOLVO-V50-MW-WAGON-FACELIFT-01	4522	1770	1457
EU-VOLVO-V50-MW-WAGON-PREFL-01	4514	1770	1452
EU-VOLVO-V70-III-FACELIFT-WAGON-5D-01	4814	1907	1547
EU-VOLVO-V70-III-WAGON-5D-PREFL-01	4823	1861	1547
EU-VW-GOLF-PLUS-V-HATCHBACK-5D-01	4206	1759	1580
EU-VW-GOLF-PLUS-VI-MPV-FACELIFT-01	4204	1759	1592
EU-VW-GOLF-PLUS-V-MPV-PREFL-01	4206	1759	1592
EU-VW-GOLF-V-VARIANT-WAGON-5D-01	4556	1781	1504
EU-VW-MULTIVAN-T5-MPV-SWB-01	4890	1904	1970
EU-VW-PASSAT-B6-3C2-SEDAN-01	4765	1820	1472
EU-VW-PASSAT-B6-3C5-WAGON-01	4774	1820	1517
EU-VW-PASSAT-B6-R36-SEDAN-01	4806	1820	1447
EU-VW-PASSAT-B6-R36-WAGON-01	4820	1820	1456
EU-VW-PASSAT-B6-SEDAN-4D-01	4765	1820	1472
EU-VW-PASSAT-B6-VARIANT-WAGON-01	4774	1820	1517
EU-VW-PASSAT-B6-WAGON-5D-01	4774	1820	1517
EU-VW-TRANSPORTER-T5-CHASSIS-CAB-LWB-01	5292	1904	1963
EU-VW-TRANSPORTER-T5-CHASSIS-CAB-LWB-02	5292	1904	1949
EU-VW-TRANSPORTER-T5-CHASSIS-DOUBLE-CAB-LWB-01	5292	1904	1949
EU-VW-TRANSPORTER-T5-DOUBLE-CAB-LWB-01	5292	1904	1963
EU-VW-TRANSPORTER-T5-LWB-HIGHROOF-01	5290	1904	2470
EU-VW-TRANSPORTER-T5-LWB-LOWROOF-01	5290	1904	1969
EU-VW-TRANSPORTER-T5-LWB-MEDROOF-01	5290	1904	2170
EU-VW-TRANSPORTER-T5-MPV-LWB-HIGHROOF-01	5290	1904	2460
EU-VW-TRANSPORTER-T5-MPV-LWB-LOWROOF-01	5290	1904	1959
EU-VW-TRANSPORTER-T5-MPV-LWB-MIDROOF-01	5290	1904	2160
EU-VW-TRANSPORTER-T5-MPV-SWB-LOWROOF-01	4890	1904	1959
EU-VW-TRANSPORTER-T5-MPV-SWB-MIDROOF-01	4890	1904	2160
EU-VW-TRANSPORTER-T5-SWB-LOWROOF-01	4890	1904	1969
EU-VW-TRANSPORTER-T5-SWB-MEDROOF-01	4890	1904	2170
EU-VW-TRANSPORTER-T5-VAN-LWB-HIGHROOF-01	5290	1904	2470
EU-VW-TRANSPORTER-T5-VAN-LWB-LOWROOF-01	5290	1904	1969
EU-VW-TRANSPORTER-T5-VAN-LWB-MEDROOF-01	5290	1904	2170
EU-VW-TRANSPORTER-T5-VAN-SWB-LOWROOF-01	4890	1904	1969
EU-VW-TRANSPORTER-T5-VAN-SWB-MEDROOF-01	4890	1904	2170

【TSV 数据】
Make	Model	VariantName	BodyStyle	DriveType	Energy	EngineOutputKW	EngineOutputHP	Product Start Month-Year	Product End Month-Year	LastProcessedDate	Ktype
VW	Jetta ii	1.8	Stufenheck	Frontantrieb	Benzin	70	95	Aug 1984	Jul 1988	2024-05-01	27224
VW	Jetta ii	1.8	Stufenheck	Frontantrieb	Benzin	77	105	Jan 1985	Dec 1992	2024-03-01	27225
Ford	Focus i turnier	1.8 Bifuel	Kombi	Frontantrieb	Benzin/Autogas (LPG)	82	111	Feb 2003	Jan 2005	2024-03-01	27247
Toyota	Hiace iv	2.4 D	Kasten	Heckantrieb	Diesel	55	75	Aug 1995	Aug 2001	2024-03-01	27275
Toyota	Hiace iv	2.5 D-4d 4WD	Kasten	Allrad	Diesel	65	88	Aug 2001	Aug 2004	2024-03-01	27276
Toyota	Hiace v	2.5 D-4d	Kasten	Heckantrieb	Diesel	70	95	Sep 2006	-	2024-03-01	27277
Toyota	Hiace iv	2.5 D-4d	Kasten	Heckantrieb	Diesel	86	117	Sep 2006	Dec 2012	2024-03-01	27278
Toyota	Hiace iv	2.5 D-4d 4WD	Kasten	Allrad	Diesel	86	117	Sep 2006	Dec 2012	2024-03-01	27279
Fiat	Ducato	1.9 TD	Pritsche/Fahrgestell	Frontantrieb	Diesel	59	80	May 1998	Nov 2001	2024-03-01	27281
Fiat	Ducato	2.5 TD 4X4	Pritsche/Fahrgestell	Allrad	Diesel	85	116	Nov 1994	Apr 1998	2024-03-01	27282
Seat	Leon	2.8	Schrägheck	Frontantrieb	Benzin	150	204	May 2002	Jun 2004	2024-03-01	27288
Alfa Romeo	156	1.9 JTD	Kombi	Frontantrieb	Diesel	93	126	Nov 2003	May 2006	2024-03-01	27296
Alfa Romeo	156	1.9 JTD	Kombi	Frontantrieb	Diesel	100	136	Nov 2002	Nov 2004	2024-03-01	27297
Alfa Romeo	156	2.0 JTS	Kombi	Frontantrieb	Benzin	119	162	Mar 2002	May 2006	2024-03-01	27298
Alfa Romeo	156	2.4 JTD	Kombi	Frontantrieb	Diesel	120	163	Jun 2003	May 2006	2024-03-01	27299
Land Rover	Discovery i	2.5 TDI 4X4	Geländewagen geschlossen	Allrad	Diesel	90	122	Jun 1993	Oct 1998	2024-03-01	27305
Fiat	Punto	1.4 Natural Power	Schrägheck	Frontantrieb	Benzin/Erdgas (CNG)	57	78	Mar 2012	-	2024-03-01	27308
Renault	Clio ii	1.5 DCI	Kasten/Schrägheck	Frontantrieb	Diesel	50	68	Apr 2004	-	2026-05-01	27313
Mazda	6	2.3	Stufenheck	Frontantrieb	Benzin	120	163	Mar 2005	Jul 2007	2024-03-01	27317
Audi	A4 b7	2.0 TDI	Stufenheck	Frontantrieb	Diesel	93	126	Nov 2005	Nov 2006	2024-03-01	27326
Renault	Clio iii	1.2 16V	Schrägheck	Frontantrieb	Benzin	43	58	Jun 2006	Aug 2010	2026-05-01	27329
Suzuki	Swift iii	1.3 4X4	Schrägheck	Allrad	Benzin	68	92	Feb 2005	Jun 2012	2026-05-01	27332
Dodge	Ram 1500	5.7 4X4	Pick-up	Allrad	Benzin	257	350	Oct 2008	-	2024-03-01	27337
VW	Cc b7	1.8 TSI	Coupe	Frontantrieb	Benzin	118	160	Nov 2011	Dec 2016	2024-03-01	27347
Chevrolet	Tahoe	5.7 AWD	SUV	Allrad	Benzin	184	250	Oct 1995	Sep 1996	2024-03-01	27352
VW	Transporter t5	2.0 TSI	Bus	Frontantrieb	Benzin	150	204	May 2011	Aug 2015	2024-03-01	27394
VW	Transporter t5	2.0 TSI 4motion	Bus	Allrad	Benzin	150	204	Jul 2011	Aug 2015	2024-03-01	27396
Mercedes-benz	S-Klasse	S 500 4-matic	Stufenheck	Allrad	Benzin	335	455	May 2013	May 2017	2024-03-01	27400
VW	Transporter t5	2.0 TSI	Kasten	Frontantrieb	Benzin	150	204	May 2011	Aug 2015	2024-03-01	27402
VW	Transporter t5	2.0 TSI 4motion	Kasten	Allrad	Benzin	150	204	Jul 2011	Aug 2015	2024-03-01	27403
VW	Multivan t5	2.0 TSI	Bus	Frontantrieb	Benzin	150	204	May 2011	Aug 2015	2024-03-01	27416
VW	Multivan t5	2.0 TSI 4motion	Bus	Allrad	Benzin	150	204	Jul 2011	Aug 2015	2024-03-01	27456
Opel	Insignia a sports tourer	2.0 Cdti	Kombi	Frontantrieb	Diesel	103	140	Jul 2013	Jun 2015	2024-03-01	27483
Nissan	Quest	3	Großraumlimousine	Frontantrieb	Benzin	113	154	May 1992	Sep 1998	2024-03-01	27496
Opel	Movano a	2.5 Cdti	Kasten	Frontantrieb	Diesel	74	101	Oct 2003	-	2024-03-01	27512
Opel	Movano a	2.5 Cdti	Pritsche/Fahrgestell	Frontantrieb	Diesel	74	101	Aug 2006	-	2024-03-01	27513
Opel	Vivaro a	2.0 16V	Pritsche/Fahrgestell	Frontantrieb	Benzin	88	120	Jan 2002	Jul 2006	2024-03-01	27517
Opel	Vivaro a	1.9 DTI	Pritsche/Fahrgestell	Frontantrieb	Diesel	74	101	Feb 2001	Dec 2010	2024-03-01	27518
KIA	Sorento i	3.3 V6 4WD	SUV	Allrad	Benzin	182	248	Feb 2007	Dec 2011	2024-03-01	27519
Suzuki	Splash	1	Schrägheck	Frontantrieb	Benzin	48	65	Jan 2008	-	2024-03-01	27528
Suzuki	Splash	1.2	Schrägheck	Frontantrieb	Benzin	63	86	Jan 2008	-	2024-03-01	27529
Suzuki	Splash	1.3 Cdti	Schrägheck	Frontantrieb	Diesel	55	75	Jan 2008	-	2024-03-01	27530
Renault	Laguna iii	2.0 DCI	Schrägheck	Frontantrieb	Diesel	127	173	Jan 2008	Dec 2015	2024-03-01	27531
Renault	Laguna iii grandtour	2.0 DCI	Kombi	Frontantrieb	Diesel	127	173	Jan 2008	Dec 2015	2024-03-01	27532
Renault	Laguna	3.0 DCI	Coupe	Frontantrieb	Diesel	173	235	Sep 2008	Dec 2015	2024-03-01	27533
Renault	Laguna	2.0 16V Turbo	Coupe	Frontantrieb	Benzin	125	170	Sep 2008	Dec 2015	2024-03-01	27534
Renault	Laguna	2.0 DCI	Coupe	Frontantrieb	Diesel	127	173	Sep 2008	Dec 2015	2024-03-01	27535
VW	Golf plus v	1.4 TSI	Schrägheck	Frontantrieb	Benzin	118	160	Jun 2008	Dec 2013	2024-03-01	27537
VW	Golf v variant	1.4 TSI	Kombi	Frontantrieb	Benzin	118	160	Jul 2008	Jul 2009	2024-03-01	27539
VW	Passat b6 variant	1.4 TSI	Kombi	Frontantrieb	Benzin	90	122	May 2007	Nov 2010	2024-03-01	27540
VW	Passat b6 variant	1.8 TSI	Kombi	Frontantrieb	Benzin	118	160	May 2007	Oct 2011	2024-03-01	27541
VW	Passat b6	1.4 TSI	Stufenheck	Frontantrieb	Benzin	90	122	May 2007	Jul 2010	2024-03-01	27544
VW	Passat b6	1.8 TSI	Stufenheck	Frontantrieb	Benzin	118	160	May 2007	Jul 2010	2024-03-01	27545
VW	Passat b6	2.0 TDI	Stufenheck	Frontantrieb	Diesel	100	136	Mar 2005	Nov 2010	2024-03-01	27547
Renault	Koleos i	2.5	SUV	Frontantrieb	Benzin	126	171	Sep 2008	-	2024-03-01	27548
Renault	Koleos i	2.5 4X4	SUV	Allrad	Benzin	126	171	Sep 2008	-	2024-03-01	27549
Renault	Laguna	3.5 V6	Coupe	Frontantrieb	Benzin	175	238	Sep 2008	Dec 2015	2024-03-01	27550
Nissan	Gt-R	V6	Coupe	Allrad	Benzin	357	486	Dec 2007	Oct 2010	2024-03-01	27551
Lexus	Gs	460	Stufenheck	Heckantrieb	Benzin	255	347	Sep 2007	Nov 2011	2024-03-01	27554
BMW	3	316 I	Stufenheck	Heckantrieb	Benzin	85	115	Sep 2005	Oct 2011	2024-03-01	27555
Audi	A3	S3 Quattro	Schrägheck	Allrad	Benzin	195	265	Jun 2008	Mar 2013	2024-03-01	27562
Audi	Q5	2.0 Tfsi Quattro	SUV	Allrad	Benzin	155	211	Nov 2008	Sep 2012	2024-03-01	27563
Audi	Q5	2.0 TDI Quattro	SUV	Allrad	Diesel	125	170	Nov 2008	Sep 2012	2024-03-01	27564
Audi	Q5	3.0 TDI Quattro	SUV	Allrad	Diesel	176	240	Nov 2008	May 2017	2024-03-01	27565
Chevrolet	Avalanche	5.3 Flex-fuel	Pick-up	Heckantrieb	Benzin/Ethanol	235	320	Jun 2005	Jul 2007	2024-03-01	27566
Chevrolet	Avalanche	5.3 Flex-fuel AWD	Pick-up	Allrad	Benzin/Ethanol	231	314	Jan 2007	Dec 2013	2024-03-01	27567
Mitsubishi	Lancer viii	1.5	Stufenheck	Frontantrieb	Benzin	80	109	Jun 2008	-	2024-03-01	27568
Peugeot	4007	2.4 16V	SUV	Allrad	Benzin	125	170	Feb 2007	Mar 2013	2024-03-01	27569
Peugeot	807	2.0 HDI	Großraumlimousine	Frontantrieb	Diesel	88	120	Feb 2006	-	2024-03-01	27570
Chevrolet	Express	5.3 Flex-fuel	Bus	Heckantrieb	Benzin/Ethanol	216	294	Jan 2007	-	2024-03-01	27571
Chevrolet	Silverado 1500	5.3 Flexfuel AWD	Pick-up	Allrad	Benzin/Ethanol	232	316	Jan 2007	-	2024-03-01	27572
Chevrolet	Silverado 1500	5.3 AWD	Pick-up	Allrad	Benzin	232	316	Jan 2007	-	2024-03-01	27573
Chevrolet	Silverado 2500 hd	6.6 TD 4WD	Pick-up	Allrad	Diesel	268	364	Jan 2007	Dec 2007	2024-03-01	27574
Chevrolet	Suburban	5.3 Flex-fuel 4WD	SUV	Allrad	Benzin/Ethanol	228	310	Jan 2007	-	2024-03-01	27575
Dacia	Sandero	1.4	Schrägheck	Frontantrieb	Benzin	55	75	Jun 2008	Dec 2012	2025-12-01	27576
Dacia	Sandero	1.6	Schrägheck	Frontantrieb	Benzin	64	87	Jun 2008	Dec 2012	2025-12-01	27577
Citroën	C4 i	1.6 16V Bio-flex	Schrägheck	Frontantrieb	Benzin/Ethanol	80	109	Sep 2007	Jul 2008	2024-03-01	27579
Dodge	Avenger	2.7 Flex-fuel	Stufenheck	Frontantrieb	Benzin/Ethanol	139	189	Jun 2007	Dec 2009	2024-03-01	27580
Ford	Focus i	1.6 16V Flexifuel	Schrägheck	Frontantrieb	Benzin/Ethanol	75	102	Jan 2002	Nov 2004	2024-03-01	27581
Ford USA	Explorer	4.0 Flex-fuel 4WD	SUV	Allrad	Benzin/Ethanol	156	212	Jan 2002	-	2024-03-01	27583
Seat	Ibiza iv	1.2	Schrägheck	Frontantrieb	Benzin	51	70	Mar 2008	May 2015	2024-03-01	27584
Seat	Ibiza iv	1.4	Schrägheck	Frontantrieb	Benzin	63	85	Mar 2008	May 2015	2024-03-01	27585
Seat	Ibiza iv	1.4 TDI	Schrägheck	Frontantrieb	Diesel	59	80	Jul 2008	Jun 2010	2024-03-01	27586
Seat	Ibiza iv	1.9 TDI	Schrägheck	Frontantrieb	Diesel	66	90	Jul 2008	Jun 2010	2024-03-01	27587
Renault	Megane ii grandtour	1.6 16V Hi-flex	Kombi	Frontantrieb	Benzin/Ethanol	77	105	Feb 2008	Jul 2009	2024-03-01	27598
Renault	Megane ii	1.6 Flex-fuel	Schrägheck	Frontantrieb	Benzin/Ethanol	77	105	Jan 2007	Feb 2008	2024-03-01	27599
Saab	9-3	2.0 T Biopower	Kombi	Frontantrieb	Benzin/Ethanol	110	150	Jan 2007	Feb 2015	2024-03-01	27600
Saab	9-3	2.0 T Biopower	Kombi	Frontantrieb	Benzin/Ethanol	129	175	Jan 2007	Feb 2015	2024-03-01	27601
Saab	9-3	2.0 T Biopower	Cabriolet	Frontantrieb	Benzin/Ethanol	129	175	Jan 2007	Feb 2015	2024-03-01	27611
Saab	9-3	1,8t Biopower	Stufenheck	Frontantrieb	Benzin/Ethanol	110	150	Jan 2007	Feb 2015	2024-03-01	27612
Saab	9-3	2.0 T Biopower	Stufenheck	Frontantrieb	Benzin/Ethanol	129	175	Jan 2007	Feb 2015	2024-03-01	27613
Saab	9-5	2.0 T Biopower	Stufenheck	Frontantrieb	Benzin/Ethanol	110	150	Jan 2005	Dec 2009	2024-03-01	27614
Saab	9-5	2.0 T Biopower	Kombi	Frontantrieb	Benzin/Ethanol	110	150	Jan 2006	Dec 2009	2024-03-01	27615
Volvo	C30	1.8 Flexfuel	Schrägheck	Frontantrieb	Benzin/Ethanol	92	125	Jan 2007	Dec 2012	2024-03-01	27618
Volvo	S40 ii	1.8 Flexfuel	Stufenheck	Frontantrieb	Benzin/Ethanol	92	125	Jan 2006	Dec 2010	2024-03-01	27619
Volvo	S80 ii	2.5 T Flexfuel	Stufenheck	Frontantrieb	Benzin/Ethanol	147	200	May 2008	Dec 2011	2024-03-01	27620
Volvo	S80 ii	2.0 Flexfuel	Stufenheck	Frontantrieb	Benzin/Ethanol	107	146	Jan 2008	Dec 2011	2024-03-01	27622
Volvo	V50	1.8 Flexfuel	Kombi	Frontantrieb	Benzin/Ethanol	92	125	Jan 2005	Dec 2010	2024-03-01	27624
Volvo	V70 iii	2.5 T Flexifuel	Kombi	Frontantrieb	Benzin/Ethanol	147	200	May 2008	Dec 2009	2024-03-01	27625
Volvo	V70 iii	2.0 Flexifuel	Kombi	Frontantrieb	Benzin/Ethanol	107	146	Jan 2008	Dec 2011	2024-03-01	27626


--- Round 1 / 首次发送 ---
## 更新点

* 按已有尺寸组索引完成缓存优先聚类，48 个输入 Ktype 已闭合，共形成 72 条 READY 映射，复用 61 个既有尺寸组。
* 已拆分门数、改款、轴距等明确影响外廓的分支，包括 Clio III、Discovery I、Tahoe I、Golf Plus、Koleos I、BMW E90、Audi S3、Saab 9-3、Volvo C30/S40/V50/V70 等。
* Jetta II 官方档案给出的车身高度为 1395–1415 mm 范围，无法直接确定当前两个 1.8 Ktype 的精确高度及两门/四门边界，因此暂不创建尺寸组。([Volkswagen Newsroom][1])
* 皮卡 Cab/Bed、商用车轴距/车顶，以及未出现在累计索引中的新车型尺寸组保持 PENDING，未用相近车型强行代替。

## 当前批次进度

* 输入 Ktype：100
* 已闭合 Ktype：48
* 待处理 Ktype：52
* READY 映射：72
* PENDING 映射：52
* 已引用既有尺寸组：61
* 本轮首次创建尺寸组：0
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27224	27224	Sedan	Jetta II				LOW	物理分支或尺寸组尚未闭合。	PENDING: 1.8 版本的精确高度与两门/四门物理边界尚未闭合。
27225	27225	Sedan	Jetta II				LOW	物理分支或尺寸组尚未闭合。	PENDING: 1.8 版本的精确高度与两门/四门物理边界尚未闭合。
27247	27247	Wagon	Focus I	DNW	5		LOW	物理分支或尺寸组尚未闭合。	PENDING: Focus I Turnier 三维及无后视镜宽度尚未建立尺寸组。
27275_swb	27275	Van	Hiace IV	XH10		EU-TOYOTA-HIACE-IV-XH10-VAN-KLH18-01	MEDIUM	XH10 短轴厢式车分支。	READY
27275_lwb	27275	Van	Hiace IV	XH10		EU-TOYOTA-HIACE-IV-XH10-VAN-KLH28-01	MEDIUM	XH10 长轴厢式车分支。	READY
27276	27276	Van	Hiace IV	XH10			LOW	物理分支或尺寸组尚未闭合。	PENDING: 4WD D-4D 对应的轴距/车身代码与高度分支未确认。
27277	27277	Van	Hiace V	H200			LOW	物理分支或尺寸组尚未闭合。	PENDING: Hiace V 欧洲厢式车的 SWB/LWB 与车顶分支尚未闭合。
27278	27278	Van	Hiace IV				LOW	物理分支或尺寸组尚未闭合。	PENDING: 输入代际标注与 2006–2012 年份冲突，需确认是否实际为 Hiace V/H200。
27279	27279	Van	Hiace IV				LOW	物理分支或尺寸组尚未闭合。	PENDING: 输入代际标注与 2006–2012 年份冲突，且 4WD 外廓分支未确认。
27281_swb	27281	Pickup	Ducato II X230	X230		EU-FIAT-DUCATO-X230-TRUCK-SWB-01	MEDIUM	X230 短轴平台/底盘分支。	READY
27281_mwb	27281	Pickup	Ducato II X230	X230		EU-FIAT-DUCATO-X230-TRUCK-MWB-01	MEDIUM	X230 中轴平台/底盘分支。	READY
27281_lwb	27281	Pickup	Ducato II X230	X230		EU-FIAT-DUCATO-X230-TRUCK-LWB-01	MEDIUM	X230 长轴平台/底盘分支。	READY
27282	27282	Pickup	Ducato II X230	X230			LOW	物理分支或尺寸组尚未闭合。	PENDING: 4X4 平台/底盘可用轴距分支未确认，不能直接套用全部 X230 组。
27288	27288	Hatchback	Leon I	1M	5	EU-SEAT-LEON-I-1M-HATCHBACK-01	HIGH	1M 五门外廓。	READY
27296	27296	Wagon	156 (932) facelift	932	5	EU-ALFA-ROMEO-156-932-FACELIFT-WAGON-01	HIGH	改款 Sportwagon 外廓。	READY
27297	27297	Wagon	156 (932)	932	5		LOW	物理分支或尺寸组尚未闭合。	PENDING: 生产期跨越 2003 改款，改款前 Sportwagon 尺寸组尚未建立。
27298	27298	Wagon	156 (932)	932	5		LOW	物理分支或尺寸组尚未闭合。	PENDING: 生产期跨越 2003 改款，需拆分改款前后并补建前期尺寸组。
27299	27299	Wagon	156 (932)	932	5		LOW	物理分支或尺寸组尚未闭合。	PENDING: 起始月份位于改款边界附近，前期/改款后外廓覆盖尚未闭合。
27305_3dr	27305	SUV	Discovery I		3	EU-LAND-ROVER-DISCOVERY-I-SUV-3D-01	HIGH	三门短车顶外廓。	READY
27305_5dr	27305	SUV	Discovery I		5	EU-LAND-ROVER-DISCOVERY-I-SUV-5D-01	HIGH	五门高车顶外廓。	READY
27308	27308	Hatchback	Punto 2012	199	5	EU-FIAT-PUNTO-2012-HATCHBACK-01	HIGH	Natural Power 五门外廓。	READY
27313	27313	Van	Clio II Phase III		3	EU-RENAULT-CLIO-II-PHASE-III-VAN-01	HIGH	商用厢式分支。	READY
27317	27317	Sedan	Mazda 6 I facelift	GG	4		LOW	物理分支或尺寸组尚未闭合。	PENDING: 标准 2.3 轿车不能复用 MPS 组，标准车三维尚未建立。
27326	27326	Sedan	A4 B7	8E	4	EU-AUDI-A4-B7-SEDAN-4D-01	HIGH	B7 四门轿车。	READY
27329_3dr_prefl	27329	Hatchback	Clio III Phase I		3	EU-RENAULT-CLIO-III-PHASE-I-HATCHBACK-3D-01	HIGH	3门；按改款边界拆分。	READY
27329_5dr_prefl	27329	Hatchback	Clio III Phase I		5	EU-RENAULT-CLIO-III-PHASE-I-HATCHBACK-5D-01	HIGH	5门；按改款边界拆分。	READY
27329_3dr_facelift	27329	Hatchback	Clio III Phase II		3	EU-RENAULT-CLIO-III-PHASE-II-HATCHBACK-3D-01	HIGH	3门；按改款边界拆分。	READY
27329_5dr_facelift	27329	Hatchback	Clio III Phase II		5	EU-RENAULT-CLIO-III-PHASE-II-HATCHBACK-5D-01	HIGH	5门；按改款边界拆分。	READY
27332	27332	Hatchback	Swift III		5	EU-SUZUKI-SWIFT-III-HATCHBACK-5D-01	MEDIUM	4X4 版本按五门外廓映射。	READY
27337	27337	Pickup	Ram 1500 IV				LOW	物理分支或尺寸组尚未闭合。	PENDING: Cab/Bed 组合及对应三维尚未拆分。
27347	27347	Coupe	Volkswagen CC	358	4		LOW	物理分支或尺寸组尚未闭合。	PENDING: CC B7 四门轿跑三维及来源尚未建立。
27352_2dr	27352	SUV	Tahoe I		2	EU-CHEVROLET-TAHOE-I-SUV-2D-01	HIGH	两门短轴外廓。	READY
27352_4dr	27352	SUV	Tahoe I		4	EU-CHEVROLET-TAHOE-I-SUV-4D-01	HIGH	四门长轴外廓。	READY
27394	27394	MPV	Transporter T5 facelift	7H	5		LOW	物理分支或尺寸组尚未闭合。	PENDING: Bus 的 SWB/LWB 与可用车顶组合尚未按 2.0 TSI 版本闭合。
27396	27396	MPV	Transporter T5 facelift	7H	5		LOW	物理分支或尺寸组尚未闭合。	PENDING: 4Motion Bus 的 SWB/LWB 与车顶组合尚未闭合。
27400	27400	Sedan	S-Class W222	W222	4		LOW	物理分支或尺寸组尚未闭合。	PENDING: S 500 4MATIC 的标准轴距/长轴版本边界尚未确认。
27402	27402	Van	Transporter T5 facelift	7H			LOW	物理分支或尺寸组尚未闭合。	PENDING: Kasten 的 SWB/LWB 与低/中/高顶组合尚未按 2.0 TSI 版本闭合。
27403	27403	Van	Transporter T5 facelift	7H			LOW	物理分支或尺寸组尚未闭合。	PENDING: 4Motion Kasten 的轴距与车顶组合尚未闭合。
27416	27416	MPV	Multivan T5	7H	5	EU-VW-MULTIVAN-T5-MPV-SWB-01	HIGH	Multivan 短轴乘用外廓。	READY
27456	27456	MPV	Multivan T5	7H	5	EU-VW-MULTIVAN-T5-MPV-SWB-01	HIGH	4Motion 不改变外廓。	READY
27483	27483	Wagon	Insignia A facelift	A	5		LOW	物理分支或尺寸组尚未闭合。	PENDING: 改款 Sports Tourer 三维及无后视镜宽度尚未建立。
27496	27496	MPV	Quest I	V40	5		LOW	物理分支或尺寸组尚未闭合。	PENDING: 1992–1998 Quest 代际与现有 Quest III 组不符，需新建尺寸组。
27512	27512	Van	Movano A	X70			LOW	物理分支或尺寸组尚未闭合。	PENDING: L1/L2/L3 与 H1/H2/H3 的 74 kW 版本覆盖未确认。
27513_mwb	27513	Pickup	Movano A	X70		EU-OPEL-MOVANO-A-X70-CHASSIS-CAB-MWB-01	MEDIUM	X70 中轴单排底盘分支。	READY
27513_lwb	27513	Pickup	Movano A	X70		EU-OPEL-MOVANO-A-X70-CHASSIS-CAB-LWB-01	MEDIUM	X70 长轴单排底盘分支。	READY
27517	27517	Pickup	Vivaro A	X83			LOW	物理分支或尺寸组尚未闭合。	PENDING: 平台/底盘轴距与驾驶室外廓尚未建立尺寸组。
27518	27518	Pickup	Vivaro A	X83			LOW	物理分支或尺寸组尚未闭合。	PENDING: 平台/底盘轴距与驾驶室外廓尚未建立尺寸组。
27519	27519	SUV	Sorento I facelift	BL	5	EU-KIA-SORENTO-I-FACELIFT-SUV-01	HIGH	改款 SUV 外廓。	READY
27528	27528	Hatchback	Splash I	EX	5		LOW	物理分支或尺寸组尚未闭合。	PENDING: Splash 三维及无后视镜宽度尚未建立。
27529	27529	Hatchback	Splash I	EX	5		LOW	物理分支或尺寸组尚未闭合。	PENDING: Splash 三维及无后视镜宽度尚未建立。
27530	27530	Hatchback	Splash I	EX	5		LOW	物理分支或尺寸组尚未闭合。	PENDING: Splash 三维及无后视镜宽度尚未建立。
27531	27531	Hatchback	Laguna III	BT	5	EU-RENAULT-LAGUNA-III-HATCHBACK-5D-01	HIGH	五门掀背外廓。	READY
27532	27532	Wagon	Laguna III	KT	5	EU-RENAULT-LAGUNA-III-WAGON-5D-01	HIGH	Grandtour 五门旅行车。	READY
27533	27533	Coupe	Laguna III Coupe	DT	3		LOW	物理分支或尺寸组尚未闭合。	PENDING: Laguna Coupe 三维及来源尚未建立。
27534	27534	Coupe	Laguna III Coupe	DT	3		LOW	物理分支或尺寸组尚未闭合。	PENDING: Laguna Coupe 三维及来源尚未建立。
27535	27535	Coupe	Laguna III Coupe	DT	3		LOW	物理分支或尺寸组尚未闭合。	PENDING: Laguna Coupe 三维及来源尚未建立。
27537_prefl	27537	MPV	Golf Plus V	5M	5	EU-VW-GOLF-PLUS-V-MPV-PREFL-01	HIGH	改款前外廓。	READY
27537_facelift	27537	MPV	Golf Plus VI	5M	5	EU-VW-GOLF-PLUS-VI-MPV-FACELIFT-01	HIGH	2009 改款后外廓。	READY
27539	27539	Wagon	Golf V Variant	1K5	5	EU-VW-GOLF-V-VARIANT-WAGON-5D-01	HIGH	五门旅行车。	READY
27540	27540	Wagon	Passat B6	3C5	5	EU-VW-PASSAT-B6-3C5-WAGON-01	HIGH	3C5 旅行车外廓。	READY
27541	27541	Wagon	Passat B6	3C5	5	EU-VW-PASSAT-B6-3C5-WAGON-01	HIGH	3C5 旅行车外廓。	READY
27544	27544	Sedan	Passat B6	3C2	4	EU-VW-PASSAT-B6-3C2-SEDAN-01	HIGH	3C2 四门轿车外廓。	READY
27545	27545	Sedan	Passat B6	3C2	4	EU-VW-PASSAT-B6-3C2-SEDAN-01	HIGH	3C2 四门轿车外廓。	READY
27547	27547	Sedan	Passat B6	3C2	4	EU-VW-PASSAT-B6-3C2-SEDAN-01	HIGH	3C2 四门轿车外廓。	READY
27548_phase1	27548	SUV	Koleos I Phase I	HY	5	EU-RENAULT-KOLEOS-I-SUV-PHASE-I-01	HIGH	第一阶段外廓。	READY
27548_phase2	27548	SUV	Koleos I Phase II	HY	5	EU-RENAULT-KOLEOS-I-SUV-PHASE-II-01	HIGH	第二阶段外廓。	READY
27548_phase3	27548	SUV	Koleos I Phase III	HY	5	EU-RENAULT-KOLEOS-I-SUV-PHASE-III-01	HIGH	第三阶段加宽外廓。	READY
27549_phase1	27549	SUV	Koleos I Phase I	HY	5	EU-RENAULT-KOLEOS-I-SUV-PHASE-I-01	HIGH	第一阶段外廓。	READY
27549_phase2	27549	SUV	Koleos I Phase II	HY	5	EU-RENAULT-KOLEOS-I-SUV-PHASE-II-01	HIGH	第二阶段外廓。	READY
27549_phase3	27549	SUV	Koleos I Phase III	HY	5	EU-RENAULT-KOLEOS-I-SUV-PHASE-III-01	HIGH	第三阶段加宽外廓。	READY
27550	27550	Coupe	Laguna III Coupe	DT	3		LOW	物理分支或尺寸组尚未闭合。	PENDING: Laguna Coupe 三维及来源尚未建立。
27551	27551	Coupe	GT-R R35	R35	2		LOW	物理分支或尺寸组尚未闭合。	PENDING: 2007–2010 R35 前期三维及来源尚未建立。
27554	27554	Sedan	GS III	S190	4		LOW	物理分支或尺寸组尚未闭合。	PENDING: GS 460 属于第三代 S190，不能复用现有 GS IV 组。
27555_prefl	27555	Sedan	3 Series E90	E90	4	EU-BMW-3-E90-SEDAN-4D-PREFL-01	HIGH	改款前四门轿车。	READY
27555_facelift	27555	Sedan	3 Series E90	E90	4	EU-BMW-3-E90-SEDAN-4D-FACELIFT-01	HIGH	改款后四门轿车。	READY
27562_3dr	27562	Hatchback	A3 II facelift	8P	3	EU-AUDI-A3-II-HATCHBACK-3D-FACELIFT-01	HIGH	S3 三门改款外廓。	READY
27562_5dr	27562	Hatchback	A3 II facelift	8PA	5	EU-AUDI-A3-II-HATCHBACK-5D-FACELIFT-01	HIGH	S3 Sportback 五门外廓。	READY
27563	27563	SUV	Q5 I pre-facelift	8R	5		LOW	物理分支或尺寸组尚未闭合。	PENDING: Q5 8R 改款前三维及来源尚未建立。
27564	27564	SUV	Q5 I pre-facelift	8R	5		LOW	物理分支或尺寸组尚未闭合。	PENDING: Q5 8R 改款前三维及来源尚未建立。
27565	27565	SUV	Q5 I	8R	5		LOW	物理分支或尺寸组尚未闭合。	PENDING: 生产期跨越 2012 改款，需拆分前后外廓并建立尺寸组。
27566	27566	Pickup	Avalanche I	GMT800	4	EU-CHEVROLET-AVALANCHE-I-GMT800-PICKUP-4D-01	HIGH	GMT800 四门短货斗一体式外廓。	READY
27567	27567	Pickup	Avalanche II	GMT900	4		LOW	物理分支或尺寸组尚未闭合。	PENDING: 第二代 GMT900 三维及来源尚未建立。
27568	27568	Sedan	Lancer VIII	CY0	4	EU-MITSUBISHI-LANCER-VIII-CY0-SEDAN-4D-01	HIGH	CY0 四门轿车。	READY
27569	27569	SUV	4007 I		5	EU-PEUGEOT-4007-I-SUV-5D-01	HIGH	五门 SUV 外廓。	READY
27570	27570	MPV	807		5	EU-PEUGEOT-807-MPV-01	HIGH	大型 MPV 外廓。	READY
27571	27571	MPV	Express I	GMT610	4		LOW	物理分支或尺寸组尚未闭合。	PENDING: Passenger van 的 1500/2500/3500 与 SWB/LWB 外廓未拆分。
27572	27572	Pickup	Silverado 1500 II	GMT900			LOW	物理分支或尺寸组尚未闭合。	PENDING: Cab/Bed 组合及对应三维尚未拆分。
27573	27573	Pickup	Silverado 1500 II	GMT900			LOW	物理分支或尺寸组尚未闭合。	PENDING: Cab/Bed 组合及对应三维尚未拆分。
27574	27574	Pickup	Silverado 2500 HD II	GMT900			LOW	物理分支或尺寸组尚未闭合。	PENDING: Regular/Extended/Crew Cab 与 Bed 组合尚未拆分。
27575	27575	SUV	Suburban X	GMT900	5		LOW	物理分支或尺寸组尚未闭合。	PENDING: 1500/2500 外廓及高度差异尚未确认。
27576	27576	Hatchback	Sandero I	BS	5		LOW	物理分支或尺寸组尚未闭合。	PENDING: 第一代 Sandero 三维及来源尚未建立。
27577	27577	Hatchback	Sandero I	BS	5		LOW	物理分支或尺寸组尚未闭合。	PENDING: 第一代 Sandero 三维及来源尚未建立。
27579	27579	Hatchback	C4 I	LC	5		LOW	物理分支或尺寸组尚未闭合。	PENDING: 五门 Hatchback 不能复用现有三门 Coupe 组，需新建尺寸组。
27580	27580	Sedan	Avenger JS	JS	4	EU-DODGE-AVENGER-JS-SEDAN-01	HIGH	JS 四门轿车。	READY
27581	27581	Hatchback	Focus I				LOW	物理分支或尺寸组尚未闭合。	PENDING: 三门/五门边界及 Focus I Hatchback 三维组尚未闭合。
27583	27583	SUV	Explorer III	U152	5	EU-FORD-USA-EXPLORER-III-U152-SUV-5D-01	HIGH	U152 五门 SUV。	READY
27584	27584	Hatchback	Ibiza IV	6J			LOW	物理分支或尺寸组尚未闭合。	PENDING: SC 三门与五门外廓、以及 2012 改款边界尚未拆分。
27585	27585	Hatchback	Ibiza IV	6J			LOW	物理分支或尺寸组尚未闭合。	PENDING: SC 三门与五门外廓、以及 2012 改款边界尚未拆分。
27586	27586	Hatchback	Ibiza IV	6J			LOW	物理分支或尺寸组尚未闭合。	PENDING: 三门/五门外廓尚未拆分；当前生产期为改款前。
27587	27587	Hatchback	Ibiza IV	6J			LOW	物理分支或尺寸组尚未闭合。	PENDING: 三门/五门外廓尚未拆分；当前生产期为改款前。
27598	27598	Wagon	Megane II Phase II	KM	5	EU-RENAULT-MEGANE-II-GRANDTOUR-PHASE-II-WAGON-5D-01	HIGH	Phase II Grandtour 外廓。	READY
27599_3dr	27599	Hatchback	Megane II Phase II	CM	3	EU-RENAULT-MEGANE-II-PHASE-II-HATCHBACK-3D-01	HIGH	三门掀背分支。	READY
27599_5dr	27599	Hatchback	Megane II Phase II	BM	5	EU-RENAULT-MEGANE-II-PHASE-II-HATCHBACK-5D-01	HIGH	五门掀背分支。	READY
27600	27600	Wagon	9-3 II	YS3F	5		LOW	物理分支或尺寸组尚未闭合。	PENDING: 2007 起始月份与改款边界重叠，改款前 SportCombi 组尚未建立。
27601	27601	Wagon	9-3 II	YS3F	5		LOW	物理分支或尺寸组尚未闭合。	PENDING: 2007 起始月份与改款边界重叠，改款前 SportCombi 组尚未建立。
27611_prefl	27611	Convertible	9-3 II pre-facelift		2	EU-SAAB-9-3-II-CONVERTIBLE-PREFL-01	HIGH	改款前敞篷外廓。	READY
27611_facelift	27611	Convertible	9-3 II facelift		2	EU-SAAB-9-3-II-CONVERTIBLE-FACELIFT-01	HIGH	改款后敞篷外廓。	READY
27612_prefl	27612	Sedan	9-3 II pre-facelift		4	EU-SAAB-9-3-II-SEDAN-01	HIGH	改款前四门轿车。	READY
27612_facelift	27612	Sedan	9-3 II facelift		4	EU-SAAB-9-3-II-FACELIFT-SEDAN-4D-01	HIGH	改款后四门轿车。	READY
27613_prefl	27613	Sedan	9-3 II pre-facelift		4	EU-SAAB-9-3-II-SEDAN-01	HIGH	改款前四门轿车。	READY
27613_facelift	27613	Sedan	9-3 II facelift		4	EU-SAAB-9-3-II-FACELIFT-SEDAN-4D-01	HIGH	改款后四门轿车。	READY
27614	27614	Sedan	9-5 facelift 2005		4	EU-SAAB-9-5-FACELIFT-2005-SEDAN-01	HIGH	2005 改款轿车。	READY
27615	27615	Wagon	9-5 facelift 2005		5	EU-SAAB-9-5-FACELIFT-2005-WAGON-01	HIGH	2005 改款旅行车。	READY
27618_prefl	27618	Hatchback	C30 I pre-facelift		3	EU-VOLVO-C30-I-HATCHBACK-3D-PREFL-01	HIGH	改款前三门外廓。	READY
27618_facelift	27618	Hatchback	C30 I facelift		3	EU-VOLVO-C30-I-HATCHBACK-3D-FACELIFT-01	HIGH	改款后三门外廓。	READY
27619_prefl	27619	Sedan	S40 II pre-facelift		4	EU-VOLVO-S40-II-SEDAN-01	HIGH	改款前四门轿车。	READY
27619_facelift	27619	Sedan	S40 II facelift		4	EU-VOLVO-S40-II-FACELIFT-SEDAN-4D-01	HIGH	改款后四门轿车。	READY
27620	27620	Sedan	S80 II		4	EU-VOLVO-S80-II-SEDAN-4D-01	HIGH	第二代四门轿车。	READY
27622	27622	Sedan	S80 II		4	EU-VOLVO-S80-II-SEDAN-4D-01	HIGH	第二代四门轿车。	READY
27624_prefl	27624	Wagon	V50 pre-facelift	MW	5	EU-VOLVO-V50-MW-WAGON-PREFL-01	HIGH	改款前旅行车。	READY
27624_facelift	27624	Wagon	V50 facelift	MW	5	EU-VOLVO-V50-MW-WAGON-FACELIFT-01	HIGH	改款后旅行车。	READY
27625	27625	Wagon	V70 III pre-facelift		5	EU-VOLVO-V70-III-WAGON-5D-PREFL-01	HIGH	改款前旅行车。	READY
27626_prefl	27626	Wagon	V70 III pre-facelift		5	EU-VOLVO-V70-III-WAGON-5D-PREFL-01	HIGH	改款前旅行车。	READY
27626_facelift	27626	Wagon	V70 III facelift		5	EU-VOLVO-V70-III-FACELIFT-WAGON-5D-01	MEDIUM	2011 改款边界分支。	READY
```

## 本轮新增/修改的 DIMENSION_GROUP TSV

无

## 下一步优先处理

1. 优先建立可一次解决多个 Ktype 的乘用车尺寸组：Splash、Laguna Coupe、Q5 8R、Sandero I、Focus I、Ibiza IV。
2. 随后解决 Alfa Romeo 156 Sportwagon 改款前、Mazda 6 标准轿车、Volkswagen CC、Insignia Sports Tourer、GT-R R35、Lexus GS S190 等单车身组。
3. 最后集中拆分 Ram、Silverado、Express、Transporter、Movano、Vivaro、Hiace 等 Cab/Bed、轴距和车顶组合。

推进信号：CONTINUE

[1]: https://www.volkswagen-newsroom.com/en/vehicle-data-jetta-2-profile-19644?utm_source=chatgpt.com "Vehicle data Jetta II profile"


--- 发送 / 继续到 Round 2 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2501-2600_ktype_dimension_mapping_final.tsv
- all_2501-2600_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 2 / 下一步 ---
## 更新点

* 本轮闭合 17 个 PENDING Ktype，首次创建 9 个尺寸组。
* Volkswagen CC、Insignia Sports Tourer、Audi Q5 和 Nissan GT-R 的三维及不含后视镜宽度已由车型官方规格资料闭合。
* Splash、Laguna Coupe、Sandero I、C4 I Hatchback 使用规则允许的规格数据库闭合；GS 460 使用 Lexus UK 历史技术资料闭合。([汽车数据网][1])
* Q5 的三个动力版本均属于 8R 改款前外廓，没有因输入表中过宽的结束日期猜测创建 facelift 分支。

## 当前批次进度

* 输入 Ktype：100
* 已闭合 Ktype：65
* 待处理 Ktype：35
* READY 映射：89
* PENDING 映射：35
* 已确认尺寸组：70
* 本轮新增尺寸组：9
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27347	27347	Coupe	CC B7	358	4	EU-VW-CC-B7-COUPE-4D-01	HIGH	358四门CC外廓。	READY
27483	27483	Wagon	Insignia A facelift	G09	5	EU-OPEL-INSIGNIA-A-SPORTS-TOURER-FACELIFT-01	HIGH	Sports Tourer外廓；不含Country Tourer。	READY
27528	27528	Hatchback	Splash I		5	EU-SUZUKI-SPLASH-I-HATCHBACK-5D-01	HIGH	五门掀背外廓。	READY
27529	27529	Hatchback	Splash I		5	EU-SUZUKI-SPLASH-I-HATCHBACK-5D-01	HIGH	五门掀背外廓。	READY
27530	27530	Hatchback	Splash I		5	EU-SUZUKI-SPLASH-I-HATCHBACK-5D-01	HIGH	五门掀背外廓。	READY
27533	27533	Coupe	Laguna III Coupe	DT	2	EU-RENAULT-LAGUNA-III-COUPE-2D-01	HIGH	DT双门Coupe外廓。	READY
27534	27534	Coupe	Laguna III Coupe	DT	2	EU-RENAULT-LAGUNA-III-COUPE-2D-01	HIGH	DT双门Coupe外廓。	READY
27535	27535	Coupe	Laguna III Coupe	DT	2	EU-RENAULT-LAGUNA-III-COUPE-2D-01	HIGH	DT双门Coupe外廓。	READY
27550	27550	Coupe	Laguna III Coupe	DT	2	EU-RENAULT-LAGUNA-III-COUPE-2D-01	HIGH	DT双门Coupe外廓。	READY
27551	27551	Coupe	GT-R R35 pre-facelift	R35	2	EU-NISSAN-GT-R-R35-COUPE-PREFL-01	HIGH	R35前期双门外廓。	READY
27554	27554	Sedan	GS III facelift	S190	4	EU-LEXUS-GS-III-S190-FACELIFT-SEDAN-4D-01	HIGH	S190改款四门外廓。	READY
27563	27563	SUV	Q5 I pre-facelift	8R	5	EU-AUDI-Q5-I-8R-SUV-PREFL-01	HIGH	8R改款前外廓。	READY
27564	27564	SUV	Q5 I pre-facelift	8R	5	EU-AUDI-Q5-I-8R-SUV-PREFL-01	HIGH	8R改款前外廓。	READY
27565	27565	SUV	Q5 I pre-facelift	8R	5	EU-AUDI-Q5-I-8R-SUV-PREFL-01	MEDIUM	8R改款前外廓。	READY
27576	27576	Hatchback	Sandero I	BS	5	EU-DACIA-SANDERO-I-HATCHBACK-5D-01	HIGH	BS五门掀背外廓。	READY
27577	27577	Hatchback	Sandero I	BS	5	EU-DACIA-SANDERO-I-HATCHBACK-5D-01	HIGH	BS五门掀背外廓。	READY
27579	27579	Hatchback	C4 I	LC	5	EU-CITROEN-C4-I-HATCHBACK-5D-01	HIGH	LC五门掀背外廓；不复用三门Coupe组。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-VW-CC-B7-COUPE-4D-01	4802	1855	1421	Volkswagen CC official brochure	https://www.volkswagen.co.uk/idhub/content/dam/onehub_pkw/importers/gb/downloads/brochures/used-cars/cc/VW-CC-Brochure-February-2012.pdf
EU-OPEL-INSIGNIA-A-SPORTS-TOURER-FACELIFT-01	4913	1856	1513	Vauxhall New Insignia official price/specification guide	https://www.vauxhall.co.uk/content/dam/vauxhall/Home/PDFs/historical-brochures/discounted-models/insignia-a/NEW_Insignia_Spec_PG_10_March_2014.pdf
EU-SUZUKI-SPLASH-I-HATCHBACK-5D-01	3715	1680	1590	Auto-Data Suzuki Splash	https://www.auto-data.net/en/suzuki-splash-model-1901
EU-RENAULT-LAGUNA-III-COUPE-2D-01	4643	1812	1401	Automobile-Catalog Renault Laguna Coupe GT	https://www.automobile-catalog.com/car/2012/2958905/renault_laguna_coupe_gt_2_0_dci_180_fap.html
EU-NISSAN-GT-R-R35-COUPE-PREFL-01	4650	1895	1370	Nissan GT-R 2009 UK brochure	https://xr793.com/wp-content/uploads/2022/10/2009-Nissan-GT-R-UK.pdf
EU-LEXUS-GS-III-S190-FACELIFT-SEDAN-4D-01	4825	1820	1430	Lexus UK GS technical archive	https://media.lexus.co.uk/the-new-lexus-gs-exploring-new-frontiers-in-dynamic-performance-and-safety/
EU-AUDI-Q5-I-8R-SUV-PREFL-01	4629	1880	1653	Audi Q5 2012 UK pricing and specification guide	https://press.audi.co.uk/assets/documents/original/20863-AudiUK00000109Q5PriceandSpecification.pdf
EU-DACIA-SANDERO-I-HATCHBACK-5D-01	4020	1746	1534	Automoli Dacia Sandero I	https://www.automoli.com/au/vehicles/dacia/sandero/sandero-i-3532/
EU-CITROEN-C4-I-HATCHBACK-5D-01	4260	1773	1458	Automobile-Catalog Citroen C4 five-door hatchback	https://www.automobile-catalog.com/car/2007/551300/citroen_c4_1_6_hdi_110_fap_vtr.html
```

## 下一步优先处理

1. Focus I Hatchback/Turnier、Ibiza IV 三门/五门及 Mazda 6 I 标准 Sedan。
2. Alfa Romeo 156 Sportwagon 改款前、Saab 9-3 SportCombi 改款前、Quest I 和 Jetta II。
3. 最后集中处理 Hiace、Transporter、Movano、Vivaro、Ram、Silverado、Express 等轴距、车顶及 Cab/Bed 组合。

推进信号：CONTINUE

[1]: https://www.auto-data.net/en/suzuki-splash-model-1901?utm_source=chatgpt.com "Suzuki Splash | Technical Specs, Fuel consumption ..."


--- 发送 / 继续到 Round 3 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2501-2600_ktype_dimension_mapping_final.tsv
- all_2501-2600_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 3 / 下一步 ---
## 更新点

* 本轮闭合 9 个 PENDING Ktype，新增 14 条 READY 映射，首次创建 8 个尺寸组。
* Focus I 已按 DAW 三门、DBW 五门和 DNW Turnier 分支闭合；Ibiza IV 对应 6J5 五门车身，并按 2012 年改款前后拆分。([汽车目录档案][1])
* Mazda 6 I 改款轿车与 Saab 9-3 SportCombi 改款前后尺寸已闭合。Saab 改款后证据高度为 1498 mm，与累计表既有 `-01` 的 1496 mm 不同，因此未覆盖旧组，按规则创建 `-02`。([Scribd][2])

## 当前批次进度

* 输入 Ktype：100
* 已闭合 Ktype：74
* 待处理 Ktype：26
* READY 映射：103
* PENDING 映射：26
* 已确认尺寸组：78
* 本轮新增尺寸组：8
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27247	27247	Wagon	Focus I facelift	DNW	5	EU-FORD-FOCUS-I-DNW-WAGON-5D-01	HIGH	DNW五门Turnier外廓。	READY
27317	27317	Sedan	Mazda 6 I facelift	GG	4	EU-MAZDA-6-I-GG-FACELIFT-SEDAN-4D-01	HIGH	GG改款四门轿车外廓。	READY
27581_3dr	27581	Hatchback	Focus I facelift	DAW	3	EU-FORD-FOCUS-I-DAW-HATCHBACK-3D-01	HIGH	DAW三门外廓。	READY
27581_5dr	27581	Hatchback	Focus I facelift	DBW	5	EU-FORD-FOCUS-I-DBW-HATCHBACK-5D-01	HIGH	DBW五门外廓。	READY
27584_prefl	27584	Hatchback	Ibiza IV pre-facelift	6J5	5	EU-SEAT-IBIZA-IV-6J5-HATCHBACK-5D-PREFL-01	HIGH	6J5五门；按2012改款边界拆分。	READY
27584_facelift	27584	Hatchback	Ibiza IV facelift	6J5	5	EU-SEAT-IBIZA-IV-6J5-HATCHBACK-5D-FACELIFT-01	HIGH	6J5五门；按2012改款边界拆分。	READY
27585_prefl	27585	Hatchback	Ibiza IV pre-facelift	6J5	5	EU-SEAT-IBIZA-IV-6J5-HATCHBACK-5D-PREFL-01	HIGH	6J5五门；按2012改款边界拆分。	READY
27585_facelift	27585	Hatchback	Ibiza IV facelift	6J5	5	EU-SEAT-IBIZA-IV-6J5-HATCHBACK-5D-FACELIFT-01	HIGH	6J5五门；按2012改款边界拆分。	READY
27586	27586	Hatchback	Ibiza IV pre-facelift	6J5	5	EU-SEAT-IBIZA-IV-6J5-HATCHBACK-5D-PREFL-01	HIGH	6J5改款前五门外廓。	READY
27587	27587	Hatchback	Ibiza IV pre-facelift	6J5	5	EU-SEAT-IBIZA-IV-6J5-HATCHBACK-5D-PREFL-01	HIGH	6J5改款前五门外廓。	READY
27600_prefl	27600	Wagon	9-3 II pre-facelift	YS3F	5	EU-SAAB-9-3-II-PREFL-WAGON-5D-01	HIGH	改款前SportCombi外廓。	READY
27600_facelift	27600	Wagon	9-3 II facelift	YS3F	5	EU-SAAB-9-3-II-FACELIFT-WAGON-5D-02	HIGH	改款后SportCombi外廓。	READY
27601_prefl	27601	Wagon	9-3 II pre-facelift	YS3F	5	EU-SAAB-9-3-II-PREFL-WAGON-5D-01	HIGH	改款前SportCombi外廓。	READY
27601_facelift	27601	Wagon	9-3 II facelift	YS3F	5	EU-SAAB-9-3-II-FACELIFT-WAGON-5D-02	HIGH	改款后SportCombi外廓。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-FORD-FOCUS-I-DNW-WAGON-5D-01	4454	1702	1532	Ford Focus 2003 UK brochure	https://autocatalogarchive.com/wp-content/uploads/2025/10/Ford-Focus-2003-UK.pdf
EU-MAZDA-6-I-GG-FACELIFT-SEDAN-4D-01	4690	1780	1435	Mazda6 Specifications October 2005	https://www.scribd.com/document/513396129/Mazda6-Specifications-Oct-2005
EU-FORD-FOCUS-I-DAW-HATCHBACK-3D-01	4174	1702	1430	Ford Focus 2003 UK brochure	https://autocatalogarchive.com/wp-content/uploads/2025/10/Ford-Focus-2003-UK.pdf
EU-FORD-FOCUS-I-DBW-HATCHBACK-5D-01	4174	1702	1430	Ford Focus 2003 UK brochure	https://autocatalogarchive.com/wp-content/uploads/2025/10/Ford-Focus-2003-UK.pdf
EU-SEAT-IBIZA-IV-6J5-HATCHBACK-5D-PREFL-01	4052	1693	1445	SEAT Ibiza 2011 official brochure	https://autocatalogarchive.com/wp-content/uploads/2017/05/Seat-Ibiza-2011-.pdf
EU-SEAT-IBIZA-IV-6J5-HATCHBACK-5D-FACELIFT-01	4061	1693	1445	SEAT Ibiza 2012 official brochure	https://autocatalogarchive.com/wp-content/uploads/2017/05/Seat-Ibiza-2012-UK.pdf
EU-SAAB-9-3-II-PREFL-WAGON-5D-01	4654	1762	1490	Automobile-Catalog Saab 9-3 2.0t SportCombi pre-facelift	https://www.automobile-catalog.com/car/2007/3036110/saab_9-3_2_0t_sportcombi.html
EU-SAAB-9-3-II-FACELIFT-WAGON-5D-02	4670	1762	1498	Automobile-Catalog Saab 9-3 2.0t SportCombi facelift	https://www.automobile-catalog.com/car/2007/3037040/saab_9-3_2_0t_sportcombi.html
```

## 下一步优先处理

1. Alfa Romeo 156 改款前 Sportwagon、Jetta II 精确车身边界及 Quest I。
2. Hiace、Transporter、Movano、Vivaro 的轴距和车顶组合。
3. Ram、Silverado、Express、Suburban 的 Cab、Bed 和载重级别分支。

推进信号：CONTINUE

[1]: https://autocatalogarchive.com/wp-content/uploads/2025/10/Ford-Focus-2003-UK.pdf?utm_source=chatgpt.com "Ford-Focus-2003-UK.pdf"
[2]: https://www.scribd.com/document/513396129/Mazda6-Specifications-Oct-2005?utm_source=chatgpt.com "Mazda6 - Specifications - Oct 2005 | PDF"


--- 发送 / 继续到 Round 4 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2501-2600_ktype_dimension_mapping_final.tsv
- all_2501-2600_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 4 / 下一步 ---
## 更新点

* 闭合 Alfa Romeo 156 Sportwagon 改款边界：27297、27298 拆分改款前后，27299 直接关联改款后既有组；新增改款前 Sportwagon 尺寸组。官方资料确认改款前外廓为 4430 × 1745 × 1420 mm，外观改款车型于 2003 年 6 月发布。([Stellantis Media][1])
* 闭合 Mercedes-Benz S 500 4MATIC 的标准轴距 W222 与长轴 V222 两个物理分支；官方车型手册分别给出 5116 mm 和 5246 mm 车长，宽度和高度均为 1899 mm、1496 mm。([澳大利亚汽车评论][2])
* 闭合 Chevrolet Avalanche II、Express G1500 后驱短轴乘用版和 Suburban 1500 4WD。GM 资料已明确三维及对应车型边界；Suburban 手册同时明确宽度不含后视镜。([Dezo's Garage][3])

## 当前批次进度

* 输入 Ktype：100
* 已闭合 Ktype：81
* 待处理 Ktype：19
* READY 映射：113
* PENDING 映射：19
* 已确认尺寸组：84
* 本轮新增尺寸组：6
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27297_prefl	27297	Wagon	156 (932) pre-facelift	932	5	EU-ALFA-ROMEO-156-932-WAGON-PREFL-01	HIGH	生产期覆盖改款前Sportwagon外廓。	READY
27297_facelift	27297	Wagon	156 (932) facelift	932	5	EU-ALFA-ROMEO-156-932-FACELIFT-WAGON-01	HIGH	生产期覆盖改款后Sportwagon外廓。	READY
27298_prefl	27298	Wagon	156 (932) pre-facelift	932	5	EU-ALFA-ROMEO-156-932-WAGON-PREFL-01	HIGH	生产期覆盖改款前Sportwagon外廓。	READY
27298_facelift	27298	Wagon	156 (932) facelift	932	5	EU-ALFA-ROMEO-156-932-FACELIFT-WAGON-01	HIGH	生产期覆盖改款后Sportwagon外廓。	READY
27299	27299	Wagon	156 (932) facelift	932	5	EU-ALFA-ROMEO-156-932-FACELIFT-WAGON-01	HIGH	2003年6月起改款Sportwagon外廓。	READY
27400_swb	27400	Sedan	S-Class W222	W222	4	EU-MERCEDES-BENZ-S-CLASS-W222-SEDAN-4D-01	MEDIUM	标准轴距四门分支。	READY
27400_lwb	27400	Sedan	S-Class V222	V222	4	EU-MERCEDES-BENZ-S-CLASS-V222-SEDAN-LWB-4D-01	MEDIUM	长轴四门分支。	READY
27567	27567	Pickup	Avalanche II	GMT900	4	EU-CHEVROLET-AVALANCHE-II-GMT900-PICKUP-4D-01	HIGH	GMT900四门一体式货斗外廓。	READY
27571	27571	MPV	Express I	GMT610		EU-CHEVROLET-EXPRESS-I-PASSENGER-VAN-SWB-1500-01	HIGH	G1500后驱短轴乘用厢式分支。	READY
27575	27575	SUV	Suburban X	GMT900	4	EU-CHEVROLET-SUBURBAN-X-GMT900-SUV-4D-1500-01	HIGH	1500四驱FlexFuel外廓。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-ALFA-ROMEO-156-932-WAGON-PREFL-01	4430	1745	1420	Alfa Romeo New 156 Sportwagon official technical specification	https://www.media.stellantis.com/uk-en/alfa-romeo/press/new-alfa-156-range-in-uk
EU-MERCEDES-BENZ-S-CLASS-W222-SEDAN-4D-01	5116	1899	1496	Mercedes-Benz S-Class W222 official brochure May 2014	https://www.australiancar.reviews/_pdfs/Mercedes-Benz_S-Class_W222_Brochure_201405.pdf
EU-MERCEDES-BENZ-S-CLASS-V222-SEDAN-LWB-4D-01	5246	1899	1496	Mercedes-Benz S-Class W222 official brochure May 2014	https://www.australiancar.reviews/_pdfs/Mercedes-Benz_S-Class_W222_Brochure_201405.pdf
EU-CHEVROLET-AVALANCHE-II-GMT900-PICKUP-4D-01	5621	2009	1946	General Motors 2007 Fleet Guide	https://xr793.com/wp-content/uploads/2020/03/2007-GM-Fleet-Guide.pdf
EU-CHEVROLET-EXPRESS-I-PASSENGER-VAN-SWB-1500-01	5692	2017	2073	General Motors 2007 Fleet Guide	https://xr793.com/wp-content/uploads/2020/03/2007-GM-Fleet-Guide.pdf
EU-CHEVROLET-SUBURBAN-X-GMT900-SUV-4D-1500-01	5649	2007	1951	Chevrolet 2007 Tahoe and Suburban official brochure	https://xr793.com/wp-content/uploads/2022/07/2007-Chevrolet-Tahoe-Suburban-CN.pdf
```

## 下一步优先处理

1. 集中闭合 Hiace IV/V 的代际冲突、四驱、轴距和车顶分支。
2. 批量处理 Transporter T5 Bus/Kasten、Movano A Kasten、Vivaro A 平台底盘。
3. 最后拆分 Ram 1500、Silverado 1500/2500 HD 的 Cab/Bed 组合，并解决 Jetta II、Quest I 和 Ducato X230 4×4。

推进信号：CONTINUE

[1]: https://www.media.stellantis.com/uk-en/alfa-romeo/press/new-alfa-156-range-in-uk?utm_source=chatgpt.com "NEW ALFA 156 RANGE IN UK | Alfa Romeo"
[2]: https://www.australiancar.reviews/_pdfs/Mercedes-Benz_S-Class_W222_Brochure_201405.pdf "Brochure: Mercedes-Benz W222 S-Class (May 2014)"
[3]: https://xr793.com/wp-content/uploads/2020/03/2007-GM-Fleet-Guide.pdf?utm_source=chatgpt.com "2007
Car and Truck GuideGMCGM Fleet and Commercial"


--- 发送 / 继续到 Round 5 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2501-2600_ktype_dimension_mapping_final.tsv
- all_2501-2600_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 5 / 下一步 ---
## 更新点

* 闭合 Jetta II 两个 Ktype，并按两门、四门拆分；两种车身共用相同三维，但分别建立稳定尺寸组。Volkswagen 资料确认 Jetta II 1.8 覆盖 1984–1992 年，Auto-Data 给出的两门及四门外廓均为 4385 × 1675 × 1415 mm。([Volkswagen Newsroom][1])
* 闭合 Quest I，新增第一代 V40 MPV 尺寸组 4823 × 1872 × 1717 mm，其中宽度明确为不含后视镜。([Edmunds][2])
* Transporter T5 的 Bus 与 Kasten 按 SWB/LWB、低顶/中顶/高顶关联现有缓存组；2.0 TSI 及 4Motion 资料确认存在多个轴距和车顶组合。([Bind][3])
* Movano A 2.5 CDTI Kasten 按现有 L1H1、L1H2、L2H2、L3H2、L3H3 五个缓存组完成关联。

## 当前批次进度

* 输入 Ktype：100
* 已闭合 Ktype：89
* 待处理 Ktype：11
* READY 映射：143
* PENDING 映射：11
* 已确认尺寸组：87
* 本轮首次创建尺寸组：3
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27224_2dr	27224	Sedan	Jetta II		2	EU-VW-JETTA-II-SEDAN-2D-01	MEDIUM	两门轿车外廓。	READY
27224_4dr	27224	Sedan	Jetta II		4	EU-VW-JETTA-II-SEDAN-4D-01	MEDIUM	四门轿车外廓。	READY
27225_2dr	27225	Sedan	Jetta II		2	EU-VW-JETTA-II-SEDAN-2D-01	MEDIUM	两门轿车外廓。	READY
27225_4dr	27225	Sedan	Jetta II		4	EU-VW-JETTA-II-SEDAN-4D-01	MEDIUM	四门轿车外廓。	READY
27394_swb_lowroof	27394	MPV	Transporter T5 facelift	7H		EU-VW-TRANSPORTER-T5-MPV-SWB-LOWROOF-01	MEDIUM	短轴低顶Bus分支。	READY
27394_swb_midroof	27394	MPV	Transporter T5 facelift	7H		EU-VW-TRANSPORTER-T5-MPV-SWB-MIDROOF-01	MEDIUM	短轴中顶Bus分支。	READY
27394_lwb_lowroof	27394	MPV	Transporter T5 facelift	7H		EU-VW-TRANSPORTER-T5-MPV-LWB-LOWROOF-01	MEDIUM	长轴低顶Bus分支。	READY
27394_lwb_midroof	27394	MPV	Transporter T5 facelift	7H		EU-VW-TRANSPORTER-T5-MPV-LWB-MIDROOF-01	MEDIUM	长轴中顶Bus分支。	READY
27394_lwb_highroof	27394	MPV	Transporter T5 facelift	7H		EU-VW-TRANSPORTER-T5-MPV-LWB-HIGHROOF-01	MEDIUM	长轴高顶Bus分支。	READY
27396_swb_lowroof	27396	MPV	Transporter T5 facelift	7H		EU-VW-TRANSPORTER-T5-MPV-SWB-LOWROOF-01	MEDIUM	4Motion短轴低顶Bus分支。	READY
27396_swb_midroof	27396	MPV	Transporter T5 facelift	7H		EU-VW-TRANSPORTER-T5-MPV-SWB-MIDROOF-01	MEDIUM	4Motion短轴中顶Bus分支。	READY
27396_lwb_lowroof	27396	MPV	Transporter T5 facelift	7H		EU-VW-TRANSPORTER-T5-MPV-LWB-LOWROOF-01	MEDIUM	4Motion长轴低顶Bus分支。	READY
27396_lwb_midroof	27396	MPV	Transporter T5 facelift	7H		EU-VW-TRANSPORTER-T5-MPV-LWB-MIDROOF-01	MEDIUM	4Motion长轴中顶Bus分支。	READY
27396_lwb_highroof	27396	MPV	Transporter T5 facelift	7H		EU-VW-TRANSPORTER-T5-MPV-LWB-HIGHROOF-01	MEDIUM	4Motion长轴高顶Bus分支。	READY
27402_swb_lowroof	27402	Van	Transporter T5 facelift	7H		EU-VW-TRANSPORTER-T5-VAN-SWB-LOWROOF-01	MEDIUM	短轴低顶Kasten分支。	READY
27402_swb_medroof	27402	Van	Transporter T5 facelift	7H		EU-VW-TRANSPORTER-T5-VAN-SWB-MEDROOF-01	MEDIUM	短轴中顶Kasten分支。	READY
27402_lwb_lowroof	27402	Van	Transporter T5 facelift	7H		EU-VW-TRANSPORTER-T5-VAN-LWB-LOWROOF-01	MEDIUM	长轴低顶Kasten分支。	READY
27402_lwb_medroof	27402	Van	Transporter T5 facelift	7H		EU-VW-TRANSPORTER-T5-VAN-LWB-MEDROOF-01	MEDIUM	长轴中顶Kasten分支。	READY
27402_lwb_highroof	27402	Van	Transporter T5 facelift	7H		EU-VW-TRANSPORTER-T5-VAN-LWB-HIGHROOF-01	MEDIUM	长轴高顶Kasten分支。	READY
27403_swb_lowroof	27403	Van	Transporter T5 facelift	7H		EU-VW-TRANSPORTER-T5-VAN-SWB-LOWROOF-01	MEDIUM	4Motion短轴低顶Kasten分支。	READY
27403_swb_medroof	27403	Van	Transporter T5 facelift	7H		EU-VW-TRANSPORTER-T5-VAN-SWB-MEDROOF-01	MEDIUM	4Motion短轴中顶Kasten分支。	READY
27403_lwb_lowroof	27403	Van	Transporter T5 facelift	7H		EU-VW-TRANSPORTER-T5-VAN-LWB-LOWROOF-01	MEDIUM	4Motion长轴低顶Kasten分支。	READY
27403_lwb_medroof	27403	Van	Transporter T5 facelift	7H		EU-VW-TRANSPORTER-T5-VAN-LWB-MEDROOF-01	MEDIUM	4Motion长轴中顶Kasten分支。	READY
27403_lwb_highroof	27403	Van	Transporter T5 facelift	7H		EU-VW-TRANSPORTER-T5-VAN-LWB-HIGHROOF-01	MEDIUM	4Motion长轴高顶Kasten分支。	READY
27496	27496	MPV	Quest I	V40		EU-NISSAN-QUEST-I-V40-MPV-01	HIGH	第一代Quest MPV外廓。	READY
27512_l1h1	27512	Van	Movano A	X70		EU-OPEL-MOVANO-A-VAN-L1H1-01	MEDIUM	L1H1厢式车分支。	READY
27512_l1h2	27512	Van	Movano A	X70		EU-OPEL-MOVANO-A-VAN-L1H2-01	MEDIUM	L1H2厢式车分支。	READY
27512_l2h2	27512	Van	Movano A	X70		EU-OPEL-MOVANO-A-VAN-L2H2-01	MEDIUM	L2H2厢式车分支。	READY
27512_l3h2	27512	Van	Movano A	X70		EU-OPEL-MOVANO-A-VAN-L3H2-01	MEDIUM	L3H2厢式车分支。	READY
27512_l3h3	27512	Van	Movano A	X70		EU-OPEL-MOVANO-A-VAN-L3H3-01	MEDIUM	L3H3厢式车分支。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-VW-JETTA-II-SEDAN-2D-01	4385	1675	1415	Auto-Data Volkswagen Jetta II 2-door	https://www.auto-data.net/en/volkswagen-jetta-ii-2-doors-generation-8973
EU-VW-JETTA-II-SEDAN-4D-01	4385	1675	1415	Auto-Data Volkswagen Jetta II	https://www.auto-data.net/en/volkswagen-jetta-ii-generation-1914
EU-NISSAN-QUEST-I-V40-MPV-01	4823	1872	1717	Edmunds 1993 Nissan Quest specifications	https://www.edmunds.com/nissan/quest/1993/features-specs/
```

## 下一步优先处理

1. Hiace 27276–27279：闭合 XH10/H200 代际标注、四驱高度及 SWB/LWB 分支。
2. Ducato X230 4×4 与 Vivaro A 平台底盘：确认适用轴距后优先复用或一次建组。
3. Ram 1500、Silverado 1500 和 Silverado 2500 HD：集中拆分 Cab/Bed 组合，消除最后的美系皮卡 PENDING。

推进信号：CONTINUE

[1]: https://www.volkswagen-newsroom.com/en/vehicle-data-jetta-2-profile-19644?utm_source=chatgpt.com "Vehicle data Jetta II profile | Volkswagen Newsroom"
[2]: https://www.edmunds.com/nissan/quest/1993/features-specs/?utm_source=chatgpt.com "Used 1993 Nissan Quest Specs & Features"
[3]: https://bind.lt/en/technical-specifications/volkswagen/transporter/t5-restyling/kombi-minibus-4-doors/2-0-tsi-dsg-4motion-l2h3-204-hp?utm_source=chatgpt.com "Volkswagen Transporter - 2.0 TSI DSG 4Motion L2H3 (204 hp) Kombi minibus 4-doors - T5 [Restyling] - Technical data - Bind"


--- 发送 / 继续到 Round 6 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2501-2600_ktype_dimension_mapping_final.tsv
- all_2501-2600_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 6 / 下一步 ---
## 更新点

* 闭合 27276：确认其对应 XH10 的 KLH18 短轴与 KLH28 长轴 4WD 分支，三维与累计索引完全一致，直接复用既有尺寸组。
* 闭合 27278：确认 KLH12、KLH22 后驱分支。2006 年改款后的短轴和长轴外廓分别为 4795 × 1800 × 2000 mm、5240 × 1800 × 1995 mm，与旧组不同，因此新建尺寸组。([Autodoc][1])
* 闭合 27279：确认 KLH18、KLH28 四驱改款后分支，并新建对应尺寸组，未覆盖累计表中的改款前 KLH18/KLH28 组。([Дром][2])

## 当前批次进度

* 输入 Ktype：100
* 已闭合 Ktype：92
* 待处理 Ktype：8
* READY 映射：149
* PENDING 映射：8
* 已确认尺寸组：91
* 本轮首次创建尺寸组：4
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27276_swb	27276	Van	Hiace IV XH10	XH10-KLH18		EU-TOYOTA-HIACE-IV-XH10-VAN-KLH18-01	HIGH	KLH18短轴四驱分支。	READY
27276_lwb	27276	Van	Hiace IV XH10	XH10-KLH28		EU-TOYOTA-HIACE-IV-XH10-VAN-KLH28-01	HIGH	KLH28长轴四驱分支。	READY
27278_swb	27278	Van	Hiace IV XH10 facelift	XH10-KLH12		EU-TOYOTA-HIACE-IV-XH10-VAN-KLH12-FACELIFT-01	HIGH	KLH12改款后短轴后驱分支。	READY
27278_lwb	27278	Van	Hiace IV XH10 facelift	XH10-KLH22		EU-TOYOTA-HIACE-IV-XH10-VAN-KLH22-FACELIFT-01	HIGH	KLH22改款后长轴后驱分支。	READY
27279_swb	27279	Van	Hiace IV XH10 facelift	XH10-KLH18		EU-TOYOTA-HIACE-IV-XH10-VAN-KLH18-FACELIFT-01	HIGH	KLH18改款后短轴四驱分支。	READY
27279_lwb	27279	Van	Hiace IV XH10 facelift	XH10-KLH28		EU-TOYOTA-HIACE-IV-XH10-VAN-KLH28-FACELIFT-01	MEDIUM	KLH28改款后长轴四驱分支。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-TOYOTA-HIACE-IV-XH10-VAN-KLH12-FACELIFT-01	4795	1800	2000	Toyota GB More Power New Looks for 2007 Toyota Hiace	https://media.toyota.co.uk/more-power-new-looks-for-2007-toyota-hiace/
EU-TOYOTA-HIACE-IV-XH10-VAN-KLH22-FACELIFT-01	5240	1800	1995	Toyota GB More Power New Looks for 2007 Toyota Hiace	https://media.toyota.co.uk/more-power-new-looks-for-2007-toyota-hiace/
EU-TOYOTA-HIACE-IV-XH10-VAN-KLH18-FACELIFT-01	4795	1800	2000	Drom Toyota Hiace KLH18 2.5 D-4D Van 4WD	https://www.drom.ru/catalog/toyota/hiace/277601/
EU-TOYOTA-HIACE-IV-XH10-VAN-KLH28-FACELIFT-01	5240	1800	1995	Drom Toyota Hiace KLH28 body specifications	https://www.drom.ru/catalog/toyota/frame/klh28/
```

## 下一步优先处理

1. 27277：拆分 H200 的 KDH200/KDH202/KDH212/KDH222 等实际车身分支，避免把宽泛 H200 代码错误压缩为单一尺寸。
2. 27282、27517、27518：闭合 Ducato X230 4×4 与 Vivaro A 单排/双排平台底盘边界。
3. 27337、27572、27573、27574：集中完成 Ram 1500、Silverado 1500 和 Silverado 2500 HD 的 Cab/Bed 组合。

推进信号：CONTINUE

[1]: https://www.autodoc.co.uk/car-parts/mounting-kit-charger-15070/toyota/hiace/hiace-iv-box-lxh1-rzh1-lh1/27278-2-5-d-4d-klh12-klh22?utm_source=chatgpt.com "Toyota Hiace 4 2.5 D-4D Mounting kit, charger"
[2]: https://www.drom.ru/catalog/toyota/hiace/277601/?utm_source=chatgpt.com "Toyota Hiace 2.5 D-4D MT Van 4WD - технические характеристики"


--- 发送 / 继续到 Round 7 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2501-2600_ktype_dimension_mapping_final.tsv
- all_2501-2600_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 7 / 下一步 ---
## 更新点

* 闭合 Ktype `27572`、`27573`。2007 Silverado 1500 GMT900 的 5.3L V8 与 FlexFuel 5.3L V8 均覆盖 4WD Regular Cab、Extended Cab 和 Crew Cab 的对应货斗组合，因此分别拆为六个物理外廓分支。官方资料同时给出了各 Cab/Bed 组合的长度，并明确宽度不含后视镜。
* 六个尺寸组按具体 Cab/Bed 组合首次建立；同一组由 `27572` 和 `27573` 共同引用，未因燃料类型不同重复建组。
* 本轮未修改既有尺寸组。

## 当前批次进度

* 输入 Ktype：100
* 已闭合 Ktype：94
* 待处理 Ktype：6
* READY 映射：161
* PENDING 映射：6
* 已确认尺寸组：97
* 本轮首次创建尺寸组：6
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27572_regcab_stdbed	27572	Pickup	Silverado 1500 II	GMT900	2	EU-CHEVROLET-SILVERADO-1500-II-GMT900-PICKUP-REGCAB-STDBED-4WD-01	HIGH	Regular Cab标准货斗四驱分支。	READY
27572_regcab_longbed	27572	Pickup	Silverado 1500 II	GMT900	2	EU-CHEVROLET-SILVERADO-1500-II-GMT900-PICKUP-REGCAB-LONGBED-4WD-01	HIGH	Regular Cab长货斗四驱分支。	READY
27572_extcab_shortbed	27572	Pickup	Silverado 1500 II	GMT900	4	EU-CHEVROLET-SILVERADO-1500-II-GMT900-PICKUP-EXTCAB-SHORTBED-4WD-01	HIGH	Extended Cab短货斗四驱分支。	READY
27572_extcab_stdbed	27572	Pickup	Silverado 1500 II	GMT900	4	EU-CHEVROLET-SILVERADO-1500-II-GMT900-PICKUP-EXTCAB-STDBED-4WD-01	HIGH	Extended Cab标准货斗四驱分支。	READY
27572_extcab_longbed	27572	Pickup	Silverado 1500 II	GMT900	4	EU-CHEVROLET-SILVERADO-1500-II-GMT900-PICKUP-EXTCAB-LONGBED-4WD-01	HIGH	Extended Cab长货斗四驱分支。	READY
27572_crewcab_shortbed	27572	Pickup	Silverado 1500 II	GMT900	4	EU-CHEVROLET-SILVERADO-1500-II-GMT900-PICKUP-CREWCAB-SHORTBED-4WD-01	HIGH	Crew Cab短货斗四驱分支。	READY
27573_regcab_stdbed	27573	Pickup	Silverado 1500 II	GMT900	2	EU-CHEVROLET-SILVERADO-1500-II-GMT900-PICKUP-REGCAB-STDBED-4WD-01	HIGH	Regular Cab标准货斗四驱分支。	READY
27573_regcab_longbed	27573	Pickup	Silverado 1500 II	GMT900	2	EU-CHEVROLET-SILVERADO-1500-II-GMT900-PICKUP-REGCAB-LONGBED-4WD-01	HIGH	Regular Cab长货斗四驱分支。	READY
27573_extcab_shortbed	27573	Pickup	Silverado 1500 II	GMT900	4	EU-CHEVROLET-SILVERADO-1500-II-GMT900-PICKUP-EXTCAB-SHORTBED-4WD-01	HIGH	Extended Cab短货斗四驱分支。	READY
27573_extcab_stdbed	27573	Pickup	Silverado 1500 II	GMT900	4	EU-CHEVROLET-SILVERADO-1500-II-GMT900-PICKUP-EXTCAB-STDBED-4WD-01	HIGH	Extended Cab标准货斗四驱分支。	READY
27573_extcab_longbed	27573	Pickup	Silverado 1500 II	GMT900	4	EU-CHEVROLET-SILVERADO-1500-II-GMT900-PICKUP-EXTCAB-LONGBED-4WD-01	HIGH	Extended Cab长货斗四驱分支。	READY
27573_crewcab_shortbed	27573	Pickup	Silverado 1500 II	GMT900	4	EU-CHEVROLET-SILVERADO-1500-II-GMT900-PICKUP-CREWCAB-SHORTBED-4WD-01	HIGH	Crew Cab短货斗四驱分支。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-CHEVROLET-SILVERADO-1500-II-GMT900-PICKUP-REGCAB-STDBED-4WD-01	5222	2029	1867	Chevrolet 2007 Silverado official brochure; AutoEvolution Silverado 1500 Regular Cab	https://xr793.com/wp-content/uploads/2022/07/2007-Chevrolet-Silverado-CN.pdf;https://www.autoevolution.com/cars/chevrolet-silverado-1500-regular-cab-2008.html
EU-CHEVROLET-SILVERADO-1500-II-GMT900-PICKUP-REGCAB-LONGBED-4WD-01	5702	2029	1867	Chevrolet 2007 Silverado official brochure; Auto123 Silverado 1500 4WD Regular Cab LWB	https://xr793.com/wp-content/uploads/2022/07/2007-Chevrolet-Silverado-CN.pdf;https://www.auto123.com/en/new-cars/technical-specs/chevrolet/silverado/2007/1500-4wd-regular-cab-lwb/lt/
EU-CHEVROLET-SILVERADO-1500-II-GMT900-PICKUP-EXTCAB-SHORTBED-4WD-01	5596	2029	1875	Chevrolet 2007 Silverado official brochure; Auto123 Silverado 1500 4WD Extended Cab SWB	https://xr793.com/wp-content/uploads/2022/07/2007-Chevrolet-Silverado-CN.pdf;https://www.auto123.com/en/new-cars/technical-specs/chevrolet/silverado/2007/1500-4wd-extended-cab-swb/lt/
EU-CHEVROLET-SILVERADO-1500-II-GMT900-PICKUP-EXTCAB-STDBED-4WD-01	5839	2029	1877	Chevrolet 2007 Silverado official brochure; Edmunds 2007 Silverado 1500 Extended Cab specifications	https://xr793.com/wp-content/uploads/2022/07/2007-Chevrolet-Silverado-CN.pdf;https://www.edmunds.com/chevrolet/silverado-1500/2007/extended-cab/features-specs/
EU-CHEVROLET-SILVERADO-1500-II-GMT900-PICKUP-EXTCAB-LONGBED-4WD-01	6320	2029	1869	Chevrolet 2007 Silverado official brochure; Auto123 Silverado 1500 4WD Extended Cab LWB	https://xr793.com/wp-content/uploads/2022/07/2007-Chevrolet-Silverado-CN.pdf;https://www.auto123.com/en/new-cars/technical-specs/chevrolet/silverado/2007/1500-4wd-extended-cab-lwb/lt/
EU-CHEVROLET-SILVERADO-1500-II-GMT900-PICKUP-CREWCAB-SHORTBED-4WD-01	5839	2029	1875	Chevrolet 2007 Silverado official brochure; Auto123 Silverado 1500 4WD Crew Cab SWB	https://xr793.com/wp-content/uploads/2022/07/2007-Chevrolet-Silverado-CN.pdf;https://www.auto123.com/en/new-cars/technical-specs/chevrolet/silverado/2007/1500-4wd-crew-cab-swb/lt/
```

## 下一步优先处理

1. `27574`：拆分 Silverado 2500 HD II 的 Regular Cab、Extended Cab、Crew Cab 与标准/长货斗组合。
2. `27337`：确认其属于 Ram 1500 第三代还是第四代，再按 Cab/Bed 组合一次性闭合。
3. `27277`、`27282`、`27517`、`27518`：完成 Hiace H200、Ducato X230 4×4 和 Vivaro A 平台底盘分支。

推进信号：CONTINUE


--- 发送 / 继续到 Round 8 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2501-2600_ktype_dimension_mapping_final.tsv
- all_2501-2600_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 8 / 下一步 ---
## 更新点

* Ktype `27337` 已按 Ram 1500 IV（DS）5.7L 4WD 的 Regular Cab 标准/长货斗、Quad Cab 标准货斗、Crew Cab 短货斗四种外廓拆分。官方运输规格表明确列出长度、不含后视镜宽度和高度。
* Ktype `27574` 已按 Silverado 2500 HD II 的 Regular Cab、Extended Cab、Crew Cab及标准/长货斗组合拆成五个外廓。各规格页均明确标注四驱、车长及不含后视镜宽度。([Edmunds][1])
* Ktype `27282` 按缓存优先规则，直接关联三个已有 Ducato X230 平台/底盘尺寸组；四驱动力形式未单独重复建组。
* `27277` 仍覆盖 H200 的多个车身代码和车顶组合，不能压缩成一个尺寸组。`27517`、`27518` 的记录边界是 Platform/Chassis，而官方资料中可闭合三维的是后装 Dropside 成品，二者不能强行等同，因此继续保留 PENDING。([Autodoc][2])

## 当前批次进度

* 输入 Ktype：100
* 已闭合 Ktype：97
* 待处理 Ktype：3
* READY 映射：173
* PENDING 映射：3
* 已确认尺寸组：106
* 本轮首次创建尺寸组：9
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27277	27277	Van	Hiace V (H200)				LOW	候选覆盖多个KDH2/TRH2车身及车顶分支。	PENDING: H200具体物理分支及各分支三维尚未完整闭合。
27282_swb	27282	Pickup	Ducato II X230	X230		EU-FIAT-DUCATO-X230-TRUCK-SWB-01	MEDIUM	X230短轴平台/底盘分支。	READY
27282_mwb	27282	Pickup	Ducato II X230	X230		EU-FIAT-DUCATO-X230-TRUCK-MWB-01	MEDIUM	X230中轴平台/底盘分支。	READY
27282_lwb	27282	Pickup	Ducato II X230	X230		EU-FIAT-DUCATO-X230-TRUCK-LWB-01	MEDIUM	X230长轴平台/底盘分支。	READY
27337_regcab_stdbed	27337	Pickup	Ram 1500 IV	DS	2	EU-DODGE-RAM-1500-IV-DS-PICKUP-REGCAB-STDBED-4WD-01	MEDIUM	Regular Cab标准货斗四驱分支。	READY
27337_regcab_longbed	27337	Pickup	Ram 1500 IV	DS	2	EU-DODGE-RAM-1500-IV-DS-PICKUP-REGCAB-LONGBED-4WD-01	MEDIUM	Regular Cab长货斗四驱分支。	READY
27337_quadcab_stdbed	27337	Pickup	Ram 1500 IV	DS	4	EU-DODGE-RAM-1500-IV-DS-PICKUP-QUADCAB-STDBED-4WD-01	MEDIUM	Quad Cab标准货斗四驱分支。	READY
27337_crewcab_shortbed	27337	Pickup	Ram 1500 IV	DS	4	EU-DODGE-RAM-1500-IV-DS-PICKUP-CREWCAB-SHORTBED-4WD-01	MEDIUM	Crew Cab短货斗四驱分支。	READY
27517	27517	Pickup	Vivaro A	X83	2		LOW	X83平台/底盘；成品转换外廓未唯一化。	PENDING: 平台/底盘可搭载不同转换车身，尚无唯一完整三维。
27518	27518	Pickup	Vivaro A	X83	2		LOW	X83平台/底盘；成品转换外廓未唯一化。	PENDING: 平台/底盘可搭载不同转换车身，尚无唯一完整三维。
27574_regcab_longbed	27574	Pickup	Silverado 2500 HD II	GMT900	2	EU-CHEVROLET-SILVERADO-2500-HD-II-GMT900-PICKUP-REGCAB-LONGBED-4WD-01	HIGH	Regular Cab长货斗四驱分支。	READY
27574_extcab_stdbed	27574	Pickup	Silverado 2500 HD II	GMT900	4	EU-CHEVROLET-SILVERADO-2500-HD-II-GMT900-PICKUP-EXTCAB-STDBED-4WD-01	HIGH	Extended Cab标准货斗四驱分支。	READY
27574_extcab_longbed	27574	Pickup	Silverado 2500 HD II	GMT900	4	EU-CHEVROLET-SILVERADO-2500-HD-II-GMT900-PICKUP-EXTCAB-LONGBED-4WD-01	HIGH	Extended Cab长货斗四驱分支。	READY
27574_crewcab_stdbed	27574	Pickup	Silverado 2500 HD II	GMT900	4	EU-CHEVROLET-SILVERADO-2500-HD-II-GMT900-PICKUP-CREWCAB-STDBED-4WD-01	HIGH	Crew Cab标准货斗四驱分支。	READY
27574_crewcab_longbed	27574	Pickup	Silverado 2500 HD II	GMT900	4	EU-CHEVROLET-SILVERADO-2500-HD-II-GMT900-PICKUP-CREWCAB-LONGBED-4WD-01	HIGH	Crew Cab长货斗四驱分支。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-DODGE-RAM-1500-IV-DS-PICKUP-REGCAB-STDBED-4WD-01	5309	2017	1941	Ram 1500 Vehicle Shipping Manual	https://www.ramtrucks.com/assets/pdf/specsheet/ram_1500_dimensions.pdf
EU-DODGE-RAM-1500-IV-DS-PICKUP-REGCAB-LONGBED-4WD-01	5867	2017	1935	Ram 1500 Vehicle Shipping Manual	https://www.ramtrucks.com/assets/pdf/specsheet/ram_1500_dimensions.pdf
EU-DODGE-RAM-1500-IV-DS-PICKUP-QUADCAB-STDBED-4WD-01	5817	2017	1951	Ram 1500 Vehicle Shipping Manual	https://www.ramtrucks.com/assets/pdf/specsheet/ram_1500_dimensions.pdf
EU-DODGE-RAM-1500-IV-DS-PICKUP-CREWCAB-SHORTBED-4WD-01	5817	2017	1953	Ram 1500 Vehicle Shipping Manual	https://www.ramtrucks.com/assets/pdf/specsheet/ram_1500_dimensions.pdf
EU-CHEVROLET-SILVERADO-2500-HD-II-GMT900-PICKUP-REGCAB-LONGBED-4WD-01	5707	2029	1941	Edmunds 2007 Chevrolet Silverado 2500HD Regular Cab specifications	https://www.edmunds.com/chevrolet/silverado-2500hd/2007/regular-cab/features-specs/
EU-CHEVROLET-SILVERADO-2500-HD-II-GMT900-PICKUP-EXTCAB-STDBED-4WD-01	5850	2029	1953	Edmunds 2007 Chevrolet Silverado 2500HD Extended Cab standard-bed specifications	https://www.edmunds.com/chevrolet/silverado-2500hd/2007/st-100820813/features-specs/
EU-CHEVROLET-SILVERADO-2500-HD-II-GMT900-PICKUP-EXTCAB-LONGBED-4WD-01	6330	2029	1948	Edmunds 2007 Chevrolet Silverado 2500HD Extended Cab long-bed specifications	https://www.edmunds.com/chevrolet/silverado-2500hd/2007/st-100820822/features-specs/
EU-CHEVROLET-SILVERADO-2500-HD-II-GMT900-PICKUP-CREWCAB-STDBED-4WD-01	6093	2029	1958	Edmunds 2007 Chevrolet Silverado 2500HD Crew Cab standard-bed specifications	https://www.edmunds.com/chevrolet/silverado-2500hd/2007/features-specs/
EU-CHEVROLET-SILVERADO-2500-HD-II-GMT900-PICKUP-CREWCAB-LONGBED-4WD-01	6571	2029	1953	Edmunds 2007 Chevrolet Silverado 2500HD Crew Cab long-bed specifications	https://www.edmunds.com/chevrolet/silverado-2500hd/2007/st-100822232/features-specs/
```

## 下一步优先处理

1. 完整闭合 `27277` 的 H200 标准宽标准顶、标准宽高顶、宽体中顶及超长宽体高顶分支。
2. 对 `27517`、`27518` 区分原始平台/底盘和具有固定三维的厂家 Dropside 成品；只有边界闭合后才创建派生行与尺寸组。

推进信号：CONTINUE

[1]: https://www.edmunds.com/chevrolet/silverado-2500hd/2007/regular-cab/features-specs/ "Used 2007 Chevrolet Silverado 2500HD Regular Cab Specs & Features | Edmunds"
[2]: https://www.autodoc.co.uk/car-parts/fuel-filter-10361/toyota/hiace/hiace-iv-box-trh2-kdh2/27277-2-5-d-4d "Fuel filter for Toyota Hiace 4 Van 2.5 D-4D 95 hp Diesel 2006 - 2026 2KD-FTV | AUTODOC"


--- 发送 / 继续到 Round 9 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2501-2600_ktype_dimension_mapping_final.tsv
- all_2501-2600_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 9 / 下一步 ---
## 更新点

* 闭合 `27517`、`27518`。Vauxhall 官方手册明确：长轴 Platform Cab 支持 F4R 2.0 汽油机和 F9Q 1.9 柴油机；Dropside 仅列 F9Q，因此 `27517` 只映射 Platform Cab，`27518` 同时覆盖 Platform Cab、标准地板 Dropside 和低地板 Dropside。
* 官方尺寸表确认三种外廓的不含后视镜宽度分别为 1904 mm、1980 mm、1980 mm，三维可以独立闭合。
* `27277` 仍未确认 70 kW Ktype 是否仅对应标准窄体低顶 H200，暂不将相近功率的官方 Panel Van 规格强行套用。

## 当前批次进度

* 输入 Ktype：100
* 已闭合 Ktype：99
* 待处理 Ktype：1
* READY 映射：177
* PENDING 映射：1
* 已确认尺寸组：109
* 本轮首次创建尺寸组：3
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27517_platformcab	27517	Pickup	Vivaro A	X83	2	EU-OPEL-VIVARO-A-X83-PLATFORM-CAB-LWB-01	HIGH	F4R长轴平台驾驶室分支。	READY
27518_platformcab	27518	Pickup	Vivaro A	X83	2	EU-OPEL-VIVARO-A-X83-PLATFORM-CAB-LWB-01	HIGH	F9Q长轴平台驾驶室分支。	READY
27518_dropside_standard	27518	Pickup	Vivaro A	X83	2	EU-OPEL-VIVARO-A-X83-DROPSIDE-STANDARD-01	HIGH	F9Q长轴标准地板Dropside分支。	READY
27518_dropside_lowfloor	27518	Pickup	Vivaro A	X83	2	EU-OPEL-VIVARO-A-X83-DROPSIDE-LOWFLOOR-01	HIGH	F9Q长轴低地板Dropside分支。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-OPEL-VIVARO-A-X83-PLATFORM-CAB-LWB-01	5130	1904	1981	Vauxhall Vivaro Owner's Manual January 2007	https://www.vauxhall.co.uk/content/dam/vauxhall/Home/PDFs/owners/owners-manuals/vivaro/vivaro-owners-manual-january-2007.pdf
EU-OPEL-VIVARO-A-X83-DROPSIDE-STANDARD-01	5350	1980	2000	Vauxhall Vivaro Owner's Manual January 2007	https://www.vauxhall.co.uk/content/dam/vauxhall/Home/PDFs/owners/owners-manuals/vivaro/vivaro-owners-manual-january-2007.pdf
EU-OPEL-VIVARO-A-X83-DROPSIDE-LOWFLOOR-01	5438	1980	2000	Vauxhall Vivaro Owner's Manual January 2007	https://www.vauxhall.co.uk/content/dam/vauxhall/Home/PDFs/owners/owners-manuals/vivaro/vivaro-owners-manual-january-2007.pdf
```

## 下一步优先处理

1. 仅处理 `27277`：确认 70 kW Hiace H200 Ktype 的具体车身代码、宽体/窄体及车顶边界。
2. 一旦闭合，立即进行一次机械收尾并输出两张最终完整 TSV及指定下载链接。

推进信号：CONTINUE


--- 发送 / 继续到 Round 10 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2501-2600_ktype_dimension_mapping_final.tsv
- all_2501-2600_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 10 / 下一步 ---
## 更新点

* `27277` 已将候选车身代码收窄为 `KDH200、KDH202、KDH212、KDH222`，不再保留泛化的 `TRH2_/KDH2_` 判断。零部件目录将 70 kW / 95 hp 的 2KD-FTV 版本关联至上述代码。([凯摩商店][1])
* `KDH200` 标准窄体和 `KDH222` 超长宽体高顶的三维已经能够闭合；Toyota 资料分别支持约 `4695 × 1695 × 1980 mm` 和 `5380 × 1880 × 2285 mm`。([丰田官网][2])
* `KDH212` 对应的具体宽体/车顶物理外廓仍缺少可直接落盘的完整三维页面；现在创建全部派生行会混入推断，因此暂不清零 PENDING。

## 当前批次进度

* 输入 Ktype：100
* 已闭合 Ktype：99
* 待处理 Ktype：1
* READY 映射：177
* PENDING 映射：1
* 已确认尺寸组：109
* 本轮首次创建/修正尺寸组：0
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27277	27277	Van	Hiace V (H200)				LOW	候选车身代码已收窄为KDH200、KDH202、KDH212、KDH222；KDH212物理外廓尚未闭合。	PENDING: 各车身代码与具体宽体、长度及车顶分支的对应关系尚未全部确认。
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

无

## 下一步优先处理

1. 只核对 `KDH212` 的直接车型级三维及其宽度口径。
2. 确认 `KDH200/KDH202` 是否属于同一物理外廓，避免相同三维重复建组。
3. `27277` 闭合后立即进行机械检查并输出两张最终完整 TSV、两个指定下载链接。

推进信号：CONTINUE

[1]: https://www.kmotorshop.com/en/article-detail/view/342941/crankshaft-bearing-shell-set-mb5423si0-75-king?utm_source=chatgpt.com "Crankshaft Bearing Shell Set - MB5423SI0.75 KING | K MOTORSHOP s.r.o."
[2]: https://www.toyota-global.com/company/history_of_toyota/75years/vehicle_lineage/car/id60015495/index.html?utm_source=chatgpt.com "75 Years of TOYOTA | TOYOTA MOTOR CORPORATION GLOBAL WEBSITE | Vehicle Lineage | In-depth Vehicle Information, Specification"


--- 发送 / 继续到 Round 11 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2501-2600_ktype_dimension_mapping_final.tsv
- all_2501-2600_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- 脚本异常 ---
异常: 对话分支失败（已尝试 3 次）: 没有找到最后一条用户消息的【在新聊天中分支】入口

