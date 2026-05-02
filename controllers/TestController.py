from database.TestDAO import TestDAO
from models.Test import Test


class TestController:

    def __init__(self, db_manager):
        self.dao = TestDAO(db_manager)

    # ── CREATE ────────────────────────────────

    def add_test(self, test_name: str, description: str = "") -> int:

        if not test_name:
            raise ValueError("Test name cannot be empty")

        return self.dao.add_test(test_name, description)

    def add_default_tests(self):
        return self.dao.add_default_tests()

    # ── READ ──────────────────────────────────

    def get_test_by_id(self, test_id: int):

        if test_id <= 0:
            return None

        row = self.dao.get_by_id(test_id)
        return Test.from_row(row)

    def get_test_by_name(self, test_name: str):

        if not test_name:
            return None

        row = self.dao.get_by_name(test_name)
        return Test.from_row(row)

    def get_all_tests(self):

        rows = self.dao.get_all_tests()
        return [Test.from_row(row) for row in rows]

    def get_test_names(self):
        return self.dao.get_test_names()

    def search_tests(self, query: str):

        if not query:
            return []

        rows = self.dao.search_tests(query)
        return [Test.from_row(row) for row in rows]

    # ── UPDATE ────────────────────────────────

    def update_test(self, test_id: int, test_name: str, description: str) -> bool:

        if test_id <= 0:
            return False

        if not test_name:
            raise ValueError("Test name cannot be empty")

        return self.dao.update_test(test_id, test_name, description)

    # ── DELETE ────────────────────────────────

    def delete_test(self, test_id: int) -> bool:

        if test_id <= 0:
            return False

        return self.dao.delete_test(test_id)