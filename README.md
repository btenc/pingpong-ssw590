# Ping Pong

## Formatting / Development
1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `pip install -r requirements-dev.txt`
5. `python -m black .`
6. `npm install`
7. `npm run tailwind` (let Tailwind watch for styling changes)

## Use the CLI demo:
1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python init_db.py` (create ./db/pingpong.db if not exists)
5. `python run_cli.py`

## GUI / API

### Start the Server
1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python init_db.py` (create ./db/pingpong.db if not exists)
5. `python run_gui.py`

### GUI Endpoints:
* `/`: Main dashboard
* `/endpoints/{id}`: More detailed endpoint info

### API Endpoints:
* `GET /api/endpoints`: Get all endpoints
* `POST /api/endpoints`: Create a new endpoint
* `GET /api/endpoints/{id}`: Get specified endpoint
* `PATCH /api/endpoints/{id}`: Update an existing endpoint
* `DELETE /api/endpoints/{id}`: Delete the specified endpoint
* `GET /api/endpoints/active`: Get all active endpoints
* `GET /api/endpoints/checks`: Get the result of checking all active endpoints
* `GET /api/checks?limit=N`: Get the N most recent endpoint checks

## What is does not do yet:
- No CI/CD
- Prettiying the GUI
- No running checks on schedule
- No data aggregation
