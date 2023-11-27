from PySide6.QtCore import Qt, QEasingCurve, QRectF, QLineF, QPointF, QPropertyAnimation, QParallelAnimationGroup, \
    QTimer, QThread, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QHBoxLayout, QFrame, QWidget, QVBoxLayout, QListWidgetItem, QListWidget, QLineEdit, \
    QPushButton, QSizePolicy, QGraphicsObject, QGraphicsItem, QStyleOptionGraphicsItem, QGraphicsView, QGraphicsScene, \
    QComboBox, QFileDialog, QLabel, QDockWidget, QGraphicsDropShadowEffect
from qfluentwidgets import SmoothScrollArea, SubtitleLabel, StrongBodyLabel, BodyLabel, ComboBox, PushButton, \
    ImageLabel, IndeterminateProgressRing
from PySide6 import QtCharts
from api.data_analyse.import_messages_from_QQ import QQGroupMessage
from api.data_analyse.msg_processor import MsgProcessor
import matplotlib.pyplot as plt
import matplotlib.colors as mc


class TimeGraphInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.wordcloud_img = None
        self.wordcloud_label = None
        self.mp = None
        self.months = None
        self.setObjectName('timegraph_interface')
        self.comboBox = ComboBox()

        self.h_box_layout = QHBoxLayout(self)

        self.v_box_layout1 = QVBoxLayout()
        self.wordcloud_layout = QVBoxLayout()
        self.wordcloud_layout.addStretch(1)
        self.v_box_layout2 = QVBoxLayout()
        self.v_box_layout1.addWidget(self.comboBox)
        self.v_box_layout1.addLayout(self.wordcloud_layout)
        self.h_box_layout.addLayout(self.v_box_layout1)
        self.h_box_layout.addLayout(self.v_box_layout2)

        self.day_chart_view = QtCharts.QChartView()
        self.time_chart_view = QtCharts.QChartView()

        self.v_box_layout2.addWidget(self.day_chart_view)
        self.v_box_layout2.addWidget(self.time_chart_view)

        self.day_chart_view.hide()
        self.time_chart_view.hide()

        self.view = None
        self.import_msg_btn = PushButton('导入QQ聊天记录', self)
        self.import_msg_btn.clicked.connect(self.open_file)
        self.h_box_layout.addWidget(self.import_msg_btn)

        self.comboBox.hide()

    def month_changed(self, month):
        # draw word cloud
        self.wordcloud_layout.removeWidget(self.wordcloud_img)

        img_path = f'./resource/images/wordclouds/{month}-wordcloud.png'
        self.wordcloud_img = ImageLabel(img_path, self)

        self.wordcloud_label.show()
        self.wordcloud_layout.addWidget(self.wordcloud_img)

        # draw month activity trend and day activity trend
        month_trend = self.mp.month_activity_trend[month]
        day_trend = self.mp.day_activity_trend[month]

        month_series = QtCharts.QLineSeries()
        month_trend = dict(sorted(month_trend.items(), key=lambda x: x[0]))
        for key, value in month_trend.items():
            month_series.append(float(key), float(value))
        day_series = QtCharts.QLineSeries()
        day_trend = dict(sorted(day_trend.items(), key=lambda x: x[0]))
        for key, value in day_trend.items():
            day_series.append(float(key), float(value))

        month_chart = QtCharts.QChart()
        month_chart.addSeries(month_series)
        day_chart = QtCharts.QChart()
        day_chart.addSeries(day_series)

        month_axis_x = QtCharts.QValueAxis()
        month_axis_x.setTickCount(int(len(month_trend) / 2))
        month_axis_x.setLabelFormat("%i")
        month_axis_x.setTitleText("日期")
        month_chart.addAxis(month_axis_x, Qt.AlignBottom)
        month_series.attachAxis(month_axis_x)

        month_axis_y = QtCharts.QValueAxis()
        month_axis_y.setTickCount(5)
        month_axis_y.setLabelFormat("%g")
        month_axis_y.setTitleText("活跃度")
        month_chart.addAxis(month_axis_y, Qt.AlignLeft)
        month_series.attachAxis(month_axis_y)

        month_chart.legend().setVisible(False)
        month_chart.setTitle("每日活跃度")

        day_axis_x = QtCharts.QValueAxis()
        day_axis_x.setTickCount(int(len(day_trend) / 2))
        day_axis_x.setLabelFormat("%i")
        day_axis_x.setTitleText("时间")
        day_chart.addAxis(day_axis_x, Qt.AlignBottom)
        day_series.attachAxis(day_axis_x)

        day_axis_y = QtCharts.QValueAxis()
        day_axis_y.setTickCount(5)
        day_axis_y.setLabelFormat("%g")
        day_axis_y.setTitleText("活跃度")
        day_chart.addAxis(day_axis_y, Qt.AlignLeft)
        day_series.attachAxis(day_axis_y)

        day_chart.legend().setVisible(False)
        day_chart.setTitle("活跃时间段")

        self.day_chart_view.setChart(month_chart)
        self.time_chart_view.setChart(day_chart)
        self.day_chart_view.show()
        self.time_chart_view.show()

    def open_file(self):
        self.h_box_layout.removeWidget(self.import_msg_btn)
        self.import_msg_btn.hide()
        self.ring = IndeterminateProgressRing(self)

        self.h_box_layout.addWidget(self.ring, alignment=Qt.AlignCenter)

        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "打开文件", "", "文本文件 (*.txt);;所有文件 (*)",
                                                   options=options)

        self.draw_thread = DrawWordcloudThread(file_path)
        self.draw_thread.finished.connect(self.draw_wordcloud_finished)

        self.draw_thread.start()

    def draw_wordcloud_finished(self, result):
        self.months, self.mp = result

        self.h_box_layout.removeWidget(self.ring)
        self.ring.deleteLater()

        self.comboBox.setPlaceholderText("选择月份")

        self.comboBox.addItems(self.months)
        self.comboBox.setCurrentIndex(-1)

        self.wordcloud_label = SubtitleLabel()
        self.wordcloud_label.setText('本月词云')
        self.wordcloud_label.hide()
        self.wordcloud_layout.addWidget(self.wordcloud_label)
        self.comboBox.show()

        self.comboBox.currentTextChanged.connect(self.month_changed)


class DrawWordcloudThread(QThread):
    finished = Signal(list)

    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path

    def run(self):
        # 在这里执行 draw_wordcloud() 方法
        QQ = QQGroupMessage(self.file_path)
        msgDF = QQ.get_messagesDF()
        self.mp = MsgProcessor()
        self.mp.init_from_pd(msgDF)
        months = self.mp.draw_wordcloud()
        self.finished.emit((months,self.mp))

