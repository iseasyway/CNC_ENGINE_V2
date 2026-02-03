# -*- coding: utf-8 -*-
"""

============================================================


============================================================
"""

import math


def solve_e(data):
    # ===============================
    # 輸入端（圖面角度）
    # ===============================
    r  = float(data["刀鼻半徑"]) 
    theta_deg  = float(data["角度"])


    # ===============================
    # 角度鎖定（核心）
    # ===============================
    if theta_deg <= 0 or theta_deg >= 90:
        raise ValueError("角度 theta 必須大於 0 度且小於 90 度")

    # ===============================
    # 計算（固定公式，不玩花樣）
    # ===============================
    theta = math.radians(theta_deg)

    X = r * math.sin(theta)
    Z = r * math.cos(theta)

    e01=X
    e02=Z


    def _fmt(x):
    # 例如固定顯示到小數點兩位
        return f"{x:.3f}"
    
    result_values = {
        "e01": e01,
        "e02": e02,
          
     }

    text_lines = [
        "➡️ 前端斜角 → 平線 → 終點弧（C 工廠）",
        f"e01 = {_fmt(e01)}",
        f"e02 = {_fmt(e02)}",
        
      
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
    return solve_e(data)
