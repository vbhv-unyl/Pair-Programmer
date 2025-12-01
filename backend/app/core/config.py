# app/config.py
from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "sharecode-backend")
APP_ENV = os.getenv("APP_ENV", "development")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/sharecode")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
