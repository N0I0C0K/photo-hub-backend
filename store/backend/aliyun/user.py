from .base import UserInfo, _gen_base_get_func, UserDriveInfo, UserSpaceInfo


get_user_info = _gen_base_get_func("/oauth/users/info", UserInfo)

get_user_drive_info = _gen_base_get_func(
    "/adrive/v1.0/user/getDriveInfo", UserDriveInfo
)

get_user_space_info = _gen_base_get_func(
    "/adrive/v1.0/user/getSpaceInfo", UserSpaceInfo
)
