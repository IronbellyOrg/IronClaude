"""Canonical data models for the ``sc:pr-submit`` deterministic core.

Defines the closed run-log event enum (exactly 37 members — the 32 from spec
§11.3 plus ``push_aborted_or_not_landed`` from §12.1, plus the 4 V1.1
re-review/fallback events from addendum §6.1), the severity tiers, the
single-FSM state lexicon (spec §5.1; Python identifiers drop the spec's prime, so
``S4'_HALT_BEFORE_PUSH`` becomes ``S4_HALT_BEFORE_PUSH``), and the ``Finding`` /
``SkillResult`` dataclasses the test bodies assert against.

Core-purity (NFR-6 / AC-9 / FR-G1): this module imports NO ``anthropic`` SDK and
contains ZERO ``gh``/``git`` tokens.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class EventType(str, Enum):
    """Closed enum of run-log event types — EXACTLY 37 members.

    The 32 event types listed in spec §11.3 (merged-spec.md:724-731) PLUS
    ``push_aborted_or_not_landed`` (spec §12.1 line 771 — the crash-window
    not-landed branch) — the 33 prior members — PLUS the 4 V1.1
    re-review/fallback events (``rereview_requested``, ``decline_detected``,
    ``auggie_fallback_invoked``, ``max_rounds_clamped``; addendum §6.1). The
    run-log writer validates every appended event against this closed set; an
    event outside it is a programming error.
    """

    # --- lifecycle / setup (§11.3) ---
    RUN_STARTED = "run_started"
    ENVIRONMENT_CHECK = "environment_check"
    PR_CREATE_ATTEMPTED = "pr_create_attempted"
    PR_CREATED = "pr_created"
    MONITOR_ARMED = "monitor_armed"
    BASELINE_CAPTURED = "baseline_captured"
    # --- polling / detection ---
    POLL_ATTEMPT = "poll_attempt"
    POLL_RESULT = "poll_result"
    API_BACKOFF = "api_backoff"
    CLASSIFIER_UNKNOWN_SHAPE = "classifier_unknown_shape"
    REVIEW_DETECTED = "review_detected"
    FINDINGS_NORMALIZED = "findings_normalized"
    # --- verify-before-remediate ---
    FINDING_VERIFIED = "finding_verified"
    FINDING_UNVERIFIED = "finding_unverified"
    # --- loop / routing ---
    ROUND_INCREMENTED = "round_incremented"
    ROUTE_DECISION = "route_decision"
    # --- diagnose / fix ---
    TROUBLESHOOT_STARTED = "troubleshoot_started"
    TROUBLESHOOT_COMPLETED = "troubleshoot_completed"
    FIX_APPLIED = "fix_applied"
    # --- validation ---
    VALIDATION_STARTED = "validation_started"
    VALIDATION_COMPLETED = "validation_completed"
    # --- write-ahead push triad (§12.1) ---
    PUSH_DECISION = "push_decision"
    PUSH_INITIATED = "push_initiated"
    PUSH_COMPLETED = "push_completed"
    # --- reply / resolve ---
    REPLY_POSTED = "reply_posted"
    THREAD_RESOLVED = "thread_resolved"
    IDEMPOTENCY_SKIP = "idempotency_skip"
    # --- terminals (§11.3) ---
    TERMINAL_CLEAN = "terminal_clean"
    TERMINAL_TIMEOUT = "terminal_timeout"
    TERMINAL_MAX_ROUNDS = "terminal_max_rounds"
    TERMINAL_HALTED = "terminal_halted"
    TERMINAL_FAILED = "terminal_failed"
    # --- crash-window not-landed branch (§12.1 line 771) — the 33rd ---
    PUSH_ABORTED_OR_NOT_LANDED = "push_aborted_or_not_landed"
    # --- V1.1 re-review / fallback events (addendum §6.1) — the 34th-37th ---
    REREVIEW_REQUESTED = "rereview_requested"
    DECLINE_DETECTED = "decline_detected"
    AUGGIE_FALLBACK_INVOKED = "auggie_fallback_invoked"
    MAX_ROUNDS_CLAMPED = "max_rounds_clamped"


class Severity(str, Enum):
    """Severity tiers — the rubric's 5-tier scheme (reused from auggie-review)."""

    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    NIT = "Nit"


