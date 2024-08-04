from typing import Self
from .file import (
    get_download_url,
    get_file_datail_by_path,
    get_file_detail_by_id,
    get_file_list,
)
from .login import login_use_redirect
from .token import acquire_token_by_code, acquire_token_by_refresh_token
from .exception import *
from .user import get_user_drive_info, get_user_info, get_user_space_info


class AliyunApiClient:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret


# TODO 支持创建多个不同 client id 的 api 客户端
