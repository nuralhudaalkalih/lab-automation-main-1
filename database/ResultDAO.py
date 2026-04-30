"""
ResultDAO.py
────────────
CONCEPT: 
    Results is the "junction table" of the system — it sits between Samples
    and Tests, linking them together with a measured value.

    A plain SELECT on Results returns raw IDs (sample_id="S001", test_id=3)
    which aren't human-readable. JOINs let us combine data from multiple tables
    so we get "John Doe | CBC | Hemoglobin=13.5 g/dL" in one query.

CONCEPTS LEARNED:
    - JOIN (INNER JOIN) : Combines rows from two tables where IDs match
    - Multiple JOINs    : Chain as many as needed (we join both Samples and Tests)
    - Aliases (AS)      : Rename columns in the result set for clarity
    - lastrowid         : Get the new result_id after inserting
    - One-to-many       : One sample can have many results (one per test)
"""

import sqlite3


class ResultDAO:
    """
    Handles all Create, Read, Update, Delete operations for the Results table.

    The Results table is the "junction" between Samples and Tests:

        Samples ──────┐
                       ├── Results (sample_id, test_id, result_value)
        Tests  ────────┘

    One sample can have multiple results (one per test performed on it).
    """

    def __init__(self, db_manager):
        self.db = db_manager

    # ── CREATE ────────────────────────────────

    def add_result(self, sample_id: str, test_id: int, result_value: str) -> int:
        """
        Records a test result for a specific sample.

        Parameters:
            sample_id    : e.g. "S001"
            test_id      : the integer ID from the Tests table
            result_value : the measured value as text, e.g. "13.5 g/dL"

        Returns:
            The new result_id (integer), or -1 if the foreign keys are invalid.

        CONCEPT — Foreign Key enforcement:
            If sample_id "S999" doesn't exist in Samples, SQLite raises
            IntegrityError because of the FOREIGN KEY constraint we defined.
            This prevents "orphan" results that point to nothing.
        """
        try:
            self.db.cursor.execute(
                """INSERT INTO Results (sample_id, test_id, result_value)
                   VALUES (?, ?, ?)""",
                (sample_id, test_id, result_value)
            )
            self.db.conn.commit()
            return self.db.cursor.lastrowid

        except sqlite3.IntegrityError as e:
            print(f"[ResultDAO] Could not insert result: {e}")
            return -1

    # ── READ (with JOINs) ─────────────────────

    def get_by_sample(self, sample_id: str) -> list:
        """
        Fetches all results for one sample, with test names included.

        CONCEPT — INNER JOIN:
            Two tables are combined into one result set wherever their IDs match.

            Results table:           Tests table:
            result_id | test_id      test_id | test_name
            ───────────────────      ──────────────────────
            1         | 3            3       | CBC
            2         | 5            5       | Urinalysis

            After JOIN, you get one combined row:
            result_id | test_id | test_name  | result_value
            ─────────────────────────────────────────────────
            1         | 3       | CBC        | Hemoglobin=13.5

            We use  r.  and  t.  prefixes to avoid ambiguity when both
            tables share a column name (both have an "id" column).

        Returns list of rows with columns:
            result_id, sample_id, patient_name, test_name, result_value
        """
        self.db.cursor.execute(
            """
            SELECT
                r.result_id,
                r.sample_id,
                s.patient_name,
                t.test_name,
                r.result_value
            FROM Results r
            INNER JOIN Samples s ON r.sample_id = s.sample_id
            INNER JOIN Tests   t ON r.test_id   = t.test_id
            WHERE r.sample_id = ?
            ORDER BY r.result_id ASC
            """,
            (sample_id,)
        )
        return self.db.cursor.fetchall()


    def get_all_results(self) -> list:
        
        """
        Returns every result in the system, enriched with patient and test names.

        CONCEPT — Multiple JOINs:
            We JOIN three tables in one query.
            FROM Results r           ← start here
            JOIN Samples s ON ...    ← pull in patient_name
            JOIN Tests   t ON ...    ← pull in test_name

        Returns list of rows with columns:
            result_id, sample_id, patient_name, test_name, result_value
        """
        self.db.cursor.execute(
            """
            SELECT
                r.result_id,
                r.sample_id,
                s.patient_name,
                t.test_name,
                r.result_value
            FROM Results r
            INNER JOIN Samples s ON r.sample_id = s.sample_id
            INNER JOIN Tests   t ON r.test_id   = t.test_id
            ORDER BY r.result_id DESC
            """
        )
        return self.db.cursor.fetchall()

    def get_by_id(self, result_id: int):
        """Fetches one result row by result_id, with full join data."""
        self.db.cursor.execute(
            """
            SELECT
                r.result_id,
                r.sample_id,
                s.patient_name,
                t.test_name,
                r.result_value
            FROM Results r
            INNER JOIN Samples s ON r.sample_id = s.sample_id
            INNER JOIN Tests   t ON r.test_id   = t.test_id
            WHERE r.result_id = ?
            """,
            (result_id,)
        )
        return self.db.cursor.fetchone()

    def get_by_test_name(self, test_name: str) -> list:
        """
        Fetches all results for a specific test type (e.g. all CBC results).
        Useful for generating trend reports across patients.
        """
        self.db.cursor.execute(
            """
            SELECT
                r.result_id,
                r.sample_id,
                s.patient_name,
                t.test_name,
                r.result_value
            FROM Results r
            INNER JOIN Samples s ON r.sample_id = s.sample_id
            INNER JOIN Tests   t ON r.test_id   = t.test_id
            WHERE t.test_name = ?
            ORDER BY s.date_added DESC
            """,
            (test_name,)
        )
        return self.db.cursor.fetchall()

    def sample_has_results(self, sample_id: str) -> bool:
        """Returns True if any results have been entered for this sample."""
        self.db.cursor.execute(
            "SELECT 1 FROM Results WHERE sample_id = ?",
            (sample_id,)
        )
        return self.db.cursor.fetchone() is not None

    # ── UPDATE ────────────────────────────────

    def update_result_value(self, result_id: int, new_value: str) -> bool:
        """
        Corrects a result value (e.g. if a technician entered the wrong number).

        Returns True if the result was found and updated.
        """
        self.db.cursor.execute(
            "UPDATE Results SET result_value = ? WHERE result_id = ?",
            (new_value, result_id)
        )
        self.db.conn.commit()
        return self.db.cursor.rowcount > 0

    # ── DELETE ────────────────────────────────

    def delete_result(self, result_id: int) -> bool:
        """Removes one result entry by its ID."""
        self.db.cursor.execute(
            "DELETE FROM Results WHERE result_id = ?",
            (result_id,)
        )
        self.db.conn.commit()
        return self.db.cursor.rowcount > 0

    def delete_results_for_sample(self, sample_id: str) -> int:
        """
        Removes ALL results for a given sample.
        Returns the number of rows deleted.

        NOTE: This normally happens automatically via CASCADE DELETE
        when the sample itself is deleted. Call this only if you want
        to clear results while keeping the sample record.
        """
        self.db.cursor.execute(
            "DELETE FROM Results WHERE sample_id = ?",
            (sample_id,)
        )
        self.db.conn.commit()
        return self.db.cursor.rowcount