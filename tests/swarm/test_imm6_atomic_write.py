"""T03.13 -- IMM-6 atomic-write idempotency sweep across every writer.

IMM-6 / NFR-002 contract: every durable artifact in the swarm package
is written through the ``tmp + os.replace`` idiom (or, for the
append-only event log, a ``threading.Lock`` + ``O_APPEND`` pair). A
SIGKILL between the tmp write and the swap MUST leave the live path
in one of two states:

    * **absent**  -- the swap never happened, no prior file existed.
    * **prior**   -- the swap never happened, the previous live file
                     is still intact byte-for-byte.

What MUST never appear is a *partial* live path: a half-flushed file
that looks like the new write but is truncated mid-payload. The
matching rerun arm asserts that after a kill, running the writer
again produces the expected content -- the leftover ``.tmp`` sibling
must not block recovery.

This file is the cross-writer sweep that complements the per-module
mid-write-kill test in ``tests/swarm/test_state.py``
(``test_mid_write_kill_leaves_no_partial_state_file``). The phase-3
tasklist (T03.13) lists the writer surface as ``state, log, contract,
sentinel``:

    * **state**   -- ``superclaude.cli.swarm.state.write_state`` writes
                     ``.swarm-state.json``.
    * **manifest** -- ``superclaude.cli.swarm.preflight.write_manifest``
                     writes ``manifest.json`` (the Wave-0 source-of-truth
                     artifact; the spec-level "contract" surface).
    * **env-missing contract** --
                     ``superclaude.cli.swarm.preflight.emit_env_missing_contract``
                     writes ``return-contract.yaml`` on the INV-007 /
                     OQ-008 failure path.
    * **log**     -- ``superclaude.cli.swarm.logging_.Logger`` is the
                     append-only surface. It does NOT use ``os.replace``
                     because append-only files have a different atomicity
                     model: a per-Logger ``threading.Lock`` plus
                     ``open(path, "a")`` (which opens with ``O_APPEND``
                     so the kernel positions each ``write(2)`` at
                     end-of-file atomically). A mid-write kill there
                     leaves either zero bytes or a complete line --
                     never a partial one -- because each event is one
                     ``write`` syscall under the lock. This module pins
                     that behavior with a static-source assertion so a
                     regression to ``open(path, "w")`` (truncating
                     write) is caught here.
    * **sentinel** -- the ``DoneSentinel`` (``done.json``) writer lands
                     in M5/M6 with the executor terminal-emit path.
                     The dataclass exists today (``DM-017``); the
                     writer does not. This module pins the dataclass
                     contract today and the IMM-6 rerun arm for the
                     sentinel writer is deferred to T05.* with a
                     forward-reference comment so the gap is auditable.

Validation grep (phase-3-tasklist T03.13)::

    grep -RnE "os\\.replace\\(" src/superclaude/cli/swarm/

must surface a hit in every writer module on the ``os.replace``
contract (state.py, preflight.py). The log module is intentionally
excluded; the static-source assertion in
:func:`test_log_module_uses_append_only_not_replace` documents why.
"""

from __future__ import annotations

import json
import signal
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

# IMM-6 atomic-write mid-write kill (T08.03 / NFR-007). Module-level
# marker so every test in this file is selected by ``pytest -m imm``.
pytestmark = pytest.mark.imm


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
SWARM_PKG = SRC_DIR / "superclaude" / "cli" / "swarm"


# ---------------------------------------------------------------------------
# Static grep sweep -- every os.replace-shaped writer must call os.replace.
# ---------------------------------------------------------------------------


_OS_REPLACE_WRITERS: tuple[tuple[str, str], ...] = (
    # (module-relative-path, short-name-for-error-messages)
    ("state.py", "write_state"),
    ("preflight.py", "write_manifest / emit_env_missing_contract"),
)


@pytest.mark.parametrize(
    "module_rel,writer_label",
    _OS_REPLACE_WRITERS,
    ids=[label for _, label in _OS_REPLACE_WRITERS],
)
def test_writer_module_calls_os_replace(module_rel: str, writer_label: str) -> None:
    """Each ``os.replace``-shaped writer module must invoke ``os.replace(``.

    This is the static half of the validation grep
    ``grep -RnE 'os\\.replace\\(' src/superclaude/cli/swarm/``: if a
    regression turns one of these writers into a direct ``open(path, "w")``
    call, this test fails before the dynamic mid-write-kill tests even run.
    """
    source = (SWARM_PKG / module_rel).read_text(encoding="utf-8")
    assert "os.replace(" in source, (
        f"{module_rel} owns {writer_label} but no os.replace( call was "
        "found; the tmp+os.replace atomicity contract (NFR-002 / IMM-6) "
        "is broken."
    )


