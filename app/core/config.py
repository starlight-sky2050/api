import os
from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv()

class Settings:
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "")
    
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    SESSION_SECRET_KEY: str = os.getenv("SESSION_SECRET_KEY", "")
    
    AUTH_COOKIE_SECURE: bool = os.getenv("AUTH_COOKIE_SECURE", "false").lower() == "true"
    ACCESS_TOKEN_EXPIRE_SECONDS: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", "28800"))
    AUTH_SUCCESS_REDIRECT_URL: str = os.getenv("AUTH_SUCCESS_REDIRECT_URL", "http://127.0.0.1:7777/docs")

settings = Settings()