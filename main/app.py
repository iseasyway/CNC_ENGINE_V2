from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from main.v1_solver import run_all_modules_with_output

app = FastAPI()

# 靜態檔案（圖片用）
app.mount("/public", StaticFiles(directory="public"), name="public")

# 模板路徑（HTML）
templates = Jinja2Templates(directory="main/templates")


# -------------------------
# 顯示運算頁面
# -------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/v1", response_class=HTMLResponse)
def v1_page(request: Request):
    return templates.TemplateResponse("v1.html", {"request": request})


# -------------------------
# 接收前端表單 → 運算 → 回傳結果
# -------------------------
@app.post("/api/v1/calc")
async def api_calc(
    前端x軸外徑: float = Form(...),
    斜度長: float = Form(...),
    角度: float = Form(...),
    前端R角: float = Form(...),
    未端R角: float = Form(...),
    z軸長度: float = Form(...),
    R角: float = Form(...),
    刀鼻半徑: float = Form(...),
    斜度x起始點: float = Form(...),
):

    data = {
        "前端x軸外徑": 前端x軸外徑,
        "斜度長": 斜度長,
        "角度": 角度,
        "前端R角": 前端R角,
        "未端R角": 未端R角,
        "z軸長度": z軸長度,
        "R角": R角,
        "刀鼻半徑": 刀鼻半徑,
        "斜度x起始點": 斜度x起始點,
    }

    try:
        html_output = run_all_modules_with_output(data)
        return JSONResponse({"ok": True, "html": html_output})

    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)})
