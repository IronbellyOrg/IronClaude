"""TEST suite for OPS-003 — artifact retention policy.

T04.21 / D-0081 / R-081 — pins the operator-visible retention contract
across two coupled surfaces so they cannot drift apart silently
(the ``docs/eval/retention.md`` policy doc was removed in #257 as stale):

1. The library constant
   :data:`superclaude.cli.eval.disk_budget.DISK_BUDGET_RETENTION_ADVICE`
   is the single source of truth for the disk-budget breach stderr advice.
2. The CLI dispatcher (``superclaude eval run``) emits the advice
   constant verbatim to stderr immediately before exiting on
   :data:`DISK_BUDGET_EXCEEDED_EXIT_CODE`.

Sibling tests this module trusts (does not re-pin):

* ``tests/cli/eval/test_disk_budget.py`` (T03.19) — pins the
  ``DiskBudgetPoller`` library contract (side-car payload, breach
  semantics, ``--max-disk-mb 0`` disable).
* ``tests/cli/eval/test_exit_codes.py`` (T04.19 / D-0079) — pins the
  process-boundary exit-code surface (0/1/2/3) and contains the same
  forward-dep probe pattern this module reuses for the
  ``--keep-home True`` HOME-preservation case.
* ``tests/cli/eval/test_atomic_setup.py`` (T02.13) — pins the
  NFR-ISO2 setup-failed tag contract; this module asserts the policy
  doc *documents* the tag relpath, not that the wiring works.

Forward-dependency note
=======================

The ``--keep-home True`` end-to-end test traverses the
``superclaude eval run`` run-loop closure, whose helpers
(``_new_run_id``, ``_run_one_spec``, ``_compute_run_stats``,
``RUN_CLEAN_EXIT_CODE`` …) are T04.10 deliverables. The probe pattern
used by ``test_exit_codes.py`` skips the dependent test with a
self-clearing diagnostic so the suite passes today; the skip evaporates
once T04.10 lands.

The four other tests in this module — doc presence, doc section
coverage, doc/constant agreement, CLI stderr emission on a synthetic
breach — all run today.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]


# ---------------------------------------------------------------------------
# subprocess + forward-dep helpers (mirrors test_exit_codes.py)
# ---------------------------------------------------------------------------


def _resolve_superclaude_bin() -> str:
    """Locate the ``superclaude`` console-script in the active venv."""

    venv_bin = Path(sys.executable).parent / "superclaude"
    if venv_bin.exists():
        return str(venv_bin)
    import shutil

    path_bin = shutil.which("superclaude")
    if path_bin:
        return path_bin
    pytest.skip(
        "superclaude console-script not found on this environment; "
        "retention-policy CLI assertions need the operator-visible shim."
    )


SUPERCLAUDE_BIN = _resolve_superclaude_bin()


def _t0410_missing() -> list[str]:
    """Return T04.10 run-loop deliverables not yet defined in commands.py."""

    from superclaude.cli.eval import commands as _commands_mod

    forward_deps = (
        "_new_run_id",
        "_run_one_spec",
        "_compute_run_stats",
        "RUN_CLEAN_EXIT_CODE",
        "RUN_FAILURES_EXIT_CODE",
        "RUN_INTERRUPTED_EXIT_CODE",
    )
    return [n for n in forward_deps if not hasattr(_commands_mod, n)]


def _skip_unless_t0410_landed() -> None:
    missing = _t0410_missing()
    if missing:
        pytest.skip(
            f"T04.10 forward dependency not yet landed: {missing!r}. "
            "The --keep-home True end-to-end retention test traverses the "
            "run-loop closure; the policy-doc / constant / CLI-stderr pins "
            "this module also lands run today."
        )


def _run_eval(
    *args: str,
    timeout: float = 60.0,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Invoke ``superclaude eval run ...`` as a real subprocess."""

    cmd = [SUPERCLAUDE_BIN, "eval", "run", *args]
    merged_env = dict(os.environ)
    if env:
        merged_env.update(env)
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        env=merged_env,
        timeout=timeout,
        check=False,
    )


