"""EXT-01 설정 파일 정상 로드 RED 스켈레톤.

SPEC.md §7.1 Track D (C-CFG-02). RED 단계: 구현 코드 없음.
pytest.fail("RED: ...")로 실패. skip / xfail 금지.

(깨진 파일 케이스 D-CFG-01은 test_convert.py에서 이미 검증됨.)
"""

import pytest


def test_load_config_json_applies_ratios():  # C-CFG-02
    # Given: 정상 units.json → When: load_config → Then: Registry에 비율 반영
    pytest.fail("RED: C-CFG-02 정상 설정 로드 → 비율 반영 검증 미구현")
