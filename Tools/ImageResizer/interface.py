from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QFileDialog, QRadioButton, QSlider, QLineEdit, 
    QMessageBox, QFrame, QCheckBox, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QCursor

from Tools.ImageResizer.image_resizer import ImageResizer
from Tools.ImageResizer.thread_handler import ResizeWorker

class Interface(QWidget):
    def __init__(self):
        super().__init__()

        self.logic = ImageResizer()
        self.original_size = (0,0)
        self.aspect_ratio = None
        self._syncing = False
        self._updating_inputs = False
        self.worker = None

        self.build_ui()

        self.set_controls_enabled(False)

        self.percent_radio.toggled.connect(self.update_resize_mode)
        self.freesize_radio.toggled.connect(self.update_resize_mode)

        self.width_input.textEdited.connect(self.on_width_changed)
        self.height_input.textEdited.connect(self.on_height_changed)

        self.preview_overlay.hide()
    
    def build_ui(self):
        main_layout = QHBoxLayout(self)

        left_panel = QFrame()
        left_layout = QVBoxLayout(left_panel)

        self.upload_btn = QPushButton("Upload Image")
        self.upload_btn.clicked.connect(self.upload_image)
        left_layout.addWidget(self.upload_btn)
        left_layout.addSpacing(15)

        # [ Resize by percentage ]
        self.percent_radio = QRadioButton("Resize by percentage")
        self.percent_radio.setChecked(True)

        percent_radio_row = QHBoxLayout()
        percent_radio_row.setContentsMargins(10,0,0,0)
        percent_radio_row.addWidget(self.percent_radio)
        percent_radio_row.addStretch()

        left_layout.addLayout(percent_radio_row)

        self.percent_slider = QSlider(Qt.Horizontal)
        self.percent_slider.setRange(20,200)
        self.percent_slider.setSingleStep(10)
        self.percent_slider.setPageStep(10)
        self.percent_slider.setTickInterval(10)
        self.percent_slider.setTickPosition(QSlider.TicksBelow)
        self.percent_slider.setValue(100)
        self.percent_slider.valueChanged.connect(self.on_slider_changed)

        self.percent_label = QLabel("100%")
        
        percent_layout = QHBoxLayout()
        percent_layout.setContentsMargins(0,0,20,0)
        percent_layout.addWidget(self.percent_slider)
        percent_layout.addWidget(self.percent_label)

        percent_container = QVBoxLayout()
        percent_container.setContentsMargins(30,5,0,10)
        percent_container.addLayout(percent_layout)

        left_layout.addLayout(percent_container)

        # [ Resize freely ]
        self.freesize_radio = QRadioButton("Resize Freely")

        freesize_radio_row = QHBoxLayout()
        freesize_radio_row.setContentsMargins(10,0,0,0)
        freesize_radio_row.addWidget(self.freesize_radio)
        freesize_radio_row.addStretch()

        left_layout.addLayout(freesize_radio_row)

        height_layout = QHBoxLayout()
        height_label = QLabel("Height")
        height_label.setFixedWidth(50)

        self.height_input = QLineEdit()
        self.height_input.setFixedWidth(80)
        self.height_input.textChanged.connect(self.on_height_changed)

        height_px = QLabel("px")

        height_layout.addWidget(height_label)
        height_layout.addWidget(self.height_input)
        height_layout.addWidget(height_px)
        height_layout.addStretch()

        width_layout = QHBoxLayout()
        width_label = QLabel("Width")
        width_label.setFixedWidth(50)

        self.width_input = QLineEdit()
        self.width_input.setFixedWidth(80)
        self.width_input.textChanged.connect(self.on_width_changed)

        width_px = QLabel("px")

        width_layout.addWidget(width_label)
        width_layout.addWidget(self.width_input)
        width_layout.addWidget(width_px)
        width_layout.addStretch()

        self.aspect_ratio_lock = QCheckBox("Lock aspect ratio")
        self.aspect_ratio_lock.setChecked(True)

        freesize_container = QVBoxLayout()
        freesize_container.setContentsMargins(30,5,0,10)
        freesize_container.addLayout(width_layout)
        freesize_container.addLayout(height_layout)
        freesize_container.addWidget(self.aspect_ratio_lock)

        left_layout.addLayout(freesize_container)
        left_layout.addStretch()

        self.resize_btn = QPushButton("Resize")
        self.resize_btn.clicked.connect(self.resize_image)
        left_layout.addWidget(self.resize_btn)

        # --- Right Panel ---
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)

        self.preview_label = QLabel("Image Preview")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumSize(400,300)
        self.preview_label.setStyleSheet("border: 1px solid #888")
        self.preview_label.setLayout(QVBoxLayout())

        self.preview_overlay = QLabel("", self.preview_label)
        self.preview_overlay.setStyleSheet("""
            color: white;
            background-color: rgba(0,0,0,120);
            padding: 4px 6px;
            border-radius: 4px;
            font-size: 10px;
        """)
        self.preview_overlay.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        self.preview_label.layout().addStretch()
        self.preview_label.layout().addWidget(
            self.preview_overlay,
            alignment=Qt.AlignRight | Qt.AlignBottom
        )

        right_layout.addWidget(self.preview_label)

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)

    def set_controls_enabled(self, enabled: bool):
        self.percent_radio.setEnabled(enabled)
        self.freesize_radio.setEnabled(enabled)
        self.percent_slider.setEnabled(enabled)
        self.resize_btn.setEnabled(enabled)

        self.width_input.setEnabled(enabled)
        self.height_input.setEnabled(enabled)
        self.aspect_ratio_lock.setEnabled(enabled)

    def update_resize_mode(self):
        percent_mode = self.percent_radio.isChecked()

        self.percent_slider.setEnabled(percent_mode)

        self.width_input.setReadOnly(percent_mode)
        self.height_input.setReadOnly(percent_mode)

    def upload_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if not path:
            return
        
        image = self.logic.load_image(path)
        self.original_size = image.size
        w, h = self.original_size
        self.aspect_ratio = w / h if  h != 0 else None

        self.preview_overlay.setText(
            f"{self.original_size[0]} x {self.original_size[1]} px"
        )
        self.preview_overlay.show()

        self.update_dimension_inputs(*self.original_size)
        self.show_preview(path)
        self.set_controls_enabled(True)
        self.update_resize_mode()

    def on_slider_changed(self, value):
        value =  round(value/10) * 10
        self.percent_slider.blockSignals(True)
        self.percent_slider.setValue(value)
        self.percent_slider.blockSignals(False)

        self.percent_label.setText(f"{value}%")

        if self.original_size != (0,0):
            w = int(self.original_size[0] * value / 100)
            h = int(self.original_size[1] * value / 100)
            self.update_dimension_inputs(w,h)

    def on_width_changed(self, text):
        if self._syncing: return
        if self._updating_inputs or not self.aspect_ratio_lock.isChecked(): return
        if not text.isdigit(): return
        
        try:
            width = int(text)
            if width <= 0: return
            
            self._syncing = True
            height = int(width / self.aspect_ratio)
            self.height_input.setText(str(height))
        finally:
            self._syncing = False

    def on_height_changed(self, text):
        if self._syncing: return
        if self._updating_inputs or not self.aspect_ratio_lock.isChecked(): return
        if not text.isdigit(): return
        
        try:
            height = int(text)
            if height <= 0: return
            
            self._syncing = True
            width = int(height * self.aspect_ratio)
            self.width_input.setText(str(width))
        finally:
            self._syncing = False

    def update_dimension_inputs(self, width, height):
        self._updating_inputs = True
        self.width_input.setText(str(width))
        self.height_input.setText(str(height))
        self._updating_inputs = False

    def show_preview(self, image_path):
        pixmap = QPixmap(image_path)
        self.preview_label.setPixmap(
            pixmap.scaled(
                self.preview_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

    def resize_image(self):
        params = {}
        mode = 'percent' if self.percent_radio.isChecked() else 'free'

        if mode == 'percent':
            params['percentage'] = self.percent_slider.value()
        else:
            try:
                params['width'] = int(self.width_input.text())
                params['height'] = int(self.height_input.text())
            except ValueError:
                QMessageBox.warning(self, "Input Error", "Please ensure width/height are valid numbers.")
                return

        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "resized_image.png",
            "Images (*.png *.jpg *.jpeg)"
        )
        if not save_path:
            return

        self.set_controls_enabled(False)
        self.upload_btn.setEnabled(False) 
        self.resize_btn.setText("Processing...")
        self.setCursor(Qt.WaitCursor)

        self.worker = ResizeWorker(self.logic, save_path, mode, **params)
        self.worker.finished.connect(self.on_resize_finished)
        self.worker.error.connect(self.on_resize_error)
        self.worker.start()

    def on_resize_finished(self, save_path):
        self.setCursor(Qt.ArrowCursor)
        self.resize_btn.setText("Resize")
        self.set_controls_enabled(True)
        self.upload_btn.setEnabled(True)

        self.show_preview(save_path)
        
        try:
            image = self.logic.load_image(save_path)
            self.original_size = image.size
            self.aspect_ratio = self.original_size[0] / self.original_size[1]
            self.update_dimension_inputs(*self.original_size)
            
            QMessageBox.information(self, "Success", "Image resized successfully!")
        except Exception as e:
            self.on_resize_error(str(e))

    def on_resize_error(self, error_msg):
        self.setCursor(Qt.ArrowCursor)
        self.resize_btn.setText("Resize")
        self.set_controls_enabled(True)
        self.upload_btn.setEnabled(True) 
        
        QMessageBox.critical(self, "Resize Failed", error_msg)