"""python -m unit_converter.app.gui 진입점."""

import sys

from PyQt6.QtWidgets import QApplication

from unit_converter.app.gui.window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
