"""CLI 경계 — 입력 파싱·검증·변환·포맷을 조립한다 (SPEC §4/§5)."""

import argparse

from unit_converter.parser import InputParser
from unit_converter.validator import validate
from unit_converter.formatters import get_formatter
from unit_converter.converter import Converter
from unit_converter.registry import default_registry
from unit_converter.config import load_config

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


def _registry_from_args(args):
    # --config가 있으면 설정 로드, 없으면 기본 비율 (EXT-01)
    registry = load_config(args.config) if args.config else default_registry()
    # --register UNIT=METER_TO_UNIT 동적 등록 (EXT-02)
    # 입력은 "1 unit = X meter"의 X(meter당 비율)이므로 meter→unit = 1/X 로 환산
    for item in args.register:
        unit, _, value = item.partition("=")
        registry.register(unit.strip(), 1 / float(value))
    return registry


def run_cli(argv):
    args = _build_parser().parse_args(argv)
    converter = Converter(_registry_from_args(args))
    return render(args.input, converter, fmt=args.fmt, precision=args.precision)
