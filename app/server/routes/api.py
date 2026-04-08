from flask import Blueprint, jsonify, request
import app.database as database
from app.validation import validate_endpoint_id, validate_limit, validate_string
import app.checker as checker
import bleach

api_bp = Blueprint("api", __name__, url_prefix="/api")


# GET /endpoints
@api_bp.route("/endpoints")
def get_all_endpoints():
    try:
        endpoints = database.get_all_endpoints()
        endpoints = [dict(endpoint) for endpoint in endpoints]
        return jsonify(endpoints)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET /endpoints/{id}
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


# POST /endpoints
@api_bp.route("/endpoints", methods=["POST"])
def add_endpoint():
    data = request.get_json()
    name = data.get("endpointName")
    url = data.get("endpointUrl")

    if name is None and url is None:
        return jsonify({"error": "Must provide a new name and/or url."}), 400

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


# PATCH /endpoints/{id}
@api_bp.route("/endpoints/<id>", methods=["PATCH"])
def patch_endpoint(id):
    try:
        id = validate_endpoint_id(id, "Endpoint Id")

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    data = request.get_json()
    name = data.get("name")
    url = data.get("url")

    if name is None and url is None:
        return jsonify({"error": "Must provide a new name and/or url."}), 400

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
        patched_endpoint = dict(database.update_endpoint(id, name, url))
        return jsonify(patched_endpoint)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# DELETE /endpoints/{id}
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


# GET /checks?limit=20
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


# GET /endpoints/checks
@api_bp.route("/endpoints/checks")
def get_endpoint_checks():
    try:
        checks = checker.check_all_active_endpoints()
        return jsonify(checks)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET /endpoints/active
@api_bp.route("/endpoints/active")
def get_active_endpoints():
    try:
        endpoints = database.get_active_endpoints()
        endpoints = [dict(endpoint) for endpoint in endpoints]
        return jsonify(endpoints)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
