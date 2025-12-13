# -*- coding: utf-8 -*-
"""
module_b_outer_perp_R.py
外圓垂直端 R角（B 工廠）
航母版：統一格式、統一輸出、master 可直接串接
"""

import math


def solve(data):
    """
    data = {
        "前端x軸外徑": ,
        "z軸長度": ,
        "R角": ,
        "刀鼻半徑": ,
    }
    """

    # ========= 1. 讀取輸入 =========
    B2 = float(data["前端x軸外徑"]) / 2
    B3 = float(data["z軸長度"])
    B5 = float(data["R角"])
    nose_r = float(data["刀鼻半徑"])
    B6 = nose_r * 2
    B9 = B6 / 2

    # ========= 2. 套入你原本的公式（完全相同）=========
    E3 = B3 + B5       # Z 前端
    E4 = B2 + B9       # X(未使用，但保留你的邏輯)
    E6 = B3 + B9       # Z 後端
    E7 = B2 + B5       # X 後端
    E9 = B5 - B9       # R（刀鼻補正）

    # ========= 3. 統一航母格式輸出 =========
    text_lines = [
        "➡️ 外圓垂直端 R角運算結果（B 工廠）",
        f"E3（前端 Z） = {E3:.6f}",
        f"E4（中間值 X） = {E4:.6f}",
        f"E6（後端 Z） = {E6:.6f}",
        f"E7（後端 X） = {E7:.6f}",
        f"E9（刀鼻補正 R） = {E9:.6f}",
    ]

    result_values = {
        "OUT_E3": E3,
        "OUT_E4": E4,   # 保留但 master 不使用
        "OUT_E6": E6,
        "OUT_E7": E7,
        "OUT_E9": E9,
    }

    return {
        "ok": True,
        "text_lines": text_lines,
        "values": result_values
    }
