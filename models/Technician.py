from models.User import User
class Technician(User):
    """
    CONCEPT — Polymorphism:
        Admin and Technician both have is_admin() and check_password() from User,
        but Technician.can_manage_users() returns False while Admin's returns True.
        Same method name, different behaviour depending on the type — that's polymorphism.
    """

    def __init__(self, user_id: int, username: str, password: str, role: str ="Technician"):
        super().__init__(user_id, username, password, role="Technician")


    def can_add_samples(self) -> bool:
        return True

    def can_enter_results(self) -> bool:
        return True

    def can_manage_users(self) -> bool:
        return False   # only Admins can manage users

    def can_delete_samples(self) -> bool:
        return False

    def __str__(self) -> str:
        return f"[Technician] {self.username}"



