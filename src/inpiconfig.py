import sys, os
from PySide6.QtWidgets import QMainWindow, QDialog
from PySide6.QtCore import QTimer
from modbus import Modbus

from ui_inpiconfig import Ui_INPIConfig
class INPIConfig(QDialog):

    def __init__(self):
        QDialog.__init__(self)

        self.ui = Ui_INPIConfig()
        self.ui.setupUi(self)

        self.ui.pushButtonConnect.clicked.connect(self.portConnect)
        self.ui.pushButtonSave.clicked.connect(self.saveChanges)
        self.btnOUT0.clicked.connect(self.setOUT0)
        self.btnOUT1.clicked.connect(self.setOUT1)
        self.btnCH0Low.clicked.connect(self.setCH0LowRange)
        self.btnCH0High.clicked.connect(self.setCH0HighRange)
        self.btnCH1Low.clicked.connect(self.setCH1LowRange)
        self.btnCH1High.clicked.connect(self.setCH1HighRange)
        self.timer.timeout.connect(self.displayValues)
        # # Init setup
        # self.out0 = 0
        # self.out1 = 0
        # # self.port.setText('/dev/ttyUSB0')
        # self.port.setText('')
        # self.baudrate.setText('115200')
        # self.barCH0.setMinimum(0)
        # self.barCH0.setMaximum(10000)
        # self.barCH1.setMinimum(0)
        # self.barCH1.setMaximum(10000)
        # self.buttonsState(False)

        for i in range(1, 241):
            self.ui.comboBoxId.addItem(str(i))

    def buttonsState(self, enable):
        self.btnOUT0.setEnabled(enable)
        self.btnOUT1.setEnabled(enable)
        self.btnCH0Low.setEnabled(enable)
        self.btnCH0High.setEnabled(enable)
        self.btnCH1Low.setEnabled(enable)
        self.btnCH1High.setEnabled(enable)

    def setDefaultValues(self):
        self.inpi.writeDevice(21, 0)
        self.inpi.writeDevice(22, 10000)
        self.inpi.writeDevice(27, 0)
        self.inpi.writeDevice(28, 10000)

    def saveChanges(self):
        self.setDefaultValues()
        index = self.sensormode.currentIndex()
        if index == 0:
            self.inpi.writeDevice(35, 0)
        else:
            self.inpi.writeDevice(35, 5)
        self.inpi.writeDevice(36, self.slaveId.currentIndex() + 1)
        # self.inpi.writeDevice(37, int(self.baudrate.text()) // 100)
        self.inpi.writeDevice(39, 240)
        self.portDisconnect()

    def portConnect(self):
        if self.ui.pushButtonConnect.text() == 'Connect':
            connect = self.inpi.connect(
                self.port.text(), self.baudrate.text(), self.ui.comboBoxId.currentIndex() + 1)
            if connect == True:
                self.timer.start(200)
                self.pushButtonConnect.setText('Disconnect')
                self.buttonsState(True)
            else:
                print(connect)
                self.buttonsState(False)
                self.inpi.disconnect()
        else:
            self.portDisconnect()

    def portDisconnect(self):
        self.timer.stop()
        self.inpi.disconnect()
        self.ui.pushButtonConnect.setText('Connect')
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
        self.inpi.writeDevice(24, self.registers[23])

    def setCH0HighRange(self):
        self.inpi.writeDevice(25, self.registers[23])

    def setCH1LowRange(self):
        self.inpi.writeDevice(30, self.registers[29])

    def setCH1HighRange(self):
        self.inpi.writeDevice(31, self.registers[29])

    def displayValues(self):
        self.registers = self.inpi.readDevice()
        self.heartbeat.setText(str(self.registers[0]))
        self.adcCH0.display(self.registers[23])
        self.adcCH1.display(self.registers[29])
        self.barCH0.setValue(self.registers[9])
        self.barCH1.setValue(self.registers[10])
        if self.registers[1] == 1:
            self.labelIN0.setText("ON")
        else:
            self.labelIN0.setText("OFF")
        if self.registers[4] == 1:
            self.labelIN1.setText("ON")
        else:
            self.labelIN1.setText("OFF")