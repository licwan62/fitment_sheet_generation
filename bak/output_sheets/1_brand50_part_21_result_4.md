# 文件名：1_brand50_part_21.tsv


--- Round 1 / 首次发送 ---
已按文件要求处理本批次：原始数据来自你上传的 1_brand50_part_21.tsv 内容。

粘贴的文本 (1)

更新点
车型	操作	描述
Lexus RX / Hyundai Santa Fe / Hyundai Sonata 等	字段升级	从旧字段升级为最新全量表字段：品牌、分类、结构、版本、代际拆开
Pontiac Firebird / Mercury Marquis	拆出	原 coupe/conv、sdn/cou/wgn 等合并结构拆成单一结构；未逐结构核对的拆分行标为待终核
Ford Crown Victoria	保留并结构化	保留普通车与老爷车记录，统一为 Sedan 结构
Subaru Outback Sp	待终核	原 hch/wgn 合并结构不能直接可入库，拆成 Hatchback / Wagon 并标待终核
多个旧普通车空状态行	待终核	参考车型未覆盖完整年份范围的，暂不标可入库
阶段性 TSV
tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	1999-2003	180.1	71.5	65.7	1999 Lexus RX 300 SUV Base	参考车型未覆盖完整年份范围	待终核: 2000-2003
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2004-2009	186.2	72.6	66.1	2004 Lexus RX 330	参考车型未覆盖完整年份范围	待终核: 2005-2009
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2010-2015	187.8	74.2	66.3	2010 Lexus RX 350	参考车型未覆盖完整年份范围	待终核: 2011-2015
Lexus RX	Lexus	越野车	SUV	Std.	gen4 midsize SUV	2016-2022	192.5	74.6	67.7	2016 Lexus RX 350	excl: L；参考车型未覆盖完整年份范围	待终核: 2017-2022
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2018	196.9	74.6	67.7	2018 Lexus RX 350L Base	长轴版	
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2019-2022	196.9	74.6	67.3	2022 Lexus RX 350L Base	参考车型未覆盖完整年份范围	待终核: 2019-2021
Lexus RX	Lexus	越野车	SUV	inc: PHEV	gen5 midsize SUV	2023-2026	192.5	75.6	67.3	2026 Lexus RX 450h+ Luxury	参考车型未覆盖完整年份范围	待终核: 2023-2025
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身；原coupe/conv拆分	待终核: Coupe 1968-1969
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身；原coupe/conv拆分	待终核: Convertible 1967-1969
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1970-1973	191.1	73.4	49.3	1970 Firebird	第二代早期；原coupe/Trans Am拆分	待终核: 1971-1973结构
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1974-1981	196.8	73.2	49.6	1974-1981 Trans Am / Formula	保险杠增长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1982-1988	191.8	72.4	50	1988 Firebird / Trans Am	低矮楔形；参考车型未覆盖完整年份范围	待终核: 1982-1987
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1989-1992	195.2	72.8	49.7	1990/1991 Firebird	末期造型更长；参考车型未覆盖完整年份范围	待终核: 1989/1992
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Coupe 1994-1997
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Convertible 1993-1997
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Coupe 1998-1999/2001-2002
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Convertible 1998-2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2001-2006	177.2	72.6	65.9	2001 Hyundai Santa Fe GL	参考车型未覆盖完整年份范围	待终核: 2002-2006
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen2 midsize SUV	2007-2012	184.1	74.4	67.9	2007/2012 Hyundai Santa Fe	中间年份待确认	待终核: 2008-2011
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2013-2018	185	74	66.5	2018 Hyundai Santa Fe Sport	短轴版；参考车型未覆盖完整年份范围	待终核: 2013-2017
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2013-2018	193.1	74.2	66.9	2013 Hyundai Santa Fe Limited	长轴版；参考车型未覆盖完整年份范围	待终核: 2014-2018
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2019	193.1	74.2	66.9	2019 Hyundai Santa Fe XL	长轴版	
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen4 midsize SUV	2019-2023	188.4	74.4	66.3	2019-2023 Hyundai Santa Fe		
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen5 midsize SUV	2024-2026	190.2	74.8	69.7	2024-2026 Hyundai Santa Fe Limited/Calligraphy		
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2001	172.2	67.1	60	2001 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2001	172.2	67.1	60	2001 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen3 compact	2008-2011	173.8	68.5	58.3	2008-2011 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen3 compact	2008-2011	173.8	68.5	58.3	2008-2011 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen5 midsize	1983-1986	196.5	71	53.8	1986 Mercury Marquis brochure / Mercury Marquis specs	中型四门；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen5 midsize	1983-1986	196.5	71	54.4	1986 Mercury Marquis brochure / Mercury Marquis specs	中型旅行车更高；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Coupe 1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Sedan 1967-1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Sedan 1969-1972
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Coupe 1969-1971
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Sedan 1973-1974/1976/1978
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Coupe 1973-1978
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen3 full-size	1973-1978	231	79.6	55	1975/1978 Mercury Marquis Colony Park Wagon	wagon超长；中间年份待确认	待终核: 1973-1974/1976-1977
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Sedan 1979-1982
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Coupe 1979-1982
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Wagon 1979-1982
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1992	212.4	77.8	56.7	Ford Crown Victoria	参考车型过泛	待终核: 1992
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1993-1997	212	77.8	56.8	Ford Crown Victoria	参考车型过泛	待终核: 1993-1997
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1998-2011	212	78.2	56.8	Ford Crown Victoria	参考车型过泛	待终核: 1998-2011
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen1 full-size Panther	1979-1991	212	78	56.8	Ford LTD Crown Victoria box Panther cross-ref	方正长尾厢	待终核: 1979-1991
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1992-1997	212.4	77.8	56.8	1992/1995 Ford Crown Victoria LX	圆润Panther；中间年份待确认	待终核: 1993-1994/1996-1997
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1998-2002	212	78.2	56.8	1998/2000 Ford Crown Victoria LX	facelift宽度高点；中间年份待确认	待终核: 1999/2001-2002
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2003-2011	212	77.3	56.8	2003/2008/2011 Ford Crown Victoria Sedan	后期Panther；中间年份待确认	待终核: 2004-2007/2009-2010
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen2 midsize sedan	1989-1998	185	69.7	55.3	1998 Hyundai Sonata	参考车型未覆盖完整年份范围	待终核: 1989-1997
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	1999-2005	185.4	71.6	55.5	1999 Hyundai Sonata	参考车型未覆盖完整年份范围	待终核: 2000-2005
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen4 midsize sedan	2006-2010	188.9	72.1	58	2006 Hyundai Sonata LX	参考车型未覆盖完整年份范围	待终核: 2007-2010
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen5 midsize sedan	2011-2014	189.8	72.2	57.9	2011 Hyundai Sonata / 2014 Hybrid	中间年份待确认	待终核: 2012-2013
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2015-2019	191.1	73.4	58.1	2015 Hyundai Sonata Limited 2.0T	参考车型未覆盖完整年份范围	待终核: 2016-2019
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 midsize sedan	2020-2023	192.9	73.2	56.9	2023 Hyundai Sonata Hybrid Limited	参考车型未覆盖完整年份范围	待终核: 2020-2022
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 facelift midsize sedan	2024-2026	193.3	73.2	56.9	2025-2026 Hyundai Sonata Hybrid / N Line	缺2024参考	待终核: 2024
Chevrolet Bolt EUV	Chevrolet	越野车	SUV	EV	gen1 compact EV SUV	2022-2023	169.5	69.7	63.6	2023 Chevrolet Bolt EUV	EV小型SUV；参考车型未覆盖完整年份范围	待终核: 2022

下一步。


--- Round 2 / 下一步 ---
本轮先补强了可快速确认的普通车型与 Ford Crown Victoria 关键年份：Lexus RX 1999/2000/2003、Hyundai Santa Fe 2001/2006/2007、Ford Crown Victoria 1992/1995/1997/2003/2011、Hyundai Sonata 1998/1999/2026、Chevrolet Bolt EUV 2022/2023 等关键点已用 Edmunds / C&D 交叉确认；其中 Santa Fe 2006 与 2001 不是完全同一组尺寸，所以本轮拆出 2006 单年。
Car and Driver
+14
Edmunds
+14
Edmunds
+14

