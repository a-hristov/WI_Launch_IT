import time

from PyQt6 import uic
from PyQt6.QtCore import QThread
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
        self.b_launch.setEnabled(False)
        self.b_ejection.clicked.connect(c.ejection)
        self.b_ejection.setEnabled(False)
        self.b_abort.clicked.connect(c.abort)
        self.b_abort.setEnabled(False)
        self.b_init.clicked.connect(c.init)
        self.app = app

    def runLongTask(self, c: Controller):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = c
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.longRunningBtn.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.longRunningBtn.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.stepLabel.setText("Long-Running Step: 0")
        )

    def updateConsole(self, text):
        self.console.append(str(text))

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
