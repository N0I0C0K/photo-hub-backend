from os import fspath
from typing import Callable, Optional, Self, Protocol
from inspect import iscoroutinefunction
from datetime import datetime

from store.base import BaseFile, BaseStore, BasePath, StrPath, Thumbnail
from store.backend.aliyun import *
from store.backend.aliyun.exception import AccessTokenException, RefreshTokenException
from store.backend.aliyun.utils import parse_name_path
from utils import bidict

from config._base import AliyunConfig


class AliyunFileItem(Protocol):
    file_type: FileType
    file_id: str
    drive_id: str
    size: Optional[int]
    thumbnail: Optional[str]
    created_at: datetime
    updated_at: datetime


class AliyunPath(BasePath):
    def __init__(
        self, *args: str, file_item: AliyunFileItem, _store: "AliyunStore"
    ) -> None:
        super().__init__(*args)
        self.file_item = file_item
        self._store = _store
        self._store.file_id_and_file_path_mapping[file_item.file_id] = self.as_posix()

    def is_dir(self) -> bool:
        return self.file_item.file_type == "folder"

    def is_file(self) -> bool:
        return self.file_item.file_type == "file"

    async def listdir(self) -> list["AliyunPath"]:
        if not self.is_dir():
            raise ValueError("not a dir")

        file_list = await get_file_list(
            self._store.access_token,
            drive_id=self.file_item.drive_id,
            parent_file_id=self.file_item.file_id,
        )
        return [
            AliyunPath(fspath(self), it.name, file_item=it, _store=self._store)
            for it in file_list.items
        ]

    async def get_download_url(self) -> str:
        return await self._store.get_download_url_by_file_id(self.file_item.file_id)

    def to_model(self) -> BaseFile:
        return BaseFile(
            name=self.name,
            path=self.as_posix(),
            type=self.file_item.file_type,
            extension=self.suffix,
            size=self.file_item.size,
            thumbnail=(
                Thumbnail(url=self.file_item.thumbnail)
                if self.file_item.thumbnail
                else None
            ),
            created_at=self.file_item.created_at,
            updated_at=self.file_item.updated_at,
        )


class AliyunStore(BaseStore[AliyunPath]):
    access_token: str
    refresh_token: str
    drive_id: str
    file_id_and_file_path_mapping: bidict[str, StrPath]

    def __init__(self) -> None:
        pass

    @classmethod
    async def create(
        cls, refresh_token: str, access_token: Optional[str] = None
    ) -> Self:
        target = cls()
        target.refresh_token = refresh_token
        if not access_token:
            await target._refresh_token()
        else:
            target.access_token = access_token
        user_drive_info = await get_user_drive_info(target.access_token)
        target.drive_id = user_drive_info.default_drive_id
        target.file_id_and_file_path_mapping = bidict(
            {"root": "/root"},
            max_size=128,
            ttl=60 * 10,
        )
        target._make_func_auto_refresh()
        return target

    async def _refresh_token(self):
        new_token = await acquire_token_by_refresh_token(self.refresh_token)
        self.access_token = new_token.access_token
        self.refresh_token = new_token.refresh_token

    def _make_func_auto_refresh(self):
        def warp_retry_when_token_failed(func: Callable):
            async def inner_func(*args, **kwargs):
                try:
                    res = await func(*args, **kwargs)
                except (AccessTokenException, RefreshTokenException):
                    await self._refresh_token()
                    res = await func(*args, **kwargs)
                return res

            return inner_func

        for att_name in dir(self):
            att_val = getattr(self, att_name, None)
            if iscoroutinefunction(att_val):
                setattr(self, att_name, warp_retry_when_token_failed(att_val))

    async def listdir(self, dir_path: StrPath = "/root") -> list[AliyunPath]:
        dir_file_id = self.file_id_and_file_path_mapping.by_val(dir_path)
        if dir_file_id is None:
            # dir_file_id = await self.get_file_id_by_path(dir_path)
            await self.get_file_item_by_path(dir_path)

        dir_file_id = self.file_id_and_file_path_mapping.by_val(dir_path)
        assert dir_file_id
        return await self.listdir_by_file_id(dir_file_id)

    async def get_file_item_by_id(self, file_id: str) -> AliyunPath:
        file_item = await get_file_detail_by_id(
            self.access_token, drive_id=self.drive_id, file_id=file_id
        )
        assert file_item.name_path
        return AliyunPath(
            parse_name_path(file_item.name_path), file_item=file_item, _store=self
        )

    async def get_file_item_by_path(self, path: StrPath) -> AliyunPath:
        file_item = await get_file_datail_by_path(
            self.access_token, self.drive_id, fspath(path)
        )
        return AliyunPath(fspath(path), file_item=file_item, _store=self)

    async def listdir_by_file_id(self, file_id: str) -> list[AliyunPath]:
        if file_id not in self.file_id_and_file_path_mapping:
            await self.get_file_item_by_id(file_id)
        parent_path = self.file_id_and_file_path_mapping[file_id]
        file_list = await get_file_list(
            self.access_token, drive_id=self.drive_id, parent_file_id=file_id
        )
        return [
            AliyunPath(fspath(parent_path), it.name, file_item=it, _store=self)
            for it in file_list.items
        ]

    async def get_download_url(self, path: StrPath) -> str:
        file_id = self.file_id_and_file_path_mapping.by_val(path)
        if file_id is None:
            await self.get_file_item_by_path(path)
        file_id = self.file_id_and_file_path_mapping.by_val(path)
        if file_id is None:
            raise ValueError(f"{path} 路径不存在")
        return await self.get_download_url_by_file_id(file_id)

    async def get_download_url_by_file_id(self, file_id: str) -> str:
        res = await get_download_url(self.access_token, self.drive_id, file_id)
        return res.url

    @classmethod
    async def spawn(cls, cfg: AliyunConfig) -> Self:
        init_aliyun_api(cfg.client_id, cfg.client_secret)
        return await cls.create(cfg.refresh_token, cfg.access_token)
