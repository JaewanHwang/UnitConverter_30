"""Track D — CLI Integration RED 스켈레톤.

SPEC.md §7.1 Track D 기준. RED 단계: 구현 코드 없음.
각 테스트는 pytest.fail("RED: ...")로 실패한다. skip / xfail 금지.

대상: unit_converter.cli.run_cli(argv) — 인자 파싱 + 조립 (EXT-01/02/03 wiring)
"""

import pytest


def test_cli_default_table():  # C-CLI-01
    # Given: ["meter:2.5"] → When: run_cli → Then: table 출력 (에코 헤더 포함)
    pytest.fail("RED: C-CLI-01 run_cli 기본 table 출력 미구현")


def test_cli_format_json():  # C-CLI-02
    # Given: ["meter:2.5", "--format", "json"] → Then: JSON 출력
    pytest.fail("RED: C-CLI-02 --format json 미구현")


def test_cli_config_load():  # C-CLI-03
    # Given: ["meter:2.5", "--config", "units.json"] → Then: 설정 비율 로드 (EXT-01)
    pytest.fail("RED: C-CLI-03 --config 로드 미구현")


def test_cli_register_dynamic_unit():  # C-CLI-04
    # Given: ["cubit:1", "--register", "cubit=0.4572"] → Then: 동적 등록 후 변환 (EXT-02)
    pytest.fail("RED: C-CLI-04 --register 동적 등록 미구현")
