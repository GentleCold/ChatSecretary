from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton
from qfluentwidgets import SettingCard, FluentIconBase, IndeterminateProgressRing
from typing import Union


class PushProgressSettingCard(SettingCard):
    """ Setting card with a push button """

    clicked = Signal()

    def __init__(self, text, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.button = QPushButton(text, self)
        self.progress = IndeterminateProgressRing()
        self.progress.setFixedSize(25, 25)
        self.progress.setStrokeWidth(4)
        self.progress.stop()

        self.hBoxLayout.addWidget(self.progress)
        self.hBoxLayout.addSpacing(5)
        self.hBoxLayout.addWidget(self.button, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button.clicked.connect(self.clicked)

    def start_progress(self):
        self.progress.start()

    def stop_progress(self):
        self.progress.stop()
