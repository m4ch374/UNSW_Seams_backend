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

ENDPOINT_USERS_ALL = f"{url}users/all/v1"

ENDPOINT_CHNL_INVITE = f"{url}channel/invite/v2"

ENDPOINT_CHNL_LEAVE = f"{url}channel/leave/v1"

ENDPOINT_CHNL_ADDOWNER = f"{url}channel/addowner/v1"

ENDPOINT_CHNL_REMOVEOWNER = f"{url}channel/removeowner/v1"

ENDPOINT_ADMIN_REMOVE = f"{url}admin/user/remove/v1"

ENDPOINT_ADMIN_PERM_CHANGE = f"{url}admin/userpermission/change/v1"

ENDPOINT_CLEAR = f"{url}clear/v1"

ENDPOINT_CHANNEL_DETAILS = f"{url}/channel/details/v2"

ENDPOINT_CHANNEL_MESSAGE = f"{url}/channel/messages/v2"

ENDPOINT_DM_MESSAGE = f"{url}/dm/messages/v1"

ENDPOINT_MESSAGE_SEND = f"{url}/message/send/v1"

ENDPOINT_DM_SEND = f"{url}/message/senddm/v1"

ENDPOINT_MESSAGE_EDIT = f"{url}/message/edit/v1"

ENDPOINT_MESSAGE_REMOVE = f"{url}/message/remove/v1"

ENDPOINT_LOGOUT = f"{url}/auth/logout/v1"