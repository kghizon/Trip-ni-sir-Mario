from PySide6.QtCore import QThread, Signal

class ResizeWorker(QThread):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, logic_instance, save_path, mode, **kwargs):
        super().__init__()
        self.logic = logic_instance
        self.save_path = save_path
        self.mode = mode 
        self.kwargs = kwargs

    def run(self):
        try:
            if self.mode == 'percent':
                percentage = self.kwargs.get('percentage')
                resized_image = self.logic.resize_by_percentage(percentage)
            else:
                width = self.kwargs.get('width')
                height = self.kwargs.get('height')
                resized_image = self.logic.resize_free(width, height)

            self.logic.save_image(resized_image, self.save_path)

            self.finished.emit(self.save_path)

        except Exception as e:
            self.error.emit(str(e))