def test_log_module_uses_append_only_not_replace() -> None:
    """``logging_.py`` is append-only; it MUST NOT use ``open(path, "w")``.

    The atomicity model for the event log is per-Logger
    :class:`threading.Lock` + ``O_APPEND`` (``open(path, "a")``), not
    ``os.replace``. The IMM-6 contract is satisfied differently: a
    SIGKILL between two events leaves the file with N or N+1
    *complete* lines -- never a partial one -- because each event is
    one ``write(2)`` syscall under the lock. A regression to ``open
    (path, "w")`` would truncate the file on every event; a regression
    to *no* lock would let parallel workers interleave bytes mid-line.
    Pin both invariants here so a future refactor cannot quietly
    violate either.
    """
    source = (SWARM_PKG / "logging_.py").read_text(encoding="utf-8")
    assert "threading.Lock" in source, (
        "logging_.py must serialize appends with a threading.Lock; "
        "without it concurrent workers can interleave bytes mid-line."
    )
    assert 'open(self.jsonl_path, "a")' in source, (
        "logging_.py must open the JSONL file in append mode ('a' / "
        "O_APPEND) so each write(2) is positioned at end-of-file "
        "atomically by the kernel."
    )
    # Truncating-write regression guard: the logger must never open
    # the JSONL path in a mode that truncates ("w"/"w+"/"wb").
    for forbidden_mode in ('"w"', '"w+"', '"wb"'):
        assert f"open(self.jsonl_path, {forbidden_mode})" not in source, (
            f"logging_.py must never open the JSONL file in {forbidden_mode}; "
            "the append-only contract (NFR-002) requires O_APPEND."
        )


def test_done_sentinel_writer_is_deferred_but_dataclass_exists() -> None:
    """Forward-reference guard for the ``DoneSentinel`` (``done.json``) writer.

    The DM-017 dataclass exists today (``superclaude.cli.swarm.models.
    DoneSentinel``); the executor-side writer that persists
    ``done.json`` lands in M5/M6 with the terminal-emit path. When
    that writer is added, it MUST follow the same tmp+os.replace
    pattern -- this test will fail the moment a ``done.json`` writer
    appears anywhere in the swarm package without ``os.replace`` next
    to it, so the IMM-6 sweep cannot silently grow a gap.
    """
    from superclaude.cli.swarm.models import DoneSentinel  # noqa: F401

    # Sweep the package for any line that writes ``done.json`` (the
    # sentinel filename per DM-017). If one appears, the same module
    # MUST also contain ``os.replace(`` -- otherwise the new writer
    # is bypassing the atomicity contract.
    for source_path in SWARM_PKG.rglob("*.py"):
        text = source_path.read_text(encoding="utf-8")
        # Match only writer-shaped references (file-mode 'w'/'wb' near
        # a done.json string) rather than docstring mentions.
        # We use a conservative heuristic: any line containing
        # ``"done.json"`` paired with ``open(`` on the same line.
        for line in text.splitlines():
            if "done.json" in line and "open(" in line and '"a"' not in line:
                assert "os.replace(" in text, (
                    f"{source_path.relative_to(REPO_ROOT)} appears to "
                    "write done.json without an os.replace( in the "
                    "same module; the sentinel writer must follow the "
                    "tmp+os.replace atomicity contract (IMM-6)."
                )


# ---------------------------------------------------------------------------
# Mid-write SIGKILL -- per-writer subprocess tests.
#
# Each test monkey-patches ``os.replace`` in the writer's module to
# SIGKILL the subprocess instead of performing the swap. The tmp
# sibling will have been written by then, but the live target must
# not exist (or, if a prior version existed, must be unchanged).
# ---------------------------------------------------------------------------


def _run_suicide_subprocess(
    script_body: str, timeout: float = 15.0
) -> subprocess.CompletedProcess:
    """Execute ``script_body`` in a fresh subprocess and expect SIGKILL exit."""
    completed = subprocess.run(
        [sys.executable, "-c", script_body],
        capture_output=True,
        timeout=timeout,
    )
    assert completed.returncode == -signal.SIGKILL, (
        f"subprocess did not SIGKILL itself "
        f"(exit code {completed.returncode}); "
        f"stdout={completed.stdout!r} stderr={completed.stderr!r}"
    )
    return completed


