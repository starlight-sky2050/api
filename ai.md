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
