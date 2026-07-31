# 任务：all 第 1-100 行
# 来源文件：all.tsv
# 任务 ID：all__batch__0001__a0cf2888


--- 发送 / 首次任务 ---
【任务名称】
【全量表更新】all 第 1-100 行

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
all 第 1-100 行

【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1-100_ktype_dimension_mapping_final.tsv
- all_1-100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


【TSV 数据】
Make	Model	VariantName	BodyStyle	DriveType	Energy	EngineOutputKW	EngineOutputHP	Product Start Month-Year	Product End Month-Year	LastProcessedDate	Ktype
Audi	Q3	RS Performance 2.5 Quattro	SUV	Allrad	Benzin	270	367	Jan 2015	Oct 2018	2024-03-01	119111
Mitsubishi	I	Miev	Schrägheck	Heckantrieb	Elektro	35	48	Jul 2009	May 2020	2024-03-01	119112
Mitsubishi	L200	2.4 Di-d	Pick-up	Heckantrieb	Diesel	113	154	Sep 2015	-	2024-03-01	119113
Hyundai	Tucson	1.7 Crdi	SUV	Frontantrieb	Diesel	104	141	Jun 2015	Sep 2020	2024-03-01	119122
Hyundai	I20 ii	1.0 T-gdi	Coupe	Frontantrieb	Benzin	74	101	Jan 2016	Sep 2021	2025-06-01	119123
Mazda	3	2	Stufenheck	Frontantrieb	Benzin	113	154	Sep 2011	Sep 2014	2024-03-01	119146
Audi	A4 b9	2.0 TDI	Stufenheck	Frontantrieb	Diesel	90	122	May 2016	Nov 2019	2024-03-01	119148
KIA	Sorento ii	3.5 4WD	SUV	Allrad	Benzin	204	278	May 2013	Dec 2015	2024-03-01	119149
Audi	A4 b9 avant	2.0 TDI	Kombi	Frontantrieb	Diesel	90	122	Apr 2016	Sep 2018	2024-03-01	119152
Suzuki	Vitara	1.6 Allrad	Geländewagen geschlossen	Allrad	Benzin	70	95	Feb 1991	Mar 1998	2024-03-01	119160
Audi	A4 allroad b9	2.0 Tfsi Quattro	Kombi	Allrad	Benzin	185	252	Jan 2016	-	2024-03-01	119166
Audi	A4 allroad b9	3.0 TDI Quattro	Kombi	Allrad	Diesel	160	218	Jan 2016	Aug 2018	2024-03-01	119167
Audi	A4 allroad b9	2.0 TDI Quattro	Kombi	Allrad	Diesel	140	190	Jan 2016	Dec 2019	2026-07-01	119168
Audi	A4 allroad b9	3.0 TDI Quattro	Kombi	Allrad	Diesel	200	272	Jan 2016	Aug 2018	2024-03-01	119169
Hyundai	I20 ii	1.0 T-gdi	Coupe	Frontantrieb	Benzin	88	120	Jan 2016	Sep 2021	2025-06-01	119185
Aston Martin	Db11 vantage	5.2 V12	Coupe	Heckantrieb	Benzin	447	608	Jan 2016	-	2024-03-01	119186
Dacia	Sandero	1.6 LPG	Schrägheck	Frontantrieb	Benzin/Autogas (LPG)	62	84	May 2010	Oct 2012	2024-03-01	119193
Alpina	B7	Biturbo Allrad	Stufenheck	Allrad	Benzin	447	608	Feb 2016	Dec 2022	2026-06-01	119200
Peugeot	Partner tepee	1.2 THP	Großraumlimousine	Frontantrieb	Benzin	81	110	Feb 2016	-	2024-03-01	119202
VW	Passat b2	1.6 D	Stufenheck	Frontantrieb	Diesel	40	54	Aug 1984	Mar 1988	2024-03-01	119206
Renault Trucks	Mascott	150.35	Pritsche/Fahrgestell	Heckantrieb	Diesel	110	150	May 2004	Dec 2013	2024-03-01	119207
Seat	Ibiza iv st	1.6	Kombi	Frontantrieb	Benzin	77	105	Feb 2012	May 2015	2024-03-01	119216
Hyundai	I20 ii	1.2 Lpgi	Schrägheck	Frontantrieb	Benzin/Autogas (LPG)	61	83	Nov 2014	Jun 2019	2024-05-01	119222
BMW	X6	Xdrive 30 D	SUV	Allrad	Diesel	183	249	Dec 2014	Jul 2019	2024-03-01	119225
Maserati	Levante	3.0 S Q4	SUV	Allrad	Benzin	316	430	Jun 2016	-	2024-03-01	119226
Maserati	Levante	3.0 D Q4	SUV	Allrad	Diesel	202	275	Jun 2016	-	2024-03-01	119227
Nissan	Navara	2.3 DCI	Pick-up	Heckantrieb	Diesel	140	190	Jan 2015	-	2025-06-01	119256
Renault	Master iii	2.3 DCI 130 FWD	Pritsche/Fahrgestell	Frontantrieb	Diesel	96	130	Jul 2015	Dec 2020	2026-03-01	119278
Hyundai	Ix35	2	SUV	Frontantrieb	Benzin	114	155	Nov 2013	Dec 2015	2024-03-01	119295
Hyundai	Ix35	2.0 AWD	SUV	Allrad	Benzin	114	155	Nov 2013	Dec 2015	2024-03-01	119296
Fiat	124	1.4	Cabriolet	Heckantrieb	Benzin	103	140	Mar 2016	-	2024-03-01	119302
Maserati	Levante	3.0 Q4	SUV	Allrad	Benzin	257	350	Jun 2016	-	2024-03-01	119326
Citroën	Berlingo	1.2 Puretech 110	Großraumlimousine	Frontantrieb	Benzin	81	110	Mar 2016	Dec 2018	2026-05-01	119329
Infiniti	Qx30	2.2 D AWD	SUV	Allrad	Diesel	125	170	Apr 2016	-	2024-03-01	119351
Maserati	Mistral	3.7	Cabriolet	Heckantrieb	Benzin	180	245	Sep 1963	Dec 1970	2025-06-01	119424
Maserati	Mistral	4	Cabriolet	Heckantrieb	Benzin	188	255	Sep 1966	Dec 1970	2025-06-01	119432
Ford	Transit v363	2.0 Ecoblue	Kasten	Frontantrieb	Diesel	96	130	Mar 2016	-	2024-03-01	119467
Ford	Transit v363	2.0 Ecoblue	Kasten	Frontantrieb	Diesel	77	105	Mar 2016	-	2024-03-01	119468
Ford	Transit v363	2.0 Ecoblue	Kasten	Frontantrieb	Diesel	125	170	Mar 2016	Jun 2024	2024-11-01	119470
Ford	Transit v363	2.0 Ecoblue RWD	Kasten	Heckantrieb	Diesel	77	105	Mar 2016	-	2024-03-01	119471
Ford	Transit v363	2.0 Ecoblue RWD	Kasten	Heckantrieb	Diesel	96	130	Mar 2016	-	2024-03-01	119472
Ford	Transit v363	2.0 Ecoblue RWD	Kasten	Heckantrieb	Diesel	125	170	Mar 2016	Jun 2024	2024-11-01	119473
Mercedes-benz	Cla	CLA 220 4-matic	Coupe	Allrad	Benzin	135	184	Apr 2016	Mar 2019	2024-03-01	119474
Ford	Transit v363	2.0 Ecoblue	Pritsche/Fahrgestell	Frontantrieb	Diesel	77	105	Mar 2016	-	2024-03-01	119475
Ford	Transit v363	2.0 Ecoblue	Pritsche/Fahrgestell	Frontantrieb	Diesel	96	130	Mar 2016	-	2024-03-01	119476
Ford	Transit v363	2.0 Ecoblue	Pritsche/Fahrgestell	Frontantrieb	Diesel	125	170	Mar 2016	Jun 2024	2024-11-01	119477
Ford	Transit v363	2.0 Ecoblue RWD	Pritsche/Fahrgestell	Heckantrieb	Diesel	77	105	Mar 2016	-	2024-03-01	119478
Ford	Transit v363	2.0 Ecoblue RWD	Pritsche/Fahrgestell	Heckantrieb	Diesel	96	130	Mar 2016	-	2024-03-01	119479
Ford	Transit v363	2.0 Ecoblue RWD	Pritsche/Fahrgestell	Heckantrieb	Diesel	125	170	Mar 2016	Jun 2024	2024-11-01	119480
Ford	Transit v363	2.0 Ecoblue	Bus	Frontantrieb	Diesel	77	105	Mar 2016	-	2024-03-01	119481
Ford	Transit v363	2.0 Ecoblue	Bus	Frontantrieb	Diesel	96	130	Mar 2016	-	2024-03-01	119482
Ford	Transit v363	2.0 Ecoblue	Bus	Frontantrieb	Diesel	125	170	Mar 2016	Jun 2024	2024-11-01	119483
Citroën	Jumpy iii	1.6 Bluehdi 95	Kasten	Frontantrieb	Diesel	70	95	Apr 2016	Apr 2020	2025-02-03	119484
Citroën	Jumpy iii	1.6 Bluehdi 115	Kasten	Frontantrieb	Diesel	85	116	Apr 2016	Jun 2022	2025-12-01	119485
Citroën	Jumpy iii	2.0 Bluehdi 120	Kasten	Frontantrieb	Diesel	90	122	Apr 2016	Dec 2022	2025-12-01	119486
Citroën	Jumpy iii	2.0 Bluehdi 150	Kasten	Frontantrieb	Diesel	110	150	Apr 2016	Dec 2022	2025-12-01	119487
Citroën	Jumpy iii	2.0 Bluehdi 180	Kasten	Frontantrieb	Diesel	130	177	Apr 2016	Apr 2025	2025-12-01	119488
Dacia	Duster	1.2 TCE 125 4X4	Kasten/SUV	Allrad	Benzin	92	125	Oct 2013	-	2024-03-01	119489
Dacia	Duster	1.6 SCE 115	Kasten/SUV	Frontantrieb	Benzin	84	115	Jun 2015	-	2024-03-01	119490
Dacia	Duster	1.6 SCE 115 4X4	Kasten/SUV	Allrad	Benzin	84	115	Jun 2015	Jan 2018	2024-03-01	119491
Renault	Captur i	1.2 TCE 120	Schrägheck	Frontantrieb	Benzin	87	118	Jan 2016	Aug 2018	2025-12-01	119493
Renault	Clio iv	1.2 TCE 120	Schrägheck	Frontantrieb	Benzin	87	118	Jan 2016	Aug 2021	2026-05-01	119495
Renault	Clio iv grandtour	1.2 TCE 120	Kombi	Frontantrieb	Benzin	87	118	Jan 2016	Aug 2021	2026-05-01	119497
Mercedes-benz	Cla	CLA 220 4-matic	Kombi	Allrad	Benzin	135	184	Apr 2016	Mar 2019	2024-03-01	119500
Peugeot	Traveller	1.6 Bluehdi 95	Bus	Frontantrieb	Diesel	70	95	Apr 2016	Dec 2019	2025-12-01	119502
Peugeot	Traveller	1.6 Bluehdi 115	Bus	Frontantrieb	Diesel	85	116	Apr 2016	Dec 2019	2025-12-01	119503
Mercedes-benz	Glc	AMG 43 4-matic	SUV	Allrad	Benzin	270	367	Apr 2016	Aug 2019	2024-03-01	119509
Peugeot	Traveller	2.0 Bluehdi 150 / HDI 150	Bus	Frontantrieb	Diesel	110	150	Apr 2016	Dec 2022	2025-12-01	119511
Abarth	124	1.4	Cabriolet	Heckantrieb	Benzin	125	170	Mar 2016	-	2024-03-01	119512
Peugeot	Traveller	2.0 Bluehdi 180	Bus	Frontantrieb	Diesel	130	177	Apr 2016	Apr 2025	2025-12-01	119513
Fiat	Ducato	150 Multijet 2,3 D	Kasten	Frontantrieb	Diesel	110	150	Dec 2015	-	2024-03-01	119515
Mercedes-benz	C-Klasse	AMG C 43 4-matic	Stufenheck	Allrad	Benzin	270	367	Apr 2016	May 2018	2024-03-01	119516
Fiat	Ducato	150 Multijet 2,3 D	Pritsche/Fahrgestell	Frontantrieb	Diesel	110	150	Dec 2015	-	2024-03-01	119519
Fiat	Ducato	180 Multijet 2,3 D	Pritsche/Fahrgestell	Frontantrieb	Diesel	130	177	Dec 2015	-	2024-03-01	119521
Fiat	Ducato	180 Multijet 2,3 D	Kasten	Frontantrieb	Diesel	130	177	Dec 2015	-	2024-03-01	119523
Mercedes-benz	C-Klasse	AMG C 43 4-matic	Kombi	Allrad	Benzin	270	367	Apr 2016	May 2018	2024-03-01	119530
Nissan	Cabstar	2.5 TD	Pritsche/Fahrgestell	Heckantrieb	Diesel	59	80	Oct 1982	Jun 1992	2024-03-01	119556
Nissan	Cabstar	2.5 D	Pritsche/Fahrgestell	Heckantrieb	Diesel	53	72	Feb 1983	Dec 1990	2024-03-01	119560
Nissan	Cabstar	1.6	Pritsche/Fahrgestell	Heckantrieb	Benzin	62	84	Oct 1986	Sep 1992	2024-03-01	119563
Nissan	Cabstar	2.0 TD	Pritsche/Fahrgestell	Heckantrieb	Diesel	60	82	Jan 1982	Dec 1987	2024-03-01	119566
Nissan	Cabstar	2.2	Pritsche/Fahrgestell	Heckantrieb	Benzin	71	97	Oct 1984	Jun 1992	2024-03-01	119567
Nissan	Cabstar	2.7 TD	Pritsche/Fahrgestell	Heckantrieb	Diesel	66	90	Feb 1983	Dec 1992	2024-03-01	119570
Nissan	Cabstar	3.3 TD	Pritsche/Fahrgestell	Heckantrieb	Diesel	71	97	Feb 1983	Dec 1990	2024-03-01	119571
Mercedes-benz	Sprinter 3-T	211 CDI	Bus	Heckantrieb	Diesel	84	114	Apr 2016	Dec 2018	2024-03-01	119573
Mercedes-benz	Sprinter 3-T	214 CDI	Bus	Heckantrieb	Diesel	105	143	Apr 2016	Dec 2018	2024-03-01	119574
Mercedes-benz	Sprinter 3-T	211 CDI	Kasten	Heckantrieb	Diesel	84	114	Apr 2016	Dec 2018	2024-03-01	119576
Volvo	Xc60 i	T5 AWD	SUV	Allrad	Benzin	180	245	Oct 2015	Feb 2017	2024-03-01	119578
Mercedes-benz	Sprinter 3-T	214 CDI	Kasten	Heckantrieb	Diesel	105	143	Apr 2016	Dec 2018	2024-03-01	119579
Mercedes-benz	Sprinter 3-T	214 CDI	Pritsche/Fahrgestell	Heckantrieb	Diesel	105	143	Apr 2016	Dec 2018	2024-03-01	119580
Mercedes-benz	Sprinter 3-T	211 CDI	Pritsche/Fahrgestell	Heckantrieb	Diesel	84	114	Apr 2016	Dec 2018	2024-03-01	119581
Nissan	Cabstar	75.28	Pritsche/Fahrgestell	Heckantrieb	Diesel	55	75	Oct 1998	Oct 2006	2024-03-01	119585
Nissan	Cabstar	90.32, 90.28, 95.32, 95.28	Pritsche/Fahrgestell	Heckantrieb	Diesel	66	90	Oct 1998	Oct 2006	2024-03-01	119587
Nissan	Cabstar	105.35, 110.35, 110.45	Pritsche/Fahrgestell	Heckantrieb	Diesel	78	106	Oct 1998	Oct 2006	2024-03-01	119589
Nissan	Cabstar	120.35, 120.45	Pritsche/Fahrgestell	Heckantrieb	Diesel	88	120	Oct 1998	Oct 2006	2024-03-01	119591
Nissan	Cabstar	125.35, 125.45	Pritsche/Fahrgestell	Heckantrieb	Diesel	92	125	Oct 1998	Oct 2006	2024-03-01	119597
Mercedes-benz	C-Klasse	C 220 D 4-matic	Coupe	Allrad	Diesel	125	170	Apr 2016	May 2018	2024-03-01	119602
Mercedes-benz	C-Klasse	C 250 D 4-matic	Coupe	Allrad	Diesel	150	204	Apr 2016	May 2018	2024-03-01	119603
Mercedes-benz	C-Klasse	C 200 4-matic	Coupe	Allrad	Benzin	135	184	Apr 2016	May 2018	2024-03-01	119604
Mercedes-benz	C-Klasse	C 400 4-matic	Coupe	Allrad	Benzin	245	333	Apr 2016	Jun 2022	2024-03-01	119605
Mercedes-benz	C-Klasse	AMG C 43 4-matic	Coupe	Allrad	Benzin	270	367	Apr 2016	May 2018	2024-03-01	119606


--- Round 1 / 首次发送 ---
## 更新点

* 已按物理外廓聚类处理前 26 个输入 Ktype，形成 18 条 READY 映射和 13 个已闭合尺寸组。
* `119168` 的生产范围跨越 Audi A4 allroad B9 2019 年改款，已拆分为 `prefl` 与 `facelift` 两条派生映射；改款前后车长、车宽不同，不能强行共用同一尺寸组。([auto-data.net][1])
* i20 Coupe 的两个动力 Ktype、Levante 的三个动力 Ktype，以及多个 A4 allroad 改款前动力版本均已复用对应尺寸组，未重复建组。
* L200、Mascott、Vitara 等存在驾驶室、货斗、轴距或门数分支的记录暂不猜测建组。

## 当前批次进度

