# :book: Docs on Classes - Iteration 1

This is a quick doc on the classes that we currently have and how we use them in general.

## :computer: Current available classes

1. `Datastore()`
2. `User()`
3. `Channel()`

## :robot: Datastore()

As mentioned in `data_store.py`, `Datastore()` is a class that stores data for the backend, nothing much to talk about lol.

### :bookmark_tabs: Properties:

- `__store`: A dictionary contains key `users` and `channel`

    type: `dict`

    > Note: It is not recommended to access __store directly, but instead use data_store.get(), seen below.

### :construction_worker: Methods:

- `get()`: Returns property `__store`

    Example Usage:

    ```python
    data = data_store.get()
    user_list = data['users']
    ```

- `set(store: dict)`: Set `__store` as the given dict

    Example Usage:

    ```python
    data = data_store.get()
    user_list = data['users']
    user_list.append(new_user)
    data_store.set(data)
    ```

- `get_user(id: int)` Returns a `User()` object from id

    > Note: Assumes the given id is valid  
    > Returns None if there are no users in data_store

    Example Usage:

    ```python
    user = data_store.get_user(1)
    ```

- `get_channel(id: int)` Returns a `Channel()` object from id

    > Note: Assumes the given id is valid  
    > Returns None if there are no channel in data_store

    Example Usage:

    ```python
    channel = data_store.get_channel(1)
    ```

## :monkey: User()

`User()` is a class which represents a user, containing various details.

### :cherry_blossom: Initialization:

Example Usage:

`User()` takes in the following arguments:

- email : string
- password : string
- name_first : string
- name_last : string

```python
new_user = User('joe_mama@gmail.com', 'password', 'joe', 'mama')

# or

new_user = User(
    email='joe_mama@gmail.com',
    password='password',
    name_first='joe',
    name_last='mama'
)
```

### :bookmark_tabs: Properties:

- `email`: Represents the user's email (`string`)

- `passowrd`: Represents the user's password (`string`)

- `name_first`: Represents the user's first name (`string`)

- `name_last`: Represents the user's last name (`string`)

- `id`: Represents the user's id (`int`)

- `handle`: Represents the user's handle (`string`)

Example Usage:

```python
# To access a user's id
user_id = new_user.id

# If the user changes his email
new_user.email = new_email
```

### :construction_worker: Methods:

- `to_dict()`: Returns a dictionary representation of the user

    Example Usage:

    ```python
    def channel_details_v1(auth_user_id, channel_id):
        ...
        return {
            'name': 'Hayden',
            'owner_members': [usr.to_dict() for usr in owners], # here
            'all_members': [usr.to_dict() for usr in members],  # and here
        }
    ```

## :hammer: Channel()

`Channel()` is a class representing a channel.

### :cherry_blossom: Initialization:

`Channel()` takes in the following arguments:

- name : string
- owner: User()
- is_public: bool

Example Usage:

```python
auth_user_id = auth_register_v1(....)['auth_user_id']
new_channel = Channel('this is a name', data_store.get_user(auth_user_id), True)

# or

auth_user_id = auth_register_v1(....)['auth_user_id']
new_channel = Channel(
    name='this is a name',
    owner=data_store.get_user(auth_user_id),
    is_public=True
)
```

### :bookmark_tabs: Properties:

- `id`: Represents the channel's id (`int`)

- `name`: Represents the channel's name (`string`)

- `owners`: Represents the channel's owners (`list(User())`)

- `members`: Represents the channel's members (`list(User())`)

- `is_public`: Denotes whether the channel is a DM or not (`bool`)

Example Usage:

```python
# To access the channel's name
channel_name = new_channel.name

# To change the visibility of the channel
new_channel.is_public = False
```
### :construction_worker: Methods:

- `has_member(member: User())`: Returns a boolean, `True` if the channel has the said member, `False` otherwise

    Example Usage:

    ```python
    channel_has_member = new_channel.has_member(new_user)
    ```

- `has_member_id(member_id: int)`: Returns a boolean, `True` if the channel has the said member's id, `False` otherwise

    Example Usage:

    ```python
    channel_has_member = new_channel.has_member_id(1)
    ```

- `add_member(member: User())`: Adds the user to the channel

    Example Usage:

    ```python
    def channel_join_v1(auth_user_id, channel_id):
        chnl = data_store.get_channel(channel_id)
        chnl.add_member(data_store.get_user(auth_user_id)) # here

        return {
            ...
        }
    ```

- `add_member_id(member_id: int)`: Adds the user to the channel by user's id

    Example Usage:

    ```python
    def channel_join_v1(auth_user_id, channel_id):
        chnl = data_store.get_channel(channel_id)
        chnl.add_member_id(auth_user_id) # here

        return {
            ...
        }
    ```

- `channel_details_dict()`: A dictionary representation of Channel()

    Example Usage:

    ```python
    def channel_details_v1(auth_user_id, channel_id):
        chnl = data_store.get_channel(channel_id)
        return chnl.channel_details_dict()
    ```
