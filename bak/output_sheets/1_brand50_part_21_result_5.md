# 文件名：1_brand50_part_21.tsv


--- Round 1 / 首次发送 ---
已按你上传的 1_brand50_part_21.tsv 做字段升级与阶段性修复；本轮依据为当前文件内容，未把参考车型未覆盖完整年份范围的记录误标为完成。

粘贴的文本 (1)

更新点

车型	操作/字段	描述
Lexus RX / Hyundai Santa Fe / Hyundai Sonata	状态修正	多个年份区间参考车型只覆盖单年或部分年份，改为待终核
Pontiac Firebird / Mercury Marquis	结构拆出	将 coupe/conv、sdn/cou/wgn 拆成单一结构记录
Subaru Outback Sp	结构标准化	2001-2007 归为 Wagon，2008-2011 归为 Hatchback
Ford Crown Victoria	状态修正	原普通口径参考车型过泛，保留但标记待终核/缺参考明细
全表	字段升级	统一为最新字段：主车型、品牌、分类、结构、版本、代际、年份、三维、参考车型、备注、迭代状态

阶段性 TSV：

tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	1999-2003	180.1	71.5	65.7	1999 Lexus RX 300 SUV Base		待终核: 2000-2003
Lexus RX	Lexus	越野车	SUV	Std.	gen2/3 midsize SUV	2004-2009	186.2	72.6	66.1	2004 Lexus RX 330		待终核: 2005-2009
Lexus RX	Lexus	越野车	SUV	Std.	gen2/3 midsize SUV	2010-2015	187.8	74.2	66.3	2010 Lexus RX 350		待终核: 2011-2015
Lexus RX	Lexus	越野车	SUV	Std.	gen4 midsize SUV	2016-2022	192.5	74.6	67.7	2016 Lexus RX 350		待终核: 2017-2022
Lexus RX	Lexus	越野车	SUV	L	gen4 L midsize SUV	2018	196.9	74.6	67.7	2018 Lexus RX 350L Base		可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 L midsize SUV	2019-2022	196.9	74.6	67.3	2022 Lexus RX 350L Base		待终核: 2019-2021
Lexus RX	Lexus	越野车	SUV	inc: PHEV	gen5 midsize SUV	2023-2026	192.5	75.6	67.3	2026 Lexus RX 450h+ Luxury		待终核: 2023-2025
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身	可入库
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen2 pony car	1970-1973	191.1	73.4	49.3	1970 Firebird	第二代早期	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Formula/Trans Am	gen2 pony car	1974-1981	196.8	73.2	49.6	1974-1981 Trans Am / Formula	保险杠增长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen3 pony car	1982-1988	191.8	72.4	50	1988 Firebird / Trans Am	低矮楔形	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen3 pony car	1989-1992	195.2	72.8	49.7	1990/1991 Firebird	末期造型更长	待终核: 1989/1992
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期	待终核: 1994-1997
Pontiac Firebird	Pontiac	跑车	Convertible	Std./Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期	待终核: 1994-1997
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸	待终核: 1998/1999/2001/2002
Pontiac Firebird	Pontiac	跑车	Convertible	Std./Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	2000 Firebird / Trans Am	末期前脸	待终核: 1998/1999/2001/2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2001-2006	177.2	72.6	65.9	2001 Hyundai Santa Fe GL		待终核: 2002-2006
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen2 midsize SUV	2007-2012	184.1	74.4	67.9	2007 / 2012 Hyundai Santa Fe		待终核: 2008-2011
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport/short	gen3 short midsize SUV	2013-2018	185	74	66.5	2018 Hyundai Santa Fe Sport		待终核: 2013-2017
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2013-2018	193.1	74.2	66.9	2013 Hyundai Santa Fe Limited		待终核: 2014-2018
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2019	193.1	74.2	66.9	2019 Hyundai Santa Fe XL		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen4 midsize SUV	2019-2023	188.4	74.4	66.3	2019-2023 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen5 midsize SUV	2024-2026	190.2	74.8	69.7	2024-2026 Hyundai Santa Fe Limited/Calligraphy		可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen1 Outback Sport wagon	2001	172.2	67.1	60	2001 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Hatchback	Std.	gen3 Outback Sport hatchback	2008-2011	173.8	68.5	58.3	2008-2011 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen5 midsize	1983-1986	196.5	71	53.8	1986 Mercury Marquis brochure / Mercury Marquis specs	中型四门	可入库
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen5 midsize	1983-1986	196.5	71	54.4	1986 Mercury Marquis brochure / Mercury Marquis specs	中型旅行车更高	可入库
Mercury Marquis	Mercury	三厢车	Coupe	2dr hardtop	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size	待终核: 1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size	待终核: sedan结构/1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低	待终核: sedan结构/1969-1971
Mercury Marquis	Mercury	三厢车	Coupe	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低	待终核: 1969-1971
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe	待终核: 1973/1974/1976/1978
Mercury Marquis	Mercury	三厢车	Coupe	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe	待终核: coupe结构/1973-1978
Mercury Marquis	Mercury	两厢车	Wagon	Colony Park	gen3 full-size	1973-1978	231	79.6	55	1975/1978 Mercury Marquis Colony Park Wagon	wagon超长	待终核: 1973/1974/1976/1977
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸	待终核: 1979-1982逐年
Mercury Marquis	Mercury	三厢车	Coupe	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸	待终核: 1979-1982逐年/coupe结构
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸	待终核: 1979-1982逐年/wagon结构
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	1992	212.4	77.8	56.7	Ford Crown Victoria		缺参考年份车型明细
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	1993-1997	212	77.8	56.8	Ford Crown Victoria		待终核: 1993-1997参考车型
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	1998-2011	212	78.2	56.8	Ford Crown Victoria		待终核: 1998-2011参考车型
Ford Crown Victoria	Ford	三厢车	Sedan	box	gen1 full-size Panther	1979-1991	212	78	56.8	Ford LTD Crown Victoria box Panther cross-ref	方正长尾厢	待终核: 1979-1991
Ford Crown Victoria	Ford	三厢车	Sedan	aero early	gen2 full-size Panther	1992-1997	212.4	77.8	56.8	1992/1995 Ford Crown Victoria LX	圆润Panther	待终核: 1993/1994/1996/1997
Ford Crown Victoria	Ford	三厢车	Sedan	aero facelift	gen2 full-size Panther	1998-2002	212	78.2	56.8	1998/2000 Ford Crown Victoria LX	facelift宽度高点	待终核: 1999/2001/2002
Ford Crown Victoria	Ford	三厢车	Sedan	aero late	gen2 full-size Panther	2003-2011	212	77.3	56.8	2003/2008/2011 Ford Crown Victoria Sedan	后期Panther	待终核: 2004-2007/2009/2010
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen1/2 midsize sedan	1989-1998	185	69.7	55.3	1998 Hyundai Sonata		待终核: 1989-1997
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	1999-2005	185.4	71.6	55.5	1999 Hyundai Sonata		待终核: 2000-2005
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen4 midsize sedan	2006-2010	188.9	72.1	58	2006 Hyundai Sonata LX		待终核: 2007-2010
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen5 midsize sedan	2011-2014	189.8	72.2	57.9	2011 Hyundai Sonata / 2014 Hybrid		待终核: 2012/2013
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2015-2019	191.1	73.4	58.1	2015 Hyundai Sonata Limited 2.0T		待终核: 2016-2019
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 midsize sedan	2020-2023	192.9	73.2	56.9	2023 Hyundai Sonata Hybrid Limited		待终核: 2020-2022
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 facelift midsize sedan	2024-2026	193.3	73.2	56.9	2025-2026 Hyundai Sonata Hybrid / N Line		待终核: 2024
Chevrolet Bolt EUV	Chevrolet	越野车	SUV	EV	gen1 compact EV SUV	2022-2023	169.5	69.7	63.6	2023 Chevrolet Bolt EUV	EV小型SUV	待终核: 2022

下一步


--- Round 2 / 下一步 ---
本轮优先推进了 Lexus RX、Hyundai Santa Fe、Hyundai Sonata、Chevrolet Bolt EUV，并修正了 Lexus RX 若干年份不能压缩的问题。Lexus RX 1999/2000/2003 为 180.1 × 71.5 × 65.7，但 2002 为 180.3 × 71.5 × 65.7，因此已拆出 2002；Lexus RX 2010、2011/2012、2013、2015 高度也不完全一致，已拆分；Hyundai Sonata 2024/2025/2026 三维一致，可合并；Bolt EUV 2022/2023 三维一致，已推进为可入库。
Edmunds
+12
Edmunds
+12
Edmunds
+12

更新点

车型	操作/字段	描述
Lexus RX	拆出 / 值修改	1999-2003 拆为 1999-2000、2001待终核、2002、2003；2002 长度改为 180.3
Lexus RX	拆出 / 值修改	2010-2015 因高度不同拆分，2010=66.3、2011-2012=67.7、2013=66.7、2014-2015待终核
Lexus RX	值修改	2016-2022 标准版拆为 2016 待确认和 2017-2022 待终核段，避免直接合并
Hyundai Santa Fe	拆出 / 值修改	2001-2006 拆为 2001、2002待终核、2003、2004-2006，宽高按已核年份修正
Hyundai Sonata	稳定	2024-2026 三维一致，推进为可入库
Chevrolet Bolt EUV	稳定	2022-2023 三维一致，推进为可入库

阶段性 TSV：

tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	1999-2000	180.1	71.5	65.7	1999/2000 Lexus RX 300 SUV Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2001	180.1	71.5	65.7	2001 Lexus RX 300 Base		待终核: 2001三维
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2002	180.3	71.5	65.7	2002 Lexus RX 300	2002长度略长	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2003	180.1	71.5	65.7	2003 Lexus RX 300		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2004-2005	186.2	72.6	66.1	2004/2005 Lexus RX 330		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2006	186.6	72.6	68.3	2006 Lexus RX 350 / CarsGuide cross-ref	高度来源待复核	待终核: Edmunds交叉确认
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2007	186.2	72.6	66.1	2007 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2008-2009	186.2	72.6	66.1	2007 Lexus RX 350 reference		待终核: 2008-2009
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2010	187.8	74.2	66.3	2010 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2011-2012	187.8	74.2	67.7	2011/2012 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2013	187.8	74.2	66.7	2013 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2014-2015	187.8	74.2	67.7	2015 Lexus RX 350 F SPORT		待终核: 2014
Lexus RX	Lexus	越野车	SUV	Std.	gen4 midsize SUV	2016	192.5	74.6	66.5	2016 Lexus RX 350 / CarsGuide cross-ref	高度需Edmunds复核	待终核: 2016 Edmunds
Lexus RX	Lexus	越野车	SUV	Std.	gen4 midsize SUV	2017-2022	192.5	74.6	67.7	2017/2021 Lexus RX 350		待终核: 2018-2020/2022
Lexus RX	Lexus	越野车	SUV	L	gen4 L midsize SUV	2018	196.9	74.6	67.7	2018 Lexus RX 350L Base		可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 L midsize SUV	2019-2022	196.9	74.6	67.3	2020/2021/2022 Lexus RX 350L		待终核: 2019
Lexus RX	Lexus	越野车	SUV	inc: PHEV	gen5 midsize SUV	2023-2026	192.5	75.6	67.3	2025/2026 Lexus RX 350/RX 450h+		待终核: 2023-2024
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身	可入库
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen2 pony car	1970-1973	191.1	73.4	49.3	1970 Firebird	第二代早期	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Formula/Trans Am	gen2 pony car	1974-1981	196.8	73.2	49.6	1974-1981 Trans Am / Formula	保险杠增长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen3 pony car	1982-1988	191.8	72.4	50	1988 Firebird / Trans Am	低矮楔形	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen3 pony car	1989-1992	195.2	72.8	49.7	1990/1991 Firebird	末期造型更长	待终核: 1989/1992
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期	待终核: 1994-1997
Pontiac Firebird	Pontiac	跑车	Convertible	Std./Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期	待终核: 1994-1997
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	1998/2000 Firebird / Trans Am	末期前脸	待终核: 1999/2001/2002
Pontiac Firebird	Pontiac	跑车	Convertible	Std./Trans Am	gen4 pony car	1998-2002	193.8	74.5	52	1998 Pontiac Firebird Convertible Trans Am / 2000 Firebird Convertible	末期前脸，敞篷高度略高	待终核: 1999/2001/2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2001	177.2	72.6	65.9	2001 Hyundai Santa Fe GL		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2002	177.2	72.6	65.9	2001/2003 Hyundai Santa Fe reference		待终核: 2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2003	177.2	72.6	65.9	2003 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2004-2006	177.2	72.7	66	2004/2005/2006 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen2 midsize SUV	2007-2012	184.1	74.4	67.9	2007 / 2012 Hyundai Santa Fe		待终核: 2008-2011
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport/short	gen3 short midsize SUV	2013-2018	185	74	66.5	2018 Hyundai Santa Fe Sport		待终核: 2013-2017
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2013-2018	193.1	74.2	66.9	2013 Hyundai Santa Fe Limited		待终核: 2014-2018
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2019	193.1	74.2	66.9	2019 Hyundai Santa Fe XL		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen4 midsize SUV	2019-2023	188.4	74.4	66.3	2019-2023 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen5 midsize SUV	2024-2026	190.2	74.8	69.7	2024-2026 Hyundai Santa Fe Limited/Calligraphy		可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen1 Outback Sport wagon	2001	172.2	67.1	60	2001 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Hatchback	Std.	gen3 Outback Sport hatchback	2008-2011	173.8	68.5	58.3	2008-2011 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen5 midsize	1983-1986	196.5	71	53.8	1986 Mercury Marquis brochure / Mercury Marquis specs	中型四门	可入库
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen5 midsize	1983-1986	196.5	71	54.4	1986 Mercury Marquis brochure / Mercury Marquis specs	中型旅行车更高	可入库
Mercury Marquis	Mercury	三厢车	Coupe	2dr hardtop	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size	待终核: 1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size	待终核: sedan结构/1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低	待终核: sedan结构/1969-1971
Mercury Marquis	Mercury	三厢车	Coupe	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低	待终核: 1969-1971
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe	待终核: 1973/1974/1976/1978
Mercury Marquis	Mercury	三厢车	Coupe	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe	待终核: coupe结构/1973-1978
Mercury Marquis	Mercury	两厢车	Wagon	Colony Park	gen3 full-size	1973-1978	231	79.6	55	1975/1978 Mercury Marquis Colony Park Wagon	wagon超长	待终核: 1973/1974/1976/1977
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸	待终核: 1979-1982逐年
Mercury Marquis	Mercury	三厢车	Coupe	Std.	gen4 full-size	1979-1982	212.3	77.5	55.1	1980/1982 Mercury Grand Marquis 2-Door, Automobile-Catalog	Grand Marquis 2dr参考，Marquis coupe待交叉	待终核: 1979/1981及Marquis口径
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸	待终核: 1979-1982逐年/wagon结构
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	1992	212.4	77.8	56.7	Ford Crown Victoria		缺参考年份车型明细
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	1993-1997	212	77.8	56.8	Ford Crown Victoria		待终核: 1993-1997参考车型
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	1998-2011	212	78.2	56.8	Ford Crown Victoria		待终核: 1998-2011参考车型
Ford Crown Victoria	Ford	三厢车	Sedan	box	gen1 full-size Panther	1979-1991	212	78	56.8	Ford LTD Crown Victoria box Panther cross-ref	方正长尾厢	待终核: 1979-1991
Ford Crown Victoria	Ford	三厢车	Sedan	aero early	gen2 full-size Panther	1992-1997	212.4	77.8	56.8	1992/1995 Ford Crown Victoria LX	圆润Panther	待终核: 1993/1994/1996/1997
Ford Crown Victoria	Ford	三厢车	Sedan	aero facelift	gen2 full-size Panther	1998-2002	212	78.2	56.8	1998/2000 Ford Crown Victoria LX	facelift宽度高点	待终核: 1999/2001/2002
Ford Crown Victoria	Ford	三厢车	Sedan	aero late	gen2 full-size Panther	2003-2011	212	78.2	56.8	2003/2007 Ford Crown Victoria LX	后期Panther，宽度按Edmunds/AutoDetective修正	待终核: 2004-2006/2008-2011
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen1/2 midsize sedan	1989-1998	185	69.7	55.3	1998 Hyundai Sonata		待终核: 1989-1997
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	1999-2005	185.4	71.6	55.5	1999/2001 Hyundai Sonata		待终核: 2000/2002-2005
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen4 midsize sedan	2006-2010	188.9	72.1	58	2006 Hyundai Sonata LX		待终核: 2007-2010
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen5 midsize sedan	2011-2014	189.8	72.2	57.9	2011 Hyundai Sonata / 2014 Hybrid		待终核: 2012/2013
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2015-2019	191.1	73.4	58.1	2015/2019 Hyundai Sonata		待终核: 2016-2018
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 midsize sedan	2020-2023	192.9	73.2	56.9	2022/2023 Hyundai Sonata Hybrid Limited		待终核: 2020/2021
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 facelift midsize sedan	2024-2026	193.3	73.2	56.9	2024/2025/2026 Hyundai Sonata Hybrid / N Line		可入库
Chevrolet Bolt EUV	Chevrolet	越野车	SUV	EV	gen1 compact EV SUV	2022-2023	169.5	69.7	63.6	2022/2023 Chevrolet Bolt EUV	EV小型SUV	可入库

下一步


--- Round 3 / 下一步 ---
本轮继续补强了 Lexus RX、Hyundai Santa Fe、Hyundai Sonata、Chevrolet Bolt EUV，并把能确认完整年份覆盖的记录推进为可入库。Lexus RX 2001/2002 在 Edmunds 上均为 180.3 × 71.5 × 65.7，不能并入 1999/2000/2003 的 180.1 长度组；2014 RX 350 Base 为 66.7 高，但 F SPORT 为 67.7，因此按最大高度保留 67.7 并与 2015 合并待继续补 2015；2023/2025/2026 RX 350/450h+ 均为 192.5 × 75.6 × 67.3，可把 2023-2026 当前代推进到只剩 2024待终核。
Edmunds
+7
Edmunds
+7
Edmunds
+7

Hyundai Santa Fe 2008/2010 Edmunds 均显示 184.1 × 74.4 × 67.9，可推进 2007-2012 段；2013 Santa Fe Sport 2.0T 高度 66.5，可保留 Sport/short 行最大高 66.5；2014 Santa Fe Limited 为 193.1 × 74.2 × 66.9，可推进 XL/long 行。Hyundai Sonata 2000、2006、2016、2020 的 Edmunds 数据分别支撑对应代际尺寸，2024-2026 已维持可入库；Bolt EUV 2022/2023 Edmunds 均为 169.5 × 69.7 × 63.6，可入库。
Edmunds
+9
Edmunds
+9
Edmunds
+9

更新点

车型	操作/字段	描述
Lexus RX	值修改 / 拆分	2001 长度修正为 180.3，并与 2002 合并为 2001-2002
Lexus RX	稳定	2008 已核，2008-2009 仍保留 2009待终核
Lexus RX	稳定	2023/2025/2026 已核，2023-2026 仅剩 2024待终核
Hyundai Santa Fe	稳定	2008/2010 已核，2007-2012 仅剩 2009/2011待终核
Hyundai Santa Fe	值修改	2013 Sport/short 长度修正为 184.6，保留高点 66.5
Hyundai Sonata	稳定	2000、2006、2016、2020 已核，多个区间待核年份减少
Chevrolet Bolt EUV	稳定	2022/2023 均已核，保持可入库

