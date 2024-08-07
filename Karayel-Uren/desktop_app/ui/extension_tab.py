from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog
from PyQt6.QtCore import QTimer
import requests

class ExtensionTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.refresh_button = QPushButton("Verileri Güncelle")
        self.refresh_button.clicked.connect(self.update_data)
        layout.addWidget(self.refresh_button)

        self.save_button = QPushButton("Verileri Kaydet")
        self.save_button.clicked.connect(self.save_data)
        layout.addWidget(self.save_button)

        self.result_table = QTableWidget(0, 1)
        self.result_table.setHorizontalHeaderLabels(["Tweet Metni"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.result_table)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(60000)

    def update_data(self):
        try:
            response = requests.get('http://127.0.0.1:5000/get_tweets')
            response.raise_for_status()
            tweets = response.json().get('tweets', [])
            print("Fetched tweets from server:", tweets)
            self.result_table.setRowCount(len(tweets))
            for i, tweet in enumerate(tweets):
                self.result_table.setItem(i, 0, QTableWidgetItem(tweet))
        except requests.RequestException as e:
            print(f"Error fetching tweets: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def save_data(self):
        try:
            path, _ = QFileDialog.getSaveFileName(self, "Verileri Kaydet", "", "CSV Files (*.csv);;All Files (*)")
            if path:
                with open(path, 'w', encoding='utf-8') as file:
                    for row in range(self.result_table.rowCount()):
                        tweet = self.result_table.item(row, 0).text()
                        file.write(f'"{tweet}"\n')
                print(f"Veriler {path} dosyasına kaydedildi.")
        except Exception as e:
            print(f"Error saving tweets: {e}")
