# Auto next transcript
开始时间：2026-06-26 23:59:45
发送内容：下一步


--- Round 1 / 手动初始 prompt 回复 ---
ChatGPT 说：本轮我把上一轮已经固定的结果整理成正式 TSV 交付：一个全量表、一个子车系对照表、一个待补清单。不生成 XLSX，下面也直接展示本轮 TSV 内容。Pythonfrom pathlib import Pathimport csvbase = Path("/mnt/data")full_cols = ["主车型","年份区间","结构","品牌","前台车型","分类","版本","门数","代际","max_length_in","max_width_in","max_height_in","驾驶室类型","货斗长度_ft","参考车型","备注","迭代状态"]rows = [["Chevrolet C/K","1967","Pickup","Chevrolet","Chevrolet C/K","皮卡","","2","gen2","188.5","79","69.5","Regular","6.5","1967 Chevrolet C10 Regular Cab Fleetside/Stepside 6.5ft","Action Line; 2WD; 1/2 ton; Regular Cab; 6.5ft bed","单年已核，可入库"],["Chevrolet C/K","1967","Pickup","Chevrolet","Chevrolet C/K","皮卡","","2","gen2","207.75","79","69.5","Regular","8.0","1967 Chevrolet C10 Regular Cab Fleetside/Stepside 8ft","Action Line; 2WD; 1/2 ton; Regular Cab; 8ft bed","单年已核，可入库"],["Chevrolet C/K","1967","Pickup","Chevrolet","Chevrolet C/K","皮卡","","2","gen2","207.75","79","71","Regular","8.0","1967 Chevrolet C20 Regular Cab Fleetside/Stepside 8ft","Action Line; 2WD; 3/4 ton; Regular Cab; 8ft bed","单年已核，可入库"],["Chevrolet C/K","1967","Pickup","Chevrolet","Chevrolet C/K","皮卡","","2","gen2","217.75","79","71","Regular","9.0","1967 Chevrolet C30 Regular Cab Stepside 9ft","Action Line; 2WD; 1 ton; Regular Cab; 9ft bed","单年已核，可入库"],["Chevrolet C/K","1967","Pickup","Chevrolet","Chevrolet C/K","皮卡","","2","gen2","188.5","79","72.5","Regular","6.5","1967 Chevrolet K10 Regular Cab Fleetside/Stepside 6.5ft","Action Line; 4WD; 1/2 ton; Regular Cab; 6.5ft bed","单年已核，可入库"],["Chevrolet C/K","1967","Pickup","Chevrolet","Chevrolet C/K","皮卡","","2","gen2","207.75","79","72.5","Regular","8.0","1967 Chevrolet K10 Regular Cab Fleetside/Stepside 8ft","Action Line; 4WD; 1/2 ton; Regular Cab; 8ft bed","单年已核，可入库"],["Chevrolet C/K","1967","Pickup","Chevrolet","Chevrolet C/K","皮卡","","2","gen2","207.75","79","74","Regular","8.0","1967 Chevrolet K20 Regular Cab Fleetside/Stepside 8ft","Action Line; 4WD; 3/4 ton; Regular Cab; 8ft bed","单年已核，可入库"],["Chevrolet C/K","1973","Pickup","Chevrolet","Chevrolet C/K","皮卡","","2","gen3","191.25","79.5","69.5","Regular","6.5","1973 Chevrolet C10 Regular Cab Fleetside/Stepside 6.5ft","Squarebody early; 2WD; 1/2 ton; Regular Cab; 6.5ft bed; Fleetside/Stepside","单年已核，可入库"],["Chevrolet C/K","1973","Pickup","Chevrolet","Chevrolet C/K","皮卡","","2","gen3","211.25","79.5","69.5","Regular","8.0","1973 Chevrolet C10 Regular Cab Fleetside/Stepside 8ft","Squarebody early; 2WD; 1/2 ton; Regular Cab; 8ft bed; Fleetside/Stepside","单年已核，可入库"],["Chevrolet C/K","1973","Pickup","Chevrolet","Chevrolet C/K","皮卡","","2","gen3","191.25","79.5","72.25","Regular","6.5","1973 Chevrolet K10 Regular Cab Fleetside/Stepside 6.5ft","Squarebody early; 4WD; 1/2 ton; Regular Cab; 6.5ft bed; Fleetside/Stepside","单年已核，可入库"],["Chevrolet C/K","1973","Pickup","Chevrolet","Chevrolet C/K","皮卡","","2","gen3","211.25","79.5","72.25","Regular","8.0","1973 Chevrolet K10 Regular Cab Fleetside/Stepside 8ft","Squarebody early; 4WD; 1/2 ton; Regular Cab; 8ft bed; Fleetside/Stepside","单年已核，可入库"],["Chevrolet C/K","1973","Pickup","Chevrolet","Chevrolet C/K","皮卡","","2","gen3","211.25","79.5","71.0","Regular","8.0","1973 Chevrolet C20 Regular Cab Fleetside/Stepside 8ft","Squarebody early; 2WD; 3/4 ton; Regular Cab; 8ft bed; Fleetside/Stepside","单年已核，可入库"],["Chevrolet C/K","1973","Pickup","Chevrolet","Chevrolet C/K","皮卡","","4","gen3","244.25","79.5","71.75","Crew","8.0","1973 Chevrolet C20 Crew Cab Fleetside 8ft","Squarebody early; 2WD; 3/4 ton; Crew Cab; 8ft bed; Fleetside","单年已核，可入库"],["Chevrolet C/K","1973","Pickup","Chevrolet","Chevrolet C/K","皮卡","","2","gen3","211.25","79.5","73.5","Regular","8.0","1973 Chevrolet K20 Regular Cab Fleetside/Stepside 8ft","Squarebody early; 4WD; 3/4 ton; Regular Cab; 8ft bed; Fleetside/Stepside","单年已核，可入库"],["Chevrolet C/K","1973","Pickup","Chevrolet","Chevrolet C/K","皮卡","","2","gen3","211.25","79.5","71.0","Regular","8.0","1973 Chevrolet C30 Regular Cab Fleetside/Stepside 8ft","Squarebody early; 2WD; 1 ton; Regular Cab; 8ft bed; Fleetside/Stepside; SRW","单年已核，可入库"],["Chevrolet C/K","1973","Pickup","Chevrolet","Chevrolet C/K","皮卡","","4","gen3","244.25","79.5","71.0","Crew","8.0","1973 Chevrolet C30 Crew Cab Fleetside 8ft","Squarebody early; 2WD; 1 ton; Crew Cab; 8ft bed; Fleetside; SRW","单年已核，可入库"],["Chevrolet C/K","1987","Pickup","Chevrolet","Chevrolet C/K","皮卡","R/V","2","gen3","193.5","79.6","69.2","Regular","6.5","1987 Chevrolet R10/1500 Regular Cab Fleetside/Wideside 6.5ft","R/V; Squarebody facelift; 2WD; 1/2 ton; Regular Cab; 6.5ft bed","单年已核，可入库"],["Chevrolet C/K","1987","Pickup","Chevrolet","Chevrolet C/K","皮卡","R/V","2","gen3","212.2","79.6","69.2","Regular","8.0","1987 Chevrolet R10/1500 Regular Cab Fleetside/Wideside 8ft","R/V; Squarebody facelift; 2WD; 1/2 ton; Regular Cab; 8ft bed","单年已核，可入库"],["Chevrolet C/K","1987","Pickup","Chevrolet","Chevrolet C/K","皮卡","R/V","2","gen3","192.6","79.6","73.0","Regular","6.5","1987 Chevrolet V10/1500 Regular Cab Fleetside/Wideside 6.5ft","R/V; Squarebody facelift; 4WD; 1/2 ton; Regular Cab; 6.5ft bed","单年已核，可入库"],["Chevrolet C/K","1987","Pickup","Chevrolet","Chevrolet C/K","皮卡","R/V","2","gen3","212.5","79.6","73.0","Regular","8.0","1987 Chevrolet V10/1500 Regular Cab Fleetside/Wideside 8ft","R/V; Squarebody facelift; 4WD; 1/2 ton; Regular Cab; 8ft bed","单年已核，可入库"],["Chevrolet C/K","1987","Pickup","Chevrolet","Chevrolet C/K","皮卡","R/V","2","gen3","212.2","79.6","72.2","Regular","8.0","1987 Chevrolet R20/2500 Regular Cab Fleetside/Wideside 8ft","R/V; Squarebody facelift; 2WD; 3/4 ton; Regular Cab; 8ft bed","单年已核，可入库"],["Chevrolet C/K","1987","Pickup","Chevrolet","Chevrolet C/K","皮卡","R/V","2","gen3","212.5","79.6","73.6","Regular","8.0","1987 Chevrolet V20/2500 Regular Cab Fleetside/Wideside 8ft","R/V; Squarebody facelift; 4WD; 3/4 ton; Regular Cab; 8ft bed","单年已核，可入库"],["Chevrolet C/K","1987","Pickup","Chevrolet","Chevrolet C/K","皮卡","R/V","2","gen3","212.2","79.6","73.0","Regular","8.0","1987 Chevrolet R30/3500 Regular Cab Fleetside/Wideside 8ft","R/V; Squarebody facelift; 2WD; 1 ton; Regular Cab; 8ft bed; SRW","单年已核，可入库"],["Chevrolet C/K","1987","Pickup","Chevrolet","Chevrolet C/K","皮卡","R/V","2","gen3","212.5","79.6","75.8","Regular","8.0","1987 Chevrolet V30/3500 Regular Cab Fleetside/Wideside 8ft","R/V; Squarebody facelift; 4WD; 1 ton; Regular Cab; 8ft bed","单年已核，可入库"],["Chevrolet C/K","1998","Pickup","Chevrolet","Chevrolet C/K","皮卡","","2","gen4","194.5","76.8","70.8","Regular","6.5","1998 Chevrolet C/K 1500 Series Regular Cab 4WD","GMT400; 4WD; 1/2 ton; Regular Cab; 6.5ft bed","单年已核，可入库"],["Chevrolet C/K","1998","Pickup","Chevrolet","Chevrolet C/K","皮卡","","2/3","gen4","218.5","76.8","70.8","Extended","6.5","1998 Chevrolet C/K 1500 Series Extended Cab SB","GMT400; 2WD; 1/2 ton; Extended Cab; 6.5ft bed; L修正为218.5","单年已核，可入库"],["Chevrolet C/K","1998","Pickup","Chevrolet","Chevrolet C/K","皮卡","","2","gen4","213.1","76.8","71.2","Regular","8.0","1998 Chevrolet C/K 2500 Series Regular Cab RWD","GMT400; 2WD; 3/4 ton; Regular Cab; 8ft bed","单年已核，可入库"],["Chevrolet C/K","1998","Pickup","Chevrolet","Chevrolet C/K","皮卡","","2/3","gen4","237.4","76.8","76.0","Extended","8.0","1998 Chevrolet C/K 2500 Series HD Extended Cab 4WD LB","GMT400; 4WD; 3/4 ton; HD; Extended Cab; 8ft bed","单年已核，可入库"],["Chevrolet C/K","1998","Pickup","Chevrolet","Chevrolet C/K","皮卡","","2","gen4","213.1","76.8","73.2","Regular","8.0","1998 Chevrolet C/K 3500 Series Regular Cab RWD","GMT400; 2WD; 1 ton; Regular Cab; 8ft bed; SRW","单年已核，可入库"],["Chevrolet C/K","1998","Pickup","Chevrolet","Chevrolet C/K","皮卡","","2/3","gen4","237.4","76.8","74.0","Extended","8.0","1998 Chevrolet C/K 3500 Series Extended Cab 4WD LB","GMT400; 4WD; 1 ton; Extended Cab; 8ft bed; SRW","单年已核，可入库"],["Chevrolet C/K","1998","Pickup","Chevrolet","Chevrolet C/K","皮卡","","4","gen4","250.1","76.8","73.9","Crew","8.0","1998 Chevrolet C/K 3500 Series Crew Cab RWD","GMT400; 2WD; 1 ton; Crew Cab; 8ft bed; SRW; L修正为250.1","单年已核，可入库"],["Chevrolet C/K","1999","Pickup","Chevrolet","Chevrolet C/K","皮卡","Classic","2/3","gen4","227.6","78.5","74.0","Extended","6.5","1999 Chevrolet C/K 1500 Series Extended Cab SB","GMT400 Classic; 2WD; 1/2 ton; Extended Cab; 6.5ft bed","单年已核，可入库"],["Chevrolet C/K","1999","Pickup","Chevrolet","Chevrolet C/K","皮卡","Classic","2","gen4","227.6","78.5","73.7","Regular","8.0","1999 Chevrolet C/K 2500 Series Regular Cab LB","GMT400 Classic; 2WD; 3/4 ton; Regular Cab; 8ft bed","单年已核，可入库"],["Chevrolet C/K","1999","Pickup","Chevrolet","Chevrolet C/K","皮卡","Classic","2/3","gen4","246.5","78.5","74.1","Extended","8.0","1999 Chevrolet C/K 2500 Series Extended Cab LB","GMT400 Classic; 2WD; 3/4 ton; Extended Cab; 8ft bed","单年已核，可入库"],["Chevrolet C/K","1999","Pickup","Chevrolet","Chevrolet C/K","皮卡","Classic","2","gen4","227.6","78.5","74.2","Regular","8.0","1999 Chevrolet C/K 3500 Series Regular Cab 4WD LB","GMT400 Classic; 4WD; 1 ton; Regular Cab; 8ft bed; SRW","单年已核，可入库"],["Chevrolet C/K","1999","Pickup","Chevrolet","Chevrolet C/K","皮卡","Classic","4","gen4","250.9","77.0","73.9","Crew","8.0","1999 Chevrolet C/K 3500 Series Crew Cab LB","GMT400 Classic; 2WD; 1 ton; Crew Cab; 8ft bed; SRW","单年已核，可入库"],["Chevrolet C/K","2000","Pickup","Chevrolet","Chevrolet C/K","皮卡","Classic","2","gen4","213.1","77.0","71.2","Regular","8.0","2000 Chevrolet C/K 2500 Series Regular Cab 4WD LB","GMT400 Classic; 4WD; 3/4 ton; Regular Cab; 8ft bed","单年已核，可入库"],["Chevrolet C/K","2000","Pickup","Chevrolet","Chevrolet C/K","皮卡","Classic","2/3","gen4","237.4","77.0","76.0","Extended","8.0","2000 Chevrolet C/K 2500 Series Extended Cab 4WD LB","GMT400 Classic; 4WD; 3/4 ton; Extended Cab; 8ft bed","单年已核，可入库"],["Chevrolet C/K","2000","Pickup","Chevrolet","Chevrolet C/K","皮卡","Classic","4","gen4","231.9","77.0","73.9","Crew","6.5","2000 Chevrolet C/K 2500 Series Crew Cab RWD","GMT400 Classic; 2WD; 3/4 ton; Crew Cab; 6.5ft bed","单年已核，可入库"],["Chevrolet C/K","2000","Pickup","Chevrolet","Chevrolet C/K","皮卡","Classic","4","gen4","231.9","77.0","74.5","Crew","6.5","2000 Chevrolet C/K 2500 Series Crew Cab 4WD SB","GMT400 Classic; 4WD; 3/4 ton; Crew Cab; 6.5ft bed","单年已核，可入库"],["Chevrolet C/K","2000","Pickup","Chevrolet","Chevrolet C/K","皮卡","Classic","2","gen4","213.1","77.0","73.2","Regular","8.0","2000 Chevrolet C/K 3500 Series Regular Cab 4WD LB","GMT400 Classic; 4WD; 1 ton; Regular Cab; 8ft bed; SRW","单年已核，可入库"],["Chevrolet C/K","2000","Pickup","Chevrolet","Chevrolet C/K","皮卡","Classic","2/3","gen4","237.4","77.0","74.0","Extended","8.0","2000 Chevrolet C/K 3500 Series Extended Cab 4WD LB","GMT400 Classic; 4WD; 1 ton; Extended Cab; 8ft bed; SRW","单年已核，可入库"],["Chevrolet C/K","2000","Pickup","Chevrolet","Chevrolet C/K","皮卡","Classic DRW","4","gen4","250.9","94.3","74.5","Crew","8.0","2000 Chevrolet C/K 3500 Series Crew Cab 4WD DRW","GMT400 Classic; 4WD; 1 ton; Crew Cab; 8ft bed; DRW","单年已核，可入库"],]sub_cols = ["Year","主车型","结构","版本","候选车型","匹配数量"]sub_rows = [["1967","Chevrolet C/K","","","Chevrolet|C10 Pickup; Chevrolet|C20 Pickup; Chevrolet|C30 Pickup; Chevrolet|K10 Pickup; Chevrolet|K20 Pickup","5"],["1973","Chevrolet C/K","","","Chevrolet|C10 Pickup; Chevrolet|C20 Pickup; Chevrolet|C30 Pickup; Chevrolet|K10 Pickup; Chevrolet|K20 Pickup","5"],["1987","Chevrolet C/K","","","Chevrolet|R10; Chevrolet|R20; Chevrolet|R30; Chevrolet|V10; Chevrolet|V20; Chevrolet|V30","6"],["1998","Chevrolet C/K","","","Chevrolet|C1500; Chevrolet|C2500; Chevrolet|C3500; Chevrolet|K1500; Chevrolet|K2500; Chevrolet|K3500","6"],["1999","Chevrolet C/K","","","Chevrolet|C1500; Chevrolet|C2500; Chevrolet|C3500; Chevrolet|K3500","4"],["2000","Chevrolet C/K","","","Chevrolet|C2500; Chevrolet|C3500; Chevrolet|K2500; Chevrolet|K3500","4"],]pending_cols = ["待补对象","当前问题","处理状态"]pending_rows = [["1968-1972 Action Line","只有1967完整L/W/H，不能覆盖1968-1972","继续待补"],["1974-1980 Squarebody early","只有1973完整L/W/H，不能覆盖1974-1980","继续待补"],["1981-1986 Squarebody facelift","只有1987 R/V完整L/W/H，不能覆盖1981-1986","继续待补"],["1988-1997 GMT400 Regular/Extended","只有1998完整L/W/H，不能覆盖1988-1997","继续待补"],["1992-1997 GMT400 Crew Cab","只有1998 Crew Cab完整L/W/H，不能覆盖1992-1997","继续待补"],]def write_tsv(path, cols, data):    with path.open("w", encoding="utf-8-sig", newline="") as f:        writer = csv.writer(f, delimiter="\t", lineterminator="\n")        writer.writerow(cols)        writer.writerows(data)full_path = base / "chevrolet_ck_import_ready_conservative_full.tsv"sub_path = base / "chevrolet_ck_import_ready_submodel_mapping.tsv"pending_path = base / "chevrolet_ck_remaining_dimension_gaps.tsv"write_tsv(full_path, full_cols, rows)write_tsv(sub_path, sub_cols, sub_rows)write_tsv(pending_path, pending_cols, pending_rows)# Basic validationdef check_table(path):    with path.open("r", encoding="utf-8-sig", newline="") as f:        return sum(1 for _ in f) - 1missing_lwh = [r for r in rows if not r[9] or not r[10] or not r[11]]bad_gen = [r for r in rows if r[8] not in {"gen2","gen3","gen4"}]bad_interval = [r for r in rows if ";" in r[1]]print("正式TSV已生成")print(f"全量表: {full_path} 行数={check_table(full_path)}")print(f"子车系对照: {sub_path} 行数={check_table(sub_path)}")print(f"待补清单: {pending_path} 行数={check_table(pending_path)}")print(f"L/W/H缺失={len(missing_lwh)}; 代际异常={len(bad_gen)}; 断续年份区间={len(bad_interval)}")STDOUT/STDERR正式TSV已生成
全量表: /mnt/data/chevrolet_ck_import_ready_conservative_full.tsv 行数=43
子车系对照: /mnt/data/chevrolet_ck_import_ready_submodel_mapping.tsv 行数=6
待补清单: /mnt/data/chevrolet_ck_remaining_dimension_gaps.tsv 行数=5
L/W/H缺失=0; 代际异常=0; 断续年份区间=0
本轮已正式导出 3 个 TSV，不生成 XLSX。
下载：











