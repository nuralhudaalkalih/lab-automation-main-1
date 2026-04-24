class AuthController:
    def __init__(self, user_dao):
        self.user_dao = user_dao

    def register(self, username, password, role):
        if self.user_dao.username_exists(username):
            return False, "Username already exists"

        success = self.user_dao.add_user(username, password, role)
        if success:
            return True, "User created successfully"
        return False, "Invalid role or error"

    def login(self, username, password):
        user = self.user_dao.get_by_username(username)

        if not user:
            return False, "User not found"

        if user["password"] != password:
            return False, "Wrong password"

        return True, user  