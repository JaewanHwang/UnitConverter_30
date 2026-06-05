"""TableFormatter — 사람이 읽는 라인 출력 (EXT-03, F-TBL-01)."""

from unit_converter.domain.models import ConversionResult


class TableFormatter:
    def __init__(self, precision=4):
        self.precision = precision

    def format(self, results: list[ConversionResult]) -> str:
        return "\n".join(
            f"{r.source_value} {r.source_unit} = "
            f"{round(r.target_value, self.precision)} {r.target_unit}"
            for r in results
        )
