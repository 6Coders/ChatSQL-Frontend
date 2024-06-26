import unittest
from unittest import TestCase
from chatsql.utils.JSONValidator import JSONValidator

class TestJSONValidator(TestCase):
    def test_is_valid_structure_valid(self):
        json_data = {
            "tables_info": {
                "table1": {"table_description": "Description", "columns": [], "attribute_types": []}
            },
            "primary_key": {"table1": ["column1"]},
            "foreign_keys": []
        }
        assert JSONValidator.is_valid_structure(json_data) == True

    def test_is_valid_structure_invalid(self):
        # Test caso in cui mancano chiavi
        json_data_missing_keys = {"tables_info": {}, "primary_key": {}, "foreign_keys": {}}
        TestCase.assertTrue(self, JSONValidator.is_valid_structure(json_data_missing_keys))

        # Test caso in cui le tabelle non hanno tutte le informazioni necessarie
        json_data_invalid_tables_info = {
            "tables_info": {"table1": {"columns": [], "attribute_types": []}},
            "primary_key": {"table1": ["column1"]},
            "foreign_keys": []
        }
        TestCase.assertFalse(self, JSONValidator.is_valid_structure(json_data_invalid_tables_info))

        # Test caso in cui le chiavi primarie non sono correttamente strutturate
        json_data_invalid_primary_key = {
            "tables_info": {"table1": {"table_description": "Description", "columns": [], "attribute_types": []}},
            "primary_key": {"table1": "column1"},
            "foreign_keys": []
        }
        TestCase.assertFalse(self, JSONValidator.is_valid_structure(json_data_invalid_primary_key))
        
        # Test caso in cui le chiavi esterne non sono correttamente strutturate
        json_data_invalid_foreign_keys = {
            "tables_info": {"table1": {"table_description": "Description", "columns": [], "attribute_types": []}},
            "primary_key": {"table1": ["column1"]},
            "foreign_keys": [{"table": "table1"}]
        }
        TestCase.assertFalse(self, JSONValidator.is_valid_structure(json_data_invalid_foreign_keys))

if __name__ == '__main__':
    unittest.main()
