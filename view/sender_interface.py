from PySide6.QtCore import Qt, QDateTime
from PySide6.QtWidgets import QFrame, QVBoxLayout, QDateTimeEdit, QTextEdit, QHBoxLayout
from qfluentwidgets import (SubtitleLabel,
                            MessageBoxBase, PushButton, FluentStyleSheet, setFont, SmoothScrollDelegate, BodyLabel)
from qfluentwidgets.components.widgets.line_edit import EditLayer, LineEdit
from qfluentwidgets.components.widgets.menu import TextEditMenu
from qfluentwidgets.components.widgets.spin_box import SpinBoxBase


class Task(PushButton):
    def __init__(self, receiver, datetime, msg, parent=None):
        super().__init__(parent=parent)

        # global vertical layout
        h_box_layout = QHBoxLayout(self)
        h_box_layout.addWidget(BodyLabel(datetime, self))
        h_box_layout.addWidget(BodyLabel('接收者: ' + receiver, self))
        h_box_layout.addWidget(BodyLabel('消息: ' + msg, self))


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
        self.v_box_layout.setSpacing(0)
        self.v_box_layout.setContentsMargins(0, 0, 0, 0)

        button = PushButton('添加定时任务')
        button.clicked.connect(self.addTask)
        self.v_box_layout.addWidget(button, alignment=Qt.AlignTop)

    def addTask(self):
        w = CustomMessageBox(self.window())
        if w.exec():
            self.v_box_layout.addWidget(Task(w.lineEdit.text(), w.time.dateTime().toString(), w.textEdit.toPlainText()),
                                        alignment=Qt.AlignTop)
