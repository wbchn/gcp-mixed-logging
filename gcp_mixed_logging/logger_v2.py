"""

"""
import sys
import atexit
import collections
import datetime
import inspect
import logging
import socket
import threading
import time
from typing import Any, Collection, Dict, List, Optional, Tuple, Type

import fluent.asyncsender
import fluent.event
import google.auth
if sys.version_info >= (3, 8):
    from functools import cached_property
else:
    from cached_property import cached_property
from google.cloud import logging as gcp_logging
from google.cloud.logging_v2.handlers.transports.background_thread import (
    BackgroundThreadTransport,
    _Worker,
)
from google.cloud.logging_v2.resource import Resource
from inspect import getframeinfo, stack

_GLOBAL_RESOURCE = Resource(type="global", labels={})

_DEFAULT_SCOPESS = frozenset([
    "https://www.googleapis.com/auth/logging.read",
    "https://www.googleapis.com/auth/logging.write"
])


def caller_reader(f):
    """This wrapper updates the context with the callor infos"""

    def wrapper(self, *args):
        caller = getframeinfo(stack()[1][0])
        self._filter.file = caller.filename
        self._filter.line_n = caller.lineno
        return f(self, *args)
    return wrapper


logging.info


class MixedLogging(object):
    LOG_VIEWER_BASE_URL = "https://console.cloud.google.com/logs/viewer"
    LOG_NAME = 'Google Stackdriver'

    hostname: str = socket.gethostname()

    _sender: fluent.asyncsender.FluentSender

    def __init__(
            self, module: str, stage: str,
            fluent_host: str = 'localhost',
            fluent_port: int = 24224,
            project: str = None,
            scopes: Optional[Collection[str]] = _DEFAULT_SCOPESS,
            resource: Resource = _GLOBAL_RESOURCE,
            **kw):
        """
        """

        self.name: str = f'{module}_{stage}'
        self.fluent_host = fluent_host
        self.fluent_port = fluent_port
        self.project: str = project
        self.scopes: Optional[Collection[str]] = scopes
        self.resource: Resource = resource
        self.labels: Optional[Dict[str, str]] = {
            "module": module,
            "stage": stage,
            "host": self.hostname,
        }

        self._closed = False
        self._persist_insertids: dict = collections.defaultdict(int)
        self._insertid_lock = threading.Lock()
        atexit.register(self.close)

    def _get_credentials_using_adc(self):
        credentials, project_id = google.auth.default(scopes=self.scopes)
        return credentials, project_id

    @cached_property
    def _cloudligging_client(self) -> gcp_logging.Client:
        """Google Cloud Library API client"""
        credentials, project = self._get_credentials_using_adc()
        project = self.project or project

        client = gcp_logging.Client(
            credentials=credentials,
            project=project,
        )
        return client

    @cached_property
    def _transport(self) -> BackgroundThreadTransport:
        """Object responsible for sending data to Stackdriver"""
        return BackgroundThreadTransport(self._cloudligging_client, self.name)

    @cached_property
    def _fluent_sender(self) -> fluent.sender:
        sender = fluent.asyncsender.FluentSender(
            self.name,
            host=self.fluent_host,
            port=self.fluent_port,
            timeout=3,
        )
        return sender

    @cached_property
    def cloudlogging_name(self):
        return f"projects/{self._cloudligging_client.project}/logs/{self.name}"

    def cloudligging_emit(self, msg: Any, severity: str = logging.INFO) -> None:
        """Actually log the specified logging record.

        :param record: The record to be logged.
        :type record: logging.LogRecord
        """
        frame = inspect.stack()[2]
        record = logging.LogRecord(
            self.name, severity, frame.filename, frame.lineno, msg, None, None, frame.function
        )
        message = self.format(msg, frame)
        self._transport.send(
            record,
            message=message,
            severity=severity,
            resource=self.resource,
            labels=self.labels)

    @property
    def is_alive(self):
        """Returns True is the background thread is running."""
        return not self._closed

    def format(self, msg: Any, frame: inspect.FrameInfo) -> dict:
        payload = {
            "timestamp": int(time.time()),
            "filename": frame.filename,
            "function": frame.function,
            "lineno": frame.lineno,
        }
        if isinstance(msg, str):
            payload["message"] = msg
        elif isinstance(msg, dict):
            payload.update(msg)
        else:
            # unsupport type
            payload["message"] = str(msg)
        return payload

    def close(self):
        if self._closed:
            return True

        self._transport.flush()
        self._fluent_sender.close()
        self._closed = True

        return True

    def debug(self, msg: Any, **kw):
        """Write debug log to Cloud Logging."""
        return self.cloudligging_emit(msg, severity="DEBUG", **kw)

    def info(self, msg: Any, **kw):
        """Write info log to Cloud Logging."""
        return self.cloudligging_emit(msg, severity="INFO", **kw)

    def warning(self, msg: Any, **kw):
        """Write warning log to Cloud Logging."""
        return self.cloudligging_emit(msg, severity="WARNING", **kw)

    def error(self, msg: Any, **kw):
        """Write error log to Cloud Logging."""
        return self.cloudligging_emit(msg, severity="ERROR", **kw)

    def metric(self, tag: str, msg: dict, **kw) -> None:
        """Send metrics data to ElasticSearch"""
        payload = {
            "tag": tag,
            "@timestamp": int(time.time()),
        }
        payload.update(msg)
        return self.cloudligging_emit(payload, severity="INFO", **kw)

    def persist(self, tag: str, msg: dict, track: bool = False, track_severity: str = "DEFAULT", **kw) -> None:
        """Save log to GCS."""
        # increment insert id with locking
        with self._insertid_lock:
            self._persist_insertids[tag] += 1
        payload = {
            "host": self.hostname,
            "tag": tag,
            "insert_id": self._persist_insertids[tag],
            "time": int(time.time()),
        }
        payload.update(msg)
        if track:
            self.cloudligging_emit(payload, severity=track_severity, **kw)
        self._fluent_sender.emit(tag, payload)
