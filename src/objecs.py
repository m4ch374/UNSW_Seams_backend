# This python file contains all custom objects and classes
# besides the given ones

class User:
    def __init__(self, email, password, name_first, name_last, id, handle):
        self.email = email
        self.password = password
        self.name_first = name_first
        self.name_last = name_last
        self.id = id
        self.handle = handle

    def __eq__(self, other):
        return all(
            [
                self.email == other.email,
                self.password == other.password,
                self.name_first == other.name_first,
                self.name_last == other.name_last,
                self.id == other.id,
                self.handle == other.handle
            ]
        )

    def to_dict(self):
        return_dict = {
            'u_id': int(self.id),
            'email': str(self.email),
            'name_first': str(self.name_first),
            'name_last': str(self.name_last),
            'handle_str': str(self.handle),
        }
        return return_dict

class Channel:
    def __init__(self, id, name, owners, is_public):
        self.id = id
        self.name = name
        self.owners = [owners]
        self.members = [owners]
        self.is_public = is_public

    # Might need it someday
    # def __eq__(self, other):
    #     return all(
    #         [
    #             self.id == other.id,
    #             self.name == other.name,
    #             len(set(self.owners) ^ set(other.owners)) == 0,  # Same owners
    #             len(set(self.members) ^ set(other.members)) == 0,
    #             self.is_public == other.is_public
    #         ]
    #     )

    def has_member(self, member):
        return member in self.members

    def to_dict(self):
        return_dict = {
            'name': self.name,
            'owner_members': self.owners,
            'all_members': self.members,
        }
        return return_dict