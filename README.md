# Ping Pong

## Formatting / Development
1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `pip install -r requirements-dev.txt`
5. `python -m black .`

## Use the CLI demo:
1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python init_db.py` (create ./db/pingpong.db if not exists)
5. `python run_cli.py`
- GUI placeholder: `python run_gui.py`

### What is does not do yet:
- No CI/CD
- No GUI
- No running checks on schedule
- No data aggregation
