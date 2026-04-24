from database.ResultDAO import ResultDAO


class ReportController:

    def __init__(self, db_manager):
        self.dao = ResultDAO(db_manager)

    # ── CREATE ────────────────────────────────

    def add_result(self, sample_id: str, test_id: int, result_value: str) -> int:
        if not sample_id or not result_value:
            raise ValueError("Invalid result data")

        return self.dao.add_result(sample_id, test_id, result_value)

    # ── READ ──────────────────────────────────

    def get_results_by_sample(self, sample_id: str):
        if not sample_id:
            return []

        return self.dao.get_by_sample(sample_id)

    def get_all_results(self):
        return self.dao.get_all_results()

    def get_result_by_id(self, result_id: int):
        if result_id <= 0:
            return None

        return self.dao.get_by_id(result_id)

    def get_results_by_test_name(self, test_name: str):
        if not test_name:
            return []

        return self.dao.get_by_test_name(test_name)

    def check_sample_has_results(self, sample_id: str) -> bool:
        return self.dao.sample_has_results(sample_id)

    # ── UPDATE ────────────────────────────────

    def update_result(self, result_id: int, new_value: str) -> bool:
        if result_id <= 0:
            return False

        if not new_value:
            raise ValueError("Result value cannot be empty")

        return self.dao.update_result_value(result_id, new_value)

    # ── DELETE ────────────────────────────────

    def delete_result(self, result_id: int) -> bool:
        if result_id <= 0:
            return False

        return self.dao.delete_result(result_id)

    def delete_results_for_sample(self, sample_id: str) -> int:
        if not sample_id:
            return 0

        return self.dao.delete_results_for_sample(sample_id)