"""The pure merge-conflict core for sc:pr-submit (issue #305, design section 5).

This module parses the read-only probe output, classifies every conflicted path
into a tier and builds the conflict plan the SKILL reports before any edit. It also
holds the only conflict routing decision (``conflict_action``), the merge and sync
gates, the validation status, cycle ids, the resolution record and commit message
helpers, and the two pure resume planners.

Module rules (design section 5.1):

- Standard library only (``base64``, ``re``, ``dataclasses``, ``typing`` and, on
  Python 3.11 and later, ``tomllib``; on 3.10 ``tomllib`` is ``None`` and the lock
  trust gate fails closed); the only internal imports are ``MonitorState`` from ``.models`` and, for the validation
  status helper, ``run_validation_gates`` from ``.fsm``. This module never imports
  ``recovery`` (``recovery`` imports this module), so it defines its own branch
  literals.
- No I/O, no clock, no environment reads, and no version-control command names
  anywhere in this file. The probe, the merge and the merge-tree command are named
  in words.
- Every public function fails closed: malformed input raises ``ValueError`` where
  the contract says so, and otherwise the most restrictive answer is returned
  (``False``, Tier 3, a ``halt`` class).
"""

import base64
import re
from dataclasses import dataclass

try:
    import tomllib
except ImportError:  # Python 3.10: no TOML parser; lock_trust_findings fails closed
    tomllib = None

from .fsm import run_validation_gates
from .models import MonitorState

# ---------------------------------------------------------------------------
# Constants (design section 5.2)
# ---------------------------------------------------------------------------

SYNC_CAP: int = 1  # conflict cycles per run, both tiers together (INV-019)
TIER2_MAX_FILES: int = 8  # text:* paths; regen:* paths do not count (OQ-9)
MAX_PROBE_BYTES: int = (
    102_400  # the probe truncates above this; a truncated probe is Tier 3
)
CONFLICT_CYCLE_PREFIXES: tuple[str, ...] = ("sync-", "conflict-")
HOOKS: tuple[str, ...] = ("wave0", "c_initial", "wave8a")
ENTERING_OUTCOMES: tuple[str, ...] = (
    "clean",
    "report_only",
    "halt_max_rounds",
    "no_response",
)
PRESERVED_OUTCOMES: tuple[str, ...] = ("halt_max_rounds", "no_response")
ACTIONS: tuple[str, ...] = (
    "none",
    "report",
    "propose",
    "resolve_local",
    "resolve_push",
    "halt",
)
PUSH_KINDS: tuple[str, ...] = ("fix", "merge", "sync", "ci")
FOREIGN_OPS: tuple[str, ...] = (
    "MERGE_HEAD",
    "rebase-merge",
    "rebase-apply",
    "CHERRY_PICK_HEAD",
    "REVERT_HEAD",
    "sequencer",
)
CONFLICT_PROPOSE_PROMPT: str = "resolve these conflicts? y/n"
PROTECTED_PREFIXES: tuple[str, ...] = (".github/workflows/", ".github/actions/")
PROTECTED_PATHS: tuple[str, ...] = (
    ".claude/settings.json",
    ".claude/settings.local.json",
)
MIGRATION_SEGMENTS: tuple[tuple[str, ...], ...] = (
    ("migrations",),
    ("alembic", "versions"),
    ("db", "migrate"),
)
LOCKFILE_NAMES: tuple[str, ...] = (
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "Cargo.lock",
    "poetry.lock",
    "Pipfile.lock",
    "flake.lock",
    "uv.lock",
)
GENERATED_SEGMENTS: tuple[str, ...] = ("generated", "dist", "build", "__snapshots__")
RECORD_KINDS: tuple[str, ...] = (
    "trivial",
    "additive",
    "competing",
    "structural",
    "modify-delete",
    "add-add",
    "semantic",
)
RECORD_RESOLUTIONS: tuple[str, ...] = (
    "keep_both",
    "take_ours",
    "take_theirs",
    "synthesized",
)
RECORD_FIELDS: tuple[str, ...] = (
    "kind",
    "root_cause",
    "ours_intent",
    "theirs_intent",
    "resolution",
    "behavior_after",
    "dropped",
    "evidence",
)

# Every reason conflict_action can return, in any row (design section 4.4, section 9).
REPORT_REASONS: frozenset[str] = frozenset(
    {
        # report-only reasons (no halt by themselves)
        "no_conflict",
        "behind_only",
        "blocked",
        "tier1_planned",
        "tier2_planned",
        "tier2_report_only",
        "tier1_deferred",
        "tier1_proposed",
        "tier1_l2_preserved",
        "tier1_local",
        "tier1_sync",
        "tier2_merge",
        "no_round_budget",
        "l0",
        "tier1_l1_preserved",
        # router return values that halt on some rows
        "tier_above_cap",
        "conflict_tier3",
        "probe_failed",
        "merge_tree_unsupported",
        "github_disagrees",
        "sync_cap",
        "late_conflict",
        "router_unreachable",
    }
)
# Every reason ever written to terminal_halted by a conflict path (design section 9).
HALT_REASONS: frozenset[str] = frozenset(
    {
        "foreign_op_in_progress",
        "conflict_tier3",
        "late_conflict",
        "tier_above_cap",
        "github_disagrees",
        "probe_failed",
        "merge_tree_unsupported",
        "sync_cap",
        "merge_preflight_dirty",
        "sync_foreign_operation",
        "sync_merge_failed",
        "sync_marker_left",
        "sync_unmerged_left",
        "sync_staged_unexpected",
        "sync_commit_failed",
        "sync_head_mismatch",
        "sync_range_mismatch",
        "sync_base_moved",
        "sync_tier3",
        "sync_validation_failed",
        "push_rejected",
        "push_failed",
        "resume_unrepresentable",
        "router_unreachable",
    }
)
# The two sets overlap by design: a reason is reported at one hook or ordinal and halts at
# another. The intersection is exactly {"tier_above_cap", "conflict_tier3", "probe_failed",
# "merge_tree_unsupported", "github_disagrees", "sync_cap", "late_conflict", "router_unreachable"},
# pinned by a test so a new reason must be placed deliberately.

BRANCH_LANDED: str = "landed"  # equal to recovery.BRANCH_A_LANDED (pinned by a test)
BRANCH_NOT_LANDED: str = "not_landed"  # equal to recovery.BRANCH_B_NOT_LANDED
BRANCH_AMBIGUOUS: str = "ambiguous"  # equal to recovery.BRANCH_C_AMBIGUOUS


# ---------------------------------------------------------------------------
# Data types (design section 5.2)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MechanicalRule:
    """One mechanical regeneration rule. Adding a rule = one row in MECHANICAL_RULES
    plus one parametrized test row."""

    pattern: str  # exact repository-root-relative path, never a bare basename
    kind: str  # "lockfile" | "generated"
    sources: tuple[
        str, ...
    ]  # paths the output is derived from (documentation and report)
    regenerate: tuple[str, ...]  # argv; argv[0] must be in SKILL.md allowed-tools
    check: tuple[str, ...] = ()  # argv; argv[0] must be in SKILL.md allowed-tools


MECHANICAL_RULES: tuple[MechanicalRule, ...] = (
    MechanicalRule(
        "uv.lock",
        "lockfile",
        ("pyproject.toml",),
        ("uv", "lock"),
        ("uv", "lock", "--check"),
    ),
)

# ---------------------------------------------------------------------------
# Lock trust gate (PR #378 review, owner decision): `uv lock` runs build code that
# the merged pyproject.toml can name. Tier 1 halts before `uv lock` when it does.
# ---------------------------------------------------------------------------

