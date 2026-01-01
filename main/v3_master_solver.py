# -*- coding: utf-8 -*-
"""
V3 Master Solver（最終正式版）
"""

import importlib

FORMULA_VERSION = "v3"
formula_path = f"main.formulas.{FORMULA_VERSION}"

module_a = importlib.import_module(f"{formula_path}.module_a_escape_groove_v3")
module_b = importlib.import_module(f"{formula_path}.module_b_simple_arc_v3")


# ======================================================
# 🧠 主運算流程（A → B）
# ======================================================
def run_all_modules(data: dict):

    # -------------------------
    # A 工廠（專用資料包）
    # -------------------------
    data_A = {
        "K1_A": data["K1_A"],   # 小徑 X
        "K2_A": data["K2_A"],   # Z 原點 → 起始距離
        "K3_A": data["K3_A"],   # R角
        "K4": data["K4"],     # 刀鼻半徑（共用）
    }

    # -------------------------
    # B 工廠（專用資料包）
    # -------------------------
    data_B = {
        "K1_B": data["K1_B"],   # 終點外徑 X
        "K2_B": data["K2_B"],   # R角
        "K4":   data["K4"],     # 刀鼻半徑（共用）
    }

    # -------------------------
    # 執行 A、B 工廠
    # -------------------------
    res_a = module_a.solve(data_A)
    res_b = module_b.solve(data_B)

    return {
        "A": res_a["values"],
        "B": res_b["values"],
    }


# ======================================================
# 🟢 專門給 Web 的輸出格式
# ======================================================
def run_all_v3_modules_with_output(data: dict) -> str:

    results = run_all_modules(data)
    A = results["A"]
    B = results["B"]

    L_value = A.get("Z_END", 0)       # A 工廠的 Z_END
    B51_value = B.get("Z_END", 0)   # B 工廠的 Z_END
    # 計算差值
    diff_L_B51 = L_value + B51_value
    # 存成新的結果
    results["AB"] = {
    "L_minus_B51": diff_L_B51
    }


    def g(dic, key): 
        return dic.get(key, 0)

    html = ""
    html += "=== 🧩 刀點座標總表 ===\n\n"

    # -------------------------
    # A 工廠輸出
    # -------------------------

    html += f"G1 X{g(A,'X_START'):.3f} F0.1🔴\n"
    html += f"G1 Z{g(A,'Z_START'):.3f} F0.1🔴\n"

    html += f"G02X{g(A,'X_END'):.3f} Z{g(A,'Z_END'):.3f} R{g(A,'R_AFTER'):.3f} F0.1🟡 \n"
     # -------------------------
    # B 工廠輸出
    # -------------------------
    
    html += f"G1 X{g(B,'X_START'):.3f} F0.1⚫\n"
    AB = results.get("AB", {})
    html += f"G03 X{g(B,'X_END'):.3f} Z{AB.get('L_minus_B51', 0):.3f} R{g(B,'R_AFTER'):.3f} F0.1 🔵\n\n"
   
    html += "=== ⭐ 幾何運算完成 ==="

    return html
