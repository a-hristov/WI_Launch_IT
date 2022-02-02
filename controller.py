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
            time.sleep(1)
            print('test')
            self.v.updateConsole(self.m.readFromArduino())


'''
    def readArduino2(self):
        while True:
            time.sleep(1)
            self.v.updateConsole(self.m.readFromArduino())
'''

if __name__ == '__main__':
    """
    Start the Program
    """
    app = QApplication([])
    c = Controller(app)
    c.v.show()
    sys.exit(app.exec())
