import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from inpiconfig import INPIConfig


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = INPIConfig()
    win.setWindowIcon(QIcon('./assets/icons/config.ico'))
    win.show()
    sys.exit(app.exec())