"""UnitRegistry — 단위·비율 보관/조회/동적등록 (SPEC §4, NFR-01 OCP)."""

from unit_converter.exceptions import UnknownUnitError


class UnitRegistry:
    """`1 base = N unit` 형태의 meter→unit 비율을 보관한다."""

    def __init__(self, base="meter", ratios=None):
        self.base = base
        self._ratios = {base: 1.0}
        if ratios:
            self._ratios.update(ratios)

    def register(self, unit, meter_to_unit):
        self._ratios[unit] = meter_to_unit

    def ratio(self, unit):
        try:
            return self._ratios[unit]
        except KeyError:
            raise UnknownUnitError(unit)

    def units(self):
        return list(self._ratios)
