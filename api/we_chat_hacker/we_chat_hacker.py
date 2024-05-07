"""
Author: GentleCold@qq.com
Reference: https://github.com/LTEnjoy/easyChat/blob/main/ui_auto_wechat.py
Version: 1.0.1
"""
from typing import List

import keyboard
import uiautomation as uia
from enum import Enum
import jieba
from common.utils import get_stopwords, is_today


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


class WeChatHacker:
    """
    Used for WeChat manipulation
    """
    msgs_time = {}
    msgs_cache = []
    # 分词后的记录
    word_cache = {}
    # 分词记录（区分人）
    word_person = {}
    # 发言数量记录（每个人发了多少条消息）
    speaker_msg_count = {}
    cached = False
    interactive_count = {}
    today_interactive_count = {}
    topic_started_num = {}

    def __init__(self):
        uia.SetGlobalSearchTimeout(0.1)
        self._we_chat_window = None
        self.user_name = None

        self.if_pressed = False
        keyboard.add_hotkey('ctrl+alt', self._hotkey_handler)

    @staticmethod
    def analyse_message():
        stopwords = get_stopwords("./resource/stopwords/stopwords.txt")
        WeChatHacker.speaker_msg_count.clear()
        WeChatHacker.word_cache.clear()
        WeChatHacker.msgs_time.clear()
        WeChatHacker.interactive_count.clear()
        WeChatHacker.topic_started_num.clear()
        WeChatHacker.word_person.clear()
        # 初始化msgs_time['self']
        WeChatHacker.msgs_time['self'] = []
        for i in range(12):
            WeChatHacker.msgs_time['self'].append(0)
        # 初始化interactive_count['self']
        WeChatHacker.interactive_count['self'] = {}
        WeChatHacker.today_interactive_count['self'] = {}

        if not WeChatHacker.cached:
            return
        else:
            is_first_msg = False
            time = ''
            hour = ''
            # 互动集合（这段时间内这个集合内的人在互动）
            temp_self_interactive_set = set([])
            for m in WeChatHacker.msgs_cache:
                if m['type'] == MessageType.USER_MESSAGE:
                    # 初始化人，如果该发言者没有在统计量中，则初始化他
                    if m['sender'] not in WeChatHacker.word_person:
                        WeChatHacker.word_person[m['sender']] = {}

                    # 记录话题发起统计量
                    if is_first_msg:
                        is_first_msg = False
                        if m['sender'] in WeChatHacker.topic_started_num:
                            WeChatHacker.topic_started_num[m['sender']] += 1
                        else:
                            WeChatHacker.topic_started_num[m['sender']] = 1

                    if m['sender'] in WeChatHacker.speaker_msg_count:
                        WeChatHacker.speaker_msg_count[m['sender']] += 1
                    else:
                        WeChatHacker.speaker_msg_count[m['sender']] = 1

                    words = jieba.cut(m['msg'])
                    for word in words:
                        word = word.strip()
                        if word and word not in stopwords:
                            if word in WeChatHacker.word_cache:
                                WeChatHacker.word_cache[word] += 1
                            else:
                                WeChatHacker.word_cache[word] = 1
                            # 记录每个人的话题记录统计量
                            if word in WeChatHacker.word_person[m['sender']]:
                                WeChatHacker.word_person[m['sender']][word] += 1
                            else:
                                WeChatHacker.word_person[m['sender']][word] = 1

                    if m['sender'] in WeChatHacker.msgs_time:
                        temp_hour = int(hour)+1
                        if temp_hour == 24:
                            temp_hour = 0
                        WeChatHacker.msgs_time[m['sender']][int(temp_hour/2)] += 1
                    temp_self_interactive_set.add(m['sender'])

                if m['type'] == MessageType.TIME:
                    # 每次时间改变，都要将is_first_msg设置成True，为了记录话题发起者统计量
                    is_first_msg = True
                    # 每次时间改变，都要更新一次互动集合
                    for key in WeChatHacker.interactive_count.keys():
                        if key in temp_self_interactive_set:
                            for person in temp_self_interactive_set:
                                if person != key:
                                    if person in WeChatHacker.interactive_count[key]:
                                        WeChatHacker.interactive_count[key][person] += 1
                                    else:
                                        WeChatHacker.interactive_count[key][person] = 1
                                    # 如果时间是今天，那么也需要单独更新今天互动的统计量
                                    if is_today(time):
                                        if person in WeChatHacker.today_interactive_count[key]:
                                            WeChatHacker.today_interactive_count[key][person] += 1
                                        else:
                                            WeChatHacker.today_interactive_count[key][person] = 1

                    temp_self_interactive_set.clear()

                    time = m['msg']
                    first_index = time.find(' ')
                    if first_index == -1:
                        first_index = 0
                    else:
                        first_index += 1
                    hour = time[first_index:time.find(':')]

    @staticmethod
    def get_word_person():
        return WeChatHacker.word_person

    @staticmethod
    def get_topic_started_num():
        return WeChatHacker.topic_started_num

    @staticmethod
    def get_interactive_count():
        return WeChatHacker.interactive_count

    @staticmethod
    def get_today_interactive_count():
        return WeChatHacker.today_interactive_count

    @staticmethod
    def get_msg_time():
        return WeChatHacker.msgs_time

    @staticmethod
    def get_word_cache():
        return WeChatHacker.word_cache

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
    print(we.get_all_current_message())
    # print(we.get_current_dialog_name())
