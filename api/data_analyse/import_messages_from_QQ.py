import jieba.posseg as pseg
import pandas as pd
import re
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']


class QQGroupMessage:
    def __init__(self, file_path) -> None:
        self.messageDF = pd.DataFrame([], columns=['idx', 'name', 'number', 'text', 'date', 'time'])
        # 读取数据
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            now_read = 8
            # idx = 0
            number_list = []
            while now_read < len(lines):
                # 正则表达式匹配
                delete_patterns = [r'(\[.*?\])', r'(@.*? )']
                pattern = r'(.*?-.*?-.*?)\s(.*?:.*?:.*?)\s(.*?)(\(.*?\)|<.*?>)'
                match = re.search(pattern, lines[now_read].strip())
                date = match.group(1)
                time = match.group(2)
                name = match.group(3)
                number = match.group(4)[1:-1]
                if number in number_list:
                    idx = number_list.index(number)
                else:
                    idx = len(number_list)
                    number_list.append(number)
                now_read += 1
                message = ""
                while lines[now_read].strip() != "":
                    line = lines[now_read].strip()
                    for pattern in delete_patterns:
                        matches = re.findall(pattern, line)
                        for match in matches:
                            match = match.strip()
                            line = line.replace(match, " ").strip()
                    message += line + " "
                    now_read += 1
                while lines[now_read].strip() == "":
                    now_read += 1
                    if now_read >= len(lines):
                        break
                message = message.strip()
                if message != "":
                    self.messageDF.loc[len(self.messageDF)] = [idx, name, number, message, date, time]

    def get_messagesDF(self):
        return self.messageDF