* 已处理输入 Ktype：26 / 100
* READY 映射：18 行，覆盖 17 个 Ktype
* PENDING 映射：9 行，覆盖 9 个 Ktype
* 已确认尺寸组：13
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
119111	119111	SUV	RS Q3 8U Facelift	8U	5	EU-AUDI-RS-Q3-8U-FACELIFT-SUV-01	HIGH		READY
119112	119112	Hatchback	i-MiEV		5	EU-MITSUBISHI-I-MIEV-HATCHBACK-01	HIGH		READY
119113	119113	Pickup	L200 V				LOW	候选含不同驾驶室/货斗，当前输入未能确定具体物理分支。	PENDING: 驾驶室与货斗分支未确定
119122	119122	SUV	Tucson III	TL	5	EU-HYUNDAI-TUCSON-III-SUV-01	HIGH		READY
119123	119123	Coupe	i20 II Coupe	GB	3	EU-HYUNDAI-I20-II-COUPE-3D-01	HIGH		READY
119146	119146	Sedan	Mazda 3 II Facelift	BL	4	EU-MAZDA-3-II-BL-FACELIFT-SEDAN-01	HIGH		READY
119148	119148	Sedan	A4 B9	8W2	4		LOW	生产区间跨越B9改款，需确认Ktype覆盖的具体外廓分支。	PENDING: B9改款分支未闭合
119149	119149	SUV	Sorento II Facelift	XM	5		LOW	3.5 4WD的功率与生产期和已找到的欧洲规格不完全一致。	PENDING: 版本与市场边界冲突未解决
119152	119152	Wagon	A4 B9 Avant	8W5	5		LOW	结束月份接近2018改款边界，需确认是否仅覆盖改款前外廓。	PENDING: 改款边界未确认
119160	119160	SUV	Vitara I				LOW	该代1.6四驱存在3门与5门外廓，当前输入未能确定具体分支。	PENDING: 门数分支未确定
119166	119166	Wagon	A4 allroad B9	8WH	5	EU-AUDI-A4-ALLROAD-B9-WAGON-PREFL-01	HIGH		READY
119167	119167	Wagon	A4 allroad B9	8WH	5	EU-AUDI-A4-ALLROAD-B9-WAGON-PREFL-01	HIGH		READY
119168_prefl	119168	Wagon	A4 allroad B9	8WH	5	EU-AUDI-A4-ALLROAD-B9-WAGON-PREFL-01	MEDIUM	生产区间跨越2019改款，按改款前外廓拆分。	READY
119168_facelift	119168	Wagon	A4 allroad B9 Facelift	8WH	5	EU-AUDI-A4-ALLROAD-B9-WAGON-FACELIFT-01	MEDIUM	生产区间跨越2019改款，按改款后外廓拆分。	READY
119169	119169	Wagon	A4 allroad B9	8WH	5	EU-AUDI-A4-ALLROAD-B9-WAGON-PREFL-01	HIGH		READY
119185	119185	Coupe	i20 II Coupe	GB	3	EU-HYUNDAI-I20-II-COUPE-3D-01	HIGH		READY
119186	119186	Coupe	DB11		2	EU-ASTON-MARTIN-DB11-COUPE-V12-01	MEDIUM	输入Model含vantage字样；动力与生产期匹配DB11 V12。	READY
119193	119193	Hatchback	Sandero I		5	EU-DACIA-SANDERO-I-HATCHBACK-01	MEDIUM		READY
119200	119200	Sedan	B7 G12	G12	4		LOW	生产区间跨越G12改款，需确认Ktype是否覆盖改款前后外廓。	PENDING: G12改款分支未闭合
119202	119202	MPV	Partner II Tepee Phase III		5		LOW	需闭合Phase III 1.2 THP对应外廓的直接三维来源。	PENDING: 直接三维来源未闭合
119206	119206	Sedan	Passat B2	B2			LOW	输入为Sedan，但直接车型资料将B2 1.6 D列为5门Hatchback。	PENDING: 车身形式冲突未解决
119207	119207	Pickup	Mascott				LOW	底盘/平台存在多轴距与驾驶室配置，当前输入未能确定具体外廓。	PENDING: 轴距与驾驶室分支未确定
119216	119216	Wagon	Ibiza IV ST Facelift	6J8	5	EU-SEAT-IBIZA-IV-ST-WAGON-01	HIGH		READY
119222	119222	Hatchback	i20 II	GB	5	EU-HYUNDAI-I20-II-HATCHBACK-01	HIGH		READY
119225	119225	SUV	X6 F16	F16	5	EU-BMW-X6-F16-SUV-01	MEDIUM		READY
119226	119226	SUV	Levante	M161	5	EU-MASERATI-LEVANTE-M161-SUV-01	HIGH		READY
119227	119227	SUV	Levante	M161	5	EU-MASERATI-LEVANTE-M161-SUV-01	HIGH		READY
```

## 本轮新增/修改的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-AUDI-RS-Q3-8U-FACELIFT-SUV-01	4411	1841	1580	Auto-Data Audi RS Q3 facelift 2.5 TFSI performance 367	https://www.auto-data.net/en/audi-rsq3-facelift-2015-2.5-tfsi-performance-367hp-quattro-s-tronic-23153
EU-MITSUBISHI-I-MIEV-HATCHBACK-01	3475	1475	1610	Auto-Data Mitsubishi i-MiEV generation	https://www.auto-data.net/en/mitsubishi-i-miev-generation-4265
EU-HYUNDAI-TUCSON-III-SUV-01	4475	1850	1660	Auto-Data Hyundai Tucson III generation	https://www.auto-data.net/en/hyundai-tucson-iii-generation-4645
EU-HYUNDAI-I20-II-COUPE-3D-01	4045	1730	1449	Auto-Data Hyundai i20 II Coupe 1.0 T-GDI 120	https://www.auto-data.net/en/hyundai-i20-ii-coupe-1.0-t-gdi-120hp-24714
EU-MAZDA-3-II-BL-FACELIFT-SEDAN-01	4580	1755	1470	Auto-Data Mazda 3 II Sedan BL facelift 2.0 DISI	https://www.auto-data.net/en/mazda-3-ii-sedan-bl-facelift-2011-2.0-disi-150hp-17498
EU-AUDI-A4-ALLROAD-B9-WAGON-PREFL-01	4750	1842	1493	Auto-Data Audi A4 allroad B9 2.0 TFSI 252; Auto-Data Audi A4 allroad B9 3.0 TDI 272	https://www.auto-data.net/en/audi-a4-allroad-b9-8w-2.0-tfsi-252hp-quattro-ultra-s-tronic-22691;https://www.auto-data.net/en/audi-a4-allroad-b9-8w-3.0-tdi-v6-272hp-quattro-tiptronic-22723
EU-AUDI-A4-ALLROAD-B9-WAGON-FACELIFT-01	4762	1847	1493	Auto-Data Audi A4 allroad B9 facelift 2019 generation	https://www.auto-data.net/en/audi-a4-allroad-b9-8w-facelift-2019-generation-7284
EU-ASTON-MARTIN-DB11-COUPE-V12-01	4739	1940	1279	Auto-Data Aston Martin DB11 5.2 V12 608	https://www.auto-data.net/en/aston-martin-db11-5.2-v12-608hp-automatic-24281
EU-DACIA-SANDERO-I-HATCHBACK-01	4020	1746	1534	Auto-Data Dacia Sandero I 1.6 8V	https://www.auto-data.net/en/dacia-sandero-i-1.6-8v-87hp-15894
EU-SEAT-IBIZA-IV-ST-WAGON-01	4236	1693	1445	Auto-Data Seat Ibiza IV ST facelift	https://www.auto-data.net/en/seat-ibiza-iv-st-facelift-2012-1.2-tsi-105hp-19329
EU-HYUNDAI-I20-II-HATCHBACK-01	4035	1734	1474	Auto-Data Hyundai i20 model specifications	https://www.auto-data.net/en/hyundai-i20-model-1503
EU-BMW-X6-F16-SUV-01	4909	1989	1702	Auto-Data BMW X6 F16 30d xDrive	https://www.auto-data.net/en/bmw-x6-f16-30d-258hp-xdrive-steptronic-20579
EU-MASERATI-LEVANTE-M161-SUV-01	5003	1968	1679	Auto-Data Maserati Levante 3.0 V6 GDI 350; Auto-Data Maserati Levante 3.0 V6 diesel 275	https://www.auto-data.net/en/maserati-levante-3.0-v6-gdi-350hp-awd-automatic-22810;https://www.auto-data.net/en/maserati-levante-3.0-v6-275hp-awd-automatic-22815
```

## 下一步优先处理

1. 闭合当前 9 条 PENDING，优先处理 A4 B9 Sedan/Avant、Alpina B7 G12 的改款分支。
2. 确认 L200、Vitara、Mascott 的驾驶室、货斗、门数和轴距边界。
3. 继续处理 `119256` 起的 Navara、Master、ix35、Fiat 124、Berlingo、QX30 等记录。
4. 将 Transit、Jumpy、Traveller、Ducato、Sprinter、Cabstar 按轴距、车顶、驾驶室和车身形式集中聚类后批量建组。

推进信号：CONTINUE

[1]: https://www.auto-data.net/en/audi-a4-allroad-b9-8w-generation-4677?utm_source=chatgpt.com "Audi A4 allroad (B9 8W) /2016, 2017, 2018/ specs, Fuel ..."


--- 发送 / 继续到 Round 2 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1-100_ktype_dimension_mapping_final.tsv
- all_1-100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 2 / 下一步 ---
## 更新点

* 闭合上一轮 4 个 PENDING Ktype：`119148`、`119152`、`119200`、`119206`。其中 `119200` 按 Alpina B7 G12 改款前后拆为两个物理分支；A4 B9 Sedan、Avant 使用改款前官方尺寸组；Passat B2 按四门 notchback 分支落盘。
* 新推进 `119256–119432` 共 10 个 Ktype；ix35 两个驱动版本复用同一尺寸组，`119326` 直接复用既有 Levante 尺寸组，未重复输出尺寸事实。Fiat 124 Spider 与 QX30 已完成首次建组。([汽车目录][1])
* Mistral Spyder 的直接规格来源存在 `1650 mm` 与 `1675 mm` 车宽冲突，`119424`、`119432` 暂不创建尺寸组。([汽车目录][2])

## 当前批次进度

* 已覆盖输入 Ktype：36 / 100
* READY 映射：28
* PENDING 映射：10
* 已确认尺寸组：21
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
119148	119148	Sedan	A4 B9	8W2	4	EU-AUDI-A4-B9-SEDAN-PREFL-01	HIGH		READY
119152	119152	Wagon	A4 B9 Avant	8W5	5	EU-AUDI-A4-B9-AVANT-PREFL-01	HIGH		READY
119200_prefl	119200	Sedan	B7 G12	G12	4	EU-ALPINA-B7-G12-SEDAN-PREFL-01	HIGH	G12改款前物理外廓。	READY
119200_facelift	119200	Sedan	B7 G12 Facelift	G12	4	EU-ALPINA-B7-G12-SEDAN-FACELIFT-01	HIGH	G12改款后物理外廓。	READY
119206	119206	Sedan	Passat B2	32B	4	EU-VW-PASSAT-B2-NOTCHBACK-SEDAN-01	HIGH	B2四门notchback物理分支。	READY
119256	119256	Pickup	Navara NP300	D23			LOW	候选含不同驾驶室与轴距分支。	PENDING: 驾驶室与轴距分支未确定
119278	119278	Pickup	Master III Phase II	X62			LOW	底盘驾驶室存在多轴距与驾驶室配置。	PENDING: 轴距与驾驶室分支未确定
119295	119295	SUV	ix35 I Facelift	LM	5	EU-HYUNDAI-IX35-I-FACELIFT-SUV-01	MEDIUM		READY
119296	119296	SUV	ix35 I Facelift	LM	5	EU-HYUNDAI-IX35-I-FACELIFT-SUV-01	MEDIUM		READY
119302	119302	Convertible	124 Spider		2	EU-FIAT-124-SPIDER-CONVERTIBLE-01	HIGH		READY
119326	119326	SUV	Levante	M161	5	EU-MASERATI-LEVANTE-M161-SUV-01	HIGH		READY
119329	119329	MPV	Berlingo II Facelift	B9	5		LOW	乘用版不同车顶及外部配置存在高度差异。	PENDING: 高度配置边界未确定
119351	119351	SUV	QX30	H15	5	EU-INFINITI-QX30-SUV-01	HIGH		READY
119424	119424	Convertible	Mistral Spyder	AM109	2		LOW	直接规格来源存在1650与1675毫米车宽冲突。	PENDING: 车宽来源冲突未解决
119432	119432	Convertible	Mistral Spyder	AM109	2		LOW	直接规格来源存在1650与1675毫米车宽冲突。	PENDING: 车宽来源冲突未解决
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-AUDI-A4-B9-SEDAN-PREFL-01	4726	1842	1427	Audi A4 Sedan official technical specifications	https://i.i-sgcm.com/new_cars/cars/11806/brochures/brochure_20180108045227.pdf
EU-AUDI-A4-B9-AVANT-PREFL-01	4725	1842	1434	Audi A4 Avant official technical specifications	https://i.i-sgcm.com/new_cars/cars/11910/brochures/brochure_20160823092636.pdf
EU-ALPINA-B7-G12-SEDAN-PREFL-01	5250	1902	1491	Auto-Data Alpina B7 G12 generation	https://www.auto-data.net/en/alpina-b7-model-225
EU-ALPINA-B7-G12-SEDAN-FACELIFT-01	5268	1902	1491	Auto-Data Alpina B7 G12 facelift generation	https://www.auto-data.net/en/alpina-b7-model-225
EU-VW-PASSAT-B2-NOTCHBACK-SEDAN-01	4530	1710	1385	Volkswagen Newsroom Passat B2 profile	https://www.volkswagen-newsroom.com/en/vehicle-data-passat-b2-profile-19538
EU-HYUNDAI-IX35-I-FACELIFT-SUV-01	4410	1820	1665	Automobile-Catalog Hyundai ix35 2.0 GDI 2WD; Automobile-Catalog Hyundai ix35 2.0 GDI 4WD	https://www.automobile-catalog.com/car/2013/1978850/hyundai_ix35_2_0_gdi_2wd.html;https://www.automobile-catalog.com/car/2013/1978880/hyundai_ix35_2_0_gdi_4wd.html
EU-FIAT-124-SPIDER-CONVERTIBLE-01	4054	1740	1233	Automobile-Catalog Fiat 124 Spider 2016	https://www.automobile-catalog.com/car/2016/2455475/fiat_124_spider.html
EU-INFINITI-QX30-SUV-01	4425	1815	1530	INFINITI QX30 official technical specifications	https://www-europe.infiniti-cdn.net/content/dam/Infiniti/me/brochures/Infiniti-QX30-Catalogue-EN.pdf
```

## 下一步优先处理

1. 消除现有 10 个 PENDING，优先处理 L200、Navara、Master、Mascott 的驾驶室及轴距分支。
2. 闭合 Vitara 门数、Sorento 市场版本、Partner/Berlingo 高度配置及 Mistral 车宽冲突。
3. 继续推进 `119467` 起的 Transit、CLA、Jumpy、Duster、Captur、Clio 和 Traveller；先处理可单一建组或直接复用的乘用车，再集中拆分多轴距、多车顶商用车。

推进信号：CONTINUE

[1]: https://www.automobile-catalog.com/car/2013/1978850/hyundai_ix35_2_0_gdi_2wd.html?utm_source=chatgpt.com "2013 Hyundai ix35 2.0 GDI 2WD Specs Review (122 kW / 166 PS / 164 hp) (since September 2013 for Europe )"
[2]: https://www.automobile-catalog.com/car/1969/1443575/maserati_mistral_spyder_4000.html?utm_source=chatgpt.com "1969 Maserati Mistral Spyder 4000 Specs Review (187.5 ..."


--- 发送 / 继续到 Round 3 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1-100_ktype_dimension_mapping_final.tsv
- all_1-100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 3 / 下一步 ---
## 更新点

* `119160` 已按 Vitara I 三门硬顶与五门车身拆分，两种外廓均有对应尺寸资料，不再保留基础 `id=119160`。([汽车数据网][1])
* 新闭合 CLA Coupe、CLA Shooting Brake、Duster I Facelift、GLC X253 AMG 和 Abarth 124 Spider；三个 Duster 动力/驱动 Ktype 复用同一尺寸组。
* `119493`、`119495`、`119497` 的生产区间跨越改款，且改款前后高度或宽度发生变化，已分别拆为 `prefl/facelift` 映射。([汽车数据网][2])
* `119202` 的 PENDING 原因已收敛为乘用版高度配置分支未确定，未创建猜测性尺寸组。

## 当前批次进度

* 已覆盖输入 Ktype：46 / 100
* READY 映射：43
* PENDING 映射：9
* 已确认尺寸组：34
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
119160_3dr	119160	SUV	Vitara I		3	EU-SUZUKI-VITARA-I-SUV-3D-01	MEDIUM	三门硬顶物理外廓。	READY
119160_5dr	119160	SUV	Vitara I		5	EU-SUZUKI-VITARA-I-SUV-5D-01	MEDIUM	五门物理外廓。	READY
119202	119202	MPV	Partner II Tepee Phase III		5			LOW	乘用版高度随车顶附件配置变化，输入无法确定具体外廓分支。	PENDING: 高度配置分支未确定
119474	119474	Coupe	CLA C117 Facelift	C117	4	EU-MERCEDES-BENZ-CLA-C117-FACELIFT-COUPE-01	HIGH		READY
119489	119489	SUV	Duster I Facelift		5	EU-DACIA-DUSTER-I-FACELIFT-SUV-01	HIGH		READY
119490	119490	SUV	Duster I Facelift		5	EU-DACIA-DUSTER-I-FACELIFT-SUV-01	HIGH		READY
119491	119491	SUV	Duster I Facelift		5	EU-DACIA-DUSTER-I-FACELIFT-SUV-01	HIGH		READY
119493_prefl	119493	SUV	Captur I		5	EU-RENAULT-CAPTUR-I-SUV-PREFL-01	HIGH	改款前物理外廓。	READY
119493_facelift	119493	SUV	Captur I Facelift		5	EU-RENAULT-CAPTUR-I-SUV-FACELIFT-01	HIGH	2017改款后物理外廓。	READY
119495_prefl	119495	Hatchback	Clio IV Phase I		5	EU-RENAULT-CLIO-IV-HATCHBACK-PREFL-01	HIGH	改款前物理外廓。	READY
119495_facelift	119495	Hatchback	Clio IV Phase II		5	EU-RENAULT-CLIO-IV-HATCHBACK-FACELIFT-01	HIGH	2016改款后物理外廓。	READY
119497_prefl	119497	Wagon	Clio IV Grandtour Phase I		5	EU-RENAULT-CLIO-IV-GRANDTOUR-WAGON-PREFL-01	HIGH	改款前物理外廓。	READY
119497_facelift	119497	Wagon	Clio IV Grandtour Phase II		5	EU-RENAULT-CLIO-IV-GRANDTOUR-WAGON-FACELIFT-01	HIGH	2016改款后物理外廓。	READY
119500	119500	Wagon	CLA Shooting Brake X117 Facelift	X117	5	EU-MERCEDES-BENZ-CLA-X117-FACELIFT-WAGON-01	HIGH		READY
119509	119509	SUV	GLC X253	X253	5	EU-MERCEDES-BENZ-GLC-X253-AMG-SUV-01	HIGH		READY
119512	119512	Convertible	Abarth 124 Spider		2	EU-ABARTH-124-SPIDER-CONVERTIBLE-01	HIGH		READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-SUZUKI-VITARA-I-SUV-3D-01	3632	1630	1662	Auto-Data Suzuki Vitara 1.6 i 16V 3-door; Automobile-Catalog Suzuki Vitara 1.6i JLX 16V Metal Top	https://www.auto-data.net/en/suzuki-vitara-et-ta-1.6-i-16v-3-dr-97hp-16429;https://www.automobile-catalog.com/car/1997/3349625/suzuki_vitara_1_6i_jlx_se_16v_metal_top_estate.html
EU-SUZUKI-VITARA-I-SUV-5D-01	4030	1635	1700	Automobile-Catalog Suzuki Vitara 1.6i JLX 16V 5-Door	https://www.automobile-catalog.com/car/1997/3349655/suzuki_vitara_1_6i_jlx_16v_5-door.html
EU-MERCEDES-BENZ-CLA-C117-FACELIFT-COUPE-01	4640	1777	1432	Auto-Data Mercedes-Benz CLA C117 facelift CLA 220 4MATIC	https://www.auto-data.net/en/mercedes-benz-cla-coupe-c117-facelift-2016-cla-220-184hp-4matic-dct-23524
EU-DACIA-DUSTER-I-FACELIFT-SUV-01	4315	1822	1625	Auto-Data Dacia Duster facelift 1.2 TCe 125 4WD	https://www.auto-data.net/en/dacia-duster-facelift-2013-1.2-tce-125hp-4wd-22883
EU-RENAULT-CAPTUR-I-SUV-PREFL-01	4122	1778	1566	Auto-Data Renault Captur 1.2 TCe 120 EDC	https://www.auto-data.net/en/renault-captur-1.2-tce-120hp-edc-18169
EU-RENAULT-CAPTUR-I-SUV-FACELIFT-01	4122	1778	1556	Auto-Data Renault Captur facelift 1.2 TCe 120	https://www.auto-data.net/en/renault-captur-facelift-2017-1.2-tce-120hp-start-stop-edc-29779
EU-RENAULT-CLIO-IV-HATCHBACK-PREFL-01	4062	1732	1448	Auto-Data Renault Clio IV Phase I 1.2 TCe 120	https://www.auto-data.net/en/renault-clio-iv-phase-i-1.2-tce-120hp-gt-automatic-18203
EU-RENAULT-CLIO-IV-HATCHBACK-FACELIFT-01	4062	1731	1448	Auto-Data Renault Clio IV Phase II 1.2 Energy TCe 120	https://www.auto-data.net/en/renault-clio-iv-phase-ii-2016-1.2-energy-tce-120hp-s-s-25375
EU-RENAULT-CLIO-IV-GRANDTOUR-WAGON-PREFL-01	4267	1732	1445	Auto-Data Renault Clio IV Grandtour Phase I	https://www.auto-data.net/en/renault-clio-iv-grandtour-phase-i-generation-4122
EU-RENAULT-CLIO-IV-GRANDTOUR-WAGON-FACELIFT-01	4267	1732	1475	Auto-Data Renault Clio IV Grandtour Phase II	https://www.auto-data.net/en/renault-clio-iv-grandtour-phase-ii-2016-generation-5134
EU-MERCEDES-BENZ-CLA-X117-FACELIFT-WAGON-01	4640	1777	1435	Auto-Data Mercedes-Benz CLA Shooting Brake X117 facelift CLA 220 4MATIC	https://www.auto-data.net/en/mercedes-benz-cla-shooting-brake-x117-facelift-2016-cla-220-184hp-4matic-dct-23371
EU-MERCEDES-BENZ-GLC-X253-AMG-SUV-01	4656	1890	1639	Auto-Data Mercedes-Benz GLC X253 AMG GLC 43	https://www.auto-data.net/en/mercedes-benz-glc-suv-x253-amg-glc-43-367hp-4matic-g-tronic-24365
EU-ABARTH-124-SPIDER-CONVERTIBLE-01	4054	1740	1233	Auto-Data Abarth 124 Spider	https://www.auto-data.net/en/abarth-124-spider-generation-5004
```

