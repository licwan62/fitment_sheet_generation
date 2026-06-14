# Auto next transcript
开始时间：2026-06-15 01:20:42
发送内容：下一步


--- Round 1 / 手动初始 prompt 回复 ---
ChatGPT 说：继续核对剩余待终核项。我这轮优先把还能补齐尺寸、能升级为可入库的记录处理掉；仍存在主车型归属争议的，会明确保留待终核原因。继续 批次08：剩余待终核行二次核对。这轮重点把 Pontiac Bonneville Convertible 和 Grand Safari 的尺寸口径再收紧，并修正上一轮中部分年份段的包络值。
下面仍按你的全量表字段顺序输出：
tsv主车型	分类	品牌	车型名	结构	版本	门数	代际	代际说明	年份区间	区间最小年份	区间最大年份	驾驶室类型	货斗长度_ft	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态Pontiac Bonneville	跑车	Pontiac	Bonneville	Convertible		2	gen3	wide-track full-size convertible	1959-1960					220.7	80.7	56	1959-1960 Pontiac Bonneville Convertible, Conceptcarz / Automobile-Catalog	补1959-1960 Bonneville Convertible；1960 Conceptcarz给出220.7/80.7/56.0，1959 Automobile-Catalog给出220.7/80.0，取安全包络	可入库Pontiac Bonneville	跑车	Pontiac	Bonneville	Convertible		2	gen4	full-size convertible	1961					217	78.2	55.6	1961 Pontiac Bonneville Convertible, Automobile-Catalog / autoevolution	1961单年尺寸明确，不建议并入1962-1964	可入库Pontiac Bonneville	跑车	Pontiac	Bonneville	Convertible		2	gen4	full-size convertible	1962					218.6	78.6	54.9	1962 Pontiac Bonneville Convertible, Automobile-Catalog / Conceptcarz	1962单年尺寸明确，和1961、1963-1964不同	可入库Pontiac Bonneville	跑车	Pontiac	Bonneville	Convertible		2	gen4	full-size convertible	1963					218.9	78.7	55.1	1963 Pontiac Bonneville Convertible, Automobile-Catalog / Over-Drive Magazine	1963单年尺寸明确；高度55.1，宽78.7	可入库Pontiac Bonneville	跑车	Pontiac	Bonneville	Convertible		2	gen4	full-size convertible	1964					220	79.2	55.1	1964 Pontiac Bonneville Convertible / Sports Coupe, Conceptcarz / Automobile-Catalog	1964长度220.0，宽度按Automobile-Catalog同系Sports Coupe 79.2，Convertible高度沿用1963-1964近似口径55.1，建议后续若找到官方高度再终核	待终核Pontiac Bonneville	两厢车	Pontiac	Bonneville	Wagon	Grand Safari	4	gen5	full-size wagon	1971-1973					230.2	79.9	57.8	1971-1973 Pontiac Grand Safari Wagon, Automobile-Catalog / Pontiac Grand Safari	1971 Grand Safari长230.2宽79.5；1973 wagon宽度可到79.9，取安全包络；高度仍沿用wagon包络57.8	待终核Pontiac Bonneville	两厢车	Pontiac	Bonneville	Wagon	Grand Safari	4	gen5	full-size wagon	1974-1976					231.3	79.6	57.8	1974-1976 Pontiac Grand Safari Wagon, Automobile-Catalog / Pontiac Grand Safari	1974 Grand Safari长231.3宽79.6；1976同属第一代后期，保留1974-1976包络	待终核
这轮可以把以下几条从 待终核 升级为 可入库：
tsv主车型	结构	版本	年份区间	新状态Pontiac Bonneville	Convertible		1959-1960	可入库Pontiac Bonneville	Convertible		1961	可入库Pontiac Bonneville	Convertible		1962	可入库Pontiac Bonneville	Convertible		1963	可入库
仍建议保持 待终核 的是：
tsv主车型	结构	版本	年份区间	原因Pontiac Bonneville	Convertible		1964	Convertible高度未直接锁定，暂按1963-1964相近口径Pontiac Bonneville	Wagon	Grand Safari	1971-1973	高度仍是wagon安全包络，版本/主车型归属需统一Pontiac Bonneville	Wagon	Grand Safari	1974-1976	高度仍是wagon安全包络，版本/主车型归属需统一
依据：1960 Bonneville Convertible 的 Conceptcarz 规格给出长 220.7 in、宽 80.7 in、高 56.0 in；1959 Automobile-Catalog 给出 Convertible 长 220.7 in、宽 80.0 in，所以 1959-1960 取 220.7/80.7/56.0 更安全。conceptcarz.com+1 1961 Automobile-Catalog / autoevolution 支持 1961 Bonneville Convertible 为 217.0/78.2/55.6。汽车目录+1 1962 Automobile-Catalog 给出 Convertible 218.6/78.6/54.9，1963 Automobile-Catalog 给出 218.9/78.7/55.1。汽车目录+1 1971 Grand Safari Wagon 的 Automobile-Catalog 规格给出长 230.2 in、宽 79.5 in；1974 Grand Safari Wagon 给出长 231.3 in、宽 79.6 in，且 Grand Safari 是 1971-1978 的 Pontiac 顶级全尺寸 wagon。汽车目录+2汽车目录+2


--- Round 2 / 下一步回复 ---
继续 批次09：剩余待终核行继续收敛。这轮主要修正/确认 Mercury wagon 和 Oldsmobile Cutlass 早期 2 门/敞篷 的尺寸口径。

下面仍按你的全量表字段顺序输出：

