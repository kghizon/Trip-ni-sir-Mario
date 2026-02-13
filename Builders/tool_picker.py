import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QPushButton, QCheckBox, QScrollArea, 
    QFrame, QStyle, QToolButton
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

class ToolPicker(QWidget):
    # Define your tools here for easy maintenance
    TOOLS = [
        "Web Scraper", "Image Resizer", "Filetype Converter",
        "Filesize Compressor", "QR Code Generator"
    ]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("RX Toolkit")
        self.resize(380, 650)

        self._setup_ui()
        self._populate_tools()

    def _setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        top_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search tools...")
        self.search_bar.setFixedHeight(30)
        
        search_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView)
        self.search_bar.addAction(search_icon, QLineEdit.ActionPosition.TrailingPosition)

        top_layout.addWidget(self.search_bar)
        self.main_layout.addLayout(top_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame) 
        
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setSpacing(8)
        self.list_layout.setContentsMargins(10, 5, 5, 5)
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_area.setWidget(self.list_container)
        self.main_layout.addWidget(self.scroll_area)

        self.run_btn = QPushButton("Run Selected Tool(s)")
        self.run_btn.setFixedHeight(45)
        self.run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.main_layout.addWidget(self.run_btn)

    def _populate_tools(self):
        self.tool_widgets = []
        for tool_name in self.TOOLS:
            checkbox = QCheckBox(tool_name)
            self.list_layout.addWidget(checkbox)
            self.tool_widgets.append(checkbox)