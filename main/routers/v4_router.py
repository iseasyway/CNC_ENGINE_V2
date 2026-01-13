# main/routers/v4_router.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from main.v4_master_solver import run_all_modules_with_output

router = APIRouter()

templates = Jinja2Templates(directory="main/templates")


# =========================
# V1 主頁（吃 module）
# =========================
@router.get("/v4", response_class=HTMLResponse)
def v4_page(request: Request, module: str | None = None):
    """
    module:
      a1 = 前端圓角
      a2 = 前端倒角
      a3 = 前端斜線圓弧
    """

    # 預設 module（直接進 /v1 時）
    if module is None:
        module = "a4"

    return templates.TemplateResponse(
        "v4.html",
        {
            "request": request,
            "module": module
        }
    )


# =========================
# V4 計算 API（不動）
# =========================
@router.post("/api/v4/calc")
async def api_v4_calc(
    斜度x起始點: float = Form(...),
    前端x軸外徑: float = Form(...),
    角度: float = Form(...),
    斜度長: float = Form(...),
    前端R角: float = Form(...),
    未端R角: float = Form(...),
    z軸長度: float = Form(...),
    R角: float = Form(...),
    斜度角: float = Form(...),

    終點x軸外徑: float = Form(...),
    

    刀鼻半徑: float = Form(...),


    
  
    
):
    data = {
        "斜度x起始點": 斜度x起始點,
        "前端x軸外徑": 前端x軸外徑,
        "角度": 角度,
        "斜度長": 斜度長,
        "前端R角": 前端R角,
        "未端R角": 未端R角,
        "z軸長度": z軸長度,
        "R角": R角,
        "斜度角": 斜度角,
        "終點x軸外徑": 終點x軸外徑,
        "刀鼻半徑": 刀鼻半徑,
    }

    try:
        html_output = run_all_modules_with_output(data)
        return JSONResponse({"ok": True, "html": html_output})

    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)})
