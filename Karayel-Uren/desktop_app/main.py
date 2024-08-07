import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from ui.main_window import MainWindow
from flask_server import start_server

def main():
    start_server() 
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
