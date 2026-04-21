from datetime import datetime
import time
import requests
from app.config import REQUEST_TIMEOUT_SECONDS
from app.database import add_check, get_active_endpoints


def get_current_timestamp():
    return datetime.utcnow().isoformat() + "Z"


def status_code_means_success(status_code):
    if 200 <= status_code < 400:
        return True
    else:
        return False


def check_one_endpoint(endpoint_row):
    endpoint_id = endpoint_row["id"]
    endpoint_name = endpoint_row["name"]
    endpoint_url = endpoint_row["url"]

    checked_at = get_current_timestamp()

    try:
        start_time = time.perf_counter()

        response = requests.get(endpoint_url, timeout=REQUEST_TIMEOUT_SECONDS)

        end_time = time.perf_counter()

        status_code = response.status_code
        response_time_ms = (end_time - start_time) * 1000
        success = status_code_means_success(status_code)
        error_message = None

    except requests.RequestException as error:
        status_code = None
        response_time_ms = None
        success = 0
        error_message = str(error)

    add_check(
        endpoint_id=endpoint_id,
        checked_at=checked_at,
        status_code=status_code,
        response_time_ms=response_time_ms,
        success=success,
        error_message=error_message,
    )

    result = {
        "endpoint_id": endpoint_id,
        "endpoint_name": endpoint_name,
        "endpoint_url": endpoint_url,
        "checked_at": checked_at,
        "status_code": status_code,
        "response_time_ms": response_time_ms,
        "success": success,
        "error_message": error_message,
    }
    return result


def check_all_active_endpoints():
    active_endpoints = get_active_endpoints()

    results = []

    for endpoint_row in active_endpoints:
        result = check_one_endpoint(endpoint_row)
        results.append(result)

    return results