tsv
主车型	分类	品牌	车型名	结构	版本	门数	代际	代际说明	年份区间	区间最小年份	区间最大年份	驾驶室类型	货斗长度_ft	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Mercury Monterey	两厢车	Mercury	Monterey	Wagon		4	gen2	full-size wagon	1955-1956					206.3	76.4	61.2	1955-1956 Mercury Monterey / full-size Mercury Station Wagon	1955-1956可作为Monterey wagon补行；长宽高取1955 Mercury full-size安全口径，1956宽度取76.4	可入库
Mercury Colony Park	两厢车	Mercury	Colony Park	Wagon		4	gen1	full-size wagon	1957-1958					214.2	79.1	58.3	1957-1958 Mercury Colony Park / Voyager / Commuter Wagon	1957起更适合归Colony Park/Voyager/Commuter，不建议继续放Monterey Wagon；1958 Colony Park长214.2宽79.1，高度暂用1957-1958 wagon包络	待终核
Mercury Colony Park	两厢车	Mercury	Colony Park	Wagon		4	gen2	full-size wagon	1961-1964					214.6	80	57.9	1961-1964 Mercury Colony Park / Commuter Station Wagon	1961-1964 Mercury wagon建议另建Colony Park/Commuter；1964 wagon资料可支撑210.3/80/57.9，长度取1961 full-size 214.6安全包络	待终核
Mercury Colony Park	两厢车	Mercury	Colony Park	Wagon		4	gen3	full-size wagon	1965-1968					218.4	79.6	58.8	1965-1968 Mercury Colony Park Station Wagon	1965-1968建议另建Colony Park；长宽取1965 full-size安全口径，高度仍待更精确wagon来源	待终核
Oldsmobile Cutlass	跑车	Oldsmobile	Cutlass	Convertible		2	gen2	intermediate convertible	1965					204.3	74.4	54	1965 Oldsmobile Cutlass Convertible / 1965 Oldsmobile mid-size fact sheet	1965单年宽度74.4，高度54.0；不建议与1966-1967直接合并	可入库
Oldsmobile Cutlass	跑车	Oldsmobile	Cutlass	Convertible		2	gen2	intermediate convertible	1966-1967					204.2	76.3	53	1966-1967 Oldsmobile Cutlass Supreme Convertible / Conceptcarz	1966-1967 Cutlass/Cutlass Supreme Convertible尺寸接近，取1967安全宽度76.3	可入库
Oldsmobile Cutlass	跑车	Oldsmobile	Cutlass	Coupe		2	gen2	intermediate coupe	1966-1967					204.2	76.3	53	1966-1967 Oldsmobile Cutlass Sports Coupe / Cutlass Supreme Sports Coupe	补1966-1967 Coupe；1967 Conceptcarz支持204.2/76.3/53.0	可入库

这轮可以升级为 可入库 的是：

tsv
主车型	结构	版本	年份区间	新状态
Mercury Monterey	Wagon		1955-1956	可入库
Oldsmobile Cutlass	Convertible		1965	可入库
Oldsmobile Cutlass	Convertible		1966-1967	可入库
Oldsmobile Cutlass	Coupe		1966-1967	可入库

仍保持 待终核 的是：

tsv
主车型	结构	版本	年份区间	原因
Mercury Colony Park	Wagon		1957-1958	1957具体高度/是否应拆Voyager/Commuter仍需确认
Mercury Colony Park	Wagon		1961-1964	Colony Park/Commuter命名归属仍需统一，长度取安全包络
Mercury Colony Park	Wagon		1965-1968	wagon高度仍缺直接来源，先不升级

依据简述：1955 Mercury Monterey/全尺寸车身资料支持长 206.3 in、宽 75.0-76.4 in、高 61.2 in，1956可用同平台宽度 76.4 in 作安全包络。
conceptcarz.com
+1
 1958 Colony Park Station Wagon 资料明确长 214.2 in、宽 79.1 in，但高度仍需更稳定 wagon 来源，所以继续待终核。
汽车目录
 Mercury Commuter 资料显示其 1957-1968 的 wagon 线与 Monterey/Colony Park关系密切，说明 1957-1968 不宜继续简单写 Monterey Wagon。
维基百科
 1964 Mercury wagon 资料支持 210.3 / 80.0 / 57.9，1961 Mercury full-size 支持 214.6 / 79.9 / 55.0，所以 1961-1964 先用安全包络。
汽车目录
+1
 1965 Mercury full-size资料支持 218.4 in 长度和约 79.4-79.6 in 宽度，但 wagon 高度还没有直接锁定。
汽车目录
+1
 Oldsmobile 1965 mid-size 资料支持 Cutlass 2-door 高度 54.0 in、长度 204.3 in；1967 Cutlass Supreme Convertible / Sports Coupe 资料支持 204.2 / 76.3 / 53.0。
over-drive-magazine.com
+1


--- Round 3 / 下一步回复 ---
继续 批次10：Mercedes CL-Class / Oldsmobile Cutlass Supreme 核对。这轮主要把上一批里“另建主车型补行”的待终核项收紧，尤其是 CL-Class 三段和 Cutlass Supreme / International。

下面仍按你的全量表字段顺序输出：

