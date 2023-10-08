from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QFrame
from qfluentwidgets import ScrollArea, SubtitleLabel, setFont


class ChatInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('chat_interface')

    def show_user_name(self, username):
        label = SubtitleLabel('您好，' + username, self)
        hBoxLayout = QHBoxLayout(self)

        setFont(label, 24)
        label.setAlignment(Qt.AlignCenter)
        hBoxLayout.addWidget(label, 1, Qt.AlignCenter)
