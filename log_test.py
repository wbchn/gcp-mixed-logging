
import pytest

import log

def test_debug():
    log.debug('this is a debug message')

def test_debug_struct():
    log.debug({
        "integer": 999,
        "text": "plain text",
        "nested": {
            "sub_field": "a nest message"
        }
    })
