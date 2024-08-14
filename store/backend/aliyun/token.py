from aiohttp.client import request

from typing import Optional

from store.backend.aliyun.base import BASE_URL

from .base import BASE_URL, AccessToken


async def acquire_token_by_code(
    code: str,
    client_id: str,
    client_secret: str,
) -> AccessToken:
    return await _acquire_access_token(
        code=code, client_id=client_id, client_secret=client_secret
    )


async def acquire_token_by_refresh_token(
    refresh_token: str,
    client_id: str,
    client_secret: str,
) -> AccessToken:
    return await _acquire_access_token(
        refresh_token=refresh_token, client_id=client_id, client_secret=client_secret
    )


async def _acquire_access_token(
    code: Optional[str] = None,
    refresh_token: Optional[str] = None,
    *,
    client_id: str,
    client_secret: str | None = None,
) -> AccessToken:
    body = {
        "client_id": client_id,
        "client_secret": client_secret,
    }
    if code:
        body.update(code=code, grant_type="authorization_code")
    elif refresh_token:
        body.update(refresh_token=refresh_token, grant_type="refresh_token")
    else:
        raise ValueError("code and refresh token can not be both none")

    async with request(
        "POST", BASE_URL.format("/oauth/access_token"), json=body
    ) as response:
        res_json = await response.json()
        return AccessToken.model_validate(res_json)
