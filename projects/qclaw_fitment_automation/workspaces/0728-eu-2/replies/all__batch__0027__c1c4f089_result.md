# 任务：all 第 2601-2700 行
# 来源文件：all.tsv
# 任务 ID：all__batch__0027__c1c4f089


--- 发送 / 首次任务 ---
【任务名称】
【全量表更新】all 第 2601-2700 行

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
all 第 2601-2700 行

【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2601-2700_ktype_dimension_mapping_final.tsv
- all_2601-2700_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。

【跨批次已有尺寸组索引】
以下 ID 已经存在于累计表。三维和物理外廓完全相同时才可复用；如果当前证据得到不同三维，禁止改写已有组，必须使用同系列下一个可用序号创建新 DIMENSION_GROUP_ID，并把当前批次相关 Ktype 全部指向新组。

DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM
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
EU-BMW-7-SERIES-E65-SEDAN-FACELIFT-01	5039	1902	1491
EU-BMW-7-SERIES-E65-SEDAN-FACELIFT-4D-01	5039	1902	1491
EU-BMW-7-SERIES-E66-SEDAN-LWB-FACELIFT-01	5179	1902	1484
EU-CITROEN-BERLINGO-II-B9-MPV-5D-01	4380	1810	1801
EU-CITROEN-BERLINGO-II-B9-VAN-L1-01	4380	1810	1801
EU-CITROEN-BERLINGO-II-B9-VAN-L2-01	4628	1810	1828
EU-CITROEN-BERLINGO-I-M59-MPV-01	4137	1724	1810
EU-CITROEN-BERLINGO-I-M59-VAN-01	4137	1724	1819
EU-CITROEN-BERLINGO-I-VAN-MPV-01	4137	1724	1810
EU-CITROEN-JUMPER-I-230L-VAN-4X4-L1H1-01	4655	1998	2150
EU-CITROEN-JUMPER-I-230L-VAN-4X4-L2H2-01	5005	1998	2470
EU-CITROEN-JUMPER-III-BUS-VAN-L1H1-01	4963	2050	2254
EU-CITROEN-JUMPER-III-BUS-VAN-L2H1-01	5413	2050	2254
EU-CITROEN-JUMPER-III-BUS-VAN-L2H2-01	5413	2050	2524
EU-CITROEN-JUMPER-III-BUS-VAN-L3H2-01	5998	2050	2524
EU-CITROEN-JUMPER-III-BUS-VAN-L4H2-01	6363	2050	2524
EU-CITROEN-JUMPER-III-CHASSIS-CAB-L1-01	4908	2050	2153
EU-CITROEN-JUMPER-III-CHASSIS-CAB-L2-01	5358	2050	2153
EU-CITROEN-JUMPER-III-CHASSIS-CAB-L2S-01	5708	2050	2153
EU-CITROEN-JUMPER-III-CHASSIS-CAB-L3-01	5943	2050	2153
EU-CITROEN-JUMPER-III-CHASSIS-CAB-L4-01	6208	2050	2153
EU-CITROEN-JUMPER-III-VAN-L1H1-01	4963	2050	2254
EU-CITROEN-JUMPER-III-VAN-L2H1-01	5413	2050	2254
EU-CITROEN-JUMPER-III-VAN-L2H2-01	5413	2050	2524
EU-CITROEN-JUMPER-III-VAN-L3H2-01	5998	2050	2524
EU-CITROEN-JUMPER-III-VAN-L3H3-01	5998	2050	2764
EU-CITROEN-JUMPER-III-VAN-L4H2-01	6363	2050	2524
EU-CITROEN-JUMPER-III-VAN-L4H3-01	6363	2050	2764
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
EU-FIAT-MAREA-185-WEEKEND-WAGON-5D-01	4485	1740	1510
EU-FORD-SIERRA-II-HATCHBACK-5D-01	4458	1694	1407
EU-FORD-SIERRA-II-SEDAN-01	4501	1698	1407
EU-FORD-SIERRA-II-WAGON-01	4544	1720	1488
EU-HONDA-CIVIC-VI-HATCHBACK-3D-01	4190	1695	1375
EU-JAGUAR-XJS-COUPE-2D-01	4820	1793	1279
EU-JAGUAR-XJ-XJ40-SEDAN-4D-01	4990	1800	1360
EU-PEUGEOT-BOXER-I-244-CHASSIS-CAB-LWB-01	5506	2020	2150
EU-PEUGEOT-BOXER-I-244-CHASSIS-CAB-MWB-01	5006	2020	2150
EU-PEUGEOT-BOXER-I-244-FLOOR-CAB-LWB-01	5490	2020	2150
EU-PEUGEOT-BOXER-I-244-FLOOR-CAB-MWB-01	4990	2020	2150
EU-PEUGEOT-BOXER-I-244-PLATFORM-CAB-LWB-01	5680	2020	2150
EU-PEUGEOT-BOXER-I-244-PLATFORM-DOUBLE-CAB-LWB-01	5710	2020	2150
EU-PEUGEOT-BOXER-I-244-VAN-LWB-HIGHROOF-01	5599	2024	2505
EU-PEUGEOT-BOXER-I-244-VAN-LWB-SUPERHIGHROOF-01	5599	2024	2870
EU-PEUGEOT-BOXER-I-244-VAN-MWB-HIGHROOF-01	5099	2024	2505
EU-PEUGEOT-BOXER-I-244-VAN-MWB-LOWROOF-01	5099	2024	2150
EU-PEUGEOT-BOXER-I-244-VAN-MWB-SUPERHIGHROOF-01	5099	2024	2690
EU-PEUGEOT-BOXER-I-244-VAN-SWB-HIGHROOF-01	4749	2024	2515
EU-PEUGEOT-BOXER-I-244-VAN-SWB-LOWROOF-01	4749	2024	2150
EU-PEUGEOT-BOXER-II-BUS-L1H1-01	4963	2050	2254
EU-PEUGEOT-BOXER-II-BUS-L2H2-01	5413	2050	2522
EU-PEUGEOT-BOXER-II-BUS-L3H2-01	5998	2050	2522
EU-PEUGEOT-BOXER-II-CHASSIS-L1-01	4908	2050	2254
EU-PEUGEOT-BOXER-II-CHASSIS-L2-01	5358	2050	2254
EU-PEUGEOT-BOXER-II-CHASSIS-L3-01	5943	2050	2254
EU-PEUGEOT-BOXER-II-CHASSIS-L4-01	6308	2050	2270
EU-PEUGEOT-BOXER-II-VAN-L1H1-01	4963	2050	2254
EU-PEUGEOT-BOXER-II-VAN-L1H2-01	4963	2050	2522
EU-PEUGEOT-BOXER-II-VAN-L2H1-01	5413	2050	2254
EU-PEUGEOT-BOXER-II-VAN-L2H2-01	5413	2050	2522
EU-PEUGEOT-BOXER-II-VAN-L3H2-01	5998	2050	2522
EU-PEUGEOT-BOXER-II-VAN-L3H3-01	5998	2050	2760
EU-PEUGEOT-BOXER-II-VAN-L4H2-01	6363	2050	2522
EU-PEUGEOT-BOXER-II-VAN-L4H3-01	6363	2050	2760
EU-PEUGEOT-PARTNER-II-B9-VAN-L1-01	4380	1810	1834
EU-PEUGEOT-PARTNER-II-B9-VAN-L2-01	4628	1810	1834
EU-PEUGEOT-PARTNER-II-TEPEE-MPV-5D-01	4380	1810	1803
EU-PEUGEOT-PARTNER-I-PHASE-II-VAN-MPV-01	4140	1720	1810
EU-PEUGEOT-PARTNER-I-PHASE-I-VAN-MPV-01	4110	1720	1870
EU-PORSCHE-911-997-CARRERA-4-CONVERTIBLE-01	4427	1852	1310
EU-PORSCHE-911-997-CARRERA-4S-CONVERTIBLE-01	4427	1852	1300
EU-PORSCHE-911-997-COUPE-AWD-WIDEBODY-01	4427	1852	1300
EU-PORSCHE-911-997-COUPE-GT3-01	4445	1808	1280
EU-PORSCHE-911-997-COUPE-RWD-01	4427	1808	1300
EU-PORSCHE-911-997-GT2-COUPE-01	4469	1852	1285
EU-PORSCHE-911-997-TURBO-CONVERTIBLE-01	4450	1852	1300
EU-PORSCHE-911-997-TURBO-COUPE-01	4450	1852	1300
EU-RENAULT-MASTER-II-PHASE-II-CHASSIS-CAB-LWB-2D-01	5869	1990	2195
EU-RENAULT-MASTER-II-PHASE-II-CHASSIS-CAB-MWB-2D-01	5369	1990	2200
EU-RENAULT-MASTER-II-PHASE-II-VAN-L1H1-01	4899	1990	2253
EU-RENAULT-MASTER-II-PHASE-II-VAN-L1H2-01	4899	1990	2496
EU-RENAULT-MASTER-II-PHASE-II-VAN-L2H2-01	5399	1990	2493
EU-RENAULT-MASTER-II-PHASE-II-VAN-L2H3-01	5399	1990	2721
EU-RENAULT-MASTER-II-PHASE-II-VAN-L3H2-01	5899	1990	2490
EU-RENAULT-MASTER-II-PHASE-II-VAN-L3H3-01	5899	1990	2720
EU-RENAULT-RAPID-I-BODY-01	4056	1566	1776
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
EU-VOLVO-740-SEDAN-PREFL-01	4785	1760	1430
EU-VOLVO-S70-SEDAN-01	4720	1760	1400
EU-VW-GOLF-I-CABRIOLET-2D-01	3815	1630	1410
EU-VW-GOLF-II-HATCHBACK-01	3985	1665	1415
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
Renault	Rapid	1.4	Kasten/Großraumlimousine	Frontantrieb	Benzin	59	80	May 1995	Aug 1997	2024-03-01	27628
Renault	Rapid	1.4	Kasten/Großraumlimousine	Frontantrieb	Benzin	54	73	Sep 1991	Aug 1993	2024-03-01	27630
Mercedes-benz	S-Klasse	3.8	Stufenheck	Heckantrieb	Benzin	160	218	Aug 1980	Aug 1984	2024-03-01	27632
Opel	Kadett d	1	Schrägheck	Frontantrieb	Benzin	30	41	Sep 1979	Aug 1982	2024-03-01	27635
Opel	Kadett d	1	Schrägheck	Frontantrieb	Benzin	33	45	Sep 1979	Aug 1984	2024-03-01	27636
Opel	Kadett e	2.0 GSI	Cabriolet	Frontantrieb	Benzin	115	156	Sep 1990	May 1992	2024-03-01	27639
Opel	Kadett e	2	Cabriolet	Frontantrieb	Benzin	110	150	Sep 1990	May 1992	2024-03-01	27640
Audi	90	2.0 Quattro	Stufenheck	Allrad	Benzin	85	116	Aug 1984	Aug 1986	2024-03-01	27641
Jaguar	Xj	2.8	Stufenheck	Heckantrieb	Benzin	132	179	Oct 1968	Oct 1973	2024-03-01	27647
Mitsubishi	L 300 / delica ii	1.8	Bus	Heckantrieb	Benzin	60	82	Mar 1983	Oct 1986	2024-03-01	27648
Porsche	911	2.3 S	Targa	Heckantrieb	Benzin	140	190	Sep 1971	Aug 1973	2024-03-01	27649
Peugeot	204	1.4 D	Stufenheck	Frontantrieb	Diesel	33	45	Sep 1973	Dec 1977	2024-03-01	27658
Volvo	240	2	Stufenheck	Heckantrieb	Benzin	89	121	Sep 1984	Dec 1993	2024-03-01	27659
Ford	Sierra	2.0 4X4	Schrägheck	Allrad	Benzin	88	120	Oct 1991	Mar 1993	2024-03-01	27668
BMW	3	320 I	Stufenheck	Heckantrieb	Benzin	135	184	Mar 2012	Oct 2018	2024-03-01	27670
Peugeot	305 ii	1.8 D	Stufenheck	Frontantrieb	Diesel	44	60	Nov 1982	Dec 1988	2024-03-01	27673
BMW	3	316 D	Stufenheck	Heckantrieb	Diesel	85	116	Mar 2012	Oct 2018	2024-03-01	27674
Opel	Manta b cc	2	Coupe	Heckantrieb	Benzin	92	125	Aug 1981	Jul 1988	2024-03-01	27675
Opel	Manta b cc	1.6	Coupe	Heckantrieb	Benzin	55	75	Aug 1977	Jul 1981	2024-03-01	27676
Austin	Mini	1.3	Schrägheck	Frontantrieb	Benzin	53	72	Sep 1969	Sep 1980	2024-03-01	27678
Peugeot	405 ii break	2.0 4X4	Kombi	Allrad	Benzin	144	196	Aug 1992	Dec 1995	2024-03-01	27692
Citroën	Ax	Electric	Schrägheck	Frontantrieb	Elektro	25	34	Apr 1993	Oct 1996	2024-03-01	27693
Citroën	Ax	Electric	Schrägheck	Frontantrieb	Elektro	28	38	Nov 1996	Apr 1997	2024-03-01	27694
Citroën	Bx	1.4	Kombi	Frontantrieb	Benzin	44	60	Jan 1987	Jan 1992	2024-03-01	27698
Citroën	Bx	1.9 D	Kombi	Frontantrieb	Diesel	52	71	Jan 1987	Jan 1992	2024-03-01	27699
Citroën	Bx	1.4	Kombi	Frontantrieb	Benzin	52	71	Jan 1987	Jan 1992	2024-03-01	27700
Triumph	Tr 6 i	2.5	Cabriolet	Heckantrieb	Benzin	121	165	Mar 1969	Jan 1974	2024-03-01	27702
Renault	Trafic	2.1 D 4X4	Bus	Allrad	Diesel	43	58	May 1985	Feb 1989	2024-03-01	27705
Renault	Trafic	2	Bus	Frontantrieb	Benzin	58	79	Jul 1980	Apr 1985	2024-03-01	27706
VW	Golf i	1.3	Cabriolet	Frontantrieb	Benzin	40	54	Aug 1983	Jul 1986	2024-03-01	27713
Renault	18	1.6 4X4	Kombi	Allrad	Benzin	58	79	Feb 1979	Jun 1981	2024-03-01	27714
Renault	18	1.6	Kombi	Frontantrieb	Benzin	82	111	Oct 1983	Sep 1986	2024-03-01	27715
Renault	21	2	Kombi	Frontantrieb	Benzin	86	117	Jul 1989	Jun 1992	2024-03-01	27716
Renault	21	2	Kombi	Frontantrieb	Benzin	75	102	Jun 1991	May 1993	2024-03-01	27717
Alfa Romeo	Gt	1.8	Coupe	Heckantrieb	Benzin	80	109	Apr 1968	Nov 1971	2024-03-01	27718
BMW	7	735 I	Stufenheck	Heckantrieb	Benzin	160	218	Sep 1979	Sep 1982	2024-03-01	27719
Renault	4	0.7	Schrägheck	Frontantrieb	Benzin	15	20	Apr 1962	Apr 1971	2024-03-01	27722
Volvo	740	2	Stufenheck	Heckantrieb	Benzin	147	200	Sep 1990	Aug 1992	2024-03-01	27724
Renault	5	1.4	Schrägheck	Heckantrieb	Benzin	118	160	Sep 1980	Mar 1985	2024-03-01	27725
Talbot	Horizon	1.6	Schrägheck	Frontantrieb	Benzin	54	73	Aug 1983	Jul 1985	2024-03-01	27727
Renault	Super 5	1.6 D	Schrägheck	Frontantrieb	Diesel	40	54	Apr 1985	Dec 1990	2024-03-01	27728
Volvo	760	2.3	Stufenheck	Heckantrieb	Benzin	84	114	Aug 1984	Aug 1987	2024-03-01	27731
Volvo	760	2.8	Stufenheck	Heckantrieb	Benzin	125	170	Sep 1987	Aug 1990	2024-03-01	27732
Renault	Master i	2.4 D	Kasten	Heckantrieb	Diesel	52	71	Jul 1983	Aug 1986	2024-03-01	27737
Renault	Master i	2.4 D	Kasten	Heckantrieb	Diesel	50	68	Jul 1980	Jun 1983	2024-03-01	27738
Renault	Master i	2.4 D	Kasten	Heckantrieb	Diesel	53	72	Sep 1986	Dec 1992	2024-03-01	27739
Nissan	Bluebird	2.0 TD	Stufenheck	Frontantrieb	Diesel	62	84	Nov 1983	Dec 1985	2024-03-01	27743
Nissan	Cherry	1	Coupe	Frontantrieb	Benzin	33	45	Aug 1978	Jul 1981	2024-03-01	27748
Honda	Accord iv	1.8	Stufenheck	Frontantrieb	Benzin	77	105	Jan 1990	Dec 1991	2024-03-01	27752
Maserati	Ghibli	2	Coupe	Heckantrieb	Benzin	236	321	May 1992	Sep 1994	2024-03-01	27755
Opel	Diplomat b	2.8	Stufenheck	Heckantrieb	Benzin	103	140	Sep 1972	Aug 1978	2024-03-01	27756
Opel	Vectra b cc	2.5	Schrägheck	Frontantrieb	Benzin	144	196	Oct 1999	Jun 2000	2024-03-01	27758
Honda	Civic vi hatchback	2.0 Tdic	Schrägheck	Frontantrieb	Diesel	77	105	Nov 1998	Oct 2000	2025-11-01	27760
BMW	3	318 D	Stufenheck	Heckantrieb	Diesel	105	143	Mar 2012	Jun 2015	2024-03-01	27765
VW	Transporter t5	2.0 TDI	Kasten	Frontantrieb	Diesel	100	136	May 2010	Aug 2015	2024-03-01	27769
Peugeot	106 ii	Electric	Schrägheck	Frontantrieb	Elektro	20	27	Apr 1996	Jul 2004	2024-03-01	27770
Citroën	Berlingo	1.4	Großraumlimousine	Frontantrieb	Benzin	53	72	Nov 2002	Oct 2005	2024-03-01	27771
VW	Transporter t5	2.0 TDI 4motion	Kasten	Allrad	Diesel	100	136	May 2010	Aug 2015	2024-03-01	27774
Fiat	Marea	1.6	Stufenheck	Frontantrieb	Benzin	76	103	Sep 2000	Aug 2002	2024-03-01	27778
Fiat	Ducato	2	Kasten	Frontantrieb	Benzin	63	86	Jun 1990	May 1994	2024-03-01	27780
VW	Transporter t4	2.8 VR6	Kasten	Frontantrieb	Benzin	150	204	Jun 2000	Apr 2003	2024-03-01	27782
VW	Transporter t4	2.8 VR6	Kasten	Frontantrieb	Benzin	103	140	May 1996	May 2000	2024-03-01	27783
VW	Lt 28-35 i	2.4 Syncro	Pritsche/Fahrgestell	Allrad	Benzin	70	95	Aug 1992	Jul 1994	2024-03-01	27785
VW	Lt 28-35 i	2.4 D Syncro	Pritsche/Fahrgestell	Allrad	Diesel	55	75	Aug 1991	Jul 1992	2024-03-01	27787
VW	Lt 28-35 i	2.4 D Syncro	Pritsche/Fahrgestell	Allrad	Diesel	51	69	Aug 1991	Jul 1992	2024-03-01	27788
Citroën	Ds	2.4	Kombi	Frontantrieb	Benzin	93	126	Jul 1972	Jun 1974	2024-03-01	27792
Ford	Taunus	2.6	Stufenheck	Heckantrieb	Benzin	92	125	Sep 1967	Aug 1971	2024-03-01	27794
Ford	Taunus	2.3	Stufenheck	Heckantrieb	Benzin	92	125	Sep 1967	Aug 1971	2024-03-01	27795
Ford	Taunus	2.6	Stufenheck	Heckantrieb	Benzin	92	125	Sep 1967	Aug 1971	2024-03-01	27796
Ford	Taunus	2.3	Stufenheck	Heckantrieb	Benzin	92	125	Sep 1967	Aug 1971	2024-03-01	27797
Ford	Taunus	2.6	Coupe	Heckantrieb	Benzin	92	125	Sep 1967	Aug 1971	2024-03-01	27798
Ford	Taunus	2.3	Coupe	Heckantrieb	Benzin	92	125	Sep 1967	Aug 1971	2024-03-01	27799
Opel	Rekord a	1.7	Stufenheck	Heckantrieb	Benzin	55	75	Apr 1964	Aug 1965	2024-03-01	27801
Opel	Rekord b	1.9	Stufenheck	Heckantrieb	Benzin	55	75	Sep 1965	Aug 1966	2024-03-01	27804
Mitsubishi	L 300 / delica ii	1.8	Kasten	Heckantrieb	Benzin	60	82	Mar 1983	Oct 1986	2024-03-01	27805
Mitsubishi	L 300 iii	2.0 4WD	Kasten	Allrad	Benzin	63	86	Aug 1988	May 1994	2024-03-01	27806
Alfa Romeo	1750-2000	1.7	Stufenheck	Heckantrieb	Benzin	80	109	Apr 1968	Nov 1971	2024-03-01	27808
Volvo	S90 i	2.5	Stufenheck	Heckantrieb	Benzin	125	170	Nov 1996	Oct 1998	2024-03-01	27810
Volvo	V90 i	2.5	Kombi	Heckantrieb	Benzin	125	170	Nov 1996	Oct 1998	2024-03-01	27812
Rover	Montego	1.6	Kombi	Frontantrieb	Benzin	61	83	Oct 1990	Sep 1992	2024-03-01	27818
Fiat	Ducato panorama	2.0 4X4	Bus	Allrad	Benzin	63	86	Jun 1990	May 1994	2024-03-01	27819
Fiat	Ducato	2.5 D 4X4	Kasten	Allrad	Diesel	55	75	Sep 1986	May 1990	2024-03-01	27820
Fiat	Ducato	2.5 D 4X4	Kasten	Allrad	Diesel	53	72	Sep 1986	Oct 1987	2024-03-01	27821
Honda	Civic vi fastback	2.0 Tdic	Schrägheck	Frontantrieb	Diesel	77	105	Nov 1998	Oct 2000	2024-03-01	27822
Renault	Espace iii	2.2 D	Großraumlimousine	Frontantrieb	Diesel	84	114	Nov 1997	Jan 2000	2024-03-01	27823
VW	Transporter t5	2.0 TDI	Pritsche/Fahrgestell	Frontantrieb	Diesel	100	136	May 2010	Aug 2015	2024-03-01	27824
Renault	Trafic	2	Kasten	Heckantrieb	Benzin	60	82	May 1985	Feb 1989	2024-03-01	27827
Renault	Trafic	2	Kasten	Heckantrieb	Benzin	58	79	Jul 1980	Apr 1985	2024-03-01	27828
Renault	Trafic	2	Kasten	Frontantrieb	Benzin	58	79	Jul 1980	Apr 1985	2024-03-01	27829
Peugeot	Boxer	2.0 4X4	Kasten	Allrad	Benzin	80	109	Mar 1996	Sep 1998	2024-03-01	27830
Peugeot	Partner	1.9 D 4X4	Großraumlimousine	Allrad	Diesel	51	69	Apr 2004	Aug 2005	2024-03-01	27836
Peugeot	Partner	1.4	Großraumlimousine	Frontantrieb	Benzin	54	73	Nov 2002	Oct 2006	2024-03-01	27837
Peugeot	Partner	2.0 HDI 4X4	Großraumlimousine	Allrad	Diesel	66	90	Apr 2004	Aug 2005	2024-03-01	27838
Mazda	E	E2000 4WD	Kasten	Allrad	Benzin	63	86	Nov 1987	Sep 1989	2024-03-01	27847
Ferrari	Mondial	3.2	Cabriolet	Heckantrieb	Benzin	188	256	Oct 1987	Sep 1989	2024-03-01	27849
VW	Lt 28-35 ii	2.8 TDI	Bus	Heckantrieb	Diesel	96	131	Jan 1999	Jan 2002	2024-03-01	27850
Citroën	Jumper i	2.5 DT 4X4	Kasten	Allrad	Diesel	76	103	Oct 1996	Aug 1997	2024-03-01	27854
Ford	Scorpio i turnier	2.5 D	Kombi	Heckantrieb	Diesel	51	69	Oct 1990	Aug 1992	2024-03-01	27862
Honda	Accord iii aerodeck	2	Kombi	Frontantrieb	Benzin	101	137	Jan 1986	Dec 1986	2024-03-01	27871
Volvo	S70	2.4 AWD	Stufenheck	Allrad	Benzin	103	140	Apr 1999	Sep 2000	2024-03-01	27874


