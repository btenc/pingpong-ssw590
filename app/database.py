from dotenv import load_dotenv
import os
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from app.config import SCHEMA_FILE_PATH, ENV_FILE_PATH


def get_connection():
    if os.getenv("DB_NAME") is None:
        load_dotenv(ENV_FILE_PATH)

    connection = connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )

    cursor = connection.cursor(cursor_factory=RealDictCursor)

    return connection, cursor


def create_tables():
    with open(SCHEMA_FILE_PATH, "r", encoding="utf-8") as schema_file:
        schema_sql = schema_file.read()

    connection, cursor = get_connection()
    cursor.execute(schema_sql)
    connection.commit()
    connection.close()


def add_endpoint(name, url):
    connection, cursor = get_connection()

    cursor.execute(
        """
        INSERT INTO endpoints (name, url)
        VALUES (%s, %s)
        RETURNING id
        """,
        (name, url),
    )

    endpoint_id = cursor.fetchone()["id"]

    connection.commit()
    connection.close()

    return get_endpoint_by_id(endpoint_id)


def get_all_endpoints():
    connection, cursor = get_connection()

    cursor.execute("""
        SELECT
            e.*,
            MAX(c.checked_at) AS last_checked,
            ROUND(100.0 * SUM(CASE WHEN c.success THEN 1 ELSE 0 END) / NULLIF(COUNT(c.id), 0), 1) AS uptime_pct
        FROM endpoints e
        LEFT JOIN checks c ON c.endpoint_id = e.id
        GROUP BY e.id
        ORDER BY e.id ASC
        """)

    rows = cursor.fetchall()

    connection.close()

    return rows


def get_active_endpoints():
    connection, cursor = get_connection()

    cursor.execute("""
        SELECT *
        FROM endpoints
        WHERE is_active = true
        ORDER BY id ASC
        """)

    rows = cursor.fetchall()

    connection.close()
    return rows


def get_endpoint_by_id(endpoint_id):
    connection, cursor = get_connection()

    cursor.execute(
        """
        SELECT *
        FROM endpoints
        WHERE id = %s
        """,
        (endpoint_id,),
    )

    row = cursor.fetchone()

    connection.close()
    return row


def add_check(
    endpoint_id, checked_at, status_code, response_time_ms, success, error_message
):
    connection, cursor = get_connection()

    cursor.execute(
        """
        INSERT INTO checks (
            endpoint_id,
            checked_at,
            status_code,
            response_time_ms,
            success,
            error_message
        )
        VALUES (%s, %s, %s, %s, %s, %s)
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
    connection, cursor = get_connection()

    cursor.execute(
        """
        SELECT
            COALESCE(status_code::TEXT, 'Unknown') AS status_code,
            COUNT(*) AS count
        FROM checks
        WHERE endpoint_id = %s
        GROUP BY status_code
        """,
        (endpoint_id,),
    )

    rows = cursor.fetchall()

    connection.close()
    return rows


def get_checks_for_endpoint(endpoint_id, limit=100):
    connection, cursor = get_connection()

    cursor.execute(
        """
        SELECT *
        FROM checks
        WHERE endpoint_id = %s
        ORDER BY id DESC
        LIMIT %s
        """,
        (endpoint_id, limit),
    )

    rows = cursor.fetchall()

    connection.close()
    return rows


def update_endpoint(endpoint_id, name=None, url=None, is_active=None):
    fields = []
    values = []

    if name is not None:
        fields.append("name = %s")
        values.append(name)

    if url is not None:
        fields.append("url = %s")
        values.append(url)

    if is_active is not None:
        fields.append("is_active = %s")
        values.append(is_active)

    if not fields:
        return get_endpoint_by_id(endpoint_id)

    values.append(endpoint_id)

    connection, cursor = get_connection()
    cursor.execute(
        f"UPDATE endpoints SET {', '.join(fields)} WHERE id = %s",
        values,
    )
    connection.commit()
    connection.close()

    return get_endpoint_by_id(endpoint_id)


def delete_endpoint(endpoint_id):
    connection, cursor = get_connection()

    cursor.execute(
        """
        SELECT * FROM endpoints WHERE id = %s
        """,
        (endpoint_id,),
    )
    endpoint = cursor.fetchone()

    cursor.execute(
        """
        DELETE FROM checks
        WHERE endpoint_id = %s
        """,
        (endpoint_id,),
    )

    cursor.execute(
        """
        DELETE FROM endpoints
        WHERE id = %s
        """,
        (endpoint_id,),
    )

    connection.commit()

    is_deleted = cursor.rowcount > 0

    connection.close()

    return (is_deleted, endpoint)


def get_config():
    connection, cursor = get_connection()

    cursor.execute("""
        SELECT check_interval_seconds
        FROM config
        WHERE id = 1
        """)

    row = cursor.fetchone()

    connection.close()
    return row


def update_config(check_interval_seconds):
    connection, cursor = get_connection()

    cursor.execute(
        """
        UPDATE config
        SET check_interval_seconds = %s
        WHERE id = 1
        """,
        (check_interval_seconds,),
    )

    connection.commit()
    connection.close()

    return get_config()


def get_endpoint_stats(endpoint_id):
    connection, cursor = get_connection()

    cursor.execute(
        """
        SELECT
            AVG(c.response_time_ms) AS avg_response_time,
            COUNT(c.id) AS total_checks,
            SUM(CASE WHEN c.success = false THEN 1 ELSE 0 END) AS failed_checks
        FROM checks c
        JOIN endpoints e
        ON c.endpoint_id = e.id
        WHERE e.id = %s
        GROUP BY e.id
        """,
        (endpoint_id,),
    )

    stats = cursor.fetchone()

    connection.close()

    return stats
