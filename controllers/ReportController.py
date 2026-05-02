from database.ResultDAO import ResultDAO
from models.Result import Result


class ReportController:

    def __init__(self, db_manager):
        self.dao = ResultDAO(db_manager)

    # ── GET ALL RESULTS ────────────────────────────────

    def get_all_results(self):
        rows = self.dao.get_all_results()
        return [Result.from_joined_row(row) for row in rows]

    # ── GET BY SAMPLE ──────────────────────────────────

    def get_results_by_sample(self, sample_id: str):

        if not sample_id:
            return []

        rows = self.dao.get_by_sample(sample_id)
        return [Result.from_joined_row(row) for row in rows]

    # ── GET BY TEST NAME ───────────────────────────────

    def get_results_by_test_name(self, test_name: str):

        if not test_name:
            return []

        rows = self.dao.get_by_test_name(test_name)
        return [Result.from_joined_row(row) for row in rows]

    # ── GET SINGLE RESULT ──────────────────────────────

    def get_result_by_id(self, result_id: int):

        if result_id <= 0:
            return None

        row = self.dao.get_by_id(result_id)
        return Result.from_joined_row(row)

    # ── CHECK SAMPLE RESULTS ────────────────────────────

    def sample_has_results(self, sample_id: str) -> bool:
        return self.dao.sample_has_results(sample_id)