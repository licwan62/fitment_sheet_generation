# Auto next transcript
开始时间：2026-06-25 14:15:08
发送内容：下一步


--- Round 1 / 手动初始 prompt 回复 ---
ChatGPT 说：下一步我直接补尺寸字段，子车系继续留空。先从最确定且影响大的缺口开始：A4 2009、A5 2008-2019、A7/S7、A8/S8、RS6/RS7、Q6/SQ6。下一步先补一版尺寸已落地的行。这版只放已经有较稳尺寸来源的车型，子车系 / 对应尺码 / 排序依据车型 / 长度余量 继续留空。
尺寸口径统一使用 width without mirrors。例如 Edmunds 的 2009 A4 Sedan 为 185.2 / 71.9 / 56.2 in，2008 A5 Coupe 为 182.1 / 73.0 / 54.0 in，2012 A7 为 195.6 / 75.2 / 55.9 in，2020 A8 为 208.7 / 76.6 / 58.6 in。Edmunds+3Edmunds+3Edmunds+3
tsv主车型	年份区间	结构	对应尺码	品牌	前台车型	排序依据车型	子车系	分类	版本	门数	代际	区间最小年份	区间最大年份	max_length_in	max_width_in	max_height_in	max_length_cm	max_width_cm	max_height_cm	驾驶室类型	货斗长度_ft	长度余量	无尺码原因	参考车型	备注	迭代状态Audi A4	2009	Sedan		Audi	A4			三厢车		4	gen4	2009	2009	185.2	71.9	56.2	470.4	182.6	142.7				2009 Audi A4 Sedan	A4/A4 Quattro 2009 回归；B8 起始年份缺口	已补尺寸Audi A5	2008-2017	Coupe		Audi	A5			跑车		2	gen1	2008	2017	182.1	73.0	54.0	462.5	185.4	137.2				2008/2012 Audi A5 Coupe	A5 Quattro 2008-2017 回归；Quattro 不作为版本	已补尺寸Audi A5	2010-2017	Convertible		Audi	A5			跑车		2	gen1	2010	2017	182.1	73.0	54.4	462.5	185.4	138.2				2010/2015 Audi A5 Cabriolet	A5 Cabriolet 单独结构；不要与 Coupe 强行合并	已补尺寸Audi A7	2012-2013	Sportback		Audi	A7			三厢车	Sportback	4	gen1	2012	2013	195.6	75.2	55.9	496.8	191.0	142.0				2012 Audi A7	A7 Quattro 2012-2013 回归；Sportback 作为结构/版本识别	已补尺寸Audi A8	2019-2024	Sedan		Audi	A8			三厢车	LWB	4	gen4	2019	2024	208.7	76.6	58.6	530.1	194.6	148.8				2020 Audi A8 L	美国优先按 A8 L/LWB 处理；A8 Quattro 2019-2024 回归	已补尺寸Audi RS6	2021-2024	Wagon		Audi	RS6			旅行车	Avant	4	gen4	2021	2024	196.7	76.8	58.6	499.6	195.1	148.8				2021/2024 Audi RS6 Avant	RS6 Avant 保留；Avant 为 Audi 高认知旅行车名称	已补尺寸Audi RS7	2026	Sportback		Audi	RS7			三厢车	Sportback	4	gen2	2026	2026	197.2	76.8	56.1	500.9	195.1	142.5				2021 Audi RS7	RS7 Sportback 2026 保留；同代尺寸可先参考 2021 口径	待复核2026Audi Q6 e-tron	2027	SUV		Audi	Q6 e-tron			越野车		4	gen1	2027	2027	187.8	76.3	66.6	477.0	193.8	169.2				2025/2027 Audi Q6 e-tron	2027 Q6 e-tron；同平台尺寸口径	已补尺寸Audi Q6 e-tron	2027	SUV		Audi	Q6 e-tron			越野车	Sportback	4	gen1	2027	2027	187.9	76.3	65.1	477.3	193.8	165.4				2025/2027 Audi Q6 Sportback e-tron	2027 Q6 Sportback e-tron；Sportback 版本	已补尺寸Audi SQ6 e-tron	2027	SUV		Audi	SQ6 e-tron			越野车		4	gen1	2027	2027	187.9	77.4	66.8	477.3	196.6	169.7				2027 Audi SQ6 e-tron	2027 SQ6 e-tron；高性能版宽度不同，单独保留	已补尺寸Audi SQ6 e-tron	2027	SUV		Audi	SQ6 e-tron			越野车	Sportback	4	gen1	2027	2027	187.9	77.4	65.1	477.3	196.6	165.4				2027 Audi SQ6 Sportback e-tron	2027 SQ6 Sportback e-tron；Sportback 高性能版	已补尺寸
RS6/RS7、Q6/SQ6 的尺寸依据：Edmunds 给出 2021 RS6 为 196.7 / 76.8 / 58.6 in，2021 RS7 为 197.2 / 76.8 / 56.1 in；Q6 e-tron 和 Q6 Sportback e-tron 分别为 187.8 / 76.3 / 66.6 in、187.9 / 76.3 / 65.1 in。Edmunds+3Edmunds+3Edmunds+3

下一批继续补这些
Audi A3 2022-2027Audi S3 2027Audi RS3 2027Audi A5 2018-2019 SportbackAudi A5 2025-2027Audi S5 2018-2019 SportbackAudi S5 2025 / 2027Audi RS5 2019 / 2025Audi S4 1992-1994 / 2009Audi S7 2013Audi S8 2020-2024Audi Q5 2027Audi Q5 Sportback 2025 / 2027Audi SQ5 2027Audi SQ5 Sportback 2025-2027
建议下一步优先处理 A5/S5/RS5 系列，因为它们最容易因为 Coupe、Convertible、Sportback、2025 新四门口径发生串行。


--- Round 2 / 下一步回复 ---
ChatGPT 说：我继续补第二批，重点处理 A5/S5/RS5 Sportback 与 S7/S8/S4，这批都是容易和普通版、性能版混淆的行。尺寸仍先按 without mirrors 口径，子车系继续留空。继续推进第二批：这批补 A5/S5/RS5 Sportback、新旧 A5/S5 2025+、S7、S8、S4 2009。
其中 子车系 / 对应尺码 / 排序依据车型 / 长度余量 继续留空，最后统一匹配。
注意一个修正：Audi S4 2009 不建议写 Sedan，美国口径更像 B7 末期 Convertible，Edmunds 2009 S4 页面尺寸为 180.0 / 70.0 / 54.8 in；B8 S4 Sedan 更适合从 2010 开始单独处理。Edmunds
tsv主车型	年份区间	结构	对应尺码	品牌	前台车型	排序依据车型	子车系	分类	版本	门数	代际	区间最小年份	区间最大年份	max_length_in	max_width_in	max_height_in	max_length_cm	max_width_cm	max_height_cm	驾驶室类型	货斗长度_ft	长度余量	无尺码原因	参考车型	备注	迭代状态Audi A5	2018-2019	Sportback		Audi	A5			三厢车	Sportback	4	gen2	2018	2019	186.3	72.6	54.6	473.2	184.4	138.7				2018 Audi A5 Sportback	A5 Sportback 2018-2019 回归；Sportback 放版本/结构，不放主车型	已补尺寸Audi A5	2025	Sportback		Audi	A5			三厢车	Sportback	4	gen2	2025	2025	187.3	72.6	55.0	475.7	184.4	139.7				2025 Audi A5 Sportback	2025 仍按旧 A5 Sportback 尺寸；不补 Coupe/Cabriolet	已补尺寸Audi A5	2026-2027	Sportback		Audi	A5			三厢车	Sportback	4	gen3	2026	2027	190.1	73.2	57.0	482.9	185.9	144.8				2026 Audi A5 Sportback	新一代 A5 四门/Sportback 口径；替代 A4 体系	已补尺寸Audi S5	2018-2019	Sportback		Audi	S5			三厢车	Sportback	4	gen2	2018	2019	186.3	72.6	54.6	473.2	184.4	138.7				2018 Audi S5 Sportback	S5 Sportback 2018-2019 回归；与 A5 Sportback 外廓接近	已补尺寸Audi S5	2025	Sportback		Audi	S5			三厢车	Sportback	4	gen2	2025	2025	187.2	72.6	54.6	475.5	184.4	138.7				2025 Audi S5 Sportback	2025 仍按旧 S5 Sportback；不补 Coupe/Cabriolet	已补尺寸Audi S5	2026-2027	Sportback		Audi	S5			三厢车	Sportback	4	gen3	2026	2027	190.3	73.2	56.5	483.4	185.9	143.5				2026 Audi S5 Sportback	新一代 S5 四门/Sportback 口径；2027 可先沿用同代	已补尺寸Audi RS5	2019	Sportback		Audi	RS5			三厢车	Sportback	4	gen2	2019	2019	188.3	73.5	54.6	478.3	186.7	138.7				2019 Audi RS5 Sportback	RS5 Sportback 2019 回归；性能版单独保留	已补尺寸Audi RS5	2025	Sportback		Audi	RS5			三厢车	Sportback	4	gen2	2025	2025	188.3	73.5	55.1	478.3	186.7	140.0				2025 Audi RS5 Sportback	2025 不补 Coupe/Cabriolet；按 Sportback 口径	已补尺寸Audi S7	2013	Sportback		Audi	S7			三厢车	Sportback	4	gen1	2013	2013	195.6	75.2	55.9	496.8	191.0	142.0				2013 Audi S7	S7 2013 缺口；与 A7 Sportback 外廓一致	已补尺寸Audi S8	2020-2024	Sedan		Audi	S8			三厢车	LWB	4	gen4	2020	2024	209.0	76.6	58.6	530.9	194.6	148.8				2020/2023 Audi S8	S8 性能版保留；美国长轴口径	已补尺寸Audi S4	2009	Convertible		Audi	S4			跑车		2	gen3	2009	2009	180.0	70.0	54.8	457.2	177.8	139.2				2009 Audi S4 Cabriolet	修正：2009 美国口径更适合按 B7 Convertible，不写 Sedan	已补尺寸
尺寸依据：2018 A5 Sportback 为 186.3 / 72.6 / 54.6 in；2025 A5 Sportback 有旧款 187.3 / 72.6 / 55.0 in 与新一代 190.1 / 73.2 / 57.0 in 两套口径，所以我拆成 2025 和 2026-2027；2025 S5 为 187.2 / 72.6 / 54.6 in，2026 S5 为 190.3 / 73.2 / 56.5 in；2019/2025 RS5 Sportback 分别参考 2019 和 2025 Edmunds 尺寸。Edmunds+6Car and Driver+6Edmunds+6
S7 2013 使用 Edmunds 的 195.6 / 75.2 / 55.9 in；S8 2020-2024 使用 2020/2023 S8 的 209.0 / 76.6 / 58.6 in，同代可先压缩。Edmunds+2Edmunds+2
下一步建议继续补这批：
Audi A3 2022-2027Audi S3 2027Audi RS3 2027Audi Q5 2027Audi Q5 Sportback 2025 / 2027Audi SQ5 2027Audi SQ5 Sportback 2025-2027Audi A6 2027Audi Q4 e-tron 2027 待确认
这里面优先级最高的是 Q5/SQ5 2025-2027，因为它也有新旧代切换风险。


--- Round 3 / 下一步回复 ---
ChatGPT 说：我继续第三批，优先处理 Q5/SQ5 这组，因为 2025-2027 有新旧代切换风险；A3/S3/RS3 和 A6/Q4 放下一批或待确认。继续推进第三批：Q5 / SQ5 / Q5 Sportback / SQ5 Sportback。
这批我建议这样处理：2025 Q5 仍是老一代尺寸，2025-2026 Q5 Sportback / SQ5 Sportback 使用 Sportback 尺寸；2027 Q5 / SQ5 先按数据库缺口保留为待补尺寸，因为我这轮没有拿到足够稳的 2027 Q5/SQ5 尺寸源，不建议硬沿用 2026。
tsv主车型	年份区间	结构	对应尺码	品牌	前台车型	排序依据车型	子车系	分类	版本	门数	代际	区间最小年份	区间最大年份	max_length_in	max_width_in	max_height_in	max_length_cm	max_width_cm	max_height_cm	驾驶室类型	货斗长度_ft	长度余量	无尺码原因	参考车型	备注	迭代状态Audi Q5	2025	SUV		Audi	Q5			越野车		4	gen2	2025	2025	184.3	74.5	65.5	468.1	189.2	166.4				2025 Audi Q5	2025 Q5 老一代尺寸；Q5 普通版补充	已补尺寸Audi Q5	2025-2026	SUV		Audi	Q5			越野车	Sportback	4	gen2	2025	2026	185.7	74.8	65.5	471.7	190.0	166.4				2025/2026 Audi Q5 Sportback	Q5 Sportback 回归；Sportback 放版本，不放主车型	已补尺寸Audi Q5	2027	SUV		Audi	Q5			越野车		4	gen3	2027	2027									2027 Audi Q5	2027 Q5 数据库缺口；新年款/新代风险，暂不沿用 2026 尺寸	待补尺寸Audi Q5	2027	SUV		Audi	Q5			越野车	Sportback	4	gen3	2027	2027									2027 Audi Q5 Sportback	2027 Q5 Sportback 数据库缺口；待尺寸确认	待补尺寸Audi SQ5	2025-2026	SUV		Audi	SQ5			越野车		4	gen2	2025	2026	185.7	74.8	65.8	471.7	190.0	167.1				2025/2026 Audi SQ5	SQ5 普通 SUV；性能版保留	已补尺寸Audi SQ5	2025-2026	SUV		Audi	SQ5			越野车	Sportback	4	gen2	2025	2026	185.7	74.8	65.5	471.7	190.0	166.4				2025/2026 Audi SQ5 Sportback	SQ5 Sportback 回归；Sportback 版本	已补尺寸Audi SQ5	2027	SUV		Audi	SQ5			越野车		4	gen3	2027	2027									2027 Audi SQ5	2027 SQ5 数据库缺口；待新年款尺寸确认	待补尺寸Audi SQ5	2027	SUV		Audi	SQ5			越野车	Sportback	4	gen3	2027	2027									2027 Audi SQ5 Sportback	2027 SQ5 Sportback 数据库缺口；待尺寸确认	待补尺寸
尺寸依据：Edmunds 给出的 2025 Q5 为 184.3 / 74.5 / 65.5 in；2025 Q5 Sportback 为 185.7 / 74.8 / 65.5 in；2025-2026 SQ5 为 185.7 / 74.8 / 65.8 in；2026 SQ5 Sportback 为 185.7 / 74.8 / 65.5 in。Edmunds+3Edmunds+3Edmunds+3
这里我把之前草稿里的：
Audi SQ5 Sportback 2025Audi SQ5 Sportback 2026-2027
修正为：
Audi SQ5 Sportback 2025-2026 已补尺寸Audi SQ5 Sportback 2027 待补尺寸
原因是 2025 和 2026 的 Edmunds 尺寸可以压缩，2027 没有稳尺寸源，不建议混在一起。
下一步继续补：
Audi A3 2022-2027Audi S3 2027Audi RS3 2027Audi A6 2027Audi Q4 e-tron 2027 待确认Audi S4 1992-1994 待核对Audi RS5 2011 / 2016 待核对


--- Round 4 / 下一步回复 ---
ChatGPT 说：我继续第四批，处理 A3/S3/RS3、A6 2027、Q4 e-tron 2027。这里会把 2027 新年款和美国是否应补分开，避免把数据库里的未来年款直接压进已确认尺寸行。继续推进第四批：A3 / S3 / RS3、A6 2027、Q4 e-tron 2027。
这一批我建议这样处理：


A3 / S3 / RS3 2027：可以补，但 2027 主要是内饰/配置更新，目前外廓尺寸可先沿用 2025-2026 同代尺寸；后续如 Edmunds 更新 2027 页面再复核。2027 A3/S3/RS3 更新已发布，但主要描述的是内饰屏幕和辅助驾驶更新。Car and Driver


A6 2027：要区分 A6 gas sedan 和 A6 Sportback e-tron。4afitment 的 A6 Quattro 2027 更可能指燃油 A6/A6 quattro，不要误写成 A6 e-tron。


