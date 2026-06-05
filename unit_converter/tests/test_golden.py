"""Golden Master — 교차 도메인 출력 회귀 가드 (SPEC §3/§5).

render() 전체 출력을 golden/ fixture 파일과 비교한다.
구조 변경 시 출력이 한 글자도 바뀌지 않아야 한다.

갱신: pytest --update-golden unit_converter/tests/test_golden.py
"""

from unit_converter.domain.converter import Converter
from unit_converter.domain.registry import UnitRegistry
from unit_converter.app.cli import render

DEFAULT_RATIOS = {"feet": 3.28084, "yard": 1.09361}


def _converter():
    return Converter(UnitRegistry(base="meter", ratios=dict(DEFAULT_RATIOS)))


def test_render_meter_golden(golden):  # EXT-03 / FR-02
    out = "\n".join(render("meter:2.5", _converter()))
    golden(out, "meter_table.txt")


def test_render_feet_golden(golden):  # EXT-03 / FR-02
    out = "\n".join(render("feet:10", _converter()))
    golden(out, "feet_table.txt")


def test_render_json_golden(golden):  # EXT-03 (F-JSN-01 wiring)
    out = "\n".join(render("meter:2.5", _converter(), fmt="json"))
    golden(out, "meter_json.txt")


def test_render_csv_golden(golden):  # EXT-03 (F-CSV-01 wiring)
    out = "\n".join(render("meter:2.5", _converter(), fmt="csv"))
    golden(out, "meter_csv.txt")