LOCK_TRUST_UNREADABLE: str = "pyproject.toml unreadable"


def lock_trust_findings(pyproject_text: object) -> list[str]:
    """The fields of the merged ``pyproject.toml`` text that would make ``uv lock``
    run code from the tree; ``[]`` means the gate passes.

    Findings, in this order: ``"build-system.backend-path"`` (the key is present),
    ``"project.dynamic"`` (a non-empty list), then for each ``[tool.uv.sources]`` name
    in sorted order ``"tool.uv.sources.<name> (path)"`` and
    ``"tool.uv.sources.<name> (editable)"`` (a source value is a table or a list of
    tables). Fails closed: no TOML parser (Python 3.10), a non-string input, a parse
    error or an unexpected shape returns ``[LOCK_TRUST_UNREADABLE]``.
    """
    unreadable = [LOCK_TRUST_UNREADABLE]
    if tomllib is None or not isinstance(pyproject_text, str):
        return unreadable
    try:
        data = tomllib.loads(pyproject_text)
    except (ValueError, RecursionError):  # deeply nested input can exhaust the stack
        return unreadable
    build_system = data.get("build-system", {})
    project = data.get("project", {})
    tool = data.get("tool", {})
    if not all(isinstance(t, dict) for t in (build_system, project, tool)):
        return unreadable
    uv = tool.get("uv", {})
    sources = uv.get("sources", {}) if isinstance(uv, dict) else None
    dynamic = project.get("dynamic", [])
    if not isinstance(sources, dict) or not isinstance(dynamic, list):
        return unreadable
    findings: list[str] = []
    if "backend-path" in build_system:
        findings.append("build-system.backend-path")
    if dynamic:
        findings.append("project.dynamic")
    for name in sorted(sources):
        value = sources[name]
        entries = [value] if isinstance(value, dict) else value
        if not isinstance(entries, list) or not all(
            isinstance(e, dict) for e in entries
        ):
            return unreadable
        if any(not isinstance(e.get("editable", False), bool) for e in entries):
            return unreadable
        if any("path" in e for e in entries):
            findings.append(f"tool.uv.sources.{name} (path)")
        if any(e.get("editable") is True for e in entries):
            findings.append(f"tool.uv.sources.{name} (editable)")
    return findings


@dataclass(frozen=True)
class StageRecord:
    mode: str  # 6 octal digits
    oid: str  # 40 hex
    stage: int  # 1, 2 or 3
    path: str


@dataclass(frozen=True)
class MergeTreeListing:
    tree_oid: str  # 40 hex: the written merge tree
    records: tuple[StageRecord, ...]


@dataclass(frozen=True)
class ProbeResult:
    merge_tree_supported: bool
    base_ref: str
    base_sha: str
    head_sha: str
    merge_base: str
    behind: int
    ahead: int
    foreign_op: str | None
    tree_clean: bool
    status_porcelain: str  # decoded status_b64
    clean: bool | None  # None when merge_tree_supported is False
    listing: MergeTreeListing | None
    binary_paths: frozenset[str]
    programs: frozenset[str]


@dataclass(frozen=True)
class ConflictEntry:
    path: str
    stages: str  # "123", "12", "13", "23", ...
    modes: dict[str, str | None]  # keys "base", "ours", "theirs"
    oids: dict[str, str | None]
    binary: bool


@dataclass(frozen=True)
class PathClass:
    path: str
    stages: str
    cls: str  # "halt:<x>" | "regen:<pattern>" | "text:<x>"
    reason: str


@dataclass(frozen=True)
class ConflictPlan:
    tier: int | None  # 0..3, or None when unclassified
    reason: str  # plan reason (design section 4.3)
    hint: str  # mergeability_hint value
    github_conflicting: bool  # hint == "conflicting"
    paths: tuple[PathClass, ...]
    text_paths: tuple[str, ...]
    regen_paths: tuple[str, ...]
    base_sha: str | None
    head_sha: str | None
    merge_tree_oid: str | None
    behind: int | None
    listing: MergeTreeListing | None


@dataclass(frozen=True)
class ConflictAction:
    action: str  # one of ACTIONS
    reason: str
    status: str | None = (
        None  # None = continue; else "terminal_halted" | "proposed" | "halt_before_push"
    )
    skip_ci: bool = False
    fsm_event: str | None = None  # "conflicting" on the c_initial resolve_push row
    push_kind: str | None = None  # "sync" | "merge" on resolve rows


@dataclass(frozen=True)
class SyncDecision:
    predicate_1_ordinal: bool
    predicate_2_validated: bool
    predicate_3_tier_allowed: bool
    predicate_4_under_cap: bool
    authorized: bool
    kind: str  # "sync" | "merge"

    @property
    def audit_predicates(self) -> dict[str, bool]:
        return {
            "p1_ordinal": self.predicate_1_ordinal,
            "p2_validated": self.predicate_2_validated,
            "p3_tier_allowed": self.predicate_3_tier_allowed,
            "p4_under_cap": self.predicate_4_under_cap,
        }


@dataclass(frozen=True)
class ResumePlan:
    # directive: "none" | "fsm" | "wave8_ci_wait" | "redrive_then_wave8"
    #   | "abort_and_restart" | "restart" | "complete_after_push" | "crash_window" | "halt"
    directive: str
    state: MonitorState | None = None
    reason: str | None = None
    cycle_id: str | None = None
    kind: str | None = None
    wait_sha: str | None = None
    target_sha: str | None = (
        None  # the open cycle's recorded push target (row 4b' message)
    )
    base_sha: str | None = None
    review_terminal: str | None = None
    hook: str | None = (
        None  # restart rows: the open cycle's hook ("wave8a" | "c_initial")
    )
    expect_checks: bool | None = None
    rerun_guard: bool = False
    check_merge_parent: bool = False


# ---------------------------------------------------------------------------
# Internal validators
# ---------------------------------------------------------------------------

_HEX40 = re.compile(r"[0-9a-f]{40}")
_MODE = re.compile(r"[0-7]{6}")
_COUNT = re.compile(r"[0-9]+")
_VALID_STAGES = frozenset({"1", "2", "3", "12", "13", "23", "123"})
_SIDES = (("base", 1), ("ours", 2), ("theirs", 3))


def _is_hex40(value: object) -> bool:
    return isinstance(value, str) and _HEX40.fullmatch(value) is not None


def _is_nonneg_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _has_control_char(path: str) -> bool:
    return any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in path)


def _decode_b64(payload: dict, key: str) -> str:
    """Strict base64 then strict UTF-8 decode of ``payload[key]``; ``ValueError`` otherwise."""
    value = payload.get(key)
    if not isinstance(value, str):
        raise ValueError(f"{key}: expected a base64 string")
    try:
        raw = base64.b64decode(value, validate=True)
    except ValueError as exc:  # binascii.Error is a ValueError
        raise ValueError(f"{key}: not strict base64") from exc
    if len(raw) > MAX_PROBE_BYTES:
        raise ValueError(f"{key}: decoded size above MAX_PROBE_BYTES")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{key}: not valid UTF-8") from exc


# ---------------------------------------------------------------------------
# Hint (design section 5.3)
# ---------------------------------------------------------------------------


