"""domain — 길이 변환 핵심 도메인 (모델·레지스트리·변환기)."""

from unit_converter.domain.models import ParsedInput, ConversionResult
from unit_converter.domain.registry import UnitRegistry, default_registry, DEFAULT_RATIOS
from unit_converter.domain.converter import Converter

__all__ = [
    "ParsedInput",
    "ConversionResult",
    "UnitRegistry",
    "default_registry",
    "DEFAULT_RATIOS",
    "Converter",
]
