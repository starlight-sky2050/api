# FastAPI + PostgreSQL 後端系統開發：12 週實作課程

> 針對已有全端開發與系統架構背景的學習者設計，跳過基礎語法複習，直接進入後端系統的實務建構。每週包含：學習目標、為什麼這樣安排、實作步驟、本週練習、驗收標準。

## 總覽

| 週次 | 主題 | 產出 |
|---|---|---|
| W1 | FastAPI 專案架構與基礎 API | 可執行的 Hello API 專案骨架 |
| W2 | PostgreSQL 安裝與連線 | 資料庫連線成功、建立第一個 table、加入API |
| W3 | SQLAlchemy ORM + Alembic Migration | Model 定義與版本化的 schema |
| W4 | CRUD API 完整實作 | 一組完整的 RESTful CRUD 端點 |
| W5 | 關聯式設計（一對多、多對多） | 多資料表關聯查詢 |
| W6 | 身份驗證（JWT / OAuth2） | 登入、保護路由 |
| W7 | 測試（pytest） | 自動化測試覆蓋 CRUD + Auth |
| W8 | 非同步與連線池 | Async ORM 操作、效能觀念 |
| W9 | 進階查詢：分頁、篩選、搜尋 | Query 參數化的 API |
| W10 | 錯誤處理、Logging、Middleware | 具生產等級的錯誤回應與紀錄 |
| W11 | Docker 化 | docker-compose 一鍵啟動 API + DB |
| W12 | 部署與整合專題 | 完整可展示的後端專案 |

---

## W1：FastAPI 專案架構與基礎 API

### 學習目標
理解 FastAPI (Python) 的專案結構慣例，以及它跟 (Node.js) Express.js / Spring Boot 這類框架的對應關係。

### 為什麼這樣安排
自學 REST API 設計，不花時間講「什麼是 API」，而是直接建立你之後 12 週都會沿用的專案骨架，這樣後面每週只需要疊加功能。

### 操作步驟

* install Python Install Manager (Windows Market)

```bash
mkdir api
cd api
py -m venv venv
venv\Scripts\activate      # Windows Powershell, Set-ExecutionPolicy
pip install fastapi uvicorn[standard]
```

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

建立專案結構：開始學習與思考自己或團隊習慣的program structures
```
api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   └── __init__.py
│   ├── core/
│   │   └── __init__.py
│   └── models/
│       └── __init__.py
├── requirements.txt
└── venv/
```

`app/main.py`：
```python
from fastapi import FastAPI

app = FastAPI(title="My Backend API")

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

啟動：
```bash
uvicorn app.main:app --reload
```

打開 `http://127.0.0.1:8888/docs`，這是 FastAPI 自動產生的 Swagger UI（對應你熟悉的 Swagger/OpenAPI 概念，但這裡完全自動產生，不用手寫 YAML）。

### 本週練習
1. 新增一個 `/version` 端點，回傳 `{"version": "0.1.0"}`
2. 用 Pydantic 定義一個 `Item` 模型（含 `name: str`、`price: float`），寫一個 `POST /items` 接收並回傳它
3. 執行 `pip freeze > requirements.txt`，理解這個檔案對應 Node.js 的 `package.json` 扮演什麼角色
4. AI：為 py + fastapi + psql 建立 .gitignore
5. Install Git、建立 github repo，並push and commit

```git
# 1. 建立本機第一個 commit
git add .
git commit -m "W1: FastAPI Test"

# 2. 設定 GitHub 遠端 repository
git remote add origin https://github.com/icsie/api.git

# 3. 設定主分支名稱
git branch -M main

# 4. 發現 GitHub 已有 Initial commit，因此先取得遠端歷史
git fetch origin

# 5. 合併本機與 GitHub 的不同歷史
git merge origin/main --allow-unrelated-histories

# 6. 推送到 GitHub
git push -u origin main
```

### 驗收標準

- [x] `/docs` 能正常開啟並看到自訂端點
- [x] `POST /items` 能正確驗證型別（試著傳錯誤型別，觀察 FastAPI 自動回傳的 422 錯誤）
- [x] 了解建立根目錄的 .gitignore，涵蓋：Python 虛擬環境與快取、pytest、coverage、mypy、ruff 產物、.env 設定檔、FastAPI/Uvicorn log、PostgreSQL 本地資料與備份、VS Code、IDE 與作業系統檔案
- [x] 學會 `.gitignore`：`!` 取消忽略，例如 !.env.example 會保留範例設定檔。
- [x] add .env.example，並commit and push確認出現自github repo。

### Powershell經驗
- AI：let powershell can run .ps1 by default ==> PowerShell can now run local .ps1 scripts by default for your user via `RemoteSigned`. Downloaded scripts must still be signed or unblocked (考慮到資安問題).

### VSCode心得
- 安裝軟體如Git，會寫入環境變數PATH，要完全結束VSCode (close all opened code windows)，reopen vscode才會在powershell環境生效。

### Git心得
- 本機先有 commit 時，GitHub 建立 repository 最好保持完全空白；不要同時勾選建立 README 或 LICENSE，這樣第一次 `git push -u origin main` 最簡單。

---

## W2：PostgreSQL 安裝與連線

