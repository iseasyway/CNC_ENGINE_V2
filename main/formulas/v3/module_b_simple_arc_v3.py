# -*- coding: utf-8 -*-
"""
V3 - Module B ｜Simple Arc（圓弧終點計算）
"""

import math

DISPLAY_DECIMALS = 3


def solve_escape_groove(B2, B3, B4):

    C7  = B2 - B3 - (B4 / 2.0)
    B51 = C7 * 2

    C8  = 0.0
    C10 = B2
    B52 = C10 * 2

    C11 = -(B3 + B4 / 2.0)
    C13 =  (B3 + B4 / 2.0)

    return B51, C8, B52, C11, C13


def solve(data: dict):

    # -------- 正確讀取資料 --------
    K1_B = float(data["K1_B"])
    K2_B = float(data["K2_B"])
    K4   = float(data["K4"])

    # -------- K → B --------
    B2 = K1_B / 2
    B3 = K2_B
    B4 = K4 * 2

    b15, b16, b17, b18, b19 = solve_escape_groove(B2, B3, B4)

    # -------- 統一 KEY（大寫）--------
    return {
        "values": {
            "X_START": b15,
            "Z_START": b16,
            "X_END":   b17,
            "Z_END":   b18,
            "R_AFTER": b19,
        },
        "text_lines": [
            f"圓孤起始點 X = {b15:.3f}",
            f"圓孤起始點 Z = {b16:.3f}",
            f"圓孤終點   X = {b17:.3f}",
            f"圓孤終點   Z = {b18:.3f}",
            f"刀鼻補正後 R = {b19:.3f}",
        ]
    }
