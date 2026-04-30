class Test:
    """Represents one row from the Tests table (a test type in the catalogue)."""
 
    def __init__(self, test_id: int, test_name: str, description: str = ""):
        self.test_id     = test_id
        self.test_name   = test_name
        self.description = description
 
    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
        return cls(
            test_id     = row["test_id"],
            test_name   = row["test_name"],
            description = row["description"] or ""
        )
 
    def __str__(self) -> str:
        return f"[Test {self.test_id}] {self.test_name}"
 
    def __repr__(self) -> str:
        return f"Test(id={self.test_id}, name='{self.test_name}')"