import time

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QFrame, QLabel, QVBoxLayout, QPushButton, QProgressBar, QProgressDialog, \
    QWidget
from qfluentwidgets import ScrollArea, SubtitleLabel, setFont, PushButton, ToolTipFilter, ToolTipPosition, \
    IndeterminateProgressRing, ExpandLayout, CaptionLabel, SettingCardGroup, PushSettingCard, FluentIcon, HyperlinkCard, \
    PrimaryPushSettingCard, SwitchSettingCard, OptionsSettingCard, CustomColorSettingCard, setTheme, setThemeColor, \
    Theme, ThemeColor
from common.config import YEAR, AUTHOR, VERSION, cfg
from common.signal_bus import signalBus

from api.we_chat_hacker.we_chat_hacker import WeChatHacker
from view.component.setting_card import PushProgressSettingCard


class SettingsInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hacker = WeChatHacker()
        self.username = self.hacker.check_if_login_wechat()
        self.chat_name = self.hacker.get_current_dialog_name()

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

        self.personalSettingGroup = SettingCardGroup(
            "个性化", self.container_widget
        )
        self.micaSettingCard = SwitchSettingCard(
            FluentIcon.TRANSPARENT,
            "云母效果",
            "窗口显示半透明效果",
            cfg.micaEnabled,
            self.personalSettingGroup
        )
        self.themeSettingCard = OptionsSettingCard(
            cfg.themeMode,
            FluentIcon.BRUSH,
            "应用主题",
            "调整应用的外观主题",
            ["浅色", "深色", "跟随系统"],
            self.personalSettingGroup
        )
        self.themeColorSettingCard = CustomColorSettingCard(
            cfg.themeColor,
            FluentIcon.PALETTE,
            "主题颜色",
            "调整应用的主题颜色",
            self.personalSettingGroup
        )

        self.updateSoftwareGroup = SettingCardGroup("软件更新", self.container_widget)
        self.updateSoftwareCard = SwitchSettingCard(
            FluentIcon.UPDATE,
            "自动更新",
            "在应用启动时自动检查更新（建议开启）",
            cfg.checkUpdate,
            self.updateSoftwareGroup
        )

        self.aboutGroup = SettingCardGroup("关于", self.container_widget)
        self.helpCard = HyperlinkCard(
            "",
            "打开帮助页面",
            FluentIcon.HELP,
            "帮助",
            "发现新功能以及了解chat secretary的使用技巧",
            self.aboutGroup
        )
        self.feedbackCard = PrimaryPushSettingCard(
            "提供反馈",
            FluentIcon.FEEDBACK,
            "提交反馈",
            "提交使用体验或者bug以帮助chat secretary变得更好",
            self.aboutGroup
        )
        self.aboutCard = PrimaryPushSettingCard(
            "检查更新",
            FluentIcon.INFO,
            "关于",
            f"© Copyright {YEAR}, {AUTHOR}. Version {VERSION}",
            self.aboutGroup
        )

        self.__init_widgets()
        self.__init_layout()
        self.__init_signal_connection()

    def __init_widgets(self):
        self.setObjectName('SettingInterface')
        self.container_widget.setObjectName("ScrollWidget")
        self.__OnThemeChanged(Theme.AUTO)

        self.listenObjectGroup.addSettingCard(self.changeObjectCard)
        self.listenObjectGroup.addSettingCard(self.getChatRecordCard)

        self.personalSettingGroup.addSettingCard(self.micaSettingCard)
        self.personalSettingGroup.addSettingCard(self.themeSettingCard)
        self.personalSettingGroup.addSettingCard(self.themeColorSettingCard)

        self.updateSoftwareGroup.addSettingCard(self.updateSoftwareCard)

        self.aboutGroup.addSettingCard(self.helpCard)
        self.aboutGroup.addSettingCard(self.feedbackCard)
        self.aboutGroup.addSettingCard(self.aboutCard)

    def __init_layout(self):
        self.setWidget(self.container_widget)
        self.setWidgetResizable(True)

        self.layout.setSpacing(28)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(30, 10, 30, 0)
        self.layout.addWidget(self.listenObjectGroup)
        self.layout.addWidget(self.personalSettingGroup)
        self.layout.addWidget(self.updateSoftwareGroup)
        self.layout.addWidget(self.aboutGroup)

    def __init_signal_connection(self):
        self.changeObjectCard.clicked.connect(self.change_chat)
        self.getChatRecordCard.clicked.connect(self.get_message)
        self.themeSettingCard.optionChanged.connect(lambda c: setTheme(cfg.get(c)))
        self.themeSettingCard.optionChanged.connect(self.__OnThemeChanged)
        self.themeColorSettingCard.colorChanged.connect(lambda c: setThemeColor(c))
        self.micaSettingCard.checkedChanged.connect(signalBus.onMicaChanged)

    def change_chat(self):
        self.chat_name = self.hacker.get_current_dialog_name()
        self.changeObjectCard.setTitle("当前的聊天对象为：" + self.chat_name)

    def get_message(self):
        self.getChatRecordCard.start_progress()
        self.hacker.get_all_current_message()
        self.getChatRecordCard.stop_progress()
        print("get success")
        print(self.hacker.get_all_current_message(cache=True))

    def __OnThemeChanged(self, c):
        self.setStyleSheet("""
            QLabel#settingLabel {
                background-color: transparent;
            }
            SettingInterface, #ScrollWidget {
                background-color: transparent;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            """)
