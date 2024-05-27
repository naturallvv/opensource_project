import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor

class Graphic_UI(QWidget):
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
        Ok_BTN = Ripple_BTN('OK')
        Cancel_BTN = Ripple_BTN('Cancel')

        HBox = QHBoxLayout()
        HBox.addStretch(1)
        HBox.addWidget(Ok_BTN)
        HBox.addWidget(Cancel_BTN)
        HBox.addStretch(1)

        VBox = QVBoxLayout()
        VBox.addStretch(3)
        VBox.addLayout(HBox)
        VBox.addStretch(1)

        self.setLayout(VBox)

        self.setWindowTitle('Graphic_UI')
        self.resize(300, 500)
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
    cg = Graphic_UI()
    sys.exit(app.exec_())