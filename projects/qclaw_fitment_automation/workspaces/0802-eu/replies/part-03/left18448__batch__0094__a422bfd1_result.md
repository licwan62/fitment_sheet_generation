# 任务：left18448 第 9301-9400 行
# 来源文件：left18448.tsv
# 任务 ID：left18448__batch__0094__a422bfd1


--- 发送 / 首次任务 ---
【任务名称】
【全量表更新】left18448 第 9301-9400 行

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
left18448.tsv

【当前独立任务】
left18448 第 9301-9400 行

【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- left18448_9301-9400_ktype_dimension_mapping_final.tsv
- left18448_9301-9400_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


【TSV 数据】
Make	Model	VariantName	BodyStyle	DriveType	Energy	Product Start Month-Year	Product End Month-Year	Ktype
Mercedes-benz	Amg gt	GT	Coupe	Heckantrieb	Benzin	Jan 2017	Dec 2021	126755
Mercedes-benz	Amg gt	GT C	Coupe	Heckantrieb	Benzin	Mar 2017	Dec 2021	128046
Mercedes-benz	Amg gt	GT R	Coupe	Heckantrieb	Benzin	Nov 2016	Dec 2021	123743
Mercedes-benz	Amg gt	GT S	Coupe	Heckantrieb	Benzin	Oct 2014	May 2020	108074
Mercedes-benz	Amg gt	GT S	Coupe	Heckantrieb	Benzin	Jan 2017	May 2020	126756
Mercedes-benz	Amg gt roadster	GT	Cabriolet	Heckantrieb	Benzin	Nov 2016	May 2020	123745
Mercedes-benz	Amg gt roadster	GT C	Cabriolet	Heckantrieb	Benzin	Nov 2016	Dec 2021	123747
Mercedes-benz	B-Klasse sports tourer	B 150	Schrägheck	Frontantrieb	Benzin	Mar 2005	Nov 2011	18590
Mercedes-benz	B-Klasse sports tourer	B 160	Schrägheck	Frontantrieb	Benzin	Jul 2015	Dec 2018	114993
Mercedes-benz	B-Klasse sports tourer	B 160 CDI / D	Schrägheck	Frontantrieb	Diesel	May 2013	Dec 2018	59384
Mercedes-benz	B-Klasse sports tourer	B 170	Schrägheck	Frontantrieb	Benzin	Mar 2005	Nov 2011	18510
Mercedes-benz	B-Klasse sports tourer	B 180	Schrägheck	Frontantrieb	Benzin	Nov 2011	Dec 2018	12171
Mercedes-benz	B-Klasse sports tourer	B 180 CDI	Schrägheck	Frontantrieb	Diesel	Nov 2011	Aug 2014	12173
Mercedes-benz	B-Klasse sports tourer	B 180 CDI	Schrägheck	Frontantrieb	Diesel	Mar 2005	Nov 2011	18507
Mercedes-benz	B-Klasse sports tourer	B 180 CDI	Schrägheck	Frontantrieb	Diesel	Jun 2013	Aug 2014	107068
Mercedes-benz	B-Klasse sports tourer	B 180 CDI / D	Schrägheck	Frontantrieb	Diesel	Feb 2013	Dec 2018	59438
Mercedes-benz	B-Klasse sports tourer	B 180 D	Schrägheck	Frontantrieb	Diesel	Oct 2020	-	142492
Mercedes-benz	B-Klasse sports tourer	B 180 Mild Hybrid	Schrägheck	Frontantrieb	Benzin/Elektro	Nov 2022	-	150758
Mercedes-benz	B-Klasse sports tourer	B 200	Schrägheck	Frontantrieb	Benzin	Nov 2011	Dec 2018	12172
Mercedes-benz	B-Klasse sports tourer	B 200	Schrägheck	Frontantrieb	Benzin	Mar 2005	Nov 2011	18511
Mercedes-benz	B-Klasse sports tourer	B 200 4-matic	Schrägheck	Allrad	Benzin	Oct 2020	-	142493
Mercedes-benz	B-Klasse sports tourer	B 200 CDI	Schrägheck	Frontantrieb	Diesel	Nov 2011	Aug 2014	12174
Mercedes-benz	B-Klasse sports tourer	B 200 CDI	Schrägheck	Frontantrieb	Diesel	Mar 2005	Nov 2011	18508
Mercedes-benz	B-Klasse sports tourer	B 200 CDI	Schrägheck	Frontantrieb	Diesel	Mar 2005	Nov 2011	54958
Mercedes-benz	B-Klasse sports tourer	B 200 CDI / D	Schrägheck	Frontantrieb	Diesel	Aug 2014	Dec 2018	107895
Mercedes-benz	B-Klasse sports tourer	B 200 CDI / D 4-matic	Schrägheck	Allrad	Diesel	Aug 2014	Dec 2018	107896
Mercedes-benz	B-Klasse sports tourer	B 200 Mild Hybrid	Schrägheck	Frontantrieb	Benzin/Elektro	Nov 2022	-	150759
Mercedes-benz	B-Klasse sports tourer	B 200 Natural GAS Drive / B 200 C	Schrägheck	Frontantrieb	Benzin/Erdgas (CNG)	Nov 2012	Dec 2017	57257
Mercedes-benz	B-Klasse sports tourer	B 200 Turbo	Schrägheck	Frontantrieb	Benzin	Mar 2005	Nov 2011	18512
Mercedes-benz	B-Klasse sports tourer	B 220 CDI / D	Schrägheck	Frontantrieb	Diesel	Nov 2011	Dec 2018	57292
Mercedes-benz	B-Klasse sports tourer	B 220 CDI / D	Schrägheck	Frontantrieb	Diesel	Jun 2013	Dec 2018	100550
Mercedes-benz	B-Klasse sports tourer	B 220 CDI / D	Schrägheck	Frontantrieb	Diesel	Aug 2014	Dec 2018	107954
Mercedes-benz	B-Klasse sports tourer	B 220 CDI / D 4-matic	Schrägheck	Allrad	Diesel	Aug 2014	Dec 2018	107955
Mercedes-benz	B-Klasse sports tourer	B 220 Mild-hybrid 4-matic	Schrägheck	Allrad	Benzin/Elektro	Oct 2022	-	150777
Mercedes-benz	B-Klasse sports tourer	B 250	Schrägheck	Frontantrieb	Benzin	May 2012	Dec 2018	55581
Mercedes-benz	B-Klasse sports tourer	B 250 4-matic	Schrägheck	Allrad	Benzin	Aug 2014	Dec 2018	107894
Mercedes-benz	B-Klasse sports tourer	B 250 E	Schrägheck	Frontantrieb	Benzin/Elektro	Nov 2022	-	150722
Mercedes-benz	B-Klasse sports tourer	B 250 MID Hybrid 4-matic	Schrägheck	Allrad	Benzin/Elektro	Oct 2022	-	150778
Mercedes-benz	B-Klasse sports tourer	Electric Drive / B 250 E	Schrägheck	Frontantrieb	Elektro	Nov 2014	Oct 2017	108181
Mercedes-benz	B-Klasse sports tourer	Electric Drive / B 250 E	Schrägheck	Frontantrieb	Elektro	Nov 2014	Oct 2017	109338
Mercedes-benz	B-Klasse sports tourer	F-cell	Schrägheck	Frontantrieb	Wasserstoff	Jan 2010	Nov 2011	54934
Mercedes-benz	Citan	112	Kasten/Großraumlimousine	Frontantrieb	Benzin	Jun 2013	Aug 2021	100170
Mercedes-benz	Citan	1.3 110	Kasten/Großraumlimousine	Frontantrieb	Benzin	Sep 2021	-	145362
Mercedes-benz	Citan	1.3 113	Kasten/Großraumlimousine	Frontantrieb	Benzin	Sep 2021	-	145363
Mercedes-benz	Citan	1.5 108 CDI	Kasten/Großraumlimousine	Frontantrieb	Diesel	Sep 2021	-	145359
Mercedes-benz	Citan	1.5 110 CDI	Kasten/Großraumlimousine	Frontantrieb	Diesel	Sep 2021	-	145360
Mercedes-benz	Citan	1.5 112 CDI	Kasten/Großraumlimousine	Frontantrieb	Diesel	Sep 2021	-	145361
Mercedes-benz	Citan	108 CDI	Kasten/Großraumlimousine	Frontantrieb	Diesel	Nov 2012	Aug 2021	57351
Mercedes-benz	Citan	109 CDI	Kasten/Großraumlimousine	Frontantrieb	Diesel	Nov 2012	Aug 2021	57352
Mercedes-benz	Citan	111 CDI	Kasten/Großraumlimousine	Frontantrieb	Diesel	Jun 2013	Aug 2021	100171
Mercedes-benz	Citan	Ecitan	Kasten/Großraumlimousine	Frontantrieb	Elektro	Sep 2022	-	149241
Mercedes-benz	Citan mixto	109 CDI	Kasten/Großraumlimousine	Frontantrieb	Diesel	Nov 2012	Aug 2021	57353
Mercedes-benz	Citan mixto	111 CDI	Kasten/Großraumlimousine	Frontantrieb	Diesel	Jun 2013	Aug 2021	100172
Mercedes-benz	Citan tourer	110	Großraumlimousine	Frontantrieb	Benzin	Sep 2021	-	145368
Mercedes-benz	Citan tourer	112	Großraumlimousine	Frontantrieb	Benzin	Jun 2013	Aug 2021	100182
Mercedes-benz	Citan tourer	113	Großraumlimousine	Frontantrieb	Benzin	Sep 2021	-	145369
Mercedes-benz	Citan tourer	108 CDI	Großraumlimousine	Frontantrieb	Diesel	Nov 2012	Aug 2021	57354
Mercedes-benz	Citan tourer	108 CDI	Großraumlimousine	Frontantrieb	Diesel	Sep 2021	-	145370
Mercedes-benz	Citan tourer	109 CDI	Großraumlimousine	Frontantrieb	Diesel	Nov 2012	Aug 2021	57355
Mercedes-benz	Citan tourer	110 CDI	Großraumlimousine	Frontantrieb	Diesel	Sep 2021	-	145371
Mercedes-benz	Citan tourer	111 CDI	Großraumlimousine	Frontantrieb	Diesel	Jun 2013	Aug 2021	100180
Mercedes-benz	Citan tourer	112 CDI	Großraumlimousine	Frontantrieb	Diesel	Sep 2021	-	147695
Mercedes-benz	Citan tourer	Ecitan	Großraumlimousine	Frontantrieb	Elektro	Jul 2023	-	155330
Mercedes-benz	C-Klasse	AMG C 43 4-matic	Cabriolet	Allrad	Benzin	Oct 2016	May 2018	120127
Mercedes-benz	C-Klasse	AMG C 43 4-matic	Stufenheck	Allrad	Benzin/Elektro	Apr 2024	-	158612
Mercedes-benz	C-Klasse	AMG C 43 4-matic	Kombi	Allrad	Benzin/Elektro	Apr 2024	-	800858
Mercedes-benz	C-Klasse	AMG C 43 4-matic	Kombi	Allrad	Benzin/Elektro	Apr 2024	-	800859
Mercedes-benz	C-Klasse	AMG C 43 4-matic+	Kombi	Allrad	Benzin/Elektro	Apr 2022	-	147481
Mercedes-benz	C-Klasse	AMG C 43 4-matic+	Stufenheck	Allrad	Benzin/Elektro	Apr 2022	-	147483
Mercedes-benz	C-Klasse	AMG C 63	Stufenheck	Heckantrieb	Benzin	Oct 2014	May 2021	108004
Mercedes-benz	C-Klasse	AMG C 63	Kombi	Heckantrieb	Benzin	Oct 2015	Feb 2021	108009
Mercedes-benz	C-Klasse	AMG C 63	Coupe	Heckantrieb	Benzin	Feb 2016	Apr 2023	116942
Mercedes-benz	C-Klasse	AMG C 63	Cabriolet	Heckantrieb	Benzin	Oct 2016	Apr 2023	120128
Mercedes-benz	C-Klasse	AMG C 63 S	Stufenheck	Heckantrieb	Benzin	Oct 2014	May 2021	108005
Mercedes-benz	C-Klasse	AMG C 63 S	Kombi	Heckantrieb	Benzin	Oct 2015	Feb 2021	108010
Mercedes-benz	C-Klasse	AMG C 63 S	Coupe	Heckantrieb	Benzin	Feb 2016	Apr 2023	116943
Mercedes-benz	C-Klasse	AMG C 63 S	Cabriolet	Heckantrieb	Benzin	Oct 2016	Apr 2023	120129
Mercedes-benz	C-Klasse	AMG C 63 S E Performance 4-matic+	Stufenheck	Allrad	Benzin/Elektro	Nov 2022	-	150717
Mercedes-benz	C-Klasse	AMG C 63 S E Performance 4-matic+	Kombi	Allrad	Benzin/Elektro	Nov 2022	-	150719
Mercedes-benz	C-Klasse	C 160	Stufenheck	Heckantrieb	Benzin	Apr 2015	Nov 2019	112350
Mercedes-benz	C-Klasse	C 160	Kombi	Heckantrieb	Benzin	Apr 2015	Nov 2019	112361
Mercedes-benz	C-Klasse	C 160 Kompressor	Coupe	Heckantrieb	Benzin	May 2002	May 2008	18882
Mercedes-benz	C-Klasse	C 180	Coupe	Heckantrieb	Benzin	Jun 2011	-	10333
Mercedes-benz	C-Klasse	C 180	Stufenheck	Heckantrieb	Benzin	Oct 2000	May 2002	14814
Mercedes-benz	C-Klasse	C 180	Coupe	Heckantrieb	Benzin	Mar 2001	May 2002	15262
Mercedes-benz	C-Klasse	C 180	Kombi	Heckantrieb	Benzin	Mar 2001	May 2002	15832
Mercedes-benz	C-Klasse	C 180	Coupe	Heckantrieb	Benzin	Jan 2013	-	58670
Mercedes-benz	C-Klasse	C 180	Stufenheck	Heckantrieb	Benzin	Mar 2014	Mar 2021	100750
Mercedes-benz	C-Klasse	C 180	Kombi	Heckantrieb	Benzin	Feb 2012	Aug 2014	106413
Mercedes-benz	C-Klasse	C 180	Kombi	Heckantrieb	Benzin	Sep 2014	Aug 2020	106453
Mercedes-benz	C-Klasse	C 180	Coupe	Heckantrieb	Benzin	Oct 2015	Aug 2020	116938
Mercedes-benz	C-Klasse	C 180	Cabriolet	Heckantrieb	Benzin	Jun 2016	Aug 2020	120121
Mercedes-benz	C-Klasse	C 180	Stufenheck	Heckantrieb	Benzin/Elektro	Mar 2021	-	143576
Mercedes-benz	C-Klasse	C 180	Kombi	Heckantrieb	Benzin/Elektro	Mar 2021	-	145151
Mercedes-benz	C-Klasse	C 180 Bluetec / D	Stufenheck	Heckantrieb	Diesel	May 2014	May 2018	106289
Mercedes-benz	C-Klasse	C 180 Bluetec / D	Kombi	Heckantrieb	Diesel	Sep 2014	May 2018	107473
Mercedes-benz	C-Klasse	C 180 CDI	Kombi	Heckantrieb	Diesel	Apr 2010	Aug 2014	12313
Mercedes-benz	C-Klasse	C 180 CGI	Kombi	Heckantrieb	Benzin	Nov 2009	Aug 2014	10036
Mercedes-benz	C-Klasse	C 180 CGI	Stufenheck	Heckantrieb	Benzin	Jan 2008	Jan 2014	59476
Mercedes-benz	C-Klasse	C 180 Kompressor	Stufenheck	Heckantrieb	Benzin	May 2002	Feb 2007	16714


