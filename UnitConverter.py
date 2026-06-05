"""레거시 진입점 — unit_converter 패키지로 위임하는 얇은 shim.

기존 인터랙티브 실행(`python UnitConverter.py`)을 유지하되, 변환/검증/출력
로직은 모두 unit_converter 패키지를 재사용한다. (중복 로직·매직 넘버 제거)
신규 CLI: `python -m unit_converter "meter:2.5" [--format ...]`
"""

from unit_converter.cli import run_cli
from unit_converter.exceptions import (
    InvalidFormatError,
    NegativeValueError,
    UnknownUnitError,
)


def main():
    text = input("Insert value for converting (ex: meter:2.5): ")
    try:
        for line in run_cli([text]):
            print(line)
    except (InvalidFormatError, NegativeValueError, UnknownUnitError) as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
