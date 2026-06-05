"""Registry 조립 — 설정 로드/동적 등록을 한 책임으로 모은다 (SPEC §4, SRP).

CLI(인자 파싱)와 도메인(registry/converter) 사이의 조립 책임을 분리한다.
"""

from unit_converter.registry import default_registry
from unit_converter.config import load_config


def build_registry(config_path=None, registrations=None):
    """설정 파일 또는 기본 비율로 레지스트리를 만들고 동적 등록을 적용한다.

    registrations: ["unit=meter_per_unit", ...] 형태.
    `1 unit = X meter` 의미이므로 meter→unit 비율 = 1/X 로 환산한다 (EXT-02).
    """
    registry = load_config(config_path) if config_path else default_registry()
    for item in registrations or []:
        unit, _, value = item.partition("=")
        registry.register(unit.strip(), 1 / float(value))
    return registry
