# 文件名：1_brand50_part_28.tsv


--- Round 1 / 首次发送 ---
文件内容已读取。

粘贴的文本 (1)

当前文件并非最新全量表格式，存在大量需要结构化修复的记录（BMW 6 Series、Nissan Rogue、XC90、Clubman、QX80、Wagoneer、EC40 等仍为旧格式），且部分老爷车仍有“待终核”状态，因此不能输出“本批次完成”。

按最新全量表格式（主车型 | 品牌 | 分类 | 结构 | 版本 | 代际 | 年份 | max_length_in | max_width_in (w/o) | max_height_in | 参考车型 | 备注 | 迭代状态）应继续补强。

当前状态
车型	状态
Chevrolet Malibu	🟢 可入库
Chevrolet Equinox	🟢 可入库
BMW 6 Series	🟡 需拆分 Coupe / Convertible / Gran Coupe / GT 并补品牌等字段
Nissan Rogue	🟡 需转最新格式并处理 PHEV
Volvo XC90	🟡 需转最新格式并处理 PHEV
MINI Clubman	🟡 需转最新格式
Infiniti QX80	🟡 需转最新格式
Jeep Wagoneer	🟡 需拆分结构并转最新格式
Volvo EC40	🟡 需转最新格式
Dodge Ramcharger	🟡 存在待终核年份
Jaguar XJS	🟡 存在待终核年份
下一步所有可出库批次

🟢 Chevrolet Malibu

🟢 Chevrolet Equinox

待补强重点

BMW 6 Series

Nissan Rogue

Volvo XC90

MINI Clubman

Infiniti QX80

Jeep Wagoneer

Volvo EC40

Dodge Ramcharger

Jaguar XJS

继续下一步时，我将直接输出按最新格式修复后的完整可替换 TSV。


--- Round 2 / 下一步 ---
已按最新普通车全量表格式整理。来源：

粘贴的文本 (1)

tsv
主车型	品牌	分类	结构	版本	代际	年份	max_length_in	max_width_in (w/o)	max_height_in	参考车型	备注	迭代状态
Chevrolet Malibu	Chevrolet	三厢车	Sedan	Std.	gen5 midsize sedan	1997–2003	190.4	69.4	56.4	1998/2002 Chevrolet Malibu	中型轿车	可入库
Chevrolet Malibu	Chevrolet	三厢车	Sedan	Std.	gen6 midsize sedan	2004–2007	188.3	69.9	57.5	2004/2006 Chevrolet Malibu	中型轿车	可入库
Chevrolet Malibu	Chevrolet	三厢车	Sedan	Std.	gen7 midsize sedan	2008–2012	191.8	70.3	57.1	2008/2011 Chevrolet Malibu	中型轿车	可入库
Chevrolet Malibu	Chevrolet	三厢车	Sedan	Std.	gen8 midsize sedan	2013–2015	191.5	73	57.6	2013/2015 Chevrolet Malibu	中型轿车	可入库
Chevrolet Malibu	Chevrolet	三厢车	Sedan	Std.	gen9 midsize sedan	2016–2025	194.2	73	57.9	2023/2025 Chevrolet Malibu	中型轿车	可入库
Chevrolet Equinox	Chevrolet	越野车	SUV	Std.	gen1 compact SUV	2005–2009	188.8	71.4	69.3	2005/2006 Chevrolet Equinox	早期长车身SUV	可入库
Chevrolet Equinox	Chevrolet	越野车	SUV	Std.	gen2 compact SUV	2010–2017	187.8	72.5	69.3	2011/2016/2017 Chevrolet Equinox	紧凑SUV	可入库
Chevrolet Equinox	Chevrolet	越野车	SUV	Std.	gen3 compact SUV	2018–2024	183.1	72.6	65.4	2023/2024 Chevrolet Equinox	紧凑SUV	可入库
Chevrolet Equinox	Chevrolet	越野车	SUV	Std.	gen4 compact SUV	2025–2026	183.2	74.9	65.6	2025/2026 Chevrolet Equinox	紧凑SUV	可入库
Chevrolet Equinox	Chevrolet	越野车	SUV	EV	gen1 compact EV SUV	2024–2026	190.6	76.9	64.8	2025/2026 Chevrolet Equinox EV	EV尺寸更大	可入库

下一步所有可出库批次：Chevrolet Malibu、Chevrolet Equinox。

