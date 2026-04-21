from zoneinfo import ZoneInfo


def process_checks(checks):
    processed = []

    for check in checks:
        date_utc = check["checked_at"]
        date_et = date_utc.astimezone(ZoneInfo("America/New_York"))
        formatted = date_et.strftime("%B %d, %Y at %I:%M %p")

        processed.append(
            {
                "id": check["id"],
                "endpoint_id": check["endpoint_id"],
                "checked_at": formatted,
                "status_code": check["status_code"],
                "response_time_ms": check["response_time_ms"],
                "success": check["success"],
                "error_message": check["error_message"],
            }
        )

    return processed


def format_timestamp(timestamp):
    date_et = timestamp.astimezone(ZoneInfo("America/New_York"))
    return date_et.strftime("%B %d, %Y at %I:%M %p")