--- Round 1 / 首次发送 ---
## 更新点

* 已闭合 AMG GT C190/R190 车身族：标准车宽、GT C/GT R 宽体以及 Coupe/Roadster 分开；跨 2019 更新且高度变化的 GT C Ktype 已拆为 `prefl`、`facelift`。([汽车目录][1])
* 已闭合 B-Class W245、W246、W242 的主要外廓。W245 跨 2008 改款、W246 跨 2014 改款的 Ktype 已拆分。
* Ktype `57257` 已修正为两条映射：改款前 Natural Gas Drive 与普通 W246 外廓一致；改款后使用独立的 Natural Gas Drive 宽高外廓。([km77][2])
* Electric Drive 两个 Ktype 已关联独立 W242 尺寸组。([汽车目录][3])
* W247 2022 改款后的 Mild Hybrid/4MATIC 暂未落盘：资料存在“1797 mm 折叠后视镜宽度”与官方“1796 mm 不含后视镜宽度”、不同高度配置之间的口径差异，继续保持待处理。([Mercedes-Benz][4])
* C205 Coupe 与 A205 Cabriolet 两个标准外廓直接复用既有缓存尺寸组。

## 当前批次进度

* 输入 Ktype：100
* READY 映射：54 行
* 已覆盖 Ktype：37
* 待闭合 Ktype：63
* 当前映射引用的尺寸组：16
* 本轮首次创建尺寸组：12
* 本轮复用既有尺寸组：4
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
126755	126755	Coupe	AMG GT C190	C190	2	EU-MERCEDES-BENZ-AMG-GT-C190-GT-COUPE-01	HIGH	标准车宽外廓。	READY
128046_prefl	128046	Coupe	AMG GT C190	C190	2	EU-MERCEDES-BENZ-AMG-GT-C190-GTC-COUPE-PREFL-01	MEDIUM	Ktype跨2019更新，改款前宽体外廓。	READY
128046_facelift	128046	Coupe	AMG GT C190	C190	2	EU-MERCEDES-BENZ-AMG-GT-C190-GTC-COUPE-FACELIFT-01	MEDIUM	Ktype跨2019更新，改款后宽体外廓。	READY
123743	123743	Coupe	AMG GT C190	C190	2	EU-MERCEDES-BENZ-AMG-GT-C190-GTR-COUPE-01	HIGH	GT R宽体外廓。	READY
108074	108074	Coupe	AMG GT C190	C190	2	EU-MERCEDES-BENZ-AMG-GT-C190-GT-COUPE-01	HIGH	标准车宽外廓。	READY
126756	126756	Coupe	AMG GT C190	C190	2	EU-MERCEDES-BENZ-AMG-GT-C190-GT-COUPE-01	HIGH	标准车宽外廓。	READY
123745	123745	Convertible	AMG GT R190	R190	2	EU-MERCEDES-BENZ-AMG-GT-R190-GT-ROADSTER-01	HIGH	标准车宽Roadster外廓。	READY
123747_prefl	123747	Convertible	AMG GT R190	R190	2	EU-MERCEDES-BENZ-AMG-GT-R190-GTC-ROADSTER-PREFL-01	MEDIUM	Ktype跨2019更新，改款前宽体外廓。	READY
123747_facelift	123747	Convertible	AMG GT R190	R190	2	EU-MERCEDES-BENZ-AMG-GT-R190-GTC-ROADSTER-FACELIFT-01	MEDIUM	Ktype跨2019更新，改款后宽体外廓。	READY
18590_prefl	18590	MPV	B-Class W245	W245	5	EU-MERCEDES-BENZ-B-KLASSE-W245-MPV-PREFL-01	MEDIUM	Ktype跨2008改款，改款前外廓。	READY
18590_facelift	18590	MPV	B-Class W245	W245	5	EU-MERCEDES-BENZ-B-KLASSE-W245-MPV-FACELIFT-01	MEDIUM	Ktype跨2008改款，改款后外廓。	READY
114993	114993	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-FACELIFT-01	HIGH	2014改款后外廓。	READY
59384_prefl	59384	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-PREFL-01	MEDIUM	Ktype跨2014改款，改款前外廓。	READY
59384_facelift	59384	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-FACELIFT-01	MEDIUM	Ktype跨2014改款，改款后外廓。	READY
18510_prefl	18510	MPV	B-Class W245	W245	5	EU-MERCEDES-BENZ-B-KLASSE-W245-MPV-PREFL-01	MEDIUM	Ktype跨2008改款，改款前外廓。	READY
18510_facelift	18510	MPV	B-Class W245	W245	5	EU-MERCEDES-BENZ-B-KLASSE-W245-MPV-FACELIFT-01	MEDIUM	Ktype跨2008改款，改款后外廓。	READY
12171_prefl	12171	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-PREFL-01	MEDIUM	Ktype跨2014改款，改款前外廓。	READY
12171_facelift	12171	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-FACELIFT-01	MEDIUM	Ktype跨2014改款，改款后外廓。	READY
12173	12173	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-PREFL-01	HIGH	2014改款前外廓。	READY
18507_prefl	18507	MPV	B-Class W245	W245	5	EU-MERCEDES-BENZ-B-KLASSE-W245-MPV-PREFL-01	MEDIUM	Ktype跨2008改款，改款前外廓。	READY
18507_facelift	18507	MPV	B-Class W245	W245	5	EU-MERCEDES-BENZ-B-KLASSE-W245-MPV-FACELIFT-01	MEDIUM	Ktype跨2008改款，改款后外廓。	READY
107068	107068	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-PREFL-01	HIGH	2014改款前外廓。	READY
59438_prefl	59438	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-PREFL-01	MEDIUM	Ktype跨2014改款，改款前外廓。	READY
59438_facelift	59438	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-FACELIFT-01	MEDIUM	Ktype跨2014改款，改款后外廓。	READY
142492	142492	MPV	B-Class W247	W247	5	EU-MERCEDES-BENZ-B-KLASSE-W247-MPV-01	HIGH	2022改款前外廓。	READY
12172_prefl	12172	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-PREFL-01	MEDIUM	Ktype跨2014改款，改款前外廓。	READY
12172_facelift	12172	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-FACELIFT-01	MEDIUM	Ktype跨2014改款，改款后外廓。	READY
18511_prefl	18511	MPV	B-Class W245	W245	5	EU-MERCEDES-BENZ-B-KLASSE-W245-MPV-PREFL-01	MEDIUM	Ktype跨2008改款，改款前外廓。	READY
18511_facelift	18511	MPV	B-Class W245	W245	5	EU-MERCEDES-BENZ-B-KLASSE-W245-MPV-FACELIFT-01	MEDIUM	Ktype跨2008改款，改款后外廓。	READY
142493	142493	MPV	B-Class W247	W247	5	EU-MERCEDES-BENZ-B-KLASSE-W247-MPV-01	HIGH	2022改款前外廓。	READY
12174	12174	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-PREFL-01	HIGH	2014改款前外廓。	READY
18508_prefl	18508	MPV	B-Class W245	W245	5	EU-MERCEDES-BENZ-B-KLASSE-W245-MPV-PREFL-01	MEDIUM	Ktype跨2008改款，改款前外廓。	READY
18508_facelift	18508	MPV	B-Class W245	W245	5	EU-MERCEDES-BENZ-B-KLASSE-W245-MPV-FACELIFT-01	MEDIUM	Ktype跨2008改款，改款后外廓。	READY
54958_prefl	54958	MPV	B-Class W245	W245	5	EU-MERCEDES-BENZ-B-KLASSE-W245-MPV-PREFL-01	MEDIUM	Ktype跨2008改款，改款前外廓。	READY
54958_facelift	54958	MPV	B-Class W245	W245	5	EU-MERCEDES-BENZ-B-KLASSE-W245-MPV-FACELIFT-01	MEDIUM	Ktype跨2008改款，改款后外廓。	READY
107895	107895	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-FACELIFT-01	HIGH	2014改款后外廓。	READY
107896	107896	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-FACELIFT-01	HIGH	2014改款后外廓。	READY
57257_prefl	57257	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-PREFL-01	MEDIUM	Ktype跨2014改款，改款前标准外廓。	READY
57257_facelift	57257	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-NATURAL-GAS-MPV-01	MEDIUM	Ktype跨2014改款，改款后Natural Gas Drive外廓。	READY
18512_prefl	18512	MPV	B-Class W245	W245	5	EU-MERCEDES-BENZ-B-KLASSE-W245-MPV-PREFL-01	MEDIUM	Ktype跨2008改款，改款前外廓。	READY
18512_facelift	18512	MPV	B-Class W245	W245	5	EU-MERCEDES-BENZ-B-KLASSE-W245-MPV-FACELIFT-01	MEDIUM	Ktype跨2008改款，改款后外廓。	READY
57292_prefl	57292	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-PREFL-01	MEDIUM	Ktype跨2014改款，改款前外廓。	READY
57292_facelift	57292	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-FACELIFT-01	MEDIUM	Ktype跨2014改款，改款后外廓。	READY
100550_prefl	100550	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-PREFL-01	MEDIUM	Ktype跨2014改款，改款前外廓。	READY
100550_facelift	100550	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-FACELIFT-01	MEDIUM	Ktype跨2014改款，改款后外廓。	READY
107954	107954	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-FACELIFT-01	HIGH	2014改款后外廓。	READY
107955	107955	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-FACELIFT-01	HIGH	2014改款后外廓。	READY
55581_prefl	55581	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-PREFL-01	MEDIUM	Ktype跨2014改款，改款前外廓。	READY
55581_facelift	55581	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-FACELIFT-01	MEDIUM	Ktype跨2014改款，改款后外廓。	READY
107894	107894	MPV	B-Class W246	W246	5	EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-FACELIFT-01	HIGH	2014改款后外廓。	READY
108181	108181	MPV	B-Class W242	W242	5	EU-MERCEDES-BENZ-B-KLASSE-W242-ELECTRIC-MPV-01	HIGH	Electric Drive独立W242外廓。	READY
109338	109338	MPV	B-Class W242	W242	5	EU-MERCEDES-BENZ-B-KLASSE-W242-ELECTRIC-MPV-01	HIGH	Electric Drive独立W242外廓。	READY
116938	116938	Coupe	C-Class C205	C205	2	EU-MERCEDES-BENZ-C-KLASSE-C205-COUPE-FACELIFT-01	HIGH	C205 Coupe标准外廓；跨改款尺寸未变。	READY
120121	120121	Convertible	C-Class A205	A205	2	EU-MERCEDES-BENZ-C-KLASSE-A205-CONVERTIBLE-FACELIFT-01	HIGH	A205 Cabriolet标准外廓；跨改款尺寸未变。	READY
```

## 本轮新增/修改的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-MERCEDES-BENZ-AMG-GT-C190-GTC-COUPE-PREFL-01	4551	2007	1284	Automobile-Catalog 2018 Mercedes-AMG GT C	https://www.automobile-catalog.com/car/2018/2727245/mercedes-amg_gt_c.html
EU-MERCEDES-BENZ-AMG-GT-C190-GTC-COUPE-FACELIFT-01	4551	2007	1288	Automobile-Catalog 2019 Mercedes-AMG GT C	https://www.automobile-catalog.com/car/2019/2874860/mercedes-amg_gt_c.html
EU-MERCEDES-BENZ-AMG-GT-C190-GTR-COUPE-01	4551	2007	1284	Automobile-Catalog 2018 Mercedes-AMG GT R	https://www.automobile-catalog.com/car/2018/2453675/mercedes-amg_gt_r.html
EU-MERCEDES-BENZ-AMG-GT-R190-GT-ROADSTER-01	4544	1939	1259	Automobile-Catalog 2018 Mercedes-AMG GT Roadster	https://www.automobile-catalog.com/car/2018/2504705/mercedes-amg_gt_roadster.html
EU-MERCEDES-BENZ-AMG-GT-R190-GTC-ROADSTER-PREFL-01	4551	2007	1259	Automobile-Catalog 2017 Mercedes-AMG GT C Roadster	https://www.automobile-catalog.com/car/2017/2504720/mercedes-amg_gt_c_roadster.html
EU-MERCEDES-BENZ-AMG-GT-R190-GTC-ROADSTER-FACELIFT-01	4551	2007	1260	Automobile-Catalog 2019 Mercedes-AMG GT C Roadster	https://www.automobile-catalog.com/car/2019/2874950/mercedes-amg_gt_c_roadster.html
EU-MERCEDES-BENZ-B-KLASSE-W245-MPV-PREFL-01	4270	1777	1604	Auto-Data.net Mercedes-Benz B-class (W245) B 200	https://www.auto-data.net/en/mercedes-benz-b-class-w245-b-200-136hp-12513
EU-MERCEDES-BENZ-B-KLASSE-W245-MPV-FACELIFT-01	4273	1777	1604	Auto-Data.net Mercedes-Benz B-class (W245 facelift 2008) B 200	https://www.auto-data.net/en/mercedes-benz-b-class-w245-facelift-2008-b-200-136hp-12514
EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-PREFL-01	4359	1786	1557	Auto-Data.net Mercedes-Benz B-class (W246) B 180; km77 Mercedes-Benz B 200 Natural Gas Drive (2012-2014)	https://www.auto-data.net/en/mercedes-benz-b-class-w246-b-180-122hp-7g-dct-18831; https://www.km77.com/coches/mercedes/clase-b/2012/estandar/estandar/b-200-natural-gas-drive/datos
EU-MERCEDES-BENZ-B-KLASSE-W246-MPV-FACELIFT-01	4393	1786	1557	Auto-Data.net Mercedes-Benz B-class (W246 facelift 2014) B 160	https://www.auto-data.net/en/mercedes-benz-b-class-w246-facelift-2014-b-160-102hp-dct-27014
EU-MERCEDES-BENZ-B-KLASSE-W246-NATURAL-GAS-MPV-01	4359	1812	1590	Auto-Data.net Mercedes-Benz B-class (W246 facelift 2014) B 200 Natural Gas Drive	https://www.auto-data.net/en/mercedes-benz-b-class-w246-facelift-2014-b-200-156hp-natural-gas-drive-dct-20899
EU-MERCEDES-BENZ-B-KLASSE-W242-ELECTRIC-MPV-01	4358	1812	1599	Auto-Data.net Mercedes-Benz B-class Electric Drive (W242) B 250 e	https://www.auto-data.net/en/mercedes-benz-b-class-electric-drive-w242-b-250-e-31-kwh-180hp-20827
```

