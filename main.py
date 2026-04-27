from database.DatabaseManager import DatabaseManager

from controllers.AuthController import AuthController
from controllers.SampleController import SampleController
from controllers.TestController import TestController
from controllers.ReportController import ReportController


def main():

    db = DatabaseManager()

    auth = AuthController(db)
    sample = SampleController(db)
    test = TestController(db)
    report = ReportController(db)

    print("✔ System Started Successfully")

    # GUI 
    # app = MainGUI(auth, sample, test, report)
    # app.run()


if __name__ == "__main__":
    main()