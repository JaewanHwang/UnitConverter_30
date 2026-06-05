"""데이터 계약 (SPEC §4)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedInput:
    unit: str
    value: float


@dataclass(frozen=True)
class ConversionResult:
    source_unit: str
    source_value: float
    target_unit: str
    target_value: float
