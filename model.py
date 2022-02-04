import threading
import time
import constant
import serial
import datetime


class Model:

    def __init__(self):
        """
        arduino: the serial port on which the arduino is connected to the computer
        """

        self.arduino = serial.Serial('COM3', baudrate=9600, timeout=10)

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
        """
        try:
            self.writeToArduino('initiate countdown ' + (
                    datetime.datetime.now() + datetime.timedelta(seconds=constant.LAUNCH_TIME)).strftime(
                "%H:%M:%S"))
        except AttributeError as e:
            print('The Controller is not connected to the Computer')
            return None

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
        print('hi')

    def abort(self):
        """
        Write an 'abort' String to the Arduino in order to abort the launch
        :return:
        """
        self.writeToArduino('abort')
        print('abort')

    def forwardingArduinoMessage(self):
        """
        Every message sent by the controller which is meant to reach this program begins with one of three sequences in order to define which part of the data it represents.
        Sequence 1: +++
        Sequence 2: ***
        Sequence 3: ~~~
        :return:
        """
        if self.readFromArduino().startswith(b'+++'):
            print('The date begins with +++')
        if self.readFromArduino().startswith(b'***'):
            print('The date begins with ***')
        if self.readFromArduino().startswith(b'~~~'):
            print('The date begins with ~~~')


if __name__ == '__main__':

    # m = Model()
    '''
    while True:
        print(m.readFromArduino())'''

    # print('initiate countdown', (datetime.datetime.now() + datetime.timedelta(seconds=constant.LAUNCH_TIME)).strftime("%H:%M:%S"))
    # Model().launchWithTimer()
    # while True:
        # time.sleep(1)
        # print(m.forwardingArduinoMessage())
        # m.writeToArduino('init')
    s = "message from rocket 0: +++ -0.01,-0.18,40.81"

    start = s.find("message from rocket 0: +++ ") + len("message from rocket 0: +++ ")
    end = s.find(",")
    substring = s[start:end]
    print(substring)