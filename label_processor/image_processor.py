import time
from typing import Optional
from paddleocr import PaddleOCR
from label_processor.models.product_label_model import ProductLabelModel

from label_processor.text_finder import serial_number_finder, manufacturer_finder, country_finder
#pip install paddlepaddle paddleocr

ocr_engine = PaddleOCR(use_angle_cls=True, use_gpu=False,lang='en', show_log=False)   

def _image_to_list_text(image_path: str) -> list[str]:
    start_time = time.time()
    
    ocr_result = ocr_engine.ocr(img= image_path, cls=False)
    list_text = [str(res[1][0]).lower() for line in ocr_result for res in line]
    
    end_time = time.time()
    
    print(f"PaddleOCR Process {image_path} - Time: {end_time - start_time:.4f}s")
    print("PaddleOCR Output:\n", list_text)
    
    return list_text

def image_to_product_label_model(image_path: str) -> Optional[ProductLabelModel]:
    serial_number = None
    manufacturer = None
    country_of_origin = None
    all_words = []

    list_text = _image_to_list_text(image_path= image_path)
    for i, text in enumerate(list_text):
        if i < len(list_text) - 1:
            next_text = list_text[i + 1]
        else:
            next_text = None

        words = text.split()
        all_words.extend([word for word in words if len(word) >= 2])

        if serial_number is None:
            serial_number = serial_number_finder.find_in_text(text=text, next_text= next_text)
        if manufacturer is None:
            manufacturer = manufacturer_finder.find_in_words(words)
        if country_of_origin is None:
            country_of_origin = country_finder.find_in_words(words)

    if serial_number is None:
        serial_number_by_image = serial_number_finder.find_in_image(image_path= image_path)
        if serial_number_by_image is not None:
            serial_number = serial_number_by_image

    if serial_number is None:
        if len(all_words) != 1:
            return None
        else:
            serial_number = all_words[0]

    
    return ProductLabelModel(
        serial_number=serial_number,
        manufacturer=manufacturer,
        country_of_origin=country_of_origin,
        all_words= all_words,
    )






