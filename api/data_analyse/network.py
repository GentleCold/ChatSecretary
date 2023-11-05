import jieba.posseg as pseg
import pandas as pd
import re
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']


class QQGroupMessage:
    def __init__(self) -> None:
        self.messageDF = pd.DataFrame([], columns=['name', 'number', 'text', 'date', 'time'])
        # 读取数据
        with open("QQ1.txt", 'r') as f:
            lines = f.readlines()
            now_read = 8
            while now_read < len(lines):
                # 正则表达式匹配
                delete_patterns = [r'(\[.*?\])', r'(@.*? )']
                pattern = r'(.*?-.*?-.*?)\s(.*?:.*?:.*?)\s(.*?)(\(.*?\)|<.*?>)'
                match = re.search(pattern, lines[now_read].strip())
                date = match.group(1)
                time = match.group(2)
                name = match.group(3)
                number = match.group(4)[1:-1]
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
                    self.messageDF.loc[len(self.messageDF)] = [name, number, message, date, time]
        self.most_common_word = pd.DataFrame([], columns=['number', 'words'])
        for number in self.messageDF['number'].value_counts().index:
            most_common = self.most_common(number)
            self.most_common_word.loc[len(self.most_common_word)] = [number, most_common]
        self.word_node_color = ['#095dbe', '#5a9eed', '#7face1', '#e1e8ef']
        self.person_node_color = ["#ede85a"]
    def most_common(self, number):
        """找出频率最多的词"""
        target_rows = self.messageDF[self.messageDF['number'] == number]
        seg_list = []
        for txt in target_rows['text']:
            words = pseg.cut(txt)
            for word, flag in words:
                if flag in ("n", "nr", "ns", "nt", "nw", "nz"):
                    seg_list.append(word)
        c = Counter()
        for x in seg_list:
            c[x] += 1    
        return c.most_common(300)
    def draw_network(self, row_idxes):
        """画图"""
        G = nx.Graph()
        edge_list = []
        # 节点列表（一个名词或一个人是一个节点）
        node_list = []
        # 节点颜色列表（一个节点对应一个颜色，所以node_list和node_color_list的len是一样的）
        node_color_list = []
        # row_indexes是一个列表，传入的是画谁的图，[1,2]就是画发言数量前两名的图
        for idx in row_idxes:
            # 获取发言词列表
            row = self.most_common_word.iloc[idx]
            # 放入用户节点
            G.add_node(row[0])
            node_list.append(row[0])
            node_color_list.append(self.person_node_color[0])
            # 放入词节点
            for i, word_frequency in enumerate(row[1][:60]):
                if word_frequency[0] not in node_list:
                    # 放入不同的颜色以区分多频，少频词
                    node_color_list.append(self.word_node_color[int(i/15)])
                    G.add_node(word_frequency[0])
                    node_list.append(word_frequency[0])
                G.add_edge(row[0], word_frequency[0])
        pos = nx.fruchterman_reingold_layout(G)
        nx.draw_networkx_nodes(G, pos,node_size=280, node_color = node_color_list)
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_labels(G, pos, font_size=6)
        plt.show()
        # plt.savefig("fig1.png")
        

QQmsg = QQGroupMessage()