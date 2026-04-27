from database.SampleDAO import SampleDAO
from models.Sample import Sample


class SampleController:

    def __init__(self, db_manager):
        self.dao = SampleDAO(db_manager)

    # ── CREATE ────────────────────────────────

    def add_sample(self, patient_name: str, date_added: str = None) -> str:

        if not patient_name:
            raise ValueError("Patient name cannot be empty")

        return self.dao.add_sample(patient_name, date_added)

    # ── READ ──────────────────────────────────

    def get_sample_by_id(self, sample_id: str):

        if not sample_id:
            return None

        row = self.dao.get_by_id(sample_id)
        return Sample.from_row(row)

    def get_all_samples(self):

        rows = self.dao.get_all_samples()
        return [Sample.from_row(row) for row in rows]

    def get_samples_by_status(self, status: str):

        valid_status = ['Pending', 'Processing', 'Completed']

        if status not in valid_status:
            raise ValueError("Invalid status")

        rows = self.dao.get_by_status(status)
        return [Sample.from_row(row) for row in rows]

    def search_samples_by_patient(self, name_query: str):

        if not name_query:
            return []

        rows = self.dao.search_by_patient(name_query)
        return [Sample.from_row(row) for row in rows]

    def get_samples_by_date(self, date_str: str):

        rows = self.dao.get_by_date(date_str)
        return [Sample.from_row(row) for row in rows]

    def count_samples_by_status(self):
        return self.dao.count_by_status()

    # ── UPDATE ────────────────────────────────

    def update_sample_status(self, sample_id: str, new_status: str) -> bool:

        valid_status = ['Pending', 'Processing', 'Completed']

        if new_status not in valid_status:
            raise ValueError("Invalid status")

        return self.dao.update_status(sample_id, new_status)

    # ── DELETE ────────────────────────────────

    def delete_sample(self, sample_id: str) -> bool:

        if not sample_id:
            return False

        return self.dao.delete_sample(sample_id)