阶段性 TSV：

tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	1999-2000	180.1	71.5	65.7	1999/2000 Lexus RX 300 SUV Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2001-2002	180.3	71.5	65.7	2001/2002 Lexus RX 300	2001-2002长度略长	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2003	180.1	71.5	65.7	2003 Lexus RX 300		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2004-2005	186.2	72.6	66.1	2004/2005 Lexus RX 330		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2006	186.6	72.6	68.3	2006 Lexus RX 350 / CarsGuide cross-ref	高度来源待复核	待终核: Edmunds交叉确认
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2007-2008	186.2	72.6	66.1	2007/2008 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2009	186.2	72.6	66.1	2007/2008 Lexus RX 350 reference		待终核: 2009
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2010	187.8	74.2	66.3	2010 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2011-2012	187.8	74.2	67.7	2011/2012 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2013	187.8	74.2	66.7	2013 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2014-2015	187.8	74.2	67.7	2014 Lexus RX 350 F SPORT / 2015 Lexus RX 350 F SPORT	按F SPORT高点	待终核: 2015
Lexus RX	Lexus	越野车	SUV	Std.	gen4 midsize SUV	2016	192.5	74.6	66.5	2016 Lexus RX 350 / CarsGuide cross-ref	高度需Edmunds复核	待终核: 2016 Edmunds
Lexus RX	Lexus	越野车	SUV	Std.	gen4 midsize SUV	2017-2022	192.5	74.6	67.7	2017/2021 Lexus RX 350		待终核: 2018-2020/2022
Lexus RX	Lexus	越野车	SUV	L	gen4 L midsize SUV	2018	196.9	74.6	67.7	2018 Lexus RX 350L Base		可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 L midsize SUV	2019-2022	196.9	74.6	67.3	2020/2021/2022 Lexus RX 350L		待终核: 2019
Lexus RX	Lexus	越野车	SUV	inc: PHEV	gen5 midsize SUV	2023-2026	192.5	75.6	67.3	2023/2025/2026 Lexus RX 350/RX 450h+		待终核: 2024
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身	可入库
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen2 pony car	1970-1973	191.1	73.4	49.3	1970 Firebird	第二代早期	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Formula/Trans Am	gen2 pony car	1974-1981	196.8	73.2	49.6	1974-1981 Trans Am / Formula	保险杠增长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen3 pony car	1982-1988	191.8	72.4	50	1988 Firebird / Trans Am	低矮楔形	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen3 pony car	1989-1992	195.2	72.8	49.7	1990/1991 Firebird	末期造型更长	待终核: 1989/1992
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期	待终核: 1994-1997
Pontiac Firebird	Pontiac	跑车	Convertible	Std./Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期	待终核: 1994-1997
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	1998/2000 Firebird / Trans Am	末期前脸	待终核: 1999/2001/2002
Pontiac Firebird	Pontiac	跑车	Convertible	Std./Trans Am	gen4 pony car	1998-2002	193.8	74.5	52	1998 Pontiac Firebird Convertible Trans Am / 2000 Firebird Convertible	末期前脸，敞篷高度略高	待终核: 1999/2001/2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2001	177.2	72.6	65.9	2001 Hyundai Santa Fe GL		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2002	177.2	72.6	65.9	2001/2003 Hyundai Santa Fe reference		待终核: 2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2003	177.2	72.6	65.9	2003 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2004-2006	177.2	72.7	66	2004/2005/2006 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen2 midsize SUV	2007-2012	184.1	74.4	67.9	2007/2008/2010/2012 Hyundai Santa Fe		待终核: 2009/2011
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport/short	gen3 short midsize SUV	2013	184.6	74	66.5	2013 Hyundai Santa Fe Sport 2.0T	短轴Sport高点	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport/short	gen3 short midsize SUV	2014-2018	185	74	66.5	2018 Hyundai Santa Fe Sport		待终核: 2014-2017
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2013	193.1	74.2	66.5	2013 Hyundai Santa Fe GLS/Limited		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2014-2018	193.1	74.2	66.9	2014 Hyundai Santa Fe Limited / 2018 Hyundai Santa Fe		待终核: 2015-2017
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2019	193.1	74.2	66.9	2019 Hyundai Santa Fe XL		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen4 midsize SUV	2019-2023	188.4	74.4	66.3	2019-2023 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen5 midsize SUV	2024-2026	190.2	74.8	69.7	2024-2026 Hyundai Santa Fe Limited/Calligraphy		可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen1 Outback Sport wagon	2001	172.2	67.1	60	2001 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Hatchback	Std.	gen3 Outback Sport hatchback	2008-2011	173.8	68.5	58.3	2008-2011 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen5 midsize	1983-1986	196.5	71	53.8	1986 Mercury Marquis brochure / Mercury Marquis specs	中型四门	可入库
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen5 midsize	1983-1986	196.5	71	54.4	1986 Mercury Marquis brochure / Mercury Marquis specs	中型旅行车更高	可入库
Mercury Marquis	Mercury	三厢车	Coupe	2dr hardtop	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size	待终核: 1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size	待终核: sedan结构/1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低	待终核: sedan结构/1969-1971
Mercury Marquis	Mercury	三厢车	Coupe	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低	待终核: 1969-1971
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe	待终核: 1973/1974/1976/1978
Mercury Marquis	Mercury	三厢车	Coupe	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe	待终核: coupe结构/1973-1978
Mercury Marquis	Mercury	两厢车	Wagon	Colony Park	gen3 full-size	1973-1978	231	79.6	55	1975/1978 Mercury Marquis Colony Park Wagon	wagon超长	待终核: 1973/1974/1976/1977
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸	待终核: 1979-1982逐年
Mercury Marquis	Mercury	三厢车	Coupe	Std.	gen4 full-size	1979-1982	212.3	77.5	55.1	1980/1982 Mercury Grand Marquis 2-Door, Automobile-Catalog	Grand Marquis 2dr参考，Marquis coupe待交叉	待终核: 1979/1981及Marquis口径
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸	待终核: 1979-1982逐年/wagon结构
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	1992	212.4	77.8	56.7	Ford Crown Victoria		缺参考年份车型明细
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	1993-1997	212	77.8	56.8	Ford Crown Victoria		待终核: 1993-1997参考车型
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	1998-2011	212	78.2	56.8	Ford Crown Victoria		待终核: 1998-2011参考车型
Ford Crown Victoria	Ford	三厢车	Sedan	box	gen1 full-size Panther	1979-1991	212	78	56.8	Ford LTD Crown Victoria box Panther cross-ref	方正长尾厢	待终核: 1979-1991
Ford Crown Victoria	Ford	三厢车	Sedan	aero early	gen2 full-size Panther	1992-1997	212.4	77.8	56.8	1992/1995 Ford Crown Victoria LX	圆润Panther	待终核: 1993/1994/1996/1997
Ford Crown Victoria	Ford	三厢车	Sedan	aero facelift	gen2 full-size Panther	1998-2002	212	78.2	56.8	1998/2000 Ford Crown Victoria LX	facelift宽度高点	待终核: 1999/2001/2002
Ford Crown Victoria	Ford	三厢车	Sedan	aero late	gen2 full-size Panther	2003-2011	212	78.2	56.8	2003/2007 Ford Crown Victoria LX	后期Panther，宽度按Edmunds/AutoDetective修正	待终核: 2004-2006/2008-2011
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen1/2 midsize sedan	1989-1998	185	69.7	55.3	1998 Hyundai Sonata		待终核: 1989-1997
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	1999-2005	185.4	71.6	55.5	1999/2000/2001 Hyundai Sonata		待终核: 2002-2005
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen4 midsize sedan	2006-2010	188.9	72.1	58	2006 Hyundai Sonata LX		待终核: 2007-2010
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen5 midsize sedan	2011-2014	189.8	72.2	57.9	2011 Hyundai Sonata / 2014 Hybrid		待终核: 2012/2013
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2015-2019	191.1	73.4	58.1	2015/2016/2019 Hyundai Sonata		待终核: 2017-2018
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 midsize sedan	2020-2023	192.9	73.2	56.9	2020/2022/2023 Hyundai Sonata Hybrid Limited		待终核: 2021
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 facelift midsize sedan	2024-2026	193.3	73.2	56.9	2024/2025/2026 Hyundai Sonata Hybrid / N Line		可入库
Chevrolet Bolt EUV	Chevrolet	越野车	SUV	EV	gen1 compact EV SUV	2022-2023	169.5	69.7	63.6	2022/2023 Chevrolet Bolt EUV	EV小型SUV	可入库

下一步


--- Round 4 / 下一步 ---
本轮继续补强了 RX、Santa Fe、Sonata、Crown Victoria、Marquis 的缺口。重点修正：RX 2016 标准版在 Edmunds 为 192.5 × 74.6 × 67.7，可并入 2017-2022 标准版；RX 2023/2024/2026 当前代均为 192.5 × 75.6 × 67.3，可推进为可入库。
Edmunds
+5
Edmunds
+5
Edmunds
+5

Santa Fe 2009/2011 与 2007/2012 同为 184.1 × 74.4 × 67.9，因此 2007-2012 可入库；Santa Fe Sport 2015/2016 为 184.6 × 74.0 × 66.1，2017 2.0T 高度 66.5，因此短轴 Sport 2014-2018 仍按 185.0 × 74.0 × 66.5 取高点；Santa Fe 长轴 2015/2016/2017/2018 均支撑 193.1 × 74.2 × 66.9。
Edmunds
+8
Edmunds
+8
Edmunds
+8

