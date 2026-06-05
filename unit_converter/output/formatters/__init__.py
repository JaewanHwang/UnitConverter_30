"""출력 포맷 전략 레지스트리 (SPEC §4.1, EXT-03).

새 포맷 추가 = 클래스 추가 + FORMATTERS 등록. (OCP)
"""

from unit_converter.exceptions import UnknownFormatError
from unit_converter.output.formatters.table import TableFormatter
from unit_converter.output.formatters.json_fmt import JsonFormatter
from unit_converter.output.formatters.csv_fmt import CsvFormatter

FORMATTERS = {
    "table": TableFormatter,
    "json": JsonFormatter,
    "csv": CsvFormatter,
}


def get_formatter(name, **kwargs):
    try:
        factory = FORMATTERS[name]
    except KeyError:
        raise UnknownFormatError(f"지원하지 않는 포맷: '{name}' (지원: {', '.join(FORMATTERS)})")
    return factory(**kwargs)
