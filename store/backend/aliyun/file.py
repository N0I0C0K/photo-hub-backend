from typing import Annotated, Literal, TypedDict, NotRequired, Unpack, Optional
from typing_extensions import Doc
from annotated_types import Unit
from pydantic import conint, BaseModel, HttpUrl
from aiohttp import request
from datetime import datetime

from .base import (
    FileItem,
    FileCategory,
    FileType,
    BASE_URL,
    _gen_header,
    AccessTokenType,
    FileItemDetail,
    FileDownloadInfo,
)
from .exception import handle_error_status


class _BaseParams(TypedDict):
    drive_id: str
    video_thumbnail_time: NotRequired[
        Annotated[
            int,
            Doc("generate video thumbnail at the specific time, default to 12000ms"),
            Unit("ms"),
        ]
    ]
    video_thumbnail_width: NotRequired[
        Annotated[int, Doc("video thumbnail image width"), Unit("px")]
    ]
    image_thumbnail_width: NotRequired[
        Annotated[int, Doc("image thumbnail width"), Unit("px")]
    ]


class _BaseFileListMethodParams(_BaseParams):
    marker: Annotated[NotRequired[str], Doc("next page mark")]
    limit: Annotated[NotRequired[int], conint(gt=0, le=100)]
    order_by: Annotated[
        NotRequired[
            Literal["created_at", "updated_at", "name", "size", "name_enhanced"]
        ],
        Doc("name_enhanced is better for number eq: 1, 2, 10 instead of 1, 10 ,2"),
    ]
    order_direction: NotRequired[Literal["DESC", "ASC"]]


class _GetFileListParams(_BaseFileListMethodParams):
    parent_file_id: str
    category: NotRequired[list[FileCategory]]
    file_type: NotRequired[FileType]


class _GetFileListResp(BaseModel):
    next_marker: str
    items: list[FileItem]


class _SearchFileResp(_GetFileListResp):
    total_count: int


class _SearchFileParams(_BaseFileListMethodParams):
    query: str


async def get_file_list(
    access_token: AccessTokenType, **kwargs: Unpack[_GetFileListParams]
) -> _GetFileListResp:
    async with request(
        "POST",
        BASE_URL.format("/adrive/v1.0/openFile/list"),
        json={**kwargs, "image_thumbnail_width": 512},
        headers=_gen_header(access_token),
        raise_for_status=handle_error_status,  # type: ignore
    ) as resp:
        data = await resp.json()
        return _GetFileListResp.model_validate(data)


async def search_file(
    access_token: AccessTokenType, **kwargs: Unpack[_SearchFileParams]
) -> _SearchFileResp:
    async with request(
        "POST",
        BASE_URL.format("/adrive/v1.0/openFile/search"),
        json=kwargs,
        headers=_gen_header(access_token),
        raise_for_status=handle_error_status,  # type: ignore
    ) as resp:
        data = await resp.json()
        return _SearchFileResp.model_validate(data)


class _FileDetailByIdParams(_BaseParams):
    file_id: str


async def get_file_detail_by_id(
    access_token: AccessTokenType, **kwargs: Unpack[_FileDetailByIdParams]
) -> FileItemDetail:
    async with request(
        "POST",
        BASE_URL.format("/adrive/v1.0/openFile/get"),
        json={**kwargs, "fields": "id_path,name_path"},
        headers=_gen_header(access_token),
        raise_for_status=handle_error_status,  # type: ignore
    ) as resp:
        data = await resp.json()
        return FileItemDetail.model_validate(data)


async def get_file_datail_by_path(
    access_token: AccessTokenType, drive_id: str, file_path: str
) -> FileItemDetail:
    file_path = file_path.removeprefix("/root")
    async with request(
        "POST",
        BASE_URL.format("/adrive/v1.0/openFile/get_by_path"),
        json={
            "drive_id": drive_id,
            "file_path": file_path,
            "fields": "id_path,name_path",
        },
        headers=_gen_header(access_token),
        raise_for_status=handle_error_status,  # type: ignore
    ) as resp:
        data = await resp.json()
        return FileItemDetail.model_validate(data)


async def get_download_url(
    access_token: AccessTokenType,
    drive_id: str,
    file_id: str,
    expire_sec: Optional[int] = None,
) -> FileDownloadInfo:
    async with request(
        "POST",
        BASE_URL.format("/adrive/v1.0/openFile/getDownloadUrl"),
        json={
            "drive_id": drive_id,
            "file_id": file_id,
            "expire_sec": expire_sec,
        },
        headers=_gen_header(access_token),
        raise_for_status=handle_error_status,  # type: ignore
    ) as resp:
        data = await resp.json()
        return FileDownloadInfo.model_validate(data)