## 下一步优先处理

1. 按 W415、W420 聚类 Citan、Citan Mixto、Citan Tourer 与 eCitan，确认 Van/MPV、标准轴距/长轴距及代际边界。
2. 集中处理 C-Class 的 W203/CL203/S203、W204/S204/C204、W205/S205/C205/A205、W206/S206 与 AMG 外廓，优先复用已有 C-Class 缓存。
3. 补齐 B-Class F-Cell，并解决 W247 2022 改款后车型的不含后视镜宽度和驱动高度口径。

推进信号：CONTINUE

[1]: https://www.automobile-catalog.com/car/2018/2504705/mercedes-amg_gt_roadster.html?utm_source=chatgpt.com "2018 Mercedes-AMG GT Roadster Specs Review (350 kW / 476 PS / 469 hp) (until September 2018 for Europe North America worldwide)"
[2]: https://www.km77.com/coches/mercedes/clase-b/2012/estandar/estandar/b-200-natural-gas-drive/datos "Mercedes-Benz B 200 Natural Gas Drive (2012-2014) | Precio y ficha técnica - km77.com"
[3]: https://www.automobile-catalog.com/car/2016/2505545/mercedes-benz_b_250_e_electric_drive.html?utm_source=chatgpt.com "2016 Mercedes-Benz B 250 e Electric Drive (aut. 1)"
[4]: https://www.mercedes-benz.com.sg/passengercars/services/manuals.html/b-class-hatchback-2023-01-w247-mbux/vehicle-data/vehicle-dimensions?srsltid=AfmBOoose-RtA7Rk6h_pK7Gbw87mD3IlgMpFLE5JEZooNR5D9UuwqVg7&utm_source=chatgpt.com "B-Class Hatchback January 2023 W247 MBUX"