Q4 e-tron 2027：可以补为待确认。Audi USA 当前页面仍明确列 2026 Q4 e-tron / Q4 Sportback e-tron，同时已列 2027 Q6、A6 Sportback e-tron 等；Car and Driver 已报道 2027 Q4 e-tron refresh，但美国官网主页面当前仍以 2026 Q4 为主。奥迪+1


tsv主车型	年份区间	结构	对应尺码	品牌	前台车型	排序依据车型	子车系	分类	版本	门数	代际	区间最小年份	区间最大年份	max_length_in	max_width_in	max_height_in	max_length_cm	max_width_cm	max_height_cm	驾驶室类型	货斗长度_ft	长度余量	无尺码原因	参考车型	备注	迭代状态Audi A3	2022-2027	Sedan		Audi	A3			三厢车		4	gen4	2022	2027	177.3	71.5	56.2	450.3	181.6	142.7				2025/2026 Audi A3 Sedan	A3 Quattro 2022-2027 回归；2027 暂沿用 2025-2026 同代外廓	已补尺寸Audi S3	2027	Sedan		Audi	S3			三厢车		4	gen4	2027	2027	177.4	71.5	55.7	450.6	181.6	141.5				2025/2026 Audi S3 Sedan	仅补 2027；早期 S3 不进美国全量表；2027 暂沿用 2025-2026 同代外廓	已补尺寸待复核2027Audi RS3	2027	Sedan		Audi	RS3			三厢车		4	gen4	2027	2027	178.5	72.9	54.8	453.4	185.2	139.2				2025/2026 Audi RS3 Sedan	RS3 性能版保留；宽度不同，不并入普通 A3/S3；2027 暂沿用 2025-2026 外廓	已补尺寸待复核2027Audi A6	2027	Sedan		Audi	A6			三厢车		4	gen6	2027	2027	196.8	73.8	57.4	499.9	187.5	145.8				2026 Audi A6 Sedan	A6 Quattro 2027 回归；暂按 2026 A6 燃油 Sedan 同代外廓，不写 A6 e-tron	已补尺寸待复核2027Audi Q4 e-tron	2027	SUV		Audi	Q4 e-tron			越野车		4	gen1	2027	2027	180.6	73.4	64.2	458.7	186.4	163.1				2026 Audi Q4 e-tron	2027 refresh 已有报道，但美国官网当前主页面仍列 2026；暂沿用 2026 外廓	已补尺寸待复核2027Audi Q4 e-tron	2027	SUV		Audi	Q4 e-tron			越野车	Sportback	4	gen1	2027	2027	180.6	73.4	63.5	458.7	186.4	161.3				2026 Audi Q4 Sportback e-tron	如后续数据库出现 Q4 Sportback e-tron 2027，可用此行；Sportback 版本	已补尺寸待复核2027
尺寸依据：


2026 A3：177.3 / 71.5 / 56.2 in。Edmunds


2026 S3：177.4 / 71.5 / 55.7 in。Edmunds


2026 RS3：178.5 / 72.9 / 54.8 in。Edmunds


2026 A6：196.8 / 73.8 / 57.4 in。Edmunds


2026 Q4 e-tron：180.6 / 73.4 / 64.2 in；2026 Q4 Sportback e-tron：180.6 / 73.4 / 63.5 in。Edmunds+1


这一批同步修正建议
之前草稿里有：
Audi A6 2027 Sedan gen6
现在建议备注里明确写：
A6 Quattro 2027 回归；暂按 2026 A6 燃油 Sedan 同代外廓，不写 A6 e-tron
因为 Audi USA 的 2027 电动车页面列的是 A6 Sportback e-tron，这和 4afitment 的 A6 Quattro 不是同一个口径。奥迪
剩余待处理
Audi S4 1992-1994Audi RS5 2011Audi RS5 2016
这三条不建议直接补。下一步如果继续，我会把它们作为历史/断档复核项处理：先判断美国是否存在，再判断是否应该补全量表，而不是直接补尺寸。


--- Round 5 / 下一步回复 ---
ChatGPT 说：我来处理最后的历史/断档复核项：S4 1992-1994、RS5 2011、RS5 2016。这里重点不是补尺寸，而是先判断美国全量表是否应收录。继续处理最后一批：S4 1992-1994、RS5 2011、RS5 2016。
结论先说：
Audi S4 1992-1994：建议补，但标记为历史口径/Ur-S4。Audi RS5 2011：美国站不补。Audi RS5 2016：美国站不补。
原因：


早期 S4 是 C4 平台，也就是常说的 Ur-S4 / Audi 100 S4，生产期覆盖 1991-1994，后续 1994 改名进入 A6/S6 体系。这个可以作为美国历史车型补，但备注必须写清楚是 Audi 100 S4 / Ur-S4，避免和后来的 A4-based S4 混淆。维基百科+1


RS5 第一代虽然 2010/2011 已在欧洲存在，但 Edmunds 明确说 2013 RS5 是“new to the United States”，也就是美国正式进入应从 2013 开始。Edmunds


Cars.com 明确列出 RS5 2016-2017 未生产，上一代是 2013-2015，所以 RS5 2016 不补。Cars.com



可补进全量表：S4 1992-1994
这里我建议只补 Sedan。如果你后面数据库明确有 S4 Avant 候选，再补 Wagon/Avant。当前 4afitment 给的是 Audi S4 1992-1994，没指定 Avant，先按美国主销 Sedan 更稳。
tsv主车型	年份区间	结构	对应尺码	品牌	前台车型	排序依据车型	子车系	分类	版本	门数	代际	区间最小年份	区间最大年份	max_length_in	max_width_in	max_height_in	max_length_cm	max_width_cm	max_height_cm	驾驶室类型	货斗长度_ft	长度余量	无尺码原因	参考车型	备注	迭代状态Audi S4	1992-1994	Sedan		Audi	S4			三厢车		4	gen0	1992	1994	188.2	70.3	56.3	478.0	178.6	143.0				1992-1994 Audi 100 S4 / Ur-S4	早期 S4 为 C4 Audi 100 S4/Ur-S4 历史口径；不要与 A4-based S4 混淆	已补尺寸
尺寸说明：这里用 C4 S4 Sedan 的 4780 / 1786 / 1430 mm 转换，约为 188.2 / 70.3 / 56.3 in。Auto-Data 对 C4 S4 Avant 给出的同代数据为 4790 / 1805 / 1454 mm，也说明这代 S4 与后来的 A4-based S4 不是同一车系口径。auto-data.net

不补进全量表：RS5 2011 / 2016
tsvmake	model	年份区间_断开	处理建议	原因Audi	RS5	2011	不补	RS5 2011 属欧洲/全球早期口径；美国正式进入应从 2013 年款开始Audi	RS5	2016	不补	Cars.com 明确列出 RS5 2016-2017 未生产；上一代为 2013-2015
如果你后面要补 RS5 美国完整历史，建议用这个口径：
RS5 Coupe：2013-2015；2018-2019；2021-2025RS5 Convertible：2013-2015RS5 Sportback：2019；2021-2025RS5 2016-2017：不补RS5 2020：美国缺口/不建议补，需按数据库实际确认

这批 Audi 未覆盖项处理到这里可以收口
目前处理结果可以分为三类：
1. 已补尺寸：A4、A5、A7、A8、S4、S5、S7、S8、RS5 Sportback、RS6、RS7、Q4、Q5、SQ5、Q6、SQ6、A3/S3/RS3、A62. 待复核未来年款：2027 Q5/SQ5、2027 A6、2027 Q4 e-tron、2027 A3/S3/RS33. 明确不补：A1、Q2、早期 A3、早期 S3、Q3 Quattro 2013-2014、RS5 2011、RS5 2016
下一步建议做一次最终汇总 TSV：把前面所有“已补/待复核但保留”的 Audi 行合并成一张完整可粘贴表，再单独附一张“不补清单”。


--- Round 6 / 下一步回复 ---
ChatGPT 说：我把前面几批结果合并成一张最终可粘贴 TSV，并单独列出“不补清单”。这一步主要是收口，方便你直接并入全量表。下面是 Audi 未覆盖项汇总版 v1，按你最新全量表格式整理。
对应尺码 / 排序依据车型 / 子车系 / 长度余量 继续留空，等最后统一匹配。
tsv主车型	年份区间	结构	对应尺码	品牌	前台车型	排序依据车型	子车系	分类	版本	门数	代际	区间最小年份	区间最大年份	max_length_in	max_width_in	max_height_in	max_length_cm	max_width_cm	max_height_cm	驾驶室类型	货斗长度_ft	长度余量	无尺码原因	参考车型	备注	迭代状态Audi A3	2022-2027	Sedan		Audi	A3			三厢车		4	gen4	2022	2027	177.3	71.5	56.2	450.3	181.6	142.7				2025/2026 Audi A3 Sedan	A3 Quattro 2022-2027 回归；2027 暂沿用 2025-2026 同代外廓	已补尺寸待复核2027Audi A4	2009	Sedan		Audi	A4			三厢车		4	gen4	2009	2009	185.2	71.9	56.2	470.4	182.6	142.7				2009 Audi A4 Sedan	A4/A4 Quattro 2009 回归；B8 起始年份缺口	已补尺寸Audi A5	2008-2017	Coupe		Audi	A5			跑车		2	gen1	2008	2017	182.1	73.0	54.0	462.5	185.4	137.2				2008/2012 Audi A5 Coupe	A5 Quattro 2008-2017 回归；Quattro 不作为版本	已补尺寸Audi A5	2010-2017	Convertible		Audi	A5			跑车		2	gen1	2010	2017	182.1	73.0	54.4	462.5	185.4	138.2				2010/2015 Audi A5 Cabriolet	A5 Cabriolet 单独结构；不要与 Coupe 强行合并	已补尺寸Audi A5	2018-2019	Sportback		Audi	A5			三厢车	Sportback	4	gen2	2018	2019	186.3	72.6	54.6	473.2	184.4	138.7				2018 Audi A5 Sportback	A5 Sportback 2018-2019 回归；Sportback 放版本/结构，不放主车型	已补尺寸Audi A5	2025	Sportback		Audi	A5			三厢车	Sportback	4	gen2	2025	2025	187.3	72.6	55.0	475.7	184.4	139.7				2025 Audi A5 Sportback	2025 仍按旧 A5 Sportback 尺寸；不补 Coupe/Cabriolet	已补尺寸Audi A5	2026-2027	Sportback		Audi	A5			三厢车	Sportback	4	gen3	2026	2027	190.1	73.2	57.0	482.9	185.9	144.8				2026 Audi A5 Sportback	新一代 A5 四门/Sportback 口径；替代 A4 体系	已补尺寸待复核2027Audi A6	2027	Sedan		Audi	A6			三厢车		4	gen6	2027	2027	196.8	73.8	57.4	499.9	187.5	145.8				2026 Audi A6 Sedan	A6 Quattro 2027 回归；暂按 2026 A6 燃油 Sedan 同代外廓，不写 A6 e-tron	已补尺寸待复核2027Audi A7	2012-2013	Sportback		Audi	A7			三厢车	Sportback	4	gen1	2012	2013	195.6	75.2	55.9	496.8	191.0	142.0				2012 Audi A7	A7 Quattro 2012-2013 回归；Sportback 作为结构/版本识别	已补尺寸Audi A8	2019-2024	Sedan		Audi	A8			三厢车	LWB	4	gen4	2019	2024	208.7	76.6	58.6	530.1	194.6	148.8				2020 Audi A8 L	美国优先按 A8 L/LWB 处理；A8 Quattro 2019-2024 回归	已补尺寸Audi Q4 e-tron	2027	SUV		Audi	Q4 e-tron			越野车		4	gen1	2027	2027	180.6	73.4	64.2	458.7	186.4	163.1				2026 Audi Q4 e-tron	2027 refresh 已有报道，但美国官网当前主页面仍列 2026；暂沿用 2026 外廓	已补尺寸待复核2027Audi Q4 e-tron	2027	SUV		Audi	Q4 e-tron			越野车	Sportback	4	gen1	2027	2027	180.6	73.4	63.5	458.7	186.4	161.3				2026 Audi Q4 Sportback e-tron	如后续数据库出现 Q4 Sportback e-tron 2027，可用此行；Sportback 版本	已补尺寸待复核2027Audi Q5	2025	SUV		Audi	Q5			越野车		4	gen2	2025	2025	184.3	74.5	65.5	468.1	189.2	166.4				2025 Audi Q5	2025 Q5 老一代尺寸；Q5 普通版补充	已补尺寸Audi Q5	2025-2026	SUV		Audi	Q5			越野车	Sportback	4	gen2	2025	2026	185.7	74.8	65.5	471.7	190.0	166.4				2025/2026 Audi Q5 Sportback	Q5 Sportback 回归；Sportback 放版本，不放主车型	已补尺寸Audi Q5	2027	SUV		Audi	Q5			越野车		4	gen3	2027	2027									2027 Audi Q5	2027 Q5 数据库缺口；新年款/新代风险，暂不沿用 2026 尺寸	待补尺寸Audi Q5	2027	SUV		Audi	Q5			越野车	Sportback	4	gen3	2027	2027									2027 Audi Q5 Sportback	2027 Q5 Sportback 数据库缺口；待尺寸确认	待补尺寸Audi Q6 e-tron	2027	SUV		Audi	Q6 e-tron			越野车		4	gen1	2027	2027	187.8	76.3	66.6	477.0	193.8	169.2				2025/2027 Audi Q6 e-tron	2027 Q6 e-tron；同平台尺寸口径	已补尺寸Audi Q6 e-tron	2027	SUV		Audi	Q6 e-tron			越野车	Sportback	4	gen1	2027	2027	187.9	76.3	65.1	477.3	193.8	165.4				2025/2027 Audi Q6 Sportback e-tron	2027 Q6 Sportback e-tron；Sportback 版本	已补尺寸Audi RS3	2027	Sedan		Audi	RS3			三厢车		4	gen4	2027	2027	178.5	72.9	54.8	453.4	185.2	139.2				2025/2026 Audi RS3 Sedan	RS3 性能版保留；宽度不同，不并入普通 A3/S3；2027 暂沿用 2025-2026 外廓	已补尺寸待复核2027Audi RS5	2019	Sportback		Audi	RS5			三厢车	Sportback	4	gen2	2019	2019	188.3	73.5	54.6	478.3	186.7	138.7				2019 Audi RS5 Sportback	RS5 Sportback 2019 回归；性能版单独保留	已补尺寸Audi RS5	2025	Sportback		Audi	RS5			三厢车	Sportback	4	gen2	2025	2025	188.3	73.5	55.1	478.3	186.7	140.0				2025 Audi RS5 Sportback	2025 不补 Coupe/Cabriolet；按 Sportback 口径	已补尺寸Audi RS6	2021-2024	Wagon		Audi	RS6			旅行车	Avant	4	gen4	2021	2024	196.7	76.8	58.6	499.6	195.1	148.8				2021/2024 Audi RS6 Avant	RS6 Avant 保留；Avant 为 Audi 高认知旅行车名称	已补尺寸Audi RS7	2026	Sportback		Audi	RS7			三厢车	Sportback	4	gen2	2026	2026	197.2	76.8	56.1	500.9	195.1	142.5				2021 Audi RS7	RS7 Sportback 2026 保留；同代尺寸可先参考 2021 口径	待复核2026Audi S3	2027	Sedan		Audi	S3			三厢车		4	gen4	2027	2027	177.4	71.5	55.7	450.6	181.6	141.5				2025/2026 Audi S3 Sedan	仅补 2027；早期 S3 不进美国全量表；2027 暂沿用 2025-2026 同代外廓	已补尺寸待复核2027Audi S4	1992-1994	Sedan		Audi	S4			三厢车		4	gen0	1992	1994	188.2	70.3	56.3	478.0	178.6	143.0				1992-1994 Audi 100 S4 / Ur-S4	早期 S4 为 C4 Audi 100 S4/Ur-S4 历史口径；不要与 A4-based S4 混淆	已补尺寸Audi S4	2009	Convertible		Audi	S4			跑车		2	gen3	2009	2009	180.0	70.0	54.8	457.2	177.8	139.2				2009 Audi S4 Cabriolet	修正：2009 美国口径更适合按 B7 Convertible，不写 Sedan	已补尺寸Audi S5	2018-2019	Sportback		Audi	S5			三厢车	Sportback	4	gen2	2018	2019	186.3	72.6	54.6	473.2	184.4	138.7				2018 Audi S5 Sportback	S5 Sportback 2018-2019 回归；与 A5 Sportback 外廓接近	已补尺寸Audi S5	2025	Sportback		Audi	S5			三厢车	Sportback	4	gen2	2025	2025	187.2	72.6	54.6	475.5	184.4	138.7				2025 Audi S5 Sportback	2025 仍按旧 S5 Sportback；不补 Coupe/Cabriolet	已补尺寸Audi S5	2026-2027	Sportback		Audi	S5			三厢车	Sportback	4	gen3	2026	2027	190.3	73.2	56.5	483.4	185.9	143.5				2026 Audi S5 Sportback	新一代 S5 四门/Sportback 口径；2027 可先沿用同代	已补尺寸待复核2027Audi S7	2013	Sportback		Audi	S7			三厢车	Sportback	4	gen1	2013	2013	195.6	75.2	55.9	496.8	191.0	142.0				2013 Audi S7	S7 2013 缺口；与 A7 Sportback 外廓一致	已补尺寸Audi S8	2020-2024	Sedan		Audi	S8			三厢车	LWB	4	gen4	2020	2024	209.0	76.6	58.6	530.9	194.6	148.8				2020/2023 Audi S8	S8 性能版保留；美国长轴口径	已补尺寸Audi SQ5	2025-2026	SUV		Audi	SQ5			越野车		4	gen2	2025	2026	185.7	74.8	65.8	471.7	190.0	167.1				2025/2026 Audi SQ5	SQ5 普通 SUV；性能版保留	已补尺寸Audi SQ5	2025-2026	SUV		Audi	SQ5			越野车	Sportback	4	gen2	2025	2026	185.7	74.8	65.5	471.7	190.0	166.4				2025/2026 Audi SQ5 Sportback	SQ5 Sportback 回归；Sportback 版本	已补尺寸Audi SQ5	2027	SUV		Audi	SQ5			越野车		4	gen3	2027	2027									2027 Audi SQ5	2027 SQ5 数据库缺口；待新年款尺寸确认	待补尺寸Audi SQ5	2027	SUV		Audi	SQ5			越野车	Sportback	4	gen3	2027	2027									2027 Audi SQ5 Sportback	2027 SQ5 Sportback 数据库缺口；待尺寸确认	待补尺寸Audi SQ6 e-tron	2027	SUV		Audi	SQ6 e-tron			越野车		4	gen1	2027	2027	187.9	77.4	66.8	477.3	196.6	169.7				2027 Audi SQ6 e-tron	2027 SQ6 e-tron；高性能版宽度不同，单独保留	已补尺寸Audi SQ6 e-tron	2027	SUV		Audi	SQ6 e-tron			越野车	Sportback	4	gen1	2027	2027	187.9	77.4	65.1	477.3	196.6	165.4				2027 Audi SQ6 Sportback e-tron	2027 SQ6 Sportback e-tron；Sportback 高性能版	已补尺寸

