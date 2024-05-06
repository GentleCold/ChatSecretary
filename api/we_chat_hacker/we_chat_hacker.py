"""
Author: GentleCold@qq.com
Reference: https://github.com/LTEnjoy/easyChat/blob/main/ui_auto_wechat.py
Version: 1.0.1
"""
import time
from typing import List
import pyperclip

import keyboard
import uiautomation as uia
from enum import Enum


class MessageType:
    TIME = 0  # 时间
    MORE_MESSAGE_FLAG = 1  # '查看更多消息'
    WITHDRAW = 2  # 撤回
    USER_MESSAGE = 3  # 消息文本('[文件]', '[图片]', '[视频]', '[音乐]', '[链接]', '[转账]')
    HONG_BAO = 4  # 红包
    OTHER = 5


class AutoUtils:
    """
    Help to operate the mouse
    """

    @staticmethod
    def move(element):
        x, y = element.GetPosition()
        uia.SetCursorPos(x, y)

    @staticmethod
    def click(element):
        x, y = element.GetPosition()
        uia.Click(x, y)

    @staticmethod
    def right_click(element):
        x, y = element.GetPosition()
        uia.RightClick(x, y)

    @staticmethod
    def double_click(element):
        x, y = element.GetPosition()
        uia.SetCursorPos(x, y)
        element.DoubleClick()


class MsgType(Enum):
    TIME = 0,
    SPEAK = 3


class WeChatHacker:
    """
    Used for WeChat manipulation
    """
    msgs_cache = []
    # 分词后的记录
    word_cache = {}
    # 发言数量记录（每个人发了多少条消息）
    speaker_msg_count = {}
    cached = False

    def __init__(self):
        uia.SetGlobalSearchTimeout(0.1)
        self._we_chat_window = None
        self.user_name = None

        self.if_pressed = False
        keyboard.add_hotkey('ctrl+alt', self._hotkey_handler)

    @staticmethod
    def analyse_message():
        WeChatHacker.speaker_msg_count.clear()
        if not WeChatHacker.cached:
            return
        else:
            for m in WeChatHacker.msgs_cache:
                if m['type'] == MsgType.SPEAK.value:
                    if m['sender'] in WeChatHacker.speaker_msg_count:
                        WeChatHacker.speaker_msg_count[m['sender']] += 1
                    else:
                        WeChatHacker.speaker_msg_count[m['sender']] = 1

    @staticmethod
    def get_speaker_msg_count():
        return WeChatHacker.speaker_msg_count

    @staticmethod
    def is_cached():
        """返回是否有缓存数据"""
        return WeChatHacker.cached

    def _hotkey_handler(self):
        self.if_pressed = True

    def check_if_login_wechat(self):
        """
        get we chat window and name of the user
        :return: name of the user, lookupError if ''
        """
        try:
            self._we_chat_window = uia.WindowControl(searchDepth=1, ClassName='WeChatMainWndForPC')
            self.user_name = self._we_chat_window.ToolBarControl(searchDepth=3, Name='导航').GetChildren()[0].Name
        except LookupError:
            return ''
        return self.user_name

    def get_all_current_message(self, cache=False) -> List:
        """
        Get all messages of the current dialog
        :param cache: if cache is true, then read from cache
        :return: list of message dictionary, len(return) == 0 means LookupError
        """
        if cache:
            return WeChatHacker.msgs_cache

        self._we_chat_window.Show(0)

        self.if_pressed = False
        try:
            messages_list_control = self._we_chat_window.ListControl(Name='消息')
            scroll_pattern = messages_list_control.GetScrollPattern()
        except LookupError:
            return []

        while True:
            if self.if_pressed:
                break

            # 上翻至查看聊天记录
            scroll_pattern.SetScrollPercent(-1, 0)

            # 判断是否为'查看更多消息'
            message_control = messages_list_control.GetFirstChildControl()
            if self._detect_type(message_control) != MessageType.MORE_MESSAGE_FLAG:
                break
            else:
                AutoUtils.click(message_control)

        messages = []
        for message_control in messages_list_control.GetChildren():
            v = self._detect_type(message_control)
            sender = ''
            if v == MessageType.USER_MESSAGE:
                sender = message_control.ButtonControl(searchDepth=2).Name

            if sender == self.check_if_login_wechat():
                sender = 'self'
            messages.append({
                'sender': sender,
                'msg': message_control.Name,
                'type': v
            })

        WeChatHacker.msgs_cache.clear()
        WeChatHacker.msgs_cache.extend(messages)
        WeChatHacker.cached = True
        return messages

    def get_current_dialog_name(self):
        """
        Gets the current chat window name
        :return: string
        """
        try:
            name = self._we_chat_window.PaneControl(foundIndex=1).PaneControl(foundIndex=1) \
                .PaneControl(searchDepth=1, foundIndex=2).TextControl().Name
        except LookupError:
            try:
                name = self._we_chat_window.PaneControl(foundIndex=2).PaneControl(foundIndex=1) \
                    .PaneControl(searchDepth=1, foundIndex=2).TextControl().Name
            except LookupError:
                return ''

            if '(' in name:
                rIndex = name.rindex("(")
                return name[:rIndex]
        return name

    def get_contact(self, name):
        search_box = uia.EditControl(Depth=8, Name="搜索")
        AutoUtils.click(search_box)

        pyperclip.copy(name)
        uia.SendKeys("{Ctrl}v")
        # 等待客户端搜索联系人
        time.sleep(0.1)
        search_box.SendKeys("{enter}")

    def send_msg(self, name, text):
        self.get_contact(name)
        pyperclip.copy(text)
        uia.SendKeys("{Ctrl}v")

        # 获取发送按钮
        send_button = uia.ButtonControl(Depth=15, Name="发送(S)")
        AutoUtils.click(send_button)

    @staticmethod
    def _detect_type(message_control):
        """
        Detect the type of message
        :param message_control: controller of message
        :return: MessageType
        """
        raw_message = message_control.Name
        # 如果是时间框则子控件不是PaneControl
        if not isinstance(message_control.GetFirstChildControl(), uia.PaneControl):
            return MessageType.TIME
        elif raw_message == '':
            return MessageType.OTHER
        else:
            # 具体控件树区分通过inspect.exe查看
            cnt = 0
            for child in message_control.PaneControl(searchDepth=1).GetChildren():
                cnt += len(child.GetChildren())

            if cnt > 0:
                return MessageType.USER_MESSAGE
            elif raw_message == '查看更多消息' or raw_message == '以下为新消息':
                return MessageType.MORE_MESSAGE_FLAG
            elif '红包' in raw_message:
                return MessageType.HONG_BAO
            elif "撤回了一条消息" in raw_message:
                return MessageType.WITHDRAW


if __name__ == '__main__':
    we = WeChatHacker()
    we.check_if_login_wechat()
    we.send_msg('李泽朋', '测试')
    # print(we.get_current_dialog_name())
