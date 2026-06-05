"""UnitRegistry — 단위·비율 보관/조회/동적등록 (SPEC §4, NFR-01 OCP)."""

from unit_converter.exceptions import UnknownUnitError

DEFAULT_RATIOS = {"feet": 3.28084, "yard": 1.09361}


def default_registry():
    """설정 파일이 없을 때 사용하는 기본 비율 레지스트리."""
    return UnitRegistry(base="meter", ratios=dict(DEFAULT_RATIOS))


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

    def ensure_known(self, unit):
        """미등록 단위면 UnknownUnitError. 비율 조회 책임을 registry로 모은다."""
        self.ratio(unit)

    def units(self):
        return list(self._ratios)
