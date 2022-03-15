# import requests

# BASE_ADDRESS = 'http://localhost:'
# BASE_PORT = '20000'
# BASE_URL = BASE_ADDRESS + BASE_PORT
# REQUEST = "/auth/logout/v1"
# URL = BASE_URL + REQUEST
# REGISTER = BASE_URL + "/auth/register/v2"
# LOGIN = BASE_URL + "/auth/login/v2"

# def test_register_logout():
#     user = requests.post(REGISTER, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Donald', 'name_last': 'Trump'})
#     user_data = user.json()
#     response = requests.post(URL, json = {'token': user_data['token']})
#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data == {}

# def test_login_logout():
#     user = requests.post(REGISTER, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Donald', 'name_last': 'Trump'})
#     user_data = user.json()
#     requests.post(URL, json = {'token': user_data['token']})
#     user = requests.post(LOGIN, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '123123123'})
#     user_data = user.json()
#     response = requests.post(URL, json = {'token': user_data['token']})
#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data == {}

