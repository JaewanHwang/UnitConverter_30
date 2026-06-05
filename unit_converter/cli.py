"""CLI 경계 — 입력 파싱·검증·변환·포맷을 조립한다 (SPEC §4/§5)."""

from unit_converter.parser import InputParser
from unit_converter.validator import validate
from unit_converter.formatters import get_formatter

_PARSER = InputParser()


def render(text, converter, fmt="table", precision=4, echo=True):
    parsed = validate(_PARSER.parse(text))
    converter.registry.ensure_known(parsed.unit)  # 미등록 단위면 UnknownUnitError
    results = converter.convert_all(parsed.value, parsed.unit)

    body = get_formatter(fmt, precision=precision).format(results)

    # table 포맷은 입력 에코(헤더) 라인을 앞에 붙인다 (SPEC §3, U-OUT-01).
    if fmt == "table" and echo:
        header = f"{parsed.value} {parsed.unit}:"
        return [header, *body.splitlines()]
    return body.splitlines()
