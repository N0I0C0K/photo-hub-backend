from .base import BASE_URL, CLIENT_ID

from urllib.parse import quote_plus


def login_use_redirect(redirect_url: str) -> str:
    """use redirect to login, will reduirect to the taget url when login success (with code={code} query parameter)

    :param redirect_url: reduirect target url
    :return: login page url
    """
    return BASE_URL.format(
        f"/oauth/authorize?client_id={CLIENT_ID.get()}&redirect_uri={quote_plus(redirect_url)}&scope=user:base,file:all:read&response_type=code"
    )