--- 发送 / 继续到 Round 2 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- left18448_9301-9400_ktype_dimension_mapping_final.tsv
- left18448_9301-9400_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- Round 2 / 下一步 ---
## 更新点

* 本轮闭合 9 个 Ktype，覆盖 W206/S206 的 C 180、AMG C 43 与 AMG C 63 S E Performance 轿车及旅行车外廓。
* AMG C 43 在 2024 年更新后长度、宽度不变，但 Sedan 高度由 1450 mm 变为 1437 mm，Wagon 高度由 1466 mm 变为 1454 mm，因此分别建立改款前、改款后尺寸组。([汽车数据网][1])
* AMG C 63 S E Performance 的 W206 与 S206 已按不同车身高度独立建组；C 180 标准 Sedan/Wagon 同样分组。([汽车数据网][2])
* 历史索引中的 W205/S205 既有尺寸组保持不变，本轮未重复输出。

## 当前批次进度

* 输入 Ktype：100
* READY 映射：63 行
* 已覆盖 Ktype：46
* PENDING Ktype：54
* 已确认尺寸组：24
* 本轮新增 READY：9 行
* 本轮新增尺寸组：8
* 当前批次尚未完成。

## 本轮新增/修改的 Ktype 映射 TSV

```tsv
id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus
158612	158612	Sedan	C-Class W206	W206	4	EU-MERCEDES-BENZ-C-KLASSE-W206-AMG-C43-SEDAN-FACELIFT-01	HIGH	2024更新后AMG C 43外廓。	READY
800858	800858	Wagon	C-Class S206	S206	5	EU-MERCEDES-BENZ-C-KLASSE-S206-AMG-C43-WAGON-FACELIFT-01	HIGH	2024更新后AMG C 43外廓。	READY
800859	800859	Wagon	C-Class S206	S206	5	EU-MERCEDES-BENZ-C-KLASSE-S206-AMG-C43-WAGON-FACELIFT-01	HIGH	2024更新后AMG C 43外廓。	READY
147481	147481	Wagon	C-Class S206	S206	5	EU-MERCEDES-BENZ-C-KLASSE-S206-AMG-C43-WAGON-PREFL-01	HIGH	2024更新前AMG C 43外廓。	READY
147483	147483	Sedan	C-Class W206	W206	4	EU-MERCEDES-BENZ-C-KLASSE-W206-AMG-C43-SEDAN-PREFL-01	HIGH	2024更新前AMG C 43外廓。	READY
150717	150717	Sedan	C-Class W206	W206	4	EU-MERCEDES-BENZ-C-KLASSE-W206-AMG-C63-S-E-PERFORMANCE-SEDAN-01	HIGH	AMG C 63 S E Performance宽体外廓。	READY
150719	150719	Wagon	C-Class S206	S206	5	EU-MERCEDES-BENZ-C-KLASSE-S206-AMG-C63-S-E-PERFORMANCE-WAGON-01	HIGH	AMG C 63 S E Performance宽体外廓。	READY
143576	143576	Sedan	C-Class W206	W206	4	EU-MERCEDES-BENZ-C-KLASSE-W206-SEDAN-01	HIGH	W206标准Sedan外廓。	READY
145151	145151	Wagon	C-Class S206	S206	5	EU-MERCEDES-BENZ-C-KLASSE-S206-WAGON-01	HIGH	S206标准Wagon外廓。	READY
```

