from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/v3")
def v3_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        "v3.html",
        {"request": request}
    )

@router.post("/api/v3/calc")
async def api_v3_calc(
    # ===== A 工廠輸入 =====
    K1_A: float = Form(...),   # 小徑 X
    K2_A: float = Form(...),   # Z → 起點距離
    K3_A: float = Form(...),   # R 角
   

   
    K1_B: float = Form(...),   # 終點外徑 X
    K2_B: float = Form(...),   # R 角
    
       # ===== 共用 =====
    K4: float = Form(...),   # 刀鼻半徑（只收一次）

):
    from main.v3_master_solver import run_all_v3_modules_with_output

    # ----------------------------
    # 🧩 把使用者輸入轉成 Module 需要的 K 系列格式
    # ----------------------------
    data = {
        # Module A 需要 K1,K2,K3,K4
        "K1_A": K1_A,
        "K2_A": K2_A,
        "K3_A": K3_A,
        "K4": K4,
        
        # Module B 需要 K1,K2,K3
        "K1_B": K1_B,
        "K2_B": K2_B,
        "K4": K4,
  
    }

    try:
        html = run_all_v3_modules_with_output(data)
        return JSONResponse({"ok": True, "html": html})
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)})
