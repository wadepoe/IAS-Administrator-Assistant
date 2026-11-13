"""Unit tests for get_transformation tool."""
from tools.ips_transformation_tools import get_transformation


def test_get_source_transformation():
    result = get_transformation.invoke({"system_id": "sys-s4-cloud", "system_type": "source"})
    assert "sys-s4-cloud" in result
    assert "source" in result.lower()


def test_get_target_transformation():
    result = get_transformation.invoke({"system_id": "sys-s4-cloud", "system_type": "target"})
    assert "sys-s4-cloud" in result
    assert "target" in result.lower()


def test_get_transformation_default_system_type():
    result = get_transformation.invoke({"system_id": "sys-hr"})
    assert "sys-hr" in result


def test_get_transformation_returns_string():
    result = get_transformation.invoke({"system_id": "test-system", "system_type": "source"})
    assert isinstance(result, str)
    assert len(result) > 0
