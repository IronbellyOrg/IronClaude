"""Crash-window recovery for the ``sc:pr-submit`` core (spec §12.1 / INV-007).

On ``--resume``, state is reconstructed from the authoritative JSONL. If the latest
event for an idempotency key is ``push_initiated`` with no matching ``push_completed``
(the crash window), the monitor MUST NOT create another commit or push until it
queries the remote for ``target_sha`` and branches three ways:

- **A (reachable)** → append ``push_completed{recovered:true}``, resume in
  ``S5_AWAITING_REREVIEW``;
- **B (not reachable)** → append ``push_aborted_or_not_landed{recovered:true}``,
  re-drive the push for the SAME cycle **without recomputing the fix**;
- **C (ambiguous tip)** → ``HALT_HUMAN`` with the original fields + observed remote SHA.

Core purity: the LIVE remote query is performed by the SKILL/script; this module
DECIDES the branch from data, consuming the remote-reachability result as an input.
It contains no shell or version-control command tokens.
"""

from __future__ import annotations

from .models import EventType, MonitorState
from .run_log import RunLog

# Branch outcomes.
BRANCH_A_LANDED = "landed"
BRANCH_B_NOT_LANDED = "not_landed"
BRANCH_C_AMBIGUOUS = "ambiguous"


def resume(run_log_path) -> dict:
    """Reconstruct state from a run-log path's JSONL (the NFR-6 authority rule)."""
    from pathlib import Path

    path = Path(run_log_path)
    # A path that looks like a run-log file (``.jsonl`` suffix) OR is an existing
    # file resolves to its parent dir. The suffix check is load-bearing: a
    # not-yet-created ``monitor-run-<PR>.jsonl`` (resume before the file exists, or
    # a typo'd path) returns False from ``is_file()`` and would otherwise be
    # mis-detected as a directory — RunLog would then ``mkdir`` the file path and
    # look for the JSONL *inside* it.
    is_file_path = path.is_file() or path.suffix == ".jsonl"
    output_dir = path.parent if is_file_path else path
    # Recover the PR number from the filename ``monitor-run-<PR>.jsonl`` when present.
    pr_number = 0
    if path.name.startswith("monitor-run-") and path.name.endswith(".jsonl"):
        try:
            pr_number = int(path.name[len("monitor-run-") : -len(".jsonl")])
        except ValueError:
            pr_number = 0
    rl = RunLog(pr_number, output_dir)
    return rl.rebuild_state()


def detect_crash_window(run_log: RunLog) -> dict | None:
    """Return the dangling ``push_initiated`` event (no matching ``push_completed``), or None.

    Matches on ``idempotency_key``: a ``push_initiated`` whose key has no later
    ``push_completed`` (or ``push_aborted_or_not_landed``) is the crash window.
    """
    initiated: dict[str, dict] = {}
    finalized: set[str] = set()
    for ev in run_log.read_events():
        key = ev.get("idempotency_key")
        if not key:
            continue
        et = ev.get("event_type")
        if et == EventType.PUSH_INITIATED.value:
            initiated[key] = ev
        elif et in (
            EventType.PUSH_COMPLETED.value,
            EventType.PUSH_ABORTED_OR_NOT_LANDED.value,
        ):
            finalized.add(key)
    for key, ev in initiated.items():
        if key not in finalized:
            return ev
    return None


def resolve_crash_window(
    run_log: RunLog,
    dangling: dict,
    *,
    remote_reachable: bool | None,
    observed_remote_sha: str | None = None,
) -> tuple[str, MonitorState]:
    """Resolve a crash window from the LIVE remote-reachability result (INV-007 3-way).

    ``remote_reachable`` is the result of the SKILL's live remote query (NOT computed
    here): ``True`` = the ``target_sha`` is reachable from the remote branch tip
    (Branch A); ``False`` = the remote still lacks the commit (Branch B); ``None`` =
    the tip moved to an unrelated SHA, ambiguous (Branch C). Returns
    ``(branch, resume_state)`` and appends the appropriate recovery event.
    """
    common = {
        k: dangling[k]
        for k in (
            "run_id",
            "cycle_id",
            "idempotency_key",
            "pre_push_sha",
            "target_sha",
            "target_branch",
            "target_remote",
        )
        if k in dangling
    }

    if remote_reachable is True:
        # Branch A: the push landed — synthesize the missing completion, resume S5.
        run_log.append(
            {
                "event_type": EventType.PUSH_COMPLETED.value,
                "recovered": True,
                **common,
            }
        )
        return BRANCH_A_LANDED, MonitorState.S5_AWAITING_REREVIEW

    if remote_reachable is False:
        # Branch B: not landed — re-drive the push for the SAME cycle WITHOUT
        # recomputing the fix (the worktree edit is preserved; idempotent on fix_key).
        run_log.append(
            {
                "event_type": EventType.PUSH_ABORTED_OR_NOT_LANDED.value,
                "recovered": True,
                **common,
            }
        )
        return BRANCH_B_NOT_LANDED, MonitorState.S4_PUSHING

    # Branch C: ambiguous tip — HALT for a human with the original fields + observed SHA.
    run_log.append(
        {
            "event_type": EventType.TERMINAL_HALTED.value,
            "recovered": True,
            "reason": "ambiguous_remote_tip",
            "observed_remote_sha": observed_remote_sha,
            **common,
        }
    )
    return BRANCH_C_AMBIGUOUS, MonitorState.HALT_HUMAN
