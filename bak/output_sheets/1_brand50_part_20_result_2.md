# 文件名：1_brand50_part_20.tsv


--- Round 1 / 首次发送 ---
已读取文件内容。按本批次状态判断：

普通车型记录均仍为旧格式（普通 / sedan mid / hch 等），尚未转换到你当前要求的最新全量表结构。

Chevrolet K5 Blazer 存在 待终核: 1970-1972 记录。

因此当前批次不能标记为“本批次完成”，也不能直接判定全部可出库。

粘贴的文本 (1)

本批次下一步应进行：

车型	操作
Lexus ES	转换至最新全量表结构并拆分字段
Chrysler Pacifica	转换至最新全量表结构并区分 crossover / minivan
Nissan Altima	coupe 与 sedan 分离重构
Hyundai Accent	sdn/hch 拆为单一结构
Volkswagen Golf	hatchback / wagon 独立结构化
Toyota Solara	coupe / convertible 分离核对
Rivian R1S	转换最新字段
Chevrolet K5 Blazer	补强 1970-1972 后再判断可入库

当前批次状态：

状态	数量
🟢 可直接继承尺寸数据	6个车型
🟡 需结构化重构	7个车型
🟡 待终核记录	Chevrolet K5 Blazer 1970-1972
🔴 全部可出库	否

下一步可继续输出本批次最新格式完整全量表（结构化重构版）。


