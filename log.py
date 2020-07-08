"""

"""
import os
import time
from typing import Any

from aiofluent import FluentSender
import google.cloud.logging as google_logging

_logger: google_logging.logger.Logger
_sender: FluentSender


def init(module: str, stage: str, fluent_host: str, fluent_port:int, **kw):
    """Log init"""
    global _logger, _sender
    client = google_logging.Client()

    stdout_name = f'{module}_{stage}'
    _logger = client.logger(stdout_name)
    _sender = FluentSender(host=fluent_host, port=fluent_port, timeout=3)


def _format(tag: str, msg: Any) -> dict:
    if isinstance(msg, str):
        msg = {"message": msg}
    msg['tag'] = tag
    return msg


def _log_dup(
    tag: str, msg: Any, logger: google_logging.logger.Logger = None,
    severity: str = 'INFO', **kw
) -> None:
    if logger is None:
        logger = _logger
    logger.log_struct(_format(tag, msg), severity='INFO', **kw)


def debug(msg: Any, **kw):
    """Write debug log to Cloud Logging."""
    return _log_dup("debug", msg, logger=_logger, severity='DEBUG', **kw)


def info(msg: Any, **kw):
    """Write info log to Cloud Logging."""
    return _log_dup("info", msg, logger=_logger, severity='INFO', **kw)


def warning(msg: Any, **kw):
    """Write warning log to Cloud Logging."""
    return _log_dup("warn", msg, logger=_logger, severity='WARNING', **kw)


def error(msg: Any, **kw):
    """Write error log to Cloud Logging."""
    return _log_dup("error", msg, logger=_logger, severity='ERROR', **kw)


def metric(tag: str, msg: dict, **kw) -> None:
    """Send metrics data to ElasticSearch"""
    payload = {
        "tag": tag,
        "@timestamp": int(time.time()),
    }
    payload.update(msg)
    _log_dup("metrics", payload, logger=_logger, severity='INFO', **kw)


def persist(tag: str, msg: dict) -> None:
    """Save log to GCS."""
    payload = {
        "tag": tag,
        "timestamp": int(time.time()),
    }
    payload.update(msg)
    _sender.emit(label, {'message': message})
