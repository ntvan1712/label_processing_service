from typing import Optional

import requests


def download_media(media_url: str, result_local_path: str) -> Optional[str]:
    try:
        response = requests.get(media_url, stream=True)
        response.raise_for_status()

        with open(result_local_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"[AssetsInstallerRemoteDataSource] File đã được tải xuống và lưu tại: {result_local_path}")
        return result_local_path
    except Exception as e:
        print(f"[AssetsInstallerRemoteDataSource] Lỗi khi tải xuống file: {str(e)}")
        return None