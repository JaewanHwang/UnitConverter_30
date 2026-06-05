"""Track E — PyQt MainWindow 스모크 (REFACTOR)."""

import pytest

pytest.importorskip("PyQt6")

from PyQt6.QtWidgets import QApplication

from unit_converter.app.gui.window import MainWindow
from unit_converter.app.gui_controller import GuiController


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


def test_main_window_lists_default_units(qapp):  # G-GUI-03
    win = MainWindow(controller=GuiController())
    units = {win._unit_combo.itemText(i) for i in range(win._unit_combo.count())}
    assert {"meter", "feet", "yard"} <= units


def test_main_window_convert_shows_qtable(qapp):  # G-GUI-01
    win = MainWindow(controller=GuiController())
    win._value_input.setText("2.5")
    win._unit_combo.setCurrentText("meter")
    win._format_combo.setCurrentText("table")
    win._on_convert()
    assert win._output_stack.currentWidget() is win._table
    assert win._table.rowCount() == 3
    assert win._table.item(0, 0).text() == "meter"
    assert win._table.item(0, 2).text() == "2.5"
    assert win._table.item(1, 0).text() == "feet"
    assert win._table.item(1, 2).text() == "8.2021"


def test_main_window_json_uses_text_output(qapp):  # G-GUI-01
    win = MainWindow(controller=GuiController())
    win._value_input.setText("2.5")
    win._format_combo.setCurrentText("json")
    win._on_convert()
    assert win._output_stack.currentWidget() is win._text_output
    assert '"target_unit": "feet"' in win._text_output.toPlainText()
