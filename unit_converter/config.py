"""ConfigLoader — units.json 비율 로드 (SPEC §5, EXT-01)."""

import json

from unit_converter.exceptions import ConfigError
from unit_converter.registry import UnitRegistry


def load_config(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"설정 파일 로드 실패: {path}") from exc

    base = data.get("base", "meter")
    ratios = data.get("ratios", {})
    return UnitRegistry(base=base, ratios=ratios)