不补清单
这些不要并入美国全量表：
tsvmake	model	年份区间_断开	处理建议	原因Audi	A1	2011-2018; 2022-2026	不补	非美国主销车型Audi	Q2	2018-2020; 2026	不补	非美国主销车型Audi	A3	1998-2005	不补	美国站口径不建议从 1998 开始Audi	S3	2000-2004; 2008-2012; 2014	不补	早期 S3 不进美国全量表Audi	Q3 Quattro	2013-2014	不补	美国 Q3 早期年份可疑，且 Quattro 不作为主车型Audi	RS5	2011	不补	RS5 2011 属欧洲/全球早期口径；美国正式进入应从 2013 年款开始Audi	RS5	2016	不补	RS5 美国 2016 断档，不建议补

下一步建议
下一步可以开始做 子车系匹配准备表，但还不直接回填子车系。
建议先把这些全量补充行展开成：
Year	主车型	结构	版本	候选前台车型
然后用 4afitment 跑候选，最后再统一回填 子车系 / 对应尺码 / 长度余量。到目前为止，这段对话对你有帮助吗？


--- Round 7 / 下一步回复 ---
下一步做 子车系匹配准备表。

目标是从新版全量表生成这张中间表：

Year	主车型	结构	版本	前台车型	品牌	车型名	匹配主键

然后再拿这个表去匹配 4afitment 数据库，最后才回填 子车系 / 对应尺码 / 长度余量。

一、Power Query：全量表展开成逐年匹配准备表

假设你的全量表表名叫：

全量表

直接新建一个查询，粘贴下面代码：

powerquery
let
    源 = Excel.CurrentWorkbook(){[Name="全量表"]}[Content],

    更改类型 =
        Table.TransformColumnTypes(
            源,
            {
                {"主车型", type text},
                {"年份区间", type text},
                {"结构", type text},
                {"品牌", type text},
                {"前台车型", type text},
                {"版本", type text},
                {"区间最小年份", Int64.Type},
                {"区间最大年份", Int64.Type}
            }
        ),

    保留有效行 =
        Table.SelectRows(
            更改类型,
            each [主车型] <> null
                and Text.Trim([主车型]) <> ""
                and [区间最小年份] <> null
                and [区间最大年份] <> null
        ),

    添加年份列表 =
        Table.AddColumn(
            保留有效行,
            "Year",
            each {[区间最小年份]..[区间最大年份]},
            type list
        ),

    展开年份 =
        Table.ExpandListColumn(
            添加年份列表,
            "Year"
        ),

    添加车型名 =
        Table.AddColumn(
            展开年份,
            "车型名",
            each
                if [前台车型] <> null and Text.Trim([前台车型]) <> ""
                then Text.Trim([前台车型])
                else
                    let
                        car = Text.Trim([主车型]),
                        brand = Text.Trim([品牌])
                    in
                        if Text.StartsWith(car, brand & " ")
                        then Text.AfterDelimiter(car, brand & " ")
                        else car,
            type text
        ),

    添加匹配主键 =
        Table.AddColumn(
            添加车型名,
            "匹配主键",
            each
                Text.From([Year])
                & "|" & Text.Trim([品牌])
                & "|" & Text.Trim([车型名])
                & "|" & Text.Trim(if [结构] = null then "" else [结构])
                & "|" & Text.Trim(if [版本] = null then "" else [版本]),
            type text
        ),

    选择列 =
        Table.SelectColumns(
            添加匹配主键,
            {
                "Year",
                "主车型",
                "结构",
                "版本",
                "前台车型",
                "品牌",
                "车型名",
                "匹配主键"
            }
        ),

    排序 =
        Table.Sort(
            选择列,
            {
                {"品牌", Order.Ascending},
                {"车型名", Order.Ascending},
                {"Year", Order.Ascending},
                {"结构", Order.Ascending},
                {"版本", Order.Ascending}
            }
        )
in
    排序
二、针对 Audi 这批的匹配口径

匹配前要先标准化，不然 4afitment 会出现假未覆盖。

1. Quattro 不参与版本匹配

这些全部回归普通前台车型：

A3 Quattro  → A3
A4 Quattro  → A4
A5 Quattro  → A5
A6 Quattro  → A6
A7 Quattro  → A7
A8 Quattro  → A8
Q3 Quattro  → Q3

所以匹配时不要用：

品牌 = Audi
车型名 = A5 Quattro

而是用：

品牌 = Audi
车型名 = A5
备注/候选里允许 Quattro
2. Sportback 走版本或结构

全量表里这样写：

主车型 = Audi A5
结构 = Sportback
版本 = Sportback
前台车型 = A5

匹配数据库时允许命中：

Audi|A5 Sportback
Audi|A5

优先级：

A5 Sportback > A5

也就是说，子车系最后可以回填更精准的 Audi|A5 Sportback，但全量表主车型仍然保持 Audi A5。

3. Avant 走 Wagon / Avant

例如：

Audi RS6	2021-2024	Wagon	版本 Avant

匹配时优先找：

Audi|RS6 Avant

如果数据库没有，再看：

Audi|RS6
三、下一步匹配输出表建议格式

子车系匹配时建议输出这个表，而不是直接回填全量表：

Year	主车型	结构	版本	品牌	车型名	候选子车系	匹配数量	匹配状态	建议回填子车系	备注

示例：

tsv
Year	主车型	结构	版本	品牌	车型名	候选子车系	匹配数量	匹配状态	建议回填子车系	备注
2025	Audi A5	Sportback	Sportback	Audi	A5	Audi|A5 Sportback; Audi|A5	2	可匹配	Audi|A5 Sportback	Sportback 优先匹配精准子车系
2027	Audi Q6 e-tron	SUV		Audi	Q6 e-tron	Audi|Q6 e-tron	1	可匹配	Audi|Q6 e-tron	普通 SUV
2027	Audi Q6 e-tron	SUV	Sportback	Audi	Q6 e-tron	Audi|Q6 e-tron Sportback; Audi|Q6 e-tron	2	可匹配	Audi|Q6 e-tron Sportback	Sportback 优先
2021	Audi RS6	Wagon	Avant	Audi	RS6	Audi|RS6 Avant; Audi|RS6	2	可匹配	Audi|RS6 Avant	Avant 优先
四、后续真正回填规则

最后回填 子车系 时按这个优先级：

1. 完全命中 Brand|Model + Year + Sportback/Avant/特殊版
2. 命中 Brand|Model + Year + 普通车型
3. Quattro 命中时回归普通车型，不单独作为版本
4. 多候选时优先结构更精准的子车系
5. 普通版不得回填特殊版，例如 A5 普通行不要回填 RS5/S5
6. 特殊版可以回填自身子车系，例如 RS5 → Audi|RS5 Sportback
五、当前 Audi 子车系匹配优先级
Audi A3 Sedan        → Audi|A3
Audi S3 Sedan        → Audi|S3
Audi RS3 Sedan       → Audi|RS3
Audi A4 Sedan        → Audi|A4
Audi A5 Coupe        → Audi|A5
Audi A5 Convertible  → Audi|A5
Audi A5 Sportback    → Audi|A5 Sportback > Audi|A5
Audi S5 Sportback    → Audi|S5 Sportback > Audi|S5
Audi RS5 Sportback   → Audi|RS5 Sportback > Audi|RS5
Audi A6 Sedan        → Audi|A6
Audi A7 Sportback    → Audi|A7
Audi S7 Sportback    → Audi|S7
Audi A8 Sedan LWB    → Audi|A8
Audi S8 Sedan LWB    → Audi|S8
Audi Q4 e-tron       → Audi|Q4 e-tron
Audi Q5 SUV          → Audi|Q5
Audi Q5 Sportback    → Audi|Q5 Sportback > Audi|Q5
Audi SQ5 SUV         → Audi|SQ5
Audi SQ5 Sportback   → Audi|SQ5 Sportback > Audi|SQ5
Audi Q6 e-tron       → Audi|Q6 e-tron
Audi Q6 Sportback    → Audi|Q6 e-tron Sportback > Audi|Q6 e-tron
Audi SQ6 e-tron      → Audi|SQ6 e-tron
Audi SQ6 Sportback   → Audi|SQ6 e-tron Sportback > Audi|SQ6 e-tron
Audi RS6 Avant       → Audi|RS6 Avant > Audi|RS6
Audi RS7 Sportback   → Audi|RS7 Sportback > Audi|RS7

这样下一步就可以拿这个准备表去和 4afitment 的 MAKE / MODEL / YEAR / TYPE.1 / VERSION / SIZE.1 匹配了。


--- Round 8 / 下一步回复 ---
下面这一步是 子车系候选匹配表，但仍然不直接回填全量表。
输出结果用于检查：

Year	主车型	结构	版本	品牌	车型名	候选子车系	匹配数量	匹配状态	建议回填子车系	备注
Power Query：生成子车系候选匹配表

前提：

你的上一步查询叫：

子车系匹配准备表

4afitment 数据源在：

详细尺寸表.xlsx

里面有非皮卡、皮卡压缩表，列类似：

BRAND / MODEL / YEAR / TYPE.1 / VERSION / SIZE.1

完整代码如下：

