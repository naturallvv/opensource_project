import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QTextBrowser, QLineEdit
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor

import socket
from threading import Thread

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Main GUI
class Chat_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('''
        QPushButton {
            color: #fff;
            background-color: #09e;
            padding: 8px;
            font-size: 12pt;
            border: none;
        }
        QPushButton:pressed {
            color: #ddd;
        }
        ''')

        self.initUI()

    def initUI(self):
        self.x_btn = Ripple_BTN('  X  ')
        self.x_btn.pressed.connect(self.quit_chat)

        self.input_ip = QLineEdit()
        self.input_ip.setText('127.0.0.1')
        self.input_ip.setPlaceholderText('Input Your IP Address')

        self.apply_btn = Ripple_BTN('Apply')
        self.apply_btn.pressed.connect(self.ip_apply)

        self.chat_box = QTextBrowser()

        self.gesture_btn = Ripple_BTN('  G  ')

        self.input_chat = QLineEdit()
        self.input_chat.returnPressed.connect(self.send_chat)

        self.send_btn = Ripple_BTN('  ▷  ')
        self.send_btn.pressed.connect(self.send_chat)

        # TOP
        self.HBox0 = QHBoxLayout()
        self.HBox0.addWidget(self.x_btn)
        self.HBox0.addWidget(self.input_ip)
        self.HBox0.addWidget(self.apply_btn)

        # BOTTOM
        self.HBox1 = QHBoxLayout()
        self.HBox1.addWidget(self.gesture_btn)
        self.HBox1.addWidget(self.input_chat)
        self.HBox1.addWidget(self.send_btn)

        # CENTER
        self.VBoxM = QVBoxLayout()
        self.VBoxM.addLayout(self.HBox0)
        self.VBoxM.addWidget(self.chat_box)
        self.VBoxM.addLayout(self.HBox1)

        self.setLayout(self.VBoxM)

        self.setWindowTitle('Chat_GUI')
        self.setWindowFlags(Qt.WindowMaximizeButtonHint)
        self.setFixedSize(300, 500)
        self.show()

    # real-time message
    def recv_message(self, sock):
        while True:
            msg = sock.recv(1024)
            self.chat_box.append(msg.decode())

    # input ip address
    def ip_apply(self):
        text = self.input_ip.text()
        sock.connect((text, 8274))

        # Warning! : QThread 불가피한 미사용
        thr = Thread(target = self.recv_message, args = (sock, ))
        thr.daemon = True
        thr.start()

        self.input_ip.setDisabled(True)
        self.apply_btn.setDisabled(True)

    # send chat
    def send_chat(self):
        text = self.input_chat.text()
        sock.send(text.encode())
        self.input_chat.clear()

    # quit chat
    def quit_chat(self):
        sock.send('/exit'.encode())

# Ripple Button
class Ripple_BTN(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.r = 0
        self.countr = 0
        self.timer = QTimer(interval = 70, timeout = self.set_radius)

    def set_radius(self):
        self.countr += 1
        if self.r < self.width() / 2:
            self.r += self.width() / 10
        else:
            self.timer.stop()
            self.countr = 0
            self.r = 0

        self.update()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.x, self.y = event.x(), event.y()
        self.timer.start()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.r:
            self.qp = QPainter(self)
            self.qp.setBrush(QColor(255, 255, 255, 127))
            self.qp.setRenderHint(QPainter.Antialiasing)

            if self.countr == 4:
                self.qp.setOpacity(0.8)
            else:
                self.qp.setOpacity(0.3)
                self.qp.setPen(QPen(QColor(Qt.transparent), 0))

            self.qp.drawEllipse(QPoint(self.x, self.y), self.r, self.r)
            self.qp.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    cg = Chat_GUI()
    sys.exit(app.exec_())
    
sock.close()