更新点
车型	操作	描述
Hyundai Santa Fe	拆出	2006 年宽/高与 2001 年存在 0.1 in 差异，拆出 2006 单年
Ford Crown Victoria	值修改	普通车 1998-2011 不能统一用 78.2 宽；2003-2011 后期按 77.3 宽拆分
Chevrolet Bolt EUV	稳定	2022/2023 三维一致，推进为可入库
Hyundai Sonata	稳定	2024-2026 现款尺寸确认，推进为可入库
Lexus RX	部分补强	gen1 关键年份已核，仍缺 2001/2002 完整确认
Subaru Outback Sp / 老爷车合并结构	待核	拆分结构后不能直接沿用原合并尺寸，继续保留待终核
阶段性 TSV
tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	1999-2000	180.1	71.5	65.7	1999/2000 Lexus RX 300 SUV Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2001-2002	180.1	71.5	65.7	1999/2000/2003 Lexus RX 300 cross-ref	中间年份待确认	待终核: 2001-2002
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2003	180.1	71.5	65.7	2003 Lexus RX 300 Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2004-2009	186.2	72.6	66.1	2004 Lexus RX 330	参考车型未覆盖完整年份范围	待终核: 2005-2009
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2010-2015	187.8	74.2	66.3	2010 Lexus RX 350	参考车型未覆盖完整年份范围	待终核: 2011-2015
Lexus RX	Lexus	越野车	SUV	Std.	gen4 midsize SUV	2016-2022	192.5	74.6	67.7	2016 Lexus RX 350	excl: L；参考车型未覆盖完整年份范围	待终核: 2017-2022
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2018	196.9	74.6	67.7	2018 Lexus RX 350L Base	长轴版	
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2019-2022	196.9	74.6	67.3	2022 Lexus RX 350L Base	参考车型未覆盖完整年份范围	待终核: 2019-2021
Lexus RX	Lexus	越野车	SUV	inc: PHEV	gen5 midsize SUV	2023-2026	192.5	75.6	67.3	2026 Lexus RX 450h+ Luxury	参考车型未覆盖完整年份范围	待终核: 2023-2025
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身；原coupe/conv拆分	待终核: Coupe 1968-1969
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身；原coupe/conv拆分	待终核: Convertible 1967-1969
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1970-1973	191.1	73.4	49.3	1970 Firebird	第二代早期；原coupe/Trans Am拆分	待终核: 1971-1973结构
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1974-1981	196.8	73.2	49.6	1974-1981 Trans Am / Formula	保险杠增长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1982-1988	191.8	72.4	50	1988 Firebird / Trans Am	低矮楔形；参考车型未覆盖完整年份范围	待终核: 1982-1987
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1989-1992	195.2	72.8	49.7	1990/1991 Firebird	末期造型更长；参考车型未覆盖完整年份范围	待终核: 1989/1992
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Coupe 1994-1997
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Convertible 1993-1997
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Coupe 1998-1999/2001-2002
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Convertible 1998-2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2001	177.2	72.6	65.9	2001 Hyundai Santa Fe GL		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2002-2005	177.2	72.6	65.9	2001/2006 Hyundai Santa Fe cross-ref	中间年份待确认	待终核: 2002-2005
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2006	177.2	72.7	66	2006 Hyundai Santa Fe GLS	2006宽/高略变	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen2 midsize SUV	2007	184.1	74.4	67.9	2007 Hyundai Santa Fe Limited		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen2 midsize SUV	2008-2012	184.1	74.4	67.9	2007/2012 Hyundai Santa Fe	中间年份待确认	待终核: 2008-2011
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2013-2018	185	74	66.5	2018 Hyundai Santa Fe Sport	短轴版；参考车型未覆盖完整年份范围	待终核: 2013-2017
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2013-2018	193.1	74.2	66.9	2013 Hyundai Santa Fe Limited	长轴版；参考车型未覆盖完整年份范围	待终核: 2014-2018
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2019	193.1	74.2	66.9	2019 Hyundai Santa Fe XL	长轴版	
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen4 midsize SUV	2019-2023	188.4	74.4	66.3	2019-2023 Hyundai Santa Fe		
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen5 midsize SUV	2024-2026	190.2	74.8	69.7	2024-2026 Hyundai Santa Fe Limited/Calligraphy		
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2001	172.2	67.1	60	2001 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2001	172.2	67.1	60	2001 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen3 compact	2008-2011	173.8	68.5	58.3	2008-2011 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen3 compact	2008-2011	173.8	68.5	58.3	2008-2011 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen5 midsize	1983-1986	196.5	71	53.8	1986 Mercury Marquis brochure / Mercury Marquis specs	中型四门；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen5 midsize	1983-1986	196.5	71	54.4	1986 Mercury Marquis brochure / Mercury Marquis specs	中型旅行车更高；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Coupe 1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Sedan 1967-1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Sedan 1969-1972
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Coupe 1969-1971
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Sedan 1973-1974/1976/1978
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Coupe 1973-1978
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen3 full-size	1973-1978	231	79.6	55	1975/1978 Mercury Marquis Colony Park Wagon	wagon超长；中间年份待确认	待终核: 1973-1974/1976-1977
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Sedan 1979-1982
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Coupe 1979-1982
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Wagon 1979-1982
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1992	212.4	77.8	56.7	1992 Ford Crown Victoria Sedan LX		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1993-1997	212	77.8	56.8	1995/1997 Ford Crown Victoria LX	1993-1994/1996待确认	待终核: 1993-1994/1996
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1998-2002	212	78.2	56.8	1998/2000 Ford Crown Victoria LX	facelift宽度高点；2001-2002待确认	待终核: 1999/2001-2002
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2003-2011	212	77.3	56.8	2003/2008/2011 Ford Crown Victoria Sedan	后期Panther；宽度按后期修正	待终核: 2004-2007/2009-2010
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen2 midsize sedan	1989-1998	185	69.7	55.3	1998 Hyundai Sonata	参考车型未覆盖完整年份范围	待终核: 1989-1997
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	1999-2005	185.4	71.6	55.5	1999 Hyundai Sonata	参考车型未覆盖完整年份范围	待终核: 2000-2005
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen4 midsize sedan	2006-2010	188.9	72.1	58	2006 Hyundai Sonata LX	参考车型未覆盖完整年份范围	待终核: 2007-2010
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen5 midsize sedan	2011-2014	189.8	72.2	57.9	2011 Hyundai Sonata / 2014 Hybrid	中间年份待确认	待终核: 2012-2013
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2015-2019	191.1	73.4	58.1	2015 Hyundai Sonata Limited 2.0T	参考车型未覆盖完整年份范围	待终核: 2016-2019
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 midsize sedan	2020-2023	192.9	73.2	56.9	2023 Hyundai Sonata Hybrid Limited	参考车型未覆盖完整年份范围	待终核: 2020-2022
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 facelift midsize sedan	2024-2026	193.3	73.2	56.9	2024-2026 Hyundai Sonata Hybrid / N Line		可入库
Chevrolet Bolt EUV	Chevrolet	越野车	SUV	EV	gen1 compact EV SUV	2022-2023	169.5	69.7	63.6	2022/2023 Chevrolet Bolt EUV	EV小型SUV	可入库

下一步。


--- Round 3 / 下一步 ---
更新点
车型	操作	描述
Lexus RX	稳定/待拆	2004/2006/2008/2009 RX 330/350 三维一致；2008 RX 400h 高度/长度不同，暂不并入 Std. 行。
Edmunds
+4
Edmunds
+4
Edmunds
+4

Lexus RX	值修改待核	2010 与 2015 RX 350 为 187.8 / 74.2 / 66.3，但 2014 Edmunds 显示高度 66.7，先拆出 2014 待复核，不硬压成同一区间。
Edmunds
+2
Edmunds
+2

Lexus RX	稳定	2016 与 2022 RX 350 标准轴三维一致；2022 RX 350L 为 196.9 / 74.6 / 67.3。
Edmunds
+2
Edmunds
+2

Hyundai Santa Fe	值修改/拆分	2002 为 177.2 / 72.6 / 65.9，2005-2006 为 177.2 / 72.7 / 66.0，不能与 2001 原行完全合并。
Edmunds
+1

Hyundai Santa Fe	稳定	2008/2010/2012 与 2007 二代尺寸一致，可合并推进。
Edmunds
+2
Edmunds
+2

Hyundai Santa Fe	值修改	2013 Sport 基础版长 184.6、高 66.1；2018 Sport 2.0T 高到 66.5，所以 Sport 行保留最大高 66.5，但长度需从 185.0 拆出 2013 关键差异。
Edmunds
+2
Edmunds
+2

Hyundai Santa Fe	稳定	2013/2014/2018 长轴 Santa Fe / XL 为 193.1 / 74.2 / 66.9，可继续按长轴组推进。
Edmunds
+2
Edmunds
+2
阶段性 TSV
tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	1999-2000	180.1	71.5	65.7	1999/2000 Lexus RX 300 SUV Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2001-2002	180.1	71.5	65.7	1999/2000/2003 Lexus RX 300 cross-ref	中间年份待确认	待终核: 2001-2002
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2003	180.1	71.5	65.7	2003 Lexus RX 300 Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2004-2009	186.2	72.6	66.1	2004/2006/2008/2009 Lexus RX 330/350	2005/2007待补齐；RX 400h尺寸不同暂不并入	待终核: 2005/2007
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2010-2013	187.8	74.2	66.3	2010 Lexus RX 350	2011-2013待确认	待终核: 2011-2013
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2014	187.8	74.2	66.7	2014 Lexus RX 350	高度与2010/2015不同，待复核是否trim/口径差异	待终核: 2014高度
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2015	187.8	74.2	66.3	2015 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen4 midsize SUV	2016-2022	192.5	74.6	67.7	2016/2022 Lexus RX 350	excl: L；中间年份待确认	待终核: 2017-2021
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2018	196.9	74.6	67.7	2018 Lexus RX 350L Base	长轴版	
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2019-2022	196.9	74.6	67.3	2022 Lexus RX 350L Base	参考车型未覆盖完整年份范围	待终核: 2019-2021
Lexus RX	Lexus	越野车	SUV	inc: PHEV	gen5 midsize SUV	2023-2026	192.5	75.6	67.3	2026 Lexus RX 450h+ Luxury	参考车型未覆盖完整年份范围	待终核: 2023-2025
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身；原coupe/conv拆分	待终核: Coupe 1968-1969
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身；原coupe/conv拆分	待终核: Convertible 1967-1969
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1970-1973	191.1	73.4	49.3	1970 Firebird	第二代早期；原coupe/Trans Am拆分	待终核: 1971-1973结构
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1974-1981	196.8	73.2	49.6	1974-1981 Trans Am / Formula	保险杠增长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1982-1988	191.8	72.4	50	1988 Firebird / Trans Am	低矮楔形；参考车型未覆盖完整年份范围	待终核: 1982-1987
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1989-1992	195.2	72.8	49.7	1990/1991 Firebird	末期造型更长；参考车型未覆盖完整年份范围	待终核: 1989/1992
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Coupe 1994-1997
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Convertible 1993-1997
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Coupe 1998-1999/2001-2002
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Convertible 1998-2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2001-2002	177.2	72.6	65.9	2001/2002 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2003-2004	177.2	72.7	66	2005/2006 Hyundai Santa Fe cross-ref	2003-2004待确认	待终核: 2003-2004
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2005-2006	177.2	72.7	66	2005/2006 Hyundai Santa Fe GLS/LX	2005-2006宽/高高于2001-2002	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen2 midsize SUV	2007-2012	184.1	74.4	67.9	2007/2008/2010/2012 Hyundai Santa Fe	2009/2011待确认	待终核: 2009/2011
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2013	184.6	74	66.5	2013 Hyundai Santa Fe Sport / Sport 2.0T	同年Sport 2.0T高度取高值	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2014-2018	185	74	66.5	2018 Hyundai Santa Fe Sport / Sport 2.0T	短轴版；2014-2017待确认	待终核: 2014-2017
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2013-2018	193.1	74.2	66.9	2013/2014/2018 Hyundai Santa Fe Limited/XL	长轴版；2015-2017待确认	待终核: 2015-2017
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2019	193.1	74.2	66.9	2019 Hyundai Santa Fe XL	长轴版	
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen4 midsize SUV	2019-2023	188.4	74.4	66.3	2019-2023 Hyundai Santa Fe		
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen5 midsize SUV	2024-2026	190.2	74.8	69.7	2024-2026 Hyundai Santa Fe Limited/Calligraphy		
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2001	172.2	67.1	60	2001 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2001	172.2	67.1	60	2001 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen3 compact	2008-2011	173.8	68.5	58.3	2008-2011 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen3 compact	2008-2011	173.8	68.5	58.3	2008-2011 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen5 midsize	1983-1986	196.5	71	53.8	1986 Mercury Marquis brochure / Mercury Marquis specs	中型四门；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen5 midsize	1983-1986	196.5	71	54.4	1986 Mercury Marquis brochure / Mercury Marquis specs	中型旅行车更高；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Coupe 1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Sedan 1967-1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Sedan 1969-1972
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Coupe 1969-1971
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Sedan 1973-1974/1976/1978
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Coupe 1973-1978
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen3 full-size	1973-1978	231	79.6	55	1975/1978 Mercury Marquis Colony Park Wagon	wagon超长；中间年份待确认	待终核: 1973-1974/1976-1977
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Sedan 1979-1982
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Coupe 1979-1982
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Wagon 1979-1982
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1992	212.4	77.8	56.7	1992 Ford Crown Victoria Sedan LX		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1993-1997	212	77.8	56.8	1995/1997 Ford Crown Victoria LX	1993-1994/1996待确认	待终核: 1993-1994/1996
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1998-2002	212	78.2	56.8	1998/2000 Ford Crown Victoria LX	facelift宽度高点；2001-2002待确认	待终核: 1999/2001-2002
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2003-2011	212	77.3	56.8	2003/2008/2011 Ford Crown Victoria Sedan	后期Panther；宽度按后期修正	待终核: 2004-2007/2009-2010
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen2 midsize sedan	1989-1998	185	69.7	55.3	1998 Hyundai Sonata	参考车型未覆盖完整年份范围	待终核: 1989-1997
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	1999-2005	185.4	71.6	55.5	1999 Hyundai Sonata	参考车型未覆盖完整年份范围	待终核: 2000-2005
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen4 midsize sedan	2006-2010	188.9	72.1	58	2006 Hyundai Sonata LX	参考车型未覆盖完整年份范围	待终核: 2007-2010
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen5 midsize sedan	2011-2014	189.8	72.2	57.9	2011 Hyundai Sonata / 2014 Hybrid	中间年份待确认	待终核: 2012-2013
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2015-2019	191.1	73.4	58.1	2015 Hyundai Sonata Limited 2.0T	参考车型未覆盖完整年份范围	待终核: 2016-2019
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 midsize sedan	2020-2023	192.9	73.2	56.9	2023 Hyundai Sonata Hybrid Limited	参考车型未覆盖完整年份范围	待终核: 2020-2022
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 facelift midsize sedan	2024-2026	193.3	73.2	56.9	2024-2026 Hyundai Sonata Hybrid / N Line		可入库
Chevrolet Bolt EUV	Chevrolet	越野车	SUV	EV	gen1 compact EV SUV	2022-2023	169.5	69.7	63.6	2022/2023 Chevrolet Bolt EUV	EV小型SUV	可入库

