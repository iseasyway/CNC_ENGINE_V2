# -*- coding: utf-8 -*-
"""
module_a_escape_groove_v2.py
============================================================
🏭 V2 - A 工廠｜Escape Groove（最終正式版）

★ 最重要更新（100% 正確）：
  - 所有換算都使用「斜度長 W = L」作為主公式
  - A 模式：直接用 K4 = W
  - B 模式：K6 = 底部直徑 X，只負責反推 W
  - 再把 W 丟進 solve_escape_groove（A 模式主公式）
  → 因此 A / B 模式永遠算出一樣結果（例如 28.507）
============================================================
"""

import math

DISPLAY_DECIMALS = 3


# ----------------------------------------------------------
# A 模式主公式（你 formulas.py 的原版，不改）
# ----------------------------------------------------------
def solve_escape_groove(R_big, theta_deg, z_safe, L, r):
    th = math.radians(abs(theta_deg))
    ct = math.cos(th)
    tt = math.tan(th)

    # 半徑系統
    D2 = r + r * tt - r / ct + z_safe * tt
    D3 = R_big - (L * tt + D2)

    B51 = D3 * 2              # 轉成直徑
    
    D4  = z_safe
    return B51, D4


# ----------------------------------------------------------
# V2 主入口
# ----------------------------------------------------------
def solve(data: dict):

    # ========= 讀取 =========
    K1 = float(data.get("K1"))  # 起始直徑（例 40）
    K2 = float(data.get("K2"))  # 角度（例 30°）
    K3 = float(data.get("K3"))  # Z 安全距離（例 1）
    K4 = data.get("K4")         # 斜度長 W（例 8.660）
    K5 = float(data.get("K5"))  # 刀鼻半徑（例 0.4）
    K6 = data.get("K6")         # 底部直徑 X（例 30）

    def used(v):
        return v not in (None, "", 999)

    has_K4 = used(K4)
    has_K6 = used(K6)

    if has_K4 and has_K6:
        raise ValueError("K4 和 K6 不可同時輸入")
    if not has_K4 and not has_K6:
        raise ValueError("K4 和 K6 必須輸入其中一個")
    if K6!=999 and K6 >= K1:
        raise ValueError(" 斜度X起點 不可大於或等於 外徑D")    
    if K2 <= 0 or K2 >= 90:
        raise ValueError("角度 A 不可小於 0度 ~ 大於 90 度")
    # 共用參數
    R_big = K1 / 2
    theta_deg = K2
    z_safe = K3
    r = K5

    # 用來反推 W 的三角參數
    th = math.radians(abs(theta_deg))
    tt = math.tan(th)

    # ============================================================
    # ⭐⭐⭐ A 模式：直接使用 K4 = W（完全正確）
    # ============================================================
    if has_K4:
        W = float(K4)
        mode = "A 模式：斜度長 W (K4)"

    # ============================================================
    # ⭐⭐⭐ B 模式：K6 = 底部直徑 X → 先反推 W，再走主公式
    # ============================================================

    else:
        D_bottom = float(K6)   # 例 30
        D_start  = K1          # 例 40

        # 直徑下降量（例：40 → 30 = 10）
        ΔD = D_start - D_bottom

        # ⭐ 反推斜度長 W（重點）
        # ΔD = 2 * W * tanθ  → W = ΔD / (2*tanθ)
        W = ΔD / (2 * tt)
        mode = "B 模式：底部直徑 X (K6)"

    # ============================================================
    # ⭐⭐⭐ 最終：全部都使用同一個主公式 solve_escape_groove
    # ============================================================
    B51, D4 = solve_escape_groove(
        R_big=R_big,
        theta_deg=theta_deg,
        z_safe=z_safe,
        L=W,
        r=r
    )

    return {
        "ok": True,
        "values": {
            "B51": B51,
            "D4":  D4,
            "L":   W,    # W = L
            "K1": K1, 
            
        },
        "text_lines": [
            "A 工廠 Escape Groove v2（正式版）完成",
            f"模式：{mode}",
            f"K1  = {K1:.3f}",
            f"W/L = {W:.3f}",
            f"B51 = {B51:.3f}",
            f"D4  = {D4:.3f}",
        ]
    }
