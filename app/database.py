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

    with open(SCHEMA_FILE_PATH, "r", encoding="utf-8") as schema_file:
        schema_sql = schema_file.read()

    connection = get_connection()
    connection.executescript(schema_sql)
    connection.commit()
    connection.close()


def add_endpoint(name, url):
    connection = get_connection()

    row = connection.execute(
        """
        INSERT INTO endpoints (name, url)
        VALUES (?, ?)
        """,
        (name, url),
    )

    connection.commit()

    endpoint_id = row.lastrowid

    connection.close()

    return get_endpoint_by_id(endpoint_id)


def get_all_endpoints():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            e.*,
            MAX(c.checked_at) AS last_checked,
            ROUND(100.0 * SUM(c.success) / COUNT(c.id), 1) AS uptime_pct
        FROM endpoints e
        LEFT JOIN checks c ON c.endpoint_id = e.id
        GROUP BY e.id
        ORDER BY e.id ASC
        """
    ).fetchall()

    connection.close()

    return rows


def get_active_endpoints():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM endpoints
        WHERE is_active = 1
        ORDER BY id ASC
        """
    ).fetchall()

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


def get_status_code_counts(endpoint_id):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            COALESCE(status_code, 'Unknown') AS status_code,
            COUNT(*) AS count
        FROM checks
        WHERE endpoint_id = ?
        GROUP BY status_code
        """,
        (endpoint_id,),
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


def update_endpoint(endpoint_id, name=None, url=None, is_active=None):
    fields = []
    values = []

    if name is not None:
        fields.append("name = ?")
        values.append(name)

    if url is not None:
        fields.append("url = ?")
        values.append(url)

    if is_active is not None:
        fields.append("is_active = ?")
        values.append(is_active)

    if not fields:
        return get_endpoint_by_id(endpoint_id)

    values.append(endpoint_id)

    connection = get_connection()
    connection.execute(
        f"UPDATE endpoints SET {', '.join(fields)} WHERE id = ?",
        values,
    )
    connection.commit()
    connection.close()

    return get_endpoint_by_id(endpoint_id)


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


def get_config():
    connection = get_connection()

    row = connection.execute(
        """
        SELECT check_interval_seconds
        FROM config
        WHERE id = 1
        """
    ).fetchone()

    connection.close()
    return row


def update_config(check_interval_seconds):
    connection = get_connection()

    connection.execute(
        """
        UPDATE config
        SET check_interval_seconds = ?
        WHERE id = 1
        """,
        (check_interval_seconds,),
    )

    connection.commit()
    connection.close()

    return get_config()


def get_endpoint_stats(endpoint_id):
    connection = get_connection()

    stats = connection.execute(
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

    connection.close()

    return stats