下一步。


--- Round 4 / 下一步 ---
更新点
车型	操作	描述
Lexus RX	稳定	2017/2019/2021 标准轴 RX 350 均为 192.5 / 74.6 / 67.7，可把 2016-2022 标准轴推进为可入库。
Edmunds
+2
Edmunds
+2

Lexus RX	稳定	2019/2021 RX 350L 均为 196.9 / 74.6 / 67.3，2019-2022 L 长轴组可继续推进。
Edmunds
+1

Lexus RX	稳定	2023/2024/2025/2026 新一代 RX / RX 450h+ 均为 192.5 / 75.6 / 67.3，2023-2026 推进为可入库。
Edmunds
+3
Edmunds
+3
Edmunds
+3

Hyundai Santa Fe	稳定	2009/2011 已补强，与 2007/2008/2010/2012 尺寸一致，二代 2007-2012 推进为可入库。
Edmunds

Hyundai Santa Fe	稳定	2014/2016 长轴 Santa Fe 与 2013/2018 长轴尺寸一致，2013-2018 XL/long 可继续推进。
Edmunds
+1

Hyundai Sonata	值修改	1999-2004 与 2005 不能合并：2005 为 186.9 / 71.7 / 56.0，需从 1999-2005 行拆出。
Edmunds
+1

Hyundai Sonata	稳定	2010、2013、2016、2019、2020、2022 关键点已确认，部分年份段可推进或缩小待核范围。
Edmunds
+5
Edmunds
+5
Edmunds
+5
阶段性 TSV
tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	1999-2000	180.1	71.5	65.7	1999/2000 Lexus RX 300 SUV Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2001-2002	180.1	71.5	65.7	1999/2000/2003 Lexus RX 300 cross-ref	中间年份待确认	待终核: 2001-2002
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2003	180.1	71.5	65.7	2003 Lexus RX 300 Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2004-2009	186.2	72.6	66.1	2004/2006/2008/2009 Lexus RX 330/350	2005/2007待补齐；RX 400h尺寸不同暂不并入	待终核: 2005/2007
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2010-2013	187.8	74.2	66.3	2010 Lexus RX 350	2011-2013待确认	待终核: 2011-2013
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2014	187.8	74.2	66.7	2014 Lexus RX 350	高度与2010/2015不同，待复核是否trim/口径差异	待终核: 2014高度
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2015	187.8	74.2	66.3	2015 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen4 midsize SUV	2016-2022	192.5	74.6	67.7	2016/2017/2019/2021/2022 Lexus RX 350	excl: L	可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2018	196.9	74.6	67.7	2018 Lexus RX 350L Base	长轴版	
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2019-2022	196.9	74.6	67.3	2019/2021/2022 Lexus RX 350L	长轴版；2020待补齐	待终核: 2020
Lexus RX	Lexus	越野车	SUV	inc: PHEV	gen5 midsize SUV	2023-2026	192.5	75.6	67.3	2023/2024/2025/2026 Lexus RX 350/350h/450h+		可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身；原coupe/conv拆分	待终核: Coupe 1968-1969
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身；原coupe/conv拆分	待终核: Convertible 1967-1969
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1970-1973	191.1	73.4	49.3	1970 Firebird	第二代早期；原coupe/Trans Am拆分	待终核: 1971-1973结构
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1974-1981	196.8	73.2	49.6	1974-1981 Trans Am / Formula	保险杠增长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1982-1988	191.8	72.4	50	1988 Firebird / Trans Am	低矮楔形；参考车型未覆盖完整年份范围	待终核: 1982-1987
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1989-1992	195.2	72.8	49.7	1990/1991 Firebird	末期造型更长；参考车型未覆盖完整年份范围	待终核: 1989/1992
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Coupe 1994-1997
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Convertible 1993-1997
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Coupe 1998-1999/2001-2002
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Convertible 1998-2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2001-2002	177.2	72.6	65.9	2001/2002 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2003-2004	177.2	72.7	66	2005/2006 Hyundai Santa Fe cross-ref	2003-2004待确认	待终核: 2003-2004
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2005-2006	177.2	72.7	66	2005/2006 Hyundai Santa Fe GLS/LX	2005-2006宽/高高于2001-2002	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen2 midsize SUV	2007-2012	184.1	74.4	67.9	2007/2008/2009/2010/2011/2012 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2013	184.6	74	66.5	2013 Hyundai Santa Fe Sport / Sport 2.0T	同年Sport 2.0T高度取高值	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2014-2018	185	74	66.5	2018 Hyundai Santa Fe Sport / Sport 2.0T	短轴版；2014-2017待确认	待终核: 2014-2017
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2013-2018	193.1	74.2	66.9	2013/2014/2016/2018 Hyundai Santa Fe Limited/XL	长轴版；2015/2017待确认	待终核: 2015/2017
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2019	193.1	74.2	66.9	2019 Hyundai Santa Fe XL	长轴版	
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen4 midsize SUV	2019-2023	188.4	74.4	66.3	2019-2023 Hyundai Santa Fe		
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen5 midsize SUV	2024-2026	190.2	74.8	69.7	2024-2026 Hyundai Santa Fe Limited/Calligraphy		
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2001	172.2	67.1	60	2001 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2001	172.2	67.1	60	2001 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen3 compact	2008-2011	173.8	68.5	58.3	2008-2011 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen3 compact	2008-2011	173.8	68.5	58.3	2008-2011 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen5 midsize	1983-1986	196.5	71	53.8	1986 Mercury Marquis brochure / Mercury Marquis specs	中型四门；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen5 midsize	1983-1986	196.5	71	54.4	1986 Mercury Marquis brochure / Mercury Marquis specs	中型旅行车更高；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Coupe 1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Sedan 1967-1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Sedan 1969-1972
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Coupe 1969-1971
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Sedan 1973-1974/1976/1978
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Coupe 1973-1978
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen3 full-size	1973-1978	231	79.6	55	1975/1978 Mercury Marquis Colony Park Wagon	wagon超长；中间年份待确认	待终核: 1973-1974/1976-1977
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Sedan 1979-1982
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Coupe 1979-1982
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Wagon 1979-1982
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1992	212.4	77.8	56.7	1992 Ford Crown Victoria Sedan LX		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1993-1997	212.4	77.8	56.8	1993/1995/1997 Ford Crown Victoria LX	1993核对后长度修正为212.4；1994/1996待确认	待终核: 1994/1996
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1998-2002	212	78.2	56.8	1998/2000 Ford Crown Victoria LX	facelift宽度高点；2001-2002待确认	待终核: 1999/2001-2002
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2003-2011	212	77.3	56.8	2003/2008/2011 Ford Crown Victoria Sedan	后期Panther；宽度按后期修正	待终核: 2004-2007/2009-2010
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen2 midsize sedan	1989-1998	185	69.7	55.3	1998 Hyundai Sonata	参考车型未覆盖完整年份范围	待终核: 1989-1997
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	1999-2004	185.4	71.6	55.5	1999/2000 Hyundai Sonata	2001-2004待确认	待终核: 2001-2004
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	2005	186.9	71.7	56	2005 Hyundai Sonata	2005单年尺寸不同	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen4 midsize sedan	2006-2010	188.9	72.1	58	2006/2010 Hyundai Sonata LX/GLS	2007-2009待确认	待终核: 2007-2009
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen5 midsize sedan	2011-2014	189.8	72.2	57.9	2011/2013/2014 Hyundai Sonata / Hybrid	2012待确认	待终核: 2012
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2015-2019	191.1	73.4	58.1	2015/2016/2019 Hyundai Sonata / Hybrid	2017-2018待确认；hybrid高度较低不影响取高值	待终核: 2017-2018
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 midsize sedan	2020-2023	192.9	73.2	56.9	2020/2022/2023 Hyundai Sonata Hybrid Limited	2021待确认	待终核: 2021
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 facelift midsize sedan	2024-2026	193.3	73.2	56.9	2024-2026 Hyundai Sonata Hybrid / N Line		可入库
Chevrolet Bolt EUV	Chevrolet	越野车	SUV	EV	gen1 compact EV SUV	2022-2023	169.5	69.7	63.6	2022/2023 Chevrolet Bolt EUV	EV小型SUV	可入库

下一步。


--- Round 5 / 下一步 ---
更新点
车型	操作	描述
Lexus RX	值修改	2011/2012 RX 350 高度为 67.7；2013/2014 普通 trim 有 66.7，但 F SPORT 为 67.7，所以按同年最大高度修正为 67.7。
Edmunds
+3
Edmunds
+3
Edmunds
+3

Lexus RX	稳定	2004/2006/2007 RX 330/350 均为 186.2 / 72.6 / 66.1，2005 页面暂未完全抓到三维，继续留待终核。
Edmunds
+2
Edmunds
+2

Hyundai Santa Fe	值修改	2003 为 177.2 / 72.6 / 65.9，2004 为 177.2 / 72.7 / 66.0，不能把 2003-2004 合并。
Edmunds
+1

Hyundai Santa Fe	稳定	2014/2015/2016 Sport 基础版为 184.6 / 74.0 / 66.1，但 2.0T 为 66.5 高；2017 为 185.0 / 74.0 / 66.5，需分 2014-2016 与 2017-2018。
Edmunds
+4
Edmunds
+4
Edmunds
+4

Hyundai Santa Fe	稳定	2015/2017 长轴 Santa Fe / XL 与 2013/2018 长轴组一致，2013-2018 XL 推进为可入库。
Edmunds
+1

Hyundai Sonata	稳定	2007/2008/2009 已确认与 2006/2010 同尺寸，2006-2010 推进为可入库。
Edmunds
+2
Edmunds
+2

