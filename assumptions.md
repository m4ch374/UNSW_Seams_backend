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

- Return value of <user_profile_v1> is {'user': {'u_id': 'integer', 'email': 'string', 'name_first': 'string', 'name_last': 'string', 'handle_str': 'string'}}

- Return value of <users_all_v1> is {'users': [{'u_id': 'integer', 'email': 'string', 'name_first': 'string'....},
                                              {'u_id': 'integer', 'email': 'string', 'name_first': 'string'....},
                                              {'u_id': 'integer', 'email': 'string', 'name_first': 'string'....}]}

## **2. Assumptions - `message_remove.py (v2)`**

- Removed messages will never be edited/accessed again. Current implementation assigns removed messages to a channel_id of -1 which can never be accessed but retains the message as an item in the datastore list so generate_id will continue producing successive ids.

## **3. Assumptions - `dm/create/v1`**

- If the id of the creator is in list `u_ids`, it is also considered as duplicate u_ids, therefore raising `InputError`

# Iteration - 3

## **0. Assumptions **
- email: cs153122t1t15bant@unsw.com
- name: magicant
- password: unsw1531ant

- email: cs1531ant@gmail.com
- password: unsw1531ant

## **1. Assumptions - `reset_code` in `data_store` **

- inside of <reset_code> is: {"A reset code" : id}

## **2. Assumptions - `other.py`**

- clear() will also remove the images made by tests

- 'a_test.py' will change data_store to init state after tests
