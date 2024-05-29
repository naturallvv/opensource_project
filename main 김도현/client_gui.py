import os, sys, socket, client_socket
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
port = 8274

class Chat_GUI(QWidget):
    qss = '''
        QWidget {
            background: #FFFFFF;
        }
        QTextBrowser {
            border: 1px solid #CED4DA;
            border-radius: 4px;
        }
        QLineEdit {
            border: 1px solid #CED4DA;
            border-radius: 4px;
            padding: 6px;
        }
    '''
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setStyleSheet(self.qss)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.initUI()

    def __del__(self):
        pass

    def initUI(self):
        self.window_vbox = QVBoxLayout(self)
        self.window_vbox.setContentsMargins(0, 0, 0, 0)

        self.titlebar = Title_BAR(self)
        self.titlebar.setObjectName('windowTitle')

        self.content_vbox = QVBoxLayout()
        self.content_vbox.setContentsMargins(3, 3, 3, 3)

        # Client Connect
        self.client_hbox = QHBoxLayout()

        self.input_addr = QLineEdit(socket.gethostbyname(socket.gethostname()))
        self.input_addr.setPlaceholderText('Address')
        self.client_hbox.addWidget(self.input_addr)

        self.input_port = QLineEdit(str(port))
        self.input_port.setPlaceholderText('Port')
        self.client_hbox.addWidget(self.input_port)
        
        self.connect = Ripple_BTN(' ▷ ')
        self.connect.clicked.connect(self.connect_server)
        self.client_hbox.addWidget(self.connect)
        self.content_vbox.addLayout(self.client_hbox)

        # Chat Browser
        self.chat_browser = QTextBrowser()
        self.content_vbox.addWidget(self.chat_browser)

        self.chat_hbox = QHBoxLayout()

        self.input_chat = QLineEdit()
        self.input_chat.setPlaceholderText('Type your message...')
        self.input_chat.returnPressed.connect(self.send_message)
        self.chat_hbox.addWidget(self.input_chat)
        
        self.send = Ripple_BTN('Send')
        self.send.clicked.connect(self.send_message)
        self.chat_hbox.addWidget(self.send)
        self.content_vbox.addLayout(self.chat_hbox)

        self.window_vbox.addWidget(self.titlebar)
        self.window_vbox.addLayout(self.content_vbox)

        self.setFixedSize(300, 500)
        self.show()

    def connect_server(self):
        ip = self.input_addr.text()
        port = int(self.input_port.text())
        self.cSocket = client_socket.Client_Socket(ip, port)
        self.cSocket.recv_signal.connect(self.display_message)
        self.cSocket.start()

    @pyqtSlot(str)
    def display_message(self, message):
        self.chat_browser.append(message)

    def send_message(self):
        msg = self.input_chat.text()
        if hasattr(self, 'cSocket') and self.cSocket.sock:
            self.cSocket.sock.send(msg.encode())

        self.input_chat.clear()

    def closeEvent(self, event):
        if hasattr(self, 'cSocket'):
            self.cSocket.sock.send('/exit'.encode())
            self.cSocket.stop()
        event.accept()

# Title Bar
class Title_BAR(QWidget):
    qss = '''
        QWidget {
            color: #FFFFFF;
            background: #333333;
            height: 32px;
        }
        QLabel {
            color: #FFFFFF;
            background: #333333;
            font-size: 16px;
            padding: 5px 5px;
        }
        QToolButton {
            background: #333333;
            border: none;
        }
        QToolButton:hover {
             background: #444444;
        }
    '''

    def __init__(self, parent = None):
        super().__init__(parent)
        self.parent = parent

        self.bar_height = 30
        self.setStyleSheet(self.qss)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        label = QLabel('Chat_GUI')
        label.setFixedHeight(self.bar_height)
        close = self.Create_Tool_BTN('close.png')
        close.clicked.connect(self.close_event)

        layout.addWidget(label)
        layout.addWidget(close)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.is_moving = True
            self.parent.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.parent.is_moving:
            self.parent.move(event.globalPos() - self.parent.offset)

    def Create_Tool_BTN(self, icon_path):
        icon = os.path.join(ROOT_PATH, 'img', icon_path)
        button = QToolButton(self)
        button.setIcon(QIcon(icon))
        button.setIconSize(QSize(self.bar_height, self.bar_height))
        button.setFixedSize(self.bar_height, self.bar_height)
        return button
    
    def close_event(self):
        self.parent.close()

# Ripple Button
class Ripple_BTN(QPushButton):
    qss = '''
        QPushButton {
            color: #fff;
            background-color: #09e;
            padding: 8px;
            font-size: 12pt;
            border-radius: 4px;
        }
        QPushButton:pressed {
            color: #ddd;
        }
    '''
    def __init__(self, parent = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setStyleSheet(self.qss)

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

# START
if __name__ == '__main__':
    app = QApplication(sys.argv)
    cg = Chat_GUI()
    sys.exit(app.exec_())