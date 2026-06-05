"""Track B — Domain / Logic (GREEN).

SPEC.md §7.1 Dual-Track RED 설계표 기준. 최소 구현으로 통과시킨다.
"""

import pytest

from unit_converter.converter import Converter
from unit_converter.registry import UnitRegistry
from unit_converter.config import load_config
from unit_converter.exceptions import ConfigError

DEFAULT_RATIOS = {"feet": 3.28084, "yard": 1.09361}


def _converter():
    return Converter(UnitRegistry(base="meter", ratios=dict(DEFAULT_RATIOS)))


def test_to_meter_from_feet():  # D-CNV-01
    # Given: 1 feet → When: to_meter → Then: 0.3048 m (±ε)
    assert _converter().to_meter(1, "feet") == pytest.approx(0.3048, abs=1e-4)


def test_convert_all_meter_to_feet_5_digits():  # D-CNV-02
    # Given: 2.5 m → When: convert_all → Then: 8.20210 ft (5자리)
    results = {r.target_unit: r.target_value for r in _converter().convert_all(2.5, "meter")}
    assert round(results["feet"], 5) == 8.20210


def test_convert_all_feet_to_yard_via_meter():  # D-CNV-03
    # Given: feet → yard → Then: meter 경유 결과 일치
    conv = _converter()
    meters = conv.to_meter(1, "feet")
    results = {r.target_unit: r.target_value for r in conv.convert_all(1, "feet")}
    assert results["yard"] == pytest.approx(meters * 1.09361)


def test_register_dynamic_unit_cubit():  # D-REG-01
    # Given: register("cubit", 1/0.4572) → When: convert → Then: 1 cubit = 0.4572 m
    reg = UnitRegistry(base="meter", ratios=dict(DEFAULT_RATIOS))
    reg.register("cubit", 1 / 0.4572)
    conv = Converter(reg)
    assert conv.to_meter(1, "cubit") == pytest.approx(0.4572, abs=1e-6)


def test_load_broken_config_raises_config_error(tmp_path):  # D-CFG-01
    # Given: 깨진 json 파일 → When: load json → Then: ConfigError
    bad = tmp_path / "broken.json"
    bad.write_text("{ this is not valid json", encoding="utf-8")
    with pytest.raises(ConfigError):
        load_config(str(bad))
