"""GuiController — PyQt와 도메인 사이의 테스트 가능한 Presenter (GUI-01/02/03).

GUI 위젯은 I/O만 담당하고, 변환·검증·포맷은 기존 render() 파이프라인을 재사용한다.
"""

from unit_converter.app.cli import render
from unit_converter.domain.converter import Converter
from unit_converter.domain.registry import default_registry


class GuiController:
    def __init__(self, registry=None):
        self._converter = Converter(registry or default_registry())

    def available_units(self) -> list[str]:
        return self._converter.registry.units()

    def convert(self, unit: str, value: str, fmt: str = "table", precision: int = 4) -> list[str]:
        return render(f"{unit}:{value}", self._converter, fmt=fmt, precision=precision)
