# -*- coding: utf-8 -*-
import math

SENTINEL = 999


def solve_a(data: dict):
    
    B101  = float(data["斜度x起始點"])     
    B102  = float(data["前端x軸內徑"])
    B104  = float(data["角度"])


    if B104 <= 0 or B104 >= 90:
        raise ValueError("角度 必須介於 0 ~ 90 度")   
    if B101!=999 and B101 <= B102:     
        raise ValueError(" 起始點X 不可小於或等於 內徑d") 
    


    # ===================================================
    # 1️⃣ 輸入整理層（= 單機版 inputs.py）
    # ===================================================
        
    try:
        # 幾何起點
        
        B2 = float(data["前端x軸內徑"]/2)        
               
        B8 = 0.       # Z0
               
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
        K1 = X1
        K2 = B2
        K3 = -Z1
        K4 = K3

    # --- DX 模式 ---
    else:
        X1 = B8+DX1
        dX = X1 - B2
        dZ = abs(dX) / tan_theta
        J2 = B8-dZ
        mode = "DX 模式"
        Z1 = J2
        K1 = X1
        K2 = B2
        K4 = Z1
    # ===================================================
    # 4️⃣ 航母統一輸出（對齊你其他模版）
    # ===================================================

    values= {
        "C3": K1,   
        "C4": B8,   
        "C5": K2,   
        "C6": K4,
     
    }


    text_lines = [
        "➡️ C 工廠（斜線計算）",
       
        f"C3 = {K1:.3f}",
        f"C4 = {B8:.3f}",
        f"C5 = {K2:.3f}",
        f"C6 = {K4:.3f}",
    
    ]

    return {
        "ok": True,
        "values": values,
        "text_lines": text_lines,
    }

def solve(data: dict):
    return solve_a(data)