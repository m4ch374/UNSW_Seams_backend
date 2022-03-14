"""
This file stores the definitions for all endpoints
"""

from src.config import url

ENDPOINT_REGISTER_USR = f"{url}auth/register/v2"

ENDPOINT_CREATE_CHNL = f"{url}channels/create/v2"

ENDPOINT_LIST_CHNL = f"{url}channels/list/v2"

ENDPOINT_LISTALL = f"{url}channels/listall/v2"

ENDPOINT_JOIN_CHNL = f"{url}channel/join/v2"

ENDPOINT_CLEAR = f"{url}clear/v1"
