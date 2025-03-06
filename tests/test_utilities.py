import sys
from pathlib import Path
# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import unittest
from unittest.mock import mock_open, patch

from utilities import load_json

class TestUtilities(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_json_valid_file(self, mock_file):
        data = load_json("valid.json")
        self.assertIsInstance(data, dict)
        self.assertIn("key", data)
        self.assertEqual(data["key"], "value")

    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    def test_load_json_invalid_file(self, mock_file):
        data = load_json("invalid.json")
        self.assertEqual(data, {})

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_json_nonexistent_file(self, mock_file):
        data = load_json("nonexistent.json")
        self.assertEqual(data, {})

if __name__ == "__main__":
    unittest.main()