--- Round 2 / 下一步 ---
tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Lexus ES	Lexus	三厢车	Sedan	Std.	gen1 compact	1991	183.1	66.9	53.1	1991 Lexus ES 250 Sedan		可入库
Lexus ES	Lexus	三厢车	Sedan	Std.	gen3 midsize	1997-2001	190.2	70.5	54.9	1997 Lexus ES 300		可入库
Lexus ES	Lexus	三厢车	Sedan	Std.	gen4 midsize	2002-2006	191.1	71.7	56.3	2002 Lexus ES 300		可入库
Lexus ES	Lexus	三厢车	Sedan	Std.	gen5 midsize	2007-2012	191.1	71.7	57.1	2007 Lexus ES 350		可入库
Lexus ES	Lexus	三厢车	Sedan	hybrid	gen6 large	2013-2018	192.7	71.1	57.1	2015 Lexus ES 300h		可入库
Lexus ES	Lexus	三厢车	Sedan	Std.	gen7 large	2019-2025	195.9	73.4	57.1	2024 Lexus ES 250 F SPORT Design		可入库
Lexus ES	Lexus	三厢车	Sedan	EV/hybrid	gen8 large	2026	202.4	75.6	61.4	2026 Lexus ES 350e / ES 500e	EV/hybrid高车身	可入库
Chrysler Pacifica	Chrysler	越野车	Minivan	inc: PHEV	gen2 minivan	2017	203.8	79.6	69.9	2017 Chrysler Pacifica / Pacifica Hybrid		可入库
Chrysler Pacifica	Chrysler	越野车	Minivan	inc: PHEV	gen2 minivan	2018-2020	203.8	79.6	69.9	Chrysler Pacifica / Pacifica Hybrid		可入库
Chrysler Pacifica	Chrysler	越野车	Minivan	inc: PHEV	gen2 minivan facelift	2021-2026	204.3	79.6	69.9	2026 Chrysler Pacifica / Plug-in Hybrid		可入库
Chrysler Pacifica	Chrysler	越野车	CUV	Std.	gen1 crossover	2004-2008	198.9	79.3	66.5	2004-2008 Chrysler Pacifica		可入库
Chrysler Pacifica	Chrysler	越野车	Minivan	Std.	gen2 minivan	2017-2020	203.8	79.6	69.9	2017-2020 Chrysler Pacifica		可入库
Chrysler Pacifica	Chrysler	越野车	Minivan	inc: PHEV	gen2 minivan facelift	2021-2023	204.3	79.6	69.9	2021-2023 Chrysler Pacifica / Hybrid		可入库
Chrysler Pacifica	Chrysler	越野车	Minivan	inc: PHEV	gen2 minivan facelift	2024-2026	204.3	79.6	70.7	2024-2026 Chrysler Pacifica Select		可入库
Nissan Altima	Nissan	三厢车	Sedan	Std.	gen1 compact	1993-1997	180.5	67.1	55.9	1993 Nissan Altima SE / GXE		可入库
Nissan Altima	Nissan	三厢车	Sedan	Std.	gen2 compact	1998-2001	185.8	69.1	56.1	1998-2001 Nissan Altima sedan		可入库
Nissan Altima	Nissan	三厢车	Sedan	Std.	gen3 large	2002-2006	191.5	70.4	57.9	2002 Nissan Altima 3.5 SE / 2.5 SL		可入库
Nissan Altima	Nissan	三厢车	Sedan	Std.	gen4 large	2007-2012	190.7	70.7	58.3	2007-2012 Nissan Altima sedan		可入库
Nissan Altima	Nissan	跑车	Coupe	Std.	gen4 coupe	2008-2013	182.5	70.7	55.9	Nissan Altima Coupe	低车顶Coupe	可入库
Nissan Altima	Nissan	三厢车	Sedan	Std.	gen5 large	2013-2018	191.5	72	57.9	2013 Nissan Altima sedan		可入库
Nissan Altima	Nissan	三厢车	Sedan	Std.	gen6 large	2019-2026	192.9	72.9	57.4	2019-2026 Nissan Altima sedan		可入库
Hyundai Accent	Hyundai	三厢车	Sedan	Std.	gen1 compact	1995-1999	162.1	63.8	54.9	1995 Hyundai Accent Sedan / Hatchback	原sdn/hch拆分	待终核: Sedan结构
Hyundai Accent	Hyundai	两厢车	Hatchback	Std.	gen1 compact	1995-1999	162.1	63.8	54.9	1995 Hyundai Accent Sedan / Hatchback	原sdn/hch拆分	待终核: Hatchback结构
Hyundai Accent	Hyundai	三厢车	Sedan	Std.	gen2 compact	2000-2005	166.7	65.7	54.9	2000 Hyundai Accent Hatchback	原sdn/hch拆分	待终核: Sedan结构
Hyundai Accent	Hyundai	两厢车	Hatchback	Std.	gen2 compact	2000-2005	166.7	65.7	54.9	2000 Hyundai Accent Hatchback	原sdn/hch拆分	待终核: Hatchback结构
Hyundai Accent	Hyundai	三厢车	Sedan	Std.	gen3 compact	2006-2011	168.5	66.7	57.9	2011 Hyundai Accent Sedan GLS		可入库
Hyundai Accent	Hyundai	两厢车	Hatchback	Std.	gen3 compact	2006-2011	159.3	66.7	57.9	2011 Hyundai Accent SE Hatchback		可入库
Hyundai Accent	Hyundai	三厢车	Sedan	Std.	gen4 compact	2012-2017	172	66.9	57.1	2012 Hyundai Accent GLS Sedan		可入库
Hyundai Accent	Hyundai	两厢车	Hatchback	Std.	gen4 compact	2012-2017	162	66.9	57.1	2012 / 2016 Hyundai Accent Hatchback		可入库
Hyundai Accent	Hyundai	三厢车	Sedan	Std.	gen5 compact	2018-2022	172.6	68.1	57.1	2022 Hyundai Accent Limited / SE		可入库
Volkswagen Golf	Volkswagen	两厢车	Hatchback	Std.	gen4 hatchback	1999	160.4	66.7	56.2	1999 Volkswagen Golf GL Specs & Features	early body	可入库
Volkswagen Golf	Volkswagen	两厢车	Hatchback	Std.	gen4 hatchback	1999-2006	164.9	68.3	56.7	2006 Volkswagen Golf Hatchback Specs & Features		可入库
Volkswagen Golf	Volkswagen	两厢车	Hatchback	Std.	gen6 hatchback	2010-2014	165.4	70.3	58.3	2010 Volkswagen Golf Specs & Features		可入库
Volkswagen Golf	Volkswagen	两厢车	Hatchback	inc: GTI	gen7 hatchback	2015-2021	168	70.8	58.2	2021 Volkswagen Golf Specs & Features		可入库
Volkswagen Golf	Volkswagen	两厢车	Hatchback	inc: GTI/R	gen8 hatchback	2022-2026	169.1	70.4	57.8	2025 Volkswagen Golf R Specs & Features		可入库
Volkswagen Golf	Volkswagen	两厢车	Wagon	inc: SportWagen	gen7 wagon	2015-2017	179.6	70.8	58.3	2015 Volkswagen Golf SportWagen TDI S Specs & Features	长车身Wagon	可入库
Volkswagen Golf	Volkswagen	两厢车	Wagon	inc: Alltrack	gen7 wagon	2017-2019	179.6	70.8	59.7	2018 Volkswagen Golf Alltrack Specs & Features	高车身Alltrack	可入库
Chevrolet K5 Blazer	Chevrolet	越野车	SUV	Std.	gen1 full-size SUV	1969	177	79	70	1969 Chevrolet Blazer brochure / period specs	初代短轴	可入库
Chevrolet K5 Blazer	Chevrolet	越野车	SUV	Std.	gen2 square-body full-size SUV	1973	184.5	79.5	69	1973 Chevrolet Blazer brochure	square body起点	可入库
Chevrolet K5 Blazer	Chevrolet	越野车	SUV	Std.	gen2 square-body full-size SUV	1974	184.5	79.1	71.5	1974 Chevrolet Blazer brochure	2WD/4WD高度差	可入库
Chevrolet K5 Blazer	Chevrolet	越野车	SUV	Std.	gen3 GMT400 full-size SUV	1994	187.7	76.4	71	1994 Chevrolet Blazer, Edmunds	固定车顶	可入库
Chevrolet K5 Blazer	Chevrolet	越野车	SUV	Std.	gen1 full-size SUV	1970-1972	177	79	70	1969 Blazer proxy	初代待核	待终核: 1970-1972
Chevrolet K5 Blazer	Chevrolet	越野车	SUV	Std.	gen2 square-body full-size SUV	1975-1991	184.8	79.6	73.8	1990/1991 Chevrolet Blazer Edmunds	原77.8不采用	可入库
Chevrolet K5 Blazer	Chevrolet	越野车	SUV	Std.	gen3 GMT400 full-size SUV	1992-1994	187.8	76.4	71	1992/1994 Chevrolet Blazer Tahoe GMT400	GMT400过渡	可入库
Toyota Solara	Toyota	跑车	Coupe	Std.	gen1 coupe/convertible	1999-2001	190	71.1	55.1	1999/2000/2001 Toyota Camry Solara, Edmunds / C&D	原cou/conv拆分	待终核: Coupe结构
Toyota Solara	Toyota	跑车	Convertible	Std.	gen1 coupe/convertible	1999-2001	190	71.1	55.1	1999/2000/2001 Toyota Camry Solara, Edmunds / C&D	原cou/conv拆分	待终核: Convertible结构
Toyota Solara	Toyota	跑车	Coupe	Std.	gen1 coupe/convertible	2002	191.5	71.1	55.1	2002 Toyota Camry Solara SE, Edmunds / CarSpecs	原cou/conv拆分	待终核: Coupe结构
Toyota Solara	Toyota	跑车	Convertible	Std.	gen1 coupe/convertible	2002	191.5	71.1	55.1	2002 Toyota Camry Solara SE, Edmunds / CarSpecs	原cou/conv拆分	待终核: Convertible结构
Toyota Solara	Toyota	跑车	Coupe	Std.	gen1 coupe/convertible	2003	191.5	71.1	55.5	2003 Toyota Camry Solara SLE Convertible, Edmunds / CarSpecs	原cou/conv拆分	待终核: Coupe结构
Toyota Solara	Toyota	跑车	Convertible	Std.	gen1 coupe/convertible	2003	191.5	71.1	55.5	2003 Toyota Camry Solara SLE Convertible, Edmunds / CarSpecs	原cou/conv拆分	待终核: Convertible结构
Toyota Solara	Toyota	跑车	Coupe	Std.	gen2 coupe/convertible	2004-2005	192.6	71.5	56.1	2004/2005 Toyota Camry Solara, Edmunds / CarSpecs	原cou/conv拆分	待终核: Coupe结构
Toyota Solara	Toyota	跑车	Convertible	Std.	gen2 coupe/convertible	2004-2005	192.6	71.5	56.1	2004/2005 Toyota Camry Solara, Edmunds / CarSpecs	原cou/conv拆分	待终核: Convertible结构
Toyota Solara	Toyota	跑车	Coupe	Std.	gen2 coupe/convertible	2006	192.5	71.5	56.5	2006 Toyota Camry Solara Convertible, Edmunds trims	原cou/conv拆分	待终核: Coupe结构
Toyota Solara	Toyota	跑车	Convertible	Std.	gen2 coupe/convertible	2006	192.5	71.5	56.5	2006 Toyota Camry Solara Convertible, Edmunds trims	原cou/conv拆分	待终核: Convertible结构
Toyota Solara	Toyota	跑车	Coupe	Std.	gen2 coupe/convertible	2007	192.5	71.5	56.1	2007 Toyota Camry Solara, Edmunds / CarSpecs	原cou/conv拆分	待终核: Coupe结构
Toyota Solara	Toyota	跑车	Convertible	Std.	gen2 coupe/convertible	2007	192.5	71.5	56.1	2007 Toyota Camry Solara, Edmunds / CarSpecs	原cou/conv拆分	待终核: Convertible结构
Toyota Solara	Toyota	跑车	Coupe	Std.	gen2 coupe/convertible	2008	192.5	71.5	56.5	2008 Toyota Camry Solara Convertible, Edmunds / JD Power / Toyota Canada spec	原cou/conv拆分	待终核: Coupe结构
Toyota Solara	Toyota	跑车	Convertible	Std.	gen2 coupe/convertible	2008	192.5	71.5	56.5	2008 Toyota Camry Solara Convertible, Edmunds / JD Power / Toyota Canada spec	原cou/conv拆分	待终核: Convertible结构
Rivian R1S	Rivian	越野车	SUV	EV	gen1 electric SUV	2022-2026	200.8	82	77.3	Rivian R1S	高车身EV SUV	可入库

