from application import *
import unittest
import json

class TestValidators(unittest.TestCase):
    def test_char_validator(self):
        validator = CharValidator()
        self.assertEqual(validator.validate("a",0)[0],QValidator.Acceptable)
        self.assertEqual(validator.validate("aasd",3)[0],QValidator.Invalid)
        
    def test_realinvl_validator(self):
        lineEditor = None
        validator = RealInvlValidator(lineEditor)
        self.assertEqual(validator.min,float("-inf"))
        self.assertEqual(validator.max,float("inf"))
        
        validator.setRange(-3,4)
        self.assertEqual(validator.min,-3)
        self.assertEqual(validator.max,4)
        
        self.assertEqual(validator.validate('0',0)[0],QValidator.Acceptable)
        self.assertEqual(validator.validate('-',0)[0],QValidator.Intermediate)
        self.assertEqual(validator.validate('-4',0)[0],QValidator.Invalid)
        
class TestTableMerge(unittest.TestCase):
    def test_merge(self):
        data = None
        with open("test.json", 'r') as file:
            data = json.load(file)
        self.assertNotEqual(data,None)
        database = DataBase.fromDict(data)
        self.assertEqual(len(database.tables),2)
        self.assertEqual(database.tables[0].name,"1")
        self.assertEqual(database.tables[1].name,"2")
        new_table = database.mergeTables(["1","2"])
        self.assertEqual(len(database.tables),1)
        self.assertEqual(database.tables[0].name,"1 + 2")
        
if __name__ == "__main__":
    unittest.main()