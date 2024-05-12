import os

from PySide6.QtGui import QPalette, QPixmap, QBrush, QPainter, QColor
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWidgets import QFrame, QWidget, QHBoxLayout, QSplitter, QMainWindow, QLabel
from PySide6.QtWebEngineWidgets import QWebEngineView
from pyecharts.commons.utils import JsCode

from api.we_chat_hacker.we_chat_hacker import WeChatHacker
from PySide6.QtCore import Qt, QUrl, QDir
from qfluentwidgets import setTheme, Theme
from qframelesswindow.webengine import FramelessWebEngineView
from common.config import cfg
from common.signal_bus import signalBus
from view.component.FloatWebEngineView import FloatWebEngineView
from pyecharts.charts import Line, Liquid, Bar, Gauge, PictorialBar, Pie, Bar3D
from pyecharts.options import GaugePointerOpts, GaugeDetailOpts, GaugeTitleOpts, LabelOpts
import pyecharts.options as opts
from pyecharts.globals import SymbolType


class VisualDashboardInterface(QFrame):
    def __init__(self, parent=None):
        super(VisualDashboardInterface, self).__init__(parent)
        self.setObjectName("VisualDashboard_Interface")

        self.hacker = WeChatHacker()
        self.hacker.check_if_login_wechat()

        self.showEvent = self.show_event

        self.layout = QHBoxLayout(self)
        self.widget1 = QLabel(self)
        self.widget2 = FloatWebEngineView(self)
        self.widget3 = FloatWebEngineView(self)
        self.widget4 = FloatWebEngineView(self)
        self.widget5 = FloatWebEngineView(self)
        self.widget6 = FloatWebEngineView(self)
        self.widget7 = FloatWebEngineView(self)
        self.widget8 = FloatWebEngineView(self)
        self.widget9 = FloatWebEngineView(self)
        self.widget10 = FloatWebEngineView(self)
        # self.initHtml()
        # self.setStyleSheet("QFrame{background-image: url(./resource/images/bigscreen_background.png);}")
        self.setStyleSheet("background-color: rgb(232, 247, 255);")
        # self.setBackground()
        self.initUI()

        self.load = False

    def setBackground(self):
        palette = self.palette()
        pix = QPixmap("./resource/images/bigscreen_background.png")
        pix = pix.scaled(self.width(), self.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)  # 自适应图片大小
        palette.setBrush(self.backgroundRole(), QBrush(pix))  # 设置背景图片
        # palette.setColor(self.backgroundRole(), QColor(192, 253, 123))  # 设置背景颜色
        self.setPalette(palette)

    def initHtml(self):
        basic_path = os.path.join(os.path.dirname(__file__), '..')
        self.widget1.setStyleSheet('background-color: rgb(191, 231, 254);font-size: 25px;')

        self.render_activity_line()
        self.widget6.page().setBackgroundColor(Qt.transparent)
        self.widget6.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.widget6.load(QUrl.fromLocalFile(basic_path + "\\dashboard_charts\\activity_line.html"))

        self.render_today_speak_liquid()
        self.widget3.page().setBackgroundColor(Qt.transparent)
        self.widget3.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.widget3.load(QUrl.fromLocalFile(basic_path + "\\dashboard_charts\\today_speak_liquid.html"))

        self.render_speak_count_bar()
        self.widget7.page().setBackgroundColor(Qt.transparent)
        self.widget7.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.widget7.load(QUrl.fromLocalFile(basic_path + "\\dashboard_charts\\speak_count_bar.html"))

        self.render_word_bar()
        self.widget9.page().setBackgroundColor(Qt.transparent)
        self.widget9.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.widget9.load(QUrl.fromLocalFile(basic_path + "\\dashboard_charts\\word_bar.html"))

        self.render_time_line()
        self.widget10.page().setBackgroundColor(Qt.transparent)
        self.widget10.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.widget10.load(QUrl.fromLocalFile(basic_path + "\\dashboard_charts\\time_line.html"))

        self.render_interactive_gauge()
        self.widget4.page().setBackgroundColor(Qt.transparent)
        self.widget4.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.widget4.load(QUrl.fromLocalFile(basic_path + "\\dashboard_charts\\today_interactive_liquid.html"))

        self.render_intimacy_pictorialbar()
        self.widget5.page().setBackgroundColor(Qt.transparent)
        self.widget5.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.widget5.load(QUrl.fromLocalFile(basic_path + "\\dashboard_charts\\intimacy_pictorialbar.html"))

        self.render_topic_started_pie()
        self.widget8.page().setBackgroundColor(Qt.transparent)
        self.widget8.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.widget8.load(QUrl.fromLocalFile(basic_path + "\\dashboard_charts\\topic_pie.html"))

        self.render_word_person_3dBar()
        self.widget2.page().setBackgroundColor(Qt.transparent)
        self.widget2.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.widget2.load(QUrl.fromLocalFile(basic_path + "\\dashboard_charts\\word_person_3dBar.html"))

        # self.widget5.setZoomFactor(0.1)
        # self.widget6.setZoomFactor(0.15)
        # self.widget6.loadFinished.connect(self.adjust_zoom)
        # self.widget5.load(QUrl.fromLocalFile(basic_path + "\\dashboard_charts\\a.html"))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            print(self.widget5.zoomFactor())
            self.widget5.setZoomFactor(4)
            print(self.widget5.zoomFactor())
        if event.key() == Qt.Key_B:
            print(self.widget5.zoomFactor())
            self.widget5.setZoomFactor(1)
            print(self.widget5.zoomFactor())
        if event.key() == Qt.Key_C:
            print(self.widget5.zoomFactor())
            self.widget5.setZoomFactor(0.2)
            print(self.widget5.zoomFactor())

    # def adjust_zoom(self):
    #     # 获取当前缩放因子
    #     current_zoom = self.widget6.zoomFactor()
    #     print(self.widget6.page().contentsSize())
    #     # 计算新的缩放因子
    #     new_zoom = min(self.widget6.width() / self.widget6.page().contentsSize().width(),
    #                    self.widget6.height() / self.widget6.page().contentsSize().height())
    #     print(self.widget6.width())
    #     print(self.widget6.height())
    #     print(new_zoom)
    #     # 设置新的缩放因子
    #     if new_zoom != current_zoom:
    #         print("zoom changed")
    #         self.widget6.setZoomFactor(new_zoom)

    def initUI(self):
        self.widget1.setFixedHeight(50)
        self.widget1.setText("群聊小秘数据大屏")
        self.widget1.setAlignment(Qt.AlignCenter)

        splitter_width = 2
        splitter1 = QSplitter(Qt.Vertical)
        # splitter1.setStyleSheet("QSplitter::handle { background-color: white }")
        # splitter1.setStyleSheet("QSplitter::handle { background-color: rgb(0,51,102) }")
        # splitter1.setStyleSheet("background-color: rgb(255,255,255);")
        splitter1.setHandleWidth(splitter_width)
        splitter2 = QSplitter(Qt.Horizontal)
        splitter2.setHandleWidth(splitter_width)
        splitter3 = QSplitter(Qt.Horizontal)
        splitter3.setHandleWidth(splitter_width)
        splitter4 = QSplitter(Qt.Vertical)
        splitter4.setHandleWidth(splitter_width)
        splitter5 = QSplitter(Qt.Horizontal)
        splitter5.setHandleWidth(splitter_width)
        splitter6 = QSplitter(Qt.Vertical)
        splitter6.setHandleWidth(splitter_width)
        splitter7 = QSplitter(Qt.Vertical)
        splitter7.setHandleWidth(splitter_width)
        splitter8 = QSplitter(Qt.Vertical)
        splitter8.setHandleWidth(splitter_width)
        splitter9 = QSplitter(Qt.Vertical)
        splitter9.setHandleWidth(splitter_width)

        splitter1.addWidget(self.widget1)
        splitter1.addWidget(splitter2)
        splitter1.setSizes([1, 13])

        splitter2.addWidget(splitter6)
        splitter2.addWidget(splitter3)
        splitter2.setSizes([1, 3])

        splitter3.addWidget(splitter4)
        splitter3.addWidget(splitter8)
        splitter3.setSizes([2, 1])

        splitter4.addWidget(splitter5)
        splitter4.addWidget(self.widget2)
        splitter4.setSizes([1, 3])

        splitter5.addWidget(self.widget3)
        splitter5.addWidget(self.widget4)

        splitter6.addWidget(self.widget5)
        splitter6.addWidget(splitter7)
        splitter6.setSizes([1, 2])

        splitter7.addWidget(self.widget6)
        splitter7.addWidget(self.widget7)

        splitter8.addWidget(self.widget8)
        splitter8.addWidget(splitter9)
        splitter8.setSizes([1, 2])

        splitter9.addWidget(self.widget9)
        splitter9.addWidget(self.widget10)
        #

        self.layout.addWidget(splitter1)
        self.setLayout(self.layout)

    def show_event(self, event):
        if not self.load:
            self.hacker.analyse_message()
            self.initHtml()
        self.load = True
        event.accept()

    def render_activity_line(self):
        msg = self.hacker.get_all_current_message(cache=True)
        count_dict = {}
        time = ''
        for m in msg:
            if m['type'] == 0:
                time = m['msg'][0:m['msg'].rfind('日') + 1]
                time = time.replace('年', '-').replace('月', '-').replace('日', '')
            if m['type'] == 3:
                if time in count_dict:
                    count_dict[time] += 1
                else:
                    count_dict[time] = 1

        x = list(count_dict.keys())
        y = list(count_dict.values())

        (
            Line(init_opts=opts.InitOpts(
                width="400px",
                height="240px",
            ))
            .add_xaxis(xaxis_data=x)
            .add_yaxis(
                series_name="num",
                y_axis=y,
                is_smooth=True,
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="活跃度折线图"),
                datazoom_opts=[
                    opts.DataZoomOpts(xaxis_index=0, range_start=70, range_end=100),
                ],
                legend_opts=opts.LegendOpts(is_show=False),
            )
            .set_series_opts(
                areastyle_opts=opts.AreaStyleOpts(opacity=0.3)
            )
            # todo 是否需要新建文件夹
            .render("dashboard_charts/activity_line.html")
        )

    def render_today_speak_liquid(self):
        total_count = self.hacker.get_current_dialog_name()[
                      self.hacker.get_current_dialog_name().rfind('(') + 1:self.hacker.get_current_dialog_name().rfind(
                          ')')
                      ]
        msg = self.hacker.get_all_current_message(cache=True)
        msg.reverse()
        speak_today = set([])
        speak_temp = set([])
        for m in msg:
            if m['type'] == 3:
                speak_temp.add(m['sender'])
            if m['type'] == 0:
                if m['msg'].find('日') != -1 or m['msg'].find('昨天') != -1:
                    break
                else:
                    speak_today.update(speak_temp)
                    speak_temp.clear()

        (
            Liquid(init_opts=opts.InitOpts(
                width="380px",
                height="190px",
            ))
            .add("发言人数比例",
                 [len(speak_today) / int(total_count)],
                 label_opts=opts.LabelOpts(
                     font_size=20,
                 )
                 )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="今日发言人数比例"),
            )
            .render("dashboard_charts/today_speak_liquid.html")
        )

    def render_speak_count_bar(self):
        speak_count = self.hacker.get_speaker_msg_count()
        sorted_speak_count = sorted(speak_count.items(), key=lambda x: x[1])
        (
            Bar(init_opts=opts.InitOpts(
                width="390px",
                height="250px",
            ))
            .add_xaxis([item[0] for item in sorted_speak_count[0:10]])
            .add_yaxis("num", [item[1] for item in sorted_speak_count[0:10]], bar_max_width=40,
                       label_opts=opts.LabelOpts(
                           color="rgb(255, 255, 255)"
                       ))
            .set_global_opts(
                title_opts=opts.TitleOpts(title="总发言数量"),
                legend_opts=opts.LegendOpts(is_show=False),
            )
            .set_series_opts(
                itemstyle_opts={
                    "normal": {
                        "color": JsCode(
                            """
                            new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                offset: 0,
                                color: 'rgba(97, 144, 232, 1)'
                            }, {
                                offset: 1,
                                color: 'rgba(167, 191, 232, 1)'
                                }], false)
                            """
                        ),
                        "shadowColor": "rgb(0, 160, 221)",
                    }
                }
            )
            .render("dashboard_charts/speak_count_bar.html")
        )

    def render_word_bar(self):
        word_cache = self.hacker.get_word_cache()
        sorted_word_cache = sorted(word_cache.items(), key=lambda x: x[1], reverse=True)
        data = sorted_word_cache[:6]
        data.reverse()

        (
            Bar(init_opts=opts.InitOpts(
                width="380px",
                height="255px",
            ))
            .add_xaxis([item[0] for item in data])
            .add_yaxis("num", [item[1] for item in data])
            .reversal_axis()
            .set_global_opts(
                title_opts=opts.TitleOpts(title="群聊最热词"),
                legend_opts=opts.LegendOpts(is_show=False),
            )
            .render("dashboard_charts/word_bar.html")
        )

    def render_time_line(self):
        x = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        msgs_time = self.hacker.get_msg_time()

        (
            Line(init_opts=opts.InitOpts(
                width="400px",
                height="240px",
            ))
            .add_xaxis(xaxis_data=x)
            .add_yaxis(
                series_name="num",
                y_axis=msgs_time['self'],
                is_smooth=True,
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="时辰活跃度"),
                legend_opts=opts.LegendOpts(is_show=False),
            )
            .set_series_opts(
                areastyle_opts=opts.AreaStyleOpts(opacity=0.3)
            )
            .render("dashboard_charts/time_line.html")
        )

    def render_interactive_gauge(self):
        interactive_count = self.hacker.get_today_interactive_count()
        total_count = self.hacker.get_current_dialog_name()[
                      self.hacker.get_current_dialog_name().rfind('(') + 1:self.hacker.get_current_dialog_name().rfind(
                          ')')
                      ]

        (
            Liquid(init_opts=opts.InitOpts(
                width="380px",
                height="190px",
            ))
            .add("发言人数比例",
                 [len(interactive_count.items()) / int(total_count)],
                 label_opts=opts.LabelOpts(
                     font_size=20,
                 ),
                 shape=SymbolType.DIAMOND,
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="今日互动比例"),
            )
            .render("dashboard_charts/today_interactive_liquid.html")
        )

    def render_intimacy_pictorialbar(self):
        interactive_count = self.hacker.get_interactive_count()
        self_interactive_count = interactive_count['self']
        self_interactive_count = sorted(self_interactive_count.items(), key=lambda x: x[1])

        (
            PictorialBar(init_opts=opts.InitOpts(
                width="400px",
                height="240px",
            ))
            .add_xaxis([item[0] for item in self_interactive_count[0:6]])
            .add_yaxis(
                "intimacy",
                [item[1] for item in self_interactive_count[0:6]],
                label_opts=opts.LabelOpts(is_show=False),
                symbol_size=18,
                symbol_repeat="fixed",
                symbol_offset=[0, 0],
                is_symbol_clip=True,
                symbol=SymbolType.ROUND_RECT,
            )
            .reversal_axis()
            .set_global_opts(
                title_opts=opts.TitleOpts(title="亲密度"),
                xaxis_opts=opts.AxisOpts(is_show=False),
                yaxis_opts=opts.AxisOpts(
                    axistick_opts=opts.AxisTickOpts(is_show=False),
                    axisline_opts=opts.AxisLineOpts(
                        linestyle_opts=opts.LineStyleOpts(opacity=0)
                    ),
                ),
                legend_opts=opts.LegendOpts(is_show=False),
            )
            .render("dashboard_charts/intimacy_pictorialbar.html")
        )

    def render_topic_started_pie(self):
        topic_started_num = self.hacker.get_topic_started_num()
        topic_started_num = sorted(topic_started_num.items(), key=lambda x: x[1])

        (
            Pie(init_opts=opts.InitOpts(
                width="400px",
                height="240px",
            ))
            .add(
                "话题发起比例",
                topic_started_num[:10],
                radius=["30%", "75%"],
                rosetype="radius",
                label_opts=opts.LabelOpts(is_show=False),
            )
            .set_global_opts(title_opts=opts.TitleOpts(title="话题发起比例"), legend_opts=opts.LegendOpts(is_show=False),)
            .render("dashboard_charts/topic_pie.html")
        )

    def render_word_person_3dBar(self):
        word_person = self.hacker.get_word_person()
        word_count = self.hacker.get_word_cache()
        sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        speak_count = self.hacker.get_speaker_msg_count()
        sorted_speak_count = sorted(speak_count.items(), key=lambda x: x[1], reverse=True)

        word_chosen = [item[0] for item in sorted_word_count[:12]]
        speaker_chosen = [item[0] for item in sorted_speak_count[:6]]

        data = []

        for index1, word in enumerate(word_chosen):
            for index2, speaker in enumerate(speaker_chosen):
                if word in word_person[speaker]:
                    data.append([index1, index2, word_person[speaker][word]])

        (
            Bar3D(init_opts=opts.InitOpts(
                width="800px",
            ))
            .add(
                series_name="",
                data=data,
                xaxis3d_opts=opts.Axis3DOpts(type_="category", data=word_chosen, axislabel_opts=LabelOpts(interval=0)),
                yaxis3d_opts=opts.Axis3DOpts(type_="category", data=speaker_chosen),
                zaxis3d_opts=opts.Axis3DOpts(type_="value"),
            )
            .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(
                    max_=20,
                    range_color=[
                        "#313695",
                        "#4575b4",
                        "#74add1",
                        "#abd9e9",
                        "#e0f3f8",
                        "#ffffbf",
                        "#fee090",
                        "#fdae61",
                        "#f46d43",
                        "#d73027",
                        "#a50026",
                    ],
                )
            )
            .render("dashboard_charts/word_person_3dBar.html")
        )