powerquery
let
    // 1. 读取匹配准备表
    准备表 = 子车系匹配准备表,

    准备表类型 =
        Table.TransformColumnTypes(
            准备表,
            {
                {"Year", Int64.Type},
                {"主车型", type text},
                {"结构", type text},
                {"版本", type text},
                {"品牌", type text},
                {"车型名", type text}
            }
        ),

    // 2. 读取 4afitment 数据源
    源 =
        Excel.Workbook(
            File.Contents("C:\Users\hzwlc\WPSDrive\345116921\WPS云盘\共享文件夹 \杭州海局贸易有限公司\运营部-302-周报月报年报\王力成\数据源\详细尺寸表.xlsx"),
            null,
            true
        ),

    非皮卡源 = 源{[Item="非皮卡压缩表", Kind="Table"]}[Data],
    皮卡源 = 源{[Item="皮卡压缩表", Kind="Table"]}[Data],

    非皮卡列 =
        Table.SelectColumns(
            非皮卡源,
            {
                "BRAND",
                "MODEL",
                "YEAR",
                "TYPE.1",
                "VERSION",
                "SIZE.1"
            },
            MissingField.UseNull
        ),

    皮卡列 =
        Table.SelectColumns(
            皮卡源,
            {
                "BRAND",
                "MODEL",
                "YEAR",
                "TYPE.1",
                "VERSION",
                "SIZE.1"
            },
            MissingField.UseNull
        ),

    数据库合并 =
        Table.Combine(
            {
                非皮卡列,
                皮卡列
            }
        ),

    数据库类型 =
        Table.TransformColumnTypes(
            数据库合并,
            {
                {"BRAND", type text},
                {"MODEL", type text},
                {"YEAR", Int64.Type},
                {"TYPE.1", type text},
                {"VERSION", type text},
                {"SIZE.1", type text}
            }
        ),

    数据库有效 =
        Table.SelectRows(
            数据库类型,
            each [BRAND] <> null
                and Text.Trim([BRAND]) <> ""
                and [MODEL] <> null
                and Text.Trim([MODEL]) <> ""
                and [YEAR] <> null
                and [SIZE.1] <> "无可用尺码"
        ),

    // 3. 标准化准备表
    准备标准化 =
        Table.TransformColumns(
            准备表类型,
            {
                {"品牌", each if _ = null then "" else Text.Trim(_), type text},
                {"车型名", each if _ = null then "" else Text.Trim(_), type text},
                {"结构", each if _ = null then "" else Text.Trim(_), type text},
                {"版本", each if _ = null then "" else Text.Trim(_), type text}
            }
        ),

    添加匹配特征 =
        Table.AddColumn(
            准备标准化,
            "匹配特征",
            each
                let
                    s = Text.Lower([结构]),
                    v = Text.Lower([版本])
                in
                    if Text.Contains(s, "sportback") or Text.Contains(v, "sportback") then "Sportback"
                    else if Text.Contains(s, "wagon") or Text.Contains(v, "avant") then "Avant"
                    else if Text.Contains(s, "convertible") then "Convertible"
                    else if Text.Contains(s, "coupe") then "Coupe"
                    else if Text.Contains(s, "sedan") then "Sedan"
                    else if Text.Contains(s, "suv") then "SUV"
                    else "",
            type text
        ),

    // 4. 标准化数据库
    数据库标准化 =
        Table.TransformColumns(
            数据库有效,
            {
                {"BRAND", each if _ = null then "" else Text.Trim(_), type text},
                {"MODEL", each if _ = null then "" else Text.Trim(_), type text},
                {"TYPE.1", each if _ = null then "" else Text.Trim(_), type text},
                {"VERSION", each if _ = null then "" else Text.Trim(_), type text},
                {"SIZE.1", each if _ = null then "" else Text.Trim(_), type text}
            }
        ),

    添加数据库特征 =
        Table.AddColumn(
            数据库标准化,
            "数据库特征",
            each
                let
                    m = Text.Lower([MODEL]),
                    t = Text.Lower([TYPE.1]),
                    v = Text.Lower([VERSION])
                in
                    if Text.Contains(m, "sportback") or Text.Contains(v, "sportback") then "Sportback"
                    else if Text.Contains(m, "avant") or Text.Contains(t, "wagon") or Text.Contains(v, "avant") then "Avant"
                    else if Text.Contains(t, "convertible") then "Convertible"
                    else if Text.Contains(t, "coupe") then "Coupe"
                    else if Text.Contains(t, "sedan") then "Sedan"
                    else if Text.Contains(t, "suv") then "SUV"
                    else "",
            type text
        ),

    // 5. 给准备表添加候选车型列表
    添加候选模型列表 =
        Table.AddColumn(
            添加匹配特征,
            "候选模型列表",
            each
                let
                    model = [车型名],
                    feature = [匹配特征]
                in
                    if feature = "Sportback" then
                        {
                            model & " Sportback",
                            model
                        }
                    else if feature = "Avant" then
                        {
                            model & " Avant",
                            model
                        }
                    else
                        {
                            model
                        },
            type list
        ),

    展开候选模型 =
        Table.ExpandListColumn(
            添加候选模型列表,
            "候选模型列表"
        ),

    重命名候选模型 =
        Table.RenameColumns(
            展开候选模型,
            {
                {"候选模型列表", "候选MODEL"}
            }
        ),

    // 6. 合并数据库
    合并数据库 =
        Table.NestedJoin(
            重命名候选模型,
            {
                "Year",
                "品牌",
                "候选MODEL"
            },
            添加数据库特征,
            {
                "YEAR",
                "BRAND",
                "MODEL"
            },
            "匹配到的数据库",
            JoinKind.LeftOuter
        ),

    展开数据库 =
        Table.ExpandTableColumn(
            合并数据库,
            "匹配到的数据库",
            {
                "BRAND",
                "MODEL",
                "YEAR",
                "TYPE.1",
                "VERSION",
                "SIZE.1",
                "数据库特征"
            },
            {
                "DB_BRAND",
                "DB_MODEL",
                "DB_YEAR",
                "DB_TYPE",
                "DB_VERSION",
                "DB_SIZE",
                "数据库特征"
            }
        ),

    // 7. 计算匹配优先级
    添加优先级 =
        Table.AddColumn(
            展开数据库,
            "匹配优先级",
            each
                if [DB_MODEL] = null then 999
                else if [匹配特征] = "Sportback" and Text.Contains(Text.Lower([DB_MODEL]), "sportback") then 1
                else if [匹配特征] = "Avant" and Text.Contains(Text.Lower([DB_MODEL]), "avant") then 1
                else if [匹配特征] <> "" and [匹配特征] = [数据库特征] then 2
                else if [匹配特征] = "" then 3
                else 5,
            Int64.Type
        ),

    // 8. 生成子车系字段
    添加子车系 =
        Table.AddColumn(
            添加优先级,
            "候选子车系单项",
            each
                if [DB_BRAND] = null or [DB_MODEL] = null
                then null
                else [DB_BRAND] & "|" & [DB_MODEL],
            type text
        ),

    // 9. 按原行聚合
    分组 =
        Table.Group(
            添加子车系,
            {
                "Year",
                "主车型",
                "结构",
                "版本",
                "品牌",
                "车型名"
            },
            {
                {
                    "候选子车系",
                    each
                        Text.Combine(
                            List.Sort(
                                List.Distinct(
                                    List.RemoveNulls([候选子车系单项])
                                )
                            ),
                            "; "
                        ),
                    type text
                },
                {
                    "匹配数量",
                    each
                        List.Count(
                            List.Distinct(
                                List.RemoveNulls([候选子车系单项])
                            )
                        ),
                    Int64.Type
                },
                {
                    "最小优先级",
                    each
                        List.Min(
                            List.RemoveNulls([匹配优先级])
                        ),
                    Int64.Type
                },
                {
                    "建议回填子车系",
                    each
                        let
                            有效行 = Table.SelectRows(_, each [候选子车系单项] <> null),
                            排序行 = Table.Sort(有效行, {{"匹配优先级", Order.Ascending}, {"DB_MODEL", Order.Ascending}}),
                            第一行 = if Table.RowCount(排序行) = 0 then null else 排序行{0}[候选子车系单项]
                        in
                            第一行,
                    type text
                }
            }
        ),

    添加匹配状态 =
        Table.AddColumn(
            分组,
            "匹配状态",
            each
                if [匹配数量] = 0 then "未匹配"
                else if [匹配数量] = 1 then "唯一匹配"
                else "多候选",
            type text
        ),

    添加备注 =
        Table.AddColumn(
            添加匹配状态,
            "备注",
            each
                if [匹配数量] = 0 then
                    "未在 4afitment 数据库中找到候选"
                else if [匹配数量] = 1 then
                    "可直接回填"
                else if [最小优先级] = 1 then
                    "多候选，但存在精准 Sportback/Avant 命中，建议优先回填精准子车系"
                else
                    "多候选，需要人工确认是否回填普通车型或特殊车型",
            type text
        ),

    选择列 =
        Table.SelectColumns(
            添加备注,
            {
                "Year",
                "主车型",
                "结构",
                "版本",
                "品牌",
                "车型名",
                "候选子车系",
                "匹配数量",
                "匹配状态",
                "建议回填子车系",
                "备注"
            }
        ),

    排序 =
        Table.Sort(
            选择列,
            {
                {"品牌", Order.Ascending},
                {"车型名", Order.Ascending},
                {"Year", Order.Ascending},
                {"结构", Order.Ascending},
                {"版本", Order.Ascending}
            }
        )
in
    排序
这段代码的匹配逻辑
1. 普通车型

例如：

Audi A4 2009 Sedan

只匹配：

Audi|A4

不会去匹配：

Audi|S4
Audi|RS4
Audi|A4 Quattro
2. Sportback

例如：

Audi A5 2025 Sportback

会优先尝试：

Audi|A5 Sportback

然后再允许：

Audi|A5

最终 建议回填子车系 会优先给：

Audi|A5 Sportback
3. Avant / Wagon

例如：

Audi RS6 2021 Wagon / Avant

会优先尝试：

Audi|RS6 Avant

再允许：

Audi|RS6
下一步检查重点

生成结果后，重点筛这三类：

匹配状态 = 未匹配
匹配状态 = 多候选
备注 包含 特殊车型

尤其 Audi 要重点看：

A5 / S5 / RS5 Sportback
Q5 / SQ5 Sportback
Q6 / SQ6 e-tron Sportback
RS6 Avant
A6 2027
Q4 e-tron 2027
如果你想直接做“只看问题行”的查询

可以在最后 排序 后面加一步：

powerquery
问题行 =
    Table.SelectRows(
        排序,
        each [匹配状态] <> "唯一匹配"
    )
in
    问题行

这样会只输出需要人工检查的行。


--- Round 9 / 下一步回复 ---
下一步做 子车系安全回填。

目标：

把“子车系候选匹配表”里的建议回填子车系
按 主车型 + 年份区间 + 结构 + 版本
回填到新版全量表的“子车系”列

但不建议全部自动回填，规则如下：

1. 唯一匹配：可以自动回填
2. 多候选，但备注为精准 Sportback / Avant 命中：可以自动回填建议子车系
3. 未匹配：不回填
4. 多候选且无精准命中：不回填，留空人工确认
5. 2027 待复核行：可以回填子车系，但迭代状态保留“待复核2027”
一、先生成“可回填子车系表”

基于你上一步的查询：

子车系候选匹配表

新建一个查询，命名为：

可回填子车系表

代码如下：

powerquery
let
    源 = 子车系候选匹配表,

    更改类型 =
        Table.TransformColumnTypes(
            源,
            {
                {"Year", Int64.Type},
                {"主车型", type text},
                {"结构", type text},
                {"版本", type text},
                {"品牌", type text},
                {"车型名", type text},
                {"候选子车系", type text},
                {"匹配数量", Int64.Type},
                {"匹配状态", type text},
                {"建议回填子车系", type text},
                {"备注", type text}
            }
        ),

    // 只保留可以安全回填的行
    筛选可回填 =
        Table.SelectRows(
            更改类型,
            each
                [建议回填子车系] <> null
                and Text.Trim([建议回填子车系]) <> ""
                and (
                    [匹配状态] = "唯一匹配"
                    or Text.Contains([备注], "精准 Sportback/Avant 命中")
                )
        ),

    // 按全量表维度聚合
    // 例如 Audi A5 2018-2019 Sportback 每年都匹配到 Audi|A5 Sportback
    // 聚合后回填一行即可
    分组 =
        Table.Group(
            筛选可回填,
            {
                "主车型",
                "结构",
                "版本",
                "品牌",
                "车型名"
            },
            {
                {
                    "回填子车系",
                    each
                        Text.Combine(
                            List.Sort(
                                List.Distinct(
                                    List.RemoveNulls([建议回填子车系])
                                )
                            ),
                            "; "
                        ),
                    type text
                },
                {
                    "回填最小年份",
                    each List.Min([Year]),
                    Int64.Type
                },
                {
                    "回填最大年份",
                    each List.Max([Year]),
                    Int64.Type
                },
                {
                    "回填年份列表",
                    each
                        Text.Combine(
                            List.Transform(
                                List.Sort(List.Distinct([Year])),
                                each Text.From(_)
                            ),
                            "; "
                        ),
                    type text
                },
                {
                    "回填匹配数量",
                    each
                        List.Count(
                            List.Distinct(
                                List.RemoveNulls([建议回填子车系])
                            )
                        ),
                    Int64.Type
                }
            }
        ),

    添加回填状态 =
        Table.AddColumn(
            分组,
            "回填状态",
            each
                if [回填匹配数量] = 1 then "可回填"
                else "多子车系需确认",
            type text
        ),

    选择列 =
        Table.SelectColumns(
            添加回填状态,
            {
                "主车型",
                "结构",
                "版本",
                "品牌",
                "车型名",
                "回填最小年份",
                "回填最大年份",
                "回填年份列表",
                "回填子车系",
                "回填匹配数量",
                "回填状态"
            }
        )
in
    选择列
二、把子车系回填到全量表

新建一个查询，命名为：

全量表_已回填子车系

代码如下：

powerquery
let
    源 = 全量表,

    全量表类型 =
        Table.TransformColumnTypes(
            源,
            {
                {"主车型", type text},
                {"年份区间", type text},
                {"结构", type text},
                {"对应尺码", type text},
                {"品牌", type text},
                {"前台车型", type text},
                {"排序依据车型", type text},
                {"子车系", type text},
                {"分类", type text},
                {"版本", type text},
                {"门数", type text},
                {"代际", type text},
                {"区间最小年份", Int64.Type},
                {"区间最大年份", Int64.Type},
                {"max_length_in", type number},
                {"max_width_in", type number},
                {"max_height_in", type number},
                {"max_length_cm", type number},
                {"max_width_cm", type number},
                {"max_height_cm", type number},
                {"驾驶室类型", type text},
                {"货斗长度_ft", type text},
                {"长度余量", type text},
                {"无尺码原因", type text},
                {"参考车型", type text},
                {"备注", type text},
                {"迭代状态", type text}
            }
        ),

    标准化全量表 =
        Table.TransformColumns(
            全量表类型,
            {
                {"主车型", each if _ = null then "" else Text.Trim(_), type text},
                {"结构", each if _ = null then "" else Text.Trim(_), type text},
                {"版本", each if _ = null then "" else Text.Trim(_), type text},
                {"品牌", each if _ = null then "" else Text.Trim(_), type text},
                {"前台车型", each if _ = null then "" else Text.Trim(_), type text},
                {"子车系", each if _ = null then "" else Text.Trim(_), type text}
            }
        ),

    添加车型名 =
        Table.AddColumn(
            标准化全量表,
            "车型名_匹配",
            each
                if [前台车型] <> null and Text.Trim([前台车型]) <> ""
                then Text.Trim([前台车型])
                else
                    let
                        car = Text.Trim([主车型]),
                        brand = Text.Trim([品牌])
                    in
                        if Text.StartsWith(car, brand & " ")
                        then Text.AfterDelimiter(car, brand & " ")
                        else car,
            type text
        ),

    回填源 = 可回填子车系表,

    回填源类型 =
        Table.TransformColumnTypes(
            回填源,
            {
                {"主车型", type text},
                {"结构", type text},
                {"版本", type text},
                {"品牌", type text},
                {"车型名", type text},
                {"回填最小年份", Int64.Type},
                {"回填最大年份", Int64.Type},
                {"回填子车系", type text},
                {"回填状态", type text}
            }
        ),

    // 按 主车型 + 结构 + 版本 + 品牌 + 车型名 合并
    合并回填 =
        Table.NestedJoin(
            添加车型名,
            {
                "主车型",
                "结构",
                "版本",
                "品牌",
                "车型名_匹配"
            },
            回填源类型,
            {
                "主车型",
                "结构",
                "版本",
                "品牌",
                "车型名"
            },
            "回填数据",
            JoinKind.LeftOuter
        ),

    展开回填 =
        Table.ExpandTableColumn(
            合并回填,
            "回填数据",
            {
                "回填最小年份",
                "回填最大年份",
                "回填子车系",
                "回填状态"
            },
            {
                "回填最小年份",
                "回填最大年份",
                "回填子车系",
                "回填状态"
            }
        ),

    // 年份区间必须被回填年份覆盖，避免错回填
    添加是否年份覆盖 =
        Table.AddColumn(
            展开回填,
            "是否年份覆盖",
            each
                [回填子车系] <> null
                and [回填最小年份] <> null
                and [回填最大年份] <> null
                and [回填最小年份] <= [区间最小年份]
                and [回填最大年份] >= [区间最大年份],
            type logical
        ),

    添加最终子车系 =
        Table.AddColumn(
            添加是否年份覆盖,
            "子车系_新",
            each
                if [子车系] <> null and Text.Trim([子车系]) <> "" then
                    [子车系]
                else if [是否年份覆盖] = true and [回填状态] = "可回填" then
                    [回填子车系]
                else
                    "",
            type text
        ),

    删除旧列 =
        Table.RemoveColumns(
            添加最终子车系,
            {
                "子车系",
                "车型名_匹配",
                "回填最小年份",
                "回填最大年份",
                "回填子车系",
                "回填状态",
                "是否年份覆盖"
            }
        ),

    重命名 =
        Table.RenameColumns(
            删除旧列,
            {
                {"子车系_新", "子车系"}
            }
        ),

    调整列顺序 =
        Table.ReorderColumns(
            重命名,
            {
                "主车型",
                "年份区间",
                "结构",
                "对应尺码",
                "品牌",
                "前台车型",
                "排序依据车型",
                "子车系",
                "分类",
                "版本",
                "门数",
                "代际",
                "区间最小年份",
                "区间最大年份",
                "max_length_in",
                "max_width_in",
                "max_height_in",
                "max_length_cm",
                "max_width_cm",
                "max_height_cm",
                "驾驶室类型",
                "货斗长度_ft",
                "长度余量",
                "无尺码原因",
                "参考车型",
                "备注",
                "迭代状态"
            },
            MissingField.UseNull
        )
in
    调整列顺序
三、这一步会自动回填哪些

例如这些会回填：

Audi A5 2018-2019 Sportback  → Audi|A5 Sportback
Audi S5 2018-2019 Sportback  → Audi|S5 Sportback
Audi RS6 2021-2024 Avant     → Audi|RS6 Avant
Audi Q6 e-tron 2027          → Audi|Q6 e-tron
Audi SQ6 e-tron 2027         → Audi|SQ6 e-tron

这些不会自动回填：

未匹配
多候选且没有精准 Sportback/Avant 命中
年份覆盖不完整
原本子车系已有值
四、建议再建一个“未回填检查表”

用于检查哪些行还没有子车系：

powerquery
let
    源 = 全量表_已回填子车系,

    筛选未回填 =
        Table.SelectRows(
            源,
            each [子车系] = null or Text.Trim([子车系]) = ""
        ),

    选择列 =
        Table.SelectColumns(
            筛选未回填,
            {
                "主车型",
                "年份区间",
                "结构",
                "品牌",
                "前台车型",
                "版本",
                "代际",
                "备注",
                "迭代状态"
            },
            MissingField.UseNull
        )
in
    选择列
这个阶段完成后，你会有 3 张关键表
1. 子车系候选匹配表
   用来查看所有逐年候选

2. 可回填子车系表
   只保留安全可回填结果

3. 全量表_已回填子车系
   最终带子车系的全量表

下一步就可以根据 子车系 去带出 对应尺码 / 长度余量 / 无尺码原因。


