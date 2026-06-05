"""Golden Master — Safe Refactor 가드 (SPEC §3/§5).

리팩터링 전 현재 render() 출력을 스냅샷으로 고정한다.
이후 구조 변경(InputParser/registry 추출) 시 출력이 한 글자도 바뀌지 않아야 한다.
"""

from unit_converter.converter import Converter
from unit_converter.registry import UnitRegistry

DEFAULT_RATIOS = {"feet": 3.28084, "yard": 1.09361}


def _converter():
    return Converter(UnitRegistry(base="meter", ratios=dict(DEFAULT_RATIOS)))


def test_render_meter_golden():  # EXT-03 / FR-02
    from unit_converter.cli import render

    out = "\n".join(render("meter:2.5", _converter()))
    assert out == (
        "2.5 meter:\n"
        "2.5 meter = 8.2021 feet\n"
        "2.5 meter = 2.734 yard"
    )


def test_render_feet_golden():  # EXT-03 / FR-02
    from unit_converter.cli import render

    out = "\n".join(render("feet:10", _converter()))
    assert out == (
        "10.0 feet:\n"
        "10.0 feet = 3.048 meter\n"
        "10.0 feet = 3.3333 yard"
    )


def test_render_json_golden():  # EXT-03 (F-JSN-01 wiring)
    from unit_converter.cli import render

    out = "\n".join(render("meter:2.5", _converter(), fmt="json"))
    assert out == (
        '[{"source_unit": "meter", "source_value": 2.5, '
        '"target_unit": "feet", "target_value": 8.2021}, '
        '{"source_unit": "meter", "source_value": 2.5, '
        '"target_unit": "yard", "target_value": 2.734}]'
    )


def test_render_csv_golden():  # EXT-03 (F-CSV-01 wiring)
    from unit_converter.cli import render

    out = "\n".join(render("meter:2.5", _converter(), fmt="csv"))
    assert out == (
        "source_unit,source_value,target_unit,target_value\n"
        "meter,2.5,feet,8.2021\n"
        "meter,2.5,yard,2.734"
    )
