"""UnitConverter — 길이 단위 변환 패키지 (PRD/SPEC 추적 가능 재구현).

도메인 단위 패키지 구성:
- domain   : models / registry / converter (순수 핵심)
- parsing  : parser / validator (입력 처리)
- output   : config / formatters (출력·외부 IO)
- app      : assembler / cli (조립·진입)
"""

from unit_converter.domain import (
    ParsedInput,
    ConversionResult,
    UnitRegistry,
    default_registry,
    Converter,
)
from unit_converter.parsing import InputParser, parse, validate
from unit_converter.output import load_config, get_formatter
from unit_converter.app import build_registry, render, run_cli
from unit_converter.exceptions import (
    InvalidFormatError,
    NegativeValueError,
    UnknownUnitError,
    ConfigError,
    UnknownFormatError,
)

__all__ = [
    "ParsedInput",
    "ConversionResult",
    "InputParser",
    "parse",
    "validate",
    "UnitRegistry",
    "default_registry",
    "Converter",
    "load_config",
    "build_registry",
    "get_formatter",
    "render",
    "run_cli",
    "InvalidFormatError",
    "NegativeValueError",
    "UnknownUnitError",
    "ConfigError",
    "UnknownFormatError",
]
