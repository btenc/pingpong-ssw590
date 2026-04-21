CREATE TABLE IF NOT EXISTS endpoints (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS checks (
    id SERIAL PRIMARY KEY,
    endpoint_id INTEGER NOT NULL,
    checked_at TIMESTAMP NOT NULL,
    status_code INTEGER,
    response_time_ms REAL,
    success BOOLEAN NOT NULL DEFAULT FALSE,
    error_message TEXT,
    FOREIGN KEY(endpoint_id) REFERENCES endpoints(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS config (
    id INTEGER PRIMARY KEY,
    check_interval_seconds INTEGER NOT NULL DEFAULT 60,
    CHECK (id = 1)
);

INSERT INTO config (id, check_interval_seconds)
VALUES (1, 60)
ON CONFLICT (id) DO NOTHING;
