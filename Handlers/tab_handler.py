from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, 
    QLineEdit, QPushButton, QScrollArea, QFrame, 
    QStackedWidget, QLabel, QHBoxLayout, QListWidget,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal, QSize

class PlaceholderTool(QWidget):
    def __init__(self, tool_name):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop) 
        layout.setContentsMargins(20, 100, 20, 20) 
        
        lbl = QLabel(f"🔧 {tool_name} Interface")
        lbl.setStyleSheet("font-size: 24px; font-weight: bold; color: #666;")
        
        sub_lbl = QLabel("This is a placeholder QWidget.\nImport your actual class in 'tools_map'.")
        sub_lbl.setStyleSheet("font-size: 14px; color: #888; margin-top: 10px;")
        
        layout.addWidget(lbl)
        layout.addWidget(sub_lbl)
        layout.addStretch() 

class THandler(QWidget):
    tool_selected = Signal(str) 

    def __init__(self):
        super().__init__()
        self.tools_map = {
            "Web Scraper": None, 
            "Image Resizer": None,
            "Filetype Converter": None,
            "Filesize Compressor": None,
            "QR Generator": None,
            "PDF Merger": None,
        }
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0) 
        
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.grid_view = self._create_grid_view()
        self.stack.addWidget(self.grid_view)

        self.tool_container = QWidget()
        self.tool_layout = QVBoxLayout(self.tool_container)
        self.tool_layout.setContentsMargins(0,0,0,0)
        self.stack.addWidget(self.tool_container)

        self.stack.setCurrentIndex(0)

        # --- SEARCH BAR ---
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search tools...")
        self.search_bar.textChanged.connect(self.update_suggestions)
        self.search_bar.setStyleSheet("""
            QLineEdit {
                background-color: #1C1C26;
                border: 2px solid #333;
                border-radius: 10px; /* Reduced radius for wide look */
                padding: 0 20px;
                font-size: 16px;
                color: #FFF;
            }
            QLineEdit:focus {
                border: 2px solid #FA2E4E;
                background-color: #0F0F12;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(Qt.GlobalColor.black)
        shadow.setOffset(0, 5)
        self.search_bar.setGraphicsEffect(shadow)

        # --- SUGGESTION LIST ---
        self.suggestion_list = QListWidget(self)
        self.suggestion_list.hide()
        self.suggestion_list.itemClicked.connect(self.on_suggestion_clicked)
        self.suggestion_list.setStyleSheet("""
            QListWidget {
                background-color: #1C1C26;
                border: 1px solid #333;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
                color: #EEE;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 12px 20px;
                border-bottom: 1px solid #2A2A35;
            }
            QListWidget::item:hover {
                background-color: #FA2E4E;
                color: white;
            }
            QListWidget::item:selected {
                background-color: #FA2E4E;
            }
        """)

    def _create_grid_view(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        
        self.grid_layout = QGridLayout(container)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        
        self.grid_layout.setContentsMargins(20, 100, 20, 20) 

        self.tool_cards = []

        row, col = 0, 0
        for name, cls_ref in sorted(self.tools_map.items()):
            card = QPushButton(name)
            card.setFixedSize(180, 100)
            card.setCursor(Qt.CursorShape.PointingHandCursor)
            card.setProperty("class", "ToolCard")
            
            card.clicked.connect(lambda ch=False, n=name, c=cls_ref: self.launch_tool(n, c))
            
            self.grid_layout.addWidget(card, row, col)
            col += 1
            if col > 4: 
                col = 0
                row += 1

        scroll.setWidget(container)
        return scroll

    def resizeEvent(self, event):
        super().resizeEvent(event)
        
        side_margin = 20
        top_margin = 20
        bar_height = 50
        
        bar_width = self.width() - (side_margin * 2)
        
        self.search_bar.setGeometry(side_margin, top_margin, bar_width, bar_height)
        
        list_height = self.suggestion_list.height() 
        self.suggestion_list.setGeometry(side_margin, top_margin + bar_height, bar_width, list_height)

    def update_suggestions(self, text):
        self.suggestion_list.clear()
        
        if not text:
            self.suggestion_list.hide()
            self.search_bar.setStyleSheet(self.search_bar.styleSheet().replace("border-bottom-left-radius: 0px;", "border-bottom-left-radius: 10px;").replace("border-bottom-right-radius: 0px;", "border-bottom-right-radius: 10px;"))
            return

        matches = [name for name in sorted(self.tools_map.keys()) if text.lower() in name.lower()]

        if matches:
            self.suggestion_list.addItems(matches)
            
            item_height = 45 
            total_h = min(len(matches) * item_height + 10, 300)
            self.suggestion_list.setFixedHeight(total_h)
            
            self.resizeEvent(None) 
            
            self.suggestion_list.show()
            self.suggestion_list.raise_() 
            
            self.search_bar.setStyleSheet(self.search_bar.styleSheet().replace("border-radius: 10px;", "border-top-left-radius: 10px; border-top-right-radius: 10px; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px;"))

        else:
            self.suggestion_list.hide()

    def on_suggestion_clicked(self, item):
        tool_name = item.text()
        tool_class = self.tools_map.get(tool_name)
        self.launch_tool(tool_name, tool_class)

    def launch_tool(self, tool_name, tool_class):
        self.tool_selected.emit(tool_name)
        self._clear_tool_container()

        self.search_bar.hide()
        self.suggestion_list.hide()

        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 20, 20, 10)

        back_btn = QPushButton("← Back")
        back_btn.setFixedSize(80, 30)
        back_btn.setStyleSheet("""
            QPushButton { background: #333; border: none; border-radius: 4px; color: #FFF; }
            QPushButton:hover { background: #444; }
        """)
        back_btn.clicked.connect(self.back_to_grid)
        
        title = QLabel(tool_name)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #EEE; margin-left: 10px;")

        header_layout.addWidget(back_btn)
        header_layout.addWidget(title)
        header_layout.addStretch()

        self.tool_layout.addWidget(header)

        if tool_class:
            widget_instance = tool_class()
        else:
            widget_instance = PlaceholderTool(tool_name)
            
        self.tool_layout.addWidget(widget_instance)
        self.stack.setCurrentWidget(self.tool_container)

    def back_to_grid(self):
        self.tool_selected.emit("New Tab")
        self.stack.setCurrentIndex(0)
        
        self.search_bar.show() 
        self.search_bar.clear()
        self.search_bar.setFocus() 
        
        self._clear_tool_container()

    def _clear_tool_container(self):
        while self.tool_layout.count():
            item = self.tool_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()