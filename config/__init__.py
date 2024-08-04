from yaml import load

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from pydantic import BaseModel, Field
from typing import Annotated, Optional


class AliyunConfig(BaseModel):
    refresh_token: Annotated[str, Field(min_length=20)]
    access_token: Optional[str] = None
    client_id: str
    client_secret: str


class StoreConfig(BaseModel):
    aliyun: Optional[AliyunConfig] = None


class Config(BaseModel):
    store: StoreConfig


_config: Optional[Config] = None


def get_global_config() -> Config:
    global _config
    if _config:
        return _config
    with open("./config.yaml", "r", encoding="utf-8") as f:
        _config = Config.model_validate(load(f, Loader))
    return _config
