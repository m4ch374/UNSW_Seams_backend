import requests
from src.config import url

ENDPOINT_CLEAR = url + '/clear/v1'

"""
    discharge the change made by test in data_store
"""

def test_clear():
    requests.delete(ENDPOINT_CLEAR)
    pass
