# -*- coding: utf-8 -*-
"""
module_b_simple_arc_v2.py
============================================================
🏭 V2 - B 工廠｜Simple Arc（正式版）

角色定位：
- 根據「角度 + 半徑」計算圓弧起始 X 位移
- 純幾何工具型模組
- 不依賴其他工廠（A / C / D）

輸入（由 v2_router / v2_solver 傳入）：
- K2：角度（度）
- K5：刀鼻半徑

輸出：
- B51：X 位移量
============================================================
"""

import math

DISPLAY_DECIMALS = 3


# ----------------------------------------------------------
# 原始公式核心（你提供的版本，完全保留）
# ----------------------------------------------------------
def solve_simple_arc(angle_deg, radius):
    t = math.tan(math.radians(angle_deg))      # B5
    s = math.sqrt(1.0 + t * t)                 # B6
    B9  = radius * (s - 1.0) / t               # B9
    B12 = B9 - radius                          # B12
    B14 = abs(B12)                             # B14
    return B14


# ----------------------------------------------------------
# 🏭 V2 標準入口
# ----------------------------------------------------------
def solve(data: dict):
    """
    V2 B 工廠標準入口（正式版）

    data 需包含：
      K2：角度
      K5：刀鼻半徑
    """

    # ========= 讀取正式參數 =========
    K2 = data.get("K2")   # 角度
    K5 = data.get("K5")   # 刀鼻半徑

    if K2 is None or K5 is None:
        raise ValueError("B 工廠錯誤：K2(角度) 與 K5(刀鼻半徑) 必須輸入")

    angle = float(K2)
    radius = float(K5)

  

    # ========= 呼叫公式核心 =========
    B51 = solve_simple_arc(angle, radius)

    # ========= 回傳正式版格式 =========
    return {
        "ok": True,
        "values": {
            "B51": B51,
        },
        "text_lines": [
            "B 工廠（Simple Arc v2）完成",
            f"B51 = {B51:.{DISPLAY_DECIMALS}f}",
        ]
    }
