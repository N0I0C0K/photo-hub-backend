from typing import Mapping, Type

from .base import BaseStore, BasePath
from .aliyun import AliyunStore

from config import global_config

STORE_NAME_AND_STORE_FACTOR_MAPPING: Mapping[str, Type[BaseStore]] = {
    "aliyun": AliyunStore
}


class StoreManager:
    def __init__(self) -> None:
        self._store: BaseStore[BasePath] | None = None

    async def setup(self):
        await self._init_store()

    async def _init_store(self):
        store_use = global_config.store.use
        if store_use not in STORE_NAME_AND_STORE_FACTOR_MAPPING:
            raise NotImplementedError
        store_cfg = getattr(global_config.store, "aliyun")
        factor = STORE_NAME_AND_STORE_FACTOR_MAPPING[store_use]
        self._store = await factor.spawn(store_cfg)

    @property
    def store(self):
        if self._store is None:
            raise ValueError
        return self._store


store_manager = StoreManager()