--- Round 1 / 首次发送 ---
## 更新点

* 复用 13 个既有尺寸组，完成 Renault Rapid、Ford Sierra II、VW Golf I Cabriolet、VW Transporter T5 厢式车、Citroën Berlingo M59、Peugeot Partner 前驱乘用版、Citroën Jumper I 4×4 和 Volvo S70 的映射。
* Mercedes-Benz 380 SE/SEL 按 W126 短轴与 V126 长轴拆分，两者长度和高度不同，不能共用尺寸组。([汽车数据网][1])
* BMW F30 跨越改款节点的 Ktype 拆为改款前和 LCI 两个物理分支；官方规格显示车长由 4624 mm 变为 4633 mm。
* 新建 Citroën AX Electrique、Citroën BX Phase II Break 和 Honda Civic VI Fastback 尺寸组。BX 三个 Ktype 共用同一旅行车外廓；Civic 两个 2.0 TD Ktype 共用 MB7 五门 Fastback 外廓。([汽车目录][2])
* Peugeot Partner Dangel 四驱版本暂不复用前驱尺寸组，需独立确认四驱底盘是否改变整车高度。

## 当前批次进度

* 输入 Ktype：100
* READY Ktype：21
* READY 映射行：33
* PENDING Ktype：79
* 已确认尺寸组：20
* 本轮首次新建尺寸组：7
* 本轮复用既有尺寸组：13
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27628	27628	Van	Rapid I			EU-RENAULT-RAPID-I-BODY-01	MEDIUM	Kasten/MPV共用同一外廓，按Van归类。	READY
27630	27630	Van	Rapid I			EU-RENAULT-RAPID-I-BODY-01	MEDIUM	Kasten/MPV共用同一外廓，按Van归类。	READY
27632_swb	27632	Sedan	S-Class W126	W126	4	EU-MERCEDES-BENZ-S-CLASS-W126-SEDAN-SWB-4D-01	HIGH	380 SE短轴四门分支。	READY
27632_lwb	27632	Sedan	S-Class W126	V126	4	EU-MERCEDES-BENZ-S-CLASS-V126-SEDAN-LWB-4D-01	HIGH	380 SEL长轴四门分支。	READY
27668	27668	Hatchback	Sierra II		5	EU-FORD-SIERRA-II-HATCHBACK-5D-01	HIGH	五门掀背物理外廓。	READY
27670_prefl	27670	Sedan	3 Series F30	F30	4	EU-BMW-3-F30-SEDAN-4D-PREFL-01	HIGH	F30改款前四门轿车。	READY
27670_facelift	27670	Sedan	3 Series F30	F30	4	EU-BMW-3-F30-SEDAN-4D-FACELIFT-01	HIGH	F30 LCI四门轿车；长度变化需拆分。	READY
27674_prefl	27674	Sedan	3 Series F30	F30	4	EU-BMW-3-F30-SEDAN-4D-PREFL-01	HIGH	F30改款前四门轿车。	READY
27674_facelift	27674	Sedan	3 Series F30	F30	4	EU-BMW-3-F30-SEDAN-4D-FACELIFT-01	HIGH	F30 LCI四门轿车；长度变化需拆分。	READY
27693	27693	Hatchback	AX Phase II	ZA	3	EU-CITROEN-AX-PHASE-II-HATCHBACK-3D-01	HIGH	AX Electrique三门外廓。	READY
27694	27694	Hatchback	AX Phase II	ZA	3	EU-CITROEN-AX-PHASE-II-HATCHBACK-3D-01	HIGH	AX Electrique三门外廓。	READY
27698	27698	Wagon	BX I Phase II	XB	5	EU-CITROEN-BX-I-PHASE-II-BREAK-WAGON-5D-01	HIGH	BX Break五门旅行车外廓。	READY
27699	27699	Wagon	BX I Phase II	XB	5	EU-CITROEN-BX-I-PHASE-II-BREAK-WAGON-5D-01	HIGH	BX Break五门旅行车外廓。	READY
27700	27700	Wagon	BX I Phase II	XB	5	EU-CITROEN-BX-I-PHASE-II-BREAK-WAGON-5D-01	HIGH	BX Break五门旅行车外廓。	READY
27713	27713	Convertible	Golf I	155	2	EU-VW-GOLF-I-CABRIOLET-2D-01	HIGH	Golf I Cabriolet两门外廓。	READY
27760	27760	Hatchback	Civic VI Fastback	MB7	5	EU-HONDA-CIVIC-VI-FASTBACK-HATCHBACK-5D-01	HIGH	原始Schrägheck对应五门Fastback车身。	READY
27765	27765	Sedan	3 Series F30	F30	4	EU-BMW-3-F30-SEDAN-4D-PREFL-01	HIGH	生产区间止于LCI前，映射改款前外廓。	READY
27769_swb_lowroof	27769	Van	Transporter T5 Facelift			EU-VW-TRANSPORTER-T5-VAN-SWB-LOWROOF-01	MEDIUM	短轴低顶分支。	READY
27769_swb_medroof	27769	Van	Transporter T5 Facelift			EU-VW-TRANSPORTER-T5-VAN-SWB-MEDROOF-01	MEDIUM	短轴中顶分支。	READY
27769_lwb_lowroof	27769	Van	Transporter T5 Facelift			EU-VW-TRANSPORTER-T5-VAN-LWB-LOWROOF-01	MEDIUM	长轴低顶分支。	READY
27769_lwb_medroof	27769	Van	Transporter T5 Facelift			EU-VW-TRANSPORTER-T5-VAN-LWB-MEDROOF-01	MEDIUM	长轴中顶分支。	READY
27769_lwb_highroof	27769	Van	Transporter T5 Facelift			EU-VW-TRANSPORTER-T5-VAN-LWB-HIGHROOF-01	MEDIUM	长轴高顶分支。	READY
27771	27771	MPV	Berlingo I Phase II	M59	5	EU-CITROEN-BERLINGO-I-M59-MPV-01	HIGH	M59乘用型五门外廓。	READY
27774_swb_lowroof	27774	Van	Transporter T5 Facelift			EU-VW-TRANSPORTER-T5-VAN-SWB-LOWROOF-01	MEDIUM	短轴低顶分支。	READY
27774_swb_medroof	27774	Van	Transporter T5 Facelift			EU-VW-TRANSPORTER-T5-VAN-SWB-MEDROOF-01	MEDIUM	短轴中顶分支。	READY
27774_lwb_lowroof	27774	Van	Transporter T5 Facelift			EU-VW-TRANSPORTER-T5-VAN-LWB-LOWROOF-01	MEDIUM	长轴低顶分支。	READY
27774_lwb_medroof	27774	Van	Transporter T5 Facelift			EU-VW-TRANSPORTER-T5-VAN-LWB-MEDROOF-01	MEDIUM	长轴中顶分支。	READY
27774_lwb_highroof	27774	Van	Transporter T5 Facelift			EU-VW-TRANSPORTER-T5-VAN-LWB-HIGHROOF-01	MEDIUM	长轴高顶分支。	READY
27822	27822	Hatchback	Civic VI Fastback	MB7	5	EU-HONDA-CIVIC-VI-FASTBACK-HATCHBACK-5D-01	HIGH	五门Fastback车身。	READY
27837	27837	MPV	Partner I Phase II		5	EU-PEUGEOT-PARTNER-I-PHASE-II-VAN-MPV-01	HIGH	前驱乘用型共用Phase II外廓。	READY
27854_l1h1	27854	Van	Jumper I	230L		EU-CITROEN-JUMPER-I-230L-VAN-4X4-L1H1-01	HIGH	四驱L1H1分支。	READY
27854_l2h2	27854	Van	Jumper I	230L		EU-CITROEN-JUMPER-I-230L-VAN-4X4-L2H2-01	HIGH	四驱L2H2分支。	READY
27874	27874	Sedan	S70 I	P80	4	EU-VOLVO-S70-SEDAN-01	HIGH	S70四门轿车外廓。	READY
```

## 本轮新增/修改的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-MERCEDES-BENZ-S-CLASS-W126-SEDAN-SWB-4D-01	4995	1820	1436	Auto-Data Mercedes-Benz 380 SE W126 218 Hp; Auto-Data Mercedes-Benz 380 SE W126 204 Hp	https://www.auto-data.net/en/mercedes-benz-s-class-se-w126-380-se-v8-218hp-automatic-13100; https://www.auto-data.net/en/mercedes-benz-s-class-se-w126-380-se-v8-204hp-automatic-13099
EU-MERCEDES-BENZ-S-CLASS-V126-SEDAN-LWB-4D-01	5135	1820	1440	Auto-Data Mercedes-Benz 380 SEL V126 218 Hp; Auto-Data Mercedes-Benz 380 SEL V126 204 Hp	https://www.auto-data.net/en/mercedes-benz-s-class-sel-v126-380-sel-v8-218hp-automatic-42938; https://www.auto-data.net/en/mercedes-benz-s-class-sel-v126-380-sel-v8-204hp-automatic-42940
EU-BMW-3-F30-SEDAN-4D-PREFL-01	4624	1811	1429	BMW Group PressClub BMW 3 Series Sedan official specifications	https://www.press.bmwgroup.com/global/article/attachment/T0131800EN/207748/Specifications_BMW_3_Series_Sedan_316i_11_2012.pdf
EU-BMW-3-F30-SEDAN-4D-FACELIFT-01	4633	1811	1429	BMW Taiwan F30 LCI official standard equipment	https://bps.bmw.com.tw/uploads/bps/1563529610_CnMiBB.pdf
EU-CITROEN-AX-PHASE-II-HATCHBACK-3D-01	3525	1555	1355	Automobile-Catalog 1995 Citroen AX Electrique	https://www.automobile-catalog.com/car/1995/1450970/citroen_ax_electrique.html
EU-CITROEN-BX-I-PHASE-II-BREAK-WAGON-5D-01	4399	1682	1431	Auto-Data Citroen BX I Break Phase II 14 E; Auto-Data Citroen BX I Break Phase II 19 D	https://www.auto-data.net/en/citroen-bx-i-break-phase-ii-1987-14-e-72hp-15266; https://www.auto-data.net/en/citroen-bx-i-break-phase-ii-1987-19-d-71hp-15279
EU-HONDA-CIVIC-VI-FASTBACK-HATCHBACK-5D-01	4325	1695	1390	Auto-Data Honda Civic VI Fastback 2.0 TD 105 Hp	https://www.auto-data.net/en/honda-civic-vi-fastback-2.0-td-105hp-12247
```

