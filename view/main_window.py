import os

from PySide6.QtCore import QSize, QEventLoop, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentIcon as Icon, SplashScreen
from qfluentwidgets import (NavigationItemPosition, FluentWindow)

from view.chat_interface import ChatInterface
from view.graph_interface import GraphInterface
from view.home_interface import HomeInterface
from view.sender_interface import SenderInterface
from view.settings_interface import SettingsInterface
from view.timegraph_interface import TimeGraphInterface
from view.visual_dashboard_interface import VisualDashboardInterface

from common.signal_bus import signalBus


class MainWindow(FluentWindow):
    """
    Main window of the app
    """

    def __init__(self):
        super().__init__()
        self._init_window()

        # create sub interface
        self.home_interface = HomeInterface(self)
        self.chat_interface = ChatInterface(self)
        self.graph_interface = GraphInterface(self)
        self.timegraph_interface = TimeGraphInterface(self)
        self.settings_interface = SettingsInterface(self)
        self.visual_dashboard_interface = VisualDashboardInterface(self)
        self.sender_interface = SenderInterface(self)

        self._init_navigation()
        self.__init_signal_connection()
        # 延时启动页面
        loop = QEventLoop(self)
        QTimer.singleShot(2000, loop.quit)
        loop.exec()
        self.splashScreen.finish()

    def _init_navigation(self):
        """
        Config the icon, name of the interface and add them to navigation
        """
        self.addSubInterface(self.home_interface, Icon.HOME, '主页')
        self.addSubInterface(self.chat_interface, Icon.CHAT, '聊天')
        self.addSubInterface(self.sender_interface, Icon.SEND, '定时发送')
        self.addSubInterface(self.graph_interface, Icon.TILES, '图表')
        self.addSubInterface(self.timegraph_interface, Icon.MARKET, '时间图')
        self.addSubInterface(self.visual_dashboard_interface, Icon.MOVIE, "仪表盘")

        self.navigationInterface.addSeparator()

        self.addSubInterface(self.settings_interface, Icon.SETTING, '设置', NavigationItemPosition.BOTTOM)

    def _init_window(self):
        """
        Set the size, icon, title and position of the window
        :return:
        """
        self.resize(900, 700)
        self.setMinimumWidth(760)
        self.setWindowTitle('ChatSecretary')

        basedir = os.path.join(os.path.dirname(__file__), '..')
        self.icon = QIcon(os.path.join(basedir, 'resource', 'images', 'icon.png'))
        self.icon.setIsMask(False)
        self.setWindowIcon(self.icon)
        self.splashScreen = SplashScreen(self.icon, self, False)
        self.splashScreen.setIconSize(QSize(250, 250))
        self.splashScreen.raise_()

        # position in center
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def __init_signal_connection(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
