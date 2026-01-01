# main/routers/v2_router.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse

router = APIRouter()

# ----------------------------------------------------------
# V2 主畫面
# ----------------------------------------------------------
@router.get("/v2", response_class=HTMLResponse)
def v2_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        "v2.html",
        {"request": request}
    )


# ----------------------------------------------------------
# V2 計算 API
# ----------------------------------------------------------
@router.post("/api/v2/calc")
async def api_v2_calc(
    # ===== Escape Groove（module_a）=====
    K1: float = Form(...),   # 斜度角終點外徑
    K2: float = Form(...),   # 起始角度（也給 module_b 用）
    K3: float = Form(...),   # Z 軸起始安全距離
    K4: float = Form(999),   # 斜度角 Z 距離（模式 A）
    K5: float = Form(...),   # 刀鼻半徑（也給 module_b 用）
    K6: float = Form(999),   # 斜度角 X 外徑（模式 B）
):
    from main.v2_master_solver import run_all_v2_modules_with_output

    data = {
        "K1": K1,
        "K2": K2,
        "K3": K3,
        "K4": K4,
        "K5": K5,
        "K6": K6,
    }

    try:
        html_output = run_all_v2_modules_with_output(data)
        return JSONResponse({"ok": True, "html": html_output})

    except Exception as e:
        import traceback
        return JSONResponse({
            "ok": False,
            "error": str(e),
            "trace": traceback.format_exc()
        })