## 本轮新增/修改的 DIMENSION_GROUP TSV

```tsv
DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL
EU-MERCEDES-BENZ-C-KLASSE-W206-AMG-C43-SEDAN-FACELIFT-01	4791	1824	1437	Auto-Data.net Mercedes-Benz C-class W206 AMG C 43 421 Hp	https://www.auto-data.net/en/mercedes-benz-c-class-w206-amg-c-43-421hp-eq-boost-4matic-amg-speedshift-mct-9g-52979
EU-MERCEDES-BENZ-C-KLASSE-S206-AMG-C43-WAGON-FACELIFT-01	4793	1824	1454	Auto-Data.net Mercedes-Benz C-class S206 AMG C 43 421 Hp	https://www.auto-data.net/en/mercedes-benz-c-class-t-modell-s206-amg-c-43-421hp-eq-boost-4matic-amg-speedshift-mct-9g-52981
EU-MERCEDES-BENZ-C-KLASSE-S206-AMG-C43-WAGON-PREFL-01	4793	1824	1466	Auto-Data.net Mercedes-Benz C-class S206 AMG C 43 408 Hp	https://www.auto-data.net/en/mercedes-benz-c-class-t-modell-s206-amg-c-43-408hp-eq-boost-4matic-amg-speedshift-mct-9g-45711
EU-MERCEDES-BENZ-C-KLASSE-W206-AMG-C43-SEDAN-PREFL-01	4791	1824	1450	Auto-Data.net Mercedes-Benz C-class W206 AMG C 43 408 Hp	https://www.auto-data.net/en/mercedes-benz-c-class-w206-amg-c-43-408hp-eq-boost-4matic-amg-speedshift-mct-9g-45710
EU-MERCEDES-BENZ-C-KLASSE-W206-AMG-C63-S-E-PERFORMANCE-SEDAN-01	4842	1900	1458	Auto-Data.net Mercedes-Benz C-class W206 AMG C 63 S E Performance	https://www.auto-data.net/en/mercedes-benz-c-class-w206-amg-c-63-s-e-performance-680hp-plug-in-hybrid-4matic-amg-speedshift-mct-9g-46524
EU-MERCEDES-BENZ-C-KLASSE-S206-AMG-C63-S-E-PERFORMANCE-WAGON-01	4842	1900	1474	Auto-Data.net Mercedes-Benz C-class S206 AMG C 63 S E Performance	https://www.auto-data.net/en/mercedes-benz-c-class-t-modell-s206-amg-c-63-s-e-performance-680hp-plug-in-hybrid-4matic-amg-speedshift-mct-9g-46525
EU-MERCEDES-BENZ-C-KLASSE-W206-SEDAN-01	4751	1820	1437	Auto-Data.net Mercedes-Benz C-class W206 C 180	https://www.auto-data.net/en/mercedes-benz-c-class-w206-c-180-170hp-eq-boost-9g-tronic-42343
EU-MERCEDES-BENZ-C-KLASSE-S206-WAGON-01	4751	1820	1455	Auto-Data.net Mercedes-Benz C-class S206 C 180	https://www.auto-data.net/en/mercedes-benz-c-class-t-modell-s206-c-180-170hp-eq-boost-9g-tronic-52235
```

