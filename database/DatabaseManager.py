import sqlite3
class DatabaseManager:
    def __init__(self, db_path="lab.db"):
        self.db_path = db_path
        self.conn= sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;") # Enable foreign key constraints which are off by default in SQLite
        self.conn.row_factory=sqlite3.Row #ACCESS TO COLUMNS BY NAME instead of index
        self.cursor=self.conn.cursor() #execute sql commands
        self.create_tables()
    def create_tables(self):
        # executescript allows us to execute multiple SQL statements at once
        self.cursor.executescript("""
            -- 'role' is constrained to only two valid strings.
            CREATE TABLE IF NOT EXISTS Users (
                user_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                username  TEXT    NOT NULL UNIQUE,
                password  TEXT    NOT NULL,
                role      TEXT    NOT NULL CHECK(role IN ('Admin', 'Technician'))
            );

            -- One row per patient sample received by the lab.
            -- sample_id is set manually (e.g. "S001") instead of AUTOINCREMENT for convetion
            CREATE TABLE IF NOT EXISTS Samples (
                sample_id    TEXT PRIMARY KEY,
                patient_name TEXT NOT NULL,
                date_added   TEXT NOT NULL,
                status       TEXT NOT NULL DEFAULT 'Pending'
                             CHECK(status IN ('Pending','Processing','Completed'))
            );
 
            
            -- A catalogue of all test types the lab can perform.
            -- example: CBC, Urinalysis, COVID-19 PCR, TSH
            CREATE TABLE IF NOT EXISTS Tests (
                test_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                test_name   TEXT    NOT NULL UNIQUE,
                description TEXT
            );

            -- Links a Sample to a Test and stores the measured value.
            -- One sample can have many results (one per test performed on it).
                CREATE TABLE IF NOT EXISTS Results (
                result_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                sample_id    TEXT    NOT NULL,
                test_id      INTEGER NOT NULL,
                result_value TEXT,
                FOREIGN KEY (sample_id) REFERENCES Samples(sample_id)
                    ON DELETE CASCADE,
                --cascasde delete: if a parent row is deleted all choldren rows are deleted as well
                FOREIGN KEY (test_id)   REFERENCES Tests(test_id)
                    ON DELETE RESTRICT
                -- restrict: prevents the deletion of a parent row if it has any child rows referencing it
            );
        """)
        self.conn.commit()
 

 
    def close(self):
        self.conn.close()
 
    def get_db_path(self):
        """Returns the absolute path of the database file (useful for debugging)."""
        return os.path.abspath(self.db_path)