校验结果：
全量表行数：43子车系对照：6剩余待补：5L/W/H 缺失：0代际异常：0断续年份区间：0
本轮最终确认：
tsv表名	行数	状态保守可入库全量表	43	可入库子车系对照表	6	可入库剩余待补尺寸清单	5	继续待补
下一步可以继续从待补清单里补尺寸，优先查：
tsv优先级	待补对象	目标1	1988-1997 GMT400 Regular/Extended	补 1989/1993/1997 完整 L/W/H2	1981-1986 Squarebody facelift	补 1981/1984/1986 完整 L/W/H3	1974-1980 Squarebody early	补 1977/1980 完整 L/W/H4	1968-1972 Action Line	补 1970/1972 完整 L/W/H


--- Round 2 / 下一步回复 ---
本轮继续查 1988-1997 GMT400 Regular / Extended / Crew 缺口。

结论：本轮不更新全量表，不扩 1998 单年记录。

原因是目前能确认：

GMT400 Regular Cab：1988 起
GMT400 Extended Cab：1988 起
Extended Cab 6.5ft short bed：1989 起
Crew Cab：1992 起，仅 3500 起步

但我没有拿到能逐条对应 C/K + 1500/2500/3500 + cab/bed + 2WD/4WD/HD/SRW 的完整 L/W/H 表。公开总览只够确认结构和起始年份，不够直接入库。
维基百科
+1

tsv
待补对象	本轮核对结论	处理结果	下一步动作
1988-1997 GMT400 Regular Cab	能确认Regular Cab从1988起，但未取得逐结构完整L/W/H	不扩1998单年记录	继续找1988/1993/1997官方dimensions页
1989-1997 GMT400 Extended Cab 6.5ft	能确认Extended short bed从1989起，但未取得完整L/W/H	不扩1998单年记录	继续找1989/1993/1997 Extended Cab SB尺寸
1988-1997 GMT400 Extended Cab 8ft	能确认Extended Cab长货斗存在，但未取得逐结构完整L/W/H	不扩1998单年记录	继续找1988/1993/1997 Extended Cab LB尺寸
1992-1997 GMT400 Crew Cab 8ft	能确认Crew Cab从1992起，但未取得1992/1995/1997完整L/W/H	不扩1998 Crew记录	继续找1992/1995/1997 Crew Cab尺寸
1998 GMT400	已有完整L/W/H	保持1998单年可入库	无需修改

