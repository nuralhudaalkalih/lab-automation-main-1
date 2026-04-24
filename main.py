from database.DatabaseManager import DatabaseManager
from database.UserDAO import UserDAO
from database.SampleDAO import SampleDAO
from database.TestDAO import TestDAO
from database.ResultDAO import ResultDAO

from controllers.AuthController import AuthController
from controllers.SampleController import SampleController
from controllers.TestController import TestController
from controllers.ReportController import ReportController

db = DatabaseManager()

user_dao = UserDAO(db)
sample_dao = SampleDAO(db)
test_dao = TestDAO(db)
result_dao = ResultDAO(db)

auth = AuthController(user_dao)
sample_ctrl = SampleController(sample_dao)
test_ctrl = TestController(test_dao)
report_ctrl = ReportController(result_dao)