Crown Victoria 1993/1994/1997 支撑 1993-1997 行，1999-2002 为 212.0 × 78.2 × 56.8，2004/2005/2010/2011 为 212.0 × 77.3-78.2 × 56.8，2006/2008 出现 78.3 × 58.3 的高点口径，因此 2003-2011 后期行暂时不直接压成单一可入库段，先保留待终核。Mercury Marquis 1979-1982 属 downsized 第三代，1979 2-door 参考为 212 in × 77.5 in × 54.5 in，但 sedan/wagon 仍需继续补。
automobile-catalog.com
+13
Edmunds
+13
Edmunds
+13

更新点

车型	操作/字段	描述
Lexus RX	稳定	2009、2016、2024 已补，标准版 2016-2022 与当前代 2023-2026 推进为可入库
Lexus RX	值修改	2014-2015 高度按 Edmunds Base/F SPORT 口径拆成 2014=66.7、2015待终核
Hyundai Santa Fe	稳定	2007-2012、2019-2023、2024-2026 推进为可入库
Hyundai Santa Fe	稳定	Sport/short 与 XL/long 缺口减少，长轴 2015-2018 推进为可入库
Hyundai Sonata	稳定	2007-2010、2020-2023 推进为可入库，1999-2005、2015-2019 仍有少量年份待终核
Ford Crown Victoria	值修改	2003-2011 发现 77.3/78.2/78.3 宽度和 56.8/58.3 高度口径差，暂不合并为最终可入库
Mercury Marquis	值修改	1979-1982 coupe 有 1979/1980/1982 参考，sedan/wagon 继续待终核

阶段性 TSV：

tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	1999-2000	180.1	71.5	65.7	1999/2000 Lexus RX 300 SUV Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2001-2002	180.3	71.5	65.7	2001/2002 Lexus RX 300	2001-2002长度略长	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2003	180.1	71.5	65.7	2003 Lexus RX 300		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2004-2005	186.2	72.6	66.1	2004/2005 Lexus RX 330		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2006	186.6	72.6	68.3	2006 Lexus RX 350 / CarsGuide cross-ref	高度来源待复核	待终核: Edmunds交叉确认
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2007-2009	186.2	72.6	66.1	2007/2008/2009 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2010	187.8	74.2	66.3	2010 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2011-2012	187.8	74.2	67.7	2011/2012 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2013-2014	187.8	74.2	66.7	2013/2014 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2015	187.8	74.2	67.7	2015 Lexus RX 350 F SPORT	按F SPORT高点	待终核: 2015 Base/F SPORT交叉
Lexus RX	Lexus	越野车	SUV	Std.	gen4 midsize SUV	2016-2022	192.5	74.6	67.7	2016/2017/2022 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 L midsize SUV	2018	196.9	74.6	67.7	2018 Lexus RX 350L Base		可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 L midsize SUV	2019-2022	196.9	74.6	67.3	2020/2021/2022 Lexus RX 350L		待终核: 2019
Lexus RX	Lexus	越野车	SUV	inc: PHEV	gen5 midsize SUV	2023-2026	192.5	75.6	67.3	2023/2024/2025/2026 Lexus RX 350/RX 450h+		可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身	可入库
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen2 pony car	1970-1973	191.1	73.4	49.3	1970 Firebird	第二代早期	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Formula/Trans Am	gen2 pony car	1974-1981	196.8	73.2	49.6	1974-1981 Trans Am / Formula	保险杠增长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen3 pony car	1982-1988	191.8	72.4	50	1988 Firebird / Trans Am	低矮楔形	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen3 pony car	1989-1992	195.2	72.8	49.7	1990/1991 Firebird	末期造型更长	待终核: 1989/1992
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期	待终核: 1994-1997
Pontiac Firebird	Pontiac	跑车	Convertible	Std./Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期	待终核: 1994-1997
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	1998/2000 Firebird / Trans Am	末期前脸	待终核: 1999/2001/2002
Pontiac Firebird	Pontiac	跑车	Convertible	Std./Trans Am	gen4 pony car	1998-2002	193.8	74.5	52	1998 Pontiac Firebird Convertible Trans Am / 2000 Firebird Convertible	末期前脸，敞篷高度略高	待终核: 1999/2001/2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2001	177.2	72.6	65.9	2001 Hyundai Santa Fe GL		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2002	177.2	72.6	65.9	2001/2003 Hyundai Santa Fe reference		待终核: 2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2003	177.2	72.6	65.9	2003 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2004-2006	177.2	72.7	66	2004/2005/2006 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen2 midsize SUV	2007-2012	184.1	74.4	67.9	2007/2008/2009/2010/2011/2012 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport/short	gen3 short midsize SUV	2013	184.6	74	66.5	2013 Hyundai Santa Fe Sport 2.0T	短轴Sport高点	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport/short	gen3 short midsize SUV	2014	184.6	74	66.5	2014 Hyundai Santa Fe Sport	按2.0T高点保守	待终核: 2014高点交叉
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport/short	gen3 short midsize SUV	2015-2016	184.6	74	66.1	2015/2016 Hyundai Santa Fe Sport	短轴Sport	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport/short	gen3 short midsize SUV	2017-2018	185	74	66.5	2017/2018 Hyundai Santa Fe Sport 2.0T	短轴Sport高点	待终核: 2018
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2013	193.1	74.2	66.5	2013 Hyundai Santa Fe GLS/Limited		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2014	193.1	74.2	66.9	2014 Hyundai Santa Fe Limited		待终核: 2014
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2015-2018	193.1	74.2	66.9	2015/2016/2017/2018 Hyundai Santa Fe Limited		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2019	193.1	74.2	66.9	2019 Hyundai Santa Fe XL		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen4 midsize SUV	2019-2023	188.4	74.4	66.3	2019-2023 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen5 midsize SUV	2024-2026	190.2	74.8	69.7	2024-2026 Hyundai Santa Fe Limited/Calligraphy		可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen1 Outback Sport wagon	2001	172.2	67.1	60	2001 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Hatchback	Std.	gen3 Outback Sport hatchback	2008-2011	173.8	68.5	58.3	2008-2011 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen5 midsize	1983-1986	196.5	71	53.8	1986 Mercury Marquis brochure / Mercury Marquis specs	中型四门	可入库
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen5 midsize	1983-1986	196.5	71	54.4	1986 Mercury Marquis brochure / Mercury Marquis specs	中型旅行车更高	可入库
Mercury Marquis	Mercury	三厢车	Coupe	2dr hardtop	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size	待终核: 1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size	待终核: sedan结构/1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低	待终核: sedan结构/1969-1971
Mercury Marquis	Mercury	三厢车	Coupe	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低	待终核: 1969-1971
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe	待终核: 1973/1974/1976/1978
Mercury Marquis	Mercury	三厢车	Coupe	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe	待终核: coupe结构/1973-1978
Mercury Marquis	Mercury	两厢车	Wagon	Colony Park	gen3 full-size	1973-1978	231	79.6	55	1975/1978 Mercury Marquis Colony Park Wagon	wagon超长	待终核: 1973/1974/1976/1977
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸	待终核: 1979-1982逐年
Mercury Marquis	Mercury	三厢车	Coupe	Std.	gen4 full-size	1979-1982	212.3	77.5	55.1	1979/1980/1982 Mercury Marquis/Grand Marquis 2-Door, Automobile-Catalog	Grand Marquis 2dr参考，Marquis coupe待交叉	待终核: 1981及Marquis口径
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸	待终核: 1979-1982逐年/wagon结构
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	1992	212.4	77.8	56.7	Ford Crown Victoria		缺参考年份车型明细
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	1993-1997	212	77.8	56.8	1993/1994/1996/1997 Ford Crown Victoria		待终核: 1995参考车型
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	1998-2002	212	78.2	56.8	1999/2000/2001/2002 Ford Crown Victoria		待终核: 1998参考车型
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	2003-2005	212	78.2	56.8	2004/2005 Ford Crown Victoria	2005宽度口径低，按区间高点	待终核: 2003
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	2006-2008	212	78.3	58.3	2006/2008 Ford Crown Victoria	疑似P71/口径高点	待终核: 2007及口径
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	2009-2011	212	77.3	56.8	2010/2011 Ford Crown Victoria		待终核: 2009
Ford Crown Victoria	Ford	三厢车	Sedan	box	gen1 full-size Panther	1979-1991	212	78	56.8	Ford LTD Crown Victoria box Panther cross-ref	方正长尾厢	待终核: 1979-1991
Ford Crown Victoria	Ford	三厢车	Sedan	aero early	gen2 full-size Panther	1992	212.4	77.8	56.8	1992 Ford Crown Victoria LX	圆润Panther	待终核: 1992高度口径
Ford Crown Victoria	Ford	三厢车	Sedan	aero early	gen2 full-size Panther	1993-1997	212	77.8	56.8	1993/1994/1995/1996/1997 Ford Crown Victoria LX	圆润Panther	待终核: 1995
Ford Crown Victoria	Ford	三厢车	Sedan	aero facelift	gen2 full-size Panther	1998-2002	212	78.2	56.8	1998/1999/2000/2001/2002 Ford Crown Victoria LX	facelift宽度高点	待终核: 1998
Ford Crown Victoria	Ford	三厢车	Sedan	aero late	gen2 full-size Panther	2003-2005	212	78.2	56.8	2003/2004/2005 Ford Crown Victoria LX	后期Panther	待终核: 2003
Ford Crown Victoria	Ford	三厢车	Sedan	aero late	gen2 full-size Panther	2006-2008	212	78.3	58.3	2006/2008 Ford Crown Victoria	疑似高点口径，需确认民用/P71	待终核: 2007及口径
Ford Crown Victoria	Ford	三厢车	Sedan	aero late	gen2 full-size Panther	2009-2011	212	77.3	56.8	2010/2011 Ford Crown Victoria	后期Panther	待终核: 2009
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen1/2 midsize sedan	1989-1998	185	69.7	55.3	1998 Hyundai Sonata		待终核: 1989-1997
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	1999-2001	185.4	71.6	55.5	1999/2000/2001 Hyundai Sonata		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	2002-2005	185.4	71.6	55.5	1999/2001 Hyundai Sonata reference		待终核: 2002-2005
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen4 midsize sedan	2006-2010	188.9	72.1	58	2006/2007/2008/2009/2010 Hyundai Sonata		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen5 midsize sedan	2011-2014	189.8	72.2	57.9	2011/2012/2014 Hyundai Sonata / Hybrid		待终核: 2013
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2015-2016	191.1	73.4	58.1	2015/2016 Hyundai Sonata		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2017-2019	191.1	73.4	58.1	2015/2016/2019 Hyundai Sonata reference		待终核: 2017-2018
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 midsize sedan	2020-2023	192.9	73.2	56.9	2020/2021/2022/2023 Hyundai Sonata Hybrid Limited		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 facelift midsize sedan	2024-2026	193.3	73.2	56.9	2024/2025/2026 Hyundai Sonata Hybrid / N Line		可入库
Chevrolet Bolt EUV	Chevrolet	越野车	SUV	EV	gen1 compact EV SUV	2022-2023	169.5	69.7	63.6	2022/2023 Chevrolet Bolt EUV	EV小型SUV	可入库

