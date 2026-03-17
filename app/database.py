import sqlite3

DB_PATH = "db/pingpong.db"

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def add_endpoint(name, url):
    connection = get_connection()

    connection.execute(
        "INSERT INTO endpoints (name, url) VALUES (?, ?)",
        (name, url)
    )
    connection.commit()

    connection.close()

def get_active_endpoints():
    connection = get_connection()

    rows = connection.execute(
        "SELECT * FROM endpoints WHERE is_active = 1"
    ).fetchall()

    connection.close()
    return rows
