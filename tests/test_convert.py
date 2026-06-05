"""Track B — Domain / Logic RED 스켈레톤.

SPEC.md §7.1 Dual-Track RED 설계표 기준.
RED 단계: 구현 코드 없음. 각 테스트는 pytest.fail("RED: ...")로 실패한다.
skip / xfail 금지.
"""

import pytest


def test_to_meter_from_feet():  # D-CNV-01
    # Given: 1 feet  → When: to_meter
    # Then: 0.3048 m (±ε)
    pytest.fail("RED: D-CNV-01 to_meter(feet) 미구현")


def test_convert_all_meter_to_feet_5_digits():  # D-CNV-02
    # Given: 2.5 m → When: convert_all
    # Then: 8.20210 ft (5자리)
    pytest.fail("RED: D-CNV-02 convert_all 5자리 정밀도 미구현")


def test_convert_all_feet_to_yard_via_meter():  # D-CNV-03
    # Given: feet → yard → When: convert_all
    # Then: meter 경유 결과 일치
    pytest.fail("RED: D-CNV-03 meter 경유 변환 일치 미구현")


def test_register_dynamic_unit_cubit():  # D-REG-01
    # Given: register("cubit", 0.4572) → When: convert
    # Then: cubit 변환 기능 동작
    pytest.fail("RED: D-REG-01 동적 단위 등록(cubit) 미구현")


def test_load_broken_config_raises_config_error():  # D-CFG-01
    # Given: 깨진 json 파일 → When: load json
    # Then: ConfigError 발생
    pytest.fail("RED: D-CFG-01 깨진 설정 파일 ConfigError 미구현")
