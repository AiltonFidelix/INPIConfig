from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import QTimer
from modbus import Modbus
from ui_inpiconfig import Ui_INPIConfig


class INPIConfig(QDialog):

    def __init__(self):
        QDialog.__init__(self)

        self.ui = Ui_INPIConfig()
        self.ui.setupUi(self)

        self.timer = QTimer()
        self.inpi = Modbus()
        self.out0 = 0
        self.out1 = 0

        # Connect slots
        self.ui.pushButtonConnect.clicked.connect(self.portConnect)
        self.ui.pushButtonSave.clicked.connect(self.saveChanges)
        self.ui.pushButtonOUT0.clicked.connect(self.setOUT0)
        self.ui.pushButtonOUT1.clicked.connect(self.setOUT1)
        self.ui.pushButtonCH0Low.clicked.connect(self.setCH0LowRange)
        self.ui.pushButtonCH0Low.clicked.connect(self.setCH0HighRange)
        self.ui.pushButtonCH1Low.clicked.connect(self.setCH1LowRange)
        self.ui.pushButtonCH1High.clicked.connect(self.setCH1HighRange)
        self.timer.timeout.connect(self.displayValues)
        # Init setup
        self.ui.lineEditPort.setText('')
        self.ui.lineEditBaudrate.setText('115200')
        self.ui.progressBarCH0.setMinimum(0)
        self.ui.progressBarCH0.setMaximum(10000)
        self.ui.progressBarCH1.setMinimum(0)
        self.ui.progressBarCH1.setMaximum(10000)
        self.buttonsState(False)

        for i in range(1, 241):
            self.ui.comboBoxId.addItem(str(i))

    def buttonsState(self, enable):
        self.ui.pushButtonSave.setEnabled(enable)
        self.ui.pushButtonOUT0.setEnabled(enable)
        self.ui.pushButtonOUT1.setEnabled(enable)
        self.ui.pushButtonCH0Low.setEnabled(enable)
        self.ui.pushButtonCH0High.setEnabled(enable)
        self.ui.pushButtonCH1Low.setEnabled(enable)
        self.ui.pushButtonCH1High.setEnabled(enable)

    def setDefaultValues(self):
        self.inpi.writeDevice(21, 0)
        self.inpi.writeDevice(22, 10000)
        self.inpi.writeDevice(27, 0)
        self.inpi.writeDevice(28, 10000)

    def saveChanges(self):
        self.setDefaultValues()
        index = self.ui.comboBoxMode.currentIndex()
        if index == 0:
            self.inpi.writeDevice(35, 0)
        else:
            self.inpi.writeDevice(35, 5)
        self.inpi.writeDevice(36, self.ui.comboBoxId.currentIndex() + 1)
        self.inpi.writeDevice(37, int(self.ui.lineEditBaudrate.text()) // 100)
        self.inpi.writeDevice(39, 240)
        self.portDisconnect()

    def portConnect(self):
        if self.ui.pushButtonConnect.text() == 'Connect':
            ret = self.inpi.connect(
                self.ui.lineEditPort.text(), self.ui.lineEditBaudrate.text(), self.ui.comboBoxId.currentIndex() + 1)

            if ret == True:
                self.timer.start(200)
                self.ui.pushButtonConnect.setText('Disconnect')
                self.buttonsState(True)
            else:
                self.buttonsState(False)
                self.inpi.disconnect()
                
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Connection")
                msg.setText("Serial port connection failed!")
                msg.setDetailedText(ret)
                msg.exec()
        else:
            self.portDisconnect()

    def portDisconnect(self):
        self.timer.stop()
        self.inpi.disconnect()
        self.ui.pushButtonConnect.setText('Connect')
        self.buttonsState(False)

    def setOUT0(self):
        self.out0 = 1 if self.out0 == 0 else 0
        self.inpi.writeDevice(11, self.out0)

    def setOUT1(self):
        self.out1 = 1 if self.out1 == 0 else 0
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
        self.ui.lcdNumberCH0.display(self.registers[23])
        self.ui.lcdNumberCH1.display(self.registers[29])
        self.ui.progressBarCH0.setValue(self.registers[9])
        self.ui.progressBarCH1.setValue(self.registers[10])
        self.ui.labelIN0.setText("ON" if self.registers[1] == 1 else "OFF")
        self.ui.labelIN1.setText("ON" if self.registers[4] == 1 else "OFF")