def mergeability_hint(mergeable: object, merge_state: object) -> str:
    """Map the PR's ``mergeable`` / ``mergeStateStatus`` pair to a hint. Never raises.

    ``"conflicting"`` when ``mergeable`` is CONFLICTING or the state is DIRTY;
    ``"unknown"`` when ``mergeable`` is anything other than MERGEABLE; otherwise
    ``"behind"`` (BEHIND), ``"blocked"`` (BLOCKED) or ``"clean"``. Case-insensitive.
    """
    m = mergeable.upper() if isinstance(mergeable, str) else None
    s = merge_state.upper() if isinstance(merge_state, str) else None
    if m == "CONFLICTING" or s == "DIRTY":
        return "conflicting"
    if m != "MERGEABLE":
        return "unknown"
    if s == "BEHIND":
        return "behind"
    if s == "BLOCKED":
        return "blocked"
    return "clean"


def needs_probe(hint: str) -> bool:
    """True only for the hints ``"conflicting"`` and ``"unknown"``."""
    return hint in ("conflicting", "unknown")


# ---------------------------------------------------------------------------
# Parsing (design section 5.3)
# ---------------------------------------------------------------------------


def parse_stage_records(raw: str) -> MergeTreeListing:
    """Parse the decoded NUL-separated output of the merge-tree write-tree command.

    The first field is the merged tree id; then ``<mode> <oid> <stage>\\t<path>``
    records up to the first empty field; everything after it (informational
    messages) is ignored. Raises ``ValueError`` on any malformed shape.
    """
    if not isinstance(raw, str):
        raise ValueError("merge-tree output is not a string")
    fields = raw.split("\0")
    tree_oid = fields[0]
    if not _is_hex40(tree_oid):
        raise ValueError("bad tree id")
    records: list[StageRecord] = []
    seen: set[tuple[str, int]] = set()
    for field in fields[1:]:
        if field == "":
            break
        head, sep, path = field.partition("\t")
        if not sep:
            raise ValueError("stage record without a tab")
        parts = head.split(" ")
        if len(parts) != 3:
            raise ValueError("stage record header is not '<mode> <oid> <stage>'")
        mode, oid, stage_text = parts
        if _MODE.fullmatch(mode) is None:
            raise ValueError(f"bad mode {mode!r}")
        if not _is_hex40(oid):
            raise ValueError(f"bad object id {oid!r}")
        if stage_text not in ("1", "2", "3"):
            raise ValueError(f"stage outside 1..3: {stage_text!r}")
        if path == "":
            raise ValueError("empty path")
        stage = int(stage_text)
        if (path, stage) in seen:
            raise ValueError(f"duplicate (path, stage): {path!r} {stage}")
        seen.add((path, stage))
        records.append(StageRecord(mode=mode, oid=oid, stage=stage, path=path))
    return MergeTreeListing(tree_oid=tree_oid, records=tuple(records))


def parse_numstat_binary(raw: str) -> frozenset[str]:
    """Return the binary paths of a decoded ``--numstat -z --no-renames`` listing.

    Records are ``<added>\\t<deleted>\\t<path>``, NUL-terminated; a record whose
    counts are both ``-`` is binary. Raises ``ValueError`` on a record without two
    tabs, an empty path, a count that is neither a number nor ``-``, or one ``-``
    paired with a number.
    """
    if not isinstance(raw, str):
        raise ValueError("numstat output is not a string")
    if raw == "":
        return frozenset()
    body = raw[:-1] if raw.endswith("\0") else raw
    binary: set[str] = set()
    for record in body.split("\0"):
        parts = record.split("\t", 2)
        if len(parts) != 3:
            raise ValueError(f"numstat record without two tabs: {record!r}")
        added, deleted, path = parts
        if path == "":
            raise ValueError("numstat record with an empty path")
        for count in (added, deleted):
            if count != "-" and _COUNT.fullmatch(count) is None:
                raise ValueError(f"numstat count is not numeric: {count!r}")
        if (added == "-") != (deleted == "-"):
            raise ValueError(f"numstat record mixes '-' and a number: {record!r}")
        if added == "-":
            binary.add(path)
    return frozenset(binary)


def parse_probe(payload: object) -> ProbeResult:
    """Validate the full-mode probe JSON (design section 7.1); ``ValueError`` on anything else."""
    if not isinstance(payload, dict):
        raise ValueError("probe payload is not an object")
    if payload.get("ok") is not True:
        raise ValueError("probe ok is not true")
    if payload.get("mode") != "full":
        raise ValueError("probe mode is not 'full'")
    if payload.get("truncated") is not False:
        raise ValueError("probe truncated is not false")
    supported = payload.get("merge_tree_supported")
    if not isinstance(supported, bool):
        raise ValueError("merge_tree_supported is not a bool")
    base_ref = payload.get("base_ref")
    if not isinstance(base_ref, str) or base_ref == "" or _has_control_char(base_ref):
        raise ValueError("bad base_ref")
    for key in ("base_sha", "head_sha", "merge_base"):
        if not _is_hex40(payload.get(key)):
            raise ValueError(f"{key} is not 40 hex")
    for key in ("behind", "ahead"):
        if not _is_nonneg_int(payload.get(key)):
            raise ValueError(f"{key} is not a non-negative int")
    if "foreign_op" not in payload:
        raise ValueError("foreign_op missing")
    foreign_op = payload["foreign_op"]
    if foreign_op is not None and foreign_op not in FOREIGN_OPS:
        raise ValueError("foreign_op is not null or a known operation")
    merge_head = payload.get("merge_head")
    if merge_head is not None and not _is_hex40(merge_head):
        raise ValueError("merge_head is not null or 40 hex")
    tree_clean = payload.get("tree_clean")
    if not isinstance(tree_clean, bool):
        raise ValueError("tree_clean is not a bool")
    status_porcelain = _decode_b64(payload, "status_b64")
    if (status_porcelain == "") != tree_clean:
        raise ValueError("tree_clean disagrees with status_b64")
    programs_raw = payload.get("programs")
    if not isinstance(programs_raw, list) or not all(
        isinstance(p, str) for p in programs_raw
    ):
        raise ValueError("programs is not a list of strings")
    programs = frozenset(programs_raw)

    merge_keys = ("merge_tree_b64", "numstat_ours_b64", "numstat_theirs_b64")
    clean_raw = payload.get("clean", "<missing>")
    listing: MergeTreeListing | None
    clean: bool | None
    if not supported:
        if clean_raw is not None:
            raise ValueError("clean must be null when merge-tree is unsupported")
        for key in merge_keys:
            if payload.get(key, "<missing>") is not None:
                raise ValueError(f"{key} must be null when merge-tree is unsupported")
        listing, clean, binary_paths = None, None, frozenset()
    else:
        if not isinstance(clean_raw, bool):
            raise ValueError("clean is not a bool")
        clean = clean_raw
        listing = parse_stage_records(_decode_b64(payload, "merge_tree_b64"))
        if clean:
            if listing.records:
                raise ValueError("clean probe carries conflict records")
            binary: set[str] = set()
            for key in merge_keys[1:]:
                if payload.get(key) is not None:
                    binary |= parse_numstat_binary(_decode_b64(payload, key))
            binary_paths = frozenset(binary)
        else:
            if not listing.records:
                raise ValueError("conflicting probe carries no conflict records")
            binary_paths = parse_numstat_binary(
                _decode_b64(payload, "numstat_ours_b64")
            ) | parse_numstat_binary(_decode_b64(payload, "numstat_theirs_b64"))
    return ProbeResult(
        merge_tree_supported=supported,
        base_ref=base_ref,
        base_sha=payload["base_sha"],
        head_sha=payload["head_sha"],
        merge_base=payload["merge_base"],
        behind=payload["behind"],
        ahead=payload["ahead"],
        foreign_op=foreign_op,
        tree_clean=tree_clean,
        status_porcelain=status_porcelain,
        clean=clean,
        listing=listing,
        binary_paths=binary_paths,
        programs=programs,
    )


