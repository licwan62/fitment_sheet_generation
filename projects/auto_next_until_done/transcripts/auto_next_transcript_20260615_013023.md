# Auto next transcript
开始时间：2026-06-15 01:30:34
发送内容：下一步


--- Round 1 / 手动初始 prompt 回复 ---
明白，我按这个新口径继续推进：

tsv
新规则	执行方式
主要关注普通版本	普通版缺口优先补齐到可入库
特殊版本断代不管	AMG/PHEV/392/Calais 等特殊版断代不再继续追补
真实断代也进全量分析	用“确认断代/不补”记录保留原因，但不强行造尺寸行
待终核继续核到入库	除非是业务口径问题，否则继续查到可入库或明确不补

本轮先把剩余 6 条待终核继续核掉。结论：4 条升级为可入库，2 条仍建议普通表不补/另作为命名口径记录。 源表仍是你上传的当前全量表。

粘贴的文本 (1)

本轮升级为可入库
tsv
主车型	分类	品牌	车型名	结构	版本	门数	代际	代际说明	年份区间	区间最小年份	区间最大年份	驾驶室类型	货斗长度_ft	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Oldsmobile 88	三厢车	Oldsmobile	88	Sedan		4	gen7	full-size	1975					226.9	79.8	54.3	1975 Oldsmobile Delta 88 Town Sedan, Automobile-Catalog / Conceptcarz	补1975普通Delta 88 Sedan；长宽高已锁定	可入库
Oldsmobile Custom Cruiser	两厢车	Oldsmobile	Custom Cruiser	Wagon		4	gen1	full-size wagon	1971-1972					231.2	79.5	57.2	1971-1972 Oldsmobile Custom Cruiser Wagon / 1971 Oldsmobile Cruisers brochure	普通全尺寸wagon，1971-1972可用同一clamshell wagon包络；不再放Oldsmobile 88 Wagon	可入库
Oldsmobile Custom Cruiser	两厢车	Oldsmobile	Custom Cruiser	Wagon		4	gen1	full-size wagon	1973					228.3	79.5	57.2	1973 Oldsmobile Custom Cruiser Wagon, Automobile-Catalog / 1971 Oldsmobile Cruisers brochure	1973长度变化，单独保留；高度沿用同代Custom Cruiser wagon官方57.2口径	可入库
Oldsmobile Custom Cruiser	两厢车	Oldsmobile	Custom Cruiser	Wagon		4	gen1	full-size wagon	1974-1976					231.2	80	57.2	1974-1976 Oldsmobile Custom Cruiser Wagon, Automobile-Catalog / 1971 Oldsmobile Cruisers brochure	1974-1976为5mph bumper后期，1974长231.2宽79.5高57.2，1976宽80，取安全包络	可入库

依据：1975 Delta 88 Town Sedan 的 Automobile-Catalog 规格明确给出 226.9 / 79.8 / 54.3 in，因此可以从待终核升级为可入库。
汽车目录
 1971 年 Oldsmobile 官方 wagon brochure 给出 Custom Cruiser 57.2 in 高度，同时 Custom Cruiser 1971-1976 是 Oldsmobile full-size wagon 回归段；1973 Automobile-Catalog 给出 228.3 / 79.5 in，1974 给出 231.2 / 79.5 / 57.2 in，1976 给出 231 / 80 in，所以可以拆成 1971-1972、1973、1974-1976 入库。
汽车目录
+3
Dezo's Garage
+3
汽车目录
+3

本轮不建议补进“普通版本全量表”
tsv
主车型	结构	版本	门数	年份区间	结论	原因
Mercury Colony Park	Wagon		1961-1964	暂不补进普通版本主表	这是 Mercury wagon 命名体系问题，Colony Park/Commuter/Monterey 之间需要另建独立wagon线；不是普通 Monterey 缺口
Mercury Colony Park	Wagon		1965-1968	暂不补进普通版本主表	Colony Park 是独立高端wagon线，1965-1968可另建专项；如果主表只关注普通版本，不应强行补到Monterey普通wagon

依据：Mercury Colony Park 在 1965-1968 已经是独立 model line，Mercury Commuter/Colony Park 也说明 1957-1968 的 Mercury wagon 命名体系不适合简单塞回 Monterey 普通版本；因此按你“主要关注普通版本”的新口径，这两条不再作为普通版本缺失补行。
维基百科

更新后的待终核
tsv
状态	数量
继续待终核	0
更新后的最终处理口径
tsv
类别	处理
普通版缺失	补到可入库
普通版真实断代	记录为确认断代，不补尺寸
特殊版断代	不再追补
命名承接/独立子系	不污染原主车型；必要时另建主车型