## 下一步优先处理

1. 继续消除剩余 9 个 PENDING：L200、Sorento、Partner Tepee、Mascott、Navara、Master、Berlingo和两个 Mistral Ktype。
2. 优先处理可以通过明确驾驶室、门数或改款拆分消除的记录。
3. 随后集中处理 Transit、Jumpy、Traveller、Ducato、Sprinter 与 Cabstar 的轴距、车顶和驾驶室分支。

推进信号：CONTINUE

[1]: https://www.auto-data.net/en/suzuki-vitara-et-ta-1.6-i-16v-3-dr-97hp-16429 "Suzuki Vitara (ET,TA) 1.6 i 16V (3 dr) (97 Hp) | Technical specs, data, fuel consumption, Dimensions"
[2]: https://www.auto-data.net/en/renault-captur-1.2-tce-120hp-edc-18169 "Renault Captur 1.2 TCe (120 Hp) EDC | Technical specs, data, fuel consumption, Dimensions"


--- 发送 / 继续到 Round 4 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1-100_ktype_dimension_mapping_final.tsv
- all_1-100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 4 / 下一步 ---
## 更新点

* 闭合 `119149`、`119202`、`119329`、`119424`、`119432`，本轮消除 5 条 PENDING。
* Sorento II XM 改款车型外廓闭合为 `4685 × 1885 × 1745 mm`；输入动力版本存在市场差异，因此映射置信度保留为 MEDIUM。([汽车数据网][1])
* Partner Tepee 官方资料给出车长 `4384 mm`、不含后视镜宽度 `1810 mm`，标准无车顶杆高度 `1800 mm`。
* Berlingo Multispace 官方手册给出车长 `4380 mm`、不含后视镜宽度 `1810 mm`，标准无车顶附件高度 `1801 mm`。([citroeneuropass.com.au][2])
* Mistral Spyder 3.7 与 4.0 的版本专页均支持 `4500 × 1650 × 1300 mm`，其中宽度明确为不含后视镜口径，两个 Ktype 复用同一尺寸组。([汽车目录][3])

## 当前批次进度

* 已覆盖输入 Ktype：46 / 100
* READY 映射：48
* PENDING 映射：4
* 已确认尺寸组：38
* 剩余 PENDING：`119113`、`119207`、`119256`、`119278`
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
119149	119149	SUV	Sorento II Facelift	XM	5	EU-KIA-SORENTO-II-XM-FACELIFT-SUV-01	MEDIUM	输入明确为Sorento II XM；动力版本存在市场差异。	READY
119202	119202	MPV	Partner II Tepee Facelift		5	EU-PEUGEOT-PARTNER-II-TEPEE-FACELIFT-MPV-01	HIGH		READY
119329	119329	MPV	Berlingo II Multispace Facelift	B9	5	EU-CITROEN-BERLINGO-II-MULTISPACE-FACELIFT-MPV-01	HIGH		READY
119424	119424	Convertible	Mistral Spyder	AM109	2	EU-MASERATI-MISTRAL-SPYDER-CONVERTIBLE-01	HIGH		READY
119432	119432	Convertible	Mistral Spyder	AM109	2	EU-MASERATI-MISTRAL-SPYDER-CONVERTIBLE-01	HIGH		READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-KIA-SORENTO-II-XM-FACELIFT-SUV-01	4685	1885	1745	Auto-Data Kia Sorento II facelift 2012 generation	https://www.auto-data.net/en/kia-sorento-ii-facelift-2012-generation-4148
EU-PEUGEOT-PARTNER-II-TEPEE-FACELIFT-MPV-01	4384	1810	1800	Peugeot New Partner Tepee official brochure	https://www.charterspeugeot.com/wp-content/uploads/sites/15/2015/04/new-partner-tepee-brochure-pdf.pdf
EU-CITROEN-BERLINGO-II-MULTISPACE-FACELIFT-MPV-01	4380	1810	1801	Citroën Berlingo Multispace official handbook	https://www.citroeneuropass.com.au/i/VehicleManual/Berlingo.pdf
EU-MASERATI-MISTRAL-SPYDER-CONVERTIBLE-01	4500	1650	1300	Automobile-Catalog Maserati Mistral Spyder 3700; Automobile-Catalog Maserati Mistral Spyder 4000	https://www.automobile-catalog.com/car/1965/1443515/maserati_mistral_spyder_3700.html;https://www.automobile-catalog.com/car/1966/1443575/maserati_mistral_spyder_4000.html
```

## 下一步优先处理

1. 判定 `119113` L200 的具体驾驶室分支，并解决输入后驱与欧洲车型资料之间的市场边界。
2. 按载重代码、驾驶室和轴距解析 `119207` Mascott。
3. 确认 `119256` Navara D23 的 King Cab／Double Cab 分支。
4. 确认 `119278` Master III 底盘驾驶室的轴距与驾驶室分支；清零现有 PENDING 后继续处理第 47–100 个输入 Ktype。

推进信号：CONTINUE

[1]: https://www.auto-data.net/en/kia-sorento-ii-facelift-2012-generation-4148 "Kia Sorento II (facelift 2012) | Technical Specs, Fuel consumption, Dimensions"
[2]: https://www.citroeneuropass.com.au/i/VehicleManual/Berlingo.pdf?utm_source=chatgpt.com "Handbook
CITROËN
MULTISPACE
BERLINGO"
[3]: https://www.automobile-catalog.com/car/1965/1443515/maserati_mistral_spyder_3700.html?utm_source=chatgpt.com "1965 Maserati Mistral Spyder 3700 Specs Review (180 kW / 245 PS / 241 hp) (since mid-year 1965 for Europe )"


--- 发送 / 继续到 Round 5 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1-100_ktype_dimension_mapping_final.tsv
- all_1-100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 5 / 下一步 ---
## 更新点

* 新完成 8 个乘用车 Ktype：Mercedes-Benz C-Class W205 Sedan、S205 Wagon、C205 Coupe，以及 Volvo XC60 I Facelift。
* `119602`、`119603`、`119604`、`119605` 的普通 C205 Coupe 三维一致，统一复用标准 C205 Coupe 尺寸组；`119606` AMG C 43 因宽体车身及外廓不同，独立建组。([汽车数据网][1])
* `119516` 与 `119530` 分别闭合为 AMG C 43 W205 Sedan 和 S205 Wagon，不能因动力相同而共用尺寸组。([汽车数据网][2])
* `119578` 已闭合为 XC60 I 2013 Facelift 外廓。([汽车数据网][3])
* `119113`、`119256` 仍未修改：L200 同一 Ktype 涉及驾驶室及窄体/宽体配置差异；Navara 190 hp 资料存在高度范围，无法从输入确定单一高度，因此本轮未猜测建组。([汽车数据网][4])

## 当前批次进度

* 已覆盖输入 Ktype：54 / 100
* READY 映射：56
* PENDING 映射：4
* 已确认尺寸组：43
* 剩余 PENDING：`119113`、`119207`、`119256`、`119278`
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
119516	119516	Sedan	C-Class W205	W205	4	EU-MERCEDES-BENZ-C-CLASS-W205-AMG-SEDAN-01	HIGH		READY
119530	119530	Wagon	C-Class S205	S205	5	EU-MERCEDES-BENZ-C-CLASS-S205-AMG-WAGON-01	HIGH		READY
119578	119578	SUV	XC60 I Facelift		5	EU-VOLVO-XC60-I-FACELIFT-SUV-01	HIGH		READY
119602	119602	Coupe	C-Class Coupe C205	C205	2	EU-MERCEDES-BENZ-C-CLASS-C205-COUPE-01	HIGH		READY
119603	119603	Coupe	C-Class Coupe C205	C205	2	EU-MERCEDES-BENZ-C-CLASS-C205-COUPE-01	HIGH		READY
119604	119604	Coupe	C-Class Coupe C205	C205	2	EU-MERCEDES-BENZ-C-CLASS-C205-COUPE-01	HIGH		READY
119605	119605	Coupe	C-Class Coupe C205	C205	2	EU-MERCEDES-BENZ-C-CLASS-C205-COUPE-01	HIGH	生产区间跨越改款，但标准车身三维未变化。	READY
119606	119606	Coupe	C-Class Coupe C205 AMG	C205	2	EU-MERCEDES-BENZ-C-CLASS-C205-AMG-COUPE-01	HIGH	AMG宽体及保险杠外廓独立。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-MERCEDES-BENZ-C-CLASS-W205-AMG-SEDAN-01	4756	1839	1426	Auto-Data Mercedes-Benz C-Class W205 AMG C 43 V6 367	https://www.auto-data.net/en/mercedes-benz-c-class-w205-amg-c-43-v6-367hp-4matic-9g-tronic-25241
EU-MERCEDES-BENZ-C-CLASS-S205-AMG-WAGON-01	4771	1839	1441	Auto-Data Mercedes-Benz C-Class S205 AMG C 43 V6 367	https://www.auto-data.net/en/mercedes-benz-c-class-t-modell-s205-amg-c-43-v6-367hp-4matic-9g-tronic-24847
EU-VOLVO-XC60-I-FACELIFT-SUV-01	4644	1891	1713	Auto-Data Volvo XC60 I 2013 Facelift T5 AWD	https://www.auto-data.net/en/volvo-xc60-i-2013-facelift-2.0-t5-245hp-awd-automatic-23219
EU-MERCEDES-BENZ-C-CLASS-C205-COUPE-01	4686	1810	1405	Auto-Data Mercedes-Benz C-Class C205 C 220d 4MATIC; Auto-Data Mercedes-Benz C-Class C205 C 400 4MATIC	https://www.auto-data.net/en/mercedes-benz-c-class-coupe-c205-c-220d-170hp-4matic-9g-tronic-25817;https://www.auto-data.net/en/mercedes-benz-c-class-coupe-c205-c-400-333hp-4matic-9g-tronic-24848
EU-MERCEDES-BENZ-C-CLASS-C205-AMG-COUPE-01	4750	1877	1400	Auto-Data Mercedes-Benz C-Class C205 AMG C 43 V6 367	https://www.auto-data.net/en/mercedes-benz-c-class-coupe-c205-amg-c-43-v6-367hp-4matic-9g-tronic-24257
```

## 下一步优先处理

1. 继续消除 `119113` 与 `119256` 的驾驶室、宽体及高度配置分支。
2. 处理 `119207` Mascott 和 `119278` Master III 底盘驾驶室的轴距、单排/双排驾驶室边界。
3. 继续推进 Transit、Jumpy、Traveller、Ducato、Sprinter 和 Cabstar，优先按相同轴距、车顶及驾驶室批量聚类。

推进信号：CONTINUE

[1]: https://www.auto-data.net/en/mercedes-benz-c-class-coupe-c205-c-220d-170hp-4matic-9g-tronic-25817?utm_source=chatgpt.com "Mercedes-Benz C-class Coupe (C205) C 220d (170 Hp) ..."
[2]: https://www.auto-data.net/en/mercedes-benz-c-class-w205-amg-c-43-v6-367hp-4matic-9g-tronic-25241?utm_source=chatgpt.com "Mercedes-Benz C-class (W205) AMG C 43 V6 (367 Hp) ..."
[3]: https://www.auto-data.net/en/volvo-xc60-i-2013-facelift-2.0-t5-245hp-awd-automatic-23219?utm_source=chatgpt.com "Volvo XC60 I (2013 facelift) 2.0 T5 (245 Hp) AWD Automatic"
[4]: https://www.auto-data.net/en/mitsubishi-l200-v-double-cab-2.4d-154hp-4wd-34749 "Mitsubishi L200 V Double Cab 2.4d (154 Hp) 4WD | Technical specs, data, fuel consumption, Dimensions"


--- 发送 / 继续到 Round 6 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1-100_ktype_dimension_mapping_final.tsv
- all_1-100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 6 / 下一步 ---
## 更新点

* 完成 Citroën Jumpy III 五个动力 Ktype 的长度分支拆分。官方资料确认 Jumpy 提供 XS、M、XL 三种外廓，尺寸分别为 `4609×1920×1905`、`4959×1920×1895`、`5309×1920×1935 mm`；其中 BlueHDi 115 仅建立已确认的 XS、M 分支，其余本轮动力覆盖三种长度。
* 完成 Peugeot Traveller 四个动力 Ktype 的外廓拆分。BlueHDi 95 与 115 对应 Standard、Long；BlueHDi 150 与 180 对应 Compact、Standard、Long。尺寸和动力—车长组合均由同一份官方规格表闭合。
* 本轮新处理的多个动力 Ktype 直接复用 6 个已首次闭合的长度尺寸组，没有按发动机重复建组。
* 原有 4 条商用底盘／皮卡 PENDING 本轮未修改。

## 当前批次进度

