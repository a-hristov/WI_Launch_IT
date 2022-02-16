import sys
import threading
import time
from threading import Thread

from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QObject

import constant
from PyQt5.QtWidgets import QApplication

import model
import view


class Communicate(QtCore.QObject):
    myGUI_signal = QtCore.pyqtSignal(str)





class Controller():

    def __init__(self, app):
        """
        Setup references to the Model and View
        """

        self.m = model.Model()
        self.v = view.View(self, app)
        self.v.startTheThread(self)

    def myThread(self, callbackFunc):
        mySrc = Communicate()
        mySrc.myGUI_signal.connect(callbackFunc)
        while True:
            time.sleep(0.1)
            # Do something useful here.
            msgForGui = 'This is a message to send to the GUI'
            mySrc.myGUI_signal.emit(msgForGui)
            # c = Controller();
            if self.m.arduino.is_open:
            # serial_thread.start()
                if self.m.arduino.in_waiting:
                    eol = b'\n'
                    leneol = len(eol)
                    line = bytearray()
                    while True:
                        # msgForGui = 'This is a message to send to the GUI'
                        # mySrc.myGUI_signal.emit(msgForGui)
                        conn = self.m.arduino.read(1)
                        if conn:
                            line += conn
                            if line[-leneol:] == eol:
                                break
                        else:
                            break
                        # print (line)
                        # print (type(line))
                    line = line.rstrip()
                    distance = line.decode("utf-8")
                    if distance.startswith('message from rocket 0: +++'):
                        # time.sleep(0.1)
                        start = distance.find("message from rocket 0: +++ ") + len("message from rocket 0: +++ ")
                        end = distance.find(",")
                        substring = distance[start:end]
                        print(substring)
                        x = distance.split(',')
                        # self.v.update_xAxisGraph_plot_data(float(x[-1]))
                        print(float(x[-1]))
                        try:
                            if type(float(substring)) == float and type(float(x[-1])) == float:
                                self.v.update_accelZ_plot_data(float(substring), float(x[-1]), -1234.337, -1234.337,
                                                               -1234.337, -1234.337)

                            self.v.setVerticalSlider(float(x[-2]))
                        except ValueError as ve:
                            print('Value Error')

                    if distance.startswith('message from rocket 0: ~~~'):
                        # time.sleep(0.1)

                        start = distance.find("message from rocket 0: ~~~ ") + len("message from rocket 0: ~~~ ")
                        end = distance.find(",")
                        substring = distance[start:end]
                        x = distance.split(',')
                        try:
                            if type(float(substring)) == float and type(float(x[-3])) == float and type(
                                    float(x[-2])) == float and type(float(x[-1])) == float:
                                self.v.update_accelZ_plot_data(-1234.337, -1234.337, float(substring), float(x[-3]),
                                                               float(x[-2]), float(x[-1]))
                        except ValueError as ve:
                            print('Value Error')
                    if distance == 'message from rocket 0: connection established':
                        self.v.setRocketState('1')
                    if distance == 'message from rocket 0: GPS gets signal':
                        self.v.setRocketState('2')
                    if distance.startswith('message from rocket 0: ***'):
                        x = distance.split(',')
                        self.v.setRocketState(x[-2])
                    if distance.startswith('message from lPad 1: \'\'\''):
                        x = distance.split(',')
                        self.v.setLaunchpadState(x[-2])
                    if distance == 'message from lPad 1: connection established':
                        self.v.setLaunchpadState('1')
                    if distance == 'message from lPad 1: GPS gets signal':
                        self.v.setLaunchpadState('2')
                    self.v.console.append(distance + '\n')
    '''
    def myThread(self, callbackFunc):
        mySrc = Communicate()
        mySrc.myGUI_signal.connect(callbackFunc)
        if self.m.arduino.is_open:
            # serial_thread.start()
            if self.m.arduino.in_waiting:
                eol = b'\n'
                leneol = len(eol)
                line = bytearray()
                while True:
                    msgForGui = 'This is a message to send to the GUI'
                    mySrc.myGUI_signal.emit(msgForGui)
                    c = self.m.arduino.read(1)
                    if c:
                        line += c
                        if line[-leneol:] == eol:
                            break
                    else:
                        break
                    # print (line)
                    # print (type(line))
                line = line.rstrip()
                distance = line.decode("utf-8")
                if distance.startswith('message from rocket 0: +++'):
                    # time.sleep(0.1)
                    start = distance.find("message from rocket 0: +++ ") + len("message from rocket 0: +++ ")
                    end = distance.find(",")
                    substring = distance[start:end]
                    print(substring)
                    x = distance.split(',')
                    # self.v.update_xAxisGraph_plot_data(float(x[-1]))
                    print(float(x[-1]))
                    try:
                        if type(float(substring)) == float and type(float(x[-1])) == float:
                            self.v.update_accelZ_plot_data(float(substring), float(x[-1]), -1234.337, -1234.337,
                                                           -1234.337, -1234.337)

                        self.v.setVerticalSlider(float(x[-2]))
                    except ValueError as ve:
                        print('Value Error')

                if distance.startswith('message from rocket 0: ~~~'):
                    # time.sleep(0.1)

                    start = distance.find("message from rocket 0: ~~~ ") + len("message from rocket 0: ~~~ ")
                    end = distance.find(",")
                    substring = distance[start:end]
                    x = distance.split(',')
                    try:
                        if type(float(substring)) == float and type(float(x[-3])) == float and type(
                                float(x[-2])) == float and type(float(x[-1])) == float:
                            self.v.update_accelZ_plot_data(-1234.337, -1234.337, float(substring), float(x[-3]),
                                                           float(x[-2]), float(x[-1]))
                    except ValueError as ve:
                        print('Value Error')
                if distance == 'message from rocket 0: connection established':
                    self.v.setRocketState('1')
                if distance == 'message from rocket 0: GPS gets signal':
                    self.v.setRocketState('2')
                if distance.startswith('message from rocket 0: ***'):
                    x = distance.split(',')
                    self.v.setRocketState(x[-2])
                if distance.startswith('message from lPad 1: \'\'\''):
                    x = distance.split(',')
                    self.v.setLaunchpadState(x[-2])
                if distance == 'message from lPad 1: connection established':
                    self.v.setLaunchpadState('1')
                if distance == 'message from lPad 1: GPS gets signal':
                    self.v.setLaunchpadState('2')
                self.v.console.append(distance + '\n')
    '''

    def ejection(self):
        """
        Method to execute the Models chuteEjecton method
        """
        self.m.chuteEjection()

    def init(self):
        """
        Method to execute the models initMode method
        :return:
        """
        self.m.initMode()
        self.v.enableButtons()

    def launch(self):
        """
        Method to execute the Models launchWithTimer and the Views setLcdNumber methods
        :return:
        """
        self.m.launchWithTimer()
        # self.m.launchWithTimer(int(self.v.getTimer()))
        # self.v.setLcdNumber(int(self.v.getTimer()))
        # t1 = Thread(target=self.m.launchWithTimer(int(self.v.getTimer())))
        self.v.setLcdNumber(constant.LAUNCH_TIME - 1)

        # t1.start()

    def abort(self):
        """
        initiate the abort function by calling the Model abort method
        :return:
        """
        self.m.abort()
        self.v.setLcdNumber(0)
        self.v.setRocketState('8')
        self.v.setLaunchpadState('8')

    def readArduino(self):
        while True:
            time.sleep(0.05)
            print('test')
            self.v.updateConsole(self.m.readFromArduino())

    def check_serial_event(self):

        if self.m.arduino.is_open:
            # serial_thread.start()
            if self.m.arduino.in_waiting:
                eol = b'\n'
                leneol = len(eol)
                line = bytearray()
                while True:
                    # msgForGui = 'This is a message to send to the GUI'
                    # mySrc.myGUI_signal.emit(msgForGui)
                    c = self.m.arduino.read(1)
                    if c:
                        line += c
                        if line[-leneol:] == eol:
                            break
                    else:
                        break
                    # print (line)
                    # print (type(line))
                line = line.rstrip()
                distance = line.decode("utf-8")
                if distance.startswith('message from rocket 0: +++'):
                    # time.sleep(0.1)
                    start = distance.find("message from rocket 0: +++ ") + len("message from rocket 0: +++ ")
                    end = distance.find(",")
                    substring = distance[start:end]
                    print(substring)
                    x = distance.split(',')
                    # self.v.update_xAxisGraph_plot_data(float(x[-1]))
                    print(float(x[-1]))
                    try:
                        if type(float(substring)) == float and type(float(x[-1])) == float:
                            self.v.update_accelZ_plot_data(float(substring), float(x[-1]), -1234.337, -1234.337,
                                                           -1234.337, -1234.337)

                        self.v.setVerticalSlider(float(x[-2]))
                    except ValueError as ve:
                        print('Value Error')

                if distance.startswith('message from rocket 0: ~~~'):
                    # time.sleep(0.1)

                    start = distance.find("message from rocket 0: ~~~ ") + len("message from rocket 0: ~~~ ")
                    end = distance.find(",")
                    substring = distance[start:end]
                    x = distance.split(',')
                    try:
                        if type(float(substring)) == float and type(float(x[-3])) == float and type(
                                float(x[-2])) == float and type(float(x[-1])) == float:
                            self.v.update_accelZ_plot_data(-1234.337, -1234.337, float(substring), float(x[-3]),
                                                           float(x[-2]), float(x[-1]))
                    except ValueError as ve:
                        print('Value Error')
                if distance == 'message from rocket 0: connection established':
                    self.v.setRocketState('1')
                if distance == 'message from rocket 0: GPS gets signal':
                    self.v.setRocketState('2')
                if distance.startswith('message from rocket 0: ***'):
                    x = distance.split(',')
                    self.v.setRocketState(x[-2])
                if distance.startswith('message from lPad 1: \'\'\''):
                    x = distance.split(',')
                    self.v.setLaunchpadState(x[-2])
                if distance == 'message from lPad 1: connection established':
                    self.v.setLaunchpadState('1')
                if distance == 'message from lPad 1: GPS gets signal':
                    self.v.setLaunchpadState('2')
                self.v.console.append(distance + '\n')

if __name__ == '__main__':
    """
    Start the Program
    """
    app = QApplication([])
    c = Controller(app)
    c.v.show()
    sys.exit(app.exec())
