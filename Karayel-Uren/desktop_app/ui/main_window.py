from PyQt6.QtWidgets import QMainWindow, QTabWidget, QLabel
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
from .scraping_tab import ScrapingTab
from .visualization_tab import VisualizationTab
from .extension_tab import ExtensionTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Karayel-Uren")
        self.setGeometry(100, 100, 1200, 800)

        self.setWindowIcon(QIcon("desktop_app/assets/logo.png"))

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        logo_label = QLabel()
        logo_pixmap = QPixmap("desktop_app/assets/logo.png")
        logo_label.setPixmap(logo_pixmap.scaled(180,180, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.tab_widget.setCornerWidget(logo_label, Qt.Corner.TopLeftCorner)

        self.scraping_tab = ScrapingTab()
        self.visualization_tab = VisualizationTab()
        self.extension_tab = ExtensionTab()

        # Tabları ekle
        self.tab_widget.addTab(self.scraping_tab, "Tweet Scraping")
        self.tab_widget.addTab(self.visualization_tab, "Visualization")
        self.tab_widget.addTab(self.extension_tab, "Edge Extension")

        # Tab değişikliklerini bağla
        self.scraping_tab.data_updated.connect(self.visualization_tab.update_data)
        self.setStyleSheet("""
            QMainWindow, QTabWidget, QTableWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QTabWidget::pane {
                border: 1px solid #444444;
            }
            QTabBar::tab {
                background-color: #1e1e1e;
                color: #ffffff;
                padding: 8px;
            }
            QTabBar::tab:selected {
                background-color: #3a3a3a;
            }
            QPushButton {
                background-color: #0077be;
                color: white;
                border: none;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #005fa3;
            }
            QLineEdit, QDateEdit, QSpinBox {
                background-color: #3a3a3a;
                color: white;
                border: 1px solid #555555;
                padding: 3px;
            }
        """)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.scraping_tab = ScrapingTab()
        self.visualization_tab = VisualizationTab()
        self.extension_tab = ExtensionTab()

        self.tab_widget.addTab(self.scraping_tab, "Tweet Scraping")
        self.tab_widget.addTab(self.visualization_tab, "Visualization")
        self.tab_widget.addTab(self.extension_tab, "Edge Extension")

        self.scraping_tab.data_updated.connect(self.visualization_tab.update_data)
