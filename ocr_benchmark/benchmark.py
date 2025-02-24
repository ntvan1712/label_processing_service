
import os
import label_processor.image_processor as image_processor
title_log = "Benchmark"

def get_all_file_names_from_folder(folder_path: str) -> list[str]:
    try:
        # Kiểm tra xem đường dẫn thư mục tồn tại không
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"[{title_log}.get_all_file_names_from_folder] Thư mục '{folder_path}' không tồn tại")

        # Lấy danh sách tên file từ thư mục
        file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        print(f"[{title_log}.get_all_file_names_from_folder] all file name: {file_names}")
        return file_names
    except Exception as e:
        print(f"[{title_log}.get_all_file_names_from_folder] Lỗi khi lấy danh sách tên file từ thư mục: {str(e)}")
        return []

file_names = get_all_file_names_from_folder("label_example")
for file_name in file_names:
    image_processor.image_to_product_label_model(f"label_example/{file_name}")


