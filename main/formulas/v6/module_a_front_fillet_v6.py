# -*- coding: utf-8 -*-
"""

============================================================
🏭 a 工廠：外徑+斜角 角度往負向R角版本(模版)

============================================================
"""

import math


def solve_a(data):


    # ==================================================
    # 1️⃣ 讀取並整理輸入（對齊 Excel B 系列）
    # --------------------------------------------------
    # 說明：
    # - 所有輸入皆轉為 float
    # - 外徑一律轉為半徑計算
    # ==================================================
    B101  = float(data["大徑X"])
    B102  = float(data["小徑X"])
    B103  = float(data["角度2"])
    B104  = float(data["終端X"]) 
    B105  = float(data["原點至斜度角W"])   
    B106  = float(data["原點至終點面W"])

    B4  = B101 / 2.0
    B5  = -abs(float(data["原點至斜度角W"]) )
    B6  = float(data["角度1"])
    B7  = B102 / 2.0
    B8  = float(data["前端R1"])
    B9  = float(data["前端R2"])
    B10 = float(data["刀鼻半徑"]) *2
   
    if B6 <= 0 or B6 >= 90:
        raise ValueError("角度-1 不可小於 0度 ~ 大於 90 度")
    if B103 <= 0 or B103 >= 90:
        raise ValueError("角度-2 不可小於 0度 ~ 大於 90 度")  
    if  B102 >= B101:
        raise ValueError(" 前端D 不可小於或等於 中端D")         
    if  B102 >= B104:
        raise ValueError(" 中端D 不可大於或等於 終端X") 
    if  B105 >= B106:
        raise ValueError(" 斜度角W 不可大於或等於 斜角W2")                  
     # ======== 基礎三角運算（E欄公式）========
    E4 = B10 / 2.0                     # 刀鼻半徑
    E5 = math.sin(math.radians(B6))    # sin(角度)
    E6 = math.cos(math.radians(B6))    # cos(角度)
    E7 = math.tan(math.radians(B6))    # tan(角度)
    E8 = math.tan(math.radians(B6)/2)  # tan(角度/2)

    # ======== 計算過程中間值 ========
    E9 = B5 + (B7 - B4) / E7            # 斜角與小徑延伸交點 Z

    # ======== 幾何運算的中間座標（H欄）========
    H4  = B5 + B8 * E8                  # R前端 Z位置
    H5  = B4 - B8 * (1.0 - E6)          # R前端 X位置
    H6  = B5 - B8 * (E5 - E8)           # R前端 Z位置延伸
    H8  = E9 - B9 * E8                  # 後端 R 座標用
    H9  = B7 + B9 * (1.0 - E6)          # 小徑交界 X
    H10 = E9 + B9 * (E5 - E8)           # 小徑交界 Z

    # ======== 最終輸出（對應 Excel B13~B20）========
    B13 = B4 + E4                       # 左側點 X
    B51 = (B13-E4)*2
    B14 = H4                            # 左側點 Z
    B52 = B14-E4 
    B15 = H5 + E4 * E6                  # R點 X 修正
    B53 = (B15-E4)*2
    B16 = H6 - E4 * E5                  # R點 Z 修正
    B54 = B16-E4 
    B17 = H9 + E4 * E6                  # 右側點 X
    B55 = (B17-E4)*2
    B18 = H10 - E4 * E5                 # 右側點 Z
    B56 = B18-E4
    B19 = B7 + E4                       # 小徑右側 X
    B57 = (B19-E4)*2
    B20 = H8                            # 小徑延伸 Z
    B58 = B20-E4
    B59 = B9-E4
    B60 = B8+E4
    B61 = B9-E4

    def _fmt(x):
     # 例如固定顯示到小數點兩位
        return f"{x:.3f}"

 

    result_values = {
         "B51": B51,
         "B52": B52,
         "B53": B53,
         "B54": B54,
         "B55": B55,
         "B56": B56,
         "B57": B57,
         "B58": B58,
         "B59": B59,
         "B60": B60,
         "B61": B61,
     }

    text_lines = [
        "➡️ 前端斜角 → 平線 → 終點弧（C 工廠）",
        f"B51 = {_fmt(B51)}",
        f"B52 = {_fmt(B52)}",
        f"B53 = {_fmt(B53)}",
        f"B54 = {_fmt(B54)}",
        f"B55 = {_fmt(B55)}",
        f"B56 = {_fmt(B56)}",
        f"B57 = {_fmt(B57)}",
        f"B58 = {_fmt(B58)}",
        f"B59 = {_fmt(B59)}",
        f"B60 = {_fmt(B60)}",
        f"B61 = {_fmt(B61)}",
    ]

    return {
        "ok": True,
        "text_lines": text_lines,
        "values": result_values,
    }


# -------------------------------------------------------
# 🔁 對外統一介面
# -------------------------------------------------------
def solve(data: dict):
    return solve_a(data)