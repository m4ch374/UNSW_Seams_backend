# Default Imports
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src import channel


# Our own imports
import src.channel as chnl
import src.channels as chnls
import src.message as msg
from src import dm
from src import auth
from src import admin
from src.other import clear_v1
from src.data_store import data_store


def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

    
# =============== /user domain =================
@APP.route("/auth/login/v2", methods=['POST'])
def login_v2():
    data = request.get_json()
    email = data['email']
    password = data['password']
    return dumps(auth.auth_login_v2(email, password))

@APP.route("/auth/logout/v1", methods=['POST'])
def logout_v1():
    data = request.get_json()
    token = data['token']
    return dumps(auth.auth_logout_v1(token))

@APP.route("/auth/register/v2", methods=['POST'])
def register_v2():
    data = request.get_json()
    email = data['email']
    password = data['password']
    name_first = data['name_first']
    name_last = data['name_last']
    return dumps(auth.auth_register_v2(email, password, name_first, name_last))

@APP.route("/users/all/v1", methods=['GET'])
def all_v1():
    token = request.args.get('token')
    return dumps(auth.users_all_v1(token))

@APP.route("/user/profile/v1", methods=['GET'])
def profile_v1():
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    id = int(u_id)
    return dumps(auth.user_profile_v1(token, id))

@APP.route("/user/profile/setname/v1", methods=['PUT'])
def profile_setname_v1():
    data = request.get_json()
    token = data['token']
    name_first = data['name_first']
    name_last = data['name_last']
    return dumps(auth.user_profile_setname_v1(token, name_first, name_last))

@APP.route("/user/profile/setemail/v1", methods=['PUT'])
def profile_setemail_v1():
    data = request.get_json()
    token = data['token']
    email = data['email']
    return dumps(auth.user_profile_setemail_v1(token, email))

@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def profile_sethandle_v1():
    data = request.get_json()
    token = data['token']
    handle_str = data['handle_str']
    return dumps(auth.user_profile_sethandle_v1(token, handle_str))


# =============== /channels domain =================
@APP.route("/channels/create/v2", methods=['POST'])
def channels_create_v2():
    body = request.get_json(force=True)

    usr_id = data_store.get_id_from_token(body['token'])
    response = chnls.channels_create_v1(usr_id, body['name'], body['is_public'])

    return dumps(response)

@APP.route("/channels/list/v2", methods=['GET'])
def channels_list_v2():
    tok = request.args.get('token')
    usr_id = data_store.get_id_from_token(tok)
    response = chnls.channels_list_v1(usr_id)
    return dumps(response)

@APP.route("/channels/listall/v2", methods=['GET'])
def channels_listall_v2():
    tok = request.args.get('token')
    usr_id = data_store.get_id_from_token(tok)
    response = chnls.channels_listall_v1(usr_id)
    return dumps(response)
# ==================================================

# =============== /channel domain =================
@APP.route("/channel/join/v2", methods=['POST'])
def channel_join_v2():
    request_data = request.get_json()
    auth_user_id = data_store.get_id_from_token(request_data['token'])
    channel_id = request_data['channel_id']
    chnl.channel_join_v1(auth_user_id, channel_id)
    return dumps({})

@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite_v2():
    request_data = request.get_json()
    auth_user_id = data_store.get_id_from_token(request_data['token'])
    channel_id = request_data['channel_id']
    u_id = request_data['u_id']
    chnl.channel_invite_v1(auth_user_id, channel_id, u_id)
    return dumps({})

@APP.route("/channel/details/v2", methods=['GET'])
def channel_details_v2():
    user_id = data_store.get_id_from_token(request.args.get('token'))
    channel_id = int(request.args.get('channel_id'))
    response = channel.channel_details_v1(user_id, channel_id)
    return dumps(response)

# ==================================================

