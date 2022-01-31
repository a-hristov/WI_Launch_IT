import time
import constant
import serial
import datetime


class Model:

    def __init__(self):
        """
        arduino: the serial port on which the arduino is connected to the computer
        """
        # self.arduino = serial.Serial(port='COM8', baudrate=9600, timeout=.1)
        # Comment this line if you want to test GUI

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

    def launchWithTimer(self):
        """
        Send a 'Launch' String to the Serial Port after a certain amount of time
        :param timer: the amount of time
        """

        self.writeToArduino('initiate countdown ', (datetime.datetime.now() + datetime.timedelta(seconds=constant.LAUNCH_TIME)).strftime("%H:%M:%S"))

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

    def abort(self):
        """
        Write an 'abort' String to the Arduino in order to abort the launch
        :return:
        """
        self.writeToArduino('abort')


if __name__ == '__main__':
    '''
    m = Model()
    while True:
        print(m.readFromArduino())'''
    now = datetime.datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    tc = datetime.timedelta(seconds=constant.LAUNCH_TIME)
    now2 = datetime.datetime.now() + datetime.timedelta(seconds=constant.LAUNCH_TIME)
    current_time2 = (datetime.datetime.now() + datetime.timedelta(seconds=constant.LAUNCH_TIME)).strftime("%H:%M:%S")
    print("Current Time =", (datetime.datetime.now() + datetime.timedelta(seconds=constant.LAUNCH_TIME)).strftime("%H:%M:%S"))
