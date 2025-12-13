# -*- coding: utf-8 -*-
"""
module_d_angle_to_z_offset.py
角度 → Z軸距離（B14）
航母版：統一格式 + 可直接被 master 呼叫
"""

import math

def _fmt(x, p=6):
    return f"{x:.{p}f}" if x is not None else "-"

def solve(data):
    """
    data = {
        "角度": ,
        "刀鼻半徑": ,
    }
    """

    theta = float(data["角度"])
    nose_r = float(data["刀鼻半徑"])

    # === 原始公式（完全不動） ===
    t = math.tan(math.radians(theta))
    s = math.sqrt(1.0 + t**2)

    B9 = nose_r * (s - 1.0) / t
    B12 = B9 - nose_r
    B14 = abs(B12)

    # === 航母版輸出格式 ===
    values = {"B14": B14}

    text_lines = [
        "➡️ D 工廠：角度 → Z軸距離 B14",
        f"B14 = {_fmt(B14)}"
    ]

    return {
        "ok": True,
        "text_lines": text_lines,
        "values": values
    }
