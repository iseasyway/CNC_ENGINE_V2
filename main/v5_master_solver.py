# -*- coding: utf-8 -*-
"""
v5_master_solver.py — V5 正式版（合併後）
============================================================
角色定位：
- V5幾何系統唯一入口（取代 v5_solver.py）
- 同時負責：
  1️⃣ 調度 A / B / C / D 四大模組
  2️⃣ 輸出組裝（保持原本 v1_solver.py 的輸出格式）

注意：
- 本檔案完全取代 v5_solver.py
- router 只需 import 這裡的 run_all_modules_with_output
============================================================
"""

import importlib



# ----------------------------------------------------------
# 📦 指定目前使用的公式版本
# ----------------------------------------------------------
FORMULA_VERSION = "v5"
formula_path = f"main.formulas.{FORMULA_VERSION}"

# ----------------------------------------------------------
# 📦 動態載入四大加工廠（v1）
# ----------------------------------------------------------
module_a = importlib.import_module(
    f"{formula_path}.module_a_front_fillet_v5"
)
module_b = importlib.import_module(
    f"{formula_path}.module_b_outer_perp_R_v5"
)
module_c = importlib.import_module(
    f"{formula_path}.module_c_front_slope_endline_arc_v5"
)



# ==========================================================
# 🧠 主調度流程：A → B → C → D
# ==========================================================
def run_all_modules(data: dict):
    """
    調度 V5 四大模組，並將最終結果回傳
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

   

    return results



# ==========================================================
# ⭐ V5 專用輸出（完全保留原 v1_solver.py 的格式）
# ==========================================================
def _render_output_v5(results: dict) -> str:

    A = results.get("A", {})
    B = results.get("B", {})
    C = results.get("C", {})
    

    def g(dic, key, default=0):
        return dic.get(key, default)

    html = ""
    html += "=== 🧩 刀點座標總表 ===\n\n"

    
    html += f"G1 X{g(A,'B51'):.3f} F0.1 🔴\n"
    html += f"G1 Z{g(A,'B52'):.3f} F0.1 🔴\n"
    html += f"G1 X{g(B,'B55'):.3f} Z{g(B,'B56'):.3f} F0.1🟡\n"
    html += f"G02 X{g(B,'B57'):.3f} Z{g(B,'B58'):.3f} R{g(B,'B59'):.3f} F0.1🟡\n"
    html += f"G1 Z{g(C,'B52'):.3f} F0.1⚫\n"
    html += f"G02 X{g(C,'B54'):.3f} Z{g(C,'B53'):.3f} R{g(C,'B55'):.3f} F0.1⚫\n\n"

    html += "=== ⭐ 幾何運算完成 ==="

    return html



# ==========================================================
# 🌐 Web 用入口（router 叫這個）
# ==========================================================
def run_all_modules_with_output(data: dict) -> str:
    results = run_all_modules(data)
    return _render_output_v5(results)



# ==========================================================
# 🛠 熱更新（開發用）
# ==========================================================
def reload_all():
    importlib.reload(module_a)
    importlib.reload(module_b)
    importlib.reload(module_c)
    