### 學習目標
在本機建立 PostgreSQL，並讓 Python 程式成功連線。

### 為什麼這樣安排
先確保「資料庫本身活著、連得上」，再進到 ORM 抽象層。這樣之後如果連線出錯，你能分辨是資料庫問題還是程式碼問題。

### 操作步驟

**安裝 PostgreSQL（Windows Admin）**
1. 到官方下載頁安裝 PostgreSQL（建議 16 版以上）
2. 安裝時會要求設定 `postgres` 超級使用者密碼，記下來
3. 建議一併安裝 pgAdmin（GUI 管理工具，對應你熟悉的 DBeaver / TablePlus 概念）

**安裝 PostgreSQL（Windows Users Permission，電腦教室用此法安裝）**

若目前帳號只有一般 `Users` 權限，建議使用 PostgreSQL ZIP 免安裝版。此方式不建立 Windows Service，也不需要寫入 `Program Files`，可安裝在使用者目錄。

1. 下載與作業系統相容的 PostgreSQL Windows ZIP binary。
2. 將 ZIP 解壓縮至使用者目錄，例如：

```text
C:\Users\<你的帳號>\pgsql
```

3. 建立資料目錄：

```powershell
mkdir "$env:USERPROFILE\pgsql-data"
```

4. 初始化資料庫叢集：

```powershell
cd "$env:USERPROFILE\pgsql"

.\bin\initdb.exe `
  -D "$env:USERPROFILE\pgsql-data" `
  -U postgres `
  -A scram-sha-256 `
  -W
```

執行後依提示設定 `postgres` 使用者密碼。

5. 啟動 PostgreSQL。若 `5432` 已被其他服務使用，可使用 `5433`：

```powershell
.\bin\pg_ctl.exe `
  -D "$env:USERPROFILE\pgsql-data" `
  -o "-p 5433" `
  -l "$env:USERPROFILE\pgsql-data\server.log" `
  start
```

6. 連線測試：

```powershell
.\bin\psql.exe `
  -h localhost `
  -p 5433 `
  -U postgres `
  -d postgres
```

7. 在 `psql` 中建立開發用資料庫與使用者：

```sql
CREATE USER dev_user WITH PASSWORD 'dev_password';
CREATE DATABASE fastapi_dev OWNER dev_user;
\c fastapi_dev
GRANT ALL ON SCHEMA public TO dev_user;
```

檢查是否成功寫入DB：

```sql
SELECT version(); SELECT current_database(), current_user;
```

結束PSQL DB：

```sql
exit
```

8. 修改 `.env`：

```env
DATABASE_URL=postgresql://dev_user:dev_password@localhost:5433/fastapi_dev
```

停止 PostgreSQL：

```powershell
.\bin\pg_ctl.exe `
  -D "$env:USERPROFILE\pgsql-data" `
  stop
```

> ZIP 版本不會自動建立 Windows Service，因此每次使用前需要執行 `pg_ctl start`。若要讓 PostgreSQL 開機自動啟動，通常需要系統管理員協助建立服務。


#### 建立開發用資料庫與使用者
```sql: add file .\psql\createdb.sql
-- 用 psql 或 pgAdmin 執行
CREATE DATABASE fastapi_dev;
CREATE USER dev_user WITH PASSWORD 'dev_password';
GRANT ALL PRIVILEGES ON DATABASE fastapi_dev TO dev_user;

\connect fastapi_dev
GRANT USAGE, CREATE ON SCHEMA public TO dev_user; -- public schema建表權限
```

```pwsh: psql 執行
& 'C:\Program Files\PostgreSQL\18\bin\psql.exe' `
  -U postgres `
  -d postgres `
  -f .\psql\createdb.sql
```

**Python 端安裝驅動**
```bash
pip install "psycopg[binary]" python-dotenv
```

`.env`（不要進版控，需加入 `.gitignore`）：
```
DATABASE_URL=postgresql://dev_user:dev_password@localhost:5432/fastapi_dev
```

測試連線 `app/core/db_test.py`：
```python
import os
from dotenv import load_dotenv
import psycopg

load_dotenv()

def test_connection():
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    print("連線成功:", conn.info.dbname)
    conn.close()

if __name__ == "__main__":
    test_connection()
```

```pwsh
python .\app\core\db_test.py
```

連線成功: fastapi_dev

### 本週練習
1. 用 `psql` 指令手動建立一個 `notes` table（欄位：`id`, `title`, `content`, `created_at`）；用 `INSERT` 手動塞3筆資料，再用 `SELECT` 查回來
2. New REST api: /note/{id}

### 驗收標準
- [ ] Python 程式能成功連上 PostgreSQL
- [ ] 能說明為什麼密碼要放在 `.env` 而不是寫死在程式碼裡（對應你熟悉的環境變數管理概念）
- [ ] Test API and data format (了解Swagger用法，具備測試API能力)

### 心得
- VScode Extension: SQLTools PostgreSQL/Cockroach Driver，方便VSCode可以執行SQL
- psql: 另外建立db帳號 (postgres權限勿濫用)，須要給予public schema建表權限
- AI coding會建立更清楚的program structures。E.g. routers (REST api path) -> repositories (get data SQL) -> schemas (response model)