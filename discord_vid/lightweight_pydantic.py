"""
Lightweight dataclass conversion helper - provides pydantic-like dict-to-dataclass
conversion without the 5MB dependency overhead.
"""

from dataclasses import fields
from typing import get_args, get_origin


def _is_dataclass_type(field_type):
    """Check if a type is a dataclass."""
    return hasattr(field_type, "__dataclass_fields__")


def _convert_single_dataclass(value, field_type):
    """Convert a dict value to a dataclass instance if needed."""
    if not isinstance(value, dict):
        return value
    if not _is_dataclass_type(field_type):
        return value
    return to_dataclass(field_type, value)


def _convert_dict_values(value, field_type):
    """
    Convert dict values to dataclass instances
    if field type is dict[key, DataclassType].
    """
    if not isinstance(value, dict):
        return value

    if get_origin(field_type) not in (dict, type({})):
        return value

    args = get_args(field_type)
    if len(args) != 2 or not _is_dataclass_type(args[1]):
        return value

    value_type = args[1]
    return {
        k: to_dataclass(value_type, v) if isinstance(v, dict) else v
        for k, v in value.items()
    }


def to_dataclass(cls, data):
    """Convert a dict to a dataclass instance, handling nested dataclasses.

    Args:
        cls: The target dataclass type
        data: A dictionary to convert

    Returns:
        An instance of cls with dict values converted to nested dataclass instances
    """
    if not isinstance(data, dict):
        return data

    converted = {}
    for field in fields(cls):
        if field.name not in data:
            continue

        value = data[field.name]
        value = _convert_single_dataclass(value, field.type)
        value = _convert_dict_values(value, field.type)
        converted[field.name] = value

    return cls(**converted)
