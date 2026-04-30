"""

CONCEPT: Model classes vs DAO classes
    ┌──────────────────────────────────────────────────────────┐
    │  DAO class  : knows about the DATABASE (SQL, sqlite3)    │
    │  Model class: knows about the DATA (attributes, logic)   │
    └──────────────────────────────────────────────────────────┘

    A DAO fetches a raw sqlite3.Row from the database.
    A Model wraps that row in a Python object with attributes and methods.

    Without models:
        user = user_dao.get_by_username("admin")
        print(user["role"])          ← raw dict access everywhere

    With models:
        user = User.from_row(user_dao.get_by_username("admin"))
        print(user.role)             ← clean attribute access
        print(user.is_admin())       ← meaningful method

CONCEPTS LEARNED:
    - Class attributes   : Variables that belong to every instance (self.name)
    - __str__            : What Python prints when you do print(obj) # To-String method in Java
    - __repr__           : Technical string for debugging
    - Inheritance        : Admin and Technician extend User (reuse + specialise)
    - super().__init__() : Calls the parent class constructor
    - @classmethod       : A factory method — creates an instance from a row
    - @property          : Getter that looks like an attribute (no parentheses)
    - Encapsulation      : Grouping related data and behaviour in one class
"""


class User:
    """
    Represents one row from the Users table as a Python object.

    CONCEPT — Base class:
        User holds everything common to all user types.
        Admin and Technician inherit from User and add their own behaviour.
        This avoids repeating the same __init__ code in both subclasses.
    """

    def __init__(self, user_id: int, username: str, password: str, role: str):
        """
        CONCEPT — Instance attributes (self.x):
            Each User object gets its own copy of these values.
            self.username for user A is completely separate from self.username for user B.
        """
        self.user_id  = user_id
        self.username = username
        self.password = password   # in a real system, store a hash, not plain text
        self.role     = role

    # ── Factory method ────────────────────────

    @classmethod
    def from_row(cls, row):
        """
        CONCEPT — @classmethod as a factory:
            Instead of User(row[0], row[1], ...), we write User.from_row(row).
            'cls' refers to the class itself (User, Admin, or Technician).
            from_row handles None gracefully — returns None instead of crashing.

        Usage:
            row  = user_dao.get_by_username("admin")   # sqlite3.Row
            user = User.from_row(row)                  # User object or None
        """
        if row is None:
            return None
        return cls(
            user_id  = row["user_id"],
            username = row["username"],
            password = row["password"],
            role     = row["role"]
        )

    def is_admin(self) -> bool:
        """Returns True if this user has the Admin role."""
        return self.role == "Admin"

    def is_technician(self) -> bool:
        """Returns True if this user has the Technician role."""
        return self.role == "Technician"

    def check_password(self, entered_password: str) -> bool:
        """
        Verifies a login attempt.
        In a production system you'd compare hashed passwords here.
        """
        return self.password == entered_password

  
# ── Helper: create the right subclass from a database row ─────

    @staticmethod
    def create_user_from_row(row) -> 'User':
        """
        Factory function — reads the role from the row and returns
        the correct subclass (Admin or Technician).
        """
        if row is None:
            return None
            
        role = row["role"]
        if role == "Admin":
            return Admin.from_row(row)
        elif role == "Technician":
            return Technician.from_row(row)
        else:
            return User.from_row(row)
    # ── String representations ─────────────────

    def __str__(self) -> str:
        """
        CONCEPT — __str__:
            Called by print() and str(). Should be human-readable.
        """
        return f"[{self.role}] {self.username} (ID: {self.user_id})"

    def __repr__(self) -> str:
        """
        CONCEPT — __repr__:
            Called in the Python console and for debugging.
            Should be unambiguous and technical.
        """
        return f"User(id={self.user_id}, username='{self.username}', role='{self.role}')"




