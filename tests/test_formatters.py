"""EXT-03 출력 포맷 RED 스켈레톤 (table / json / csv).

SPEC.md §7.1 Dual-Track 확장. RED 단계: 구현 코드 없음.
각 테스트는 pytest.fail("RED: ...")로 실패한다. skip / xfail 금지.

대상 Test ID:
- F-TBL-01: table 포맷 직렬화
- F-JSN-01: json 포맷 직렬화
- F-CSV-01: csv 포맷 직렬화
- F-REG-01: get_formatter 전략 선택 (미지원 포맷 오류)
"""

import pytest


def test_table_formatter_serializes():  # F-TBL-01
    # Given: 변환 결과 → When: table 포맷 → Then: "src = val unit" 라인 문자열
    pytest.fail("RED: F-TBL-01 TableFormatter 미구현")


def test_json_formatter_serializes():  # F-JSN-01
    # Given: 변환 결과 → When: json 포맷 → Then: 파싱 가능한 JSON 배열
    pytest.fail("RED: F-JSN-01 JsonFormatter 미구현")


def test_csv_formatter_serializes():  # F-CSV-01
    # Given: 변환 결과 → When: csv 포맷 → Then: 헤더 + 행 CSV
    pytest.fail("RED: F-CSV-01 CsvFormatter 미구현")


def test_get_formatter_unknown_raises():  # F-REG-01
    # Given: "xml"(미지원) → When: get_formatter → Then: 명확한 오류
    pytest.fail("RED: F-REG-01 get_formatter 전략 선택/미지원 오류 미구현")
