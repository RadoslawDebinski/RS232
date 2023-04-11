from sys import executable
from subprocess import Popen, CREATE_NEW_CONSOLE

from PyQt5 import uic
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("addClient.ui", self)
        self.setWindowTitle("Controller")

        # Number of clients
        self.clients = 0

        # Define Widget
        self.addButton = self.findChild(QPushButton, "pushButton")
        self.textEdit = self.findChild(QTextEdit, "textEdit")
        # Initial textEdit message
        self.textEdit.setText("No. Clients = 0")
        # Create a QFont object with a larger font size
        font = QFont()
        font.setPointSize(30)
        # Set the font for the textEdit and addButton Widgets
        self.textEdit.setFont(font)
        self.addButton.setFont(font)
        # Connect Widget
        self.addButton.clicked.connect(self.connectClient)
        # Show the app
        self.show()

    def connectClient(self):
        Popen([executable, 'C:\\ACIR-WETI\\sem 6\\Architektura systemów komputerowych\\RS232\\RS232\\client.py'])
              # creationflags=CREATE_NEW_CONSOLE)
        self.clients += 1
        self.textEdit.setText(f"No. Clients = {self.clients}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()

