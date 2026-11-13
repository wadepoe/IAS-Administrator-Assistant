"""Unit tests for reset_user_password tool."""
from tools.ias_user_tools import reset_user_password


def test_reset_user_password_with_valid_id():
    result = reset_user_password.invoke({"user_id": "user-abc-123"})
    assert "user-abc-123" in result


def test_reset_user_password_returns_string():
    result = reset_user_password.invoke({"user_id": "user-xyz-999"})
    assert isinstance(result, str)
    assert len(result) > 0


def test_reset_user_password_contains_reset_keyword():
    result = reset_user_password.invoke({"user_id": "user-abc-123"})
    assert "reset" in result.lower() or "password" in result.lower()
