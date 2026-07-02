"""Readiness states for detection-contract setup."""

from __future__ import annotations

from enum import Enum


class ContractState(str, Enum):
    """Nine operator-facing detection-contract readiness states."""

    MISSING = "missing"
    UNLOCKED = "unlocked"
    UNPARSEABLE = "unparseable"
    EVIDENCE_MISSING = "evidence_missing"
    VALIDATION_MISSING = "validation_missing"
    VALIDATION_FAILED = "validation_failed"
    STALE = "stale"
    READY = "ready"
    DECLINED_BY_USER = "declined_by_user"


def is_ready(state: ContractState) -> bool:
    """Return True only for the validated ready state."""
    return state is ContractState.READY
