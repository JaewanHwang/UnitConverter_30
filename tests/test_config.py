"""EXT-01 설정 파일 정상 로드 (GREEN).

SPEC.md §7.1 Track D (C-CFG-02).
(깨진 파일 케이스 D-CFG-01은 test_convert.py에서 검증됨.)
"""

import json

from unit_converter.output.config import load_config


def test_load_config_json_applies_ratios(tmp_path):  # C-CFG-02
    cfg = tmp_path / "units.json"
    cfg.write_text(
        json.dumps({"base": "meter", "ratios": {"feet": 3.28084, "yard": 1.09361}}),
        encoding="utf-8",
    )
    registry = load_config(str(cfg))
    assert registry.base == "meter"
    assert registry.ratio("feet") == 3.28084
    assert set(registry.units()) == {"meter", "feet", "yard"}
