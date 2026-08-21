"""Structured logging for the onboard mission application (D2.12).

Produces JSON log lines by default (one JSON object per line), enabling
machine-parseable logs that can be consumed by systemd-journald, `jq`, or
a dedicated log shipper. Falls back to text format for local debugging.

Usage:
    from mission_app_logging import get_logger
    log = get_logger("mission_app")
    log.info("Started", extra={"state": "SWEEP", "alt_m": 120.0})

Thread-safe (RotatingFileHandler uses a lock internally).
"""

from __future__ import annotations

import json
import logging
import logging.handlers
import os
import sys
import time
from typing import Any, Optional


# Attribute names every stdlib LogRecord carries -- used to distinguish
# caller-supplied `extra={}` fields from LogRecord's own bookkeeping.
_STANDARD_LOGRECORD_ATTRS = frozenset(
    logging.LogRecord("", 0, "", 0, "", (), None).__dict__.keys()
) | {"message", "asctime"}


class JSONFormatter(logging.Formatter):
    """Emit log records as newline-delimited JSON objects.

    Each line has at minimum: ts (unix float), level, logger, msg. Every
    extra keyword passed via `extra={}` appears as a top-level key -- not
    just a fixed whitelist, so new field names (added at any call site)
    show up without touching this formatter.
    """

    def format(self, record: logging.LogRecord) -> str:
        obj: dict[str, Any] = {
            "ts": record.created,
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        for key, val in record.__dict__.items():
            if key in _STANDARD_LOGRECORD_ATTRS or key in obj:
                continue
            obj[key] = val

        # Include exception info if present
        if record.exc_info and record.exc_info[0] is not None:
            obj["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
            }

        return json.dumps(obj, default=str, separators=(",", ":"))


class TextFormatter(logging.Formatter):
    """Human-readable log format (for development / SITL runs)."""

    def format(self, record: logging.LogRecord) -> str:
        # E.g. "14:32:01.234 [INFO] mission_app SWEEP @120.0m — Started"
        t = time.strftime("%H:%M:%S", time.localtime(record.created))
        ms = int((record.created - int(record.created)) * 1000)
        state = getattr(record, "state", "")
        alt = getattr(record, "alt_m", None)
        loc = f" {state} @{alt:.0f}m" if alt is not None and state else ""
        base = f"{t}.{ms:03d} [{record.levelname}] {record.name}{loc} — {record.getMessage()}"
        extras = {k: v for k, v in record.__dict__.items()
                  if k not in _STANDARD_LOGRECORD_ATTRS and k not in ("state", "alt_m")}
        if extras:
            base += " (" + " ".join(f"{k}={v}" for k, v in extras.items()) + ")"
        if record.exc_info and record.exc_info[0] is not None:
            base += f" | exception={record.exc_info[0].__name__}: {record.exc_info[1]}"
        return base


_LOGGERS: dict[str, logging.Logger] = {}

# Runtime cache of the handler configuration so we don't re-add handlers on
# repeated calls. Module-level so it survives logger garbage collection.
_HANDLER_INIT_DONE = set()


def setup_logging(
    *,
    level: str = "INFO",
    file_path: Optional[str] = None,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
    fmt: str = "json",
    forward_to_journal: bool = True,
) -> None:
    """Configure the root logging hierarchy.

    Call once at startup.  All subsequent ``get_logger()`` calls inherit these
    settings.  Idempotent within the same process (multiple calls are no-ops).

    Args:
        level: Minimum log level (DEBUG, INFO, WARNING, ERROR).
        file_path: Path to the log file.  If None, file logging is skipped.
        max_bytes: Max size of one log file before rotation.
        backup_count: Number of rotated archives to keep.
        fmt: "json" or "text".
        forward_to_journal: If True, also log to stderr so systemd captures it.
    """
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    root_key = f"root_{fmt}_{file_path}"
    if root_key in _HANDLER_INIT_DONE:
        return

    # Build the formatter
    formatter: logging.Formatter
    if fmt == "json":
        formatter = JSONFormatter()
    else:
        formatter = TextFormatter()

    # File handler with rotation
    if file_path:
        dirname = os.path.dirname(file_path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        fh = logging.handlers.RotatingFileHandler(
            file_path, maxBytes=max_bytes, backupCount=backup_count
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    # stderr handler (for systemd/journald capture)
    if forward_to_journal:
        sh = logging.StreamHandler(sys.stderr)
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    _HANDLER_INIT_DONE.add(root_key)


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """Get or create a named logger, pre-configured with the root settings.

    Args:
        name: Logger name (typically the module name, e.g. "mission_app").
        level: Optional per-logger override (e.g. "DEBUG" for verbose modules).

    Returns:
        A :class:`logging.Logger` instance.
    """
    logger = logging.getLogger(name)
    if level:
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    return logger