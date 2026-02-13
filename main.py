import sys
from PySide6.QtWidgets import QApplication
from Handlers.ui_handler import UIHandler
import stylesheet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet.APP_THEME)
    window = UIHandler()
    window.show()
    sys.exit(app.exec())