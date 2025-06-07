import unittest
from find_colleges import find_computer_science_colleges
import json
import os

class TestFindColleges(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a sample JSON file for testing
        cls.test_json_file = 'test_tneallotment.json'
        cls.sample_data = [
            {
                "College Details": "Test College 1",
                "Branch": "Computer Science and Engineering",
                "AGGR MARK": "183",
                " RANK": "1001",
                "ALLOTTED CATEGORY": "OC"
            },
            {
                "College Details": "Test College 2",
                "Branch": "Mechanical Engineering",
                "AGGR MARK": "185",
                " RANK": "1002",
                "ALLOTTED CATEGORY": "BC"
            },
            {
                "College Details": "Test College 3",
                "Branch": "Information Technology",
                "AGGR MARK": "182",
                " RANK": "1003",
                "ALLOTTED CATEGORY": "OC"
            },
            {
                "College Details": "Test College 4",
                "Branch": "Civil Engineering",
                "AGGR MARK": "180",
                " RANK": "1004",
                "ALLOTTED CATEGORY": "SC"
            }
        ]
        with open(cls.test_json_file, 'w', encoding='utf-8') as f:
            json.dump(cls.sample_data, f)

    @classmethod
    def tearDownClass(cls):
        # Remove the sample JSON file after tests
        if os.path.exists(cls.test_json_file):
            os.remove(cls.test_json_file)

    def test_find_computer_science_colleges(self):
        # Only Test College 1 and 3 should match for OC, marks >=181 and <=185
        result = find_computer_science_colleges(self.test_json_file, target_marks=181, eligible_categories=['OC'])
        college_names = [c['College'] for c in result]
        self.assertIn('Test College 1', college_names)
        self.assertIn('Test College 3', college_names)
        self.assertNotIn('Test College 2', college_names)
        self.assertNotIn('Test College 4', college_names)
        # Test for BC category
        result_bc = find_computer_science_colleges(self.test_json_file, target_marks=181, eligible_categories=['BC'])
        self.assertEqual(result_bc, [])  # No CS/IT for BC in sample

if __name__ == '__main__':
    unittest.main() 