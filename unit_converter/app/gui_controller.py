"""GuiController — PyQt와 도메인 사이의 테스트 가능한 Presenter (GUI-01/02/03).

GUI 위젯은 I/O만 담당하고, 변환·검증·포맷은 기존 render() 파이프라인을 재사용한다.
"""

from unit_converter.app.cli import render
from unit_converter.domain.converter import Converter
from unit_converter.domain.registry import default_registry
from unit_converter.output.formatters.table import build_table_rows
from unit_converter.parsing.parser import InputParser
from unit_converter.parsing.validator import validate

_PARSER = InputParser()


class GuiController:
    def __init__(self, registry=None):
        self._converter = Converter(registry or default_registry())

    def available_units(self) -> list[str]:
        return self._converter.registry.units()

    def convert(
        self,
        unit: str,
        value: str,
        fmt: str = "table",
        precision: int = 4,
        pretty_json: bool = True,
    ) -> list[str]:
        json_indent = 2 if fmt == "json" and pretty_json else None
        return render(
            f"{unit}:{value}",
            self._converter,
            fmt=fmt,
            precision=precision,
            json_indent=json_indent,
        )

    def convert_table_rows(
        self, unit: str, value: str, precision: int = 4
    ) -> list[tuple[str, str, str]]:
        """GUI QTableWidget용 (unit, input, result) 행."""
        parsed = validate(_PARSER.parse(f"{unit}:{value}"))
        self._converter.registry.ensure_known(parsed.unit)
        results = self._converter.convert_all(parsed.value, parsed.unit)
        return build_table_rows(
            results,
            parsed.unit,
            parsed.value,
            self._converter.registry.units(),
            precision,
        )
