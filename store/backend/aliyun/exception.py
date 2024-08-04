from aiohttp import ClientResponse


class AliyunException(Exception):
    pass


class AccessTokenException(AliyunException):
    pass


class RefreshTokenException(AliyunException):
    pass


class ExceedCapacityForbidden(AliyunException):
    pass


class FileNotFound(AliyunException):
    pass


class TooManyRequests(AliyunException):
    pass


HTTP_STATUS_AND_EXCEPTION_MAPPING = {}


async def handle_error_status(resp: ClientResponse):
    if resp.status >= 400:
        data = await resp.json()
        # msg = data["msg"]
        # code = data["code"]
        info = {**data, "status": resp.status}
        if "code" in info:
            match info["code"]:
                case "AccessTokenExpired" | "AccessTokenInvalid":
                    raise AccessTokenException(info)
                case "RefreshTokenExpired" | "RefreshTokenInvalid":
                    raise RefreshTokenException(info)
                case "ExceedCapacityForbidden":
                    raise ExceedCapacityForbidden(info)
                case "NotFound.File":
                    raise FileNotFound(info)
                case "TooManyRequests":
                    raise TooManyRequests(info)
                case _:
                    raise AliyunException({**data, "status": resp.status})
