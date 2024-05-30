import sys, socket
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Server.ServerSocket import ServerSocket
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

        self.s = ServerSocket(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SERVER')

        # Server Setting
        IPBox = QHBoxLayout()

        gb = QGroupBox('Server Setting')
        IPBox.addWidget(gb)

        box = QHBoxLayout()

        label = QLabel('Server IP')
        self.ip = QLineEdit(socket.gethostbyname(socket.gethostname()))
        box.addWidget(label)
        box.addWidget(self.ip)

        label = QLabel('Server Port')
        self.port = QLineEdit(str(port))
        box.addWidget(label)
        box.addWidget(self.port)

        self.s_tg = Ripple_BTN('START')
        self.s_tg.setCheckable(True)
        self.s_tg.toggled.connect(self.Server_Toggle)
        box.addWidget(self.s_tg)

        gb.setLayout(box)

        # Info
        INFOBox = QHBoxLayout()

        # Info Users
        gb = QGroupBox('Info Users')
        INFOBox.addWidget(gb)

        box = QHBoxLayout()
 
        self.guest = QTableWidget()
        self.guest.setColumnCount(2)
        self.guest.setHorizontalHeaderItem(0, QTableWidgetItem('IP'))
        self.guest.setHorizontalHeaderItem(1, QTableWidgetItem('PORT'))
        box.addWidget(self.guest)

        gb.setLayout(box)

        # Info Chat
        gb = QGroupBox('Chat')
        INFOBox.addWidget(gb)

        box = QVBoxLayout()

        self.chat = QListWidget()
        box.addWidget(self.chat)

        hbox = QHBoxLayout()

        self.msg = QLineEdit()
        self.msg.setPlaceholderText('Type your message...')
        self.msg.returnPressed.connect(self.sendMsg)
        hbox.addWidget(self.msg)

        self.send = Ripple_BTN('Send')
        self.send.clicked.connect(self.sendMsg)
        hbox.addWidget(self.send)

        box.addLayout(hbox)

        gb.setLayout(box)

        vbox = QVBoxLayout()
        vbox.addLayout(IPBox)
        vbox.addLayout(INFOBox)

        self.setLayout(vbox)
        self.show()

    def Server_Toggle(self, state):
        if state:
            ip = self.ip.text()
            port = self.port.text()
            if self.s.start(ip, int(port)):
                self.s_tg.setText('STOP')
        else:
            self.s.stop()
            self.chat.clear()
            self.s_tg.setText('START')

    def updateClient(self, addr, isConnect = False):        
        row = self.guest.rowCount()        
        if isConnect:        
            self.guest.setRowCount(row+1)
            self.guest.setItem(row, 0, QTableWidgetItem(addr[0]))
            self.guest.setItem(row, 1, QTableWidgetItem(str(addr[1])))
        else:            
            for r in range(row):
                ip = self.guest.item(r, 0).text() # ip
                port = self.guest.item(r, 1).text() # port
                if addr[0] == ip and str(addr[1]) == port:
                    self.guest.removeRow(r)
                    break

    def updateMsg(self, msg):
        self.chat.addItem(QListWidgetItem(msg))
        self.chat.setCurrentRow(self.chat.count() - 1)

    def sendMsg(self):
        if not self.s.bListen:
            self.msg.clear()
            return
        msg = self.msg.text()
        self.updateMsg(msg)
        print(msg)
        self.s.send(msg)
        self.msg.clear()

    def closeEvent(self, e):
        self.s.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Main_Window()
    sys.exit(app.exec_())