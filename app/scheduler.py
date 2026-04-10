import threading
import time
import app.checker as checker
import app.database as database


def _run():
    while True:
        config = database.get_config()
        time.sleep(config["check_interval_seconds"] if config else 60)

        try:
            checker.check_all_active_endpoints()
        except Exception as e:
            print(f"[scheduler] Error during checks: {e}")


def start():
    thread = threading.Thread(target=_run, daemon=True, name="pingpong-scheduler")
    thread.start()
