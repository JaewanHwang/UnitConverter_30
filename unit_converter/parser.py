"""InputParser — "unit:value" → ParsedInput (SPEC §4, FR-01/FR-05)."""

from unit_converter.exceptions import InvalidFormatError
from unit_converter.models import ParsedInput


def parse(text):
    if text is None or ":" not in text:
        raise InvalidFormatError(f"형식 오류: '{text}' (unit:value 형식 필요)")

    unit, _, value_str = text.partition(":")
    unit = unit.strip()
    if not unit:
        raise InvalidFormatError("형식 오류: 단위가 비어 있음")

    try:
        value = float(value_str)
    except ValueError:
        raise InvalidFormatError(f"형식 오류: 숫자가 아님 '{value_str}'")

    return ParsedInput(unit, value)
