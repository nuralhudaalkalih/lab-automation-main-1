
from models.User import User

class Admin(User):
    """
    CONCEPT — Inheritance:
        Admin IS-A User. It gets everything User has (user_id, username,
        check_password(), __str__(), etc.) for free, then adds its own behaviour.

        'class Admin(User)' means: Admin extends User.
        super().__init__(...) calls User's __init__ to set the shared attributes.
    """

    def __init__(self, user_id: int, username: str, password: str, role: str ="Admin"):
        """
        CONCEPT — super().__init__():
            Calls the parent (User) constructor. We hardcode role="Admin"
            because an Admin is always an Admin — no need to pass it in.
        """
        super().__init__(user_id, username, password, role="Admin")


    # Admin-only capabilities
    def can_manage_users(self) -> bool:
        return True

    def can_delete_samples(self) -> bool:
        return True

    def can_add_tests(self) -> bool:
        return True

    def __str__(self) -> str:
        return f"[Admin] {self.username}"