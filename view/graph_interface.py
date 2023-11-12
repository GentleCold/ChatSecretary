"""
Reference: https://doc.qt.io/qtforpython-6/examples/example_external_networkx.html
"""
import math

from PySide6.QtCore import Qt, QEasingCurve, QRectF, QLineF, QPointF, QPropertyAnimation, QParallelAnimationGroup
from PySide6.QtGui import QPainter, QColor, QFont, QFontMetrics, QPen, QBrush, QPolygonF, QPainterPath
from PySide6.QtWidgets import QHBoxLayout, QFrame, QWidget, QVBoxLayout, QListWidgetItem, QListWidget, QLineEdit, \
    QPushButton, QSizePolicy, QGraphicsObject, QGraphicsItem, QStyleOptionGraphicsItem, QGraphicsView, QGraphicsScene, \
    QComboBox, QFileDialog, QLabel, QDockWidget, QGraphicsDropShadowEffect
from qfluentwidgets import SmoothScrollArea, SubtitleLabel, StrongBodyLabel, BodyLabel, ComboBox, PushButton

from api.data_analyse.import_messages_from_QQ import QQGroupMessage
from api.data_analyse.msg_processor import MsgProcessor


class GraphInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('graph_interface')

        # global vertical layout
        self.v_box_layout = QVBoxLayout(self)
        self.view = None
        self.import_msg_btn = PushButton('导入QQ聊天记录', self)
        self.import_msg_btn.clicked.connect(self.open_file)
        self.v_box_layout.addWidget(self.import_msg_btn)

        # display node info
        self.display_widget = DisplayInfoWidget(parent=self)
        self.display_widget.hide()

        self.mp = None

        # 是否展示lda结果
        self.lda_flag = False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            # print("press A")
            self.lda_flag = not self.lda_flag
        self.switch_network(self.lda_flag)

    def switch_network(self, flag):
        self.v_box_layout.removeWidget(self.view)
        self.view = self.mp.draw_network([0, 1], self, self.display_widget, flag)
        self.v_box_layout.addWidget(self.view)

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "打开文件", "", "文本文件 (*.txt);;所有文件 (*)", options=options)
        QQ = QQGroupMessage(file_path)
        msgDF = QQ.get_messagesDF()
        self.mp = MsgProcessor()
        self.mp.init_from_pd(msgDF)
        # 将 display_widget传入，在鼠标触碰节点时出现
        self.view = self.mp.draw_network([0, 1], self, self.display_widget, self.lda_flag)
        self.v_box_layout.addWidget(self.view)

        # self.hover_tip_widget.raise_()
        # self.display_widget.raise_()


class DisplayInfoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(0, 0)
        shadow.setBlurRadius(20)
        shadow.setColor("#808080")
        self.setGraphicsEffect(shadow)
        self.resize(200, 100)
        self.text = None

    def set_text(self, text):
        self.text = text

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.white)

        path = QPainterPath()
        w, h = self.width(), self.height()
        radius = 20  # 圆角半径
        path.addRoundedRect(0, 0, w, h, radius, radius)
        painter.drawPath(path)

        # paint text
        if self.text is not None:
            painter = QPainter(self)
            painter.setPen(QColor("#000000"))
            painter.drawText(5, 5, self.text)