* 已覆盖输入 Ktype：63 / 100
* READY 映射：80 行
* PENDING 映射：4 行
* 已确认尺寸组：49
* 剩余 PENDING：`119113`、`119207`、`119256`、`119278`
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
119484_xs	119484	Van	Jumpy III			EU-CITROEN-JUMPY-III-VAN-XS-01	HIGH	XS短轴物理外廓。	READY
119484_m	119484	Van	Jumpy III			EU-CITROEN-JUMPY-III-VAN-M-01	HIGH	M长轴短后悬物理外廓。	READY
119484_xl	119484	Van	Jumpy III			EU-CITROEN-JUMPY-III-VAN-XL-01	HIGH	XL长轴长后悬物理外廓。	READY
119485_xs	119485	Van	Jumpy III			EU-CITROEN-JUMPY-III-VAN-XS-01	HIGH	XS短轴物理外廓。	READY
119485_m	119485	Van	Jumpy III			EU-CITROEN-JUMPY-III-VAN-M-01	HIGH	M长轴短后悬物理外廓。	READY
119486_xs	119486	Van	Jumpy III			EU-CITROEN-JUMPY-III-VAN-XS-01	HIGH	XS短轴物理外廓。	READY
119486_m	119486	Van	Jumpy III			EU-CITROEN-JUMPY-III-VAN-M-01	HIGH	M长轴短后悬物理外廓。	READY
119486_xl	119486	Van	Jumpy III			EU-CITROEN-JUMPY-III-VAN-XL-01	HIGH	XL长轴长后悬物理外廓。	READY
119487_xs	119487	Van	Jumpy III			EU-CITROEN-JUMPY-III-VAN-XS-01	HIGH	XS短轴物理外廓。	READY
119487_m	119487	Van	Jumpy III			EU-CITROEN-JUMPY-III-VAN-M-01	HIGH	M长轴短后悬物理外廓。	READY
119487_xl	119487	Van	Jumpy III			EU-CITROEN-JUMPY-III-VAN-XL-01	HIGH	XL长轴长后悬物理外廓。	READY
119488_xs	119488	Van	Jumpy III			EU-CITROEN-JUMPY-III-VAN-XS-01	HIGH	XS短轴物理外廓。	READY
119488_m	119488	Van	Jumpy III			EU-CITROEN-JUMPY-III-VAN-M-01	HIGH	M长轴短后悬物理外廓。	READY
119488_xl	119488	Van	Jumpy III			EU-CITROEN-JUMPY-III-VAN-XL-01	HIGH	XL长轴长后悬物理外廓。	READY
119502_standard	119502	MPV	Traveller I			EU-PEUGEOT-TRAVELLER-I-MPV-STANDARD-01	HIGH	Standard长轴短后悬物理外廓。	READY
119502_long	119502	MPV	Traveller I			EU-PEUGEOT-TRAVELLER-I-MPV-LONG-01	HIGH	Long长轴长后悬物理外廓。	READY
119503_standard	119503	MPV	Traveller I			EU-PEUGEOT-TRAVELLER-I-MPV-STANDARD-01	HIGH	Standard长轴短后悬物理外廓。	READY
119503_long	119503	MPV	Traveller I			EU-PEUGEOT-TRAVELLER-I-MPV-LONG-01	HIGH	Long长轴长后悬物理外廓。	READY
119511_compact	119511	MPV	Traveller I			EU-PEUGEOT-TRAVELLER-I-MPV-COMPACT-01	HIGH	Compact短轴物理外廓。	READY
119511_standard	119511	MPV	Traveller I			EU-PEUGEOT-TRAVELLER-I-MPV-STANDARD-01	HIGH	Standard长轴短后悬物理外廓。	READY
119511_long	119511	MPV	Traveller I			EU-PEUGEOT-TRAVELLER-I-MPV-LONG-01	HIGH	Long长轴长后悬物理外廓。	READY
119513_compact	119513	MPV	Traveller I			EU-PEUGEOT-TRAVELLER-I-MPV-COMPACT-01	HIGH	Compact短轴物理外廓。	READY
119513_standard	119513	MPV	Traveller I			EU-PEUGEOT-TRAVELLER-I-MPV-STANDARD-01	HIGH	Standard长轴短后悬物理外廓。	READY
119513_long	119513	MPV	Traveller I			EU-PEUGEOT-TRAVELLER-I-MPV-LONG-01	HIGH	Long长轴长后悬物理外廓。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-CITROEN-JUMPY-III-VAN-XS-01	4609	1920	1905	Citroën Jumpy official catalogue	https://profesionales.citroen.cl/content/dam/citroen/chile/cat%C3%A1logos/Catalogo_Jumpy.pdf
EU-CITROEN-JUMPY-III-VAN-M-01	4959	1920	1895	Citroën Jumpy official catalogue	https://profesionales.citroen.cl/content/dam/citroen/chile/cat%C3%A1logos/Catalogo_Jumpy.pdf
EU-CITROEN-JUMPY-III-VAN-XL-01	5309	1920	1935	Citroën Jumpy official catalogue	https://profesionales.citroen.cl/content/dam/citroen/chile/cat%C3%A1logos/Catalogo_Jumpy.pdf
EU-PEUGEOT-TRAVELLER-I-MPV-COMPACT-01	4606	1920	1905	Peugeot Traveller official prices and specifications	https://www.charterspeugeot.com/wp-content/uploads/sites/15/2016/03/peugeot-traveller-prices-and-specifications-september-2017.pdf
EU-PEUGEOT-TRAVELLER-I-MPV-STANDARD-01	4956	1920	1890	Peugeot Traveller official prices and specifications	https://www.charterspeugeot.com/wp-content/uploads/sites/15/2016/03/peugeot-traveller-prices-and-specifications-september-2017.pdf
EU-PEUGEOT-TRAVELLER-I-MPV-LONG-01	5309	1920	1890	Peugeot Traveller official prices and specifications	https://www.charterspeugeot.com/wp-content/uploads/sites/15/2016/03/peugeot-traveller-prices-and-specifications-september-2017.pdf
```

## 下一步优先处理

1. 完整拆分 `119113` L200 与 `119256` Navara 的驾驶室外廓，优先清除两个皮卡 PENDING。
2. 解析 `119207` Mascott 与 `119278` Master III 底盘驾驶室的车身代码、轴距和单排／双排分支。
3. 继续批量处理 Transit V363、Ducato、Sprinter 与 Cabstar 的固定轴距及车顶组合。

推进信号：CONTINUE


--- 发送 / 继续到 Round 7 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1-100_ktype_dimension_mapping_final.tsv
- all_1-100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 7 / 下一步 ---
## 更新点

* `119113` 已闭合：厂商救援资料确认 `KJ0T` 为 L200 Double Cab；113 kW 手动版本采用窄体外廓 `5205 × 1785 × 1775 mm`。
* `119256` 已确认属于 Navara D23 Double Cab。官方规格显示 190 PS Double Cab 长 `5330 mm`、不含后视镜宽 `1850 mm`；因标准车身与原厂车顶杆车型高度分别为 `1810 mm` 和 `1840 mm`，拆成两个物理分支。([bendix.co.th][1])
* 剩余 PENDING 降至 `119207` Mascott 与 `119278` Master III 两条底盘驾驶室记录。

## 当前批次进度

* 已覆盖输入 Ktype：63 / 100
* READY 映射：83 行
* PENDING 映射：2 行
* 已确认尺寸组：52
* 剩余 PENDING：`119207`、`119278`
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
119113	119113	Pickup	L200 V	KJ0T	4	EU-MITSUBISHI-L200-V-DOUBLE-CAB-2WD-01	HIGH	KJ0T双排驾驶室窄体外廓。	READY
119256_standard	119256	Pickup	Navara D23	D23	4	EU-NISSAN-NAVARA-D23-DOUBLE-CAB-STANDARD-01	MEDIUM	Double Cab标准无车顶杆外廓。	READY
119256_roofrails	119256	Pickup	Navara D23	D23	4	EU-NISSAN-NAVARA-D23-DOUBLE-CAB-ROOFRAILS-01	MEDIUM	Double Cab原厂车顶杆外廓。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-MITSUBISHI-L200-V-DOUBLE-CAB-2WD-01	5205	1785	1775	Mitsubishi Motors L200 KJ0T official rescue sheet; Mitsubishi L200 official brochure	https://www.mitsubishi-motors.es/content/dam/mitsubishi-motors-es/es/rescate/Hoja_de_rescate_L200_KJ0T_Doble_cabina.pdf;https://www.cnp.sg/wp-content/uploads/2024/03/M.L200.Brochure.SG_.20.pdf
EU-NISSAN-NAVARA-D23-DOUBLE-CAB-STANDARD-01	5330	1850	1810	Nissan NP300 Navara official technical specifications	https://www.nissan-cdn.net/content/dam/Nissan/palestine/brochure/Nissan_NP300_Navara.pdf
EU-NISSAN-NAVARA-D23-DOUBLE-CAB-ROOFRAILS-01	5330	1850	1840	Nissan NP300 Navara official brochure and technical specifications	https://www.nissan-cdn.net/content/dam/Nissan/malta/brochures/NP300_NAVARA_2016_Brochure.pdf;https://www.nissan-cdn.net/content/dam/Nissan/palestine/brochure/Nissan_NP300_Navara.pdf
```

## 下一步优先处理

1. 完整拆分 `119207` Mascott 150.35 的轴距与单排／双排驾驶室外廓。
2. 按官方 FWD L2、L3 及驾驶室形式闭合 `119278` Master III，消除现有全部 PENDING。
3. 随后继续处理 Transit V363、Ducato、Sprinter 与 Cabstar 的长度、车顶和驾驶室组合。

推进信号：CONTINUE

[1]: https://www.bendix.co.th/catalogue/nissan/navara/navara-ute-d23-d23t/23-dci?id=119256&tab=Passenger&utm_source=chatgpt.com "NISSAN NAVARA Ute (D23, D23T) 2.3 dCi - Bendix Brakes"


--- 发送 / 继续到 Round 8 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1-100_ktype_dimension_mapping_final.tsv
- all_1-100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 8 / 下一步 ---
## 更新点

* `119278` 已按 Renault Master III 前驱底盘驾驶室完整拆分为单排 L2、单排 L3、双排 L2、双排 L3 四个物理分支。Ktype 覆盖 `EV0Y/HV0Y/UV0M/UV0Y/UV03`，官方车型表确认 130 hp 前驱发动机适用于上述四种底盘驾驶室配置。([bilstein.nl][1])
* 四个尺寸组均采用官方尺寸图中的不含后视镜宽度 `2070 mm`；含后视镜宽度 `2470 mm` 未落盘。
* `119207` 继续保持 PENDING。现有资料已确认 Ktype 同时覆盖单排与双排驾驶室，轴距范围包含多个分支，但尚未取得全部分支完整且同口径的长宽高，未猜测建组。([Typenscheinschweiz.ch][2])

## 当前批次进度

* 已覆盖输入 Ktype：63 / 100
* READY 映射：87 行
* PENDING 映射：1 行
* 已确认尺寸组：56
* 剩余 PENDING：`119207`
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
119278_sc_l2	119278	Pickup	Master III Phase II		2	EU-RENAULT-MASTER-III-CHASSIS-SINGLE-CAB-L2-FWD-01	MEDIUM	前驱单排驾驶室L2物理外廓。	READY
119278_sc_l3	119278	Pickup	Master III Phase II		2	EU-RENAULT-MASTER-III-CHASSIS-SINGLE-CAB-L3-FWD-01	MEDIUM	前驱单排驾驶室L3物理外廓。	READY
119278_dc_l2	119278	Pickup	Master III Phase II		4	EU-RENAULT-MASTER-III-CHASSIS-DOUBLE-CAB-L2-FWD-01	MEDIUM	前驱双排驾驶室L2物理外廓。	READY
119278_dc_l3	119278	Pickup	Master III Phase II		4	EU-RENAULT-MASTER-III-CHASSIS-DOUBLE-CAB-L3-FWD-01	MEDIUM	前驱双排驾驶室L3物理外廓。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-RENAULT-MASTER-III-CHASSIS-SINGLE-CAB-L2-FWD-01	5643	2070	2265	Renault Master official brochure	https://www.diacfa.com/wp-content/uploads/RENAULT_MASTER_ENG.pdf
EU-RENAULT-MASTER-III-CHASSIS-SINGLE-CAB-L3-FWD-01	6293	2070	2258	Renault Master official brochure	https://www.diacfa.com/wp-content/uploads/RENAULT_MASTER_ENG.pdf
EU-RENAULT-MASTER-III-CHASSIS-DOUBLE-CAB-L2-FWD-01	5643	2070	2275	Renault Master official brochure	https://www.diacfa.com/wp-content/uploads/RENAULT_MASTER_ENG.pdf
EU-RENAULT-MASTER-III-CHASSIS-DOUBLE-CAB-L3-FWD-01	6293	2070	2273	Renault Master official brochure	https://www.diacfa.com/wp-content/uploads/RENAULT_MASTER_ENG.pdf
```

## 下一步优先处理

1. 闭合 `119207` Mascott 150.35 的单排／双排驾驶室及多轴距完整尺寸分支，消除最后一条现有 PENDING。
2. 随后继续推进尚未覆盖的 Transit V363、Ducato、Sprinter 与 Cabstar Ktype，按驾驶室、长度和车顶组合批量复用尺寸组。

推进信号：CONTINUE

[1]: https://www.bilstein.nl/producten?bouwjaar=03%2F12&merk=RENAULT&model=MASTER+III+Platform%2FChassis+%28EV%2C+HV%2C+UV%29&sets=B+3&type=2.3+dCi+130+FWD&utm_source=chatgpt.com "Bilstein RENAULT MASTER III Platform/Chassis (EV, HV, UV ..."
[2]: https://typenscheinschweiz.ch/typenschein/auto/3RA809 "Typenschein 3RA809 - RENAULT Mascott 150.35 | Gratis PDF"


--- 发送 / 继续到 Round 9 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1-100_ktype_dimension_mapping_final.tsv
- all_1-100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 9 / 下一步 ---
## 更新点

* 完成 Ford Transit V363 厢式车 6 个 Ktype：`119467`、`119468`、`119470`、`119471`、`119472`、`119473`。
* 前驱版本按 L2H2、L2H3、L3H2、L3H3 拆分；后驱版本除上述四种外，增加 L4H3 单后轮与双后轮分支。不同驱动形式的官方最大车高存在差异，因此分别建立尺寸组；L4H3 单后轮与双后轮的不含后视镜宽度也不同。
* `119207` Mascott 150.35 仍保持 PENDING：现有资料确认其覆盖多轴距以及单排、双排驾驶室，但型式批准未提供各底盘分支完整固定外廓尺寸，暂不猜测建组。([Typenscheinschweiz.ch][1])

## 当前批次进度

* 已覆盖输入 Ktype：69 / 100
* READY 映射：117 行
* PENDING 映射：1 行
* 已确认尺寸组：66
* 剩余 PENDING：`119207`
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
119467_l2h2	119467	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L2H2-FWD-01	MEDIUM	L2H2前驱厢式车物理外廓。	READY
119467_l2h3	119467	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L2H3-FWD-01	MEDIUM	L2H3前驱厢式车物理外廓。	READY
119467_l3h2	119467	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L3H2-FWD-01	MEDIUM	L3H2前驱厢式车物理外廓。	READY
119467_l3h3	119467	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L3H3-FWD-01	MEDIUM	L3H3前驱厢式车物理外廓。	READY
119468_l2h2	119468	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L2H2-FWD-01	MEDIUM	L2H2前驱厢式车物理外廓。	READY
119468_l2h3	119468	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L2H3-FWD-01	MEDIUM	L2H3前驱厢式车物理外廓。	READY
119468_l3h2	119468	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L3H2-FWD-01	MEDIUM	L3H2前驱厢式车物理外廓。	READY
119468_l3h3	119468	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L3H3-FWD-01	MEDIUM	L3H3前驱厢式车物理外廓。	READY
119470_l2h2	119470	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L2H2-FWD-01	MEDIUM	L2H2前驱厢式车物理外廓。	READY
119470_l2h3	119470	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L2H3-FWD-01	MEDIUM	L2H3前驱厢式车物理外廓。	READY
119470_l3h2	119470	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L3H2-FWD-01	MEDIUM	L3H2前驱厢式车物理外廓。	READY
119470_l3h3	119470	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L3H3-FWD-01	MEDIUM	L3H3前驱厢式车物理外廓。	READY
119471_l2h2	119471	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L2H2-RWD-01	MEDIUM	L2H2后驱厢式车物理外廓。	READY
119471_l2h3	119471	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L2H3-RWD-01	MEDIUM	L2H3后驱厢式车物理外廓。	READY
119471_l3h2	119471	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L3H2-RWD-01	MEDIUM	L3H2后驱厢式车物理外廓。	READY
119471_l3h3	119471	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L3H3-RWD-01	MEDIUM	L3H3后驱厢式车物理外廓。	READY
119471_l4h3_srw	119471	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L4H3-RWD-SRW-01	MEDIUM	L4H3后驱单后轮物理外廓。	READY
119471_l4h3_drw	119471	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L4H3-RWD-DRW-01	MEDIUM	L4H3后驱双后轮物理外廓。	READY
119472_l2h2	119472	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L2H2-RWD-01	MEDIUM	L2H2后驱厢式车物理外廓。	READY
119472_l2h3	119472	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L2H3-RWD-01	MEDIUM	L2H3后驱厢式车物理外廓。	READY
119472_l3h2	119472	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L3H2-RWD-01	MEDIUM	L3H2后驱厢式车物理外廓。	READY
119472_l3h3	119472	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L3H3-RWD-01	MEDIUM	L3H3后驱厢式车物理外廓。	READY
119472_l4h3_srw	119472	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L4H3-RWD-SRW-01	MEDIUM	L4H3后驱单后轮物理外廓。	READY
119472_l4h3_drw	119472	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L4H3-RWD-DRW-01	MEDIUM	L4H3后驱双后轮物理外廓。	READY
119473_l2h2	119473	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L2H2-RWD-01	MEDIUM	L2H2后驱厢式车物理外廓。	READY
119473_l2h3	119473	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L2H3-RWD-01	MEDIUM	L2H3后驱厢式车物理外廓。	READY
119473_l3h2	119473	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L3H2-RWD-01	MEDIUM	L3H2后驱厢式车物理外廓。	READY
119473_l3h3	119473	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L3H3-RWD-01	MEDIUM	L3H3后驱厢式车物理外廓。	READY
119473_l4h3_srw	119473	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L4H3-RWD-SRW-01	MEDIUM	L4H3后驱单后轮物理外廓。	READY
119473_l4h3_drw	119473	Van	Transit V363			EU-FORD-TRANSIT-V363-VAN-L4H3-RWD-DRW-01	MEDIUM	L4H3后驱双后轮物理外廓。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-FORD-TRANSIT-V363-VAN-L2H2-FWD-01	5531	2059	2533	Ford Transit official brochure MY2025.5	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/cars/BRO-transit_van_25.5MY.pdf
EU-FORD-TRANSIT-V363-VAN-L2H3-FWD-01	5531	2059	2769	Ford Transit official brochure MY2025.5	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/cars/BRO-transit_van_25.5MY.pdf
EU-FORD-TRANSIT-V363-VAN-L3H2-FWD-01	5981	2059	2530	Ford Transit official brochure MY2025.5	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/cars/BRO-transit_van_25.5MY.pdf
EU-FORD-TRANSIT-V363-VAN-L3H3-FWD-01	5981	2059	2767	Ford Transit official brochure MY2025.5	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/cars/BRO-transit_van_25.5MY.pdf
EU-FORD-TRANSIT-V363-VAN-L2H2-RWD-01	5531	2059	2534	Ford Transit official brochure MY2025.5	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/cars/BRO-transit_van_25.5MY.pdf
EU-FORD-TRANSIT-V363-VAN-L2H3-RWD-01	5531	2059	2771	Ford Transit official brochure MY2025.5	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/cars/BRO-transit_van_25.5MY.pdf
EU-FORD-TRANSIT-V363-VAN-L3H2-RWD-01	5981	2059	2533	Ford Transit official brochure MY2025.5	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/cars/BRO-transit_van_25.5MY.pdf
EU-FORD-TRANSIT-V363-VAN-L3H3-RWD-01	5981	2059	2769	Ford Transit official brochure MY2025.5	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/cars/BRO-transit_van_25.5MY.pdf
EU-FORD-TRANSIT-V363-VAN-L4H3-RWD-SRW-01	6704	2059	2778	Ford Transit official brochure MY2025.5	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/cars/BRO-transit_van_25.5MY.pdf
EU-FORD-TRANSIT-V363-VAN-L4H3-RWD-DRW-01	6704	2126	2778	Ford Transit official brochure MY2025.5	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/cars/BRO-transit_van_25.5MY.pdf
```

