
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from main.id3_master_solver import run_all_modules_with_output

router = APIRouter()

templates = Jinja2Templates(directory="main/templates")


# =========================
# 
# =========================
@router.get("/id3", response_class=HTMLResponse)
def id3_page(request: Request, module: str | None = None):


    # 預設 module（）
    if module is None:
        module = "a8"

    return templates.TemplateResponse(
        "id3.html",
        {
            "request": request,
            "module": module
        }
    )


# =========================
# ID3 計算 API（不動）
# =========================
@router.post("/api/id3/calc")
async def api_id3_calc(
    斜度x起始點: float = Form(...),
    前端x軸內徑: float = Form(...),
    角度: float = Form(...),
    斜度長: float = Form(...),
    未端R角: float = Form(...),
    前端R角: float = Form(...),
    刀鼻半徑: float = Form(...),


    
  
    
):
    data = {
        "斜度x起始點": 斜度x起始點,
        "前端x軸內徑": 前端x軸內徑,
        "角度": 角度,
        "斜度長": 斜度長,  
        "未端R角": 未端R角,
        "前端R角": 前端R角,    
        "刀鼻半徑": 刀鼻半徑,
    }

    try:
        html_output = run_all_modules_with_output(data)
        return JSONResponse({"ok": True, "html": html_output})

    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)})