tsv
主车型	分类	品牌	车型名	结构	版本	门数	代际	代际说明	年份区间	区间最小年份	区间最大年份	驾驶室类型	货斗长度_ft	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Mercedes-Benz CL-Class	跑车	Mercedes-Benz	CL-Class	Coupe		2	gen1	C140 S-Class based luxury coupe	1996-1999					199.4	75.3	56.9	1998-1999 Mercedes-Benz CL500 / CL600, Edmunds	另建CL-Class承接S-Class Coupe命名缺口；1996-1999 C140取Edmunds CL500/CL600安全包络	可入库
Mercedes-Benz CL-Class	跑车	Mercedes-Benz	CL-Class	Coupe		2	gen2	C215 S-Class based luxury coupe	2000-2006					196.6	73.1	56	2000/2002/2003/2006 Mercedes-Benz CL500, Edmunds	另建CL-Class C215 Coupe；2002高度56.0高于2000/2003/2006，取安全包络	可入库
Mercedes-Benz CL-Class	跑车	Mercedes-Benz	CL-Class	Coupe		2	gen3	C216 S-Class based luxury coupe	2007-2014					199.4	73.7	55.8	2007/2009 Mercedes-Benz CL-Class CL550, Edmunds	另建CL-Class C216 Coupe；2011 CarsGuide长度虽报201.2，但美国Edmunds 2007/2009为199.4/73.7/55.8，先按美规Edmunds口径	可入库
Oldsmobile Cutlass Supreme	跑车	Oldsmobile	Cutlass Supreme	Coupe		2	gen1	downsized G-body coupe	1978-1980					200.4	71.3	54.2	1978-1980 Oldsmobile Cutlass Supreme Coupe / Supreme Brougham Coupe	另建Cutlass Supreme Coupe；1978 Conceptcarz高54.2，长度取1980安全包络200.4	可入库
Oldsmobile Cutlass Supreme	跑车	Oldsmobile	Cutlass Supreme	Coupe		2	gen1	restyled G-body coupe	1981-1988					200	71.6	54.4	1981-1988 Oldsmobile Cutlass Supreme Coupe / 1986 Cutlass Supreme Coupe	另建Cutlass Supreme Coupe；1986 Conceptcarz支持200.0/71.6/54.4，后续如要更细可拆年款	可入库
Oldsmobile Cutlass	跑车	Oldsmobile	Cutlass	Coupe	Supreme International	2	gen6	W-body FWD coupe	1989					192.1	71	52.8	1989 Oldsmobile Cutlass Supreme International Series Coupe, Automobile-Catalog / AutoDetective	补1989 Supreme International Coupe；该记录若要更准确，主车型/车型名也可改为Cutlass Supreme，版本International	可入库
Oldsmobile Cutlass Calais	跑车	Oldsmobile	Cutlass Calais	Coupe		2	gen1	G-body coupe / sport trim	1978-1984					200.1	71.3	54.2	1978-1984 Oldsmobile Cutlass Calais / Supreme Calais Coupe	可选补；如果保留Calais消费者识别名则入库，否则可由Cutlass Supreme Coupe覆盖	待终核

这轮可以明确升级为 可入库 的是：

tsv
主车型	结构	版本	年份区间	新状态
Mercedes-Benz CL-Class	Coupe		1996-1999	可入库
Mercedes-Benz CL-Class	Coupe		2000-2006	可入库
Mercedes-Benz CL-Class	Coupe		2007-2014	可入库
Oldsmobile Cutlass Supreme	Coupe		1978-1980	可入库
Oldsmobile Cutlass Supreme	Coupe		1981-1988	可入库
Oldsmobile Cutlass	Coupe	Supreme International	1989	可入库

仍建议保持 待终核 / 可选补 的是：

tsv
主车型	结构	版本	年份区间	原因
Oldsmobile Cutlass Calais	Coupe		1978-1984	Calais更像消费者可识别子系/运动化配置；如果Cutlass Supreme已覆盖尺寸，可不单独补

依据简述：1998-1999 CL500/CL600 Edmunds 规格均为 199.4 / 75.3 / 56.9 in，适合 C140 段安全包络；2000、2003、2006 CL500 Edmunds 均为 196.6 / 73.1 / 55.0 in，但 2002 Edmunds 高度为 56.0 in，所以 C215 段取 56.0 更安全。
Edmunds
+5
Edmunds
+5
Edmunds
+5
 2007 CL550 Edmunds 为 199.4 / 73.7 / 55.8 in，2009 CL-Class Edmunds高度约 55.7 in，所以 C216 段取 199.4 / 73.7 / 55.8。
Edmunds
+1
 1978 Cutlass Supreme Coupe 资料支持 197.7 / 71.3 / 54.2 in，1986 Cutlass Supreme Coupe 资料支持 200.0 / 71.6 / 54.4 in，1989 Cutlass Supreme International Coupe 支持 192.1 / 71.0 / 52.8 in。
conceptcarz.com
+2
conceptcarz.com
+2


--- Round 4 / 下一步回复 ---
继续 批次11：Oldsmobile 88 / Custom Cruiser 核对。这轮主要修正前面仍有疑问的 Oldsmobile 88 Sedan/Wagon，以及确认哪些应该继续放 Oldsmobile 88，哪些更适合另建/转成 Oldsmobile Custom Cruiser。

源表仍是你上传的当前全量表。

粘贴的文本 (1)

tsv
主车型	分类	品牌	车型名	结构	版本	门数	代际	代际说明	年份区间	区间最小年份	区间最大年份	驾驶室类型	货斗长度_ft	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Oldsmobile 88	三厢车	Oldsmobile	88	Sedan		4	gen7	full-size	1972					222.1	79.5	54.3	1972 Oldsmobile Delta 88 Royale Town Sedan, Automobile-Catalog	补1972 Oldsmobile 88 Sedan；长宽明确，高度按同代Town Sedan安全口径	可入库
Oldsmobile 88	三厢车	Oldsmobile	88	Sedan		4	gen7	full-size	1975					226.9	79.8	54.3	1975 Oldsmobile Delta 88 / Delta 88 Royale Town Sedan, Automobile-Catalog	补1975 Oldsmobile 88 Sedan；1975长226.9、宽79.8明确，高度按同代Town Sedan安全口径	待终核
Oldsmobile Custom Cruiser	两厢车	Oldsmobile	Custom Cruiser	Wagon		4	gen1	full-size wagon	1971-1972					231.2	79.5	57.2	1971-1972 Oldsmobile Custom Cruiser Wagon	建议另建Custom Cruiser，不继续写Oldsmobile 88 Wagon；1971起为Oldsmobile全尺寸wagon回归，127英寸轴距	待终核
Oldsmobile Custom Cruiser	两厢车	Oldsmobile	Custom Cruiser	Wagon		4	gen1	full-size wagon	1973					228.3	79.5	57.2	1973 Oldsmobile Custom Cruiser Wagon, Automobile-Catalog	建议另建Custom Cruiser；1973长228.3、宽79.5明确，高度沿用同代wagon包络	待终核
Oldsmobile Custom Cruiser	两厢车	Oldsmobile	Custom Cruiser	Wagon		4	gen1	full-size wagon	1974-1976					231.2	79.5	57.2	1974-1976 Oldsmobile Custom Cruiser Wagon	建议另建Custom Cruiser；1974-1976继续同代clamshell full-size wagon，后续若查到1974/1975/1976精确差异再拆	待终核

