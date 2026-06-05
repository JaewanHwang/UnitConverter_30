"""도메인 예외 (SPEC §4)."""


class InvalidFormatError(ValueError):
    """입력이 `unit:value` 형식이 아니거나 값이 숫자가 아닐 때."""


class NegativeValueError(ValueError):
    """길이 값이 음수일 때."""


class UnknownUnitError(KeyError):
    """등록되지 않은 단위일 때."""


class ConfigError(Exception):
    """설정 파일 로드/파싱 실패."""


class UnknownFormatError(ValueError):
    """지원하지 않는 출력 포맷일 때."""