当前状态不变：

本轮新增可入库：0 行
保守可入库全量表：43 行
子车系对照表：6 行
剩余待补尺寸段：5 组

下一轮建议转查 1981-1986 Squarebody facelift，因为它和 1987 R/V 的尺寸页关系最接近，最有机会补出可扩展区间。


--- Round 3 / 下一步回复 ---
ChatGPT 说：继续按待补清单推进，这轮处理 1981-1986 Squarebody facelift。我会优先找 1981/1984/1986 的逐结构完整 L/W/H；拿不到就不扩 1987 单年记录。本轮处理 1981-1986 Squarebody facelift 缺口。
结论：本轮不更新全量表，不扩 1987 单年记录。
原因：资料能确认 1981 是第三代 C/K 的中期 facelift，1987 为避免和 GMT400 新一代 C/K 重名而改称 R/V；但我没有拿到 1981/1984/1986 能逐条对应 C10/K10/C20/K20/C30 + Regular/Crew + bed 的完整 Length / Width / Height 表，所以不能用 1987 R/V 尺寸反推 1981-1986。维基百科
tsv待补对象	本轮核对结论	处理结果	下一步动作1981 Squarebody facelift	确认1981为facelift起点，但未取得逐结构完整L/W/H	不扩1987单年记录	继续找1981 Chevrolet Pickups brochure完整dimensions页1982-1984 Squarebody facelift	资料确认1982-1984有前脸/配置细节变化；未取得逐结构完整L/W/H	不新增入库	继续找1982/1984 Chevrolet Pickups dimensions页1985-1986 Squarebody facelift	已定位到1985 Chevrolet Full Size Pickups brochure相关入口，但未取得可用完整L/W/H表	不新增入库	继续找1985/1986完整dimensions页1987 R/V	已有完整L/W/H，且是命名边界	保持1987单年可入库	无需修改
当前状态不变：
本轮新增可入库：0 行保守可入库全量表：43 行子车系对照表：6 行剩余待补尺寸段：5 组
下一步转查 1974-1980 Squarebody early，重点继续找 1977 / 1980 的完整 dimensions 页，看看能不能把 1973 单年扩展。


--- Round 4 / 下一步回复 ---
本轮处理 1974-1980 Squarebody early 缺口复核。

结论：本轮不更新全量表，不扩 1973 单年记录。
原因是当前可确认 1973-1980 属于第三代 C/K 早期 Squarebody，但 1977 增加 K30，1980 K-Series 四驱系统也有变化；这些变化会影响候选结构和高度/驱动口径，不能直接用 1973 的完整 L/W/H 覆盖 1974-1980。
维基百科

tsv
待补对象	本轮核对结论	处理结果	下一步动作
1974 Squarebody early	未取得1974逐结构完整L/W/H；不能沿用1973尺寸	不新增入库；不扩1973区间	继续找1974 Chevrolet Pickups完整dimensions页
1975-1976 Squarebody early	可确认仍属早期Squarebody，但未取得逐结构完整L/W/H	不新增入库	继续找1975/1976 Chevrolet Pickups官方规格页
1977-1979 Squarebody early	1977新增K30，结构覆盖变化；未取得完整逐结构L/W/H	不新增入库	继续找1977/1978/1979 dimensions页
1980 Squarebody early	1980 K-Series四驱系统变化；未取得完整逐结构L/W/H	不新增入库	继续找1980 Chevrolet Pickups完整dimensions页
1973 Squarebody early	已有完整L/W/H	保持1973单年可入库	无需修改

当前状态不变：

本轮新增可入库：0 行
保守可入库全量表：43 行
子车系对照表：6 行
剩余待补尺寸段：5 组

剩余待补清单仍为：

tsv
待补对象	当前问题	处理状态
1968-1972 Action Line	只有1967完整L/W/H，不能覆盖1968-1972	继续待补
1974-1980 Squarebody early	只有1973完整L/W/H，不能覆盖1974-1980	继续待补
1981-1986 Squarebody facelift	只有1987 R/V完整L/W/H，不能覆盖1981-1986	继续待补
1988-1997 GMT400 Regular/Extended	只有1998完整L/W/H，不能覆盖1988-1997	继续待补
1992-1997 GMT400 Crew Cab	只有1998 Crew Cab完整L/W/H，不能覆盖1992-1997	继续待补

下一步处理 1968-1972 Action Line。


--- Round 5 / 下一步回复 ---
本轮处理 1968-1972 Action Line 缺口复核。

结论：本轮不更新全量表，不扩 1967 单年记录。

资料能确认第二代 Chevrolet C/K 覆盖 1967-1972，其中 1971 有中期前脸和底盘配置更新，1972 也有内饰/细节更新；但我本轮仍没有找到能逐条对应 C10/K10/C20/K20/C30 + Regular Cab + bed 的完整 Length / Width / Height 表，所以不能把 1967 的完整尺寸直接外推到 1968-1972。
维基百科

tsv
待补对象	本轮核对结论	处理结果	下一步动作
1968-1970 Action Line	资料确认仍属第二代Action Line，1970仅有小改；但未取得逐结构完整L/W/H	不新增入库；不扩1967区间	继续找1970 Chevrolet Pickups官方dimensions页
1971 Action Line	1971为中期更新年，前脸和底盘配置有变化；不能默认沿用1967尺寸	不新增入库	继续找1971 Chevrolet Pickups完整规格页
1972 Action Line	1972为第二代末年，有内饰/细节变化；未取得逐结构完整L/W/H	不新增入库	继续找1972 Chevrolet Pickups完整dimensions页
1967 Action Line	已有完整L/W/H	保持1967单年可入库	无需修改

当前状态不变：

本轮新增可入库：0 行
保守可入库全量表：43 行
子车系对照表：6 行
剩余待补尺寸段：5 组

到这里，5 组待补缺口都已经复核过一轮，当前没有新的可靠 L/W/H 可补入。下一步建议进入 最终交付状态确认：当前 Chevrolet C/K 先按 43 行保守表入库，待补 5 组作为后续扩展任务。


--- Round 6 / 下一步回复 ---
下一步是 最终入库确认。
Chevrolet C/K 当前阶段可以结束，按“保守可入库”版本入库。

tsv
项目	结果	说明
主车型	Chevrolet C/K	一个主车型，不拆 C10/K10/C20/K20/C30
全量表	43 行	全部有完整 L/W/H
子车系对照表	6 行	只覆盖已入库年份
待补尺寸	5 组	不入库，作为后续扩展任务
L/W/H 缺失	0	通过
断续年份区间	0	通过
代际异常	0	gen2/gen3/gen4，通过

正式入库顺序：

tsv
步骤	表	操作
1	全量表	导入保守可入库全量表 43 行
2	子车系对照表	导入 6 行子车系对照
3	待补尺寸清单	不要入库，只作为后续查证任务

当前应入库年份：

tsv
年份	状态
1967	可入库
1973	可入库
1987	可入库
1998	可入库
1999	可入库
2000	可入库

当前不应入库年份：

tsv
年份段	原因
1968-1972	没有完整逐结构 L/W/H
1974-1980	没有完整逐结构 L/W/H
1981-1986	没有完整逐结构 L/W/H
1988-1997	没有完整逐结构 L/W/H
1992-1997 Crew Cab	没有完整逐结构 L/W/H

最终文件使用这 3 个：

保守可入库全量表 TSV

子车系对照表 TSV

剩余待补尺寸清单 TSV

结论：

Chevrolet C/K 当前阶段：可以入库。
后续不是继续改当前入库表，而是单独补待补年份段，找到完整 L/W/H 后再追加或扩展区间。


--- Round 7 / 下一步回复 ---
下一步是 切换到下一个主车型。
Chevrolet C/K 当前已经到阶段终点，不建议继续反复查同一车型，否则会陷入“没有完整 L/W/H 就无法扩区间”的循环。

当前 Chevrolet C/K 的最终状态：

tsv
项目	状态	说明
全量表	完成	43 行保守可入库
子车系对照	完成	6 行，只覆盖已入库年份
待补尺寸	保留	5 组，不入库
当前车型	可结束	后续只在找到完整 L/W/H 后追加扩展

下一车型开始时，按这个流程走：

tsv
步骤	动作	目的
1	先确定主车型	不要先拆子车系
2	区分普通版/特殊版	普通版优先完整覆盖
3	确定代际/结构/版本	不要先压缩年份
4	逐条拿 L/W/H	没有 L/W/H 不进全量表
5	核边界年份	确认区间是否可入库
6	生成保守全量表	只保留可入库记录
7	生成子车系对照	只覆盖已入库年份
8	列待补清单	缺尺寸年份单独保留

建议你下一步发我下一个车型，格式可以是：

tsv
主车型	年份区间	结构	版本
Chevrolet Suburban	1947-1954

或者直接发你现有表格截图/TSV，我会继续按同样规则建模。


--- Round 8 / 下一步回复 ---
下一步需要进入 下一个主车型建模。

如果按你前面提到过的车型继续，我建议下一个做：

Chevrolet Suburban

因为它和 Chevrolet C/K 有关联，早期年份容易混入 pickup / panel / SUV，正好需要先把分类和结构边界理清。

下一步你可以直接发类似这样的表：

tsv
主车型	年份区间	结构	版本
Chevrolet Suburban	1947-1954
Chevrolet Suburban	1955
Chevrolet Suburban	1956-1959
Chevrolet Suburban	1960
Chevrolet Suburban	1961-1963
Chevrolet Suburban	1964-1966
Chevrolet Suburban	1967-1968
Chevrolet Suburban	1969
Chevrolet Suburban	1970-1971
Chevrolet Suburban	1972

我会按这个顺序处理：

tsv
步骤	处理内容
1	先判断 Suburban 是 SUV / wagon / truck-based utility，不直接归为 pickup
2	确认是否有 cab / bed，通常不按皮卡 cab/bed 建模
3	分普通版和特殊版
4	逐代际确定结构、版本、年份区间
5	逐条找 L/W/H
6	没有完整 L/W/H 的不进全量表
7	生成保守可入库全量表
8	再生成子车系对照表

你直接把下一个车型表发我，我从 全量表建模第一步 开始。


--- Round 9 / 下一步回复 ---
下一步我开始 Chevrolet Suburban 建模第 1 轮：确定主车型边界。

先不做尺寸表，先把它和 Chevrolet C/K Pickup 区分清楚。

本轮结论

Chevrolet Suburban 不应归为 Pickup，也不应该建 cab / bed。
它是基于卡车平台的 wagon / utility vehicle，也就是早期 SUV 逻辑；虽然与 C/K、Task Force、Action Line 等皮卡平台共享机械结构，但前台主车型应独立为：

Chevrolet Suburban

不能写成：

Chevrolet C/K Suburban
Chevrolet C10 Suburban
Chevrolet K10 Suburban

C/K、C10、K10、C20、K20 这类只作为数据库候选或备注口径，不作为主车型拆分。

Chevrolet Suburban 第一轮建模 TSV
tsv
主车型	分类	结构	是否皮卡	是否需要驾驶室类型	是否需要货斗长度	建模结论
Chevrolet Suburban	SUV	Wagon / Utility	否	否	否	独立主车型；不归入 Chevrolet C/K Pickup；不建 cab/bed

