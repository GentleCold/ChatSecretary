"""
Reference: https://doc.qt.io/qtforpython-6/examples/example_external_networkx.html
"""
import math

from PySide6.QtCore import Qt, QEasingCurve, QRectF, QLineF, QPointF, QPropertyAnimation, QParallelAnimationGroup
from PySide6.QtGui import QPainter, QColor, QFont, QFontMetrics, QPen, QBrush, QPolygonF
from PySide6.QtWidgets import QHBoxLayout, QFrame, QWidget, QVBoxLayout, QListWidgetItem, QListWidget, QLineEdit, \
    QPushButton, QSizePolicy, QGraphicsObject, QGraphicsItem, QStyleOptionGraphicsItem, QGraphicsView, QGraphicsScene, \
    QComboBox, QFileDialog
from qfluentwidgets import SmoothScrollArea, SubtitleLabel, StrongBodyLabel, BodyLabel, ComboBox, PushButton

import networkx as nx

from api.data_analyse.import_messages_from_QQ import QQGroupMessage
from api.data_analyse.msg_processor import MsgProcessor


class GraphInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('graph_interface')

        # global vertical layout
        self.v_box_layout = QVBoxLayout(self)

        # graph
        # self.graph = nx.Graph()
        # self.graph.add_edges_from(
        #     [
        #         ("1", "2"),
        #         ("2", "3"),
        #     ]
        # )
        #
        # self.view = GraphView(self.graph)
        # self.choice_combo = ComboBox()
        self.view = None
        self.import_msg_btn = PushButton('导入QQ聊天记录', self)

        self.import_msg_btn.clicked.connect(self.open_file)

        # self.choice_combo.addItems(self.view.get_nx_layouts())
        # self.choice_combo.currentTextChanged.connect(self.view.set_nx_layout)

        self.v_box_layout.addWidget(self.import_msg_btn)
        # v_box_layout.addWidget(self.choice_combo)
        # v_box_layout.addWidget(self.view)


    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "打开文件", "", "文本文件 (*.txt);;所有文件 (*)",
                                                   options=options)

        QQ = QQGroupMessage(file_path)
        msgDF = QQ.get_messagesDF()
        mp = MsgProcessor()
        mp.init_from_pd(msgDF)

        self.view = mp.draw_network([0, 1])

        # most_commons_words = mp.get_most_common(1)
        # name = mp.get_name_with_idx(1)

        # add graph edge
        # edges = [(name, word) for word, fre in most_commons_words]

        # graph = network.Graph()

        # self.view = GraphView(graph)
        self.v_box_layout.addWidget(self.view)