## 下一步优先处理

1. 继续寻找 `119207` Mascott 150.35 各单排／双排驾驶室及轴距分支的完整同口径外廓尺寸。
2. 处理 Transit V363 底盘驾驶室 `119475–119480`，按单排／双排、轴距及后轮形式拆分。
3. 处理 Transit V363 Bus `119481–119483`，随后推进 Ducato、Sprinter 与 Cabstar。

推进信号：CONTINUE

[1]: https://typenscheinschweiz.ch/typenschein/auto/3RA809 "Typenschein 3RA809 - RENAULT Mascott 150.35 | Gratis PDF"


--- 发送 / 继续到 Round 10 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1-100_ktype_dimension_mapping_final.tsv
- all_1-100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 10 / 下一步 ---
## 更新点

* 完成 Transit V363 底盘驾驶室 `119475–119480`。按官方 2017 车型供应矩阵拆分单排／双排驾驶室、FWD／RWD、L1–L5 以及会改变车宽的 SRW／DRW 分支；三个动力版本复用相同物理尺寸组，未按发动机重复建组。([福特英国][1])
* 官方尺寸表分别给出单排与双排驾驶室的车长、最大高度及不含后视镜宽度；DRW 仅在对应高载重 RWD 分支中派生。([福特英国][1])
* `119207` Mascott 150.35 仍为唯一 PENDING。现有型式批准能够确认车型与底盘属性，但不能闭合各驾驶室、轴距分支的完整三维，因此本轮未创建猜测尺寸组。([Typenscheinschweiz.ch][2])

## 当前批次进度

* 已覆盖输入 Ktype：75 / 100
* READY 映射：152 行
* PENDING 映射：1 行
* 已确认尺寸组：84
* 剩余 PENDING：`119207`
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
119475_sc_l2	119475	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L2-FWD-01	MEDIUM	单排驾驶室L2前驱外廓。	READY
119476_sc_l2	119476	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L2-FWD-01	MEDIUM	单排驾驶室L2前驱外廓。	READY
119476_sc_l3	119476	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L3-FWD-01	MEDIUM	单排驾驶室L3前驱外廓。	READY
119476_sc_l4	119476	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L4-FWD-01	MEDIUM	单排驾驶室L4前驱外廓。	READY
119476_dc_l3	119476	Pickup	Transit V363		4	EU-FORD-TRANSIT-V363-CHASSIS-DOUBLE-CAB-L3-FWD-01	MEDIUM	双排驾驶室L3前驱外廓。	READY
119477_sc_l3	119477	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L3-FWD-01	MEDIUM	单排驾驶室L3前驱外廓。	READY
119477_sc_l4	119477	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L4-FWD-01	MEDIUM	单排驾驶室L4前驱外廓。	READY
119477_dc_l3	119477	Pickup	Transit V363		4	EU-FORD-TRANSIT-V363-CHASSIS-DOUBLE-CAB-L3-FWD-01	MEDIUM	双排驾驶室L3前驱外廓。	READY
119478_sc_l1	119478	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L1-RWD-SRW-01	MEDIUM	单排驾驶室L1后驱单后轮外廓。	READY
119478_sc_l2	119478	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L2-RWD-SRW-01	MEDIUM	单排驾驶室L2后驱单后轮外廓。	READY
119478_sc_l3	119478	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L3-RWD-SRW-01	MEDIUM	单排驾驶室L3后驱单后轮外廓。	READY
119478_sc_l4	119478	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L4-RWD-SRW-01	MEDIUM	单排驾驶室L4后驱单后轮外廓。	READY
119478_dc_l3	119478	Pickup	Transit V363		4	EU-FORD-TRANSIT-V363-CHASSIS-DOUBLE-CAB-L3-RWD-SRW-01	MEDIUM	双排驾驶室L3后驱单后轮外廓。	READY
119479_sc_l2_srw	119479	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L2-RWD-SRW-01	MEDIUM	单排驾驶室L2后驱单后轮外廓。	READY
119479_sc_l2_drw	119479	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L2-RWD-DRW-01	MEDIUM	单排驾驶室L2后驱双后轮外廓。	READY
119479_sc_l3_srw	119479	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L3-RWD-SRW-01	MEDIUM	单排驾驶室L3后驱单后轮外廓。	READY
119479_sc_l3_drw	119479	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L3-RWD-DRW-01	MEDIUM	单排驾驶室L3后驱双后轮外廓。	READY
119479_sc_l4	119479	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L4-RWD-SRW-01	MEDIUM	单排驾驶室L4后驱单后轮外廓。	READY
119479_sc_l5	119479	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L5-RWD-01	MEDIUM	单排驾驶室L5后驱外廓。	READY
119479_dc_l3	119479	Pickup	Transit V363		4	EU-FORD-TRANSIT-V363-CHASSIS-DOUBLE-CAB-L3-RWD-SRW-01	MEDIUM	双排驾驶室L3后驱单后轮外廓。	READY
119479_dc_l4	119479	Pickup	Transit V363		4	EU-FORD-TRANSIT-V363-CHASSIS-DOUBLE-CAB-L4-RWD-SRW-01	MEDIUM	双排驾驶室L4后驱单后轮外廓。	READY
119479_dc_l5	119479	Pickup	Transit V363		4	EU-FORD-TRANSIT-V363-CHASSIS-DOUBLE-CAB-L5-RWD-SRW-01	MEDIUM	双排驾驶室L5后驱单后轮外廓。	READY
119480_sc_l2_srw	119480	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L2-RWD-SRW-01	MEDIUM	单排驾驶室L2后驱单后轮外廓。	READY
119480_sc_l2_drw	119480	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L2-RWD-DRW-01	MEDIUM	单排驾驶室L2后驱双后轮外廓。	READY
119480_sc_l3_srw	119480	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L3-RWD-SRW-01	MEDIUM	单排驾驶室L3后驱单后轮外廓。	READY
119480_sc_l3_drw	119480	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L3-RWD-DRW-01	MEDIUM	单排驾驶室L3后驱双后轮外廓。	READY
119480_sc_l4_srw	119480	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L4-RWD-SRW-01	MEDIUM	单排驾驶室L4后驱单后轮外廓。	READY
119480_sc_l4_drw	119480	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L4-RWD-DRW-01	MEDIUM	单排驾驶室L4后驱双后轮外廓。	READY
119480_sc_l5	119480	Pickup	Transit V363		2	EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L5-RWD-01	MEDIUM	单排驾驶室L5后驱外廓。	READY
119480_dc_l3_srw	119480	Pickup	Transit V363		4	EU-FORD-TRANSIT-V363-CHASSIS-DOUBLE-CAB-L3-RWD-SRW-01	MEDIUM	双排驾驶室L3后驱单后轮外廓。	READY
119480_dc_l3_drw	119480	Pickup	Transit V363		4	EU-FORD-TRANSIT-V363-CHASSIS-DOUBLE-CAB-L3-RWD-DRW-01	MEDIUM	双排驾驶室L3后驱双后轮外廓。	READY
119480_dc_l4_srw	119480	Pickup	Transit V363		4	EU-FORD-TRANSIT-V363-CHASSIS-DOUBLE-CAB-L4-RWD-SRW-01	MEDIUM	双排驾驶室L4后驱单后轮外廓。	READY
119480_dc_l4_drw	119480	Pickup	Transit V363		4	EU-FORD-TRANSIT-V363-CHASSIS-DOUBLE-CAB-L4-RWD-DRW-01	MEDIUM	双排驾驶室L4后驱双后轮外廓。	READY
119480_dc_l5_srw	119480	Pickup	Transit V363		4	EU-FORD-TRANSIT-V363-CHASSIS-DOUBLE-CAB-L5-RWD-SRW-01	MEDIUM	双排驾驶室L5后驱单后轮外廓。	READY
119480_dc_l5_drw	119480	Pickup	Transit V363		4	EU-FORD-TRANSIT-V363-CHASSIS-DOUBLE-CAB-L5-RWD-DRW-01	MEDIUM	双排驾驶室L5后驱双后轮外廓。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L2-FWD-01	5572	2052	2194	Ford Transit Chassis Cab official brochure 2017	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/commercial-vehicles/BRO-Transit_Chassis_Cab.pdf
EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L3-FWD-01	6022	2052	2186	Ford Transit Chassis Cab official brochure 2017	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/commercial-vehicles/BRO-Transit_Chassis_Cab.pdf
EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L4-FWD-01	6579	2052	2186	Ford Transit Chassis Cab official brochure 2017	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/commercial-vehicles/BRO-Transit_Chassis_Cab.pdf
EU-FORD-TRANSIT-V363-CHASSIS-DOUBLE-CAB-L3-FWD-01	6022	2066	2218	Ford Transit Chassis Cab official brochure 2017	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/commercial-vehicles/BRO-Transit_Chassis_Cab.pdf
EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L1-RWD-SRW-01	5205	2052	2215	Ford Transit Chassis Cab official brochure 2017	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/commercial-vehicles/BRO-Transit_Chassis_Cab.pdf
EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L2-RWD-SRW-01	5572	2052	2210	Ford Transit Chassis Cab official brochure 2017	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/commercial-vehicles/BRO-Transit_Chassis_Cab.pdf
EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L2-RWD-DRW-01	5572	2111	2210	Ford Transit Chassis Cab official brochure 2017	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/commercial-vehicles/BRO-Transit_Chassis_Cab.pdf
EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L3-RWD-SRW-01	6022	2052	2202	Ford Transit Chassis Cab official brochure 2017	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/commercial-vehicles/BRO-Transit_Chassis_Cab.pdf
EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L3-RWD-DRW-01	6022	2111	2202	Ford Transit Chassis Cab official brochure 2017	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/commercial-vehicles/BRO-Transit_Chassis_Cab.pdf
EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L4-RWD-SRW-01	6579	2052	2214	Ford Transit Chassis Cab official brochure 2017	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/commercial-vehicles/BRO-Transit_Chassis_Cab.pdf
EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L4-RWD-DRW-01	6579	2111	2214	Ford Transit Chassis Cab official brochure 2017	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/commercial-vehicles/BRO-Transit_Chassis_Cab.pdf
EU-FORD-TRANSIT-V363-CHASSIS-SINGLE-CAB-L5-RWD-01	7577	2066	2206	Ford Transit Chassis Cab official brochure 2017	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/commercial-vehicles/BRO-Transit_Chassis_Cab.pdf
EU-FORD-TRANSIT-V363-CHASSIS-DOUBLE-CAB-L3-RWD-SRW-01	6022	2066	2218	Ford Transit Chassis Cab official brochure 2017	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/commercial-vehicles/BRO-Transit_Chassis_Cab.pdf
EU-FORD-TRANSIT-V363-CHASSIS-DOUBLE-CAB-L3-RWD-DRW-01	6022	2111	2218	Ford Transit Chassis Cab official brochure 2017	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/commercial-vehicles/BRO-Transit_Chassis_Cab.pdf
EU-FORD-TRANSIT-V363-CHASSIS-DOUBLE-CAB-L4-RWD-SRW-01	6404	2066	2220	Ford Transit Chassis Cab official brochure 2017	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/commercial-vehicles/BRO-Transit_Chassis_Cab.pdf
EU-FORD-TRANSIT-V363-CHASSIS-DOUBLE-CAB-L4-RWD-DRW-01	6404	2111	2220	Ford Transit Chassis Cab official brochure 2017	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/commercial-vehicles/BRO-Transit_Chassis_Cab.pdf
EU-FORD-TRANSIT-V363-CHASSIS-DOUBLE-CAB-L5-RWD-SRW-01	7394	2066	2211	Ford Transit Chassis Cab official brochure 2017	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/commercial-vehicles/BRO-Transit_Chassis_Cab.pdf
EU-FORD-TRANSIT-V363-CHASSIS-DOUBLE-CAB-L5-RWD-DRW-01	7394	2111	2211	Ford Transit Chassis Cab official brochure 2017	https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/commercial-vehicles/BRO-Transit_Chassis_Cab.pdf
```

## 下一步优先处理

1. 继续闭合 `119207` Mascott 150.35，优先寻找覆盖单排／双排驾驶室及全部轴距的同口径官方尺寸表。
2. 处理 Transit V363 Bus `119481–119483`，按 Kombi 的长度、车顶和驱动分支建组。
3. 随后推进 Ducato、Sprinter 与 Cabstar，优先批量复用相同轴距和车身配置。

推进信号：CONTINUE

[1]: https://www.ford.co.uk/content/dam/guxeu/uk/documents/brochures/commercial-vehicles/BRO-Transit_Chassis_Cab.pdf?utm_source=chatgpt.com "TRANSIT CHASSIS CABS"
[2]: https://typenscheinschweiz.ch/typenschein/auto/3RA809?utm_source=chatgpt.com "Typenschein 3RA809 - RENAULT Mascott 150.35 | Gratis PDF"


--- 发送 / 继续到 Round 11 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1-100_ktype_dimension_mapping_final.tsv
- all_1-100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 11 / 下一步 ---
## 更新点

* 完成 Transit V363 Bus `119481–119483`。三个 Ktype 分别对应 105、130、170 hp 前驱 Bus，均按 L2H2、L2H3、L3H2、L3H3 四种物理外廓拆分。([Meyer Motoren][1])
* Ford 官方 Kombi 车型矩阵确认前驱 Bus 覆盖 L2/L3 与 H2/H3 组合；`WidthMM` 统一采用不含后视镜的 `2059 mm`。`HeightMM` 按任务的最大外部高度口径，取官方对应高度区间上限。
* `119207` Mascott 150.35 仍为唯一 PENDING。现有型式资料能够确认双排驾驶室、门数与轴距信息，但仍不能闭合该 Ktype 所覆盖全部底盘分支的完整长宽高。([Motoro][2])

## 当前批次进度

* 已覆盖输入 Ktype：78 / 100
* READY 映射：164 行
* PENDING 映射：1 行
* 已确认尺寸组：88
* 剩余 PENDING：`119207`
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
119481_l2h2	119481	MPV	Transit V363			EU-FORD-TRANSIT-V363-BUS-L2H2-FWD-01	MEDIUM	L2H2前驱Kombi物理外廓。	READY
119481_l2h3	119481	MPV	Transit V363			EU-FORD-TRANSIT-V363-BUS-L2H3-FWD-01	MEDIUM	L2H3前驱Kombi物理外廓。	READY
119481_l3h2	119481	MPV	Transit V363			EU-FORD-TRANSIT-V363-BUS-L3H2-FWD-01	MEDIUM	L3H2前驱Kombi物理外廓。	READY
119481_l3h3	119481	MPV	Transit V363			EU-FORD-TRANSIT-V363-BUS-L3H3-FWD-01	MEDIUM	L3H3前驱Kombi物理外廓。	READY
119482_l2h2	119482	MPV	Transit V363			EU-FORD-TRANSIT-V363-BUS-L2H2-FWD-01	MEDIUM	L2H2前驱Kombi物理外廓。	READY
119482_l2h3	119482	MPV	Transit V363			EU-FORD-TRANSIT-V363-BUS-L2H3-FWD-01	MEDIUM	L2H3前驱Kombi物理外廓。	READY
119482_l3h2	119482	MPV	Transit V363			EU-FORD-TRANSIT-V363-BUS-L3H2-FWD-01	MEDIUM	L3H2前驱Kombi物理外廓。	READY
119482_l3h3	119482	MPV	Transit V363			EU-FORD-TRANSIT-V363-BUS-L3H3-FWD-01	MEDIUM	L3H3前驱Kombi物理外廓。	READY
119483_l2h2	119483	MPV	Transit V363			EU-FORD-TRANSIT-V363-BUS-L2H2-FWD-01	MEDIUM	L2H2前驱Kombi物理外廓。	READY
119483_l2h3	119483	MPV	Transit V363			EU-FORD-TRANSIT-V363-BUS-L2H3-FWD-01	MEDIUM	L2H3前驱Kombi物理外廓。	READY
119483_l3h2	119483	MPV	Transit V363			EU-FORD-TRANSIT-V363-BUS-L3H2-FWD-01	MEDIUM	L3H2前驱Kombi物理外廓。	READY
119483_l3h3	119483	MPV	Transit V363			EU-FORD-TRANSIT-V363-BUS-L3H3-FWD-01	MEDIUM	L3H3前驱Kombi物理外廓。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-FORD-TRANSIT-V363-BUS-L2H2-FWD-01	5531	2059	2536	Ford Transit Van/Kombi official brochure 20.5MY	https://www.ford.nl/content/dam/guxeu/nl/documents/brochures/commercial-vehicles/BRO-ford_nieuwe_transit_gesloten_bestelauto_kombi.pdf
EU-FORD-TRANSIT-V363-BUS-L2H3-FWD-01	5531	2059	2781	Ford Transit Van/Kombi official brochure 20.5MY	https://www.ford.nl/content/dam/guxeu/nl/documents/brochures/commercial-vehicles/BRO-ford_nieuwe_transit_gesloten_bestelauto_kombi.pdf
EU-FORD-TRANSIT-V363-BUS-L3H2-FWD-01	5981	2059	2532	Ford Transit Van/Kombi official brochure 20.5MY	https://www.ford.nl/content/dam/guxeu/nl/documents/brochures/commercial-vehicles/BRO-ford_nieuwe_transit_gesloten_bestelauto_kombi.pdf
EU-FORD-TRANSIT-V363-BUS-L3H3-FWD-01	5981	2059	2771	Ford Transit Van/Kombi official brochure 20.5MY	https://www.ford.nl/content/dam/guxeu/nl/documents/brochures/commercial-vehicles/BRO-ford_nieuwe_transit_gesloten_bestelauto_kombi.pdf
```

