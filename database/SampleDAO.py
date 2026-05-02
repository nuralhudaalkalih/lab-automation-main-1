"""
SampleDAO.py
────────────

CONCEPTS LEARNED:
    - Auto-generating IDs in Python  : SQLite AUTOINCREMENT handles numeric IDs,
                                       but sample IDs like "S001" need Python logic.
    - LIKE operator                  : Pattern matching in SQL  (WHERE name LIKE '%doe%')
    - ORDER BY                       : Sorting results before returning them
    - COUNT()                        : Aggregate function — counts matching rows
    - Transactions                   : commit() saves; without it changes are temporary
    - rowcount                       : How many rows were affected by the last statement
"""

import sqlite3
from datetime import date


class SampleDAO:
    """
     Sample lifecycle:
        add_sample()  →  update_status("Processing")  →  update_status("Completed")
    """

    def __init__(self, db_manager):
        self.db = db_manager

    # ── ID Generation ─────────────────────────

    def generate_sample_id(self) -> str:
        """
        Automatically generates the next sample ID (S001, S002, S003 ...).

        CONCEPT — generating IDs in Python:
            We count existing rows, add 1, then format with zero-padding.
            zfill(3) pads with zeros: "1" → "001", "12" → "012"

        Example:
            If the table has 5 samples, the next ID will be "S006".
        """
        self.db.cursor.execute("SELECT COUNT(*) FROM Samples")
        count = self.db.cursor.fetchone()[0]   # [0] gets the integer from the row
        next_num = count + 1
        return "S" + str(next_num).zfill(3)    # e.g. "S001", "S042"

    # ── CREATE ────────────────────────────────

    def add_sample(self, patient_name: str, date_added: str = None) -> str:
        """
        Inserts a new sample and returns its auto-generated ID.

        Parameters:
            patient_name : The patient's full name
            date_added   : Date string "YYYY-MM-DD". Defaults to today if not given.

        Returns:
            The new sample_id string (e.g. "S003")

        CONCEPT — default parameter with None:
            We use None as default (not date.today()) because default values
            in function signatures are evaluated once at definition time,
            not each time the function runs. Using None + an if-check
            guarantees we always get today's actual date.
        """
        if date_added is None:
            date_added = str(date.today())

        sample_id = self.generate_sample_id()

        self.db.cursor.execute(
            """INSERT INTO Samples (sample_id, patient_name, date_added, status)
               VALUES (?, ?, ?, 'Pending')""",
            (sample_id, patient_name, date_added)
        )
        self.db.conn.commit()
        return sample_id   # caller can display "Sample S003 registered"

    # ── READ ──────────────────────────────────

    def get_by_id(self, sample_id: str):
        """
        Fetches one sample by its ID.
        Returns a sqlite3.Row or None if not found.
        """
        self.db.cursor.execute(
            "SELECT * FROM Samples WHERE sample_id = ?",
            (sample_id,)
        )
        return self.db.cursor.fetchone()

    def get_all_samples(self) -> list:
        """
        Returns all samples, newest first.

        CONCEPT — ORDER BY:
            Sorts the results before returning.
            DESC = descending (newest date at top)
            ASC  = ascending  (oldest at top, also the default)
        """
        self.db.cursor.execute(
            "SELECT * FROM Samples ORDER BY date_added DESC"
        )
        return self.db.cursor.fetchall()

    def get_by_status(self, status: str) -> list:
        """
        Returns all samples with a specific status.
        status must be one of: 'Pending', 'Processing', 'Completed'
        """
        self.db.cursor.execute(
            "SELECT * FROM Samples WHERE status = ? ORDER BY date_added ASC",
            (status,)
        )
        return self.db.cursor.fetchall()

    def search_by_patient(self, name_query: str) -> list:
        """
        Case-insensitive search by patient name (partial match supported).

        CONCEPT — LIKE and wildcards:
            % is a wildcard meaning "any characters".
            '%doe%' matches "John Doe", "Jane Doe", "Doe Smith" etc.
            LIKE is case-insensitive for ASCII in SQLite.

        Example:
            search_by_patient("john")  →  finds "John Doe", "Johnathan Smith"
        """
        self.db.cursor.execute(
            "SELECT * FROM Samples WHERE patient_name LIKE ?",
            (f"%{name_query}%",)   # wrap the search term in % wildcards
        )
    
        return self.db.cursor.fetchall()

    def get_by_date(self, date_str: str) -> list:
        """Returns all samples added on a specific date (format: 'YYYY-MM-DD')."""
        self.db.cursor.execute(
            "SELECT * FROM Samples WHERE date_added = ?",
            (date_str,)
        )
        return self.db.cursor.fetchall()

    def count_by_status(self) -> dict:

        """
        Returns a summary dictionary: how many samples are in each status.

        CONCEPT — GROUP BY and COUNT():
            GROUP BY collapses rows with the same value into one group.
            COUNT(*) counts how many rows are in each group.

            SQL result looks like:
                status       | COUNT(*)
                -------------|--------
                Pending      | 5
                Processing   | 2
                Completed    | 12

        Returns:
            {"Pending": 5, "Processing": 2, "Completed": 12}
        """
        self.db.cursor.execute(
            "SELECT status, COUNT(*) FROM Samples GROUP BY status"
        )
        rows = self.db.cursor.fetchall()
        return {row[0]: row[1] for row in rows}   # dict comprehension

    # ── UPDATE ────────────────────────────────

    def update_status(self, sample_id: str, new_status: str) -> bool:
        """
        Moves a sample through its lifecycle.

        Valid transitions:
            'Pending'  →  'Processing'  →  'Completed'

        Returns True if the sample was found and updated, False otherwise.
        """
        try:
            self.db.cursor.execute(
                "UPDATE Samples SET status = ? WHERE sample_id = ?",
                (new_status, sample_id)
            )
            self.db.conn.commit()
            return self.db.cursor.rowcount > 0
        except sqlite3.IntegrityError:
            # Raised if new_status violates the CHECK constraint
            return False

    # ── DELETE ────────────────────────────────

    def delete_sample(self, sample_id: str) -> bool:
        """
        Deletes a sample by ID.

        CONCEPT — CASCADE DELETE:
            Because we defined  ON DELETE CASCADE  on the Results table's
            foreign key, deleting a sample also automatically deletes all
            its results. SQLite handles this for us.
        """
        self.db.cursor.execute(
            "DELETE FROM Samples WHERE sample_id = ?",
            (sample_id,)
        )
        self.db.conn.commit()
        return self.db.cursor.rowcount > 0