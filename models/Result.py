class Result:
    """
    Represents one row from the Results table.
    Can optionally carry the enriched data from a JOIN
    (patient_name, test_name) when populated via from_joined_row().
    """

    def __init__(self, result_id: int, sample_id: str, test_id: int,
                 result_value: str, patient_name: str = "", test_name: str = ""):
        self.result_id    = result_id
        self.sample_id    = sample_id
        self.test_id      = test_id
        self.result_value = result_value
        # enriched fields (populated from JOIN queries)
        self.patient_name = patient_name
        self.test_name    = test_name

    @classmethod
    def from_row(cls, row):
        """Creates a Result from a raw Results table row (no JOIN data)."""
        if row is None:
            return None
        return cls(
            result_id    = row["result_id"],
            sample_id    = row["sample_id"],
            test_id      = row["test_id"],
            result_value = row["result_value"]
        )

    @classmethod
    def from_joined_row(cls, row):
        """
        Creates a Result from a JOIN query row that includes
        patient_name (from Samples) and test_name (from Tests).

        Use this with ResultDAO.get_by_sample() and get_all_results().
        """
        if row is None:
            return None
        return cls(
            result_id    = row["result_id"],
            sample_id    = row["sample_id"],
            test_id      = 0,               # not returned in JOIN query
            result_value = row["result_value"],
            patient_name = row["patient_name"],
            test_name    = row["test_name"]
        )

    def __str__(self) -> str:
        name = self.patient_name or self.sample_id
        test = self.test_name    or f"test_id={self.test_id}"
        return f"{name} | {test} | {self.result_value}"

    def __repr__(self) -> str:
        return (f"Result(id={self.result_id}, sample='{self.sample_id}', "
                f"value='{self.result_value}')")