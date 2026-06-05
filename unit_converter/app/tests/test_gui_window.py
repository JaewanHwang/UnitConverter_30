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


def test_main_window_convert_via_button(qapp):  # G-GUI-01
    win = MainWindow(controller=GuiController())
    win._value_input.setText("2.5")
    win._unit_combo.setCurrentText("meter")
    win._on_convert()
    out = win._output.toPlainText()
    assert out.startswith("+")
    assert "| feet  |   2.5 | 8.2021 |" in out
