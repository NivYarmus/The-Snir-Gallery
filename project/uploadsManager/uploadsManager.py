import os

from model.constants import ART_IMAGE_PATH, ART_VIDEO_PATH, ART_IMAGE_EXTENSION_TYPE, ART_VIDEO_EXTENSION_TYPE


class UploadsManager:
    @staticmethod
    def upload_image(file_name : str, bytestream : bytes) -> None:
        UploadsManager.__upload_file(UploadsManager.setup_image_path(file_name), bytestream)

    @staticmethod
    def upload_video(file_name : str, bytestream : bytes) -> None:
        UploadsManager.__upload_file(UploadsManager.setup_video_path(file_name), bytestream)

    @staticmethod
    def delete_image(file_name : str) -> None:
        UploadsManager.__delete_file(UploadsManager.setup_image_path(file_name))

    @staticmethod
    def delete_video(file_name : str) -> None:
        UploadsManager.__delete_file(UploadsManager.setup_video_path(file_name))

    @staticmethod
    def edit_image(file_name : str, bytestream : bytes) -> None:
        UploadsManager.__edit_file(UploadsManager.setup_image_path(file_name), bytestream)

    @staticmethod
    def edit_video(file_name : str, bytestream : bytes) -> None:
        UploadsManager.__edit_file(UploadsManager.setup_video_path(file_name), bytestream)

    @staticmethod
    def __upload_file(file_path : str, bytestream : bytes) -> None:
        with open(file_path, 'wb') as file:
            file.write(bytestream)

    @staticmethod
    def __delete_file(file_path : str) -> None:
        os.remove(file_path)

    @staticmethod
    def __setup_file_path(file_path : str):
        return file_path.replace('.', './static')

    @staticmethod
    def __clear_file(file_path : str):
        with open(file_path, 'r+') as file:
            file.truncate()

    @staticmethod
    def __edit_file(file_path : str, bytestream : bytes):
        UploadsManager.__clear_file(file_path)
        UploadsManager.__upload_file(file_path, bytestream)

    @staticmethod
    def setup_image_path(file_name : str) -> str:
        return f'{UploadsManager.__setup_file_path(ART_IMAGE_PATH)}/{file_name}{ART_IMAGE_EXTENSION_TYPE}'

    @staticmethod
    def setup_video_path(file_name : str) -> str:
        return f'{UploadsManager.__setup_file_path(ART_VIDEO_PATH)}/{file_name}{ART_VIDEO_EXTENSION_TYPE}'