仍有待终核：Chevrolet K5 Blazer 1970-1972、Hyundai Accent 1995-2005 分结构、Toyota Solara Coupe/Convertible 分结构。下一步优先补这三块。


--- Round 3 / 下一步 ---
补强依据：K5 Blazer 1971/1972 尺寸显示为 180 in 长、79 in 宽，高度按 4WD/硬顶最大取 72.8；Hyundai Accent 1995/2000 Sedan 与 Hatchback 三维基本一致；Solara 2002 起 Coupe/Convertible 高度不同，已拆分。
Edmunds
+5
汽车目录
+5
汽车目录
+5

tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Chevrolet K5 Blazer	Chevrolet	越野车	SUV	Std.	gen1 full-size SUV	1969-1970	177.5	79	70	1969 brochure / 1970 Automobile-Catalog	初代短轴	可入库
Chevrolet K5 Blazer	Chevrolet	越野车	SUV	Std.	gen1 full-size SUV	1971-1972	180	79	72.8	1971/1972 Chevrolet Blazer specs	初代后期较高	可入库
Hyundai Accent	Hyundai	三厢车	Sedan	Std.	gen1 compact	1995-1999	162.1	63.8	54.9	1995 Hyundai Accent Sedan, Edmunds		可入库
Hyundai Accent	Hyundai	两厢车	Hatchback	Std.	gen1 compact	1995-1999	162.1	63.8	54.9	1995 Hyundai Accent Hatchback, Edmunds / Carspecs		可入库
Hyundai Accent	Hyundai	三厢车	Sedan	Std.	gen2 compact	2000-2005	166.7	65.7	54.9	2000 Hyundai Accent Sedan, Carspecs		可入库
Hyundai Accent	Hyundai	两厢车	Hatchback	Std.	gen2 compact	2000-2005	166.7	65.7	54.9	2000 Hyundai Accent Hatchback, Edmunds		可入库
Toyota Solara	Toyota	跑车	Coupe	Std.	gen1 coupe	1999-2001	190	71.1	55.1	1999 Toyota Camry Solara Coupe, Edmunds		可入库
Toyota Solara	Toyota	跑车	Convertible	Std.	gen1 convertible	2000-2001	190	71.1	55.1	2000-2001 Toyota Camry Solara Convertible	软顶	可入库
Toyota Solara	Toyota	跑车	Coupe	Std.	gen1 coupe	2002-2003	191.5	71.1	54.3	2002-2003 Toyota Camry Solara Coupe, Cars.com	低车顶Coupe	可入库
Toyota Solara	Toyota	跑车	Convertible	Std.	gen1 convertible	2002-2003	191.5	71.1	55.5	2002-2003 Toyota Camry Solara Convertible, Cars.com / AutoDetective	软顶较高	可入库
Toyota Solara	Toyota	跑车	Coupe	Std.	gen2 coupe	2004-2008	192.5	71.5	56.1	2004-2008 Toyota Camry Solara Coupe		可入库
Toyota Solara	Toyota	跑车	Convertible	Std.	gen2 convertible	2004-2008	192.5	71.5	56.5	2008 Toyota Camry Solara Convertible, Edmunds	软顶较高	可入库

