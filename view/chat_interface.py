import sys
import threading

from PySide6.QtCore import Qt, QEasingCurve, QThread, Signal, Slot
from PySide6.QtGui import QPainter, QColor, QFont, QFontMetrics
from PySide6.QtWidgets import QHBoxLayout, QFrame, QWidget, QVBoxLayout, QListWidgetItem, QListWidget, QLineEdit, \
    QPushButton, QSizePolicy
from qfluentwidgets import SmoothScrollArea, SubtitleLabel, StrongBodyLabel, BodyLabel, PushButton, MessageBox, \
    IndeterminateProgressBar

from api.we_chat_hacker.we_chat_hacker import WeChatHacker


class ChatBubbleItem(QWidget):
    def __init__(self, sender, message, parent=None):
        """
        :param sender: pass 'self' if the sender is user
        :param message: message text
        """
        super().__init__(parent=parent)

        # global vertical layout
        v_box_layout = QVBoxLayout(self)

        # sender and msg
        sender_label = BodyLabel()
        msg = StrongBodyLabel()

        sender_label.setText(sender)
        if sender == 'self':
            sender_label.setAlignment(Qt.AlignRight)
            sender_label.setText('你')

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
        self.work = None
        self.bar = None
        self.v_box_layout = QVBoxLayout(self)

        # scroll area widget
        content = QWidget()

        scroll_area = SmoothScrollArea()

        # scroll area settings
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content)
        scroll_area.setViewportMargins(0, 5, 0, 5)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # content layout
        self.content_vbox = QVBoxLayout(content)

        # add scroll area
        self.v_box_layout.addWidget(scroll_area)

        # style settings
        self.setStyleSheet('border: none;')

    @Slot(object)
    def add_bubble(self, msg):
        alignment = Qt.AlignLeft
        if msg['sender'] == 'self':
            alignment = Qt.AlignRight

        self.content_vbox.addWidget(ChatBubbleItem(msg['sender'], msg['msg']),
                                    alignment=alignment)

    def add_all_bubbles_thread(self):
        self.bar = IndeterminateProgressBar(self)
        self.v_box_layout.addWidget(self.bar, alignment=Qt.AlignCenter)

        self.work = AddBubble()
        self.work.add_component.connect(self.add_bubble)
        self.work.finished.connect(self.on_finished)

        self.work.start()

    def on_finished(self):
        if self.bar:
            self.bar.deleteLater()


class AddBubble(QThread):
    finished = Signal()
    add_component = Signal(object)

    def run(self):
        we_chat_hacker = WeChatHacker()

        # check
        username = we_chat_hacker.check_if_login_wechat()
        while username == '':
            title = '登录微信'
            content = '您需要登录并保持微信窗口才能使用小蜜哦~'
            m = MessageBox(title, content)
            m.yesButton.setText('重试')
            m.cancelButton.setText('退出')
            if m.exec():
                username = we_chat_hacker.check_if_login_wechat()
            else:
                sys.exit()

        msgs = we_chat_hacker.get_all_current_message()
        self.finished.emit()
        for msg in msgs:
            self.add_component.emit(msg)


class OperationView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # global vertical layout
        self.v_box_layout = QVBoxLayout(self)

    def add_btn(self, chat_box_widget):
        btn_get_msg = PushButton('获取当前微信窗口的聊天记录', self)
        btn_get_msg.clicked.connect(chat_box_widget.add_all_bubbles_thread)

        self.v_box_layout.addWidget(btn_get_msg)


class ChatInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('chat_interface')

        # global vertical layout
        v_box_layout = QVBoxLayout(self)

        chat_box_view = ChatBoxView(self)
        operation_view = OperationView(self)

        operation_view.add_btn(chat_box_view)

        v_box_layout.addWidget(chat_box_view)
        v_box_layout.addWidget(operation_view)
