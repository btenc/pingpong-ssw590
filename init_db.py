import sqlite3

DB_PATH = "db/pingpong.db"
SCHEMA_PATH = "db/schema.sql"

def main():
    connection = sqlite3.connect(DB_PATH)

    schema_file = open(SCHEMA_PATH, "r", encoding="utf-8")
    schema_sql = schema_file.read()
    schema_file.close()

    connection.executescript(schema_sql)
    connection.commit()

    connection.close()

if __name__ == "__main__":
    main()
