# 文件名：1_brand50_part_20.tsv


--- Round 1 / 首次发送 ---
基于当前文件内容进行结构化修复（采用你要求的最新普通车全量表结构；老车保留老车结构逻辑）。来源文件：

粘贴的文本 (1)

tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Lexus ES	Lexus	三厢车	Sedan	Std.	gen1 compact sedan	1991	183.1	66.9	53.1	1991 Lexus ES 250 Sedan		待终核
Lexus ES	Lexus	三厢车	Sedan	Std.	gen2 midsize sedan	1997-2001	190.2	70.5	54.9	1997 Lexus ES 300		待终核
Lexus ES	Lexus	三厢车	Sedan	Std.	gen3 midsize sedan	2002-2006	191.1	71.7	56.3	2002 Lexus ES 300		待终核
Lexus ES	Lexus	三厢车	Sedan	Std.	gen4 midsize sedan	2007-2012	191.1	71.7	57.1	2007 Lexus ES 350		待终核
Lexus ES	Lexus	三厢车	Sedan	Std.	gen6 large sedan	2013-2018	192.7	71.1	57.1	2015 Lexus ES 300h		待终核
Lexus ES	Lexus	三厢车	Sedan	Std.	gen7 large sedan	2019-2025	195.9	73.4	57.1	2024 Lexus ES 250 F SPORT Design		待终核
Lexus ES	Lexus	三厢车	Sedan	inc: EV	gen8 EV sedan	2026	202.4	75.6	61.4	2026 Lexus ES 350e / ES 500e	EV新平台	待终核

Chrysler Pacifica	Chrysler	越野车	CUV	Std.	gen1 crossover	2004-2008	198.9	79.3	66.5	2004-2008 Chrysler Pacifica	跨界CUV	待终核
Chrysler Pacifica	Chrysler	越野车	Minivan	Std.	gen2 minivan	2017-2020	203.8	79.6	69.9	2017-2020 Chrysler Pacifica		待终核
Chrysler Pacifica	Chrysler	越野车	Minivan	inc: PHEV	gen2 minivan	2017-2020	203.8	79.6	69.9	2017 Chrysler Pacifica Hybrid	PHEV	待终核
Chrysler Pacifica	Chrysler	越野车	Minivan	Std.	gen2 facelift minivan	2021-2023	204.3	79.6	69.9	2021-2023 Chrysler Pacifica		待终核
Chrysler Pacifica	Chrysler	越野车	Minivan	inc: PHEV	gen2 facelift minivan	2021-2023	204.3	79.6	69.9	2021-2023 Chrysler Pacifica Hybrid	PHEV	待终核
Chrysler Pacifica	Chrysler	越野车	Minivan	Std.	gen2 facelift minivan	2024-2026	204.3	79.6	70.7	2024-2026 Chrysler Pacifica Select	高度变化	待终核
Chrysler Pacifica	Chrysler	越野车	Minivan	inc: PHEV	gen2 facelift minivan	2024-2026	204.3	79.6	70.7	2024-2026 Chrysler Pacifica Plug-in Hybrid	PHEV	待终核

Nissan Altima	Nissan	三厢车	Sedan	Std.	gen1 compact sedan	1993-1997	180.5	67.1	55.9	1993 Nissan Altima SE / GXE		待终核
Nissan Altima	Nissan	三厢车	Sedan	Std.	gen2 compact sedan	1998-2001	185.8	69.1	56.1	1998-2001 Nissan Altima Sedan		待终核
Nissan Altima	Nissan	三厢车	Sedan	Std.	gen3 midsize sedan	2002-2006	191.5	70.4	57.9	2002 Nissan Altima 3.5 SE / 2.5 SL		待终核
Nissan Altima	Nissan	三厢车	Sedan	Std.	gen4 midsize sedan	2007-2012	190.7	70.7	58.3	2007


--- Round 2 / 下一步 ---
继续处理剩余车型，来源文件：

粘贴的文本 (1)

tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Volkswagen Golf	Volkswagen	两厢车	Hatchback	Std.	gen4 hatchback	1999	160.4	66.7	56.2	1999 Volkswagen Golf GL Specs & Features	early body	待终核
Volkswagen Golf	Volkswagen	两厢车	Hatchback	Std.	gen4/5 hatchback	1999-2006	164.9	68.3	56.7	2006 Volkswagen Golf Hatchback Specs & Features		待终核
Volkswagen Golf	Volkswagen	两厢车	Hatchback	Std.	gen6 hatchback	2010-2014	165.4	70.3	58.3	2010 Volkswagen Golf Specs & Features		待终核
Volkswagen Golf	Volkswagen	两厢车	Hatchback	inc: GTI	gen7 hatchback	2015-2021	168	70.8	58.2	2021 Volkswagen Golf Specs & Features	GTI并入	待终核
Volkswagen Golf	Volkswagen	两厢车	Hatchback	inc: GTI/R	gen8 hatchback	2022-2026	169.1	70.4	57.8	2025 Volkswagen Golf R Specs & Features	GTI/R并入	待终核
Volkswagen Golf	Volkswagen	越野车	Wagon	inc: SportWagen	gen7 wagon	2015-2017	179.6	70.8	58.3	2015 Volkswagen Golf SportWagen TDI S Specs & Features	长车身wagon	待终核
Volkswagen Golf	Volkswagen	越野车	Wagon	inc: Alltrack	gen7 wagon	2017-2019	179.6	70.8	59.7	2018 Volkswagen Golf Alltrack Specs & Features	加高wagon	待终核
Toyota Solara	Toyota	跑车	Coupe	Std.	gen1 coupe	1999-2001	190	71.1	55.1	1999/2000/2001 Toyota Camry Solara Coupe		待终核
Toyota Solara	Toyota	跑车	Convertible	Std.	gen1 convertible	1999-2001	190	71.1	55.1	1999/2000/2001 Toyota Camry Solara Convertible		待终核
Toyota Solara	Toyota	跑车	Coupe	Std.	gen1 coupe	2002	191.5	71.1	55.1	2002 Toyota Camry Solara SE		待终核
Toyota Solara	Toyota	跑车	Convertibl


--- Round 3 / 下一步 ---
粘贴的文本 (1)


--- Round 4 / 下一步 ---
粘贴的文本 (1)

