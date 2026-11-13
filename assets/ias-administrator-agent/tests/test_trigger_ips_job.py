"""Unit tests for trigger_ips_job tool."""
from tools.ips_tools import trigger_ips_job


def test_trigger_read_job():
    result = trigger_ips_job.invoke({"system_name": "SAP S/4HANA Cloud", "job_type": "read"})
    assert "SAP S/4HANA Cloud" in result
    assert "read" in result.lower()


def test_trigger_resync_job():
    result = trigger_ips_job.invoke({"system_name": "SAP SuccessFactors", "job_type": "resync"})
    assert "SAP SuccessFactors" in result
    assert "resync" in result.lower()


def test_trigger_job_returns_string():
    result = trigger_ips_job.invoke({"system_name": "sys-001", "job_type": "read"})
    assert isinstance(result, str)
    assert len(result) > 0


def test_trigger_job_contains_system_name():
    result = trigger_ips_job.invoke({"system_name": "my-system", "job_type": "resync"})
    assert "my-system" in result
