Q : 我想討論一個問題，就是我的檔案為啥會多出一堆老師給的檔案，可能是哪個環節出錯了

A :

這通常是**解壓縮**或 **Git Clone** 時的層級重疊造成的，是新手在管理專案時非常容易踩到的雷。

主要有以下 3 種最常見的踩雷情境：

* **解壓縮包中包（最常見）**： 老師給的 zip 檔解開後裡面自帶了一個 `fastapi-backend` 資料夾，但你在解壓或建立 VS Code 專案時，直接把這個資料夾「拖進」了你原本就開好的 `Dbs` 專案目錄裡，導致出現 `Dbs/fastapi-backend/app` 與外層 `Dbs/app` 雙層並存的狀況。
* **在現有專案內執行 `git clone`**： 你原本已經在 `Dbs` 資料夾開好專案，後來又在 `Dbs` 裡面執行了 `git clone <老師的專案網址>`。Git 會自動在裡面再建一個同名資料夾，把程式碼整包下載進去。
* **手動複製貼上時選錯目標資料夾**： 想把老師給的範例 `app` 抓進來時，沒有把舊的覆蓋或取代，而是直接把整包 `fastapi-backend` 夾帶複製進了根目錄。

fastapi-backend是我自己創建的，所以是我在git clone出了錯誤

---

Q : `app` 資料夾為什麼長這樣？

A :

* **`routers/`（路由層）**：專門寫 API 網址的地方^^！例如 `users.py` 處理使用者 API，`items.py` 處理商品 API。
* **`schemas/`（資料型別定義層）**：定義 API 輸入與輸出的 JSON 格式（使用 Pydantic），做資料驗證。
* **`repositories/` 或 `crud/`（資料庫存取層）**：專門負責對資料庫做新增、讀取、更新、刪除（CRUD）操作。
* **`core/`（核心設定層）**：放置全域設定，例如讀取 `.env` 密碼的設定檔（`config.py`）、資料庫連線池設定（`database.py`）或安全性驗證（`security.py`）。

---

Q : main.py 到底可以寫些什麼？

A :

`main.py` 是整個後端程式的 **「總開關與進入點（Entrypoint）」**。

* **應該寫**：
  1. 建立 `app = FastAPI()` 實體。
  2. 載入並註冊各個路由：`app.include_router(users.router)`。
  3. 設定 CORS（跨域權限）、中間件（Middleware）與啟動事件。
  4. 掛載靜態檔案：`app.mount("/", ...)`。
* **不該寫**：不要把幾十個 API 的具體商業邏輯全部塞在這裡，API 應該拆去 `routers/` 裡面寫。

---

Q : FastAPI 收到 POST 資料後，資料真的會寫進資料庫嗎？關掉網站再重開，資料還會在嗎？

A :

要看 POST API 的實作。這個專案的 `POST /api/note` 會呼叫 repository 執行 `INSERT`，並用 `connection.commit()` 提交交易；只要 PostgreSQL 的資料庫沒有被清空或重建，關閉瀏覽器或重新啟動 FastAPI 後，資料仍會保留，可以用 `GET /api/note` 再查詢。

但 `POST /api/items` 目前只把收到的內容放進回應，沒有執行資料庫寫入，所以重開後不會保留。判斷資料是否真的保存，可以檢查 API 是否執行資料庫寫入並提交交易，而不只看它有沒有回傳成功訊息。

---

Q : 這次新增 Team、User、Permission、Tag 實體時，完整需求與分層規範是什麼？

A :

新增實體時，依照 Asset 模組的 Repository Pattern，分成 SQLAlchemy Model、Pydantic Schema、Repository、FastAPI Router，並在 `app/main.py` 註冊模型和路由。`app/core/db.py` 的 `create_db_tables()` 也要將新模型的資料表加入建表清單。

