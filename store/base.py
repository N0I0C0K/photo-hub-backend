from typing import Protocol, TypeVar, Generic, Literal, Optional, Self
from pathlib import PurePosixPath
from os import PathLike
from datetime import datetime

from pydantic import BaseModel

StrPath = str | PathLike[str]

# from pydantic import HttpUrl


# class FileItem(NamedTuple):
#     name: str
#     file_type: Literal["file", "folder"]
#     file_category: Literal["video", "doc", "audio", "zip", "others", " image"]
#     path: PurePath


class BaseFileIO(Protocol):
    def __enter__(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class _PathLike(Protocol):
    def __str__(self) -> str:
        raise NotImplementedError

    def is_dir(self) -> bool:
        raise NotImplementedError

    def is_file(self) -> bool:
        raise NotImplementedError

    @property
    def drive(self) -> str:
        raise NotImplementedError

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def suffix(self) -> str:
        raise NotImplementedError

    @property
    def suffixes(self) -> list[str]:
        raise NotImplementedError


FileType = Literal["file", "folder"]


class Thumbnail(BaseModel):
    url: str


class BaseFile(BaseModel):
    name: str
    path: str
    type: FileType
    extension: str
    created_at: datetime
    updated_at: datetime
    size: Optional[int] = None
    thumbnail: Optional[Thumbnail] = None


class BasePath(PurePosixPath):
    def is_file(self) -> bool:
        raise NotImplementedError

    def is_dir(self) -> bool:
        raise NotImplementedError

    def to_model(self) -> BaseFile:
        raise NotImplementedError


_T = TypeVar("_T", bound=BasePath)


class BaseStore(Generic[_T]):
    """store abstraction base class"""

    async def search_file_by_name(self, file_name: str) -> list[_T]:
        raise NotImplementedError

    async def listdir(self, dir_path: StrPath) -> list[_T]:
        raise NotImplementedError

    async def mkdir(self, dir_path: StrPath) -> bool:
        raise NotImplementedError

    async def rmdir(self, dir_path: StrPath) -> bool:
        raise NotImplementedError

    async def isdir(self, path: StrPath) -> bool:
        raise NotImplementedError

    async def isfile(self, path: StrPath) -> bool:
        raise NotImplementedError

    async def rmfile(self, path: StrPath) -> bool:
        raise NotImplementedError

    async def open_file(self, path: StrPath) -> BaseFileIO:
        raise NotImplementedError

    async def get_download_url(self, path: StrPath) -> str:
        raise NotImplementedError

    async def rename(self, path: StrPath, new_name: str) -> bool:
        raise NotImplementedError

    @classmethod
    async def spawn(cls, cfg) -> Self:
        raise NotImplementedError
