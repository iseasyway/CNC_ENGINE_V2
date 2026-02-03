# -*- coding: utf-8 -*-
import math


# -------------------------------------------------------
# 幾何子函式（你已驗證正確）
# -------------------------------------------------------
def first_point_by_vertical(R, angle_deg):
    """
    第一個點：
    圓心 → 角度線 × 垂直線 Z = +R
    """
    theta = math.radians(angle_deg)

    # 對水平量角，順時針（右下）
    dir_x = -math.sin(theta)
    dir_z =  math.cos(theta)

    # 與 Z = R 的交點
    t = R / dir_z
    X = t * dir_x
    Z = R

    return X, Z


def second_point_on_circle(R, angle_deg):
    """
    第二個點：
    圓心 → 角度線 × 圓弧
    """
    theta = math.radians(angle_deg)

    X = -R * math.sin(theta)
    Z =  R * math.cos(theta)

    return X, Z


# -------------------------------------------------------
# C 工廠主解法
# -------------------------------------------------------
def solve_b(data: dict):
    # ===============================
    # 1️⃣ 讀取輸入端
    # ===============================
    R =  float(data["前端R角"])
    B1 = float(data["角度"])
    B2 = 90.0 - B1
    B3 = B2/2
    # 幾何關係（你指定的規則）
    
    ANGLE_2 = B2  # 第二點用
    ANGLE_1 = B3  # 第一點用（等分）

    # ===============================
    # 2️⃣ 幾何計算
    # ===============================
    P1 = first_point_by_vertical(R, ANGLE_1)
    P2 = second_point_on_circle(R, ANGLE_2)
    
    # ===============================
    # 3️⃣ 格式化
    # ===============================
    def _fmt(x):
        return f"{x:.3f}"

    # ===============================
    # 4️⃣ 輸出 values（給航母 / G code）
    # ===============================
    result_values = {
        "C01X": P1[0],
        "C01Z": P1[1],
        "C02X": P2[0],
        "C02Z": P2[1],
    }

    # ===============================
    # 5️⃣ 輸出文字（給前端）
    # ===============================
    text_lines = [
        "➡️ C 工廠（R 角端點｜垂直基準）",
        f"C01X = {_fmt(P1[0])}",
        f"C01Z = {_fmt(P1[1])}",
        f"C02X = {_fmt(P2[0])}",
        f"C02Z = {_fmt(P2[1])}",
    ]

    return {
        "ok": True,
        "values": result_values,
        "text_lines": text_lines,
    }


# -------------------------------------------------------
# 🔁 對外統一介面（航母只呼叫這個）
# -------------------------------------------------------
def solve(data: dict):
    return solve_b(data)