# ---------------------------------------------------------------------------
# Classification (design section 4.3)
# ---------------------------------------------------------------------------


def group_entries(
    listing: MergeTreeListing, binary_paths: frozenset[str]
) -> tuple[ConflictEntry, ...]:
    """One ``ConflictEntry`` per path, in first-seen order, with sorted ``stages``."""
    if not isinstance(listing, MergeTreeListing):
        raise ValueError("listing is not a MergeTreeListing")
    order: list[str] = []
    by_path: dict[str, dict[int, StageRecord]] = {}
    for rec in listing.records:
        if rec.path not in by_path:
            by_path[rec.path] = {}
            order.append(rec.path)
        by_path[rec.path][rec.stage] = rec
    entries: list[ConflictEntry] = []
    for path in order:
        stages = by_path[path]
        modes: dict[str, str | None] = {}
        oids: dict[str, str | None] = {}
        for side, num in _SIDES:
            rec = stages.get(num)
            modes[side] = rec.mode if rec is not None else None
            oids[side] = rec.oid if rec is not None else None
        entries.append(
            ConflictEntry(
                path=path,
                stages="".join(str(n) for n in sorted(stages)),
                modes=modes,
                oids=oids,
                binary=path in binary_paths,
            )
        )
    return tuple(entries)


def _segments_contain(segments: list[str], seq: tuple[str, ...]) -> bool:
    n = len(seq)
    return any(tuple(segments[i : i + n]) == seq for i in range(len(segments) - n + 1))


def classify_path(
    entry: ConflictEntry,
    *,
    programs: frozenset[str],
    rules: tuple[MechanicalRule, ...] = MECHANICAL_RULES,
) -> PathClass:
    """Classify one conflicted path by the first matching rule of design section 4.3."""
    if not isinstance(entry, ConflictEntry) or not isinstance(entry.path, str):
        return PathClass(
            path=str(getattr(entry, "path", "")),
            stages="",
            cls="halt:unknown_shape",
            reason="entry is not a conflict entry",
        )
    path = entry.path
    stages = entry.stages if isinstance(entry.stages, str) else ""

    def out(cls: str, reason: str) -> PathClass:
        return PathClass(path=path, stages=stages, cls=cls, reason=reason)

    if (
        stages not in _VALID_STAGES
        or path == ""
        or not isinstance(entry.modes, dict)
        or not isinstance(entry.binary, bool)
    ):
        return out("halt:unknown_shape", "unexpected entry shape")
    # Rule 0
    if _has_control_char(path):
        return out("halt:unsafe_path", "path contains a control character")
    modes = [m for m in (entry.modes.get(s) for s, _ in _SIDES) if m is not None]
    # Rule 1
    if "160000" in modes:
        return out("halt:submodule", "a side is a submodule")
    # Rule 2
    if "120000" in modes:
        return out("halt:symlink", "a side is a symbolic link")
    # Rule 3
    ours, theirs = entry.modes.get("ours"), entry.modes.get("theirs")
    if ours is not None and theirs is not None and ours != theirs:
        return out("halt:mode_change", "the two sides have different modes")
    # Rule 4
    if path.startswith(PROTECTED_PREFIXES) or path in PROTECTED_PATHS:
        return out("halt:protected", "protected path")
    segments = path.split("/")
    basename = segments[-1]
    # Rule 5
    if any(_segments_contain(segments, seq) for seq in MIGRATION_SEGMENTS):
        return out("halt:migration", "database migration path")
    # Rule 6
    if entry.binary:
        return out("halt:binary", "binary content")
    # Rule 7
    progs = programs if isinstance(programs, (set, frozenset)) else frozenset()
    if isinstance(rules, tuple):
        for rule in rules:
            if (
                not isinstance(rule, MechanicalRule)
                or path != rule.pattern
                or stages != "123"
            ):
                continue
            argvs = [a for a in (rule.regenerate, rule.check) if a]
            if rule.regenerate and all(a[0] in progs for a in argvs):
                return out(
                    f"regen:{rule.pattern}",
                    f"regenerated by {' '.join(rule.regenerate)}",
                )
    # Rule 8
    if basename in LOCKFILE_NAMES or basename.endswith(".lock"):
        return out(
            "halt:lockfile_no_recipe", "lockfile without a usable regeneration rule"
        )
    # Rule 9
    if (
        any(seg in GENERATED_SEGMENTS for seg in segments)
        or ".generated." in basename
        or basename.endswith(".snap")
    ):
        return out(
            "halt:generated_no_recipe", "generated file without a regeneration rule"
        )
    # Rules 10 to 12
    if stages == "123":
        return out("text:content", "content conflict")
    if stages in ("12", "13"):
        return out("text:modify_delete", "modified on one side, deleted on the other")
    if stages == "23":
        return out("text:add_add", "added on both sides")
    # Rule 13
    return out("halt:unknown_shape", "unrecognised stage set")


# ---------------------------------------------------------------------------
# Planning (design section 4.3)
# ---------------------------------------------------------------------------

_HINT_TIER0_REASONS = {
    "clean": "no_conflict",
    "behind": "behind_only",
    "blocked": "blocked",
}


def _plan(
    hint: object,
    tier: int | None,
    reason: str,
    *,
    probe: ProbeResult | None = None,
    paths: tuple[PathClass, ...] = (),
) -> ConflictPlan:
    hint_str = hint if isinstance(hint, str) else ""
    listing = probe.listing if probe is not None else None
    return ConflictPlan(
        tier=tier,
        reason=reason,
        hint=hint_str,
        github_conflicting=hint_str == "conflicting",
        paths=paths,
        text_paths=tuple(p.path for p in paths if p.cls.startswith("text:")),
        regen_paths=tuple(p.path for p in paths if p.cls.startswith("regen:")),
        base_sha=probe.base_sha if probe is not None else None,
        head_sha=probe.head_sha if probe is not None else None,
        merge_tree_oid=listing.tree_oid if listing is not None else None,
        behind=probe.behind if probe is not None else None,
        listing=listing,
    )


def conflict_plan(
    *,
    hint: str,
    probe: object | None,
    probe_failed: bool = False,
    rules: tuple[MechanicalRule, ...] = MECHANICAL_RULES,
    tier2_max_files: int = TIER2_MAX_FILES,
) -> ConflictPlan:
    """Build the conflict plan by the first matching plan-tier row of design section 4.3.

    Never raises and never takes the cap (every cap decision is the router's).
    """
    if isinstance(hint, str) and hint in _HINT_TIER0_REASONS:
        return _plan(hint, 0, _HINT_TIER0_REASONS[hint])
    if not (isinstance(hint, str) and needs_probe(hint)):
        return _plan(hint, 3, "probe_malformed")
    if probe_failed is True:
        return _plan(hint, None, "probe_failed")
    if probe is None or probe_failed is not False:
        return _plan(hint, 3, "probe_malformed")
    try:
        parsed = parse_probe(probe)
    except (ValueError, TypeError, KeyError):
        return _plan(hint, 3, "probe_malformed")
    if not parsed.merge_tree_supported:
        return _plan(hint, None, "merge_tree_unsupported", probe=parsed)
    if parsed.clean:
        return _plan(hint, 0, "no_conflict", probe=parsed)
    if not _is_nonneg_int(tier2_max_files) or parsed.listing is None:
        return _plan(hint, 3, "probe_malformed")
    try:
        entries = group_entries(parsed.listing, parsed.binary_paths)
        classes = tuple(
            classify_path(e, programs=parsed.programs, rules=rules) for e in entries
        )
    except (ValueError, TypeError, AttributeError, IndexError):
        return _plan(hint, 3, "probe_malformed")
    if not classes:
        return _plan(hint, 3, "probe_malformed")
    for pc in classes:
        if pc.cls.startswith("halt:"):
            return _plan(hint, 3, pc.cls, probe=parsed, paths=classes)
    text_count = sum(1 for pc in classes if pc.cls.startswith("text:"))
    if text_count > tier2_max_files:
        return _plan(hint, 3, "too_many_files", probe=parsed, paths=classes)
    if text_count >= 1:
        return _plan(hint, 2, "text_conflict", probe=parsed, paths=classes)
    if all(pc.cls.startswith("regen:") for pc in classes):
        return _plan(hint, 1, "regen_only", probe=parsed, paths=classes)
    return _plan(hint, 3, "probe_malformed")


