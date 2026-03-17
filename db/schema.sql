CREATE TABLE IF NOT EXISTS endpoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    endpoint_id INTEGER NOT NULL,
    checked_at TEXT NOT NULL,
    status_code INTEGER,
    response_time_ms REAL,
    success INTEGER NOT NULL,
    error_message TEXT,
    FOREIGN KEY(endpoint_id) REFERENCES endpoints(id)
);
