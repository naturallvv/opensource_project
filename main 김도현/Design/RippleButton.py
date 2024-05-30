from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtWidgets import QPushButton

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