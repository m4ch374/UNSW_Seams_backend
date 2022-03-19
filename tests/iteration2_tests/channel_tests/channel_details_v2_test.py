# Imports
import requests

# Import errors
from src.error import InputError, AccessError

# Import definitions
from tests.iteration2_tests.channels_tests.definitions import ERROR_LIST, NAMES_LIST
from tests.iteration2_tests.channels_tests.definitions import INVALID_TOKEN
from tests.iteration2_tests.endpoints import ENDPOINT_CREATE_CHNL, ENDPOINT_CHANNEL_DETAILS

# Import helpers
from tests.iteration2_tests.helper import generate_channel_input_json

# test that error is thrown when channel id does not extis
# When a valid user but invalid channel is sent  should return 403 code
# create valid user
# create valid channel
# send valid user and invalid channel
# assert
def test_channel_details_invalid_channel_id(user_made_channel):
    token = user_made_channel['token']
    channel = user_made_channel['channel']

    response = requests.get(f'{ENDPOINT_CHANNEL_DETAILS}?token={token}?channel_id={channel}') 
    response_code = response.status_code
    assert response_code == 403