* **Team**：資料表 `teams`。欄位為 `tid`（Integer 主鍵、自動遞增）、`team_name`（String(100)、不可為空、唯一）、`description`（String(500)、可為空）、`invite_code`（String(50)、不可為空、唯一）、`created_at`（預設 `datetime.utcnow`）。Schema 包含 `TeamBase`、`TeamCreate`、`TeamUpdate`、`TeamResponse`；建立時可自行提供邀請碼，未提供時自動產生。Repository 提供 CRUD 與 `get_by_invite_code()`。
* **User**：資料表 `users`，避免使用 PostgreSQL 保留字 `user`。欄位為 `uid`（Integer 主鍵、自動遞增）、`username`（String(100)、不可為空、唯一）、`email`（String(255)、不可為空、唯一）、`password`（String(255)、不可為空，儲存雜湊值）、`created_at`（預設 `datetime.utcnow`）。Schema 包含 `UserBase`、`UserCreate`、`UserUpdate`、`UserResponse`；回應不得包含 password，建立和更新時需將密碼雜湊後儲存。Repository 除 CRUD 外提供 `get_by_email()`、`get_by_username()`。
* **Permission**：資料表 `permissions`。欄位為 `pid`（Integer 主鍵、自動遞增）、`pcode`（String(100)、不可為空、唯一）。Schema 包含 `PermissionBase`、`PermissionCreate`、`PermissionUpdate`、`PermissionResponse`。Repository 除 CRUD 外提供 `get_by_pcode()`。
* **Tag**：資料表 `tags`。欄位為 `tgid`（Integer 主鍵、自動遞增）、`tag_name`（String(100)、不可為空、唯一）、`tag_type`（String(50)、可為空）。Schema 包含 `TagBase`、`TagCreate`、`TagUpdate`、`TagResponse`。Repository 除 CRUD 外提供 `get_by_name()`。

四個 Router 分別使用 `/api/teams`、`/api/users`、`/api/permissions`、`/api/tags` 作為 prefix，透過 `Depends(get_db_session)` 注入 SQLAlchemy Session。每個 Router 都提供列表 GET、建立 POST、單筆 GET、PATCH 更新及 DELETE；POST 回傳 201 Created，DELETE 回傳 204 No Content，不存在的單筆資料回傳 404。各 Response Schema 均使用 `ConfigDict(from_attributes=True)`，並只暴露該實體允許回傳的欄位。

---

Q : 如何為資料庫 View `v_team_members` 與 `v_asset_details` 新增唯讀 API？

A :

新增 `app/schemas/views.py` 定義 `TeamMemberViewResponse` 和 `AssetDetailViewResponse`，依 View 欄位提供對應的回應型別。`app/repositories/views.py` 的 `ViewRepository` 使用 SQLAlchemy `text()` 和綁定參數查詢 View；`app/routers/views.py` 提供 `GET /api/views/teams/{tid}/members` 及 `GET /api/views/assets/{aid}`，並在 `app/main.py` 註冊 router。這些端點只執行讀取；找不到資產詳細資料時回傳 404。實際查詢需以資料庫已建立這兩個 View 為前提。

---

Q : 如何透過 PostgreSQL Stored Function `add_team_member` 新增團隊成員？

A :

在 `app/schemas/team.py` 定義 `AddTeamMemberRequest`，包含 `uid` 和預設為 `False` 的 `is_owner`。`TeamRepository.add_member_via_function()` 透過 SQLAlchemy 執行 `SELECT add_team_member(:tid, :uid, :is_owner)`，並在成功後提交交易。`app/routers/team.py` 新增 `POST /api/teams/{tid}/members`，成功時回傳 201；呼叫 Function 失敗時回傳 HTTP 400。

---

Q : 如何讓新增團隊成員端點回傳 Stored Function 的實際錯誤訊息，並確保失敗交易回滾？

A :

Repository 將 SQLAlchemy `text()` 查詢存入 `query` 變數後，以綁定參數呼叫 Function。Router 捕捉例外後呼叫注入的 `session.rollback()`，並將 `str(exc)` 設為 HTTP 400 的 `detail`，因此可在 Swagger UI 看到底層錯誤文字。這種做法可能暴露資料庫內部資訊，正式環境應限制錯誤細節的可見範圍。
