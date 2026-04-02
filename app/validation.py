from typing import Any, Optional


def validate_string(obj: Any, obj_name: Optional[str]) -> str:
    if obj is None:
        raise Exception(f"{obj_name or "Object"} was not supplied.")

    if not isinstance(obj, str):
        raise Exception(f"{obj_name or "Object"} is not a string.")

    if len(obj.strip()) == 0:
        raise Exception(f"{obj_name or "String"} is empty.")

    return obj.strip()


def validate_number_string(num_str: Any, num_name: Optional[str]) -> int:
    num_str = validate_string(num_str, num_name)

    try:
        num = int(num_str)
    except:
        raise Exception(f"{num_name or "String"} cannot be converted to an number.")

    return num


def validate_endpoint_id(num_str: Any, num_name: Optional[str]) -> int:
    num = validate_number_string(num_str, num_name)

    if num <= 0:
        raise Exception(f"{num_name or "Number"} is not a valid id.")

    return num


def validate_limit(limit_str: Any, limit_name: Optional[str]) -> int:
    limit = validate_number_string(limit_str, limit_name)

    if limit < 0:
        raise Exception(f"{limit_name or "Number"} is not a valid limit.")

    return limit
