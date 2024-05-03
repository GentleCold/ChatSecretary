from PySide6.QtWidgets import QFrame
from api.we_chat_hacker.we_chat_hacker import WeChatHacker


class VisualDashboardInterface(QFrame):
    def __init__(self, parent=None):
        super(VisualDashboardInterface, self).__init__(parent)
        self.setObjectName("VisualDashboard_Interface")


        # hacker = WeChatHacker()
        # hacker.check_if_login_wechat()

        # self.msg = hacker.get_all_current_message(cache=True)
        # print(self.msg)

