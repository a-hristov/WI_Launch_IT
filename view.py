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

        c.check_serial_event()
        self.plotSetup(0.0)
        # self.plotSetup2()

    def updateConsole(self, text):
        self.console.append(str(text))

    def plotSetup(self, data):
        self.x = list(range(100))  # 100 time points
        self.y = [0 for _ in range(100)]  # 100 data points

        self.accelZx = self.x
        self.xAxisx = self.x
        self.yAxisx = self.x
        self.servoXx = self.x
        self.servoYx = self.x
        self.rollx = self.x

        self.accelZy = self.y
        self.xAxisy = self.y
        self.yAxisy = self.y
        self.servoXy = self.y
        self.servoYy = self.y
        self.rolly = self.y

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line1 = self.graph1.plot(self.accelZx, self.accelZy, pen=pen)  # accelZ
        self.data_line2 = self.graph2.plot(self.xAxisx, self.xAxisy, pen=pen)  # roll
        self.data_line3 = self.xAxisGraph.plot(self.yAxisx, self.yAxisy, pen=pen)
        self.data_line4 = self.yAxisGraph.plot(self.servoXx, self.servoXy, pen=pen)
        self.data_line5 = self.servoX.plot(self.servoYx, self.servoYy, pen=pen)
        self.data_line6 = self.servoY.plot(self.rollx, self.rolly, pen=pen)
        self.graph1.setTitle('Acceleration Z')
        self.graph2.setTitle('Roll')
        self.xAxisGraph.setTitle('Position on X Axis')
        self.yAxisGraph.setTitle('Position on Y Axis')
        self.servoX.setTitle('Servo X')
        self.servoY.setTitle('Servo Y')
        # self.timer = QtCore.QTimer()
        # self.timer.setInterval(50)
        # self.timer.timeout.connect(self.update_accelZ_plot_data)

        # self.timer.start()

    '''
    def plotSetup2(self):
        self.x2 = list(range(100))  # 100 time points
        self.y2 = [0 for _ in range(100)]  # 100 data points

        self.xAxisx = self.x
        self.xAxisy = self.y

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line3 = self.xAxisGraph.plot(self.x, self.y, pen=pen)
        self.timer1 = QtCore.QTimer()
        self.timer1.setInterval(50)
        self.timer.timeout.connect(self.update_xAxisGraph_plot_data)
        self.timer.start()
    '''

    def update_accelZ_plot_data(self, accelZ: float, xAxis: float, yAxis: float, servoX: float, servoY: float, roll: float):
        if accelZ != -99991234.337:
            self.accelZx = self.accelZx[1:]  # Remove the first y element.
            self.accelZx.append(self.accelZx[-1] + 1)  # Add a new value 1 higher than the last.

            self.accelZy = self.accelZy[1:]  # Remove the first
            self.accelZy.append(accelZ)  # Add a new random value.

            self.data_line1.setData(self.accelZx, self.accelZy)  # Update the data.
        if xAxis != -99991234.337:
            self.xAxisx = self.xAxisx[1:]  # Remove the first y element.
            self.xAxisx.append(self.xAxisx[-1] + 1)  # Add a new value 1 higher than the last.

            self.xAxisy = self.xAxisy[1:]  # Remove the first
            self.xAxisy.append(xAxis)  # Add a new random value.

            self.data_line3.setData(self.xAxisx, self.xAxisy)  # Update the data.
        if yAxis != -99991234.337:
            self.yAxisx = self.yAxisx[1:]  # Remove the first y element.
            self.yAxisx.append(self.yAxisx[-1] + 1)  # Add a new value 1 higher than the last.

            self.yAxisy = self.yAxisy[1:]  # Remove the first
            self.yAxisy.append(yAxis)  # Add a new random value.

            self.data_line4.setData(self.yAxisx, self.yAxisy)  # Update the data.
        if servoX != -99991234.337:
            self.servoXx = self.servoXx[1:]  # Remove the first y element.
            self.servoXx.append(self.servoXx[-1] + 1)  # Add a new value 1 higher than the last.

            self.servoXy = self.servoXy[1:]  # Remove the first
            self.servoXy.append(servoX)  # Add a new random value.

            self.data_line5.setData(self.servoXx, self.servoXy)  # Update the data.
        if servoY != -99991234.337:
            self.servoYx = self.servoYx[1:]  # Remove the first y element.
            self.servoYx.append(self.servoYx[-1] + 1)  # Add a new value 1 higher than the last.

            self.servoYy = self.servoYy[1:]  # Remove the first
            self.servoYy.append(servoY)  # Add a new random value.

            self.data_line6.setData(self.servoYx, self.servoYy)  # Update the data.
        if roll != -99991234.337:
            self.rollx = self.rollx[1:]  # Remove the first y element.
            self.rollx.append(self.rollx[-1] + 1)  # Add a new value 1 higher than the last.

            self.rolly = self.rolly[1:]  # Remove the first
            self.rolly.append(roll)  # Add a new random value.

            self.data_line2.setData(self.rollx, self.rolly)  # Update the data.

    def update_xAxisGraph_plot_data(self, xAxis):
        self.xAxisx = self.xAxisx[1:]  # Remove the first y element.
        self.xAxisx.append(self.xAxisx[-1] + 1)  # Add a new value 1 higher than the last.

        self.xAxisy = self.xAxisy[1:]  # Remove the first
        self.xAxisy.append(xAxis)  # Add a new random value.

        self.data_line3.setData(self.xAxisx, self.xAxisy)  # Update the data.

    def update_yAxisGraph_plot_data(self, yAxis):
        self.yAxisx = self.yAxisx[1:]  # Remove the first y element.
        self.yAxisx.append(self.yAxisx[-1] + 1)  # Add a new value 1 higher than the last.

        self.yAxisy = self.yAxisy[1:]  # Remove the first
        self.yAxisy.append(yAxis)  # Add a new random value.

        self.data_line4.setData(self.yAxisx, self.yAxisy)  # Update the data.

    def update_servoX_plot_data(self, servoX):
        self.servoXx = self.servoXx[1:]  # Remove the first y element.
        self.servoXx.append(self.servoXx[-1] + 1)  # Add a new value 1 higher than the last.

        self.servoXy = self.servoXy[1:]  # Remove the first
        self.servoXy.append(servoX)  # Add a new random value.

        self.data_line5.setData(self.servoXx, self.servoXy)  # Update the data.

    def update_servoY_plot_data(self, servoY):
        self.servoYx = self.servoYx[1:]  # Remove the first y element.
        self.servoYx.append(self.servoYx[-1] + 1)  # Add a new value 1 higher than the last.

        self.servoYy = self.accelZy[1:]  # Remove the first
        self.servoYy.append(servoY)  # Add a new random value.

        self.data_line6.setData(self.servoYx, self.servoYy)  # Update the data.

    def update_roll_plot_data(self, roll):
        self.rollx = self.rollx[1:]  # Remove the first y element.
        self.rollx.append(self.rollx[-1] + 1)  # Add a new value 1 higher than the last.

        self.rolly = self.rolly[1:]  # Remove the first
        self.rolly.append(roll)  # Add a new random value.

        self.data_line2.setData(self.rollx, self.rolly)  # Update the data.

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
        for i in xrange(int(x), -1, -1):
            if int(x) < 0:
                break
            print(i)

            self.lcdNumber.display(i)
            start = time.time()
            if int(x) >= 0:
                while time.time() - start < 1:
                    self.app.processEvents()
                    time.sleep(0.02)
            else:
                break

        print('boom')

    def enableButtons(self):
        self.b_launch.setEnabled(True)
        self.b_ejection.setEnabled(True)
        self.b_abort.setEnabled(True)

    def setRocketState(self, txt):
        if txt == '0':
            self.rocketState.setText('Radio Setup')
            self.rocketState.setStyleSheet('background-color: rgb(255, 255, 255); font: 87 18pt "Arial Black";')
        if txt == '1':
            self.rocketState.setText('GPS Setup')
            self.rocketState.setStyleSheet('background-color: rgb(255, 128, 0); font: 87 18pt "Arial Black";')
        if txt == '2':
            self.rocketState.setText('waiting for \ncountdown')
            self.rocketState.setStyleSheet('background-color: rgb(0, 255, 0); font: 87 18pt "Arial Black";')
        if txt == '3':
            self.rocketState.setText('ongoing \ncountdown')  # changed from 'while countdown' because of preference
            self.rocketState.setStyleSheet('background-color: rgb(255, 255, 255); font: 87 18pt "Arial Black";')
        if txt == '4':
            self.rocketState.setText('Detect Liftoff')
            self.rocketState.setStyleSheet('background-color: rgb(87, 109, 255); font: 87 18pt "Arial Black";')
        if txt == '5':
            self.rocketState.setText('Ascend')
            self.rocketState.setStyleSheet('background-color: rgb(233, 188, 255); font: 87 18pt "Arial Black";')
        if txt == '6':
            self.rocketState.setText('Descend')
            self.rocketState.setStyleSheet('background-color: rgb(0, 255, 255); font: 87 18pt "Arial Black";')
        if txt == '7':
            self.rocketState.setText('Awaiting \nRecovery')
            self.rocketState.setStyleSheet('background-color: rgb(255, 255, 255); font: 87 18pt "Arial Black";')
        if txt == '8':
            self.rocketState.setText('Abort')
            self.rocketState.setStyleSheet('background-color: rgb(255, 0, 0); font: 87 18pt "Arial Black";')
        if txt == '9':
            self.rocketState.setText('In Flight abort')
            self.rocketState.setStyleSheet('background-color: rgb(128, 128, 128); font: 87 18pt "Arial Black";')

    def setLaunchpadState(self, txt):
        if txt == '0':
            self.launchpadState.setText('Radio Setup')
            self.launchpadState.setStyleSheet('background-color: rgb(255, 255, 255); font: 87 18pt "Arial Black";')
        if txt == '1':
            self.launchpadState.setText('GPS Setup')
            self.launchpadState.setStyleSheet('background-color: rgb(255, 128, 0); font: 87 18pt "Arial Black";')
        if txt == '2':
            self.launchpadState.setText('waiting for \ncountdown')
            self.launchpadState.setStyleSheet('background-color: rgb(0, 255, 0); font: 87 18pt "Arial Black";')
        if txt == '3':
            self.launchpadState.setText('ongoing \ncountdown')  # changed from 'while countdown' because of preference
            self.launchpadState.setStyleSheet('background-color: rgb(255, 255, 255); font: 87 18pt "Arial Black";')
        if txt == '4':
            self.launchpadState.setText('Ignition')
            self.launchpadState.setStyleSheet('background-color: rgb(87, 109, 255); font: 87 18pt "Arial Black";')
        if txt == '8':
            self.launchpadState.setText('Abort')
            self.launchpadState.setStyleSheet('background-color: rgb(255, 0, 0); font: 87 18pt "Arial Black";')

    def setVerticalSlider(self, data):
        if data < 0:
            data = 0
        self.verticalSlider.setValue(data)
        self.altitudeLabel.setText(str(data) + 'm')
        self.altitudeLabel.setStyleSheet('font: 87 26pt "Arial Black"; color: rgb(255, 255, 255);')


if __name__ == '__main__':
    import sys

    app = QApplication([])
    v = View()
    v.show()
    sys.exit(app.exec())
