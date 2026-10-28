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

    return ResolvedConf(**final_config)