# ---------------------------------------------------------------------------
# Routing (design section 4.4)
# ---------------------------------------------------------------------------

DEFAULT_ACTION = ConflictAction(
    "halt", "router_unreachable", "terminal_halted", skip_ci=True
)
# Plan reasons the router may echo back: tier None at every hook, tier 0 at wave0.
_ECHO_PLAN_REASONS: dict[int | None, frozenset[str]] = {
    None: frozenset({"probe_failed", "merge_tree_unsupported"}),
    0: frozenset({"no_conflict", "behind_only", "blocked"}),
}


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _router_domain_ok(
    hook: object,
    plan_tier: object,
    ordinal: object,
    entering: object,
    conflict_max_tier: object,
    round_counter: object,
    max_rounds: object,
    prior_conflict_cycles: object,
    github_conflicting: object,
    plan_reason: object,
) -> bool:
    if hook not in HOOKS:
        return False
    if not (_is_int(ordinal) and 0 <= ordinal <= 3):
        return False
    if not (_is_int(conflict_max_tier) and 0 <= conflict_max_tier <= 2):
        return False
    if not (plan_tier is None or (_is_int(plan_tier) and 0 <= plan_tier <= 3)):
        return False
    if not all(
        _is_nonneg_int(v) for v in (round_counter, max_rounds, prior_conflict_cycles)
    ):
        return False
    if not isinstance(github_conflicting, bool):
        return False
    if hook == "wave8a":
        if entering not in ENTERING_OUTCOMES:
            return False
    elif entering is not None:
        return False
    if hook == "c_initial" and ordinal != 3:
        return False
    echoed = plan_tier is None or (plan_tier == 0 and hook == "wave0")
    if echoed and plan_reason not in _ECHO_PLAN_REASONS[plan_tier]:
        return False
    return True


def _route_wave0(plan_tier: int | None, ordinal: int, cap: int, reason: str):
    if plan_tier is None or plan_tier == 0:
        return ConflictAction("report", reason)
    if plan_tier == 1:
        if cap < 1:
            return ConflictAction("report", "tier_above_cap")
        return ConflictAction("report", "tier1_planned")
    if plan_tier == 2:
        if cap < 2:
            return ConflictAction("report", "tier_above_cap")
        if ordinal < 3:
            return ConflictAction("report", "tier2_report_only")
        return ConflictAction("report", "tier2_planned")
    if ordinal < 3:
        return ConflictAction("report", "conflict_tier3")
    return ConflictAction("halt", "conflict_tier3", "terminal_halted")


def _route_c_initial(
    plan_tier: int | None,
    cap: int,
    round_counter: int,
    max_rounds: int,
    prior: int,
    reason: str,
):
    if plan_tier is None:
        return ConflictAction("report", reason)
    if plan_tier == 0:
        return ConflictAction("none", "no_conflict")
    if plan_tier == 1:
        return ConflictAction("none", "tier1_deferred")
    if plan_tier == 2:
        if cap < 2:
            return ConflictAction("report", "tier_above_cap")
        if max_rounds - round_counter < 2:
            return ConflictAction("report", "no_round_budget")
        if prior >= SYNC_CAP:
            return ConflictAction("report", "sync_cap")
        return ConflictAction(
            "resolve_push", "tier2_merge", fsm_event="conflicting", push_kind="merge"
        )
    return ConflictAction("halt", "conflict_tier3", "terminal_halted")


def _route_wave8a(
    plan_tier: int | None,
    ordinal: int,
    entering: str,
    cap: int,
    prior: int,
    github_conflicting: bool,
    reason: str,
):
    preserved = entering in PRESERVED_OUTCOMES
    status = None if preserved else "terminal_halted"
    stop = "report" if preserved else "halt"

    def end(why: str) -> ConflictAction:
        return ConflictAction(stop, why, status, skip_ci=True)

    if plan_tier is None:
        return end(reason)
    if plan_tier == 0:
        if not github_conflicting:
            return ConflictAction("none", "no_conflict", skip_ci=False)
        return end("github_disagrees")
    if plan_tier == 1:
        if cap < 1:
            return end("tier_above_cap")
        if prior >= SYNC_CAP:
            return end("sync_cap")
        if ordinal == 1:
            if preserved:
                return ConflictAction("report", "tier1_l1_preserved", skip_ci=True)
            return ConflictAction("propose", "tier1_proposed", "proposed", skip_ci=True)
        if ordinal == 2:
            if preserved:
                return ConflictAction("report", "tier1_l2_preserved", skip_ci=True)
            return ConflictAction(
                "resolve_local", "tier1_local", "halt_before_push", skip_ci=True
            )
        return ConflictAction("resolve_push", "tier1_sync", push_kind="sync")
    if plan_tier == 2:
        if cap < 2:
            return end("tier_above_cap")
        return end("late_conflict")
    return end("conflict_tier3")


def conflict_action(
    *,
    hook: str,
    plan_tier: int | None,
    ordinal: int,
    entering: str | None,
    conflict_max_tier: int,
    round_counter: int,
    max_rounds: int,
    prior_conflict_cycles: int,
    github_conflicting: bool,
    plan_reason: str = "",
) -> ConflictAction:
    """The only conflict routing decision (design section 4.4). Never raises.

    The domain guard runs first: any input outside its domain (including a plan
    reason this router would echo that is not a plan reason of that tier) gives
    ``DEFAULT_ACTION``. Then ordinal 0 gives ``ConflictAction("none", "l0")``, and
    the hook's table decides, rows top to bottom. ``prior_conflict_cycles`` is
    ``prior_conflict_cycles(conflict_cycles, cycle_id)``.
    """
    if not _router_domain_ok(
        hook,
        plan_tier,
        ordinal,
        entering,
        conflict_max_tier,
        round_counter,
        max_rounds,
        prior_conflict_cycles,
        github_conflicting,
        plan_reason,
    ):
        return DEFAULT_ACTION
    if ordinal == 0:
        return ConflictAction("none", "l0")
    if hook == "wave0":
        return _route_wave0(plan_tier, ordinal, conflict_max_tier, plan_reason)
    if hook == "c_initial":
        return _route_c_initial(
            plan_tier,
            conflict_max_tier,
            round_counter,
            max_rounds,
            prior_conflict_cycles,
            plan_reason,
        )
    return _route_wave8a(
        plan_tier,
        ordinal,
        entering,  # type: ignore[arg-type]
        conflict_max_tier,
        prior_conflict_cycles,
        github_conflicting,
        plan_reason,
    )


# ---------------------------------------------------------------------------
# Gates (design section 5.3)
# ---------------------------------------------------------------------------

