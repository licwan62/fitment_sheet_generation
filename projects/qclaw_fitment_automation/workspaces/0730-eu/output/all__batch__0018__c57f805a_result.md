# 任务：all 第 1701-1800 行
# 来源文件：all.tsv
# 任务 ID：all__batch__0018__c57f805a


--- 发送 / 首次任务 ---
【任务名称】
【全量表更新】all 第 1701-1800 行

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
all 第 1701-1800 行

【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1701-1800_ktype_dimension_mapping_final.tsv
- all_1701-1800_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。

【跨批次已有尺寸组索引】
以下 ID 已经存在于累计表。三维和物理外廓完全相同时才可复用；如果当前证据得到不同三维，禁止改写已有组，必须使用同系列下一个可用序号创建新 DIMENSION_GROUP_ID，并把当前批次相关 Ktype 全部指向新组。

DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM
EU-AUDI-A4-B9-AVANT-WAGON-01	4725	1842	1434
EU-AUDI-R8-II-4S-SPYDER-01	4426	1940	1244
EU-BMW-3-E30-BAUR-TC-CONVERTIBLE-01	4325	1645	1380
EU-BMW-3-E30-M3-CONVERTIBLE-01	4345	1680	1370
EU-BMW-3-E36-COMPACT-HATCHBACK-01	4210	1698	1393
EU-BMW-3-E46-COMPACT-HATCHBACK-01	4262	1751	1408
EU-BMW-3-E46-CONVERTIBLE-FACELIFT-01	4488	1757	1372
EU-BMW-3-E46-CONVERTIBLE-PREFL-01	4488	1757	1372
EU-BMW-3-E46-COUPE-FACELIFT-01	4488	1757	1369
EU-BMW-3-E46-COUPE-PREFL-01	4490	1755	1370
EU-BMW-3-E46-SEDAN-FACELIFT-01	4471	1739	1415
EU-BMW-3-E46-SEDAN-PREFL-01	4471	1739	1415
EU-BMW-3-E46-WAGON-FACELIFT-01	4478	1739	1409
EU-BMW-3-E46-WAGON-PREFL-01	4478	1739	1409
EU-BMW-3-E90-SEDAN-FACELIFT-01	4531	1817	1421
EU-BMW-3-E90-SEDAN-PREFL-01	4520	1817	1421
EU-BMW-3-E91-WAGON-FACELIFT-01	4527	1817	1418
EU-BMW-3-E91-WAGON-PREFL-01	4520	1817	1418
EU-BMW-3-E93-CONVERTIBLE-FACELIFT-01	4612	1782	1384
EU-BMW-3-E93-CONVERTIBLE-PREFL-01	4580	1782	1384
EU-BMW-3-F31-WAGON-PREFL-RWD-01	4624	1811	1429
EU-BMW-3-F31-WAGON-PREFL-XDRIVE-01	4624	1811	1434
EU-BMW-3-F34-GRAN-TURISMO-01	4824	1828	1508
EU-BMW-340-SEDAN-01	4600	1765	1630
EU-BMW-5-E39-SEDAN-FACELIFT-01	4775	1800	1435
EU-BMW-5-E39-WAGON-FACELIFT-01	4805	1800	1445
EU-BMW-5-E39-WAGON-PREFL-01	4805	1800	1445
EU-BMW-5-E60-SEDAN-01	4841	1846	1468
EU-BMW-5-E61-WAGON-01	4843	1846	1491
EU-BMW-5-F07-GRAN-TURISMO-FACELIFT-01	5004	1901	1559
EU-BMW-5-F10-SEDAN-FACELIFT-01	4907	1860	1464
EU-BMW-5-F10-SEDAN-PREFL-01	4899	1860	1464
EU-BMW-5-F11-WAGON-FACELIFT-01	4907	1860	1462
EU-BMW-5-G30-SEDAN-FACELIFT-01	4963	1868	1479
EU-BMW-5-G30-SEDAN-M550D-01	4962	1868	1467
EU-BMW-5-G30-SEDAN-PREFL-01	4936	1868	1479
EU-BMW-5-G31-WAGON-FACELIFT-01	4963	1868	1498
EU-BMW-5-G31-WAGON-M550D-01	4962	1868	1488
EU-BMW-5-G31-WAGON-PREFL-01	4943	1868	1498
EU-BMW-502-SEDAN-01	4730	1780	1530
EU-BMW-507-CONVERTIBLE-01	4380	1680	1275
EU-BMW-6-E24-COUPE-FACELIFT-01	4815	1725	1365
EU-BMW-6-G32-GRAN-TURISMO-HATCHBACK-01	5091	1902	1538
EU-BMW-7-E38-SEDAN-LWB-01	5124	1862	1425
EU-BMW-7-E38-SEDAN-SWB-01	4984	1862	1435
EU-BMW-7-E65-SEDAN-PREFL-01	5029	1902	1492
EU-BMW-7-G11-SEDAN-PREFL-01	5098	1902	1467
EU-BMW-7-G12-SEDAN-PREFL-01	5238	1902	1479
EU-CITROEN-C3-III-HATCHBACK-PREFL-01	3996	1749	1474
EU-FIAT-SCUDO-I-220-PLATFORM-CHASSIS-01	4430	1810	1927
EU-HYUNDAI-I30-II-GD-COUPE-01	4300	1780	1470
EU-HYUNDAI-I30-III-PD-HATCHBACK-5D-01	4340	1795	1455
EU-HYUNDAI-I30-III-PD-WAGON-01	4585	1795	1465
EU-JAGUAR-F-PACE-X761-SUV-PREFL-01	4731	1936	1652
EU-JAGUAR-XE-X760-SEDAN-01	4672	1850	1416
EU-JAGUAR-XE-X760-SEDAN-PROJECT-8-01	4713	1954	1436
EU-KIA-SORENTO-III-UM-SUV-FACELIFT-01	4800	1890	1685
EU-KIA-SORENTO-III-UM-SUV-PREFL-01	4780	1890	1685
EU-LAMBORGHINI-AVENTADOR-LP750-SV-ROADSTER-01	4835	2030	1136
EU-LAMBORGHINI-AVENTADOR-S-COUPE-01	4797	2030	1136
EU-MAN-TGE-I-CHASSIS-DCAB-L3-01	5996	2037	2330
EU-MAN-TGE-I-CHASSIS-DCAB-L4-01	6846	2037	2321
EU-MAN-TGE-I-CHASSIS-SCAB-L3-01	5996	2033	2312
EU-MAN-TGE-I-CHASSIS-SCAB-L4-01	6846	2033	2305
EU-MINI-MINI-F54-WAGON-01	4253	1800	1441
EU-MINI-MINI-F56-HATCHBACK-COOPER-S-01	3850	1727	1414
EU-MINI-MINI-F57-CONVERTIBLE-01	3850	1727	1415
EU-MINI-MINI-R55-CLUBMAN-WAGON-01	3961	1683	1426
EU-MINI-MINI-R57-CONVERTIBLE-COOPER-S-FACELIFT-01	3729	1683	1414
EU-MINI-MINI-R57-CONVERTIBLE-COOPER-S-PREFL-01	3714	1683	1414
EU-MINI-MINI-R61-PACEMAN-COUPE-01	4114	1786	1518
EU-PEUGEOT-EXPERT-III-VAN-COMPACT-01	4609	1920	1910
EU-PEUGEOT-EXPERT-III-VAN-COMPACT-HIGH-01	4609	1920	1950
EU-PEUGEOT-EXPERT-III-VAN-LONG-HIGH-01	5309	1920	1940
EU-PEUGEOT-EXPERT-III-VAN-STANDARD-01	4959	1920	1899
EU-PEUGEOT-EXPERT-III-VAN-STANDARD-HIGH-01	4959	1920	1940
EU-PEUGEOT-PARTNER-II-B9-TEPEE-4X4-01	4380	1810	1801
EU-RENAULT-MEGANE-II-GRANDTOUR-PHASE-II-WAGON-01	4500	1777	1467
EU-RENAULT-MEGANE-III-CC-CONVERTIBLE-01	4485	1811	1434
EU-RENAULT-MEGANE-III-HATCHBACK-5D-01	4302	1808	1471
EU-RENAULT-MEGANE-IV-GRANDTOUR-GT-WAGON-01	4626	1814	1457
EU-RENAULT-MEGANE-IV-GRANDTOUR-WAGON-01	4626	1814	1449
EU-RENAULT-MEGANE-IV-GT-HATCHBACK-01	4359	1814	1438
EU-RENAULT-MEGANE-IV-HATCHBACK-01	4359	1814	1447
EU-RENAULT-MEGANE-IV-SEDAN-01	4632	1814	1443
EU-RENAULT-TWINGO-II-HATCHBACK-FACELIFT-01	3687	1654	1470
EU-RENAULT-TWINGO-II-HATCHBACK-PREFL-01	3600	1654	1470
EU-RENAULT-TWINGO-III-HATCHBACK-01	3595	1647	1557
EU-SEAT-IBIZA-V-KJ1-HATCHBACK-01	4059	1780	1444
EU-TOYOTA-CAMRY-XV50-SEDAN-FACELIFT-01	4850	1825	1480
EU-TOYOTA-CAMRY-XV50-SEDAN-PREFL-01	4825	1825	1480
EU-TOYOTA-YARIS-III-XP130-HATCHBACK-FACELIFT-01	3945	1695	1510
EU-VW-POLO-III-6N1-HATCHBACK-01	3715	1655	1420
EU-VW-POLO-IV-9N2-SEDAN-01	4179	1650	1465
EU-VW-POLO-V-FACELIFT-CITYVAN-3D-01	3972	1682	1462
EU-VW-POLO-V-FACELIFT-CITYVAN-BLUEGT-3D-01	3972	1682	1453
EU-VW-POLO-VI-AW1-HATCHBACK-01	4053	1751	1446
EU-VW-T-ROC-I-A11-SUV-01	4234	1819	1573
EU-VW-TIGUAN-II-AD1-SUV-4MOTION-PREFL-01	4486	1839	1673
EU-VW-TIGUAN-II-AD1-SUV-FWD-PREFL-01	4486	1839	1654

