# main/routers/v6_router.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from main.v6_master_solver import run_all_modules_with_output

router = APIRouter()

templates = Jinja2Templates(directory="main/templates")


# =========================
# V6 主頁（吃 module）
# =========================
@router.get("/v6", response_class=HTMLResponse)
def v6_page(request: Request, module: str | None = None):


    # 預設 module（直接進 /v1 時）
    if module is None:
        module = "a6"

    return templates.TemplateResponse(
        "v6.html",
        {
            "request": request,
            "module": module
        }
    )


# =========================
# V6 計算 API（不動）
# =========================
@router.post("/api/v6/calc")
async def api_v6_calc(
    大徑X: float = Form(...),
    原點至斜度角W: float = Form(...),
    角度1: float = Form(...),
    前端R1: float = Form(...),
    前端R2: float = Form(...),
    小徑X: float = Form(...),
    原點至終點面W: float = Form(...),
    角度2: float = Form(...),
    終端R1: float = Form(...),
    終端X: float = Form(...),
    終端R2: float = Form(...),
    刀鼻半徑: float = Form(...),
 
  
    
):
    data = {
        "大徑X": 大徑X,
        "原點至斜度角W": 原點至斜度角W,
        "角度1": 角度1,
        "前端R1": 前端R1,
        "前端R2": 前端R2,
        "小徑X": 小徑X,
        "原點至終點面W": 原點至終點面W,
        "角度2": 角度2,
        "終端R1": 終端R1,
        "終端X": 終端X,
        "終端R2": 終端R2,
        "刀鼻半徑": 刀鼻半徑,
    }

    try:
        html_output = run_all_modules_with_output(data)
        return JSONResponse({"ok": True, "html": html_output})

    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)})
