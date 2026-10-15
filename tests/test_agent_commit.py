import sys
import pytest
from unittest.mock import patch, MagicMock

# Adjust the import path as needed, or test it appropriately
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.agent_commit import run_cmd

@patch('scripts.agent_commit.subprocess.run')
def test_run_cmd_success(mock_run):
    # Setup mock for successful command execution
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "hello world\n"
    mock_run.return_value = mock_result

    # Call function
    output = run_cmd("echo 'hello world'")

    # Assertions
    mock_run.assert_called_once_with("echo 'hello world'", shell=True, text=True, capture_output=True)
    assert output == "hello world"

@patch('scripts.agent_commit.subprocess.run')
@patch('scripts.agent_commit.sys.exit')
@patch('builtins.print')
def test_run_cmd_failure(mock_print, mock_exit, mock_run):
    # Setup mock for failed command execution
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stderr = "command not found"
    mock_run.return_value = mock_result

    # Call function - we don't expect it to return normally because of sys.exit
    run_cmd("invalid_command")

    # Assertions
    mock_run.assert_called_once_with("invalid_command", shell=True, text=True, capture_output=True)
    mock_print.assert_called_once_with(
        "Error running command: invalid_command\ncommand not found",
        file=sys.stderr
    )
    mock_exit.assert_called_once_with(1)