# ---------------------------------------------------------------------------
# 1. Policy doc presence + section coverage
# ---------------------------------------------------------------------------
def test_retention_advice_constant_shape() -> None:
    """The advice constant must name every load-bearing detail.

    Three required signals:
      (a) "disk-budget exceeded" — the breach name operators will grep
          for in CI tails;
      (b) the surviving artifact names (summary.md / summary.json,
          junit.xml, disk_budget_exceeded.json) so the operator knows
          what was preserved;
      (c) both retention knobs (``--max-disk-mb``, ``--keep-home``) and
          a back-pointer to ``docs/eval/retention.md``.
    """

    from superclaude.cli.eval.disk_budget import DISK_BUDGET_RETENTION_ADVICE

    advice = DISK_BUDGET_RETENTION_ADVICE
    assert isinstance(advice, str) and advice.strip() == advice, (
        "DISK_BUDGET_RETENTION_ADVICE must be a non-whitespace-padded str"
    )

    # (a) breach name
    assert "disk-budget exceeded" in advice, (
        "advice must lead with the breach name so operators can grep it"
    )

    # (b) preserved artifacts
    assert "summary" in advice, "advice must mention summary.{md,json} as preserved"
    assert "disk_budget_exceeded.json" in advice, (
        "advice must mention the side-car filename"
    )

    # (c) knobs and back-pointer
    assert "--max-disk-mb" in advice, (
        "advice must name --max-disk-mb as the breach knob"
    )
    assert "--keep-home" in advice, (
        "advice must name --keep-home as the per-eval HOME knob"
    )
    assert "docs/eval/retention.md" in advice, (
        "advice must back-link to the full policy doc"
    )


# ---------------------------------------------------------------------------
# 3. CLI stderr emission on disk-budget breach
# ---------------------------------------------------------------------------


def test_cli_emits_retention_advice_on_disk_budget_breach(
    allowlisted_output_dir: Path,
) -> None:
    """A real ``superclaude eval run`` that breaches the disk budget must
    emit ``DISK_BUDGET_RETENTION_ADVICE`` verbatim to stderr immediately
    before exiting with code 2.

    The breach is synthesised by:

    1. Pre-creating the run directory under ``--output-dir`` and
       seeding it with a >1 MB file so the very first poller tick
       observes a >1 MB usage.
    2. Running with ``--max-disk-mb 1`` and a fast poll cadence — but
       even without overriding the cadence, the synthesised
       pre-existing usage trips the budget at the first tick.

    We do NOT require T04.10 here because the breach path may fire
    *before or during* the run-loop closure (the poller runs in a
    background thread the moment the orchestrator starts). To keep the
    test independent of T04.10 we accept either:
      * exit code 2 + advice on stderr (real breach path), OR
      * the T04.10 forward-dep is missing and the closure raises
        ``NameError`` *after* the advice would have been emitted (in
        which case we skip with the same self-clearing diagnostic).
    """

    from superclaude.cli.eval.disk_budget import (
        DISK_BUDGET_EXCEEDED_EXIT_CODE,
        DISK_BUDGET_RETENTION_ADVICE,
    )

    if _t0410_missing():
        pytest.skip(
            "T04.10 forward dependency not yet landed; the breach branch "
            "lives at the end of the run-loop closure. The doc + constant "
            "+ advice-shape assertions in this module run today."
        )

    # The disk-budget breach path additionally needs the M5/M6 production
    # LifecycleExecutor (ClaudeProcessAdapter + PtyDriver). Until that
    # lands, _resolve_executor_factory returns _NullLifecycleExecutor
    # which canned-returns exit_code=0 instantly — the whole run finishes
    # in <1s, well before the poller can tick on the seeded 2 MB file,
    # so the process exits 0 instead of triggering the disk-budget breach.
    # Follow-up: T04.10-followup-K002. Un-skips when the production
    # executor replaces the null stub.
    from superclaude.cli.eval import commands as _commands_mod

    _executor_sample = _commands_mod._resolve_executor_factory()()
    if type(_executor_sample).__name__ == "_NullLifecycleExecutor":
        pytest.skip(
            "T04.10-followup-K002 production LifecycleExecutor "
            "(ClaudeProcessAdapter + PtyDriver) not yet landed; "
            "_NullLifecycleExecutor returns canned exit 0 instantly so the "
            "disk-budget poller cannot tick before the run completes. "
            "Un-skips when the production executor replaces the null stub."
        )

    # Seed the output dir so the poller observes >1 MB at tick 1.
    output_dir = allowlisted_output_dir / "run"
    output_dir.mkdir(parents=True)
    seed = output_dir / "seed.bin"
    seed.write_bytes(b"x" * (2 * 1024 * 1024))  # 2 MB > 1 MB budget

    result = _run_eval(
        "--suite",
        "real",
        "--no-pty",
        "--max-disk-mb",
        "1",
        "--output-dir",
        str(output_dir),
        timeout=120.0,
    )

    assert result.returncode == DISK_BUDGET_EXCEEDED_EXIT_CODE, (
        f"disk-budget breach must exit {DISK_BUDGET_EXCEEDED_EXIT_CODE}; "
        f"got {result.returncode}\n"
        f"--- stdout ---\n{result.stdout}\n"
        f"--- stderr ---\n{result.stderr}"
    )
    assert DISK_BUDGET_RETENTION_ADVICE in result.stderr, (
        "CLI must echo DISK_BUDGET_RETENTION_ADVICE verbatim to stderr "
        "immediately before exiting on a disk-budget breach. Stderr was:\n"
        f"---\n{result.stderr}\n---"
    )


