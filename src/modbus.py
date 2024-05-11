from minimalmodbus import Instrument


class Modbus:

    def __init__(self):
        self.modbus = Instrument(None, 0)

    def connect(self, port, baudrate, slave):
        try:
            self.modbus.serial.port = port
            self.modbus.serial.baudrate = int(baudrate)
            self.modbus.address = int(slave)
            self.readDevice()
            return True
        except Exception as E:
            return str(E)

    def disconnect(self):
        self.modbus.serial.close()

    def readDevice(self):
        return self.modbus.read_registers(0, 40)

    def writeDevice(self, register, value):
        self.modbus.write_register(register, value)
