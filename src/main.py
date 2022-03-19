import sys
from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton, QProgressBar, QLabel, QLCDNumber
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUiType
from modbus import Modbus

UIClass, QtBaseClass = loadUiType('./ui/inpiconfig.ui')


class MyApp(UIClass, QtBaseClass):

    def __init__(self):
        UIClass.__init__(self)
        QtBaseClass.__init__(self)
        self.setupUi(self)
        self.timer = QTimer()
        self.inpi = Modbus()
        # Inputs
        self.port = self.findChild(QLineEdit, "lineEditPort")
        self.baudrate = self.findChild(QLineEdit, "lineEditBaudrate")
        # Labels
        self.heartbeat = self.findChild(QLabel, "labelHeartBeat")
        # Displays
        self.adcCH0 = self.findChild(QLCDNumber, "lcdNumberCH0")
        self.adcCH1 = self.findChild(QLCDNumber, "lcdNumberCH1")
        self.barCH0 = self.findChild(QProgressBar, "progressBarCH0")
        self.barCH1 = self.findChild(QProgressBar, "progressBarCH1")
        # Buttons
        self.btnConnect = self.findChild(QPushButton, "pushButtonConnect")
        self.btnOUT0 = self.findChild(QPushButton, "pushButtonOUT0")
        self.btnOUT1 = self.findChild(QPushButton, "pushButtonOUT1")
        self.btnCH0Low = self.findChild(QPushButton, "pushButtonCH0Low")
        self.btnCH0High = self.findChild(QPushButton, "pushButtonCH0High")
        self.btnCH1Low = self.findChild(QPushButton, "pushButtonCH1Low")
        self.btnCH1High = self.findChild(QPushButton, "pushButtonCH1High")
        # Connect Buttons
        self.btnConnect.clicked.connect(self.portConnect)
        self.btnOUT0.clicked.connect(self.setOUT0)
        self.btnOUT1.clicked.connect(self.setOUT1)
        self.btnCH0Low.clicked.connect(self.setCH0LowRange)
        self.btnCH0High.clicked.connect(self.setCH0HighRange)
        self.btnCH1Low.clicked.connect(self.setCH1LowRange)
        self.btnCH1High.clicked.connect(self.setCH1HighRange)

        self.timer.timeout.connect(self.showTime)
        self.out0 = 0
        self.out1 = 0
        self.port.setText('/dev/ttyUSB0')
        self.baudrate.setText('115200')

        self.buttonsState(False)

    def buttonsState(self, enable):
        self.btnOUT0.setEnabled(enable)
        self.btnOUT1.setEnabled(enable)
        self.btnCH0Low.setEnabled(enable)
        self.btnCH0High.setEnabled(enable)
        self.btnCH1Low.setEnabled(enable)
        self.btnCH1High.setEnabled(enable)

    def portConnect(self):
        if self.btnConnect.text() == 'Connect':
            connect = self.inpi.connect(
                self.port.text(), self.baudrate.text(), 1)
            if connect == True:
                self.timer.start(100)
                self.btnConnect.setText('Disconnect')
                self.buttonsState(True)
            else:
                print(connect)
                self.buttonsState(False)
                self.inpi.disconnect()
        else:
            self.inpi.disconnect()
            self.timer.stop()
            self.btnConnect.setText('Connect')
            self.buttonsState(False)

    def setOUT0(self):
        if self.out0 == 1:
            self.out0 = 0
        else:
            self.out0 = 1
        self.inpi.writeDevice(11, self.out0)

    def setOUT1(self):
        if self.out1 == 1:
            self.out1 = 0
        else:
            self.out1 = 1
        self.inpi.writeDevice(13, self.out1)

    def setCH0LowRange(self):
        pass

    def setCH0HighRange(self):
        pass

    def setCH1LowRange(self):
        pass

    def setCH1HighRange(self):
        pass

    def showTime(self):
        registers = self.inpi.readDevice()
        self.heartbeat.setText(str(registers[0]))
        self.adcCH0.display(registers[23])
        self.adcCH1.display(registers[29])
        self.barCH0.setValue(registers[9])
        self.barCH1.setValue(registers[10])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyApp()
    w.show()
    sys.exit(app.exec())
