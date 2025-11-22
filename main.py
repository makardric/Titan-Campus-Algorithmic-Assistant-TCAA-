import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from ui import Ui_MainWindow   # <-- change this to the name of your UI file

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Example: connect buttons here
        # self.ui.pushButton_2.clicked.connect(self.go_to_navigation)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())