## 下一步优先处理

1. 闭合 `119207` Mascott 150.35 的单排／双排驾驶室和轴距分支，消除最后一条现有 PENDING。
2. 推进 Fiat Ducato `119515`、`119519`、`119521`、`119523` 的厢式车及底盘驾驶室组合。
3. 集中处理 Mercedes-Benz Sprinter `119573–119581` 和 Nissan Cabstar `119556–119597`。

推进信号：CONTINUE

[1]: https://www.meyermotoren.de/fahrzeuge/119481/ford/transit_v363_bus_fad_fbd_/2_0_ecoblue_119481?utm_source=chatgpt.com "2.0 EcoBlue | Transit V363 Bus (FAD, FBD) | Ford | Herstellerübersicht | Meyer Motoren"
[2]: https://motoro.ch/en/fiche-technique/renault/mascott-150-35?utm_source=chatgpt.com "RENAULT Mascott 150.35 specifications — Features | Motoro"


--- 发送 / 继续到 Round 12 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1-100_ktype_dimension_mapping_final.tsv
- all_1-100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 12 / 下一步 ---
## 更新点

* 完成 Fiat Ducato 厢式车 `119515` 与 `119523`。2016 年 Fiat Professional 官方车型表确认 150 hp 与 180 hp 均覆盖 MH1、MH2、LH2、LH3、LXH2、LXH3 六种外廓；对应长宽高采用 X290 官方技术尺寸表。两个动力 Ktype 复用同一组六个尺寸组，没有按发动机重复建组。
* `119207` Mascott 本轮未修改，仍为唯一已输出的 PENDING。

## 当前批次进度

* 已覆盖输入 Ktype：80 / 100
* READY 映射：176 行
* PENDING 映射：1 行
* 已确认尺寸组：94
* 剩余 PENDING：`119207`
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
119515_mh1	119515	Van	Ducato III X290	X290		EU-FIAT-DUCATO-X290-VAN-MH1-01	HIGH	MH1中轴低顶物理外廓。	READY
119515_mh2	119515	Van	Ducato III X290	X290		EU-FIAT-DUCATO-X290-VAN-MH2-01	HIGH	MH2中轴高顶物理外廓。	READY
119515_lh2	119515	Van	Ducato III X290	X290		EU-FIAT-DUCATO-X290-VAN-LH2-01	HIGH	LH2长轴高顶物理外廓。	READY
119515_lh3	119515	Van	Ducato III X290	X290		EU-FIAT-DUCATO-X290-VAN-LH3-01	HIGH	LH3长轴超高顶物理外廓。	READY
119515_lxh2	119515	Van	Ducato III X290	X290		EU-FIAT-DUCATO-X290-VAN-LXH2-01	HIGH	LXH2加长车身高顶物理外廓。	READY
119515_lxh3	119515	Van	Ducato III X290	X290		EU-FIAT-DUCATO-X290-VAN-LXH3-01	HIGH	LXH3加长车身超高顶物理外廓。	READY
119523_mh1	119523	Van	Ducato III X290	X290		EU-FIAT-DUCATO-X290-VAN-MH1-01	HIGH	MH1中轴低顶物理外廓。	READY
119523_mh2	119523	Van	Ducato III X290	X290		EU-FIAT-DUCATO-X290-VAN-MH2-01	HIGH	MH2中轴高顶物理外廓。	READY
119523_lh2	119523	Van	Ducato III X290	X290		EU-FIAT-DUCATO-X290-VAN-LH2-01	HIGH	LH2长轴高顶物理外廓。	READY
119523_lh3	119523	Van	Ducato III X290	X290		EU-FIAT-DUCATO-X290-VAN-LH3-01	HIGH	LH3长轴超高顶物理外廓。	READY
119523_lxh2	119523	Van	Ducato III X290	X290		EU-FIAT-DUCATO-X290-VAN-LXH2-01	HIGH	LXH2加长车身高顶物理外廓。	READY
119523_lxh3	119523	Van	Ducato III X290	X290		EU-FIAT-DUCATO-X290-VAN-LXH3-01	HIGH	LXH3加长车身超高顶物理外廓。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-FIAT-DUCATO-X290-VAN-MH1-01	5413	2050	2254	Fiat Professional New Ducato official technical information 2014; Fiat Professional Range official price list December 2016	https://www.media.stellantis.com/uploads/uk/UK/2014/FIAT_PROF/PRICES/Fiat_Professional_NEW%20DUCATO%202014_Price_List_APR_2014.pdf;https://www.media.stellantis.com/uploads/uk/UK/2016/FIAT_Professional/Price_Lists/Fiat_Professional_Range_Price_List_DEC_2016.pdf
EU-FIAT-DUCATO-X290-VAN-MH2-01	5413	2050	2524	Fiat Professional New Ducato official technical information 2014; Fiat Professional Range official price list December 2016	https://www.media.stellantis.com/uploads/uk/UK/2014/FIAT_PROF/PRICES/Fiat_Professional_NEW%20DUCATO%202014_Price_List_APR_2014.pdf;https://www.media.stellantis.com/uploads/uk/UK/2016/FIAT_Professional/Price_Lists/Fiat_Professional_Range_Price_List_DEC_2016.pdf
EU-FIAT-DUCATO-X290-VAN-LH2-01	5998	2050	2524	Fiat Professional New Ducato official technical information 2014; Fiat Professional Range official price list December 2016	https://www.media.stellantis.com/uploads/uk/UK/2014/FIAT_PROF/PRICES/Fiat_Professional_NEW%20DUCATO%202014_Price_List_APR_2014.pdf;https://www.media.stellantis.com/uploads/uk/UK/2016/FIAT_Professional/Price_Lists/Fiat_Professional_Range_Price_List_DEC_2016.pdf
EU-FIAT-DUCATO-X290-VAN-LH3-01	5998	2050	2764	Fiat Professional New Ducato official technical information 2014; Fiat Professional Range official price list December 2016	https://www.media.stellantis.com/uploads/uk/UK/2014/FIAT_PROF/PRICES/Fiat_Professional_NEW%20DUCATO%202014_Price_List_APR_2014.pdf;https://www.media.stellantis.com/uploads/uk/UK/2016/FIAT_Professional/Price_Lists/Fiat_Professional_Range_Price_List_DEC_2016.pdf
EU-FIAT-DUCATO-X290-VAN-LXH2-01	6363	2050	2524	Fiat Professional New Ducato official technical information 2014; Fiat Professional Range official price list December 2016	https://www.media.stellantis.com/uploads/uk/UK/2014/FIAT_PROF/PRICES/Fiat_Professional_NEW%20DUCATO%202014_Price_List_APR_2014.pdf;https://www.media.stellantis.com/uploads/uk/UK/2016/FIAT_Professional/Price_Lists/Fiat_Professional_Range_Price_List_DEC_2016.pdf
EU-FIAT-DUCATO-X290-VAN-LXH3-01	6363	2050	2764	Fiat Professional New Ducato official technical information 2014; Fiat Professional Range official price list December 2016	https://www.media.stellantis.com/uploads/uk/UK/2014/FIAT_PROF/PRICES/Fiat_Professional_NEW%20DUCATO%202014_Price_List_APR_2014.pdf;https://www.media.stellantis.com/uploads/uk/UK/2016/FIAT_Professional/Price_Lists/Fiat_Professional_Range_Price_List_DEC_2016.pdf
```

## 下一步优先处理

1. 闭合 `119207` Mascott 150.35 的单排／双排驾驶室和全部轴距分支。
2. 处理 Ducato 底盘驾驶室 `119519`、`119521`，补齐单排与双排驾驶室的完整外廓尺寸。
3. 集中处理 Sprinter `119573–119581`，随后推进剩余 Nissan Cabstar Ktype。

推进信号：CONTINUE


--- 发送 / 继续到 Round 13 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1-100_ktype_dimension_mapping_final.tsv
- all_1-100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 13 / 下一步 ---
## 更新点

* 完成 Fiat Ducato X290 底盘驾驶室 `119519` 与 `119521`。150 hp、180 hp 均按单排 MH1、MLH1、LH1、LXH1，以及双排 LH1、LXH1 六种物理外廓拆分；两个动力 Ktype 复用同一组六个尺寸组。2016 年官方车型表确认这些发动机与车身组合，官方技术规格表提供对应的不含后视镜宽度及完整三维。([Stellantis Media][1])
* `119207` Mascott 150.35 本轮未修改。官方瑞士型式资料确认该 Ktype 涉及单排和双排底盘，并覆盖多个轴距，但长宽高字段为空，仍不足以闭合全部物理分支。([Typenscheinschweiz.ch][2])

## 当前批次进度

* 已覆盖输入 Ktype：82 / 100
* READY 映射：188 行
* PENDING 映射：1 行
* 已确认尺寸组：100
* 剩余 PENDING：`119207`
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
119519_sc_mh1	119519	Pickup	Ducato III X290	X290	2	EU-FIAT-DUCATO-X290-CHASSIS-SINGLE-CAB-MH1-01	HIGH	单排驾驶室MH1物理外廓。	READY
119519_sc_mlh1	119519	Pickup	Ducato III X290	X290	2	EU-FIAT-DUCATO-X290-CHASSIS-SINGLE-CAB-MLH1-01	HIGH	单排驾驶室MLH1物理外廓。	READY
119519_sc_lh1	119519	Pickup	Ducato III X290	X290	2	EU-FIAT-DUCATO-X290-CHASSIS-SINGLE-CAB-LH1-01	HIGH	单排驾驶室LH1物理外廓。	READY
119519_sc_lxh1	119519	Pickup	Ducato III X290	X290	2	EU-FIAT-DUCATO-X290-CHASSIS-SINGLE-CAB-LXH1-01	HIGH	单排驾驶室LXH1物理外廓。	READY
119519_dc_lh1	119519	Pickup	Ducato III X290	X290	4	EU-FIAT-DUCATO-X290-CHASSIS-DOUBLE-CAB-LH1-01	HIGH	双排驾驶室LH1物理外廓。	READY
119519_dc_lxh1	119519	Pickup	Ducato III X290	X290	4	EU-FIAT-DUCATO-X290-CHASSIS-DOUBLE-CAB-LXH1-01	HIGH	双排驾驶室LXH1物理外廓。	READY
119521_sc_mh1	119521	Pickup	Ducato III X290	X290	2	EU-FIAT-DUCATO-X290-CHASSIS-SINGLE-CAB-MH1-01	HIGH	单排驾驶室MH1物理外廓。	READY
119521_sc_mlh1	119521	Pickup	Ducato III X290	X290	2	EU-FIAT-DUCATO-X290-CHASSIS-SINGLE-CAB-MLH1-01	HIGH	单排驾驶室MLH1物理外廓。	READY
119521_sc_lh1	119521	Pickup	Ducato III X290	X290	2	EU-FIAT-DUCATO-X290-CHASSIS-SINGLE-CAB-LH1-01	HIGH	单排驾驶室LH1物理外廓。	READY
119521_sc_lxh1	119521	Pickup	Ducato III X290	X290	2	EU-FIAT-DUCATO-X290-CHASSIS-SINGLE-CAB-LXH1-01	HIGH	单排驾驶室LXH1物理外廓。	READY
119521_dc_lh1	119521	Pickup	Ducato III X290	X290	4	EU-FIAT-DUCATO-X290-CHASSIS-DOUBLE-CAB-LH1-01	HIGH	双排驾驶室LH1物理外廓。	READY
119521_dc_lxh1	119521	Pickup	Ducato III X290	X290	4	EU-FIAT-DUCATO-X290-CHASSIS-DOUBLE-CAB-LXH1-01	HIGH	双排驾驶室LXH1物理外廓。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-FIAT-DUCATO-X290-CHASSIS-SINGLE-CAB-MH1-01	5358	2050	2254	Fiat Professional New Ducato chassis cab official technical specifications 2014; Fiat Professional Range official price list December 2016	https://www.media.stellantis.com/uploads/em/2014/schede_tecniche/DucatoTrasfConv_CT_ENG.pdf;https://www.media.stellantis.com/uploads/uk/UK/2016/FIAT_Professional/Price_Lists/Fiat_Professional_Range_Price_List_DEC_2016.pdf
EU-FIAT-DUCATO-X290-CHASSIS-SINGLE-CAB-MLH1-01	5708	2050	2254	Fiat Professional New Ducato chassis cab official technical specifications 2014; Fiat Professional Range official price list December 2016	https://www.media.stellantis.com/uploads/em/2014/schede_tecniche/DucatoTrasfConv_CT_ENG.pdf;https://www.media.stellantis.com/uploads/uk/UK/2016/FIAT_Professional/Price_Lists/Fiat_Professional_Range_Price_List_DEC_2016.pdf
EU-FIAT-DUCATO-X290-CHASSIS-SINGLE-CAB-LH1-01	5943	2050	2254	Fiat Professional New Ducato chassis cab official technical specifications 2014; Fiat Professional Range official price list December 2016	https://www.media.stellantis.com/uploads/em/2014/schede_tecniche/DucatoTrasfConv_CT_ENG.pdf;https://www.media.stellantis.com/uploads/uk/UK/2016/FIAT_Professional/Price_Lists/Fiat_Professional_Range_Price_List_DEC_2016.pdf
EU-FIAT-DUCATO-X290-CHASSIS-SINGLE-CAB-LXH1-01	6308	2050	2254	Fiat Professional New Ducato chassis cab official technical specifications 2014; Fiat Professional Range official price list December 2016	https://www.media.stellantis.com/uploads/em/2014/schede_tecniche/DucatoTrasfConv_CT_ENG.pdf;https://www.media.stellantis.com/uploads/uk/UK/2016/FIAT_Professional/Price_Lists/Fiat_Professional_Range_Price_List_DEC_2016.pdf
EU-FIAT-DUCATO-X290-CHASSIS-DOUBLE-CAB-LH1-01	5943	2050	2254	Fiat Professional New Ducato chassis crew cab official technical specifications 2014; Fiat Professional Range official price list December 2016	https://www.media.stellantis.com/uploads/em/2014/schede_tecniche/DucatoTrasfConv_CT_ENG.pdf;https://www.media.stellantis.com/uploads/uk/UK/2016/FIAT_Professional/Price_Lists/Fiat_Professional_Range_Price_List_DEC_2016.pdf
EU-FIAT-DUCATO-X290-CHASSIS-DOUBLE-CAB-LXH1-01	6308	2050	2254	Fiat Professional New Ducato chassis crew cab official technical specifications 2014; Fiat Professional Range official price list December 2016	https://www.media.stellantis.com/uploads/em/2014/schede_tecniche/DucatoTrasfConv_CT_ENG.pdf;https://www.media.stellantis.com/uploads/uk/UK/2016/FIAT_Professional/Price_Lists/Fiat_Professional_Range_Price_List_DEC_2016.pdf
```

## 下一步优先处理

1. 继续闭合 `119207` Mascott 150.35 的单排／双排驾驶室及完整轴距分支。
2. 集中处理 Sprinter `119573–119581` 的 Bus、Van 与底盘驾驶室外廓。
3. 推进 Nissan Cabstar `119556–119597`，按代际、驾驶室和轴距集中建组。
4. 补齐剩余尚未覆盖的乘用车记录，优先使用既有尺寸组。

推进信号：CONTINUE

[1]: https://www.media.stellantis.com/uploads/uk/UK/2016/FIAT_Professional/Price_Lists/Fiat_Professional_Range_Price_List_DEC_2016.pdf?utm_source=chatgpt.com "FIAT PROFESSIONAL RANGE"
[2]: https://typenscheinschweiz.ch/typenschein/auto/3RA809?utm_source=chatgpt.com "Typenschein 3RA809 - RENAULT Mascott 150.35 | Gratis PDF"


--- 发送 / 继续到 Round 14 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1-100_ktype_dimension_mapping_final.tsv
- all_1-100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 14 / 下一步 ---
## 更新点

* 完成 Sprinter 3-T Bus `119573`、`119574`。车型代码 `906.711/906.713` 对应 W906 Compact 与 Standard 车身，分别按标准顶和高顶拆成四种外廓；两个动力 Ktype 复用同一组尺寸。([www.valeoservice.com][1])
* 完成 Sprinter 3-T Van `119576`、`119579`。车型代码 `906.611/906.613` 对应 Compact 与 Standard 厢式车，拆分为 Compact 标准顶/高顶，以及 Standard 标准顶/高顶/超高顶五种外廓。([Autodoc24][2])
* 所有宽度均采用官方尺寸图中的不含后视镜宽度 `1993 mm`；`2425/2426 mm` 的含后视镜宽度未落盘。([yumpu.com][3])
* `119207` Mascott 150.35 本轮未修改，仍为唯一 PENDING。

## 当前批次进度