这轮的关键结论：

tsv
对象	处理结论
Oldsmobile 88 Sedan 1972	可入库补行
Oldsmobile 88 Sedan 1975	建议补行，但高度仍建议终核，暂待终核
Oldsmobile 88 Wagon 1971/1973/1974-1976	不建议继续放Oldsmobile 88 Wagon，建议转成/另建 Oldsmobile Custom Cruiser Wagon
Oldsmobile 88 Wagon 1965-1970	继续不补；Oldsmobile全尺寸wagon是1971 Custom Cruiser回归，不应硬补88 Wagon

依据：Oldsmobile 88 第七代 1971-1976 使用 GM B-body，1971 年全尺寸车重新设计，1974 年长度达到 226.9 in；1971 年 Custom Cruiser 作为 Oldsmobile 自 1964 后首个 full-size wagon 回归，并使用 88 的 B-body 平台和更长 127 in 轴距。
维基百科
 1975 Delta 88 Town Sedan 的 Automobile-Catalog 数据支持长 226.9 in、宽 79.8 in。
汽车目录
+1
 1973 Custom Cruiser Wagon 的 Automobile-Catalog 数据支持长 228.3 in、宽 79.5 in。
汽车目录
 Custom Cruiser 1971-1976 的生产数据也支持这一段应作为独立 wagon 线处理，而不是简单并入 88 Wagon。
维基百科


--- Round 5 / 下一步回复 ---
继续 批次12：Mercury Colony Park / Cutlass Calais / Pontiac Grand Safari 收尾核对。这轮把剩余几条“可选补 / 待终核”进一步分类：能入库的升级，仍不确定的保留待终核。

tsv
主车型	分类	品牌	车型名	结构	版本	门数	代际	代际说明	年份区间	区间最小年份	区间最大年份	驾驶室类型	货斗长度_ft	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Mercury Colony Park	两厢车	Mercury	Colony Park	Wagon		4	gen1	full-size wagon	1957-1958					214.2	79.1	58.3	1957-1958 Mercury Colony Park / Voyager / Commuter Wagon	1957起Colony Park为Mercury旗舰wagon线；1958 Colony Park长214.2宽79.1，高度暂用1957-1958 wagon包络	待终核
Mercury Colony Park	两厢车	Mercury	Colony Park	Wagon		4	gen2	full-size wagon	1961-1964					214.6	80	57.9	1961-1964 Mercury Colony Park / Commuter Station Wagon	Colony Park/Commuter归属仍需统一；1961 full-size Mercury长214.6宽79.9，1964 wagon高度约57.9，取安全包络	待终核
Mercury Colony Park	两厢车	Mercury	Colony Park	Wagon		4	gen3	full-size wagon	1965-1968					218.4	79.6	58.8	1965-1968 Mercury Colony Park Station Wagon	1965-1968建议另建Colony Park；长宽可取1965 full-size安全包络，高度仍缺直接稳定来源	待终核
Oldsmobile Cutlass Calais	跑车	Oldsmobile	Cutlass Calais	Coupe		2	gen1	G-body coupe / sport trim	1978-1984					200.4	71.3	54.2	1978-1984 Oldsmobile Cutlass Calais / Cutlass Supreme Calais Coupe	可选补；如果你希望消费者按Calais查找，则保留；若Cutlass Supreme已覆盖尺寸，可不单独补	待终核
Pontiac Bonneville	两厢车	Pontiac	Bonneville	Wagon	Grand Safari	4	gen5	full-size wagon	1971-1973					230.2	79.9	57.8	1971-1973 Pontiac Grand Safari Wagon, Automobile-Catalog / Pontiac Grand Safari	建议保留在Bonneville下但版本统一Grand Safari；高度仍按wagon安全包络	待终核
Pontiac Bonneville	两厢车	Pontiac	Bonneville	Wagon	Grand Safari	4	gen5	full-size wagon	1974-1976					231.3	79.6	57.8	1974-1976 Pontiac Grand Safari Wagon, Automobile-Catalog / Pontiac Grand Safari	建议保留在Bonneville下但版本统一Grand Safari；1974-1976长度更大，单独保留	待终核

本轮结论：

tsv
对象	结论	原因
Mercury Colony Park 1957-1958	继续待终核	1958长宽明确，但1957具体高度/是否拆Voyager/Commuter还需统一
Mercury Colony Park 1961-1964	继续待终核	Colony Park/Commuter命名归属仍需统一，尺寸为安全包络
Mercury Colony Park 1965-1968	继续待终核	wagon高度缺直接稳定来源，先不升可入库
Oldsmobile Cutlass Calais 1978-1984	可选补，继续待终核	如果Cutlass Supreme已经覆盖尺寸，Calais可不单独补；如果消费者会按Calais查找，则保留
Pontiac Grand Safari 1971-1976	继续待终核	建议版本统一Grand Safari，但是否另建Pontiac Grand Safari主车型需你确认

依据简述：1958 Mercury Colony Park Station Wagon 的长宽为 214.2 / 79.1 in；Colony Park 1957 年起是 Mercury 的旗舰 station wagon 线，和 Commuter/Voyager 属于同一 wagon体系，所以归属还需要统一。
汽车目录
+1
 1964 Mercury Colony Park 确认为 5-door wagon，Mercury Commuter资料显示 1957-1968 这一段存在 Commuter/Colony Park/Monterey 之间的 wagon命名关系，因此不建议直接把这些年写成 Monterey Wagon。
