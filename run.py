
import json
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

with open("output_labels.json", "w") as output_file:
    # Danh sách để chứa tất cả kết quả
    results = []
    file_names = get_all_file_names_from_folder("label_example")

    # Duyệt qua các file và xử lý từng file
    for file_name in file_names:
        result = image_processor.image_to_product_label_model(f"label_example/{file_name}")
        if result is not None:
            # Chuyển đối tượng ProductLabelModel thành JSON và thêm vào danh sách
            results.append({
                "serial_number": result.serial_number,
                "manufacturer": result.manufacturer,
                "country_of_origin": result.country_of_origin,
                "all_words": result.all_words
            })
    
    # Ghi danh sách các kết quả vào file dưới dạng JSON
    json.dump(results, output_file, indent=4, ensure_ascii=False)

# file_names = get_all_file_names_from_folder("label_example")
# for file_name in file_names:
#     result = image_processor.image_to_product_label_model(f"label_example/{file_name}")
#     if result is not None:
#         print(result.to_json())
