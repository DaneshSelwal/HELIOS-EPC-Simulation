import sys
import pytest
from unittest.mock import patch

from scripts.agent_commit import main

@patch("scripts.agent_commit.commit_as")
@patch.object(sys, "argv", ["agent_commit.py", "--agent", "test_agent", "--message", "test_msg", "--file", "test_file.txt"])
def test_main_happy_path(mock_commit_as):
    main()
    mock_commit_as.assert_called_once_with(
        agent="test_agent",
        paths="test_file.txt",
        message="test_msg"
    )

@patch("scripts.agent_commit.commit_as")
@patch.object(sys, "argv", ["agent_commit.py", "--agent", "test_agent"])
def test_main_missing_args(mock_commit_as):
    with pytest.raises(SystemExit) as exc_info:
        main()

    # argparse usually exits with status non-zero when arguments are invalid/missing
    assert exc_info.value.code != 0
    mock_commit_as.assert_not_called()
