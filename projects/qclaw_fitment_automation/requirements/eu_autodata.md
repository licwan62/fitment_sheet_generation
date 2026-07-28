# EU Auto-Data Ktype 车型尺寸补全规则

本规则适用于以下 13 列、Tab 分隔的欧洲车型输入表。处理单位是输入行，唯一主键是 `Ktype`。

```tsv
Make	Model	VariantName	BodyStyle	DriveType	Energy	EngineOutputKW	EngineOutputHP	Product Start Month-Year	Product End Month-Year	LastProcessedDate	Ktype	LatestStatus
Opel	Corsa d	1.4	Schrägheck	Frontantrieb	Benzin	66	90	Jul 2006	Aug 2014	2024-03-01	1	NEW
```

<!-- fitment-data-contract
full_table:
  columns:
    - Make
    - Model
    - VariantName
    - BodyStyle
    - DriveType
    - Energy
    - EngineOutputKW
    - EngineOutputHP
    - Product Start Month-Year
    - Product End Month-Year
    - LastProcessedDate
    - Ktype
    - LatestStatus
    - NormalizedBodyStyle
    - Generation
    - BodyCode
    - Doors
    - WheelbaseMM
    - DIMENSION_GROUP_ID
    - LengthMM
    - WidthMM
    - HeightMM
    - WidthBasis
    - EndDateStatus
    - ResolutionStatus
    - CacheSourceKtype
    - MatchReason
    - MatchConfidence
    - DimensionSource
    - SourceURL
    - Notes
    - IterationStatus
  auto_empty_columns: []
subseries_match:
  enabled: false
  columns: []
  auto_empty_columns: []
-->

## 一、目标与输出粒度

每轮输出一张完整 TSV。输出表头必须严格使用上方 `full_table.columns` 的字段及顺序，不得增删、改名或调换。

输出采用适合当前自动化流程的扁平表：

- 一条输入记录对应一条输出记录。
- `Ktype` 是唯一主键；不得合并、删除、改写或重复。
- 输入的 13 个字段必须逐字保留，不能用查询结果覆盖源值。
- 查询和标准化结果只写入新增字段。
- 多个 Ktype 可以引用同一个 `DIMENSION_GROUP_ID`，但仍必须各自保留一行。
- 不输出子车系匹配表，不在同一回答中另建第二张或第三张 TSV。

`DIMENSION_GROUP_ID` 表示一套真实存在且经过确认的物理车身外轮廓。扁平表合并后，可按该字段拆出尺寸组表，并按 Ktype 的生产年月生成车型年份覆盖表。

## 二、输入字段解释

| 字段 | 处理规则 |
| --- | --- |
| Make | 原始品牌。查询时允许使用标准品牌写法，但输出原值不变。 |
| Model | 原始车型/车系，可能包含代际提示，例如 `Corsa d`、`Megane iii`。不得擅自删除罗马数字或字母。 |
| VariantName | 发动机或版本名称。用于区分 Ktype，不等于物理车身。 |
| BodyStyle | 原始德语或欧洲市场车身形式。原值保留，标准化结果写入 `NormalizedBodyStyle`。 |
| DriveType | 原始驱动形式。通常不单独决定尺寸组，但不能忽略可能影响车高的特殊底盘。 |
| Energy | 原始能源类型。通常不单独决定尺寸组。 |
| EngineOutputKW / EngineOutputHP | 原始功率，仅用于版本核验，不得作为尺寸组相同或不同的唯一依据。 |
| Product Start Month-Year | Ktype 的生产开始月，格式通常为 `MMM YYYY`。 |
| Product End Month-Year | Ktype 的生产结束月；`-`、空值或未知值不能解释为生产至今。 |
| LastProcessedDate | 上游处理日期，仅保留，不作为车型生产日期或资料发布日期。 |
| Ktype | 唯一主键。按文本处理，禁止转为浮点数或改写前导零。 |
| LatestStatus | 上游状态，仅保留；本轮结论写入 `IterationStatus`。 |

输入表必须按 Tab 解析。字段内容中的空格不是分隔符，`Product Start Month-Year` 和 `Product End Month-Year` 是单个字段。

## 三、标准化字段

### 1. NormalizedBodyStyle

保留 `BodyStyle` 原文，并按物理车身形式写入以下优先标准值：

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

### 2. Generation、BodyCode、Doors、WheelbaseMM

