"""CLI 경계 — 입력 파싱·검증·변환을 조립해 출력 라인을 만든다 (SPEC §4/§5)."""

from unit_converter.parser import parse
from unit_converter.validator import validate


def render(text, converter, precision=4):
    parsed = validate(parse(text))
    converter.registry.ratio(parsed.unit)  # 미등록 단위면 UnknownUnitError
    results = converter.convert_all(parsed.value, parsed.unit)
    return [
        f"{r.source_value} {r.source_unit} = {round(r.target_value, precision)} {r.target_unit}"
        for r in results
    ]
