"""TableFormatter — ASCII 그리드 테이블 출력 (EXT-03, F-TBL-01)."""

from unit_converter.domain.models import ConversionResult


def _format_input(value: float) -> str:
    """입력값 표시 — 10.0, 2.5 등 자연스러운 형태."""
    if float(value) == int(value):
        return f"{value:.1f}"
    text = f"{value:g}"
    return text if "." in text else f"{value:.1f}"


def _format_result(value: float, precision: int) -> str:
    return f"{round(value, precision):.{precision}f}"


def _render_grid(rows: list[tuple[str, str, str]]) -> str:
    """(unit, input, result) 행 목록을 ASCII 테이블로 직렬화한다."""
    header = ("unit", "input", "result")
    body = [header, *rows]
    widths = [max(len(row[i]) for row in body) for i in range(3)]
    aligns = ("<", ">", ">")

    def border() -> str:
        return "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def row(cells: tuple[str, str, str]) -> str:
        parts = [
            f" {cell:{align}{widths[i]}} "
            for i, (cell, align) in enumerate(zip(cells, aligns))
        ]
        return "|" + "|".join(parts) + "|"

    lines = [border(), row(header), border()]
    lines.extend(row(r) for r in rows)
    lines.append(border())
    return "\n".join(lines)


class TableFormatter:
    def __init__(self, precision=4):
        self.precision = precision

    def format(
        self,
        results: list[ConversionResult],
        *,
        source_unit: str | None = None,
        source_value: float | None = None,
        units: list[str] | None = None,
        **_,
    ) -> str:
        if source_unit is None or source_value is None or units is None:
            # 하위 호환: 컨텍스트 없으면 기존 라인 형식
            return "\n".join(
                f"{r.source_value} {r.source_unit} = "
                f"{round(r.target_value, self.precision)} {r.target_unit}"
                for r in results
            )

        converted = {r.target_unit: r.target_value for r in results}
        input_text = _format_input(source_value)
        rows = []
        for unit in units:
            if unit == source_unit:
                result_text = input_text
            else:
                result_text = _format_result(converted[unit], self.precision)
            rows.append((unit, input_text, result_text))
        return _render_grid(rows)
