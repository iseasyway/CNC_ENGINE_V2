# -*- coding: utf-8 -*-


import importlib



# ----------------------------------------------------------
# 📦 指定目前使用的公式版本
# ----------------------------------------------------------
FORMULA_VERSION = "id1"
formula_path = f"main.formulas.{FORMULA_VERSION}"

# ----------------------------------------------------------
# 📦 動態載入四大加工廠（v1）
# ----------------------------------------------------------
module_a = importlib.import_module(
    f"{formula_path}.module_a_angle_leve_z"
)
module_b = importlib.import_module(
    f"{formula_path}.module_b_angle_vertica_x"
)
module_c = importlib.import_module(
    f"{formula_path}.module_c_lnside_angle"
)



# ==========================================================
# 🧠 主調度流程：A → B → C → D
# ==========================================================
def run_all_modules(data: dict):
    """
    調度 id1 四大模組，並將最終結果回傳
    """
    results = {}
    data = data.copy()  # 避免污染原輸入

    # ----- A 工廠 -----
    res_a = module_a.solve(data) or {}
    results["A"] = res_a.get("values", {})
    data["A"] = results["A"]  # C 工廠要用

    # ----- B 工廠 -----
    res_b = module_b.solve(data) or {}
    results["B"] = res_b.get("values", {})
    data["B"] = results["B"]  # C 工廠要用

    # ----- C 工廠 -----
    res_c = module_c.solve(data)or {}
    results["C"] = res_c.get("values", {})



    return results



# ==========================================================
# ⭐ V4 專用輸出（完全保留原 v1_solver.py 的格式）
# ==========================================================
def _render_output_id1(results: dict) -> str:

    A = results.get("A", {})
    B = results.get("B", {})
    C = results.get("C", {})
  

    def g(dic, key, default=0):
        return dic.get(key, default)

    html = ""
    html += "=== 🧩 刀點座標總表 ===\n\n"
       
    html += f"G0 X{g(C,'C5'):.3f} Z2.🔴\n"
    html += f"G1 Z{g(C,'C4'):.3f} F0.1🔴\n\n"
    html += f"G1 X{g(C,'C3'):.3f} Z{g(C,'C6'):.3f} F0.1🟡\n\n"
      
    html += "=== ⭐ 幾何運算完成 ===\n\n"
    html += "<span style='color:red; font-weight:bold;'>⚠ 請至機床確認座標圖形 ⚠</span>";

    return html



# ==========================================================
# 🌐 Web 用入口（router 叫這個）
# ==========================================================
def run_all_modules_with_output(data: dict) -> str:
    results = run_all_modules(data)
    return _render_output_id1(results)



# ==========================================================
# 🛠 熱更新（開發用）
# ==========================================================
def reload_all():
    importlib.reload(module_a)
    importlib.reload(module_b)
    importlib.reload(module_c)
 