## 下一步优先处理

1. 将 W205/S205 普通 C 160、C 180 与柴油版本批量关联既有尺寸组。
2. 闭合 W205/S205/C205/A205 AMG C 43、C 63 与 C 63 S 的宽体 Sedan、Wagon、Coupe、Cabriolet 外廓。
3. 随后处理 Citan W415/W420 的 Van、Mixto、Tourer、标准轴距与长轴距分支。

推进信号：CONTINUE

[1]: https://www.auto-data.net/en/mercedes-benz-c-class-w206-amg-c-43-408hp-eq-boost-4matic-amg-speedshift-mct-9g-45710 "Mercedes-Benz C-class (W206) AMG C 43 (408 Hp) EQ Boost 4MATIC AMG SPEEDSHIFT MCT 9G | Technical specs, data, fuel consumption, Dimensions"
[2]: https://www.auto-data.net/en/mercedes-benz-c-class-w206-amg-c-63-s-e-performance-680hp-plug-in-hybrid-4matic-amg-speedshift-mct-9g-46524 "Mercedes-Benz C-class (W206) AMG C 63 S E PERFORMANCE (680 Hp) Plug-in Hybrid 4MATIC+ AMG SPEEDSHIFT MCT 9G | Technical specs, data, fuel consumption, Dimensions"


