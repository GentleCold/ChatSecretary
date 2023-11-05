from PySide6.QtCore import Qt, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QFont, QFontMetrics
from PySide6.QtWidgets import QHBoxLayout, QFrame, QWidget, QVBoxLayout, QListWidgetItem, QListWidget, QLineEdit, \
    QPushButton, QSizePolicy
from qfluentwidgets import SmoothScrollArea, SubtitleLabel, StrongBodyLabel, BodyLabel


class GraphInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('graph_interface')

        # global vertical layout
        v_box_layout = QVBoxLayout(self)
        v_box_layout.addStretch(1)

