"""MainWindow — PyQt6 변환 GUI (GUI-01/02, I/O 경계)."""

from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from unit_converter.app.gui_controller import GuiController
from unit_converter.exceptions import InvalidFormatError, NegativeValueError, UnknownUnitError

_ERROR_TYPES = (InvalidFormatError, NegativeValueError, UnknownUnitError)


class MainWindow(QWidget):
    def __init__(self, controller=None):
        super().__init__()
        self._controller = controller or GuiController()
        self.setWindowTitle("Unit Converter")
        self._build_ui()
        self._populate_units()

    def _build_ui(self):
        root = QVBoxLayout(self)

        input_row = QHBoxLayout()
        input_row.addWidget(QLabel("Unit:"))
        self._unit_combo = QComboBox()
        input_row.addWidget(self._unit_combo)

        input_row.addWidget(QLabel("Value:"))
        self._value_input = QLineEdit()
        self._value_input.setPlaceholderText("2.5")
        input_row.addWidget(self._value_input)

        input_row.addWidget(QLabel("Format:"))
        self._format_combo = QComboBox()
        self._format_combo.addItems(["table", "json", "csv"])
        input_row.addWidget(self._format_combo)
        root.addLayout(input_row)

        self._convert_btn = QPushButton("Convert")
        self._convert_btn.clicked.connect(self._on_convert)
        root.addWidget(self._convert_btn)

        self._output = QPlainTextEdit()
        self._output.setReadOnly(True)
        root.addWidget(self._output)

    def _populate_units(self):
        self._unit_combo.clear()
        self._unit_combo.addItems(self._controller.available_units())

    def _on_convert(self):
        try:
            lines = self._controller.convert(
                unit=self._unit_combo.currentText(),
                value=self._value_input.text(),
                fmt=self._format_combo.currentText(),
            )
            self._output.setPlainText("\n".join(lines))
        except _ERROR_TYPES as exc:
            self._output.setPlainText(f"Error: {exc}")
