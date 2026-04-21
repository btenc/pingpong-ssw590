# PingPong

A simple endpoint monitoring tool. Add URLs and PingPong will automatically ping them on a set interval, tracking uptime and response times.

## Stack
- Python / Flask - web server and API
- PostgreSQL - database
- Tailwind CSS - styling
- ApexCharts - status code pie chart
- requests - HTTP checks
- threading / time - background scheduler
- zoneinfo - timezone conversion
- python-dateutil - timestamp parsing
- bleach - input sanitization
- black - formatting standard

## Running
1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python run.py`

The database is created automatically and saved to `./db/pingpong.db` on first run. Server runs at http://127.0.0.1:5000.

## GUI
- `/` - dashboard, all endpoints
- `/endpoint/<id>` - endpoint detail, checks history

## API
- `GET /api/endpoints` - get all endpoints
- `POST /api/endpoints` - create endpoint
- `GET /api/endpoints/<id>` - get one endpoint
- `PATCH /api/endpoints/<id>` - update endpoint (name, url, active)
- `DELETE /api/endpoints/<id>` - delete endpoint and its checks
- `POST /api/endpoints/<id>/check` - run a check for one endpoint
- `GET /api/endpoints/checks` - manually trigger a check run for all endpoints
- `GET /api/checks?limit=N` - get N most recent checks
- `GET /api/config` - get config
- `PATCH /api/config` - update check interval

## Development
1. `pip install -r requirements-dev.txt`
2. `npm install`
3. `npm run tailwind` (watch and recompile CSS)
4. `python -m black .` to format
