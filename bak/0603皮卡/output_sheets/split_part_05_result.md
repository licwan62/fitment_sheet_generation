# 文件名：split_part_05.tsv


--- Round 1 / 首次发送 ---
更新点：本批次继续处理 split_part_05 的全量表，主要是根据年份和参考车型规则，将 Chevrolet 和部分其他车型的多年份区间拆分标记为待补强，确保参考车型覆盖每一年，并保持结构/版本独立记录。暂未完成逐年可入库确认，因此仍保留“待终核/待补强”状态。

当前批次更新后的完整可替换 TSV（皮卡/非皮卡车型均已整理至当前文件）如下：

主车型 品牌 分类 结构 版本 代际 年份 max_length_in max_width_in (w/o) max_height_in 参考车型 备注 迭代状态
Chevrolet Corvette Chevrolet 跑车 Coupe inc: Z06/ZR1 gen6 sports car 2005-2013 177.9 75.9 49.1 2013 Corvette ZR1 / base C6 宽体前置跑车 待补强: 2005-2012
Chevrolet Corvette Chevrolet 跑车 Coupe inc: Z06/ZR1 gen7 sports car 2014-2019 176.9 77.4 48.8 2019 Corvette ZR1 / Z06 宽体前置跑车 待补强: 2014-2018
Chevrolet Corvette Chevrolet 跑车 Coupe inc: widebody gen8 sports car 2020-2026 186.7 79.7 48.6 2026 Corvette ZR1 / E-Ray / Stingray 宽体中置跑车 待补强: 2020-2025
Chevrolet Cruze Chevrolet 三厢车 Sedan Std. gen1 compact sedan 2011-2016 181.0 70.7 58.1 2016 Chevrolet Cruze LTZ 紧凑轿车 待补强: 2011-2015
Chevrolet Cruze Chevrolet 三厢车 Sedan Std. gen2 compact sedan 2017-2019 183.7 70.5 57.4 2019 Chevrolet Cruze Sedan Premier 紧凑轿车 待补强: 2017-2018
Chevrolet Cruze Chevrolet 两厢车 Hatchback Std. gen1 compact hatch 2011-2016 180.9 70.7 57.4 2016 Chevrolet Cruze Hatchback LTZ 紧凑两厢 待补强: 2011-2015
Chevrolet Cruze Chevrolet 两厢车 Hatchback Std. gen2 compact hatch 2017-2019 183.0 70.5 57.4 2019 Chevrolet Cruze Hatchback Premier 紧凑两厢 待补强: 2017-2018
Chevrolet Malibu Chevrolet 三厢车 Sedan Std. gen1 midsize sedan 2008-2012 190.8 72.2 58.2 2012 Chevrolet Malibu LTZ 中型轿车 待补强: 2008-2011
Chevrolet Malibu Chevrolet 三厢车 Sedan Std. gen2 midsize sedan 2013-2019 191.4 72.4 58.0 2019 Chevrolet Malibu Premier 中型轿车 待补强: 2013-2018
Chevrolet Malibu Chevrolet 三厢车 Sedan Std. gen3 midsize sedan 2020-2026 193.8 73.0 57.3 2026 Chevrolet Malibu RS / Premier 中型轿车 待补强: 2020-2025

下一步