下一步


--- Round 5 / 下一步 ---
本轮主要清掉了 Lexus RX 和 Hyundai Sonata 的大块待核。关键修正：2006 RX 应按 Edmunds 的 RX 330 口径走 186.2 × 72.6 × 66.1，可并入 2004-2009；2015 RX 350 Edmunds 为 187.8 × 74.2 × 66.3，不再按 67.7 高点；2019 RX 350L 已补齐，可并入 2019-2022 L。
Edmunds
+2
Edmunds
+2

Hyundai Sonata 2002 仍是 185.4 × 71.6 × 55.5，但 2003-2005 已变为 186.9 × 71.7 × 56.0，所以 1999-2005 必须拆为 1999-2002 与 2003-2005；2017 Sonata 普通版为 191.1 × 73.4 × 58.1，2017 Hybrid 高度 57.9，按车衣保守高点仍取 58.1。
Edmunds
+5
Edmunds
+5
Edmunds
+5

更新点

车型	操作/字段	描述
Lexus RX	合并 / 值修改	2004-2009 统一为 186.2 / 72.6 / 66.1，推进为可入库
Lexus RX	值修改	2015 高度从 67.7 修正为 66.3
Lexus RX	稳定	2019 RX 350L 已补，2019-2022 L 推进为可入库
Hyundai Sonata	拆出 / 值修改	1999-2002 与 2003-2005 尺寸不同，拆分并推进为可入库
Hyundai Sonata	稳定	2017 已补，2015-2017 可入库，2018-2019 仍待终核
Hyundai Santa Fe	保留	2002、2014 Sport、2014 XL、2018 Sport 仍待补强
Ford Crown Victoria / Mercury Marquis / Firebird	保留	老车/大车剩余待核仍保留，未误标完成

阶段性 TSV：

tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	1999-2000	180.1	71.5	65.7	1999/2000 Lexus RX 300 SUV Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2001-2002	180.3	71.5	65.7	2001/2002 Lexus RX 300	2001-2002长度略长	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2003	180.1	71.5	65.7	2003 Lexus RX 300		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2004-2009	186.2	72.6	66.1	2004/2005/2006 Lexus RX 330; 2007/2008/2009 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2010	187.8	74.2	66.3	2010 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2011-2012	187.8	74.2	67.7	2011/2012 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2013-2014	187.8	74.2	66.7	2013/2014 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2015	187.8	74.2	66.3	2015 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen4 midsize SUV	2016-2022	192.5	74.6	67.7	2016/2017/2022 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 L midsize SUV	2018	196.9	74.6	67.7	2018 Lexus RX 350L Base		可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 L midsize SUV	2019-2022	196.9	74.6	67.3	2019/2020/2021/2022 Lexus RX 350L		可入库
Lexus RX	Lexus	越野车	SUV	inc: PHEV	gen5 midsize SUV	2023-2026	192.5	75.6	67.3	2023/2024/2025/2026 Lexus RX 350/RX 450h+		可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身	可入库
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen2 pony car	1970-1973	191.1	73.4	49.3	1970 Firebird	第二代早期	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Formula/Trans Am	gen2 pony car	1974-1981	196.8	73.2	49.6	1974-1981 Trans Am / Formula	保险杠增长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen3 pony car	1982-1988	191.8	72.4	50	1988 Firebird / Trans Am	低矮楔形	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen3 pony car	1989-1992	195.2	72.8	49.7	1990/1991 Firebird	末期造型更长	待终核: 1989/1992
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期	待终核: 1994-1997
Pontiac Firebird	Pontiac	跑车	Convertible	Std./Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期	待终核: 1994-1997
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	1998/2000 Firebird / Trans Am	末期前脸	待终核: 1999/2001/2002
Pontiac Firebird	Pontiac	跑车	Convertible	Std./Trans Am	gen4 pony car	1998-2002	193.8	74.5	52	1998 Pontiac Firebird Convertible Trans Am / 2000 Firebird Convertible	末期前脸，敞篷高度略高	待终核: 1999/2001/2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2001	177.2	72.6	65.9	2001 Hyundai Santa Fe GL		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2002	177.2	72.6	65.9	2001/2003 Hyundai Santa Fe reference		待终核: 2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2003	177.2	72.6	65.9	2003 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2004-2006	177.2	72.7	66	2004/2005/2006 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen2 midsize SUV	2007-2012	184.1	74.4	67.9	2007/2008/2009/2010/2011/2012 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport/short	gen3 short midsize SUV	2013	184.6	74	66.5	2013 Hyundai Santa Fe Sport 2.0T	短轴Sport高点	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport/short	gen3 short midsize SUV	2014	184.6	74	66.5	2014 Hyundai Santa Fe Sport	按2.0T高点保守	待终核: 2014高点交叉
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport/short	gen3 short midsize SUV	2015-2016	184.6	74	66.1	2015/2016 Hyundai Santa Fe Sport	短轴Sport	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport/short	gen3 short midsize SUV	2017-2018	185	74	66.5	2017/2018 Hyundai Santa Fe Sport 2.0T	短轴Sport高点	待终核: 2018
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2013	193.1	74.2	66.5	2013 Hyundai Santa Fe GLS/Limited		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2014	193.1	74.2	66.9	2014 Hyundai Santa Fe Limited		待终核: 2014
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2015-2018	193.1	74.2	66.9	2015/2016/2017/2018 Hyundai Santa Fe Limited		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2019	193.1	74.2	66.9	2019 Hyundai Santa Fe XL		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen4 midsize SUV	2019-2023	188.4	74.4	66.3	2019-2023 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen5 midsize SUV	2024-2026	190.2	74.8	69.7	2024-2026 Hyundai Santa Fe Limited/Calligraphy		可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen1 Outback Sport wagon	2001	172.2	67.1	60	2001 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Hatchback	Std.	gen3 Outback Sport hatchback	2008-2011	173.8	68.5	58.3	2008-2011 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen5 midsize	1983-1986	196.5	71	53.8	1986 Mercury Marquis brochure / Mercury Marquis specs	中型四门	可入库
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen5 midsize	1983-1986	196.5	71	54.4	1986 Mercury Marquis brochure / Mercury Marquis specs	中型旅行车更高	可入库
Mercury Marquis	Mercury	三厢车	Coupe	2dr hardtop	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size	待终核: 1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size	待终核: sedan结构/1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低	待终核: sedan结构/1969-1971
Mercury Marquis	Mercury	三厢车	Coupe	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低	待终核: 1969-1971
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe	待终核: 1973/1974/1976/1978
Mercury Marquis	Mercury	三厢车	Coupe	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe	待终核: coupe结构/1973-1978
Mercury Marquis	Mercury	两厢车	Wagon	Colony Park	gen3 full-size	1973-1978	231	79.6	55	1975/1978 Mercury Marquis Colony Park Wagon	wagon超长	待终核: 1973/1974/1976/1977
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸	待终核: 1979-1982逐年
Mercury Marquis	Mercury	三厢车	Coupe	Std.	gen4 full-size	1979-1982	212.3	77.5	55.1	1979/1980/1982 Mercury Marquis/Grand Marquis 2-Door, Automobile-Catalog	Grand Marquis 2dr参考，Marquis coupe待交叉	待终核: 1981及Marquis口径
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸	待终核: 1979-1982逐年/wagon结构
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	1992	212.4	77.8	56.7	Ford Crown Victoria		缺参考年份车型明细
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	1993-1997	212	77.8	56.8	1993/1994/1996/1997 Ford Crown Victoria		待终核: 1995参考车型
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	1998-2002	212	78.2	56.8	1999/2000/2001/2002 Ford Crown Victoria		待终核: 1998参考车型
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	2003-2005	212	78.2	56.8	2004/2005 Ford Crown Victoria	2005宽度口径低，按区间高点	待终核: 2003
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	2006-2008	212	78.3	58.3	2006/2008 Ford Crown Victoria	疑似P71/口径高点	待终核: 2007及口径
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	2009-2011	212	77.3	56.8	2010/2011 Ford Crown Victoria		待终核: 2009
Ford Crown Victoria	Ford	三厢车	Sedan	box	gen1 full-size Panther	1979-1991	212	78	56.8	Ford LTD Crown Victoria box Panther cross-ref	方正长尾厢	待终核: 1979-1991
Ford Crown Victoria	Ford	三厢车	Sedan	aero early	gen2 full-size Panther	1992	212.4	77.8	56.8	1992 Ford Crown Victoria LX	圆润Panther	待终核: 1992高度口径
Ford Crown Victoria	Ford	三厢车	Sedan	aero early	gen2 full-size Panther	1993-1997	212	77.8	56.8	1993/1994/1995/1996/1997 Ford Crown Victoria LX	圆润Panther	待终核: 1995
Ford Crown Victoria	Ford	三厢车	Sedan	aero facelift	gen2 full-size Panther	1998-2002	212	78.2	56.8	1998/1999/2000/2001/2002 Ford Crown Victoria LX	facelift宽度高点	待终核: 1998
Ford Crown Victoria	Ford	三厢车	Sedan	aero late	gen2 full-size Panther	2003-2005	212	78.2	56.8	2003/2004/2005 Ford Crown Victoria LX	后期Panther	待终核: 2003
Ford Crown Victoria	Ford	三厢车	Sedan	aero late	gen2 full-size Panther	2006-2008	212	78.3	58.3	2006/2008 Ford Crown Victoria	疑似高点口径，需确认民用/P71	待终核: 2007及口径
Ford Crown Victoria	Ford	三厢车	Sedan	aero late	gen2 full-size Panther	2009-2011	212	77.3	56.8	2010/2011 Ford Crown Victoria	后期Panther	待终核: 2009
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	1999-2002	185.4	71.6	55.5	1999/2000/2001/2002 Hyundai Sonata		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 facelift midsize sedan	2003-2005	186.9	71.7	56	2003/2004/2005 Hyundai Sonata	小改款后变长变高	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen4 midsize sedan	2006-2010	188.9	72.1	58	2006/2007/2008/2009/2010 Hyundai Sonata		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen5 midsize sedan	2011-2014	189.8	72.2	57.9	2011/2012/2014 Hyundai Sonata / Hybrid		待终核: 2013
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2015-2017	191.1	73.4	58.1	2015/2016/2017 Hyundai Sonata	普通版高点	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2018-2019	191.1	73.4	58.1	2015/2017/2019 Hyundai Sonata reference		待终核: 2018
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 midsize sedan	2020-2023	192.9	73.2	56.9	2020/2021/2022/2023 Hyundai Sonata Hybrid Limited		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 facelift midsize sedan	2024-2026	193.3	73.2	56.9	2024/2025/2026 Hyundai Sonata Hybrid / N Line		可入库
Chevrolet Bolt EUV	Chevrolet	越野车	SUV	EV	gen1 compact EV SUV	2022-2023	169.5	69.7	63.6	2022/2023 Chevrolet Bolt EUV	EV小型SUV	可入库

