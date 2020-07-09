"""

"""
import os
import time
from typing import Any

import google.cloud.logging as google_logging
import fluent.asyncsender
import fluent.event


class mixedlogging(object):
    _client: google_logging.Client
    _logger: google_logging.logger.Logger
    _sender: fluent.asyncsender.FluentSender

    def __init__(
            self, module: str, stage: str,
            fluent_host: str = 'localhost',
            fluent_port: int = 24224,
            **kw):
        """
        """
        self._client = google_logging.Client(**kw)

        stdout_name = f'{module}_{stage}'
        # TODO: using google.cloud.logging.logger.Batch
        self._logger = self._client.logger(stdout_name)
        self._sender = fluent.asyncsender.FluentSender(
            f'persist.{stdout_name}',
            host=fluent_host,
            port=fluent_port,
            timeout=3,
        )

    def _format(self, msg: Any) -> dict:
        if isinstance(msg, str):
            msg = {"message": msg}
        return msg

    def _log_dup(
        self,
        msg: Any,
        severity: str = 'INFO', **kw
    ) -> None:
        self._logger.log_struct(self._format(msg), severity=severity, **kw)

    def close(self):
        self._sender.close()

    def debug(self, msg: Any, **kw):
        """Write debug log to Cloud Logging."""
        return self._log_dup(msg, severity='DEBUG', **kw)

    def info(self, msg: Any, **kw):
        """Write info log to Cloud Logging."""
        return self._log_dup(msg, severity='INFO', **kw)

    def warning(self, msg: Any, **kw):
        """Write warning log to Cloud Logging."""
        return self._log_dup(msg, severity='WARNING', **kw)

    def error(self, msg: Any, **kw):
        """Write error log to Cloud Logging."""
        return self._log_dup(msg, severity='ERROR', **kw)

    def metric(self, tag: str, msg: dict, **kw) -> None:
        """Send metrics data to ElasticSearch"""
        payload = {
            "tag": tag,
            "@timestamp": int(time.time()),
        }
        payload.update(msg)
        self._log_dup(payload, severity='INFO', **kw)

    def persist(self, tag: str, msg: dict) -> None:
        """Save log to GCS."""
        payload = {
            "tag": tag,
            "time": int(time.time()),
        }
        payload.update(msg)
        self._sender.emit(tag, payload)
