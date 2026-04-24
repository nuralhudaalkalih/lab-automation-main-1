"""
UserDAO.py
──────────
CONCEPT: Data Access Object (DAO) Pattern
    A DAO is a class whose ONLY job is to talk to ONE table in the database.
    UserDAO handles ONLY the Users table — nothing else.

    This separation matters because:
        - Your teammate building AuthController doesn't need to know any SQL.
          They just call  user_dao.get_by_username("admin")  and get a result.
        - If the database structure changes, only this file needs editing —
          not every place in the project that uses users.

CONCEPTS LEARNED:
    - Parameterised queries  : Using ? placeholders instead of f-strings (prevents SQL injection)
    - fetchone()             : Returns exactly one row, or None if nothing matched
    - fetchall()             : Returns a list of all matching rows (empty list if none)
    - IntegrityError         : SQLite raises this when a UNIQUE or NOT NULL constraint is broken
    - sqlite3.Row            : Lets you do row["username"] — set in DatabaseManager
    - None checks            : Always check if fetchone() returned None before using it
"""

import sqlite3


class UserDAO:

    def __init__(self, db_manager):
        """
        Receives the shared DatabaseManager instead of creating its own connection.
        This is called 'Dependency Injection' — the connection is injected from outside.
        All five DAOs share the same db_manager object (one connection to the file).
        """
        self.db = db_manager

    # ── CREATE ────────────────────────────────
    # function signature that specifies the types of the parameters and return value 
    def add_user(self, username: str, password: str, role: str) -> bool:
        """
        Inserts a new user into the Users table.

        CONCEPT — Parameterised query:
            The ? marks are placeholders. sqlite3 fills them in safely,
            preventing SQL injection. NEVER use f-strings or + to build SQL.

            SAFE   → cursor.execute("... WHERE username = ?", (username,)) #input interpreted as data, not sql code
            UNSAFE → cursor.execute(f"... WHERE username = '{username}'")

        Returns:
            True  if the user was created successfully
            False if the username already exists (UNIQUE constraint violated)
        """
        try:
            self.db.cursor.execute(
                "INSERT INTO Users (username, password, role) VALUES (?, ?, ?)",
                (username, password, role)
            )
            self.db.conn.commit()
            return True

        except sqlite3.IntegrityError:
            # Raised when username already exists (UNIQUE) or role is invalid (CHECK)
            return False

    # ── READ ──────────────────────────────────

    def get_by_username(self, username: str):
        """
        Fetches one user row by username.

        CONCEPT — fetchone():
            Returns the first matching row as a sqlite3.Row object,
            or None if no match was found. Always check for None before use!

        Example:
            user = user_dao.get_by_username("admin")
            if user:                          # None check
                print(user["role"])           # column access by name
        """
        
        self.db.cursor.execute(
            "SELECT * FROM Users WHERE username = ?",
            (username,)
        )
        return self.db.cursor.fetchone()   # sqlite3.Row or None

    def get_by_id(self, user_id: int):
        """Fetches one user row by their numeric ID."""
        self.db.cursor.execute(
            "SELECT * FROM Users WHERE user_id = ?",
            (user_id,)
        )
        return self.db.cursor.fetchone()

    def get_all_users(self) -> list:
        """
        Returns every row in the Users table.

        CONCEPT — fetchall():
            Returns a list of sqlite3.Row objects.
            If the table is empty, returns an empty list [] — never None.

        Example:
            for user in user_dao.get_all_users():
                print(user["username"], user["role"])
        """
        self.db.cursor.execute("SELECT * FROM Users")
        return self.db.cursor.fetchall()

    def get_all_by_role(self, role: str) -> list:
        """Returns only users with the given role ('Admin' or 'Technician')."""
        self.db.cursor.execute(
            "SELECT * FROM Users WHERE role = ?",
            (role,)
        )
        return self.db.cursor.fetchall()

    def username_exists(self, username: str) -> bool:
        """Quick check — returns True if the username is already taken."""
        self.db.cursor.execute(
            "SELECT 1 FROM Users WHERE username = ?",
            (username,)
        )
        return self.db.cursor.fetchone() is not None

    # ── UPDATE ────────────────────────────────

    

    def update_password(self, username: str, new_password: str) -> bool:
        """
        Changes the password for an existing user.

        CONCEPT — UPDATE statement:
            Always use WHERE in an UPDATE. Without it, EVERY row gets changed.
            rowcount tells us how many rows were actually affected.
        """
        self.db.cursor.execute(
            "UPDATE Users SET password = ? WHERE username = ?",
            (new_password, username)
        )
        self.db.conn.commit()
        return self.db.cursor.rowcount > 0   # True if a row was found and updated

    def update_role(self, username: str, new_role: str) -> bool:
        """Changes the role for an existing user (Admin only action)."""
        try:
            self.db.cursor.execute(
                "UPDATE Users SET role = ? WHERE username = ?",
                (new_role, username)
            )
            self.db.conn.commit()
            return self.db.cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False   # new_role was not 'Admin' or 'Technician'

    # ── DELETE ────────────────────────────────

    def delete_user(self, username: str) -> bool:
        """
        Removes a user by username.

        Returns True if a row was deleted, False if the username didn't exist.
        """
        self.db.cursor.execute(
            "DELETE FROM Users WHERE username = ?",
            (username,)
        )
        self.db.conn.commit()
        return self.db.cursor.rowcount > 0