class Sample:
    """
    Represents one row from the Samples table.

    CONCEPT — @property:
        A property looks like an attribute when accessed (no parentheses)
        but runs a method behind the scenes. Useful for computed values.
    """

    # Class-level constant — shared by ALL Sample instances
    VALID_STATUSES = ("Pending", "Processing", "Completed") # tuple data structure

    def __init__(self, sample_id: str, patient_name: str,
                 date_added: str, status: str = "Pending"):
        self.sample_id    = sample_id
        self.patient_name = patient_name
        self.date_added   = date_added
        self.status       = status

    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
        return cls(
            sample_id    = row["sample_id"],
            patient_name = row["patient_name"],
            date_added   = row["date_added"],
            status       = row["status"]
        )

    # ── Properties ────────────────────────────

    @property
    def is_completed(self) -> bool:
        """
        CONCEPT — @property:
            Access as  sample.is_completed  not  sample.is_completed()
            The @property decorator makes a method look like an attribute.
        """
        return self.status == "Completed"

    @property
    def is_pending(self) -> bool:
        return self.status == "Pending"

    @property
    def is_processing(self) -> bool:
        return self.status == "Processing"

    # ── Business logic ─────────────────────────

    def advance_status(self) -> str:
        """
        Moves to the next logical status.
        Returns the new status string, or current status if already Completed.
        """
        if self.status == "Pending":
            self.status = "Processing"
        elif self.status == "Processing":
            self.status = "Completed"
        return self.status

    def __str__(self) -> str:
        return f"Sample {self.sample_id} | {self.patient_name} | {self.status}"

    def __repr__(self) -> str:
        return (f"Sample(id='{self.sample_id}', patient='{self.patient_name}', "
                f"date='{self.date_added}', status='{self.status}')")
