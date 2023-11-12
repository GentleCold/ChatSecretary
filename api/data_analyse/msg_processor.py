import math

import jieba.posseg as pseg
import pandas as pd
import numpy as np
import re
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
from PySide6.QtCore import QRectF, Qt, QLineF, QPointF, QParallelAnimationGroup, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QPolygonF, QCursor
from PySide6.QtWidgets import QGraphicsObject, QGraphicsItem, QStyleOptionGraphicsItem, QWidget, QGraphicsView, \
    QGraphicsScene, QGraphicsDropShadowEffect
# from view.graph_interface import DisplayInfoWidget
from gensim.corpora import Dictionary
from gensim.models import LdaModel, LdaMulticore
import logging
# import pyLDAvis.gensim
import itertools


class MsgProcessor:
    """
    handle msg
    """
    def __init__(self):
        pass
        self._messageDF = pd.DataFrame()
        self.word_node_color = ['#095dbe', '#5a9eed', '#7face1', '#e1e8ef']
        self.person_node_color = ["#ede85a"]
        self.person2word_edge_color = "#1a4157"
        self.word2word_edge_color = "#55A7D5"

    def lda_analyse(self, idx):
        corpus = self.get_line_cut(idx)
        dictionary = Dictionary(self.get_line_cut(idx))
        corpus_bow = [dictionary.doc2bow(doc) for doc in corpus]
        temp = dictionary[0]
        id2word = dictionary.id2token
        model = LdaModel(
            corpus=corpus_bow,
            id2word=id2word,
            chunksize=2000,
            alpha='auto',
            eta='auto',
            # iterations=400,
            num_topics=10,
            # passes=20,
            eval_every=None
        )
        topic_word_dist = model.get_topics()
        N = 2
        topics_list = []
        for topic_id, dist in enumerate(topic_word_dist):
            # print("Topic {}:".format(topic_id + 1))
            topics_list.append([word for word, prob in model.show_topic(topic_id, topn=N)])
        # print(topics_list)
        return topics_list

    def init_from_pd(self, messageDF):
        """
        get mang msgs with pd
        """
        self._messageDF = messageDF
        # self.get_line_cut(0)

    def get_most_common(self, idx, count=60):
        """
        get most common words for a QQ_number
        """
        line_cut = self.get_line_cut(idx)
        c = Counter()
        for words in line_cut:
            for word in words:
                c[word] += 1
        return c.most_common(count)

    def get_line_cut(self, idx):
        """
        get lint cut for every row
        """
        target_rows = self._messageDF[self._messageDF['idx'] == idx]
        cut_list = []
        for i, txt in enumerate(target_rows['text']):
            words = pseg.cut(txt)
            cuts = []
            for word, flag in words:
                if flag in ("n", "nr", "ns", "nt", "nw", "nz"):
                    cuts.append(word)
            if cuts:
                cut_list.append(cuts)
        return cut_list

    def get_name_with_idx(self, idx):
        result = self._messageDF.query(f"idx == {idx}")
        if len(result) == 0:
            return None
        else:
            return result['name'].values[0]

    def draw_network(self, idxes, father_widget, display_widget, lda_flag, word_count=30):
        """
        Args:
            lda_flag: 是否展示lda结果
        """

        G = nx.Graph()
        edge_color_dict = {}
        edge_list = []
        # 节点列表（一个名词或一个人是一个节点）
        node_list = []
        # 节点颜色列表（一个节点对应一个颜色，所以node_list和node_color_list的len是一样的）
        node_color_list = []
        # row_indexes是一个列表，传入的是画谁的图，[1,2]就是画发言数量前两名的图
        for idx in idxes:
            # 每个人的node_list，最后再合并到总node_list中
            personal_node_list = []
            # name = self.get_name_with_idx(idx)
            name = str(idx)
            words = self.get_most_common(idx, count=word_count)
            # print(words)
            # 放入用户节点
            G.add_node(name)
            node_list.append(name)
            node_color_list.append(self.person_node_color[0])
            # 放入词节点
            for i, word in enumerate(words):
                if word[0] not in node_list:
                    # 放入不同的颜色以区分多频，少频词
                    node_color_list.append(self.word_node_color[int(i / (word_count/4))])
                    G.add_node(word[0])
                    personal_node_list.append(word[0])
                    # node_list.append(word[0])
                G.add_edge(name, word[0])
                edge_list.append((name, word[0]))
                # print(name, word[0], 0)
                edge_color_dict[(name, word[0])] = self.person2word_edge_color
                # edge_color_list.append(self.person2word_edge_color)
            if lda_flag:
                lda_result = self.lda_analyse(idx)
                for topic in lda_result:
                    word_exist_list = []
                    for word in topic:
                        if word in personal_node_list:
                            word_exist_list.append(word)
                    if len(word_exist_list) >= 2:
                        pairs = list(itertools.combinations(word_exist_list, 2))
                        for pair in pairs:
                            G.add_edge(pair[0], pair[1])
                            edge_list.append((pair[0], pair[1]))
                            # print(pair[0], pair[1], 1)
                            edge_color_dict[(pair[0], pair[1])] = self.word2word_edge_color
                            # edge_color_list.append(self.word2word_edge_color)
            node_list.extend(personal_node_list)
        return GraphView(G, node_color_list, edge_color_dict, father_widget, display_widget)


