# -*- coding: utf-8 -*-

import math


def _to_float(v):
    try:
        return float(v)
    except:
        return 0.0
    
def fmt(x, p=6):
    return f"{x:.{p}f}"
    

def solve_a(data):
 
    # ========= 1️⃣ 基本讀值 =========
    B2 = _to_float(data["前端x軸外徑"]) / 2.0
    raw_B3 = data.get("斜度長")
    raw_B7 = data.get("斜度x起始點")

    B4 = _to_float(data["角度"])
    B5 = _to_float(data["前端R角"])
    B6 = _to_float(data["刀鼻半徑"]) * 2.0

    # ========= 2️⃣ 角度防呆 =========
    if abs(math.sin(math.radians(B4))) < 1e-12:
        raise ValueError("A 模組錯誤：角度不能為 0")

    # ========= 3️⃣ 判斷 B3 / B7 是否有效 =========
    def is_blank(v):
        return v in (None, "", 999, -999)

    has_B3 = not is_blank(raw_B3)
    has_B7 = not is_blank(raw_B7)

    if not has_B3 and not has_B7:
        raise ValueError("A 模組錯誤：B3 與 B7 至少需輸入一個")

    # ========= 4️⃣ 斜率 =========
    m = -1.0 / math.tan(math.radians(B4))

    # ========= 5️⃣ 補算缺的那一個 =========
    if has_B7:
        B7 = _to_float(raw_B7) / 2.0
        B3 = m * (B2 - B7)
        src = "B7 → 推算 B3"
    else:
        B3 = -abs(_to_float(raw_B3))
        B7 = B2 - (B3 / m)
        src = "B3 → 推算 B7"

    # ========= 6️⃣ 以下「完全不動你原本公式」 =========
    B9  = B6 / 2.0
    B10 = m
    B11 = B3 - B10 * B2
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

    B52 = (-B29 + sqrt_D) / (2 * B28)
    B32 = (B52-B9)*2
    B53 = (-B29 - sqrt_D) / (2 * B28)
    B33 = (B53-B9)*2

    B54 = B10 * B52 + B26
    B34 = B54-B9
    B55 = B10 * B53 + B26
    B35 = B55-B9

    dist1 = math.hypot(B32 - B17, B34 - B18)
    dist2 = math.hypot(B33 - B17, B35 - B18)

    if dist1 <= dist2:
        B42, B43 = B32, B34
    else:
        B42, B43 = B33, B35

    B51=(B15-B9)*2
    B21 = B51

    B22 = B9-B9

    B54 = B5 + B6
    B44 = B54-B9

    return {
        "ok": True,
        "values": {
            "B21": B21,
            "B22": B22,
            "B42": B42,
            "B43": B43,
            "B44": B44,
            "B3":  B3,
            "B7":  B7,
        },
        "text_lines": [
            "A 工廠（前端 R角斜度）完成",
            f"模式：{src}",
            f"B21 = {fmt(B21)}",
            f"B22 = {fmt(B22)}",
            f"B42 = {fmt(B42)}",
            f"B43 = {fmt(B43)}",
            f"B44 = {fmt(B44)}",
        ]
    }
