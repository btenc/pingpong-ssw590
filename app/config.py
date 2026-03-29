import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_FOLDER = os.path.join(PROJECT_ROOT, "db")
DATABASE_PATH = os.path.join(DATABASE_FOLDER, "pingpong.db")
SCHEMA_FILE_PATH = os.path.join(DATABASE_FOLDER, "schema.sql")
REQUEST_TIMEOUT_SECONDS = 10
