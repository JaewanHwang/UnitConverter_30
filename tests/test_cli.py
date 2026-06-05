"""Track D — CLI Integration (GREEN).

SPEC.md §7.1 Track D 기준. run_cli(argv) 조립 검증.
"""

import json

from unit_converter.cli import run_cli


def test_cli_default_table():  # C-CLI-01
    lines = run_cli(["meter:2.5"])
    assert lines[0] == "2.5 meter:"
    assert "2.5 meter = 8.2021 feet" in lines
    assert len(lines) >= 3


def test_cli_format_json():  # C-CLI-02
    out = "\n".join(run_cli(["meter:2.5", "--format", "json"]))
    parsed = json.loads(out)
    assert {r["target_unit"] for r in parsed} == {"feet", "yard"}


def test_cli_config_load(tmp_path):  # C-CLI-03
    cfg = tmp_path / "units.json"
    cfg.write_text(
        json.dumps({"base": "meter", "ratios": {"feet": 3.28084}}), encoding="utf-8"
    )
    out = "\n".join(run_cli(["meter:1", "--config", str(cfg), "--format", "json"]))
    parsed = json.loads(out)
    # 설정에 feet만 있으므로 yard는 없어야 한다 (EXT-01 비율 반영)
    assert {r["target_unit"] for r in parsed} == {"feet"}


def test_cli_register_dynamic_unit():  # C-CLI-04
    out = "\n".join(run_cli(["cubit:1", "--register", "cubit=0.4572", "--format", "json"]))
    parsed = json.loads(out)
    by_unit = {r["target_unit"]: r["target_value"] for r in parsed}
    # 1 cubit = 0.4572 m → meter 변환값이 0.4572 (EXT-02)
    assert round(by_unit["meter"], 4) == 0.4572
