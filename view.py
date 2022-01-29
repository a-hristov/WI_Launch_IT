import time

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication
from pip._vendor.msgpack.fallback import xrange

from controller import Controller


class View(QMainWindow):
    def __init__(self, c: Controller, app):
        """
        Setup the GUI with a reference to the Controller and connections to the Buttons
        :param c: the reference to the Controller
        """
        super().__init__()
        uic.loadUi("diplomprojekt.ui", self)
        self.b_launch.clicked.connect(c.launch)
        self.b_ejection.clicked.connect(c.ejection)
        self.b_init.clicked.connect(c.init)
        self.app = app

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


        print('helloworld')

    """
    def setConsole(self,x:str):
        self.l_console.text(x)
    """


if __name__ == '__main__':
    import sys

    app = QApplication([])
    v = View()
    v.show()
    sys.exit(app.exec())
