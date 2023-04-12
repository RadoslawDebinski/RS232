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
        # Get message
        mess = self.textEdit.toPlainText()
        # Convert message to int and RS format
        intMess, packedMess = self.conversionRS232(mess)
        # Create time waveforms
        waveforms = [elem.replace('1', '_') for elem in packedMess]
        waveforms = [elem.replace('0', '‾') for elem in waveforms]
        waveforms = [' '.join(elem) for elem in waveforms]
        # Combine signs with ASCII and waveforms
        display = [f'{sign} - {integer} -  {waveform}' for sign, integer, waveform in zip(mess, intMess, waveforms)]
        # Display for user
        self.sentChain.setText('\n\n'.join(display))
        # Send
        self.receiveMess(packedMess)

    def conversionRS232(self, mess):
        # Convert to int
        mess = [ord(c) for c in mess]
        # Convert to bits
        pureMess = [int(format(integer, 'b')) for integer in mess]
        # Fill up to byte
        pureMess = ["{:08d}".format(elem) for elem in pureMess]
        # Add start bit and stop bits
        packedMess = [f'0 {byte} 11' for byte in pureMess]
        return mess, packedMess

    def receiveMess(self, packedMess):
        # Create time waveforms
        waveforms = [elem.replace('1', '_') for elem in packedMess]
        waveforms = [elem.replace('0', '‾') for elem in waveforms]
        waveforms = [' '.join(elem) for elem in waveforms]
        # Unpack bytes
        unpacked = [elem[2:-3] for elem in packedMess]
        unpacked = [int(str(byte), 2) for byte in unpacked]
        # Convert to ASCII
        mess = [chr(byte) for byte in unpacked]
        # Combine waveforms with ASCII and signs
        display = [f'{waveform} - {integer} -  {sign}' for waveform, integer, sign in zip(waveforms, unpacked, mess)]
        # Display for user
        self.receiveChain.setText('\n\n'.join(display))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = Client()
    app.exec_()