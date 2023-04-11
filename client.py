from sys import executable
from subprocess import Popen

from PyQt5 import uic
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *


class Client(QMainWindow):
    def __init__(self):
        super(Client, self).__init__()
        uic.loadUi("clientUI.ui", self)
        self.setWindowTitle("Client")

        # Define Widget
        self.sendButton = self.findChild(QPushButton, "pushButton")
        self.sentChain = self.findChild(QTextEdit, "textEdit_2")
        self.receiveChain = self.findChild(QTextEdit, "textEdit_3")
        self.textEdit = self.findChild(QTextEdit, "textEdit")
        # Initial chains messages
        self.sentChain.setText("There will be shown last sent chain")
        self.receiveChain.setText("There will be shown last received chain")
        # Create a QFont object with a larger font size
        font = QFont()
        font.setPointSize(14)
        # Set the font for the textEdits
        self.sentChain.setFont(font)
        self.receiveChain.setFont(font)
        # Connect Widget
        self.sendButton.clicked.connect(self.sendMessage)
        # Show the app
        self.show()

    def sendMessage(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = Client()
    app.exec_()
