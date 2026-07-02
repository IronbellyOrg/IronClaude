"""Read-only detection-contract readiness diagnosis."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from superclaude.pr_submit.detection import (
    _CONTRACT_PATH,
    _LOCAL_OVERRIDE_REL,
    DetectionContract,
    _extract_yaml_block,
    _local_override_path,
)

from .evidence import load_evidence
from .states import ContractState


@dataclass(frozen=True)
class Diagnosis:
    """Read-only readiness diagnosis for the locked detection contract."""

    state: ContractState
    checked_paths: list[Path]
    override_present: bool
    override_locked: bool | None
    shipped_locked: bool
    evidence_path: Path | None
    evidence_sha256: str | None
    repo: str | None
    pr_number: int | None
    validation_report_path: Path | None
    validation_result: str | None
    blockers: list[str]
    next_command: str

    def summary(self) -> str:
        """Render safe status, paths, hashes, counts, and blockers only."""
        parts = [
            f"state={self.state.value}",
            f"checked_paths={len(self.checked_paths)}",
            f"override_present={self.override_present}",
        ]
        if self.evidence_path is not None:
            parts.append(f"evidence_path={self.evidence_path}")
        if self.evidence_sha256 is not None:
            parts.append(f"evidence_sha256={self.evidence_sha256}")
        if self.validation_report_path is not None:
            parts.append(f"validation_report={self.validation_report_path}")
        if self.validation_result is not None:
            parts.append(f"validation_result={self.validation_result}")
        if self.blockers:
            parts.append(f"blockers={len(self.blockers)}")
        parts.append(f"next_command={self.next_command}")
        return "\n".join(parts)


def diagnose(
    *,
    repo: str | None = None,
    pr_number: int | None = None,
    cwd: Path | None = None,
) -> Diagnosis:
    """Probe detection-contract readiness without writes, network calls, or arming."""
    base = Path(cwd).resolve() if cwd is not None else Path.cwd()
    override_path = _override_path_for(base, cwd_provided=cwd is not None)
    shipped_path = Path(_CONTRACT_PATH)
    checked_paths = [override_path, shipped_path]

    override_present = override_path.exists()
    shipped_contract, shipped_error = _read_contract(shipped_path)
    shipped_locked = bool(shipped_contract.locked) if shipped_contract else False

    if not override_present:
        blockers = ["No local locked detection contract override exists."]
        if shipped_error:
            blockers.append(f"Shipped contract could not be parsed: {shipped_error}")
        return Diagnosis(
            state=ContractState.MISSING,
            checked_paths=checked_paths,
            override_present=False,
            override_locked=None,
            shipped_locked=shipped_locked,
            evidence_path=None,
            evidence_sha256=None,
            repo=repo,
            pr_number=pr_number,
            validation_report_path=None,
            validation_result=None,
            blockers=blockers,
            next_command=_next_command(ContractState.MISSING, repo, pr_number),
        )

    contract, parse_error = _read_contract(override_path)
    if contract is None:
        return Diagnosis(
            state=ContractState.UNPARSEABLE,
            checked_paths=checked_paths,
            override_present=True,
            override_locked=None,
            shipped_locked=shipped_locked,
            evidence_path=None,
            evidence_sha256=None,
            repo=repo,
            pr_number=pr_number,
            validation_report_path=None,
            validation_result=None,
            blockers=[f"Local contract could not be parsed: {parse_error}"],
            next_command=_next_command(ContractState.UNPARSEABLE, repo, pr_number),
        )

    if not contract.locked:
        return Diagnosis(
            state=ContractState.UNLOCKED,
            checked_paths=checked_paths,
            override_present=True,
            override_locked=False,
            shipped_locked=shipped_locked,
            evidence_path=None,
            evidence_sha256=None,
            repo=repo,
            pr_number=pr_number,
            validation_report_path=None,
            validation_result=None,
            blockers=["Local detection contract is locked:false."],
            next_command=_next_command(ContractState.UNLOCKED, repo, pr_number),
        )

    evidence_path = _resolve_optional_path(contract.probe_evidence, base)
    if (
        evidence_path is None
        or not evidence_path.exists()
        or not evidence_path.is_file()
    ):
        return Diagnosis(
            state=ContractState.EVIDENCE_MISSING,
            checked_paths=checked_paths,
            override_present=True,
            override_locked=True,
            shipped_locked=shipped_locked,
            evidence_path=evidence_path,
            evidence_sha256=None,
            repo=repo,
            pr_number=pr_number,
            validation_report_path=None,
            validation_result=None,
            blockers=["Locked contract probe_evidence is missing or unreadable."],
            next_command=_next_command(ContractState.EVIDENCE_MISSING, repo, pr_number),
        )

    evidence_sha256 = _evidence_sha256(evidence_path)
    validation_report_path = evidence_path.parent / "validation-report.yaml"
    if not validation_report_path.exists():
        return Diagnosis(
            state=ContractState.VALIDATION_MISSING,
            checked_paths=checked_paths,
            override_present=True,
            override_locked=True,
            shipped_locked=shipped_locked,
            evidence_path=evidence_path,
            evidence_sha256=evidence_sha256,
            repo=repo,
            pr_number=pr_number,
            validation_report_path=validation_report_path,
            validation_result=None,
            blockers=["No validation report exists for the locked evidence."],
            next_command=_next_command(
                ContractState.VALIDATION_MISSING, repo, pr_number
            ),
        )

    report_data = _read_yaml_file(validation_report_path)
    validation_result = _validation_result(report_data)
    stale_blockers = _stale_blockers(report_data, repo, pr_number, evidence_sha256)
    if stale_blockers:
        state = ContractState.STALE
        blockers = stale_blockers
    elif validation_result != "passed":
        state = ContractState.VALIDATION_FAILED
        blockers = ["Validation report does not record result: passed."]
    else:
        state = ContractState.READY
        blockers = []

    return Diagnosis(
        state=state,
        checked_paths=checked_paths,
        override_present=True,
        override_locked=True,
        shipped_locked=shipped_locked,
        evidence_path=evidence_path,
        evidence_sha256=evidence_sha256,
        repo=repo,
        pr_number=pr_number,
        validation_report_path=validation_report_path,
        validation_result=validation_result,
        blockers=blockers,
        next_command=_next_command(state, repo, pr_number),
    )


def declined_by_user(
    *, repo: str | None = None, pr_number: int | None = None, cwd: Path | None = None
) -> Diagnosis:
    """Return the cancellation state without touching contract files."""
    base = Path(cwd).resolve() if cwd is not None else Path.cwd()
    override_path = _override_path_for(base, cwd_provided=cwd is not None)
    shipped_path = Path(_CONTRACT_PATH)
    return Diagnosis(
        state=ContractState.DECLINED_BY_USER,
        checked_paths=[override_path, shipped_path],
        override_present=override_path.exists(),
        override_locked=None,
        shipped_locked=False,
        evidence_path=None,
        evidence_sha256=None,
        repo=repo,
        pr_number=pr_number,
        validation_report_path=None,
        validation_result=None,
        blockers=[
            "Setup was declined by the user; existing contract files were left untouched."
        ],
        next_command=_next_command(ContractState.DECLINED_BY_USER, repo, pr_number),
    )


def render_pr_submit_missing_contract_halt(diagnosis: Diagnosis) -> str:
    """Render the fail-closed pr-submit missing-contract halt.

    This is presentation-only: it never arms a monitor, mutates PR state, writes a
    lock, or executes the next command it prints.
    """
    checked = "\n".join(f"  - {path}" for path in diagnosis.checked_paths)
    blockers = (
        "\n".join(f"  - {blocker}" for blocker in diagnosis.blockers) or "  - <none>"
    )
    return "\n".join(
        [
            "HALT: detection contract is locked:false (or absent) — run the R1 probe first and flip locked:true before arming (T-210). No monitor was armed. No comments, pushes, retries, resolves, or retriggers were performed.",
            "",
            f"Diagnosis state: {diagnosis.state.value}",
            "Checked paths:",
            checked,
            "Blockers:",
            blockers,
            "Next safe step:",
            f"  {diagnosis.next_command}",
        ]
    )


def _override_path_for(base: Path, *, cwd_provided: bool) -> Path:
    if cwd_provided:
        return base / _LOCAL_OVERRIDE_REL
    return _local_override_path()


def _read_contract(path: Path) -> tuple[DetectionContract | None, str | None]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None, f"absent at {path}"
    except OSError as exc:
        return None, str(exc)

    try:
        block = _extract_yaml_block(text)
        data = yaml.safe_load(block) if block else None
        if not isinstance(data, dict):
            return None, "no parseable YAML block"
        return DetectionContract.from_yaml(data), None
    except Exception as exc:  # noqa: BLE001 - diagnose reports parse failures as state.
        return None, str(exc)


def _resolve_optional_path(value: str | None, base: Path) -> Path | None:
    if not value:
        return None
    path = Path(value)
    if path.is_absolute():
        return path
    return base / path


def _evidence_sha256(path: Path) -> str:
    """Return the same canonical payload hash produced by load_evidence() when possible."""
    probe_dir = path.parent if path.is_file() else path
    try:
        return load_evidence(probe_dir).sha256
    except Exception:  # noqa: BLE001 - diagnosis falls back to byte hash for malformed evidence.
        return _sha256_file(path)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_yaml_file(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return {}
    return data if isinstance(data, dict) else {}


def _validation_result(data: dict[str, Any]) -> str | None:
    for key in ("result", "status", "verdict"):
        value = data.get(key)
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"pass", "passed", "success", "ok"}:
                return "passed"
            if normalized in {"fail", "failed", "error"}:
                return "failed"
            return normalized or None
    return None


def _stale_blockers(
    data: dict[str, Any],
    repo: str | None,
    pr_number: int | None,
    evidence_sha256: str,
) -> list[str]:
    blockers: list[str] = []
    report_repo = _first_str(data, "repo", "repository")
    report_pr = data.get("pr_number", data.get("pr"))
    report_hash = _first_str(data, "evidence_sha256", "sha256", "evidence_hash")

    if repo and report_repo and report_repo != repo:
        blockers.append(
            f"Validation report repo {report_repo!r} does not match {repo!r}."
        )
    if (
        pr_number is not None
        and report_pr is not None
        and str(report_pr) != str(pr_number)
    ):
        blockers.append(
            f"Validation report PR {report_pr!r} does not match {pr_number!r}."
        )
    if report_hash and report_hash != evidence_sha256:
        blockers.append(
            "Validation report evidence hash does not match current evidence."
        )
    return blockers


def _first_str(data: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _next_command(state: ContractState, repo: str | None, pr_number: int | None) -> str:
    repo_arg = f" --repo {repo}" if repo else " --repo <owner/repo>"
    pr_arg = f" --pr {pr_number}" if pr_number is not None else " --pr <number>"
    future_status = f"superclaude reflect contract-status{repo_arg}{pr_arg}"
    future_validate = (
        f"superclaude reflect contract-status --validate{repo_arg}{pr_arg}"
    )
    if state is ContractState.READY:
        return f"/sc:pr-submit --monitor 1{pr_arg}"
    if state is ContractState.DECLINED_BY_USER:
        return (
            "cancelled: setup declined by user; existing contract files left untouched"
        )
    if state in {
        ContractState.VALIDATION_MISSING,
        ContractState.VALIDATION_FAILED,
        ContractState.STALE,
        ContractState.UNLOCKED,
        ContractState.EVIDENCE_MISSING,
    }:
        return future_validate
    return future_status
