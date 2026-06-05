"""InputParser — "unit:value" → ParsedInput (SPEC §4, FR-01/FR-05)."""

from unit_converter.exceptions import InvalidFormatError
from unit_converter.domain.models import ParsedInput


class InputParser:
    """`unit:value` 문자열을 구조화 객체로 변환한다 (순수, I/O 없음)."""

    SEP = ":"

    def parse(self, text):
        if text is None or self.SEP not in text:
            raise InvalidFormatError(f"형식 오류: '{text}' (unit:value 형식 필요)")

        unit, _, value_str = text.partition(self.SEP)
        unit = unit.strip()
        if not unit:
            raise InvalidFormatError("형식 오류: 단위가 비어 있음")

        try:
            value = float(value_str)
        except ValueError:
            raise InvalidFormatError(f"형식 오류: 숫자가 아님 '{value_str}'")

        return ParsedInput(unit, value)


_DEFAULT_PARSER = InputParser()


def parse(text):
    """모듈 레벨 하위호환 래퍼."""
    return _DEFAULT_PARSER.parse(text)