## 下一步优先处理

1. 集中处理 Opel Kadett D、Kadett E、Manta、Rekord 和 Diplomat，确定门数、车身代码及不同外廓边界。
2. 处理 Renault Trafic I、Master I、Fiat Ducato I/Panorama 的轴距、车顶和四驱分支。
3. 独立核对 Peugeot Partner Dangel 4×4、VW Transporter T4、T5 底盘车及 LT I/II 商用车分支。
4. 批量闭合 Ford Taunus、Volvo 240/760/S90/V90、Renault 18/21、Audi 90、Jaguar XJ、Porsche 911 等乘用车聚类。

推进信号：CONTINUE

[1]: https://www.auto-data.net/en/mercedes-benz-s-class-se-w126-380-se-v8-218hp-automatic-13100 "Mercedes-Benz S-class SE (W126) 380 SE V8 (218 Hp) Automatic | Technical specs, data, fuel consumption, Dimensions"
[2]: https://www.automobile-catalog.com/car/1995/1450970/citroen_ax_electrique.html?utm_source=chatgpt.com "1995 Citroen AX Electrique (n. ) (model for Europe ) car ..."


--- 发送 / 继续到 Round 2 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2601-2700_ktype_dimension_mapping_final.tsv
- all_2601-2700_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 2 / 下一步 ---
## 更新点

* 闭合 Renault 21 Combi 两个 Ktype，均关联 K48 五门旅行车尺寸组，不按功率版本重复建组。([汽车数据网][1])
* 闭合 Volvo 760 两个 Ktype；2.3 与 2.8 版本的四门轿车外廓三维一致，合并为一个稳定尺寸组。([汽车数据网][2])
* 新增 Honda Accord IV、Fiat Marea 185、Volvo S90 I、Volvo V90 I、Renault Espace III 映射及尺寸组。Honda 与 Fiat 来源明确给出不含后视镜宽度。([汽车目录][3])

## 当前批次进度

* 输入 Ktype：100
* READY Ktype：30
* READY 映射行：42
* PENDING Ktype：70
* 已确认尺寸组：27
* 本轮新增尺寸组：7
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27716	27716	Wagon	21 Combi	K48	5	EU-RENAULT-21-K48-WAGON-5D-01	HIGH	K48五门旅行车外廓。	READY
27717	27717	Wagon	21 Combi	K48	5	EU-RENAULT-21-K48-WAGON-5D-01	HIGH	K48五门旅行车外廓。	READY
27731	27731	Sedan	760			EU-VOLVO-760-SEDAN-4D-01	MEDIUM	四门轿车外廓。	READY
27732	27732	Sedan	760			EU-VOLVO-760-SEDAN-4D-01	MEDIUM	四门轿车外廓。	READY
27752	27752	Sedan	Accord IV		4	EU-HONDA-ACCORD-IV-SEDAN-4D-01	HIGH	四门轿车外廓。	READY
27778	27778	Sedan	Marea	185	4	EU-FIAT-MAREA-185-SEDAN-4D-01	HIGH	185四门轿车外廓。	READY
27810	27810	Sedan	S90 I		4	EU-VOLVO-S90-I-SEDAN-4D-01	MEDIUM	四门轿车外廓。	READY
27812	27812	Wagon	V90 I		5	EU-VOLVO-V90-I-WAGON-5D-01	MEDIUM	五门旅行车外廓。	READY
27823	27823	MPV	Espace III	JE	5	EU-RENAULT-ESPACE-III-JE-MPV-5D-01	HIGH	JE五门MPV外廓。	READY
```

## 本轮新增/修改的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-RENAULT-21-K48-WAGON-5D-01	4693	1726	1450	Auto-Data Renault 21 Combi K48 2.0 i	https://www.auto-data.net/en/renault-21-combi-k48-2.0-i-120hp-10383
EU-VOLVO-760-SEDAN-4D-01	4785	1760	1430	Auto-Data Volvo 760 2.3 Turbo; Auto-Data Volvo 760 2.8	https://www.auto-data.net/en/volvo-760-704-764-2.3-turbo-704-182hp-9484; https://www.auto-data.net/en/volvo-760-704-764-2.8-764-147hp-9490
EU-HONDA-ACCORD-IV-SEDAN-4D-01	4685	1695	1390	Automobile-Catalog 1990 Honda Accord 1.8	https://www.automobile-catalog.com/car/1990/1104860/honda_accord_1_8.html
EU-FIAT-MAREA-185-SEDAN-4D-01	4390	1741	1420	Automobile-Catalog 2001 Fiat Marea 100 16V ELX	https://www.automobile-catalog.com/car/2001/722510/fiat_marea_100_16v_elx.html
EU-VOLVO-S90-I-SEDAN-4D-01	4871	1750	1422	Auto-Data Volvo S90 2.9 24V	https://www.auto-data.net/en/volvo-s90-2.9-24v-204hp-9441
EU-VOLVO-V90-I-WAGON-5D-01	4861	1750	1450	Auto-Data Volvo V90 3.0 24V	https://www.auto-data.net/en/volvo-v90-3.0-24v-204hp-9311
EU-RENAULT-ESPACE-III-JE-MPV-5D-01	4517	1810	1773	Auto-Data Renault Espace III JE 2.2 TD	https://www.auto-data.net/en/renault-espace-iii-je-2.2-td-12v-113hp-10503
```

## 下一步优先处理

1. 批量闭合 Opel Kadett D、Kadett E Cabriolet、Manta B CC、Diplomat B、Rekord A/B。
2. 处理 Renault Trafic I、Master I 和 Fiat Ducato I 的轴距、车顶及四驱派生分支。
3. 处理 Ford Taunus Sedan/Coupe 聚类，以及 Volvo 240、740 的改款边界。
4. 核对 VW Transporter T4、T5 底盘车和 LT I/II 的完整车长、车顶及驾驶室分支。

推进信号：CONTINUE

[1]: https://www.auto-data.net/en/renault-21-combi-k48-2.0-i-120hp-10383 "Renault 21 Combi (K48) 2.0 i (120 Hp) | Technical specs, data, fuel consumption, Dimensions"
[2]: https://www.auto-data.net/en/volvo-760-704-764-2.3-turbo-704-182hp-9484 "Volvo 760 (704,764) 2.3 Turbo (704) (182 Hp) | Technical specs, data, fuel consumption, Dimensions"
[3]: https://www.automobile-catalog.com/car/1990/1104860/honda_accord_1_8.html?utm_source=chatgpt.com "1990 Honda Accord 1.8 Specs Review (73.5 kW / 100 PS / 99 hp) (for Europe )"


--- 发送 / 继续到 Round 3 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2601-2700_ktype_dimension_mapping_final.tsv
- all_2601-2700_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 3 / 下一步 ---
## 更新点

* 闭合 Alfa Romeo 1750 系列两种独立外廓：1750 GTV Coupe 与 1750 Berlina Sedan 分别建组，不因相同生产时期合并。([汽车目录][1])
* 闭合 Porsche 911 F Targa、Triumph TR6、BMW 7 Series E23、Maserati Ghibli II、Opel Diplomat B 等单一车身映射。([汽车数据网][2])
* Peugeot 106 Electrique 按 Phase II 三门电动车外廓独立建组，未直接复用普通 106 II 的通用尺寸。([Car Info][3])

## 当前批次进度

