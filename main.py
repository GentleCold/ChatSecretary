import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from qfluentwidgets import MessageBox

from view.main_window import MainWindow
from api.we_chat_hacker.we_chat_hacker import WeChatHacker


class MainProcess:
    """
    Main process of the app
    """

    def __init__(self):
        # create application
        self.app = QApplication(sys.argv)
        self.app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

        # create main window
        self.main_window = MainWindow()

        self._check_if_login_we_chat()

    def _check_if_login_we_chat(self):
        # check the login of the WeChat
        we_chat_hacker = WeChatHacker()
        username = we_chat_hacker.check_if_login_wechat()
        while username == '':
            title = '登录微信'
            content = '您需要登录并保持微信窗口才能使用小蜜哦~'
            m = MessageBox(title, content, self.main_window.home_interface.window())
            m.yesButton.setText('重试')
            m.cancelButton.setText('退出')
            self.main_window.show()
            if m.exec():
                username = we_chat_hacker.check_if_login_wechat()
            else:
                sys.exit()

        # set username
        self.main_window.show()
        self.main_window.home_interface.show_user_name(username)

    def start(self):
        """
        After start the process will enter the loop of QT, nothing will do after start unless app exit
        :return:
        """
        self.app.exec()


if __name__ == '__main__':
    main = MainProcess()
    main.start()
    # Do not write things after this!
