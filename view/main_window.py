from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentIcon as Icon
from qfluentwidgets import (NavigationItemPosition, FluentWindow)

from view.chat_interface import ChatInterface
from view.graph_interface import GraphInterface
from view.home_interface import HomeInterface
from view.sender_interface import SenderInterface
from view.settings_interface import SettingsInterface
from view.timegraph_interface import TimeGraphInterface


class MainWindow(FluentWindow):
    """
    Main window of the app
    """

    def __init__(self):
        super().__init__()

        # create sub interface
        self.home_interface = HomeInterface(self)
        self.chat_interface = ChatInterface(self)
        self.graph_interface = GraphInterface(self)
        self.timegraph_interface = TimeGraphInterface(self)
        self.settings_interface = SettingsInterface(self)
        self.sender_interface = SenderInterface(self)

        self._init_navigation()
        self._init_window()

    def _init_navigation(self):
        """
        Config the icon, name of the interface and add them to navigation
        """
        self.addSubInterface(self.home_interface, Icon.HOME, '主页')
        self.addSubInterface(self.chat_interface, Icon.CHAT, '聊天')
        self.addSubInterface(self.sender_interface, Icon.SEND, '定时发送')
        self.addSubInterface(self.graph_interface, Icon.TILES, '图表')
        self.addSubInterface(self.timegraph_interface, Icon.MARKET, '时间图')

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

        # position in center
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
