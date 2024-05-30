import sys, socket
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Server.ClientSocket import ClientSocket
from Design.RippleButton import Ripple_BTN

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
port = 5614

class Main_Window(QWidget):
    qss = '''
        QWidget {
            background: #FFFFFF;
        }
        QTableWidget {
            border: 1px solid #CED4DA;
            border-radius: 4px;
        }
        QListWidget {
            border: 1px solid #CED4DA;
            border-radius: 4px;
        }
        QLineEdit {
            border: 1px solid #CED4DA;
            border-radius: 4px;
            padding: 6px;
        }
    '''
    def __init__(self):
        super().__init__()
        self.setStyleSheet(self.qss)

        self.c = ClientSocket(self)
        self.initUI()

    def __del__(self):
        self.c.stop()

    def initUI(self):
        self.setWindowTitle('CLIENT')

        IPBox = QVBoxLayout()

        box = QHBoxLayout()

        self.ip = QLineEdit(socket.gethostbyname(socket.gethostname()))
        self.ip.setInputMask('000.000.000.000;_')
        box.addWidget(self.ip)

        self.port = QLineEdit(str(port))
        box.addWidget(self.port)

        self.c_tg = Ripple_BTN('START')
        self.c_tg.clicked.connect(self.Client_Connect)
        box.addWidget(self.c_tg)

        IPBox.addLayout(box)

        self.chat = QListWidget()
        IPBox.addWidget(self.chat)

        hbox = QHBoxLayout()

        self.name = QLineEdit('Users')
        self.name.setFixedWidth(60)
        hbox.addWidget(self.name)

        self.msg = QLineEdit()
        self.msg.returnPressed.connect(self.sendMsg)
        hbox.addWidget(self.msg)

        self.send = Ripple_BTN('Send')
        self.send.clicked.connect(self.sendMsg)
        hbox.addWidget(self.send)

        IPBox.addLayout(hbox)

        self.setLayout(IPBox)
        self.show()

    def Client_Connect(self):
        if self.c.bConnect == False:
            ip = self.ip.text()
            port = self.port.text()
            if self.c.start(ip, int(port)):
                self.c_tg.setText('STOP')
            else:
                self.c.stop()
                self.msg.clear()
                self.chat.clear()
                self.c_tg.setText('START')
        else:
            self.c.stop()
            self.msg.clear()
            self.chat.clear()
            self.c_tg.setText('START')

    def updateMsg(self, msg):
        self.chat.addItem(QListWidgetItem(msg))

    def updateDisconnect(self):
        self.c_tg.setText('START')

    def sendMsg(self):
        name = self.name.text()
        msg = self.msg.text()
        self.c.send(name, msg)
        self.msg.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Main_Window()
    sys.exit(app.exec_())