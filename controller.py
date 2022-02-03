import sys
import threading
import time
from threading import Thread

from PyQt6.QtCore import QThread, pyqtSignal, QObject

import constant
from PyQt6.QtWidgets import QApplication

import model
import view


class Controller():

    def __init__(self, app):
        """
        Setup references to the Model and View
        """

        self.m = model.Model()
        self.v = view.View(self, app)

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
        t1 = Thread(target=self.m.initMode())
        t1.start()
        t1.join()

        t2 = Thread(target=self.v.enableButtons())
        t2.start()
        t2.join()
        # self.v.runLongTask(self, self.m)

    def launch(self):
        """
        Method to execute the Models launchWithTimer and the Views setLcdNumber methods
        :return:
        """
        self.m.launchWithTimer()
        # self.m.launchWithTimer(int(self.v.getTimer()))
        # self.v.setLcdNumber(int(self.v.getTimer()))
        # t1 = Thread(target=self.m.launchWithTimer(int(self.v.getTimer())))
        t2 = Thread(target=self.v.setLcdNumber(constant.LAUNCH_TIME - 1), args=[])
        t2.start()
        t2.join()
        # t1.start()

    def abort(self):
        """
        initiate the abort function by calling the Model abort method
        :return:
        """
        self.m.abort()

    def readArduino(self):
        while True:
            time.sleep(0.05)
            print('test')
            self.v.updateConsole(self.m.readFromArduino())

    def check_serial_event(self):
        self.timeout = 0

        self.timeout += 1
        # print (self.timeout)
        serial_thread = threading.Timer(0.05, self.check_serial_event)
        if self.m.arduino.is_open:
            serial_thread.start()
            if self.m.arduino.in_waiting:
                eol = b'\n'
                leneol = len(eol)
                line = bytearray()
                while True:
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
                if distance == 'message from rocket 0: connection established':
                    self.v.setRocketState('1')
                if distance == 'message from rocket 0: GPS gets signal':
                    self.v.setRocketState('2')
                if distance.startswith('***'):
                    x = distance.split(',')
                    self.v.setRocketState(x[-2])
                if distance.startswith('\'\'\''):
                    x = distance.split(',')
                    self.v.setLaunchpadState(x[-2])
                if distance == 'message from lPad 1: connection established':
                    self.v.setLaunchpadState('1')
                if distance == 'message from lPad 1: GPS gets signal':
                    self.v.setLaunchpadState('2')
                self.v.console.append(distance + '\n')
                # print (distance)
                self.timeout = 0

        if self.timeout >= 10:
            self.m.arduino.close()


if __name__ == '__main__':
    """
    Start the Program
    """
    app = QApplication([])
    c = Controller(app)
    c.v.show()
    sys.exit(app.exec())
