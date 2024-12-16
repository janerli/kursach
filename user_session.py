class UserSession:
    def __init__(self):
        self.access_level = None

    def set_access_level(self, access_level):
        self.access_level = access_level

    def get_access_level(self):
        return self.access_level

session = UserSession()