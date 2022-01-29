import time

import serial


class Model:

    def __init__(self):
        """
        arduino: the serial port on which the arduino is connected to the computer
        """
        self.arduino = serial.Serial(port='COM8', baudrate=9600, timeout=.1)

    def writeToArduino(self, x: str):
        """
        sends the input to the arduino
        :param x: the input
        :return:
        """
        self.arduino.write(bytes(x, 'utf-8'))

    def readFromArduino(self):
        """
        returns the received data from the arduino
        :return: the received data
        """
        return self.arduino.readline()

    def launchWithTimer(self, timer):
        """
        Send a 'Launch' String to the Serial Port after a certain amount of time
        :param timer: the amount of time
        """
        time.sleep(timer)
        self.writeToArduino('Launch')

    def chuteEjection(self):
        """
        Send an 'ejection' String to the Serial Port
        :return:
        """
        self.writeToArduino('ejection')

    def initMode(self):
        """
        Write an 'init' String to the Arduino in order to engage INIT mode
        :return:
        """
        self.writeToArduino('init')


if __name__ == '__main__':
    m = Model()
    while True:
        print(m.readFromArduino())
