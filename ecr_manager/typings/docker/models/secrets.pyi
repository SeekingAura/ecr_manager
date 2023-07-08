from ..api import APIClient as APIClient
from .resource import Collection as Collection, Model as Model

class Secret(Model):
    id_attribute: str
    @property
    def name(self): ...
    def remove(self): ...

class SecretCollection(Collection):
    model = Secret
    def create(self, **kwargs): ...
    def get(self, secret_id): ...
    def list(self, **kwargs): ...