* 输入 Ktype：100
* READY Ktype：40
* READY 映射行：52
* PENDING Ktype：60
* 已确认尺寸组：37
* 本轮新增尺寸组：10
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27649	27649	Convertible	911 F Targa	F	2	EU-PORSCHE-911-F-TARGA-2D-01	HIGH	F系列Targa两门外廓。	READY
27658	27658	Sedan	204		4	EU-PEUGEOT-204-SEDAN-4D-01	MEDIUM	四门轿车外廓。	READY
27702	27702	Convertible	TR 6		2	EU-TRIUMPH-TR-6-CONVERTIBLE-2D-01	HIGH	两门敞篷外廓。	READY
27718	27718	Coupe	1750 GTV	105	2	EU-ALFA-ROMEO-1750-GTV-COUPE-2D-01	MEDIUM	Tipo 105两门Coupe外廓。	READY
27719	27719	Sedan	7 Series E23	E23	4	EU-BMW-7-SERIES-E23-SEDAN-4D-PREFL-01	HIGH	E23改款前四门轿车。	READY
27755	27755	Coupe	Ghibli II		2	EU-MASERATI-GHIBLI-II-COUPE-2D-01	HIGH	两门Coupe外廓。	READY
27756	27756	Sedan	Diplomat B		4	EU-OPEL-DIPLOMAT-B-SEDAN-4D-01	HIGH	四门轿车外廓。	READY
27770	27770	Hatchback	106 II		3	EU-PEUGEOT-106-II-HATCHBACK-3D-ELECTRIC-01	HIGH	Electrique三门外廓。	READY
27792	27792	Wagon	DS Break		5	EU-CITROEN-DS-BREAK-WAGON-5D-01	MEDIUM	DS Break五门旅行车外廓。	READY
27808	27808	Sedan	1750 Berlina		4	EU-ALFA-ROMEO-1750-BERLINA-SEDAN-4D-01	HIGH	四门Berlina外廓。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-PORSCHE-911-F-TARGA-2D-01	4291	1625	1320	Auto-Data Porsche 911 Targa F	https://www.auto-data.net/en/porsche-911-targa-f-generation-1526
EU-PEUGEOT-204-SEDAN-4D-01	3970	1560	1400	Auto-Data Peugeot 204	https://www.auto-data.net/en/peugeot-204-generation-1263
EU-TRIUMPH-TR-6-CONVERTIBLE-2D-01	3937	1470	1270	Auto-Data Triumph TR 6	https://www.auto-data.net/en/triumph-tr-6-generation-1294
EU-ALFA-ROMEO-1750-GTV-COUPE-2D-01	4100	1580	1315	Automobile-Catalog Alfa Romeo 1750 GTV	https://www.automobile-catalog.com/car/1968/65030/alfa_romeo_1750_gtv.html
EU-BMW-7-SERIES-E23-SEDAN-4D-PREFL-01	4860	1800	1430	Auto-Data BMW 7 Series E23	https://www.auto-data.net/en/bmw-7-series-e23-generation-1987
EU-MASERATI-GHIBLI-II-COUPE-2D-01	4223	1775	1300	Auto-Data Maserati Ghibli II	https://www.auto-data.net/en/maserati-ghibli-ii-generation-2258
EU-OPEL-DIPLOMAT-B-SEDAN-4D-01	4920	1852	1450	Auto-Data Opel Diplomat B	https://www.auto-data.net/en/opel-diplomat-b-generation-560
EU-PEUGEOT-106-II-HATCHBACK-3D-ELECTRIC-01	3678	1594	1380	Automobile-Catalog Peugeot 106 Electric; Car.info Peugeot 106 3-door Phase II	https://www.automobile-catalog.com/car/2000/2609645/peugeot_106_electric_electrique.html; https://www.car.info/en-se/peugeot/106/106-3-door-phase-ii-553208
EU-CITROEN-DS-BREAK-WAGON-5D-01	5026	1803	1530	Auto-Data Citroen DS Break	https://www.auto-data.net/en/citroen-ds-break-generation-3327
EU-ALFA-ROMEO-1750-BERLINA-SEDAN-4D-01	4390	1565	1430	Automobile-Catalog Alfa Romeo 1750 Berlina	https://www.automobile-catalog.com/car/1968/65150/alfa_romeo_1750_berlina.html
```

## 下一步优先处理

1. 拆分 Ford Taunus P7A/P7B、Sedan/Coupe 及门数外廓。
2. 批量处理 Opel Kadett D、Kadett E Cabriolet、Manta B CC、Rekord A/B。
3. 处理 Renault Trafic I、Master I、Fiat Ducato I、VW Transporter T4 与 LT 商用车的轴距和车顶分支。
4. 解决 Peugeot 405 II Break 4×4、Partner Dangel 4×4 等输入版本与常规外廓资料存在冲突的记录。

推进信号：CONTINUE

[1]: https://www.automobile-catalog.com/car/1968/65030/alfa_romeo_1750_gtv.html?utm_source=chatgpt.com "1968 Alfa Romeo 1750 GTV Specs Review (83 kW / 113 PS / 111 hp) (for Europe Australia )"
[2]: https://www.auto-data.net/en/porsche-911-targa-f-generation-1526 "Porsche 911 Targa (F) | Technical Specs, Fuel consumption, Dimensions"
[3]: https://www.car.info/en-se/peugeot/106/106-3-door-phase-ii-553208?utm_source=chatgpt.com "Peugeot 106 3-door Phase II 1996 - 2004"


--- 发送 / 继续到 Round 4 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2601-2700_ktype_dimension_mapping_final.tsv
- all_2601-2700_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 4 / 下一步 ---
## 更新点

* 本轮闭合 8 个 Ktype，新增 7 个尺寸组。
* Opel Kadett E Cabriolet 两个动力版本共用同一双门敞篷外廓，不按发动机功率重复建组。([汽车目录][1])
* Audi 90 B2 quattro、Jaguar XJ Series I、Peugeot 305 II、Talbot Horizon、Opel Vectra B CC facelift 和 Ferrari Mondial 3.2 Cabriolet 均完成映射及首次建组。([汽车数据网][2])

## 当前批次进度

* 输入 Ktype：100
* READY Ktype：48
* READY 映射行：60
* PENDING Ktype：52
* 已确认尺寸组：44
* 本轮首次新建尺寸组：7
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27639	27639	Convertible	Kadett E		2	EU-OPEL-KADETT-E-CONVERTIBLE-2D-FACELIFT-01	MEDIUM	Kadett E后期双门敞篷外廓。	READY
27640	27640	Convertible	Kadett E		2	EU-OPEL-KADETT-E-CONVERTIBLE-2D-FACELIFT-01	MEDIUM	Kadett E后期双门敞篷外廓。	READY
27641	27641	Sedan	90 B2	85	4	EU-AUDI-90-B2-TYP85-SEDAN-4D-01	HIGH	Typ 85 quattro四门轿车外廓。	READY
27647	27647	Sedan	XJ Series I		4	EU-JAGUAR-XJ-SERIES-I-SEDAN-4D-SWB-01	HIGH	Series I 2.8短轴四门轿车。	READY
27673	27673	Sedan	305 II	581M	4	EU-PEUGEOT-305-II-581M-SEDAN-4D-01	MEDIUM	581M四门轿车外廓。	READY
27727	27727	Hatchback	Horizon		5	EU-TALBOT-HORIZON-HATCHBACK-5D-FACELIFT-01	HIGH	后期五门掀背外廓。	READY
27758	27758	Hatchback	Vectra B Facelift	J96	5	EU-OPEL-VECTRA-B-CC-HATCHBACK-5D-FACELIFT-01	HIGH	CC改款后五门掀背外廓。	READY
27849	27849	Convertible	Mondial 3.2	F108	2	EU-FERRARI-MONDIAL-3-2-CONVERTIBLE-2D-01	HIGH	Mondial 3.2双门敞篷外廓。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-OPEL-KADETT-E-CONVERTIBLE-2D-FACELIFT-01	3998	1663	1380	Automobile-Catalog Opel Kadett Cabrio GSi	https://www.automobile-catalog.com/car/1987/2460290/opel_kadett_cabrio_gsi_cat.html
EU-AUDI-90-B2-TYP85-SEDAN-4D-01	4465	1682	1365	Auto-Data Audi 90 B2 Typ 85 quattro; Auto-Data Audi 90 B2 2.0	https://www.auto-data.net/en/audi-90-b2-typ-81-85-2.2-e-136hp-quattro-4809; https://www.auto-data.net/en/audi-90-b2-typ-81-85-2.0-113hp-4804
EU-JAGUAR-XJ-SERIES-I-SEDAN-4D-SWB-01	4813	1768	1341	Automobile-Catalog Jaguar XJ6 2.8 Series I	https://www.automobile-catalog.com/car/1969/1278470/jaguar_xj6_2_8_litre_overdrive.html
EU-PEUGEOT-305-II-581M-SEDAN-4D-01	4263	1636	1411	Automobile-Catalog Peugeot 305 II Sedan; Auto-Data Peugeot 305 II 581M	https://www.automobile-catalog.com/car/1986/2568620/peugeot_305_gr.html; https://www.auto-data.net/en/peugeot-305-ii-581m-1.6-97hp-5542
EU-TALBOT-HORIZON-HATCHBACK-5D-FACELIFT-01	3960	1680	1410	Automobile-Catalog Talbot Horizon 1.6 Premium	https://www.automobile-catalog.com/car/1983/3116930/talbot_horizon_1_6_premium.html
EU-OPEL-VECTRA-B-CC-HATCHBACK-5D-FACELIFT-01	4495	1707	1425	Auto-Data Opel Vectra B CC Facelift 2.5i V6	https://www.auto-data.net/en/opel-vectra-b-cc-facelift-1999-2.5i-v6-170hp-26124
EU-FERRARI-MONDIAL-3-2-CONVERTIBLE-2D-01	4535	1795	1265	Automobile-Catalog Ferrari Mondial 3.2 Cabriolet	https://www.automobile-catalog.com/car/1985/53660/ferrari_mondial_3_2_cabriolet.html
```

## 下一步优先处理

1. 闭合 Opel Kadett D、Manta B CC、Rekord A/B 聚类。
2. 批量处理 Ford Taunus Sedan/Coupe 的代际、门数和车身分支。
3. 处理 Renault 18、Volvo 240/740、Peugeot 405 Break 等乘用车外廓。
4. 最后集中解决 Renault Master/Trafic、Fiat Ducato、VW Transporter/LT 和 Mitsubishi L300 的轴距、车顶及车身组合。

推进信号：CONTINUE

[1]: https://www.automobile-catalog.com/car/1987/2460290/opel_kadett_cabrio_gsi_cat.html?utm_source=chatgpt.com "1987 Opel Kadett Cabrio GSi catalyst (man. 5)"
[2]: https://www.auto-data.net/en/audi-90-b2-typ-81-85-2.2-e-136hp-quattro-4809?utm_source=chatgpt.com "Audi 90 (B2, Typ 81,85) 2.2 E (136 Hp) quattro /Sedan 1984"


--- 发送 / 继续到 Round 5 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2601-2700_ktype_dimension_mapping_final.tsv
- all_2601-2700_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 5 / 下一步 ---
## 更新点

* Opel Kadett D 两条 Ktype 均确认覆盖三门、五门两种车身，按门数拆分；虽然三维相同，但物理车身边界不同，分别建组。([汽车数据网][1])
* 闭合 Opel Manta B CC 1.6、Renault 18 Break Turbo 和 Renault 5 Turbo 宽体外廓。([汽车数据网][2])
* Renault Super 5 1.6 D 按 C404 三门与 B404 五门拆分；两种车身长度不同。([Ultimate Specs][3])

## 当前批次进度

