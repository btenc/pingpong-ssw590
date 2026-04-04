from collections import Counter
import datetime as dt
from zoneinfo import ZoneInfo
from dateutil import parser


def process_checks(checks):
    processed = []

    for i in range(0, len(checks)):
        date_utc = parser.parse(checks[i]["checked_at"])
        date_et = date_utc.astimezone(ZoneInfo("America/New_York"))
        formatted = date_et.strftime("%B %d, %Y at %I:%M %p")

        processed.append(
            {
                "id": checks[i]["id"],
                "endpoint_id": checks[i]["endpoint_id"],
                "checked_at": formatted,
                "status_code": checks[i]["status_code"],
                "response_time_ms": checks[i]["response_time_ms"],
                "success": checks[i]["success"],
                "error_message": checks[i]["error_message"],
            }
        )

    return processed


def get_status_counts(checks):
    codes = [check["status_code"] for check in checks]
    codes = ["Unknown" if code is None else code for code in codes]

    counts = Counter(codes)

    result = {str(code): count for code, count in counts.items()}

    return result