Hyundai Sonata	稳定	2012、2017、2018、2021 已补齐；2011-2014、2015-2019、2020-2023 关键待核范围缩小。
Edmunds
+3
Edmunds
+3
Edmunds
+3
阶段性 TSV
tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	1999-2000	180.1	71.5	65.7	1999/2000 Lexus RX 300 SUV Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2001-2002	180.1	71.5	65.7	1999/2000/2003 Lexus RX 300 cross-ref	中间年份待确认	待终核: 2001-2002
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2003	180.1	71.5	65.7	2003 Lexus RX 300 Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2004	186.2	72.6	66.1	2004 Lexus RX 330		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2005	186.2	72.6	66.1	2004/2006/2007 Lexus RX 330/350 cross-ref	2005待补齐	待终核: 2005
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2006-2009	186.2	72.6	66.1	2006/2007/2008/2009 Lexus RX 330/350	RX 400h尺寸不同暂不并入	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2010	187.8	74.2	66.3	2010 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	F SPORT/gen max	gen3 midsize SUV	2011-2014	187.8	74.2	67.7	2011/2012 Lexus RX 350; 2013/2014 Lexus RX 350 F SPORT	取同年最高F SPORT高度	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2015	187.8	74.2	66.3	2015 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen4 midsize SUV	2016-2022	192.5	74.6	67.7	2016/2017/2019/2021/2022 Lexus RX 350	excl: L	可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2018	196.9	74.6	67.7	2018 Lexus RX 350L Base	长轴版	
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2019-2022	196.9	74.6	67.3	2019/2021/2022 Lexus RX 350L	长轴版；2020待补齐	待终核: 2020
Lexus RX	Lexus	越野车	SUV	inc: PHEV	gen5 midsize SUV	2023-2026	192.5	75.6	67.3	2023/2024/2025/2026 Lexus RX 350/350h/450h+		可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身；原coupe/conv拆分	待终核: Coupe 1968-1969
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身；原coupe/conv拆分	待终核: Convertible 1967-1969
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1970-1973	191.1	73.4	49.3	1970 Firebird	第二代早期；原coupe/Trans Am拆分	待终核: 1971-1973结构
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1974-1981	196.8	73.2	49.6	1974-1981 Trans Am / Formula	保险杠增长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1982-1988	191.8	72.4	50	1988 Firebird / Trans Am	低矮楔形；参考车型未覆盖完整年份范围	待终核: 1982-1987
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1989-1992	195.2	72.8	49.7	1990/1991 Firebird	末期造型更长；参考车型未覆盖完整年份范围	待终核: 1989/1992
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Coupe 1994-1997
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Convertible 1993-1997
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Coupe 1998-1999/2001-2002
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Convertible 1998-2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2001-2003	177.2	72.6	65.9	2001/2002/2003 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2004-2006	177.2	72.7	66	2004/2005/2006 Hyundai Santa Fe GLS/LX	2004后宽/高高于2001-2003	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen2 midsize SUV	2007-2012	184.1	74.4	67.9	2007/2008/2009/2010/2011/2012 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2013	184.6	74	66.5	2013 Hyundai Santa Fe Sport / Sport 2.0T	同年Sport 2.0T高度取高值	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2014-2016	184.6	74	66.5	2014/2015/2016 Hyundai Santa Fe Sport / Sport 2.0T	同年2.0T高度取高值	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2017-2018	185	74	66.5	2017/2018 Hyundai Santa Fe Sport / Sport 2.0T	2017后长度增至185.0	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2013-2018	193.1	74.2	66.9	2013/2014/2015/2016/2017/2018 Hyundai Santa Fe Limited/XL	长轴版	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2019	193.1	74.2	66.9	2019 Hyundai Santa Fe XL	长轴版	
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen4 midsize SUV	2019-2023	188.4	74.4	66.3	2019-2023 Hyundai Santa Fe		
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen5 midsize SUV	2024-2026	190.2	74.8	69.7	2024-2026 Hyundai Santa Fe Limited/Calligraphy		
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2001	172.2	67.1	60	2001 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2001	172.2	67.1	60	2001 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen3 compact	2008-2011	173.8	68.5	58.3	2008-2011 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen3 compact	2008-2011	173.8	68.5	58.3	2008-2011 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen5 midsize	1983-1986	196.5	71	53.8	1986 Mercury Marquis brochure / Mercury Marquis specs	中型四门；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen5 midsize	1983-1986	196.5	71	54.4	1986 Mercury Marquis brochure / Mercury Marquis specs	中型旅行车更高；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Coupe 1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Sedan 1967-1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Sedan 1969-1972
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Coupe 1969-1971
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Sedan 1973-1974/1976/1978
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Coupe 1973-1978
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen3 full-size	1973-1978	231	79.6	55	1975/1978 Mercury Marquis Colony Park Wagon	wagon超长；中间年份待确认	待终核: 1973-1974/1976-1977
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Sedan 1979-1982
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Coupe 1979-1982
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Wagon 1979-1982
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1992	212.4	77.8	56.7	1992 Ford Crown Victoria Sedan LX		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1993-1997	212.4	77.8	56.8	1993/1995/1997 Ford Crown Victoria LX	1993核对后长度修正为212.4；1994/1996待确认	待终核: 1994/1996
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1998-2002	212	78.2	56.8	1998/2000 Ford Crown Victoria LX	facelift宽度高点；2001-2002待确认	待终核: 1999/2001-2002
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2003-2011	212	77.3	56.8	2003/2008/2011 Ford Crown Victoria Sedan	后期Panther；宽度按后期修正	待终核: 2004-2007/2009-2010
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen2 midsize sedan	1989-1998	185	69.7	55.3	1998 Hyundai Sonata	参考车型未覆盖完整年份范围	待终核: 1989-1997
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	1999-2004	185.4	71.6	55.5	1999/2000/2001 Hyundai Sonata	2002-2004待确认	待终核: 2002-2004
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	2005	186.9	71.7	56	2005 Hyundai Sonata	2005单年尺寸不同	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen4 midsize sedan	2006-2010	188.9	72.1	58	2006/2007/2008/2009/2010 Hyundai Sonata LX/GLS		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen5 midsize sedan	2011-2014	189.8	72.2	57.9	2011/2012/2013/2014 Hyundai Sonata / Hybrid		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2015-2019	191.1	73.4	58.1	2015/2016/2017/2018/2019 Hyundai Sonata / Hybrid	hybrid高度较低不影响取高值	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 midsize sedan	2020-2023	192.9	73.2	56.9	2020/2021/2022/2023 Hyundai Sonata Hybrid/N Line		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 facelift midsize sedan	2024-2026	193.3	73.2	56.9	2024-2026 Hyundai Sonata Hybrid / N Line		可入库
Chevrolet Bolt EUV	Chevrolet	越野车	SUV	EV	gen1 compact EV SUV	2022-2023	169.5	69.7	63.6	2022/2023 Chevrolet Bolt EUV	EV小型SUV	可入库

下一步。


--- Round 6 / 下一步 ---
更新点
车型	操作	描述
Lexus RX	稳定	2001 RX 300 已核到 180.1 / 71.5 / 65.7；2002 仍缺直接页，暂不强行压成 1999-2003 全可入库。
Edmunds
+1

Lexus RX	稳定	2005 RX 330 页面已定位，但当前摘录未显示三维；2005 继续单独待终核，不影响 2004 与 2006-2009 已确认段。
Edmunds
+1

Lexus RX	稳定	2020 RX 350 标准轴为 192.5 / 74.6 / 67.7；2020 RX 350L 未直接核到，但 2022 RX 350L 为 196.9 / 74.6 / 67.3，所以 2020 L 仍单独待终核。
Edmunds
+1

Ford Crown Victoria	值修改	1997 Edmunds 显示宽度 78.2，不应并入 1993-1996 的 77.8 宽段；1993/1994 为 212.4 / 77.8 / 56.8，1995 为 212.0 / 77.8 / 56.8。
Edmunds
+3
Edmunds
+3
Edmunds
+3

Hyundai Sonata	值修改	2002 为 185.4 / 71.6 / 55.5，2004 为 186.9 / 71.7 / 56.0，所以 1999-2004 必须拆为 1999-2002 与 2004；2003 待核。
Edmunds
+1
阶段性 TSV
tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	1999-2001	180.1	71.5	65.7	1999/2000/2001 Lexus RX 300 SUV Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2002	180.1	71.5	65.7	1999/2001/2003 Lexus RX 300 cross-ref	2002待直接核对	待终核: 2002
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2003	180.1	71.5	65.7	2003 Lexus RX 300 Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2004	186.2	72.6	66.1	2004 Lexus RX 330		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2005	186.2	72.6	66.1	2004/2006/2007 Lexus RX 330/350 cross-ref	2005待直接核对	待终核: 2005
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2006-2009	186.2	72.6	66.1	2006/2007/2008/2009 Lexus RX 330/350	RX 400h尺寸不同暂不并入	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2010	187.8	74.2	66.3	2010 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	F SPORT/gen max	gen3 midsize SUV	2011-2014	187.8	74.2	67.7	2011/2012 Lexus RX 350; 2013/2014 Lexus RX 350 F SPORT	取同年最高F SPORT高度	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2015	187.8	74.2	66.3	2015 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen4 midsize SUV	2016-2022	192.5	74.6	67.7	2016/2017/2019/2020/2021/2022 Lexus RX 350	excl: L	可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2018	196.9	74.6	67.7	2018 Lexus RX 350L Base	长轴版	
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2019	196.9	74.6	67.3	2019 Lexus RX 350L	长轴版	可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2020	196.9	74.6	67.3	2019/2021/2022 Lexus RX 350L cross-ref	2020待直接核对	待终核: 2020
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2021-2022	196.9	74.6	67.3	2021/2022 Lexus RX 350L	长轴版	可入库
Lexus RX	Lexus	越野车	SUV	inc: PHEV	gen5 midsize SUV	2023-2026	192.5	75.6	67.3	2023/2024/2025/2026 Lexus RX 350/350h/450h+		可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身；原coupe/conv拆分	待终核: Coupe 1968-1969
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身；原coupe/conv拆分	待终核: Convertible 1967-1969
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1970-1973	191.1	73.4	49.3	1970 Firebird	第二代早期；原coupe/Trans Am拆分	待终核: 1971-1973结构
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1974-1981	196.8	73.2	49.6	1974-1981 Trans Am / Formula	保险杠增长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1982-1988	191.8	72.4	50	1988 Firebird / Trans Am	低矮楔形；参考车型未覆盖完整年份范围	待终核: 1982-1987
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1989-1992	195.2	72.8	49.7	1990/1991 Firebird	末期造型更长；参考车型未覆盖完整年份范围	待终核: 1989/1992
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Coupe 1994-1997
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Convertible 1993-1997
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Coupe 1998-1999/2001-2002
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Convertible 1998-2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2001-2003	177.2	72.6	65.9	2001/2002/2003 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2004-2006	177.2	72.7	66	2004/2005/2006 Hyundai Santa Fe GLS/LX	2004后宽/高高于2001-2003	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen2 midsize SUV	2007-2012	184.1	74.4	67.9	2007/2008/2009/2010/2011/2012 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2013	184.6	74	66.5	2013 Hyundai Santa Fe Sport / Sport 2.0T	同年Sport 2.0T高度取高值	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2014-2016	184.6	74	66.5	2014/2015/2016 Hyundai Santa Fe Sport / Sport 2.0T	同年2.0T高度取高值	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2017-2018	185	74	66.5	2017/2018 Hyundai Santa Fe Sport / Sport 2.0T	2017后长度增至185.0	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2013-2018	193.1	74.2	66.9	2013/2014/2015/2016/2017/2018 Hyundai Santa Fe Limited/XL	长轴版	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2019	193.1	74.2	66.9	2019 Hyundai Santa Fe XL	长轴版	
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen4 midsize SUV	2019-2023	188.4	74.4	66.3	2019-2023 Hyundai Santa Fe		
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen5 midsize SUV	2024-2026	190.2	74.8	69.7	2024-2026 Hyundai Santa Fe Limited/Calligraphy		
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2001	172.2	67.1	60	2001 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2001	172.2	67.1	60	2001 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen3 compact	2008-2011	173.8	68.5	58.3	2008-2011 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen3 compact	2008-2011	173.8	68.5	58.3	2008-2011 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen5 midsize	1983-1986	196.5	71	53.8	1986 Mercury Marquis brochure / Mercury Marquis specs	中型四门；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen5 midsize	1983-1986	196.5	71	54.4	1986 Mercury Marquis brochure / Mercury Marquis specs	中型旅行车更高；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Coupe 1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Sedan 1967-1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Sedan 1969-1972
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Coupe 1969-1971
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Sedan 1973-1974/1976/1978
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Coupe 1973-1978
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen3 full-size	1973-1978	231	79.6	55	1975/1978 Mercury Marquis Colony Park Wagon	wagon超长；中间年份待确认	待终核: 1973-1974/1976-1977
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Sedan 1979-1982
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Coupe 1979-1982
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Wagon 1979-1982
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1992	212.4	77.8	56.7	1992 Ford Crown Victoria Sedan LX		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1993-1994	212.4	77.8	56.8	1993/1994 Ford Crown Victoria Sedan		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1995-1996	212	77.8	56.8	1995 Ford Crown Victoria cross-ref	1996待直接核对	待终核: 1996
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1997	212	78.2	56.8	1997 Ford Crown Victoria S	1997宽度高于1995	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1998-2002	212	78.2	56.8	1998/2000/2001 Ford Crown Victoria LX	facelift宽度高点；1999/2002待确认	待终核: 1999/2002
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2003-2011	212	77.3	56.8	2003/2008/2011 Ford Crown Victoria Sedan	后期Panther；宽度按后期修正	待终核: 2004-2007/2009-2010
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen2 midsize sedan	1989-1998	185	69.7	55.3	1998 Hyundai Sonata	参考车型未覆盖完整年份范围	待终核: 1989-1997
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	1999-2002	185.4	71.6	55.5	1999/2000/2001/2002 Hyundai Sonata		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	2003	185.4	71.6	55.5	2002/2004 Hyundai Sonata cross-ref	2003待直接核对	待终核: 2003
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	2004-2005	186.9	71.7	56	2004/2005 Hyundai Sonata	2004后长度/宽/高增加	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen4 midsize sedan	2006-2010	188.9	72.1	58	2006/2007/2008/2009/2010 Hyundai Sonata LX/GLS		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen5 midsize sedan	2011-2014	189.8	72.2	57.9	2011/2012/2013/2014 Hyundai Sonata / Hybrid		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2015-2019	191.1	73.4	58.1	2015/2016/2017/2018/2019 Hyundai Sonata / Hybrid	hybrid高度较低不影响取高值	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 midsize sedan	2020-2023	192.9	73.2	56.9	2020/2021/2022/2023 Hyundai Sonata Hybrid/N Line		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 facelift midsize sedan	2024-2026	193.3	73.2	56.9	2024-2026 Hyundai Sonata Hybrid / N Line		可入库
Chevrolet Bolt EUV	Chevrolet	越野车	SUV	EV	gen1 compact EV SUV	2022-2023	169.5	69.7	63.6	2022/2023 Chevrolet Bolt EUV	EV小型SUV	可入库

