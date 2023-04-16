import sys
from sys import executable
from subprocess import Popen, CREATE_NEW_CONSOLE

from PyQt5 import uic
from PyQt5.QtCore import QFile
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

import ui


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        uiFile = QFile(":/addClient")
        uiFile.open(QFile.ReadOnly)
        uic.loadUi(uiFile, self)
        uiFile.close()
        self.setWindowTitle("Controller")

        # Number of clients
        self.clients = 0

        # Define Widget
        self.addButton = self.findChild(QPushButton, "pushButton")
        self.textEdit = self.findChild(QPushButton, "pushButton_2")
        # Initial textEdit message
        self.textEdit.setText("Button not clicked")
        # Create a QFont object with a larger font size
        font = QFont()
        font.setPointSize(30)
        # Set the font for the textEdit and addButton Widgets
        self.textEdit.setFont(font)
        self.addButton.setFont(font)
        # Connect Widget
        self.addButton.clicked.connect(self.connectClient)
        # Create main line
        Popen([executable, 'dataBus.py'])  # , creationflags=CREATE_NEW_CONSOLE)
        # Set resolution
        self.setFixedSize(self.size())
        # Show the app
        self.show()

    def connectClient(self):
        Popen([executable, 'client.py'])
        self.clients += 1
        self.textEdit.setText(f"Button clicking No. {self.clients}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()
