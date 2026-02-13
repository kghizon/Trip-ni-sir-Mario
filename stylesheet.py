APP_THEME = """
/* Main Window Background */
QWidget {
    background-color: #222222;
    color: #F3F4F6;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
}

/* Search Bar - Subtle Inset Look */
QLineEdit {
    background-color: #111111;
    border: 1px solid #444444;
    border-radius: 4px;
    padding: 6px 10px;
    color: #D1D5DB; 
}

QLineEdit:focus {
    border: 1px solid #D1D5DB;
    background-color: #000000;
}

/* Filter Button */
QToolButton {
    background-color: #333333;
    border: 1px solid #444444;
    border-radius: 4px;
    color: #D1D5DB;
}

QToolButton:hover {
    background-color: #444444;
    border: 1px solid #D1D5DB;
}

/* Scroll Area */
QScrollArea {
    background-color: transparent;
    border: none;
}

/* Tool Checkboxes */
QCheckBox {
    spacing: 12px;
    padding: 10px;
    color: #9CA3AF; /* Dimmer gray for unselected text */
}

QCheckBox:hover {
    background-color: #2A2A2A;
    color: #FFFFFF;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    border: 2px solid #444444;
    background-color: #111111;
}

QCheckBox::indicator:checked {
    background-color: #D1D5DB; /* Lighter gray pop */
    border: 2px solid #F3F4F6;
}

/* Run Button - Maximum Contrast */
QPushButton {
    background-color: #D1D5DB;
    color: #111111;
    border-radius: 4px;
    font-weight: 800;
    font-size: 14px;
    text-transform: uppercase;
}

QPushButton:hover {
    background-color: #F3F4F6;
}

QPushButton:pressed {
    background-color: #9CA3AF;
}

/* Scrollbar Styling */
QScrollBar:vertical {
    border: none;
    background: #222222;
    width: 10px;
}

QScrollBar::handle:vertical {
    background: #444444;
    min-height: 30px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #D1D5DB;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""