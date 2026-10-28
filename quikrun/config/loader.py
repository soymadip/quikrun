import copy
lazy import tomllib
lazy import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .defaults import DEFAULT_CONF
from .types import Config, ResolvedConf
from ..lib.logger import log

type CfgList = list[None | Config | Path | tuple[Path, str]]


class CfgLoadError(Exception): ...


# TODO: expand '@ext' variables


def _update_dict(
    base_dict: dict[str, Any], update_dict: dict[str, Any]
) -> dict[str, Any]:
    """
    Recursively updates base_dict in place with values from update_dict.
    Skips any key not in base_dict or whose value is explicitly None.
    """
    for key, value in update_dict.items():
        # Skip if key is not in base_dict or Value is explicitely null
        if key not in base_dict or value is None:
            continue

        if isinstance(base_dict[key], dict) and isinstance(value, dict):
            # Recursively update the nested dictionary in place
            _update_dict(base_dict[key], value)
        else:
            # Assign a deep copy of the update value
            base_dict[key] = copy.deepcopy(value)

    return base_dict


def _resolve_references(cmd_dict: dict[str, Any]) -> dict[str, Any]:
    """Resolve any @ references up to 2 levels deep for strings, lists, and dicts."""

    def resolve_item(item: Any, depth: int) -> Any:
        if depth >= 3:
            return item

        # Handle string
        if isinstance(item, str) and "@" in item:
            ref_key = item.split("@")[-1]
            if ref_key in cmd_dict:
                return resolve_item(cmd_dict[ref_key], depth + 1)
            else:
                log.error(f"Couldn't find reference key: {ref_key}")
                raise CfgLoadError(f"Reference key '{ref_key}' not found.")

        # Handle lists
        elif isinstance(item, list):
            resolved_list = []
            for sub_item in item:
                res = resolve_item(sub_item, depth)
                if isinstance(res, list):
                    resolved_list.extend(res)
                else:
                    resolved_list.append(res)
            return resolved_list

        # dictionaries
        elif isinstance(item, dict):
            return {k: resolve_item(v, depth) for k, v in item.items()}

        return item

    temp_cmd_cfg = {}
    for key, value in cmd_dict.items():
        temp_cmd_cfg[key] = resolve_item(value, 0)

    return temp_cmd_cfg


def load_config(configs: CfgList) -> ResolvedConf:
    """
    Merge & Load Config from given config files
    Files should be in highest to lowest priority
    """
    final_config = asdict(DEFAULT_CONF)

    for cfg_entry in configs:
        if not cfg_entry:
            continue

        elif isinstance(cfg_entry, Config):
            _update_dict(final_config, asdict(cfg_entry))

        else:
            file: Path | None = None
            part: str | None = None

            if isinstance(cfg_entry, tuple):
                file = cfg_entry[0]
                part = cfg_entry[1]
            else:
                file = cfg_entry

            if not file.exists() or not file.is_file():
                continue

            config: dict = {}
            file_ext = file.suffix

            try:
                omode, encoding = (
                    ("rb", None) if file_ext == ".toml" else ("r", "utf-8")
                )
                with open(file, omode, encoding=encoding) as f:
                    match file_ext:
                        case ".toml":
                            config = tomllib.load(f)
                        case ".json":
                            config = json.load(f)

            except (tomllib.TOMLDecodeError, json.JSONDecodeError) as e:
                log.error("Invalid Syntax in Config:", log.fmt(str(file), "GRAY"))
                log.error("Error:", str(e))
                raise CfgLoadError

            except OSError as e:
                log.error("Failed to Open Config File: ", log.fmt(str(file), "GRAY"))
                log.error('Error:', str(e))
                raise CfgLoadError

            if part:
                for key in part.split("."):
                    config = config.get(key, "")

            if not config:
                continue

            # Validates the keys defined in the config dict
            try:
                config = asdict(Config(**config))
            except TypeError as e:
                log.error(
                    "invalid Keys detected in Config file:", log.fmt(str(file), "GRAY")
                )
                log.error("Error:", str(e).removeprefix("Config.__init__()").strip())
                raise CfgLoadError

            _update_dict(final_config, config)

    final_config["commands"] = _resolve_references(final_config["commands"])

    return ResolvedConf(**final_config)
