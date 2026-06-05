"""Validator — 음수 등 도메인 검증 (SPEC §4, FR-04)."""

from unit_converter.exceptions import NegativeValueError


def validate(parsed):
    if parsed.value < 0:
        raise NegativeValueError(f"음수 거부: {parsed.value}")
    return parsed