--- Round 10 / 下一步回复 ---
下一步做 尺码回填。

目标：

全量表_已回填子车系
↓
根据 子车系 + 年份区间 匹配 4afitment 的 SIZE.1
↓
回填：
对应尺码
长度余量
无尺码原因

其中 长度余量 用：

对应尺码最大可覆盖长度 - max_length_in

如果你现在尺码表里还没有每个尺码的最大长度，就先只回填 对应尺码 / 无尺码原因，长度余量 后面再算。

一、先生成逐年尺码匹配表

新建查询，命名：

全量表_逐年尺码匹配

代码如下：

powerquery
let
    源 = 全量表_已回填子车系,

    更改类型 =
        Table.TransformColumnTypes(
            源,
            {
                {"主车型", type text},
                {"年份区间", type text},
                {"结构", type text},
                {"对应尺码", type text},
                {"品牌", type text},
                {"前台车型", type text},
                {"排序依据车型", type text},
                {"子车系", type text},
                {"分类", type text},
                {"版本", type text},
                {"门数", type text},
                {"代际", type text},
                {"区间最小年份", Int64.Type},
                {"区间最大年份", Int64.Type},
                {"max_length_in", type number},
                {"max_width_in", type number},
                {"max_height_in", type number},
                {"max_length_cm", type number},
                {"max_width_cm", type number},
                {"max_height_cm", type number},
                {"驾驶室类型", type text},
                {"货斗长度_ft", type text},
                {"长度余量", type text},
                {"无尺码原因", type text},
                {"参考车型", type text},
                {"备注", type text},
                {"迭代状态", type text}
            }
        ),

    保留可匹配行 =
        Table.SelectRows(
            更改类型,
            each [子车系] <> null
                and Text.Trim([子车系]) <> ""
                and [区间最小年份] <> null
                and [区间最大年份] <> null
        ),

    添加年份列表 =
        Table.AddColumn(
            保留可匹配行,
            "Year",
            each {[区间最小年份]..[区间最大年份]},
            type list
        ),

    展开年份 =
        Table.ExpandListColumn(
            添加年份列表,
            "Year"
        ),

    拆分子车系 =
        Table.AddColumn(
            展开年份,
            "子车系列表",
            each
                List.Transform(
                    Text.Split([子车系], ";"),
                    each Text.Trim(_)
                ),
            type list
        ),

    展开子车系 =
        Table.ExpandListColumn(
            拆分子车系,
            "子车系列表"
        ),

    添加DB品牌 =
        Table.AddColumn(
            展开子车系,
            "DB_BRAND_KEY",
            each
                if Text.Contains([子车系列表], "|")
                then Text.BeforeDelimiter([子车系列表], "|")
                else [品牌],
            type text
        ),

    添加DB车型 =
        Table.AddColumn(
            添加DB品牌,
            "DB_MODEL_KEY",
            each
                if Text.Contains([子车系列表], "|")
                then Text.AfterDelimiter([子车系列表], "|")
                else [子车系列表],
            type text
        ),

    标准化Key =
        Table.TransformColumns(
            添加DB车型,
            {
                {"DB_BRAND_KEY", each if _ = null then "" else Text.Trim(_), type text},
                {"DB_MODEL_KEY", each if _ = null then "" else Text.Trim(_), type text}
            }
        ),

    // 读取 4afitment 数据源
    数据源 =
        Excel.Workbook(
            File.Contents("C:\Users\hzwlc\WPSDrive\345116921\WPS云盘\共享文件夹 \杭州海局贸易有限公司\运营部-302-周报月报年报\王力成\数据源\详细尺寸表.xlsx"),
            null,
            true
        ),

    非皮卡源 = 数据源{[Item="非皮卡压缩表", Kind="Table"]}[Data],
    皮卡源 = 数据源{[Item="皮卡压缩表", Kind="Table"]}[Data],

    非皮卡列 =
        Table.SelectColumns(
            非皮卡源,
            {
                "BRAND",
                "MODEL",
                "YEAR",
                "TYPE.1",
                "VERSION",
                "SIZE.1"
            },
            MissingField.UseNull
        ),

    皮卡列 =
        Table.SelectColumns(
            皮卡源,
            {
                "BRAND",
                "MODEL",
                "YEAR",
                "TYPE.1",
                "VERSION",
                "SIZE.1"
            },
            MissingField.UseNull
        ),

    数据库合并 =
        Table.Combine(
            {
                非皮卡列,
                皮卡列
            }
        ),

    数据库类型 =
        Table.TransformColumnTypes(
            数据库合并,
            {
                {"BRAND", type text},
                {"MODEL", type text},
                {"YEAR", Int64.Type},
                {"TYPE.1", type text},
                {"VERSION", type text},
                {"SIZE.1", type text}
            }
        ),

    数据库标准化 =
        Table.TransformColumns(
            数据库类型,
            {
                {"BRAND", each if _ = null then "" else Text.Trim(_), type text},
                {"MODEL", each if _ = null then "" else Text.Trim(_), type text},
                {"TYPE.1", each if _ = null then "" else Text.Trim(_), type text},
                {"VERSION", each if _ = null then "" else Text.Trim(_), type text},
                {"SIZE.1", each if _ = null then "" else Text.Trim(_), type text}
            }
        ),

    合并尺码 =
        Table.NestedJoin(
            标准化Key,
            {
                "Year",
                "DB_BRAND_KEY",
                "DB_MODEL_KEY"
            },
            数据库标准化,
            {
                "YEAR",
                "BRAND",
                "MODEL"
            },
            "DB匹配",
            JoinKind.LeftOuter
        ),

    展开尺码 =
        Table.ExpandTableColumn(
            合并尺码,
            "DB匹配",
            {
                "TYPE.1",
                "VERSION",
                "SIZE.1"
            },
            {
                "DB_TYPE",
                "DB_VERSION",
                "DB_SIZE"
            }
        ),

    选择列 =
        Table.SelectColumns(
            展开尺码,
            {
                "主车型",
                "年份区间",
                "结构",
                "品牌",
                "前台车型",
                "子车系",
                "分类",
                "版本",
                "门数",
                "代际",
                "区间最小年份",
                "区间最大年份",
                "max_length_in",
                "max_width_in",
                "max_height_in",
                "max_length_cm",
                "max_width_cm",
                "max_height_cm",
                "驾驶室类型",
                "货斗长度_ft",
                "参考车型",
                "备注",
                "迭代状态",
                "Year",
                "子车系列表",
                "DB_BRAND_KEY",
                "DB_MODEL_KEY",
                "DB_TYPE",
                "DB_VERSION",
                "DB_SIZE"
            },
            MissingField.UseNull
        )
in
    选择列
二、聚合回全量表行，生成对应尺码

新建查询，命名：

全量表_尺码回填结果

代码如下：

powerquery
let
    源 = 全量表_逐年尺码匹配,

    更改类型 =
        Table.TransformColumnTypes(
            源,
            {
                {"主车型", type text},
                {"年份区间", type text},
                {"结构", type text},
                {"品牌", type text},
                {"前台车型", type text},
                {"子车系", type text},
                {"分类", type text},
                {"版本", type text},
                {"门数", type text},
                {"代际", type text},
                {"区间最小年份", Int64.Type},
                {"区间最大年份", Int64.Type},
                {"max_length_in", type number},
                {"max_width_in", type number},
                {"max_height_in", type number},
                {"max_length_cm", type number},
                {"max_width_cm", type number},
                {"max_height_cm", type number},
                {"驾驶室类型", type text},
                {"货斗长度_ft", type text},
                {"参考车型", type text},
                {"备注", type text},
                {"迭代状态", type text},
                {"Year", Int64.Type},
                {"DB_SIZE", type text}
            }
        ),

    分组 =
        Table.Group(
            更改类型,
            {
                "主车型",
                "年份区间",
                "结构",
                "品牌",
                "前台车型",
                "子车系",
                "分类",
                "版本",
                "门数",
                "代际",
                "区间最小年份",
                "区间最大年份",
                "max_length_in",
                "max_width_in",
                "max_height_in",
                "max_length_cm",
                "max_width_cm",
                "max_height_cm",
                "驾驶室类型",
                "货斗长度_ft",
                "参考车型",
                "备注",
                "迭代状态"
            },
            {
                {
                    "对应尺码_新",
                    each
                        let
                            sizes =
                                List.Sort(
                                    List.Distinct(
                                        List.RemoveItems(
                                            List.Transform([DB_SIZE], each if _ = null then "" else Text.Trim(_)),
                                            {"", "无可用尺码"}
                                        )
                                    )
                                )
                        in
                            Text.Combine(sizes, "; "),
                    type text
                },
                {
                    "匹配年份数",
                    each List.Count(List.Distinct([Year])),
                    Int64.Type
                },
                {
                    "有尺码年份数",
                    each
                        List.Count(
                            List.Select(
                                [DB_SIZE],
                                each _ <> null and Text.Trim(_) <> "" and Text.Trim(_) <> "无可用尺码"
                            )
                        ),
                    Int64.Type
                },
                {
                    "无尺码年份列表",
                    each
                        let
                            t = Table.SelectRows(_, each [DB_SIZE] = null or Text.Trim([DB_SIZE]) = "" or Text.Trim([DB_SIZE]) = "无可用尺码"),
                            ys = List.Sort(List.Distinct(t[Year]))
                        in
                            Text.Combine(List.Transform(ys, each Text.From(_)), "; "),
                    type text
                }
            }
        ),

    添加无尺码原因 =
        Table.AddColumn(
            分组,
            "无尺码原因_新",
            each
                if [对应尺码_新] <> null and Text.Trim([对应尺码_新]) <> "" and [无尺码年份列表] = "" then
                    ""
                else if [对应尺码_新] <> null and Text.Trim([对应尺码_新]) <> "" and [无尺码年份列表] <> "" then
                    "部分年份无尺码：" & [无尺码年份列表]
                else
                    "子车系已匹配，但 4afitment 无可用尺码",
            type text
        ),

    添加迭代状态 =
        Table.AddColumn(
            添加无尺码原因,
            "迭代状态_新",
            each
                if [对应尺码_新] <> null and Text.Trim([对应尺码_新]) <> "" and [无尺码年份列表] = "" then
                    "已匹配尺码"
                else if [对应尺码_新] <> null and Text.Trim([对应尺码_新]) <> "" and [无尺码年份列表] <> "" then
                    "部分年份无尺码"
                else
                    "无可用尺码",
            type text
        )
in
    添加迭代状态
三、把尺码结果回填到全量表

新建查询，命名：

全量表_已回填尺码

代码如下：

powerquery
let
    源 = 全量表_已回填子车系,

    源类型 =
        Table.TransformColumnTypes(
            源,
            {
                {"主车型", type text},
                {"年份区间", type text},
                {"结构", type text},
                {"对应尺码", type text},
                {"品牌", type text},
                {"前台车型", type text},
                {"排序依据车型", type text},
                {"子车系", type text},
                {"分类", type text},
                {"版本", type text},
                {"门数", type text},
                {"代际", type text},
                {"区间最小年份", Int64.Type},
                {"区间最大年份", Int64.Type},
                {"max_length_in", type number},
                {"max_width_in", type number},
                {"max_height_in", type number},
                {"max_length_cm", type number},
                {"max_width_cm", type number},
                {"max_height_cm", type number},
                {"驾驶室类型", type text},
                {"货斗长度_ft", type text},
                {"长度余量", type text},
                {"无尺码原因", type text},
                {"参考车型", type text},
                {"备注", type text},
                {"迭代状态", type text}
            }
        ),

    尺码结果 = 全量表_尺码回填结果,

    合并 =
        Table.NestedJoin(
            源类型,
            {
                "主车型",
                "年份区间",
                "结构",
                "品牌",
                "前台车型",
                "子车系",
                "版本",
                "代际"
            },
            尺码结果,
            {
                "主车型",
                "年份区间",
                "结构",
                "品牌",
                "前台车型",
                "子车系",
                "版本",
                "代际"
            },
            "尺码结果",
            JoinKind.LeftOuter
        ),

    展开 =
        Table.ExpandTableColumn(
            合并,
            "尺码结果",
            {
                "对应尺码_新",
                "无尺码原因_新",
                "迭代状态_新"
            },
            {
                "对应尺码_新",
                "无尺码原因_新",
                "迭代状态_新"
            }
        ),

    添加对应尺码最终 =
        Table.AddColumn(
            展开,
            "对应尺码_最终",
            each
                if [对应尺码] <> null and Text.Trim([对应尺码]) <> "" then
                    [对应尺码]
                else if [对应尺码_新] <> null then
                    [对应尺码_新]
                else
                    "",
            type text
        ),

    添加无尺码原因最终 =
        Table.AddColumn(
            添加对应尺码最终,
            "无尺码原因_最终",
            each
                if [无尺码原因] <> null and Text.Trim([无尺码原因]) <> "" then
                    [无尺码原因]
                else if [无尺码原因_新] <> null then
                    [无尺码原因_新]
                else
                    "",
            type text
        ),

    添加迭代状态最终 =
        Table.AddColumn(
            添加无尺码原因最终,
            "迭代状态_最终",
            each
                if [迭代状态] <> null and Text.Contains([迭代状态], "待复核") then
                    [迭代状态]
                else if [迭代状态_新] <> null and Text.Trim([迭代状态_新]) <> "" then
                    [迭代状态_新]
                else
                    [迭代状态],
            type text
        ),

    删除旧列 =
        Table.RemoveColumns(
            添加迭代状态最终,
            {
                "对应尺码",
                "无尺码原因",
                "迭代状态",
                "对应尺码_新",
                "无尺码原因_新",
                "迭代状态_新"
            }
        ),

    重命名 =
        Table.RenameColumns(
            删除旧列,
            {
                {"对应尺码_最终", "对应尺码"},
                {"无尺码原因_最终", "无尺码原因"},
                {"迭代状态_最终", "迭代状态"}
            }
        ),

    调整列顺序 =
        Table.ReorderColumns(
            重命名,
            {
                "主车型",
                "年份区间",
                "结构",
                "对应尺码",
                "品牌",
                "前台车型",
                "排序依据车型",
                "子车系",
                "分类",
                "版本",
                "门数",
                "代际",
                "区间最小年份",
                "区间最大年份",
                "max_length_in",
                "max_width_in",
                "max_height_in",
                "max_length_cm",
                "max_width_cm",
                "max_height_cm",
                "驾驶室类型",
                "货斗长度_ft",
                "长度余量",
                "无尺码原因",
                "参考车型",
                "备注",
                "迭代状态"
            },
            MissingField.UseNull
        )
in
    调整列顺序
四、结果检查表

最后建议再建一个检查查询：

尺码异常检查表

代码：

powerquery
let
    源 = 全量表_已回填尺码,

    筛选 =
        Table.SelectRows(
            源,
            each
                [对应尺码] = null
                or Text.Trim([对应尺码]) = ""
                or Text.Contains([无尺码原因], "部分年份")
                or Text.Contains([迭代状态], "待复核")
                or Text.Contains([迭代状态], "无可用")
        ),

    选择列 =
        Table.SelectColumns(
            筛选,
            {
                "主车型",
                "年份区间",
                "结构",
                "品牌",
                "前台车型",
                "子车系",
                "版本",
                "max_length_in",
                "对应尺码",
                "无尺码原因",
                "备注",
                "迭代状态"
            },
            MissingField.UseNull
        )
in
    选择列
当前阶段的产物链路
全量表
↓
子车系匹配准备表
↓
子车系候选匹配表
↓
可回填子车系表
↓
全量表_已回填子车系
↓
全量表_逐年尺码匹配
↓
全量表_尺码回填结果
↓
全量表_已回填尺码
↓
尺码异常检查表

下一步才适合做 长度余量：因为要先确认 对应尺码 是否稳定、是否存在一行多个尺码。


--- Round 11 / 下一步回复 ---
下一步做 长度余量回填。

核心逻辑：

长度余量 = 尺码最大覆盖长度_in - max_length_in

如果一行有多个尺码，例如：

SD-L; SD-XL

建议取最小可用余量，也就是更保守的那个尺码余量。

一、先建“尺码容量表”

在 Excel 里建一个表，表名建议叫：

尺码容量表

表头：

对应尺码	最大覆盖长度_in

示例：