维基百科
+1
 1978 Cutlass/Calais/Supreme 的尺寸基本在 197.7-200.4 / 71.3 / 54.2 in 范围内，因此 Calais是否单独补更多是消费者识别名策略，而不是尺寸必要性。
conceptcarz.com
+2
汽车目录
+2


--- Round 6 / 下一步回复 ---
下面是 批次13：剩余待终核的最终处理建议表。
这一步不再强行新增尺寸，而是把剩余几类分成：继续待终核保留、可选补、建议另建主车型、暂不补。源表仍是你上传的当前全量表。

粘贴的文本 (1)

tsv
对象	建议结论	是否进入新增表	原因	后续动作
Mercury Colony Park Wagon 1957-1958	继续待终核	可以进入待终核新增表	1958 Colony Park长宽有依据，但1957具体尺寸、Voyager/Commuter/Colony Park命名关系还没完全统一	先作为 Mercury Colony Park Wagon 待终核补行，不要放回 Monterey Wagon
Mercury Colony Park Wagon 1961-1964	继续待终核	可以进入待终核新增表	1961-1964 Mercury wagon 存在，但 Colony Park / Commuter / Monterey wagon 归属容易混淆	保留 Mercury Colony Park Wagon 1961-1964，状态待终核
Mercury Colony Park Wagon 1965-1968	继续待终核	可以进入待终核新增表	1965-1968 Mercury wagon 长宽可估，但 wagon 高度仍缺直接稳定来源	保留 Mercury Colony Park Wagon 1965-1968，状态待终核
Oldsmobile Cutlass Calais Coupe 1978-1984	可选补	不建议默认进入新增表	Calais 与 Cutlass Supreme 尺寸高度接近，若 Cutlass Supreme 已覆盖，Calais不是尺寸必要记录	除非你希望消费者按 Calais 查找，否则先不补
Pontiac Bonneville Wagon Grand Safari 1971-1973	建议保留待终核	可以进入待终核新增表	Grand Safari 是消费者可识别 wagon 名称，但是否另建 Pontiac Grand Safari 主车型还需业务统一	如果主车型保持 Bonneville，则版本写 Grand Safari；如果更规范，另建 Pontiac Grand Safari
Pontiac Bonneville Wagon Grand Safari 1974-1976	建议保留待终核	可以进入待终核新增表	1974-1976 长度更大，适合和 1971-1973 分开；但主车型归属同样需确认	同上，建议版本统一 Grand Safari
Oldsmobile Custom Cruiser Wagon 1971-1976	建议另建主车型	可以进入待终核新增表	它比 “Oldsmobile 88 Wagon” 更准确，是 Oldsmobile 全尺寸 wagon 的消费者识别名	建议不要再补 Oldsmobile 88 Wagon，改补 Oldsmobile Custom Cruiser
Mercedes-Benz CL-Class Coupe 1996-2014	建议另建主车型	可以进入可入库新增表	CL-Class 承接 S-Class Coupe 命名缺口，不能补到 S-Class Coupe	按 CL-Class 三段加入新增表

按“是否继续补进表”的最终建议：

tsv
主车型	结构	版本	年份区间	建议状态	是否补入新增表
Mercury Colony Park	Wagon		1957-1958	待终核	补入
Mercury Colony Park	Wagon		1961-1964	待终核	补入
Mercury Colony Park	Wagon		1965-1968	待终核	补入
Oldsmobile Cutlass Calais	Coupe		1978-1984	可选补	默认不补
Pontiac Bonneville	Wagon	Grand Safari	1971-1973	待终核	补入
Pontiac Bonneville	Wagon	Grand Safari	1974-1976	待终核	补入
Oldsmobile Custom Cruiser	Wagon		1971-1976	待终核	补入
Mercedes-Benz CL-Class	Coupe		1996-2014	可入库	补入

所以到这一步，建议你把缺失年代补充结果分成三张表：

tsv
表名	内容
新增_可入库	尺寸完整、归属明确，可以直接加入全量表
新增_待终核	尺寸基本有，但归属/高度/版本语义仍需后续核对
不补_确认断代或命名承接	不应补入原主车型，防止污染全量表

下一步我建议做 最终可复制版 TSV 三表：

新增_可入库 TSV

新增_待终核 TSV

不补_说明 TSV

这样你可以先把“可入库”加入全量表，“待终核”作为补充候选表单独保留，不会污染主表。


--- Round 7 / 下一步回复 ---
下面进入 最终可复制版三表。源表仍是你上传的当前全量表，字段顺序按你指定格式。

粘贴的文本 (1)

