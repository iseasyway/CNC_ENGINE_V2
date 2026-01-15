# main/routers/v5_router.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from main.v5_master_solver import run_all_modules_with_output

router = APIRouter()

templates = Jinja2Templates(directory="main/templates")


# =========================
# V1 主頁（吃 module）
# =========================
@router.get("/v5", response_class=HTMLResponse)
def v5_page(request: Request, module: str | None = None):


    # 預設 module（直接進 /v1 時）
    if module is None:
        module = "a5"

    return templates.TemplateResponse(
        "v5.html",
        {
            "request": request,
            "module": module
        }
    )


# =========================
# V5 計算 API（不動）
# =========================
@router.post("/api/v5/calc")
async def api_v5_calc(
    大徑X: float = Form(...),
    工件原點至斜度角W: float = Form(...),
    角度: float = Form(...),
    前端R角: float = Form(...),
    小徑X: float = Form(...),
    工件原點至終點面W: float = Form(...),
    終端R角: float = Form(...),
    刀鼻半徑: float = Form(...),
 
  
    
):
    data = {
        "大徑X": 大徑X,
        "工件原點至斜度角W": 工件原點至斜度角W,
        "角度": 角度,
        "前端R角": 前端R角,
        "小徑X": 小徑X,
        "工件原點至終點面W": 工件原點至終點面W,
        "終端R角": 終端R角,
        "刀鼻半徑": 刀鼻半徑,
    }

    try:
        html_output = run_all_modules_with_output(data)
        return JSONResponse({"ok": True, "html": html_output})

    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)})