* 已覆盖输入 Ktype：86 / 100
* READY 映射：206 行
* PENDING 映射：1 行
* 已确认尺寸组：109
* 剩余 PENDING：`119207`
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
119573_compact_stdroof	119573	MPV	Sprinter II W906	906.711		EU-MERCEDES-BENZ-SPRINTER-W906-BUS-COMPACT-STANDARD-ROOF-01	HIGH	Compact标准顶客车外廓。	READY
119573_compact_highroof	119573	MPV	Sprinter II W906	906.711		EU-MERCEDES-BENZ-SPRINTER-W906-BUS-COMPACT-HIGH-ROOF-01	HIGH	Compact高顶客车外廓。	READY
119573_standard_stdroof	119573	MPV	Sprinter II W906	906.713		EU-MERCEDES-BENZ-SPRINTER-W906-BUS-STANDARD-STANDARD-ROOF-01	HIGH	Standard标准顶客车外廓。	READY
119573_standard_highroof	119573	MPV	Sprinter II W906	906.713		EU-MERCEDES-BENZ-SPRINTER-W906-BUS-STANDARD-HIGH-ROOF-01	HIGH	Standard高顶客车外廓。	READY
119574_compact_stdroof	119574	MPV	Sprinter II W906	906.711		EU-MERCEDES-BENZ-SPRINTER-W906-BUS-COMPACT-STANDARD-ROOF-01	HIGH	Compact标准顶客车外廓。	READY
119574_compact_highroof	119574	MPV	Sprinter II W906	906.711		EU-MERCEDES-BENZ-SPRINTER-W906-BUS-COMPACT-HIGH-ROOF-01	HIGH	Compact高顶客车外廓。	READY
119574_standard_stdroof	119574	MPV	Sprinter II W906	906.713		EU-MERCEDES-BENZ-SPRINTER-W906-BUS-STANDARD-STANDARD-ROOF-01	HIGH	Standard标准顶客车外廓。	READY
119574_standard_highroof	119574	MPV	Sprinter II W906	906.713		EU-MERCEDES-BENZ-SPRINTER-W906-BUS-STANDARD-HIGH-ROOF-01	HIGH	Standard高顶客车外廓。	READY
119576_compact_stdroof	119576	Van	Sprinter II W906	906.611		EU-MERCEDES-BENZ-SPRINTER-W906-VAN-COMPACT-STANDARD-ROOF-01	HIGH	Compact标准顶厢式车外廓。	READY
119576_compact_highroof	119576	Van	Sprinter II W906	906.611		EU-MERCEDES-BENZ-SPRINTER-W906-VAN-COMPACT-HIGH-ROOF-01	HIGH	Compact高顶厢式车外廓。	READY
119576_standard_stdroof	119576	Van	Sprinter II W906	906.613		EU-MERCEDES-BENZ-SPRINTER-W906-VAN-STANDARD-STANDARD-ROOF-01	HIGH	Standard标准顶厢式车外廓。	READY
119576_standard_highroof	119576	Van	Sprinter II W906	906.613		EU-MERCEDES-BENZ-SPRINTER-W906-VAN-STANDARD-HIGH-ROOF-01	HIGH	Standard高顶厢式车外廓。	READY
119576_standard_superhighroof	119576	Van	Sprinter II W906	906.613		EU-MERCEDES-BENZ-SPRINTER-W906-VAN-STANDARD-SUPER-HIGH-ROOF-01	HIGH	Standard超高顶厢式车外廓。	READY
119579_compact_stdroof	119579	Van	Sprinter II W906	906.611		EU-MERCEDES-BENZ-SPRINTER-W906-VAN-COMPACT-STANDARD-ROOF-01	HIGH	Compact标准顶厢式车外廓。	READY
119579_compact_highroof	119579	Van	Sprinter II W906	906.611		EU-MERCEDES-BENZ-SPRINTER-W906-VAN-COMPACT-HIGH-ROOF-01	HIGH	Compact高顶厢式车外廓。	READY
119579_standard_stdroof	119579	Van	Sprinter II W906	906.613		EU-MERCEDES-BENZ-SPRINTER-W906-VAN-STANDARD-STANDARD-ROOF-01	HIGH	Standard标准顶厢式车外廓。	READY
119579_standard_highroof	119579	Van	Sprinter II W906	906.613		EU-MERCEDES-BENZ-SPRINTER-W906-VAN-STANDARD-HIGH-ROOF-01	HIGH	Standard高顶厢式车外廓。	READY
119579_standard_superhighroof	119579	Van	Sprinter II W906	906.613		EU-MERCEDES-BENZ-SPRINTER-W906-VAN-STANDARD-SUPER-HIGH-ROOF-01	HIGH	Standard超高顶厢式车外廓。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-MERCEDES-BENZ-SPRINTER-W906-BUS-COMPACT-STANDARD-ROOF-01	5245	1993	2415	Mercedes-Benz Sprinter Crewbus official dimensions and weights	https://www.yumpu.com/en/document/view/29030113/dimensions-and-weights-pdf-xxxx-kb
EU-MERCEDES-BENZ-SPRINTER-W906-BUS-COMPACT-HIGH-ROOF-01	5245	1993	2705	Mercedes-Benz Sprinter Crewbus official dimensions and weights	https://www.yumpu.com/en/document/view/29030113/dimensions-and-weights-pdf-xxxx-kb
EU-MERCEDES-BENZ-SPRINTER-W906-BUS-STANDARD-STANDARD-ROOF-01	5910	1993	2435	Mercedes-Benz Sprinter Crewbus official dimensions and weights	https://www.yumpu.com/en/document/view/29030113/dimensions-and-weights-pdf-xxxx-kb
EU-MERCEDES-BENZ-SPRINTER-W906-BUS-STANDARD-HIGH-ROOF-01	5910	1993	2720	Mercedes-Benz Sprinter Crewbus official dimensions and weights	https://www.yumpu.com/en/document/view/29030113/dimensions-and-weights-pdf-xxxx-kb
EU-MERCEDES-BENZ-SPRINTER-W906-VAN-COMPACT-STANDARD-ROOF-01	5245	1993	2435	Mercedes-Benz Sprinter Panel Van official brochure	https://xr793.com/wp-content/uploads/2022/12/2011-Mercedes-Benz-Sprinter-Panel-Van-UK.pdf
EU-MERCEDES-BENZ-SPRINTER-W906-VAN-COMPACT-HIGH-ROOF-01	5245	1993	2720	Mercedes-Benz Sprinter Panel Van official brochure	https://xr793.com/wp-content/uploads/2022/12/2011-Mercedes-Benz-Sprinter-Panel-Van-UK.pdf
EU-MERCEDES-BENZ-SPRINTER-W906-VAN-STANDARD-STANDARD-ROOF-01	5910	1993	2530	Mercedes-Benz Sprinter Panel Van official brochure	https://xr793.com/wp-content/uploads/2022/12/2011-Mercedes-Benz-Sprinter-Panel-Van-UK.pdf
EU-MERCEDES-BENZ-SPRINTER-W906-VAN-STANDARD-HIGH-ROOF-01	5910	1993	2820	Mercedes-Benz Sprinter Panel Van official brochure	https://xr793.com/wp-content/uploads/2022/12/2011-Mercedes-Benz-Sprinter-Panel-Van-UK.pdf
EU-MERCEDES-BENZ-SPRINTER-W906-VAN-STANDARD-SUPER-HIGH-ROOF-01	5910	1993	3050	Mercedes-Benz Sprinter Panel Van official brochure	https://xr793.com/wp-content/uploads/2022/12/2011-Mercedes-Benz-Sprinter-Panel-Van-UK.pdf
```

## 下一步优先处理

1. 闭合 `119207` Mascott 150.35 的单排／双排驾驶室和轴距分支。
2. 处理 Sprinter 底盘驾驶室 `119580`、`119581`，按 `906.111/906.113/906.211/906.213` 的驾驶室及轴距分支建组。
3. 集中处理剩余 Nissan Cabstar `119556–119597`，补齐全部尚未覆盖 Ktype。

推进信号：CONTINUE

[1]: https://www.valeoservice.com/techassist/vehicle/P-119573?country=GB&utm_source=chatgpt.com "Parts MERCEDES-BENZ SPRINTER 3-t Bus (B906)"
[2]: https://www.autodoc24.fr/spares/mercedes-benz/sprinter/sprinter-3-t-box-906/119579-214-cdi-906-611-906-613?utm_source=chatgpt.com "Parts Mercedes Sprinter 3t Van 214 CDI 2.1 143 hp Diesel 2016"
[3]: https://www.yumpu.com/en/document/view/29030113/dimensions-and-weights-pdf-xxxx-kb "Dimensions and weights (PDF, x.xxx KB)"


--- 发送 / 继续到 Round 15 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1-100_ktype_dimension_mapping_final.tsv
- all_1-100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 15 / 下一步 ---
## 更新点

* 完成 Sprinter 3-T 底盘驾驶室 `119580`、`119581`。两个动力 Ktype 均覆盖 `906.111`、`906.113`、`906.211`、`906.213`，按单排／双排驾驶室及 3250／3665 mm 轴距拆分为四种物理外廓。官方车身制造指南确认车身代码和 `5305/5870 mm` 车长，技术规格确认 `1990 mm` 不含后视镜宽度及 `2355 mm` 高度。([DIY Sprinter][1])
* `119207` 本轮未修改，仍是唯一 PENDING。

## 当前批次进度

* 已覆盖输入 Ktype：88 / 100
* READY 映射：214 行
* PENDING 映射：1 行
* 已确认尺寸组：113
* 剩余未覆盖 Ktype：12 个 Nissan Cabstar Ktype
* 剩余 PENDING：`119207`
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
119580_sc_swb	119580	Pickup	Sprinter II W906	906.111	2	EU-MERCEDES-BENZ-SPRINTER-W906-CHASSIS-SINGLE-CAB-SWB-01	MEDIUM	单排驾驶室3250毫米轴距外廓。	READY
119580_sc_mwb	119580	Pickup	Sprinter II W906	906.113	2	EU-MERCEDES-BENZ-SPRINTER-W906-CHASSIS-SINGLE-CAB-MWB-01	MEDIUM	单排驾驶室3665毫米轴距外廓。	READY
119580_dc_swb	119580	Pickup	Sprinter II W906	906.211	4	EU-MERCEDES-BENZ-SPRINTER-W906-CHASSIS-DOUBLE-CAB-SWB-01	MEDIUM	双排驾驶室3250毫米轴距外廓。	READY
119580_dc_mwb	119580	Pickup	Sprinter II W906	906.213	4	EU-MERCEDES-BENZ-SPRINTER-W906-CHASSIS-DOUBLE-CAB-MWB-01	MEDIUM	双排驾驶室3665毫米轴距外廓。	READY
119581_sc_swb	119581	Pickup	Sprinter II W906	906.111	2	EU-MERCEDES-BENZ-SPRINTER-W906-CHASSIS-SINGLE-CAB-SWB-01	MEDIUM	单排驾驶室3250毫米轴距外廓。	READY
119581_sc_mwb	119581	Pickup	Sprinter II W906	906.113	2	EU-MERCEDES-BENZ-SPRINTER-W906-CHASSIS-SINGLE-CAB-MWB-01	MEDIUM	单排驾驶室3665毫米轴距外廓。	READY
119581_dc_swb	119581	Pickup	Sprinter II W906	906.211	4	EU-MERCEDES-BENZ-SPRINTER-W906-CHASSIS-DOUBLE-CAB-SWB-01	MEDIUM	双排驾驶室3250毫米轴距外廓。	READY
119581_dc_mwb	119581	Pickup	Sprinter II W906	906.213	4	EU-MERCEDES-BENZ-SPRINTER-W906-CHASSIS-DOUBLE-CAB-MWB-01	MEDIUM	双排驾驶室3665毫米轴距外廓。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-MERCEDES-BENZ-SPRINTER-W906-CHASSIS-SINGLE-CAB-SWB-01	5305	1990	2355	Mercedes-Benz Sprinter Model Series 906 official body/equipment mounting directives; AutoScout24 Mercedes-Benz Sprinter technical data	https://diysprinter.co.uk/reference/UK-body-builders-arl_sprinterbm906_uk.pdf;https://www.autoscout24.de/auto/technische-daten/mercedes-benz/sprinter/216-cdi-bluetec-sprinter-906-111-blueefficiency-2009-2018-transporter-diesel/
EU-MERCEDES-BENZ-SPRINTER-W906-CHASSIS-SINGLE-CAB-MWB-01	5870	1990	2355	Mercedes-Benz Sprinter Model Series 906 official body/equipment mounting directives; Autogidas Mercedes-Benz Sprinter 906.113 technical data	https://diysprinter.co.uk/reference/UK-body-builders-arl_sprinterbm906_uk.pdf;https://autogidas.lt/en/auto-katalogas/mercedes-benz/sprinter/216-cdi-906.113-2009-2013-k79517
EU-MERCEDES-BENZ-SPRINTER-W906-CHASSIS-DOUBLE-CAB-SWB-01	5305	1990	2355	Mercedes-Benz Sprinter Model Series 906 official body/equipment mounting directives; AutoScout24 Mercedes-Benz Sprinter technical data	https://diysprinter.co.uk/reference/UK-body-builders-arl_sprinterbm906_uk.pdf;https://www.autoscout24.de/auto/technische-daten/mercedes-benz/sprinter/216-cdi-bluetec-sprinter-906-111-blueefficiency-2009-2018-transporter-diesel/
EU-MERCEDES-BENZ-SPRINTER-W906-CHASSIS-DOUBLE-CAB-MWB-01	5870	1990	2355	Mercedes-Benz Sprinter Model Series 906 official body/equipment mounting directives; Autogidas Mercedes-Benz Sprinter 906.113 technical data	https://diysprinter.co.uk/reference/UK-body-builders-arl_sprinterbm906_uk.pdf;https://autogidas.lt/en/auto-katalogas/mercedes-benz/sprinter/216-cdi-906.113-2009-2013-k79517
```

## 下一步优先处理

1. 闭合 `119207` Mascott 150.35 的单排／双排驾驶室及轴距分支。
2. 集中处理第一代 Nissan Cabstar `119556–119571`，按发动机无关的驾驶室和轴距外廓聚类。
3. 处理后期 Cabstar `119585–119597`，按载重代码、驾驶室和轴距批量复用尺寸组。

推进信号：CONTINUE

[1]: https://diysprinter.co.uk/reference/UK-body-builders-arl_sprinterbm906_uk.pdf?utm_source=chatgpt.com "Body/Equipment Mounting Directives for Sprinter Model ..."


--- 发送 / 继续到 Round 16 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1-100_ktype_dimension_mapping_final.tsv
- all_1-100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 16 / 下一步 ---
## 更新点

* `119207` 已从单一基础 PENDING 拆为双排驾驶室的 `3630`、`4130`、`4630 mm` 三个轴距分支。瑞士型式批准确认该版本为四门双排驾驶室，轴距覆盖 `3630–4630 mm`；历史车型目录进一步确认三种双排驾驶室轴距。由于现有尺寸页未明确声明 `2093 mm` 是否为不含后视镜宽度，本轮不创建尺寸组。([Typenscheinschweiz.ch][1])
* 已补齐此前尚未落盘的 12 个 Nissan Cabstar Ktype PENDING 行，当前 100 个输入 Ktype 均已至少出现在映射表中。
* `119556–119571` 已确认属于 Cabstar F22 底盘系列；`119585–119597` 属于 Cabstar E 的 TL0/VL0 范围。由于各 Ktype 的轴距、驾驶室及完整三维尚未闭合，本轮不创建猜测性尺寸组。([KMotoShop][2])

## 当前批次进度

* 已覆盖输入 Ktype：100 / 100
* READY 映射：214 行
* PENDING 映射：15 行
* 已确认尺寸组：113
* 当前所有输入 Ktype 均已有映射行，但尚有 Mascott 3 个物理分支和 Cabstar 12 个 Ktype 未闭合。
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
119207_dc_3630	119207	Pickup	Mascott II		4		MEDIUM	双排驾驶室3630毫米轴距分支；不含后视镜宽度口径尚未闭合。	PENDING: 完整三维及无后视镜宽度口径未闭合
119207_dc_4130	119207	Pickup	Mascott II		4		MEDIUM	双排驾驶室4130毫米轴距分支；不含后视镜宽度口径尚未闭合。	PENDING: 完整三维及无后视镜宽度口径未闭合
119207_dc_4630	119207	Pickup	Mascott II		4		MEDIUM	双排驾驶室4630毫米轴距分支；不含后视镜宽度口径尚未闭合。	PENDING: 完整三维及无后视镜宽度口径未闭合
119556	119556	Pickup	Cabstar F22	F22	2		MEDIUM	F22底盘驾驶室；轴距及完整外廓分支尚未闭合。	PENDING: 轴距与完整三维未闭合
119560	119560	Pickup	Cabstar F22	F22	2		MEDIUM	F22底盘驾驶室；轴距及完整外廓分支尚未闭合。	PENDING: 轴距与完整三维未闭合
119563	119563	Pickup	Cabstar F22	F22	2		MEDIUM	F22底盘驾驶室；轴距及完整外廓分支尚未闭合。	PENDING: 轴距与完整三维未闭合
119566	119566	Pickup	Cabstar F22	F22	2		MEDIUM	F22底盘驾驶室；轴距及完整外廓分支尚未闭合。	PENDING: 轴距与完整三维未闭合
119567	119567	Pickup	Cabstar F22	F22	2		MEDIUM	F22底盘驾驶室；轴距及完整外廓分支尚未闭合。	PENDING: 轴距与完整三维未闭合
119570	119570	Pickup	Cabstar F22	F22	2		MEDIUM	F22底盘驾驶室；轴距及完整外廓分支尚未闭合。	PENDING: 轴距与完整三维未闭合
119571	119571	Pickup	Cabstar F22	F22	2		MEDIUM	F22底盘驾驶室；轴距及完整外廓分支尚未闭合。	PENDING: 轴距与完整三维未闭合
119585	119585	Pickup	Cabstar E		2		LOW	TL0/VL0底盘范围；具体轴距和物理外廓分支尚未闭合。	PENDING: 车身代码、轴距与完整三维未闭合
119587	119587	Pickup	Cabstar E		2		LOW	TL0/VL0底盘范围；输入包含多个载重及轴距版本。	PENDING: 载重版本、轴距与完整三维未闭合
119589	119589	Pickup	Cabstar E		2		LOW	TL0/VL0底盘范围；输入包含35和45载重版本。	PENDING: 载重版本、轴距与完整三维未闭合
119591	119591	Pickup	Cabstar E		2		LOW	TL0/VL0底盘范围；输入包含35和45载重版本。	PENDING: 载重版本、轴距与完整三维未闭合
119597	119597	Pickup	Cabstar E		2		LOW	TL0/VL0底盘范围；输入包含35和45载重版本。	PENDING: 载重版本、轴距与完整三维未闭合
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

