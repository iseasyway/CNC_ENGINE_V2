# -*- coding: utf-8 -*-
#(7)
import math


def solve_a(data):
 
    # ========= 1️⃣ 基本讀值 =========
    B101  = float(data["大徑X"])  
    B102  = float(data["小徑X"]) 
    B103  = -abs(float(data["工件原點至終點面W"]) )    
   
    B4  = B101/ 2.0
    B5  = -abs(float(data["工件原點至斜度角W"]) )
    B6  = float(data["角度"])
    B7  = B102 / 2.0
    B8 = float(data["刀鼻半徑"])


    if B6 <= 0 or B6 >= 90:
        raise ValueError("角度 A-A 不可小於 0度 ~ 大於 90 度") 
    if  B102 >= B101:
        raise ValueError(" 小徑d 不可大於或等於 大徑D")        
    if  B5 <= B103:
        raise ValueError(" 斜度角W 不可大於或等於 終點面W") 


    E4 = B8 
    E7 = math.tan(math.radians(B6) / 2.0)
    E8 = B5 + (B7 - B4) / math.tan(math.radians(B6))
   
    B11 = B4 + E4
    B12 = B5 - E4 * E7
    B14 = B7 + E4
    B15 = E8 - E4 * E7
   
   
    B51 = (B11-B8)*2
    B52 = B12-B8
    B53 = (B14-B8)*2
    B54 = B15-B8
 
    def _fmt(x):
        # 例如固定顯示到小數點兩位
        return f"{x:.3f}"

    result_values = {
         "B51": B51,
         "B52": B52,
         "B53": B53,
         "B54": B54,
     }

    text_lines = [
        "➡️ 前端斜角 → 平線 → 終點弧（C 工廠）",
        f"B51 = {_fmt(B51)}",
        f"B52 = {_fmt(B52)}",
        f"B53 = {_fmt(B53)}",
        f"B54 = {_fmt(B54)}",
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


