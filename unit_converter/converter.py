"""Converter — value → meter → 전 단위 (SPEC §3/§4, FR-02)."""

from unit_converter.models import ConversionResult


class Converter:
    def __init__(self, registry):
        self.registry = registry

    def to_meter(self, value, unit):
        return value / self.registry.ratio(unit)

    def convert_all(self, value, unit):
        meters = self.to_meter(value, unit)
        results = []
        for target in self.registry.units():
            if target == unit:
                continue
            results.append(
                ConversionResult(unit, value, target, meters * self.registry.ratio(target))
            )
        return results
