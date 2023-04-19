from PyQt5 import uic
import sys

from PyQt5.QtCore import QMetaObject, Q_ARG
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import socket
import threading


class Client(QMainWindow):
    def __init__(self, clientSideSocket):
        super(Client, self).__init__()
        uic.loadUi("clientUI.ui", self)
        self.setWindowTitle("Client")

        # Define Widget
        self.sendButton = self.findChild(QPushButton, "pushButton")
        self.sentChain = self.findChild(QTextEdit, "textEdit_2")
        self.receiveChain = self.findChild(QTextEdit, "textEdit_3")
        self.receiveMessBox = self.findChild(QTextEdit, "textEdit_4")
        self.textEdit = self.findChild(QTextEdit, "textEdit")
        # Initial chains messages
        self.sentChain.setText("There will be shown last sent chain")
        self.receiveChain.setText("There will be shown last received chain")
        # Create a QFont object with a larger font size
        font = QFont("Courier")
        font.setPointSize(13)
        # Set the font for the chains
        self.sentChain.setFont(font)
        self.receiveChain.setFont(font)
        # Set the font for the textEdits
        font.setPointSize(30)
        self.receiveMessBox.setFont(font)
        self.textEdit.setFont(font)
        # Connect Widget
        self.sendButton.clicked.connect(self.sendMessage)
        # TCP/IP
        self.clientSideSocket = clientSideSocket
        self.packedMessLen = 11
        # Set resolution
        self.setFixedSize(self.size())
        # Show the app
        self.show()

    def sendMessage(self):
        # Get message
        mess = self.textEdit.toPlainText()
        # Convert message to int and RS format
        intMess, packedMess = self.conversionRS232(mess)
        # Create time waveforms
        waveforms = [elem.replace('1', '_') for elem in packedMess]
        waveforms = [elem.replace('0', '‾') for elem in waveforms]
        waveforms = [' '.join(elem) for elem in waveforms]
        # Combine signs with ASCII and waveforms
        display = [" {:<3} {:<5} {:<13} ".format(sign, integer, waveform) for sign, integer, waveform in zip(mess, intMess, waveforms)]
        # Display for user
        self.sentChain.setText('\n\n'.join(display))
        # Send
        self.clientSideSocket.send(''.join(packedMess).encode())

    def conversionRS232(self, mess):
        # Convert to int
        mess = [ord(c) for c in mess]
        # Convert to bits
        pureMess = [int(format(integer, 'b')) for integer in mess]
        # Fill up to byte
        pureMess = ["{:08d}".format(elem) for elem in pureMess]
        # Add start bit and stop bits
        packedMess = [f'0{byte}11' for byte in pureMess]
        return mess, packedMess

    def receiveMess(self):
        while True:
            packedMess = self.clientSideSocket.recv(1024).decode()
            packedMess = [packedMess[i * self.packedMessLen: i * self.packedMessLen + self.packedMessLen]
                          for i in range(int(len(packedMess) / self.packedMessLen))]
            # Create time waveforms
            waveforms = [elem.replace('1', '_') for elem in packedMess]
            waveforms = [elem.replace('0', '‾') for elem in waveforms]
            waveforms = [' '.join(elem) for elem in waveforms]
            # Unpack bytes
            unpacked = [elem[1:-2] for elem in packedMess]
            unpacked = [int(str(byte), 2) for byte in unpacked]
            # Convert to ASCII
            mess = [chr(byte) for byte in unpacked]
            # Combine waveforms with ASCII and signs
            display = [" {:<13} {:<4} {:<3} ".format(waveform, integer, sign) for waveform, integer, sign in
                       zip(waveforms, unpacked, mess)]

            mess = (''.join(mess)).split(' ')

            # Swears detection
            with open('swears.txt') as file:
                contents = file.read()
                contents = contents.split("\n")
                clearMess = ['*' * len(word) if word in contents else word for word in mess]

            # Display for user
            QMetaObject.invokeMethod(self.receiveChain, "setText", Qt.QueuedConnection,
                                     Q_ARG(str, '\n\n'.join(display)))
            QMetaObject.invokeMethod(self.receiveMessBox, "setText", Qt.QueuedConnection,
                                     Q_ARG(str, ' '.join(clearMess)))


class ClientConnection:
    def __init__(self, port):
        self.port = port

    def connect(self):
        app = QApplication(sys.argv)

        clientSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
        clientSideSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        host = socket.gethostname()  # as both code is running on same pc

        # clientSideSocket.bind((host, 0))  # assign socket to free port
        # host, port = clientSideSocket.getsockname()

        clientSideSocket.connect((host, self.port))  # connect to the server

        UIWindow = Client(clientSideSocket)
        # Thread for receiving messages
        receiveThread = threading.Thread(target=UIWindow.receiveMess)
        receiveThread.start()
        app.exec_()

        clientSideSocket.close()  # close the connection

if __name__ == '__main__':
    ClientConnection()
