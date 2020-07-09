import os
import pytest

from gcp_mixed_logging import mixedlogging


@pytest.fixture
def log(monkeypatch):
    # using data-stat@kakapo-grandwin.iam.gserviceaccount.com account.
    # monkeypatch.setenv('GOOGLE_APPLICATION_CREDENTIALS', '')
    project = os.environ.get('GCLOUD_PROJECT')
    if project:
        monkeypatch.setenv('GOOGLE_CLOUD_PROJECT', project)

    log = mixedlogging("data", "test")
    print(log._logger.full_name)
    return log


def test_debug(log):
    log.debug('this is a debug message')


def test_debug_struct(log):
    log.debug({
        "integer": 999,
        "text": "plain text",
        "nested": {
            "sub_field": "a nest message"
        }
    })


def test_error_struct(log):
    log.error({
        "integer": 999,
        "text": "plain text",
        "nested": {
            "sub_field": "a nest message"
        }
    })


def test_metric_struct(log):
    log.metric('cpu_usage', {
        "integer": 47,
        "text": "metric will send to es.",
        "nested": {
            "sub_field": "a nest message"
        }
    })