tsv
对应尺码	最大覆盖长度_in
SD-S
SD-M
SD-L
SD-XL
SUV-S
SUV-M
SUV-L
SUV-XL
PK-S
PK-M
PK-L
PK-XL

你需要把每个尺码实际能覆盖的最大长度填进去。比如如果 SD-L 最大覆盖 190 in，就写：

tsv
SD-L	190
二、生成“尺码拆分余量表”

新建 Power Query，命名为：

全量表_尺码余量明细

代码：

powerquery
let
    源 = 全量表_已回填尺码,

    更改类型 =
        Table.TransformColumnTypes(
            源,
            {
                {"主车型", type text},
                {"年份区间", type text},
                {"结构", type text},
                {"对应尺码", type text},
                {"品牌", type text},
                {"前台车型", type text},
                {"排序依据车型", type text},
                {"子车系", type text},
                {"分类", type text},
                {"版本", type text},
                {"门数", type text},
                {"代际", type text},
                {"区间最小年份", Int64.Type},
                {"区间最大年份", Int64.Type},
                {"max_length_in", type number},
                {"max_width_in", type number},
                {"max_height_in", type number},
                {"max_length_cm", type number},
                {"max_width_cm", type number},
                {"max_height_cm", type number},
                {"驾驶室类型", type text},
                {"货斗长度_ft", type text},
                {"长度余量", type text},
                {"无尺码原因", type text},
                {"参考车型", type text},
                {"备注", type text},
                {"迭代状态", type text}
            }
        ),

    保留有尺码 =
        Table.SelectRows(
            更改类型,
            each [对应尺码] <> null
                and Text.Trim([对应尺码]) <> ""
                and [max_length_in] <> null
        ),

    添加尺码列表 =
        Table.AddColumn(
            保留有尺码,
            "尺码列表",
            each
                List.Transform(
                    Text.Split([对应尺码], ";"),
                    each Text.Trim(_)
                ),
            type list
        ),

    展开尺码 =
        Table.ExpandListColumn(
            添加尺码列表,
            "尺码列表"
        ),

    尺码容量源 = Excel.CurrentWorkbook(){[Name="尺码容量表"]}[Content],

    尺码容量类型 =
        Table.TransformColumnTypes(
            尺码容量源,
            {
                {"对应尺码", type text},
                {"最大覆盖长度_in", type number}
            }
        ),

    标准化容量表 =
        Table.TransformColumns(
            尺码容量类型,
            {
                {"对应尺码", each if _ = null then "" else Text.Trim(_), type text}
            }
        ),

    合并容量 =
        Table.NestedJoin(
            展开尺码,
            {"尺码列表"},
            标准化容量表,
            {"对应尺码"},
            "容量表",
            JoinKind.LeftOuter
        ),

    展开容量 =
        Table.ExpandTableColumn(
            合并容量,
            "容量表",
            {"最大覆盖长度_in"},
            {"尺码最大覆盖长度_in"}
        ),

    添加余量 =
        Table.AddColumn(
            展开容量,
            "长度余量_单尺码",
            each
                if [尺码最大覆盖长度_in] = null or [max_length_in] = null
                then null
                else Number.Round([尺码最大覆盖长度_in] - [max_length_in], 1),
            type number
        ),

    添加余量状态 =
        Table.AddColumn(
            添加余量,
            "余量状态",
            each
                if [长度余量_单尺码] = null then "尺码容量缺失"
                else if [长度余量_单尺码] < 0 then "长度超出尺码"
                else if [长度余量_单尺码] < 3 then "余量偏小"
                else "余量正常",
            type text
        )
in
    添加余量状态
三、聚合回全量表行

新建 Power Query，命名：

全量表_长度余量结果

代码：

powerquery
let
    源 = 全量表_尺码余量明细,

    分组 =
        Table.Group(
            源,
            {
                "主车型",
                "年份区间",
                "结构",
                "品牌",
                "前台车型",
                "子车系",
                "版本",
                "代际"
            },
            {
                {
                    "长度余量_新",
                    each
                        let
                            margins = List.RemoveNulls([长度余量_单尺码]),
                            minMargin =
                                if List.Count(margins) = 0
                                then null
                                else List.Min(margins)
                        in
                            if minMargin = null
                            then ""
                            else Text.From(minMargin),
                    type text
                },
                {
                    "余量状态汇总",
                    each
                        Text.Combine(
                            List.Sort(
                                List.Distinct([余量状态])
                            ),
                            "; "
                        ),
                    type text
                },
                {
                    "尺码容量缺失列表",
                    each
                        let
                            t = Table.SelectRows(_, each [余量状态] = "尺码容量缺失"),
                            s = List.Sort(List.Distinct(t[尺码列表]))
                        in
                            Text.Combine(s, "; "),
                    type text
                }
            }
        )
in
    分组
四、把长度余量回填到全量表

新建 Power Query，命名：

全量表_最终结果

代码：

powerquery
let
    源 = 全量表_已回填尺码,

    余量结果 = 全量表_长度余量结果,

    合并 =
        Table.NestedJoin(
            源,
            {
                "主车型",
                "年份区间",
                "结构",
                "品牌",
                "前台车型",
                "子车系",
                "版本",
                "代际"
            },
            余量结果,
            {
                "主车型",
                "年份区间",
                "结构",
                "品牌",
                "前台车型",
                "子车系",
                "版本",
                "代际"
            },
            "余量结果",
            JoinKind.LeftOuter
        ),

    展开 =
        Table.ExpandTableColumn(
            合并,
            "余量结果",
            {
                "长度余量_新",
                "余量状态汇总",
                "尺码容量缺失列表"
            },
            {
                "长度余量_新",
                "余量状态汇总",
                "尺码容量缺失列表"
            }
        ),

    添加长度余量最终 =
        Table.AddColumn(
            展开,
            "长度余量_最终",
            each
                if [长度余量] <> null and Text.Trim([长度余量]) <> "" then
                    [长度余量]
                else if [长度余量_新] <> null then
                    [长度余量_新]
                else
                    "",
            type text
        ),

    添加无尺码原因最终 =
        Table.AddColumn(
            添加长度余量最终,
            "无尺码原因_最终",
            each
                if [尺码容量缺失列表] <> null and Text.Trim([尺码容量缺失列表]) <> "" then
                    Text.Combine(
                        List.RemoveItems(
                            {
                                if [无尺码原因] = null then "" else Text.Trim([无尺码原因]),
                                "尺码容量缺失：" & [尺码容量缺失列表]
                            },
                            {""}
                        ),
                        "；"
                    )
                else
                    [无尺码原因],
            type text
        ),

    添加迭代状态最终 =
        Table.AddColumn(
            添加无尺码原因最终,
            "迭代状态_最终",
            each
                if [余量状态汇总] <> null and Text.Contains([余量状态汇总], "长度超出尺码") then
                    "尺码长度不足"
                else if [余量状态汇总] <> null and Text.Contains([余量状态汇总], "余量偏小") then
                    "余量偏小"
                else if [迭代状态] <> null and Text.Trim([迭代状态]) <> "" then
                    [迭代状态]
                else
                    "已匹配尺码",
            type text
        ),

    删除旧列 =
        Table.RemoveColumns(
            添加迭代状态最终,
            {
                "长度余量",
                "无尺码原因",
                "迭代状态",
                "长度余量_新",
                "余量状态汇总",
                "尺码容量缺失列表"
            }
        ),

    重命名 =
        Table.RenameColumns(
            删除旧列,
            {
                {"长度余量_最终", "长度余量"},
                {"无尺码原因_最终", "无尺码原因"},
                {"迭代状态_最终", "迭代状态"}
            }
        ),

    调整列顺序 =
        Table.ReorderColumns(
            重命名,
            {
                "主车型",
                "年份区间",
                "结构",
                "对应尺码",
                "品牌",
                "前台车型",
                "排序依据车型",
                "子车系",
                "分类",
                "版本",
                "门数",
                "代际",
                "区间最小年份",
                "区间最大年份",
                "max_length_in",
                "max_width_in",
                "max_height_in",
                "max_length_cm",
                "max_width_cm",
                "max_height_cm",
                "驾驶室类型",
                "货斗长度_ft",
                "长度余量",
                "无尺码原因",
                "参考车型",
                "备注",
                "迭代状态"
            },
            MissingField.UseNull
        )
in
    调整列顺序
五、余量异常检查表

最后再建一个检查表：

长度余量异常检查表

代码：

powerquery
let
    源 = 全量表_最终结果,

    筛选 =
        Table.SelectRows(
            源,
            each
                [长度余量] = null
                or Text.Trim([长度余量]) = ""
                or (
                    try Number.From([长度余量]) < 3
                    otherwise false
                )
                or Text.Contains([迭代状态], "尺码长度不足")
                or Text.Contains([迭代状态], "余量偏小")
                or Text.Contains([无尺码原因], "尺码容量缺失")
        ),

    选择列 =
        Table.SelectColumns(
            筛选,
            {
                "主车型",
                "年份区间",
                "结构",
                "对应尺码",
                "品牌",
                "前台车型",
                "子车系",
                "版本",
                "max_length_in",
                "长度余量",
                "无尺码原因",
                "备注",
                "迭代状态"
            },
            MissingField.UseNull
        )
in
    选择列
完整链路现在就是
全量表
↓
子车系匹配准备表
↓
子车系候选匹配表
↓
可回填子车系表
↓
全量表_已回填子车系
↓
全量表_逐年尺码匹配
↓
全量表_尺码回填结果
↓
全量表_已回填尺码
↓
全量表_尺码余量明细
↓
全量表_长度余量结果
↓
全量表_最终结果
↓
长度余量异常检查表

下一步适合做 排序依据车型 自动列：让 A3/S3/RS3、A5/S5/RS5、Q5/SQ5 这类组合在排序时靠在一起。


--- Round 12 / 下一步回复 ---
下一步做 排序依据车型。

目标是让这些车型排序时靠在一起：

Audi A3 / S3 / RS3          → Audi A3
Audi A4 / S4 / RS4          → Audi A4
Audi A5 / S5 / RS5          → Audi A5
Audi A6 / S6 / RS6          → Audi A6
Audi A7 / S7 / RS7          → Audi A7
Audi A8 / S8                → Audi A8
Audi Q5 / SQ5               → Audi Q5
Audi Q6 e-tron / SQ6 e-tron → Audi Q6 e-tron

也就是：

主车型              排序依据车型
Audi A5             Audi A5
Audi S5             Audi A5
Audi RS5            Audi A5
Audi RS5 Sportback  Audi A5
Audi SQ5            Audi Q5
Audi SQ6 e-tron     Audi Q6 e-tron
一、Power Query：自动生成排序依据车型

建议接在最终结果后面，新建查询：

全量表_最终排序

代码如下：

powerquery
let
    源 = 全量表_最终结果,

    更改类型 =
        Table.TransformColumnTypes(
            源,
            {
                {"主车型", type text},
                {"年份区间", type text},
                {"结构", type text},
                {"对应尺码", type text},
                {"品牌", type text},
                {"前台车型", type text},
                {"排序依据车型", type text},
                {"子车系", type text},
                {"分类", type text},
                {"版本", type text},
                {"门数", type text},
                {"代际", type text},
                {"区间最小年份", Int64.Type},
                {"区间最大年份", Int64.Type},
                {"max_length_in", type number},
                {"max_width_in", type number},
                {"max_height_in", type number},
                {"max_length_cm", type number},
                {"max_width_cm", type number},
                {"max_height_cm", type number},
                {"驾驶室类型", type text},
                {"货斗长度_ft", type text},
                {"长度余量", type text},
                {"无尺码原因", type text},
                {"参考车型", type text},
                {"备注", type text},
                {"迭代状态", type text}
            }
        ),

    标准化 =
        Table.TransformColumns(
            更改类型,
            {
                {"主车型", each if _ = null then "" else Text.Trim(_), type text},
                {"品牌", each if _ = null then "" else Text.Trim(_), type text},
                {"前台车型", each if _ = null then "" else Text.Trim(_), type text},
                {"排序依据车型", each if _ = null then "" else Text.Trim(_), type text}
            }
        ),

    添加排序依据车型新 =
        Table.AddColumn(
            标准化,
            "排序依据车型_新",
            each
                let
                    brand = [品牌],
                    car = [主车型],
                    front = [前台车型],

                    model =
                        if front <> "" then
                            front
                        else if brand <> "" and Text.StartsWith(car, brand & " ") then
                            Text.AfterDelimiter(car, brand & " ")
                        else
                            car,

                    result =
                        if brand = "Audi" then
                            if List.Contains({"A3", "S3", "RS3"}, model) then "Audi A3"
                            else if List.Contains({"A4", "S4", "RS4"}, model) then "Audi A4"
                            else if List.Contains({"A5", "S5", "RS5"}, model) then "Audi A5"
                            else if List.Contains({"A6", "S6", "RS6"}, model) then "Audi A6"
                            else if List.Contains({"A7", "S7", "RS7"}, model) then "Audi A7"
                            else if List.Contains({"A8", "S8"}, model) then "Audi A8"
                            else if List.Contains({"Q5", "SQ5"}, model) then "Audi Q5"
                            else if List.Contains({"Q6 e-tron", "SQ6 e-tron"}, model) then "Audi Q6 e-tron"
                            else car
                        else
                            car
                in
                    if [排序依据车型] <> "" then
                        [排序依据车型]
                    else
                        result,
            type text
        ),

    删除旧排序列 =
        Table.RemoveColumns(
            添加排序依据车型新,
            {"排序依据车型"}
        ),

    重命名 =
        Table.RenameColumns(
            删除旧排序列,
            {
                {"排序依据车型_新", "排序依据车型"}
            }
        ),

    调整列顺序 =
        Table.ReorderColumns(
            重命名,
            {
                "主车型",
                "年份区间",
                "结构",
                "对应尺码",
                "品牌",
                "前台车型",
                "排序依据车型",
                "子车系",
                "分类",
                "版本",
                "门数",
                "代际",
                "区间最小年份",
                "区间最大年份",
                "max_length_in",
                "max_width_in",
                "max_height_in",
                "max_length_cm",
                "max_width_cm",
                "max_height_cm",
                "驾驶室类型",
                "货斗长度_ft",
                "长度余量",
                "无尺码原因",
                "参考车型",
                "备注",
                "迭代状态"
            },
            MissingField.UseNull
        )
in
    调整列顺序
二、如果你想直接排序

可以在最后 调整列顺序 后面加：

powerquery
排序 =
    Table.Sort(
        调整列顺序,
        {
            {"品牌", Order.Ascending},
            {"排序依据车型", Order.Ascending},
            {"主车型", Order.Ascending},
            {"区间最小年份", Order.Ascending},
            {"结构", Order.Ascending},
            {"版本", Order.Ascending}
        }
    )
in
    排序

如果加了这段，记得把原来的：

powerquery
in
    调整列顺序

改成：

powerquery
in
    排序
三、Audi 排序依据车型效果
tsv
主车型	前台车型	排序依据车型
Audi A3	A3	Audi A3
Audi S3	S3	Audi A3
Audi RS3	RS3	Audi A3
Audi A4	A4	Audi A4
Audi S4	S4	Audi A4
Audi A5	A5	Audi A5
Audi S5	S5	Audi A5
Audi RS5	RS5	Audi A5
Audi A6	A6	Audi A6
Audi RS6	RS6	Audi A6
Audi A7	A7	Audi A7
Audi S7	S7	Audi A7
Audi RS7	RS7	Audi A7
Audi A8	A8	Audi A8
Audi S8	S8	Audi A8
Audi Q5	Q5	Audi Q5
Audi SQ5	SQ5	Audi Q5
Audi Q6 e-tron	Q6 e-tron	Audi Q6 e-tron
Audi SQ6 e-tron	SQ6 e-tron	Audi Q6 e-tron
四、后续其它品牌也可以这样扩展

例如后面做 BMW，可以增加：

powerquery
else if brand = "BMW" then
    if List.Contains({"3 Series", "M3"}, model) then "BMW 3 Series"
    else if List.Contains({"4 Series", "M4"}, model) then "BMW 4 Series"
    else if List.Contains({"5 Series", "M5"}, model) then "BMW 5 Series"
    else if List.Contains({"X3", "X3 M"}, model) then "BMW X3"
    else if List.Contains({"X5", "X5 M"}, model) then "BMW X5"
    else car

