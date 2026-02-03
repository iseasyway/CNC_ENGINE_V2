# -*- coding: utf-8 -*-


import importlib



# ----------------------------------------------------------
# 📦 指定目前使用的公式版本
# ----------------------------------------------------------
FORMULA_VERSION = "id3"
formula_path = f"main.formulas.{FORMULA_VERSION}"

# ----------------------------------------------------------
# 📦 動態載入四大加工廠（v1）
# ----------------------------------------------------------
module_a = importlib.import_module(
    f"{formula_path}.module_a_lnside_angle"
)
module_b = importlib.import_module(
    f"{formula_path}.module_b_solve_r_fillet_x"
)
module_c = importlib.import_module(
    f"{formula_path}.module_c_solve_r_fillet_z"
)
module_d = importlib.import_module(
    f"{formula_path}.module_d_Rendpoint"
)
module_e = importlib.import_module(
    f"{formula_path}.module_e_Front_center"
)
module_f = importlib.import_module(
    f"{formula_path}.module_f_Back center"
)



# ==========================================================
# 🧠 主調度流程：A → B → C → D
# ==========================================================
def run_all_modules(data: dict):
    """
    調度 id3 四大模組，並將最終結果回傳
    """
    results = {}
    data = data.copy()  # 避免污染原輸入

    # ----- B 工廠 -----
    res_b = module_b.solve(data) or {}
    results["B"] = res_b.get("values", {})
    data["B"] = results["B"]  # C 工廠要用

    # ----- C 工廠 -----
    res_c = module_c.solve(data)or {}
    results["C"] = res_c.get("values", {})
    data["C"] = results["C"]  # C 工廠要用

    # ----- A 工廠 -----
    res_a = module_a.solve(data) or {}
    results["A"] = res_a.get("values", {})
    data["A"] = results["A"]  

    # ----- E 工廠 -----
    res_e = module_e.solve(data) or {}
    results["E"] = res_e.get("values", {})
    data["E"] = results["E"] 

    # ----- F 工廠 -----
    res_f = module_f.solve(data) or {}
    results["F"] = res_f.get("values", {})
    data["F"] = results["F"]  

    

    # ----- D 工廠 -----
    res_d = module_d.solve(data) or {}
    results["D"] = res_d.get("values", {})
    data["D"] = results["D"]  



    return results



# ==========================================================
# ⭐ V4 專用輸出（完全保留原 v1_solver.py 的格式）
# ==========================================================
def _render_output_id3(results: dict) -> str:

    A = results.get("A", {})
    B = results.get("B", {})
    C = results.get("C", {})
    D = results.get("D", {})
    E = results.get("E", {})
    F = results.get("F", {})

    def g(dic, key, default=0):
        return dic.get(key, default)

    html = ""
    html += "=== 🧩 刀點座標總表 ===\n\n"
  

    html += f"G0 X{g(D,'R1X'):.3f} Z2.🔴\n"
    html += f"G1 Z{g(D,'R1Z'):.3f} F0.1🔴\n"
    
    html += f"G02 X{g(D,'R2X'):.3f} Z-{g(D,'R2Z'):.3f} R{g(D,'R1R'):.3f} F0.1🔴\n"
    html += f"G1 X{g(D,'R3X'):.3f} Z{g(D,'R3Z'):.3f} F0.1🟡\n"
    html += f"G02 X{g(D,'R4X'):.3f} Z{g(D,'R4Z'):.3f} R{g(D,'R2R'):.3f} F0.1🟡\n\n"
    
      
    html += "=== ⭐ 幾何運算完成 ==="

    return html



# ==========================================================
# 🌐 Web 用入口（router 叫這個）
# ==========================================================
def run_all_modules_with_output(data: dict) -> str:
    results = run_all_modules(data)
    return _render_output_id3(results)



# ==========================================================
# 🛠 熱更新（開發用）
# ==========================================================
def reload_all():
    importlib.reload(module_a)
    importlib.reload(module_b)
    importlib.reload(module_c)
    importlib.reload(module_d)
    importlib.reload(module_e)
    importlib.reload(module_f)