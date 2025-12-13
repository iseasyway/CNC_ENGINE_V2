# -*- coding: utf-8 -*-
"""
v1_solver.py — 航母主控版
整合四大幾何工廠：A、B、C、D
可給 Web / API / 本地使用
"""

import importlib
from main.formulas import (
    module_a_front_fillet,
    module_b_outer_perp_R,
    module_c_front_slope_endline_arc_v1,
    module_d_angle_to_z_offset,
)

# ===========================================================
#  主運算：跑 A → B → C → D
# ===========================================================
def run_all_modules(data):

    results = {}

    print("\n=== 🚀 開始執行所有幾何工廠 ===\n")

    # -------------------------------------------------------
    # A 工廠
    # -------------------------------------------------------
    print("【A】前端 R角斜度計算：")

    res_a = module_a_front_fillet.solve_a(data)

    for line in res_a["text_lines"]:
        print("   " + line)

    results["A"] = res_a["values"]
    print()

    # -------------------------------------------------------
    # B 工廠
    # -------------------------------------------------------
    print("【B】外徑接垂直角 R 計算：")

    res_b = module_b_outer_perp_R.solve(data)

    for line in res_b["text_lines"]:
        print("   " + line)

    results["B"] = res_b["values"]
    print()

    # -------------------------------------------------------
    # C 工廠（會需要 A 的輸出 B7）
    # -------------------------------------------------------
    print("【C】斜角 → 平線 → 終點弧 計算：")

    data["A"] = results["A"]

    res_c = module_c_front_slope_endline_arc_v1.solve(data)

    for line in res_c["text_lines"]:
        print("   " + line)

    results["C"] = res_c["values"]
    print()

    # -------------------------------------------------------
    # D 工廠
    # -------------------------------------------------------
    print("【D】角度 Z軸距離 B14：")

    res_d = module_d_angle_to_z_offset.solve(data)

    for line in res_d["text_lines"]:
        print("   " + line)

    results["D"] = res_d["values"]
    print()

    print("=== ✅ 所有工廠完成 ===")
    return results


# ===========================================================
#  轉成 Web（HTML）輸出用
# ===========================================================
# ===========================================================
#  轉成 Web（HTML）輸出用（刀點座標總表）
# ===========================================================
def run_all_modules_with_output(data):

    importlib.reload(module_a_front_fillet)
    importlib.reload(module_b_outer_perp_R)
    importlib.reload(module_c_front_slope_endline_arc_v1)
    importlib.reload(module_d_angle_to_z_offset)

    results = run_all_modules(data)

    A = results.get("A", {})
    B = results.get("B", {})
    C = results.get("C", {})
    D = results.get("D", {})

    # 安全取值用工具
    def g(dic, key, default=0):
        return dic.get(key, default)

    # 🔧 刀鼻半徑
    R_tool = data.get("刀鼻半徑", 0)

    # 組成輸出 HTML（與你手機截圖格式完全相同）
    html = ""
    html += "=== 🧩 刀點座標總表 ===\n\n"

    # --- 前端 R 起點 ---
    html += f"前端R角起始點  X={g(A,'B21'):.3f}\n"
    html += f"前端R角起始點  Z={g(A,'B22'):.3f}\n\n"

    # --- 前端 R 終點 ---
    html += f"前端R角終點    X={g(A,'B42'):.3f}\n"
    html += f"前端R角終點    Z={g(A,'B43'):.3f}\n"
    html += f"前端R角刀鼻補正 R={g(A,'B44'):.3f}\n\n"

    # --- 未端 R 起點 ---
    html += f"未端R角起始點  X={g(C,'E3'):.3f}\n"
    html += f"未端R角起始點  Z={g(C,'E2'):.3f}\n\n"

    # --- 未端 R 終點 ---
    html += f"未端R角終點    X={g(C,'E5'):.3f}\n"
    html += f"未端R角終點    Z={g(C,'E4'):.3f}\n"
    html += f"刀鼻補正後圓孤 R={g(C,'E6'):.3f}\n\n"

    # --- 圓弧資訊（B 工廠） ---
    html += f"圓孤R前端 z={g(B,'OUT_E3'):.3f}\n\n"
    html += f"圓孤後x座標: X={g(B,'OUT_E7'):.3f}\n"
    html += f"圓孤後z座標: Z={g(B,'OUT_E6'):.3f}\n"
    html += f"刀鼻補正後圓孤: R={g(B,'OUT_E9'):.3f}\n\n"

    html += "=== 🟢 幾何運算完成 ==="

    return html
