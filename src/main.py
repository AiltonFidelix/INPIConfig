import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from inpiconfig import INPIConfig

app_path = os.path.dirname(os.path.abspath(__file__))
ico_path = os.path.join(app_path, 'assets', 'icons', 'config.ico')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = INPIConfig()
    win.setWindowIcon(QIcon(ico_path))
    win.show()
    sys.exit(app.exec())
