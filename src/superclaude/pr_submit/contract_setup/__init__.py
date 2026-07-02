"""Facade for detection-contract setup/readiness helpers.

This package owns diagnosis, file-based evidence loading, candidate derivation,
validation, report writing, and confirmation-gated local-lock writing for the
``sc:pr-submit`` detection contract. Importing the facade is intentionally
side-effect free: it does not arm monitors, call GitHub, or import the pr-submit
FSM.
"""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "CandidateContract",
    "CheckResult",
    "ContractSetupError",
    "ContractSetupRefused",
    "ContractState",
    "Diagnosis",
    "EvidenceBundle",
    "EvidenceUnreadable",
    "FieldProvenance",
    "GateResult",
    "LockGate",
    "SETUP_QUESTIONS",
    "SetupAnswers",
    "SetupQuestion",
    "ValidationReport",
    "declined_by_user",
    "derive_candidate",
    "diagnose",
    "load_evidence",
    "render_pr_submit_missing_contract_halt",
    "validate_candidate",
    "write_lock",
    "write_report",
]

_EXPORT_MODULES = {
    "CandidateContract": ".candidate",
    "CheckResult": ".validation",
    "ContractSetupError": ".writer",
    "ContractSetupRefused": ".writer",
    "ContractState": ".states",
    "Diagnosis": ".diagnosis",
    "EvidenceBundle": ".evidence",
    "EvidenceUnreadable": ".writer",
    "FieldProvenance": ".candidate",
    "GateResult": ".lockgate",
    "LockGate": ".lockgate",
    "SETUP_QUESTIONS": ".questions",
    "SetupAnswers": ".questions",
    "SetupQuestion": ".questions",
    "ValidationReport": ".validation",
    "declined_by_user": ".diagnosis",
    "derive_candidate": ".candidate",
    "diagnose": ".diagnosis",
    "load_evidence": ".evidence",
    "render_pr_submit_missing_contract_halt": ".diagnosis",
    "validate_candidate": ".validation",
    "write_lock": ".writer",
    "write_report": ".writer",
}

if TYPE_CHECKING:  # pragma: no cover - imported for static analysis only
    from .candidate import CandidateContract, FieldProvenance, derive_candidate
    from .diagnosis import (
        Diagnosis,
        declined_by_user,
        diagnose,
        render_pr_submit_missing_contract_halt,
    )
    from .evidence import EvidenceBundle, load_evidence
    from .lockgate import GateResult, LockGate
    from .questions import SETUP_QUESTIONS, SetupAnswers, SetupQuestion
    from .states import ContractState
    from .validation import CheckResult, ValidationReport, validate_candidate
    from .writer import (
        ContractSetupError,
        ContractSetupRefused,
        EvidenceUnreadable,
        write_lock,
        write_report,
    )


def __getattr__(name: str) -> Any:
    """Lazily resolve facade exports without importing implementation modules."""
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = import_module(module_name, __name__)
    value = getattr(module, name)
    globals()[name] = value
    return value
