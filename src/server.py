# Default Imports
import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src import channel


# Our own imports
import src.channels as chnls
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


@APP.route("/channel/details/v2", methods=['GET'])
def channel_details_v2():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    response = channel.channel_details_v1(token, channel_id)
    return dumps(response)

@APP.route("/channel/messages/v2", methods=['POST'])
def channel_details_v2():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')
    response = channel.channel_details_v1(token, channel_id, start)
    return dumps(response)
    


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

# ================ /clear domain ===================
@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    clear_v1()
    return dumps({})
# ==================================================

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port, debug=True) # Do not edit this port
