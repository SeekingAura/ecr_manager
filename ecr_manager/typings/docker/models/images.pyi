from typing import (
    Any,
    Generator,
    TypedDict,
    Optional,
)

from _typeshed import Incomplete

from ..api import APIClient as APIClient
from ..constants import DEFAULT_DATA_CHUNK_SIZE as DEFAULT_DATA_CHUNK_SIZE
from ..errors import BuildError as BuildError
from ..errors import ImageLoadError as ImageLoadError
from ..errors import InvalidArgument as InvalidArgument
from ..utils import parse_repository_tag as parse_repository_tag
from ..utils.json_stream import json_stream as json_stream
from .resource import Collection as Collection
from .resource import Model as Model

class Image(Model):
    @property
    def labels(self): ...
    @property
    def short_id(self): ...
    @property
    def tags(self): ...
    def history(self): ...
    def remove(self, force: bool = ..., noprune: bool = ...): ...
    def save(self, chunk_size=..., named: bool = ...): ...
    def tag(self, repository, tag: Incomplete | None = ..., **kwargs): ...

class RegistryData(Model):
    image_name: Incomplete
    def __init__(self, image_name, *args, **kwargs) -> None: ...
    @property
    def id(self): ...
    @property
    def short_id(self): ...
    def pull(self, platform: Incomplete | None = ...): ...
    def has_platform(self, platform): ...
    attrs: Incomplete
    def reload(self) -> None: ...

class ImagePushProgressDetailI(TypedDict):
    current: Optional[int]
    total: Optional[int]

class ImagePushInfoI(TypedDict):
    status: str
    """
    Some Possible values
    - "Layer already exists"
    - "Pushing"
    - "Preparing"
    """
    progressDetail: Optional[ImagePushProgressDetailI]
    progress: str
    id: Optional[str]

class ImageCollection(Collection):
    model = Image
    def build(self, **kwargs): ...
    def get(self, name): ...
    def get_registry_data(
        self, name, auth_config: Incomplete | None = ...
    ): ...
    def list(
        self,
        name: Incomplete | None = ...,
        all: bool = ...,
        filters: Incomplete | None = ...,
    ): ...
    def load(self, data): ...
    def pull(
        self,
        repository,
        tag: Incomplete | None = ...,
        all_tags: bool = ...,
        **kwargs,
    ): ...
    def push(
        self,
        repository: str,
        tag: str | None,
        stream: bool,
        decode: bool = ...,
        **kwargs: Any,
    ) -> Generator[ImagePushInfoI, None, None]: ...
    def remove(self, *args, **kwargs) -> None: ...
    def search(self, *args, **kwargs): ...
    def prune(self, filters: Incomplete | None = ...): ...
    def prune_builds(self, *args, **kwargs): ...

def normalize_platform(platform, engine_info): ...