下一步


--- Round 6 / 下一步 ---
本轮重点清了 Santa Fe、Sonata、Crown Victoria 的待核。Santa Fe Sport 2014-2018 的高度应按 Edmunds 66.1，而不是之前阶段表里的 66.5；Sonata 2013、2018 已补齐，2011-2014 和 2018-2019 可入库；Crown Victoria 1995、1998、2003、2007 已补，1993-2002 可以推进，但 2007 Edmunds 同时存在普通 212 in 和 Commercial 218 in 长轴口径，所以 2006-2008 仍需保留“需确认是否纳入LWB商业版”。本轮仍基于当前上传文件批次处理。

粘贴的文本 (1)

 Edmunds 对 2014/2015/2016 Santa Fe Sport 均列出 184.6 × 74.0 × 66.1，2018 Santa Fe Sport 为 185.0 × 74.0 × 66.1。
Edmunds
+3
Edmunds
+3
Edmunds
+3
 Edmunds 对 2013 Sonata 列出 189.8 × 72.2 × 57.9，2018/2019 Sonata 列出 191.1 × 73.4 × 58.1。
Edmunds
+2
Edmunds
+2
 Edmunds 对 1995 Crown Victoria 为 212.0 × 77.8 × 56.8，1998 为 212.0 × 78.2 × 56.8，2003 为 212.0 × 78.2 × 56.8，2007 普通 LX 为 212.0 × 77.3 × 58.3，但 2007 Commercial Base 为 218.0 × 77.3 × 58.9。
Edmunds
+4
Edmunds
+4
Edmunds
+4

更新点

车型	操作/字段	描述
Hyundai Santa Fe	值修改 / 稳定	2014-2018 Sport 高度统一修正为 66.1；2014-2016 与 2017-2018 分段可入库
Hyundai Sonata	稳定	2013、2018 已补，2011-2014、2018-2019 推进为可入库
Ford Crown Victoria	稳定	1993-1997、1998-2002 普通 sedan 推进为可入库
Ford Crown Victoria	拆分风险	2007 Commercial LWB 为 218 in，和普通 212 in 差 6 in，需确认是否纳入本主车型
Lexus RX	保持	RX 已基本可入库，本轮不再改动
Mercury Marquis / Firebird	保留	仍有老车结构/年份待终核

阶段性 TSV：

tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	1999-2000	180.1	71.5	65.7	1999/2000 Lexus RX 300 SUV Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2001-2002	180.3	71.5	65.7	2001/2002 Lexus RX 300	2001-2002长度略长	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2003	180.1	71.5	65.7	2003 Lexus RX 300		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2004-2009	186.2	72.6	66.1	2004/2005/2006 Lexus RX 330; 2007/2008/2009 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2010	187.8	74.2	66.3	2010 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2011-2012	187.8	74.2	67.7	2011/2012 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2013-2014	187.8	74.2	66.7	2013/2014 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2015	187.8	74.2	66.3	2015 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen4 midsize SUV	2016-2022	192.5	74.6	67.7	2016/2017/2022 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 L midsize SUV	2018	196.9	74.6	67.7	2018 Lexus RX 350L Base		可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 L midsize SUV	2019-2022	196.9	74.6	67.3	2019/2020/2021/2022 Lexus RX 350L		可入库
Lexus RX	Lexus	越野车	SUV	inc: PHEV	gen5 midsize SUV	2023-2026	192.5	75.6	67.3	2023/2024/2025/2026 Lexus RX 350/RX 450h+		可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身	可入库
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen2 pony car	1970-1973	191.1	73.4	49.3	1970 Firebird	第二代早期	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Formula/Trans Am	gen2 pony car	1974-1981	196.8	73.2	49.6	1974-1981 Trans Am / Formula	保险杠增长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen3 pony car	1982-1988	191.8	72.4	50	1988 Firebird / Trans Am	低矮楔形	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen3 pony car	1989-1992	195.2	72.8	49.7	1990/1991 Firebird	末期造型更长	待终核: 1989/1992
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期	待终核: 1994-1997
Pontiac Firebird	Pontiac	跑车	Convertible	Std./Trans Am	gen4 pony car	1993-1997	197	74.5	51.7	1993 Firebird Trans Am	第四代早期	待终核: 1994-1997
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	1998/2000 Firebird / Trans Am	末期前脸	待终核: 1999/2001/2002
Pontiac Firebird	Pontiac	跑车	Convertible	Std./Trans Am	gen4 pony car	1998-2002	193.8	74.5	52	1998 Pontiac Firebird Convertible Trans Am / 2000 Firebird Convertible	末期前脸，敞篷高度略高	待终核: 1999/2001/2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2001	177.2	72.6	65.9	2001 Hyundai Santa Fe GL		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2002	177.2	72.6	65.9	2001/2003 Hyundai Santa Fe reference		待终核: 2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2003	177.2	72.6	65.9	2003 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2004-2006	177.2	72.7	66	2004/2005/2006 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen2 midsize SUV	2007-2012	184.1	74.4	67.9	2007/2008/2009/2010/2011/2012 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport/short	gen3 short midsize SUV	2013	184.6	74	66.5	2013 Hyundai Santa Fe Sport 2.0T	短轴Sport高点	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport/short	gen3 short midsize SUV	2014-2016	184.6	74	66.1	2014/2015/2016 Hyundai Santa Fe Sport	短轴Sport	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport/short	gen3 short midsize SUV	2017-2018	185	74	66.1	2017/2018 Hyundai Santa Fe Sport	短轴Sport facelift	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2013	193.1	74.2	66.5	2013 Hyundai Santa Fe GLS/Limited		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2014	193.1	74.2	66.9	2014 Hyundai Santa Fe Limited		待终核: 2014
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2015-2018	193.1	74.2	66.9	2015/2016/2017/2018 Hyundai Santa Fe Limited		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2019	193.1	74.2	66.9	2019 Hyundai Santa Fe XL		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen4 midsize SUV	2019-2023	188.4	74.4	66.3	2019-2023 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen5 midsize SUV	2024-2026	190.2	74.8	69.7	2024-2026 Hyundai Santa Fe Limited/Calligraphy		可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen1 Outback Sport wagon	2001	172.2	67.1	60	2001 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Hatchback	Std.	gen3 Outback Sport hatchback	2008-2011	173.8	68.5	58.3	2008-2011 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen5 midsize	1983-1986	196.5	71	53.8	1986 Mercury Marquis brochure / Mercury Marquis specs	中型四门	可入库
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen5 midsize	1983-1986	196.5	71	54.4	1986 Mercury Marquis brochure / Mercury Marquis specs	中型旅行车更高	可入库
Mercury Marquis	Mercury	三厢车	Coupe	2dr hardtop	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size	待终核: 1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size	待终核: sedan结构/1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低	待终核: sedan结构/1969-1971
Mercury Marquis	Mercury	三厢车	Coupe	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低	待终核: 1969-1971
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe	待终核: 1973/1974/1976/1978
Mercury Marquis	Mercury	三厢车	Coupe	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe	待终核: coupe结构/1973-1978
Mercury Marquis	Mercury	两厢车	Wagon	Colony Park	gen3 full-size	1973-1978	231	79.6	55	1975/1978 Mercury Marquis Colony Park Wagon	wagon超长	待终核: 1973/1974/1976/1977
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸	待终核: 1979-1982逐年
Mercury Marquis	Mercury	三厢车	Coupe	Std.	gen4 full-size	1979-1982	212.3	77.5	55.1	1979/1980/1982 Mercury Marquis/Grand Marquis 2-Door, Automobile-Catalog	Grand Marquis 2dr参考，Marquis coupe待交叉	待终核: 1981及Marquis口径
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸	待终核: 1979-1982逐年/wagon结构
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	1992	212.4	77.8	56.7	Ford Crown Victoria		缺参考年份车型明细
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	1993-1997	212	77.8	56.8	1993/1994/1995/1996/1997 Ford Crown Victoria	普通sedan	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	1998-2002	212	78.2	56.8	1998/1999/2000/2001/2002 Ford Crown Victoria	普通sedan	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	2003-2005	212	78.2	56.8	2003/2004/2005 Ford Crown Victoria	普通sedan	待终核: 2004/2005来源补齐
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	2006-2008	212	77.3	58.3	2006/2007/2008 Ford Crown Victoria LX	普通sedan；Commercial LWB另有218in风险	待终核: 是否纳入Commercial LWB
Ford Crown Victoria	Ford	三厢车	Sedan	Commercial LWB	gen2 Panther LWB	2007	218	77.3	58.9	2007 Ford Crown Victoria Commercial Base	LWB比普通长6in，建议单独处理	待终核: 是否保留LWB行
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	2009-2011	212	77.3	56.8	2010/2011 Ford Crown Victoria		待终核: 2009
Ford Crown Victoria	Ford	三厢车	Sedan	box	gen1 full-size Panther	1979-1991	212	78	56.8	Ford LTD Crown Victoria box Panther cross-ref	方正长尾厢	待终核: 1979-1991
Ford Crown Victoria	Ford	三厢车	Sedan	aero early	gen2 full-size Panther	1992	212.4	77.8	56.8	1992 Ford Crown Victoria LX	圆润Panther	待终核: 1992高度口径
Ford Crown Victoria	Ford	三厢车	Sedan	aero early	gen2 full-size Panther	1993-1997	212	77.8	56.8	1993/1994/1995/1996/1997 Ford Crown Victoria LX	圆润Panther	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	aero facelift	gen2 full-size Panther	1998-2002	212	78.2	56.8	1998/1999/2000/2001/2002 Ford Crown Victoria LX	facelift宽度高点	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	aero late	gen2 full-size Panther	2003-2005	212	78.2	56.8	2003/2004/2005 Ford Crown Victoria LX	后期Panther	待终核: 2004/2005来源补齐
Ford Crown Victoria	Ford	三厢车	Sedan	aero late	gen2 full-size Panther	2006-2008	212	77.3	58.3	2006/2007/2008 Ford Crown Victoria LX	Commercial LWB另有218in风险	待终核: 是否纳入Commercial LWB
Ford Crown Victoria	Ford	三厢车	Sedan	aero late	gen2 full-size Panther	2009-2011	212	77.3	56.8	2010/2011 Ford Crown Victoria	后期Panther	待终核: 2009
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	1999-2002	185.4	71.6	55.5	1999/2000/2001/2002 Hyundai Sonata		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 facelift midsize sedan	2003-2005	186.9	71.7	56	2003/2004/2005 Hyundai Sonata	小改款后变长变高	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen4 midsize sedan	2006-2010	188.9	72.1	58	2006/2007/2008/2009/2010 Hyundai Sonata		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen5 midsize sedan	2011-2014	189.8	72.2	57.9	2011/2012/2013/2014 Hyundai Sonata / Hybrid		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2015-2017	191.1	73.4	58.1	2015/2016/2017 Hyundai Sonata	普通版高点	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2018-2019	191.1	73.4	58.1	2018/2019 Hyundai Sonata	普通版高点	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 midsize sedan	2020-2023	192.9	73.2	56.9	2020/2021/2022/2023 Hyundai Sonata Hybrid Limited		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 facelift midsize sedan	2024-2026	193.3	73.2	56.9	2024/2025/2026 Hyundai Sonata Hybrid / N Line		可入库
Chevrolet Bolt EUV	Chevrolet	越野车	SUV	EV	gen1 compact EV SUV	2022-2023	169.5	69.7	63.6	2022/2023 Chevrolet Bolt EUV	EV小型SUV	可入库