* 输入 Ktype：100
* READY Ktype：54
* READY 映射行：69
* PENDING Ktype：46
* 已确认尺寸组：51
* 本轮新增尺寸组：7
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27635_3dr	27635	Hatchback	Kadett D		3	EU-OPEL-KADETT-D-HATCHBACK-3D-01	HIGH	三门掀背车身分支。	READY
27635_5dr	27635	Hatchback	Kadett D		5	EU-OPEL-KADETT-D-HATCHBACK-5D-01	HIGH	五门掀背车身分支。	READY
27636_3dr	27636	Hatchback	Kadett D		3	EU-OPEL-KADETT-D-HATCHBACK-3D-01	HIGH	三门掀背车身分支。	READY
27636_5dr	27636	Hatchback	Kadett D		5	EU-OPEL-KADETT-D-HATCHBACK-5D-01	HIGH	五门掀背车身分支。	READY
27676	27676	Coupe	Manta B CC		3	EU-OPEL-MANTA-B-CC-COUPE-3D-PREFL-01	HIGH	CC三门掀背式Coupe改款前外廓。	READY
27715	27715	Wagon	18 Break	135	5	EU-RENAULT-18-BREAK-135-WAGON-5D-01	HIGH	135五门旅行车外廓。	READY
27725	27725	Hatchback	5 Turbo		3	EU-RENAULT-5-TURBO-HATCHBACK-WIDEBODY-3D-01	HIGH	Turbo及Turbo 2共用三门宽体外廓。	READY
27728_3dr	27728	Hatchback	Super 5	C404	3	EU-RENAULT-SUPER-5-C404-HATCHBACK-3D-01	HIGH	C404三门掀背车身。	READY
27728_5dr	27728	Hatchback	Super 5	B404	5	EU-RENAULT-SUPER-5-B404-HATCHBACK-5D-01	HIGH	B404五门掀背车身。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-OPEL-KADETT-D-HATCHBACK-3D-01	3998	1636	1380	Auto-Data Opel Kadett D 1.0 40 Hp	https://www.auto-data.net/en/opel-kadett-d-1.0-40hp-25902
EU-OPEL-KADETT-D-HATCHBACK-5D-01	3998	1636	1380	Auto-Data Opel Kadett D 1.0 40 Hp	https://www.auto-data.net/en/opel-kadett-d-1.0-40hp-25902
EU-OPEL-MANTA-B-CC-COUPE-3D-PREFL-01	4376	1670	1340	Auto-Data Opel Manta B CC 1.6 N; Automobile-Catalog Opel Manta CC L 1.6 S	https://www.auto-data.net/en/opel-manta-b-cc-1.6-n-60hp-2151; https://www.automobile-catalog.com/car/1979/2428940/opel_manta_cc_l_1_6_s.html
EU-RENAULT-18-BREAK-135-WAGON-5D-01	4487	1689	1407	Automobile-Catalog Renault 18 Break Turbo Injection	https://www.automobile-catalog.com/car/1984/2932295/renault_18_break_turbo_injection.html
EU-RENAULT-5-TURBO-HATCHBACK-WIDEBODY-3D-01	3664	1752	1323	Automobile-Catalog Renault 5 Turbo	https://www.automobile-catalog.com/car/1982/29330/renault_5_turbo.html
EU-RENAULT-SUPER-5-C404-HATCHBACK-3D-01	3590	1580	1390	UltimateSpecs Renault Super 5 1.6 D 3-door; Renault UK Superfive Press Release	https://www.ultimatespecs.com/car-specs/Renault/6386/Renault-Super-5-16-D---SD---TD.html; https://renaultownersclub.com/wp-content/uploads/vehicles/Superfive%20Press%20Release%205.pdf
EU-RENAULT-SUPER-5-B404-HATCHBACK-5D-01	3650	1580	1390	UltimateSpecs Renault Super 5 1.6 GTD 5-door; Renault UK Superfive Press Release	https://www.ultimatespecs.com/car-specs/Renault/142513/Renault-Super-5-16-GTD-5-door.html; https://renaultownersclub.com/wp-content/uploads/vehicles/Superfive%20Press%20Release%205.pdf
```

## 下一步优先处理

1. 闭合 Volvo 240、Volvo 740 facelift、Peugeot 405 II Break 和 Renault 18 Break 4×4。
2. 处理 Opel Manta B CC 2.0 GSI、Rekord A/B 及 Ford Taunus Sedan/Coupe。
3. 集中处理 Mitsubishi L300、Renault Trafic I、Master I、Fiat Ducato I 的轴距和车顶分支。
4. 最后处理 VW Transporter T4/T5 底盘车及 LT I/II 商用车组合。

推进信号：CONTINUE

[1]: https://www.auto-data.net/en/opel-kadett-d-1.0-40hp-25902?utm_source=chatgpt.com "Specs of Opel Kadett D 1.0 (40 Hp) /1979, 1980, 1981"
[2]: https://www.auto-data.net/en/opel-manta-b-cc-1.6-n-60hp-2151?utm_source=chatgpt.com "Specs of Opel Manta B CC 1.6 N (60 Hp) /1978, 1979, 1980"
[3]: https://www.ultimatespecs.com/car-specs/Renault/142513/Renault-Super-5-16-GTD-5-door.html?utm_source=chatgpt.com "Renault Super 5 1.6 GTD 5-door Specs"


--- 发送 / 继续到 Round 6 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2601-2700_ktype_dimension_mapping_final.tsv
- all_2601-2700_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 6 / 下一步 ---
## 更新点

* Opel Rekord A 与 Rekord B 的输入记录均覆盖两门、四门轿车边界，本轮按门数拆分；同代两种门数三维相同，但作为不同物理车身分别建组。([汽车目录][1])
* 闭合 Renault 4、Rover Montego Estate 与 Honda Accord III Aerodeck 三个单一外廓 Ktype。([汽车数据网][2])

## 当前批次进度

* 输入 Ktype：100
* READY Ktype：59
* READY 映射行：76
* PENDING Ktype：41
* 已确认尺寸组：58
* 本轮首次新建尺寸组：7
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27722	27722	Hatchback	Renault 4		5	EU-RENAULT-4-HATCHBACK-5D-01	MEDIUM	五门掀背车身外廓。	READY
27801_2dr	27801	Sedan	Rekord A		2	EU-OPEL-REKORD-A-SEDAN-2D-01	MEDIUM	两门轿车分支。	READY
27801_4dr	27801	Sedan	Rekord A		4	EU-OPEL-REKORD-A-SEDAN-4D-01	MEDIUM	四门轿车分支。	READY
27804_2dr	27804	Sedan	Rekord B		2	EU-OPEL-REKORD-B-SEDAN-2D-01	MEDIUM	两门轿车分支。	READY
27804_4dr	27804	Sedan	Rekord B		4	EU-OPEL-REKORD-B-SEDAN-4D-01	MEDIUM	四门轿车分支。	READY
27818	27818	Wagon	Montego Estate	XE	5	EU-ROVER-MONTEGO-XE-WAGON-5D-01	HIGH	XE五门旅行车外廓。	READY
27871	27871	Wagon	Accord III Aerodeck		3	EU-HONDA-ACCORD-III-AERODECK-WAGON-3D-01	HIGH	三门Aerodeck车身外廓。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-RENAULT-4-HATCHBACK-5D-01	3670	1485	1550	Auto-Data Renault 4	https://www.auto-data.net/en/renault-4-generation-2164
EU-OPEL-REKORD-A-SEDAN-2D-01	4512	1696	1465	Automobile-Catalog 1964 Opel Rekord 1700 2-door	https://www.automobile-catalog.com/car/1964/2411570/opel_rekord_1700_2d_4gang.html
EU-OPEL-REKORD-A-SEDAN-4D-01	4512	1696	1465	Automobile-Catalog 1964 Opel Rekord 1700 4-door	https://www.automobile-catalog.com/car/1964/2411585/opel_rekord_1700_4d_3gang.html
EU-OPEL-REKORD-B-SEDAN-2D-01	4529	1690	1440	Automobile-Catalog 1965 Opel Rekord 1900 S 2-door	https://www.automobile-catalog.com/car/1965/2411810/opel_rekord_1900_s_2d_4gang.html
EU-OPEL-REKORD-B-SEDAN-4D-01	4529	1690	1440	Automobile-Catalog 1965 Opel Rekord 1900 S 4-door	https://www.automobile-catalog.com/car/1965/2411870/opel_rekord_1900_s_4d_4gang.html
EU-ROVER-MONTEGO-XE-WAGON-5D-01	4465	1710	1447	Automobile-Catalog 1988 Montego Estate 1.6	https://www.automobile-catalog.com/car/1988/1700930/montego_estate_1_6.html
EU-HONDA-ACCORD-III-AERODECK-WAGON-3D-01	4335	1695	1335	Automobile-Catalog 1986 Honda Accord Aerodeck 2.0 Si	https://www.automobile-catalog.com/car/1986/1096580/honda_accord_aerodeck_2_0_si.html
```

## 下一步优先处理

1. 闭合 Volvo 240、Volvo 740 facelift、Opel Manta B CC 后期版本。
2. 处理 Ford Taunus P7A/P7B 的 Sedan、Coupe 与门数分支。
3. 集中解决 Renault Trafic I、Master I、Fiat Ducato I 和 Mitsubishi L300 的轴距、车顶及乘用/厢式车组合。
4. 最后处理 VW Transporter T4、T5 底盘车及 LT I/II 的驾驶室和轴距分支。

推进信号：CONTINUE

[1]: https://www.automobile-catalog.com/car/1964/2411585/opel_rekord_1700_4d_3gang.html?utm_source=chatgpt.com "1964 Opel Rekord 1700 4d 3Gang Specs Review (44.1 kW ..."
[2]: https://www.auto-data.net/en/renault-4-generation-2164 "Renault 4 | Technical Specs, Fuel consumption, Dimensions"


--- 发送 / 继续到 Round 7 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2601-2700_ktype_dimension_mapping_final.tsv
- all_2601-2700_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 7 / 下一步 ---
## 更新点

* 新增 Volvo 240 四门轿车尺寸组，Ktype `27659` 完成映射。1990 年欧洲规格显示外廓为 4785 × 1707 × 1427 mm，宽度不含后视镜。([汽车目录][1])
* Opel Manta B CC 后期车身与此前改款前尺寸不同，新建 facelift 尺寸组，未覆盖既有组。后期外廓为 4443 × 1686 × 1330 mm。([汽车目录][2])
* Austin Mini 按经典两门 Sedan 归类，不沿用输入的 Hatchback；完成 Ktype `27678` 映射。([维基百科][3])
* Volvo 740 后期轿车高度与既有 `PREFL` 尺寸组不同，因此新建 facelift 组，不改写累计缓存。1990 年规格明确宽度为不含后视镜口径。([Edmunds][4])

## 当前批次进度

* 输入 Ktype：100
* READY Ktype：63
* READY 映射行：80
* PENDING Ktype：37
* 已确认尺寸组：62
* 本轮首次新建尺寸组：4
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27659	27659	Sedan	240	244	4	EU-VOLVO-240-244-SEDAN-4D-01	HIGH	244四门轿车外廓。	READY
27675	27675	Coupe	Manta B CC		3	EU-OPEL-MANTA-B-CC-COUPE-3D-FACELIFT-01	MEDIUM	CC后期三门Coupe外廓。	READY
27678	27678	Sedan	Classic Mini	ADO20	2	EU-AUSTIN-MINI-CLASSIC-SEDAN-2D-01	MEDIUM	经典Mini两门轿车外廓。	READY
27724	27724	Sedan	740 Facelift	744	4	EU-VOLVO-740-744-SEDAN-4D-FACELIFT-01	HIGH	后期四门轿车外廓。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-VOLVO-240-244-SEDAN-4D-01	4785	1707	1427	Automobile-Catalog 1990 Volvo 244 Turbo	https://www.automobile-catalog.com/car/1990/45905/volvo_244_turbo.html
EU-OPEL-MANTA-B-CC-COUPE-3D-FACELIFT-01	4443	1686	1330	Automobile-Catalog 1984 Opel Manta B GSi; Automobile-Catalog 1985 Opel Manta GT 1.3 S	https://www.automobile-catalog.com/make/opel/manta_b/manta_b_gsi/1984.html; https://www.automobile-catalog.com/car/1985/2430365/opel_manta_gt_1_3_s.html
EU-AUSTIN-MINI-CLASSIC-SEDAN-2D-01	3054	1410	1346	Automobile-Catalog 1969 Austin Mini Mk II; Automobile-Catalog 1968 Austin Mini Cooper Mk II	https://www.automobile-catalog.com/make/austin/mini/mini_mk_ii_austin/1969.html; https://www.automobile-catalog.com/car/1968/256430/austin_mini_cooper_mk_ii.html
EU-VOLVO-740-744-SEDAN-4D-FACELIFT-01	4785	1760	1410	Edmunds 1990 Volvo 740 Sedan GLE	https://www.edmunds.com/volvo/740/1990/sedan/st-6247/features-specs/
```

## 下一步优先处理

1. 批量闭合 Ford Taunus P7B 的两门、四门 Sedan 与 Hardtop Coupe 分支。
2. 处理 Peugeot 405 II Break、Renault 18 Break 4×4、Nissan Bluebird 与 Cherry。
3. 集中处理 Mitsubishi L300、Renault Trafic I、Master I 和 Fiat Ducato I 的轴距、车顶及乘用/厢式车组合。
4. 最后解决 VW Transporter T4/T5 底盘车、LT I/II 及 Peugeot Partner Dangel 四驱外廓。

推进信号：CONTINUE

[1]: https://www.automobile-catalog.com/car/1990/45905/volvo_244_turbo.html?utm_source=chatgpt.com "1990 Volvo 244 Turbo (man. 5) (model up to mid-year ..."
[2]: https://www.automobile-catalog.com/make/opel/manta_b/manta_b_gsi/1984.html?utm_source=chatgpt.com "1984 Opel Manta B GSi Coupe full range specs"
[3]: https://en.wikipedia.org/wiki/Mini?utm_source=chatgpt.com "Mini"
[4]: https://www.edmunds.com/volvo/740/1990/sedan/st-6247/features-specs/?utm_source=chatgpt.com "Used 1990 Volvo 740 Sedan GLE Specs & Features"


--- 发送 / 继续到 Round 8 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2601-2700_ktype_dimension_mapping_final.tsv
- all_2601-2700_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 8 / 下一步 ---
## 更新点

* Nissan Bluebird `27743` 闭合为 U11 四门轿车外廓。
* Nissan Cherry `27748` 的 1.0/45 PS 版本实际对应 N10 三门掀背车身，不按输入中的 Coupe 建立错误车身。其尺寸为 3960 × 1620 × 1360 mm。([汽车目录][1])
* Peugeot Boxer `27830` 与本批已确认的 Citroën Jumper 230L 四驱车身同平台，直接复用既有 L1H1、L2H2 尺寸组，不重复建组。
* Peugeot Partner Dangel 四驱的 `27836`、`27838` 共用 Phase II 五门四驱外廓；发动机差异不重复建组。2005 年 2.0 HDi Dangel 车身尺寸为 4149 × 1720 × 1950 mm。([auta5p.eu][2])

## 当前批次进度

* 输入 Ktype：100
* READY Ktype：68
* READY 映射行：86
* PENDING Ktype：32
* 已确认尺寸组：65
* 本轮首次新建尺寸组：3
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27743	27743	Sedan	Bluebird U11	U11	4	EU-NISSAN-BLUEBIRD-U11-SEDAN-4D-01	HIGH	U11四门轿车外廓。	READY
27748	27748	Hatchback	Cherry N10	N10	3	EU-NISSAN-CHERRY-N10-HATCHBACK-3D-01	HIGH	1.0版本对应N10三门掀背车身。	READY
27830_l1h1	27830	Van	Boxer I	230		EU-CITROEN-JUMPER-I-230L-VAN-4X4-L1H1-01	HIGH	230系四驱L1H1分支。	READY
27830_l2h2	27830	Van	Boxer I	230		EU-CITROEN-JUMPER-I-230L-VAN-4X4-L2H2-01	HIGH	230系四驱L2H2分支。	READY
27836	27836	MPV	Partner I Phase II	M59	5	EU-PEUGEOT-PARTNER-I-PHASE-II-DANGEL-4X4-MPV-5D-01	MEDIUM	Phase II Dangel四驱五门车身。	READY
27838	27838	MPV	Partner I Phase II	M59	5	EU-PEUGEOT-PARTNER-I-PHASE-II-DANGEL-4X4-MPV-5D-01	HIGH	Phase II Dangel四驱五门车身。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-NISSAN-BLUEBIRD-U11-SEDAN-4D-01	4360	1690	1400	Auto-Data Nissan Bluebird U11 2.0 D; Automobile-Catalog Nissan Bluebird U11 export sedan	https://www.auto-data.net/en/nissan-bluebird-u11-2.0-d-58hp-886; https://www.automobile-catalog.com/make/nissan/bluebird_7gen_u11/bluebird_7gen_export_sedan/1984.html
EU-NISSAN-CHERRY-N10-HATCHBACK-3D-01	3960	1620	1360	Automobile-Catalog 1980 Datsun Cherry 1.0 3door	https://www.automobile-catalog.com/car/1980/2105435/datsun_cherry_1_0_3door.html
EU-PEUGEOT-PARTNER-I-PHASE-II-DANGEL-4X4-MPV-5D-01	4149	1720	1950	Auta5P Dangel Peugeot Partner 4x4 2005	https://auta5p.eu/lang/en/katalog/auto.php?idf=Dangel-Peugeot-Partner-4x4-3810
```