1）新增_可入库 TSV
tsv
主车型	分类	品牌	车型名	结构	版本	门数	代际	代际说明	年份区间	区间最小年份	区间最大年份	驾驶室类型	货斗长度_ft	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Jeep Wrangler	越野车	Jeep	Wrangler	SUV	Unlimited	4	gen3	JK	2012					173.4	73.7	72.6	2012 Jeep Wrangler Unlimited Sport, Edmunds / Car and Driver	补缺失2012 JK四门Unlimited；后续可与2007-2011或2013段按尺寸再压缩	可入库
Jeep Wrangler	越野车	Jeep	Wrangler	SUV	Unlimited	4	gen4	JL	2018-2020					188.4	73.9	73.6	2018-2020 Jeep Wrangler Unlimited 4-door, Edmunds / Quadratec	补JL四门普通版；不要用原第2261行承接，第2261更适合改为2014-2015 JK	可入库
Chevrolet Equinox	越野车	Chevrolet	Equinox	SUV		4	gen3	compact SUV	2018-2024					183.1	72.6	65.4	2018-2024 Chevrolet Equinox	补普通燃油/普通SUV gen3；EV行应另写版本EV	可入库
Mercedes-Benz C-Class	三厢车	Mercedes-Benz	C-Class	Sedan		4	gen4	W205 compact executive	2015					184.5	71.3	56.8	2015 Mercedes-Benz C300 Sedan, Edmunds / MBUSA	补W205美规首年普通Sedan	可入库
Mercedes-Benz C-Class	三厢车	Mercedes-Benz	C-Class	Sedan	AMG	4	gen4	W205 AMG sedan	2015					187	72.4	56.5	2015 Mercedes-AMG C63 S Sedan, Edmunds / MotorTrend	补W205 AMG首年；后续可与相邻AMG段核尺寸后压缩	可入库
Mercedes-Benz S-Class	三厢车	Mercedes-Benz	S-Class	Sedan		4	gen4	W220 full-size luxury sedan	2006					203.3	73	56.9	2006 Mercedes-Benz S-Class S500 4MATIC, Edmunds	补2006 W220美规普通Sedan	可入库
Mercedes-Benz S-Class	跑车	Mercedes-Benz	S-Class	Coupe		2	gen6	C217 luxury coupe	2015-2017					198.9	74.8	55.8	2015-2017 Mercedes-Benz S-Class Coupe / S550 4MATIC Coupe	补C217前期S-Class Coupe；1996-2014不补到S-Class，应由CL-Class承接	可入库
Mercedes-Benz S-Class	跑车	Mercedes-Benz	S-Class	Coupe		2	gen6	C217 facelift luxury coupe	2019					198.9	74.8	55.6	2019 Mercedes-Benz S560 4MATIC Coupe, Car and Driver	补2019 S-Class Coupe缺失年	可入库
Mercedes-Benz S-Class	跑车	Mercedes-Benz	S-Class	Convertible		2	gen6	A217 facelift luxury cabriolet	2019					198.9	74.8	56.2	2019 Mercedes-Benz S560 Cabriolet, Edmunds / C&D / MBUSA	补2019 S-Class Cabriolet缺失年	可入库
Mercedes-Benz SL-Class	跑车	Mercedes-Benz	SL-Class	Roadster		2	gen3	R107 roadster	1972-1989					180.3	70.5	51.2	1972-1989 Mercedes-Benz SL-Class R107 / 560 SL	补R107美规SL Roadster长缺口；取后期560 SL安全包络	可入库
Mercedes-Benz CL-Class	跑车	Mercedes-Benz	CL-Class	Coupe		2	gen1	C140 S-Class based luxury coupe	1996-1999					199.4	75.3	56.9	1998-1999 Mercedes-Benz CL500 / CL600, Edmunds	另建CL-Class承接S-Class Coupe命名缺口；1996-1999 C140取Edmunds CL500/CL600安全包络	可入库
Mercedes-Benz CL-Class	跑车	Mercedes-Benz	CL-Class	Coupe		2	gen2	C215 S-Class based luxury coupe	2000-2006					196.6	73.1	56	2000/2002/2003/2006 Mercedes-Benz CL500, Edmunds	另建CL-Class C215 Coupe；2002高度56.0高于2000/2003/2006，取安全包络	可入库
Mercedes-Benz CL-Class	跑车	Mercedes-Benz	CL-Class	Coupe		2	gen3	C216 S-Class based luxury coupe	2007-2014					199.4	73.7	55.8	2007/2009 Mercedes-Benz CL-Class CL550, Edmunds	另建CL-Class C216 Coupe；2011 CarsGuide长度虽报201.2，但美国Edmunds 2007/2009为199.4/73.7/55.8，先按美规Edmunds口径	可入库
Mercury Sable	三厢车	Mercury	Sable	Sedan		4	gen3	midsize	1996					199.7	73	55.4	1996 Mercury Sable Sedan, Edmunds	补1996 Sable Sedan；注意原第2970建议改为2008-2009	可入库
Mercury Monterey	两厢车	Mercury	Monterey	Wagon		4	gen2	full-size wagon	1955-1956					206.3	76.4	61.2	1955-1956 Mercury Monterey / full-size Mercury Station Wagon	1955-1956可作为Monterey wagon补行；长宽高取1955 Mercury full-size安全口径，1956宽度取76.4	可入库
Oldsmobile 88	三厢车	Oldsmobile	88	Sedan		4	gen7	full-size	1972					222.1	79.5	54.3	1972 Oldsmobile Delta 88 Royale Town Sedan, Automobile-Catalog	补1972 Oldsmobile 88 Sedan；长宽明确，高度按同代Town Sedan安全口径	可入库
Oldsmobile 88	跑车	Oldsmobile	88	Coupe		2	gen8	downsized full-size coupe	1977-1979					217.5	76.8	54.5	1977-1979 Oldsmobile Delta 88 Coupe / Royale Coupe	补1977-1979 downsized 88 Coupe	可入库
Oldsmobile 88	跑车	Oldsmobile	88	Coupe		2	gen8	downsized full-size coupe	1980					218.4	76.3	54.7	1980 Oldsmobile Delta 88 Coupe	补1980 Coupe；尺寸与1977-1979不同，单独保留	可入库
Oldsmobile Cutlass	三厢车	Oldsmobile	Cutlass	Sedan		4	gen2	intermediate	1966					204.2	75.4	54.5	1966 Oldsmobile F-85 / Cutlass 4-Door Sedan	补1966 Cutlass/F-85 Sedan	可入库
Oldsmobile Cutlass	跑车	Oldsmobile	Cutlass	Convertible		2	gen2	intermediate convertible	1965					204.3	74.4	54	1965 Oldsmobile Cutlass Convertible / 1965 Oldsmobile mid-size fact sheet	1965单年宽度74.4，高度54.0；不建议与1966-1967直接合并	可入库
Oldsmobile Cutlass	跑车	Oldsmobile	Cutlass	Convertible		2	gen2	intermediate convertible	1966-1967					204.2	76.3	53	1966-1967 Oldsmobile Cutlass Supreme Convertible / Conceptcarz	1966-1967 Cutlass/Cutlass Supreme Convertible尺寸接近，取1967安全宽度76.3	可入库
Oldsmobile Cutlass	跑车	Oldsmobile	Cutlass	Convertible		2	gen3	intermediate convertible	1968-1972					203.6	76.8	52.9	1968-1972 Oldsmobile Cutlass / Cutlass Supreme Convertible	补1968-1972 Convertible	可入库
Oldsmobile Cutlass	跑车	Oldsmobile	Cutlass	Coupe		2	gen2	intermediate coupe	1966-1967					204.2	76.3	53	1966-1967 Oldsmobile Cutlass Sports Coupe / Cutlass Supreme Sports Coupe	补1966-1967 Coupe；1967 Conceptcarz支持204.2/76.3/53.0	可入库
Oldsmobile Cutlass	跑车	Oldsmobile	Cutlass	Coupe		2	gen3	intermediate coupe	1968-1972					203.6	76.8	53	1968-1972 Oldsmobile Cutlass / Cutlass Supreme Hardtop Coupe	补1968-1972 Coupe	可入库
Oldsmobile Cutlass Supreme	跑车	Oldsmobile	Cutlass Supreme	Coupe		2	gen1	downsized G-body coupe	1978-1980					200.4	71.3	54.2	1978-1980 Oldsmobile Cutlass Supreme Coupe / Supreme Brougham Coupe	另建Cutlass Supreme Coupe；1978 Conceptcarz高54.2，长度取1980安全包络200.4	可入库
Oldsmobile Cutlass Supreme	跑车	Oldsmobile	Cutlass Supreme	Coupe		2	gen1	restyled G-body coupe	1981-1988					200	71.6	54.4	1981-1988 Oldsmobile Cutlass Supreme Coupe / 1986 Cutlass Supreme Coupe	另建Cutlass Supreme Coupe；1986 Conceptcarz支持200.0/71.6/54.4，后续如要更细可拆年款	可入库
Oldsmobile Cutlass	跑车	Oldsmobile	Cutlass	Coupe	Supreme International	2	gen6	W-body FWD coupe	1989					192.1	71	52.8	1989 Oldsmobile Cutlass Supreme International Series Coupe, Automobile-Catalog / AutoDetective	补1989 Supreme International Coupe；该记录若要更准确，主车型/车型名也可改为Cutlass Supreme，版本International	可入库
Plymouth Barracuda	跑车	Plymouth	Barracuda	Coupe		2	gen3	E-body pony car	1970-1971					186.7	74.9	51.2	1970-1971 Plymouth Barracuda / Cuda Hardtop, Conceptcarz / Automobile-Catalog / Over-Drive Magazine	补E-body早期Coupe；后续可与原第3400修正行合并	可入库
Pontiac Bonneville	跑车	Pontiac	Bonneville	Convertible		2	gen2	one-year full-size convertible	1958					211.7	77.4	55.7	1958 Pontiac Bonneville Convertible Coupe	补1958 Convertible；独立大车身	可入库
Pontiac Bonneville	跑车	Pontiac	Bonneville	Convertible		2	gen3	wide-track full-size convertible	1959-1960					220.7	80.7	56	1959-1960 Pontiac Bonneville Convertible, Conceptcarz / Automobile-Catalog	补1959-1960 Bonneville Convertible；1960 Conceptcarz给出220.7/80.7/56.0，1959 Automobile-Catalog给出220.7/80.0，取安全包络	可入库
Pontiac Bonneville	跑车	Pontiac	Bonneville	Convertible		2	gen4	full-size convertible	1961					217	78.2	55.6	1961 Pontiac Bonneville Convertible, Automobile-Catalog / autoevolution	1961单年尺寸明确，不建议并入1962-1964	可入库
Pontiac Bonneville	跑车	Pontiac	Bonneville	Convertible		2	gen4	full-size convertible	1962					218.6	78.6	54.9	1962 Pontiac Bonneville Convertible, Automobile-Catalog / Conceptcarz	1962单年尺寸明确，和1961、1963-1964不同	可入库
Pontiac Bonneville	跑车	Pontiac	Bonneville	Convertible		2	gen4	full-size convertible	1963					218.9	78.7	55.1	1963 Pontiac Bonneville Convertible, Automobile-Catalog / Over-Drive Magazine	1963单年尺寸明确；高度55.1，宽78.7	可入库
Pontiac Bonneville	跑车	Pontiac	Bonneville	Coupe		2	gen4	full-size coupe	1969-1970					224.6	79.8	55	1969-1970 Pontiac Bonneville Hardtop Coupe, Automobile-Catalog / Over-Drive Magazine / Carfolio	补1969-1970 Bonneville Coupe；取安全包络	可入库
2）新增_待终核 TSV
tsv
主车型	分类	品牌	车型名	结构	版本	门数	代际	代际说明	年份区间	区间最小年份	区间最大年份	驾驶室类型	货斗长度_ft	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Mercedes-Benz C-Class	跑车	Mercedes-Benz	C-Class	Coupe		2	gen4	C205 coupe	2016					184.5	71.3	55.3	2016 Mercedes-Benz C-Class Coupe / C300 Coupe	补2016 C-Class Coupe；Convertible若无2016美国销售则不补	待终核
Mercury Colony Park	两厢车	Mercury	Colony Park	Wagon		4	gen1	full-size wagon	1957-1958					214.2	79.1	58.3	1957-1958 Mercury Colony Park / Voyager / Commuter Wagon	1957起Colony Park为Mercury旗舰wagon线；1958 Colony Park长214.2宽79.1，高度暂用1957-1958 wagon包络	待终核
Mercury Colony Park	两厢车	Mercury	Colony Park	Wagon		4	gen2	full-size wagon	1961-1964					214.6	80	57.9	1961-1964 Mercury Colony Park / Commuter Station Wagon	Colony Park/Commuter归属仍需统一；1961 full-size Mercury长214.6宽79.9，1964 wagon高度约57.9，取安全包络	待终核
Mercury Colony Park	两厢车	Mercury	Colony Park	Wagon		4	gen3	full-size wagon	1965-1968					218.4	79.6	58.8	1965-1968 Mercury Colony Park Station Wagon	1965-1968建议另建Colony Park；长宽可取1965 full-size安全包络，高度仍缺直接稳定来源	待终核
Oldsmobile 88	三厢车	Oldsmobile	88	Sedan		4	gen7	full-size	1975					226.9	79.8	54.3	1975 Oldsmobile Delta 88 / Delta 88 Royale Town Sedan, Automobile-Catalog	补1975 Oldsmobile 88 Sedan；1975长226.9、宽79.8明确，高度按同代Town Sedan安全口径	待终核
Oldsmobile Custom Cruiser	两厢车	Oldsmobile	Custom Cruiser	Wagon		4	gen1	full-size wagon	1971-1972					231.2	79.5	57.2	1971-1972 Oldsmobile Custom Cruiser Wagon	建议另建Custom Cruiser，不继续写Oldsmobile 88 Wagon；1971起为Oldsmobile全尺寸wagon回归，127英寸轴距	待终核
Oldsmobile Custom Cruiser	两厢车	Oldsmobile	Custom Cruiser	Wagon		4	gen1	full-size wagon	1973					228.3	79.5	57.2	1973 Oldsmobile Custom Cruiser Wagon, Automobile-Catalog	建议另建Custom Cruiser；1973长228.3、宽79.5明确，高度沿用同代wagon包络	待终核
Oldsmobile Custom Cruiser	两厢车	Oldsmobile	Custom Cruiser	Wagon		4	gen1	full-size wagon	1974-1976					231.2	79.5	57.2	1974-1976 Oldsmobile Custom Cruiser Wagon	建议另建Custom Cruiser；1974-1976继续同代clamshell full-size wagon，后续若查到1974/1975/1976精确差异再拆	待终核
Oldsmobile Cutlass Calais	跑车	Oldsmobile	Cutlass Calais	Coupe		2	gen1	G-body coupe / sport trim	1978-1984					200.4	71.3	54.2	1978-1984 Oldsmobile Cutlass Calais / Cutlass Supreme Calais Coupe	可选补；如果你希望消费者按Calais查找，则保留；若Cutlass Supreme已覆盖尺寸，可不单独补	待终核
Pontiac Bonneville	跑车	Pontiac	Bonneville	Convertible		2	gen4	full-size convertible	1964					220	79.2	55.1	1964 Pontiac Bonneville Convertible / Sports Coupe, Conceptcarz / Automobile-Catalog	1964长度220.0，宽度按同系Sports Coupe 79.2，Convertible高度沿用1963-1964近似口径55.1，建议后续若找到官方高度再终核	待终核
Pontiac Bonneville	两厢车	Pontiac	Bonneville	Wagon	Grand Safari	4	gen5	full-size wagon	1971-1973					230.2	79.9	57.8	1971-1973 Pontiac Grand Safari Wagon, Automobile-Catalog / Pontiac Grand Safari	建议保留在Bonneville下但版本统一Grand Safari；高度仍按wagon安全包络	待终核
Pontiac Bonneville	两厢车	Pontiac	Bonneville	Wagon	Grand Safari	4	gen5	full-size wagon	1974-1976					231.3	79.6	57.8	1974-1976 Pontiac Grand Safari Wagon, Automobile-Catalog / Pontiac Grand Safari	建议保留在Bonneville下但版本统一Grand Safari；1974-1976长度更大，单独保留	待终核
3）不补_确认断代或命名承接 TSV
tsv
主车型	结构	版本	门数	缺失年份区间	结论	原因
Mercedes-Benz C-Class	Sedan	AMG	4	2001	不补	2001处于W202 C43结束与W203 C32 AMG美规开始前后，按AMG Sedan口径确认断代
Mercedes-Benz C-Class	Sedan	AMG	4	2007	不补	2007处于C55 AMG末期与W204 C63 AMG前的换代空窗
Mercedes-Benz C-Class	Sedan	AMG	4	2022	不补	W206普通C-Class有2022，但AMG Sedan未同步闭合，按AMG口径确认断代
Mercedes-Benz S-Class	Coupe/Convertible	PHEV	2	2018	不补	疑似结构/版本错误；PHEV资料主要对应Sedan，不建议补Coupe/Convertible PHEV
Mercedes-Benz SL-Class	Roadster	AMG	2	2021	不补	R231/R232 AMG SL换代空窗，2022后回归
Mercury Sable	Sedan		4	2006-2007	不补	Sable名称2008-2009由Montego/Taurus体系回归，2006-2007不补Sable Sedan
Mercury Tracer	Wagon		4	1995-1996	不补	Tracer Wagon结构不宜补1995-1996，建议确认结构停产
Oldsmobile Cutlass	Sedan	RWD	4	1979-1980	不补	RWD Sedan口径与Cutlass子系/平台口径混乱，不建议硬补
Oldsmobile 88	Wagon		4	1965-1970	不补	Oldsmobile全尺寸wagon更适合按Custom Cruiser/Vista Cruiser等归属处理，不补88 Wagon
Oldsmobile Cutlass	Coupe		2	1978-1988	不补空版本	应由Cutlass Supreme / Calais / 442 / Hurst Olds等消费者可识别子系承接
Mercedes-Benz S-Class	Coupe		2	1996-2014	不补到S-Class	应由Mercedes-Benz CL-Class承接；已在新增表中补CL-Class
Mercury Monterey	Wagon		4	1961-1968	不补到Monterey	更适合另建/补Mercury Colony Park或Commuter，不建议污染Monterey主车型

汇总：

tsv
表	数量
新增_可入库	35
新增_待终核	12
不补_确认断代或命名承接	12

