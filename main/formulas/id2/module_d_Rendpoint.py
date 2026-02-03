# -*- coding: utf-8 -*-
import math

SENTINEL = 999


def solve_d(data: dict):
    r  = float(data["刀鼻半徑"])
    R1  = float(data["前端R角"])
    R2  = float(data["未端R角"])
    G101 = float(data["未端斜度W"])
    G102 = float(data["內端小徑X"])
    A_values = data.get("A", {})
    B_values = data.get("B", {})
    C_values = data.get("C", {})
    E_values = data.get("E", {})
    F_values = data.get("F", {})
    G_values = data.get("G", {})
    H_values = data.get("H", {})
    B1 = A_values.get("C3")
    B2 = A_values.get("C4")
    B3 = A_values.get("C5")
    B4 = A_values.get("C6")
   
    B5 = B_values.get("C01X")
    B6 = B_values.get("C01Z")
    B7 = B_values.get("C02X")
    B8 = B_values.get("C02Z")

    B9 = C_values.get("D01X")
    B10 = C_values.get("D01Z")
    B11 = C_values.get("D02X")
    B12 = C_values.get("D02Z")

    E01 = E_values.get("e01")
    E02 = E_values.get("e02")

    F01 = F_values.get("f01")
    F02 = F_values.get("f02")
  
    G01 = G_values.get("G01")
  
    H01 = H_values.get("H02")
    # ==================================================
    # 1️⃣ 讀取並整理輸入（對齊 Excel B 系列）
    # --------------------------------------------------
    # 說明：
    # - 所有輸入皆轉為 float
    # - 外徑一律轉為半徑計算
    # ==================================================
    B1  = float(B1) 
    B2  = float(B2) 
    B3  = float(B3) 
    B4  = float(B4)
    B5  = +abs(float(B5))
    B6  = float(B6)
    B7  = +abs(float(B7))
    B8  = float(B8)
    B9  = +abs(float(B9))
    B10  = float(B10)
    B11  = +abs(float(B11))
    B12  = float(B12)
    B13  = B7-B5
    B14  = B6-B8
    B15  = B9-B11#R3X
    B16  = B12-B10#R3Z
    B17  = G01+G101+r
    B18  = H01+G01+r
    B19  = G102

    R1X =(B1+B5+r)*2
    R1Z =B2 

    R2X =(B1-B13-E02+r)*2
    R2Z =B14-E01+r
    
    R3X =(B3+B15-F02+r)*2
    R3Z =B4+B16+F01-r

    R4X =B3*2
    R4Z =B4-B10-r
    R1R =R1+r
    R2R =R2+r
    def _fmt(x):
        return f"{x:.3f}"

    result_values = {
        "R1R": R1R, 
        "R2R": R2R, 
    

        "R1X": R1X,   
        "R1Z": R1Z, 

        "R2X": R2X,   
        "R2Z": R2Z,

        "R3X": R3X,
        "R3Z": R3Z,

        "R4X": R4X,
        "R4Z": R4Z,

        "B17": B17,
        "B18": B18,
        "B19": B19,
    }

    text_lines = [
        "➡️ D 工廠（R 角端點｜垂直基準）",
        f"R1X = {_fmt(R1X)}",
        f"R1Z = {_fmt(R1Z)}",
        f"R2X = {_fmt(R2X)}",
        f"R2Z = {_fmt(R2Z)}",
        f"R3X = {_fmt(R3X)}",
        f"R3Z = {_fmt(R3Z)}",
        f"R4X = {_fmt(R4X)}",
        f"R4Z = {_fmt(R4Z)}",
        f"R1R = {_fmt(R1R)}",
        f"R2R = {_fmt(R2R)}",
        f"B17 = {_fmt(B17)}",
        f"B18 = {_fmt(B18)}",
        f"B19 = {_fmt(B19)}",

    ]



    return {
        "ok": True,
        "values": result_values,
        "text_lines": text_lines,
    }

def solve(data: dict):
    return solve_d(data)