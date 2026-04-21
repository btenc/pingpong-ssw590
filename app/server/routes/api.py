from flask import Blueprint, jsonify, request
import app.database as database
from app.validation import validate_endpoint_id, validate_limit, validate_string
import app.checker as checker
import bleach

api_bp = Blueprint("api", __name__, url_prefix="/api")


# GET /api/endpoints
@api_bp.route("/endpoints")
def get_all_endpoints():
    try:
        endpoints = database.get_all_endpoints()
        endpoints = [dict(endpoint) for endpoint in endpoints]
        return jsonify(endpoints)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET /api/endpoints/{id}
@api_bp.route("/endpoints/<id>")
def get_endpoint(id):
    try:
        id = validate_endpoint_id(id, "Endpoint Id")
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    try:
        endpoint = database.get_endpoint_by_id(id)
        return jsonify(dict(endpoint))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# POST /api/endpoints
@api_bp.route("/endpoints", methods=["POST"])
def add_endpoint():
    data = request.get_json()
    name = data.get("endpointName")
    url = data.get("endpointUrl")

    if name is None or url is None:
        return jsonify({"error": "Must provide both a name and a url."}), 400

    if name is not None:
        try:
            name = validate_string(name, "Endpoint Name")
            name = bleach.clean(name)

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    if url is not None:
        try:
            url = validate_string(url, "Endpoint URL")
            url = bleach.clean(url)

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    try:
        new_endpoint = dict(database.add_endpoint(name, url))
        return jsonify(new_endpoint)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# PATCH /api/endpoints/{id}
@api_bp.route("/endpoints/<id>", methods=["PATCH"])
def patch_endpoint(id):
    try:
        id = validate_endpoint_id(id, "Endpoint Id")

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    data = request.get_json()
    name = data.get("endpointName")
    url = data.get("endpointUrl")
    is_active = data.get("isActive")

    if name is None and url is None and is_active is None:
        return jsonify({"error": "Must provide a new name, url, and/or isActive."}), 400

    if name is not None:
        try:
            name = validate_string(name, "Endpoint Name")
            name = bleach.clean(name)

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    if url is not None:
        try:
            url = validate_string(url, "Endpoint URL")
            url = bleach.clean(url)

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    if is_active is not None:
        if not isinstance(is_active, bool):
            return jsonify({"error": "isActive must be a boolean."}), 400

    try:
        patched_endpoint = dict(database.update_endpoint(id, name, url, is_active))
        return jsonify(patched_endpoint)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# DELETE /api/endpoints/{id}
@api_bp.route("/endpoints/<id>", methods=["DELETE"])
def delete_endpoint(id):
    try:
        id = validate_endpoint_id(id, "Endpoint Id")

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    try:
        status, endpoint = database.delete_endpoint(id)
        return jsonify({"is_deleted": status, "endpoint": dict(endpoint)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET /api/checks?limit=20
@api_bp.route("/checks")
def get_checks():
    limit = request.args.get("limit")

    if limit is None:
        limit = 20
    else:
        try:
            limit = validate_limit(limit, "Limit")

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    try:
        checks = database.get_recent_checks(limit)
        checks = [dict(check) for check in checks]
        return jsonify(checks)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET /api/endpoints/checks
@api_bp.route("/endpoints/checks")
def get_endpoint_checks():
    try:
        checks = checker.check_all_active_endpoints()
        return jsonify(checks)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# POST /api/endpoints/<id>/check
@api_bp.route("/endpoints/<int:id>/check", methods=["POST"])
def check_one(id):
    try:
        endpoint = database.get_endpoint_by_id(id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if endpoint is None:
        return jsonify({"error": "Endpoint not found."}), 404

    try:
        result = checker.check_one_endpoint(endpoint)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET /api/config
@api_bp.route("/config")
def get_config():
    try:
        config = database.get_config()
        return jsonify(dict(config))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# PATCH /api/config
@api_bp.route("/config", methods=["PATCH"])
def update_config():
    data = request.get_json()
    check_interval_seconds = data.get("checkIntervalSeconds")

    if check_interval_seconds is None:
        return jsonify({"error": "Must provide checkIntervalSeconds."}), 400

    try:
        check_interval_seconds = int(check_interval_seconds)
        if check_interval_seconds < 1:
            raise ValueError()
    except (ValueError, TypeError):
        return (
            jsonify({"error": "checkIntervalSeconds must be a positive integer."}),
            400,
        )

    try:
        updated_config = database.update_config(check_interval_seconds)
        return jsonify(dict(updated_config))

    except Exception as e:
        return jsonify({"error": str(e)}), 500
