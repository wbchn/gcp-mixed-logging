"""

"""
import os
import time
from typing import Any

from google.cloud import logging

stdout_logger: logging.logger.Logger
stderr_logger: logging.logger.Logger


def init(module: str, stage: str, **kw):
    """Log init"""
    global stdout_logger, stderr_logger
    client = logging.Client()

    stdout_name = f'{module}_{stage}_stdout'
    stderr_name = f'{module}_{stage}_stderr'
    stdout_logger = client.logger(stdout_name)
    stderr_logger = client.logger(stderr_name)


def _log_dup(tag: str, msg: Any, logger: logging.logger.Logger=None, severity='INFO', **kw) -> None:
    if isinstance(msg, str):
        msg = {"message": msg}

    msg['tag'] = tag
    logger.log_struct(msg, severity='INFO')


def debug(msg):
    """Write debug log to Cloud Logging."""
    return _log_dup("debug", msg, logger=stdout_logger, severity='INFO')


def info(msg):
    """Write info log to Cloud Logging."""
    return _log_dup("info", msg, logger=stdout_logger, severity='INFO')


def warning(msg):
    """Write warning log to Cloud Logging."""
    return _log_dup("warn", msg, logger=stderr_logger, severity='WARNING')


def error(msg):
    """Write error log to Cloud Logging."""
    return _log_dup("error", msg, logger=stderr_logger, severity='ERROR')


def metric(tag: str, msg: dict) -> None:
    """Send metrics data to ElasticSearch"""
    payload = {
        "tag": tag,
        "@timestamp": int(time.time()),
    }
    payload.update(msg)
    _log_dup("metrics", payload, logger=stdout_logger, severity='INFO')


def persist(tag: str, msg: dict) -> None:
    """Save log to GCS."""
    payload = {
        "tag": tag,
        "timestamp": int(time.time()),
    }
    payload.update(msg)
    _log_dup("persist", payload, logger=stdout_logger, severity='INFO')