下一步。


--- Round 7 / 下一步 ---
更新点
车型	操作	描述
Lexus RX	值修改	2002 RX 300 实测为 180.3 / 71.5 / 65.7，长度比 1999-2001/2003 的 180.1 多 0.2，所以单独拆出 2002。
Edmunds

Lexus RX	稳定	2005 RX 330 为 186.2 / 72.6 / 66.1，2004-2009 标准轴 RX 可推进为可入库。
Edmunds

Lexus RX	稳定	2020 RX 350L 为 196.9 / 74.6 / 67.3，2019-2022 L 长轴组可推进为可入库。
Edmunds

Ford Crown Victoria	稳定/拆分	1996 已确认 212.0 / 77.8 / 56.8，可与 1995 合并；1997 宽度 78.2，继续单独保留。
Edmunds
+1

Ford Crown Victoria	值修改	2004 为 212 / 78.2 / 56.8，2005 为 212 / 77.3 / 56.8，所以 2003-2011 后期不能整段用 77.3，需要拆出 2004 单年。
Edmunds
+1

Hyundai Sonata	值修改	2003 Sonata 为 186.9 / 71.7 / 56.0，应并入 2004-2005，而不是 1999-2002。
Edmunds
阶段性 TSV
tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	1999-2001	180.1	71.5	65.7	1999/2000/2001 Lexus RX 300 SUV Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2002	180.3	71.5	65.7	2002 Lexus RX 300 SUV Base	2002长度略增	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2003	180.1	71.5	65.7	2003 Lexus RX 300 Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2004-2009	186.2	72.6	66.1	2004/2005/2006/2007/2008/2009 Lexus RX 330/350	RX 400h尺寸不同暂不并入	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2010	187.8	74.2	66.3	2010 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	F SPORT/gen max	gen3 midsize SUV	2011-2014	187.8	74.2	67.7	2011/2012 Lexus RX 350; 2013/2014 Lexus RX 350 F SPORT	取同年最高F SPORT高度	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2015	187.8	74.2	66.3	2015 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen4 midsize SUV	2016-2022	192.5	74.6	67.7	2016/2017/2019/2020/2021/2022 Lexus RX 350	excl: L	可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2018	196.9	74.6	67.7	2018 Lexus RX 350L Base	长轴版	可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2019-2022	196.9	74.6	67.3	2019/2020/2021/2022 Lexus RX 350L	长轴版	可入库
Lexus RX	Lexus	越野车	SUV	inc: PHEV	gen5 midsize SUV	2023-2026	192.5	75.6	67.3	2023/2024/2025/2026 Lexus RX 350/350h/450h+		可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身；原coupe/conv拆分	待终核: Coupe 1968-1969
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身；原coupe/conv拆分	待终核: Convertible 1967-1969
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1970-1973	191.1	73.4	49.3	1970 Firebird	第二代早期；原coupe/Trans Am拆分	待终核: 1971-1973结构
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1974-1981	196.8	73.2	49.6	1974-1981 Trans Am / Formula	保险杠增长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1982-1988	191.8	72.4	50	1988 Firebird / Trans Am	低矮楔形；参考车型未覆盖完整年份范围	待终核: 1982-1987
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1989-1992	195.2	72.8	49.7	1990/1991 Firebird	末期造型更长；参考车型未覆盖完整年份范围	待终核: 1989/1992
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Coupe 1994-1997
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Convertible 1993-1997
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Coupe 1998-1999/2001-2002
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Convertible 1998-2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2001-2003	177.2	72.6	65.9	2001/2002/2003 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2004-2006	177.2	72.7	66	2004/2005/2006 Hyundai Santa Fe GLS/LX	2004后宽/高高于2001-2003	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen2 midsize SUV	2007-2012	184.1	74.4	67.9	2007/2008/2009/2010/2011/2012 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2013	184.6	74	66.5	2013 Hyundai Santa Fe Sport / Sport 2.0T	同年Sport 2.0T高度取高值	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2014-2016	184.6	74	66.5	2014/2015/2016 Hyundai Santa Fe Sport / Sport 2.0T	同年2.0T高度取高值	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2017-2018	185	74	66.5	2017/2018 Hyundai Santa Fe Sport / Sport 2.0T	2017后长度增至185.0	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2013-2018	193.1	74.2	66.9	2013/2014/2015/2016/2017/2018 Hyundai Santa Fe Limited/XL	长轴版	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2019	193.1	74.2	66.9	2019 Hyundai Santa Fe XL	长轴版	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen4 midsize SUV	2019-2023	188.4	74.4	66.3	2019-2023 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen5 midsize SUV	2024-2026	190.2	74.8	69.7	2024-2026 Hyundai Santa Fe Limited/Calligraphy		可入库
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2001	172.2	67.1	60	2001 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2001	172.2	67.1	60	2001 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen2 compact	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Subaru Outback Sp	Subaru	两厢车	Hatchback	Outback Sport	gen3 compact	2008-2011	173.8	68.5	58.3	2008-2011 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Hatchback结构
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen3 compact	2008-2011	173.8	68.5	58.3	2008-2011 Subaru Impreza Outback Sport, Edmunds	原hch/wgn合并结构拆分	待终核: Wagon结构
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen5 midsize	1983-1986	196.5	71	53.8	1986 Mercury Marquis brochure / Mercury Marquis specs	中型四门；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen5 midsize	1983-1986	196.5	71	54.4	1986 Mercury Marquis brochure / Mercury Marquis specs	中型旅行车更高；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Coupe 1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Sedan 1967-1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Sedan 1969-1972
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Coupe 1969-1971
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Sedan 1973-1974/1976/1978
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Coupe 1973-1978
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen3 full-size	1973-1978	231	79.6	55	1975/1978 Mercury Marquis Colony Park Wagon	wagon超长；中间年份待确认	待终核: 1973-1974/1976-1977
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Sedan 1979-1982
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Coupe 1979-1982
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Wagon 1979-1982
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1992	212.4	77.8	56.7	1992 Ford Crown Victoria Sedan LX		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1993-1994	212.4	77.8	56.8	1993/1994 Ford Crown Victoria Sedan		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1995-1996	212	77.8	56.8	1995/1996 Ford Crown Victoria Sedan		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1997	212	78.2	56.8	1997 Ford Crown Victoria S	1997宽度高于1995-1996	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1998-2002	212	78.2	56.8	1998/2000/2002 Ford Crown Victoria LX/Sedan	facelift宽度高点；1999/2001待补齐	待终核: 1999/2001
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2003	212	77.3	56.8	2003 Ford Crown Victoria Sedan	后期Panther；宽度按后期修正	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2004	212	78.2	56.8	2004 Ford Crown Victoria Sedan	2004宽度仍为78.2，需单独拆出	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2005-2011	212	77.3	56.8	2005/2007/2008/2011 Ford Crown Victoria Sedan	2006部分页面高度异常，待核是否LWB/Commercial口径	待终核: 2006/2009-2010
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen2 midsize sedan	1989-1998	185	69.7	55.3	1998 Hyundai Sonata	参考车型未覆盖完整年份范围	待终核: 1989-1997
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	1999-2002	185.4	71.6	55.5	1999/2000/2001/2002 Hyundai Sonata		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	2003-2005	186.9	71.7	56	2003/2004/2005 Hyundai Sonata	2003后长度/宽/高增加	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen4 midsize sedan	2006-2010	188.9	72.1	58	2006/2007/2008/2009/2010 Hyundai Sonata LX/GLS		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen5 midsize sedan	2011-2014	189.8	72.2	57.9	2011/2012/2013/2014 Hyundai Sonata / Hybrid		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2015-2019	191.1	73.4	58.1	2015/2016/2017/2018/2019 Hyundai Sonata / Hybrid	hybrid高度较低不影响取高值	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 midsize sedan	2020-2023	192.9	73.2	56.9	2020/2021/2022/2023 Hyundai Sonata Hybrid/N Line		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 facelift midsize sedan	2024-2026	193.3	73.2	56.9	2024-2026 Hyundai Sonata Hybrid / N Line		可入库
Chevrolet Bolt EUV	Chevrolet	越野车	SUV	EV	gen1 compact EV SUV	2022-2023	169.5	69.7	63.6	2022/2023 Chevrolet Bolt EUV	EV小型SUV	可入库

下一步。


--- Round 8 / 下一步 ---
更新点
车型	操作	描述
Ford Crown Victoria	补强/拆分	1998、2001 均为 212.0 / 78.2 / 56.8，可继续归入 1998-2002 宽体段；1999 仍缺直接三维显示，保留待终核。
Edmunds
+1

Ford Crown Victoria	值修改	2006/2007 Edmunds 显示高度 58.3，高于 2005/2011 的 56.8，不能继续把 2005-2011 全部压成同一行。
Edmunds
+2
Edmunds
+2

Subaru Outback Sp	结构修正	Outback Sport 在 Edmunds 对应 Impreza Wagon Outback Sport，不应再拆 Hatchback；本轮删除 Hatchback 待核行，保留 Wagon。2001 与 2008 直接核到对应 Outback Sport wagon 尺寸。
Edmunds
+1