下一步建议：我继续把前面三张最终表重新整理一版，移除“待终核”，改成：

tsv
表名	内容
新增_可入库	所有已核到可入库的普通版/必要另建主车型
不补_断代或命名承接	确认不补、特殊版断代不追、命名承接说明
可选_独立子系	如 Mercury Colony Park、Cutlass Calais 这类非普通主线


--- Round 2 / 下一步回复 ---
下面是按你新口径整理后的 最终三表版：

口径：

tsv
规则	处理
普通版本缺失	补到可入库
普通版本真实断代	放入不补说明，不造尺寸行
特殊版本断代	不追补
命名承接/独立子系	不污染原主车型，单独放“可选_独立子系”

源表为你上传的当前全量表。

粘贴的文本 (1)

1）新增_可入库 TSV
tsv
主车型	分类	品牌	车型名	结构	版本	门数	代际	代际说明	年份区间	区间最小年份	区间最大年份	驾驶室类型	货斗长度_ft	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Jeep Wrangler	越野车	Jeep	Wrangler	SUV	Unlimited	4	gen3	JK	2012					173.4	73.7	72.6	2012 Jeep Wrangler Unlimited Sport, Edmunds / Car and Driver	补缺失2012 JK四门Unlimited；后续可与2007-2011或2013段按尺寸再压缩	可入库
Jeep Wrangler	越野车	Jeep	Wrangler	SUV	Unlimited	4	gen4	JL	2018-2020					188.4	73.9	73.6	2018-2020 Jeep Wrangler Unlimited 4-door, Edmunds / Quadratec	补JL四门普通版；不要用原第2261行承接，第2261更适合改为2014-2015 JK	可入库
Chevrolet Equinox	越野车	Chevrolet	Equinox	SUV		4	gen3	compact SUV	2018-2024					183.1	72.6	65.4	2018-2024 Chevrolet Equinox	补普通燃油/普通SUV gen3；EV行应另写版本EV	可入库
Mercedes-Benz C-Class	跑车	Mercedes-Benz	C-Class	Coupe		2	gen4	C205 coupe	2016					184.5	71.3	55.3	2016 Mercedes-Benz C-Class Coupe / C300 Coupe	补2016 C-Class Coupe；Convertible若无2016美国销售则不补	可入库
Mercedes-Benz C-Class	三厢车	Mercedes-Benz	C-Class	Sedan		4	gen4	W205 compact executive	2015					184.5	71.3	56.8	2015 Mercedes-Benz C300 Sedan, Edmunds / MBUSA	补W205美规首年普通Sedan	可入库
Mercedes-Benz S-Class	三厢车	Mercedes-Benz	S-Class	Sedan		4	gen4	W220 full-size luxury sedan	2006					203.3	73	56.9	2006 Mercedes-Benz S-Class S500 4MATIC, Edmunds	补2006 W220美规普通Sedan	可入库
Mercedes-Benz S-Class	跑车	Mercedes-Benz	S-Class	Coupe		2	gen6	C217 luxury coupe	2015-2017					198.9	74.8	55.8	2015-2017 Mercedes-Benz S-Class Coupe / S550 4MATIC Coupe	补C217前期S-Class Coupe；1996-2014不补到S-Class，应由CL-Class承接	可入库
Mercedes-Benz S-Class	跑车	Mercedes-Benz	S-Class	Coupe		2	gen6	C217 facelift luxury coupe	2019					198.9	74.8	55.6	2019 Mercedes-Benz S560 4MATIC Coupe, Car and Driver	补2019 S-Class Coupe缺失年	可入库
Mercedes-Benz S-Class	跑车	Mercedes-Benz	S-Class	Convertible		2	gen6	A217 facelift luxury cabriolet	2019					198.9	74.8	56.2	2019 Mercedes-Benz S560 Cabriolet, Edmunds / C&D / MBUSA	补2019 S-Class Cabriolet缺失年	可入库
Mercedes-Benz SL-Class	跑车	Mercedes-Benz	SL-Class	Roadster		2	gen3	R107 roadster	1972-1989					180.3	70.5	51.2	1972-1989 Mercedes-Benz SL-Class R107 / 560 SL	补R107美规SL Roadster长缺口；取后期560 SL安全包络	可入库
Mercury Sable	三厢车	Mercury	Sable	Sedan		4	gen3	midsize	1996					199.7	73	55.4	1996 Mercury Sable Sedan, Edmunds	补1996 Sable Sedan；注意原第2970建议改为2008-2009	可入库
Mercury Monterey	两厢车	Mercury	Monterey	Wagon		4	gen2	full-size wagon	1955-1956					206.3	76.4	61.2	1955-1956 Mercury Monterey / full-size Mercury Station Wagon	1955-1956可作为Monterey wagon补行；长宽高取1955 Mercury full-size安全口径，1956宽度取76.4	可入库
Oldsmobile 88	三厢车	Oldsmobile	88	Sedan		4	gen7	full-size	1972					222.1	79.5	54.3	1972 Oldsmobile Delta 88 Royale Town Sedan, Automobile-Catalog	补1972 Oldsmobile 88 Sedan；长宽明确，高度按同代Town Sedan安全口径	可入库
Oldsmobile 88	三厢车	Oldsmobile	88	Sedan		4	gen7	full-size	1975					226.9	79.8	54.3	1975 Oldsmobile Delta 88 Town Sedan, Automobile-Catalog / Conceptcarz	补1975普通Delta 88 Sedan；长宽高已锁定	可入库
Oldsmobile 88	跑车	Oldsmobile	88	Coupe		2	gen8	downsized full-size coupe	1977-1979					217.5	76.8	54.5	1977-1979 Oldsmobile Delta 88 Coupe / Royale Coupe	补1977-1979 downsized 88 Coupe	可入库
Oldsmobile 88	跑车	Oldsmobile	88	Coupe		2	gen8	downsized full-size coupe	1980					218.4	76.3	54.7	1980 Oldsmobile Delta 88 Coupe	补1980 Coupe；尺寸与1977-1979不同，单独保留	可入库
Oldsmobile Cutlass	三厢车	Oldsmobile	Cutlass	Sedan		4	gen2	intermediate	1966					204.2	75.4	54.5	1966 Oldsmobile F-85 / Cutlass 4-Door Sedan	补1966 Cutlass/F-85 Sedan	可入库
Oldsmobile Cutlass	跑车	Oldsmobile	Cutlass	Convertible		2	gen2	intermediate convertible	1965					204.3	74.4	54	1965 Oldsmobile Cutlass Convertible / 1965 Oldsmobile mid-size fact sheet	1965单年宽度74.4，高度54.0；不建议与1966-1967直接合并	可入库
Oldsmobile Cutlass	跑车	Oldsmobile	Cutlass	Convertible		2	gen2	intermediate convertible	1966-1967					204.2	76.3	53	1966-1967 Oldsmobile Cutlass Supreme Convertible / Conceptcarz	1966-1967 Cutlass/Cutlass Supreme Convertible尺寸接近，取1967安全宽度76.3	可入库
Oldsmobile Cutlass	跑车	Oldsmobile	Cutlass	Convertible		2	gen3	intermediate convertible	1968-1972					203.6	76.8	52.9	1968-1972 Oldsmobile Cutlass / Cutlass Supreme Convertible	补1968-1972 Convertible	可入库
Oldsmobile Cutlass	跑车	Oldsmobile	Cutlass	Coupe		2	gen2	intermediate coupe	1966-1967					204.2	76.3	53	1966-1967 Oldsmobile Cutlass Sports Coupe / Cutlass Supreme Sports Coupe	补1966-1967 Coupe；1967 Conceptcarz支持204.2/76.3/53.0	可入库
Oldsmobile Cutlass	跑车	Oldsmobile	Cutlass	Coupe		2	gen3	intermediate coupe	1968-1972					203.6	76.8	53	1968-1972 Oldsmobile Cutlass / Cutlass Supreme Hardtop Coupe	补1968-1972 Coupe	可入库
Plymouth Barracuda	跑车	Plymouth	Barracuda	Coupe		2	gen3	E-body pony car	1970-1971					186.7	74.9	51.2	1970-1971 Plymouth Barracuda / Cuda Hardtop, Conceptcarz / Automobile-Catalog / Over-Drive Magazine	补E-body早期Coupe；后续可与原第3400修正行合并	可入库
Pontiac Bonneville	跑车	Pontiac	Bonneville	Convertible		2	gen2	one-year full-size convertible	1958					211.7	77.4	55.7	1958 Pontiac Bonneville Convertible Coupe	补1958 Convertible；独立大车身	可入库
Pontiac Bonneville	跑车	Pontiac	Bonneville	Convertible		2	gen3	wide-track full-size convertible	1959-1960					220.7	80.7	56	1959-1960 Pontiac Bonneville Convertible, Conceptcarz / Automobile-Catalog	补1959-1960 Bonneville Convertible；1960 Conceptcarz给出220.7/80.7/56.0，1959 Automobile-Catalog给出220.7/80.0，取安全包络	可入库
Pontiac Bonneville	跑车	Pontiac	Bonneville	Convertible		2	gen4	full-size convertible	1961					217	78.2	55.6	1961 Pontiac Bonneville Convertible, Automobile-Catalog / autoevolution	1961单年尺寸明确，不建议并入1962-1964	可入库
Pontiac Bonneville	跑车	Pontiac	Bonneville	Convertible		2	gen4	full-size convertible	1962					218.6	78.6	54.9	1962 Pontiac Bonneville Convertible, Automobile-Catalog / Conceptcarz	1962单年尺寸明确，和1961、1963-1964不同	可入库
Pontiac Bonneville	跑车	Pontiac	Bonneville	Convertible		2	gen4	full-size convertible	1963					218.9	78.7	55.1	1963 Pontiac Bonneville Convertible, Automobile-Catalog / Over-Drive Magazine	1963单年尺寸明确；高度55.1，宽78.7	可入库
Pontiac Bonneville	跑车	Pontiac	Bonneville	Convertible		2	gen4	full-size convertible	1964					220	79.2	55.1	1964 Pontiac Bonneville Convertible / Sports Coupe, Conceptcarz / Automobile-Catalog	1964 Bonneville Convertible确认存在；长220.0、宽79.2，高度按1963-1964同系敞篷安全口径55.1	可入库
Pontiac Bonneville	跑车	Pontiac	Bonneville	Coupe		2	gen4	full-size coupe	1969-1970					224.6	79.8	55	1969-1970 Pontiac Bonneville Hardtop Coupe, Automobile-Catalog / Over-Drive Magazine / Carfolio	补1969-1970 Bonneville Coupe；取安全包络	可入库
Pontiac Bonneville	两厢车	Pontiac	Bonneville	Wagon	Grand Safari	4	gen5	full-size wagon	1971-1973					230.2	79.9	57.8	1971-1973 Pontiac Grand Safari Wagon / Grand Safari first generation	Grand Safari是1971-1978顶级全尺寸wagon；1971长230.2宽79.5，1973宽取79.9，高度按同代wagon包络	可入库
Pontiac Bonneville	两厢车	Pontiac	Bonneville	Wagon	Grand Safari	4	gen5	full-size wagon	1974-1976					231.3	79.6	57.8	1974-1976 Pontiac Grand Safari Wagon / Grand Safari first generation	1974-1976是第一代后期，长度231.3；版本保留Grand Safari可解决Bonneville/Wagon归属语义	可入库
2）可选_独立子系 TSV

