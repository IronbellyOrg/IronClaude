"""Fixture for T3: two literal DEAD_LETTER producers + one return."""

from __future__ import annotations


def handle(msg: dict) -> str:
    status = "PENDING"
    if msg.get("attempts", 0) >= 3:
        status = "DEAD_LETTER"
        return status
    if not msg.get("payload"):
        status = "DEAD_LETTER"
    return status
