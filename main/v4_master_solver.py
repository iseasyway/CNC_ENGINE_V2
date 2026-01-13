# -*- coding: utf-8 -*-
"""
v4_master_solver.py — V4 正式版（合併後）
============================================================
角色定位：
- V4 幾何系統唯一入口（取代 v4_solver.py）
- 同時負責：
  1️⃣ 調度 A / B / C / D 四大模組
  2️⃣ 輸出組裝（保持原本 v1_solver.py 的輸出格式）

注意：
- 本檔案完全取代 v4_solver.py
- router 只需 import 這裡的 run_all_modules_with_output
============================================================
"""

import importlib



# ----------------------------------------------------------
# 📦 指定目前使用的公式版本
# ----------------------------------------------------------
FORMULA_VERSION = "v4"
formula_path = f"main.formulas.{FORMULA_VERSION}"

# ----------------------------------------------------------
# 📦 動態載入四大加工廠（v1）
# ----------------------------------------------------------
module_a = importlib.import_module(
    f"{formula_path}.module_a_front_fillet_v4"
)
module_b = importlib.import_module(
    f"{formula_path}.module_b_outer_perp_R_v4"
)
module_c = importlib.import_module(
    f"{formula_path}.module_c_front_slope_endline_arc_v4"
)
module_d = importlib.import_module(
    f"{formula_path}.module_d_front_slope_endline_arc_v4"
)



# ==========================================================
# 🧠 主調度流程：A → B → C → D
# ==========================================================
def run_all_modules(data: dict):
    """
    調度 V4 四大模組，並將最終結果回傳
    """
    results = {}
    data = data.copy()  # 避免污染原輸入

    # ----- A 工廠 -----
    res_a = module_a.solve(data)
    results["A"] = res_a.get("values", {})
    data["A"] = results["A"]  # C 工廠要用

    # ----- B 工廠 -----
    res_b = module_b.solve(data)
    results["B"] = res_b.get("values", {})

    # ----- C 工廠 -----
    res_c = module_c.solve(data)
    results["C"] = res_c.get("values", {})

    # ----- D 工廠 -----
    res_d = module_d.solve(data)
    results["D"] = res_d.get("values", {})
    

    return results



# ==========================================================
# ⭐ V4 專用輸出（完全保留原 v1_solver.py 的格式）
# ==========================================================
def _render_output_v4(results: dict) -> str:

    A = results.get("A", {})
    B = results.get("B", {})
    C = results.get("C", {})
    D = results.get("D", {})

    def g(dic, key, default=0):
        return dic.get(key, default)

    html = ""
    html += "=== 🧩 刀點座標總表 ===\n\n"

    # ===== 前端 R 角 =====
    html += f"G0 X{g(A,'B21'):.3f} Z2. 🔴\n"
    html += f"G1 Z{g(A,'B22'):.3f} F0.1🔴\n\n"

    html += f"G03 X{g(A,'B42'):.3f} Z{g(A,'B43'):.3f} R{g(A,'B44'):.3f} F0.1🔴\n"
    #html += f"前端R角刀鼻補正    \n\n"

    # ===== 未端 R 角 =====
    html += f"G1 X{g(C,'E3'):.3f} Z{g(C,'E2'):.3f} F0.1🟡\n"
    #html += f"未端R角起始點      \n\n"

    html += f"G03 X{g(C,'E5'):.3f} Z{g(C,'E4'):.3f} R{g(C,'E6'):.3f} F0.1🟡\n"
    #html += f"未端R角終點        \n"
    #html += f"刀鼻補正後圓孤     \n\n"

    # ===== 外徑圓弧補正 =====
    html += f"G1 Z{g(B,'OUT_B52'):.3f} F0.1⚫\n\n"
    html += f"G02 X{g(B,'OUT_B54'):.3f} Z{g(B,'OUT_B53'):.3f} R{g(B,'OUT_B55'):.3f} F0.1⚫\n"
    #html += f"圓孤後z座標:       \n"
    #html += f"刀鼻補正後圓孤:    \n\n"

   # ===== 外徑圓弧補正 =====
    html += f"G1 X{D['D43']:.3f} Z{D['D44']:.3f} F0.1🔵\n\n"
    
    #html += f"圓孤後z座標:       \n"
    #html += f"刀鼻補正後圓孤:    \n\n"


    html += "=== ⭐ 幾何運算完成 ==="

    return html



# ==========================================================
# 🌐 Web 用入口（router 叫這個）
# ==========================================================
def run_all_modules_with_output(data: dict) -> str:
    results = run_all_modules(data)
    return _render_output_v4(results)



# ==========================================================
# 🛠 熱更新（開發用）
# ==========================================================
def reload_all():
    importlib.reload(module_a)
    importlib.reload(module_b)
    importlib.reload(module_c)
    importlib.reload(module_d)
