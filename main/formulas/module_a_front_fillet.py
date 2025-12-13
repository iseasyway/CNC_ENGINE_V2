# -*- coding: utf-8 -*-
"""
module_a_front_fillet.py
A 加工廠：前端 R角斜度（完全 Web 版）
輸入：data 字典
輸出：統一 values + text_lines
"""

import math


# -------------------------------------------------------
# 小工具
# -------------------------------------------------------
def _to_float(v):
    try:
        return float(v)
    except:
        return 0.0


def fmt(x, p=6):
    return f"{x:.{p}f}"


# -------------------------------------------------------
# 核心計算（官方 A 模組）
# -------------------------------------------------------
def solve_a(data):
    """
    data = {
       "前端x軸外徑": ,
       "斜度長": ,
       "角度": ,
       "前端R角": ,
       "未端R角": ,
       "刀鼻半徑": ,
       "斜度x起始點":
    }
    """

    # 1️⃣ 取值（全部轉成 B 系列）
    B2 = _to_float(data["前端x軸外徑"]) / 2.0
    B3 = -abs(_to_float(data["斜度長"]))             # 強制負號（你原本的工廠邏輯）
    B4 = _to_float(data["角度"])
    B5 = _to_float(data["前端R角"])
    B6 = _to_float(data["刀鼻半徑"]) * 2.0
    B7 = _to_float(data["斜度x起始點"]) / 2.0

    if abs(math.sin(math.radians(B4))) < 1e-12:
        raise ValueError("A 模組錯誤：角度不能為 0")

    # 2️⃣ 開始計算（完全沿用你原本加工廠公式）
    m = -1.0 / math.tan(math.radians(B4))
    B3_int = m * (B2 - B7)

    B9 = B6 / 2.0
    B10 = m
    B11 = B3_int - B10 * B2
    B12 = math.sqrt(1 + B10**2)

    B13 = (-B11 - B5 + B5 * B12) / B10
    B14 = (-B11 - B5 - B5 * B12) / B10
    B15 = min(B13, B14)

    B16 = -B5
    B17 = (B15 + B10 * (B16 - B11)) / (1 + B10**2)
    B18 = B10 * B17 + B11

    B25 = math.copysign(1.0, B16 - (B10 * B15 + B11))
    B26 = B11 - B25 * B9 * B12
    B27 = B5 + B9
    B28 = 1 + B10**2
    B29 = 2 * (B10 * (B26 - B16) - B15)
    B30 = B15**2 + (B26 - B16)**2 - B27**2

    D = max(0.0, B29**2 - 4 * B28 * B30)
    sqrt_D = math.sqrt(D)

    B32 = (-B29 + sqrt_D) / (2 * B28)
    B33 = (-B29 - sqrt_D) / (2 * B28)
    B34 = B10 * B32 + B26
    B35 = B10 * B33 + B26

    dist1 = math.hypot(B32 - B17, B34 - B18)
    dist2 = math.hypot(B33 - B17, B35 - B18)

    if dist1 <= dist2:
        B42, B43 = B32, B34
    else:
        B42, B43 = B33, B35

    # 與工廠版一致的輸出
    B21 = B15
    B22 = B9
    B44 = B5 + B6

    # -------------------------------------------------------
    # 整理輸出
    # -------------------------------------------------------
    values = {
        "B21": B21,
        "B22": B22,
        "B42": B42,
        "B43": B43,
        "B44": B44,
        "B7": B7
    }

    text_lines = [
        "A 工廠（前端 R角斜度）完成",
        f"B21 = {fmt(B21)}",
        f"B22 = {fmt(B22)}",
        f"B42 = {fmt(B42)}",
        f"B43 = {fmt(B43)}",
        f"B44 = {fmt(B44)}",
        f"B7  = {fmt(B7)}",
    ]

    return {"ok": True, "values": values, "text_lines": text_lines}


# -------------------------------------------------------
# Web 統一路口（給 master_solver 用）
# -------------------------------------------------------
def calc_front_fillet_from_direct_inputs(data):
    return solve_a(data)
