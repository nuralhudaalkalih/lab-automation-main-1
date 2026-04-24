class ReportController:
    def __init__(self, result_dao):
        self.result_dao = result_dao

    def add_result(self, sample_id, test_id, value):
        result_id = self.result_dao.add_result(sample_id, test_id, value)
        return result_id

    def get_sample_report(self, sample_id):
        return self.result_dao.get_by_sample(sample_id)

    def get_all_reports(self):
        return self.result_dao.get_all_results()

    def update_result(self, result_id, new_value):
        return self.result_dao.update_result_value(result_id, new_value)

    def delete_result(self, result_id):
        return self.result_dao.delete_result(result_id)