这些不是普通版本缺口。你如果希望消费者按独立子系搜索，可以加入；否则不进入普通全量表。

tsv
主车型	分类	品牌	车型名	结构	版本	门数	代际	代际说明	年份区间	区间最小年份	区间最大年份	驾驶室类型	货斗长度_ft	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Mercedes-Benz CL-Class	跑车	Mercedes-Benz	CL-Class	Coupe		2	gen1	C140 S-Class based luxury coupe	1996-1999					199.4	75.3	56.9	1998-1999 Mercedes-Benz CL500 / CL600, Edmunds	CL-Class承接S-Class Coupe命名缺口；如你要补独立车系可加入	可选
Mercedes-Benz CL-Class	跑车	Mercedes-Benz	CL-Class	Coupe		2	gen2	C215 S-Class based luxury coupe	2000-2006					196.6	73.1	56	2000/2002/2003/2006 Mercedes-Benz CL500, Edmunds	CL-Class独立车系；非S-Class普通缺口	可选
Mercedes-Benz CL-Class	跑车	Mercedes-Benz	CL-Class	Coupe		2	gen3	C216 S-Class based luxury coupe	2007-2014					199.4	73.7	55.8	2007/2009 Mercedes-Benz CL-Class CL550, Edmunds	CL-Class独立车系；2015后回归S-Class Coupe命名	可选
Mercury Colony Park	两厢车	Mercury	Colony Park	Wagon		4	gen1	full-size wagon	1957-1958					214.2	79.1	58.3	1957-1958 Mercury Colony Park / Voyager / Commuter Wagon	独立高端wagon线；不塞回Monterey普通wagon	可选
Mercury Colony Park	两厢车	Mercury	Colony Park	Wagon		4	gen2	full-size wagon	1961-1964					214.6	80	57.9	1961-1964 Mercury Colony Park / Commuter Station Wagon	独立wagon线；若不做Mercury wagon专项，可不补	可选
Mercury Colony Park	两厢车	Mercury	Colony Park	Wagon		4	gen3	full-size wagon	1965-1968					218.4	79.6	58.8	1965-1968 Mercury Colony Park Station Wagon	独立wagon线；不作为Monterey普通版本缺口	可选
Oldsmobile Custom Cruiser	两厢车	Oldsmobile	Custom Cruiser	Wagon		4	gen1	full-size wagon	1971-1972					231.2	79.5	57.2	1971-1972 Oldsmobile Custom Cruiser Wagon / 1971 Oldsmobile Cruisers brochure	独立全尺寸wagon名称；比Oldsmobile 88 Wagon更准确	可选
Oldsmobile Custom Cruiser	两厢车	Oldsmobile	Custom Cruiser	Wagon		4	gen1	full-size wagon	1973					228.3	79.5	57.2	1973 Oldsmobile Custom Cruiser Wagon, Automobile-Catalog / 1971 Oldsmobile Cruisers brochure	独立全尺寸wagon名称；如保留88 Wagon则不要重复加入	可选
Oldsmobile Custom Cruiser	两厢车	Oldsmobile	Custom Cruiser	Wagon		4	gen1	full-size wagon	1974-1976					231.2	80	57.2	1974-1976 Oldsmobile Custom Cruiser Wagon, Automobile-Catalog / 1971 Oldsmobile Cruisers brochure	独立全尺寸wagon名称；1974-1976后期包络	可选
Oldsmobile Cutlass Supreme	跑车	Oldsmobile	Cutlass Supreme	Coupe		2	gen1	downsized G-body coupe	1978-1980					200.4	71.3	54.2	1978-1980 Oldsmobile Cutlass Supreme Coupe / Supreme Brougham Coupe	独立消费者识别子系；不补空版本Cutlass Coupe	可选
Oldsmobile Cutlass Supreme	跑车	Oldsmobile	Cutlass Supreme	Coupe		2	gen1	restyled G-body coupe	1981-1988					200	71.6	54.4	1981-1988 Oldsmobile Cutlass Supreme Coupe / 1986 Cutlass Supreme Coupe	独立消费者识别子系；不补空版本Cutlass Coupe	可选
Oldsmobile Cutlass	跑车	Oldsmobile	Cutlass	Coupe	Supreme International	2	gen6	W-body FWD coupe	1989					192.1	71	52.8	1989 Oldsmobile Cutlass Supreme International Series Coupe, Automobile-Catalog / AutoDetective	特殊子系；若主表只保普通版，可不加入	可选
3）不补_断代或命名承接 TSV
tsv
主车型	结构	版本	门数	缺失年份区间	结论	原因
Mercedes-Benz C-Class	Sedan	AMG	4	2001	不补	特殊版本断代，不追补
Mercedes-Benz C-Class	Sedan	AMG	4	2007	不补	特殊版本断代，不追补
Mercedes-Benz C-Class	Sedan	AMG	4	2015	不作为普通缺口	AMG属于特殊版本；如果不管特殊版本断代，可不补
Mercedes-Benz C-Class	Sedan	AMG	4	2022	不补	特殊版本断代，不追补
Mercedes-Benz S-Class	Coupe/Convertible	PHEV	2	2018	不补	PHEV属于特殊版本，且资料主要对应Sedan
Mercedes-Benz SL-Class	Roadster	AMG	2	2021	不补	AMG特殊版本换代空窗，不追补
Mercury Sable	Sedan		4	2006-2007	不补	Sable名称2008-2009由Montego/Taurus体系回归，2006-2007不补
Mercury Tracer	Wagon		4	1995-1996	不补	普通wagon结构不宜补1995-1996，建议视为结构停产
Oldsmobile Cutlass	Sedan	RWD	4	1979-1980	不补	RWD版本口径混乱，不作为普通版缺口
Oldsmobile 88	Wagon		4	1965-1970	不补	Oldsmobile全尺寸wagon更适合Custom Cruiser/Vista Cruiser等独立名称，不补88 Wagon
Oldsmobile Cutlass	Coupe		2	1978-1988	不补空版本	应由Cutlass Supreme / Calais / 442 / Hurst Olds等子系承接；普通空版本不补
Oldsmobile Cutlass Calais	Coupe		2	1978-1984	默认不补	Calais属于可选独立子系；Cutlass Supreme已覆盖尺寸
Mercedes-Benz S-Class	Coupe		2	1996-2014	不补到S-Class	由CL-Class承接；如做独立子系可加入CL-Class
Mercury Monterey	Wagon		4	1961-1968	不补到Monterey	更适合Colony Park/Commuter，不污染Monterey普通wagon

汇总：

tsv
表	数量
新增_可入库	31
可选_独立子系	12
不补_断代或命名承接	14

下一步可以把 新增_可入库 做成可链表操作表，带插入参考行号。

