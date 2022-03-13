# :bowling: Docs on Shared Fixtures - Iteration 2

This is a quick doc to explain how shared fixtures was done

## :dollar: Sharing Fixtures between different files

So what I've seen in the test files for `iteration 1` is that fixtures like `first_user_and_channel()` was used in both `channel_test.py` and `messages_test.py`.

And given that we're gonna split the test files to function based instead of module based, there's no way we're gonna `Ctrl+C` and `Ctrl+V` our way through.

So, to overcome this, we need a way to share fixtures, to do that, we could create a file called `conftest.py`. Say we have a file structure as such:
```
tests
├── __init__.py
├── iteration1_tests
|   ├── conftest.py     # here's the conftest
|   ├── channels_test
|   |   ├── channels_test.py
|   ├── auth_test
|   |   ├── auth_test.py
|   ├── other_test.py
├── iteration2_tests
|   |── stubbed_test.py
```

Content of `conftest.py`:
```python
@pytest.fixture
def gimme_id():
    return 1
```

With this, any `.py` file could access the fixture `gimme_id()` inside directory `iteration1_tests` without importing, including the files in the sub-folders i.e. `channels_test.py` and `auth_test.py`.

In practise, to call the fixture:

```python
# We dont even need to import fixtures! Wow! xd
import pytest
from channels import channels_list_v1

# We could just use it directly and it works via magic
def some_test(gimme_id):
    with pytest.raises(Exception):
        channels_list_v1(gimme_id)
```

## :eyes: Running a function before every tests

Another thing I've spotted is that we call `clear_v1()` every time we write a new test, which creates alot of repeated code.

So to run `clear_v1()` before every tests, we need to utilize the `autouse` keyword:

```python
import pytest

@pytest.fixture(autouse=True)
def clear():
    clear_v1()
```

`Pytest` will run `clear()` before every tests, put it in `conftest.py` for maximum laziness.

----

Authored by `Henry Wan`