这一步完成后，整套链路就变成：

全量表_最终结果
↓
全量表_最终排序

后面你只需要看 全量表_最终排序 作为最终输出表。


--- Round 13 / 下一步回复 ---
下一步建议做 全量表最终质检表。

目标是检查这几类问题：

1. 主车型 + 结构 + 版本 + 年份 是否重复覆盖
2. 关键字段是否为空
3. 对应尺码是否为空
4. 长度余量是否异常
5. 2027 待复核行
6. 同主车型同年份是否出现普通版误匹配特殊版风险
一、最终质检：逐年展开检查重复覆盖

新建 Power Query，命名：

全量表_逐年质检

代码：

powerquery
let
    源 = 全量表_最终排序,

    更改类型 =
        Table.TransformColumnTypes(
            源,
            {
                {"主车型", type text},
                {"年份区间", type text},
                {"结构", type text},
                {"对应尺码", type text},
                {"品牌", type text},
                {"前台车型", type text},
                {"排序依据车型", type text},
                {"子车系", type text},
                {"分类", type text},
                {"版本", type text},
                {"门数", type text},
                {"代际", type text},
                {"区间最小年份", Int64.Type},
                {"区间最大年份", Int64.Type},
                {"max_length_in", type number},
                {"max_width_in", type number},
                {"max_height_in", type number},
                {"长度余量", type text},
                {"无尺码原因", type text},
                {"参考车型", type text},
                {"备注", type text},
                {"迭代状态", type text}
            }
        ),

    保留有效年份 =
        Table.SelectRows(
            更改类型,
            each [区间最小年份] <> null
                and [区间最大年份] <> null
        ),

    添加年份列表 =
        Table.AddColumn(
            保留有效年份,
            "Year",
            each {[区间最小年份]..[区间最大年份]},
            type list
        ),

    展开年份 =
        Table.ExpandListColumn(
            添加年份列表,
            "Year"
        ),

    添加质检Key =
        Table.AddColumn(
            展开年份,
            "质检Key",
            each
                Text.From([Year])
                & "|" & Text.Trim(if [主车型] = null then "" else [主车型])
                & "|" & Text.Trim(if [结构] = null then "" else [结构])
                & "|" & Text.Trim(if [版本] = null then "" else [版本])
                & "|" & Text.Trim(if [门数] = null then "" else [门数])
                & "|" & Text.Trim(if [驾驶室类型] = null then "" else [驾驶室类型])
                & "|" & Text.Trim(if [货斗长度_ft] = null then "" else [货斗长度_ft]),
            type text
        ),

    添加普通特殊标记 =
        Table.AddColumn(
            添加质检Key,
            "普通特殊标记",
            each
                let
                    car = Text.Upper(if [主车型] = null then "" else [主车型]),
                    ver = Text.Upper(if [版本] = null then "" else [版本])
                in
                    if Text.Contains(car, " RS")
                        or Text.Contains(car, " S")
                        or Text.Contains(car, " SQ")
                        or Text.Contains(ver, "RS")
                        or Text.Contains(ver, "SRT")
                        or Text.Contains(ver, "AMG")
                        or Text.Contains(ver, "M ")
                    then "特殊版"
                    else "普通版",
            type text
        )
in
    添加普通特殊标记
二、重复覆盖检查表

新建查询：

质检_重复覆盖

代码：

powerquery
let
    源 = 全量表_逐年质检,

    分组 =
        Table.Group(
            源,
            {"质检Key"},
            {
                {"重复数量", each Table.RowCount(_), Int64.Type},
                {
                    "涉及行",
                    each
                        Text.Combine(
                            List.Transform(
                                List.Distinct([主车型]),
                                each Text.From(_)
                            ),
                            "; "
                        ),
                    type text
                },
                {
                    "年份",
                    each Text.From(List.Min([Year])),
                    type text
                },
                {
                    "结构",
                    each Text.Combine(List.Distinct([结构]), "; "),
                    type text
                },
                {
                    "版本",
                    each Text.Combine(List.Distinct([版本]), "; "),
                    type text
                },
                {
                    "尺码",
                    each Text.Combine(List.Distinct([对应尺码]), "; "),
                    type text
                }
            }
        ),

    筛选重复 =
        Table.SelectRows(
            分组,
            each [重复数量] > 1
        )
in
    筛选重复

如果这张表为空，说明没有明显的逐年重复覆盖。

三、关键字段缺失检查表

新建查询：

质检_关键字段缺失

代码：

powerquery
let
    源 = 全量表_最终排序,

    筛选 =
        Table.SelectRows(
            源,
            each
                [主车型] = null or Text.Trim([主车型]) = ""
                or [年份区间] = null or Text.Trim([年份区间]) = ""
                or [结构] = null or Text.Trim([结构]) = ""
                or [品牌] = null or Text.Trim([品牌]) = ""
                or [前台车型] = null or Text.Trim([前台车型]) = ""
                or [分类] = null or Text.Trim([分类]) = ""
                or [代际] = null or Text.Trim([代际]) = ""
                or [区间最小年份] = null
                or [区间最大年份] = null
                or [max_length_in] = null
                or [max_width_in] = null
                or [max_height_in] = null
        ),

    选择列 =
        Table.SelectColumns(
            筛选,
            {
                "主车型",
                "年份区间",
                "结构",
                "品牌",
                "前台车型",
                "分类",
                "版本",
                "代际",
                "区间最小年份",
                "区间最大年份",
                "max_length_in",
                "max_width_in",
                "max_height_in",
                "备注",
                "迭代状态"
            },
            MissingField.UseNull
        )
in
    选择列

这张表应该只剩下你刻意保留的 待补尺寸 / 待复核2027 行。

四、尺码异常检查表

如果你前面已经建过 长度余量异常检查表，这一步可以合并增强一下。

新建查询：

质检_尺码异常

代码：

powerquery
let
    源 = 全量表_最终排序,

    筛选 =
        Table.SelectRows(
            源,
            each
                [对应尺码] = null
                or Text.Trim([对应尺码]) = ""
                or [长度余量] = null
                or Text.Trim([长度余量]) = ""
                or (
                    try Number.From([长度余量]) < 3
                    otherwise false
                )
                or Text.Contains(if [无尺码原因] = null then "" else [无尺码原因], "无")
                or Text.Contains(if [无尺码原因] = null then "" else [无尺码原因], "缺失")
                or Text.Contains(if [迭代状态] = null then "" else [迭代状态], "无可用")
                or Text.Contains(if [迭代状态] = null then "" else [迭代状态], "余量偏小")
                or Text.Contains(if [迭代状态] = null then "" else [迭代状态], "尺码长度不足")
        ),

    选择列 =
        Table.SelectColumns(
            筛选,
            {
                "主车型",
                "年份区间",
                "结构",
                "对应尺码",
                "品牌",
                "前台车型",
                "子车系",
                "版本",
                "max_length_in",
                "长度余量",
                "无尺码原因",
                "备注",
                "迭代状态"
            },
            MissingField.UseNull
        )
in
    选择列
五、待复核年份检查表

新建查询：

质检_待复核

代码：

powerquery
let
    源 = 全量表_最终排序,

    筛选 =
        Table.SelectRows(
            源,
            each
                Text.Contains(if [迭代状态] = null then "" else [迭代状态], "待复核")
                or Text.Contains(if [备注] = null then "" else [备注], "待")
                or Text.Contains(if [备注] = null then "" else [备注], "暂沿用")
                or Text.Contains(if [备注] = null then "" else [备注], "不直接沿用")
        ),

    选择列 =
        Table.SelectColumns(
            筛选,
            {
                "主车型",
                "年份区间",
                "结构",
                "品牌",
                "前台车型",
                "版本",
                "代际",
                "max_length_in",
                "max_width_in",
                "max_height_in",
                "参考车型",
                "备注",
                "迭代状态"
            },
            MissingField.UseNull
        )
in
    选择列
六、普通版误匹配特殊版风险检查

这个是针对你之前强调的规则：普通版不能匹配特殊版子车系。

新建查询：

质检_普通版特殊子车系风险

代码：

powerquery
let
    源 = 全量表_最终排序,

    添加是否普通行 =
        Table.AddColumn(
            源,
            "是否普通行",
            each
                let
                    car = Text.Upper(if [主车型] = null then "" else [主车型]),
                    ver = Text.Upper(if [版本] = null then "" else [版本])
                in
                    not (
                        Text.Contains(car, " RS")
                        or Text.Contains(car, " S")
                        or Text.Contains(car, " SQ")
                        or Text.Contains(ver, "RS")
                        or Text.Contains(ver, "SRT")
                        or Text.Contains(ver, "AMG")
                        or Text.Contains(ver, "M ")
                        or Text.Contains(ver, "TYPE S")
                        or Text.Contains(ver, "RAPTOR")
                        or Text.Contains(ver, "ZR2")
                        or Text.Contains(ver, "TRAIL BOSS")
                        or Text.Contains(ver, "RUBICON")
                    ),
            type logical
        ),

    添加子车系风险 =
        Table.AddColumn(
            添加是否普通行,
            "子车系风险",
            each
                let
                    sub = Text.Upper(if [子车系] = null then "" else [子车系])
                in
                    Text.Contains(sub, "|S")
                    or Text.Contains(sub, "|RS")
                    or Text.Contains(sub, "|SQ")
                    or Text.Contains(sub, " AMG")
                    or Text.Contains(sub, " M")
                    or Text.Contains(sub, "TYPE S")
                    or Text.Contains(sub, "RAPTOR")
                    or Text.Contains(sub, "ZR2")
                    or Text.Contains(sub, "TRAIL BOSS")
                    or Text.Contains(sub, "RUBICON"),
            type logical
        ),

    筛选风险 =
        Table.SelectRows(
            添加子车系风险,
            each [是否普通行] = true and [子车系风险] = true
        ),

    选择列 =
        Table.SelectColumns(
            筛选风险,
            {
                "主车型",
                "年份区间",
                "结构",
                "品牌",
                "前台车型",
                "子车系",
                "版本",
                "备注",
                "迭代状态"
            },
            MissingField.UseNull
        )
in
    选择列
七、最终质检汇总表

最后建一个总览，方便一眼看各问题数量。

新建查询：

质检_汇总

代码：

powerquery
let
    重复覆盖数量 = Table.RowCount(质检_重复覆盖),
    关键字段缺失数量 = Table.RowCount(质检_关键字段缺失),
    尺码异常数量 = Table.RowCount(质检_尺码异常),
    待复核数量 = Table.RowCount(质检_待复核),
    普通版特殊风险数量 = Table.RowCount(质检_普通版特殊子车系风险),

    汇总 =
        #table(
            {"检查项", "问题数量", "建议"},
            {
                {"重复覆盖", 重复覆盖数量, if 重复覆盖数量 = 0 then "通过" else "需要处理重复年份/结构/版本"},
                {"关键字段缺失", 关键字段缺失数量, if 关键字段缺失数量 = 0 then "通过" else "补齐关键字段或确认待补尺寸"},
                {"尺码异常", 尺码异常数量, if 尺码异常数量 = 0 then "通过" else "检查对应尺码、长度余量、无尺码原因"},
                {"待复核", 待复核数量, if 待复核数量 = 0 then "通过" else "集中复核 2027 或暂沿用尺寸行"},
                {"普通版特殊子车系风险", 普通版特殊风险数量, if 普通版特殊风险数量 = 0 then "通过" else "普通版行可能误回填特殊版子车系"}
            }
        )
in
    汇总
最终链路到这里就完整了
全量表
↓
子车系匹配准备表
↓
子车系候选匹配表
↓
可回填子车系表
↓
全量表_已回填子车系
↓
全量表_已回填尺码
↓
全量表_最终结果
↓
全量表_最终排序
↓
质检_汇总

后面每次补一个品牌，都只需要看这 5 张质检表：

质检_重复覆盖
质检_关键字段缺失
质检_尺码异常
质检_待复核
质检_普通版特殊子车系风险


--- Round 14 / 下一步回复 ---
下一步建议做 最终并表输出 / 版本留痕。

也就是把这套链路产出的结果整理成 4 张最终可用表：

1. 全量表_最终排序        → 最终主表
2. 质检_汇总              → 总体问题数量
3. 质检_待处理明细        → 需要人工处理的问题行
4. 本次补充记录_Audi      → 本次 Audi 新增/修正行留痕
一、先做“质检_待处理明细”

把所有质检问题合并成一张表，方便集中处理。

新建查询：

质检_待处理明细

代码：

powerquery
let
    重复覆盖 =
        Table.AddColumn(
            质检_重复覆盖,
            "问题类型",
            each "重复覆盖",
            type text
        ),

    关键字段缺失 =
        Table.AddColumn(
            质检_关键字段缺失,
            "问题类型",
            each "关键字段缺失",
            type text
        ),

    尺码异常 =
        Table.AddColumn(
            质检_尺码异常,
            "问题类型",
            each "尺码异常",
            type text
        ),

    待复核 =
        Table.AddColumn(
            质检_待复核,
            "问题类型",
            each "待复核",
            type text
        ),

    普通版特殊风险 =
        Table.AddColumn(
            质检_普通版特殊子车系风险,
            "问题类型",
            each "普通版特殊子车系风险",
            type text
        ),

    合并 =
        Table.Combine(
            {
                重复覆盖,
                关键字段缺失,
                尺码异常,
                待复核,
                普通版特殊风险
            }
        ),

    调整列 =
        Table.ReorderColumns(
            合并,
            {
                "问题类型",
                "主车型",
                "年份区间",
                "结构",
                "品牌",
                "前台车型",
                "子车系",
                "版本",
                "代际",
                "对应尺码",
                "max_length_in",
                "max_width_in",
                "max_height_in",
                "长度余量",
                "无尺码原因",
                "参考车型",
                "备注",
                "迭代状态"
            },
            MissingField.UseNull
        )
in
    调整列
二、做“本次补充记录_Audi”

这个表用于留痕：哪些行是本次补的，哪些是不补的。

表头建议：

品牌	主车型	年份区间	结构	版本	处理类型	处理结果	原因	备注

示例：

tsv
品牌	主车型	年份区间	结构	版本	处理类型	处理结果	原因	备注
Audi	Audi A4	2009	Sedan		补充	已补尺寸	A4/A4 Quattro 2009 回归	B8 起始年份缺口
Audi	Audi A5	2018-2019	Sportback	Sportback	补充	已补尺寸	A5 Sportback 回归	Sportback 不作为主车型
Audi	Audi Q6 e-tron	2027	SUV		补充	已补尺寸	2027 Q6 e-tron 美国站可补	待后续复核 2027
Audi	Audi A1	2011-2018; 2022-2026			排除	不补	非美国主销车型	不进入美国全量表
Audi	Audi Q2	2018-2020; 2026			排除	不补	非美国主销车型	不进入美国全量表
Audi	Audi RS5	2011			排除	不补	美国正式进入应从 2013 年款开始	欧洲/全球早期口径
Audi	Audi RS5	2016			排除	不补	美国 RS5 2016 断档	不进入全量表
三、最终输出主表

最后保留这个查询作为主表：

全量表_最终排序

它的列顺序保持你最新格式：

主车型	年份区间	结构	对应尺码	品牌	前台车型	排序依据车型	子车系	分类	版本	门数	代际	区间最小年份	区间最大年份	max_length_in	max_width_in	max_height_in	max_length_cm	max_width_cm	max_height_cm	驾驶室类型	货斗长度_ft	长度余量	无尺码原因	参考车型	备注	迭代状态
四、建议最终落表方式

在 Excel 里建议这样放：

工作表：全量表
    原始人工维护表

工作表：全量表_最终排序
    Power Query 输出最终表

工作表：质检_汇总
    问题数量总览

工作表：质检_待处理明细
    所有问题行集合

工作表：本次补充记录_Audi
    本次 Audi 处理留痕
五、最终检查标准

这几张表通过后，就可以认为本轮 Audi 处理完成：

质检_重复覆盖 = 空
质检_普通版特殊子车系风险 = 空
质检_关键字段缺失 只剩待补尺寸/待复核2027
质检_尺码异常 只剩无数据库尺码或余量偏小行
质检_待复核 只剩 2027 暂沿用尺寸行

下一步如果继续推进品牌，可以直接进入下一个品牌的“未覆盖清单分析”，流程沿用这套链路。


