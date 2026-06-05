"""OutputFormatter 전략 인터페이스 (SPEC §4, EXT-03)."""

from typing import Protocol

from unit_converter.domain.models import ConversionResult


class OutputFormatter(Protocol):
    def format(self, results: list[ConversionResult]) -> str: ...