【TSV 数据】
Make	Model	VariantName	BodyStyle	DriveType	Energy	EngineOutputKW	EngineOutputHP	Product Start Month-Year	Product End Month-Year	LastProcessedDate	Ktype
Renault	Megane iv	1.5 DCI 90	Stufenheck	Frontantrieb	Diesel	66	90	Oct 2016	-	2024-03-01	128576
Renault	Megane iv	1.5 DCI 110	Stufenheck	Frontantrieb	Diesel	81	110	Oct 2016	-	2024-03-01	128577
Renault	Megane iv	1.6 DCI 130	Stufenheck	Frontantrieb	Diesel	96	130	Oct 2016	-	2024-03-01	128578
Nissan	Leaf	Electric	Schrägheck	Frontantrieb	Elektro	110	150	Aug 2017	-	2024-03-01	128580
Goupil	G4	Electric	Pritsche/Fahrgestell	Heckantrieb	Elektro	10	14	Jan 2016	-	2024-03-01	128588
BMW	6	640 D Xdrive	Schrägheck	Allrad	Diesel	235	320	Nov 2017	Jun 2020	2024-03-01	128591
Goupil	G5	Electric	Pritsche/Fahrgestell	Heckantrieb	Elektro	20	27	Jan 2016	-	2024-03-01	128592
Lamborghini	Aventador	6.5 LP 740-4 S AWD	Targa	Allrad	Benzin	544	740	Dec 2016	-	2024-03-01	128595
Jeep	Patriot	2.2 CRD	Geländewagen geschlossen	Frontantrieb	Diesel	100	136	Jan 2011	Dec 2017	2024-03-01	128596
Ford	Transit v363	2.2 Tdci Allrad	Bus	Allrad	Diesel	114	155	Aug 2015	Dec 2018	2024-03-01	128597
VW	Polo	1.0 TSI	Schrägheck	Frontantrieb	Benzin	85	116	Sep 2017	-	2024-08-01	128598
VW	Polo	1.0 TGI	Schrägheck	Frontantrieb	Benzin/Erdgas (CNG)	66	90	Sep 2017	-	2024-03-01	128599
Mercedes-benz	X-Klasse	X 220 D	Pick-up	Heckantrieb	Diesel	120	163	Sep 2017	May 2020	2024-03-01	128600
Mercedes-benz	X-Klasse	X 220 D 4-matic	Pick-up	Allrad	Diesel	120	163	Sep 2017	May 2020	2024-03-01	128601
Mercedes-benz	X-Klasse	X 250 D 4-matic	Pick-up	Allrad	Diesel	140	190	Sep 2017	May 2020	2024-03-01	128602
Mercedes-benz	X-Klasse	X 250 D	Pick-up	Heckantrieb	Diesel	140	190	Sep 2017	May 2020	2024-03-01	128603
Rolls-royce	Phantom viii	V12, V12 EWB	Stufenheck	Heckantrieb	Benzin	420	571	Sep 2017	-	2024-03-01	128606
Toyota	Camry	2.5 Hybrid	Stufenheck	Frontantrieb	Benzin/Elektro	160	218	Aug 2017	-	2024-03-01	128630
Jaguar	Xf sportbrake	2	Kombi	Heckantrieb	Benzin	147	200	Jul 2017	-	2024-03-01	128637
Jaguar	Xe	2	Stufenheck	Heckantrieb	Benzin	221	300	Jun 2017	-	2024-03-01	128638
Audi	A8 d5	55 Tfsi Mild Hybrid Quattro	Stufenheck	Allrad	Benzin/Elektro	250	340	Jun 2017	-	2024-03-01	128644
Audi	A8 d5	50 TDI Mild Hybrid Quattro	Stufenheck	Allrad	Diesel/Elektro	210	286	Jun 2017	-	2024-03-01	128645
Mclaren	570s	3.8	Cabriolet	Heckantrieb	Benzin	419	570	Jul 2017	-	2024-03-01	128648
Mercedes-benz	E-Klasse	E 350 D 4-matic	Coupe	Allrad	Diesel	190	258	Jun 2017	-	2024-03-01	128649
VW	T-Roc	2.0 TDI 4motion	SUV	Allrad	Diesel	110	150	Sep 2017	-	2024-03-01	128651
Opel	Insignia a country tourer	2.0 Turbo 4X4	Kombi	Allrad	Benzin	184	250	Sep 2013	Mar 2017	2024-03-01	128664
Genesis	G70	2.0 T-gdi	Stufenheck	Heckantrieb	Benzin	185	252	Sep 2017	Jan 2020	2024-05-01	128668
Genesis	G70	2.0 T-gdi Htrac	Stufenheck	Allrad	Benzin	185	252	Sep 2017	Jan 2020	2024-05-01	128669
Opel	Insignia a country tourer	2.0 Cdti 4X4	Kombi	Allrad	Diesel	120	163	Sep 2013	Mar 2017	2024-03-01	128670
Opel	Insignia a country tourer	2.0 Cdti 4X4	Kombi	Allrad	Diesel	143	194	Sep 2013	Mar 2017	2024-03-01	128673
Opel	Insignia a country tourer	2.0 Cdti	Kombi	Frontantrieb	Diesel	120	163	Jul 2014	Mar 2017	2024-03-01	128674
Opel	Insignia a country tourer	1.6 Sidi	Kombi	Frontantrieb	Benzin	125	170	Jul 2014	Mar 2017	2024-03-01	128675
Opel	Insignia a country tourer	2.0 Cdti	Kombi	Frontantrieb	Diesel	125	170	Nov 2014	Mar 2017	2024-03-01	128676
Opel	Insignia a country tourer	2.0 Cdti 4X4	Kombi	Allrad	Diesel	125	170	Nov 2014	Mar 2017	2024-03-01	128677
Opel	Insignia a country tourer	2.0 Cdti	Kombi	Frontantrieb	Diesel	96	131	Jul 2008	Mar 2017	2024-03-01	128678
Opel	Insignia a country tourer	2.0 Cdti	Kombi	Frontantrieb	Diesel	88	120	Mar 2012	Mar 2017	2024-03-01	128679
Opel	Insignia a country tourer	1.6 Cdti	Kombi	Frontantrieb	Diesel	88	120	Jul 2015	Mar 2017	2024-03-01	128680
Opel	Insignia a country tourer	1.6 Cdti	Kombi	Frontantrieb	Diesel	100	136	Jul 2015	Mar 2017	2024-03-01	128681
VW	Tiguan	1.4 TSI E100 Flex	SUV	Frontantrieb	Benzin/Ethanol	110	150	Jul 2017	-	2024-03-01	128682
KIA	Sorento iii	2.0 Crdi 4WD	SUV	Allrad	Diesel	136	185	Jul 2015	Dec 2020	2024-05-01	128687
BMW	5	520 D Xdrive	Kombi	Allrad	Diesel	120	163	Jul 2017	-	2024-03-01	128696
VW	Tiguan	2.0 TSI 4motion	SUV	Allrad	Benzin	162	220	Jul 2017	-	2024-03-01	128698
BMW	7	725 D, LD	Stufenheck	Heckantrieb	Diesel	155	211	Jul 2016	Feb 2019	2024-03-01	128702
Mini	Mini	Cooper S JCW	Kombi	Frontantrieb	Benzin	155	211	Nov 2014	Jun 2018	2024-03-01	128704
Mini	Mini	Cooper S JCW All4	Kombi	Allrad	Benzin	155	211	Nov 2014	-	2024-03-01	128710
Mini	Mini	Cooper S JCW	Cabriolet	Frontantrieb	Benzin	155	211	Nov 2015	-	2025-06-01	128711
Mini	Mini	Cooper S JCW	Schrägheck	Frontantrieb	Benzin	155	211	Dec 2013	-	2024-03-01	128712
Mini	Mini	Cooper S JCW	Schrägheck	Frontantrieb	Benzin	155	211	Jul 2014	-	2025-06-01	128713
BMW	6	640 I	Schrägheck	Heckantrieb	Benzin	265	360	Jun 2017	Jun 2020	2024-03-01	128716
BMW	6	640 I Xdrive	Schrägheck	Allrad	Benzin	265	360	Jun 2017	Jun 2020	2024-03-01	128718
BMW	6	630 D	Schrägheck	Heckantrieb	Diesel	155	211	Jun 2017	Jun 2020	2024-03-01	128720
BMW	6	630 D Xdrive	Schrägheck	Allrad	Diesel	155	211	Jun 2017	Jun 2020	2024-03-01	128722
Volvo	Xc40	T5 AWD	SUV	Allrad	Benzin	182	247	Oct 2017	Sep 2021	2024-03-01	128759
Volvo	Xc40	D4 AWD	SUV	Allrad	Diesel	140	190	Oct 2017	Sep 2021	2024-03-01	128760
Hyundai	I30	2.0 N	Schrägheck	Frontantrieb	Benzin	184	250	Jul 2017	-	2024-03-01	128761
Hyundai	I30	2.0 N	Schrägheck	Frontantrieb	Benzin	202	275	Jul 2017	-	2024-03-01	128762
Toyota	Yaris	1.8 Grmn	Schrägheck	Frontantrieb	Benzin	156	212	Sep 2017	Jun 2020	2024-05-01	128765
VW	Amarok	3.0 TDI 4motion	Pick-up	Allrad	Diesel	120	163	Jun 2016	Jun 2020	2024-03-01	128766
VW	Amarok	3.0 TDI	Pick-up	Heckantrieb	Diesel	120	163	Jun 2016	Jun 2020	2025-06-01	128767
Jaguar	F-Pace	2.0 TI4	SUV	Heckantrieb	Benzin	184	250	Sep 2017	-	2024-03-01	128768
Mercedes-benz	S-Klasse	S 650 Maybach	Cabriolet	Heckantrieb	Benzin	463	630	Aug 2017	May 2019	2024-03-01	128772
Seat	Ibiza v	1.6 TDI	Schrägheck	Frontantrieb	Diesel	70	95	Sep 2017	-	2024-03-01	128786
Opel	Insignia b country tourer	1.5	Kombi	Frontantrieb	Benzin	121	165	Jun 2017	-	2024-03-01	128794
Opel	Insignia b country tourer	2.0 4X4	Kombi	Allrad	Benzin	191	260	Jun 2017	-	2024-03-01	128795
Opel	Insignia b country tourer	2.0 Cdti	Kombi	Frontantrieb	Diesel	125	170	Jun 2017	-	2024-03-01	128796
Opel	Insignia b country tourer	2.0 Cdti 4X4	Kombi	Allrad	Diesel	125	170	Jun 2017	-	2024-03-01	128797
Audi	R8	5.2 FSI RWS	Coupe	Heckantrieb	Benzin	397	540	Sep 2017	-	2025-12-01	128799
Audi	R8	5.2 FSI RWS	Cabriolet	Heckantrieb	Benzin	397	540	Sep 2017	-	2025-12-01	128800
Opel	Astra k	1.4 CNG	Schrägheck	Frontantrieb	Benzin/Erdgas (CNG)	81	110	Oct 2017	May 2018	2025-12-01	128802
Renault	Twingo	1.2 LPG	Schrägheck	Frontantrieb	Benzin/Autogas (LPG)	43	58	Sep 2000	Jun 2007	2026-05-01	128810
Opel	Astra k sports tourer	1.4 CNG	Kombi	Frontantrieb	Benzin/Erdgas (CNG)	81	110	Aug 2017	May 2018	2025-12-01	128814
Audi	A4 b9 avant	RS4 Tfsi Quattro	Kombi	Allrad	Benzin	331	450	Oct 2017	-	2025-11-01	128816
Citroën	C3 iii	1.6 VTI	Schrägheck	Frontantrieb	Benzin	85	116	Feb 2017	-	2025-12-01	128824
Renault	Alaskan	2.3 DCI 190 4X4	Pick-up	Allrad	Diesel	140	190	Sep 2017	-	2024-03-01	128831
Renault	Alaskan	2.3 DCI 163 4X4	Pick-up	Allrad	Diesel	120	163	Sep 2017	-	2024-03-01	128832
Renault	Super 5	1.4	Schrägheck	Frontantrieb	Benzin	43	58	Aug 1986	Dec 1996	2024-03-01	128834
Renault	Megane ii	1.5 DCI	Kasten/Kombi	Frontantrieb	Diesel	63	86	May 2005	Jul 2009	2024-03-01	128854
DS	Ds	1.6 Puretech 225	SUV	Frontantrieb	Benzin	165	224	Sep 2017	Dec 2022	2025-06-01	128856
DS	Ds	2.0 Bluehdi 180	SUV	Frontantrieb	Diesel	130	177	Sep 2017	Sep 2020	2024-03-01	128857
Ssangyong	Rexton	2.2 XDI	SUV	Heckantrieb	Diesel	133	181	Jul 2017	-	2024-03-01	128860
Audi	A6 c4 avant	2	Kombi	Frontantrieb	Benzin	79	107	Jun 1994	Jul 1995	2024-03-01	128865
Audi	A6 c4 avant	2.8	Kombi	Frontantrieb	Benzin	120	163	Jun 1994	Jul 1995	2024-03-01	128866
Mercedes-benz	E-Klasse	E 320 T CDI	Kombi	Heckantrieb	Diesel	155	211	Nov 2007	Jul 2009	2024-03-01	128872
Renault	Twingo	1.2	Kasten/Schrägheck	Frontantrieb	Benzin	55	75	Jan 2001	Jun 2012	2026-05-01	128882
Renault	Logan/stepway ii	1.6	Stufenheck	Frontantrieb	Benzin	83	113	Sep 2016	-	2024-03-01	128883
Renault	Espace v	1.8 TCE 225	Großraumlimousine	Frontantrieb	Benzin	165	224	Oct 2016	Mar 2023	2026-01-01	128888
BMW	3	330 XI	Coupe	Allrad	Benzin	200	272	Mar 2007	Feb 2010	2024-03-01	128906
BMW	3	325 I Xdrive	Coupe	Allrad	Benzin	155	211	Mar 2010	Apr 2013	2024-03-01	128917
Ford USA	Taurus	3	Stufenheck	Frontantrieb	Benzin	115	156	Jan 2000	Dec 2005	2024-03-01	128922
Fiat	Scudo	2.0 D Multijet 4X4	Kasten	Allrad	Diesel	94	128	May 2011	Mar 2016	2024-03-01	128923
Fiat	Scudo	2.0 D Multijet 4X4	Kasten	Allrad	Diesel	100	136	Jan 2007	Mar 2016	2024-03-01	128924
Peugeot	206+	1.1 LPG	Schrägheck	Frontantrieb	Benzin/Autogas (LPG)	44	60	Apr 2009	Jun 2013	2024-03-01	128928
Peugeot	207 sw	1.4 LPG	Kombi	Frontantrieb	Benzin/Autogas (LPG)	54	73	Aug 2007	Dec 2012	2024-03-01	128929
VW	T-Roc	1.5 TSI	SUV	Frontantrieb	Benzin	110	150	Nov 2017	-	2024-03-01	128940
Peugeot	Expert	2.0 HDI	Pritsche/Fahrgestell	Frontantrieb	Diesel	80	109	Oct 2000	Oct 2006	2024-03-01	128943
Peugeot	Partner	1.6 HDI 75	Kasten/Großraumlimousine	Frontantrieb	Diesel	55	75	Aug 2005	Jul 2008	2024-03-01	128944
Ssangyong	Rexton	2.2 XDI Allrad	SUV	Allrad	Diesel	133	181	Jul 2017	-	2024-03-01	128946
Peugeot	J5	2.5 DT	Bus	Frontantrieb	Diesel	70	95	Jan 1986	Aug 1990	2024-03-01	128950
Fiat	Fiorino	1.4 Natural Power	Kasten/Großraumlimousine	Frontantrieb	Benzin/Erdgas (CNG)	51	69	Jun 2008	-	2024-03-01	128951
MAN	Tge	2.0 TDI RWD	Kasten	Heckantrieb	Diesel	90	122	Aug 2017	Dec 2021	2025-11-01	128959


