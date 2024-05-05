import os

from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWidgets import QFrame, QWidget, QHBoxLayout, QSplitter, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from pyecharts.commons.utils import JsCode

from api.we_chat_hacker.we_chat_hacker import WeChatHacker
from PySide6.QtCore import Qt, QUrl, QDir
from qfluentwidgets import setTheme, Theme
from qframelesswindow.webengine import FramelessWebEngineView
from common.config import cfg
from common.signal_bus import signalBus
from pyecharts.charts import Line, Liquid, Bar
from pyecharts.faker import Faker
import pyecharts.options as opts


def test1(a):
    print(a)


class VisualDashboardInterface(QFrame):
    def __init__(self, parent=None):
        super(VisualDashboardInterface, self).__init__(parent)
        self.setObjectName("VisualDashboard_Interface")

        self.hacker = WeChatHacker()
        self.hacker.check_if_login_wechat()

        self.showEvent = self.show_event

        # self.container_widget = QWidget(self)
        self.layout = QHBoxLayout(self)
        self.widget1 = FramelessWebEngineView(self)
        # self.widget1 = QWebEngineView()
        self.widget2 = FramelessWebEngineView(self)
        self.widget3 = FramelessWebEngineView(self)
        self.widget4 = FramelessWebEngineView(self)
        self.widget5 = FramelessWebEngineView(self)
        self.widget6 = FramelessWebEngineView(self)
        self.widget7 = FramelessWebEngineView(self)
        self.widget8 = FramelessWebEngineView(self)
        self.widget9 = FramelessWebEngineView(self)
        self.widget10 = FramelessWebEngineView(self)
        # self.initHtml()
        self.initUI()

        self.load = False

    def initHtml(self):
        basic_path = os.path.join(os.path.dirname(__file__), '..')
        self.render_activity_line()
        # self.widget6.page().setBackgroundColor(Qt.transparent)
        self.widget6.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.widget6.load(QUrl.fromLocalFile(basic_path + "\\dashboard_charts\\activity_line.html"))

        self.render_today_speak_liquid()
        self.widget3.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.widget3.load(QUrl.fromLocalFile(basic_path + "\\dashboard_charts\\today_speak_liquid.html"))

        self.render_speak_count_bar()
        self.widget7.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.widget7.load(QUrl.fromLocalFile(basic_path + "\\dashboard_charts\\speak_count_bar.html"))

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
            .add("lq",
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


