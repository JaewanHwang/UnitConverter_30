"""Golden Master 테스트 헬퍼."""

from pathlib import Path

import pytest

GOLDEN_DIR = Path(__file__).parent / "golden"


def pytest_addoption(parser):
    parser.addoption(
        "--update-golden",
        action="store_true",
        default=False,
        help="Golden Master 기대값 파일을 실제 출력으로 갱신한다.",
    )


@pytest.fixture
def golden(request):
    """실제 출력을 golden/ fixture와 비교한다."""

    def _assert(actual: str, filename: str) -> None:
        path = GOLDEN_DIR / filename
        if request.config.getoption("--update-golden"):
            path.write_text(actual, encoding="utf-8", newline="\n")
            return
        expected = path.read_text(encoding="utf-8")
        assert actual == expected, f"golden mismatch: {filename}"

    return _assert