--- Round 1 / 首次发送 ---
## 更新点

* 本轮继续处理剩余 PENDING：

  * `119207` Renault Trucks Mascott 150.35
  * `119556/119560/119563/119566/119567/119570/119571` Nissan Cabstar F22
* Mascott：

  * 已确认 `119207` 对应 Mascott II 双排驾驶室底盘系列。
  * 已确认轴距存在 `3630 / 4130 / 4630 mm` 三个物理分支。
  * 当前公开资料仍缺少统一口径的整车高度及明确 WITHOUT MIRRORS 宽度，因此暂不创建 DIMENSION_GROUP。
* Cabstar F22：

  * 已进一步确认 F22 平台存在 BF22/BGF22/TF22 等车身代码族。
  * 已确认部分规格尺寸：

    * 短轴车型约 `4460 mm`
    * 长轴车型约 `4690 mm`
    * 宽度存在 `1690–1695 mm` 不同资料值
  * 当前资料无法确认：

    * 单排/双排边界
    * 高床/低床边界
    * 宽度是否均为 WITHOUT MIRRORS
  * 按规则未建立猜测性尺寸组。

## 当前批次进度

* 输入 Ktype 覆盖：100 / 100
* READY 映射：234 行
* PENDING 映射：10 行
* 已确认 DIMENSION_GROUP：118
* 当前剩余：

  * Mascott 3 个轴距分支
  * Cabstar F22 7 个 Ktype
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

无

## 本轮首次创建/修正的 DIMENSION_GROUP TSV

无

## 下一步优先处理

1. 继续寻找 Nissan Cabstar F22 欧洲市场原厂 brochure / homologation 文件，优先闭合：

   * BF22
   * BGF22
   * TF22
   * AGF22
     对应驾驶室和轴距关系。
2. 查找 Renault Mascott II 官方车身制造商尺寸附件，确认：

   * 3630 mm
   * 4130 mm
   * 4630 mm
     三个双排驾驶室底盘的完整外廓。
3. PENDING 清零后执行一次机械检查，直接输出：

   * 完整 Ktype 映射 TSV
   * 完整 DIMENSION_GROUP TSV
   * 两个指定 sandbox 下载链接
   * `推进信号：COMPLETE`

推进信号：CONTINUE


--- 发送 / 继续到 Round 2 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- all_1701-1800_ktype_dimension_mapping_final.tsv
- all_1701-1800_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- 脚本异常 ---
异常: 对话分支失败（已尝试 3 次）: 没有找到最后一条用户消息的【在新聊天中分支】入口

