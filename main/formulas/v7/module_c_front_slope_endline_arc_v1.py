# -*- coding: utf-8 -*-
"""

============================================================
🏭 C 工廠：雙角度中段倒角，圓心(模版)

============================================================
"""

import math

# -------------------------------------------------------
# 🧠 核心計算（C 工廠）
# -------------------------------------------------------
def solve_c(data):
    A_values = data.get("A", {})
    B51 = A_values.get("B51")
  
    # ===================================================
    # 1️⃣ 讀取並整理輸入（對齊 Excel B 欄）
    # ===================================================
    B3  = float(B51)   #起始點X直徑
    B2  = -abs(float(data["前端w"]) )
    B4  = float(data["角度1"]) # 斜度角   
    B5  = float(data["角度2"])
    B6  = float(data["中端R"])   
    B7  = float(data["刀鼻半徑"]) *2    #刀鼻直徑
   

    B10 = B7 / 2.0
    B11 = -math.tan(math.radians(B4))
    B12 = -math.tan(math.radians(B5))
    B13 = B3 - B11 * B2
    B14 = B3 - B12 * B2
    B15 = math.sqrt(1 + B11**2)
    B16 = math.sqrt(1 + B12**2)
    B17 = B6 + B10
    H11 = 1.0 / math.sqrt(1 + B11**2)
    I11 = B11 * H11

    # ---- 幫手函式 ----
    def FG(s1, s2):
        F = (((s1)*B15 - (s2)*B16)*B6 - (B13 - B14)) / (B11 - B12)
        G = B11*F + B13 - (s1)*B6*B15
        return F, G

    # ---- 產生候選點 ----
    combos = [(+1,+1),(+1,-1),(-1,+1),(-1,-1)]
    cands = []
    for sign_b10 in (+1, -1):
        for s1, s2 in combos:
            Fk, Gk = FG(s1, s2)
            A = 1 + B11**2
            B = 2*( B11*((B13 + sign_b10*B10*B15) - Gk) - Fk )
            C = Fk**2 + ((B13 + sign_b10*B10*B15) - Gk)**2 - B17**2
            disc = B*B - 4*A*C
            if disc < -1e-9:
                continue
            disc = max(0.0, disc)
            for rs in (+1, -1):
                Z = (-B + rs*math.sqrt(disc)) / (2*A)
                X = B11*Z + (B13 + sign_b10*B10*B15)
                Fproj = (Z - B2)*H11 + (X - B3)*I11
                if Fproj > 0:
                    cands.append((Fproj, Z, X))

    if not cands:
        raise ValueError("❌ 無可用解：判別式<0 或投影<=0")

    cands.sort(key=lambda t: t[0])
    Zc_star, Xc_star = cands[0][1], cands[0][2]   # B72, B73
    B51=Zc_star-B7/2
    B52=(Xc_star-B10)*2
    # ---- 第二組固定 (+,+) ----
    F3 = (((+1)*B15 - (+1)*B16)*B6 - (B13 - B14)) / (B11 - B12)
    G3 = B11*F3 + B13 - (+1)*B6*B15
    A2 = 1 + B12**2
    B2c = 2*( B12*( B14 + (+1)*B10*B16 - G3) - F3 )
    C2 = F3**2 + ( B14 + (+1)*B10*B16 - G3 )**2 - B17**2
    disc2 = max(0.0, B2c*B2c - 4*A2*C2)
    Zc2 = (-B2c + math.sqrt(disc2)) / (2*A2)
    Xc2 = B12*Zc2 + (B14 + (+1)*B10*B16)
    B53= Zc2-B7/2
    B54= (Xc2-B10)*2
    B55= B6 + B10

    def _fmt(x):
     # 例如固定顯示到小數點兩位
        return f"{x:.3f}"

    result_values = {
        "B51": B51,
        "B52": B52,
        "B53": B53,
        "B54": B54,
        "B55": B55,
        
    }

    text_lines = [
        "➡️ 前端斜角 → 平線 → 終點弧（C 工廠）",
        f"B51 = {_fmt(B51)}",
        f"B52 = {_fmt(B52)}",
        f"B53 = {_fmt(B53)}",
        f"B54 = {_fmt(B54)}",
        f"B55 = {_fmt(B55)}",
        
    ]

    return {
        "ok": True,
        "text_lines": text_lines,
        "values": result_values,
    }


# -------------------------------------------------------
# 🔁 對外統一介面
# -------------------------------------------------------
def solve(data: dict):
    return solve_c(data)