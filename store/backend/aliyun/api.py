from typing import Self
from functools import partial

from .file import (
    get_download_url,
    get_file_datail_by_path,
    get_file_detail_by_id,
    get_file_list,
)
from .token import acquire_token_by_code, acquire_token_by_refresh_token
from .login import login_use_redirect
from .exception import *
from .user import get_user_drive_info, get_user_info, get_user_space_info


class AliyunApiClient:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self._client_id = client_id
        self._client_secret = client_secret

        self.login_use_redirect = partial(login_use_redirect, client_id=client_id)

        self.acquire_token_by_code = partial(
            acquire_token_by_code, client_id=client_id, client_secret=client_secret
        )
        self.acquire_token_by_refresh_token = partial(
            acquire_token_by_refresh_token,
            client_id=client_id,
            client_secret=client_secret,
        )
