# -*- coding: utf-8 -*-
"""
============================================================
🏭 C 工廠：雙角度中段倒角（前段斜線 → 圓弧 → 後段斜線）
============================================================
"""

import math


# ==================================================
# 【幾何工具】
# ==================================================
def dir_vec(theta_deg):
    t = math.radians(theta_deg)
    return (math.sin(t), -math.cos(t))   # X↑, Z→


def normal_vec(theta_deg):
    t = math.radians(theta_deg)
    return (math.cos(t), math.sin(t))


def foot_point(Xc, Zc, X0, Z0, d):
    vx = Xc - X0
    vz = Zc - Z0
    t = vx * d[0] + vz * d[1]
    return (X0 + t * d[0], Z0 + t * d[1])


# ==================================================
# 【核心幾何：雙角度圓弧】
# ==================================================
def solve_fillet_arc_front_back(Xf, Zf, theta_front, theta_back, R):
    d1 = dir_vec(theta_front)
    n1 = normal_vec(theta_front)

    d2 = dir_vec(theta_back)
    n2 = normal_vec(theta_back)

    candidates = []

    for sign in (+1, -1):
        A11, A12 = d1[0], -d2[0]
        A21, A22 = d1[1], -d2[1]

        B1 = sign * R * (n2[0] - n1[0])
        B2 = sign * R * (n2[1] - n1[1])

        det = A11 * A22 - A12 * A21
        if abs(det) < 1e-9:
            continue

        a = (B1 * A22 - B2 * A12) / det

        Xc = Xf + sign * R * n1[0] + a * d1[0]
        Zc = Zf + sign * R * n1[1] + a * d1[1]

        T_front = foot_point(Xc, Zc, Xf, Zf, d1)
        T_back  = foot_point(Xc, Zc, Xf, Zf, d2)

        candidates.append((Xc, Zc, T_front, T_back))

    if len(candidates) != 2:
        raise ValueError("圓心候選數量錯誤")

    # 加工順序判斷（前段 Z 要大於後段 Z）
    valid = [c for c in candidates if c[2][1] > c[3][1]]

    if len(valid) != 1:
        raise ValueError("無法唯一決定圓心（前後段順序錯誤）")

    return valid[0]


# ==================================================
# 🧠 對外主介面（C 工廠）
# ==================================================
def solve(data: dict):
    values = {}

    # ---------- 1️⃣ 讀取輸入 ----------
    A_values = data.get("A", {})
    c_1_values = data.get("c_1", {})
    c_2_values = data.get("c_2", {})
    B51 = A_values.get("B51")

    
    Center1 = c_1_values.get("C51")
    Center2 = c_1_values.get("C52")
    Center3 = c_2_values.get("C53")
    Center4 = c_2_values.get("C54")
    if B51 is None:
        return {"values": values}

    try:
        Center1=float(Center1)
        Center2=float(Center2)
        Center3=float(Center3)
        Center4=float(Center4)
        FOCUS_X = float(B51)
        FOCUS_Z = -abs(float(data["前端w"]))
        THETA_FRONT = float(data["角度1"])
        THETA_BACK  = float(data["角度2"])
        R = float(data["中端R"])
        B5= float(data["中端R"])
        B6= float(data["刀鼻半徑"])
    except Exception:
        return {"values": values}
    

    # ---------- 2️⃣ 核心計算 ----------
    Xc, Zc, T_front, T_back = solve_fillet_arc_front_back(
        FOCUS_X, FOCUS_Z,
        THETA_FRONT, THETA_BACK,
        R
    )

    # ---------- 3️⃣ 輸出對齊（Excel / 你系統用的 key） ----------
    values["C51"] = Xc
    values["B59"] = Zc
    values["B5"] = B5+B6
    values["B53"] = (T_front[0]+Center2-B6)*2
    values["B54"] = T_front[1]+Center1-B6
    values["B55"] = (T_back[0]+Center4-B6)*2
    values["B56"] = T_back[1]+Center3-B6

    # ---------- 4️⃣ Debug（你可先留著） ----------
    print("DEBUG C 工廠 values =", values)

    return {
        "ok": True,
        "values": values
    }
