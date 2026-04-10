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
    FOREIGN KEY(endpoint_id) REFERENCES endpoints(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS config (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    check_interval_seconds INTEGER NOT NULL DEFAULT 60
);

INSERT OR IGNORE INTO config (id, check_interval_seconds)
VALUES (1, 60);
