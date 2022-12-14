from typing import Self

from model.constants import ART_IMAGE_PATH, ART_IMAGE_EXTENSION_TYPE, SHORT_DESCRIPTION_MAX_LENGTH


class ArtIntro:
    def __init__(self : Self, id : int, name : str, description : str) -> None:
        self.id = id
        self.name = name
        self.short_description = description[:SHORT_DESCRIPTION_MAX_LENGTH] + '...' if len(description) > SHORT_DESCRIPTION_MAX_LENGTH else description
        self.image_path = f"{ART_IMAGE_PATH}/{id}{ART_IMAGE_EXTENSION_TYPE}"