# ================== /dm domain ====================
@APP.route("/dm/create/v1", methods=['POST'])
def dm_create_v1():
    # Create dm channel
    data = request.get_json()
    usr_id = data_store.get_id_from_token(data['token'])
    response = dm.dm_create_v1(usr_id, data['u_ids'])
    return dumps(response)

@APP.route("/dm/list/v1", methods=['GET'])
def dm_list_v1():
    tok = request.args.get('token')
    usr_id = data_store.get_id_from_token(tok)
    response = dm.dm_list_v1(usr_id)
    return dumps(response)

@APP.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove_v1():
    data = request.get_json()
    usr_id = data_store.get_id_from_token(data['token'])
    response = dm.dm_remove_v1(usr_id, data['dm_id'])
    return dumps(response)

@APP.route("/dm/details/v1", methods=['GET'])
def dm_details_v1():
    data = dict(request.args)
    usr_id = data_store.get_id_from_token(data['token'])
    response = dm.dm_details_v1(usr_id, int(data['dm_id']))
    return dumps(response)

@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave_v1():
    data = request.get_json()
    u_id = data_store.get_id_from_token(data['token'])
    response = dm.dm_leave_v1(u_id, data['dm_id'])
    return dumps(response)

# Commented for coverage
# @APP.route("/dm/messages/v1", methods=['GET'])
# def dm_messages_v1():
#     data = dict(request.args)
#     u_id = data_store.get_id_from_token(data['token'])
#     response = dm.dm_messages_v1(u_id, int(data['dm_id'], int(data['start'])))
#     return response


# # =============== /messages domain =================
@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages_v2():
    user_id = data_store.get_id_from_token(request.args.get('token'))
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    response = msg.channel_messages_v1(user_id, channel_id, start)
    return dumps(response)

@APP.route("/dm/messages/v1", methods = ['GET'])
def dm_messages_v1():
    user_id = data_store.get_id_from_token(request.args.get('token'))
    dm_id = int(request.args.get('dm_id'))
    start = int(request.args.get('start'))
    response = msg.dm_messages_v1(user_id, dm_id, start)
    return dumps(response)

@APP.route("/message/send/v1", methods = ['POST'])
def message_send_v1():
    data = request.get_json()
    user_id = data_store.get_id_from_token(data['token'])
    channel_id = data['channel_id']
    message = data['message']
    response = msg.message_send_v1(user_id, channel_id, message)
    return dumps(response)

@APP.route("/message/senddm/v1", methods = ['POST'])
def message_senddm_v1():
    data = request.get_json()
    user_id = data_store.get_id_from_token(data['token'])
    dm_id = data['channel_id']
    message = data['message']
    response = msg.message_senddm_v1(user_id, dm_id, message)
    return dumps(response)

@APP.route("/message/edit/v1", methods = ['PUT'])
def message_edit_v1():
    data = request.get_json()
    user_id = data_store.get_id_from_token(data['token'])
    msg_id = data['message_id']
    message = data['message']
    response = msg.message_edit_v1(user_id, msg_id, message)
    return dumps(response)

@APP.route("/message/remove/v1", methods = ['DELETE'])
def message_remove_v1():
    data = request.get_json()
    user_id = data_store.get_id_from_token(data['token'])
    msg_id = data['message_id']
    response = msg.message_remove_v1(user_id, msg_id)
    return dumps (response)

# ================ /admin domain ===================
'''
@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_user_remove_v1():
    return dumps({})
'''
@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_userpermission_change_v1():
    request_data = request.get_json()
    auth_user_id = data_store.get_id_from_token(request_data['token'])
    u_id = request_data['u_id']
    permission_id = request_data['permission_id']
    response = admin.admin_userpermission_change_v1(auth_user_id, u_id,
                                                    permission_id)
    return dumps(response)

# ==================================================

# ================ /clear domain ===================
@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    clear_v1()
    return dumps({})

# ==================================================

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port, debug=False) # Do not edit this port