依据：Suburban 多代都与卡车平台共享机械结构，例如 1947 一代基于 Advance Design pickups，1960-1966 一代基于第一代 C/K，1967-1972 一代基于 Action-Line C/K；但资料也明确它作为 truck-based wagon / utility vehicle，而不是 pickup。
维基百科
+2
维基百科
+2

初步代际切分
tsv
主车型	年份区间	分类	结构	版本	代际	代际说明	建模状态
Chevrolet Suburban	1947-1954	SUV	Wagon / Utility		gen1	Advance Design-based Suburban	待取 L/W/H
Chevrolet Suburban	1955-1959	SUV	Wagon / Utility		gen2	Task Force-based Suburban	待取 L/W/H
Chevrolet Suburban	1960-1966	SUV	Wagon / Utility		gen3	First-generation C/K-based Suburban	待取 L/W/H
Chevrolet Suburban	1967-1972	SUV	Wagon / Utility		gen4	Action-Line-based Suburban	待取 L/W/H

说明：

1947-1954：基于 Chevrolet Advance Design pickup 平台。
1955：Task Force 系列在 1955 年中引入，因此 1955 可能需要单独核。
1960-1966：第一代 C/K 平台，Suburban 为 two-door utility wagon，也有 panel van 口径。
1967-1972：Action-Line 平台，Suburban 轴距增至 127 in，并首次有 C-20 Suburban、K-10/K-20 4WD 口径。

这些边界目前只是 建模切分，不是可入库全量表。下一步要逐段拿完整 L/W/H，没有完整尺寸的不进全量表。

下一轮动作

下一步处理：

Chevrolet Suburban 1947-1954

目标是先查 1947-1954 Advance Design Suburban 的完整：

Length / Width / Height

如果只找到 wheelbase 或总览长度，没有完整 L/W/H，就不入库。


--- Round 10 / 下一步回复 ---
ChatGPT 说：本轮处理 Chevrolet Suburban 1947-1954 / Advance Design 段。
结论：本轮不新增全量表记录。
原因是我没有拿到可直接入库的完整 L / W / H。目前资料能确认：


1947-1955 First Series Suburban 基于 Advance Design 平台，在你的表里可作为 Suburban 的早期 gen1 处理。资料页显示该代 model years 为 1947-1955 First Series，平台为 Advance Design。维基百科


该代 Suburban 是 2-door carryall / panel truck / canopy express 口径，不是 Pickup，不建 cab / bed。维基百科


公开可读资料只明确给到 wheelbase 116 in 和 length 196.375 in，没有完整宽高，所以不能入库。维基百科


1954 官方规格手册目录里确实有 Truck Specifications、Chassis and Body Dimensions、Chassis Treads and Overall Widths 等页，但当前可读文本没有展开出 Suburban 的完整 L/W/H 表。chevy.oldcarmanualproject.com


本轮 TSV：
tsv主车型	年份区间	结构	品牌	前台车型	分类	版本	门数	代际	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态Chevrolet Suburban	1947-1954	Wagon / Utility	Chevrolet	Chevrolet Suburban	SUV		2	gen1				1947-1954 Chevrolet Suburban 3106/3116	Advance Design-based Suburban; 2-door carryall; rear panel doors 3106 / tailgate 3116	缺完整L/W/H，暂不入库
注意：这条只是 待补记录，不是可入库全量表。
Length 196.375 in 不能单独使用，因为没有 width / height，不满足你的入库规则。
当前待补状态：
tsv待补对象	当前问题	处理结果	下一步动作1947-1954 Advance Design Suburban	只确认wheelbase/length，缺width/height	不入库	继续找1954 Chevrolet Truck Specifications原始图片页或GM Heritage资料包
下一步处理 1955-1959 Task Force Suburban。目标同样是先找完整 L / W / H，如果只找到 wheelbase 或 length，也不进全量表。


--- Round 11 / 下一步回复 ---
本轮处理 Chevrolet Suburban 1955-1959 / Task Force 段。

结论：本轮不新增全量表记录。
原因是资料能确认这代 Suburban 的基本边界，但没有拿到完整 L / W / H，只确认到 wheelbase。

关键信息：

年份边界：1955 Second Series - 1959
平台：Task Force
结构：2-door carryall / 2-door panel truck
驱动：RWD / 4WD
wheelbase：114 in

这些信息可以用于建模，但不能直接入库，因为缺少完整 max_length_in / max_width_in / max_height_in。资料明确列出该代 Suburban model years 为 1955 Second Series-1959、body style 为 2-door carryall / panel truck、平台为 Task Force、wheelbase 为 114 in；但没有列出完整外部长宽高。
维基百科

本轮 TSV：

tsv
主车型	年份区间	结构	品牌	前台车型	分类	版本	门数	代际	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Chevrolet Suburban	1955-1959	Wagon / Utility	Chevrolet	Chevrolet Suburban	SUV		2	gen2				1955-1959 Chevrolet Suburban Task Force	需区分1955 Second Series；Task Force-based Suburban; 2-door carryall / panel truck; RWD/4WD; wheelbase 114 in	缺完整L/W/H，暂不入库

注意：1957 起有 4WD Suburban 口径，对应 3156 / 3166；但在没有完整 L/W/H 前，不拆 2WD/4WD 入全量表。资料也提到 1957 引入 4WD Suburban model numbers 3156 / 3166。
维基百科

当前 Chevrolet Suburban 进度：

tsv
区间	代际	当前状态	原因
1947-1954	gen1	待补	缺完整L/W/H
1955-1959	gen2	待补	缺完整L/W/H

下一步处理 1960-1966 Chevrolet Suburban / First-generation C/K-based 段。这段要特别注意：虽然是 C/K 平台，但仍然不按 Pickup 建 cab/bed；只在备注或子车系里体现 C/K 口径。


--- Round 12 / 下一步回复 ---
本轮处理 Chevrolet Suburban 1960-1966 / First-generation C/K-based 段。

结论：本轮不新增全量表记录。
原因是资料能确认这一代 Suburban 的平台、结构和年份边界，但没有拿到可直接入库的完整 L / W / H。

可以确认的信息：

年份区间：1960-1966
平台：First-generation C/K-based
结构：2-door Suburban / carryall / panel-style utility wagon
驱动：C-series 2WD；K-series 4WD
wheelbase：115 in 左右
特殊结构：Stageway 15-passenger conversion 不作为普通 Suburban 入库

这代 Suburban 是基于第一代 C/K truck 平台，1960 年引入新车身和独立前悬架，1964 年前挡风玻璃和门玻璃区域有更新；同时该系列首次提供工厂 4WD K-series 选项。但资料中没有逐条给出 C/K Suburban + 2WD/4WD + panel/tailgate 的完整外部长宽高，所以不能入库。
维基百科
+1

本轮 TSV：

tsv
主车型	年份区间	结构	品牌	前台车型	分类	版本	门数	代际	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Chevrolet Suburban	1960-1966	Wagon / Utility	Chevrolet	Chevrolet Suburban	SUV		2	gen3				1960-1966 Chevrolet Suburban C/K-based	First-generation C/K-based Suburban; 2-door utility wagon / panel-style body; C-series 2WD / K-series 4WD; wheelbase around 115 in; Stageway conversion excluded	缺完整L/W/H，暂不入库

当前 Chevrolet Suburban 进度：

tsv
区间	代际	当前状态	原因
1947-1954	gen1	待补	缺完整L/W/H
1955-1959	gen2	待补	缺完整L/W/H
1960-1966	gen3	待补	缺完整L/W/H

下一步处理 1967-1972 Chevrolet Suburban / Action-Line-based 段。这段资料相对更清楚：127 in wheelbase、C-20 Suburban、K-10/K-20 4WD 都要注意，但仍然必须拿到完整 L / W / H 才能入库。


--- Round 13 / 下一步回复 ---
本轮处理 Chevrolet Suburban 1967-1972 / Action-Line-based 段。

结论：本轮不新增全量表记录。
资料能确认这一代 Suburban 的年份、结构、平台、轴距和长度，但没有完整 W / H，所以不能入库。资料显示第六代 Suburban 为 1967-1972，平台为 C/K series，结构为 3-door station wagon 或 2-door panel truck，驱动为 RWD / 4WD。尺寸信息只明确给出 wheelbase 127 in 和 length 215.5 in，没有完整宽高。
维基百科

tsv
主车型	年份区间	结构	品牌	前台车型	分类	版本	门数	代际	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Chevrolet Suburban	1967-1972	Wagon / Utility	Chevrolet	Chevrolet Suburban	SUV		3	gen4	215.5			1967-1972 Chevrolet Suburban Action-Line	Action-Line-based Suburban; C/K platform; 3-door station wagon; RWD/4WD; wheelbase 127 in; C-20 introduced; K-10/K-20 4WD offered	缺完整W/H，暂不入库

建模注意点：

tsv
项目	结论
是否归入Pickup	否
是否建cab/bed	否
结构	Wagon / Utility
门数	3
版本	普通为空
代际	gen4
C10/K10/C20/K20	不进主车型；只作为数据库候选或备注
Panel Truck	1967-1970 可作为特殊结构/备注；1970后退出

补充：这一代首次引入 C-20 Suburban，同时提供 K-10/K-20 四驱；Action-Line Suburban 还有独特的“一侧单门、另一侧双门”三门结构。
维基百科
+1
 后驱 panel truck 版本在 1970 model year 后退出，所以如果后续数据库里有 Panel 候选，需要单独限制年份，不要默认覆盖 1971-1972。
维基百科

当前 Chevrolet Suburban 进度：

tsv
区间	代际	当前状态	原因
1947-1954	gen1	待补	缺完整L/W/H
1955-1959	gen2	待补	缺完整L/W/H
1960-1966	gen3	待补	缺完整L/W/H
1967-1972	gen4	待补	只有Length，缺Width/Height

下一步处理 1973-1991 Chevrolet Suburban / Rounded-Line 段。这段是四门 Suburban，和前面三门 Action-Line 不同，需要重新建模。


--- Round 14 / 下一步回复 ---
本轮处理 Chevrolet Suburban 1973-1991 / Rounded-Line 段。

结论：本轮不新增全量表记录。
这代确实是 Suburban 很关键的一代：1973 年改为四门 station wagon / SUV 结构，1973-1991 为 Rounded-Line Suburban；1987 年后因 C/K 命名让位给 GMT400，新旧平台重叠，所以改为 R/V 命名，直到 1991 年结束。资料能确认结构和年份边界，但我没有拿到可逐条入库的完整 L / W / H，因此不能入库。
维基百科
+2
维基百科
+2

