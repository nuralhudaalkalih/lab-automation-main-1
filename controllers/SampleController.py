from SampleDAO import SampleDAO


class SampleController:

    def __init__(self, db_manager):
        # ربط الـ DAO
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

        return self.dao.get_by_id(sample_id)

    def get_all_samples(self):
        return self.dao.get_all_samples()

    def get_samples_by_status(self, status: str):
        valid_status = ['Pending', 'Processing', 'Completed']
        if status not in valid_status:
            raise ValueError("Invalid status")

        return self.dao.get_by_status(status)

    def search_samples_by_patient(self, name_query: str):
        if not name_query:
            return []

        return self.dao.search_by_patient(name_query)

    def get_samples_by_date(self, date_str: str):
        return self.dao.get_by_date(date_str)

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