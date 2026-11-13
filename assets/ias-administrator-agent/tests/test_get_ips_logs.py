"""Unit tests for get_ips_logs tool."""
from tools.ips_tools import get_ips_logs


def test_get_ips_logs_with_system_name():
    result = get_ips_logs.invoke({"system_name": "SAP S/4HANA Cloud"})
    assert "SAP S/4HANA Cloud" in result


def test_get_ips_logs_without_system_name():
    result = get_ips_logs.invoke({})
    assert "all systems" in result.lower() or "log" in result.lower()


def test_get_ips_logs_default_limit():
    result = get_ips_logs.invoke({"system_name": "sys-001"})
    assert "20" in result


def test_get_ips_logs_custom_limit():
    result = get_ips_logs.invoke({"system_name": "sys-001", "limit": 50})
    assert "50" in result


def test_get_ips_logs_returns_string():
    result = get_ips_logs.invoke({"system_name": "test-system"})
    assert isinstance(result, str)
    assert len(result) > 0
