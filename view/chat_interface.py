from PySide6.QtCore import Qt, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QFont, QFontMetrics
from PySide6.QtWidgets import QHBoxLayout, QFrame, QWidget, QVBoxLayout, QListWidgetItem, QListWidget, QLineEdit, \
    QPushButton, QSizePolicy
from qfluentwidgets import SmoothScrollArea, SubtitleLabel, StrongBodyLabel, BodyLabel


class ChatBubbleItem(QWidget):
    def __init__(self, sender, message, parent=None):
        super().__init__(parent=parent)

        # global vertical layout
        v_box_layout = QVBoxLayout(self)

        # sender and msg
        sender_label = BodyLabel(sender)
        msg = StrongBodyLabel()

        if sender == 'self':
            sender_label.setAlignment(Qt.AlignRight)

        # magic to set word wrap(break-all)
        msg.setText("\u200b".join(message))
        msg.setWordWrap(True)

        msg.setMaximumWidth(400)
        msg.setStyleSheet('background-color: #E7F8FF; padding: 5;')

        # magic to avoid hiding of words
        msg.setMinimumHeight(msg.sizeHint().height() + 5)

        v_box_layout.addWidget(sender_label)
        v_box_layout.addWidget(msg)


class ChatBoxView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # global vertical layout
        v_box_layout = QVBoxLayout(self)

        # scroll area widget
        content = QWidget()

        scroll_area = SmoothScrollArea()

        # scroll area settings
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content)
        scroll_area.setViewportMargins(0, 5, 0, 5)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # content layout
        content_vbox = QVBoxLayout(content)
        content_vbox.addWidget(ChatBubbleItem('self', 'This is a lllllllllllllllllong text', content), alignment=Qt.AlignRight)
        content_vbox.addWidget(ChatBubbleItem('a', 'This is a lllllllllllllllllong text', content), alignment=Qt.AlignLeft)
        content_vbox.addWidget(ChatBubbleItem('b', 'This is a llll、llllllwdaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaalllllllong text', content), alignment=Qt.AlignLeft)
        content_vbox.addWidget(ChatBubbleItem('self', 'This is a lllllllllllllllllong text', content), alignment=Qt.AlignRight)
        content_vbox.addWidget(ChatBubbleItem('c', 'This is a lllllllllllllllllong text', content), alignment=Qt.AlignLeft)

        # add scroll area
        v_box_layout.addWidget(scroll_area)

        # style settings
        self.setStyleSheet('border: none;')


class ChatInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('chat_interface')

        # global vertical layout
        v_box_layout = QVBoxLayout(self)
        v_box_layout.addWidget(ChatBoxView(self))
        v_box_layout.addStretch(1)  # todo: operation view