class MonitorState(str, Enum):
    """The single-FSM state lexicon (spec §5.1).

    The ``--monitor {0,1,2,3}`` ordinal is a capability ceiling on THIS one FSM,
    not four divergent code paths. Python identifiers cannot contain an
    apostrophe, so the spec's ``S4'_HALT_BEFORE_PUSH`` is represented here as
    ``S4_HALT_BEFORE_PUSH`` (the ref/prose retain the primed spec name). This is
    a spec-faithful adaptation, not a deviation.
    """

    # --- working states ---
    S0_IDLE = "S0_IDLE"
    S2_CLASSIFY = "S2_CLASSIFY"
    S2B_VERIFY = "S2b_VERIFY"
    S3_DIAGNOSE = "S3_DIAGNOSE"
    S3_FIXING = "S3_FIXING"
    S7_VALIDATING = "S7_VALIDATING"
    S4_PUSHING = "S4_PUSHING"
    S4_HALT_BEFORE_PUSH = "S4_HALT_BEFORE_PUSH"  # spec S4'_HALT_BEFORE_PUSH
    S6_REPLYING = "S6_REPLYING"
    RESOLVING = "RESOLVING"
    S5_AWAITING_REREVIEW = "S5_AWAITING_REREVIEW"
    # --- V1.1 re-trigger / fallback working states (non-terminal, addendum §6.1) ---
    S5A_RETRIGGER_REVIEW = "S5a_RETRIGGER_REVIEW"
    S5B_AUGGIE_FALLBACK = "S5b_AUGGIE_FALLBACK"
    PROPOSED = "PROPOSED"
    REPORT_ONLY = "REPORT_ONLY"
    # --- terminals ---
    TERMINAL_CLEAN = "TERMINAL_CLEAN"
    HALT_MAX_ROUNDS = "HALT_MAX_ROUNDS"
    HALT_HUMAN = "HALT_HUMAN"
    VALIDATION_FAIL = "VALIDATION_FAIL"
    TERMINAL_TIMEOUT = "TERMINAL_TIMEOUT"
    TERMINAL_FAILED = "TERMINAL_FAILED"


# Terminal states the FSM never transitions out of.
TERMINAL_STATES = frozenset(
    {
        MonitorState.TERMINAL_CLEAN,
        MonitorState.HALT_MAX_ROUNDS,
        MonitorState.HALT_HUMAN,
        MonitorState.VALIDATION_FAIL,
        MonitorState.TERMINAL_TIMEOUT,
        MonitorState.TERMINAL_FAILED,
    }
)


@dataclass
class Finding:
    """A normalized Augment review finding.

    ``severity_hint``/``category``/``confidence``/``in_diff`` are the raw Augment
    inputs; ``remapped_severity`` is filled by the severity router (FR-3.1) and
    ``verification_status`` by the verify-before-remediate wave (FR-3.5,
    one of ``"unverified"`` / ``"verified"`` / ``"report_only"``).
    """

    path: str
    line: int
    body: str
    severity_hint: str | None = None
    category: str | None = None
    confidence: str | None = None
    in_diff: bool = True
    comment_id: int | None = None
    remapped_severity: Severity | None = None
    verification_status: str = "unverified"
    needs_human_decision: bool = False

    @property
    def fix_key(self) -> str:
        """``sha256(path + line + finding_body)`` — comment_id-INDEPENDENT (INV-009).

        Imported lazily to keep this dataclass dependency-free at module load.
        """
        import hashlib

        digest = hashlib.sha256(
            f"{self.path}\n{self.line}\n{self.body}".encode("utf-8")
        )
        return digest.hexdigest()


@dataclass
class SkillResult:
    """The object ``run_skill(...)`` returns; test bodies assert on its attributes.

    ``round_counter`` is the monotonic count of completed remediation cycles
    (INV-001); ``push_count``/``reply_count`` count landed side effects;
    ``summary_posted`` flags the single clean-re-review summary thread;
    ``state`` is the terminal :class:`MonitorState`; ``applied_edits`` is the
    INV-016 predicate-5 input (a push requires ``applied_edits > 0``).
    """

    state: MonitorState = MonitorState.S0_IDLE
    round_counter: int = 0
    push_count: int = 0
    reply_count: int = 0
    summary_posted: bool = False
    applied_edits: int = 0
    findings: list[Finding] = field(default_factory=list)
    validation_status: str = "pending"
    push_decision: "PushDecision | None" = None
    # The L1 user-facing proposal text ("fix these? y/n"), set only when the FSM
    # ends in PROPOSED (the L1 ceiling proposes but applies no edits, T-402).
    proposal: str | None = None
    # --- V1.1 re-trigger / fallback fields (addendum §6.1) ---
    # ``rereview_request_count`` counts S5a re-trigger comments (INV-R1, monotone,
    # <= max_rounds); ``fallback_engaged``/``auggie_review_invoked`` flag the R2
    # single-shot /sc:auggie-review fallback (INV-R2 strict-once);
    # ``decline_detected`` flags an Augment "abnormally large" decline (FR-9.1);
    # ``effective_max_rounds`` is the INV-R3 monotone clamp (None = never clamped);
    # ``fallback_round_counter`` is the SEPARATE cap-1 fallback counter (independent
    # of ``round_counter``).
    rereview_request_count: int = 0
    fallback_engaged: bool = False
    auggie_review_invoked: bool = False
    decline_detected: bool = False
    effective_max_rounds: int | None = None
    fallback_round_counter: int = 0


@dataclass
class PushDecision:
    """Records the INV-016 5-predicate G-push conjunction outcome (spec §5.3).

    ``authorized`` is the AND of all five predicates; the individual
    ``predicate_*`` fields make each gate independently assertable
    (``T-ZERO-EDIT-NO-PUSH`` asserts ``predicate_5_applied_edits == 0`` and
    ``authorized is False`` when no edit was applied).
    """

    predicate_1_ordinal: bool = False  # monitor_ordinal >= 3
    predicate_2_validated: bool = False  # validation_status == "validated"
    predicate_3_no_human: bool = False  # needs_human_decision == false (all)
    predicate_4_under_cap: bool = False  # round_counter < max_rounds
    predicate_5_applied_edits: int = 0  # applied_edits (> 0 required)
    authorized: bool = False
