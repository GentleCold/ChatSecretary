import functools
import json
import os

import matplotlib.colors as mc
import matplotlib.pyplot as plt
import pyecharts.options as opts
from PySide6.QtCore import Qt, QThread, Signal, Slot, QUrl
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QHBoxLayout
from pyecharts.charts import Line
from qfluentwidgets import SmoothScrollArea, BodyLabel, PushButton, IndeterminateProgressBar, InfoBarPosition, InfoBar, \
    PrimaryPushButton
from qframelesswindow.webengine import FramelessWebEngineView
from snownlp import SnowNLP

from api.gpt.gpt import GPT
from api.we_chat_hacker.we_chat_hacker import WeChatHacker

EMOTIONS = {}
MSG_COUNT = 0
FORGPT = []


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

        global MSG_COUNT
        MSG_COUNT += 1
        if sender not in EMOTIONS:
            EMOTIONS[sender] = [[emotion_value, MSG_COUNT]]
        else:
            EMOTIONS[sender].append([emotion_value, MSG_COUNT])

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

    def add_all_bubbles_thread(self, parent, gpt):
        self.bar = IndeterminateProgressBar(self)
        self.v_box_layout.addWidget(self.bar, alignment=Qt.AlignCenter)
        self.work = AddBubble()
        self.work.add_component.connect(self.add_bubble)
        self.work.finished.connect(functools.partial(self.on_finished, parent, gpt))
        self.work.error.connect(self.handle_error)

        self.work.start()

    def on_finished(self, parent, gpt):
        parent.draw_chart()
        gpt_api = GPT()
        print(json.dumps(FORGPT, ensure_ascii=False))
        ret = gpt_api.get_response(
            f"你是一名聊天助手，接下来我会给出一段json格式的我和其他人的聊天记录，其中sender字段为self的表示我的发言，你需要帮我根据现有的聊天记录扩展更多的话题，给出发言意见，注意给出的发言意见不需要是json格式，仅为字符串即可，以下是聊天记录：{json.dumps(FORGPT, ensure_ascii=False)}，再次注意给出的发言意见不需要是json格式，仅为字符串即可")
        print(ret)
        gpt.setText(ret['output']['choices'][0]['message']['content'])
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

        for msg in reversed(msgs):
            if len(FORGPT) < 10:
                FORGPT.append(msg)
            else:
                break


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
        self.chart = FramelessWebEngineView(self)
        self.chart.setMinimumHeight(250)

        self.v_box_layout.addWidget(self.chart)

    def draw_chart(self):
        basic_path = os.path.join(os.path.dirname(__file__), '..')

        c = Line(init_opts=opts.InitOpts(
            width="370px",
            height="220px",
        ))

        print(json.dumps(EMOTIONS, ensure_ascii=False))
        for key, emotions in EMOTIONS.items():
            if key == "":
                continue
            x = []
            y = []
            for e in emotions:
                x.append(e[1])
                y.append(e[0])

            c.add_xaxis(xaxis_data=x)
            c.add_yaxis(
                series_name=key,
                y_axis=y,
                is_smooth=True,
                label_opts=opts.LabelOpts(is_show=False),
            )

        c.add_xaxis(xaxis_data=[i for i in range(MSG_COUNT)])
        (c
         .set_global_opts(
            title_opts=opts.TitleOpts(title="情绪折线图"),
            datazoom_opts=[
                opts.DataZoomOpts(xaxis_index=0, range_start=70, range_end=100),
            ],
        )
         .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(opacity=0.3)
        )
         # todo 是否需要新建文件夹
         .render("dashboard_charts/emotion_line.html")
         )
        # self.widget6.page().setBackgroundColor(Qt.transparent)
        self.chart.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.chart.load(QUrl.fromLocalFile(basic_path + "\\dashboard_charts\\emotion_line.html"))


class ChatInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('chat_interface')
        self.setStyleSheet('border: none;')

        # global vertical layout
        self.v_box_layout = QVBoxLayout(self)

        self.chat_box_view = ChatBoxView(self)

        # operation_view = OperationView(self)
        self.chart_view = ChartView(self)

        chart_gpt = QWidget()
        layout = QHBoxLayout(chart_gpt)
        layout.addWidget(self.chart_view)

        # scroll area widget
        content = QWidget()
        scroll_area = SmoothScrollArea()
        # scroll area settings
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content)
        scroll_area.setViewportMargins(0, 5, 0, 5)
        scroll_area.setStyleSheet('background-color: #ffffff;')
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setMinimumWidth(400)
        scroll_area.setMaximumWidth(400)

        # content layout
        self.content_vbox = QVBoxLayout(content)
        self.content_vbox.setSpacing(0)
        self.gpt = BodyLabel()
        self.gpt.setWordWrap(True)

        self.regenerate = PrimaryPushButton("重新生成建议")
        self.content_vbox.addWidget(self.regenerate)
        self.content_vbox.addWidget(self.gpt)

        layout.addWidget(scroll_area)
        # operation_view.add_btn(self)

        self.v_box_layout.addWidget(self.chat_box_view)
        self.v_box_layout.addWidget(chart_gpt)
        # self.v_box_layout.addWidget(operation_view)

    def showEvent(self, evt):
        self.chat_box_view.add_all_bubbles_thread(self.chart_view, self.gpt)
        QWidget.showEvent(self, evt)
