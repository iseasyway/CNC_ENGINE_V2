# -*- coding: utf-8 -*-
"""
V3 - Module A ｜Escape Groove（B 系列公式）
"""

import math

DISPLAY_DECIMALS = 3


# ----------------------------------------------------------
# ⭐ 原始加工廠公式（你的 formulas.py）
# ----------------------------------------------------------
def solve_escape_groove(B2, B3, B5, B6):

    B9 = B6
    E3 = B3 + B5
    E4 = B2 + B9
    E6 = B3 + B9
    E7 = B2 + B5
    E9 = B5 - B9

    B52 = E3 - B9
    B51 = (E4 - B9) * 2
    B53 = E6 - B9
    B54 = (E7 - B9) * 2
    B55 = E9

    return B51, B52, B54, B53, B55


# ----------------------------------------------------------
# ⭐ 主入口（V3 模組 A）
# ----------------------------------------------------------
def solve(data: dict):

    # ========= 正確讀取 (A 工廠使用 K1_A ~ K4_A) =========
    K1 = float(data["K1_A"])   # 小徑 X
    K2 = float(data["K2_A"])   # Z → 起點距離
    K3 = float(data["K3_A"])   # R 角
    K4 = float(data["K4"])   # 刀鼻半徑

    # ========= K → B（照你 main.py 設計）=========
    B2 = K1 / 2
    B3 = -abs(K2)
    B5 = K3
    B6 = K4

    # ========= 呼叫加工廠公式 =========
    b15, b16, b17, b18, b19 = solve_escape_groove(B2, B3, B5, B6)

    # ========= 輸出到 master_solver =========
    return {
        "ok": True,
        "values": {
            "X_START": b15,
            "Z_START": b16,
            "X_END":   b17,
            "Z_END":   b18,
            "R_AFTER": b19,
        },
        "text_lines": [
            f"圓孤起始點  X = {b15:.3f}",
            f"圓孤起始點  Z = {b16:.3f}",
            f"圓孤終點    X = {b17:.3f}",
            f"圓孤終點    Z = {b18:.3f}",
            f"刀鼻補正後  R = {b19:.3f}",
        ]
    }
