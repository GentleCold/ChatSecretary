from PySide6.QtWidgets import QFrame, QWidget, QHBoxLayout, QSplitter, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from api.we_chat_hacker.we_chat_hacker import WeChatHacker
from PySide6.QtCore import Qt, QUrl
from qfluentwidgets import setTheme, Theme
from qframelesswindow.webengine import FramelessWebEngineView
from common.config import cfg
from common.signal_bus import signalBus


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
        self.initUI()

    def initUI(self):
        # self.setStyleSheet("""
        #     QWebEngineView {
        #         background-color: rgb(100, 100, 100);
        #     }
        # """)

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
        # self.layout.addWidget(self.widget1)
        self.setLayout(self.layout)

        # print(cfg.theme)
        # setTheme(cfg.theme)

    def show_event(self, event):
        print("dashboard show")
        if self.hacker.is_cached():
            msg = self.hacker.get_all_current_message(cache=True)
            # print(msg)
        event.accept()
