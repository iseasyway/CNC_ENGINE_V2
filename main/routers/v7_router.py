# main/routers/v6_router.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from main.v7_master_solver import run_all_modules_with_output

router = APIRouter()

templates = Jinja2Templates(directory="main/templates")


# =========================
# V7 主頁（吃 module）
# =========================
@router.get("/v7", response_class=HTMLResponse)
def v7_page(request: Request, module: str | None = None):


    # 預設 module（直接進 /v1 時）
    if module is None:
        module = "a7"

    return templates.TemplateResponse(
        "v7.html",
        {
            "request": request,
            "module": module
        }
    )


# =========================
# V7 計算 API（不動）
# =========================
@router.post("/api/v7/calc")
async def api_v7_calc(
    前端w: float = Form(...),
    前端R: float = Form(...),
    角度1: float = Form(...),
    角度2: float = Form(...),
    中端R: float = Form(...),
    未端R: float = Form(...),
    原點至終點面W: float = Form(...),
    未端D: float = Form(...),
    刀鼻半徑: float = Form(...),
 
    
):
    data = {
        "前端w": 前端w,
        "前端R": 前端R,
        "角度1": 角度1,
        "角度2": 角度2,
        "中端R": 中端R,
        "未端R": 未端R,
        "原點至終點面W": 原點至終點面W,
        "未端D": 未端D,
        "刀鼻半徑": 刀鼻半徑,
    }

    try:
        html_output = run_all_modules_with_output(data)
        return JSONResponse({"ok": True, "html": html_output})

    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)})
