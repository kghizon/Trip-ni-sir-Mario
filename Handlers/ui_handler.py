from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
    QTabBar, QApplication, QLabel
)
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QIcon, QPixmap, QPainter, QPen, QColor 
from Handlers.tab_handler import THandler 
from stylesheet import APP_THEME 

class UIHandler(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RX Toolkit")
        self.resize(1100, 750)
        
        self.setStyleSheet(APP_THEME)

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True) 
        
        self.tabs.tabBar().setMouseTracking(True)
        self.tabs.tabBar().installEventFilter(self)

        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.tabBarClicked.connect(self.handle_tab_click)

        main_layout.addWidget(self.tabs)
        self.setCentralWidget(central_widget)

        self.add_new_tab()
        self.add_plus_tab()

    def _get_close_icon(self):
        pix = QPixmap(16, 16)
        pix.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pix)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.setPen(QPen(QColor("white"), 2))
        painter.drawLine(4, 4, 12, 12)
        painter.drawLine(12, 4, 4, 12)
        
        painter.end()
        return QIcon(pix)

    def add_new_tab(self):
        new_tab = THandler()
        new_tab.tool_selected.connect(self.update_tab_title)
        
        index = self.tabs.count() - 1
        if index < 0: index = 0 
        
        self.tabs.insertTab(index, new_tab, "New Tab")
        self.tabs.setCurrentIndex(index)
        
        self.tabs.tabBar().setTabIcon(index, QIcon()) 
        btn = self.tabs.tabBar().tabButton(index, QTabBar.ButtonPosition.RightSide)
        if btn:
            btn.setIcon(self._get_close_icon())
            
        self._update_close_buttons(-1) 

    def update_tab_title(self, new_title):
        sender_widget = self.sender()
        index = self.tabs.indexOf(sender_widget)
        if index != -1:
            self.tabs.setTabText(index, new_title)

    def add_plus_tab(self):
        self.tabs.addTab(QWidget(), "+")
        plus_tab_index = self.tabs.count() - 1
        self.tabs.tabBar().setTabButton(plus_tab_index, QTabBar.ButtonPosition.RightSide, None)

    def eventFilter(self, source, event):
        if source == self.tabs.tabBar():
            if event.type() == QEvent.Type.MouseMove:
                point = event.pos()
                tab_index = self.tabs.tabBar().tabAt(point)
                self._update_close_buttons(tab_index)
                
            elif event.type() == QEvent.Type.HoverLeave or event.type() == QEvent.Type.Leave:
                self._update_close_buttons(-1)

        return super().eventFilter(source, event)

    def _update_close_buttons(self, active_index):
        for i in range(self.tabs.count()):
            if i == self.tabs.count() - 1:
                continue

            btn = self.tabs.tabBar().tabButton(i, QTabBar.ButtonPosition.RightSide)
            if btn:
                should_show = (i == active_index)
                btn.setVisible(should_show)

    def handle_tab_click(self, index):
        if index == self.tabs.count() - 1:
            self.add_new_tab()

    def close_tab(self, index):
        if index == self.tabs.count() - 1:
            return

        if index == self.tabs.currentIndex():
            target_index = index - 1 if index > 0 else 0
            self.tabs.removeTab(index)
            self.tabs.setCurrentIndex(target_index)
        else:
            self.tabs.removeTab(index)
        
        if self.tabs.count() == 1: 
            self.add_new_tab()