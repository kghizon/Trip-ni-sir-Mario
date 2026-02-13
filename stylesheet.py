APP_THEME = """
/* --- Global Background --- */
QMainWindow, QWidget {
    background-color: #0F0F12;
    color: #E0E0E0;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
}

/* --- The Tab Widget Pane --- */
QTabWidget::pane { 
    border: 2px solid #333333; 
    border-radius: 8px;
    background: #0F0F12;
    top: -2px; 
}

/* --- The Tab Bar --- */
QTabBar {
    background: transparent;
    qproperty-drawBase: 0;
}

/* --- Standard Tabs --- */
QTabBar::tab {
    background: #1C1C26;
    color: #888888;
    height: 35px; 
    
    /* CRITICAL FIX: Uneven padding creates space for the close button */
    padding-left: 15px;
    padding-right: 35px; /* Large right padding so text doesn't touch the X */
    
    margin-right: 4px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    min-width: 120px;
    font-weight: 500;
    border: 1px solid #333333;
    border-bottom: none;
}

QTabBar::tab:selected {
    background: #0F0F12; 
    color: #FFFFFF;
    border: 2px solid #333333;
    border-bottom: 2px solid #0F0F12; 
    font-weight: bold;
}

QTabBar::tab:hover:!selected {
    background: #252530;
    color: #D1D5DB;
}

/* --- The Close Button (The 'X') --- */
QTabBar::close-button {
    subcontrol-position: right; /* Anchors it to the right side */
    margin-right: 10px;         /* Pushes it 10px away from the edge */
    
    width: 16px;
    height: 16px;
    border-radius: 4px;         /* Slight rounding */
    background: transparent;    /* Transparent so we see the icon */
}

QTabBar::close-button:hover {
    background-color: #FA2E4E; /* Red background on hover */
}

/* --- The '+' Tab (Special styling) --- */
QTabBar::tab:last {
    background: transparent;
    color: #FFFFFF;
    min-width: 30px;
    max-width: 30px;
    border: none;
    font-size: 20px;
    margin-left: 5px;
    
    /* Reset padding for the + tab since it has no close button */
    padding-left: 0px;
    padding-right: 0px; 
}

QTabBar::tab:last:hover {
    background: #252530;
    border-radius: 15px;
}

QTabBar::tab:last:selected {
    border-bottom: none;
}

/* --- Search Bar --- */
QLineEdit#PageSearch {
    background-color: #1C1C26;
    border: 2px solid #333333;
    border-radius: 18px; 
    padding: 8px 15px;
    font-size: 14px;
    color: #FFFFFF;
    margin-bottom: 10px;
}
QLineEdit#PageSearch:focus {
    border: 2px solid #FA2E4E; 
    background-color: #000000;
}

/* --- Tool Cards --- */
QPushButton.ToolCard {
    background-color: #1C1C26;
    border: 1px solid #333333;
    border-radius: 12px;
    color: #F3F4F6;
    font-size: 15px;
    font-weight: 600;
}
QPushButton.ToolCard:hover {
    background-color: #2D2D3A;
    border: 1px solid #FA2E4E;
}
QPushButton.ToolCard:pressed {
    background-color: #FA2E4E;
    color: #000000;
}
"""