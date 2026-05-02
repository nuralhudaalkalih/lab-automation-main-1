"""
TestDAO.py
──────────
CONCEPT: Managing the test catalogue
    The Tests table is a reference catalogue — it lists every type of test
    the lab can perform. Tests are created once by an Admin and then
    assigned to samples repeatedly.

    This is a "lookup table" or "reference table" pattern: it holds
    stable data that other tables point to (Results.test_id → Tests.test_id).

CONCEPTS LEARNED:
    - lastrowid     : Gets the auto-generated ID of the row just inserted
    - Reference data: Some tables hold configuration/catalogue data, not
                      transactional data. Tests rarely change; Results change daily.
    - fetchall()    : Always returns a list, even when empty
"""

import sqlite3


class TestDAO:
    """
    Handles all Create, Read, Update, Delete operations for the Tests table.

    The Tests table is a catalogue of available test types, for example:
        test_id=1  name="CBC"            desc="Complete Blood Count"
        test_id=2  name="Urinalysis"     desc="Full urine panel"
        test_id=3  name="COVID-19 PCR"   desc="Nasal swab PCR"
        test_id=4  name="TSH"            desc="Thyroid Stimulating Hormone"

    Admins populate this table. Technicians pick from it when assigning tests.
    """

    def __init__(self, db_manager):
        self.db = db_manager

    # ── CREATE ────────────────────────────────

    def add_test(self, test_name: str, description: str = "") -> int:
        """
        Adds a new test type to the catalogue.

        CONCEPT — lastrowid:
            After an INSERT with AUTOINCREMENT, SQLite assigns the new row an ID.
            cursor.lastrowid gives us that ID immediately after the insert.
            We return it so the caller can use it right away (e.g. to link a result).

        Returns:
            The new test_id (integer), or -1 if the test name already exists.
        """
        try:
            self.db.cursor.execute(
                "INSERT INTO Tests (test_name, description) VALUES (?, ?)",
                (test_name, description)
            )
            self.db.conn.commit()
            return self.db.cursor.lastrowid   # the auto-generated test_id

        except sqlite3.IntegrityError:
            # test_name is UNIQUE — duplicate names are rejected
            return -1

    def add_default_tests(self):
        """
        Seeds the Tests table with the standard lab test catalogue.
        Safe to call multiple times — duplicates are silently ignored.

        This is called a 'seed' or 'fixture' — pre-loading known good data
        so the app is usable immediately after installation.
        """
        default_tests = [
            # Blood tests
            ("CBC",               "Complete Blood Count — Hemoglobin, WBC, Platelets"),
            ("Blood Glucose",     "Measures blood sugar level (fasting or random)"),
            ("Cholesterol",       "Total cholesterol, LDL, HDL, Triglycerides"),
            ("Hemoglobin",        "Single hemoglobin value measurement"),
            # Urine tests
            ("Urinalysis",        "pH, Protein, Glucose, Nitrites — full urine panel"),
            ("Urine Protein",     "Detects abnormal protein levels in urine"),
            ("Urine Glucose",     "Checks for glucose presence in urine"),
            # Viral / swab tests
            ("COVID-19 PCR",      "Nasal swab — PCR method, Positive or Negative"),
            ("Rapid Antigen",     "Nasal swab — rapid antigen test"),
            ("Influenza A/B",     "Tests for Influenza A and B strains"),
            # Hormone tests
            ("TSH",               "Thyroid Stimulating Hormone — mIU/L"),
            ("T3",                "Triiodothyronine thyroid hormone"),
            ("T4",                "Thyroxine thyroid hormone"),
            ("Insulin",           "Fasting insulin level"),
        ]

        for name, desc in default_tests:
            self.add_test(name, desc)   # duplicates return -1, that's fine

    # ── READ ──────────────────────────────────

    def get_by_id(self, test_id: int):
        """
        Fetches one test by its numeric ID.
        Returns a sqlite3.Row or None.
        """
        self.db.cursor.execute(
            "SELECT * FROM Tests WHERE test_id = ?",
            (test_id,)
        )
        return self.db.cursor.fetchone()

    def get_by_name(self, test_name: str):
        """
        Fetches one test by its exact name.
        Useful for checking if a test already exists before adding it.
        """
        self.db.cursor.execute(
            "SELECT * FROM Tests WHERE test_name = ?",
            (test_name,)
        )
        return self.db.cursor.fetchone()

    def get_all_tests(self) -> list:
        """
        Returns all test types, sorted alphabetically by name.
        Used to populate dropdown menus in the GUI.
        """
        self.db.cursor.execute(
            "SELECT * FROM Tests ORDER BY test_name ASC"
        )
        return self.db.cursor.fetchall()

    def get_test_names(self) -> list:
        """
        Returns just the names as a plain Python list of strings.
        Convenient for populating tkinter OptionMenu / Combobox widgets.

        Example:
            names = test_dao.get_test_names()
            # ["Blood Glucose", "CBC", "Cholesterol", ...]
            combo['values'] = names
        """
        self.db.cursor.execute(
            "SELECT test_name FROM Tests ORDER BY test_name ASC"
        )
        rows = self.db.cursor.fetchall()
        return [row["test_name"] for row in rows]   # list comprehension

    def search_tests(self, query: str) -> list:
        """
        Partial name search. Useful for a search-as-you-type feature.
        """
        self.db.cursor.execute(
            "SELECT * FROM Tests WHERE test_name LIKE ?",
            (f"%{query}%",)
        )
        return self.db.cursor.fetchall()

    # ── UPDATE ────────────────────────────────

    def update_test(self, test_id: int, test_name: str, description: str) -> bool:
        """Updates the name and description of an existing test."""
        try:
            self.db.cursor.execute(
                "UPDATE Tests SET test_name = ?, description = ? WHERE test_id = ?",
                (test_name, description, test_id)
            )
            self.db.conn.commit()
            return self.db.cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False   # new name clashes with an existing test name

    # ── DELETE ────────────────────────────────

    def delete_test(self, test_id: int) -> bool:
        """
        Deletes a test type from the catalogue.

        NOTE: Because Results has ON DELETE RESTRICT on test_id, this will
        FAIL if any results are already linked to this test.
        That's intentional — we don't want orphaned results.
        """
        try:
            self.db.cursor.execute(
                "DELETE FROM Tests WHERE test_id = ?",
                (test_id,)
            )
            self.db.conn.commit()
            return self.db.cursor.rowcount > 0
        except sqlite3.IntegrityError:
            # RESTRICT prevents deletion if results reference this test
            return False