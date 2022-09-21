from typing import Self

from model.constants import ART_IMAGE_PATH, ART_VIDEO_PATH, ART_IMAGE_EXTENSION_TYPE, ART_VIDEO_EXTENSION_TYPE


class Art:
    def __init__(self : Self, id : int, artists : str, name : str, description : str, creation_date : str, is_video_included : int) -> None:
        self.id = id
        self.name = name
        self.artists = artists
        self.description = description
        self.creation_date = creation_date
        self.is_video_included = is_video_included
        self.image_path = f"{ART_IMAGE_PATH}/{id}{ART_IMAGE_EXTENSION_TYPE}"
        self.video_path = f"{ART_VIDEO_PATH}/{id}{ART_VIDEO_EXTENSION_TYPE}"
