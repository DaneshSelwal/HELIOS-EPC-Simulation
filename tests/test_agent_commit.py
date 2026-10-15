import sys
import unittest
from unittest.mock import patch, mock_open
import io
import json

from scripts.agent_commit import main

class TestAgentCommit(unittest.TestCase):
    @patch('sys.argv', ['agent_commit.py', '--agent', 'INVALID_AGENT', '--message', 'test', '--file', 'test.txt'])
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.open', new_callable=mock_open, read_data='{"VALID_AGENT": {"name": "Valid Agent", "email": "valid@example.com"}}')
    def test_invalid_agent_identity(self, mock_file, mock_stdout):
        with self.assertRaises(SystemExit) as cm:
            main()

        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: Identity for INVALID_AGENT not found.", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