剩余待终核已清掉；下一步可出完整全量表并给“所有可出库批次”。


--- Round 4 / 下一步 ---
完整全量表如下：

粘贴的文本 (1)

tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Lexus ES	Lexus	三厢车	Sedan	Std.	gen1 compact	1991	183.1	66.9	53.1	1991 Lexus ES 250 Sedan		可入库
Lexus ES	Lexus	三厢车	Sedan	Std.	gen3 midsize	1997-2001	190.2	70.5	54.9	1997 Lexus ES 300		可入库
Lexus ES	Lexus	三厢车	Sedan	Std.	gen4 midsize	2002-2006	191.1	71.7	56.3	2002 Lexus ES 300		可入库
Lexus ES	Lexus	三厢车	Sedan	Std.	gen5 midsize	2007-2012	191.1	71.7	57.1	2007 Lexus ES 350		可入库
Lexus ES	Lexus	三厢车	Sedan	hybrid	gen6 large	2013-2018	192.7	71.1	57.1	2015 Lexus ES 300h		可入库
Lexus ES	Lexus	三厢车	Sedan	Std.	gen7 large	2019-2025	195.9	73.4	57.1	2024 Lexus ES 250 F SPORT Design		可入库
Lexus ES	Lexus	三厢车	Sedan	EV/hybrid	gen8 large	2026	202.4	75.6	61.4	2026 Lexus ES 350e / ES 500e	EV/hybrid高车身	可入库
Chrysler Pacifica	Chrysler	越野车	Minivan	inc: PHEV	gen2 minivan	2017	203.8	79.6	69.9	2017 Chrysler Pacifica / Pacifica Hybrid		可入库
Chrysler Pacifica	Chrysler	越野车	Minivan	inc: PHEV	gen2 minivan	2018-2020	203.8	79.6	69.9	Chrysler Pacifica / Pacifica Hybrid		可入库
Chrysler Pacifica	Chrysler	越野车	Minivan	inc: PHEV	gen2 minivan facelift	2021-2026	204.3	79.6	69.9	2026 Chrysler Pacifica / Plug-in Hybrid		可入库
Chrysler Pacifica	Chrysler	越野车	CUV	Std.	gen1 crossover	2004-2008	198.9	79.3	66.5	2004-2008 Chrysler Pacifica		可入库
Chrysler Pacifica	Chrysler	越野车	Minivan	Std.	gen2 minivan	2017-2020	203.8	79.6	69.9	2017-2020 Chrysler Pacifica		可入库
Chrysler Pacifica	Chrysler	越野车	Minivan	inc: PHEV	gen2 minivan facelift	2021-2023	204.3	79.6	69.9	2021-2023 Chrysler Pacifica / Hybrid		可入库
Chrysler Pacifica	Chrysler	越野车	Minivan	inc: PHEV	gen2 minivan facelift	2024-2026	204.3	79.6	70.7	2024-2026 Chrysler Pacifica Select		可入库
Nissan Altima	Nissan	三厢车	Sedan	Std.	gen1 compact	1993-1997	180.5	67.1	55.9	1993 Nissan Altima SE / GXE		可入库
Nissan Altima	Nissan	三厢车	Sedan	Std.	gen2 compact	1998-2001	185.8	69.1	56.1	1998-2001 Nissan Altima sedan		可入库
Nissan Altima	Nissan	三厢车	Sedan	Std.	gen3 large	2002-2006	191.5	70.4	57.9	2002 Nissan Altima 3.5 SE / 2.5 SL		可入库
Nissan Altima	Nissan	三厢车	Sedan	Std.	gen4 large	2007-2012	190.7	70.7	58.3	2007-2012 Nissan Altima sedan		可入库
Nissan Altima	Nissan	跑车	Coupe	Std.	gen4 coupe	2008-2013	182.5	70.7	55.9	Nissan Altima Coupe	低车顶Coupe	可入库
Nissan Altima	Nissan	三厢车	Sedan	Std.	gen5 large	2013-2018	191.5	72	57.9	2013 Nissan Altima sedan		可入库
Nissan Altima	Nissan	三厢车	Sedan	Std.	gen6 large	2019-2026	192.9	72.9	57.4	2019-2026 Nissan Altima sedan		可入库
Hyundai Accent	Hyundai	三厢车	Sedan	Std.	gen1 compact	1995-1999	162.1	63.8	54.9	1995 Hyundai Accent Sedan, Edmunds		可入库
Hyundai Accent	Hyundai	两厢车	Hatchback	Std.	gen1 compact	1995-1999	162.1	63.8	54.9	1995 Hyundai Accent Hatchback, Edmunds / Carspecs		可入库
Hyundai Accent	Hyundai	三厢车	Sedan	Std.	gen2 compact	2000-2005	166.7	65.7	54.9	2000 Hyundai Accent Sedan, Carspecs		可入库
Hyundai Accent	Hyundai	两厢车	Hatchback	Std.	gen2 compact	2000-2005	166.7	65.7	54.9	2000 Hyundai Accent Hatchback, Edmunds		可入库
Hyundai Accent	Hyundai	三厢车	Sedan	Std.	gen3 compact	2006-2011	168.5	66.7	57.9	2011 Hyundai Accent Sedan GLS		可入库
Hyundai Accent	Hyundai	两厢车	Hatchback	Std.	gen3 compact	2006-2011	159.3	66.7	57.9	2011 Hyundai Accent SE Hatchback		可入库
Hyundai Accent	Hyundai	三厢车	Sedan	Std.	gen4 compact	2012-2017	172	66.9	57.1	2012 Hyundai Accent GLS Sedan		可入库
Hyundai Accent	Hyundai	两厢车	Hatchback	Std.	gen4 compact	2012-2017	162	66.9	57.1	2012 / 2016 Hyundai Accent Hatchback		可入库
Hyundai Accent	Hyundai	三厢车	Sedan	Std.	gen5 compact	2018-2022	172.6	68.1	57.1	2022 Hyundai Accent Limited / SE		可入库
Volkswagen Golf	Volkswagen	两厢车	Hatchback	Std.	gen4 hatchback	1999	160.4	66.7	56.2	1999 Volkswagen Golf GL Specs & Features	early body	可入库
Volkswagen Golf	Volkswagen	两厢车	Hatchback	Std.	gen4 hatchback	1999-2006	164.9	68.3	56.7	2006 Volkswagen Golf Hatchback Specs & Features		可入库
Volkswagen Golf	Volkswagen	两厢车	Hatchback	Std.	gen6 hatchback	2010-2014	165.4	70.3	58.3	2010 Volkswagen Golf Specs & Features		可入库
Volkswagen Golf	Volkswagen	两厢车	Hatchback	inc: GTI	gen7 hatchback	2015-2021	168	70.8	58.2	2021 Volkswagen Golf Specs & Features		可入库
Volkswagen Golf	Volkswagen	两厢车	Hatchback	inc: GTI/R	gen8 hatchback	2022-2026	169.1	70.4	57.8	2025 Volkswagen Golf R Specs & Features		可入库
Volkswagen Golf	Volkswagen	两厢车	Wagon	inc: SportWagen	gen7 wagon	2015-2017	179.6	70.8	58.3	2015 Volkswagen Golf SportWagen TDI S Specs & Features	长车身Wagon	可入库
Volkswagen Golf	Volkswagen	两厢车	Wagon	inc: Alltrack	gen7 wagon	2017-2019	179.6	70.8	59.7	2018 Volkswagen Golf Alltrack Specs & Features	高车身Alltrack	可入库
Chevrolet K5 Blazer	Chevrolet	越野车	SUV	Std.	gen1 full-size SUV	1969-1970	177.5	79	70	1969 brochure / 1970 Automobile-Catalog	初代短轴	可入库
Chevrolet K5 Blazer	Chevrolet	越野车	SUV	Std.	gen1 full-size SUV	1971-1972	180	79	72.8	1971/1972 Chevrolet Blazer specs	初代后期较高	可入库
Chevrolet K5 Blazer	Chevrolet	越野车	SUV	Std.	gen2 square-body full-size SUV	1973	184.5	79.5	69	1973 Chevrolet Blazer brochure	square body起点	可入库
Chevrolet K5 Blazer	Chevrolet	越野车	SUV	Std.	gen2 square-body full-size SUV	1974	184.5	79.1	71.5	1974 Chevrolet Blazer brochure	2WD/4WD高度差	可入库
Chevrolet K5 Blazer	Chevrolet	越野车	SUV	Std.	gen2 square-body full-size SUV	1975-1991	184.8	79.6	73.8	1990/1991 Chevrolet Blazer Edmunds	原77.8不采用	可入库
Chevrolet K5 Blazer	Chevrolet	越野车	SUV	Std.	gen3 GMT400 full-size SUV	1992-1994	187.8	76.4	71	1992/1994 Chevrolet Blazer Tahoe GMT400	GMT400过渡	可入库
Chevrolet K5 Blazer	Chevrolet	越野车	SUV	Std.	gen3 GMT400 full-size SUV	1994	187.7	76.4	71	1994 Chevrolet Blazer, Edmunds	固定车顶	可入库
Toyota Solara	Toyota	跑车	Coupe	Std.	gen1 coupe	1999-2001	190	71.1	55.1	1999 Toyota Camry Solara Coupe, Edmunds		可入库
Toyota Solara	Toyota	跑车	Convertible	Std.	gen1 convertible	2000-2001	190	71.1	55.1	2000-2001 Toyota Camry Solara Convertible	软顶	可入库
Toyota Solara	Toyota	跑车	Coupe	Std.	gen1 coupe	2002-2003	191.5	71.1	54.3	2002-2003 Toyota Camry Solara Coupe, Cars.com	低车顶Coupe	可入库
Toyota Solara	Toyota	跑车	Convertible	Std.	gen1 convertible	2002-2003	191.5	71.1	55.5	2002-2003 Toyota Camry Solara Convertible, Cars.com / AutoDetective	软顶较高	可入库
Toyota Solara	Toyota	跑车	Coupe	Std.	gen2 coupe	2004-2008	192.5	71.5	56.1	2004-2008 Toyota Camry Solara Coupe		可入库
Toyota Solara	Toyota	跑车	Convertible	Std.	gen2 convertible	2004-2008	192.5	71.5	56.5	2008 Toyota Camry Solara Convertible, Edmunds	软顶较高	可入库
Rivian R1S	Rivian	越野车	SUV	EV	gen1 electric SUV	2022-2026	200.8	82	77.3	Rivian R1S	高车身EV SUV	可入库

本批次完成。
所有可出库批次：1_brand50_part_20.tsv。

