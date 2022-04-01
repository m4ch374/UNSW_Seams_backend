"""
Fixtures for iteration 3
"""

# Imports
import pytest
import requests

# Import definitions
from tests.iteration3_tests.endpoints import ENDPOINT_CLEAR

# ==================================================

@pytest.fixture(autouse=True)
def clear():
    requests.delete(ENDPOINT_CLEAR)

