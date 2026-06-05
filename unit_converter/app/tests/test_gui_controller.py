"""Track E — GUI Presenter (RED).

PyQt 창은 I/O 경계이므로, 테스트 가능한 GuiController가
단위·값·포맷을 받아 기존 render() 파이프라인 결과를 반환한다.

대상 요구: GUI-01 (변환 실행), GUI-02 (입력 검증), GUI-03 (단위 목록)
"""

import pytest

from unit_converter.app.gui_controller import GuiController
from unit_converter.exceptions import InvalidFormatError, NegativeValueError, UnknownUnitError


@pytest.fixture
def controller():
    return GuiController()


def test_convert_meter_returns_table_grid(controller):  # G-GUI-01 (CLI ASCII)
    lines = controller.convert(unit="meter", value="2.5", fmt="table")
    assert lines[0].startswith("+")
    assert "| meter |   2.5 |    2.5 |" in lines
    assert "| feet  |   2.5 | 8.2021 |" in lines


def test_convert_table_rows_for_gui_widget(controller):  # G-GUI-01
    rows = controller.convert_table_rows(unit="meter", value="2.5")
    assert rows == [
        ("meter", "2.5", "2.5"),
        ("feet", "2.5", "8.2021"),
        ("yard", "2.5", "2.7340"),
    ]


def test_convert_json_format_pretty(controller):  # G-GUI-01
    lines = controller.convert(unit="meter", value="2.5", fmt="json")
    out = "\n".join(lines)
    assert lines[0].startswith("[")
    assert '  "target_unit": "feet"' in out
    assert '  "target_unit": "yard"' in out


def test_available_units_includes_defaults(controller):  # G-GUI-03
    assert set(controller.available_units()) >= {"meter", "feet", "yard"}


def test_negative_value_rejected(controller):  # G-GUI-02
    with pytest.raises(NegativeValueError):
        controller.convert(unit="meter", value="-1")


def test_empty_value_rejected(controller):  # G-GUI-02
    with pytest.raises(InvalidFormatError):
        controller.convert(unit="meter", value="")


def test_unknown_unit_rejected(controller):  # G-GUI-02
    with pytest.raises(UnknownUnitError):
        controller.convert(unit="inch", value="1")