tsv
主车型	年份区间	结构	品牌	前台车型	分类	版本	门数	代际	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Chevrolet Suburban	1973-1980	Wagon / Utility	Chevrolet	Chevrolet Suburban	SUV		4	gen5				1973-1980 Chevrolet Suburban Rounded-Line	Rounded-Line Suburban; 4-door truck-based station wagon; C/K platform; C10/K10/C20/K20 payload/drive口径只作备注或子车系候选; 1981前早期外观段	缺完整L/W/H，暂不入库
Chevrolet Suburban	1981-1986	Wagon / Utility	Chevrolet	Chevrolet Suburban	SUV		4	gen5				1981-1986 Chevrolet Suburban Rounded-Line facelift	Rounded-Line Suburban; 4-door SUV / truck-based station wagon; 1981 facelift后; C/K口径只作备注或子车系候选	缺完整L/W/H，暂不入库
Chevrolet Suburban	1987-1991	Wagon / Utility	Chevrolet	Chevrolet Suburban	SUV	R/V	4	gen5				1987-1991 Chevrolet R/V Suburban	R/V naming period; Rounded-Line Suburban; 1987为R/V命名边界; 1989前脸大改; 1991为Rounded-Line末年	缺完整L/W/H，暂不入库

建模结论：

tsv
项目	结论
主车型	Chevrolet Suburban
分类	SUV
结构	Wagon / Utility
是否建cab/bed	否
是否拆C10/K10/C20/K20	不拆主车型；只放备注或子车系对照
1973-1991是否一整段入库	否，缺完整L/W/H
是否需要拆1987-1991 R/V	需要，版本写 R/V
代际	gen5

本轮待补清单更新：

tsv
待补对象	当前问题	处理状态
1947-1954 Advance Design Suburban	缺完整L/W/H	继续待补
1955-1959 Task Force Suburban	缺完整L/W/H	继续待补
1960-1966 C/K-based Suburban	缺完整L/W/H	继续待补
1967-1972 Action-Line Suburban	只有Length，缺Width/Height	继续待补
1973-1980 Rounded-Line Suburban	缺完整逐结构L/W/H	继续待补
1981-1986 Rounded-Line facelift Suburban	缺完整逐结构L/W/H	继续待补
1987-1991 R/V Suburban	缺完整逐结构L/W/H	继续待补

下一步处理 1992-1999 Chevrolet Suburban / GMT400 段。这段资料相对更完整，有机会先做出可入库记录。


--- Round 15 / 下一步回复 ---
本轮处理 Chevrolet Suburban 1992-1999 / GMT400 段。

结论：本轮可以新增 2 条保守可入库记录，但不能覆盖整个 1992-1999。
资料明确给出 GMT400 Suburban 的完整外尺寸口径：Length 219.5 in、Width 77.0 in，并且高度范围标注了两个具体端点：1992-1994 1500 2WD = 68.8 in，1997-1999 2500 4WD = 74.6 in。所以这两个端点配置可以先入库；其他 1500 4WD、2500 2WD、1995-1996 等高度没有逐结构确认，继续待补。
维基百科

tsv
主车型	年份区间	结构	品牌	前台车型	分类	版本	门数	代际	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Chevrolet Suburban	1992-1994	Wagon / Utility	Chevrolet	Chevrolet Suburban	SUV		5	gen6	219.5	77.0	68.8	1992-1994 Chevrolet Suburban 1500 2WD	GMT400 Suburban; 5-door station wagon; 1500; 2WD; wheelbase 131.5 in	区间已核，可入库
Chevrolet Suburban	1997-1999	Wagon / Utility	Chevrolet	Chevrolet Suburban	SUV		5	gen6	219.5	77.0	74.6	1997-1999 Chevrolet Suburban 2500 4WD	GMT400 Suburban; 5-door station wagon; 2500; 4WD; wheelbase 131.5 in	区间已核，可入库

不能入库的部分：

tsv
待补对象	当前问题	处理状态
1992-1994 Suburban 1500 4WD	缺逐结构高度	继续待补
1992-1994 Suburban 2500 2WD/4WD	缺逐结构高度	继续待补
1995-1996 Suburban 1500/2500	资料有年度变化，但缺逐结构完整高度	继续待补
1997-1999 Suburban 1500 2WD/4WD	缺逐结构高度	继续待补
1997-1999 Suburban 2500 2WD	缺逐结构高度	继续待补

本轮状态更新：

本轮新增可入库：2 行
Chevrolet Suburban 当前可入库：2 行
Chevrolet Suburban 待补段：继续保留

建模结论：

tsv
项目	结论
主车型	Chevrolet Suburban
分类	SUV
结构	Wagon / Utility
是否建 cab/bed	否
C/K、1500、2500、2WD、4WD	不进主车型；写备注或后续子车系候选
1992-1999 是否整体入库	否，只能先入库已确认完整 L/W/H 的端点配置

下一步处理 2000-2006 Chevrolet Suburban / GMT800 段。这段资料通常更完整，优先查 1500 / 2500、2WD / 4WD 的完整 L/W/H。


--- Round 16 / 下一步回复 ---
本轮处理 Chevrolet Suburban 2000-2006 / GMT800 段。

结论：本轮暂不新增全量表记录。
原因是资料可以确认 GMT800 Suburban 的总尺寸范围，但还不能逐条对应到 Chevrolet Suburban 1500 / 2500 / 2WD / 4WD 的完整 L/W/H。

可确认信息：

tsv
项目	信息
年份	2000-2006
平台	GMT800
结构	5-door wagon / extended wagon
系列	1500 / 2500
轴距	130.0 in
长度	219.3 in
宽度	78.8-79.8 in
高度	73.3 in 到 77.1 in

资料明确：GMT800 Suburban 于 2000 model year 引入，分 1500 和 2500 两个系列；尺寸表给出 Length 219.3 in、Width 78.8-79.8 in，高度范围从 2000-02 Chevy 1500 4WD = 73.3 in 到 Yukon XL 2500 4WD = 77.1 in。但这里的宽度是范围，高度端点也混入 Yukon XL 2500 4WD，不是完整的 Chevrolet Suburban 逐结构表，所以不能直接入库。
维基百科
+2
维基百科
+2

本轮 TSV：

tsv
主车型	年份区间	结构	品牌	前台车型	分类	版本	门数	代际	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Chevrolet Suburban	2000-2006	Wagon / Utility	Chevrolet	Chevrolet Suburban	SUV		5	gen7	219.3			2000-2006 Chevrolet Suburban GMT800	GMT800 Suburban; 5-door wagon / extended wagon; 1500/2500; 2WD/4WD; wheelbase 130.0 in; width range 78.8-79.8; height range 73.3-77.1	缺逐结构W/H，暂不入库

本轮不能入库的原因拆开看：

tsv
待补对象	当前问题	处理结果	下一步动作
2000-2002 Suburban 1500 4WD	已知高度73.3，但宽度仍是78.8-79.8范围	暂不入库	继续找2000/2001/2002 Chevrolet Suburban 1500 4WD官方specs
2000-2006 Suburban 1500 2WD	缺对应高度	暂不入库	继续找1500 2WD完整L/W/H
2000-2006 Suburban 2500 2WD	缺对应高度	暂不入库	继续找2500 2WD完整L/W/H
2000-2006 Suburban 2500 4WD	高度端点引用到Yukon XL 2500 4WD，不能直接作为Chevrolet Suburban入库	暂不入库	继续找Chevrolet Suburban 2500 4WD完整L/W/H
2003-2006 Suburban 1500/2500	2003内饰更新、2005外观/配置更新、2006末年LTZ；未取得逐结构完整L/W/H	暂不入库	继续找2003/2005/2006官方specs

当前 Chevrolet Suburban 进度：

tsv
区间	代际	状态	原因
1947-1954	gen1	待补	缺完整L/W/H
1955-1959	gen2	待补	缺完整L/W/H
1960-1966	gen3	待补	缺完整L/W/H
1967-1972	gen4	待补	只有Length，缺Width/Height
1973-1991	gen5	待补	缺逐结构L/W/H
1992-1999	gen6	部分可入库	已确认2条端点配置
2000-2006	gen7	待补	只有总尺寸范围，缺逐结构W/H

下一步处理 2007-2014 Chevrolet Suburban / GMT900 段。这段通常有更清晰的 1500 / 2500 尺寸，优先看能不能形成可入库记录。


--- Round 17 / 下一步回复 ---
本轮处理 Chevrolet Suburban 2007-2014 / GMT900 段。

结论：本轮可以新增 1 条可入库记录。
资料明确给出第十代 Suburban 的 model years 为 2007-2014，平台为 GMT930 / GMT900，尺寸为 Length 222.4 in / Width 79.1 in / Height 76.8 in；Denali 高度 77.1 in 属于 GMC Yukon XL Denali，不作为 Chevrolet Suburban 普通记录。资料还说明 2500 Suburban 在 2013 年后停产，所以 2014 只按普通 Suburban 口径处理，不单独写 2500 版本。
维基百科
+1

tsv
主车型	年份区间	结构	品牌	前台车型	分类	版本	门数	代际	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Chevrolet Suburban	2007-2014	Wagon / Utility	Chevrolet	Chevrolet Suburban	SUV		4	gen8	222.4	79.1	76.8	2007-2014 Chevrolet Suburban GMT900	GMT900 / GMT930 Suburban; 4-door SUV; 1500/2500 body; 2500 public model discontinued after 2013; Denali excluded	区间已核，可入库

本轮不拆 1500 / 2500 的原因：

tsv
项目	处理
1500 / 2500	不进版本列
2WD / 4WD	不进版本列
Denali	排除，不属于 Chevrolet Suburban
2014 2500	不覆盖，2500 after 2013 discontinued
尺寸口径	按 Chevrolet Suburban 普通 GMT900 外尺寸 222.4 / 79.1 / 76.8

当前 Chevrolet Suburban 可入库进度：

tsv
区间	代际	新增/状态
1992-1994	gen6	已有 1 条可入库：1500 2WD
1997-1999	gen6	已有 1 条可入库：2500 4WD
2007-2014	gen8	本轮新增 1 条可入库

当前累计：

本轮新增可入库：1 行
Chevrolet Suburban 当前可入库：3 行

下一步处理 2015-2020 Chevrolet Suburban / K2XX 段。这段资料也有完整 L/W/H，预计可以继续新增可入库记录。


--- Round 18 / 下一步回复 ---
本轮处理 Chevrolet Suburban 2015-2020 / K2XX 段。

结论：本轮可以新增 1 条可入库记录。
资料明确第十一代 Suburban 为 2015-2020，并说明该代车身尺寸从上一代的 222.4 / 79.1 / 76.8 调整为 224.4 / 80.5 / 74.4，即长度增加、宽度增加、高度降低。这个尺寸可作为普通 Chevrolet Suburban K2XX 记录入库。
维基百科
+1

tsv
主车型	年份区间	结构	品牌	前台车型	分类	版本	门数	代际	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Chevrolet Suburban	2015-2020	Wagon / Utility	Chevrolet	Chevrolet Suburban	SUV		4	gen9	224.4	80.5	74.4	2015-2020 Chevrolet Suburban K2XX	K2XX Suburban; 4-door SUV; 1500 ordinary consumer model; 2WD/4WD not split; 3500HD fleet excluded	区间已核，可入库

本轮特殊处理：

tsv
项目	处理
Suburban 1500	作为普通 consumer model 入库
Suburban 3500HD	暂不并入普通记录
2WD / 4WD	不进版本列
LT / LTZ / Premier	不进版本列
GMC Yukon XL / Denali XL	排除，不属于 Chevrolet Suburban

Suburban 3500HD 需要单独待补：它是 K2 平台下的 fleet-only / Class 3 口径，2016 model year 引入，只提供 4WD，并且不是普通 1500 consumer model，不能混进普通 Suburban 记录。
维基百科

