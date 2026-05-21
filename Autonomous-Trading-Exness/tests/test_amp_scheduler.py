import pytest
from unittest.mock import patch

from amp_scheduler import get_scheduler_status, update_scheduler_config

@patch('amp_scheduler.amp_scheduler')
def test_get_scheduler_status(mock_scheduler):
    """Test get_scheduler_status calls amp_scheduler.get_status()."""
    mock_status = {
        "is_running": True,
        "config": {"enabled": True},
        "next_jobs": [],
        "last_run": "2023-10-27 10:00:00",
    }
    mock_scheduler.get_status.return_value = mock_status

    result = get_scheduler_status()

    mock_scheduler.get_status.assert_called_once()
    assert result == mock_status

@patch('amp_scheduler.amp_scheduler')
def test_update_scheduler_config(mock_scheduler):
    """Test update_scheduler_config calls amp_scheduler.update_config(**kwargs)."""
    update_scheduler_config(interval_minutes=15, enabled=False)

    mock_scheduler.update_config.assert_called_once_with(interval_minutes=15, enabled=False)
