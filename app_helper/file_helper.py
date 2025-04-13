import hashlib
import json
import os
import shutil
from typing import Optional

title_log = "FileHelper"

def get_file_extension(filename: str) -> str:
    _, ext = os.path.splitext(filename)

    return ext

def file_name_without_extension(filename: str) -> str:
    _, ext = os.path.splitext(filename)

    return filename[:-len(ext)]

def create_folder(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print(f"[{title_log}.create_folder] Folder already exists")

def remove_folder(path: str):
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"[{title_log}.remove_folder] Removed folder {path}")
    else:
        print(f"[{title_log}.remove_folder] Folder does not exist")

def delete_file(file_path):
    try:
        os.remove(file_path)  
    except Exception as e:
        print(f"[{title_log}.dele_file] Remove file err: {e}")

def check_file_exists(file_path: str) -> bool:
    return os.path.exists(file_path)

def copy_file(file_path: str, new_file_path: str) -> Optional[str]:
    try:
        shutil.copy(file_path, new_file_path)
        print(f"[{title_log}.copy_file] File đã được copy từ {file_path} tới {new_file_path}")
        return new_file_path
    except Exception as e:
        print(f"[{title_log}.copy_file] Lỗi khi copy file: {str(e)}")
        return None

def move_folder(root_folder_path: str, new_folder_path: str)-> bool:
    try:
        shutil.move(root_folder_path, new_folder_path)
        print(f"[{title_log}.move_folder] Folder đã được move từ {root_folder_path} tới {new_folder_path}")
        return True
    except Exception as e:
        print(f"[{title_log}.move_folder] Lỗi khi move folder: {e}")
        return False


def write_data_to_json_file(file_path: str, json_data):
    try:
        with open(file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        print(f"[{title_log}.write_data_to_json_file] Data has been written to JSON file at: {file_path}")
        return None
    except Exception as e:
        print(f"[{title_log}.write_data_to_json_file] Error: {e}")
        return e

def read_json_file(file_path: str):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"[{title_log}.read_json_file] Failed {e}")
        return None

    
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
    
def get_all_subfolders_from_folder(parent_folder_path: str) -> list[str]:
    try:
        # Kiểm tra xem đường dẫn thư mục tồn tại không
        if not os.path.exists(parent_folder_path):
            raise FileNotFoundError(f"Thư mục '{parent_folder_path}' không tồn tại")

        # Lấy danh sách tên thư mục con từ thư mục mẹ
        subfolders = [f for f in os.listdir(parent_folder_path) if os.path.isdir(os.path.join(parent_folder_path, f))]
        print(f"[{title_log}.get_all_subfolders_from_folder] Tất cả các thư mục con của '{parent_folder_path}': {subfolders}")
        return subfolders
    except Exception as e:
        print(f"[{title_log}.get_all_subfolders_from_folder] Lỗi khi lấy danh sách tên thư mục con từ thư mục mẹ: {str(e)}")
        return []
    
def calculate_md5_checksum(file_path: str)-> Optional[str]:
    try:
        md5_hash = hashlib.md5()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
        return md5_hash.hexdigest()
    except Exception as e:
        print(f"[{title_log}.calculate_md5_checksum] Checksum video failed {str(e)}")
        return None
