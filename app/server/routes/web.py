from flask import Blueprint, render_template, abort
from app.database import (
    get_all_endpoints,
    get_endpoint_by_id,
    get_checks_for_endpoint,
    get_status_code_counts,
    get_endpoint_stats,
)
from app.server.helpers import process_checks, format_timestamp

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def index():
    endpoints = get_all_endpoints()

    if endpoints is None:
        endpoints = []

    endpoints = [
        {**dict(e), "last_checked": format_timestamp(e["last_checked"])}
        for e in endpoints
    ]

    return render_template("index.html", endpoints=endpoints)


@web_bp.route("/endpoint/<int:id>")
def endpoint_id(id):
    endpoint = get_endpoint_by_id(id)

    if endpoint is None:
        abort(404)

    checks = get_checks_for_endpoint(id, 20)

    checks = process_checks(checks)
    code_data = {
        str(row["status_code"]): row["count"] for row in get_status_code_counts(id)
    }
    aggregate = get_endpoint_stats(id)

    return render_template(
        "endpoint.html",
        endpoint=endpoint,
        checks=checks,
        code_data=code_data,
        aggregate=aggregate,
    )