## 下一步优先处理

1. 处理 Mitsubishi L300 II Bus/Van 与 L300 III 4WD Van 的轴距和车顶分支。
2. 集中闭合 Renault Trafic I Bus/Van 的前驱、后驱、四驱及车身长度组合。
3. 处理 Renault Master I 和 Fiat Ducato I Typ 290 的车顶、轴距及四驱差异。
4. 最后处理 VW Transporter T4、T5 底盘车及 LT I/II 商用车，并解决 Ford Taunus P7A/P7B 多车身分支。

推进信号：CONTINUE

[1]: https://www.automobile-catalog.com/car/1980/2105435/datsun_cherry_1_0_3door.html?utm_source=chatgpt.com "1980 Datsun Cherry 1.0 3door Specs Review (33 kW ..."
[2]: https://auta5p.eu/lang/en/katalog/auto.php?idf=Dangel-Peugeot-Partner-4x4-3810&utm_source=chatgpt.com "Dangel Peugeot Partner 4x4, 2005 [Auta5P ID:3810 EN]"


--- 发送 / 继续到 Round 9 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2601-2700_ktype_dimension_mapping_final.tsv
- all_2601-2700_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 9 / 下一步 ---
## 更新点

* 通过 Ktype 目录确认：`41F` 为两门轿车、`42F` 为四门轿车、`43F` 为双门 Hardtop Coupe；6 个 Ford Taunus Ktype 不再按模糊的 `Stufenheck/Coupe` 字段合并。([Prom.ua][1])
* P7A 与 P7B 的外廓确有变化：P7A 为 4736 × 1756 × 1494 mm；P7B Sedan 为 4721 × 1756 × 1478 mm，P7B Coupe 高度为 1464 mm，因此跨代 Ktype 按 `prefl/facelift` 拆分。([汽车目录][2])
* 2.3/125 PS Ktype 覆盖 P7A 与 P7B 两种外廓；2.6/125 PS 对应 P7B 车身，仅关联后期尺寸组。([汽车目录][3])

## 当前批次进度

* 输入 Ktype：100
* READY Ktype：74
* READY 映射行：95
* PENDING Ktype：26
* 已确认尺寸组：71
* 本轮首次新建尺寸组：6
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27794	27794	Sedan	Taunus 20M II P7B	41F	2	EU-FORD-TAUNUS-20M-II-P7B-SEDAN-2D-01	HIGH	41F两门轿车；2.6版本对应P7B外廓。	READY
27795_prefl	27795	Sedan	Taunus 20M II P7A	41F	2	EU-FORD-TAUNUS-20M-II-P7A-SEDAN-2D-01	HIGH	41F两门轿车P7A分支。	READY
27795_facelift	27795	Sedan	Taunus 20M II P7B	41F	2	EU-FORD-TAUNUS-20M-II-P7B-SEDAN-2D-01	HIGH	41F两门轿车P7B分支。	READY
27796	27796	Sedan	Taunus 20M II P7B	42F	4	EU-FORD-TAUNUS-20M-II-P7B-SEDAN-4D-01	HIGH	42F四门轿车；2.6版本对应P7B外廓。	READY
27797_prefl	27797	Sedan	Taunus 20M II P7A	42F	4	EU-FORD-TAUNUS-20M-II-P7A-SEDAN-4D-01	HIGH	42F四门轿车P7A分支。	READY
27797_facelift	27797	Sedan	Taunus 20M II P7B	42F	4	EU-FORD-TAUNUS-20M-II-P7B-SEDAN-4D-01	HIGH	42F四门轿车P7B分支。	READY
27798	27798	Coupe	Taunus 20M II P7B	43F	2	EU-FORD-TAUNUS-20M-II-P7B-COUPE-2D-01	HIGH	43F双门Hardtop Coupe；2.6版本对应P7B外廓。	READY
27799_prefl	27799	Coupe	Taunus 20M II P7A	43F	2	EU-FORD-TAUNUS-20M-II-P7A-COUPE-2D-01	HIGH	43F双门Hardtop Coupe P7A分支。	READY
27799_facelift	27799	Coupe	Taunus 20M II P7B	43F	2	EU-FORD-TAUNUS-20M-II-P7B-COUPE-2D-01	HIGH	43F双门Hardtop Coupe P7B分支。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-FORD-TAUNUS-20M-II-P7A-SEDAN-2D-01	4736	1756	1494	Automobile-Catalog 1967 Ford 20M 2000 S 4-speed	https://www.automobile-catalog.com/car/1967/901505/ford_20m_2000_s_4-speed.html
EU-FORD-TAUNUS-20M-II-P7B-SEDAN-2D-01	4721	1756	1478	Automobile-Catalog 1969 Ford 20M RS 2300 S-125PS	https://www.automobile-catalog.com/car/1969/902990/ford_20m_rs_2300_s-125ps.html
EU-FORD-TAUNUS-20M-II-P7A-SEDAN-4D-01	4736	1756	1494	Automobile-Catalog 1968 Ford 20M 2300 S 4-speed	https://www.automobile-catalog.com/car/1968/901595/ford_20m_2300_s_4-speed.html
EU-FORD-TAUNUS-20M-II-P7B-SEDAN-4D-01	4721	1756	1478	Automobile-Catalog 1970 Ford 26M	https://www.automobile-catalog.com/car/1970/903665/ford_26m.html
EU-FORD-TAUNUS-20M-II-P7A-COUPE-2D-01	4736	1756	1494	Automobile-Catalog 1968 Ford 20M TS Hardtop 2300 S	https://www.automobile-catalog.com/car/1968/901655/ford_20m_ts_hardtop_2300_s.html
EU-FORD-TAUNUS-20M-II-P7B-COUPE-2D-01	4721	1756	1464	Automobile-Catalog 1970 Ford 20M RS Hardtop 2300 S-125PS; Automobile-Catalog 1969 Ford 26M Hardtop automatic	https://www.automobile-catalog.com/car/1970/903410/ford_20m_rs_hardtop_2300_s-125ps.html; https://www.automobile-catalog.com/car/1969/903680/ford_26m_hardtop_automatic.html
```

## 下一步优先处理

1. 集中闭合 Mitsubishi L300 II Bus/Van 与 L300 III 4WD Van。
2. 处理 Renault Trafic I 的 Bus、Van、前驱、后驱和四驱分支。
3. 处理 Renault Master I、Fiat Ducato I/Panorama 的轴距、车顶和四驱组合。
4. 最后处理 VW Transporter T4/T5 Chassis、VW LT I/II、Mazda E2000 4WD，以及仍有字段冲突的 Peugeot 405 Break、Renault 18 4×4、Ford Scorpio Turnier。

推进信号：CONTINUE

[1]: https://prom.ua/p2977605790-pas-privodnoj-dlinoj.html?utm_source=chatgpt.com "Пас приводной с длиной круга более 60 см, но не более 180 см BUICK, CHEVROLET, CITROEN, FIAT, FORD, LANCIA, MERCEDES-BENZ,, цена: 341.31 ₴, купить на Prom.ua"
[2]: https://www.automobile-catalog.com/car/1968/901655/ford_20m_ts_hardtop_2300_s.html?utm_source=chatgpt.com "1968 Ford 20M TS Hardtop 2300 S Specs Review (79.5 kW / 108 PS / 107 hp) (up to July 1968 for Europe )"
[3]: https://www.automobile-catalog.com/car/1969/902990/ford_20m_rs_2300_s-125ps.html?utm_source=chatgpt.com "1969 Ford 20M RS 2300 S-125PS Specs Review (92 kW / 125 PS / 123 hp) (up to September 1969 for Europe )"


--- 发送 / 继续到 Round 10 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2601-2700_ktype_dimension_mapping_final.tsv
- all_2601-2700_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 10 / 下一步 ---
## 更新点

* 闭合 Peugeot 405 II Break `27692`。该 Ktype 对应 `4E` 五门旅行车 2.0 4×4 144 kW 版本；采用 Phase II Break 外廓 4398 × 1704 × 1445 mm，宽度为不含后视镜口径。([Autodoc][1])
* Renault 18 `27714` 已确认属于 `135` 五门旅行车，直接复用已建立的 Renault 18 Break 尺寸组，不重复输出尺寸来源。([Autodoc][2])
* 闭合 Ford Scorpio I Turnier `27862`，对应 `GGE` 五门旅行车外廓 4744 × 1760 × 1490 mm。([汽车数据网][3])

## 当前批次进度

* 输入 Ktype：100
* READY Ktype：77
* READY 映射行：98
* PENDING Ktype：23
* 已确认尺寸组：73
* 本轮首次新建尺寸组：2
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27692	27692	Wagon	405 II Break	4E	5	EU-PEUGEOT-405-II-4E-BREAK-WAGON-5D-4X4-01	MEDIUM	4E五门四驱旅行车外廓。	READY
27714	27714	Wagon	18 Variable	135	5	EU-RENAULT-18-BREAK-135-WAGON-5D-01	MEDIUM	135五门四驱旅行车外廓。	READY
27862	27862	Wagon	Scorpio I Turnier	GGE	5	EU-FORD-SCORPIO-I-GGE-WAGON-5D-01	HIGH	GGE五门旅行车外廓。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-PEUGEOT-405-II-4E-BREAK-WAGON-5D-4X4-01	4398	1704	1445	Automobile-Catalog 1993 Peugeot 405 Break GRD; AUTODOC Peugeot 405 II Break 2.0 4x4 Ktype 27692	https://www.automobile-catalog.com/car/1993/2585510/peugeot_405_break_grd.html; https://www.autodoc.co.uk/car-parts/headlight-insert-10533/peugeot/405/405-ii-break-4e/27692-2-0-4x4
EU-FORD-SCORPIO-I-GGE-WAGON-5D-01	4744	1760	1490	Auto-Data Ford Scorpio I Turnier GGE	https://www.auto-data.net/en/ford-scorpio-i-turnier-gge-generation-1790
```

## 下一步优先处理

1. 闭合 Mitsubishi L300 II Bus/Van 与 L300 III P23V 四驱 Van。
2. 集中处理 Renault Trafic I 的前驱、后驱、四驱及 Bus/Van 分支。
3. 处理 Renault Master I、Fiat Ducato I/Panorama 的轴距、车顶和四驱组合。
4. 最后处理 VW Transporter T4、T5 Chassis、VW LT I/II 与 Mazda E2000 4WD。

推进信号：CONTINUE

[1]: https://www.autodoc.co.uk/car-parts/headlight-insert-10533/peugeot/405/405-ii-break-4e/27692-2-0-4x4?utm_source=chatgpt.com "PEUGEOT 405 II Estate (4E) 2.0 4x4 Headlights"
[2]: https://www.autodoc.co.uk/car-parts/support-steering-link-10681/renault/18/18-variable-135/27714-1-6-4x4?utm_source=chatgpt.com "Renault 18 Variable 135 1.6 4x4 Ball joint (79 hp Petrol 841 725)"
[3]: https://www.auto-data.net/en/ford-scorpio-i-turnier-gge-generation-1790?utm_source=chatgpt.com "Ford Scorpio I Turnier (GGE) | Technical Specs, Fuel ..."


--- 发送 / 继续到 Round 11 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2601-2700_ktype_dimension_mapping_final.tsv
- all_2601-2700_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 11 / 下一步 ---
## 更新点

* 闭合 Mitsubishi L300 III `27806`。该 Ktype 对应 2.0 4WD 的 `P23W/P23V` 代码范围；依据输入车身类型 `Kasten`，本轮落盘为 `P23V` 厢式车外廓。两处规格资料一致给出 4275 × 1694 × 1834 mm。([catalogonuevo.icerbrakes.com][1])
* Mazda E2000 4WD `27847` 已确认属于 `SR2` 厢式车，但当前资料仍无法确定其对应 4590 mm 或 4915 mm 车长及准确高度，本轮不创建猜测性尺寸组。([Meyer Motoren][2])
* Renault Trafic I 剩余 Ktype 涉及多个车身代码、轴距和车顶组合，继续保持待闭合，不强行压缩为单一尺寸组。([Autodoc][3])

## 当前批次进度

