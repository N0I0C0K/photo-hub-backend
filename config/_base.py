from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from pydantic import BaseModel, Field
from typing import Annotated, Optional

CONFIG_PATH = "./config.yaml"


class AliyunConfig(BaseModel):
    refresh_token: Annotated[str, Field(min_length=20)]
    access_token: Optional[str] = None
    client_id: str
    client_secret: str


class StoreConfig(BaseModel):
    use: str
    aliyun: Optional[AliyunConfig] = None


class Config(BaseModel):
    store: StoreConfig


_config: Optional[Config] = None


def get_global_config() -> Config:
    global _config
    if _config:
        return _config
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        _config = Config.model_validate(load(f, Loader))
    return _config


def save_config(cfg: Config | None = None):
    json_data = cfg or get_global_config().model_dump()
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        dump(json_data, f)
