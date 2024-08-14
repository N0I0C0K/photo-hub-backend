from urllib.parse import quote_plus
from .base import BASE_URL


def login_use_redirect(redirect_url: str, client_id: str) -> str:
    """use redirect to login, will reduirect to the taget url when login success (with code={code} query parameter)

    :param redirect_url: reduirect target url
    :return: login page url
    """
    return BASE_URL.format(
        f"/oauth/authorize?client_id={client_id}&redirect_uri={quote_plus(redirect_url)}&scope=user:base,file:all:read&response_type=code"
    )