--- 发送 / 继续到 Round 3 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- left18448_9301-9400_ktype_dimension_mapping_final.tsv
- left18448_9301-9400_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- 脚本异常 ---
异常: 已打开消息操作菜单，但没有找到【在新聊天中分支】。菜单可见项: 复制消息 | 分享提示 | 编辑消息 | 思考了 6m 34s | Mercedes-Benz
+2
Mercedes-Benz
+2 | 梅赛德斯-奔驰媒体
+2
Mercedes-Benz
+2 | 复制 | 复制 | 开始新对话 | 复制回复 | 喜欢 | 不喜欢 | 切换模型 | 更多操作 | 来源 来源 |  | 添加文件等 | 高 | 启动语音功能 | 今天，1:59


--- 脚本异常 ---
异常: 已打开消息操作菜单，但没有找到【在新聊天中分支】。菜单可见项: 无


--- 发送 / checkpoint 续跑到 Round 4 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- left18448_9301-9400_ktype_dimension_mapping_final.tsv
- left18448_9301-9400_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- 脚本异常 ---
异常: 未找到任何用户消息，无法执行分支（原因: no-user-turn）


--- 发送 / checkpoint 续跑到 Round 5 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- left18448_9301-9400_ktype_dimension_mapping_final.tsv
- left18448_9301-9400_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。


