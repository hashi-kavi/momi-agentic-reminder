import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    DB_PATH = "data/memory.db"
    MODEL_NAME = "gemini-2.5-flash"
