from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
import pandas as pd
from collections import Counter
# tamamlanmamis durumda
class VisualizationTab(QWidget):
    def __init__(self):
        super().__init__()
        self.data = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(["Kelime Sıklığı", "Günlük Tweet Sayısı"])
        layout.addWidget(self.chart_type_combo)

        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        layout.addWidget(self.chart_view)

        self.update_button = QPushButton("Grafiği Güncelle")
        self.update_button.clicked.connect(self.update_chart)
        layout.addWidget(self.update_button)

        self.setLayout(layout)

    def update_data(self, new_data):
        self.data = new_data
        self.update_chart()

    def update_chart(self):
        if not self.data:
            return

        chart_type = self.chart_type_combo.currentText()
        
        if chart_type == "Kelime Sıklığı":
            self.show_word_frequency_chart()
        elif chart_type == "Günlük Tweet Sayısı":
            self.show_daily_tweet_count_chart()

    def show_word_frequency_chart(self):
        all_text = " ".join([tweet[2] for tweet in self.data])
        
        word_counts = Counter(all_text.split())
        
        top_words = dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10])

        series = QBarSeries()
        bar_set = QBarSet("Kelime Sıklığı")

        for count in top_words.values():
            bar_set.append(count)

        series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("En Sık Kullanılan 10 Kelime")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        axis_x = QBarCategoryAxis()
        axis_x.append(list(top_words.keys()))
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.chart_view.setChart(chart)

    def show_daily_tweet_count_chart(self):
        df = pd.DataFrame(self.data, columns=['date', 'id', 'text', 'username'])
        df['date'] = pd.to_datetime(df['date']).dt.date
        daily_counts = df.groupby('date').size().sort_index()

        series = QBarSeries()
        bar_set = QBarSet("Günlük Tweet Sayısı")

        for count in daily_counts.values:
            bar_set.append(count)

        series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Günlük Tweet Sayısı")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        axis_x = QBarCategoryAxis()
        axis_x.append([str(date) for date in daily_counts.index])
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.chart_view.setChart(chart)