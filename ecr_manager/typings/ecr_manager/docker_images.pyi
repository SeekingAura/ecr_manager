from typing import TypedDict

class IDockerImagesData(TypedDict):
    images: dict[str, str]
