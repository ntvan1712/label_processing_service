import time
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"


# print(pytesseract.get_languages())

def benchmark(image_path):
    # img = Image.open(image_path)
    
    # Bắt đầu đo thời gian
    start_time = time.time()
    
    # Nhận diện văn bản bằng Tesseract
    text = pytesseract.image_to_string(image= Image.open(image_path))
    
    # Kết thúc đo thời gian
    end_time = time.time()
    
    # In kết quả
    print(image_path)
    print(f"Tesseract Processing Time: {end_time - start_time:.4f}s")
    print("Tesseract OCR Output:\n", text)
    
    return text


