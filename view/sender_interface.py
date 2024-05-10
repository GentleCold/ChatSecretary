import time

from PySide6.QtCore import Qt, QDateTime, QThread, Signal
from PySide6.QtWidgets import QFrame, QVBoxLayout, QDateTimeEdit, QTextEdit, QHBoxLayout, QWidget
from qfluentwidgets import (SubtitleLabel,
                            MessageBoxBase, FluentStyleSheet, setFont, SmoothScrollDelegate, BodyLabel,
                            PushSettingCard, FluentIcon, SmoothScrollArea, InfoBar, InfoBarPosition, PrimaryPushButton)
from qfluentwidgets.components.widgets.line_edit import EditLayer, LineEdit
from qfluentwidgets.components.widgets.menu import TextEditMenu
from qfluentwidgets.components.widgets.spin_box import SpinBoxBase

from api.we_chat_hacker.we_chat_hacker import WeChatHacker


class SendMsg(QThread):
    duration = 0
    receiver = ''
    msg = ''

    finished = Signal()
    add_component = Signal(object)
    error = Signal()

    def run(self):
        time.sleep(self.duration)

        we_chat_hacker = WeChatHacker()
        # check
        username = we_chat_hacker.check_if_login_wechat()
        if username == '':
            self.error.emit()
            return

        we_chat_hacker.send_msg(self.receiver, self.msg)


class Task(QFrame):
    def __init__(self, receiver, datetime, msg, parent=None):
        super().__init__(parent=parent)

        # global vertical layout
        self.h_box_layout = QHBoxLayout(self)
        # h_box_layout.addWidget(BodyLabel(datetime, self))
        # h_box_layout.addWidget(BodyLabel('接收者: ' + receiver, self))
        # h_box_layout.addWidget(BodyLabel('消息: ' + msg, self))

        self.task = PushSettingCard(
            "取消",
            FluentIcon.TAG,
            f"{datetime.toString('yyyy-MM-dd hh:mm:ss')}: to {receiver} with {msg}",
            parent=self,
        )
        self.task.button.setStyleSheet('background-color: #f7768e;')
        self.task.clicked.connect(self.delete)

        self.h_box_layout.addWidget(self.task)

        # start thread of send msg
        self.work = SendMsg()
        self.work.duration = datetime.toSecsSinceEpoch() - time.time()
        self.work.receiver = receiver
        self.work.msg = msg

        self.work.finished.connect(self.on_finished)
        self.work.error.connect(self.handle_error)

        self.work.start()

    def on_finished(self):
        self.task.button.setText("完成")
        self.task.button.setStyleSheet('background-color: #9ece6a;')

    def nothing(self):
        pass

    def handle_error(self):
        InfoBar.info(
            title='警告',
            content="请保持微信窗口的存在",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self,
        )

    def delete(self):
        self.deleteLater()


class TextEdit(QTextEdit):
    """ Text edit """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layer = EditLayer(self)
        self.scrollDelegate = SmoothScrollDelegate(self)
        FluentStyleSheet.LINE_EDIT.apply(self)
        setFont(self)

    def contextMenuEvent(self, e):
        menu = TextEditMenu(self)
        menu.exec(e.globalPos(), ani=True)


class DateTimeEdit(SpinBoxBase, QDateTimeEdit):
    """ Date time edit """

    def paintEvent(self, e):
        QDateTimeEdit.paintEvent(self, e)
        self._drawBorderBottom()


class CustomMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('添加定时任务', self)
        self.time = DateTimeEdit(self)
        self.time.setMinimumDateTime(QDateTime.currentDateTime())

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)

        self.viewLayout.addWidget(BodyLabel('设置发送时间', self))
        self.viewLayout.addWidget(self.time)

        self.viewLayout.addWidget(BodyLabel('设置接收人', self))
        self.lineEdit = LineEdit(self)
        self.lineEdit.setClearButtonEnabled(True)
        self.viewLayout.addWidget(self.lineEdit)

        self.viewLayout.addWidget(BodyLabel('设置发送文本', self))
        self.textEdit = TextEdit(self)
        self.viewLayout.addWidget(self.textEdit)

        # change the text of button
        self.yesButton.setText('添加')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(360)


class SenderInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('sender_interface')

        # global vertical layout
        self.v_box_layout = QVBoxLayout(self)

        # scroll area widget
        content = QWidget()

        scroll_area = SmoothScrollArea()

        # scroll area settings
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content)
        scroll_area.setViewportMargins(0, 5, 0, 5)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet('background-color: transparent;')

        # content layout
        self.content_vbox = QVBoxLayout(content)
        self.content_vbox.setSpacing(0)

        # add scroll area
        self.v_box_layout.addWidget(scroll_area)

        # style settings
        self.setStyleSheet('border: none;')

        button = PrimaryPushButton('添加定时任务')
        button.clicked.connect(self.addTask)
        button.setContentsMargins(0, 0, 0, 0)

        b = QWidget()
        self.h_box_layout = QHBoxLayout(b)
        self.h_box_layout.addStretch()
        self.h_box_layout.addWidget(button)
        self.h_box_layout.addStretch()

        self.content_vbox.addWidget(b, alignment=Qt.AlignTop)
        self.content_vbox.addStretch()

    def addTask(self):
        w = CustomMessageBox(self.window())
        if w.exec():
            task = Task(w.lineEdit.text(), w.time.dateTime(), w.textEdit.toPlainText())
            task.setContentsMargins(0, 0, 0, 0)
            self.content_vbox.removeItem(self.content_vbox.itemAt(self.content_vbox.count() - 1))
            self.content_vbox.addWidget(task, alignment=Qt.AlignTop)
            self.content_vbox.addStretch()
