import sys
import threading
import time
from threading import Thread

from PyQt6.QtCore import QThread, pyqtSignal, QObject

import constant
from PyQt5.QtWidgets import QApplication

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

    def readArduino(self):
        while True:
            time.sleep(0.05)
            print('test')
            self.v.updateConsole(self.m.readFromArduino())

    def check_serial_event(self):
        # self.timeout = 0

        # self.timeout += 1
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
                if distance.startswith('message from rocket 0: +++'):
                    start = distance.find("message from rocket 0: +++ ") + len("message from rocket 0: +++ ")
                    end = distance.find(",")
                    substring = distance[start:end]
                    print(substring)
                    x = distance.split(',')
                    # self.v.update_xAxisGraph_plot_data(float(x[-1]))
                    print(float(x[-1]))
                    if isinstance(float(substring), float) and isinstance(float(x[-1]), float):
                        self.v.update_accelZ_plot_data(float(substring), float(x[-1]), -99991234.337, -99991234.337, -99991234.337, -99991234.337)

                    self.v.setVerticalSlider(float(x[-2]))

                if distance.startswith('message from rocket 0: ~~~'):
                    start = distance.find("message from rocket 0: ~~~ ") + len("message from rocket 0: ~~~ ")
                    end = distance.find(",")
                    substring = distance[start:end]
                    x = distance.split(',')
                    if isinstance(float(substring), float) and isinstance(float(x[-3]), float) and isinstance(float(x[-2]), float) and isinstance(float(x[-1]), float):
                        self.v.update_accelZ_plot_data(-99991234.337, -99991234.337, float(substring), float(x[-3]), float(x[-2]), float(x[-1]))

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
                # print (distance)
                # self.timeout = 0

        # if self.timeout >= 10:
            # self.m.arduino.close()


if __name__ == '__main__':
    """
    Start the Program
    """
    app = QApplication([])
    c = Controller(app)
    c.v.show()
    sys.exit(app.exec())
