"""
This file stores the definitions for all endpoints
"""

from src.config import url

ENDPOINT_REGISTER_USR = f"{url}auth/register/v2"

ENDPOINT_CREATE_CHNL = f"{url}channels/create/v2"

ENDPOINT_LIST_CHNL = f"{url}channels/list/v2"

ENDPOINT_LISTALL = f"{url}channels/listall/v2"

ENDPOINT_JOIN_CHNL = f"{url}channel/join/v2"

ENDPOINT_DM_CREATE = f"{url}dm/create/v1"

ENDPOINT_DM_LIST = f"{url}dm/list/v1"

ENDPOINT_DM_REMOVE = f"{url}dm/remove/v1"

ENDPOINT_DM_DETAILS = f"{url}dm/details/v1"

ENDPOINT_DM_LEAVE = f"{url}dm/leave/v1"

ENDPOINT_USER_PROF = f"{url}user/profile/v1"

ENDPOINT_CHNL_INVITE = f"{url}channel/invite/v2"

ENDPOINT_CLEAR = f"{url}clear/v1"

ENDPOINT_CHANNEL_DETAILS = f"{url}/channel/details/v2"

ENDPOINT_CHANNEL_MESSAGE = f"{url}/channel/messages/v2"

ENDPOINT_DM_MESSAGE = f"{url}/dm/messages/v1"
