import os

import mock
import pytest

from gcp_mixed_logging import MixedLogging



def _make_credentials():
    import google.auth.credentials
    return mock.Mock(spec=google.auth.credentials.Credentials)


@pytest.fixture
def log(monkeypatch):
    # using data-stat@kakapo-grandwin.iam.gserviceaccount.com account.
    # monkeypatch.setenv('GOOGLE_APPLICATION_CREDENTIALS', '')
    project = os.environ.get('GCLOUD_PROJECT')
    if project:
        monkeypatch.setenv('GOOGLE_CLOUD_PROJECT', project)

    log = MixedLogging("data", "test")
    print(log.cloudlogging_name)
        # project="test-project", credentials=_make_credentials())
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


class _Client(object):
    def __init__(self, project, connection=None):
        self.project = project
        self._connection = connection


class _Bugout(Exception):
    pass


class _Connection(object):

    _called_with = None

    def __init__(self, *responses):
        self._responses = responses

    def api_request(self, **kw):
        self._called_with = kw
        response, self._responses = self._responses[0], self._responses[1:]
        return response