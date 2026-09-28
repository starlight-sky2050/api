#測試連線PostgreSQL

import os

import psycopg
from dotenv import load_dotenv

# 載入 DATABASE_URL，讓這個獨立測試使用和 API 相同的設定。
load_dotenv()


def test_connection():
    """建立資料庫連線，印出資料庫名稱後關閉連線。"""

    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    print("連線成功:", conn.info.dbname)
    conn.close()


# 只有直接執行此檔案時才測試連線；被 import 時不會自動連線。
if __name__ == "__main__":
    test_connection()