class Node(QGraphicsObject):
    """A QGraphicsItem representing node in a graph"""

    def __init__(self, name: str, color, father_widget: QWidget, display_widget: QWidget, parent=None):
        """Node constructor
        Args:
            name (str): Node label
            display_widget: display (node) info widget
        """
        super().__init__(parent)
        self.setAcceptHoverEvents(True)
        self.father_widget = father_widget
        self._name = name
        self._edges = []
        self._color = QColor(color)
        self._color.setAlpha(230)
        self._radius = 25
        self._rect = QRectF(0, 0, self._radius * 2, self._radius * 2)

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)

        self.display_widget = display_widget
        self.display_widget.raise_()

    def hoverEnterEvent(self, event):
        self._color.setAlpha(255)
        # set shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(0, 0)
        shadow.setBlurRadius(50)
        shadow.setColor("#808080")
        self.setGraphicsEffect(shadow)
        pos = QCursor.pos()
        pos = self.father_widget.mapFromGlobal(pos)
        pos.setX(pos.x() + 20)
        pos.setY(pos.y() - 20)
        self.display_widget.move(pos)
        self.display_widget.set_text(self._name)
        # self.display_widget.show()
        self.update()

    def hoverLeaveEvent(self, event):
        self._color.setAlpha(230)
        self.setGraphicsEffect(None)
        self.display_widget.hide()
        self.update()

    def boundingRect(self) -> QRectF:
        """Override from QGraphicsItem

        Returns:
            QRect: Return node bounding rect
        """
        return self._rect

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        """Override from QGraphicsItem

        Draw node

        Args:
            painter (QPainter)
            option (QStyleOptionGraphicsItem)
        """
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(
            QPen(
                self._color,
                2,
                Qt.SolidLine,
                Qt.RoundCap,
                Qt.RoundJoin,
            )
        )
        painter.setBrush(QBrush(self._color))
        painter.drawEllipse(self.boundingRect())
        painter.setPen(QPen(QColor("1E1F22")))
        painter.drawText(self.boundingRect(), Qt.AlignCenter, self._name)

    def add_edge(self, edge):
        """Add an edge to this node

        Args:
            edge (Edge)
        """
        self._edges.append(edge)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value):
        """Override from QGraphicsItem

        Args:
            change (QGraphicsItem.GraphicsItemChange)
            value (Any)

        Returns:
            Any
        """
        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in self._edges:
                edge.adjust()

        return super().itemChange(change, value)