Mercury Marquis	结构保留	1983-1986 Mercury Marquis brochure / iSeeCars 可支持 sedan/wagon 结构存在；本轮暂不强行全部可入库，仍保留 1983-1985 待终核。
iseecars.com
+1
阶段性 TSV
tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	1999-2001	180.1	71.5	65.7	1999/2000/2001 Lexus RX 300 SUV Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2002	180.3	71.5	65.7	2002 Lexus RX 300 SUV Base	2002长度略增	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2003	180.1	71.5	65.7	2003 Lexus RX 300 Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2004-2009	186.2	72.6	66.1	2004/2005/2006/2007/2008/2009 Lexus RX 330/350	RX 400h尺寸不同暂不并入	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2010	187.8	74.2	66.3	2010 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	F SPORT/gen max	gen3 midsize SUV	2011-2014	187.8	74.2	67.7	2011/2012 Lexus RX 350; 2013/2014 Lexus RX 350 F SPORT	取同年最高F SPORT高度	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2015	187.8	74.2	66.3	2015 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen4 midsize SUV	2016-2022	192.5	74.6	67.7	2016/2017/2019/2020/2021/2022 Lexus RX 350	excl: L	可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2018	196.9	74.6	67.7	2018 Lexus RX 350L Base	长轴版	可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2019-2022	196.9	74.6	67.3	2019/2020/2021/2022 Lexus RX 350L	长轴版	可入库
Lexus RX	Lexus	越野车	SUV	inc: PHEV	gen5 midsize SUV	2023-2026	192.5	75.6	67.3	2023/2024/2025/2026 Lexus RX 350/350h/450h+		可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身；原coupe/conv拆分	待终核: Coupe 1968-1969
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身；原coupe/conv拆分	待终核: Convertible 1967-1969
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1970-1973	191.1	73.4	49.3	1970 Firebird	第二代早期；原coupe/Trans Am拆分	待终核: 1971-1973结构
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1974-1981	196.8	73.2	49.6	1974-1981 Trans Am / Formula	保险杠增长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1982-1988	191.8	72.4	50	1988 Firebird / Trans Am	低矮楔形；参考车型未覆盖完整年份范围	待终核: 1982-1987
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1989-1992	195.2	72.8	49.7	1990/1991 Firebird	末期造型更长；参考车型未覆盖完整年份范围	待终核: 1989/1992
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Coupe 1994-1997
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Convertible 1993-1997
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Coupe 1998-1999/2001-2002
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Convertible 1998-2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2001-2003	177.2	72.6	65.9	2001/2002/2003 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2004-2006	177.2	72.7	66	2004/2005/2006 Hyundai Santa Fe GLS/LX	2004后宽/高高于2001-2003	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen2 midsize SUV	2007-2012	184.1	74.4	67.9	2007/2008/2009/2010/2011/2012 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2013	184.6	74	66.5	2013 Hyundai Santa Fe Sport / Sport 2.0T	同年Sport 2.0T高度取高值	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2014-2016	184.6	74	66.5	2014/2015/2016 Hyundai Santa Fe Sport / Sport 2.0T	同年2.0T高度取高值	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2017-2018	185	74	66.5	2017/2018 Hyundai Santa Fe Sport / Sport 2.0T	2017后长度增至185.0	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2013-2018	193.1	74.2	66.9	2013/2014/2015/2016/2017/2018 Hyundai Santa Fe Limited/XL	长轴版	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2019	193.1	74.2	66.9	2019 Hyundai Santa Fe XL	长轴版	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen4 midsize SUV	2019-2023	188.4	74.4	66.3	2019-2023 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen5 midsize SUV	2024-2026	190.2	74.8	69.7	2024-2026 Hyundai Santa Fe Limited/Calligraphy		可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2001	172.2	67.1	60	2001 Subaru Impreza Wagon Outback Sport, Edmunds	Outback Sport按Impreza wagon口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	原始尺寸待直接复核	待终核: 2002-2003
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	原始尺寸待直接复核	待终核: 2004
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	原始尺寸待直接复核	待终核: 2005
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	原始尺寸待直接复核	待终核: 2006
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	原始尺寸待直接复核	待终核: 2007
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen3 compact	2008	173.8	68.5	58.3	2008 Subaru Impreza Outback Sport, Edmunds	Outback Sport高度高于普通wagon	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen3 compact	2009-2011	173.8	68.5	58.3	2008 Subaru Impreza Outback Sport cross-ref	2009-2011待直接复核	待终核: 2009-2011
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen5 midsize	1983-1986	196.5	71	53.8	1986 Mercury Marquis brochure / Mercury Marquis specs	中型四门；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen5 midsize	1983-1986	196.5	71	54.4	1986 Mercury Marquis brochure / Mercury Marquis specs	中型旅行车更高；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Coupe 1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Sedan 1967-1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Sedan 1969-1972
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Coupe 1969-1971
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Sedan 1973-1974/1976/1978
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Coupe 1973-1978
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen3 full-size	1973-1978	231	79.6	55	1975/1978 Mercury Marquis Colony Park Wagon	wagon超长；中间年份待确认	待终核: 1973-1974/1976-1977
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Sedan 1979-1982
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Coupe 1979-1982
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Wagon 1979-1982
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1992	212.4	77.8	56.7	1992 Ford Crown Victoria Sedan LX		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1993-1994	212.4	77.8	56.8	1993/1994 Ford Crown Victoria Sedan		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1995-1996	212	77.8	56.8	1995/1996 Ford Crown Victoria Sedan		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1997	212	78.2	56.8	1997 Ford Crown Victoria S	1997宽度高于1995-1996	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1998	212	78.2	56.8	1998 Ford Crown Victoria LX/Sedan		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1999	212	78.2	56.8	1998/2001 Ford Crown Victoria cross-ref	1999待直接三维核对	待终核: 1999
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2000-2002	212	78.2	56.8	2000/2001/2002 Ford Crown Victoria LX/Sedan		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2003	212	77.3	56.8	2003 Ford Crown Victoria Sedan	后期Panther；宽度按后期修正	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2004	212	78.2	56.8	2004 Ford Crown Victoria Sedan	2004宽度仍为78.2，需单独拆出	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2005	212	77.3	56.8	2005 Ford Crown Victoria Sedan		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2006-2007	212	78.3	58.3	2006/2007 Ford Crown Victoria Sedan	高度/宽度高于2005，按Edmunds保留	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2008	212	77.3	56.8	2008 Ford Crown Victoria Sedan		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2009-2010	212	77.3	56.8	2008/2011 Ford Crown Victoria cross-ref	2009-2010待直接核对	待终核: 2009-2010
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2011	212	77.3	56.8	2011 Ford Crown Victoria Sedan		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen2 midsize sedan	1989-1998	185	69.7	55.3	1998 Hyundai Sonata	参考车型未覆盖完整年份范围	待终核: 1989-1997
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	1999-2002	185.4	71.6	55.5	1999/2000/2001/2002 Hyundai Sonata		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	2003-2005	186.9	71.7	56	2003/2004/2005 Hyundai Sonata	2003后长度/宽/高增加	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen4 midsize sedan	2006-2010	188.9	72.1	58	2006/2007/2008/2009/2010 Hyundai Sonata LX/GLS		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen5 midsize sedan	2011-2014	189.8	72.2	57.9	2011/2012/2013/2014 Hyundai Sonata / Hybrid		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2015-2019	191.1	73.4	58.1	2015/2016/2017/2018/2019 Hyundai Sonata / Hybrid	hybrid高度较低不影响取高值	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 midsize sedan	2020-2023	192.9	73.2	56.9	2020/2021/2022/2023 Hyundai Sonata Hybrid/N Line		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 facelift midsize sedan	2024-2026	193.3	73.2	56.9	2024-2026 Hyundai Sonata Hybrid / N Line		可入库
Chevrolet Bolt EUV	Chevrolet	越野车	SUV	EV	gen1 compact EV SUV	2022-2023	169.5	69.7	63.6	2022/2023 Chevrolet Bolt EUV	EV小型SUV	可入库

下一步。


--- Round 9 / 下一步 ---
更新点
车型	操作	描述
Ford Crown Victoria	稳定	1999 已直接核到 212.0 / 78.2 / 56.8，可并入 1998-2002 宽体段。
Edmunds

Ford Crown Victoria	稳定	2009/2010 已核到 212.0 / 77.3 / 56.8，可并入 2008/2011 后期标准段。
Edmunds
+1

Ford Crown Victoria	修正	2006 的 218.0 / 78.3 / 58.3 属于 Commercial Police Package Fleet LWB，不应当覆盖 Std. 标准轴；本轮拆出 LWB 特殊版。
Edmunds

Subaru Outback Sp	稳定	2002/2003/2004 Outback Sport wagon 均为 173.4 / 67.3 / 60.2，原 2004 宽 66.7、高 57.7 应修正。
Edmunds
+2
Edmunds
+2

Subaru Outback Sp	稳定	2005/2006/2007/2008/2009/2010/2011 已核到对应 Outback Sport 尺寸，其中 2008-2011 可合并为 173.8 / 68.5 / 58.3。
Edmunds
+5
Edmunds
+5
Edmunds
+5
阶段性 TSV
tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	1999-2001	180.1	71.5	65.7	1999/2000/2001 Lexus RX 300 SUV Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2002	180.3	71.5	65.7	2002 Lexus RX 300 SUV Base	2002长度略增	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2003	180.1	71.5	65.7	2003 Lexus RX 300 Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2004-2009	186.2	72.6	66.1	2004/2005/2006/2007/2008/2009 Lexus RX 330/350	RX 400h尺寸不同暂不并入	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2010	187.8	74.2	66.3	2010 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	F SPORT/gen max	gen3 midsize SUV	2011-2014	187.8	74.2	67.7	2011/2012 Lexus RX 350; 2013/2014 Lexus RX 350 F SPORT	取同年最高F SPORT高度	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2015	187.8	74.2	66.3	2015 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen4 midsize SUV	2016-2022	192.5	74.6	67.7	2016/2017/2019/2020/2021/2022 Lexus RX 350	excl: L	可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2018	196.9	74.6	67.7	2018 Lexus RX 350L Base	长轴版	可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2019-2022	196.9	74.6	67.3	2019/2020/2021/2022 Lexus RX 350L	长轴版	可入库
Lexus RX	Lexus	越野车	SUV	inc: PHEV	gen5 midsize SUV	2023-2026	192.5	75.6	67.3	2023/2024/2025/2026 Lexus RX 350/350h/450h+		可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身；原coupe/conv拆分	待终核: Coupe 1968-1969
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身；原coupe/conv拆分	待终核: Convertible 1967-1969
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1970-1973	191.1	73.4	49.3	1970 Firebird	第二代早期；原coupe/Trans Am拆分	待终核: 1971-1973结构
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1974-1981	196.8	73.2	49.6	1974-1981 Trans Am / Formula	保险杠增长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1982-1988	191.8	72.4	50	1988 Firebird / Trans Am	低矮楔形；参考车型未覆盖完整年份范围	待终核: 1982-1987
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1989-1992	195.2	72.8	49.7	1990/1991 Firebird	末期造型更长；参考车型未覆盖完整年份范围	待终核: 1989/1992
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Coupe 1994-1997
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Convertible 1993-1997
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Coupe 1998-1999/2001-2002
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Convertible 1998-2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2001-2003	177.2	72.6	65.9	2001/2002/2003 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2004-2006	177.2	72.7	66	2004/2005/2006 Hyundai Santa Fe GLS/LX	2004后宽/高高于2001-2003	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen2 midsize SUV	2007-2012	184.1	74.4	67.9	2007/2008/2009/2010/2011/2012 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2013	184.6	74	66.5	2013 Hyundai Santa Fe Sport / Sport 2.0T	同年Sport 2.0T高度取高值	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2014-2016	184.6	74	66.5	2014/2015/2016 Hyundai Santa Fe Sport / Sport 2.0T	同年2.0T高度取高值	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2017-2018	185	74	66.5	2017/2018 Hyundai Santa Fe Sport / Sport 2.0T	2017后长度增至185.0	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2013-2018	193.1	74.2	66.9	2013/2014/2015/2016/2017/2018 Hyundai Santa Fe Limited/XL	长轴版	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2019	193.1	74.2	66.9	2019 Hyundai Santa Fe XL	长轴版	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen4 midsize SUV	2019-2023	188.4	74.4	66.3	2019-2023 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen5 midsize SUV	2024-2026	190.2	74.8	69.7	2024-2026 Hyundai Santa Fe Limited/Calligraphy		可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2001	172.2	67.1	60	2001 Subaru Impreza Wagon Outback Sport, Edmunds	Outback Sport按Impreza wagon口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2002-2004	173.4	67.3	60.2	2002/2003/2004 Subaru Impreza Outback Sport Wagon, Edmunds	2004原宽/高修正	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport Wagon, Edmunds		可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport Wagon, Edmunds		可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport Special Edition, Edmunds		可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen3 compact	2008-2011	173.8	68.5	58.3	2008/2009/2010/2011 Subaru Impreza Outback Sport, Edmunds	Outback Sport高度高于普通wagon	可入库
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen5 midsize	1983-1986	196.5	71	53.8	1986 Mercury Marquis brochure / Mercury Marquis specs	中型四门；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen5 midsize	1983-1986	196.5	71	54.4	1986 Mercury Marquis brochure / Mercury Marquis specs	中型旅行车更高；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Coupe 1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Sedan 1967-1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Sedan 1969-1972
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Coupe 1969-1971
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Sedan 1973-1974/1976/1978
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Coupe 1973-1978
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen3 full-size	1973-1978	231	79.6	55	1975/1978 Mercury Marquis Colony Park Wagon	wagon超长；中间年份待确认	待终核: 1973-1974/1976-1977
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Sedan 1979-1982
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Coupe 1979-1982
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Wagon 1979-1982
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1992	212.4	77.8	56.7	1992 Ford Crown Victoria Sedan LX		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1993-1994	212.4	77.8	56.8	1993/1994 Ford Crown Victoria Sedan		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1995-1996	212	77.8	56.8	1995/1996 Ford Crown Victoria Sedan		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1997-2002	212	78.2	56.8	1997/1998/1999/2000/2001/2002 Ford Crown Victoria Sedan	1997后宽度高于1995-1996	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2003	212	77.3	56.8	2003 Ford Crown Victoria Sedan	后期Panther；宽度按后期修正	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2004	212	78.2	56.8	2004 Ford Crown Victoria Sedan	2004宽度仍为78.2，需单独拆出	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2005	212	77.3	56.8	2005 Ford Crown Victoria Sedan		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	LWB	gen2 full-size Panther	2006	218	78.3	58.3	2006 Ford Crown Victoria Commercial Police Package Fleet LWB	LWB特殊版，不能覆盖Std.	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2006-2007	212	77.3	56.8	2005/2008 Ford Crown Victoria Std. cross-ref	Std. 2006-2007待直接核对	待终核: Std. 2006-2007
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2008-2011	212	77.3	56.8	2008/2009/2010/2011 Ford Crown Victoria Sedan		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen2 midsize sedan	1989-1998	185	69.7	55.3	1998 Hyundai Sonata	参考车型未覆盖完整年份范围	待终核: 1989-1997
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	1999-2002	185.4	71.6	55.5	1999/2000/2001/2002 Hyundai Sonata		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	2003-2005	186.9	71.7	56	2003/2004/2005 Hyundai Sonata	2003后长度/宽/高增加	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen4 midsize sedan	2006-2010	188.9	72.1	58	2006/2007/2008/2009/2010 Hyundai Sonata LX/GLS		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen5 midsize sedan	2011-2014	189.8	72.2	57.9	2011/2012/2013/2014 Hyundai Sonata / Hybrid		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2015-2019	191.1	73.4	58.1	2015/2016/2017/2018/2019 Hyundai Sonata / Hybrid	hybrid高度较低不影响取高值	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 midsize sedan	2020-2023	192.9	73.2	56.9	2020/2021/2022/2023 Hyundai Sonata Hybrid/N Line		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 facelift midsize sedan	2024-2026	193.3	73.2	56.9	2024-2026 Hyundai Sonata Hybrid / N Line		可入库
Chevrolet Bolt EUV	Chevrolet	越野车	SUV	EV	gen1 compact EV SUV	2022-2023	169.5	69.7	63.6	2022/2023 Chevrolet Bolt EUV	EV小型SUV	可入库