tsv
待补对象	当前问题	处理状态
2016-2020 Suburban 3500HD	特殊fleet/HD版本，缺单独完整L/W/H	继续待补，不并入普通Suburban

当前 Chevrolet Suburban 可入库进度：

tsv
区间	代际	状态
1992-1994	gen6	已入库：1500 2WD端点配置
1997-1999	gen6	已入库：2500 4WD端点配置
2007-2014	gen8	已入库：普通GMT900
2015-2020	gen9	本轮新增：普通K2XX

当前累计：

本轮新增可入库：1 行
Chevrolet Suburban 当前可入库：4 行

下一步处理 2021-2026 Chevrolet Suburban / T1XX 段。这段属于最新一代，需要核普通版与 Z71 / High Country 是否需要拆尺寸。


--- Round 19 / 下一步回复 ---
本轮处理 Chevrolet Suburban 2021-2026 / T1XX 段。

结论：本轮可以新增 1 条可入库记录。
第十二代 Suburban 从 2021 model year 开始，基于 GMT T1XX 平台；资料给出完整尺寸：Length 225.7 in / Width 81.1 in / Height 75.7 in / Wheelbase 134.1 in。2025 refresh 主要是前后造型、灯组、内饰屏幕、柴油机升级、科技配置等更新，没有看到外部长宽高变化，所以当前可按 2021-2026 普通 Suburban 记录入库。
维基百科
+1

tsv
主车型	年份区间	结构	品牌	前台车型	分类	版本	门数	代际	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Chevrolet Suburban	2021-2026	Wagon / Utility	Chevrolet	Chevrolet Suburban	SUV		4	gen10	225.7	81.1	75.7	2021-2026 Chevrolet Suburban T1XX	T1XX Suburban; 4-door full-size SUV; wheelbase 134.1 in; LS/LT/RST/Z71/Premier/High Country not split; 2025 refresh does not change L/W/H	区间已核，可入库

本轮特殊处理：

tsv
项目	处理
Z71	不单独拆尺寸；作为普通 Suburban 覆盖
RST	不单独拆尺寸；作为普通 Suburban 覆盖
Premier / High Country	不单独拆尺寸；配置名不进版本列
Duramax Diesel	动力不同，不拆尺寸
2025 refresh	外观/内饰/动力配置更新，不作为尺寸断点
GMC Yukon XL / Denali XL	排除，不属于 Chevrolet Suburban
Suburban Shield / HD SUV	军用/特殊用途，暂不并入普通 Suburban

当前 Chevrolet Suburban 可入库进度：

tsv
区间	代际	状态
1992-1994	gen6	已入库：1500 2WD端点配置
1997-1999	gen6	已入库：2500 4WD端点配置
2007-2014	gen8	已入库：普通GMT900
2015-2020	gen9	已入库：普通K2XX
2021-2026	gen10	本轮新增：普通T1XX

当前累计：

本轮新增可入库：1 行
Chevrolet Suburban 当前可入库：5 行

下一步整理 Chevrolet Suburban 当前保守可入库全量表 + 待补尺寸清单。


--- Round 20 / 下一步回复 ---
本轮整理 Chevrolet Suburban 当前保守可入库全量表 + 待补尺寸清单。

1. 当前保守可入库全量表 TSV
tsv
主车型	年份区间	结构	品牌	前台车型	分类	版本	门数	代际	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Chevrolet Suburban	1992-1994	Wagon / Utility	Chevrolet	Chevrolet Suburban	SUV		5	gen6	219.5	77.0	68.8	1992-1994 Chevrolet Suburban 1500 2WD	GMT400 Suburban; 5-door station wagon; 1500; 2WD; wheelbase 131.5 in	区间已核，可入库
Chevrolet Suburban	1997-1999	Wagon / Utility	Chevrolet	Chevrolet Suburban	SUV		5	gen6	219.5	77.0	74.6	1997-1999 Chevrolet Suburban 2500 4WD	GMT400 Suburban; 5-door station wagon; 2500; 4WD; wheelbase 131.5 in	区间已核，可入库
Chevrolet Suburban	2007-2014	Wagon / Utility	Chevrolet	Chevrolet Suburban	SUV		4	gen8	222.4	79.1	76.8	2007-2014 Chevrolet Suburban GMT900	GMT900 / GMT930 Suburban; 4-door SUV; 1500/2500 body; 2500 public model discontinued after 2013; Denali excluded	区间已核，可入库
Chevrolet Suburban	2015-2020	Wagon / Utility	Chevrolet	Chevrolet Suburban	SUV		4	gen9	224.4	80.5	74.4	2015-2020 Chevrolet Suburban K2XX	K2XX Suburban; 4-door SUV; 1500 ordinary consumer model; 2WD/4WD not split; 3500HD fleet excluded	区间已核，可入库
Chevrolet Suburban	2021-2026	Wagon / Utility	Chevrolet	Chevrolet Suburban	SUV		4	gen10	225.7	81.1	75.7	2021-2026 Chevrolet Suburban T1XX	T1XX Suburban; 4-door full-size SUV; wheelbase 134.1 in; LS/LT/RST/Z71/Premier/High Country not split; 2025 refresh does not change L/W/H	区间已核，可入库
2. 当前待补尺寸清单 TSV
tsv
待补对象	当前问题	处理状态
1947-1954 Advance Design Suburban	缺完整L/W/H	继续待补
1955-1959 Task Force Suburban	缺完整L/W/H	继续待补
1960-1966 C/K-based Suburban	缺完整L/W/H	继续待补
1967-1972 Action-Line Suburban	只有Length，缺Width/Height	继续待补
1973-1980 Rounded-Line Suburban	缺完整逐结构L/W/H	继续待补
1981-1986 Rounded-Line facelift Suburban	缺完整逐结构L/W/H	继续待补
1987-1991 R/V Suburban	缺完整逐结构L/W/H	继续待补
1992-1994 Suburban 1500 4WD	缺逐结构高度	继续待补
1992-1994 Suburban 2500 2WD/4WD	缺逐结构高度	继续待补
1995-1996 Suburban 1500/2500	缺逐结构完整高度	继续待补
1997-1999 Suburban 1500 2WD/4WD	缺逐结构高度	继续待补
1997-1999 Suburban 2500 2WD	缺逐结构高度	继续待补
2000-2006 GMT800 Suburban	只有总尺寸范围，缺逐结构W/H	继续待补
2016-2020 Suburban 3500HD	特殊fleet/HD版本，缺单独完整L/W/H	继续待补
3. 当前阶段状态
tsv
项目	结果
可入库全量表	5 行
L/W/H 缺失	0
断续年份区间	0
代际异常	0
待补尺寸清单	14 行

下一步生成 Chevrolet Suburban 子车系对照表。
只覆盖当前已入库年份区间：1992-1994 / 1997-1999 / 2007-2014 / 2015-2020 / 2021-2026。


--- Round 21 / 下一步回复 ---
ChatGPT 说：下一步是 Suburban 子车系对照表。我会只覆盖已入库年份段，并且保持你要求的 6 列；结构、版本默认留空，表示这些年份下通用匹配。本轮生成 Chevrolet Suburban 子车系对照表。
规则：
只覆盖当前可入库年份结构留空 = 匹配该年份所有结构版本留空 = 匹配该年份普通版本不把待补尺寸候选写进去不覆盖 Suburban 3500 HD / 未核 2500 / 未核 4WD

Chevrolet Suburban 子车系对照表 TSV
tsvYear	主车型	结构	版本	候选车型	匹配数量1992	Chevrolet Suburban			Chevrolet|C1500 Suburban	11993	Chevrolet Suburban			Chevrolet|C1500 Suburban	11994	Chevrolet Suburban			Chevrolet|C1500 Suburban	11997	Chevrolet Suburban			Chevrolet|K2500 Suburban	11998	Chevrolet Suburban			Chevrolet|K2500 Suburban	11999	Chevrolet Suburban			Chevrolet|K2500 Suburban	12007	Chevrolet Suburban			Chevrolet|Suburban 1500; Chevrolet|Suburban 2500	22008	Chevrolet Suburban			Chevrolet|Suburban 1500; Chevrolet|Suburban 2500	22009	Chevrolet Suburban			Chevrolet|Suburban 1500; Chevrolet|Suburban 2500	22010	Chevrolet Suburban			Chevrolet|Suburban 1500; Chevrolet|Suburban 2500	22011	Chevrolet Suburban			Chevrolet|Suburban 1500; Chevrolet|Suburban 2500	22012	Chevrolet Suburban			Chevrolet|Suburban 1500; Chevrolet|Suburban 2500	22013	Chevrolet Suburban			Chevrolet|Suburban 1500; Chevrolet|Suburban 2500	22014	Chevrolet Suburban			Chevrolet|Suburban; Chevrolet|Suburban 1500	22015	Chevrolet Suburban			Chevrolet|Suburban	12016	Chevrolet Suburban			Chevrolet|Suburban	12017	Chevrolet Suburban			Chevrolet|Suburban	12018	Chevrolet Suburban			Chevrolet|Suburban	12019	Chevrolet Suburban			Chevrolet|Suburban	12020	Chevrolet Suburban			Chevrolet|Suburban	12021	Chevrolet Suburban			Chevrolet|Suburban	12022	Chevrolet Suburban			Chevrolet|Suburban	12023	Chevrolet Suburban			Chevrolet|Suburban	12024	Chevrolet Suburban			Chevrolet|Suburban	12025	Chevrolet Suburban			Chevrolet|Suburban	12026	Chevrolet Suburban			Chevrolet|Suburban	1

本轮排除项
tsv年份/候选	排除原因1992-1994 Chevrolet|K1500 Suburban	当前只入库了1500 2WD端点尺寸，未核1500 4WD高度1992-1994 Chevrolet|C2500/K2500 Suburban	当前未入库2500完整逐结构尺寸1997-1999 Chevrolet|C1500/K1500 Suburban	当前只入库了2500 4WD端点尺寸，未核1500尺寸1997-1999 Chevrolet|C2500 Suburban	当前未核2500 2WD高度2016-2019 Chevrolet|Suburban 3500 HD	特殊HD/fleet版本，未入库2027 Chevrolet|Suburban	当前全量表只做到2026，暂不覆盖
当前 Suburban 阶段状态：
tsv表	行数	状态保守可入库全量表	5	完成子车系对照表	26	本轮完成待补尺寸清单	14	继续待补
下一步可以正式导出 Suburban 的 3 个 TSV：全量表、子车系对照表、待补清单。


