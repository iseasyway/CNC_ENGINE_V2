# app.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# 主線只掛 v1 V2
from main.routers.v1_router import router as v1_router
from main.routers.v2_router import router as v2_router 
from main.routers.v3_router import router as v3_router
from main.routers.v4_router import router as v4_router
# 等 v4 完成再打開
# from main.routers.v3_router import router as v5_router 


app = FastAPI()

# 靜態檔案
app.mount("/public", StaticFiles(directory="public"), name="public")

# HTML 模板
templates = Jinja2Templates(directory="main/templates")
app.state.templates = templates

# 首頁（分類）
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 分類頁
@app.get("/category/a", response_class=HTMLResponse)
def category_a(request: Request):
    return templates.TemplateResponse("category_a.html", {"request": request})

@app.get("/category/b", response_class=HTMLResponse)
def category_b(request: Request):
    return templates.TemplateResponse("category_b.html", {"request": request})

# 主線只掛 v1 V2
app.include_router(v1_router)
app.include_router(v2_router)
app.include_router(v3_router)
app.include_router(v4_router)
# 等 v4 完成再打開
# app.include_router(v5_router)

