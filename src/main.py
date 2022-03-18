import sys
from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton, QProgressBar
from PyQt5.uic import loadUiType
from time import sleep

UIClass, QtBaseClass = loadUiType('./ui/inpiconfig.ui')


class MyApp(UIClass, QtBaseClass):

    def __init__(self):
        UIClass.__init__(self)
        QtBaseClass.__init__(self)
        self.setupUi(self)
        # Inputs
        self.port = self.findChild(QLineEdit, "lineEditPort")
        self.baudrate = self.findChild(QLineEdit, "lineEditBaudrate")
        # Displays
        self.barCH0 = self.findChild(QProgressBar, "progressBarCH0")
        self.barCH1 = self.findChild(QProgressBar, "progressBarCH1")
        # Buttons
        self.btnConnect = self.findChild(QPushButton, "pushButtonConnect")
        self.btnCH0Low = self.findChild(QPushButton, "pushButtonCH0Low")
        self.btnCH0High = self.findChild(QPushButton, "pushButtonCH0High")
        self.btnCH1Low = self.findChild(QPushButton, "pushButtonCH1Low")
        self.btnCH1High = self.findChild(QPushButton, "pushButtonCH1High")
        # Connect Buttons
        self.btnConnect.clicked.connect(self.portConnect)
        self.btnCH0Low.clicked.connect(self.setCH0LowRange)
        self.btnCH0High.clicked.connect(self.setCH0HighRange)
        self.btnCH1Low.clicked.connect(self.setCH1LowRange)
        self.btnCH1High.clicked.connect(self.setCH1HighRange)

    def portConnect(self):
        print(self.port.text())
        self.btnConnect.setText('Disconnect')

    def setCH0LowRange(self):
        print('CH0 low range')
        for i in range(100):
            sleep(0.1)
            self.barCH0.setValue(i)
            self.barCH1.setValue(i)
        self.barCH0.setValue(0)
        self.barCH1.setValue(0)

    def setCH0HighRange(self):
        print('CH0 high range')

    def setCH1LowRange(self):
        print('CH1 low range')

    def setCH1HighRange(self):
        print('CH1 high range')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyApp()
    w.show()
    sys.exit(app.exec())
