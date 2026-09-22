import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from pydantic import BaseModel

app = FastAPI()

# ----------------------------------------------------
# 1. 所有 API 路徑一律加上 /api/ 前綴
# ----------------------------------------------------
@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "FastAPI is running"}

class Item(BaseModel):
    name: str
    price: int

@app.post("/api/items")
def create_item(item: Item):
    return {"message": "Item created", "data": item}


# ----------------------------------------------------
# 2. 安全限制：僅允許存取 .html 與 .css 檔案
# ----------------------------------------------------
class RestrictedStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope) -> Response:
        # 取得副檔名
        ext = os.path.splitext(path)[1].lower()
        # 非 .html 或 .css 檔案直接拒絕 (403 Forbidden)
        if ext not in [".html", ".css", ""]:  # "" 代表目錄首頁（index.html）
            raise HTTPException(
                status_code=403, 
                detail="Access denied: Only .html and .css files are allowed."
            )
        return await super().get_response(path, scope)


# ----------------------------------------------------
# 3. 定義 WebUI 目錄並掛載至根目錄 /
# ----------------------------------------------------
# 指向 app/webui-lab 資料夾
APP_DIR = os.path.dirname(os.path.abspath(__file__))      # .../Dbs/app
DBS_DIR = os.path.dirname(APP_DIR)                        # .../Dbs
PARENT_DIR = os.path.dirname(DBS_DIR)

public_directory = os.path.join(PARENT_DIR, "webui-lab")

if os.path.exists(public_directory):
    app.mount("/", RestrictedStaticFiles(directory=public_directory, html=True), name="static")
else:
    print(f"Warning: Public directory '{public_directory}' not found.")