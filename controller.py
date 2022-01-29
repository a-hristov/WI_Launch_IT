import sys
from threading import Thread

from PyQt6.QtWidgets import QApplication

import model
import view


class Controller:
    def __init__(self,app):
        """
        Setup references to the Model and View
        """
        self.m = model.Model()
        self.v = view.View(self,app)

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

    def launch(self):
        """
        Method to execute the Models launchWithTimer and the Views setLcdNumber methods
        :return:
        """
        # self.m.launchWithTimer(int(self.v.getTimer()))
        # self.v.setLcdNumber(int(self.v.getTimer()))
        # t1 = Thread(target=self.m.launchWithTimer(int(self.v.getTimer())))
        t2 = Thread(target=self.v.setLcdNumber(int(self.v.getTimer())))
        t2.start()
        #t1.start()


if __name__ == '__main__':
    """
    Main zum Starten des Programms/ controller
    """
    app = QApplication([])
    c = Controller(app)
    c.v.show()
    sys.exit(app.exec())