- `Generation`：正式代际名称，例如 `Corsa D`。不能仅从生产年份推断。
- `BodyCode`：厂商平台/车身代码；无可靠证据时留空。
- `Doors`：只写整数，例如 `3`、`5`；来源未明确时留空。
- `WheelbaseMM`：只写毫米数字，不写单位。不同轴距不能共用尺寸组。

不得把发动机代号、底盘配置或营销版本误写为 `BodyCode`。

## 四、尺寸字段与尺寸组

### 1. 统一口径

- `LengthMM`：量产标准状态下的最大车身外部长度，单位 mm。
- `WidthMM`：优先使用不含外后视镜的车身宽度，单位 mm。
- `HeightMM`：量产标准状态下的外部高度，单位 mm。
- 三个尺寸格中只写数字，不写 `mm`、约数符号、范围或多个候选值。
- 同一行的长、宽、高必须对应同一物理车身配置，不能从不同版本拼接。
- 英寸换算毫米时使用 `1 in = 25.4 mm`，最终取整到 1 mm，并在 `Notes` 标注换算。
- 厘米换算毫米时使用 `1 cm = 10 mm`。

### 2. WidthBasis

只允许以下值：

- `WITHOUT_MIRRORS`
- `WITH_MIRRORS`
- `UNKNOWN`

`WITH_MIRRORS` 或 `UNKNOWN` 不能标记为 `READY`，除非存在明确人工豁免；豁免必须写入 `Notes`。

### 3. DIMENSION_GROUP_ID

只有长、宽、高和物理车身边界均已确认后才能创建或命中尺寸组。ID 在当前批次及后续缓存中必须稳定，推荐格式：

```text
EU-{MAKE}-{MODEL}-{GENERATION}-{BODYSTYLE}-{SEQUENCE}
```

示例：

```text
EU-OPEL-CORSA-D-HATCHBACK-01
```

ID 中使用大写 ASCII、数字和连字符。不得把 Ktype 直接当作尺寸组 ID，也不得在证据不足时创建“临时确认”尺寸组。

以下差异通常不单独创建尺寸组：

- 发动机排量、功率、增压方式
- 燃料或能源类型
- 变速箱
- 不改变外部轮廓的驱动形式
- 普通配置等级

以下差异必须独立核对，存在差异时使用不同尺寸组：

- 不同代际或车身代码
- 不同 BodyStyle、门数且外形不同
- 不同轴距、SWB/LWB
- 普通车身/宽体、SRW/DRW
- 普通顶/高顶
- facelift 前后长宽高变化
- 不同 CAB/BED
- 特殊悬架高度、保险杠或外部套件
- 同名车型停产后重新推出

不得仅凭 `Make + Model + VariantName` 相似命中缓存。

## 五、生产日期与 EndDateStatus

月份使用英文三字母缩写：`Jan`、`Feb`、`Mar`、`Apr`、`May`、`Jun`、`Jul`、`Aug`、`Sep`、`Oct`、`Nov`、`Dec`。

`EndDateStatus` 只允许：

- `KNOWN`：输入或可靠来源给出明确结束年月。
- `STILL_IN_PRODUCTION`：可靠的当前官方资料确认仍在生产。
- `SOURCE_MISSING`：来源未提供结束时间。
- `UNKNOWN`：来源冲突或无法判断。

当 `Product End Month-Year` 为 `-` 或空值时：

- 不得自动补成当前年月或当前年份。
- 只有可靠官方资料明确仍在生产时，才能写 `STILL_IN_PRODUCTION`。
- 已确认停产且查到结束年月时，只在 `Notes` 记录补充值；不得覆盖输入原字段。
- 历史车型默认使用 `SOURCE_MISSING` 或 `UNKNOWN`，不得扩展到当前年份。

车型年份覆盖只能由有效生产月份展开。首尾年可视为覆盖年，但若同一年存在换代、改款或不同车身并行，必须保留对应尺寸组的实际月份边界，不能只按年份强行合并。

## 六、解析状态与缓存

`ResolutionStatus` 只允许：

- `DIRECT_NEW`：本次由可靠来源直接确认并创建新尺寸组。
- `CACHE_EXACT`：有直接证据确认与已有尺寸组完全相同。
- `CACHE_VERIFIED`：经过代际、车身代码、轴距或尺寸交叉核验后命中缓存。
- `MANUAL_OVERRIDE`：依据明确的人工决定；原因必须写入 `Notes`。
- `PENDING`：证据不足、来源冲突或关键字段缺失。

