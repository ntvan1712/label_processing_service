import time
from paddleocr import PaddleOCR
from PIL import Image

#pip install paddlepaddle paddleocr
ocr_engine = PaddleOCR(use_angle_cls=True, use_gpu=False,lang='en', show_log=True)   

def benchmark(image_path):
    # Khởi tạo PaddleOCR
    # Bắt đầu đo thời gian
    start_time = time.time()
    
    # Nhận diện văn bản bằng PaddleOCR
    result = ocr_engine.ocr(img= image_path, cls=False)
    text_list = [str(res[1][0]).lower() for line in result for res in line]
    
    # Kết thúc đo thời gian
    end_time = time.time()
    
    print(image_path)
    print(f"PaddleOCR Processing Time: {end_time - start_time:.4f}s")
    print("PaddleOCR Output:\n", text_list)
    
    return result