--- Round 22 / 下一步回复 ---
ChatGPT 说：本轮正式导出 Chevrolet Suburban 的 3 个 TSV：保守可入库全量表、子车系对照表、待补尺寸清单。不生成 XLSX。Pythonfrom pathlib import Pathimport csvbase = Path("/mnt/data")# 1) 保守可入库全量表full_cols = [    "主车型", "年份区间", "结构", "品牌", "前台车型", "分类", "版本", "门数", "代际",    "max_length_in", "max_width_in", "max_height_in", "参考车型", "备注", "迭代状态"]full_rows = [    ["Chevrolet Suburban","1992-1994","Wagon / Utility","Chevrolet","Chevrolet Suburban","SUV","","5","gen6","219.5","77.0","68.8","1992-1994 Chevrolet Suburban 1500 2WD","GMT400 Suburban; 5-door station wagon; 1500; 2WD; wheelbase 131.5 in","区间已核，可入库"],    ["Chevrolet Suburban","1997-1999","Wagon / Utility","Chevrolet","Chevrolet Suburban","SUV","","5","gen6","219.5","77.0","74.6","1997-1999 Chevrolet Suburban 2500 4WD","GMT400 Suburban; 5-door station wagon; 2500; 4WD; wheelbase 131.5 in","区间已核，可入库"],    ["Chevrolet Suburban","2007-2014","Wagon / Utility","Chevrolet","Chevrolet Suburban","SUV","","4","gen8","222.4","79.1","76.8","2007-2014 Chevrolet Suburban GMT900","GMT900 / GMT930 Suburban; 4-door SUV; 1500/2500 body; 2500 public model discontinued after 2013; Denali excluded","区间已核，可入库"],    ["Chevrolet Suburban","2015-2020","Wagon / Utility","Chevrolet","Chevrolet Suburban","SUV","","4","gen9","224.4","80.5","74.4","2015-2020 Chevrolet Suburban K2XX","K2XX Suburban; 4-door SUV; 1500 ordinary consumer model; 2WD/4WD not split; 3500HD fleet excluded","区间已核，可入库"],    ["Chevrolet Suburban","2021-2026","Wagon / Utility","Chevrolet","Chevrolet Suburban","SUV","","4","gen10","225.7","81.1","75.7","2021-2026 Chevrolet Suburban T1XX","T1XX Suburban; 4-door full-size SUV; wheelbase 134.1 in; LS/LT/RST/Z71/Premier/High Country not split; 2025 refresh does not change L/W/H","区间已核，可入库"],]# 2) 子车系对照表mapping_cols = ["Year", "主车型", "结构", "版本", "候选车型", "匹配数量"]mapping_rows = [    ["1992","Chevrolet Suburban","","","Chevrolet|C1500 Suburban","1"],    ["1993","Chevrolet Suburban","","","Chevrolet|C1500 Suburban","1"],    ["1994","Chevrolet Suburban","","","Chevrolet|C1500 Suburban","1"],    ["1997","Chevrolet Suburban","","","Chevrolet|K2500 Suburban","1"],    ["1998","Chevrolet Suburban","","","Chevrolet|K2500 Suburban","1"],    ["1999","Chevrolet Suburban","","","Chevrolet|K2500 Suburban","1"],    ["2007","Chevrolet Suburban","","","Chevrolet|Suburban 1500; Chevrolet|Suburban 2500","2"],    ["2008","Chevrolet Suburban","","","Chevrolet|Suburban 1500; Chevrolet|Suburban 2500","2"],    ["2009","Chevrolet Suburban","","","Chevrolet|Suburban 1500; Chevrolet|Suburban 2500","2"],    ["2010","Chevrolet Suburban","","","Chevrolet|Suburban 1500; Chevrolet|Suburban 2500","2"],    ["2011","Chevrolet Suburban","","","Chevrolet|Suburban 1500; Chevrolet|Suburban 2500","2"],    ["2012","Chevrolet Suburban","","","Chevrolet|Suburban 1500; Chevrolet|Suburban 2500","2"],    ["2013","Chevrolet Suburban","","","Chevrolet|Suburban 1500; Chevrolet|Suburban 2500","2"],    ["2014","Chevrolet Suburban","","","Chevrolet|Suburban; Chevrolet|Suburban 1500","2"],    ["2015","Chevrolet Suburban","","","Chevrolet|Suburban","1"],    ["2016","Chevrolet Suburban","","","Chevrolet|Suburban","1"],    ["2017","Chevrolet Suburban","","","Chevrolet|Suburban","1"],    ["2018","Chevrolet Suburban","","","Chevrolet|Suburban","1"],    ["2019","Chevrolet Suburban","","","Chevrolet|Suburban","1"],    ["2020","Chevrolet Suburban","","","Chevrolet|Suburban","1"],    ["2021","Chevrolet Suburban","","","Chevrolet|Suburban","1"],    ["2022","Chevrolet Suburban","","","Chevrolet|Suburban","1"],    ["2023","Chevrolet Suburban","","","Chevrolet|Suburban","1"],    ["2024","Chevrolet Suburban","","","Chevrolet|Suburban","1"],    ["2025","Chevrolet Suburban","","","Chevrolet|Suburban","1"],    ["2026","Chevrolet Suburban","","","Chevrolet|Suburban","1"],]# 3) 待补尺寸清单pending_cols = ["待补对象", "当前问题", "处理状态"]pending_rows = [    ["1947-1954 Advance Design Suburban","缺完整L/W/H","继续待补"],    ["1955-1959 Task Force Suburban","缺完整L/W/H","继续待补"],    ["1960-1966 C/K-based Suburban","缺完整L/W/H","继续待补"],    ["1967-1972 Action-Line Suburban","只有Length，缺Width/Height","继续待补"],    ["1973-1980 Rounded-Line Suburban","缺完整逐结构L/W/H","继续待补"],    ["1981-1986 Rounded-Line facelift Suburban","缺完整逐结构L/W/H","继续待补"],    ["1987-1991 R/V Suburban","缺完整逐结构L/W/H","继续待补"],    ["1992-1994 Suburban 1500 4WD","缺逐结构高度","继续待补"],    ["1992-1994 Suburban 2500 2WD/4WD","缺逐结构高度","继续待补"],    ["1995-1996 Suburban 1500/2500","缺逐结构完整高度","继续待补"],    ["1997-1999 Suburban 1500 2WD/4WD","缺逐结构高度","继续待补"],    ["1997-1999 Suburban 2500 2WD","缺逐结构高度","继续待补"],    ["2000-2006 GMT800 Suburban","只有总尺寸范围，缺逐结构W/H","继续待补"],    ["2016-2020 Suburban 3500HD","特殊fleet/HD版本，缺单独完整L/W/H","继续待补"],]def write_tsv(path, cols, rows):    with path.open("w", encoding="utf-8-sig", newline="") as f:        writer = csv.writer(f, delimiter="\t", lineterminator="\n")        writer.writerow(cols)        writer.writerows(rows)full_path = base / "chevrolet_suburban_import_ready_conservative_full.tsv"mapping_path = base / "chevrolet_suburban_submodel_mapping.tsv"pending_path = base / "chevrolet_suburban_remaining_dimension_gaps.tsv"write_tsv(full_path, full_cols, full_rows)write_tsv(mapping_path, mapping_cols, mapping_rows)write_tsv(pending_path, pending_cols, pending_rows)# 校验missing_lwh = [r for r in full_rows if not r[9] or not r[10] or not r[11]]bad_interval = [r for r in full_rows if ";" in r[1]]bad_gen = [r for r in full_rows if r[8] not in {"gen1","gen2","gen3","gen4","gen5","gen6","gen7","gen8","gen9","gen10"}]print("Suburban TSV 已生成")print(f"全量表: {full_path} 行数={len(full_rows)}")print(f"子车系对照: {mapping_path} 行数={len(mapping_rows)}")print(f"待补清单: {pending_path} 行数={len(pending_rows)}")print(f"L/W/H缺失={len(missing_lwh)}; 断续年份区间={len(bad_interval)}; 代际异常={len(bad_gen)}")STDOUT/STDERRSuburban TSV 已生成
全量表: /mnt/data/chevrolet_suburban_import_ready_conservative_full.tsv 行数=5
子车系对照: /mnt/data/chevrolet_suburban_submodel_mapping.tsv 行数=26
待补清单: /mnt/data/chevrolet_suburban_remaining_dimension_gaps.tsv 行数=14
L/W/H缺失=0; 断续年份区间=0; 代际异常=0
本轮已正式导出 Chevrolet Suburban 的 3 个 TSV：











校验结果：
全量表行数：5子车系对照：26剩余待补：14L/W/H 缺失：0断续年份区间：0代际异常：0
当前 Suburban 阶段可以按这版保守表入库；后续找到待补年份的完整 L/W/H 后，再追加或扩展区间。


--- Round 23 / 下一步回复 ---
下一步我开始 Chevrolet Tahoe 建模第 1 轮：确定主车型边界。

本轮结论

Chevrolet Tahoe 应该作为独立主车型，不并入 Chevrolet Suburban，也不并入 Chevrolet C/K。

但有一个关键边界：1992-1994 的 Chevrolet 全尺寸两门 SUV 仍叫 Blazer，不应直接归入 Chevrolet Tahoe。资料说明 GMC Yukon 在 1992 model year 接替 K5 Jimmy，而 Chevrolet 继续直接归入 Chevrolet Tahoe**。资料说明 GMC Yukon 在使用 Blazer 名称到 1994；到 199
维基百科
hevrolet Tahoe。citeturn372550search4

Chevrolet Tahoe 第一轮建模 TSV
tsv
主车型	分类	结构	是否皮卡	是否需要驾驶室类型	是否需要货斗长度	建模结论
Chevrolet Tahoe	SUV	Wagon / Utility	否	否	否	独立主车型；不归入Suburban/C/K；不建cab/bed；1992-1994 Chevrolet Blazer不并入Tahoe
初步代际切分
tsv
主车型	年份区间	分类	结构	版本	代际	代际说明	建模状态
Chevrolet Tahoe	1995-2000	SUV	Wagon / Utility		gen1	GMT400 Tahoe	待取L/W/H
Chevrolet Tahoe	2000-2006	SUV	Wagon / Utility		gen2	GMT800 Tahoe	待取L/W/H
Chevrolet Tahoe	2007-2014	SUV	Wagon / Utility		gen3	GMT900 Tahoe	待取L/W/H
Chevrolet Tahoe	2015-2020	SUV	Wagon / Utility		gen4	K2XX Tahoe	待取L/W/H
Chevrolet Tahoe	2021-2026	SUV	Wagon / Utility		gen5	T1XX Tahoe	待取L/W/H

说明：

tsv
项目	结论
1992-1994 Chevrolet Blazer	不并入Tahoe，另做Blazer/Full-Size Blazer
1995 Tahoe	正式进入Tahoe主车型
Suburban关系	同平台但短轴，不并入Suburban
C/K关系	GMT400来源平台，不作为主车型
2-door Tahoe	需要后续核年份和尺寸，不能默认与4-door合并
Z71 / RST / Premier / High Country	先不进版本列，除非尺寸不同
Police / PPV / SSV	特殊用途，后续单独判断是否排除或待补

GMT400 平台资料也列出 GMT420 = 1995-2000 Chevrolet Tahoe，并说明 T
维基百科
400 的 SUV 派生车型。citeturn372550search3

下一步处理 1995-2000 Chevrolet Tahoe / GMT400段，重点先拆 2-door / 4-door，再找完整 L/W/H。


--- Round 24 / 下一步回复 ---
本轮处理 Chevrolet Tahoe 1995-2000 / GMT400 段。

结论：本轮可以新增 2 条可入库记录，但不把 2000 Limited / Z71 直接并入普通 Tahoe。

资料能确认第一代 Tahoe / Yukon 的完整尺寸：

2-door：188 in / 77 in / 72 in
4-door：199 in / 77 in / 72 in