命中缓存时必须填写：

- `CacheSourceKtype`：提供已确认尺寸组的 Ktype。
- `MatchReason`：简洁说明相同代际、车身、轴距和尺寸等依据。
- `MatchConfidence`：只允许 `HIGH`、`MEDIUM`、`LOW`。

未命中缓存时 `CacheSourceKtype` 留空。`PENDING` 不得填写确定的 `DIMENSION_GROUP_ID`；可在 `Notes` 写候选 ID。

## 七、来源要求

来源优先级如下：

1. 厂商欧洲/国家官网、官方 brochure、technical specification、press kit、历史资料、homologation 或 type approval。
2. Auto-Data、Car.info、UltimateSpecs、Automobile-Catalog、Parkers。
3. 其他可信规格数据库，只用于交叉验证。

二手车广告、论坛、搜索摘要、AI 摘要和无出处聚合页只能作为线索，不能单独支撑 `DIRECT_NEW`、`CACHE_EXACT` 或最终 `READY`。

`DimensionSource` 填来源名称；`SourceURL` 填直接支持尺寸或车身判断的页面 URL。多个来源用分号分隔，并保持名称与 URL 顺序对应。不得填写搜索结果页 URL。

来源冲突时依次核对市场、年份、代际、BodyStyle、门数、轴距、含镜/不含镜和特殊版本；仍无法解决则使用 `PENDING`。

## 八、IterationStatus

`IterationStatus` 只允许：

- `READY`
- `PENDING: <具体原因>`

只有同时满足以下条件才能写 `READY`：

- Ktype 唯一且输入 13 列完整保留。
- Generation、NormalizedBodyStyle 及必要的物理车身边界已经确认。
- LengthMM、WidthMM、HeightMM 均有值且属于同一配置。
- WidthBasis 为 `WITHOUT_MIRRORS`。
- DIMENSION_GROUP_ID 和 ResolutionStatus 有效。
- 生产结束状态处理正确。
- 来源可追溯，无未解决冲突。

待处理原因必须具体，例如：

```text
PENDING: 缺少不含后视镜宽度
PENDING: Corsa D 三门与五门车长是否一致未确认
PENDING: Product End 缺失且无法确认是否停产
PENDING: 官方与 Auto-Data 高度冲突
```

不得只写 `待查`、`未完成`、`有问题` 或沿用输入的 `LatestStatus`。

## 九、每轮固定输出

每轮回答依次包含：

1. `更新点`
2. `当前批次进度`
3. `本轮更新后的全量 TSV`
4. 未完成时输出 `下一步优先处理`
5. 最后一行输出 `下一步` 或 `本批次完成`

全量 TSV 必须包含当前输入文件的全部 Ktype，保持原始顺序。不得只输出变化行，不得用“其余不变”代替完整数据。

未完成时：

````text
更新点
- ……

当前批次进度
- 已完成：……
- 待处理：……
- 当前批次尚未完成。

本轮更新后的全量 TSV

```tsv
Make	Model	VariantName	BodyStyle	DriveType	Energy	EngineOutputKW	EngineOutputHP	Product Start Month-Year	Product End Month-Year	LastProcessedDate	Ktype	LatestStatus	NormalizedBodyStyle	Generation	BodyCode	Doors	WheelbaseMM	DIMENSION_GROUP_ID	LengthMM	WidthMM	HeightMM	WidthBasis	EndDateStatus	ResolutionStatus	CacheSourceKtype	MatchReason	MatchConfidence	DimensionSource	SourceURL	Notes	IterationStatus
……
```

下一步优先处理
1. ……

下一步
……
````

全部完成时，仍需输出完整 TSV，最后一行改为：

```text
本批次完成
```

## 十、强制检查

提交每轮结果前逐项检查：

1. 表头是否严格为 32 列且顺序正确。
2. 数据行数是否与输入 Ktype 数相同。
3. 每个输入 Ktype 是否恰好出现一次。
4. 输入 13 列是否逐字保留。
5. 是否错误地将发动机或功率差异当成车身尺寸差异。
6. 是否错误地把不同代际、BodyStyle、轴距或宽体合并。
7. 长宽高是否来自同一配置并统一为 mm。
8. WidthBasis 是否明确。
9. 缓存命中是否有来源 Ktype、理由和置信度。
10. `-` 结束时间是否被错误解释为生产至今。
11. 每个 `READY` 是否有可追溯来源。
12. 是否保持输入顺序且未新增范围外车型。