_HEX40_ANY_CASE = re.compile(r"[0-9a-fA-F]{40}")
_STATUS_CODES = frozenset(" MTADRCU?!")
_UNPARSABLE_STATUS = "<unparsable status>"


def _is_sha(value: object) -> bool:
    return isinstance(value, str) and _HEX40_ANY_CASE.fullmatch(value) is not None


def merge_preflight_ok(porcelain: object) -> tuple[bool, list[str]]:
    """Whether the tracked tree is clean before the merge (untracked files tolerated).

    ``porcelain`` is the decoded NUL-separated porcelain v1 status listing, taken
    without untracked files. ``(True, [])`` for the empty string; otherwise
    ``(False, paths)`` naming every path (both paths of a rename or copy record).
    A ``??`` record is ignored. A non-string, or a record that cannot be parsed,
    gives ``(False, ["<unparsable status>"])``.
    """
    if not isinstance(porcelain, str):
        return False, [_UNPARSABLE_STATUS]
    if porcelain == "":
        return True, []
    if not porcelain.endswith("\0"):
        return False, [_UNPARSABLE_STATUS]
    fields = porcelain[:-1].split("\0")
    paths: list[str] = []
    i = 0
    while i < len(fields):
        record = fields[i]
        i += 1
        if len(record) < 4 or record[2] != " ":
            return False, [_UNPARSABLE_STATUS]
        code, path = record[:2], record[3:]
        if not set(code) <= _STATUS_CODES or code == "  ":
            return False, [_UNPARSABLE_STATUS]
        if code == "??":
            continue
        paths.append(path)
        if "R" in code or "C" in code:
            if i >= len(fields) or fields[i] == "":
                return False, [_UNPARSABLE_STATUS]
            paths.append(fields[i])
            i += 1
    if not paths:
        return True, []
    return False, paths


def merge_parent_ok(
    target_parents: list[str] | None, pre_push_sha: str | None, base_sha: str | None
) -> bool:
    """Whether the commit to push is exactly the merge of the base tip into the PR head.

    True iff ``target_parents`` is a list of exactly two full 40-hex ids, the first
    equal to ``pre_push_sha`` and the second to ``base_sha`` (case-insensitive), and
    ``pre_push_sha != base_sha``. Disjoint from ``fsm.push_parent_ok`` by parent count.
    """
    if not isinstance(target_parents, list) or len(target_parents) != 2:
        return False
    ids = (target_parents[0], target_parents[1], pre_push_sha, base_sha)
    if not all(_is_sha(v) for v in ids):
        return False
    first, second, pre, base = (v.lower() for v in ids)  # type: ignore[union-attr]
    return first == pre and second == base and pre != base


def evaluate_sync_decision(
    *,
    monitor_ordinal: int,
    validation_status: str,
    tier: int,
    conflict_max_tier: int,
    halt_reason: str | None,
    prior_conflict_cycles: int,
    round_counter: int,
    max_rounds: int,
) -> SyncDecision:
    """The four-predicate conflict push gate (design section 5.3).

    ``p1`` ordinal at least 3; ``p2`` validated; ``p3`` tier 1 or 2, within the cap
    and no halt reason; ``p4`` under ``SYNC_CAP`` (earlier cycles, the current one
    excluded) and, for tier 2, ``round_counter < max_rounds``. Non-int inputs make the
    affected predicate false.
    """
    tier_ok = _is_int(tier) and tier in (1, 2)
    p1 = _is_int(monitor_ordinal) and monitor_ordinal >= 3
    p2 = validation_status == "validated"
    p3 = (
        tier_ok
        and _is_int(conflict_max_tier)
        and tier <= conflict_max_tier
        and halt_reason is None
    )
    p4 = _is_nonneg_int(prior_conflict_cycles) and prior_conflict_cycles < SYNC_CAP
    if p4 and tier_ok and tier == 2:
        p4 = (
            _is_nonneg_int(round_counter)
            and _is_nonneg_int(max_rounds)
            and round_counter < max_rounds
        )
    return SyncDecision(
        predicate_1_ordinal=p1,
        predicate_2_validated=p2,
        predicate_3_tier_allowed=p3,
        predicate_4_under_cap=p4,
        authorized=p1 and p2 and p3 and p4,
        kind="merge" if tier_ok and tier == 2 else "sync",
    )


def sync_fail_state(decision: SyncDecision) -> MonitorState:
    """Map a blocked ``SyncDecision`` to its fail route; never a push state.

    ``p3`` false: ``HALT_HUMAN``; otherwise ``REPORT_ONLY`` (``p4`` false is reported
    as ``sync_cap``). A non-``SyncDecision`` gives ``HALT_HUMAN``.
    """
    if not isinstance(decision, SyncDecision):
        return MonitorState.HALT_HUMAN
    if not decision.predicate_3_tier_allowed:
        return MonitorState.HALT_HUMAN
    return MonitorState.REPORT_ONLY


def conflict_validation_status(tier: int, results: dict[str, bool]) -> str:
    """``run_validation_gates(results)``; tier 2 also needs ``VG-2`` green.

    Any tier other than 1 or 2, or a non-dict ``results``, gives ``"failed"``.
    """
    if not (_is_int(tier) and tier in (1, 2)) or not isinstance(results, dict):
        return "failed"
    status = run_validation_gates(results)
    if tier == 2 and results.get("VG-2") is not True:
        return "failed"
    return status


# ---------------------------------------------------------------------------
# Cycle ids (design sections 4.7 and 4.8)
# ---------------------------------------------------------------------------


def conflict_cycle_id(tier: int, n: int) -> str:
    """``"sync-<n>"`` for tier 1, ``"conflict-<n>"`` for tier 2; ``ValueError`` otherwise."""
    if not (_is_int(n) and n >= 1):
        raise ValueError("cycle number must be an int >= 1")
    if _is_int(tier) and tier == 1:
        return f"sync-{n}"
    if _is_int(tier) and tier == 2:
        return f"conflict-{n}"
    raise ValueError("conflict cycles exist only for tier 1 or 2")


def conflict_attempt(events: object, cycle_id: object) -> int:
    """The attempt number of ``cycle_id``: how many ``sync_started`` events in the
    run-log ``events`` carry that id (1 for a first run, 2 after one restart).

    Called right after step 3 appends the cycle's ``sync_started``, so a count of 0
    (or a non-list, or a non-string id) is a contract breach: ``ValueError``.
    """
    if not isinstance(events, list) or not isinstance(cycle_id, str):
        raise ValueError(
            "conflict_attempt needs a list of events and a string cycle id"
        )
    count = sum(
        1
        for ev in events
        if isinstance(ev, dict)
        and ev.get("event_type") == "sync_started"
        and ev.get("cycle_id") == cycle_id
    )
    if count == 0:
        raise ValueError(f"no sync_started event for {cycle_id!r}")
    return count


def is_conflict_cycle(cycle_id: object) -> bool:
    """True only for a string starting with a reserved conflict-cycle prefix."""
    return isinstance(cycle_id, str) and cycle_id.startswith(CONFLICT_CYCLE_PREFIXES)


def prior_conflict_cycles(conflict_cycles: object, cycle_id: object) -> int:
    """Distinct string ids in ``conflict_cycles`` other than ``cycle_id``.

    A non-list input returns ``SYNC_CAP`` (fail closed: the cap is treated as reached).
    """
    if not isinstance(conflict_cycles, list):
        return SYNC_CAP
    return len({c for c in conflict_cycles if isinstance(c, str) and c != cycle_id})


