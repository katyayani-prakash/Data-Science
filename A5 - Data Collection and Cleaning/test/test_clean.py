import unittest
from pathlib import Path
import os, sys
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)
from src.clean import validate_title, validate_author, validate_count, validate_date, validate_tags, isValidJson
import json
import re


class CleanTest(unittest.TestCase):
    def setUp(self):
        # You might want to load the fixture files as variables, and test your code against them. Check the fixtures folder.
        dr = os.path.dirname(__file__)
        fixture1_path = os.path.join(dr,'fixtures','test_1.json')
        with open(fixture1_path) as f:
            record = f.readline()
            self.fixture1 = json.loads(record)

        fixture2_path = os.path.join(dr,'fixtures','test_2.json')
        with open(fixture2_path) as f2:
            record2 = f2.readline()
            self.fixture2 = json.loads(record2)

        fixture3_path = os.path.join(dr,'fixtures','test_3.json')
        with open(fixture3_path) as f3:
            self.fixture3 = f3.readline()
            
        fixture4_path = os.path.join(dr,'fixtures','test_4.json')
        with open(fixture4_path) as f4:
            record4 = f4.readline()
            self.fixture4 = json.loads(record4)

        fixture5_path = os.path.join(dr,'fixtures','test_5.json')
        with open(fixture5_path) as f5:
            record5 = f5.readline()
            self.fixture5 = json.loads(record5)

        fixture6_path = os.path.join(dr,'fixtures','test_6.json')
        with open(fixture6_path) as f6:
            record6 = f6.readline()
            self.fixture6 = json.loads(record6)

    
    def test_title(self):
        self.assertEqual(validate_title(self.fixture1),None)

    def test_date(self):
        self.assertEqual(validate_date(self.fixture2),None)

    def test_json(self):
        self.assertEqual(isValidJson(self.fixture3),None)
        
    def test_author(self):
        self.assertEqual(validate_author(self.fixture4),None)

    def test_count(self):
        self.assertEqual(validate_count(self.fixture5),None)

    

    def test_tags(self):
        words = 0
        for item in self.fixture6['tags']:
            res = len(re.findall(r'\w+', item))
            words = words + res
        
        f = validate_tags(self.fixture6)
        self.assertEqual(len(f['tags']),words)
        

if __name__ == '__main__':
    unittest.main()

