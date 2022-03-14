# Asumptions

# Iteration - 1

## **1. General Assumptions**

- Assuming that all inputs provided will be in the correct format/order/numer (Other than those stated error cases in asignment specs)

- data_store structure:
  ```python
    data_store = {
        'users': [ ], # list of User() objects
        'channel': [ ], # list of Channel() objects
    }
  ```

## **2. Assumptions - `auth.py`**

- Assuming user id starts form `1` instead of `0`
- Accepts name with all special characters or whitespaces

## **3. Assumptions - `channels.py`**

- `channels_list_v1()` will list both `public` and `private` channels that the user is a part of
- `channels_listall_v1()` will list all channels from `data_store` therefore `auth_user_id` argument is unused.
- Assumes `owner` is also a `member` of the channel

## **4. Assumptions - `channel.py`**

- Assuming that message id 0 will always be valid, for the sake of current autotests. Subject to change later once an add messages function is implemented.
- Messages returned form `channel_messages_v1()` will always be an empty list as there are no function for adding messages implemented yet.

# Iteration - 2

## **1. Assumptions - `auth.py (v2)`**

- Return value of <login_v2> and <register_v2> is {'token': 'a string', 'auth_user_id' = integer}

- Return value of <user_profile_v1> is {'email'     : 'string',
                                        'password'  : 'string',
                                        'name_first': 'string',
                                        'name_last' : 'string',
                                        'id'        : 'integer',
                                        'handle'    : 'string',
                                        'channels'  : 'list',
                                        'owner'     : 'boolean',}

- Return value of <users_all_v1> is {'user 1': {'email': 'string', 'password': 'string'......},
                                    'user 2': {'email': 'string', 'password': 'string'......},
                                    'user 3': {'email': 'string', 'password': 'string'......},}