--- Round 15 / 下一步回复 ---
ChatGPT 说：下一步就是进入“下一个品牌循环”，不再继续堆 Audi 流程。把 Audi 作为模板，后面每个品牌都按同一套顺序走：未覆盖清单 → 主表补行 → 子车系 → 尺码 → 质检。下一步建议进入 下一个品牌的未覆盖清单分析。
后续每个品牌都按这个固定流程推进：
1. 读取未覆盖清单2. 判断是否美国站应补3. 排除非美国车型 / 数据库假拆分4. 统一主车型、前台车型、版本、结构5. 生成新版全量表补充行6. 补尺寸7. 子车系最后匹配8. 回填对应尺码 / 长度余量9. 跑最终质检10. 输出不补清单 + 补充记录
你可以直接发下一个品牌的未覆盖清单，格式继续用：
make,model,覆盖状态,年份区间_断开
我会按这套新版全量表格式继续分析：
主车型	年份区间	结构	对应尺码	品牌	前台车型	排序依据车型	子车系	分类	版本	门数	代际	区间最小年份	区间最大年份	max_length_in	max_width_in	max_height_in	max_length_cm	max_width_cm	max_height_cm	驾驶室类型	货斗长度_ft	长度余量	无尺码原因	参考车型	备注	迭代状态
如果你要继续 Audi，也可以下一步做：
Audi 本次补充记录_Audi 完整留痕表
但正常流程上，Audi 已经可以收口，建议换下一个品牌。


--- Round 16 / 下一步回复 ---
下一步就是：从总未覆盖清单里自动筛出下一个品牌，然后继续按 Audi 流程处理。

你可以先建一个查询，找出每个品牌的未覆盖数量，决定下一个优先处理哪个品牌。

powerquery
let
    源 = Excel.CurrentWorkbook(){[Name="未覆盖清单"]}[Content],

    更改类型 =
        Table.TransformColumnTypes(
            源,
            {
                {"make", type text},
                {"model", type text},
                {"覆盖状态", type text},
                {"年份区间_断开", type text}
            }
        ),

    筛选未覆盖 =
        Table.SelectRows(
            更改类型,
            each [覆盖状态] = "未覆盖"
        ),

    分组 =
        Table.Group(
            筛选未覆盖,
            {"make"},
            {
                {"未覆盖车型数", each Table.RowCount(_), Int64.Type},
                {
                    "车型列表",
                    each Text.Combine(List.Sort(List.Distinct([model])), "; "),
                    type text
                }
            }
        ),

    排序 =
        Table.Sort(
            分组,
            {
                {"未覆盖车型数", Order.Descending},
                {"make", Order.Ascending}
            }
        )
in
    排序

然后再建一个查询，只提取某个品牌，例如下一个处理 BMW：

powerquery
let
    源 = Excel.CurrentWorkbook(){[Name="未覆盖清单"]}[Content],

    更改类型 =
        Table.TransformColumnTypes(
            源,
            {
                {"make", type text},
                {"model", type text},
                {"覆盖状态", type text},
                {"年份区间_断开", type text}
            }
        ),

    筛选品牌 =
        Table.SelectRows(
            更改类型,
            each [覆盖状态] = "未覆盖"
                and [make] = "BMW"
        ),

    排序 =
        Table.Sort(
            筛选品牌,
            {
                {"model", Order.Ascending}
            }
        )
in
    排序

如果下一个品牌不是 BMW，把这里改掉即可：

powerquery
[make] = "BMW"

改成：

powerquery
[make] = "Mercedes-Benz"

或：

powerquery
[make] = "Chevrolet"
下一步实际操作顺序
1. 跑“品牌未覆盖数量统计”
2. 选未覆盖数量最多或最重要的品牌
3. 导出该品牌未覆盖清单
4. 发给我
5. 我继续按新版全量表格式分析

你发下一个品牌清单后，我会直接输出：

1. 不补清单
2. 假未覆盖说明
3. 可补全量表 TSV
4. 待复核项
5. 后续子车系匹配规则


--- Round 17 / 下一步回复 ---
下一步可以做一个通用品牌推进模板，以后每个品牌都不用重新写流程，直接替换品牌名即可。

1. 品牌参数表

先在 Excel 建一个表，表名：

品牌参数表

表头：

当前品牌

内容示例：

BMW

以后要处理 Mercedes-Benz、Chevrolet，只改这个单元格。

2. 当前品牌未覆盖清单

新建 Power Query：

当前品牌_未覆盖清单

代码：

powerquery
let
    品牌参数源 = Excel.CurrentWorkbook(){[Name="品牌参数表"]}[Content],
    当前品牌 = Text.Trim(品牌参数源{0}[当前品牌]),

    源 = Excel.CurrentWorkbook(){[Name="未覆盖清单"]}[Content],

    更改类型 =
        Table.TransformColumnTypes(
            源,
            {
                {"make", type text},
                {"model", type text},
                {"覆盖状态", type text},
                {"年份区间_断开", type text}
            }
        ),

    筛选 =
        Table.SelectRows(
            更改类型,
            each Text.Trim([make]) = 当前品牌
                and Text.Trim([覆盖状态]) = "未覆盖"
        ),

    排序 =
        Table.Sort(
            筛选,
            {
                {"model", Order.Ascending}
            }
        )
in
    排序
3. 当前品牌处理清单导出格式

你后面给我时，直接复制这个查询结果即可：

make,model,覆盖状态,年份区间_断开

我会按固定输出：

不补清单
假未覆盖说明
可补全量表 TSV
待复核项
子车系匹配规则
4. 当前品牌推进状态表

建议再建一张人工维护表：

品牌推进状态表

表头：

品牌	未覆盖车型数	处理状态	备注

示例：

tsv
品牌	未覆盖车型数	处理状态	备注
Audi	33	已完成	等待最终质检/子车系回填
BMW		待处理
Mercedes-Benz		待处理
Chevrolet		待处理

这样后续就能按品牌批量推进，不会乱。


--- Round 18 / 下一步回复 ---
下一步做 品牌推进状态表自动统计，让 品牌推进状态表 自动显示每个品牌有多少未覆盖、是否已处理。

1. 自动生成品牌未覆盖统计表

新建 Power Query：

品牌未覆盖统计

代码：

powerquery
let
    源 = Excel.CurrentWorkbook(){[Name="未覆盖清单"]}[Content],

    更改类型 =
        Table.TransformColumnTypes(
            源,
            {
                {"make", type text},
                {"model", type text},
                {"覆盖状态", type text},
                {"年份区间_断开", type text}
            }
        ),

    筛选未覆盖 =
        Table.SelectRows(
            更改类型,
            each Text.Trim([覆盖状态]) = "未覆盖"
        ),

    分组 =
        Table.Group(
            筛选未覆盖,
            {"make"},
            {
                {"未覆盖车型数", each Table.RowCount(_), Int64.Type},
                {
                    "未覆盖车型列表",
                    each Text.Combine(List.Sort(List.Distinct([model])), "; "),
                    type text
                }
            }
        ),

    排序 =
        Table.Sort(
            分组,
            {
                {"未覆盖车型数", Order.Descending},
                {"make", Order.Ascending}
            }
        )
in
    排序
2. 品牌推进状态表建议结构

你可以维护这个表：

tsv
品牌	未覆盖车型数	处理状态	处理优先级	备注
Audi	33	已完成	1	已完成主表补行，子车系最后匹配
BMW		待处理	2
Mercedes-Benz		待处理	3
Chevrolet		待处理	4
3. 自动回填未覆盖车型数

如果 品牌推进状态表 是 Excel 表，可以新建查询：

品牌推进状态_自动更新

代码：

powerquery
let
    状态源 = Excel.CurrentWorkbook(){[Name="品牌推进状态表"]}[Content],

    状态类型 =
        Table.TransformColumnTypes(
            状态源,
            {
                {"品牌", type text},
                {"未覆盖车型数", Int64.Type},
                {"处理状态", type text},
                {"处理优先级", Int64.Type},
                {"备注", type text}
            }
        ),

    统计源 = 品牌未覆盖统计,

    合并 =
        Table.NestedJoin(
            状态类型,
            {"品牌"},
            统计源,
            {"make"},
            "统计",
            JoinKind.LeftOuter
        ),

    展开 =
        Table.ExpandTableColumn(
            合并,
            "统计",
            {"未覆盖车型数", "未覆盖车型列表"},
            {"未覆盖车型数_统计", "未覆盖车型列表"}
        ),

    添加未覆盖车型数最终 =
        Table.AddColumn(
            展开,
            "未覆盖车型数_最终",
            each
                if [未覆盖车型数_统计] = null
                then 0
                else [未覆盖车型数_统计],
            Int64.Type
        ),

    删除旧列 =
        Table.RemoveColumns(
            添加未覆盖车型数最终,
            {
                "未覆盖车型数",
                "未覆盖车型数_统计"
            }
        ),

    重命名 =
        Table.RenameColumns(
            删除旧列,
            {
                {"未覆盖车型数_最终", "未覆盖车型数"}
            }
        ),

    调整列顺序 =
        Table.ReorderColumns(
            重命名,
            {
                "品牌",
                "未覆盖车型数",
                "处理状态",
                "处理优先级",
                "未覆盖车型列表",
                "备注"
            },
            MissingField.UseNull
        ),

    排序 =
        Table.Sort(
            调整列顺序,
            {
                {"处理状态", Order.Ascending},
                {"处理优先级", Order.Ascending},
                {"未覆盖车型数", Order.Descending},
                {"品牌", Order.Ascending}
            }
        )
in
    排序
4. 后续你只需要这样推进
1. 刷新 品牌未覆盖统计
2. 看哪个品牌未覆盖车型数最多
3. 在 品牌参数表 改当前品牌
4. 刷新 当前品牌_未覆盖清单
5. 复制该品牌清单给我
6. 我继续做该品牌全量分析

现在这套流程已经完整闭环。下一步真正进入业务分析，就需要你发下一个品牌的未覆盖清单。


--- Round 19 / 下一步回复 ---
下一步已经没有新的自动流程可继续堆了，真正进入业务推进需要你给我下一个品牌的未覆盖清单。

你现在只需要做这一步：

刷新 当前品牌_未覆盖清单
复制结果
发给我

格式仍然是：

csv
make,model,覆盖状态,年份区间_断开
BMW,1 Series,未覆盖,2008-2013
BMW,2 Series,未覆盖,2014-2026
...

我收到后会直接按 Audi 的完整流程继续输出：

1. 不补清单
2. 假未覆盖说明
3. 可补全量表 TSV
4. 待复核项
5. 子车系匹配规则
6. 后续尺码/质检处理建议

如果你还没确定下一个品牌，优先选 品牌未覆盖统计 里未覆盖车型数最多的那个。


--- Round 20 / 下一步回复 ---
下一步需要你提供下一个品牌的未覆盖清单，否则我这边不能继续做车型分析。

你复制这个格式发我即可：

csv
make,model,覆盖状态,年份区间_断开
BMW,1 Series,未覆盖,2008-2013
BMW,2 Series,未覆盖,2014-2026
BMW,3 Series,未覆盖,1999-2005; 2027

我收到后会直接继续：

1. 判断哪些不补
2. 判断哪些是假未覆盖
3. 输出新版全量表补充 TSV
4. 补尺寸
5. 子车系最后匹配
6. 尺码/余量/质检

现在真正的下一步就是：把下一个品牌清单发来。


--- Round 21 / 下一步回复 ---
现在已经到必须输入新数据的节点了，不能再继续“下一步”自动推进。

你当前唯一下一步是：

把下一个品牌的未覆盖清单发给我

格式：

csv
make,model,覆盖状态,年份区间_断开
BMW,1 Series,未覆盖,2008-2013
BMW,2 Series,未覆盖,2014-2026
BMW,3 Series,未覆盖,1999-2005; 2027

我收到后会直接继续做：

不补清单
假未覆盖说明
新版全量表补充 TSV
待复核项
子车系最后匹配规则
尺码/质检建议

如果暂时没有下一个品牌清单，那 Audi 这轮已经收口，下一步就是在 Excel / Power Query 里刷新这些最终表：

全量表_最终排序
质检_汇总
质检_待处理明细
品牌未覆盖统计
当前品牌_未覆盖清单


--- Round 22 / 下一步回复 ---
下一步还是同一个节点：需要你发下一个品牌的未覆盖清单。

现在我不能继续生成车型分析，因为缺少新的输入数据。你直接复制下面这种格式给我：

csv
make,model,覆盖状态,年份区间_断开
BMW,1 Series,未覆盖,2008-2013
BMW,2 Series,未覆盖,2014-2026
BMW,3 Series,未覆盖,1999-2005; 2027

收到清单后，我会直接继续按 Audi 流程输出：

不补清单
假未覆盖说明
新版全量表补充 TSV
待复核项
子车系最后匹配规则
尺码/质检建议

如果没有新品牌清单，Audi 这轮已经完成，建议你先在 Excel 里刷新：

品牌未覆盖统计
当前品牌_未覆盖清单
全量表_最终排序
质检_汇总


--- Round 23 / 下一步回复 ---
现在没有可继续的“下一步”了，流程已经走到等待新品牌清单。

你接下来只能二选一：

方案 A：继续车型分析

把下一个品牌的未覆盖清单发我：

csv
make,model,覆盖状态,年份区间_断开
BMW,1 Series,未覆盖,2008-2013
BMW,2 Series,未覆盖,2014-2026
BMW,3 Series,未覆盖,1999-2005; 2027

我收到后继续分析。

方案 B：不发新清单，先在 Excel 里执行

刷新这些查询：

品牌未覆盖统计
当前品牌_未覆盖清单
全量表_最终排序
质检_汇总
质检_待处理明细

然后看 品牌未覆盖统计，选择下一个品牌。


--- Round 24 / 下一步回复 ---
现在这条“下一步”已经卡在缺少输入数据，我不能继续凭空分析。

你现在要做的下一步只有这个：

发下一个品牌的未覆盖清单

格式：

csv
make,model,覆盖状态,年份区间_断开
BMW,1 Series,未覆盖,2008-2013
BMW,2 Series,未覆盖,2014-2026
BMW,3 Series,未覆盖,1999-2005; 2027

没有这份清单，我不能继续输出下一个品牌的：

不补清单
假未覆盖说明
新版全量表补充 TSV
待复核项
子车系匹配规则

如果你只是想确认 Audi 后续步骤，那 Audi 已经收口，下一步就是在 Excel 里刷新：

全量表_最终排序
质检_汇总
质检_待处理明细
品牌未覆盖统计
当前品牌_未覆盖清单


--- Round 25 / 下一步回复 ---
现在不能再“下一步”推进了，因为没有新的品牌未覆盖清单。

你现在只需要发这个：

csv
make,model,覆盖状态,年份区间_断开
BMW,1 Series,未覆盖,2008-2013
BMW,2 Series,未覆盖,2014-2026
BMW,3 Series,未覆盖,1999-2005; 2027

或者你从 Excel 里复制 当前品牌_未覆盖清单 查询结果发我。

收到后我会继续输出下一个品牌的：

不补清单
假未覆盖说明
新版全量表补充 TSV
待复核项
子车系最后匹配规则

如果你没有新清单，那 Audi 流程已经结束，下一步就是去 Excel 里刷新查询。


--- Round 26 / 下一步回复 ---
ChatGPT 说：到这里不能再继续“下一步”了，需要你给新的输入。
请发下一个品牌的未覆盖清单，格式像这样：
csvmake,model,覆盖状态,年份区间_断开BMW,1 Series,未覆盖,2008-2013BMW,2 Series,未覆盖,2014-2026BMW,3 Series,未覆盖,1999-2005; 2027
收到后我继续按 Audi 流程做：不补清单、假未覆盖说明、全量表补充 TSV、待复核项、子车系匹配规则。


--- Round 27 / 下一步回复 ---
ChatGPT 说：现在没有新数据，不能继续分析车型。
下一步就是把下一个品牌的未覆盖清单发我。
格式：
csvmake,model,覆盖状态,年份区间_断开BMW,1 Series,未覆盖,2008-2013BMW,2 Series,未覆盖,2014-2026BMW,3 Series,未覆盖,1999-2005; 2027
没有这份清单，我只能重复同一个步骤，无法继续推进。

