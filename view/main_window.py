import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, FluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, InfoBadge,
                            InfoBadgePosition)
from qfluentwidgets import FluentIcon as Icon


class Widget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.homeInterface = Widget('Search Interface', self)
        self.musicInterface = Widget('Music Interface', self)
        self.videoInterface = Widget('Video Interface', self)
        self.folderInterface = Widget('Folder Interface', self)
        self.settingInterface = Widget('Setting Interface', self)
        self.albumInterface = Widget('Album Interface', self)
        self.albumInterface1 = Widget('Album Interface 1', self)
        self.albumInterface2 = Widget('Album Interface 2', self)
        self.albumInterface1_1 = Widget('Album Interface 1-1', self)

        self.init_navigation()
        self.init_window()

    def init_navigation(self):
        self.addSubInterface(self.homeInterface, Icon.HOME, 'Home')
        self.addSubInterface(self.musicInterface, Icon.MUSIC, 'Music library')
        self.addSubInterface(self.videoInterface, Icon.VIDEO, 'Video library')

        self.navigationInterface.addSeparator()

        self.addSubInterface(self.albumInterface, Icon.ALBUM, 'Albums', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.albumInterface1, Icon.ALBUM, 'Album 1', parent=self.albumInterface)
        self.addSubInterface(self.albumInterface1_1, Icon.ALBUM, 'Album 1.1', parent=self.albumInterface1)
        self.addSubInterface(self.albumInterface2, Icon.ALBUM, 'Album 2', parent=self.albumInterface)
        self.addSubInterface(self.folderInterface, Icon.FOLDER, 'Folder library', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.settingInterface, Icon.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

        # add badge to navigation item
        item = self.navigationInterface.widget(self.videoInterface.objectName())
        InfoBadge.attension(
            text=9,
            parent=item.parent(),
            target=item,
            position=InfoBadgePosition.NAVIGATION_ITEM
        )

    def init_window(self):
        basedir = os.path.join(os.path.dirname(__file__), '..')  # main.py
        self.resize(900, 700)
        self.setWindowIcon(QIcon(os.path.join(basedir, 'resource', 'images', 'logo.ico')))

        # in center
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
