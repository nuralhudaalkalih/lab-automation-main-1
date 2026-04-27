from database.UserDAO import UserDAO
from models.User import User


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

        row = self.dao.get_by_username(username)
        user = User.from_row(row)

        if user is None:
            return None

        if not user.check_password(password):
            return None

        return user  # login successful

    # ── GET USER ────────────────────────────────

    def get_user_by_username(self, username: str):

        if not username:
            return None

        row = self.dao.get_by_username(username)
        return User.from_row(row)

    # ── PASSWORD UPDATE ─────────────────────────

    def change_password(self, username: str, new_password: str) -> bool:

        if not username or not new_password:
            return False

        return self.dao.update_password(username, new_password)

    # ── ROLE UPDATE ─────────────────────────────

    def change_role(self, username: str, new_role: str) -> bool:

        valid_roles = ["Admin", "Technician"]

        if new_role not in valid_roles:
            return False

        return self.dao.update_role(username, new_role)

    # ── DELETE USER ─────────────────────────────

    def delete_user(self, username: str) -> bool:

        if not username:
            return False

        return self.dao.delete_user(username)