def test_state_mid_write_kill_leaves_no_partial_live_file(tmp_path: Path) -> None:
    """``write_state`` mid-write SIGKILL: live ``.swarm-state.json`` absent."""
    target = tmp_path / ".swarm-state.json"

    script = textwrap.dedent(
        f"""
        import os, signal, sys
        sys.path.insert(0, {str(SRC_DIR)!r})

        from superclaude.cli.swarm.models import SwarmState
        from superclaude.cli.swarm import state as state_mod

        def _suicide(*_a, **_kw):
            os.kill(os.getpid(), signal.SIGKILL)

        state_mod.os.replace = _suicide
        state_mod.write_state({str(target)!r}, SwarmState(job_id="job-state-kill"))
        """
    ).strip()

    _run_suicide_subprocess(script)

    assert not target.exists(), (
        "Mid-write SIGKILL left a partial .swarm-state.json at the live "
        "path; tmp+os.replace contract (NFR-002) violated."
    )


def test_manifest_mid_write_kill_leaves_no_partial_live_file(tmp_path: Path) -> None:
    """``write_manifest`` mid-write SIGKILL: live ``manifest.json`` absent."""
    target = tmp_path / "manifest.json"

    script = textwrap.dedent(
        f"""
        import os, signal, sys
        sys.path.insert(0, {str(SRC_DIR)!r})

        from superclaude.cli.swarm.models import Manifest
        from superclaude.cli.swarm import preflight as preflight_mod

        def _suicide(*_a, **_kw):
            os.kill(os.getpid(), signal.SIGKILL)

        preflight_mod.os.replace = _suicide
        preflight_mod.write_manifest(Manifest(job_id="job-manifest-kill"), {str(tmp_path)!r})
        """
    ).strip()

    _run_suicide_subprocess(script)

    assert not target.exists(), (
        "Mid-write SIGKILL left a partial manifest.json at the live "
        "path; tmp+os.replace contract (NFR-002 / IMM-6) violated."
    )


def test_env_missing_contract_mid_write_kill_leaves_no_partial_live_file(
    tmp_path: Path,
) -> None:
    """``emit_env_missing_contract`` mid-write SIGKILL: live YAML absent."""
    target = tmp_path / "return-contract.yaml"

    script = textwrap.dedent(
        f"""
        import os, signal, sys
        sys.path.insert(0, {str(SRC_DIR)!r})

        from superclaude.cli.swarm.models import JobSpec
        from superclaude.cli.swarm import preflight as preflight_mod

        def _suicide(*_a, **_kw):
            os.kill(os.getpid(), signal.SIGKILL)

        preflight_mod.os.replace = _suicide

        job = JobSpec(job_id="job-contract-kill")
        job.output.dir = {str(tmp_path)!r}
        preflight_mod.emit_env_missing_contract(job)
        """
    ).strip()

    _run_suicide_subprocess(script)

    assert not target.exists(), (
        "Mid-write SIGKILL left a partial return-contract.yaml at the "
        "live path; tmp+os.replace contract (NFR-002 / IMM-6) violated."
    )


# ---------------------------------------------------------------------------
# Idempotency: after the kill, re-invoking the writer succeeds and the
# result is identical to a single clean run. Leftover ``.tmp`` siblings
# (from any prior crash) must not block recovery.
# ---------------------------------------------------------------------------


def test_state_rerun_after_kill_is_idempotent(tmp_path: Path) -> None:
    """After SIGKILL, re-running ``write_state`` produces a clean live file.

    Simulates the leftover-tmp-from-prior-crash scenario by pre-seeding
    the ``.tmp`` sibling with garbage. The next call must succeed,
    overwrite the tmp via the standard write, and leave a clean live
    path with the expected payload.
    """
    from superclaude.cli.swarm.models import SwarmState
    from superclaude.cli.swarm.state import read_state, write_state

    target = tmp_path / ".swarm-state.json"
    leftover_tmp = target.with_suffix(target.suffix + ".tmp")
    leftover_tmp.write_text("partial-write-from-prior-crash", encoding="utf-8")

    write_state(target, SwarmState(state="dispatching", job_id="job-state-rerun"))

    loaded = read_state(target)
    assert loaded is not None
    assert loaded.state == "dispatching"
    assert loaded.job_id == "job-state-rerun"
    assert not leftover_tmp.exists(), (
        "Leftover .tmp sibling must be consumed by the successful "
        "os.replace; recovery is not idempotent if garbage remains."
    )