下一步。


--- Round 10 / 下一步 ---
本轮继续补强当前批次，原始批次数据来自上传文件。

粘贴的文本 (1)

更新点
车型	操作	描述
Ford Crown Victoria	值修改	2006 标准轴页面显示 Length 212.0、Width 78.3、Height 58.3；LWB Fleet 仍单独保留为 218.0 长。
Edmunds
+1

Hyundai Sonata	拆出	1989 早期 Sonata 尺寸按 4680/1751/1411 mm 换算约 184.3 / 68.9 / 55.6，不能并入 1997/1998 的 185.0 / 69.7 / 55.3。
carsguide.com.au
+1

Pontiac Firebird	拆出	1968/1969 Firebird 外尺寸与 1967-1969 原合并行不完全一致；1969 长宽明显增加到 191.1 / 73.9，先拆分为 1967、1968、1969 三段继续核。
Over-Drive Magazine
+2
automobile-catalog.com
+2
阶段性 TSV
tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	1999-2001	180.1	71.5	65.7	1999/2000/2001 Lexus RX 300 SUV Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2002	180.3	71.5	65.7	2002 Lexus RX 300 SUV Base	2002长度略增	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2003	180.1	71.5	65.7	2003 Lexus RX 300 Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2004-2009	186.2	72.6	66.1	2004/2005/2006/2007/2008/2009 Lexus RX 330/350	RX 400h尺寸不同暂不并入	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2010	187.8	74.2	66.3	2010 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	F SPORT/gen max	gen3 midsize SUV	2011-2014	187.8	74.2	67.7	2011/2012 Lexus RX 350; 2013/2014 Lexus RX 350 F SPORT	取同年最高F SPORT高度	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2015	187.8	74.2	66.3	2015 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen4 midsize SUV	2016-2022	192.5	74.6	67.7	2016/2017/2019/2020/2021/2022 Lexus RX 350	excl: L	可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2018	196.9	74.6	67.7	2018 Lexus RX 350L Base	长轴版	可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2019-2022	196.9	74.6	67.3	2019/2020/2021/2022 Lexus RX 350L	长轴版	可入库
Lexus RX	Lexus	越野车	SUV	inc: PHEV	gen5 midsize SUV	2023-2026	192.5	75.6	67.3	2023/2024/2025/2026 Lexus RX 350/350h/450h+		可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1967	188.8	72.6	51.5	1967 Pontiac Firebird Fact Sheet	F-body低车身；1967待高度复核	待终核: 1967高度
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1967	188.8	72.6	51.5	1967 Pontiac Firebird Fact Sheet	F-body低车身；1967 convertible待高度复核	待终核: 1967 Convertible高度
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1968	188.8	73.6	50.2	1968 Pontiac Firebird Conceptcarz / Automobile-Catalog	1968宽高与原合并行不同	待终核: Coupe交叉确认
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1968	188.8	73.6	50.2	1968 Pontiac Firebird Convertible Conceptcarz / Automobile-Catalog	1968 convertible待交叉确认	待终核: Convertible交叉确认
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1969	191.1	73.9	49.6	1969 Pontiac Firebird Fact Sheet / Conceptcarz	1969车身增长	可入库
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1969	191.1	73.9	49.6	1969 Pontiac Firebird Convertible Conceptcarz	1969车身增长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1970-1973	191.1	73.4	49.3	1970 Firebird	第二代早期；原coupe/Trans Am拆分	待终核: 1971-1973结构
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1974-1981	196.8	73.2	49.6	1974-1981 Trans Am / Formula	保险杠增长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1982-1988	191.8	72.4	50	1988 Firebird / Trans Am	低矮楔形；参考车型未覆盖完整年份范围	待终核: 1982-1987
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1989-1992	195.2	72.8	49.7	1990/1991 Firebird	末期造型更长；参考车型未覆盖完整年份范围	待终核: 1989/1992
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Coupe 1994-1997
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Convertible 1993-1997
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Coupe 1998-1999/2001-2002
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Convertible 1998-2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2001-2003	177.2	72.6	65.9	2001/2002/2003 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2004-2006	177.2	72.7	66	2004/2005/2006 Hyundai Santa Fe GLS/LX	2004后宽/高高于2001-2003	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen2 midsize SUV	2007-2012	184.1	74.4	67.9	2007/2008/2009/2010/2011/2012 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2013	184.6	74	66.5	2013 Hyundai Santa Fe Sport / Sport 2.0T	同年Sport 2.0T高度取高值	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2014-2016	184.6	74	66.5	2014/2015/2016 Hyundai Santa Fe Sport / Sport 2.0T	同年2.0T高度取高值	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2017-2018	185	74	66.5	2017/2018 Hyundai Santa Fe Sport / Sport 2.0T	2017后长度增至185.0	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2013-2018	193.1	74.2	66.9	2013/2014/2015/2016/2017/2018 Hyundai Santa Fe Limited/XL	长轴版	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2019	193.1	74.2	66.9	2019 Hyundai Santa Fe XL	长轴版	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen4 midsize SUV	2019-2023	188.4	74.4	66.3	2019-2023 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen5 midsize SUV	2024-2026	190.2	74.8	69.7	2024-2026 Hyundai Santa Fe Limited/Calligraphy		可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2001	172.2	67.1	60	2001 Subaru Impreza Wagon Outback Sport, Edmunds	Outback Sport按Impreza wagon口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2002-2004	173.4	67.3	60.2	2002/2003/2004 Subaru Impreza Outback Sport Wagon, Edmunds	2004原宽/高修正	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport Wagon, Edmunds		可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport Wagon, Edmunds		可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport Special Edition, Edmunds		可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen3 compact	2008-2011	173.8	68.5	58.3	2008/2009/2010/2011 Subaru Impreza Outback Sport, Edmunds	Outback Sport高度高于普通wagon	可入库
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen5 midsize	1983-1986	196.5	71	53.8	1986 Mercury Marquis brochure / Mercury Marquis specs	中型四门；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen5 midsize	1983-1986	196.5	71	54.4	1986 Mercury Marquis brochure / Mercury Marquis specs	中型旅行车更高；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Coupe 1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Sedan 1967-1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Sedan 1969-1972
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Coupe 1969-1971
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Sedan 1973-1974/1976/1978
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Coupe 1973-1978
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen3 full-size	1973-1978	231	79.6	55	1975/1978 Mercury Marquis Colony Park Wagon	wagon超长；中间年份待确认	待终核: 1973-1974/1976-1977
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Sedan 1979-1982
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Coupe 1979-1982
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Wagon 1979-1982
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1992	212.4	77.8	56.7	1992 Ford Crown Victoria Sedan LX		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1993-1994	212.4	77.8	56.8	1993/1994 Ford Crown Victoria Sedan		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1995-1996	212	77.8	56.8	1995/1996 Ford Crown Victoria Sedan		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1997-2002	212	78.2	56.8	1997/1998/1999/2000/2001/2002 Ford Crown Victoria Sedan	1997后宽度高于1995-1996	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2003	212	77.3	56.8	2003 Ford Crown Victoria Sedan	后期Panther；宽度按后期修正	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2004	212	78.2	56.8	2004 Ford Crown Victoria Sedan	2004宽度仍为78.2，需单独拆出	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2005	212	77.3	56.8	2005 Ford Crown Victoria Sedan		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2006	212	78.3	58.3	2006 Ford Crown Victoria Sedan	2006标准轴页面宽高高于2005/2008	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	LWB	gen2 full-size Panther	2006	218	78.3	58.3	2006 Ford Crown Victoria Commercial Police Package Fleet LWB	LWB特殊版，不能覆盖Std.	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2007	212	77.3	56.8	2005/2008 Ford Crown Victoria Std. cross-ref	Std. 2007待直接核对	待终核: Std. 2007
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2008-2011	212	77.3	56.8	2008/2009/2010/2011 Ford Crown Victoria Sedan		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen1 midsize sedan	1989	184.3	68.9	55.6	1989 Hyundai Sonata CarsGuide / Autotrader AU	早期尺寸换算	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen1 midsize sedan	1990-1993	184.3	68.9	55.6	1989 Hyundai Sonata cross-ref	早期年份待直接核对	待终核: 1990-1993
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen2 midsize sedan	1994-1998	185	69.7	55.3	1997/1998 Hyundai Sonata	二代/改款尺寸；1994-1996待直接核对	待终核: 1994-1996
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	1999-2002	185.4	71.6	55.5	1999/2000/2001/2002 Hyundai Sonata		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	2003-2005	186.9	71.7	56	2003/2004/2005 Hyundai Sonata	2003后长度/宽/高增加	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen4 midsize sedan	2006-2010	188.9	72.1	58	2006/2007/2008/2009/2010 Hyundai Sonata LX/GLS		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen5 midsize sedan	2011-2014	189.8	72.2	57.9	2011/2012/2013/2014 Hyundai Sonata / Hybrid		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2015-2019	191.1	73.4	58.1	2015/2016/2017/2018/2019 Hyundai Sonata / Hybrid	hybrid高度较低不影响取高值	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 midsize sedan	2020-2023	192.9	73.2	56.9	2020/2021/2022/2023 Hyundai Sonata Hybrid/N Line		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 facelift midsize sedan	2024-2026	193.3	73.2	56.9	2024-2026 Hyundai Sonata Hybrid / N Line		可入库
Chevrolet Bolt EUV	Chevrolet	越野车	SUV	EV	gen1 compact EV SUV	2022-2023	169.5	69.7	63.6	2022/2023 Chevrolet Bolt EUV	EV小型SUV	可入库

