"""Unit tests for search_user tool."""
import pytest
from unittest.mock import patch, MagicMock
from tools.ias_user_tools import search_user


def test_search_user_by_email():
    """Test that search_user returns a string result with the query."""
    result = search_user.invoke({"query": "john.doe@company.com"})
    assert "john.doe@company.com" in result


def test_search_user_by_name():
    result = search_user.invoke({"query": "John Doe"})
    assert "John Doe" in result


def test_search_user_by_id():
    result = search_user.invoke({"query": "user-abc-123"})
    assert "user-abc-123" in result


def test_search_user_returns_string():
    result = search_user.invoke({"query": "test@example.com"})
    assert isinstance(result, str)
    assert len(result) > 0
