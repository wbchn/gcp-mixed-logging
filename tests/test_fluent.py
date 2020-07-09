import os
import pytest

from gcp_mixed_logging import mixedlogging


@pytest.fixture
def log(monkeypatch):
    log = mixedlogging("data", "test")
    print(log._logger.full_name)
    return log


def test_persist_struct(log):
    log.persist('impression', {
        "text": "log forever",
        "nested": {
            "sub_field": "a nest message"
        }
    })
