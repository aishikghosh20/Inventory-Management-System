from dotenv import load_dotenv
import os
from pathlib import Path
import sys

if getattr(sys, "frozen", False):
    # Running as an executable
    BASE_DIR = Path(sys.executable).parent
else:
    # Running from source code
    BASE_DIR = Path(__file__).resolve().parent

env_path = BASE_DIR / ".env" # Path to .env

# Loading the enviourment variable
load_dotenv(env_path)

DB_HOST = os.getenv("DB_HOST")  
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
