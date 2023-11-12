import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHBoxLayout, QFrame, QLabel, QVBoxLayout
from qfluentwidgets import ScrollArea, SubtitleLabel, setFont, ImageLabel


class HomeInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('home_interface')

    def show_user_name(self, username):
        vBoxLayout = QVBoxLayout(self)

        label = SubtitleLabel('您好，' + username, self)
        label.setAlignment(Qt.AlignCenter)
        setFont(label, 24)

        basedir = os.path.join(os.path.dirname(__file__), '..')  # main.py path
        img = ImageLabel(os.path.join(basedir, 'resource', 'images', 'icon.png'), self)
        img.setFixedSize(180, 120)

        vBoxLayout.addStretch(1)
        vBoxLayout.addWidget(img, alignment=Qt.AlignCenter)
        vBoxLayout.addWidget(label, alignment=Qt.AlignCenter)
        vBoxLayout.addStretch(1)
