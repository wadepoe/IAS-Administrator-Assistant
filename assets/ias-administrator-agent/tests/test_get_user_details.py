"""Unit tests for get_user_details tool."""
from tools.ias_user_tools import get_user_details


def test_get_user_details_with_valid_id():
    result = get_user_details.invoke({"user_id": "user-abc-123"})
    assert "user-abc-123" in result


def test_get_user_details_returns_string():
    result = get_user_details.invoke({"user_id": "some-user-id"})
    assert isinstance(result, str)
    assert len(result) > 0
