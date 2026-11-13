"""Unit tests for bulk_manage_user_groups tool."""
from tools.ias_group_tools import bulk_manage_user_groups


def test_bulk_assign_group_to_multiple_users():
    user_ids = ["user-001", "user-002", "user-003"]
    result = bulk_manage_user_groups.invoke({"user_ids": user_ids, "group_name": "EmployeeGroup", "action": "assign"})
    assert "EmployeeGroup" in result
    assert "3" in result


def test_bulk_remove_group_from_users():
    user_ids = ["user-001", "user-002"]
    result = bulk_manage_user_groups.invoke({"user_ids": user_ids, "group_name": "HRUsers", "action": "remove"})
    assert "HRUsers" in result
    assert "remove" in result.lower()


def test_bulk_manage_returns_string():
    result = bulk_manage_user_groups.invoke({"user_ids": ["user-abc"], "group_name": "TestGroup", "action": "assign"})
    assert isinstance(result, str)
    assert len(result) > 0


def test_bulk_manage_shows_user_count():
    user_ids = ["user-001", "user-002", "user-003", "user-004", "user-005"]
    result = bulk_manage_user_groups.invoke({"user_ids": user_ids, "group_name": "SomeGroup", "action": "assign"})
    assert "5" in result


def test_bulk_manage_single_user():
    result = bulk_manage_user_groups.invoke({"user_ids": ["single-user"], "group_name": "TestGroup", "action": "assign"})
    assert "single-user" in result
