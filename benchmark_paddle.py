import json
import os
import re
import time
import shutil
import label_processor.image_processor as image_processor
import matplotlib.pyplot as plt
import numpy as np  # Thêm để tính toán trung bình và trung vị

title_log = "Benchmark"

def get_all_file_names_from_folder(folder_path: str) -> list[str]:
    try:
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"[{title_log}.get_all_file_names_from_folder] Thư mục '{folder_path}' không tồn tại")

        file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        print(f"[{title_log}.get_all_file_names_from_folder] all file name: {file_names}")
        return file_names
    except Exception as e:
        print(f"[{title_log}.get_all_file_names_from_folder] Lỗi khi lấy danh sách tên file từ thư mục: {str(e)}")
        return []

def sanitize_file_name(file_name: str) -> str:
    # Thay thế các ký tự không hợp lệ bằng dấu gạch dưới
    return re.sub(r'[\/\\:*?"<>|]', '_', file_name)

def save_file_to_folder(source_file_path: str, destination_folder: str, new_file_name: str = None):
    try:
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)  # Tạo thư mục nếu chưa tồn tại
        
        if new_file_name:
            destination_file_path = os.path.join(destination_folder, new_file_name)
        else:
            destination_file_path = os.path.join(destination_folder, os.path.basename(source_file_path))

        shutil.copy(source_file_path, destination_file_path)
        print(f"[{title_log}] Đã lưu file vào '{destination_file_path}'")
    except Exception as e:
        print(f"[{title_log}] Lỗi khi lưu file: {str(e)}")

# Danh sách để chứa tất cả kết quả
results = []
folder_name = "label_example"
file_names = get_all_file_names_from_folder(folder_name)

# Danh sách để chứa thời gian xử lý cho từng file
processing_times = []
success_count = 0
failure_count = 0

with open("output_labels.json", "w") as output_file:
    for file_name in file_names:
        source_file_path = f"{folder_name}/{file_name}"

        # Đo thời gian bắt đầu xử lý
        start_time = time.time()

        # Xử lý file
        result = image_processor.image_to_product_label_model(source_file_path)
        if result is not None:
            results.append({
                "serial_number": result.serial_number,
                "manufacturer": result.manufacturer,
                "country_of_origin": result.country_of_origin,
                "all_words": result.all_words
            })

            # Lọc bỏ các ký tự không hợp lệ khỏi serial_number trước khi dùng làm tên file
            sanitized_serial_number = sanitize_file_name(result.serial_number)
            new_file_name = f"{sanitized_serial_number}.jpg"  # Giả sử bạn muốn dùng serial_number làm tên file
            save_file_to_folder(source_file_path, "paddle_test/success", new_file_name)
            success_count += 1  # Tăng số lượng file thành công
        else:
            # Lưu vào thư mục failed với tên file giữ nguyên
            save_file_to_folder(source_file_path, "paddle_test/failed")
            failure_count += 1  # Tăng số lượng file thất bại

        # Đo thời gian kết thúc xử lý và tính toán thời gian xử lý
        end_time = time.time()
        processing_time = end_time - start_time
        processing_times.append(processing_time)
        print(f"[{title_log}] Processed '{file_name}' in {processing_time:.4f} seconds")

    # Ghi danh sách các kết quả vào file dưới dạng JSON
    json.dump(results, output_file, indent=4, ensure_ascii=False)

# Tính toán thông tin tóm tắt
average_time = np.mean(processing_times) if processing_times else 0
median_time = np.median(processing_times) if processing_times else 0

# Vẽ biểu đồ benchmark thời gian xử lý
plt.figure(figsize=(10, 6))

# Biểu đồ nối các điểm thời gian xử lý, x-axis dùng chỉ số thay vì tên file
plt.plot(range(len(file_names)), processing_times, marker='o')  # Dùng plt.plot để nối các điểm
plt.xlabel('File Index')
plt.ylabel('Processing Time (seconds)')
plt.title(f'Benchmark Processing Time\nSuccess: {success_count} | Failure: {failure_count} | '
          f'Average Time: {average_time:.1f}s | Median Time: {median_time:.1f}s')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Xác định top 15 file có thời gian xử lý cao nhất
top_15_files = sorted(zip(file_names, processing_times), key=lambda x: x[1], reverse=True)[:15]
top_15_file_names = [file for file, _ in top_15_files]
top_15_processing_times = [time for _, time in top_15_files]

# Vẽ biểu đồ cho top 15 file có thời gian xử lý cao nhất
plt.figure(figsize=(10, 6))
plt.bar(top_15_file_names, top_15_processing_times, color='orange')
plt.xlabel('File Name')
plt.ylabel('Processing Time (seconds)')
plt.title('Top 15 Files with the Highest Processing Time')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Xác định top 15 file có thời gian xử lý thấp nhất
bottom_15_files = sorted(zip(file_names, processing_times), key=lambda x: x[1])[:15]
bottom_15_file_names = [file for file, _ in bottom_15_files]
bottom_15_processing_times = [time for _, time in bottom_15_files]

# Vẽ biểu đồ cho top 15 file có thời gian xử lý thấp nhất
plt.figure(figsize=(10, 6))
plt.bar(bottom_15_file_names, bottom_15_processing_times, color='green')
plt.xlabel('File Name')
plt.ylabel('Processing Time (seconds)')
plt.title('Top 15 Files with the Lowest Processing Time')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