def test_manifest_rerun_after_kill_is_idempotent(tmp_path: Path) -> None:
    """After SIGKILL, re-running ``write_manifest`` produces a clean file."""
    from superclaude.cli.swarm.models import Manifest, from_json
    from superclaude.cli.swarm.preflight import write_manifest

    target = tmp_path / "manifest.json"

    # Pre-seed a leftover tmp (the tempfile.mkstemp prefix is
    # ``.manifest-`` per preflight.write_manifest); the writer must
    # not be blocked by stale tmp files in the output directory.
    stale = tmp_path / ".manifest-stale.json.tmp"
    stale.write_text("partial-write-from-prior-crash", encoding="utf-8")

    written_path = write_manifest(Manifest(job_id="job-manifest-rerun"), tmp_path)
    assert Path(written_path) == target.resolve()

    payload = target.read_text(encoding="utf-8")
    parsed = json.loads(payload)
    assert parsed["job_id"] == "job-manifest-rerun"

    # Round-trip via the canonical decoder to confirm byte-stability
    # (INV-016): the rerun output is what the resume path will read.
    rehydrated = from_json(Manifest, payload)
    assert rehydrated.job_id == "job-manifest-rerun"

    # A second clean run produces byte-identical content (INV-016 /
    # IMM-6 idempotency arm).
    write_manifest(Manifest(job_id="job-manifest-rerun"), tmp_path)
    assert target.read_text(encoding="utf-8") == payload


def test_env_missing_contract_rerun_after_kill_is_idempotent(tmp_path: Path) -> None:
    """After SIGKILL, re-running ``emit_env_missing_contract`` is idempotent."""
    from superclaude.cli.swarm.models import JobSpec
    from superclaude.cli.swarm.preflight import emit_env_missing_contract

    job = JobSpec(job_id="job-contract-rerun")
    job.output.dir = str(tmp_path)

    target = tmp_path / "return-contract.yaml"

    # Pre-seed a stale tmp sibling matching the writer's prefix
    # (``.return-contract-``).
    stale = tmp_path / ".return-contract-stale.yaml.tmp"
    stale.write_text("partial-write-from-prior-crash", encoding="utf-8")

    first_path = emit_env_missing_contract(job)
    assert first_path is not None
    assert Path(first_path) == target.resolve()

    first_bytes = target.read_bytes()

    # Re-run with the same JobSpec: the writer should be idempotent
    # (env-missing contracts capture a deterministic envelope; the
    # only volatile fields -- ``started`` / ``finished`` / ``elapsed_ms``
    # -- are zero/empty on the failure path).
    second_path = emit_env_missing_contract(job)
    assert second_path == first_path
    assert target.read_bytes() == first_bytes, (
        "Two clean runs of emit_env_missing_contract with the same "
        "JobSpec must produce byte-identical files (IMM-6 idempotency)."
    )


# ---------------------------------------------------------------------------
# Cross-cutting: confirm no writer module under cli/swarm/ opens a
# ``.json`` or ``.yaml`` path directly in truncating-write mode.
# ---------------------------------------------------------------------------


def test_no_writer_module_uses_truncating_open_for_live_artifact() -> None:
    """No ``open(<live-artifact-path>, "w")`` calls in the swarm package.

    Walks every ``.py`` file under ``src/superclaude/cli/swarm/`` and
    fails if a source line opens a known live-artifact path (state
    file, manifest, contract, done sentinel) in truncating-write
    mode. The exception is the ``.tmp`` sibling which is the staging
    file before ``os.replace`` -- that is the entire point of the
    pattern.
    """
    forbidden_targets = (
        '".swarm-state.json"',
        '"manifest.json"',
        '"return-contract.yaml"',
        '"done.json"',
    )
    for source_path in SWARM_PKG.rglob("*.py"):
        text = source_path.read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.strip()
            # Skip comments / docstrings: only flag real open() calls.
            if stripped.startswith("#"):
                continue
            for target in forbidden_targets:
                if target in stripped and "open(" in stripped:
                    # Allow append-only mode for the event log (does
                    # not match any of the forbidden targets above,
                    # but keep the guard tight).
                    assert '"a"' in stripped, (
                        f"{source_path.relative_to(REPO_ROOT)}: "
                        f"{stripped!r} opens a live artifact "
                        "directly; writes MUST go through tmp+os.replace "
                        "(NFR-002 / IMM-6)."
                    )
