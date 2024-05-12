from PySide6.QtGui import QPainter, QPalette, QColor, QBrush
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsDropShadowEffect
from qframelesswindow.webengine import FramelessWebEngineView


class FloatWebEngineView(FramelessWebEngineView):

    def __init__(self, parent):
        super().__init__(parent=parent)

    def add_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(Qt.gray)
        self.setGraphicsEffect(shadow)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制背景
        painter.setBrush(QColor(250, 250, 255, 80))
        painter.setPen(QColor(43, 45, 48, 80))
        painter.drawRoundedRect(self.rect(), 8, 8)

        painter.end()
