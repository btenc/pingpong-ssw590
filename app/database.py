import os
import sqlite3
from app.config import DATABASE_FOLDER, DATABASE_PATH, SCHEMA_FILE_PATH


def ensure_database_folder_exists():
    if not os.path.exists(DATABASE_FOLDER):
        os.makedirs(DATABASE_FOLDER)


def get_connection():
    ensure_database_folder_exists()

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def create_tables():
    ensure_database_folder_exists()

    schema_file = open(SCHEMA_FILE_PATH, "r", encoding="utf-8")
    schema_sql = schema_file.read()
    schema_file.close()

    connection = get_connection()
    connection.executescript(schema_sql)
    connection.commit()
    connection.close()


def add_endpoint(name, url):
    connection = get_connection()

    if url is not None and name is not None:
        row = connection.execute(
            """
            INSERT INTO endpoints (name, url)
            VALUES (?, ?)
            """,
            (name, url),
        )

    elif url is None:
        row = connection.execute(
            """
            INSERT INTO endpoints (url)
            VALUES (?)
            """,
            (url),
        )

    else:
        row = connection.execute(
            """
            INSERT INTO endpoints (name)
            VALUES (?)
            """,
            (name),
        )

    connection.commit()

    endpoint_id = row.lastrowid

    connection.close()

    return get_endpoint_by_id(endpoint_id)


def get_all_endpoints():
    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM endpoints
        ORDER BY id ASC
        """).fetchall()

    connection.close()

    return rows


def get_active_endpoints():
    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM endpoints
        WHERE is_active = 1
        ORDER BY id ASC
        """).fetchall()

    connection.close()
    return rows


def get_endpoint_by_id(endpoint_id):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT *
        FROM endpoints
        WHERE id = ?
        """,
        (endpoint_id,),
    ).fetchone()

    connection.close()
    return row


def add_check(
    endpoint_id, checked_at, status_code, response_time_ms, success, error_message
):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO checks (
            endpoint_id,
            checked_at,
            status_code,
            response_time_ms,
            success,
            error_message
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            endpoint_id,
            checked_at,
            status_code,
            response_time_ms,
            success,
            error_message,
        ),
    )

    connection.commit()
    connection.close()


def get_recent_checks(limit=50):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            checks.id,
            checks.endpoint_id,
            checks.checked_at,
            checks.status_code,
            checks.response_time_ms,
            checks.success,
            checks.error_message,
            endpoints.name AS endpoint_name,
            endpoints.url AS endpoint_url
        FROM checks
        JOIN endpoints
            ON checks.endpoint_id = endpoints.id
        ORDER BY checks.id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()

    connection.close()
    return rows


def get_checks_for_endpoint(endpoint_id, limit=100):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM checks
        WHERE endpoint_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (endpoint_id, limit),
    ).fetchall()

    connection.close()
    return rows


def update_endpoint(endpoint_id, name, url):
    connection = get_connection()

    if name is not None and url is not None:
        connection.execute(
            """
            UPDATE endpoints
            SET name = ?, url = ?
            WHERE id = ?
            """,
            (name, url, endpoint_id),
        )

    elif name is None:
        connection.execute(
            """
            UPDATE endpoints
            SET url = ?
            WHERE id = ?
            """,
            (url, endpoint_id),
        )

    else:
        connection.execute(
            """
            UPDATE endpoints
            SET name = ?
            WHERE id = ?
            """,
            (name, endpoint_id),
        )

    connection.commit()
    connection.close()

    updated_endpoint = get_endpoint_by_id(endpoint_id)
    return updated_endpoint


def delete_endpoint(endpoint_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM endpoints WHERE id = ?
        """,
        (endpoint_id,),
    )
    endpoint = cursor.fetchone()

    cursor.execute(
        """
        DELETE FROM checks
        WHERE endpoint_id = ?
        """,
        (endpoint_id,),
    )

    cursor.execute(
        """
        DELETE FROM endpoints
        WHERE id = ?
        """,
        (endpoint_id,),
    )

    connection.commit()

    is_deleted = cursor.rowcount > 0

    connection.close()

    return (is_deleted, endpoint)


def avg_check_response_time(endpoint_id):
    connection = get_connection()

    avg = connection.execute(
        """
        SELECT
            AVG(c.response_time_ms) AS avg_response_time,
            COUNT(c.id) AS total_checks,
            SUM(CASE WHEN c.success = 0 THEN 1 ELSE 0 END) AS failed_checks
        FROM checks c
        JOIN endpoints e
        ON c.endpoint_id = e.id
        WHERE e.id = ?
        GROUP BY e.id
        """,
        (endpoint_id,),
    ).fetchone()

    connection.commit()
    connection.close()

    return avg
