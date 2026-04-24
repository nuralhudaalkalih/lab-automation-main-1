class TestController:
    def __init__(self, test_dao):
        self.test_dao = test_dao

    def create_test(self, test_name, description=None):
        return self.test_dao.add_test(test_name, description)

    def get_all_tests(self):
        return self.test_dao.get_all_tests()

    def get_test(self, test_id):
        return self.test_dao.get_by_id(test_id)

    def delete_test(self, test_id):
        return self.test_dao.delete_test(test_id)

    def load_default_tests(self):
        self.test_dao.add_default_tests()