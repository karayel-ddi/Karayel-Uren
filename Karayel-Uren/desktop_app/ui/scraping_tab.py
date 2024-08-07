from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QMessageBox, QFileDialog, QProgressBar, QComboBox, QHeaderView, QAbstractItemView
from PyQt6.QtCore import pyqtSignal, QThread, pyqtSlot, Qt
from scraper.sikayetvar_scraper import SikayetvarScraper
from scraper.eksisozluk_scraper import EksiSozlukScraper 
import pandas as pd

class ScrapingWorker(QThread):
    progress = pyqtSignal(int)
    result = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, scraper, *args, **kwargs):
        super().__init__()
        self.scraper = scraper
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            for i, result in enumerate(self.scraper.scrape()):
                if not self.scraper.is_running:
                    break
                self.progress.emit(i + 1)
                self.result.emit(result)
        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        self.scraper.is_running = False

class ScrapingTab(QWidget):
    data_updated = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.worker = None

    def init_ui(self):
        layout = QVBoxLayout()

        self.scraper_selector = QComboBox()
        self.scraper_selector.addItems(["Şikayetvar", "Ekşi Sözlük"])
        self.scraper_selector.currentIndexChanged.connect(self.update_ui)
        layout.addWidget(self.scraper_selector)

        self.custom_layout = QVBoxLayout()
        layout.addLayout(self.custom_layout)

        button_layout = QHBoxLayout()
        self.search_button = QPushButton("Verileri çek")
        self.search_button.clicked.connect(self.start_scraping)
        self.stop_button = QPushButton("Durdur")
        self.stop_button.clicked.connect(self.stop_scraping)
        self.save_button = QPushButton("Kaydet")
        self.save_button.clicked.connect(self.save_results)
        self.load_button = QPushButton("Yükle")
        self.load_button.clicked.connect(self.load_results)
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.load_button)
        layout.addLayout(button_layout)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.result_table = QTableWidget(0, 2)
        self.result_table.setHorizontalHeaderLabels(["Metin", "İşlem"])
        self.result_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.result_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.result_table.setColumnWidth(1, 60)
        self.result_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.result_table.setShowGrid(True)
        self.result_table.setGridStyle(Qt.PenStyle.SolidLine)
        self.result_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #E0E0E0;
                border: none;
            }
            QTableWidget::item {
                border-bottom: 1px solid #E0E0E0;
            }
            QHeaderView::section {
                background-color: #F5F5F5;
                border: none;
                border-bottom: 1px solid #E0E0E0;
                padding: 5px;
            }
        """)
        self.result_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.result_table)

        self.setLayout(layout)
        self.update_ui()

    def update_ui(self):
        for i in reversed(range(self.custom_layout.count())):
            self.custom_layout.itemAt(i).widget().setParent(None)

        current_scraper = self.scraper_selector.currentText()
        if current_scraper == "Şikayetvar":
            self.setup_sikayetvar_ui()
        elif current_scraper == "Instagram":
            self.setup_instagram_ui()
        elif current_scraper == "Ekşi Sözlük":
            self.setup_eksi_ui()

    def setup_sikayetvar_ui(self):
        self.brand_input = QLineEdit()
        self.brand_input.setPlaceholderText("Marka (örn: turkcell-bulut)")
        self.custom_layout.addWidget(self.brand_input)

        self.start_page_input = QLineEdit()
        self.start_page_input.setPlaceholderText("Başlangıç Sayfası (örn: 1)")
        self.custom_layout.addWidget(self.start_page_input)

        self.end_page_input = QLineEdit()
        self.end_page_input.setPlaceholderText("Bitiş Sayfası (örn: 350)")
        self.custom_layout.addWidget(self.end_page_input)


    def setup_eksi_ui(self):
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("Konu (örn: python)")
        self.custom_layout.addWidget(self.topic_input)

        self.max_pages_input = QLineEdit()
        self.max_pages_input.setPlaceholderText("Maksimum Sayfa Sayısı (varsayılan: 220)")
        self.custom_layout.addWidget(self.max_pages_input)

    def start_scraping(self):
        current_scraper = self.scraper_selector.currentText()

        if current_scraper == "Şikayetvar":
            brand = self.brand_input.text()
            start_page = int(self.start_page_input.text() or 1) 
            end_page = int(self.end_page_input.text() or 350) 

            self.scraper = SikayetvarScraper(brand)
            self.scraper.start_page = start_page
            self.scraper.end_page = end_page

        elif current_scraper == "Ekşi Sözlük":
            topic = self.topic_input.text()
            max_pages = int(self.max_pages_input.text() or 220)
            self.scraper = EksiSozlukScraper(topic, max_pages)

        self.progress_bar.setMaximum(0)
        self.progress_bar.setValue(0)

        self.worker = ScrapingWorker(self.scraper)
        self.worker.progress.connect(self.update_progress)
        self.worker.result.connect(self.add_result)
        self.worker.error.connect(self.show_error)
        self.worker.start()

    def stop_scraping(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()

    @pyqtSlot(int)
    def update_progress(self, value):
        self.progress_bar.setMaximum(value + 1)
        self.progress_bar.setValue(value)

    @pyqtSlot(list)
    def add_result(self, result):
        row_position = self.result_table.rowCount()
        self.result_table.insertRow(row_position)
        self.result_table.setItem(row_position, 0, QTableWidgetItem(result[0]))
        
        delete_button = QPushButton("Sil")
        delete_button.clicked.connect(lambda: self.delete_row(row_position))
        self.result_table.setCellWidget(row_position, 1, delete_button)

    def delete_row(self, row):
        self.result_table.removeRow(row)

    @pyqtSlot(str)
    def show_error(self, error):
        QMessageBox.critical(self, "Hata", error)

    def save_results(self):
        path, _ = QFileDialog.getSaveFileName(self, "Kaydet", "", "CSV Files (*.csv);;All Files (*)")
        if path:
            data = []
            for row in range(self.result_table.rowCount()):
                text = self.result_table.item(row, 0).text()
                if text:
                    data.append([text])
            df = pd.DataFrame(data, columns=["Metin"])
            df.to_csv(path, index=False)


    def load_results(self):
        path, _ = QFileDialog.getOpenFileName(self, "Yükle", "", "CSV Files (*.csv);;All Files (*)")
        if path:
            df = pd.read_csv(path)
            self.result_table.setRowCount(0)
            for row in df.itertuples():
                self.add_result([row.Metin])