无

## 下一步优先处理

1. 获取 Mascott II 双排驾驶室三种轴距明确标注不含后视镜宽度的技术尺寸表，闭合 `119207` 三个分支。
2. 优先闭合 Cabstar F22 的轴距和驾驶室共用外廓，一次解决 `119556–119571` 七个 Ktype。
3. 再处理 Cabstar E TL0/VL0 的载重代码与轴距矩阵，批量解决 `119585–119597`。

推进信号：CONTINUE

[1]: https://typenscheinschweiz.ch/typenschein/auto/3RA809 "Typenschein 3RA809 - RENAULT Mascott 150.35 | Gratis PDF"
[2]: https://www.kmotorshop.com/en/article-list/list/car/119556?utm_source=chatgpt.com "Spare parts NISSAN CABSTAR (F22, H40) 2.5 TD (F22)"


--- 发送 / 继续到 Round 17 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1-100_ktype_dimension_mapping_final.tsv
- all_1-100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 17 / 下一步 ---
## 更新点

* Renault Trucks 2004 年官方车身制造指南确认 Mascott 双排驾驶室确有 `3630`、`4130`、`4630 mm` 三种轴距，因此保留 `119207` 的三个派生分支；该指南同时明确，具体车型的精确外廓必须以对应 1:20 车身图或型式批准报告为准。目前尚未取得这三张图中的完整长宽高与不含后视镜宽度，暂不能建组。([scribd.com][1])
* Cabstar E 的现有规格资料出现同代车型宽度 `1800 mm` 与 `2100 mm` 两种口径，且页面没有明确说明是否包含车身上装或后视镜；按统一宽度规则，本轮不采用任一数值建组。([autoscout24.fr][2])
* 本轮没有满足 READY 条件的新映射，也没有首次闭合的新尺寸组。

## 当前批次进度

* 输入 Ktype 覆盖：100 / 100
* READY 映射：214 行
* PENDING 映射：15 行
* 已确认尺寸组：113
* 待闭合：Mascott 3 个轴距分支、Cabstar F22 7 个 Ktype、Cabstar E 5 个 Ktype
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

无

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

无

## 下一步优先处理

1. 按 Mascott 官方图号体系查找双排驾驶室 `3630/4130/4630` 三张 1:20 车身图，闭合完整外廓和不含后视镜宽度。
2. 查找 Cabstar F22 1982–1992 年原厂销售手册或车身制造图，集中解决 7 个共用底盘 Ktype。
3. 查找 Cabstar E TL0/VL0 1998–2006 年原厂底盘尺寸矩阵，区分单排／双排、轴距和上装宽度，避免采用二手规格页的冲突尺寸。

推进信号：CONTINUE

[1]: https://www.scribd.com/document/726709779/364-4-AN-MASCOTT "Renault Mascott Bodywork Fitting Guide | PDF | Truck | Vehicles"
[2]: https://www.autoscout24.fr/voiture/caracteristiques-techniques/nissan/cabstar/cabstar-35-13-route-se-autres-diesel-2953/ "Nissan CABSTAR 35.13 ROUTE SE | Autres | Diesel | 2004-2006 - Spécifications techniques"


--- 发送 / 继续到 Round 18 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1-100_ktype_dimension_mapping_final.tsv
- all_1-100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 18 / 下一步 ---
## 更新点

* 已闭合 Cabstar E 的 5 个 Ktype：`119585`、`119587`、`119589`、`119591`、`119597`。政府车型目录确认了 `/1`、`/2`、`/3` 轴距版本以及部分车型的双排驾驶室 `/2`、`/3` 分支。([sede.gobiernodecanarias.org][1])
* 三种轴距对应的底盘外廓为：

  * 2400 mm：`4569 × 1800 × 2053 mm`
  * 2900 mm：`5369 × 1800 × 2053 mm`
  * 3400 mm：`6169 × 1800 × 2053 mm`。([autocasion.com][2])
* 双排驾驶室 2900 mm、3400 mm 版本分别同样为 `5369 × 1800 × 2053 mm` 和 `6169 × 1800 × 2053 mm`。虽然三维相同，因驾驶室物理外廓不同，仍独立建立尺寸组。([autocasion.com][3])
* 规格页将 `1800 mm` 列为整车宽度，并将外后视镜独立列为车外装备；据此按无后视镜车身宽度落盘。([autocasion.com][2])

## 当前批次进度

* 输入 Ktype 覆盖：100 / 100
* READY 映射：234 行
* PENDING 映射：10 行
* 已确认尺寸组：118
* 剩余 PENDING：Mascott 3 个轴距分支、Cabstar F22 7 个 Ktype
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
119585_sc_2400	119585	Pickup	Cabstar E	TL0	2	EU-NISSAN-CABSTAR-E-CHASSIS-SINGLE-CAB-2400-01	MEDIUM	单排驾驶室2400毫米轴距物理分支。	READY
119585_sc_2900	119585	Pickup	Cabstar E	TL0	2	EU-NISSAN-CABSTAR-E-CHASSIS-SINGLE-CAB-2900-01	MEDIUM	单排驾驶室2900毫米轴距物理分支。	READY
119587_sc_2400	119587	Pickup	Cabstar E	TL0	2	EU-NISSAN-CABSTAR-E-CHASSIS-SINGLE-CAB-2400-01	MEDIUM	单排驾驶室2400毫米轴距物理分支。	READY
119587_sc_2900	119587	Pickup	Cabstar E	TL0	2	EU-NISSAN-CABSTAR-E-CHASSIS-SINGLE-CAB-2900-01	MEDIUM	单排驾驶室2900毫米轴距物理分支。	READY
119587_sc_3400	119587	Pickup	Cabstar E	TL0	2	EU-NISSAN-CABSTAR-E-CHASSIS-SINGLE-CAB-3400-01	MEDIUM	单排驾驶室3400毫米轴距物理分支。	READY
119589_sc_2400	119589	Pickup	Cabstar E	TL0	2	EU-NISSAN-CABSTAR-E-CHASSIS-SINGLE-CAB-2400-01	MEDIUM	单排驾驶室2400毫米轴距物理分支。	READY
119589_sc_2900	119589	Pickup	Cabstar E	TL0	2	EU-NISSAN-CABSTAR-E-CHASSIS-SINGLE-CAB-2900-01	MEDIUM	单排驾驶室2900毫米轴距物理分支。	READY
119589_sc_3400	119589	Pickup	Cabstar E	TL0	2	EU-NISSAN-CABSTAR-E-CHASSIS-SINGLE-CAB-3400-01	MEDIUM	单排驾驶室3400毫米轴距物理分支。	READY
119589_dc_2900	119589	Pickup	Cabstar E	TL0	4	EU-NISSAN-CABSTAR-E-CHASSIS-DOUBLE-CAB-2900-01	MEDIUM	双排驾驶室2900毫米轴距物理分支。	READY
119589_dc_3400	119589	Pickup	Cabstar E	TL0	4	EU-NISSAN-CABSTAR-E-CHASSIS-DOUBLE-CAB-3400-01	MEDIUM	双排驾驶室3400毫米轴距物理分支。	READY
119591_sc_2400	119591	Pickup	Cabstar E	TL0	2	EU-NISSAN-CABSTAR-E-CHASSIS-SINGLE-CAB-2400-01	MEDIUM	单排驾驶室2400毫米轴距物理分支。	READY
119591_sc_2900	119591	Pickup	Cabstar E	TL0	2	EU-NISSAN-CABSTAR-E-CHASSIS-SINGLE-CAB-2900-01	MEDIUM	单排驾驶室2900毫米轴距物理分支。	READY
119591_sc_3400	119591	Pickup	Cabstar E	TL0	2	EU-NISSAN-CABSTAR-E-CHASSIS-SINGLE-CAB-3400-01	MEDIUM	单排驾驶室3400毫米轴距物理分支。	READY
119591_dc_2900	119591	Pickup	Cabstar E	TL0	4	EU-NISSAN-CABSTAR-E-CHASSIS-DOUBLE-CAB-2900-01	MEDIUM	双排驾驶室2900毫米轴距物理分支。	READY
119591_dc_3400	119591	Pickup	Cabstar E	TL0	4	EU-NISSAN-CABSTAR-E-CHASSIS-DOUBLE-CAB-3400-01	MEDIUM	双排驾驶室3400毫米轴距物理分支。	READY
119597_sc_2400	119597	Pickup	Cabstar E	TL0	2	EU-NISSAN-CABSTAR-E-CHASSIS-SINGLE-CAB-2400-01	MEDIUM	单排驾驶室2400毫米轴距物理分支。	READY
119597_sc_2900	119597	Pickup	Cabstar E	TL0	2	EU-NISSAN-CABSTAR-E-CHASSIS-SINGLE-CAB-2900-01	MEDIUM	单排驾驶室2900毫米轴距物理分支。	READY
119597_sc_3400	119597	Pickup	Cabstar E	TL0	2	EU-NISSAN-CABSTAR-E-CHASSIS-SINGLE-CAB-3400-01	MEDIUM	单排驾驶室3400毫米轴距物理分支。	READY
119597_dc_2900	119597	Pickup	Cabstar E	TL0	4	EU-NISSAN-CABSTAR-E-CHASSIS-DOUBLE-CAB-2900-01	MEDIUM	双排驾驶室2900毫米轴距物理分支。	READY
119597_dc_3400	119597	Pickup	Cabstar E	TL0	4	EU-NISSAN-CABSTAR-E-CHASSIS-DOUBLE-CAB-3400-01	MEDIUM	双排驾驶室3400毫米轴距物理分支。	READY
```

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-NISSAN-CABSTAR-E-CHASSIS-SINGLE-CAB-2400-01	4569	1800	2053	Autocasion Nissan Cabstar-E 120.35/1 technical specifications; Gobierno de Canarias Cabstar-E historical variant table	https://www.autocasion.com/marcas/nissan/cabstar-industrial/cabstar-e-120-35-1-2-puertas-24085;https://sede.gobiernodecanarias.org/boc/boc-a-2024-259-4403.pdf
EU-NISSAN-CABSTAR-E-CHASSIS-SINGLE-CAB-2900-01	5369	1800	2053	Autocasion Nissan Cabstar-E 120.35/2 technical specifications; Gobierno de Canarias Cabstar-E historical variant table	https://www.autocasion.com/marcas/nissan/cabstar-industrial/cabstar-e-120-35-2-2-puertas-24087;https://sede.gobiernodecanarias.org/boc/boc-a-2024-259-4403.pdf
EU-NISSAN-CABSTAR-E-CHASSIS-SINGLE-CAB-3400-01	6169	1800	2053	Autocasion Nissan Cabstar-E 120.35/3 technical specifications; Gobierno de Canarias Cabstar-E historical variant table	https://www.autocasion.com/marcas/nissan/cabstar-industrial/cabstar-e-120-35-3-2-puertas-24090;https://sede.gobiernodecanarias.org/boc/boc-a-2024-259-4403.pdf
EU-NISSAN-CABSTAR-E-CHASSIS-DOUBLE-CAB-2900-01	5369	1800	2053	Autocasion Nissan Cabstar-E 120.35/2 Double Cab technical specifications; Gobierno de Canarias Cabstar-E historical variant table	https://www.autocasion.com/marcas/nissan/cabstar-industrial/cabstar-e-120-35-2-doble-cabina-4-puertas-24089;https://sede.gobiernodecanarias.org/boc/boc-a-2024-259-4403.pdf
EU-NISSAN-CABSTAR-E-CHASSIS-DOUBLE-CAB-3400-01	6169	1800	2053	Autocasion Nissan Cabstar-E 120.35/3 Double Cab technical specifications; Gobierno de Canarias Cabstar-E historical variant table	https://www.autocasion.com/marcas/nissan/cabstar-industrial/cabstar-e-120-35-3-doble-cabina-4-puertas-24092;https://sede.gobiernodecanarias.org/boc/boc-a-2024-259-4403.pdf
```

## 下一步优先处理

1. 闭合 Cabstar F22 `119556–119571` 的短轴／长轴、低床／高床物理分支及无后视镜宽度。
2. 获取 Mascott 双排驾驶室 `3630/4130/4630 mm` 三个轴距对应的官方 1:20 车身图，闭合最后三个 Mascott 分支。
3. PENDING 清零后立即执行一次机械检查并输出两张最终完整 TSV、指定下载链接和 `COMPLETE`。

推进信号：CONTINUE

[1]: https://sede.gobiernodecanarias.org/boc/boc-a-2024-259-4403.pdf?utm_source=chatgpt.com "Boletín Oficial de Canarias núm. 259"
[2]: https://www.autocasion.com/marcas/nissan/cabstar-industrial/cabstar-e-120-35-1-2-puertas-24085?utm_source=chatgpt.com "Ficha técnica y precios del NISSAN Cabstar ..."
[3]: https://www.autocasion.com/marcas/nissan/cabstar-industrial/cabstar-e-120-35-2-doble-cabina-4-puertas-24089?utm_source=chatgpt.com "Ficha técnica y precios del NISSAN Cabstar ..."


--- 发送 / 继续到 Round 19 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1-100_ktype_dimension_mapping_final.tsv
- all_1-100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 19 / 下一步 ---
## 更新点

* Cabstar `119556–119571` 已确认均属于 F22 车型记录，但 F22 原厂零件目录同时覆盖 Long Body、High Bed、单／双后轮等组合；现有车型资料至少存在 `4460 × 1695 × 1930 mm` 双排短轴和 `4690 × 1695 × 1945 mm` 单排长轴外廓，仍无法将每个 Ktype 完整对应到具体物理分支，因此本轮不建立猜测尺寸组。([日产欧洲][1])
* Mascott `119207` 已确认覆盖双排驾驶室多轴距，但现有资料仍只给出轴距或上装后整车尺寸，缺少三个裸底盘分支统一口径的车长、高度及明确不含后视镜宽度。([scribd.com][2])
* 本轮没有新增 READY 映射，也没有首次闭合或修正的尺寸组。

## 当前批次进度

* 输入 Ktype 覆盖：100 / 100
* READY 映射：234 行
* PENDING 映射：10 行
* 已确认尺寸组：118
* 待闭合：Mascott 3 个轴距分支、Cabstar F22 7 个 Ktype
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

无

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

无

## 下一步优先处理

1. 继续查找 Cabstar F22 原厂完整车型矩阵，将发动机 Ktype 与单排／双排、短轴／长轴、高床／低床分支对应。
2. 查找 Mascott 双排驾驶室 `3630/4130/4630 mm` 的原厂 1:20 外廓图或型式批准尺寸附件。
3. 仅在长宽高和无后视镜宽度同时闭合后创建尺寸组；PENDING 清零后立即组装最终两张完整 TSV 与指定下载文件。

推进信号：CONTINUE

[1]: https://nissan-europe.epc-data.com/cabstar/f22/1632-h/body_back_door_and_rear/930/93550/ "930 - REAR BODY for Cabstar F22 Nissan Cabstar - Genuine parts"
[2]: https://www.scribd.com/document/726709779/364-4-AN-MASCOTT?utm_source=chatgpt.com "Renault Mascott Bodywork Fitting Guide | PDF | Truck"


--- 发送 / 继续到 Round 20 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1-100_ktype_dimension_mapping_final.tsv
- all_1-100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 20 / 下一步 ---
## 更新点

* 已进一步确认 `119556`、`119560`、`119563`、`119566`、`119567`、`119570`、`119571` 均为 Cabstar **F22** Ktype，并确认对应发动机分别为 TD25、SD25、Z16、LD20T、Z22、TD27、ED33。([Prom][1])
* 原厂零件目录确认 F22 同时存在标准／长车身、高床／低床以及单／双后轮组合；例如 Z16 同时用于 BF22 与 BGF22，TD25、SD25 则能检索到长车身不同床面配置。因此不能将整个 Ktype 简化为单一外廓。([日产零件目录][2])
* 已找到的 F22 规格分别出现 `4460×1695×1930 mm` 和 `4690×1690×1975 mm`，但它们对应不同车型代码、载重、床面和轮胎配置，尚不足以完成七个 Ktype 的全分支映射，未跨配置拼接尺寸。([nextage.jp][3])
* Mascott 官方车身制造资料仍只闭合双排驾驶室结构及三个轴距，尚未提供三个分支可直接落盘的完整外廓尺寸和明确无后视镜宽度。([scribd.com][4])
* 本轮没有达到 READY 条件的新映射或新尺寸组。

## 当前批次进度

* 输入 Ktype 覆盖：100 / 100
* READY 映射：234 行
* PENDING 映射：10 行
* 已确认尺寸组：118
* 待闭合：Mascott 3 个轴距分支、Cabstar F22 7 个 Ktype
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

无

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

无

## 下一步优先处理

1. 按 BF22、BGF22、TF22、AGF22 等具体车型代码查找对应的原厂车型尺寸页，闭合 Cabstar F22 标准／长车身及床面、轮胎分支。
2. 获取 Mascott 双排驾驶室 `3630/4130/4630 mm` 三张原厂 1:20 外廓图或型式批准尺寸附件。
3. PENDING 清零后立即执行一次机械检查，并输出两张最终完整 TSV、两个指定下载链接及 `推进信号：COMPLETE`。

推进信号：CONTINUE

[1]: https://prom.ua/p2977544949-opora-kulova-nissan.html?utm_source=chatgpt.com "Опора кульова NISSAN 555 SB-4391, цена: 869 ₴, купить на Prom.ua"
[2]: https://nissan.epc-data.com/atlas/bgf22/1810/body/H8005/80256M/?utm_source=chatgpt.com "front door window - & regulator (body) for Nissan Atlas BGF22"
[3]: https://www.nextage.jp/carcatalog/nissan/atlas/u-tf22/?utm_source=chatgpt.com "アトラス型式：U-TF22（日産）のクルマカタログ"
[4]: https://www.scribd.com/document/726709779/364-4-AN-MASCOTT?utm_source=chatgpt.com "Renault Mascott Bodywork Fitting Guide | PDF | Truck"


--- 发送 / 继续到 Round 21 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1-100_ktype_dimension_mapping_final.tsv
- all_1-100_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- 脚本异常 ---
异常: 对话分支失败（已尝试 3 次）: 没有找到最后一条用户消息的【在新聊天中分支】入口


--- 脚本异常 ---
异常: ChatGPT 页面显示未登录

