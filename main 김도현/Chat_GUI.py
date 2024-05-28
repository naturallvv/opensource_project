import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QTextBrowser, QLineEdit
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor

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
        input_ip = QLineEdit()
        input_ip.setPlaceholderText('Input Your IP Address:Port')

        input_name = QLineEdit()
        input_name.setPlaceholderText('Input Your NickNAME')

        apply_btn = Ripple_BTN('Apply')

        chat_box = QTextBrowser()

        gesture_btn = Ripple_BTN('G')
        input_chat = QLineEdit()
        send_btn = Ripple_BTN('  ▷  ')

        # TOP
        VBox0 = QVBoxLayout()
        VBox0.addWidget(input_ip)
        VBox0.addWidget(input_name)

        HBox0 = QHBoxLayout()
        HBox0.addLayout(VBox0)
        HBox0.addWidget(apply_btn)

        # BOTTOM
        HBox1 = QHBoxLayout()
        HBox1.addWidget(gesture_btn)
        HBox1.addWidget(input_chat)
        HBox1.addWidget(send_btn)

        # CENTER
        VBoxM = QVBoxLayout()
        VBoxM.addLayout(HBox0)
        VBoxM.addWidget(chat_box)
        VBoxM.addLayout(HBox1)

        self.setLayout(VBoxM)

        self.setWindowTitle('Chat_GUI')
        self.setFixedSize(300, 500)
        self.show()

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