并且资料明确：Tahoe 在 1995 年由全尺寸 Blazer 改名而来，1995 年同时加入 4-door 版本；2-door Tahoe 到 1999 年结束，2000 年 GMT400 平台只保留 Tahoe Limited / Tahoe Z71 特别版。
维基百科

tsv
主车型	年份区间	结构	品牌	前台车型	分类	版本	门数	代际	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Chevrolet Tahoe	1995-1999	Wagon / Utility	Chevrolet	Chevrolet Tahoe	SUV		2	gen1	188	77	72	1995-1999 Chevrolet Tahoe 2-door GMT400	GMT400 Tahoe; 2-door SUV; 2WD/4WD not split; diesel 2-door 4WD not split	区间已核，可入库
Chevrolet Tahoe	1995-1999	Wagon / Utility	Chevrolet	Chevrolet Tahoe	SUV		4	gen1	199	77	72	1995-1999 Chevrolet Tahoe 4-door GMT400	GMT400 Tahoe; 4-door SUV; 2WD/4WD not split; ordinary base/LS/LT trims	区间已核，可入库

2000 年不直接并入上面两条：

tsv
待补对象	当前问题	处理状态
2000 Tahoe Limited	特殊版，Z60/police-style lowered chassis，车身高度可能不同	继续待补，不并入普通Tahoe
2000 Tahoe Z71	特殊版，4WD Z71，需单独确认完整L/W/H	继续待补，不并入普通Tahoe
2000 GMT800 Tahoe	下一代平台，单独在2000-2006段处理	下一轮处理

当前 Tahoe 可入库进度：

tsv
区间	代际	状态
1995-1999	gen1	本轮新增：2-door / 4-door 两条

当前累计：

本轮新增可入库：2 行
Chevrolet Tahoe 当前可入库：2 行

下一步处理 2000-2006 Chevrolet Tahoe / GMT800 段。这段要单独建 gen2，不能和 2000 GMT400 Limited / Z71 混在一起。


--- Round 25 / 下一步回复 ---
本轮处理 Chevrolet Tahoe 2000-2006 / GMT800 段。

结论：本轮暂不新增可入库记录。
原因是资料能确认 GMT800 Tahoe 的年份、平台、结构和部分尺寸，但 Length 存在分段变化，Height 只给范围 74.2-76.7 in，没有明确对应到具体 2WD / 4WD / trim / 年份。所以不能直接生成一条完整安全的全量表记录。资料显示第二代 Tahoe 为 2000-2006、4-door SUV、GMT800 平台，尺寸为 wheelbase 116.0 in、width 78.9 in，但长度分为 198.9 / 196.9 / 198.8 in，高度是范围值。
维基百科

tsv
主车型	年份区间	结构	品牌	前台车型	分类	版本	门数	代际	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Chevrolet Tahoe	2000-2006	Wagon / Utility	Chevrolet	Chevrolet Tahoe	SUV		4	gen2		78.9		2000-2006 Chevrolet Tahoe GMT800	GMT800 Tahoe; 4-door SUV; wheelbase 116.0 in; length varies 198.9/196.9/198.8; height range 74.2-76.7; 2WD/4WD高度未逐项确认	缺完整逐结构L/H，暂不入库

本轮拆分判断：

tsv
待补对象	当前问题	处理结果	下一步动作
2000-2001 GMT800 Tahoe	长度资料为198.9，但高度只给范围	暂不入库	继续找2000/2001 Chevrolet Tahoe 2WD/4WD完整L/W/H
2001-2003 GMT800 Tahoe	长度资料为196.9，但高度只给范围	暂不入库	继续找2002/2003 Chevrolet Tahoe完整L/W/H
2003-2006 GMT800 Tahoe	长度资料为198.8，但高度只给范围	暂不入库	继续找2004/2005/2006 Chevrolet Tahoe完整L/W/H
2000 GMT400 Tahoe Limited/Z71	特殊上一代GMT400车型，不并入GMT800	继续待补	单独找Limited/Z71完整L/W/H

当前 Tahoe 进度：

tsv
区间	代际	状态
1995-1999	gen1	已入库：2-door / 4-door 两条
2000-2006	gen2	待补，缺逐结构完整高度

当前累计：

本轮新增可入库：0 行
Chevrolet Tahoe 当前可入库：2 行

下一步处理 2007-2014 Chevrolet Tahoe / GMT900 段。这一段资料中有完整 Length / Width，但 Height 仍可能是范围，需要判断能否保守入库或继续待补。


--- Round 26 / 下一步回复 ---
本轮处理 Chevrolet Tahoe 2007-2014 / GMT900 段。

结论：本轮暂不新增可入库记录。
原因是资料能确认 GMT900 Tahoe 的完整 Length / Width，但 Height 仍是范围值 74.6-77.0 in，没有明确对应到普通版、Hybrid、2WD、4WD、PPV/SSV 或具体年份。你的规则是每条全量表必须有明确 L/W/H，所以不能直接入库。资料显示第三代 Tahoe 为 GMT900 平台，尺寸为 Length 202.0 in / Width 79.0 in / Height 74.6-77.0 in。
维基百科

tsv
主车型	年份区间	结构	品牌	前台车型	分类	版本	门数	代际	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Chevrolet Tahoe	2007-2014	Wagon / Utility	Chevrolet	Chevrolet Tahoe	SUV		4	gen3	202.0	79.0		2007-2014 Chevrolet Tahoe GMT900	GMT900 Tahoe; 4-door SUV; wheelbase 116.0 in; height range 74.6-77.0; 2WD/4WD/Hybrid/PPV/SSV高度未逐项确认	缺明确H，暂不入库

本轮拆分判断：

tsv
待补对象	当前问题	处理结果	下一步动作
2007-2014 GMT900 Tahoe 普通版	Length/Width明确，但Height只有74.6-77.0范围	暂不入库	继续找2007/2010/2014 Chevrolet Tahoe普通版完整L/W/H
2008-2013 Tahoe Hybrid	Hybrid有独立动力/重量口径，可能高度不同	暂不入库	单独找Hybrid完整尺寸
2007-2014 Tahoe PPV / SSV	警用/特殊服务版，悬架和高度可能不同	暂不入库	特殊版本单独待补
2007-2014 Tahoe Z71	越野套件可能影响高度口径	暂不入库	如数据库/前台需要，再单独核

当前 Tahoe 进度：

tsv
区间	代际	状态
1995-1999	gen1	已入库：2-door / 4-door 两条
2000-2006	gen2	待补，缺逐结构完整高度
2007-2014	gen3	本轮待补，缺明确高度

当前累计：

本轮新增可入库：0 行
Chevrolet Tahoe 当前可入库：2 行

下一步处理 2015-2020 Chevrolet Tahoe / K2XX 段。这段资料给出了明确 203.9 / 80.5 / 74.4，预计可以新增可入库记录。


--- Round 27 / 下一步回复 ---
本轮处理 Chevrolet Tahoe 2015-2020 / K2XX 段。

结论：本轮可以新增 1 条可入库记录。
资料明确给出第四代 Tahoe 的 model years 为 2015-2020，结构为 4-door SUV，平台为 GMTK2XX / K2UC，完整尺寸为 Length 203.9 in / Width 80.5 in / Height 74.4 in；Denali 的 77.1 in 是 GMC Yukon Denali，不并入 Chevrolet Tahoe 普通记录。
维基百科

tsv
主车型	年份区间	结构	品牌	前台车型	分类	版本	门数	代际	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Chevrolet Tahoe	2015-2020	Wagon / Utility	Chevrolet	Chevrolet Tahoe	SUV		4	gen4	203.9	80.5	74.4	2015-2020 Chevrolet Tahoe K2XX	K2XX Tahoe; 4-door SUV; K2UC; 2WD/4WD not split; LS/LT/LTZ/Premier not split; GMC Yukon/Yukon Denali excluded	区间已核，可入库

本轮特殊处理：

tsv
项目	处理
2WD / 4WD	不拆，普通Tahoe尺寸统一覆盖
LS / LT / LTZ / Premier	配置名，不进版本列
Z71	先不拆，除非后续找到尺寸差异
RST	2018起外观/套件口径，先不拆尺寸
PPV / SSV	警用/特殊服务版，悬架高度可能不同，暂不并入普通记录
GMC Yukon / Yukon Denali	排除，不属于 Chevrolet Tahoe
Cadillac Escalade	排除

当前 Tahoe 可入库进度：

tsv
区间	代际	状态
1995-1999	gen1	已入库：2-door / 4-door 两条
2000-2006	gen2	待补，缺逐结构完整高度
2007-2014	gen3	待补，缺明确高度
2015-2020	gen4	本轮新增：普通K2XX

当前累计：

本轮新增可入库：1 行
Chevrolet Tahoe 当前可入库：3 行

下一步处理 2021-2026 Chevrolet Tahoe / T1XX 段。这段需要核普通版、Z71、High Country、RST 是否尺寸一致。


--- Round 28 / 下一步回复 ---
本轮处理 Chevrolet Tahoe 2021-2026 / T1XX 段。

结论：本轮可以新增 1 条可入库记录。
第五代 Tahoe 从 2021 model year 开始，平台为 GMT T1XX，车身为 4-door SUV，资料给出完整尺寸：Length 210.7 in / Width 81.1 in / Height 75.7 in / Wheelbase 120.9 in。2025 facelift 是前后造型、灯组、内饰屏幕、柴油机输出、拖拽科技等更新，没有看到 L/W/H 变化，所以当前可按 2021-2026 普通 Tahoe 记录入库。
维基百科
+1

tsv
主车型	年份区间	结构	品牌	前台车型	分类	版本	门数	代际	max_length_in	max_width_in	max_height_in	参考车型	备注	迭代状态
Chevrolet Tahoe	2021-2026	Wagon / Utility	Chevrolet	Chevrolet Tahoe	SUV		4	gen5	210.7	81.1	75.7	2021-2026 Chevrolet Tahoe T1XX	T1XX Tahoe; 4-door full-size SUV; wheelbase 120.9 in; LS/LT/RST/Z71/Premier/High Country not split; Duramax not split; 2025 refresh does not change L/W/H	区间已核，可入库

本轮特殊处理：

tsv
项目	处理
Z71	不单独拆尺寸；作为普通 Tahoe 覆盖
RST	不单独拆尺寸；作为普通 Tahoe 覆盖
Premier / High Country	配置名，不进版本列
Duramax Diesel	动力不同，不拆尺寸
Air Ride / Magnetic Ride	悬架配置可能影响实际高度，但资料未给独立外尺寸；先不拆
PPV / SSV	警用/特殊服务版，悬架/高度可能不同，暂不并入普通记录
GMC Yukon / Yukon Denali	排除，不属于 Chevrolet Tahoe
Cadillac Escalade	排除
2025 refresh	作为中期改款，不作为尺寸断点

当前 Tahoe 可入库进度：

tsv
区间	代际	状态
1995-1999	gen1	已入库：2-door / 4-door 两条
2000-2006	gen2	待补，缺逐结构完整高度
2007-2014	gen3	待补，缺明确高度
2015-2020	gen4	已入库：普通K2XX
2021-2026	gen5	本轮新增：普通T1XX

当前累计：

本轮新增可入库：1 行
Chevrolet Tahoe 当前可入库：4 行

下一步整理 Chevrolet Tahoe 当前保守可入库全量表 + 待补尺寸清单。

