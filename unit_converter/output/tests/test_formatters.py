"""EXT-03 출력 포맷 (table / json / csv) — GREEN.

SPEC.md §7.1 Track C 기준. 최소 구현으로 통과시킨다.
"""

import json

import pytest

from unit_converter.domain.models import ConversionResult
from unit_converter.output.formatters import get_formatter
from unit_converter.output.formatters.table import TableFormatter
from unit_converter.output.formatters.json_fmt import JsonFormatter
from unit_converter.output.formatters.csv_fmt import CsvFormatter
from unit_converter.exceptions import UnknownFormatError

RESULTS = [
    ConversionResult("meter", 2.5, "feet", 8.2021),
    ConversionResult("meter", 2.5, "yard", 2.734025),
]


def test_table_formatter_serializes():  # F-TBL-01
    out = TableFormatter().format(
        RESULTS,
        source_unit="meter",
        source_value=2.5,
        units=["meter", "feet", "yard"],
    )
    assert "| unit  | input | result |" in out
    assert "| meter |   2.5 |    2.5 |" in out
    assert "| feet  |   2.5 | 8.2021 |" in out
    assert "| yard  |   2.5 | 2.7340 |" in out


def test_json_formatter_serializes():  # F-JSN-01
    out = JsonFormatter().format(RESULTS)
    parsed = json.loads(out)
    assert isinstance(parsed, list) and len(parsed) == 2
    assert parsed[0]["target_unit"] == "feet"
    assert parsed[0]["target_value"] == 8.2021
    assert "\n" not in out


def test_json_formatter_pretty_indent():  # F-JSN-02
    out = JsonFormatter(indent=2).format(RESULTS)
    parsed = json.loads(out)
    assert len(parsed) == 2
    assert out.startswith("[\n")
    assert '  "target_unit": "feet"' in out


def test_csv_formatter_serializes():  # F-CSV-01
    out = CsvFormatter().format(RESULTS)
    lines = out.splitlines()
    assert lines[0] == "source_unit,source_value,target_unit,target_value"
    assert lines[1] == "meter,2.5,feet,8.2021"


def test_get_formatter_unknown_raises():  # F-REG-01
    with pytest.raises(UnknownFormatError):
        get_formatter("xml")
    assert isinstance(get_formatter("json"), JsonFormatter)