* 输入 Ktype：100
* READY Ktype：78
* READY 映射行：99
* PENDING Ktype：22
* 已确认尺寸组：74
* 本轮首次新建尺寸组：1
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27806	27806	Van	L300 III	P23V		EU-MITSUBISHI-L300-III-P23V-VAN-4WD-01	HIGH	P23V四驱厢式车外廓。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-MITSUBISHI-L300-III-P23V-VAN-4WD-01	4275	1694	1834	AutoEvolution Mitsubishi L300 1986-1994; Mitsubishi DrivePlace L300 II Van 2.0 4WD	https://www.autoevolution.com/cars/mitsubishi-l300-1993.html; https://mitsubishi.drive.place/l300/ii/group_furgon/597555
```

## 下一步优先处理

1. 确认 Mazda E2000 `SR2` 4WD 的具体轴距、车长和高度分支。
2. 解码 Renault Trafic I 的 `T1–T7` 车身代码，批量闭合 Bus、Van、前驱、后驱和四驱组合。
3. 处理 Renault Master I 与 Fiat Ducato I/Panorama 的轴距、车顶和四驱分支。
4. 最后处理 VW Transporter T4、T5 Chassis、VW LT I/II 及 Mitsubishi L300 II Bus/Van。

推进信号：CONTINUE

[1]: https://catalogonuevo.icerbrakes.com/Vehiculo/Details?idTipoVehiculo=2&idVehiculo=27806&utm_source=chatgpt.com "2.0 4WD (P23W, P23V) details - Web Catalogo"
[2]: https://www.meyermotoren.de/en/fahrzeuge/27847/mazda/e-serie_kasten_sr2_/e2000_4wd?utm_source=chatgpt.com "Mazda E-Serie Kasten (SR2) E2000 4WD"
[3]: https://www.autodoc.co.uk/car-parts/motor-windscreen-wipers-10234/renault/trafic/trafic-bus-t5-t6-t7/27705-2-1-d-4x4?utm_source=chatgpt.com "Renault Trafic Minibus T5 2.1 D 4x4 Wiper motor (58 hp 852 750)"


--- 发送 / 继续到 Round 12 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2601-2700_ktype_dimension_mapping_final.tsv
- all_2601-2700_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 12 / 下一步 ---
## 更新点

* 闭合 VW Transporter T4 两个 Ktype。`27782` 与 `27783` 均属于 facelift T4 Panel Van 车身系列，按 `L1H1`、`L2H1`、`L2H2` 三种物理外廓拆分；发动机功率变化不重复建组。三种外廓分别为 4707×1840×1940、5107×1840×1940、5107×1840×2430 mm，宽度均为不含后视镜口径。([肉土里亚][1])
* 闭合 VW Transporter T5 底盘车 `27824`，按单排驾驶室和双排驾驶室拆分，直接复用累计表中的既有尺寸组，不重复输出尺寸来源。该 Ktype 对应 T5 平板车/底盘车代码范围 `7JD/7JE/7JL/7JY/7JZ/7FD/7FE/7FL`。([Eualkatresz][2])

## 当前批次进度

* 输入 Ktype：100
* READY Ktype：81
* READY 映射行：107
* PENDING Ktype：19
* 已确认尺寸组：77
* 本轮首次新建尺寸组：3
* 本轮复用既有尺寸组：2
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27782_l1h1	27782	Van	Transporter T4 Facelift			EU-VW-TRANSPORTER-T4-VAN-L1H1-01	MEDIUM	短轴低顶厢式车分支。	READY
27782_l2h1	27782	Van	Transporter T4 Facelift			EU-VW-TRANSPORTER-T4-VAN-L2H1-01	MEDIUM	长轴低顶厢式车分支。	READY
27782_l2h2	27782	Van	Transporter T4 Facelift			EU-VW-TRANSPORTER-T4-VAN-L2H2-01	MEDIUM	长轴高顶厢式车分支。	READY
27783_l1h1	27783	Van	Transporter T4 Facelift			EU-VW-TRANSPORTER-T4-VAN-L1H1-01	MEDIUM	短轴低顶厢式车分支。	READY
27783_l2h1	27783	Van	Transporter T4 Facelift			EU-VW-TRANSPORTER-T4-VAN-L2H1-01	MEDIUM	长轴低顶厢式车分支。	READY
27783_l2h2	27783	Van	Transporter T4 Facelift			EU-VW-TRANSPORTER-T4-VAN-L2H2-01	MEDIUM	长轴高顶厢式车分支。	READY
27824_singlecab	27824	Pickup	Transporter T5 Facelift		2	EU-VW-TRANSPORTER-T5-CHASSIS-CAB-LWB-01	MEDIUM	长轴单排驾驶室底盘车分支。	READY
27824_doublecab	27824	Pickup	Transporter T5 Facelift		4	EU-VW-TRANSPORTER-T5-CHASSIS-DOUBLE-CAB-LWB-01	MEDIUM	长轴双排驾驶室底盘车分支。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-VW-TRANSPORTER-T4-VAN-L1H1-01	4707	1840	1940	Auto-Data Volkswagen Transporter T4 Facelift Panel Van L1H1	https://www.auto-data.net/en/volkswagen-transporter-t4-facelift-1996-panel-van-2.5-110hp-l1h1-50416
EU-VW-TRANSPORTER-T4-VAN-L2H1-01	5107	1840	1940	Auto-Data Volkswagen Transporter T4 Facelift Panel Van L2H1	https://www.auto-data.net/en/volkswagen-transporter-t4-facelift-1996-panel-van-2.5-110hp-l2h1-50437
EU-VW-TRANSPORTER-T4-VAN-L2H2-01	5107	1840	2430	Auto-Data Volkswagen Transporter T4 Facelift Panel Van L2H2	https://www.auto-data.net/en/volkswagen-transporter-t4-facelift-1996-panel-van-2.0-84hp-l2h2-50430
```

## 下一步优先处理

1. 闭合 Mitsubishi L300 II 的 Bus 与 Van 外廓，重点区分标准车身、长轴高顶及 `L035P` 边界。
2. 批量解决 Renault Trafic I 的 Bus/Van、前驱/后驱/四驱及 `T1–T7` 物理分支。
3. 处理 Renault Master I 与 Fiat Ducato I/290 的轴距、车顶和四驱组合。
4. 最后处理 VW LT I/II、Mazda E2000 4WD，并完成剩余引用闭合。

推进信号：CONTINUE

[1]: https://meat-doria.com/de/car/VW-TRANSPORTER-IV-Furgonato-%2870A%2C-70H%2C-7DA%2C-7DH%29-yAll/27782?utm_source=chatgpt.com "VW TRANSPORTER T4 Kasten (70A, 70H, 7DA, 7DH, 70J)"
[2]: https://www.eualkatresz.hu/autoalkatresz-katalogus/sarvedoe_alkatreszek-10285/vw/transporter/transporter-v-alvaz-7jd-7je-7jl-7jy-7jz-7fd-7fe-7fl/27824-2-0-tdi?utm_source=chatgpt.com "VW Transporter T5 Platós teherautó / Alváz 7JD, 7JE, 7JL ..."


--- 发送 / 继续到 Round 13 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2601-2700_ktype_dimension_mapping_final.tsv
- all_2601-2700_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 13 / checkpoint 续跑 ---
## 更新点

* Mitsubishi L300 II 两个剩余 Ktype 已闭合。`27648` 对应 1.8 后驱乘用型 Starwagon，`27805` 对应 1.8 后驱长轴厢式车；两者宽度、高度相同，但车长分别为 4035 mm 和 4435 mm，不能共用尺寸组。([CarsGuide][1])
* 未使用 L300 Country 4×4 或后续 L300 III 的尺寸替代本轮后驱车型。

## 当前批次进度

* 输入 Ktype：100
* READY Ktype：83
* READY 映射行：109
* PENDING Ktype：17
* 已确认尺寸组：79
* 本轮首次新建尺寸组：2
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27648	27648	MPV	L300 II	L035P	4	EU-MITSUBISHI-L300-II-L035P-MPV-RWD-4D-01	MEDIUM	1.8后驱乘用型车身。	READY
27805	27805	Van	L300 II	L035P		EU-MITSUBISHI-L300-II-L035P-VAN-LWB-01	MEDIUM	1.8后驱长轴厢式车身。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-MITSUBISHI-L300-II-L035P-MPV-RWD-4D-01	4035	1690	1995	CarsGuide 1983 Mitsubishi Express dimensions; Carsales 1983 Mitsubishi Express Starwagon specifications	https://www.carsguide.com.au/mitsubishi/express/car-dimensions/1983; https://www.carsales.com.au/research/mitsubishi/express/1983/starwagon/
EU-MITSUBISHI-L300-II-L035P-VAN-LWB-01	4435	1690	1995	CarsGuide 1983 Mitsubishi Express dimensions; Trodo Mitsubishi L300 L035P vehicle catalogue	https://www.carsguide.com.au/mitsubishi/express/car-dimensions/1983; https://www.trodo.com/car-parts/mitsubishi-l-300-box-l03-p-1-8-60kw-22864-cid
```

## 下一步优先处理

1. 批量闭合 Renault Trafic I 的 5 个 Ktype，拆清 Bus/Van、前驱、后驱和四驱外廓。
2. 处理 Renault Master I 的 3 个 Ktype，确认各生产阶段覆盖的轴距和车顶分支。
3. 处理 Fiat Ducato I/290 的前驱、四驱 Van 和 Panorama 分支。
4. 最后处理 VW LT I/II、Mazda E2000 4WD，并完成引用闭合。

推进信号：CONTINUE

[1]: https://www.carsguide.com.au/mitsubishi/express/car-dimensions/1983 "Mitsubishi Express Dimensions 1983 - Length, Width, Height, Turning Circle, Ground Clearance, Wheelbase & Size | CarsGuide"


--- 发送 / 继续到 Round 14 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2601-2700_ktype_dimension_mapping_final.tsv
- all_2601-2700_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 14 / checkpoint 续跑 ---
## 更新点

* 闭合 Renault Trafic I 全部 5 个剩余 Ktype。
* Bus 代码 `T5/T6/T7` 与 Van 代码 `T1/T3/T4` 分别对应 `L1H1/L1H2/L2H2` 三种外廓，因此每个 Ktype 拆为三个物理分支。
* 汽油版三种外廓分别为 `4337×1905×2037`、`4337×1905×2425`、`4737×1905×2425 mm`；柴油版因加长前部，车长分别为 `4434/4434/4834 mm`。尺寸图中的宽度均为车身宽度口径。
* `27827`、`27828`、`27829` 虽然功率和驱动形式不同，但对应相同三种汽油 Van 外廓，统一复用三个尺寸组，不按驱动重复建组。相关目录分别确认了其 Van 车身范围和前驱/后驱属性。([demo.automotive-presta.com][1])

## 当前批次进度

* 输入 Ktype：100
* READY Ktype：88
* READY 映射行：124
* PENDING Ktype：12
* 已确认尺寸组：88
* 本轮首次新建尺寸组：9
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27705_l1h1	27705	MPV	Trafic I	T5		EU-RENAULT-TRAFIC-I-BUS-T5-L1H1-DIESEL-4X4-01	MEDIUM	T5短轴低顶四驱Bus分支。	READY
27705_l1h2	27705	MPV	Trafic I	T6		EU-RENAULT-TRAFIC-I-BUS-T6-L1H2-DIESEL-4X4-01	MEDIUM	T6短轴高顶四驱Bus分支。	READY
27705_l2h2	27705	MPV	Trafic I	T7		EU-RENAULT-TRAFIC-I-BUS-T7-L2H2-DIESEL-4X4-01	MEDIUM	T7长轴高顶四驱Bus分支。	READY
27706_l1h1	27706	MPV	Trafic I	T5		EU-RENAULT-TRAFIC-I-BUS-T5-L1H1-PETROL-01	MEDIUM	T5短轴低顶Bus分支。	READY
27706_l1h2	27706	MPV	Trafic I	T6		EU-RENAULT-TRAFIC-I-BUS-T6-L1H2-PETROL-01	MEDIUM	T6短轴高顶Bus分支。	READY
27706_l2h2	27706	MPV	Trafic I	T7		EU-RENAULT-TRAFIC-I-BUS-T7-L2H2-PETROL-01	MEDIUM	T7长轴高顶Bus分支。	READY
27827_l1h1	27827	Van	Trafic I	T1		EU-RENAULT-TRAFIC-I-VAN-T1-L1H1-PETROL-01	MEDIUM	T1短轴低顶Van分支。	READY
27827_l1h2	27827	Van	Trafic I	T3		EU-RENAULT-TRAFIC-I-VAN-T3-L1H2-PETROL-01	MEDIUM	T3短轴高顶Van分支。	READY
27827_l2h2	27827	Van	Trafic I	T4		EU-RENAULT-TRAFIC-I-VAN-T4-L2H2-PETROL-01	MEDIUM	T4长轴高顶Van分支。	READY
27828_l1h1	27828	Van	Trafic I	T1		EU-RENAULT-TRAFIC-I-VAN-T1-L1H1-PETROL-01	MEDIUM	T1短轴低顶Van分支。	READY
27828_l1h2	27828	Van	Trafic I	T3		EU-RENAULT-TRAFIC-I-VAN-T3-L1H2-PETROL-01	MEDIUM	T3短轴高顶Van分支。	READY
27828_l2h2	27828	Van	Trafic I	T4		EU-RENAULT-TRAFIC-I-VAN-T4-L2H2-PETROL-01	MEDIUM	T4长轴高顶Van分支。	READY
27829_l1h1	27829	Van	Trafic I	T1		EU-RENAULT-TRAFIC-I-VAN-T1-L1H1-PETROL-01	MEDIUM	T1短轴低顶Van分支。	READY
27829_l1h2	27829	Van	Trafic I	T3		EU-RENAULT-TRAFIC-I-VAN-T3-L1H2-PETROL-01	MEDIUM	T3短轴高顶Van分支。	READY
27829_l2h2	27829	Van	Trafic I	T4		EU-RENAULT-TRAFIC-I-VAN-T4-L2H2-PETROL-01	MEDIUM	T4长轴高顶Van分支。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-RENAULT-TRAFIC-I-BUS-T5-L1H1-DIESEL-4X4-01	4434	1905	2036	Transit Center Renault Trafic I L1H1 dimension diagram	https://www.transitcenter.uk/blog/1985traficwymiara.webp
EU-RENAULT-TRAFIC-I-BUS-T6-L1H2-DIESEL-4X4-01	4434	1905	2424	Transit Center Renault Trafic I L1H2 dimension diagram	https://www.transitcenter.uk/blog/1985traficwymiarb.webp
EU-RENAULT-TRAFIC-I-BUS-T7-L2H2-DIESEL-4X4-01	4834	1905	2425	Transit Center Renault Trafic I L2H2 dimension diagram	https://www.transitcenter.uk/blog/1985traficwymiarc.webp
EU-RENAULT-TRAFIC-I-BUS-T5-L1H1-PETROL-01	4337	1905	2037	Transit Center Renault Trafic I L1H1 dimension diagram	https://www.transitcenter.uk/blog/1985traficwymiara.webp
EU-RENAULT-TRAFIC-I-BUS-T6-L1H2-PETROL-01	4337	1905	2425	Transit Center Renault Trafic I L1H2 dimension diagram	https://www.transitcenter.uk/blog/1985traficwymiarb.webp
EU-RENAULT-TRAFIC-I-BUS-T7-L2H2-PETROL-01	4737	1905	2425	Transit Center Renault Trafic I L2H2 dimension diagram	https://www.transitcenter.uk/blog/1985traficwymiarc.webp
EU-RENAULT-TRAFIC-I-VAN-T1-L1H1-PETROL-01	4337	1905	2037	Transit Center Renault Trafic I L1H1 dimension diagram	https://www.transitcenter.uk/blog/1985traficwymiara.webp
EU-RENAULT-TRAFIC-I-VAN-T3-L1H2-PETROL-01	4337	1905	2425	Transit Center Renault Trafic I L1H2 dimension diagram	https://www.transitcenter.uk/blog/1985traficwymiarb.webp
EU-RENAULT-TRAFIC-I-VAN-T4-L2H2-PETROL-01	4737	1905	2425	Transit Center Renault Trafic I L2H2 dimension diagram	https://www.transitcenter.uk/blog/1985traficwymiarc.webp
```

## 下一步优先处理

