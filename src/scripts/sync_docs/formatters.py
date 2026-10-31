from typing import Any, Literal, Union, get_args, get_origin

from .constants import NAME_MAP, TYPE_DISPLAY_NAMES


def format_command_value(val: Any) -> str:
    """Formats command values for documentation, keeping @notations intact as code tags."""
    if isinstance(val, str):
        return f"`{val}`"
    elif isinstance(val, list):
        return " → ".join(format_command_value(v) for v in val)
    elif isinstance(val, dict):
        parts = []
        for k, v in val.items():
            label = NAME_MAP.get(k, k)
            formatted_v = format_command_value(v)
            parts.append(f"{label}: {formatted_v}")
        return "<br>".join(parts)
    return f"`{val}`"


def is_compiled_config(val: Any) -> bool:
    """Determines whether a command configuration represents a compiled language."""
    if isinstance(val, dict):
        if "compile" in val and "run" in val:
            return True
        for sub_val in val.values():
            if is_compiled_config(sub_val):
                return True
    return False


def format_type_hint(tp: Any) -> str:
    """Recursively resolves type aliases and formats type hints for Markdown."""
    if hasattr(tp, "__value__"):
        return format_type_hint(tp.__value__)

    origin = get_origin(tp)
    if origin is Union or type(tp).__name__ == "UnionType":
        args = get_args(tp)
        parts = []
        for arg in args:
            if arg is type(None) or arg is None:
                continue
            else:
                formatted_arg = format_type_hint(arg)
                if formatted_arg not in parts:
                    parts.append(formatted_arg)
        return " / ".join(
            f"`{part}`" if not part.startswith("`") else part for part in parts
        )

    if origin is Literal or getattr(tp, "__name__", "") == "Literal":
        return " / ".join(f'`"{arg}"`' for arg in get_args(tp))

    if tp is type(None) or tp is None:
        return "`None`"

    tp_str = str(tp)
    prefixes_to_strip = [
        "quikrun.config.types.",
        "typing.",
        "pathlib.",
        "<class '",
        "'>",
    ]
    for prefix in prefixes_to_strip:
        tp_str = tp_str.replace(prefix, "")

    display_name = TYPE_DISPLAY_NAMES.get(tp_str)
    if display_name is None and tp_str.startswith("list["):
        display_name = "array"

    return f"`{display_name or tp_str}`"

