"""MainWindow — PyQt6 변환 GUI (GUI-01/02, I/O 경계)."""

from PyQt6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from unit_converter.app.gui_controller import GuiController
from unit_converter.exceptions import InvalidFormatError, NegativeValueError, UnknownUnitError

_ERROR_TYPES = (InvalidFormatError, NegativeValueError, UnknownUnitError)
_TABLE_HEADERS = ["unit", "input", "result"]


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

        self._table = QTableWidget(0, len(_TABLE_HEADERS))
        self._table.setHorizontalHeaderLabels(_TABLE_HEADERS)
        self._table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self._table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._table.setAlternatingRowColors(True)

        self._text_output = QPlainTextEdit()
        self._text_output.setReadOnly(True)

        self._output_stack = QStackedWidget()
        self._output_stack.addWidget(self._table)
        self._output_stack.addWidget(self._text_output)
        root.addWidget(self._output_stack)

    def _populate_units(self):
        self._unit_combo.clear()
        self._unit_combo.addItems(self._controller.available_units())

    def _show_error(self, message: str) -> None:
        self._output_stack.setCurrentWidget(self._text_output)
        self._text_output.setPlainText(message)

    def _show_table(self, rows: list[tuple[str, str, str]]) -> None:
        self._output_stack.setCurrentWidget(self._table)
        self._table.setRowCount(len(rows))
        for row_idx, (unit, inp, result) in enumerate(rows):
            self._table.setItem(row_idx, 0, QTableWidgetItem(unit))
            self._table.setItem(row_idx, 1, QTableWidgetItem(inp))
            self._table.setItem(row_idx, 2, QTableWidgetItem(result))

    def _show_text(self, lines: list[str]) -> None:
        self._output_stack.setCurrentWidget(self._text_output)
        self._text_output.setPlainText("\n".join(lines))

    def _on_convert(self):
        unit = self._unit_combo.currentText()
        value = self._value_input.text()
        fmt = self._format_combo.currentText()
        try:
            if fmt == "table":
                rows = self._controller.convert_table_rows(unit=unit, value=value)
                self._show_table(rows)
            else:
                lines = self._controller.convert(unit=unit, value=value, fmt=fmt)
                self._show_text(lines)
        except _ERROR_TYPES as exc:
            self._show_error(f"Error: {exc}")
