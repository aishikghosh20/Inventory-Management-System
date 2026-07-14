from dotenv import load_dotenv
import os
from pathlib import Path
import sys

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent

    # Location of bundled files (schema.sql, etc.)
    RESOURCE_DIR = Path(getattr(sys, "_MEIPASS"))
else:
    BASE_DIR = Path(__file__).resolve().parent
    RESOURCE_DIR = BASE_DIR

env_path = BASE_DIR / ".env" # Path to .env

# Loading the enviourment variable
load_dotenv(env_path)

DB_HOST = os.getenv("DB_HOST")  
port = os.getenv("DB_PORT")
DB_PORT = int(port) if port else None
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
