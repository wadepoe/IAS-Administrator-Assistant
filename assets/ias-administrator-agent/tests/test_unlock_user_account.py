"""Unit tests for unlock_user_account tool."""
from tools.ias_user_tools import unlock_user_account


def test_unlock_user_account_with_valid_id():
    result = unlock_user_account.invoke({"user_id": "user-abc-123"})
    assert "user-abc-123" in result


def test_unlock_user_account_returns_string():
    result = unlock_user_account.invoke({"user_id": "locked-user-id"})
    assert isinstance(result, str)
    assert len(result) > 0


def test_unlock_user_account_contains_unlock_keyword():
    result = unlock_user_account.invoke({"user_id": "user-abc-123"})
    assert "unlock" in result.lower() or "account" in result.lower()
