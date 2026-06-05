"""JsonFormatter — JSON 배열 출력 (EXT-03, F-JSN-01)."""

import json

from unit_converter.domain.models import ConversionResult


class JsonFormatter:
    def __init__(self, precision=4, indent=None):
        self.precision = precision
        self.indent = indent

    def format(self, results: list[ConversionResult], **_) -> str:
        payload = [
            {
                "source_unit": r.source_unit,
                "source_value": r.source_value,
                "target_unit": r.target_unit,
                "target_value": round(r.target_value, self.precision),
            }
            for r in results
        ]
        return json.dumps(payload, ensure_ascii=False, indent=self.indent)
