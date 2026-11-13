"""Unit tests for manage_user_group tool."""
from tools.ias_group_tools import manage_user_group


def test_assign_group_to_user():
    result = manage_user_group.invoke({"user_id": "user-abc-123", "group_name": "EmployeeGroup", "action": "assign"})
    assert "EmployeeGroup" in result
    assert "user-abc-123" in result


def test_remove_group_from_user():
    result = manage_user_group.invoke({"user_id": "user-abc-123", "group_name": "HRUsers", "action": "remove"})
    assert "HRUsers" in result
    assert "user-abc-123" in result


def test_manage_user_group_returns_string():
    result = manage_user_group.invoke({"user_id": "user-abc-123", "group_name": "SomeGroup", "action": "assign"})
    assert isinstance(result, str)
    assert len(result) > 0


def test_manage_user_group_action_in_result():
    result = manage_user_group.invoke({"user_id": "user-abc-123", "group_name": "TestGroup", "action": "remove"})
    assert "remove" in result.lower()