下一步


--- Round 7 / 下一步 ---
本轮主要补强 Firebird 和 Mercury Marquis，并修正 Crown Victoria 的 LWB 风险口径。关键变化：1990 Firebird 不能继续和 1991/1992 合并，Edmunds 显示 1990 为 188.1 × 72.4 × 50.0，而 1991/1992 为约 195.1/195.2 × 72.4 × 49.7；1994 Firebird 为 197.0 × 74.5 × 51.7，而 1995/1996 为 195.6 × 74.5 × 52.7，所以 gen4 早期也必须拆开。
Edmunds
+5
Edmunds
+5
Edmunds
+5

Mercury Marquis 1973 wagon 来源显示 223.4 × 79.6，不能沿用之前 231 的 wagon 超长值；1982 Marquis wagon 来源显示 218 × 79.3 × 57.2，说明 1979-1982 wagon 也不能继续和 sedan/coupe 共用 220.4 × 78.1 × 55。
automobile-catalog.com
+1
 本轮仍只处理当前上传文件批次。

粘贴的文本 (1)

更新点

车型	操作/字段	描述
Pontiac Firebird	拆出 / 值修改	gen3 1989-1992 拆为 1989待核、1990、1991、1992，不再错误合并
Pontiac Firebird	拆出 / 值修改	gen4 1993-1997 拆为 1993待核、1994、1995-1996、1997待核
Mercury Marquis	值修改	1973-1978 wagon 先按 1973/1975/1978 已核数据保留待终核，不再直接用 231 全段
Mercury Marquis	拆出	1979-1982 wagon 与 sedan/coupe 拆开，1982 wagon 高度 57.2 明显不同
Ford Crown Victoria	保留风险	Commercial LWB 218 in 与普通 212 in 差 6 in，继续单独保留待确认

阶段性 TSV：

tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	1999-2000	180.1	71.5	65.7	1999/2000 Lexus RX 300 SUV Base		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2001-2002	180.3	71.5	65.7	2001/2002 Lexus RX 300	2001-2002长度略长	可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen1 compact SUV	2003	180.1	71.5	65.7	2003 Lexus RX 300		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen2 midsize SUV	2004-2009	186.2	72.6	66.1	2004/2005/2006 Lexus RX 330; 2007/2008/2009 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2010	187.8	74.2	66.3	2010 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2011-2012	187.8	74.2	67.7	2011/2012 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2013-2014	187.8	74.2	66.7	2013/2014 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen3 midsize SUV	2015	187.8	74.2	66.3	2015 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	Std.	gen4 midsize SUV	2016-2022	192.5	74.6	67.7	2016/2017/2022 Lexus RX 350		可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 L midsize SUV	2018	196.9	74.6	67.7	2018 Lexus RX 350L Base		可入库
Lexus RX	Lexus	越野车	SUV	L	gen4 L midsize SUV	2019-2022	196.9	74.6	67.3	2019/2020/2021/2022 Lexus RX 350L		可入库
Lexus RX	Lexus	越野车	SUV	inc: PHEV	gen5 midsize SUV	2023-2026	192.5	75.6	67.3	2023/2024/2025/2026 Lexus RX 350/RX 450h+		可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身	可入库
Pontiac Firebird	Pontiac	跑车	Convertible	Std.	gen1 pony car	1967-1969	188.8	72.6	51.5	1967 Firebird	F-body低车身	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen2 pony car	1970-1973	191.1	73.4	49.3	1970 Firebird	第二代早期	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Formula/Trans Am	gen2 pony car	1974-1981	196.8	73.2	49.6	1974-1981 Trans Am / Formula	保险杠增长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen3 pony car	1982-1988	191.8	72.4	50	1988 Firebird / Trans Am	低矮楔形	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen3 pony car	1989	195.2	72.4	49.7	1990/1991/1992 Firebird reference	末期造型更长	待终核: 1989
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen3 pony car	1990	188.1	72.4	50	1990 Pontiac Firebird	低矮楔形	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen3 pony car	1991	195.1	72.4	49.7	1991 Pontiac Firebird Base	末期造型更长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std.	gen3 pony car	1992	195.2	72.4	49.7	1992 Pontiac Firebird	末期造型更长	可入库
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen4 pony car	1993	197	74.5	51.7	1993 Firebird Trans Am	第四代早期	待终核: 1993
Pontiac Firebird	Pontiac	跑车	Convertible	Std./Trans Am	gen4 pony car	1993	197	74.5	51.7	1993 Firebird Trans Am	第四代早期	待终核: 1993 convertible
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen4 pony car	1994	197	74.5	51.7	1994 Pontiac Firebird Trans Am GT	第四代早期	可入库
Pontiac Firebird	Pontiac	跑车	Convertible	Std./Trans Am	gen4 pony car	1994	197	74.5	51.7	1994 Pontiac Firebird reference	第四代早期敞篷	待终核: 1994 convertible
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen4 pony car	1995-1996	195.6	74.5	52.7	1995/1996 Pontiac Firebird	第四代中期高点	可入库
Pontiac Firebird	Pontiac	跑车	Convertible	Std./Trans Am	gen4 pony car	1995-1996	195.6	74.5	52.7	1995/1996 Pontiac Firebird reference	敞篷待交叉	待终核: convertible结构
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen4 pony car	1997	195.6	74.5	52.7	1995/1996 Pontiac Firebird reference	第四代中期高点	待终核: 1997
Pontiac Firebird	Pontiac	跑车	Convertible	Std./Trans Am	gen4 pony car	1997	195.6	74.5	52.7	1995/1996 Pontiac Firebird reference	敞篷待交叉	待终核: 1997 convertible
Pontiac Firebird	Pontiac	跑车	Coupe	Std./Trans Am	gen4 pony car	1998-2002	193.7	74.4	51.8	1998/2000 Firebird / Trans Am	末期前脸	待终核: 1999/2001/2002
Pontiac Firebird	Pontiac	跑车	Convertible	Std./Trans Am	gen4 pony car	1998-2002	193.8	74.5	52	1998 Pontiac Firebird Convertible Trans Am / 2000 Firebird Convertible	末期前脸，敞篷高度略高	待终核: 1999/2001/2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2001	177.2	72.6	65.9	2001 Hyundai Santa Fe GL		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2002	177.2	72.6	65.9	2001/2003 Hyundai Santa Fe reference		待终核: 2002
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2003	177.2	72.6	65.9	2003 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen1 compact SUV	2004-2006	177.2	72.7	66	2004/2005/2006 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen2 midsize SUV	2007-2012	184.1	74.4	67.9	2007/2008/2009/2010/2011/2012 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport/short	gen3 short midsize SUV	2013	184.6	74	66.5	2013 Hyundai Santa Fe Sport 2.0T	短轴Sport高点	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport/short	gen3 short midsize SUV	2014-2016	184.6	74	66.1	2014/2015/2016 Hyundai Santa Fe Sport	短轴Sport	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Sport/short	gen3 short midsize SUV	2017-2018	185	74	66.1	2017/2018 Hyundai Santa Fe Sport	短轴Sport facelift	可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2013	193.1	74.2	66.5	2013 Hyundai Santa Fe GLS/Limited		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2014	193.1	74.2	66.9	2014 Hyundai Santa Fe Limited		待终核: 2014
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2015-2018	193.1	74.2	66.9	2015/2016/2017/2018 Hyundai Santa Fe Limited		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	XL/long	gen3 long midsize SUV	2019	193.1	74.2	66.9	2019 Hyundai Santa Fe XL		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen4 midsize SUV	2019-2023	188.4	74.4	66.3	2019-2023 Hyundai Santa Fe		可入库
Hyundai Santa Fe	Hyundai	越野车	SUV	Std.	gen5 midsize SUV	2024-2026	190.2	74.8	69.7	2024-2026 Hyundai Santa Fe Limited/Calligraphy		可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen1 Outback Sport wagon	2001	172.2	67.1	60	2001 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2002-2003	173.4	67.3	60.2	2002/2003 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2004	173.4	66.7	57.7	2004 Subaru Impreza Outback Sport/Wagon, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2005	173.8	67.3	58.9	2005 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2006	175.4	66.7	58.9	2006 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Wagon	Std.	gen2 Outback Sport wagon	2007	175.8	67.3	60.6	2007 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Subaru Outback Sp	Subaru	两厢车	Hatchback	Std.	gen3 Outback Sport hatchback	2008-2011	173.8	68.5	58.3	2008-2011 Subaru Impreza Outback Sport, Edmunds	Outback Sport参考口径	可入库
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen5 midsize	1983-1986	196.5	71	53.8	1986 Mercury Marquis brochure / Mercury Marquis specs	中型四门	可入库
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen5 midsize	1983-1986	196.5	71	54.4	1986 Mercury Marquis brochure / Mercury Marquis specs	中型旅行车更高	可入库
Mercury Marquis	Mercury	三厢车	Coupe	2dr hardtop	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size	待终核: 1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen1 full-size	1967-1968	218.5	77.9	55.1	1967 Mercury Marquis 2-Door Hardtop	早期full-size	待终核: sedan结构/1968
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低	待终核: sedan结构/1969-1971
Mercury Marquis	Mercury	三厢车	Coupe	Std.	gen2 full-size	1969-1972	224.8	79.3	53.1	1972 Mercury Marquis Brougham 2-Door Hardtop	更长更低	待终核: 1969-1971
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe	待终核: 1973/1974/1976/1978
Mercury Marquis	Mercury	三厢车	Coupe	Std.	gen3 full-size	1973-1978	229	79.6	54.7	1975/1977 Mercury Marquis Brougham Sedan	full-size sedan/coupe	待终核: coupe结构/1973-1978
Mercury Marquis	Mercury	两厢车	Wagon	Colony Park	gen3 full-size	1973	223.4	79.6	55	1973 Mercury Marquis Station Wagon	早期wagon参考	可入库
Mercury Marquis	Mercury	两厢车	Wagon	Colony Park	gen3 full-size	1974-1978	231	79.6	55	1975/1978 Mercury Marquis Colony Park Wagon	wagon超长	待终核: 1974/1976/1977
Mercury Marquis	Mercury	三厢车	Sedan	Std.	gen4 full-size	1979-1982	220.4	78.1	55	1979-1982 Mercury Marquis reference	downsized全尺寸	待终核: 1979-1982逐年
Mercury Marquis	Mercury	三厢车	Coupe	Std.	gen4 full-size	1979-1982	212.3	77.5	55.1	1979/1980/1982 Mercury Marquis/Grand Marquis 2-Door, Automobile-Catalog	Grand Marquis 2dr参考，Marquis coupe待交叉	待终核: 1981及Marquis口径
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen4 full-size	1979-1981	218	79.3	57.2	1982 Mercury Marquis Station Wagon reference	downsized wagon待逐年	待终核: 1979-1981 wagon
Mercury Marquis	Mercury	两厢车	Wagon	Std.	gen4 full-size	1982	218	79.3	57.2	1982 Mercury Marquis Station Wagon 5.0L V8	downsized wagon更高	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	1992	212.4	77.8	56.7	Ford Crown Victoria		缺参考年份车型明细
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	1993-1997	212	77.8	56.8	1993/1994/1995/1996/1997 Ford Crown Victoria	普通sedan	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	1998-2002	212	78.2	56.8	1998/1999/2000/2001/2002 Ford Crown Victoria	普通sedan	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	2003-2005	212	78.2	56.8	2003/2004/2005 Ford Crown Victoria	普通sedan	待终核: 2004/2005来源补齐
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	2006-2008	212	77.3	58.3	2006/2007/2008 Ford Crown Victoria LX	普通sedan；Commercial LWB另有218in风险	待终核: 是否纳入Commercial LWB
Ford Crown Victoria	Ford	三厢车	Sedan	Commercial LWB	gen2 Panther LWB	2007	218	77.3	58.9	2007 Ford Crown Victoria Commercial Base	LWB比普通长6in，建议单独处理	待终核: 是否保留LWB行
Ford Crown Victoria	Ford	三厢车	Sedan	Std.	gen2 Panther	2009-2011	212	77.3	56.8	2010/2011 Ford Crown Victoria		待终核: 2009
Ford Crown Victoria	Ford	三厢车	Sedan	box	gen1 full-size Panther	1979-1991	212	78	56.8	Ford LTD Crown Victoria box Panther cross-ref	方正长尾厢	待终核: 1979-1991
Ford Crown Victoria	Ford	三厢车	Sedan	aero early	gen2 full-size Panther	1992	212.4	77.8	56.8	1992 Ford Crown Victoria LX	圆润Panther	待终核: 1992高度口径
Ford Crown Victoria	Ford	三厢车	Sedan	aero early	gen2 full-size Panther	1993-1997	212	77.8	56.8	1993/1994/1995/1996/1997 Ford Crown Victoria LX	圆润Panther	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	aero facelift	gen2 full-size Panther	1998-2002	212	78.2	56.8	1998/1999/2000/2001/2002 Ford Crown Victoria LX	facelift宽度高点	可入库
Ford Crown Victoria	Ford	三厢车	Sedan	aero late	gen2 full-size Panther	2003-2005	212	78.2	56.8	2003/2004/2005 Ford Crown Victoria LX	后期Panther	待终核: 2004/2005来源补齐
Ford Crown Victoria	Ford	三厢车	Sedan	aero late	gen2 full-size Panther	2006-2008	212	77.3	58.3	2006/2007/2008 Ford Crown Victoria LX	Commercial LWB另有218in风险	待终核: 是否纳入Commercial LWB
Ford Crown Victoria	Ford	三厢车	Sedan	aero late	gen2 full-size Panther	2009-2011	212	77.3	56.8	2010/2011 Ford Crown Victoria	后期Panther	待终核: 2009
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 midsize sedan	1999-2002	185.4	71.6	55.5	1999/2000/2001/2002 Hyundai Sonata		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen3 facelift midsize sedan	2003-2005	186.9	71.7	56	2003/2004/2005 Hyundai Sonata	小改款后变长变高	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	Std.	gen4 midsize sedan	2006-2010	188.9	72.1	58	2006/2007/2008/2009/2010 Hyundai Sonata		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen5 midsize sedan	2011-2014	189.8	72.2	57.9	2011/2012/2013/2014 Hyundai Sonata / Hybrid		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2015-2017	191.1	73.4	58.1	2015/2016/2017 Hyundai Sonata	普通版高点	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid	gen6 midsize sedan	2018-2019	191.1	73.4	58.1	2018/2019 Hyundai Sonata	普通版高点	可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 midsize sedan	2020-2023	192.9	73.2	56.9	2020/2021/2022/2023 Hyundai Sonata Hybrid Limited		可入库
Hyundai Sonata	Hyundai	三厢车	Sedan	inc: hybrid/N Line	gen7 facelift midsize sedan	2024-2026	193.3	73.2	56.9	2024/2025/2026 Hyundai Sonata Hybrid / N Line		可入库
Chevrolet Bolt EUV	Chevrolet	越野车	SUV	EV	gen1 compact EV SUV	2022-2023	169.5	69.7	63.6	2022/2023 Chevrolet Bolt EUV	EV小型SUV	可入库

下一步


--- 脚本异常 ---
异常: Requested Clipboard operation did not succeed.

