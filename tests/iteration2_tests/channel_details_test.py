import requests

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = '8080'
BASE_URL = f'{BASE_ADDRESS}:{BASE_PORT}'

def test_channel_details_invalid_channel_id():
    response = requests.get(f'{BASE_URL}/channel/details/v2') # How to pass in token/channel_id for autotest?
    response_code = response.status_code
    assert response_code == 403
