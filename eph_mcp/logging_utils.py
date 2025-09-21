"""Utility helpers for structured logging in EPH-MCP."""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Optional


class StructuredJSONFormatter(logging.Formatter):
    """Formatter that outputs logs following the canonical JSON schema."""

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created, tz=timezone.utc)
        log_payload: Dict[str, Any] = {
            "timestamp": timestamp.isoformat(),
            "filename": record.pathname,
            "classname": getattr(record, "classname", ""),
            "function": record.funcName,
            "system_section": getattr(record, "system_section", "general"),
            "line_num": record.lineno,
            "error": getattr(record, "error", ""),
            "db_phase": getattr(record, "db_phase", "none"),
            "method": getattr(record, "method", "NONE"),
            "message": record.getMessage(),
        }

        context = getattr(record, "context", None)
        if context:
            log_payload["context"] = context

        return json.dumps(log_payload, ensure_ascii=False)


class HumanReadableFormatter(logging.Formatter):
    """Formatter that renders a concise human-friendly log line."""

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created, tz=timezone.utc)
        section = getattr(record, "system_section", "general")
        filename = record.pathname
        line = record.lineno
        message = record.getMessage()
        return f"[{timestamp.isoformat()}][{section}][{filename}:{line}] {message}"


class DualStructuredHandler(logging.Handler):
    """Handler that emits both JSON and human readable log lines."""

    def __init__(self) -> None:
        super().__init__()
        self.json_formatter = StructuredJSONFormatter()
        self.human_formatter = HumanReadableFormatter()

    def emit(self, record: logging.LogRecord) -> None:
        json_line = self.json_formatter.format(record)
        human_line = self.human_formatter.format(record)
        stream = sys.stdout
        stream.write(json_line + "\n")
        stream.write(human_line + "\n")
        stream.flush()


class StructuredLoggerAdapter(logging.LoggerAdapter):
    """Logger adapter that injects default structured log metadata."""

    def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
        extra = kwargs.setdefault("extra", {})
        base: Dict[str, Any] = {
            "classname": self.extra.get("classname", ""),
            "system_section": self.extra.get("system_section", "general"),
            "db_phase": "none",
            "method": "NONE",
            "error": "",
            "context": {},
        }
        base.update(self.extra)
        base.update(extra)
        kwargs["extra"] = base
        return msg, kwargs


_LOGGING_CONFIGURED = False


def configure_logging(level: int = logging.INFO) -> None:
    """Configure logging for EPH-MCP once per process."""

    global _LOGGING_CONFIGURED
    if _LOGGING_CONFIGURED:
        return

    logger = logging.getLogger("eph_mcp")
    logger.setLevel(level)
    logger.propagate = False

    handler = DualStructuredHandler()
    handler.setLevel(level)
    logger.addHandler(handler)

    _LOGGING_CONFIGURED = True


def get_logger(module_name: str, system_section: str, *, classname: Optional[str] = None) -> StructuredLoggerAdapter:
    """Return a structured logger adapter for the requested module."""

    configure_logging()

    if not module_name.startswith("eph_mcp"):
        module_name = f"eph_mcp.{module_name}"

    base_logger = logging.getLogger(module_name)
    base_logger.setLevel(logging.INFO)

    adapter_defaults = {
        "classname": classname or module_name.split(".")[-1],
        "system_section": system_section,
    }
    return StructuredLoggerAdapter(base_logger, adapter_defaults)