下一步。


--- Round 11 / 下一步 ---
本轮继续补强当前批次，原始批次数据来自上传文件。

粘贴的文本 (1)

更新点
车型	操作	描述
Ford Crown Victoria	值修改	2007 标准轴已直接核到 212.0 / 77.3 / 58.3，不能与 2008-2011 的 56.8 高度段合并，需单独拆出。
Edmunds

Ford Crown Victoria	稳定	1997 为 212.0 / 78.2 / 56.8，2001 同为 212.0 / 78.2 / 56.8，1997-2002 宽体段继续保持可入库。
Edmunds
+1

Ford Crown Victoria	稳定	2011 为 212.0 / 77.3 / 56.8，2008-2011 标准段保留；2007 高度不同已拆出。
Edmunds

Hyundai Sonata	稳定	1990 Sonata 与 1989 同为 4680 / 1751 / 1411 mm，换算约 184.3 / 68.9 / 55.6，可并入 1989-1990。
carsguide.com.au

Pontiac Firebird	稳定	1968 Firebird coupe/convertible 长宽高为 188.8 / 73.6 / 50.2，可推进为可入库；1967 仍需高度复核。
conceptcarz.com
阶段性 TSV
tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	1999-2001	180.1	71.5	65.7	1999/2000/2001 Lexus RX 300 SUV Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2002	180.3	71.5	65.7	2002 Lexus RX 300 SUV Base	2002长度略增	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2003	180.1	71.5	65.7	2003 Lexus RX 300 Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2004-2009	186.2	72.6	66.1	2004/2005/2006/2007/2008/2009 Lexus RX 330/350	RX 400h尺寸不同暂不并入	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2010	187.8	74.2	66.3	2010 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	F SPORT/gen max	gen3 midsize SUV	2011-2014	187.8	74.2	67.7	2011/2012 Lexus RX 350; 2013/2014 Lexus RX 350 F SPORT	取同年最高F SPORT高度	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2015	187.8	74.2	66.3	2015 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen4 midsize SUV	2016-2022	192.5	74.6	67.7	2016/2017/2019/2020/2021/2022 Lexus RX 350	excl: L	可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2018	196.9	74.6	67.7	2018 Lexus RX 350L Base	长轴版	可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 midsize SUV	2019-2022	196.9	74.6	67.3	2019/2020/2021/2022 Lexus RX 350L	长轴版	可入库
Lexus RX	Lexus	越野车	SUV	inc: PHEV	gen5 midsize SUV	2023-2026	192.5	75.6	67.3	2023/2024/2025/2026 Lexus RX 350/350h/450h+		可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1967	188.8	72.6	51.5	1967 Pontiac Firebird Fact Sheet	F-body低车身；1967待高度复核	待终核: 1967高度
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1967	188.8	72.6	51.5	1967 Pontiac Firebird Fact Sheet	F-body低车身；1967 convertible待高度复核	待终核: 1967 Convertible高度
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1968	188.8	73.6	50.2	1968 Pontiac Firebird Conceptcarz / Automobile-Catalog	1968宽高与1967不同	可入库
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1968	188.8	73.6	50.2	1968 Pontiac Firebird Convertible Conceptcarz / Automobile-Catalog	1968 convertible	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1969	191.1	73.9	49.6	1969 Pontiac Firebird Fact Sheet / Conceptcarz	1969车身增长	可入库
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1969	191.1	73.9	49.6	1969 Pontiac Firebird Convertible Conceptcarz	1969车身增长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1970-1973	191.1	73.4	49.3	1970 Firebird	第二代早期；原coupe/Trans Am拆分	待终核: 1971-1973结构
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen2 pony car	1974-1981	196.8	73.2	49.6	1974-1981 Trans Am / Formula	保险杠增长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1982-1988	191.8	72.4	50	1988 Firebird / Trans Am	低矮楔形；参考车型未覆盖完整年份范围	待终核: 1982-1987
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen3 pony car	1989-1992	195.2	72.8	49.7	1990/1991 Firebird	末期造型更长；参考车型未覆盖完整年份范围	待终核: 1989/1992
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Coupe 1994-1997
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期；原coupe/conv拆分	待终核: Convertible 1993-1997
Pontiac Firebird	Pontiac	跑车	Coupe	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Coupe 1998-1999/2001-2002
Pontiac Firebird	Pontiac	跑车	Convertible	Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸；原coupe/conv拆分	待终核: Convertible 1998-2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2001-2003	177.2	72.6	65.9	2001/2002/2003 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 midsize SUV	2004-2006	177.2	72.7	66	2004/2005/2006 Hyundai Santa Fe GLS/LX	2004后宽/高高于2001-2003	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen2 midsize SUV	2007-2012	184.1	74.4	67.9	2007/2008/2009/2010/2011/2012 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2013	184.6	74	66.5	2013 Hyundai Santa Fe Sport / Sport 2.0T	同年Sport 2.0T高度取高值	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2014-2016	184.6	74	66.5	2014/2015/2016 Hyundai Santa Fe Sport / Sport 2.0T	同年2.0T高度取高值	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport	gen3 midsize SUV	2017-2018	185	74	66.5	2017/2018 Hyundai Santa Fe Sport / Sport 2.0T	2017后长度增至185.0	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2013-2018	193.1	74.2	66.9	2013/2014/2015/2016/2017/2018 Hyundai Santa Fe Limited/XL	长轴版	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL	gen3 midsize SUV	2019	193.1	74.2	66.9	2019 Hyundai Santa Fe XL	长轴版	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen4 midsize SUV	2019-2023	188.4	74.4	66.3	2019-2023 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen5 midsize SUV	2024-2026	190.2	74.8	69.7	2024-2026 Hyundai Santa Fe Limited/Calligraphy		可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2001	172.2	67.1	60	2001 Subaru Impreza Wagon Outback Sport, Edmunds	Outback Sport按Impreza wagon口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2002-2004	173.4	67.3	60.2	2002/2003/2004 Subaru Impreza Outback Sport Wagon, Edmunds	2004原宽/高修正	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport Wagon, Edmunds		可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport Wagon, Edmunds		可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen2 compact	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport Special Edition, Edmunds		可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Outback Sport	gen3 compact	2008-2011	173.8	68.5	58.3	2008/2009/2010/2011 Subaru Impreza Outback Sport, Edmunds	Outback Sport高度高于普通wagon	可入库
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen5 midsize	1983-1986	196.5	71	53.8	1986 Mercury Marquis brochure / Mercury Marquis specs	中型四门；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen5 midsize	1983-1986	196.5	71	54.4	1986 Mercury Marquis brochure / Mercury Marquis specs	中型旅行车更高；参考车型未覆盖完整年份范围	待终核: 1983-1985
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Coupe 1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size；原2dr hardtop/sdn拆分	待终核: Sedan 1967-1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Sedan 1969-1972
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低；原sdn/cou拆分	待终核: Coupe 1969-1971
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Sedan 1973-1974/1976/1978
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe；原sdn/cou拆分	待终核: Coupe 1973-1978
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen3 full-size	1973-1978	231	79.6	55	1975/1978 Mercury Marquis Colony Park Wagon	wagon超长；中间年份待确认	待终核: 1973-1974/1976-1977
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Sedan 1979-1982
Mercury Marquis	Mercury	跑车	Coupe	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Coupe 1979-1982
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸；原sdn/cou/wgn拆分	待终核: Wagon 1979-1982
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1992	212.4	77.8	56.7	1992 Ford Crown Victoria Sedan LX		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1993-1994	212.4	77.8	56.8	1993/1994 Ford Crown Victoria Sedan		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1995-1996	212	77.8	56.8	1995/1996 Ford Crown Victoria Sedan		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	1997-2002	212	78.2	56.8	1997/1998/1999/2000/2001/2002 Ford Crown Victoria Sedan	1997后宽度高于1995-1996	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2003	212	77.3	56.8	2003 Ford Crown Victoria Sedan	后期Panther；宽度按后期修正	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2004	212	78.2	56.8	2004 Ford Crown Victoria Sedan	2004宽度仍为78.2，需单独拆出	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2005	212	77.3	56.8	2005 Ford Crown Victoria Sedan		可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2006	212	78.3	58.3	2006 Ford Crown Victoria Sedan	2006标准轴页面宽高高于2005/2008	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	LWB	gen2 full-size Panther	2006	218	78.3	58.3	2006 Ford Crown Victoria Commercial Police Package Fleet LWB	LWB特殊版，不能覆盖Std.	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2007	212	77.3	58.3	2007 Ford Crown Victoria Sedan Base	2007高度高于2008-2011，单独拆出	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 full-size Panther	2008-2011	212	77.3	56.8	2008/2009/2010/2011 Ford Crown Victoria Sedan		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen1 midsize sedan	1989-1990	184.3	68.9	55.6	1989/1990 Hyundai Sonata CarsGuide / Autotrader AU	早期尺寸换算	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen1 midsize sedan	1991-1993	184.3	68.9	55.6	1989/1990 Hyundai Sonata cross-ref	1991-1993待直接核对	待终核: 1991-1993
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen2 midsize sedan	1994-1998	185	69.7	55.3	1997/1998 Hyundai Sonata	二代/改款尺寸；1994-1996待直接核对	待终核: 1994-1996
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	1999-2002	185.4	71.6	55.5	1999/2000/2001/2002 Hyundai Sonata		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	2003-2005	186.9	71.7	56	2003/2004/2005 Hyundai Sonata	2003后长度/宽/高增加	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen4 midsize sedan	2006-2010	188.9	72.1	58	2006/2007/2008/2009/2010 Hyundai Sonata LX/GLS		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen5 midsize sedan	2011-2014	189.8	72.2	57.9	2011/2012/2013/2014 Hyundai Sonata / Hybrid		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2015-2019	191.1	73.4	58.1	2015/2016/2017/2018/2019 Hyundai Sonata / Hybrid	hybrid高度较低不影响取高值	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 midsize sedan	2020-2023	192.9	73.2	56.9	2020/2021/2022/2023 Hyundai Sonata Hybrid/N Line		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 facelift midsize sedan	2024-2026	193.3	73.2	56.9	2024-2026 Hyundai Sonata Hybrid / N Line		可入库
Chevrolet Bolt EUV	Chevrolet	越野车	SUV	EV	gen1 compact EV SUV	2022-2023	169.5	69.7	63.6	2022/2023 Chevrolet Bolt EUV	EV小型SUV	可入库

下一步。

