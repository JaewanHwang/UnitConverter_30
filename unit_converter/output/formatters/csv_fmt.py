"""CsvFormatter — CSV(헤더 + 행) 출력 (EXT-03, F-CSV-01)."""

import csv
import io

from unit_converter.domain.models import ConversionResult

HEADER = ["source_unit", "source_value", "target_unit", "target_value"]


class CsvFormatter:
    def __init__(self, precision=4):
        self.precision = precision

    def format(self, results: list[ConversionResult]) -> str:
        buf = io.StringIO()
        writer = csv.writer(buf, lineterminator="\n")
        writer.writerow(HEADER)
        for r in results:
            writer.writerow(
                [r.source_unit, r.source_value, r.target_unit, round(r.target_value, self.precision)]
            )
        return buf.getvalue().rstrip("\n")
