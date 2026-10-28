import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings
from app.core.db import create_db_tables
from app.core.security import validate_auth_secrets
import app.models.team
import app.models.user
import app.models.permission
import app.models.tag


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    validate_auth_secrets()
    create_db_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET_KEY,
    session_cookie="oauth_session",
    max_age=600,
    same_site="lax",
    https_only=settings.AUTH_COOKIE_SECURE,
)

from app.routers import asset, asset_tag, auth, notes, team, team_asset, team_member, user, user_team_permission, permission, tag, views  # 匯入路由模組
app.include_router(notes.router) # 註冊 notes 路由
app.include_router(asset.router) # 註冊 assets 路由
app.include_router(asset_tag.router) # 註冊 asset-tags 路由
app.include_router(auth.router) # 註冊 authentication 路由
app.include_router(team.router) # 註冊 teams 路由
app.include_router(team_member.router) # 註冊 team-members 路由
app.include_router(user_team_permission.router) # 註冊 team-permissions 路由
app.include_router(team_asset.router) # 註冊 team-assets 路由
app.include_router(user.router) # 註冊 users 路由
app.include_router(permission.router) # 註冊 permissions 路由
app.include_router(tag.router) # 註冊 tags 路由
app.include_router(views.router) # 註冊 database view 路由


# api路徑

@app.get("/health")
@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.get("/version")
@app.get("/api/version")
def version_check():
    return {"version": "0.1.0"}

class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
@app.post("/api/items")
def create_item(item: Item):
    return {"message": "Item created", "data": item.model_dump()}


# 安全限制：僅允許存取 .html 與 .css 檔案

class RestrictedStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope) -> Response:
        ext = os.path.splitext(path)[1].lower()
        # 定義允許的副檔名集合
        allowed_extensions = {".html", ".css", ".js", ".json", ".svg", ".png", ".jpg", ""}

        if ext not in allowed_extensions:
            raise HTTPException(
                status_code=403, 
                detail=f"Access denied: File type '{ext}' is not allowed."
            )
        return await super().get_response(path, scope)



# 3. 定義 WebUI 目錄並掛載至根目錄 /

# 指向 app/webui-lab 資料夾

APP_DIR = os.path.dirname(os.path.abspath(__file__))      
DBS_DIR = os.path.dirname(APP_DIR)                      
PARENT_DIR = os.path.dirname(DBS_DIR)

public_directory = os.path.join(PARENT_DIR, "webui-lab")

if os.path.exists(public_directory):
    app.mount("/", RestrictedStaticFiles(directory=public_directory, html=True), name="static")
else:
    print(f"Warning: Public directory '{public_directory}' not found.")