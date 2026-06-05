"""Track A — UI / Boundary (GREEN).

SPEC.md §7.1 Dual-Track RED 설계표 기준. 최소 구현으로 통과시킨다.

주의: U-OUT-01은 설계표에 "3줄 이상"으로 적혀 있으나, SPEC §3
"출력에는 입력 단위 자기 자신을 제외한다" 규칙상 meter 입력 시 feet/yard
2줄이 출력된다. 설계 SSOT(SPEC §3)를 따라 ">= 2줄"로 검증한다.
"""

import pytest

from unit_converter.converter import Converter
from unit_converter.registry import UnitRegistry
from unit_converter.parser import parse
from unit_converter.cli import render
from unit_converter.exceptions import InvalidFormatError, NegativeValueError

DEFAULT_RATIOS = {"feet": 3.28084, "yard": 1.09361}


def _converter():
    return Converter(UnitRegistry(base="meter", ratios=dict(DEFAULT_RATIOS)))


def test_empty_input_format_error():  # U-IN-01
    # Given: "" (빈 입력) → Then: 형식 오류
    with pytest.raises(InvalidFormatError):
        parse("")


def test_missing_colon_format_error():  # U-IN-02
    # Given: "meter" (콜론 없음) → Then: 형식 오류
    with pytest.raises(InvalidFormatError):
        parse("meter")


def test_negative_value_rejected():  # U-IN-03
    # Given: "meter:-1" → Then: 음수 거부
    with pytest.raises(NegativeValueError):
        render("meter:-1", _converter())


def test_output_has_multiple_lines():  # U-OUT-01
    # Given: "meter:2.5" → Then: 입력 단위 제외 전 단위 출력 (>= 2줄)
    lines = render("meter:2.5", _converter())
    assert len(lines) >= 2
