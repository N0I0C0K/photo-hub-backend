from aiohttp.client import request

from typing import Optional

from .base import BASE_URL, AccessToken, CLIENT_ID, CLIENT_SECRET


async def acquire_token_by_code(
    code: str,
) -> AccessToken:
    return await _acquire_access_token(code=code)


async def acquire_token_by_refresh_token(refresh_token: str) -> AccessToken:
    return await _acquire_access_token(refresh_token=refresh_token)


async def _acquire_access_token(
    code: Optional[str] = None,
    refresh_token: Optional[str] = None,
) -> AccessToken:
    body = {
        "client_id": CLIENT_ID.get(),
        "client_secret": CLIENT_SECRET.get(),
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
