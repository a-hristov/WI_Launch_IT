import sys
from threading import Thread

from PyQt6.QtCore import QThread

import constant
from PyQt6.QtWidgets import QApplication

import model
import view


class Controller:
    def __init__(self, app):
        """
        Setup references to the Model and View
        """
        self.thread1 = QThread()
        self.m = model.Model()
        self.v = view.View(self, app)
        self.readArduino()

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
        print(self.m.readFromArduino())
        print('hello')
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
        t2 = Thread(target=self.v.setLcdNumber(constant.LAUNCH_TIME-1))
        t2.start()
        # t1.start()

    def abort(self):
        """
        initiate the abort function by calling the Model abort method
        :return:
        """
        self.m.abort()

    def readArduino(self):
        t1 = Thread(self.v.updateConsole(self.m.readFromArduino()))
        t1.start()


if __name__ == '__main__':
    """
    Start the Program
    """
    app = QApplication([])
    c = Controller(app)
    c.v.show()
    sys.exit(app.exec())
