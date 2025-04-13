import time
from typing import Optional
from label_task.model.label_task_model import LabelTaskModel
from app_helper import  file_helper,download
from label_task.common import error_code_define
from label_processor import image_processor
from label_task.data import repository

root_path = "http://localhost:9000/asset-management"
media_folder = "./label_task/label_images"

def _download_label(task: LabelTaskModel)-> Optional[str]:
    file_helper.create_folder(path=media_folder)
    image_url = f"{root_path}/{task.path}"
    image_ext = file_helper.get_file_extension(task.path)
    local_path = f"{media_folder}/{task.id}{image_ext}"
    return download.download_media(media_url=image_url, result_local_path= local_path)

def process_label_task(task: LabelTaskModel):
    # time.sleep(40)
    local_image_path = _download_label(task= task)
    error_code = None
    if local_image_path is None:
        error_code = error_code_define.DOWNLOAD_LABEL_FAILED
    else:
        label_info_model = image_processor.image_to_product_label_model(image_path= local_image_path)
        if label_info_model is None:
            error_code = error_code_define.PROCESS_LABEL_FAILED
        else:
            repository.update_success_task(label_info_model, task.id)
    
    if error_code is not None:
        repository.update_error_task(error_code, task.id)
    if local_image_path is not None:
        file_helper.delete_file(local_image_path)