# ---------------------------------------------------------------------------
# Finish manifest, resolution record and commit message (design section 5.3)
# ---------------------------------------------------------------------------


def finish_manifest(listing: MergeTreeListing, resolved_paths: list[str]) -> str:
    """One ``<stage-1 oid or ->\\t<path>\\n`` line per resolved path, in listing order.

    ``ValueError`` when a resolved path is not in the listing, appears twice, or
    contains a control character.
    """
    if not isinstance(listing, MergeTreeListing):
        raise ValueError("listing is not a MergeTreeListing")
    if not isinstance(resolved_paths, (list, tuple)):
        raise ValueError("resolved_paths is not a list")
    wanted: set[str] = set()
    for path in resolved_paths:
        if not isinstance(path, str) or path == "":
            raise ValueError("resolved path is not a non-empty string")
        if _has_control_char(path):
            raise ValueError(f"resolved path contains a control character: {path!r}")
        if path in wanted:
            raise ValueError(f"resolved path appears twice: {path!r}")
        wanted.add(path)
    order: list[str] = []
    base_oid: dict[str, str] = {}
    for rec in listing.records:
        if rec.path not in order:
            order.append(rec.path)
        if rec.stage == 1:
            base_oid[rec.path] = rec.oid
    missing = wanted.difference(order)
    if missing:
        raise ValueError(f"resolved path not in the listing: {sorted(missing)!r}")
    return "".join(f"{base_oid.get(p, '-')}\t{p}\n" for p in order if p in wanted)


def parse_resolution_record(text: str) -> dict[str, dict[str, str]]:
    """Parse ``resolution.md``: ``## <path>`` headings, then ``<field>: <value>`` lines.

    Blank lines are skipped. ``ValueError`` on a duplicate heading, a duplicate
    field, an unknown field (any other non-blank line), an empty heading, or a field
    line before the first heading.
    """
    if not isinstance(text, str):
        raise ValueError("record text is not a string")
    record: dict[str, dict[str, str]] = {}
    current: dict[str, str] | None = None
    for line in text.splitlines():
        if line.strip() == "":
            continue
        if line.startswith("## "):
            path = line[3:].strip()
            if path == "":
                raise ValueError("empty heading")
            if path in record:
                raise ValueError(f"duplicate heading: {path!r}")
            current = record[path] = {}
            continue
        name, sep, value = line.partition(":")
        name = name.strip()
        if current is None:
            raise ValueError("field line before the first heading")
        if not sep or name not in RECORD_FIELDS:
            raise ValueError(f"unknown field: {name!r}")
        if name in current:
            raise ValueError(f"duplicate field: {name!r}")
        current[name] = value.strip()
    return record


_SENTENCE_FIELDS = ("ours_intent", "theirs_intent", "behavior_after")
_SENTENCE_STOP = re.compile(r"[.!?](?=\s|$)")
_KEEP_BOTH_ORDER = re.compile(r"keep_both\(\s*\S.*\)")


def _one_sentence(value: str) -> bool:
    if "\n" in value or "\r" in value:
        return False
    text = value.strip()
    return text[-1:] in (".", "!", "?") and len(_SENTENCE_STOP.findall(text)) == 1


def resolution_record_ok(
    record: dict[str, dict[str, str]], text_paths: tuple[str, ...]
) -> list[str]:
    """Problems with a parsed resolution record; empty when it is valid (section 5.3)."""
    if not isinstance(record, dict):
        return ["record is not a mapping"]
    if not isinstance(text_paths, (tuple, list)):
        return ["text paths are not a sequence"]
    problems: list[str] = []
    for path in text_paths:
        if path not in record:
            problems.append(f"{path}: missing entry")
    for path, entry in record.items():
        if path not in text_paths:
            problems.append(f"{path}: extra entry")
            continue
        if not isinstance(entry, dict):
            problems.append(f"{path}: entry is not a mapping")
            continue
        for name in entry:
            if name not in RECORD_FIELDS:
                problems.append(f"{path}: unknown field {name}")
        for name in RECORD_FIELDS:
            value = entry.get(name)
            if not isinstance(value, str) or value.strip() == "":
                problems.append(f"{path}: {name} is missing or empty")
                continue
            if name in _SENTENCE_FIELDS and not _one_sentence(value):
                problems.append(f"{path}: {name} is not exactly one sentence")
            elif name == "kind":
                if value == "semantic":
                    problems.append(f"{path}: kind semantic means Tier 3")
                elif value not in RECORD_KINDS:
                    problems.append(f"{path}: unknown kind {value}")
            elif name == "resolution" and not (
                value in RECORD_RESOLUTIONS or _KEEP_BOTH_ORDER.fullmatch(value)
            ):
                problems.append(f"{path}: unknown resolution {value}")
    return problems


def _one_line(value: object, what: str) -> str:
    if not isinstance(value, str) or value.strip() == "" or _has_control_char(value):
        raise ValueError(f"{what} must be a non-empty single-line string")
    return value


def merge_commit_message(
    *,
    base_ref: str,
    head_branch: str,
    tier: int,
    rule_patterns: tuple[str, ...] = (),
    record: dict[str, dict[str, str]] | None = None,
    lock_changes: str = "",
) -> str:
    """The merge commit message without the attribution lines (the SKILL appends them).

    Subject ``Merge <base_ref> into <head_branch> (sc:pr-submit sync, tier <t>)``.
    Tier 1 body: one line per rule path naming its sources, then ``lock_changes``.
    Tier 2 body: one line per path with ``kind``, ``resolution`` and ``dropped``.
    Labels only, never file content. ``ValueError`` on a tier other than 1 or 2, a
    tier 2 call without a record, or an unknown rule pattern.
    """
    subject = (
        f"Merge {_one_line(base_ref, 'base_ref')} into "
        f"{_one_line(head_branch, 'head_branch')} (sc:pr-submit sync, tier {tier})"
    )
    lines: list[str] = []
    if _is_int(tier) and tier == 1:
        if not isinstance(rule_patterns, (tuple, list)) or not isinstance(
            lock_changes, str
        ):
            raise ValueError("rule_patterns must be a tuple and lock_changes a string")
        rules = {r.pattern: r for r in MECHANICAL_RULES}
        for pattern in rule_patterns:
            rule = rules.get(pattern) if isinstance(pattern, str) else None
            if rule is None:
                raise ValueError(f"unknown rule pattern: {pattern!r}")
            lines.append(
                f"{rule.pattern} regenerated from the merged {', '.join(rule.sources)}"
            )
        if lock_changes.strip():
            lines.append(lock_changes.strip())
    elif _is_int(tier) and tier == 2:
        if not isinstance(record, dict) or not record:
            raise ValueError("a tier 2 merge commit message needs a resolution record")
        for path, entry in record.items():
            if not isinstance(entry, dict):
                raise ValueError(f"record entry for {path!r} is not a mapping")
            labels = [
                _one_line(entry.get(k), f"{path} {k}")
                for k in ("kind", "resolution", "dropped")
            ]
            lines.append(
                f"{_one_line(path, 'path')}: kind {labels[0]}, "
                f"resolution {labels[1]}, dropped {labels[2]}"
            )
    else:
        raise ValueError("tier must be 1 or 2")
    if not lines:
        return subject + "\n"
    return subject + "\n\n" + "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Resume planners (design section 4.8)
# ---------------------------------------------------------------------------

_BRANCHES = (BRANCH_LANDED, BRANCH_NOT_LANDED, BRANCH_AMBIGUOUS)
_RESUME_STATE_KEYS = (
    "sync_push_count",
    "conflict_cycles",
    "open_conflict_cycle",
    "push_rejected",
)


