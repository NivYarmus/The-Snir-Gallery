import os

from model.constants import ART_IMAGE_PATH, ART_VIDEO_PATH, ART_IMAGE_EXTENSION_TYPE, ART_VIDEO_EXTENSION_TYPE


class UploadsManager:
    @staticmethod
    def upload_image(file_name : str, bytestream : bytes) -> None:
        UploadsManager.__upload_file(ART_IMAGE_PATH, ART_IMAGE_EXTENSION_TYPE, file_name, bytestream)

    @staticmethod
    def upload_video(file_name : str, bytestream : bytes) -> None:
        UploadsManager.__upload_file(ART_VIDEO_PATH, ART_VIDEO_EXTENSION_TYPE, file_name, bytestream)

    @staticmethod
    def delete_image(file_name : str) -> None:
        UploadsManager.__delete_file(ART_IMAGE_PATH, ART_IMAGE_EXTENSION_TYPE, file_name)

    @staticmethod
    def delete_video(file_name : str) -> None:
        UploadsManager.__delete_file(ART_VIDEO_PATH, ART_VIDEO_EXTENSION_TYPE, file_name)

    @staticmethod
    def __upload_file(file_path : str, file_extension : str, file_name : str, bytestream : bytes) -> None:
        with open(f'{UploadsManager.__setup_file_path(file_path)}/{file_name}{file_extension}', 'wb') as file:
            file.write(bytestream)

    @staticmethod
    def __delete_file(file_path : str, file_extension : str, file_name : str) -> None:
        os.remove(f'{UploadsManager.__setup_file_path(file_path)}/{file_name}{file_extension}')

    @staticmethod
    def __setup_file_path(file_path):
        return file_path.replace('.', './static')