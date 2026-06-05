"""CLI 경계 — 입력 파싱·검증·변환을 조립해 출력 라인을 만든다 (SPEC §4/§5)."""

from unit_converter.parser import InputParser
from unit_converter.validator import validate

_PARSER = InputParser()


def render(text, converter, precision=4, echo=True):
    parsed = validate(_PARSER.parse(text))
    converter.registry.ensure_known(parsed.unit)  # 미등록 단위면 UnknownUnitError
    results = converter.convert_all(parsed.value, parsed.unit)

    lines = []
    if echo:
        lines.append(f"{parsed.value} {parsed.unit}:")  # 입력 에코(헤더) 라인
    lines.extend(
        f"{r.source_value} {r.source_unit} = {round(r.target_value, precision)} {r.target_unit}"
        for r in results
    )
    return lines
