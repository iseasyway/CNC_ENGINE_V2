# -*- coding: utf-8 -*-
"""

============================================================

============================================================
"""

import importlib

# ----------------------------------------------------------
# 📦 指定目前使用的公式版本
# ----------------------------------------------------------
FORMULA_VERSION = "v7"
formula_path = f"main.formulas.{FORMULA_VERSION}"

# ----------------------------------------------------------
# 📦 動態載入四大加工廠（v7）
# ----------------------------------------------------------
module_a = importlib.import_module(
    f"{formula_path}.module_a_front_fillet"
)
module_b = importlib.import_module(
    f"{formula_path}.module_b_outer_perp_R"
)
module_c_1 = importlib.import_module(
    f"{formula_path}.module_c_1"
)
module_c_2 = importlib.import_module(
    f"{formula_path}.module_c_2"
)

module_c = importlib.import_module(
    f"{formula_path}.module_c_front_slope_endline_arc_v1"
)
module_d = importlib.import_module(
    f"{formula_path}.module_d_angle_to_z_offset"
)



# ==========================================================
# 🧠 主調度流程：A → B → C → D
# ==========================================================
def run_all_modules(data: dict):
    """
    調度 V1 四大模組，並將最終結果回傳
    """
    results = {}
    data = data.copy()  # 避免污染原輸入

    # ----- c_1 工廠 -----
    res_c_1 = module_c_1.solve(data)or {}
    results["c_1"] = res_c_1.get("values", {})
    data["c_1"] = results["c_1"]  # C 工廠要用

    res_c_2 = module_c_2.solve(data)or {}
    results["c_2"] = res_c_2.get("values", {})
    data["c_2"] = results["c_2"]  # C 工廠要用  

    # ----- A 工廠 -----
    res_a = module_a.solve(data) or {}
    results["A"] = res_a.get("values", {})
    data["A"] = results["A"]  # C 工廠要用

    # ----- B 工廠 -----
    res_b = module_b.solve(data)or {}
    results["B"] = res_b.get("values", {})


    # ----- C 工廠 -----
    res_c = module_c.solve(data)or {}
    results["C"] = res_c.get("values", {})

    # ----- D 工廠 -----
    res_d = module_d.solve(data)or {}
    results["D"] = res_d.get("values", {})

    return results



# ==========================================================
# 
# ==========================================================
def _render_output_v7(results: dict) -> str:
    c_1 = results.get("c_1", {})
    c_2 = results.get("c_2", {})
    A = results.get("A", {})
    B = results.get("B", {})
    C = results.get("C", {})
    D = results.get("D", {})

    def g(dic, key, default=0):
        return dic.get(key, default)

    html = ""
    html += "=== 🧩 刀點座標總表 ===\n\n"

    # ===== 前端 R 角 =====
    
    html += f"G0 X{g(B,'B51'):.3f} Z2. 🔴\n"
    html += f"G1 Z{g(B,'B52'):.3f} F0.1🔴\n"
    html += f"G03 X{g(B,'B53'):.3f} Z{g(B,'B54'):.3f} R{g(B,'B55'):.3f} F0.1🔴\n\n"
   

    html += f"G1 X{g(C,'B53'):.3f} Z{g(C,'B54'):.3f} F0.1🟡\n"
    html += f"G03 X{g(C,'B55'):.3f} Z{g(C,'B56'):.3f} R{g(C,'B5'):.3f} F0.1🟡\n\n"
    
    #html += f"前端R角刀鼻補正    \n\n"

    # ===== 未端 R 角 =====
    html += f"G1 X{g(D,'B52'):.3f} Z{g(D,'D51'):.3f} F0.1⚫\n"
    #html += f"未端R角起始點      \n\n"

    html += f"G03 X{g(D,'B53'):.3f} Z{g(D,'B54'):.3f} R{g(D,'B55'):.3f} F0.1⚫\n\n"
    #html += f"未端R角終點        \n"
    #html += f"刀鼻補正後圓孤     \n\n"

    # ===== 外徑圓弧補正 =====
   
    #html += f"圓孤後z座標:       \n"
    #html += f"刀鼻補正後圓孤:    \n\n"

    html += "=== ⭐ 幾何運算完成 ==="

    return html



# ==========================================================
# 🌐 Web 用入口（router 叫這個）
# ==========================================================
def run_all_modules_with_output(data: dict) -> str:
    results = run_all_modules(data)
    return _render_output_v7(results)



# ==========================================================
# 🛠 熱更新（開發用）
# ==========================================================
def reload_all():
    importlib.reload(module_c_1)
    importlib.reload(module_c_2)
    importlib.reload(module_a)
    importlib.reload(module_b)
    importlib.reload(module_c)
    importlib.reload(module_d)
   
