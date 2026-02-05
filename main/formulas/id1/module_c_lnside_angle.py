# -*- coding: utf-8 -*-
import math

SENTINEL = 999


def solve(data: dict):
    values = {}
    A_values = data.get("A", {}) 
    B_values = data.get("B", {})
    B4 = A_values.get("C01")
    B5 = B_values.get("C02")
    """
    C 工廠（斜線計算）

    等價於單機版：
    - inputs.py      → 輸入端
    - main.py        → 中繼層
    - solve_slanted_line → 純運算
    """

    # ===================================================
    # 1️⃣ 輸入整理層（= 單機版 inputs.py）
    # ===================================================
        
    try:
        # 幾何起點
        
        B2 = float(data["前端x軸內徑"]/2)        
        B4 = float(B4)
        B5 = float(B5) 
        B8 = 0.       # Z0
        B9 = float(data["刀鼻半徑"])
       
        B3 = float(data["角度"])     
        

        # 距離（二選一，999）
        
        raw_DX = data.get("斜度x起始點", SENTINEL)
        raw_DZ = data.get("斜度長", SENTINEL)

    except KeyError as e:
        raise ValueError(f"C 工廠錯誤：缺少必要輸入欄位 {e}")

    # ===================================================
    # 2️⃣ 999 防呆（完全對齊你既有模版）
    # ===================================================

    def is_blank(v):
        return v in (None, "", SENTINEL, -SENTINEL)

    has_DX = not is_blank(raw_DX)
    has_DZ = not is_blank(raw_DZ)

    if has_DX and has_DZ:
        raise ValueError("C 工廠錯誤：DX / DZ 只能選一個")
    if not has_DX and not has_DZ:
        raise ValueError("C 工廠錯誤：DX / DZ 至少需輸入一個")

    DX = float(raw_DX) if has_DX else SENTINEL
    DZ = float(raw_DZ) if has_DZ else SENTINEL
    DX1= DX/2
    # ===================================================
    # 3️⃣ 幾何核心（= 單機 solve_slanted_line）
    # ===================================================

    tan_theta = math.tan(math.radians(B3))
    if abs(tan_theta) < 1e-12:
        raise ValueError("C 工廠錯誤：角度不可為 0")

    # --- DZ 模式 ---
    if DZ != SENTINEL:
        Z1 = B8 + DZ
        dZ = Z1 - B8
        dX = abs(dZ) * tan_theta
        X1 = B2+dX
       
        mode = "DZ 模式"
        K1 = (X1-B5+B9)*2
        K2 = B2*2
        K3 = -Z1
        K4 = K3+B4-B9
    # --- DX 模式 ---
    else:

        X1 = B8+DX1
        dX = X1 - B2
        dZ = abs(dX) / tan_theta
        J2 = B8-dZ
        mode = "DX 模式"
        Z1 = J2
        K1 = (X1-B5+B9)*2
        K2 = B2*2
        K4 = Z1+B4-B9
    # ===================================================
    # 4️⃣ 航母統一輸出（對齊你其他模版）
    # ===================================================

    values = {
        "C3": K2,   
        "C4": B8,   
        "C5": K1,   
        "C6": K4,   
    }

    text_lines = [
        "➡️ C 工廠（斜線計算）",
        f"模式：{mode}",
        f"C3 = {K2:.3f}",
        f"C4 = {B8:.3f}",
        f"C5 = {K1:.3f}",
        f"C6 = {K4:.3f}",
    ]

    return {
        "ok": True,
        "values": values,
        "text_lines": text_lines,
    }