--- 对话分支 / Round 5 ---
触发原因：ChatGPT 对话长度上限
父对话：https://chatgpt.com/c/6a70b0eb-9074-83e8-b789-f7b55f7fb058
新分支：https://chatgpt.com/c/6a70b46b-9b3c-83e8-b7f9-e38347cb823e

--- Round 5 / checkpoint 续跑 ---
## 1) 更新点

* 已恢复并锁定目标批次 `left18448_9301-9400` 的最近可验证进度。
* 已排除其他行号批次及无关车罩适配数据，未混入当前批次。
* 本轮未恢复到可安全落表的完整原始行与累计缓存文件，因此未编造或覆盖既有映射。

## 2) 当前批次进度

* 输入 Ktype：100
* 已闭合 Ktype：50
* READY 映射行：68
* PENDING Ktype：50
* 已确认 DIMENSION_GROUP：19
* 当前 `PENDING ≠ 0`，不得进入 COMPLETE。

## 3) 本轮新增/修改的 Ktype 映射 TSV

无

## 4) 本轮首次创建/修正的 DIMENSION_GROUP TSV

无

## 5) 下一步优先处理

* 继续恢复并处理当前批次剩余 50 个 PENDING，仅对未命中缓存的物理车身簇补充资料。
* 优先队列：Alfa Romeo 147 普通版改款前后及 GTA、Alfa Romeo 33 第一代及 Sport Wagon 4×4、Abarth Ritmo、AC、Addax、Aixam。
* 已锁定的 19 个尺寸组只建立 Ktype 关联，不重复核对三维或来源。

推进信号：CONTINUE


--- 发送 / 继续到 Round 6 ---
继续当前批次并采用缓存优先模式。尺寸组只在首次创建或纠错时完整核对一次三维和来源；后续 Ktype 只判断关联哪个现有 DIMENSION_GROUP_ID，不重复抓取，不输出缓存来源或匹配理由。仍有 PENDING 时，CONTINUE 轮仅输出：1) 更新点；2) 当前批次进度；3) 本轮新增/修改的 Ktype 映射 TSV（无变化写“无”）；4) 本轮首次创建/修正的 DIMENSION_GROUP TSV（复用既有组不重复输出，无变化写“无”）；5) 下一步优先处理。若当前或上一轮进度已经是 PENDING=0，本轮不要继续检索或再次输出 CONTINUE，必须立刻汇总并输出两张最终完整 TSV、两个任务指定 sandbox 下载链接和“推进信号：COMPLETE”。执行顺序固定为：第一阶段优先消除 PENDING 并补齐会阻塞两张最终表的数据。检测到 PENDING=0 后，第二阶段最多只做一次轻量机械收尾：核对固定表头、id 与 DIMENSION_GROUP_ID 唯一、映射引用闭合、长宽高和来源非空、两个任务指定下载链接齐全。第二阶段不得重新逐车型、逐年份或逐来源做深度检索，不得为了提高置信度反复核对，也不得因非阻塞的排序或措辞问题继续多轮。PENDING=0 后的下一条回复必须直接输出两张最终完整 TSV、两个精确 sandbox 下载链接，并以“推进信号：COMPLETE”结束；不要再输出 CONTINUE。Ktype 映射 TSV 表头必须严格使用 requirement 指定的字段顺序：id	Ktype	NormalizedBodyStyle	Generation	BodyCode	Doors	DIMENSION_GROUP_ID	MatchConfidence	Notes	IterationStatus。另需维护完整 DIMENSION_GROUP TSV，表头固定为：DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	DimensionSource	SourceURL。缺少任一张表、任一映射引用的尺寸组，或尺寸组字段不完整时不得 COMPLETE。不要输出子车系匹配表。
【COMPLETE 下载文件硬性要求】
准备 COMPLETE 时，除两张完整内嵌 TSV 外，还必须创建并提供以下两个可点击 sandbox 下载链接，文件名必须完全一致：
- left18448_9301-9400_ktype_dimension_mapping_final.tsv
- left18448_9301-9400_dimension_groups_final.tsv
缺少任一下载链接时不得输出推进信号：COMPLETE。

