import sys
import json
import pytest
from unittest.mock import patch, MagicMock, mock_open
from scripts.agent_commit import main

def test_main_integration_success():
    """Integration test for main execution flow, mocking subprocess and file reads."""
    test_args = ["agent_commit.py", "--agent", "KRONOS", "--message", "Test commit", "--file", "test_file.txt"]

    mock_identities = {
        "KRONOS": {
            "name": "Kronos Agent",
            "email": "kronos@example.com"
        }
    }

    def mock_subprocess_run(cmd, *args, **kwargs):
        mock_result = MagicMock()
        mock_result.returncode = 0
        if cmd[0:2] == ["git", "add"]:
            mock_result.stdout = ""
        elif cmd[0:3] == ["git", "diff", "--cached"]:
            # returncode 1 means there are changes (diff --quiet returns 1 if differences were found)
            # wait, engine/git_identity.py says:
            # diff_res.returncode == 0: print("Warning: No staged changes...") return None
            # So we need returncode != 0
            mock_result.returncode = 1
        elif cmd[0:2] == ["git", "commit"]:
            mock_result.stdout = "Commit successful"
        elif cmd[0:2] == ["git", "log"]:
            mock_result.stdout = "1234567890abcdef|Kronos Agent|kronos@example.com|Kronos Agent|kronos@example.com|Test commit"
        else:
            mock_result.stdout = ""
        return mock_result

    with patch.object(sys, "argv", test_args):
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_identities))) as m_open:
            with patch("subprocess.run", side_effect=mock_subprocess_run) as m_subprocess:
                # Capture print output if needed, but not strictly necessary
                main()

                # Verify that files were read (identities)
                m_open.assert_called_once()

                # Verify git commands were executed
                calls = m_subprocess.call_args_list
                assert any(c[0][0][0:2] == ["git", "add"] for c in calls)
                assert any(c[0][0][0:2] == ["git", "commit"] for c in calls)
                assert any(c[0][0][0:2] == ["git", "log"] for c in calls)

def test_main_missing_arguments():
    """Test main function when required argument is missing."""
    test_args = ["agent_commit.py", "--agent", "KRONOS"]
    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            main()
