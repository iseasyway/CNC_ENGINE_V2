# -*- coding: utf-8 -*-
"""
master_solver.py
航母中央大腦：統一調度四大加工廠 A / B / C / D
提供給 app.py 使用的唯一運算入口
"""

import importlib

# 四大加工廠（模組）
from main.formulas import (
    module_a_front_fillet,
    module_b_outer_perp_R,
    module_c_front_slope_endline_arc_v1,
    module_d_angle_to_z_offset,
)


# ===========================================================
# 🧠 主運算：整合 A + B + C + D 四間加工廠
# ===========================================================
def run_all_modules(user_inputs: dict):
    """
    user_inputs = {
        "前端x軸外徑": ,
        "斜度長": ,
        "角度": ,
        "前端R角": ,
        "未端R角": ,
        "刀鼻半徑": ,
        "z軸長度": ,
        "R角": ,
        "斜度x起始點":
    }
    """

    data = user_inputs.copy()
    results = {}

    # ------------------------------------------------------
    # A 工廠：前端 R角斜度
    # ------------------------------------------------------
    res_a = module_a_front_fillet.calc_front_fillet_from_direct_inputs(data)
    results["A"] = res_a.get("values", {})
    data["A"] = results["A"]   # 給 C 工廠使用

    # ------------------------------------------------------
    # B 工廠：外圓垂直端 R角
    # ------------------------------------------------------
    res_b = module_b_outer_perp_R.solve(data)
    results["B"] = res_b.get("values", {})

    # ------------------------------------------------------
    # C 工廠：斜角 → 平線 → 終點弧
    # ------------------------------------------------------
    res_c = module_c_front_slope_endline_arc_v1.solve(data)
    results["C"] = res_c.get("values", {})

    # ------------------------------------------------------
    # D 工廠：角度 Z軸距離
    # ------------------------------------------------------
    res_d = module_d_angle_to_z_offset.solve_b14(
        data["角度"], data["刀鼻半徑"]
    )
    results["D"] = res_d.get("values", {})

    return results


# ===========================================================
# 🔥 提供 app.py 呼叫的格式化輸出（字典 → HTML）
# ===========================================================
def render_output(results: dict) -> str:
    """
    將四工廠計算結果轉換成 HTML 顯示格式
    """

    html = ["<pre>"]

    for key, val in results.items():
        html.append(f"🔹 {key} 工廠結果：")
        for k, v in val.items():
            html.append(f"  {k} = {v}")
        html.append("")  # 空行

    html.append("</pre>")
    return "\n".join(html)


# ===========================================================
# 🛠 開發模式：自動熱更新所有模組（給 app.py 用）
# ===========================================================
def reload_all():
    importlib.reload(module_a_front_fillet)
    importlib.reload(module_b_outer_perp_R)
    importlib.reload(module_c_front_slope_endline_arc_v1)
    importlib.reload(module_d_angle_to_z_offset)
