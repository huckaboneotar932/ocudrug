"""Logging helper.

Ref: R4 engineering bar — logging module, no bare print in library code.
"""

from __future__ import annotations

import logging

_CONFIGURED = False


def get_logger(name: str) -> logging.Logger:
    global _CONFIGURED
    if not _CONFIGURED:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(name)s %(levelname)s %(message)s",
        )
        _CONFIGURED = True
    return logging.getLogger(name)
