# import requests

# BASE_ADDRESS = 'http://localhost:'
# BASE_PORT = '20000'
# BASE_URL = BASE_ADDRESS + BASE_PORT
# REQUEST = "/user/profile/v1"
# URL = BASE_URL + REQUEST
# REGISTER = BASE_URL + "/auth/register/v2"

# def test_invalid_token():
#     response = requests.post(URL, json = {'token': '123123123123123'})
#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data == None

# def test_self_detail():
#     user = requests.post(REGISTER, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
#     user_data = user.json()
#     response = requests.post(URL, json = {'token': user_data['token'], 'id': user_data['id']})
#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data ==  {'id': 1, 'email': 'z5555555@ed.unsw.edu.au', 'name_first': 'William', 'name_last': 'Wu', 'handle': 'williamwu'}

# def test_other_detail():
#     user = requests.post(REGISTER, json = {'email': 'z8888888@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Russell', 'name_last': 'Wang'})
#     requests.post(REGISTER, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
#     user_data = user.json()
#     response = requests.post(URL, json = {'token': user_data['token'], 'id': 2})
#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data ==  {'id': 2, 'email': 'z5555555@ed.unsw.edu.au', 'name_first': 'William', 'name_last': 'Wu', 'handle': 'williamwu'}

# def test_error_id():
#     user = requests.post(REGISTER, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
#     user_data = user.json()
#     response = requests.post(URL, json = {'token': user_data['token'], 'id': 2})
#     assert response.status_code == 400

