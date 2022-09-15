ART_PATH = './images/arts'
ART_EXTENSION_TYPE = '.jpg'


class Art:
    def __init__(self, id, artist, name, description, creation_date):
        self.name = name
        self.artist = artist
        self.description = description
        self.creation_date = creation_date
        self.path = f"{ART_PATH}/{id}{ART_EXTENSION_TYPE}"


class ArtIntro:
    SHORT_DESCRIPTION_MAX_LENGTH = 50

    def __init__(self, id, name, description):
        self.name = name
        self.short_description = description[:ArtIntro.SHORT_DESCRIPTION_MAX_LENGTH] + '...' if len(description) > ArtIntro.SHORT_DESCRIPTION_MAX_LENGTH else description
        self.path = f"{ART_PATH}/{id}{ART_EXTENSION_TYPE}"
