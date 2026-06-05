"""Track A — UI / Boundary RED 스켈레톤.

SPEC.md §7.1 Dual-Track RED 설계표 기준.
RED 단계: 구현 코드 없음. 각 테스트는 pytest.fail("RED: ...")로 실패한다.
skip / xfail 금지.
"""

import pytest


def test_empty_input_format_error():  # U-IN-01
    # Given: "" (빈 입력)
    # Then: 형식 오류 메시지
    pytest.fail("RED: U-IN-01 빈 입력 형식 오류 미구현")


def test_missing_colon_format_error():  # U-IN-02
    # Given: "meter" (콜론 없음)
    # Then: 형식 오류
    pytest.fail("RED: U-IN-02 콜론 없는 입력 형식 오류 미구현")


def test_negative_value_rejected():  # U-IN-03
    # Given: "meter:-1"
    # Then: 음수 거부
    pytest.fail("RED: U-IN-03 음수 입력 거부 미구현")


def test_output_has_three_or_more_lines():  # U-OUT-01
    # Given: "meter:2.5"
    # Then: 3줄 이상 출력 (스켈레톤)
    pytest.fail("RED: U-OUT-01 전 단위 다중 라인 출력 미구현")
