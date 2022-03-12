"""
Shared Global fixturs
Runs before EVERY tests
"""

import pytest

from src.other import clear_v1

# Runs clean_v1() before all tests
@pytest.fixture(autouse=True)
def clean():
    clear_v1()
