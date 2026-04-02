from flask import Blueprint, render_template
from app.database import get_all_endpoints, get_endpoint_by_id, get_checks_for_endpoint
import datetime as dt
from zoneinfo import ZoneInfo
from dateutil import parser

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def index():
    endpoints = get_all_endpoints()

    if endpoints is None:
        endpoints = []

    print(endpoints)

    return render_template("index.html", endpoints=endpoints)


@web_bp.route("/endpoint/<id>")
def endpoint_id(id):
    endpoint = get_endpoint_by_id(id)
    checks = get_checks_for_endpoint(id, 20)

    formatted_checks = []

    for i in range(0, len(checks)):
        date_utc = parser.parse(checks[i]["checked_at"])
        date_et = date_utc.astimezone(ZoneInfo("America/New_York"))
        formatted = date_et.strftime("%B %d, %Y at %I:%M %p")

        formatted_checks.append(
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

    return render_template("endpoint.html", endpoint=endpoint, checks=formatted_checks)
