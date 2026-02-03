# -*- coding: utf-8 -*-
import math


# -------------------------------------------------------
# 幾何子函式（垂直基準）
# -------------------------------------------------------
def first_point_by_vertical_base(R, angle_deg):
    """
    第一個點：
    以『垂直線』為基準
    圓心 → 角度線 × 垂直線 X = -R
    """
    theta = math.radians(angle_deg)

    # 對垂直量角，順時針（右下）
    dir_x = -math.cos(theta)
    dir_z =  math.sin(theta)

    # 與 X = -R 的交點
    t = (-R) / dir_x
    X = -R
    Z = t * dir_z

    return X, Z


def second_point_on_circle_vertical_base(R, angle_deg):
    """
    第二個點：
    以『垂直基準角』
    圓心 → 角度線 × 圓弧
    """
    theta = math.radians(angle_deg)

    X = -R * math.cos(theta)
    Z =  R * math.sin(theta)

    return X, Z


# -------------------------------------------------------
# D 工廠主解法（垂直基準 R 角）
# -------------------------------------------------------
def solve_c(data: dict):
    # ===============================
    # 1️⃣ 讀取輸入端
    # ===============================
    R =  float(data["未端R角"])
    B1 = float(data["角度"])
    B2 = B1
    B3 = B2/2
    # 幾何規則（你定的）
    ANGLE_1 = B3         # 第一點：× 垂直線
    ANGLE_2 = B2         # 第二點：× 圓弧

    # ===============================
    # 2️⃣ 幾何計算
    # ===============================
    P1 = first_point_by_vertical_base(R, ANGLE_1)
    P2 = second_point_on_circle_vertical_base(R, ANGLE_2)

    # ===============================
    # 3️⃣ 格式化
    # ===============================
    def _fmt(x):
        return f"{x:.3f}"

    # ===============================
    # 4️⃣ 輸出 values（給航母 / G-code）
    # ===============================
    result_values = {
        "D01X": P1[0],
        "D01Z": P1[1],
        "D02X": P2[0],
        "D02Z": P2[1],
    }

    # ===============================
    # 5️⃣ 輸出文字（給前端）
    # ===============================
    text_lines = [
        "➡️ D 工廠（R 角端點｜垂直基準）",
        f"D01X = {_fmt(P1[0])}",
        f"D01Z = {_fmt(P1[1])}",
        f"D02X = {_fmt(P2[0])}",
        f"D02Z = {_fmt(P2[1])}",
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
    return solve_c(data)
