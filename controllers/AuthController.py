from database.UserDAO import UserDAO


class AuthController:

    def __init__(self, db_manager):
        self.dao = UserDAO(db_manager)

    # ── REGISTER ────────────────────────────────

    def register(self, username: str, password: str, role: str) -> bool:
        if not username or not password:
            raise ValueError("Username and password cannot be empty")

        if self.dao.username_exists(username):
            return False

        return self.dao.add_user(username, password, role)

    # ── LOGIN ──────────────────────────────────

    def login(self, username: str, password: str):
        if not username or not password:
            return None

        user = self.dao.get_by_username(username)

        if user is None:
            return None

        if user["password"] != password:
            return None

        return user  # login successful

    # ── USER CHECKS ───────────────────────────

    def user_exists(self, username: str) -> bool:
        return self.dao.username_exists(username)

    def get_user(self, username: str):
        return self.dao.get_by_username(username)

    # ── UPDATE PASSWORD ────────────────────────

    def change_password(self, username: str, new_password: str) -> bool:
        if not username or not new_password:
            return False

        return self.dao.update_password(username, new_password)

    # ── ROLE MANAGEMENT ────────────────────────

    def change_role(self, username: str, new_role: str) -> bool:
        valid_roles = ["Admin", "Technician"]

        if new_role not in valid_roles:
            return False

        return self.dao.update_role(username, new_role)

    # ── DELETE USER ────────────────────────────

    def delete_user(self, username: str) -> bool:
        if not username:
            return False

        return self.dao.delete_user(username)