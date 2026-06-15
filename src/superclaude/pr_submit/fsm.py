"""The single finite state machine for ``sc:pr-submit`` (spec §5).

Encodes the gate table as three one-line ordinal checks (G-arm / G-edit / G-push)
plus the ``needs_human_decision`` pre-gate override (§5.2), the INV-016 5-predicate
G-push conjunction (§5.3), and the ``run_skill(...)`` integration driver that the
spec's test bodies call and assert on (returns a :class:`~superclaude.pr_submit.models.SkillResult`).

NFR-6 / AC-9 / FR-G1 core purity: this module imports NO ``anthropic`` SDK and
contains ZERO shell / version-control command tokens. All side-effecting I/O (the
review poll, the push, the reply/resolve, the validation commands) is performed by
the skill's bash scripts and the SKILL.md VAL validator; ``fsm.py`` consumes
already-fetched / already-classified data and records DECISIONS only. The
side-effect seams below default to recording-only callables.

This module is extended by Phase 6 (the §10 validation-gate driver, ``S7_VALIDATING``)
and Phase 7 (the L3 push triad ``S4_PUSHING`` / ``S6_REPLYING`` / ``RESOLVING``).
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from typing import Callable

from .loop_guard import should_halt as loop_guard_should_halt
from .models import Finding, MonitorState, PushDecision, SkillResult
from .severity_router import ROUTE_REPORT_ONLY, remap_severity, route

# Defaults (spec FR-1.1 / FR-2.3).
DEFAULT_MAX_ROUNDS = 2
HARD_CAP_MAX_ROUNDS = 5
MIN_POLL_INTERVAL = 30
DEFAULT_TIMEOUT = 1800

POLL_INTERVAL_ERROR = "minimum is 30 seconds"
MAX_ROUNDS_ERROR = "--max-rounds hard cap is 5"

# The exact L1 user-facing proposal prompt (FR-4.1 / T-402).
PROPOSE_PROMPT = "fix these? y/n"


# --------------------------------------------------------------------------- #
# Argument parsing (spec FR-1.1 / FR-1.2 / FR-1.6 / FR-1.7)
# --------------------------------------------------------------------------- #


@dataclass
class SkillArgs:
    """Parsed `sc:pr-submit` flags."""

    monitor: int = 0
    max_rounds: int = DEFAULT_MAX_ROUNDS
    poll_interval: int = MIN_POLL_INTERVAL
    timeout: int = DEFAULT_TIMEOUT
    base: str | None = None
    head: str | None = None
    title: str | None = None
    body: str | None = None
    output_dir: str | None = None
    resume: str | None = None
    yes: bool = False

    @property
    def armed(self) -> bool:
        """The monitor arms only at ordinal >= 1 (G-arm). L0 never arms (T-103/T-110)."""
        return self.monitor >= 1


def build_arg_parser() -> argparse.ArgumentParser:
    """Build the argparse parser for the `sc:pr-submit` command surface."""
    parser = argparse.ArgumentParser(prog="sc:pr-submit", add_help=False)
    parser.add_argument("--monitor", type=int, choices=[0, 1, 2, 3], default=0)
    parser.add_argument(
        "--max-rounds", dest="max_rounds", type=int, default=DEFAULT_MAX_ROUNDS
    )
    parser.add_argument(
        "--poll-interval", dest="poll_interval", type=int, default=MIN_POLL_INTERVAL
    )
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--base", default=None)
    parser.add_argument("--head", default=None)
    parser.add_argument("--title", default=None)
    parser.add_argument("--body", default=None)
    parser.add_argument("--output-dir", dest="output_dir", default=None)
    parser.add_argument("--resume", default=None)
    parser.add_argument("--yes", action="store_true")
    return parser


def parse_args(argv: list[str]) -> SkillArgs:
    """Parse `argv` into :class:`SkillArgs`, enforcing the documented bounds.

    Raises :class:`ValueError` with the EXACT spec message when ``--poll-interval``
    is below 30 (T-111: "minimum is 30 seconds") or ``--max-rounds`` exceeds the
    hard cap of 5 (T-102). ``--monitor`` choices are enforced by argparse (T-101).
    """
    parser = build_arg_parser()
    ns = parser.parse_args(argv)
    if ns.poll_interval < MIN_POLL_INTERVAL:
        raise ValueError(f"--poll-interval {POLL_INTERVAL_ERROR}")
    if ns.max_rounds > HARD_CAP_MAX_ROUNDS:
        raise ValueError(MAX_ROUNDS_ERROR)
    if ns.max_rounds < 0:
        raise ValueError("--max-rounds must be >= 0")
    return SkillArgs(
        monitor=ns.monitor,
        max_rounds=ns.max_rounds,
        poll_interval=ns.poll_interval,
        timeout=ns.timeout,
        base=ns.base,
        head=ns.head,
        title=ns.title,
        body=ns.body,
        output_dir=ns.output_dir,
        resume=ns.resume,
        yes=ns.yes,
    )


# --------------------------------------------------------------------------- #
# Gate predicates (spec §5.2 / §5.3) — one-line ordinal checks, never nested ifs
# --------------------------------------------------------------------------- #


def gate_arm(ordinal: int) -> bool:
    """G-arm: ``ordinal >= 1`` to leave S0_IDLE and enter polling."""
    return ordinal >= 1


def gate_edit(ordinal: int) -> bool:
    """G-edit: ``ordinal >= 2`` to enter S3_FIXING; else route to PROPOSED."""
    return ordinal >= 2


def should_halt_rounds(round_counter: int, max_rounds: int) -> bool:
    """Round-budget gate: ``round_counter >= max_rounds`` (INV-5, ``>=`` not ``>``).

    Delegates to :func:`loop_guard.should_halt` — the canonical, standalone-tested
    fence-post — so there is a SINGLE source for the INV-001 gate predicate (no
    drift between the in-FSM check and the loop-guard module).
    """
    return loop_guard_should_halt(round_counter, max_rounds)


def clamp_max_rounds(effective: int, hard: int = 1) -> int:
    """INV-R3 fallback clamp: ``min(effective, hard)`` (default ``hard=1``, single-shot).

    A pure one-liner mirroring the gate-predicate style. The V1.1 oversized-PR
    auggie-review fallback clamps the effective round budget to 1 on engage — a
    one-way, monotone non-increasing clamp (the run-log monotone-min fold guarantees
    a later higher value never raises it back; this helper provides the clamp value).
    """
    return min(effective, hard)


def evaluate_push_decision(
    *,
    monitor_ordinal: int,
    validation_status: str,
    needs_human_decision: bool,
    round_counter: int,
    max_rounds: int,
    applied_edits: int,
) -> PushDecision:
    """Evaluate the INV-016 5-predicate G-push conjunction (spec §5.3, verbatim).

    A push is authorized iff ALL five predicates hold, ANDed immediately before the
    push: (1) ``monitor_ordinal >= 3``; (2) ``validation_status == "validated"``;
    (3) ``needs_human_decision == false`` for every finding; (4)
    ``round_counter < max_rounds``; (5) ``applied_edits > 0``. The returned
    :class:`PushDecision` records each predicate independently (the write-ahead
    audit primitive) so callers can assert the exact gate that blocked.
    """
    p1 = monitor_ordinal >= 3
    p2 = validation_status == "validated"
    p3 = not needs_human_decision
    p4 = round_counter < max_rounds
    p5 = applied_edits  # int; truthy when > 0
    authorized = bool(p1 and p2 and p3 and p4 and p5 > 0)
    return PushDecision(
        predicate_1_ordinal=p1,
        predicate_2_validated=p2,
        predicate_3_no_human=p3,
        predicate_4_under_cap=p4,
        predicate_5_applied_edits=p5,
        authorized=authorized,
    )


def push_fail_state(decision: PushDecision) -> MonitorState:
    """Map a blocked :class:`PushDecision` to its fail-route terminal (§5.3).

    predicate 3 → HALT_HUMAN; 4 → HALT_MAX_ROUNDS; 5 → TERMINAL_CLEAN (report);
    1–2 → REPORT_ONLY. Evaluated in spec order so the most-specific HALT wins.
    """
    if not decision.predicate_3_no_human:
        return MonitorState.HALT_HUMAN
    if not decision.predicate_4_under_cap:
        return MonitorState.HALT_MAX_ROUNDS
    if decision.predicate_5_applied_edits <= 0:
        return MonitorState.TERMINAL_CLEAN
    return MonitorState.REPORT_ONLY


# --------------------------------------------------------------------------- #
# L3 write-ahead push triad (spec §12.1 / INV-007)
# --------------------------------------------------------------------------- #


def push_idempotency_key(
    run_id: str, cycle_id: str, pre_push_sha: str, target_branch: str
) -> str:
    """The PRE-push idempotency key: ``push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>``.

    Keyed on the PRE-push SHA (not a post-hoc value) so a crash-window resume can
    match a ``push_initiated`` to its cycle and avoid a double push (INV-007).
    """
    return f"push:{run_id}:{cycle_id}:{pre_push_sha}:{target_branch}"


def build_push_triad(
    *,
    run_id: str,
    cycle_id: str,
    round_counter: int,
    pre_push_sha: str,
    target_sha: str,
    target_branch: str,
    target_remote: str,
    decision: PushDecision,
) -> list[dict]:
    """Build the ordered write-ahead push triad records (spec §12.1, verbatim order).

    Returns three event payloads IN ORDER — ``push_decision`` (the authorization
    audit, fsynced first), ``push_initiated`` (fsynced BEFORE the actual push), and
    ``push_completed`` (fsynced after). ``fsm.py`` only RECORDS these decisions; the
    actual push side-effect (the version-control push of ``<sha>:<branch>`` to the
    remote) is the SKILL's job. The idempotency key is on every record so recovery
    can match the triad.
    """
    key = push_idempotency_key(run_id, cycle_id, pre_push_sha, target_branch)
    common = {
        "run_id": run_id,
        "cycle_id": cycle_id,
        "idempotency_key": key,
        "pre_push_sha": pre_push_sha,
        "target_sha": target_sha,
        "target_branch": target_branch,
        "target_remote": target_remote,
    }
    return [
        {
            "event_type": "push_decision",
            "round_counter": round_counter,
            "authorized": decision.authorized,
            "predicates": {
                "p1_ordinal": decision.predicate_1_ordinal,
                "p2_validated": decision.predicate_2_validated,
                "p3_no_human": decision.predicate_3_no_human,
                "p4_under_cap": decision.predicate_4_under_cap,
                "p5_applied_edits": decision.predicate_5_applied_edits,
            },
            **common,
        },
        {
            "event_type": "push_initiated",
            "remote_ref": f"{target_remote}/{target_branch}",
            **common,
        },
        {"event_type": "push_completed", **common},
    ]


# --------------------------------------------------------------------------- #
# Reply construction (spec FR-6.1 / FR-6.5)
# --------------------------------------------------------------------------- #

NO_CODE_CHANGE_TEXT = "no code change applied"
TRIVIAL_FIX_MAX_LINES = 10


def is_groundable(finding: Finding) -> bool:
    """Whether a finding has a valid `file:line` to ground against (EC-9 structural check).

    A finding missing its `file:line` (empty path or a non-positive line) is
    STRUCTURALLY ungroundable and is DROPPED per the hallucination contract — never
    downgraded, never dispatched. This is distinct from the FR-3.5 false-positive
    demote (location exists but the defect does not reproduce → report-only).
    """
    return bool(finding.path) and isinstance(finding.line, int) and finding.line > 0


def audit_validated_not_verified(
    *, validation_status: str, behavioral_test_failures: list | None
) -> dict:
    """INV-015 / AC-13 audit: flag a fix that VALIDATED but is not behaviorally VERIFIED.

    Distinct from verify-before-remediate (FR-3.5, the INPUT-side false-positive
    filter): INV-015 is the OUTPUT-side residual — a genuine, validated fix that
    drifts an untested behavior. When validation passed (``validation_status ==
    "validated"``) yet behavioral tests reveal failures (an untested behavior
    drifted), the cycle is flagged ``validated_not_verified`` and NOT auto-resolved;
    the run-log records ``validated_not_verified`` + ``behavioral_test_failures``.
    """
    failures = list(behavioral_test_failures or [])
    flagged = validation_status == "validated" and bool(failures)
    return {
        "validated_not_verified": flagged,
        "behavioral_test_failures": failures,
    }


def is_trivial_fix(*, changed_lines: int, files: int, single_hunk: bool) -> bool:
    """A fix is trivial iff ≤10 changed lines, a single file, a single contiguous hunk (FR-6.5)."""
    return changed_lines <= TRIVIAL_FIX_MAX_LINES and files == 1 and single_hunk


def build_reply(
    *,
    applied_edits: int,
    sha: str | None = None,
    hunk: str | None = None,
    trivial: bool = False,
) -> str:
    """Construct the thread-reply text citing `applied_edits` status (FR-6.1 / FR-6.5).

    An ``applied_edits == 0`` cycle MUST say "no code change applied" and NEVER
    "resolved" (T-603), and NEVER embeds a suggestion block. A cycle that applied a
    grounded edit summarizes fix + SHA + passing validation; a TRIVIAL fix
    (``trivial`` and a ``hunk``) embeds a fenced ``suggestion`` block reproducing the
    applied hunk (T-640); a non-trivial fix carries prose + SHA only (T-641).
    """
    if applied_edits == 0:
        return (
            f"{NO_CODE_CHANGE_TEXT} — this finding produced no grounded edit; "
            "reporting only, the thread is not marked resolved."
        )
    lines = [
        f"Applied fix in {applied_edits} edit(s); validation passed.",
    ]
    if sha:
        lines.append(f"Commit: {sha}.")
    if trivial and hunk:
        lines.append("```suggestion")
        lines.append(hunk)
        lines.append("```")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Troubleshoot dispatch / seeding (C3b, spec FR-3.3 / FR-3.4)
# --------------------------------------------------------------------------- #


def seed_troubleshoot(finding: Finding) -> dict:
    """Construct the troubleshoot invocation seed for a VERIFIED finding (FR-3.3).

    Returns a dict with ``scope`` (``"<path>:<line>"`` — T-320 asserts this contains
    the finding's file:line), ``issue`` (the finding body), ``type`` (the rubric
    category), and ``route`` (the tier route from :func:`severity_router.route`,
    never ``--depth quick --fix``). The dict is the data the SKILL turns into the
    actual ``> Skill sc:troubleshoot-protocol`` call; the core never shells out.
    """
    if finding.remapped_severity is None:
        remap_severity(finding)
    return {
        "scope": f"{finding.path}:{finding.line}",
        "issue": finding.body,
        "type": finding.category,
        "route": route(finding),
    }


def batch_by_file(findings: list[Finding]) -> list[list[Finding]]:
    """Group findings by file path so same-file findings dispatch as one batch (T-330).

    Preserves first-seen file order; findings within a file keep their order.
    """
    batches: dict[str, list[Finding]] = {}
    for f in findings:
        batches.setdefault(f.path, []).append(f)
    return list(batches.values())


@dataclass
class DispatchPlan:
    """The plan for dispatching verified findings within the round budget (FR-3.4)."""

    batches: list[list[Finding]] = field(default_factory=list)
    truncated: bool = False
    summary: str = ""


def plan_dispatch(
    findings: list[Finding], *, max_rounds: int, current_round: int
) -> DispatchPlan:
    """Batch verified findings by file and TRUNCATE to the remaining round budget (FR-3.4).

    Only dispatchable (non report-only) findings are batched. If the number of
    file-batches exceeds the remaining budget (``max_rounds - current_round``), the
    plan is truncated and ``truncated`` is set with a HALT summary (T-331).
    """
    dispatchable = [f for f in findings if route(f) != ROUTE_REPORT_ONLY]
    all_batches = batch_by_file(dispatchable)
    remaining = max(0, max_rounds - current_round)
    if len(all_batches) > remaining:
        kept = all_batches[:remaining]
        dropped = len(all_batches) - remaining
        return DispatchPlan(
            batches=kept,
            truncated=True,
            summary=(
                f"round budget exhausted: {dropped} finding-batch(es) deferred "
                f"(max_rounds={max_rounds}); HALT with residual summary"
            ),
        )
    return DispatchPlan(batches=all_batches, truncated=False)


# --------------------------------------------------------------------------- #
# §10 validation-gate driver (S7_VALIDATING, VG-1..VG-6, FR-5)
# --------------------------------------------------------------------------- #

# The ordered gate list (spec §10). VG-3 (lint) and VG-4 (format) are TWO DISTINCT
# gates — the documented "make lint != CI ruff format" gotcha. Collapsing them is
# the bug T-511 regresses.
VALIDATION_GATES = ("VG-1", "VG-2", "VG-3", "VG-4", "VG-5", "VG-6")

# Gates that MUST be present and green for "validated" (the mandatory trio: targeted
# tests + lint + format). VG-2 (cross-cutting escalation), VG-5 (sync, skill-self-edits
# only), and VG-6 (PR-target, checked at arm) are conditional — present only when
# applicable, but if present they must be green too.
MANDATORY_GATES = ("VG-1", "VG-3", "VG-4")


def run_validation_gates(results: dict[str, bool]) -> str:
    """Compute ``validation_status`` from the §10 gate results (the S7_VALIDATING driver).

    Returns ``"validated"`` ONLY when every gate that ran is green AND the mandatory
    trio (VG-1 targeted tests, VG-3 lint, VG-4 format) are all present and green —
    the single definition consumed by the INV-016 G-push predicate (2). Any non-zero
    gate (or a missing mandatory gate, i.e. partial-green) yields ``"failed"``.

    NFR-6: this function consumes pass/fail RESULTS; the actual gate commands
    (`uv run pytest` / `make lint` / `uv run ruff format --check`) are executed by the
    SKILL's VAL validator, never here — the core stays free of shell tokens. The
    VG-3≠VG-4 split is load-bearing: a green VG-3 with a failing/absent VG-4 is
    ``"failed"`` (T-511 / T-522), so green lint alone can never authorize a push.
    """
    # Iterate in gate order so the first failure is deterministic.
    for gate in VALIDATION_GATES:
        if gate in results and not results[gate]:
            return "failed"
    for gate in MANDATORY_GATES:
        if not results.get(gate):
            return "failed"
    return "validated"


def pr_target_ok(pr_url: str, target_repo: str) -> bool:
    """Whether ``pr_url`` targets ``target_repo`` — the VG-6 / FM-11 misroute check.

    ``target_repo`` is the RESOLVED ``owner/repo`` of the origin remote, NOT a
    hardcoded constant: the SKILL resolves it at runtime (origin's ``nameWithOwner``,
    fallback the origin remote URL) and passes it in. A returned URL whose owner/repo is
    NOT ``target_repo`` (e.g. the host CLI silently defaulted the PR onto the upstream
    PARENT of a fork) is a misroute → the caller HALTs (`terminal_failed`) and instructs
    the operator to close it (T-108 / FM-11). Core-pure: a pure string check, no
    version-control command tokens.
    """
    if not pr_url or not target_repo:
        return False
    return f"/{target_repo}/" in pr_url or pr_url.rstrip("/").endswith(target_repo)


def origin_ok(origin_url: str, target_repo: str) -> bool:
    """Whether the `origin` remote URL matches the resolved ``target_repo`` (pre-PR check, T-106).

    ``target_repo`` is the resolved ``owner/repo`` the PR is meant to land on (the
    SKILL resolves it from origin at runtime, never a module constant). Accepts https
    or ssh remote URLs — a substring match on ``owner/repo`` works for both (and for a
    trailing repo-suffix). A mismatch (origin points somewhere other than the intended
    target) → HALT before opening the PR. Core-pure: a pure string check (the SKILL
    runs the actual remote query and passes its result here).
    """
    return bool(origin_url) and bool(target_repo) and target_repo in origin_url


def needs_rebase(commits_behind: int) -> bool:
    """Whether the branch is behind its base branch (``origin/<default-branch>``) and must rebase before create (T-107).

    Pure arithmetic: ``commits_behind`` is computed by the SKILL against the repo's
    ACTUAL default branch (resolved by the SKILL from the repo's ``defaultBranchRef``, or
    the explicit ``--base`` override) — not a literal ``master`` assumption.
    """
    return commits_behind > 0


def is_cross_cutting(changed_files: list[str]) -> bool:
    """Whether a change is cross-cutting → escalate VG-1 targeted tests to VG-2 `make test`.

    Cross-cutting when ≥5 files, OR ≥2 distinct top-level packages under ``src/``, OR
    shared infra is touched (hooks / pyproject / conftest / run-log / fsm). A single
    file in one area is targeted-only (T-501); a broad change escalates (T-502).
    The actual ``make test`` execution is the SKILL's job (NFR-6).
    """
    if len(changed_files) >= 5:
        return True
    shared_markers = ("hooks/", "pyproject", "conftest", "run_log", "fsm.py")
    if any(marker in f for f in changed_files for marker in shared_markers):
        return True
    packages: set[str] = set()
    for f in changed_files:
        parts = f.split("/")
        # top-level package under src/superclaude/<pkg>/... or src/<pkg>/...
        if "superclaude" in parts:
            idx = parts.index("superclaude")
            if idx + 1 < len(parts):
                packages.add(parts[idx + 1])
        elif len(parts) >= 2:
            packages.add(
                parts[0]
                if parts[0] != "src"
                else parts[1]
                if len(parts) > 1
                else parts[0]
            )
    return len(packages) >= 2


# --------------------------------------------------------------------------- #
# Poll timing: backoff + timeout arithmetic (FR-2.3 / FR-2.5 / NFR-2)
# The FSM owns this arithmetic; the poll SCRIPT only returns a status (NFR-6).
# --------------------------------------------------------------------------- #

BACKOFF_BASE = MIN_POLL_INTERVAL  # 30s
BACKOFF_CAP = 300  # 5 min


def next_backoff(prev_interval: int) -> int:
    """Next exponential backoff interval: ``30 → 60 → 120 → … → cap 300`` (FR-2.5).

    ``prev_interval <= 0`` (or below base) restarts at the 30s base; otherwise it
    doubles, capped at 300s. A successful poll resets the caller's interval to 0 so
    the next backoff restarts at the base (T-231: backoff 30, 60, reset).
    """
    if prev_interval < BACKOFF_BASE:
        return BACKOFF_BASE
    return min(prev_interval * 2, BACKOFF_CAP)


def timed_out(elapsed_seconds: int, timeout: int) -> bool:
    """Whether the wall-clock timeout has fired (``elapsed >= timeout``, FR-2.3)."""
    return elapsed_seconds >= timeout


def poll_outcome(review_state: str, elapsed_seconds: int, timeout: int) -> MonitorState:
    """Map a poll result + elapsed time to the next FSM state.

    A ``clean``/``findings`` review proceeds (S2_CLASSIFY); a still-``polling`` review
    that has exceeded the wall-clock timeout fires TERMINAL_TIMEOUT (T-221/T-222);
    otherwise polling continues (loop back to S2_CLASSIFY).
    """
    if review_state in ("clean", "findings"):
        return MonitorState.S2_CLASSIFY
    if timed_out(elapsed_seconds, timeout):
        return MonitorState.TERMINAL_TIMEOUT
    return MonitorState.S2_CLASSIFY


# --------------------------------------------------------------------------- #
# transition() — the transition table (spec §5.4: a table, not nested ifs)
# --------------------------------------------------------------------------- #


def transition(
    state: MonitorState, event: str, context: dict | None = None
) -> MonitorState:
    """Return the next state for ``(state, event)`` under the ordinal ceiling.

    The ``needs_human_decision`` override is evaluated FIRST (pre-gate, §5.2): any
    event in a cycle carrying ``needs_human_decision`` routes to HALT_HUMAN
    regardless of ordinal. Otherwise the edge is looked up in the transition table,
    with the three ordinal gates applied at their edges.
    """
    ctx = context or {}
    ordinal = int(ctx.get("monitor_ordinal", 0))

    # Pre-gate override (the ONLY ceiling short-circuit).
    if ctx.get("needs_human_decision"):
        return MonitorState.HALT_HUMAN

    edge = (state, event)

    if edge == (MonitorState.S0_IDLE, "arm"):
        return MonitorState.S2_CLASSIFY if gate_arm(ordinal) else MonitorState.S0_IDLE
    if edge == (MonitorState.S2_CLASSIFY, "no_review"):
        return MonitorState.S2_CLASSIFY  # loop back (poll again)
    if edge == (MonitorState.S2_CLASSIFY, "clean"):
        return MonitorState.TERMINAL_CLEAN
    if edge == (MonitorState.S2_CLASSIFY, "findings"):
        # round-budget gate evaluated here
        if should_halt_rounds(
            int(ctx.get("round_counter", 0)),
            int(ctx.get("max_rounds", DEFAULT_MAX_ROUNDS)),
        ):
            return MonitorState.HALT_MAX_ROUNDS
        return MonitorState.S2B_VERIFY
    if edge == (MonitorState.S2B_VERIFY, "verified"):
        return MonitorState.S3_DIAGNOSE
    if edge == (MonitorState.S2B_VERIFY, "unverified"):
        return MonitorState.REPORT_ONLY  # no round consumed
    if edge == (MonitorState.S3_DIAGNOSE, "diagnosed"):
        # G-edit: ordinal >= 2 enters S3_FIXING; else PROPOSED (offer, no edits)
        return MonitorState.S3_FIXING if gate_edit(ordinal) else MonitorState.PROPOSED
    if edge == (MonitorState.S3_FIXING, "edits_applied"):
        return MonitorState.S7_VALIDATING
    if edge == (MonitorState.S7_VALIDATING, "validated"):
        # G-push handled by evaluate_push_decision at the caller; default edge
        return MonitorState.S4_PUSHING
    if edge == (MonitorState.S7_VALIDATING, "validation_failed"):
        return MonitorState.VALIDATION_FAIL
    if edge == (MonitorState.S4_PUSHING, "pushed"):
        return MonitorState.S6_REPLYING
    if edge == (MonitorState.S6_REPLYING, "replied"):
        return MonitorState.RESOLVING
    if edge == (MonitorState.RESOLVING, "resolved"):
        # V1.1 (FR-8.1): after resolve, route to S5a to post the re-trigger comment
        # BEFORE awaiting the re-review (a push does NOT auto-trigger an Augment
        # re-review). The increment is NOT here; INV-001's edge is below.
        return MonitorState.S5A_RETRIGGER_REVIEW
    if edge == (MonitorState.S5A_RETRIGGER_REVIEW, "retriggered"):
        # The re-trigger comment was posted → await the re-review (INV-R1). The
        # re-trigger itself does NOT tick round_counter.
        return MonitorState.S5_AWAITING_REREVIEW
    if edge == (MonitorState.S5_AWAITING_REREVIEW, "rereview_attributed"):
        return MonitorState.S2_CLASSIFY  # loop-guard increments at this edge (INV-001)
    if edge == (MonitorState.S5_AWAITING_REREVIEW, "timeout"):
        return MonitorState.TERMINAL_TIMEOUT
    if edge == (MonitorState.S5_AWAITING_REREVIEW, "declined"):
        # V1.1 (FR-9): a decline observed at the S5 re-trigger poll → oversized-PR
        # auggie-review fallback (S5b). Sibling of rereview_attributed/timeout; the
        # INV-001 edge above is unchanged.
        return MonitorState.S5B_AUGGIE_FALLBACK
    if edge == (MonitorState.S2_CLASSIFY, "declined"):
        # V1.1 (FR-9.1): a decline observed at the INITIAL S2 poll → fallback (S5b).
        return MonitorState.S5B_AUGGIE_FALLBACK
    if edge == (MonitorState.S5B_AUGGIE_FALLBACK, "fallback_findings"):
        # The fallback /sc:auggie-review produced findings → re-enter classification
        # ONCE under the clamp (no loop-back).
        return MonitorState.S2_CLASSIFY
    if edge == (MonitorState.S5B_AUGGIE_FALLBACK, "fallback_skip"):
        # Single-shot fallback terminal selector (FR-10, OQ-2 reuse): clean residual →
        # TERMINAL_CLEAN; residual findings remain → HALT_MAX_ROUNDS.
        return (
            MonitorState.HALT_MAX_ROUNDS
            if ctx.get("fallback_residual_findings")
            else MonitorState.TERMINAL_CLEAN
        )

    # Unknown edge: stay put (defensive; real runs never hit this).
    return state


# --------------------------------------------------------------------------- #
# run_skill() — the integration driver the spec test bodies call
# --------------------------------------------------------------------------- #


def _noop(*_args, **_kwargs) -> None:
    return None


def _default_verify(finding: Finding) -> bool:
    """Default verify-before-remediate: a finding is verified unless flagged unverified.

    Fixtures carry ``verification_status``; a finding explicitly ``"unverified"`` is
    a false positive (FR-3.5) and is NOT verified. Otherwise it is treated as
    grounded (the real grounding spawns the evidence-validator agent — injected via
    the ``verify`` seam in production).
    """
    return finding.verification_status != "unverified"


def _default_apply_edits(findings: list[Finding]) -> int:
    """Default edit application: count groundable, verified, in-diff findings.

    An ungroundable finding (``in_diff is False`` or unverified) yields no applied
    edit — the INV-016 predicate-5 ``applied_edits == 0`` path (T-ZERO-EDIT-NO-PUSH).
    """
    return sum(
        1 for f in findings if f.in_diff and f.verification_status != "unverified"
    )


@dataclass
class RunConfig:
    """Injected seams + inputs for :func:`run_skill` (keeps the core pure/testable)."""

    monitor_ordinal: int = 0
    max_rounds: int = DEFAULT_MAX_ROUNDS
    poll_interval: int = MIN_POLL_INTERVAL
    timeout: int = DEFAULT_TIMEOUT
    pr_number: int | None = None
    resume: str | None = None
    # The findings for the (first) cycle, already classified/normalized.
    findings: list[Finding] = field(default_factory=list)
    # Optional multi-round sequence: each entry is the residual finding set observed
    # at the next re-review (drives the loop-guard off-by-one tests, Phase 8).
    rereview_findings: list[list[Finding]] = field(default_factory=list)
    review_state: str = "findings"  # "polling" | "clean" | "findings" | "declined"
    # V1.1 (addendum §6.4): per-cycle attributed-re-review outcome sequence, indexed
    # by cycle_index — each is "attributed" | "declined" | "timeout". When EMPTY
    # (legacy callers), each pushed cycle defaults to "attributed" so the optimistic
    # INV-001 tick (max_rounds=N ⇒ N pushes) is preserved verbatim. When NON-EMPTY,
    # explicit per-index outcomes are honored and any missing trailing index defaults
    # to "timeout" (a push WITHOUT an attributed re-review does NOT tick round_counter).
    rereview_outcome: list[str] = field(default_factory=list)
    # V1.1 oversized-PR fallback (R2/R3): the findings the in-session /sc:auggie-review
    # fallback produces (re-graded through verify-before-remediate, FR-9.4 — NOT trusted
    # verbatim), and an optional post-fallback residual set that routes the single-shot
    # fallback's terminal selector (residual present ⇒ HALT_MAX_ROUNDS, else TERMINAL_CLEAN).
    fallback_findings: list[Finding] = field(default_factory=list)
    fallback_residual_findings: list[Finding] = field(default_factory=list)
    # Side-effect seams (defaults keep the core pure / recording-only).
    arm_monitor: Callable[..., None] = _noop
    verify: Callable[[Finding], bool] = _default_verify
    apply_edits: Callable[[list[Finding]], int] = _default_apply_edits
    run_validation: Callable[..., str] = staticmethod(lambda **_: "validated")
    do_push: Callable[..., None] = _noop
    do_reply: Callable[..., None] = _noop
    do_resolve: Callable[..., None] = _noop
    # V1.1 seams (addendum §6.4) — both default to the module-level `_noop` (NOT inline
    # lambdas, to avoid the dataclass self-binding trap). do_retrigger = the S5a
    # re-trigger comment-post; invoke_auggie_review = the S5b fallback
    # `> Skill sc:auggie-review-protocol` invocation. The real version-control / Skill
    # I/O lives in SKILL.md — these stay recording-only seams (NFR-6 core purity).
    do_retrigger: Callable[..., None] = _noop
    invoke_auggie_review: Callable[..., None] = _noop


def _run_fallback(result: SkillResult, config: RunConfig) -> None:
    """Single-shot oversized-PR auggie-review fallback (S5b — FR-9/FR-10, R2/R3).

    Engaged when a ``declined`` is observed (at the initial S2 poll or the S5 re-trigger
    poll). Records the INV-R3 monotone clamp ONCE (``effective_max_rounds → min(., 1)``),
    invokes ``/sc:auggie-review`` AT MOST ONCE (INV-R2 strict-once, guarded by the
    ``auggie_review_invoked`` flag), and re-enters the remediation pipeline EXACTLY ONCE
    under the clamp with NO loop-back and NO second invoke/re-trigger. ``round_counter``
    is FROZEN at entry — the fallback uses only ``fallback_round_counter``; the two
    counters are INDEPENDENT and neither re-opens the other's loop. The fallback's single
    push makes ``push_count <= max_rounds + 1`` hold for the whole run (INV-R2).
    """
    result.decline_detected = True
    result.fallback_engaged = True
    # Visibly enter S5b (transition()'s S2/S5 → S5B_AUGGIE_FALLBACK target); the terminal
    # selector below overwrites result.state, but this materializes the topology entry.
    result.state = MonitorState.S5B_AUGGIE_FALLBACK
    # INV-R3: one-way monotone clamp to 1, recorded once (a later re-entry never raises it).
    base = (
        result.effective_max_rounds
        if result.effective_max_rounds is not None
        else config.max_rounds
    )
    result.effective_max_rounds = clamp_max_rounds(base)

    # INV-R2: invoke /sc:auggie-review AT MOST ONCE per PR (strict-once).
    if not result.auggie_review_invoked:
        config.invoke_auggie_review(pr_number=config.pr_number)
        result.auggie_review_invoked = True

    # Single fallback cycle, capped at 1 (structural termination, not merely budget).
    if loop_guard_should_halt(
        result.fallback_round_counter, result.effective_max_rounds
    ):
        result.state = MonitorState.HALT_MAX_ROUNDS
        return

    ordinal = config.monitor_ordinal
    fallback_findings = list(config.fallback_findings)
    result.findings = fallback_findings

    # needs_human_decision pre-gate (FR-4.4 / EC-7) — mirror the main loop, which gates
    # on the full cycle_findings BEFORE verify. A human-decision finding HALTs regardless
    # of verification status AND before the no-verified→TERMINAL_CLEAN path below;
    # otherwise an unverified human-decision fallback finding would be silently auto-
    # defaulted to clean (a needs_human_decision item must HALT, never auto-default).
    if ordinal >= 3 and any(f.needs_human_decision for f in fallback_findings):
        result.state = MonitorState.HALT_HUMAN
        return

    # verify-before-remediate (FR-9.4): fallback findings are NOT trusted verbatim.
    verified = [f for f in fallback_findings if config.verify(f)]
    if not verified:
        # Nothing grounded to remediate → the fallback converges clean.
        result.fallback_round_counter += 1
        result.state = MonitorState.TERMINAL_CLEAN
        result.summary_posted = True
        return

    if not gate_edit(ordinal):
        result.state = MonitorState.PROPOSED
        result.applied_edits = 0
        result.proposal = PROPOSE_PROMPT
        return

    result.applied_edits = config.apply_edits(verified)
    result.validation_status = config.run_validation(findings=verified)
    if result.validation_status != "validated":
        result.state = MonitorState.VALIDATION_FAIL
        return

    # G-push: the fallback's budget gate uses fallback_round_counter (NOT the frozen
    # round_counter) against the clamped effective_max_rounds.
    decision = evaluate_push_decision(
        monitor_ordinal=ordinal,
        validation_status=result.validation_status,
        needs_human_decision=any(f.needs_human_decision for f in verified),
        round_counter=result.fallback_round_counter,
        max_rounds=result.effective_max_rounds,
        applied_edits=result.applied_edits,
    )
    result.push_decision = decision
    if not decision.authorized:
        result.state = (
            MonitorState.S4_HALT_BEFORE_PUSH
            if ordinal < 3
            else push_fail_state(decision)
        )
        return

    # The fallback's single push (contributes at most ONE push — INV-R2).
    config.do_push(pre_push_sha=None)
    result.push_count += 1
    config.do_reply(applied_edits=result.applied_edits, findings=verified)
    result.reply_count += 1
    config.do_resolve(findings=verified)
    result.fallback_round_counter += (
        1  # the SEPARATE fallback counter (NOT round_counter)
    )

    # Single-shot terminal selector (no loop-back): residual remains → HALT_MAX_ROUNDS,
    # else converged → TERMINAL_CLEAN (OQ-2 reuse of the existing terminals).
    if config.fallback_residual_findings:
        result.findings = list(config.fallback_residual_findings)
        result.state = MonitorState.HALT_MAX_ROUNDS
    else:
        result.state = MonitorState.TERMINAL_CLEAN
    result.summary_posted = True


def run_skill(config: RunConfig | None = None, **overrides) -> SkillResult:
    """Drive the FSM over the configured inputs and return a :class:`SkillResult`.

    Honors the capability ceiling: at L0 the FSM never leaves S0_IDLE (AC-1); at L1
    it verifies + proposes but applies NO edits; at L2 it applies edits + validates
    then HALTs before any push/reply (``S4'_HALT_BEFORE_PUSH``); at L3 it pushes
    (only when the INV-016 conjunction holds), replies, resolves, and loops under
    the monotonic round counter. The ``needs_human_decision`` override HALTs at any
    armed ordinal.
    """
    if config is None:
        config = RunConfig(**overrides)
    elif overrides:
        for k, v in overrides.items():
            setattr(config, k, v)

    result = SkillResult(state=MonitorState.S0_IDLE)
    ordinal = config.monitor_ordinal

    # G-arm: L0 returns immediately, byte-identical to today (AC-1).
    if not gate_arm(ordinal):
        result.state = MonitorState.S0_IDLE
        return result
    config.arm_monitor(config.pr_number)
    result.state = MonitorState.S2_CLASSIFY

    if config.review_state == "polling":
        result.state = MonitorState.S2_CLASSIFY
        return result
    if config.review_state == "clean":
        # A clean re-review posts exactly ONE summary thread (FR-6.5, T-642).
        result.state = MonitorState.TERMINAL_CLEAN
        result.summary_posted = True
        return result
    if config.review_state == "declined":
        # V1.1 (FR-9.1): an "abnormally large" decline observed at the INITIAL S2 poll
        # → Augment will not auto-review → engage the single-shot auggie-review fallback
        # (S5b). round_counter stays frozen at 0; the fallback uses fallback_round_counter.
        _run_fallback(result, config)
        return result

    # Multi-round loop: cycle 0 is `findings`; subsequent residuals come from
    # `rereview_findings`. The round counter ticks on each attributed re-review
    # (INV-001) — modeled here as advancing to the next residual set.
    cycles = [config.findings] + list(config.rereview_findings)
    for cycle_index, cycle_findings in enumerate(cycles):
        # Round-budget gate (evaluated at S2_CLASSIFY, before opening a fix cycle).
        if should_halt_rounds(result.round_counter, config.max_rounds):
            result.state = MonitorState.HALT_MAX_ROUNDS
            # Residual findings → post a single summary listing them (FR-6.4, T-630).
            result.findings = cycle_findings
            result.summary_posted = True
            break

        result.findings = cycle_findings
        if not cycle_findings:
            result.state = MonitorState.TERMINAL_CLEAN
            break

        # Pre-gate override (FR-4.4 / EC-7): a needs_human_decision finding HALTs
        # IMMEDIATELY at L3 (where the ceiling would otherwise push) — no fix, no
        # push, no reply (T-430, EC-7 L3: edits==0). At L1/L2 the ceiling already
        # prevents the push, so the finding flows through the normal path: L1
        # proposes (edits==0); L2 fixes locally then HALTs before push (edits>0,
        # pushes==0, EC-7 L2). The push-gate predicate 3 additionally blocks any L3
        # push if a needs_human finding somehow reaches it.
        if ordinal >= 3 and any(f.needs_human_decision for f in cycle_findings):
            result.state = MonitorState.HALT_HUMAN
            break

        # S2b_VERIFY (FR-3.5): unverified findings route to REPORT_ONLY, no round.
        verified = [f for f in cycle_findings if config.verify(f)]
        if not verified:
            result.state = MonitorState.REPORT_ONLY
            break

        # S3_DIAGNOSE → G-edit.
        if not gate_edit(ordinal):
            # L1 ceiling: propose, apply NO edits. Emit the exact "fix these? y/n".
            result.state = MonitorState.PROPOSED
            result.applied_edits = 0
            result.proposal = PROPOSE_PROMPT
            break

        # S3_FIXING: apply the diagnosed edits in the working tree.
        result.applied_edits = config.apply_edits(verified)

        # S7_VALIDATING.
        result.validation_status = config.run_validation(findings=verified)
        if result.validation_status != "validated":
            result.state = MonitorState.VALIDATION_FAIL
            break

        # G-push (INV-016 conjunction).
        decision = evaluate_push_decision(
            monitor_ordinal=ordinal,
            validation_status=result.validation_status,
            needs_human_decision=any(f.needs_human_decision for f in verified),
            round_counter=result.round_counter,
            max_rounds=config.max_rounds,
            applied_edits=result.applied_edits,
        )
        result.push_decision = decision
        if not decision.authorized:
            # L2 ceiling (ordinal < 3) halts before push; other blocks route per §5.3.
            if ordinal < 3:
                result.state = MonitorState.S4_HALT_BEFORE_PUSH
            else:
                result.state = push_fail_state(decision)
            break

        # S4_PUSHING → S6_REPLYING → RESOLVING (L3). Side effects via seams.
        config.do_push(pre_push_sha=None)
        result.push_count += 1
        config.do_reply(applied_edits=result.applied_edits, findings=verified)
        result.reply_count += 1
        config.do_resolve(findings=verified)

        # S5a (FR-8.1/8.6): a push does NOT auto-trigger an Augment re-review — post the
        # re-trigger comment (the trigger token lives in the bash script, never the core),
        # but ONLY when this cycle actually pushed (applied_edits > 0). The re-trigger
        # itself does NOT tick round_counter (INV-R1).
        if result.applied_edits > 0:
            # S5a: visibly enter the re-trigger state, then post the comment (the state
            # is overwritten by S5_AWAITING_REREVIEW below — materialized for topology
            # fidelity with transition()'s RESOLVING→S5A→S5 edges).
            result.state = MonitorState.S5A_RETRIGGER_REVIEW
            config.do_retrigger(pr_number=config.pr_number)
            result.rereview_request_count += 1
        result.state = MonitorState.S5_AWAITING_REREVIEW

        # Determine the attributed re-review outcome for THIS cycle. Explicit
        # rereview_outcome wins; an EMPTY sequence (legacy callers) defaults every cycle
        # to "attributed" so INV-001's optimistic tick (max_rounds=N ⇒ N pushes) is
        # preserved verbatim; a NON-EMPTY but shorter sequence defaults missing trailing
        # indices to "timeout" (a push WITHOUT an attributed re-review does NOT tick).
        # NB: the `"attributed"` OUTCOME token (this run_skill vocabulary) is the thing
        # the SKILL surfaces as transition()'s `"rereview_attributed"` EDGE event / a
        # ROUND_INCREMENTED run-log event — two deliberately distinct vocabularies (an
        # outcome token vs an FSM edge name); they are NOT the same string by design.
        if cycle_index < len(config.rereview_outcome):
            outcome = config.rereview_outcome[cycle_index]
        else:
            outcome = "attributed" if not config.rereview_outcome else "timeout"

        if outcome == "declined":
            # Decline observed at the S5 re-trigger poll (FR-9) → single-shot fallback
            # (S5b). round_counter is NOT ticked for this cycle (no attributed re-review).
            _run_fallback(result, config)
            break
        if outcome == "timeout":
            # Push WITHOUT an attributed re-review → round_counter does NOT advance
            # (T-PUSH-WITHOUT-REREVIEW-NO-TICK / EC-18).
            result.state = MonitorState.TERMINAL_TIMEOUT
            break

        # outcome == "attributed": the SINGLE relocated INV-001 increment site. Fires
        # AFTER the push (monotonicity) and BEFORE the next iteration's top-of-loop
        # should_halt_rounds gate (so max_rounds=N ⇒ N pushes is preserved verbatim).
        result.round_counter += 1

        # If there is a next residual cycle, loop; else clean re-review terminates
        # with a SINGLE summary thread (FR-6.5, T-642 — not one comment per finding).
        if cycle_index + 1 >= len(cycles):
            result.state = MonitorState.TERMINAL_CLEAN
            result.summary_posted = True
            break

    return result
