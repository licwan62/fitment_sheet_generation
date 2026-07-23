# Ktype、尺寸组与车型年份表规则

<!-- fitment-data-contract
full_table:
  columns:
    - 主车型
    - 年份区间
    - 结构
    - 对应尺码
    - 品牌
    - 前台车型
    - 排序依据车型
    - 子车系
    - 分类
    - 版本
    - 门数
    - 代际
    - 区间最小年份
    - 区间最大年份
    - max_length_in
    - max_width_in
    - max_height_in
    - max_length_cm
    - max_width_cm
    - max_height_cm
    - 驾驶室类型
    - 货斗长度_ft
    - 长度余量
    - 无尺码原因
    - 参考车型
    - 备注
    - 迭代状态
  auto_empty_columns:
    - 对应尺码
    - 排序依据车型
    - 子车系
    - 区间最小年份
    - 区间最大年份
    - max_length_cm
    - max_width_cm
    - max_height_cm
    - 长度余量
    - 无尺码原因
subseries_match:
  enabled: true
  columns:
    - Year
    - 主车型
    - 结构
    - 版本
    - 候选车型
    - 匹配数量
  auto_empty_columns:
    - 匹配数量
-->

## 一、数据模型

本任务使用三个相互关联的数据表：

1. KTYPE_DETAIL：以 Ktype 为主键的详细子车型表。
2. DIMENSION_GROUP：以 DIMENSION_GROUP_ID 为主键的物理车身尺寸表。
3. MODEL_BODY_YEAR：Make、Model、BodyStyle、Year 与 DIMENSION_GROUP_ID 的年份覆盖表。

数据关系为：

* 一个 Ktype 只能绑定一个最终确认的 DIMENSION_GROUP_ID。
* 一个 DIMENSION_GROUP_ID 可以被多个 Ktype 引用。
* 一个 DIMENSION_GROUP_ID 可以覆盖多个年份。
* 同一 Make、Model、BodyStyle、Year 可以存在多个不同的 DIMENSION_GROUP_ID。

## 二、Ktype 处理粒度

Ktype 是详细车型记录的唯一主键。

每一条 Ktype 记录都必须独立完成尺寸解析，不得因为发动机、功率或配置相似而跳过该记录。

尺寸解析任务以 Ktype 为最小处理粒度，但长宽高不以 Ktype 为单位重复存储。

每个 Ktype 必须获得以下结果之一：

* DIRECT_NEW
* CACHE_EXACT
* CACHE_VERIFIED
* MANUAL_OVERRIDE
* PENDING

## 三、尺寸存储粒度

车辆长宽高统一存储在 DIMENSION_GROUP 表中。

DIMENSION_GROUP_ID 表示一套经过确认的物理车身尺寸和外部轮廓。

多个 Ktype 在确认使用相同物理车身后，可以引用同一个 DIMENSION_GROUP_ID。

不得为了保留详细发动机版本而重复创建完全相同的尺寸记录。

不得为了减少尺寸记录而把不同物理车身绑定到同一个 DIMENSION_GROUP_ID。

## 四、缓存命中规则

处理一个 Ktype 时，应先搜索已有 DIMENSION_GROUP 缓存。

以下差异默认不单独创建尺寸组：

* 发动机排量
* 发动机功率
* 增压方式
* 燃料类型
* 变速箱
* 普通配置等级
* 不影响外部轮廓的驱动形式

以下信息一致并且不存在相反证据时，可以命中缓存：

* Make
* Model
* 代际或车身代码
* BodyStyle
* 生产阶段
* 门数
* 轴距
* SWB/LWB状态
* 普通车身/宽体状态
* 车顶类型
* CAB
* BED
* SRW/DRW状态

直接有充分证据证明属于同一物理车身时，填写：

CACHE_EXACT

需要经过代际、轴距、车身尺寸或外部轮廓核验后才能确认时，填写：

CACHE_VERIFIED

命中缓存时必须记录：

* DIMENSION_GROUP_ID
* CacheSourceKtype
* MatchReason
* MatchConfidence

## 五、不得命中缓存的情况

出现以下情况时，不得直接使用已有尺寸缓存：

* 不同代际
* 不同车身代码
* 不同 BodyStyle
* 不同轴距
* SWB 与 LWB
* 普通车身与宽体
* 普通顶与高顶
* 不同门数且车身尺寸不同
* facelift 前后尺寸变化
* 不同 CAB
* 不同 BED
* SRW 与 DRW
* 特殊悬架高度
* 特殊前后保险杠
* 同名车型停产后重新推出
* 无法确认是否属于同一物理车身

无法确认时必须填写：

PENDING

不得仅根据 Model 名称和 VariantName 相似自动命中缓存。

## 六、Ktype 原始版本保留

每一条输入 Ktype 记录都必须保留。

原始 VariantName 必须原样或标准化后保存在 KTYPE_DETAIL 中。

不同 Ktype 不得因为以下原因被删除或合并：

* 三维尺寸相同
* 仅发动机排量不同
* 仅发动机功率不同
* 仅增压方式不同
* 仅燃料类型不同
* 仅驱动形式不同
* 仅变速箱不同

多个 Ktype 可以共享 DIMENSION_GROUP_ID，但不得共享 Ktype 主键。

## 七、车型年份覆盖表

MODEL_BODY_YEAR 固定输出：

Make	Model	BodyStyle	Year	DIMENSION_GROUP_ID

唯一约束为：

Make + Model + BodyStyle + Year + DIMENSION_GROUP_ID

同一 Make、Model、BodyStyle、Year 存在不同代际、不同轴距、不同宽体或其他不同物理车身时，允许输出多个 DIMENSION_GROUP_ID。

连续年份可以从生产时间展开，但必须确认该物理车身在对应年份真实存在。

不得仅因为某个 Ktype 的生产区间较长，就把 DIMENSION_GROUP_ID 扩展到没有任何对应 Ktype 或车型证据的年份。

## 八、生产结束时间缺失

Product End Month-Year 为“-”时，不得自动解释为生产至今。

必须增加 EndDateStatus：

* KNOWN
* STILL_IN_PRODUCTION
* SOURCE_MISSING
* UNKNOWN

只有经过可靠来源确认仍在生产时，才能填写 STILL_IN_PRODUCTION。

历史车型的结束时间缺失，默认不得扩展至当前年份。

## 九、尺寸数据来源

尺寸查询优先使用欧洲市场资料：

第一优先级：

* 厂商欧洲官网
* 厂商国家官网
* 官方 brochure
* 官方 technical specification
* 官方 press kit
* 官方历史资料
* 官方 homologation 或 type approval 资料

第二优先级：

* Auto-Data
* Car.info
* UltimateSpecs
* Automobile-Catalog
* Parkers

已经命中可靠 DIMENSION_GROUP 缓存的 Ktype，不需要重复从网站抓取完整长宽高。

但必须完成缓存命中判断，并记录命中依据。
