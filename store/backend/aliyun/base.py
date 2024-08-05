from typing import (
    Literal,
    Annotated,
    Optional,
    Coroutine,
    TypeVar,
    Type,
    Any,
    Callable,
    TypeAlias,
    TypedDict,
)

from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from datetime import datetime
from aiohttp import request
from contextvars import ContextVar


_Model_T = TypeVar("_Model_T", bound=BaseModel)

CLIENT_SECRET = ContextVar[str]("aliyun_client_secret")
CLIENT_ID = ContextVar[str]("aliyun_client_id")
BASE_URL = "https://openapi.alipan.com{}"

AccessTokenType: TypeAlias = Annotated[str, "access_token"]


class _RequestBaseKWargs(TypedDict):
    access_token: str


def _gen_header(access_token: str):
    return {"Authorization": "Bearer " + access_token}


def _gen_base_get_func(
    url: str, model: Type[_Model_T]
) -> Callable[[AccessTokenType], Coroutine[Any, Any, _Model_T]]:
    async def _inner(access_token: AccessTokenType):
        async with request(
            "POST",
            BASE_URL.format(url),
            headers=_gen_header(access_token),
        ) as resp:
            t = await resp.json()
            return model.model_validate(t)

    return _inner


FileCategory = Literal["video", "doc", "audio", "zip", "others", "image"]
FileType = Literal["file", "folder"]


class AccessToken(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: Literal["Bearer"] = "Bearer"


class FileItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    drive_id: str
    file_id: str
    parent_file_id: str
    name: str
    file_type: Annotated[
        FileType,
        Field(
            alias="type",
        ),
    ]

    created_at: datetime
    updated_at: datetime

    size: Annotated[Optional[int], Field(gt=0)] = None
    file_extension: Optional[str] = None
    content_hash: Optional[str] = None
    category: Optional[FileCategory] = None

    thumbnail: Optional[str] = None
    url: Optional[HttpUrl] = None

    # video profile
    play_cursor: Optional[str] = None


class FileItemDetail(FileItem):
    id_path: Optional[str] = None
    name_path: Optional[str] = None


class UserInfo(BaseModel):
    user_id: Annotated[str, Field(alias="id")]
    name: str
    avater: HttpUrl
    phone: Annotated[str, Field(pattern=r"^\d*$")]


class UserDriveInfo(BaseModel):
    user_id: str
    name: str
    avatar: str
    default_drive_id: str
    resource_drive_id: Optional[str] = None
    backup_drive_id: Optional[str] = None


class PersonalSpaceInfo(BaseModel):
    used_size: int
    total_size: int


class UserSpaceInfo(BaseModel):
    personal_space_info: PersonalSpaceInfo


class FileDownloadInfo(BaseModel):
    url: str
    expiration: datetime
    method: str
    method: str


ROOT_FILE_ITEM = FileItem(
    drive_id="1",
    file_id="root",
    parent_file_id="1",
    name="root",
    file_type="folder",
    created_at=datetime.now(),
    updated_at=datetime.now(),
)


def init_aliyun_api(client_id: str, client_secret: str):
    CLIENT_ID.set(client_id)
    CLIENT_SECRET.set(client_secret)
