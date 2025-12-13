# -*- coding: utf-8 -*-
"""
module_c_front_slope_endline_arc_v1.py
前端斜角 → 終點平線 → 圓弧在終點（v1）
航母版：統一格式、統一輸出、master 可直接串接
"""

import math


def _fmt(x, p=6):
    return f"{x:.{p}f}" if x is not None else "-"


def solve(data):

    # 🔥 A 工廠計算後會把 B7 塞在 data["A"] 裡
    A_values = data.get("A", {})
    B7 = A_values.get("B7")

    # ========= 1. 讀取輸入 =========
    B2 = float(B7)                          # 小徑 X（來自 A 工廠）
    B3 = float(data["角度"])                # 角度
    B4 = float(data["前端x軸外徑"]) / 2      # 外徑半徑
    B5 = float(data["未端R角"])             # 終點 R
    B6 = float(data["刀鼻半徑"]) * 2        # 刀鼻直徑
    B8 = 0.0                                # 固定 0

    # ========= 2. 幾何推算（原公式完全沿用） =========
    B10 = -math.tan(math.radians(B3))
    B11 = B2 - B10 * B8
    B12 = math.sqrt(1.0 + B10**2)

    B13 = B6 / 2.0
    B14 = B5 + B13
    B16 = B4 - B5

    # === 第一個圓與直線交會 ===
    B17 = (B16 - B11 + B5 * B12) / B10
    B20 = 1.0 + B10**2
    B21 = 2.0 * (B10 * (B11 - B16) - B17)
    B22 = B17**2 + (B11 - B16)**2 - B5**2
    B23 = B21**2 - 4.0 * B20 * B22
    sqrt_B23 = math.sqrt(max(0.0, B23))
    B24 = (-B21 - sqrt_B23) / (2.0 * B20)
    B25 = (-B21 + sqrt_B23) / (2.0 * B20)
    B26 = B10 * B24 + B11
    B27 = B10 * B25 + B11
    if B24 < B25:
        B28, B29 = B24, B26
    else:
        B28, B29 = B25, B27

    # === 第二個圓 ===
    B32 = B11 + B13 * B12
    B33 = 1.0 + B10**2
    B34 = 2.0 * (B10 * (B32 - B16) - B17)
    B35 = B17**2 + (B32 - B16)**2 - B14**2
    B36 = B34**2 - 4.0 * B33 * B35
    sqrt_B36 = math.sqrt(max(0.0, B36))
    B37 = (-B34 - sqrt_B36) / (2.0 * B33)
    B38 = (-B34 + sqrt_B36) / (2.0 * B33)
    B39 = B10 * B37 + B32
    B40 = B10 * B38 + B32

    # === E2, E3 ===
    d1 = (B37 - B28)**2 + (B39 - B29)**2
    d2 = (B38 - B28)**2 + (B40 - B29)**2
    B41 = B37 if d1 <= d2 else B38
    B42 = B39 if abs(B41 - B37) < 1e-12 else B40

    # === E4, E5 ===
    B45 = B4 + B13
    inside = max(0.0, B14**2 - (B45 - B16)**2)
    B46 = B17 - math.sqrt(inside)
    B47 = B5 + (B6 / 2)

    # ========= 3. 航母版輸出格式 =========
    result_values = {
        "E2": B41,
        "E3": B42,
        "E4": B46,
        "E5": B45,
        "E6": B47
    }

    text_lines = [
        "➡️ 前端斜角 → 平線 → 終點弧（C 工廠）",
        f"E2 = {_fmt(B41)}",
        f"E3 = {_fmt(B42)}",
        f"E4 = {_fmt(B46)}",
        f"E5 = {_fmt(B45)}",
        f"E6 = {_fmt(B47)}",
    ]

    return {
        "ok": True,
        "text_lines": text_lines,
        "values": result_values
    }
