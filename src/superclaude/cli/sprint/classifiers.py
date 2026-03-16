"""Classifier registry for preflight executor task result classification.

Classifiers evaluate subprocess output (exit code, stdout, stderr) and return
a classification label string. The registry maps classifier names to callables.
"""

from __future__ import annotations

import logging
from typing import Callable

logger = logging.getLogger(__name__)

# Registry mapping classifier names to classifier callables.
# Each callable signature: (exit_code: int, stdout: str, stderr: str) -> str
CLASSIFIERS: dict[str, Callable[[int, str, str], str]] = {}


def empirical_gate_v1(exit_code: int, stdout: str, stderr: str) -> str:
    """Classify based solely on subprocess exit code.

    Returns ``"pass"`` when exit_code is 0, ``"fail"`` otherwise.
    """
    return "pass" if exit_code == 0 else "fail"


CLASSIFIERS["empirical_gate_v1"] = empirical_gate_v1


def run_classifier(name: str, exit_code: int, stdout: str, stderr: str) -> str:
    """Look up and invoke a classifier by name.

    Raises:
        KeyError: If *name* is not present in :data:`CLASSIFIERS`.

    Returns:
        Classification label string.  On any exception raised by the
        classifier itself, logs a WARNING and returns ``"error"``.
    """
    fn = CLASSIFIERS[name]  # KeyError propagates to caller on unknown name
    try:
        return fn(exit_code, stdout, stderr)
    except Exception as exc:
        logger.warning("Classifier %s raised %s: %s", name, type(exc).__name__, exc)
        return "error"