1. Renault Master I：`27737`、`27738`、`27739`。
2. Fiat Ducato I/290：`27780`、`27819`、`27820`、`27821`。
3. VW LT I Syncro：`27785`、`27787`、`27788`。
4. Mazda E2000 4WD `27847` 与 VW LT II Bus `27850`。

推进信号：CONTINUE

[1]: https://demo.automotive-presta.com/back-office/en/tecdoc/passenger/renault/trafic-van-t-p-v/27828-20/101656-headlight-parts?utm_source=chatgpt.com "Headlight / parts"


--- 发送 / 继续到 Round 15 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2601-2700_ktype_dimension_mapping_final.tsv
- all_2601-2700_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 15 / checkpoint 续跑 ---
## 更新点

* Renault Master I 的 3 个 Ktype 已全部闭合。
* `27737`、`27738`、`27739` 均属于 `MASTER I Van (T__)`，覆盖同一套五种物理外廓：`L1H1`、`L1H2`、`L2H1`、`L2H2`、`L3H1`。发动机功率和生产阶段不同，不重复建组。Master I 资料列出的整车长度和高度分别为 4434/5000/5640 mm 与 2050/2413/2415 mm，维修资料给出不含后视镜车宽 2000 mm。([Transit Center Ford Transit Spare Parts][1])
* 本轮新建 5 个尺寸组，三个 Ktype 全部复用这五组。

## 当前批次进度

* 输入 Ktype：100
* READY Ktype：91
* READY 映射行：139
* PENDING Ktype：9
* 已确认尺寸组：93
* 本轮首次新建尺寸组：5
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27737_l1h1	27737	Van	Master I			EU-RENAULT-MASTER-I-VAN-L1H1-01	MEDIUM	短轴低顶Van分支。	READY
27737_l1h2	27737	Van	Master I			EU-RENAULT-MASTER-I-VAN-L1H2-01	MEDIUM	短轴高顶Van分支。	READY
27737_l2h1	27737	Van	Master I			EU-RENAULT-MASTER-I-VAN-L2H1-01	MEDIUM	中轴低顶Van分支。	READY
27737_l2h2	27737	Van	Master I			EU-RENAULT-MASTER-I-VAN-L2H2-01	MEDIUM	中轴高顶Van分支。	READY
27737_l3h1	27737	Van	Master I			EU-RENAULT-MASTER-I-VAN-L3H1-01	MEDIUM	长轴车身Van分支。	READY
27738_l1h1	27738	Van	Master I			EU-RENAULT-MASTER-I-VAN-L1H1-01	MEDIUM	短轴低顶Van分支。	READY
27738_l1h2	27738	Van	Master I			EU-RENAULT-MASTER-I-VAN-L1H2-01	MEDIUM	短轴高顶Van分支。	READY
27738_l2h1	27738	Van	Master I			EU-RENAULT-MASTER-I-VAN-L2H1-01	MEDIUM	中轴低顶Van分支。	READY
27738_l2h2	27738	Van	Master I			EU-RENAULT-MASTER-I-VAN-L2H2-01	MEDIUM	中轴高顶Van分支。	READY
27738_l3h1	27738	Van	Master I			EU-RENAULT-MASTER-I-VAN-L3H1-01	MEDIUM	长轴车身Van分支。	READY
27739_l1h1	27739	Van	Master I			EU-RENAULT-MASTER-I-VAN-L1H1-01	MEDIUM	短轴低顶Van分支。	READY
27739_l1h2	27739	Van	Master I			EU-RENAULT-MASTER-I-VAN-L1H2-01	MEDIUM	短轴高顶Van分支。	READY
27739_l2h1	27739	Van	Master I			EU-RENAULT-MASTER-I-VAN-L2H1-01	MEDIUM	中轴低顶Van分支。	READY
27739_l2h2	27739	Van	Master I			EU-RENAULT-MASTER-I-VAN-L2H2-01	MEDIUM	中轴高顶Van分支。	READY
27739_l3h1	27739	Van	Master I			EU-RENAULT-MASTER-I-VAN-L3H1-01	MEDIUM	长轴车身Van分支。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-RENAULT-MASTER-I-VAN-L1H1-01	4434	2000	2050	Transit Center Renault Master I specifications; Renault Master I service repair manual	https://www.transitcenter.uk/renault-master-1-data-specification.php; https://vnx.su/content/avto/renault/master_1980.html
EU-RENAULT-MASTER-I-VAN-L1H2-01	4434	2000	2415	Transit Center Renault Master I specifications; Renault Master I service repair manual	https://www.transitcenter.uk/renault-master-1-data-specification.php; https://vnx.su/content/avto/renault/master_1980.html
EU-RENAULT-MASTER-I-VAN-L2H1-01	5000	2000	2050	Transit Center Renault Master I specifications; Renault Master I service repair manual	https://www.transitcenter.uk/renault-master-1-data-specification.php; https://vnx.su/content/avto/renault/master_1980.html
EU-RENAULT-MASTER-I-VAN-L2H2-01	5000	2000	2415	Transit Center Renault Master I specifications; Renault Master I service repair manual	https://www.transitcenter.uk/renault-master-1-data-specification.php; https://vnx.su/content/avto/renault/master_1980.html
EU-RENAULT-MASTER-I-VAN-L3H1-01	5640	2000	2413	Transit Center Renault Master I specifications; Renault Master I service repair manual	https://www.transitcenter.uk/renault-master-1-data-specification.php; https://vnx.su/content/avto/renault/master_1980.html
```

## 下一步优先处理

1. Fiat Ducato I/290：`27780`、`27819`、`27820`、`27821`。
2. VW LT I Syncro：`27785`、`27787`、`27788`。
3. Mazda E2000 4WD：`27847`。
4. VW LT II Bus：`27850`。

推进信号：CONTINUE

[1]: https://www.transitcenter.uk/renault-master-1-data-specification.php?srsltid=AfmBOooMEvydHmIwizT1S8hq0EGC02z1NCXzHZwg6rzltz6rDx7CtqA3 "Renault Master I - Specifications"


--- 发送 / 继续到 Round 16 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2601-2700_ktype_dimension_mapping_final.tsv
- all_2601-2700_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 16 / checkpoint 续跑 ---
## 更新点

* `27820` 与 `27821` 均已确认属于 **Fiat Ducato I Van Typ 280 2.5 D 4×4**，仅发动机功率与生产阶段不同。([m.buycarparts.co.uk][1])
* 两个 Ktype 均按已确认的 `L1H1`、`L1H2`、`L2H2` 三种 Van 外廓拆分，直接复用跨批次现有尺寸组，不重新抓取或重复输出尺寸来源。
* `27780` 属于 Typ 290 Van，不能直接复用 Typ 280 组；当前继续保持待闭合。([autodoc.dk][2])

## 当前批次进度

* 输入 Ktype：100
* READY Ktype：93
* READY 映射行：145
* PENDING Ktype：7
* 已确认尺寸组：93
* 本轮复用既有尺寸组：3
* 本轮首次新建尺寸组：0
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27820_l1h1	27820	Van	Ducato I	280		EU-FIAT-DUCATO-I-280-VAN-L1H1-01	MEDIUM	Typ 280四驱短轴低顶Van分支。	READY
27820_l1h2	27820	Van	Ducato I	280		EU-FIAT-DUCATO-I-280-VAN-L1H2-01	MEDIUM	Typ 280四驱短轴高顶Van分支。	READY
27820_l2h2	27820	Van	Ducato I	280		EU-FIAT-DUCATO-I-280-VAN-L2H2-01	MEDIUM	Typ 280四驱长轴高顶Van分支。	READY
27821_l1h1	27821	Van	Ducato I	280		EU-FIAT-DUCATO-I-280-VAN-L1H1-01	MEDIUM	Typ 280四驱短轴低顶Van分支。	READY
27821_l1h2	27821	Van	Ducato I	280		EU-FIAT-DUCATO-I-280-VAN-L1H2-01	MEDIUM	Typ 280四驱短轴高顶Van分支。	READY
27821_l2h2	27821	Van	Ducato I	280		EU-FIAT-DUCATO-I-280-VAN-L2H2-01	MEDIUM	Typ 280四驱长轴高顶Van分支。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

无

## 下一步优先处理

1. Fiat Ducato Typ 290：`27780`、`27819`。
2. VW LT I Syncro 底盘车：`27785`、`27787`、`27788`。
3. Mazda E2000 4WD：`27847`。
4. VW LT II Bus：`27850`。

推进信号：CONTINUE

[1]: https://m.buycarparts.co.uk/fiat/ducato-box-280/27820/10787/locks-exterior?utm_source=chatgpt.com "Door lock for Fiat Ducato 280 Van 2.5 D 4x4 75 hp Diesel"
[2]: https://www.autodoc.dk/reservedele/stoeddaemper-10221/fiat/ducato/ducato-kasse-290/27780-2-0?utm_source=chatgpt.com "Støddæmper Fiat Ducato 290 Van 2.0 86 HK Benzin 170 D"


--- 发送 / 继续到 Round 17 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2601-2700_ktype_dimension_mapping_final.tsv
- all_2601-2700_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 17 / checkpoint 续跑 ---
## 更新点

* 闭合 Mazda E2000 4WD `27847`。该 Ktype 对应 `SR2` 厢式车；第三代 E-Series 的 4WD 汽油版对应约 4.7 m 长车身，1988 年规格为 `4690×1690×1960 mm`。由于资料未提供明确门数，本轮 `Doors` 留空。([CarsGuide][1])
* VW LT I Syncro 的输入功率与 1991 年官方 LT 4×4 目录中的 LT40/45 发动机规格不一致，暂不套用官方目录中的 `5630×2140×2315 mm` 等尺寸，避免错误建组。

## 当前批次进度

* 输入 Ktype：100
* READY Ktype：94
* READY 映射行：146
* PENDING Ktype：6
* 已确认尺寸组：94
* 本轮首次新建尺寸组：1
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27847	27847	Van	E-Series III	SR2		EU-MAZDA-E-SERIES-III-SR2-VAN-4WD-01	MEDIUM	SR2四驱厢式车；对应4.7米级车身。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-MAZDA-E-SERIES-III-SR2-VAN-4WD-01	4690	1690	1960	CarsGuide 1988 Mazda E2000 dimensions; Mazda Bongo third-generation model history	https://www.carsguide.com.au/mazda/e2000/car-dimensions/1988; https://en.wikipedia.org/wiki/Mazda_Bongo
```

## 下一步优先处理

1. Fiat Ducato I Typ 290：`27780`、`27819`。
2. VW LT I Syncro：`27785`、`27787`、`27788`，重点解决输入功率与官方 LT40/45 4×4 目录冲突。
3. VW LT II Bus：`27850`，拆清短轴、中轴、长轴及车顶高度覆盖范围。

推进信号：CONTINUE

[1]: https://www.carsguide.com.au/mazda/e2000/car-dimensions/1988?utm_source=chatgpt.com "Mazda E2000 Dimensions 1988 - Length, Width, Height ..."


--- 发送 / 继续到 Round 18 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2601-2700_ktype_dimension_mapping_final.tsv
- all_2601-2700_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 18 / checkpoint 续跑 ---
## 更新点

* 闭合 Mazda E2000 4WD `27847`。该 Ktype 对应 `SR2` 厢式车；第三代 E-Series 的 4WD 汽油版对应约 4.7 m 长车身，1988 年规格为 `4690×1690×1960 mm`。由于资料未提供明确门数，本轮 `Doors` 留空。([CarsGuide][1])
* VW LT I Syncro 的输入功率与 1991 年官方 LT 4×4 目录中的 LT40/45 发动机规格不一致，暂不套用官方目录中的 `5630×2140×2315 mm` 等尺寸，避免错误建组。

## 当前批次进度

* 输入 Ktype：100
* READY Ktype：94
* READY 映射行：146
* PENDING Ktype：6
* 已确认尺寸组：94
* 本轮首次新建尺寸组：1
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
27847	27847	Van	E-Series III	SR2		EU-MAZDA-E-SERIES-III-SR2-VAN-4WD-01	MEDIUM	SR2四驱厢式车；对应4.7米级车身。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-MAZDA-E-SERIES-III-SR2-VAN-4WD-01	4690	1690	1960	CarsGuide 1988 Mazda E2000 dimensions; Mazda Bongo third-generation model history	https://www.carsguide.com.au/mazda/e2000/car-dimensions/1988; https://en.wikipedia.org/wiki/Mazda_Bongo
```

## 下一步优先处理

1. Fiat Ducato I Typ 290：`27780`、`27819`。
2. VW LT I Syncro：`27785`、`27787`、`27788`，重点解决输入功率与官方 LT40/45 4×4 目录冲突。
3. VW LT II Bus：`27850`，拆清短轴、中轴、长轴及车顶高度覆盖范围。

推进信号：CONTINUE

[1]: https://www.carsguide.com.au/mazda/e2000/car-dimensions/1988?utm_source=chatgpt.com "Mazda E2000 Dimensions 1988 - Length, Width, Height ..."


--- 发送 / 继续到 Round 19 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2601-2700_ktype_dimension_mapping_final.tsv
- all_2601-2700_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- 脚本异常 ---
异常: 对话分支失败（已尝试 3 次）: 没有找到最后一条用户消息的【在新聊天中分支】入口


--- 发送 / checkpoint 续跑到 Round 20 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2601-2700_ktype_dimension_mapping_final.tsv
- all_2601-2700_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 20 / checkpoint 续跑 ---
ChatGPT 说：最后 6 个 PENDING 已锁定：Fiat Ducato 290 两条、VW LT I Syncro 三条、VW LT II Bus 一条。我将只补齐这 6 条，不回头重查已 READY 记录。到目前为止，这段对话对你有帮助吗？


--- 发送 / 推进信号纠偏 / Round 21 ---
你的上一轮回复缺少正常推进信号。继续当前批次：尺寸组首次建档后必须复用；仅输出本轮新增/修改的 Ktype 映射行和首次创建/修正的 DIMENSION_GROUP 行，无变化明确写“无”，并给出下一步优先处理。未完成输出“推进信号：CONTINUE”；只有同一回复包含两张最终完整表且全部映射闭合时才可 COMPLETE。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_2601-2700_ktype_dimension_mapping_final.tsv
- all_2601-2700_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- 脚本异常 ---
异常: 对话分支失败（已尝试 3 次）: 没有找到最后一条用户消息的【在新聊天中分支】入口

