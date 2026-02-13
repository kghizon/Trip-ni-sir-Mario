import os
from PIL import Image

class ImageResizer:
    def __init__(self):
        self.image = None
        self.image_path = None

    def load_image(self, path: str):
        self.image_path = path
        img = Image.open(path)

        if img.mode != 'RGB':
            img = img.convert('RGB')

        self.image = img
        return self.image
    
    def resize_by_percentage(self, percentage: int):
        if not self.image:
            raise ValueError("No image loaded")
        
        width, height = self.image.size
        new_size = (
            int(width * percentage / 100),
            int(height * percentage / 100)
        )
        return self.image.resize(new_size, Image.LANCZOS)
    
    def resize_free(self, width: int, height: int):
       if not self.image:
            raise ValueError("No image loaded")
       
       return self.image.resize((width, height), Image.LANCZOS)
    
    def save_image(self, image: Image.Image, output_path: str):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path)
        return output_path