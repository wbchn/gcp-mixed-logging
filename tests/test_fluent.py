import os
import pytest

from gcp_mixed_logging import MixedLogging


@pytest.fixture
def log(monkeypatch):
    log = MixedLogging("data", "test")
    print(log.cloud_logging_name)
    
    return log


def test_persist_struct(log):
    log.persist('impression', {
        "text": "log forever",
        "nested": {
            "sub_field": "a nest message"
        }
    })

def test_persist_struct_trace(log):
    log.persist('click', {
        "text": "click log forever",
        "nested": {
            "sub_field": "a nest message"
        }
    }, track=True)