def _sha_or_none(value: object) -> str | None:
    return value if _is_sha(value) else None


def crash_resume_plan(
    dangling: dict, branch: str, fsm_state: MonitorState
) -> ResumePlan:
    """Map a settled crash window to a resume directive (design section 4.8, table 2).

    ``kind`` is the record's ``kind`` (absent means ``fix``). ``fix`` and ``merge``
    keep today's states; ``sync`` and ``ci`` re-enter the Wave 8 CI wait and never
    resume into a push or review state. An unknown branch or kind, or an unusable
    record, gives ``halt`` / ``resume_unrepresentable``. Pure: appends nothing.
    """
    if not isinstance(dangling, dict):
        return ResumePlan("halt", reason="resume_unrepresentable")
    raw_kind = dangling.get("kind") or "fix"
    kind = raw_kind if raw_kind in PUSH_KINDS else None
    cycle_id = dangling.get("cycle_id")
    common = {
        "cycle_id": cycle_id if isinstance(cycle_id, str) else None,
        "kind": kind,
        "target_sha": _sha_or_none(dangling.get("target_sha")),
        "base_sha": _sha_or_none(dangling.get("base_sha")),
    }

    def halt(reason: str, state: MonitorState | None = None) -> ResumePlan:
        return ResumePlan("halt", state=state, reason=reason, **common)

    if kind is None or branch not in _BRANCHES:
        return halt("resume_unrepresentable")
    if branch == BRANCH_AMBIGUOUS:
        return halt("ambiguous_remote_tip", MonitorState.HALT_HUMAN)
    if kind in ("fix", "merge"):
        if branch == BRANCH_LANDED:
            if not isinstance(fsm_state, MonitorState):
                return halt("resume_unrepresentable")
            return ResumePlan("fsm", state=fsm_state, **common)
        return ResumePlan(
            "fsm",
            state=MonitorState.S4_PUSHING,
            check_merge_parent=kind == "merge",
            **common,
        )
    review_terminal = dangling.get("review_terminal")
    if review_terminal not in ENTERING_OUTCOMES or common["target_sha"] is None:
        return halt("resume_unrepresentable")
    if kind == "sync" and common["base_sha"] is None:
        return halt("resume_unrepresentable")
    expect = dangling.get("expect_checks")
    wave8 = {
        "wait_sha": common["target_sha"],
        "review_terminal": review_terminal,
        "expect_checks": expect if isinstance(expect, bool) else True,
    }
    if branch == BRANCH_LANDED:
        return ResumePlan("wave8_ci_wait", **common, **wave8)
    return ResumePlan(
        "redrive_then_wave8",
        rerun_guard=True,
        check_merge_parent=kind == "sync",
        **common,
        **wave8,
    )


def conflict_resume_plan(
    state: dict,
    *,
    foreign_op: str | None,
    merge_head_sha: str | None,
    local_head_sha: str | None,
    local_head_parents: list[str] | None,
    dangling: dict | None,
) -> ResumePlan:
    """The ``--resume`` directive for an open conflict cycle (design section 4.8, table 1).

    Rows in table order, first match wins: 1, 2, 3, 3b, 4c, 4, 4b, 4b', 5, 6, 7, 8.
    Every halt plan that finds an open cycle carries its ``cycle_id`` so the SKILL
    closes it once; restart rows carry the open cycle's ``cycle_id``, ``hook`` and
    ``review_terminal``. ``local_head_parents`` never changes the outcome: a local
    two-parent commit no push record covers still reaches row 8. A ``state``
    without the run-log keys of design section 6.3 gives ``halt`` /
    ``resume_unrepresentable``. Pure: the SKILL appends the events the rows name.
    """
    unrepresentable = ResumePlan("halt", reason="resume_unrepresentable")
    if not isinstance(state, dict) or any(k not in state for k in _RESUME_STATE_KEYS):
        return unrepresentable
    open_cycle = state["open_conflict_cycle"]
    if (
        not isinstance(state["push_rejected"], bool)
        or not isinstance(state["conflict_cycles"], list)
        or not _is_nonneg_int(state["sync_push_count"])
        or not (open_cycle is None or isinstance(open_cycle, dict))
    ):
        return unrepresentable
    cycle_id = open_cycle.get("cycle_id") if open_cycle is not None else None
    cycle_id = cycle_id if is_conflict_cycle(cycle_id) else None

    def halt(reason: str, **extra: object) -> ResumePlan:
        return ResumePlan("halt", reason=reason, cycle_id=cycle_id, **extra)  # type: ignore[arg-type]

    # Row 1
    if state["push_rejected"]:
        return halt("push_rejected")
    # Rows 2 and 3
    if open_cycle is None:
        if foreign_op is None:
            return ResumePlan("none")
        return ResumePlan("halt", reason="foreign_op_in_progress")
    if cycle_id is None:
        return unrepresentable
    # Row 3b
    if open_cycle.get("superseded") is not False:
        return halt("resume_unrepresentable")
    # Row 4c
    hook = open_cycle.get("hook")
    review_terminal = open_cycle.get("review_terminal")
    if (
        hook not in ("wave8a", "c_initial")
        or (hook == "wave8a" and review_terminal not in ENTERING_OUTCOMES)
        or (hook == "c_initial" and review_terminal is not None)
    ):
        return halt("resume_unrepresentable")
    kind = open_cycle.get("kind")
    kind = kind if kind in ("sync", "merge") else None
    target_sha = _sha_or_none(open_cycle.get("target_sha"))
    base_sha = _sha_or_none(open_cycle.get("base_sha"))
    cycle = {"cycle_id": cycle_id, "hook": hook, "review_terminal": review_terminal}
    pushed = open_cycle.get("push_completed") is True
    initiated = open_cycle.get("push_initiated") is True
    # Row 4
    if pushed:
        if kind is None or target_sha is None:
            return halt("resume_unrepresentable", target_sha=target_sha)
        expect = open_cycle.get("expect_checks")
        return ResumePlan(
            "complete_after_push",
            state=MonitorState.S5A_RETRIGGER_REVIEW if kind == "merge" else None,
            kind=kind,
            wait_sha=target_sha if kind == "sync" else None,
            target_sha=target_sha,
            base_sha=base_sha,
            expect_checks=expect if isinstance(expect, bool) else True,
            **cycle,
        )
    # Rows 4b and 4b'
    if initiated:
        if isinstance(dangling, dict) and dangling.get("cycle_id") == cycle_id:
            return ResumePlan(
                "crash_window",
                kind=kind,
                target_sha=target_sha,
                base_sha=base_sha,
                **cycle,
            )
        return halt("resume_unrepresentable", target_sha=target_sha)
    # Row 5
    if (
        foreign_op == "MERGE_HEAD"
        and _is_sha(merge_head_sha)
        and base_sha is not None
        and merge_head_sha.lower() == base_sha.lower()  # type: ignore[union-attr]
    ):
        return ResumePlan("abort_and_restart", kind=kind, base_sha=base_sha, **cycle)
    # Row 6
    if foreign_op is not None:
        return halt("sync_foreign_operation")
    # Row 7
    pre_push_sha = open_cycle.get("pre_push_sha")
    if (
        _is_sha(local_head_sha)
        and _is_sha(pre_push_sha)
        and local_head_sha.lower() == pre_push_sha.lower()  # type: ignore[union-attr]
    ):
        return ResumePlan("restart", kind=kind, base_sha=base_sha, **cycle)
    # Row 8
    return halt("resume_unrepresentable")