class Edge(QGraphicsItem):
    def __init__(self, source: Node, dest: Node, color, parent: QGraphicsItem = None):
        """Edge constructor

        Args:
            source (Node): source node
            dest (Node): destination node
        """
        super().__init__(parent)
        self._source = source
        self._dest = dest

        self._tickness = 2
        # self._color = color
        self._color = QColor(color)
        self._arrow_size = 20

        self._source.add_edge(self)
        self._dest.add_edge(self)

        self._line = QLineF()
        self.setZValue(-1)
        self.adjust()

    def boundingRect(self) -> QRectF:
        """Override from QGraphicsItem

        Returns:
            QRect: Return node bounding rect
        """
        return (
            QRectF(self._line.p1(), self._line.p2())
            .normalized()
            .adjusted(
                -self._tickness - self._arrow_size,
                -self._tickness - self._arrow_size,
                self._tickness + self._arrow_size,
                self._tickness + self._arrow_size,
            )
        )

    def adjust(self):
        """
        Update edge position from source and destination node.
        This method is called from Node::itemChange
        """
        self.prepareGeometryChange()
        self._line = QLineF(
            self._source.pos() + self._source.boundingRect().center(),
            self._dest.pos() + self._dest.boundingRect().center(),
        )

    def _draw_arrow(self, painter: QPainter, start: QPointF, end: QPointF):
        """Draw arrow from start point to end point.

        Args:
            painter (QPainter)
            start (QPointF): start position
            end (QPointF): end position
        """
        painter.setBrush(QBrush(self._color))

        line = QLineF(end, start)

        angle = math.atan2(-line.dy(), line.dx())
        arrow_p1 = line.p1() + QPointF(
            math.sin(angle + math.pi / 3) * self._arrow_size,
            math.cos(angle + math.pi / 3) * self._arrow_size,
        )
        arrow_p2 = line.p1() + QPointF(
            math.sin(angle + math.pi - math.pi / 3) * self._arrow_size,
            math.cos(angle + math.pi - math.pi / 3) * self._arrow_size,
        )

        arrow_head = QPolygonF()
        arrow_head.clear()
        arrow_head.append(line.p1())
        arrow_head.append(arrow_p1)
        arrow_head.append(arrow_p2)
        painter.drawLine(line)
        painter.drawPolygon(arrow_head)

    def _arrow_target(self) -> QPointF:
        """Calculate the position of the arrow taking into account the size of the destination node

        Returns:
            QPointF
        """
        target = self._line.p1()
        center = self._line.p2()
        radius = self._dest._radius
        vector = target - center
        length = math.sqrt(vector.x() ** 2 + vector.y() ** 2)
        if length == 0:
            return target
        normal = vector / length
        target = QPointF(center.x() + (normal.x() * radius), center.y() + (normal.y() * radius))

        return target

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget=None):
        """Override from QGraphicsItem

        Draw Edge. This method is called from Edge.adjust()

        Args:
            painter (QPainter)
            option (QStyleOptionGraphicsItem)
        """

        if self._source and self._dest:
            painter.setRenderHints(QPainter.Antialiasing)

            painter.setPen(
                QPen(
                    self._color,
                    self._tickness,
                    Qt.SolidLine,
                    Qt.RoundCap,
                    Qt.RoundJoin,
                )
            )
            painter.drawLine(self._line)
            # self._draw_arrow(painter, self._line.p1(), self._arrow_target())
            # self._arrow_target()


class GraphView(QGraphicsView):
    def __init__(self, graph: nx.Graph, node_color_list, edge_color_dict, father_widget, display_widget, parent=None):
        """GraphView constructor

        This widget can display a directed graph

        Args:
            graph (nx.Graph): a networkx graph
            node_color_list : node color list, len(node_color_list) = len(node_list)
            display_widget: display info widget. Display when hover
        """
        super().__init__()
        self.display_widget = display_widget
        self.father_widget = father_widget
        self._graph = graph
        self._scene = QGraphicsScene()
        self.setScene(self._scene)

        self.node_color_list = node_color_list
        self.edge_color_dict = edge_color_dict

        # Used to add space between nodes
        self._graph_scale = 400

        # Map node name to Node object {str=>Node}
        self._nodes_map = {}

        # List of networkx layout function
        self._nx_layout = {
            "fruchterman_reingold_layout": nx.fruchterman_reingold_layout,
            "circular": nx.circular_layout,
            "planar": nx.planar_layout,
            "random": nx.random_layout,
            "shell_layout": nx.shell_layout,
            "spring_layout": nx.spring_layout,
            "spiral_layout": nx.spiral_layout,
        }

        self._load_graph()
        # self.set_nx_layout("fruchterman_reingold_layout")shell_layout
        self.set_nx_layout("fruchterman_reingold_layout")

        self.setStyleSheet('border: none;')

    def get_nx_layouts(self):
        """Return all layout names

        Returns:
            list: layout name (str)
        """
        return self._nx_layout.keys()

    def set_nx_layout(self, name: str):
        """Set networkx layout and start animation

        Args:
            name (str): Layout name
        """
        if name in self._nx_layout:
            self._nx_layout_function = self._nx_layout[name]

            # Compute node position from layout function
            positions = self._nx_layout_function(self._graph)

            # Change position of all nodes using an animation
            self.animations = QParallelAnimationGroup()
            for node, pos in positions.items():
                x, y = pos
                x *= self._graph_scale
                y *= self._graph_scale
                item: Node = self._nodes_map[node]

                animation = QPropertyAnimation(item, b"pos")
                animation.setDuration(1000)
                animation.setEndValue(QPointF(x, y))
                animation.setEasingCurve(QEasingCurve.OutExpo)
                self.animations.addAnimation(animation)

            self.animations.start()

    def _load_graph(self):
        """Load graph into QGraphicsScene using Node class and Edge class"""

        self.scene().clear()
        self._nodes_map.clear()

        # Add nodes
        for i, node in enumerate(self._graph):
            item = Node(node, self.node_color_list[i], self.father_widget, self.display_widget)
            self.scene().addItem(item)
            self._nodes_map[node] = item

        # Add edges
        for a, b in self._graph.edges:
            source = self._nodes_map[a]
            dest = self._nodes_map[b]
            try:
                color = self.edge_color_dict[(a, b)]
            except KeyError:
                color = self.edge_color_dict[(b, a)]
            self.scene().addItem(Edge(source, dest, color))
