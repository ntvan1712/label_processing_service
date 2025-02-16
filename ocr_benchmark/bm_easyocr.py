import time
import easyocr

def benchmark(image_path):
    # Khởi tạo EasyOCR
    reader = easyocr.Reader(lang_list=['en'], gpu=False)  # Hỗ trợ nhiều ngôn ngữ, thay 'en' bằng ngôn ngữ cần thiết
    
    # Bắt đầu đo thời gian
    start_time = time.time()
    
    # Nhận diện văn bản bằng EasyOCR
    results = reader.readtext(image_path, output_format="dict")
    list_str = []
    for result in results:
        list_str.append(result["text"])
    
    # Kết thúc đo thời gian
    end_time = time.time()
    
    # In kết quả
    # text = ' '.join([res[1] for res in result])
    print(image_path)
    print(f"EasyOCR Processing Time: {end_time - start_time:.4f}s")
    print("EasyOCR Output:\n", list_str)
    
    return results