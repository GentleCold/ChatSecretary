import time

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QFrame, QLabel, QVBoxLayout, QPushButton, QProgressBar, QProgressDialog, \
    QWidget
from qfluentwidgets import ScrollArea, SubtitleLabel, setFont, PushButton, ToolTipFilter, ToolTipPosition, \
    IndeterminateProgressRing, ExpandLayout, CaptionLabel, SettingCardGroup, PushSettingCard, FluentIcon

from api.we_chat_hacker.we_chat_hacker import WeChatHacker
from view.component.setting_card import PushProgressSettingCard


class SettingsInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hacker = WeChatHacker()
        self.username = self.hacker.check_if_login_wechat()
        self.chat_name = self.hacker.get_current_dialog_name()
        print("chatname: " + self.chat_name)

        self.container_widget = QWidget()
        self.layout = ExpandLayout(self.container_widget)
        self.listenObjectGroup = SettingCardGroup("聊天对象", self.container_widget)
        self.changeObjectCard = PushSettingCard(
            "重新选择",
            FluentIcon.CAFE,
            "当前的聊天对象为：" + self.chat_name,
            parent=self.listenObjectGroup,
        )
        self.getChatRecordCard = PushProgressSettingCard(
            "拉取",
            FluentIcon.CHAT,
            "获取聊天记录",
            parent=self.listenObjectGroup
        )

        self.__init_widgets()
        self.__init_layout()
        self.__init_signal_connection()

    def __init_widgets(self):
        self.setObjectName('settings_interface')
        self.container_widget.setObjectName("ScrollWidget")
        self.container_widget.setStyleSheet("""
            background-color: rgb(255, 255, 255);
        """)

        self.listenObjectGroup.addSettingCard(self.changeObjectCard)
        self.listenObjectGroup.addSettingCard(self.getChatRecordCard)

    def __init_layout(self):
        self.setWidget(self.container_widget)
        self.setWidgetResizable(True)

        self.layout.setSpacing(28)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(30, 10, 30, 0)
        self.layout.addWidget(self.listenObjectGroup)

    def __init_signal_connection(self):
        self.changeObjectCard.clicked.connect(self.change_chat)
        self.getChatRecordCard.clicked.connect(self.get_message)

    def change_chat(self):
        self.chat_name = self.hacker.get_current_dialog_name()
        self.changeObjectCard.setTitle("当前的聊天对象为：" + self.chat_name)

    def get_message(self):
        self.getChatRecordCard.start_progress()
        # time.sleep(5)
        self.hacker.get_all_current_message()
        self.getChatRecordCard.stop_progress()
        print("get success")
        print(self.hacker.get_all_current_message(cache=True))


# class SettingsInterface(QFrame):
#     def __init__(self, parent=None):
#         super().__init__(parent=parent)
#         self.error = Signal()
#         self.setObjectName('settings_interface')
#         self.hacker = WeChatHacker()
#         self.username = self.hacker.check_if_login_wechat()
#         # if not self.username:
#         #     self.error.emit()
#         self.chat_name = self.hacker.get_current_dialog_name()
#
#         # 组件
#         self.btn_get_msg = None
#         self.tip_label = None
#         self.btn_change_chat = None
#         self.hello_label = None
#         self.progress = None
#         self.generate_widgets()
#
#         self.initUI()
#
#     def initUI(self):
#         hello_box = self.get_horizontal_center_box([self.hello_label])
#         tip_box = self.get_horizontal_center_box([self.tip_label])
#         btn_box = self.get_horizontal_center_box([self.btn_get_msg, self.btn_change_chat])
#
#         # 使用QVBoxLayout将hbox垂直居中
#         vbox = QVBoxLayout(self)
#         vbox.addStretch(1)
#         vbox.addLayout(hello_box)
#         vbox.addLayout(tip_box)
#         vbox.addLayout(btn_box)
#         vbox.addStretch(1)
#
#         # spinner = IndeterminateProgressRing()
#         # spinner.setFixedSize(50, 50)
#         # vbox.addWidget(spinner)
#
#         # self.setLayout(vbox)
#
#     def get_horizontal_center_box(self, widget):
#         """widget是一个列表"""
#         # 使用QHBoxLayout将label水平居中
#         hbox = QHBoxLayout()
#         hbox.addStretch(1)
#         for w in widget:
#             hbox.addWidget(w)
#         hbox.addStretch(1)
#         return hbox
#
#     def generate_widgets(self):
#         """生成所有的组件。在布局之前先调用这个函数。为了简化布局函数的复杂度"""
#         hello_label = QLabel("Hello, " + self.username)
#         hello_label.setFont(QFont('Arial', 20))
#         self.hello_label = hello_label
#
#         tip_label = QLabel("您目前的聊天对象为：" + self.chat_name)
#         tip_label.setFont(QFont('Arial', 15))
#         self.tip_label = tip_label
#
#         btn_change_chat = PushButton("Change", self)
#         btn_change_chat.setFont(QFont('Arial', 15))
#         btn_change_chat.setCursor(Qt.PointingHandCursor)
#         btn_change_chat.installEventFilter(ToolTipFilter(btn_change_chat, showDelay=300, position=ToolTipPosition.BOTTOM))
#         btn_change_chat.setToolTip("点击改变聊天对象")
#         btn_change_chat.clicked.connect(self.change_chat)
#         self.btn_change_chat = btn_change_chat
#
#         btn_get_msg = PushButton("Get", self)
#         btn_get_msg.setFont(QFont('Arial', 15))
#         btn_get_msg.setCursor(Qt.PointingHandCursor)
#         btn_get_msg.installEventFilter(ToolTipFilter(btn_get_msg, showDelay=300, position=ToolTipPosition.BOTTOM))
#         btn_get_msg.setToolTip("点击获取当前聊天对象的消息记录")
#         btn_get_msg.clicked.connect(self.get_message)
#         self.btn_get_msg = btn_get_msg
#
#         progress = QProgressDialog(self)
#         progress.setWindowTitle("请稍等...")
#         progress.setLabelText("正在获取数据...")
#         progress.setMinimumSize(400, 120)
#         progress.setMinimum(0)
#         progress.setMaximum(1000)
#         progress.setCancelButton(None)
#         progress.close()
#         self.progress = progress
#
#     def change_chat(self):
#         self.chat_name = self.hacker.get_current_dialog_name()
#         self.tip_label.setText("您目前的聊天对象为：" + self.chat_name)
#
#     def get_message(self):
#         self.progress.show()
#         self.hacker.get_all_current_message()
#         self.progress.close()
#         print(self.hacker.get_all_current_message(cache=True))