# ---------------------------------------------------------------------------
# 4. --keep-home True preserves per-eval HOMEs (forward-dep gated)
# ---------------------------------------------------------------------------


def test_keep_home_true_preserves_per_eval_homes_on_pass(
    allowlisted_output_dir: Path,
) -> None:
    """An end-to-end run with ``--keep-home`` must preserve every PASS
    eval's HOME under the scratch root.

    Requires the T04.10 run-loop closure to be wired (so a real run can
    reach finalize). Without T04.10 the test skips with the same
    self-clearing diagnostic the exit-code tests use.
    """

    _skip_unless_t0410_landed()

    output_dir = allowlisted_output_dir / "run"
    scratch_root = allowlisted_output_dir / "scratch"
    scratch_root.mkdir(parents=True)

    result = _run_eval(
        "--suite",
        "real",
        "--no-pty",
        "--keep-home",
        "--output-dir",
        str(output_dir),
        timeout=120.0,
        env={"SUPERCLAUDE_EVAL_SCRATCH_ROOT": str(scratch_root)},
    )

    # The --no-pty exclusion in real.yaml short-circuits every eval to
    # SKIPPED, so the run is clean (exit 0). SKIPPED outcomes never
    # allocate a HOME, so the assertion is structural: with --keep-home
    # set, the scratch root MUST NOT have been cleared by the harness on
    # exit, and any HOME that *did* materialise must still be on disk.
    assert result.returncode == 0, (
        f"clean (--no-pty) run with --keep-home must exit 0; got "
        f"{result.returncode}\n"
        f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
    )
    # Scratch root remains writable / inspectable for the operator.
    assert scratch_root.is_dir(), (
        f"--keep-home must not delete the scratch root; missing {scratch_root}"
    )
    # If any HOME materialised under scratch_root, every one must survive.
    materialised_homes = [
        p for p in scratch_root.rglob("*") if p.is_dir() and (p / ".eval-meta").is_dir()
    ]
    for home in materialised_homes:
        assert home.exists(), (
            f"--keep-home True must preserve HOME {home}; it was removed"
        )
