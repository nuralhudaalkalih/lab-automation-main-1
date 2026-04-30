import unittest
import sqlite3
from DatabaseManager import DatabaseManager 
from UserDAO import UserDAO
from TestDAO import TestDAO
from SampleDAO import SampleDAO
from ResultDAO import ResultDAO

# Assuming your classes are defined in a file named lab_database.py
# from lab_database import DatabaseManager, UserDAO, TestDAO, SampleDAO, ResultDAO

class TestLASMSDatabase(unittest.TestCase):
    
    def setUp(self):
        """
        Runs before EVERY test. 
        Sets up a fresh, empty in-memory database to ensure tests are isolated.
        """
        self.db = DatabaseManager(":memory:")
        self.user_dao = UserDAO(self.db)
        self.test_dao = TestDAO(self.db)
        self.sample_dao = SampleDAO(self.db)
        self.result_dao = ResultDAO(self.db)

    def tearDown(self):
        """Runs after EVERY test. Cleans up the connection."""
        self.db.close()

    # ── UserDAO Tests ──────────────────────────────────────────

    def test_add_valid_user(self):
        success = self.user_dao.add_user("admin_roaa", "secure123", "Admin")
        self.assertTrue(success)
        
        user = self.user_dao.get_by_username("admin_roaa")
        self.assertIsNotNone(user)
        self.assertEqual(user["role"], "Admin")

    def test_add_duplicate_username_fails(self):
        self.user_dao.add_user("tech1", "pass", "Technician")
        # Attempting to add the exact same username should return False
        success = self.user_dao.add_user("tech1", "newpass", "Technician")
        self.assertFalse(success, "Duplicate username should violate UNIQUE constraint")

    def test_invalid_role_fails(self):
        # Database CHECK constraint only allows 'Admin' or 'Technician'
        success = self.user_dao.add_user("hacker", "pass", "SuperUser")
        self.assertFalse(success, "Role not in ('Admin', 'Technician') should fail CHECK constraint")

    # ── TestDAO Tests ──────────────────────────────────────────

    def test_add_and_retrieve_test(self):
        test_id = self.test_dao.add_test("CBC", "Complete Blood Count")
        self.assertGreater(test_id, 0) # lastrowid should be > 0
        
        test = self.test_dao.get_by_id(test_id)
        self.assertEqual(test["test_name"], "CBC")

    def test_add_default_tests(self):
        self.test_dao.add_default_tests()
        names = self.test_dao.get_test_names()
        
        # Verify a few standard lab tests were populated
        self.assertIn("COVID-19 PCR", names)
        self.assertIn("Cholesterol", names)
        self.assertIn("TSH", names)

    # ── SampleDAO Tests ────────────────────────────────────────

    def test_auto_generate_sample_id(self):
        id1 = self.sample_dao.add_sample("John Doe")
        id2 = self.sample_dao.add_sample("Jane Smith")
        
        self.assertEqual(id1, "S001")
        self.assertEqual(id2, "S002")

    def test_update_sample_status(self):
        s_id = self.sample_dao.add_sample("John Doe")
        success = self.sample_dao.update_status(s_id, "Processing")
        self.assertTrue(success)
        
        sample = self.sample_dao.get_by_id(s_id)
        self.assertEqual(sample["status"], "Processing")

    def test_invalid_sample_status_fails(self):
        s_id = self.sample_dao.add_sample("John Doe")
        # 'Lost' is not in the CHECK('Pending','Processing','Completed') constraint
        success = self.sample_dao.update_status(s_id, "Lost")
        self.assertFalse(success)

    # ── ResultDAO Tests & Relational Integrity ─────────────────

    def test_add_result_with_valid_foreign_keys(self):
        s_id = self.sample_dao.add_sample("Alice")
        t_id = self.test_dao.add_test("TSH")
        
        r_id = self.result_dao.add_result(s_id, t_id, "2.5 mIU/L")
        self.assertGreater(r_id, 0)
        
        results = self.result_dao.get_by_sample(s_id)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["result_value"], "2.5 mIU/L")
        # Check if INNER JOIN pulled the correct human-readable names
        self.assertEqual(results[0]["patient_name"], "Alice")
        self.assertEqual(results[0]["test_name"], "TSH")

    def test_cascade_delete_sample_removes_results(self):
        s_id = self.sample_dao.add_sample("Bob")
        t_id = self.test_dao.add_test("Urinalysis")
        self.result_dao.add_result(s_id, t_id, "Normal")
        
        self.assertTrue(self.result_dao.sample_has_results(s_id))
        
        # Action: Delete the sample
        self.sample_dao.delete_sample(s_id)
        
        # Assertion: The associated result should vanish due to ON DELETE CASCADE
        self.assertFalse(self.result_dao.sample_has_results(s_id))

    def test_restrict_delete_test_with_existing_results(self):
        s_id = self.sample_dao.add_sample("Charlie")
        t_id = self.test_dao.add_test("Insulin")
        self.result_dao.add_result(s_id, t_id, "10 mIU/L")
        
        # Action: Attempt to delete the test from the catalogue
        success = self.test_dao.delete_test(t_id)
        
        # Assertion: Should fail because a result is referencing it (ON DELETE RESTRICT)
        self.assertFalse(success)

if __name__ == "__main__":
    unittest.main()