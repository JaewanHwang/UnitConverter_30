"""Track A — UI / Boundary (GREEN).

SPEC.md §7.1 Dual-Track RED 설계표 기준. 최소 구현으로 통과시킨다.

U-OUT-01: 입력 에코(헤더) 1줄 + 변환 라인(입력 단위 제외)으로 총 3줄 이상.
변환 라인은 SPEC §3대로 입력 단위 자기 자신을 제외한다.
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


def test_output_has_three_or_more_lines():  # U-OUT-01
    # Given: "meter:2.5" → Then: 에코 헤더 + 변환 라인 = 3줄 이상
    lines = render("meter:2.5", _converter())
    assert len(lines) >= 3
