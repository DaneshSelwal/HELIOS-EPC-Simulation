import os
import sys
import json
import pytest
from unittest.mock import patch, mock_open

# Add repo root to sys.path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from scripts.agent_commit import main

def test_invalid_agent_identity(capsys):
    """
    Test that passing an invalid agent to agent_commit.py exits with status 1
    and prints the correct error message.
    """
    test_args = ["agent_commit.py", "--agent", "GHOST_AGENT", "--message", "Test", "--file", "dummy.txt"]
    mock_identities = json.dumps({
        "VALID_AGENT": {
            "name": "Valid Agent",
            "email": "valid@example.com"
        }
    })

    with patch("sys.argv", test_args), \
         patch("builtins.open", mock_open(read_data=mock_identities)):

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Error: Identity for GHOST_AGENT not found." in captured.out

def test_valid_agent_identity():
    """
    Test that passing a valid agent to agent_commit.py proceeds to call commit_as.
    """
    test_args = ["agent_commit.py", "--agent", "VALID_AGENT", "--message", "Test message", "--file", "dummy.txt"]
    mock_identities = json.dumps({
        "VALID_AGENT": {
            "name": "Valid Agent",
            "email": "valid@example.com"
        }
    })

    with patch("sys.argv", test_args), \
         patch("builtins.open", mock_open(read_data=mock_identities)), \
         patch("scripts.agent_commit.commit_as") as mock_commit_as:

        main()

        mock_commit_as.assert_called_once_with(
            agent="VALID_AGENT",
            paths="dummy.txt",
            message="Test message"
        )
