import functools

from PySide6 import QtCharts
from PySide6.QtCore import Qt, QEasingCurve, QThread, Signal, Slot
from PySide6.QtGui import QPainter, QColor, QFont, QFontMetrics
from PySide6.QtWidgets import QHBoxLayout, QFrame, QWidget, QVBoxLayout, QListWidgetItem, QListWidget, QLineEdit, \
    QPushButton, QSizePolicy
from qfluentwidgets import SmoothScrollArea, SubtitleLabel, StrongBodyLabel, BodyLabel, PushButton, MessageBox, \
    IndeterminateProgressBar, InfoBarPosition, InfoBar, ComboBox

from api.we_chat_hacker.we_chat_hacker import WeChatHacker
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import matplotlib.colors as mc

EMOTIONS = {}


class ChatBubbleItem(QWidget):
    def __init__(self, sender, message, msg_type, parent=None):
        """
        :param sender: pass 'self' if the sender is user
        :param message: message text
        """
        super().__init__(parent=parent)

        # global vertical layout
        v_box_layout = QVBoxLayout(self)

        if msg_type == 0 or msg_type == 1:
            v_box_layout.addWidget(BodyLabel(message))
            return

        # sender and msg
        sender_label = BodyLabel()
        sender_label.setText(sender)
        msg = BodyLabel()
        emotion = BodyLabel()

        emotion_value = 0
        align_flag = Qt.AlignLeft
        background_color = '#FFFFFF'

        if sender == 'self':
            background_color = '#95EC69'
            align_flag = Qt.AlignRight
            sender_label.setText('你')

        # calculate emotion value
        try:
            s = SnowNLP(message.strip())
            for sentence in s.sentences:
                emotion_value += SnowNLP(sentence).sentiments
            if len(s.sentences):
                emotion_value /= len(s.sentences)
        except:
            pass

        sender_label.setAlignment(align_flag)
        sender_label.setStyleSheet('color: #B8B8B8;')

        # magic to set word wrap(break-all)
        msg.setText("\u200b".join(message))
        msg.setWordWrap(True)

        msg.setMaximumWidth(400)
        msg.setStyleSheet(f'background-color: {background_color}; padding: 5;')

        # magic to avoid hiding of words
        msg.setMinimumHeight(msg.sizeHint().height() + 5)

        if sender not in EMOTIONS:
            EMOTIONS[sender] = [emotion_value]
        else:
            EMOTIONS[sender].append(emotion_value)

        emotion.setText(f'情绪值：{emotion_value}')

        # define reflect of color
        color = mc.to_hex(plt.cm.RdYlGn(emotion_value))
        emotion.setStyleSheet(f'background-color: {color}; padding: 5;')

        v_box_layout.addWidget(sender_label)
        v_box_layout.addWidget(msg)
        v_box_layout.addWidget(emotion)


class ChatBoxView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # global vertical layout
        self.work = None
        self.bar = None
        self.v_box_layout = QVBoxLayout(self)

        # scroll area widget
        content = QWidget()

        scroll_area = SmoothScrollArea()

        # scroll area settings
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content)
        scroll_area.setViewportMargins(0, 5, 0, 5)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # content layout
        self.content_vbox = QVBoxLayout(content)

        # add scroll area
        self.v_box_layout.addWidget(scroll_area)

        # style settings
        self.setStyleSheet('border: none;')

    @Slot(object)
    def add_bubble(self, msg):
        alignment = Qt.AlignLeft
        if msg['sender'] == 'self':
            alignment = Qt.AlignRight
        elif msg['type'] == 0 or msg['type'] == 1:
            alignment = Qt.AlignCenter

        self.content_vbox.addWidget(ChatBubbleItem(msg['sender'], msg['msg'], msg['type']),
                                    alignment=alignment)

    def add_all_bubbles_thread(self, parent):
        self.bar = IndeterminateProgressBar(self)
        self.v_box_layout.addWidget(self.bar, alignment=Qt.AlignCenter)
        self.work = AddBubble()
        self.work.add_component.connect(self.add_bubble)
        self.work.finished.connect(functools.partial(self.on_finished, parent))
        self.work.error.connect(self.handle_error)

        self.work.start()

    def on_finished(self, parent):
        parent.draw_chart()
        if self.bar:
            self.bar.deleteLater()

    def handle_error(self):
        InfoBar.info(
            title='警告',
            content="请保持微信窗口的存在",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self,
        )


class AddBubble(QThread):
    finished = Signal()
    add_component = Signal(object)
    error = Signal()

    def run(self):
        we_chat_hacker = WeChatHacker()

        # check
        username = we_chat_hacker.check_if_login_wechat()
        if username == '':
            self.error.emit()
            return

        msgs = we_chat_hacker.get_all_current_message()
        for msg in msgs:
            self.add_component.emit(msg)


class OperationView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # global vertical layout
        self.v_box_layout = QVBoxLayout(self)

    def add_btn(self, parent):
        btn_get_msg = PushButton('获取当前微信窗口的聊天记录', self)
        btn_get_msg.clicked.connect(functools.partial(parent.chat_box_view.add_all_bubbles_thread, parent.chart_view))

        self.v_box_layout.addWidget(btn_get_msg)


class ChartView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.v_box_layout = QVBoxLayout(self)
        self.chart = QtCharts.QChart()
        chart_view = QtCharts.QChartView(self.chart)

        self.chart.setTitle("情绪折线图")

        self.comboBox = ComboBox()
        self.comboBox.setCurrentIndex(0)
        self.comboBox.setMinimumWidth(210)

        self.v_box_layout.addWidget(self.comboBox)
        self.v_box_layout.addWidget(chart_view)

        self.comboBox.currentIndexChanged.connect(
            lambda index: self.chart.series()[index].setVisible(True) if index >= 0 else None)

    def draw_chart(self):
        # 添加数据点
        sorted_value = dict(sorted(EMOTIONS.items(), key=lambda x: len(x[1]), reverse=True))
        for key, value_list in sorted_value.items():
            if key == '':
                continue
            series = QtCharts.QLineSeries()
            for i, value in enumerate(value_list):
                series.append(i, value)

            series.setName(key)
            series.setVisible(False)
            self.chart.addSeries(series)
            self.chart.createDefaultAxes()

            self.comboBox.addItem(key)


class ChatInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('chat_interface')

        # global vertical layout
        self.v_box_layout = QVBoxLayout(self)

        self.chat_box_view = ChatBoxView(self)
        operation_view = OperationView(self)
        self.chart_view = ChartView(self)

        operation_view.add_btn(self)

        self.v_box_layout.addWidget(self.chat_box_view)
        self.v_box_layout.addWidget(self.chart_view)
        self.v_box_layout.addWidget(operation_view)
