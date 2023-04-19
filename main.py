import socket
import threading

from PyQt5 import uic
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import *
from dataBus import server_program
from client import ClientConnection
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

        serverSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSideSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        host = socket.gethostname()
        serverSideSocket.bind((host, 0))  # assign socket to free port

        self.actual_host, self.actual_port = serverSideSocket.getsockname()

        serverThread = threading.Thread(target=server_program, args=(serverSideSocket, ))
        serverThread.start()

        # Set resolution
        self.setFixedSize(self.size())
        # Show the app
        self.show()

    def connectClient(self):
        client = ClientConnection(self.actual_port)
        client.connect()
        self.clients += 1
        self.textEdit.setText(f"Button clicking No. {self.clients}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()
