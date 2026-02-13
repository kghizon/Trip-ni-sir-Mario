from PySide6.QtWidgets import QApplication
from Builders.tool_picker import ToolPicker
import stylesheet
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet.APP_THEME)
    window = ToolPicker()
    window.show()
    sys.exit(app.exec())