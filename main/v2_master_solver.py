# -*- coding: utf-8 -*-
"""
v2_master_solver.py
============================================================
🧠 航母中央大腦（V2 版本）

角色定位：
- 作為 V2 幾何計算的「唯一總入口」
- 統一調度 V2 模組（module_a / module_b）
- 控制模組執行順序與資料流向
- 提供 app.py / router 呼叫的穩定介面

設計原則：
- 本檔案不寫任何幾何公式
- 不相依 v1 模組
- 只負責「調度、串接、整合」
============================================================
"""

import importlib

# ------------------------------------------------------
# 🔧 指定目前使用的公式版本（V2）
# ------------------------------------------------------
FORMULA_VERSION = "v2"
formula_path = f"main.formulas.{FORMULA_VERSION}"


# ------------------------------------------------------
# 📦 動態匯入 V2 模組（只剩 A / B）
# ------------------------------------------------------
module_a = importlib.import_module(
    f"{formula_path}.module_a_escape_groove_v2"
)
module_b = importlib.import_module(
    f"{formula_path}.module_b_simple_arc_v2"
)


# ==========================================================
# 🧠 主運算流程：整合 A → B
# ==========================================================
def run_all_modules(user_inputs: dict):
    """
    主運算流程（V2）：

    輸入：
    - user_inputs：由前端傳入的原始參數 dict

    流程：
    1️⃣ 複製輸入資料，避免污染原始資料
    2️⃣ 執行 A → B
    3️⃣ 收集各模組回傳的 values
    4️⃣ 回傳完整結果 dict

    輸出：
    - results = {
        "A": {...},
        "B": {...}
      }
    """

    # --------------------------------------------------
    # 建立內部資料副本
    # --------------------------------------------------
    data = user_inputs.copy()

    results = {}

    # --------------------------
    # 🏭 A 模組（Escape Groove）
    # --------------------------
    res_a = module_a.solve(data)
    results["A"] = res_a.get("values", {})

    # 若 B 需要 A 的結果（保留擴充彈性）
    data["A"] = results["A"]

    # --------------------------
    # 🏭 B 模組（Simple Arc）
    # --------------------------
    res_b = module_b.solve(data)
    results["B"] = res_b.get("values", {})

    return results


# ==========================================================
# 🔥 統一輸出格式（結果 dict → HTML）
# ==========================================================
def _render_output_v2(results: dict) -> str:

    A = results.get("A", {})
    B = results.get("B", {})


    L_value = A.get("L", 0)       # A 工廠的 L
    B51_value = B.get("B51", 0)   # B 工廠的 B51
    # 計算差值
    diff_L_B51 = L_value + B51_value
    # 存成新的結果
    results["AB"] = {
    "L_minus_B51": diff_L_B51
    }


    def g(dic, key, default=0):
        return dic.get(key, default)

    html = ""
    html += "=== 🧩 刀點座標總表 ===\n\n"

    # ===========================
    #      A 工廠（Escape Groove）
    # ===========================
    html += f"G0 X{g(A,'B51'):.3f}🔴\n"
    html += f"G0 Z{g(A,'D4'):.3f}🔴\n\n"
    

    # ===========================
    #      B 工廠（Simple Arc）
    # ===========================
  
    #html += f"B51 = {g(B,'B51'):.3f}\n\n"

    AB = results.get("AB", {})
    html += f"G1 X{g(A,'K1'):.3f} Z-{AB.get('L_minus_B51', 0):.3f} F0.1🟡\n\n"
    html += "=== ⭐ 幾何運算完成 ===\n\n"
    html += "<span style='color:red; font-weight:bold;'>⚠ 請至機床確認座標圖形 ⚠</span>";

    return html


# ==========================================================
# 🛠 開發模式：動態熱更新
# ==========================================================
def reload_all():
    """
    重新載入 V2 模組
    （開發階段使用，避免重啟 FastAPI）
    """
    importlib.reload(module_a)
    importlib.reload(module_b)
# ==========================================================
# 🌐 Web / API 專用入口（V2）
# ==========================================================
def run_all_v2_modules_with_output(data: dict) -> str:
    results = run_all_modules(data)
    return _render_output_v2(results)
