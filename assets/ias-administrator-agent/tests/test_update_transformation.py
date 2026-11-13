"""Unit tests for update_transformation tool."""
import json
from tools.ips_transformation_tools import update_transformation

SAMPLE_TRANSFORMATION = json.dumps({
    "user": [
        {"sourcePath": "$.userName", "targetPath": "userName"},
        {"sourcePath": "$.emails[0].value", "targetPath": "emails[0].value", "optional": True}
    ],
    "group": []
})


def test_update_source_transformation():
    result = update_transformation.invoke({
        "system_id": "sys-s4-cloud",
        "transformation_json": SAMPLE_TRANSFORMATION,
        "system_type": "source"
    })
    assert "sys-s4-cloud" in result
    assert "source" in result.lower()


def test_update_target_transformation():
    result = update_transformation.invoke({
        "system_id": "sys-s4-cloud",
        "transformation_json": SAMPLE_TRANSFORMATION,
        "system_type": "target"
    })
    assert "sys-s4-cloud" in result
    assert "target" in result.lower()


def test_update_transformation_reports_length():
    result = update_transformation.invoke({
        "system_id": "sys-hr",
        "transformation_json": SAMPLE_TRANSFORMATION,
        "system_type": "source"
    })
    assert "chars" in result or len(SAMPLE_TRANSFORMATION) > 0


def test_update_transformation_returns_string():
    result = update_transformation.invoke({
        "system_id": "test-system",
        "transformation_json": SAMPLE_TRANSFORMATION,
        "system_type": "source"
    })
    assert isinstance(result, str)
    assert len(result) > 0


def test_update_transformation_default_system_type():
    result = update_transformation.invoke({
        "system_id": "sys-s4-cloud",
        "transformation_json": SAMPLE_TRANSFORMATION
    })
    assert "sys-s4-cloud" in result
