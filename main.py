from database.DatabaseManager import DatabaseManager

from controllers.AuthController import AuthController
from controllers.SampleController import SampleController
from controllers.TestController import TestController
from controllers.ReportController import ReportController


def main():

    # ── DB CONNECTION ─────────────────────
    db = DatabaseManager()

    # ── CONTROLLERS ───────────────────────
    auth = AuthController(db)
    sample = SampleController(db)
    test = TestController(db)
    report = ReportController(db)

    print("✔ System Started Successfully")


# ── RUN PROGRAM ───────────────────────────
if __name__ == "__main__":
    main()