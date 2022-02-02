import threading
import time
from random import randint

import serial
from PyQt6 import uic, QtCore
from PyQt6.QtCore import QThread, QObject, pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QApplication
from pip._vendor.msgpack.fallback import xrange
from controller import Controller
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg


class View(QMainWindow):
    def __init__(self, c: Controller, app):
        """
        Setup the GUI with a reference to the Controller and connections to the Buttons
        :param c: the reference to the Controller
        """
        super().__init__()
        uic.loadUi("diplomprojekt.ui", self)
        self.b_launch.clicked.connect(c.launch)
        self.b_launch.setEnabled(False)
        self.b_ejection.clicked.connect(c.ejection)
        self.b_ejection.setEnabled(False)
        self.b_abort.clicked.connect(c.abort)
        self.b_abort.setEnabled(False)
        self.b_init.clicked.connect(c.init)
        self.app = app
        self.plotSetup()
        c.check_serial_event()

    def updateConsole(self, text):
        self.console.append(str(text))

    def plotSetup(self):
        self.x = list(range(100))  # 100 time points
        self.y = [randint(0, 100) for _ in range(100)]  # 100 data points
        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line1 = self.graph1.plot(self.x, self.y, pen=pen)
        self.data_line2 = self.graph2.plot(self.x, self.y, pen=pen)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append(randint(0, 100))  # Add a new random value.

        self.data_line1.setData(self.x, self.y)  # Update the data.
        self.data_line2.setData(self.x, self.y)  # Update the data.


    def getTimer(self):
        """
        Return the User specified Launchtimer
        :return: the timer
        """
        return self.lineEdit.text()

    def setLcdNumber(self, x: str):
        """
        Set the LCD Number as a countdown with the timer
        :param x: the timer
        """
        for i in xrange(int(x), 0, -1):
            time.sleep(1)
            print(i)
            self.app.processEvents()
            self.lcdNumber.display(i)

        print('boom')

    def enableButtons(self):
        self.b_launch.setEnabled(True)
        self.b_ejection.setEnabled(True)
        self.b_abort.setEnabled(True)


if __name__ == '__main__':
    import sys

    app = QApplication([])
    v = View()
    v.show()
    sys.exit(app.exec())
