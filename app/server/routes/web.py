from flask import Blueprint, render_template
from app.database import get_all_endpoints, get_endpoint_by_id, get_checks_for_endpoint, avg_check_response_time
from app.server.helpers import process_checks, get_status_counts

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def index():
    endpoints = get_all_endpoints()

    if endpoints is None:
        endpoints = []

    print(endpoints)

    return render_template("index.html", endpoints=endpoints)

@web_bp.route("/endpoint/add")
def add_endpoint():
    return render_template("add-endpoint.html")

@web_bp.route("/endpoint/<id>")
def endpoint_id(id):
    endpoint = get_endpoint_by_id(id)
    checks = get_checks_for_endpoint(id, 20)

    checks = process_checks(checks)
    code_data = get_status_counts(checks)
    aggregate = avg_check_response_time(id)

    return render_template(
        "endpoint.html", endpoint=endpoint, checks=checks, code_data=code_data, aggregate=aggregate
    )
