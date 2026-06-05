"""CLI 경계 — 입력 파싱·검증·변환·포맷을 조립한다 (SPEC §4/§5)."""

import argparse

from unit_converter.parsing.parser import InputParser
from unit_converter.parsing.validator import validate
from unit_converter.output.formatters import get_formatter
from unit_converter.domain.converter import Converter
from unit_converter.app.assembler import build_registry

_PARSER = InputParser()


def render(text, converter, fmt="table", precision=4, json_indent=None):
    parsed = validate(_PARSER.parse(text))
    converter.registry.ensure_known(parsed.unit)  # 미등록 단위면 UnknownUnitError
    results = converter.convert_all(parsed.value, parsed.unit)

    formatter_kwargs = {"precision": precision}
    if fmt == "json" and json_indent is not None:
        formatter_kwargs["indent"] = json_indent
    formatter = get_formatter(fmt, **formatter_kwargs)
    if fmt == "table":
        body = formatter.format(
            results,
            source_unit=parsed.unit,
            source_value=parsed.value,
            units=converter.registry.units(),
        )
    else:
        body = formatter.format(results)
    return body.splitlines()


def _build_parser():
    p = argparse.ArgumentParser(prog="unit_converter", description="길이 단위 변환 CLI")
    p.add_argument("input", help="변환 입력 (예: meter:2.5)")
    p.add_argument("--format", dest="fmt", default="table",
                   choices=["table", "json", "csv"], help="출력 포맷")
    p.add_argument("--config", dest="config", help="비율 설정 파일 (units.json)")
    p.add_argument("--register", dest="register", action="append", default=[],
                   metavar="UNIT=METER_TO_UNIT", help="동적 단위 등록 (예: cubit=0.4572)")
    p.add_argument("--precision", type=int, default=4, help="소수 자릿수")
    return p


def run_cli(argv):
    args = _build_parser().parse_args(argv)
    registry = build_registry(config_path=args.config, registrations=args.register)
    converter = Converter(registry)
    return render(args.input, converter, fmt=args.fmt, precision=args.precision)
