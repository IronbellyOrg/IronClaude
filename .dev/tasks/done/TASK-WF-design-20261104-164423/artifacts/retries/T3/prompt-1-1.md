64543aeb313326b3ff49f862f8c1ea2f7d7b8375
Review one task for spec compliance.

Task brief: ## Task 3: Create `conflicts.py` with parsing, classification and planning

Depends on: Task 2

Create `src/superclaude/pr_submit/conflicts.py` per source sections 5.1, 5.2 and the parsing, classification and planning rows of 5.3, with the rules of source section 4.3:

- Module rules of source section 5.1 (standard library `base64`, `re`, `dataclasses`, `typing` only; internal imports `from .models import MonitorState` and `from .fsm import run_validation_gates`; never import `recovery`; no I/O; T-N50 clean; fail closed).
- Every constant and data type of source section 5.2 (including `REPORT_REASONS`, `HALT_REASONS`, the three `BRANCH_*` literals, `MechanicalRule`, `MECHANICAL_RULES`, `StageRecord`, `MergeTreeListing`, `ProbeResult`, `ConflictEntry`, `PathClass`, `ConflictPlan`, `ConflictAction`, `SyncDecision`, `ResumePlan` with `target_sha` and `hook`).
- Functions `mergeability_hint`, `needs_probe`, `parse_stage_records`, `parse_numstat_binary`, `parse_probe`, `group_entries`, `classify_path` (the 14-row first-match table of source section 4.3) and `conflict_plan` (the plan-tier table of source section 4.3; never takes the cap).
- Create the fixture `tests/pr_submit/fixtures/merge_tree_conflict.z` from a scratch repository under a temporary directory (one content conflict `f.txt` with stages 1/2/3, one modify/delete `d.txt` with stages 1/2), and put the capture recipe as a comment at the top of the test file.
- Create `tests/pr_submit/test_conflicts_core.py` with the Hint, Parse, Classify, Plan and Purity cases of source section 12.1.
- Append `PR_SUBMIT_PKG / "conflicts.py",` to `CORE_PURE_FILES` in `tests/pr_submit/test_static_grep.py:37-51` with the comment from source section 12.2.

Acceptance criteria:
- `parse_stage_records` on the fixture returns the exact records; every malformed shape listed in source section 12.1 raises `ValueError`.
- One parametrized test row per classification rule 0 to 13 passes, including the boundary rows of source section 12.1 (`pkg/uv.lock`, root `uv.lock` without `uv`, `uv.lock` with stages `"12"`, a path with a tab, `__snapshots__/x.snap`).
- Plan rows: 8 text paths give Tier 2, 9 give Tier 3 `too_many_files`; regen plus text is Tier 2; `probe_failed` and `merge_tree_unsupported` give tier `None`; a malformed probe gives Tier 3 `probe_malformed`.
- The AST purity test shows `conflicts.py` imports only the allowed modules; T-N50 and T-N41 in `test_static_grep.py` pass with `conflicts.py` in `CORE_PURE_FILES`.
- `uv run pytest tests/pr_submit/test_conflicts_core.py tests/pr_submit/test_static_grep.py -q` passes; log saved to `./artifacts/t3-tests.log`.
Global constraints: 
- The design in `./source.md` is the specification. Every section reference below (for example "source section 5.3") points into it. Where a task and the source disagree, the source wins; record the disagreement in the task's evidence.
- Never force-push, and never write a force flag after the words "git push" on any line of a `.md` or `.sh` file in `src/superclaude/skills/sc-pr-submit-protocol/` (the force-push scan in `tests/pr_submit/test_static_grep.py:758-776` covers every such file). The only push text is `git push origin <target_sha>:<HEAD_BRANCH>`; prohibitions are written in words.
- `push_parent_ok`, `evaluate_push_decision`, `push_fail_state`, `push_idempotency_key`, `needs_rebase` and every existing `transition()` edge in `src/superclaude/pr_submit/fsm.py` stay byte-identical (source section 6.1). `resolve_crash_window` in `recovery.py` keeps its signature and return value.
- T-N50: no `git` or `gh` token (regex `\bgh\b|\bgit\b`), docstrings and comments included, in `conflicts.py`, `fsm.py`, `ci.py`, `refs/state-machine.md`, `refs/loop-guard.md` and every other file in `CORE_PURE_FILES` (`tests/pr_submit/test_static_grep.py:37-51`).
- Installed primitives (`SKILL.md`, refs, scripts, `commands/pr-submit.md`) never name a `src/superclaude/` path in new text.
- Every `gh` call in new text carries `--repo "$REPO"` or a `repos/<owner/repo>/` path. Nothing contacts `SuperClaude-Org/SuperClaude_Framework`.
- Never stash, never use a hook-skipping flag, never amend, never stage everything; stage exact paths only.
- `SKILL.md` keeps exactly one python code block (`tests/pr_submit/test_cosmos_protocol.py:36`, `tests/pr_submit/test_codex_reviews.py:688`) and grows by at most 15 lines (source section 8.1).
- Edit `src/superclaude/`, then run `make sync-dev`; never stage `.claude/` paths except `.claude/settings.json`. `.dev/tasks/` is always staged (`git add .dev/tasks`), including this package and its `artifacts/`.
- Python through UV only (`uv run pytest ...`, `uv run python ...`). Run the tests each task names plus `tests/pr_submit/`, `tests/unit/test_cli_install.py` and `tests/commands/`; do not run the full suite (`make test`) or `tests/cli/eval/` as a directory (orchestrator brief; this overrides the `make test` step of source section 12.5).
- Real-git tests run only inside pytest temporary directories with a local bare repository as `origin`, a `gh` stub on `PATH`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, and for real `uv` `UV_OFFLINE=1`, `UV_NO_CONFIG=1`, `UV_CACHE_DIR=<tmp>` (source section 12 preamble). No test touches the network or `~/.claude`.
- Out of scope: P3 late re-sync (#361) and the post-release verification follow-ups V1 to V8 of source section 14; they are not implemented by this plan.
- Task evidence (test logs, grep output) goes under `./artifacts/` in this package.
Start sha: 64543aeb313326b3ff49f862f8c1ea2f7d7b8375
Diff against the start snapshot: diff --git a/src/superclaude/pr_submit/conflicts.py b/src/superclaude/pr_submit/conflicts.py
new file mode 100644
index 00000000..a13177da
--- /dev/null
+++ b/src/superclaude/pr_submit/conflicts.py
@@ -0,0 +1,789 @@
+"""The pure merge-conflict core for sc:pr-submit (issue #305, design section 5).
+
+This module parses the read-only probe output, classifies every conflicted path
+into a tier and builds the conflict plan the SKILL reports before any edit.
+
+Module rules (design section 5.1):
+
+- Standard library only (``base64``, ``re``, ``dataclasses``, ``typing``); the only
+  internal imports are ``MonitorState`` from ``.models`` and, for the validation
+  status helper, ``run_validation_gates`` from ``.fsm``. This module never imports
+  ``recovery`` (``recovery`` imports this module), so it defines its own branch
+  literals.
+- No I/O, no clock, no environment reads, and no version-control command names
+  anywhere in this file. The probe, the merge and the merge-tree command are named
+  in words.
+- Every public function fails closed: malformed input raises ``ValueError`` where
+  the contract says so, and otherwise the most restrictive answer is returned
+  (``False``, Tier 3, a ``halt`` class).
+"""
+
+import base64
+import re
+from dataclasses import dataclass
+
+from .models import MonitorState
+
+# ---------------------------------------------------------------------------
+# Constants (design section 5.2)
+# ---------------------------------------------------------------------------
+
+SYNC_CAP: int = 1  # conflict cycles per run, both tiers together (INV-019)
+TIER2_MAX_FILES: int = 8  # text:* paths; regen:* paths do not count (OQ-9)
+MAX_PROBE_BYTES: int = (
+    102_400  # the probe truncates above this; a truncated probe is Tier 3
+)
+CONFLICT_CYCLE_PREFIXES: tuple[str, ...] = ("sync-", "conflict-")
+HOOKS: tuple[str, ...] = ("wave0", "c_initial", "wave8a")
+ENTERING_OUTCOMES: tuple[str, ...] = (
+    "clean",
+    "report_only",
+    "halt_max_rounds",
+    "no_response",
+)
+PRESERVED_OUTCOMES: tuple[str, ...] = ("halt_max_rounds", "no_response")
+ACTIONS: tuple[str, ...] = (
+    "none",
+    "report",
+    "propose",
+    "resolve_local",
+    "resolve_push",
+    "halt",
+)
+PUSH_KINDS: tuple[str, ...] = ("fix", "merge", "sync", "ci")
+FOREIGN_OPS: tuple[str, ...] = (
+    "MERGE_HEAD",
+    "rebase-merge",
+    "rebase-apply",
+    "CHERRY_PICK_HEAD",
+    "REVERT_HEAD",
+    "sequencer",
+)
+CONFLICT_PROPOSE_PROMPT: str = "resolve these conflicts? y/n"
+PROTECTED_PREFIXES: tuple[str, ...] = (".github/workflows/", ".github/actions/")
+PROTECTED_PATHS: tuple[str, ...] = (
+    ".claude/settings.json",
+    ".claude/settings.local.json",
+)
+MIGRATION_SEGMENTS: tuple[tuple[str, ...], ...] = (
+    ("migrations",),
+    ("alembic", "versions"),
+    ("db", "migrate"),
+)
+LOCKFILE_NAMES: tuple[str, ...] = (
+    "package-lock.json",
+    "yarn.lock",
+    "pnpm-lock.yaml",
+    "Cargo.lock",
+    "poetry.lock",
+    "Pipfile.lock",
+    "flake.lock",
+    "uv.lock",
+)
+GENERATED_SEGMENTS: tuple[str, ...] = ("generated", "dist", "build", "__snapshots__")
+RECORD_KINDS: tuple[str, ...] = (
+    "trivial",
+    "additive",
+    "competing",
+    "structural",
+    "modify-delete",
+    "add-add",
+    "semantic",
+)
+RECORD_RESOLUTIONS: tuple[str, ...] = (
+    "keep_both",
+    "take_ours",
+    "take_theirs",
+    "synthesized",
+)
+RECORD_FIELDS: tuple[str, ...] = (
+    "kind",
+    "root_cause",
+    "ours_intent",
+    "theirs_intent",
+    "resolution",
+    "behavior_after",
+    "dropped",
+    "evidence",
+)
+
+# Every reason conflict_action can return, in any row (design section 4.4, section 9).
+REPORT_REASONS: frozenset[str] = frozenset(
+    {
+        # report-only reasons (no halt by themselves)
+        "no_conflict",
+        "behind_only",
+        "blocked",
+        "tier1_planned",
+        "tier2_planned",
+        "tier2_report_only",
+        "tier1_deferred",
+        "tier1_proposed",
+        "tier1_l2_preserved",
+        "tier1_local",
+        "tier1_sync",
+        "tier2_merge",
+        "no_round_budget",
+        "l0",
+        "tier1_l1_preserved",
+        # router return values that halt on some rows
+        "tier_above_cap",
+        "conflict_tier3",
+        "probe_failed",
+        "merge_tree_unsupported",
+        "github_disagrees",
+        "sync_cap",
+        "late_conflict",
+        "router_unreachable",
+    }
+)
+# Every reason ever written to terminal_halted by a conflict path (design section 9).
+HALT_REASONS: frozenset[str] = frozenset(
+    {
+        "foreign_op_in_progress",
+        "conflict_tier3",
+        "late_conflict",
+        "tier_above_cap",
+        "github_disagrees",
+        "probe_failed",
+        "merge_tree_unsupported",
+        "sync_cap",
+        "merge_preflight_dirty",
+        "sync_foreign_operation",
+        "sync_merge_failed",
+        "sync_marker_left",
+        "sync_unmerged_left",
+        "sync_staged_unexpected",
+        "sync_commit_failed",
+        "sync_head_mismatch",
+        "sync_range_mismatch",
+        "sync_base_moved",
+        "sync_tier3",
+        "sync_validation_failed",
+        "push_rejected",
+        "push_failed",
+        "resume_unrepresentable",
+        "router_unreachable",
+    }
+)
+# The two sets overlap by design: a reason is reported at one hook or ordinal and halts at
+# another. The intersection is exactly {"tier_above_cap", "conflict_tier3", "probe_failed",
+# "merge_tree_unsupported", "github_disagrees", "sync_cap", "late_conflict", "router_unreachable"},
+# pinned by a test so a new reason must be placed deliberately.
+
+BRANCH_LANDED: str = "landed"  # equal to recovery.BRANCH_A_LANDED (pinned by a test)
+BRANCH_NOT_LANDED: str = "not_landed"  # equal to recovery.BRANCH_B_NOT_LANDED
+BRANCH_AMBIGUOUS: str = "ambiguous"  # equal to recovery.BRANCH_C_AMBIGUOUS
+
+
+# ---------------------------------------------------------------------------
+# Data types (design section 5.2)
+# ---------------------------------------------------------------------------
+
+
+@dataclass(frozen=True)
+class MechanicalRule:
+    """One mechanical regeneration rule. Adding a rule = one row in MECHANICAL_RULES
+    plus one parametrized test row."""
+
+    pattern: str  # exact repository-root-relative path, never a bare basename
+    kind: str  # "lockfile" | "generated"
+    sources: tuple[
+        str, ...
+    ]  # paths the output is derived from (documentation and report)
+    regenerate: tuple[str, ...]  # argv; argv[0] must be in SKILL.md allowed-tools
+    check: tuple[str, ...] = ()  # argv; argv[0] must be in SKILL.md allowed-tools
+
+
+MECHANICAL_RULES: tuple[MechanicalRule, ...] = (
+    MechanicalRule(
+        "uv.lock",
+        "lockfile",
+        ("pyproject.toml",),
+        ("uv", "lock"),
+        ("uv", "lock", "--check"),
+    ),
+)
+
+
+@dataclass(frozen=True)
+class StageRecord:
+    mode: str  # 6 octal digits
+    oid: str  # 40 hex
+    stage: int  # 1, 2 or 3
+    path: str
+
+
+@dataclass(frozen=True)
+class MergeTreeListing:
+    tree_oid: str  # 40 hex: the written merge tree
+    records: tuple[StageRecord, ...]
+
+
+@dataclass(frozen=True)
+class ProbeResult:
+    merge_tree_supported: bool
+    base_ref: str
+    base_sha: str
+    head_sha: str
+    merge_base: str
+    behind: int
+    ahead: int
+    foreign_op: str | None
+    tree_clean: bool
+    status_porcelain: str  # decoded status_b64
+    clean: bool | None  # None when merge_tree_supported is False
+    listing: MergeTreeListing | None
+    binary_paths: frozenset[str]
+    programs: frozenset[str]
+
+
+@dataclass(frozen=True)
+class ConflictEntry:
+    path: str
+    stages: str  # "123", "12", "13", "23", ...
+    modes: dict[str, str | None]  # keys "base", "ours", "theirs"
+    oids: dict[str, str | None]
+    binary: bool
+
+
+@dataclass(frozen=True)
+class PathClass:
+    path: str
+    stages: str
+    cls: str  # "halt:<x>" | "regen:<pattern>" | "text:<x>"
+    reason: str
+
+
+@dataclass(frozen=True)
+class ConflictPlan:
+    tier: int | None  # 0..3, or None when unclassified
+    reason: str  # plan reason (design section 4.3)
+    hint: str  # mergeability_hint value
+    github_conflicting: bool  # hint == "conflicting"
+    paths: tuple[PathClass, ...]
+    text_paths: tuple[str, ...]
+    regen_paths: tuple[str, ...]
+    base_sha: str | None
+    head_sha: str | None
+    merge_tree_oid: str | None
+    behind: int | None
+    listing: MergeTreeListing | None
+
+
+@dataclass(frozen=True)
+class ConflictAction:
+    action: str  # one of ACTIONS
+    reason: str
+    status: str | None = (
+        None  # None = continue; else "terminal_halted" | "proposed" | "halt_before_push"
+    )
+    skip_ci: bool = False
+    fsm_event: str | None = None  # "conflicting" on the c_initial resolve_push row
+    push_kind: str | None = None  # "sync" | "merge" on resolve rows
+
+
+@dataclass(frozen=True)
+class SyncDecision:
+    predicate_1_ordinal: bool
+    predicate_2_validated: bool
+    predicate_3_tier_allowed: bool
+    predicate_4_under_cap: bool
+    authorized: bool
+    kind: str  # "sync" | "merge"
+
+    @property
+    def audit_predicates(self) -> dict[str, bool]:
+        return {
+            "p1_ordinal": self.predicate_1_ordinal,
+            "p2_validated": self.predicate_2_validated,
+            "p3_tier_allowed": self.predicate_3_tier_allowed,
+            "p4_under_cap": self.predicate_4_under_cap,
+        }
+
+
+@dataclass(frozen=True)
+class ResumePlan:
+    # directive: "none" | "fsm" | "wave8_ci_wait" | "redrive_then_wave8"
+    #   | "abort_and_restart" | "restart" | "complete_after_push" | "crash_window" | "halt"
+    directive: str
+    state: MonitorState | None = None
+    reason: str | None = None
+    cycle_id: str | None = None
+    kind: str | None = None
+    wait_sha: str | None = None
+    target_sha: str | None = (
+        None  # the open cycle's recorded push target (row 4b' message)
+    )
+    base_sha: str | None = None
+    review_terminal: str | None = None
+    hook: str | None = (
+        None  # restart rows: the open cycle's hook ("wave8a" | "c_initial")
+    )
+    expect_checks: bool | None = None
+    rerun_guard: bool = False
+    check_merge_parent: bool = False
+
+
+# ---------------------------------------------------------------------------
+# Internal validators
+# ---------------------------------------------------------------------------
+
+_HEX40 = re.compile(r"[0-9a-f]{40}")
+_MODE = re.compile(r"[0-7]{6}")
+_COUNT = re.compile(r"[0-9]+")
+_VALID_STAGES = frozenset({"1", "2", "3", "12", "13", "23", "123"})
+_SIDES = (("base", 1), ("ours", 2), ("theirs", 3))
+
+
+def _is_hex40(value: object) -> bool:
+    return isinstance(value, str) and _HEX40.fullmatch(value) is not None
+
+
+def _is_nonneg_int(value: object) -> bool:
+    return isinstance(value, int) and not isinstance(value, bool) and value >= 0
+
+
+def _has_control_char(path: str) -> bool:
+    return any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in path)
+
+
+def _decode_b64(payload: dict, key: str) -> str:
+    """Strict base64 then strict UTF-8 decode of ``payload[key]``; ``ValueError`` otherwise."""
+    value = payload.get(key)
+    if not isinstance(value, str):
+        raise ValueError(f"{key}: expected a base64 string")
+    try:
+        raw = base64.b64decode(value, validate=True)
+    except ValueError as exc:  # binascii.Error is a ValueError
+        raise ValueError(f"{key}: not strict base64") from exc
+    if len(raw) > MAX_PROBE_BYTES:
+        raise ValueError(f"{key}: decoded size above MAX_PROBE_BYTES")
+    try:
+        return raw.decode("utf-8")
+    except UnicodeDecodeError as exc:
+        raise ValueError(f"{key}: not valid UTF-8") from exc
+
+
+# ---------------------------------------------------------------------------
+# Hint (design section 5.3)
+# ---------------------------------------------------------------------------
+
+
+def mergeability_hint(mergeable: object, merge_state: object) -> str:
+    """Map the PR's ``mergeable`` / ``mergeStateStatus`` pair to a hint. Never raises.
+
+    ``"conflicting"`` when ``mergeable`` is CONFLICTING or the state is DIRTY;
+    ``"unknown"`` when ``mergeable`` is anything other than MERGEABLE; otherwise
+    ``"behind"`` (BEHIND), ``"blocked"`` (BLOCKED) or ``"clean"``. Case-insensitive.
+    """
+    m = mergeable.upper() if isinstance(mergeable, str) else None
+    s = merge_state.upper() if isinstance(merge_state, str) else None
+    if m == "CONFLICTING" or s == "DIRTY":
+        return "conflicting"
+    if m != "MERGEABLE":
+        return "unknown"
+    if s == "BEHIND":
+        return "behind"
+    if s == "BLOCKED":
+        return "blocked"
+    return "clean"
+
+
+def needs_probe(hint: str) -> bool:
+    """True only for the hints ``"conflicting"`` and ``"unknown"``."""
+    return hint in ("conflicting", "unknown")
+
+
+# ---------------------------------------------------------------------------
+# Parsing (design section 5.3)
+# ---------------------------------------------------------------------------
+
+
+def parse_stage_records(raw: str) -> MergeTreeListing:
+    """Parse the decoded NUL-separated output of the merge-tree write-tree command.
+
+    The first field is the merged tree id; then ``<mode> <oid> <stage>\\t<path>``
+    records up to the first empty field; everything after it (informational
+    messages) is ignored. Raises ``ValueError`` on any malformed shape.
+    """
+    if not isinstance(raw, str):
+        raise ValueError("merge-tree output is not a string")
+    fields = raw.split("\0")
+    tree_oid = fields[0]
+    if not _is_hex40(tree_oid):
+        raise ValueError("bad tree id")
+    records: list[StageRecord] = []
+    seen: set[tuple[str, int]] = set()
+    for field in fields[1:]:
+        if field == "":
+            break
+        head, sep, path = field.partition("\t")
+        if not sep:
+            raise ValueError("stage record without a tab")
+        parts = head.split(" ")
+        if len(parts) != 3:
+            raise ValueError("stage record header is not '<mode> <oid> <stage>'")
+        mode, oid, stage_text = parts
+        if _MODE.fullmatch(mode) is None:
+            raise ValueError(f"bad mode {mode!r}")
+        if not _is_hex40(oid):
+            raise ValueError(f"bad object id {oid!r}")
+        if stage_text not in ("1", "2", "3"):
+            raise ValueError(f"stage outside 1..3: {stage_text!r}")
+        if path == "":
+            raise ValueError("empty path")
+        stage = int(stage_text)
+        if (path, stage) in seen:
+            raise ValueError(f"duplicate (path, stage): {path!r} {stage}")
+        seen.add((path, stage))
+        records.append(StageRecord(mode=mode, oid=oid, stage=stage, path=path))
+    return MergeTreeListing(tree_oid=tree_oid, records=tuple(records))
+
+
+def parse_numstat_binary(raw: str) -> frozenset[str]:
+    """Return the binary paths of a decoded ``--numstat -z --no-renames`` listing.
+
+    Records are ``<added>\\t<deleted>\\t<path>``, NUL-terminated; a record whose
+    counts are both ``-`` is binary. Raises ``ValueError`` on a record without two
+    tabs, an empty path, a count that is neither a number nor ``-``, or one ``-``
+    paired with a number.
+    """
+    if not isinstance(raw, str):
+        raise ValueError("numstat output is not a string")
+    if raw == "":
+        return frozenset()
+    body = raw[:-1] if raw.endswith("\0") else raw
+    binary: set[str] = set()
+    for record in body.split("\0"):
+        parts = record.split("\t", 2)
+        if len(parts) != 3:
+            raise ValueError(f"numstat record without two tabs: {record!r}")
+        added, deleted, path = parts
+        if path == "":
+            raise ValueError("numstat record with an empty path")
+        for count in (added, deleted):
+            if count != "-" and _COUNT.fullmatch(count) is None:
+                raise ValueError(f"numstat count is not numeric: {count!r}")
+        if (added == "-") != (deleted == "-"):
+            raise ValueError(f"numstat record mixes '-' and a number: {record!r}")
+        if added == "-":
+            binary.add(path)
+    return frozenset(binary)
+
+
+def parse_probe(payload: object) -> ProbeResult:
+    """Validate the full-mode probe JSON (design section 7.1); ``ValueError`` on anything else."""
+    if not isinstance(payload, dict):
+        raise ValueError("probe payload is not an object")
+    if payload.get("ok") is not True:
+        raise ValueError("probe ok is not true")
+    if payload.get("mode") != "full":
+        raise ValueError("probe mode is not 'full'")
+    if payload.get("truncated") is not False:
+        raise ValueError("probe truncated is not false")
+    supported = payload.get("merge_tree_supported")
+    if not isinstance(supported, bool):
+        raise ValueError("merge_tree_supported is not a bool")
+    base_ref = payload.get("base_ref")
+    if not isinstance(base_ref, str) or base_ref == "" or _has_control_char(base_ref):
+        raise ValueError("bad base_ref")
+    for key in ("base_sha", "head_sha", "merge_base"):
+        if not _is_hex40(payload.get(key)):
+            raise ValueError(f"{key} is not 40 hex")
+    for key in ("behind", "ahead"):
+        if not _is_nonneg_int(payload.get(key)):
+            raise ValueError(f"{key} is not a non-negative int")
+    if "foreign_op" not in payload:
+        raise ValueError("foreign_op missing")
+    foreign_op = payload["foreign_op"]
+    if foreign_op is not None and foreign_op not in FOREIGN_OPS:
+        raise ValueError("foreign_op is not null or a known operation")
+    merge_head = payload.get("merge_head")
+    if merge_head is not None and not _is_hex40(merge_head):
+        raise ValueError("merge_head is not null or 40 hex")
+    tree_clean = payload.get("tree_clean")
+    if not isinstance(tree_clean, bool):
+        raise ValueError("tree_clean is not a bool")
+    status_porcelain = _decode_b64(payload, "status_b64")
+    if (status_porcelain == "") != tree_clean:
+        raise ValueError("tree_clean disagrees with status_b64")
+    programs_raw = payload.get("programs")
+    if not isinstance(programs_raw, list) or not all(
+        isinstance(p, str) for p in programs_raw
+    ):
+        raise ValueError("programs is not a list of strings")
+    programs = frozenset(programs_raw)
+
+    merge_keys = ("merge_tree_b64", "numstat_ours_b64", "numstat_theirs_b64")
+    clean_raw = payload.get("clean", "<missing>")
+    listing: MergeTreeListing | None
+    clean: bool | None
+    if not supported:
+        if clean_raw is not None:
+            raise ValueError("clean must be null when merge-tree is unsupported")
+        for key in merge_keys:
+            if payload.get(key, "<missing>") is not None:
+                raise ValueError(f"{key} must be null when merge-tree is unsupported")
+        listing, clean, binary_paths = None, None, frozenset()
+    else:
+        if not isinstance(clean_raw, bool):
+            raise ValueError("clean is not a bool")
+        clean = clean_raw
+        listing = parse_stage_records(_decode_b64(payload, "merge_tree_b64"))
+        if clean:
+            if listing.records:
+                raise ValueError("clean probe carries conflict records")
+            binary: set[str] = set()
+            for key in merge_keys[1:]:
+                if payload.get(key) is not None:
+                    binary |= parse_numstat_binary(_decode_b64(payload, key))
+            binary_paths = frozenset(binary)
+        else:
+            if not listing.records:
+                raise ValueError("conflicting probe carries no conflict records")
+            binary_paths = parse_numstat_binary(
+                _decode_b64(payload, "numstat_ours_b64")
+            ) | parse_numstat_binary(_decode_b64(payload, "numstat_theirs_b64"))
+    return ProbeResult(
+        merge_tree_supported=supported,
+        base_ref=base_ref,
+        base_sha=payload["base_sha"],
+        head_sha=payload["head_sha"],
+        merge_base=payload["merge_base"],
+        behind=payload["behind"],
+        ahead=payload["ahead"],
+        foreign_op=foreign_op,
+        tree_clean=tree_clean,
+        status_porcelain=status_porcelain,
+        clean=clean,
+        listing=listing,
+        binary_paths=binary_paths,
+        programs=programs,
+    )
+
+
+# ---------------------------------------------------------------------------
+# Classification (design section 4.3)
+# ---------------------------------------------------------------------------
+
+
+def group_entries(
+    listing: MergeTreeListing, binary_paths: frozenset[str]
+) -> tuple[ConflictEntry, ...]:
+    """One ``ConflictEntry`` per path, in first-seen order, with sorted ``stages``."""
+    if not isinstance(listing, MergeTreeListing):
+        raise ValueError("listing is not a MergeTreeListing")
+    order: list[str] = []
+    by_path: dict[str, dict[int, StageRecord]] = {}
+    for rec in listing.records:
+        if rec.path not in by_path:
+            by_path[rec.path] = {}
+            order.append(rec.path)
+        by_path[rec.path][rec.stage] = rec
+    entries: list[ConflictEntry] = []
+    for path in order:
+        stages = by_path[path]
+        modes: dict[str, str | None] = {}
+        oids: dict[str, str | None] = {}
+        for side, num in _SIDES:
+            rec = stages.get(num)
+            modes[side] = rec.mode if rec is not None else None
+            oids[side] = rec.oid if rec is not None else None
+        entries.append(
+            ConflictEntry(
+                path=path,
+                stages="".join(str(n) for n in sorted(stages)),
+                modes=modes,
+                oids=oids,
+                binary=path in binary_paths,
+            )
+        )
+    return tuple(entries)
+
+
+def _segments_contain(segments: list[str], seq: tuple[str, ...]) -> bool:
+    n = len(seq)
+    return any(tuple(segments[i : i + n]) == seq for i in range(len(segments) - n + 1))
+
+
+def classify_path(
+    entry: ConflictEntry,
+    *,
+    programs: frozenset[str],
+    rules: tuple[MechanicalRule, ...] = MECHANICAL_RULES,
+) -> PathClass:
+    """Classify one conflicted path by the first matching rule of design section 4.3."""
+    if not isinstance(entry, ConflictEntry) or not isinstance(entry.path, str):
+        return PathClass(
+            path=str(getattr(entry, "path", "")),
+            stages="",
+            cls="halt:unknown_shape",
+            reason="entry is not a conflict entry",
+        )
+    path = entry.path
+    stages = entry.stages if isinstance(entry.stages, str) else ""
+
+    def out(cls: str, reason: str) -> PathClass:
+        return PathClass(path=path, stages=stages, cls=cls, reason=reason)
+
+    if (
+        stages not in _VALID_STAGES
+        or path == ""
+        or not isinstance(entry.modes, dict)
+        or not isinstance(entry.binary, bool)
+    ):
+        return out("halt:unknown_shape", "unexpected entry shape")
+    # Rule 0
+    if _has_control_char(path):
+        return out("halt:unsafe_path", "path contains a control character")
+    modes = [m for m in (entry.modes.get(s) for s, _ in _SIDES) if m is not None]
+    # Rule 1
+    if "160000" in modes:
+        return out("halt:submodule", "a side is a submodule")
+    # Rule 2
+    if "120000" in modes:
+        return out("halt:symlink", "a side is a symbolic link")
+    # Rule 3
+    ours, theirs = entry.modes.get("ours"), entry.modes.get("theirs")
+    if ours is not None and theirs is not None and ours != theirs:
+        return out("halt:mode_change", "the two sides have different modes")
+    # Rule 4
+    if path.startswith(PROTECTED_PREFIXES) or path in PROTECTED_PATHS:
+        return out("halt:protected", "protected path")
+    segments = path.split("/")
+    basename = segments[-1]
+    # Rule 5
+    if any(_segments_contain(segments, seq) for seq in MIGRATION_SEGMENTS):
+        return out("halt:migration", "database migration path")
+    # Rule 6
+    if entry.binary:
+        return out("halt:binary", "binary content")
+    # Rule 7
+    progs = programs if isinstance(programs, (set, frozenset)) else frozenset()
+    if isinstance(rules, tuple):
+        for rule in rules:
+            if (
+                not isinstance(rule, MechanicalRule)
+                or path != rule.pattern
+                or stages != "123"
+            ):
+                continue
+            argvs = [a for a in (rule.regenerate, rule.check) if a]
+            if rule.regenerate and all(a[0] in progs for a in argvs):
+                return out(
+                    f"regen:{rule.pattern}",
+                    f"regenerated by {' '.join(rule.regenerate)}",
+                )
+    # Rule 8
+    if basename in LOCKFILE_NAMES or basename.endswith(".lock"):
+        return out(
+            "halt:lockfile_no_recipe", "lockfile without a usable regeneration rule"
+        )
+    # Rule 9
+    if (
+        any(seg in GENERATED_SEGMENTS for seg in segments)
+        or ".generated." in basename
+        or basename.endswith(".snap")
+    ):
+        return out(
+            "halt:generated_no_recipe", "generated file without a regeneration rule"
+        )
+    # Rules 10 to 12
+    if stages == "123":
+        return out("text:content", "content conflict")
+    if stages in ("12", "13"):
+        return out("text:modify_delete", "modified on one side, deleted on the other")
+    if stages == "23":
+        return out("text:add_add", "added on both sides")
+    # Rule 13
+    return out("halt:unknown_shape", "unrecognised stage set")
+
+
+# ---------------------------------------------------------------------------
+# Planning (design section 4.3)
+# ---------------------------------------------------------------------------
+
+_HINT_TIER0_REASONS = {
+    "clean": "no_conflict",
+    "behind": "behind_only",
+    "blocked": "blocked",
+}
+
+
+def _plan(
+    hint: object,
+    tier: int | None,
+    reason: str,
+    *,
+    probe: ProbeResult | None = None,
+    paths: tuple[PathClass, ...] = (),
+) -> ConflictPlan:
+    hint_str = hint if isinstance(hint, str) else ""
+    listing = probe.listing if probe is not None else None
+    return ConflictPlan(
+        tier=tier,
+        reason=reason,
+        hint=hint_str,
+        github_conflicting=hint_str == "conflicting",
+        paths=paths,
+        text_paths=tuple(p.path for p in paths if p.cls.startswith("text:")),
+        regen_paths=tuple(p.path for p in paths if p.cls.startswith("regen:")),
+        base_sha=probe.base_sha if probe is not None else None,
+        head_sha=probe.head_sha if probe is not None else None,
+        merge_tree_oid=listing.tree_oid if listing is not None else None,
+        behind=probe.behind if probe is not None else None,
+        listing=listing,
+    )
+
+
+def conflict_plan(
+    *,
+    hint: str,
+    probe: object | None,
+    probe_failed: bool = False,
+    rules: tuple[MechanicalRule, ...] = MECHANICAL_RULES,
+    tier2_max_files: int = TIER2_MAX_FILES,
+) -> ConflictPlan:
+    """Build the conflict plan by the first matching plan-tier row of design section 4.3.
+
+    Never raises and never takes the cap (every cap decision is the router's).
+    """
+    if isinstance(hint, str) and hint in _HINT_TIER0_REASONS:
+        return _plan(hint, 0, _HINT_TIER0_REASONS[hint])
+    if not (isinstance(hint, str) and needs_probe(hint)):
+        return _plan(hint, 3, "probe_malformed")
+    if probe_failed is True:
+        return _plan(hint, None, "probe_failed")
+    if probe is None or probe_failed is not False:
+        return _plan(hint, 3, "probe_malformed")
+    try:
+        parsed = parse_probe(probe)
+    except (ValueError, TypeError, KeyError):
+        return _plan(hint, 3, "probe_malformed")
+    if not parsed.merge_tree_supported:
+        return _plan(hint, None, "merge_tree_unsupported", probe=parsed)
+    if parsed.clean:
+        return _plan(hint, 0, "no_conflict", probe=parsed)
+    if not _is_nonneg_int(tier2_max_files) or parsed.listing is None:
+        return _plan(hint, 3, "probe_malformed")
+    try:
+        entries = group_entries(parsed.listing, parsed.binary_paths)
+        classes = tuple(
+            classify_path(e, programs=parsed.programs, rules=rules) for e in entries
+        )
+    except (ValueError, TypeError, AttributeError, IndexError):
+        return _plan(hint, 3, "probe_malformed")
+    if not classes:
+        return _plan(hint, 3, "probe_malformed")
+    for pc in classes:
+        if pc.cls.startswith("halt:"):
+            return _plan(hint, 3, pc.cls, probe=parsed, paths=classes)
+    text_count = sum(1 for pc in classes if pc.cls.startswith("text:"))
+    if text_count > tier2_max_files:
+        return _plan(hint, 3, "too_many_files", probe=parsed, paths=classes)
+    if text_count >= 1:
+        return _plan(hint, 2, "text_conflict", probe=parsed, paths=classes)
+    if all(pc.cls.startswith("regen:") for pc in classes):
+        return _plan(hint, 1, "regen_only", probe=parsed, paths=classes)
+    return _plan(hint, 3, "probe_malformed")
diff --git a/tests/pr_submit/test_conflicts_core.py b/tests/pr_submit/test_conflicts_core.py
new file mode 100644
index 00000000..7b1ab496
--- /dev/null
+++ b/tests/pr_submit/test_conflicts_core.py
@@ -0,0 +1,850 @@
+# Capture recipe for fixtures/merge_tree_conflict.z (run once in a scratch directory,
+# then copy out.z next to this file; the scratch directory is removed afterwards):
+#
+#   S=$(mktemp -d /tmp/t3-mergetree.XXXXXXXX)
+#   export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
+#   export GIT_AUTHOR_NAME=Test GIT_AUTHOR_EMAIL=test@example.com
+#   export GIT_COMMITTER_NAME=Test GIT_COMMITTER_EMAIL=test@example.com
+#   export GIT_AUTHOR_DATE=2026-01-01T00:00:00Z GIT_COMMITTER_DATE=2026-01-01T00:00:00Z
+#   cd "$S" && git init -q -b main repo && cd repo
+#   printf 'base\n' > f.txt; printf 'keep\n' > d.txt
+#   git add f.txt d.txt && git commit -q -m base
+#   git checkout -q -b pr
+#   printf 'ours\n' > f.txt; printf 'modified\n' > d.txt
+#   git commit -q -am pr
+#   git checkout -q main
+#   printf 'theirs\n' > f.txt; git rm -q d.txt
+#   git commit -q -am main
+#   git merge-tree --write-tree -z pr main > "$S/out.z"   # exit 1: conflicts
+#   cp "$S/out.z" tests/pr_submit/fixtures/merge_tree_conflict.z
+#   cd / && rm -rf "$S"
+#
+# Result: one content conflict f.txt (stages 1/2/3) and one modify/delete d.txt
+# (stages 1/2: deleted on main, modified on pr), captured with git 2.47.3.
+"""Pure conflict core tests (design section 5; section 12.1 Hint, Parse, Classify,
+Plan and Purity cases). Task 4 adds the router, gate, record and resume cases."""
+
+from __future__ import annotations
+
+import ast
+import base64
+from pathlib import Path
+
+import pytest
+
+from superclaude.pr_submit import conflicts as c
+from superclaude.pr_submit.conflicts import (
+    MECHANICAL_RULES,
+    ConflictEntry,
+    MergeTreeListing,
+    StageRecord,
+    classify_path,
+    conflict_plan,
+    group_entries,
+    mergeability_hint,
+    needs_probe,
+    parse_numstat_binary,
+    parse_probe,
+    parse_stage_records,
+)
+
+FIXTURE = Path(__file__).parent / "fixtures" / "merge_tree_conflict.z"
+CONFLICTS_PY = (
+    Path(__file__).resolve().parents[2]
+    / "src"
+    / "superclaude"
+    / "pr_submit"
+    / "conflicts.py"
+)
+
+TREE = "94f94fd471e0a27a1da0c3e76fc54479e74be423"
+SHA_A = "a" * 40
+SHA_B = "b" * 40
+SHA_C = "c" * 40
+OID = "1" * 40
+
+
+def _b64(text: str) -> str:
+    return base64.b64encode(text.encode("utf-8")).decode("ascii")
+
+
+# ---------------------------------------------------------------------------
+# Hint
+# ---------------------------------------------------------------------------
+
+_STATES = [
+    "CLEAN",
+    "DIRTY",
+    "BEHIND",
+    "BLOCKED",
+    "UNSTABLE",
+    "HAS_HOOKS",
+    "UNKNOWN",
+    "dirty",
+    "behind",
+    "blocked",
+    None,
+    "junk",
+    7,
+]
+# Expected hint for mergeable == MERGEABLE, by state.
+_MERGEABLE_ROW = {
+    "CLEAN": "clean",
+    "DIRTY": "conflicting",
+    "BEHIND": "behind",
+    "BLOCKED": "blocked",
+    "UNSTABLE": "clean",
+    "HAS_HOOKS": "clean",
+    "UNKNOWN": "clean",
+    "dirty": "conflicting",
+    "behind": "behind",
+    "blocked": "blocked",
+    None: "clean",
+    "junk": "clean",
+    7: "clean",
+}
+
+
+@pytest.mark.parametrize("mergeable", ["MERGEABLE", "mergeable", "Mergeable"])
+@pytest.mark.parametrize("state", _STATES)
+def test_hint_mergeable(mergeable, state):
+    assert mergeability_hint(mergeable, state) == _MERGEABLE_ROW[state]
+
+
+@pytest.mark.parametrize("mergeable", ["CONFLICTING", "conflicting"])
+@pytest.mark.parametrize("state", _STATES)
+def test_hint_conflicting_always_wins(mergeable, state):
+    assert mergeability_hint(mergeable, state) == "conflicting"
+
+
+@pytest.mark.parametrize(
+    "mergeable", ["UNKNOWN", "unknown", None, "junk", "", 3, ["MERGEABLE"]]
+)
+@pytest.mark.parametrize("state", _STATES)
+def test_hint_not_mergeable_is_unknown_unless_dirty(mergeable, state):
+    expected = (
+        "conflicting"
+        if isinstance(state, str) and state.upper() == "DIRTY"
+        else "unknown"
+    )
+    assert mergeability_hint(mergeable, state) == expected
+
+
+@pytest.mark.parametrize(
+    "hint, expected",
+    [
+        ("conflicting", True),
+        ("unknown", True),
+        ("clean", False),
+        ("behind", False),
+        ("blocked", False),
+        ("CONFLICTING", False),
+        ("", False),
+    ],
+)
+def test_needs_probe(hint, expected):
+    assert needs_probe(hint) is expected
+
+
+# ---------------------------------------------------------------------------
+# Parse: merge-tree stage records
+# ---------------------------------------------------------------------------
+
+
+def test_parse_stage_records_on_captured_fixture():
+    listing = parse_stage_records(FIXTURE.read_bytes().decode("utf-8"))
+    assert listing == MergeTreeListing(
+        tree_oid=TREE,
+        records=(
+            StageRecord(
+                "100644", "2fa992c0b8b5c6acd2bdd4fa31de29d29799bdd5", 1, "d.txt"
+            ),
+            StageRecord(
+                "100644", "2e0996000b7e9019eabcad29391bf0f5c7702f0b", 2, "d.txt"
+            ),
+            StageRecord(
+                "100644", "df967b96a579e45a18b8251732d16804b2e56a55", 1, "f.txt"
+            ),
+            StageRecord(
+                "100644", "b19a1e93bec1317dc6097229e12afaffbfa74dc2", 2, "f.txt"
+            ),
+            StageRecord(
+                "100644", "950b81b7eee953d050aa05a641f8e056c85dd1bd", 3, "f.txt"
+            ),
+        ),
+    )
+
+
+def test_group_entries_on_captured_fixture():
+    listing = parse_stage_records(FIXTURE.read_bytes().decode("utf-8"))
+    entries = group_entries(listing, frozenset({"f.txt"}))
+    assert [(e.path, e.stages, e.binary) for e in entries] == [
+        ("d.txt", "12", False),
+        ("f.txt", "123", True),
+    ]
+    d = entries[0]
+    assert d.modes == {"base": "100644", "ours": "100644", "theirs": None}
+    assert d.oids == {
+        "base": "2fa992c0b8b5c6acd2bdd4fa31de29d29799bdd5",
+        "ours": "2e0996000b7e9019eabcad29391bf0f5c7702f0b",
+        "theirs": None,
+    }
+
+
+def test_group_entries_sorts_stages_and_keeps_first_seen_order():
+    listing = MergeTreeListing(
+        TREE,
+        (
+            StageRecord("100644", OID, 3, "b"),
+            StageRecord("100644", OID, 2, "a"),
+            StageRecord("100644", OID, 2, "b"),
+        ),
+    )
+    entries = group_entries(listing, frozenset())
+    assert [(e.path, e.stages) for e in entries] == [("b", "23"), ("a", "2")]
+
+
+def test_group_entries_rejects_non_listing():
+    with pytest.raises(ValueError):
+        group_entries("junk", frozenset())  # type: ignore[arg-type]
+
+
+def test_parse_stage_records_tree_only_gives_no_records():
+    assert parse_stage_records(TREE + "\0") == MergeTreeListing(TREE, ())
+    assert parse_stage_records(TREE) == MergeTreeListing(TREE, ())
+
+
+def test_parse_stage_records_ignores_messages_after_empty_field():
+    raw = (
+        f"{TREE}\x00100644 {OID} 2\tx\x00\x00"
+        + "1\x00x\x00CONFLICT (junk)\x00not a record\x00"
+    )
+    assert parse_stage_records(raw).records == (StageRecord("100644", OID, 2, "x"),)
+
+
+@pytest.mark.parametrize(
+    "raw",
+    [
+        pytest.param("deadbeef\0", id="bad-tree-oid-short"),
+        pytest.param(("g" * 40) + "\0", id="bad-tree-oid-nonhex"),
+        pytest.param("", id="empty-output"),
+        pytest.param(f"{TREE}\x0010064 {OID} 1\tx\0\0", id="bad-mode-5-digits"),
+        pytest.param(f"{TREE}\x00100648 {OID} 1\tx\0\0", id="bad-mode-non-octal"),
+        pytest.param(f"{TREE}\x00100644 {OID[:39]} 1\tx\0\0", id="short-oid"),
+        pytest.param(f"{TREE}\x00100644 {OID} 0\tx\0\0", id="stage-0"),
+        pytest.param(f"{TREE}\x00100644 {OID} 4\tx\0\0", id="stage-4"),
+        pytest.param(f"{TREE}\x00100644 {OID} 1\t\0\0", id="empty-path"),
+        pytest.param(
+            f"{TREE}\x00100644 {OID} 1\tx\x00100644 {OID} 1\tx\0\0",
+            id="duplicate-path-stage",
+        ),
+        pytest.param(f"{TREE}\x00100644 {OID} 1 x\0\0", id="missing-tab"),
+        pytest.param(f"{TREE}\x00100644  {OID} 1\tx\0\0", id="extra-space"),
+    ],
+)
+def test_parse_stage_records_malformed_raises(raw):
+    with pytest.raises(ValueError):
+        parse_stage_records(raw)
+
+
+def test_parse_stage_records_non_string_raises():
+    with pytest.raises(ValueError):
+        parse_stage_records(b"bytes")  # type: ignore[arg-type]
+
+
+# ---------------------------------------------------------------------------
+# Parse: numstat binary listing
+# ---------------------------------------------------------------------------
+
+
+def test_parse_numstat_binary_rows():
+    raw = "-\t-\timg.png\x003\t1\tsrc/a.py\x00-\t-\tdir/with\ttab.bin\x00"
+    assert parse_numstat_binary(raw) == frozenset({"img.png", "dir/with\ttab.bin"})
+
+
+def test_parse_numstat_binary_text_only_and_empty():
+    assert parse_numstat_binary("1\t2\ta.txt\x00") == frozenset()
+    assert parse_numstat_binary("") == frozenset()
+
+
+@pytest.mark.parametrize(
+    "raw",
+    [
+        pytest.param("1\ta.txt\x00", id="one-tab"),
+        pytest.param("x\t2\ta.txt\x00", id="non-numeric"),
+        pytest.param("1\t-\ta.txt\x00", id="mixed-dash"),
+        pytest.param("1\t2\t\x00", id="empty-path"),
+        pytest.param("1\t2\ta\x00\x00", id="empty-record"),
+    ],
+)
+def test_parse_numstat_binary_malformed_raises(raw):
+    with pytest.raises(ValueError):
+        parse_numstat_binary(raw)
+
+
+# ---------------------------------------------------------------------------
+# Parse: probe JSON
+# ---------------------------------------------------------------------------
+
+
+def _probe(**overrides):
+    payload = {
+        "ok": True,
+        "mode": "full",
+        "merge_tree_supported": True,
+        "base_ref": "origin/main",
+        "base_sha": SHA_A,
+        "head_sha": SHA_B,
+        "merge_base": SHA_C,
+        "behind": 3,
+        "ahead": 2,
+        "foreign_op": None,
+        "merge_head": None,
+        "tree_clean": True,
+        "status_b64": "",
+        "clean": False,
+        "merge_tree_b64": base64.b64encode(FIXTURE.read_bytes()).decode("ascii"),
+        "numstat_ours_b64": _b64("1\t1\tf.txt\x001\t1\td.txt\x00"),
+        "numstat_theirs_b64": _b64("1\t1\tf.txt\x000\t1\td.txt\x00"),
+        "programs": ["uv"],
+        "truncated": False,
+    }
+    payload.update(overrides)
+    return payload
+
+
+def _without(key):
+    return {k: v for k, v in _probe().items() if k != key}
+
+
+_UNSUPPORTED = {
+    "merge_tree_supported": False,
+    "clean": None,
+    "merge_tree_b64": None,
+    "numstat_ours_b64": None,
+    "numstat_theirs_b64": None,
+}
+_CLEAN = {
+    "clean": True,
+    "merge_tree_b64": _b64(TREE + "\0"),
+    "numstat_ours_b64": None,
+    "numstat_theirs_b64": None,
+}
+
+
+def test_parse_probe_valid_conflicting():
+    result = parse_probe(_probe())
+    assert result.merge_tree_supported is True
+    assert result.clean is False
+    assert result.base_ref == "origin/main"
+    assert (result.base_sha, result.head_sha, result.merge_base) == (
+        SHA_A,
+        SHA_B,
+        SHA_C,
+    )
+    assert (result.behind, result.ahead) == (3, 2)
+    assert result.foreign_op is None
+    assert result.listing is not None and result.listing.tree_oid == TREE
+    assert len(result.listing.records) == 5
+    assert result.binary_paths == frozenset()
+    assert result.programs == frozenset({"uv"})
+    assert result.status_porcelain == ""
+
+
+@pytest.mark.parametrize("op", c.FOREIGN_OPS)
+def test_parse_probe_accepts_each_foreign_op(op):
+    assert parse_probe(_probe(foreign_op=op)).foreign_op == op
+
+
+def test_parse_probe_binary_paths_union_both_sides():
+    result = parse_probe(
+        _probe(
+            numstat_ours_b64=_b64("-\t-\tf.txt\x00"),
+            numstat_theirs_b64=_b64("-\t-\tother.bin\x00"),
+        )
+    )
+    assert result.binary_paths == frozenset({"f.txt", "other.bin"})
+
+
+def test_parse_probe_decodes_status():
+    status = " M pyproject.toml\x00"
+    result = parse_probe(_probe(tree_clean=False, status_b64=_b64(status)))
+    assert result.tree_clean is False
+    assert result.status_porcelain == status
+
+
+def test_parse_probe_unsupported_shape():
+    result = parse_probe(_probe(**_UNSUPPORTED))
+    assert result.merge_tree_supported is False
+    assert result.clean is None and result.listing is None
+    assert result.binary_paths == frozenset()
+
+
+def test_parse_probe_clean_shape():
+    result = parse_probe(_probe(**_CLEAN))
+    assert result.clean is True
+    assert result.listing == MergeTreeListing(TREE, ())
+
+
+_BAD_PROBES = {
+    "not-a-dict": ["not", "a", "dict"],
+    "ok-false": _probe(ok=False),
+    "ok-truthy": _probe(ok=1),
+    "mode-ops": _probe(mode="ops"),
+    "truncated-true": _probe(truncated=True),
+    "truncated-missing": _without("truncated"),
+    "supported-not-bool": _probe(merge_tree_supported="yes"),
+    "base-ref-empty": _probe(base_ref=""),
+    "base-ref-non-string": _probe(base_ref=3),
+    "base-sha-short": _probe(base_sha="a" * 39),
+    "head-sha-nonhex": _probe(head_sha="z" * 40),
+    "head-sha-trailing-newline": _probe(head_sha=SHA_B + "\n"),
+    "merge-base-missing": _without("merge_base"),
+    "behind-negative": _probe(behind=-1),
+    "ahead-bool": _probe(ahead=True),
+    "behind-str": _probe(behind="3"),
+    "foreign-op-unknown": _probe(foreign_op="bisect"),
+    "foreign-op-missing": _without("foreign_op"),
+    "merge-head-bad": _probe(merge_head="abc"),
+    "tree-clean-not-bool": _probe(tree_clean="true"),
+    "tree-clean-disagrees": _probe(tree_clean=True, status_b64=_b64(" M x\x00")),
+    "status-missing": _without("status_b64"),
+    "status-non-strict-b64": _probe(tree_clean=False, status_b64="IE0ge*A="),
+    "status-missing-padding": _probe(tree_clean=False, status_b64="IE0geAA"),
+    "merge-tree-b64-junk": _probe(merge_tree_b64="!!!!"),
+    "merge-tree-b64-null": _probe(merge_tree_b64=None),
+    "merge-tree-not-utf8": _probe(
+        merge_tree_b64=base64.b64encode(b"\xff\xfe").decode()
+    ),
+    "merge-tree-bad-records": _probe(
+        merge_tree_b64=_b64(TREE + "\x00100644 bad 1\tx\0\0")
+    ),
+    "numstat-ours-missing": _without("numstat_ours_b64"),
+    "numstat-theirs-malformed": _probe(numstat_theirs_b64=_b64("x\ty\tz\x00")),
+    "programs-not-list": _probe(programs="uv"),
+    "programs-non-string": _probe(programs=["uv", 1]),
+    "clean-not-bool": _probe(clean="false"),
+    "clean-missing": _without("clean"),
+    "clean-with-records": _probe(clean=True),
+    "conflicting-without-records": _probe(merge_tree_b64=_b64(TREE + "\0")),
+    "unsupported-clean-not-null": _probe(**{**_UNSUPPORTED, "clean": False}),
+    "unsupported-listing-not-null": _probe(
+        **{**_UNSUPPORTED, "merge_tree_b64": _b64(TREE + "\0")}
+    ),
+    "unsupported-numstat-missing": {
+        k: v for k, v in _probe(**_UNSUPPORTED).items() if k != "numstat_ours_b64"
+    },
+    "oversize-field": _probe(
+        merge_tree_b64=_b64(TREE + "\0" + "x" * c.MAX_PROBE_BYTES)
+    ),
+}
+
+
+@pytest.mark.parametrize("payload", list(_BAD_PROBES.values()), ids=list(_BAD_PROBES))
+def test_parse_probe_rejects_invalid(payload):
+    with pytest.raises(ValueError):
+        parse_probe(payload)
+
+
+# ---------------------------------------------------------------------------
+# Classify
+# ---------------------------------------------------------------------------
+
+
+def _entry(path, stages="123", *, mode="100644", modes=None, binary=False):
+    sides = {"base": "1", "ours": "2", "theirs": "3"}
+    if modes is None:
+        modes = {side: (mode if num in stages else None) for side, num in sides.items()}
+    oids = {side: (OID if num in stages else None) for side, num in sides.items()}
+    return ConflictEntry(
+        path=path, stages=stages, modes=modes, oids=oids, binary=binary
+    )
+
+
+UV = frozenset({"uv"})
+
+
+@pytest.mark.parametrize(
+    "entry, programs, expected",
+    [
+        # rule 0
+        pytest.param(_entry("a\nb.txt"), UV, "halt:unsafe_path", id="r0-newline"),
+        pytest.param(_entry("a\tb.txt"), UV, "halt:unsafe_path", id="r0-tab"),
+        pytest.param(_entry("a\x7fb.txt"), UV, "halt:unsafe_path", id="r0-del"),
+        # rule 1
+        pytest.param(
+            _entry("vendor/lib", mode="160000"), UV, "halt:submodule", id="r1"
+        ),
+        # rule 2
+        pytest.param(_entry("link", mode="120000"), UV, "halt:symlink", id="r2"),
+        # rule 3
+        pytest.param(
+            _entry(
+                "run.sh", modes={"base": "100644", "ours": "100755", "theirs": "100644"}
+            ),
+            UV,
+            "halt:mode_change",
+            id="r3",
+        ),
+        # rule 4
+        pytest.param(
+            _entry(".github/workflows/ci.yml"), UV, "halt:protected", id="r4-workflows"
+        ),
+        pytest.param(
+            _entry(".github/actions/a/x.yml"), UV, "halt:protected", id="r4-actions"
+        ),
+        pytest.param(
+            _entry(".claude/settings.json"), UV, "halt:protected", id="r4-settings"
+        ),
+        pytest.param(
+            _entry(".claude/settings.local.json"), UV, "halt:protected", id="r4-local"
+        ),
+        # rule 5
+        pytest.param(
+            _entry("app/migrations/0001.py"), UV, "halt:migration", id="r5-migrations"
+        ),
+        pytest.param(
+            _entry("alembic/versions/x.py"), UV, "halt:migration", id="r5-alembic"
+        ),
+        pytest.param(
+            _entry("db/migrate/2026_x.rb"), UV, "halt:migration", id="r5-db-migrate"
+        ),
+        # rule 6
+        pytest.param(_entry("img.png", binary=True), UV, "halt:binary", id="r6"),
+        # rule 7
+        pytest.param(_entry("uv.lock"), UV, "regen:uv.lock", id="r7-root-uv-lock"),
+        # rule 8
+        pytest.param(
+            _entry("package-lock.json"), UV, "halt:lockfile_no_recipe", id="r8-npm"
+        ),
+        pytest.param(
+            _entry("Cargo.lock"), UV, "halt:lockfile_no_recipe", id="r8-cargo"
+        ),
+        pytest.param(
+            _entry("x/custom.lock"), UV, "halt:lockfile_no_recipe", id="r8-dot-lock"
+        ),
+        # rule 9
+        pytest.param(
+            _entry("generated/api.py"), UV, "halt:generated_no_recipe", id="r9-seg"
+        ),
+        pytest.param(
+            _entry("web/dist/app.js"), UV, "halt:generated_no_recipe", id="r9-dist"
+        ),
+        pytest.param(
+            _entry("build/out.txt"), UV, "halt:generated_no_recipe", id="r9-build"
+        ),
+        pytest.param(
+            _entry("src/api.generated.ts"), UV, "halt:generated_no_recipe", id="r9-gen"
+        ),
+        pytest.param(
+            _entry("tests/x.snap"), UV, "halt:generated_no_recipe", id="r9-snap"
+        ),
+        # rule 10
+        pytest.param(_entry("src/a.py"), UV, "text:content", id="r10"),
+        # rule 11
+        pytest.param(_entry("src/a.py", "12"), UV, "text:modify_delete", id="r11-12"),
+        pytest.param(_entry("src/a.py", "13"), UV, "text:modify_delete", id="r11-13"),
+        # rule 12
+        pytest.param(_entry("src/a.py", "23"), UV, "text:add_add", id="r12"),
+        # rule 13
+        pytest.param(
+            _entry("src/a.py", "2"), UV, "halt:unknown_shape", id="r13-stage-2-only"
+        ),
+        pytest.param(
+            _entry("src/a.py", "1"), UV, "halt:unknown_shape", id="r13-stage-1-only"
+        ),
+        # boundaries (section 12.1)
+        pytest.param(
+            _entry("sub", mode="160000", binary=True),
+            UV,
+            "halt:submodule",
+            id="b-submodule-beats-binary",
+        ),
+        pytest.param(
+            _entry(".github/workflows/x.yml", "12"),
+            UV,
+            "halt:protected",
+            id="b-protected-beats-text",
+        ),
+        pytest.param(
+            _entry("uv.lock", "12"), UV, "halt:lockfile_no_recipe", id="b-uv-lock-12"
+        ),
+        pytest.param(
+            _entry("uv.lock", "13"), UV, "halt:lockfile_no_recipe", id="b-uv-lock-13"
+        ),
+        pytest.param(
+            _entry("pkg/uv.lock"), UV, "halt:lockfile_no_recipe", id="b-pkg-uv-lock"
+        ),
+        pytest.param(
+            _entry("uv.lock"),
+            frozenset(),
+            "halt:lockfile_no_recipe",
+            id="b-root-uv-lock-no-uv",
+        ),
+        pytest.param(
+            _entry("__snapshots__/x.snap"),
+            UV,
+            "halt:generated_no_recipe",
+            id="b-snapshots",
+        ),
+        pytest.param(_entry("a\tb.py"), UV, "halt:unsafe_path", id="b-path-with-tab"),
+        pytest.param(
+            _entry("uv.lock", binary=True), UV, "halt:binary", id="b-binary-beats-regen"
+        ),
+    ],
+)
+def test_classify_path_rules(entry, programs, expected):
+    result = classify_path(entry, programs=programs)
+    assert result.cls == expected
+    assert result.path == entry.path
+    assert result.stages == entry.stages
+    assert result.reason
+
+
+@pytest.mark.parametrize(
+    "entry",
+    [
+        pytest.param("not an entry", id="non-entry"),
+        pytest.param(None, id="none"),
+        pytest.param(
+            ConflictEntry(path=5, stages="123", modes={}, oids={}, binary=False),  # type: ignore[arg-type]
+            id="non-string-path",
+        ),
+        pytest.param(_entry("a.py", "321"), id="unsorted-stages"),
+        pytest.param(_entry("a.py", "124"), id="stage-4"),
+        pytest.param(_entry("a.py", ""), id="empty-stages"),
+        pytest.param(
+            ConflictEntry(path="a.py", stages=123, modes={}, oids={}, binary=False),  # type: ignore[arg-type]
+            id="non-string-stages",
+        ),
+        pytest.param(_entry(""), id="empty-path"),
+    ],
+)
+def test_classify_path_unexpected_shape_is_unknown_shape(entry):
+    assert classify_path(entry, programs=UV).cls == "halt:unknown_shape"
+
+
+def test_classify_regen_needs_every_program_of_the_rule():
+    rule = c.MechanicalRule(
+        "gen.lock", "lockfile", ("src",), ("uv", "lock"), ("make", "check")
+    )
+    only_uv = classify_path(_entry("gen.lock"), programs=UV, rules=(rule,))
+    assert only_uv.cls == "halt:lockfile_no_recipe"
+    both = classify_path(
+        _entry("gen.lock"), programs=frozenset({"uv", "make"}), rules=(rule,)
+    )
+    assert both.cls == "regen:gen.lock"
+
+
+def test_shipped_mechanical_rules():
+    assert MECHANICAL_RULES == (
+        c.MechanicalRule(
+            "uv.lock",
+            "lockfile",
+            ("pyproject.toml",),
+            ("uv", "lock"),
+            ("uv", "lock", "--check"),
+        ),
+    )
+
+
+# ---------------------------------------------------------------------------
+# Plan
+# ---------------------------------------------------------------------------
+
+
+def _conflict_probe(entries, programs=("uv",)):
+    """A conflicting probe from (path, stages, binary) triples."""
+    parts = [TREE]
+    for path, stages, _binary in entries:
+        parts.extend(f"100644 {OID} {s}\t{path}" for s in stages)
+    listing = "\0".join(parts) + "\0\0"
+    binary = "".join(f"-\t-\t{p}\x00" for p, _s, b in entries if b)
+    text = "".join(f"1\t1\t{p}\x00" for p, _s, b in entries if not b)
+    return _probe(
+        merge_tree_b64=_b64(listing),
+        numstat_ours_b64=_b64(binary + text),
+        numstat_theirs_b64=_b64(text),
+        programs=list(programs),
+    )
+
+
+@pytest.mark.parametrize(
+    "hint, reason",
+    [("clean", "no_conflict"), ("behind", "behind_only"), ("blocked", "blocked")],
+)
+def test_plan_tier0_hint_rows_run_no_probe(hint, reason):
+    plan = conflict_plan(hint=hint, probe=None)
+    assert (plan.tier, plan.reason, plan.hint) == (0, reason, hint)
+    assert plan.github_conflicting is False
+    assert plan.paths == () and plan.listing is None and plan.base_sha is None
+
+
+def test_plan_blocked_row_from_merge_state():
+    hint = mergeability_hint("MERGEABLE", "BLOCKED")
+    plan = conflict_plan(hint=hint, probe=None)
+    assert (plan.tier, plan.reason) == (0, "blocked")
+
+
+@pytest.mark.parametrize("hint", ["conflicting", "unknown"])
+def test_plan_probe_failed_is_unclassified(hint):
+    plan = conflict_plan(hint=hint, probe=None, probe_failed=True)
+    assert (plan.tier, plan.reason) == (None, "probe_failed")
+    assert plan.github_conflicting is (hint == "conflicting")
+
+
+def test_plan_merge_tree_unsupported_is_unclassified():
+    plan = conflict_plan(hint="conflicting", probe=_probe(**_UNSUPPORTED))
+    assert (plan.tier, plan.reason) == (None, "merge_tree_unsupported")
+    assert (
+        plan.base_sha == SHA_A and plan.merge_tree_oid is None and plan.listing is None
+    )
+
+
+@pytest.mark.parametrize(
+    "probe",
+    [
+        pytest.param(None, id="missing-probe-with-probe-hint"),
+        pytest.param(_probe(truncated=True), id="truncated"),
+        pytest.param(_probe(status_b64="***"), id="bad-b64"),
+        pytest.param(_probe(merge_tree_b64=_b64("nottree\0")), id="bad-listing"),
+        pytest.param(_probe(behind=-2), id="invalid-field"),
+        pytest.param("junk", id="non-dict"),
+    ],
+)
+def test_plan_malformed_probe_is_tier3(probe):
+    plan = conflict_plan(hint="conflicting", probe=probe)
+    assert (plan.tier, plan.reason) == (3, "probe_malformed")
+
+
+def test_plan_junk_hint_is_tier3():
+    assert conflict_plan(hint="junk", probe=None).tier == 3
+    assert conflict_plan(hint=None, probe=None).tier == 3  # type: ignore[arg-type]
+
+
+def test_plan_clean_probe_is_tier0_and_flags_github_disagreement():
+    plan = conflict_plan(hint="conflicting", probe=_probe(**_CLEAN))
+    assert (plan.tier, plan.reason) == (0, "no_conflict")
+    assert plan.github_conflicting is True
+    assert plan.merge_tree_oid == TREE and plan.behind == 3
+    assert (
+        conflict_plan(hint="unknown", probe=_probe(**_CLEAN)).github_conflicting
+        is False
+    )
+
+
+def test_plan_captured_fixture_is_tier2():
+    plan = conflict_plan(hint="conflicting", probe=_probe())
+    assert (plan.tier, plan.reason) == (2, "text_conflict")
+    assert [(p.path, p.cls) for p in plan.paths] == [
+        ("d.txt", "text:modify_delete"),
+        ("f.txt", "text:content"),
+    ]
+    assert plan.text_paths == ("d.txt", "f.txt")
+    assert plan.regen_paths == ()
+    assert plan.merge_tree_oid == TREE
+    assert (plan.base_sha, plan.head_sha) == (SHA_A, SHA_B)
+    assert plan.listing is not None and len(plan.listing.records) == 5
+
+
+def test_plan_halt_class_is_tier3_with_first_halt_reason():
+    entries = [
+        ("a.py", "123", False),
+        ("img.png", "123", True),
+        ("uv.lock", "12", False),
+    ]
+    plan = conflict_plan(hint="conflicting", probe=_conflict_probe(entries))
+    assert (plan.tier, plan.reason) == (3, "halt:binary")
+
+
+def test_plan_eight_text_paths_is_tier2():
+    entries = [(f"src/f{i}.py", "123", False) for i in range(8)]
+    plan = conflict_plan(hint="conflicting", probe=_conflict_probe(entries))
+    assert (plan.tier, plan.reason) == (2, "text_conflict")
+    assert len(plan.text_paths) == 8
+
+
+def test_plan_nine_text_paths_is_tier3_too_many_files():
+    entries = [(f"src/f{i}.py", "123", False) for i in range(9)]
+    plan = conflict_plan(hint="conflicting", probe=_conflict_probe(entries))
+    assert (plan.tier, plan.reason) == (3, "too_many_files")
+
+
+def test_plan_regen_plus_text_is_tier2_and_regen_not_counted():
+    entries = [("uv.lock", "123", False)] + [
+        (f"src/f{i}.py", "123", False) for i in range(8)
+    ]
+    plan = conflict_plan(hint="conflicting", probe=_conflict_probe(entries))
+    assert (plan.tier, plan.reason) == (2, "text_conflict")
+    assert plan.regen_paths == ("uv.lock",)
+    assert len(plan.text_paths) == 8
+
+
+def test_plan_regen_only_is_tier1():
+    plan = conflict_plan(
+        hint="unknown", probe=_conflict_probe([("uv.lock", "123", False)])
+    )
+    assert (plan.tier, plan.reason) == (1, "regen_only")
+    assert plan.regen_paths == ("uv.lock",) and plan.text_paths == ()
+
+
+def test_plan_regen_without_program_is_tier3():
+    probe = _conflict_probe([("uv.lock", "123", False)], programs=())
+    plan = conflict_plan(hint="conflicting", probe=probe)
+    assert (plan.tier, plan.reason) == (3, "halt:lockfile_no_recipe")
+
+
+def test_plan_tier2_max_files_override_and_invalid():
+    probe = _conflict_probe([(f"src/f{i}.py", "123", False) for i in range(3)])
+    assert conflict_plan(hint="conflicting", probe=probe, tier2_max_files=2).reason == (
+        "too_many_files"
+    )
+    bad = conflict_plan(hint="conflicting", probe=probe, tier2_max_files="8")  # type: ignore[arg-type]
+    assert (bad.tier, bad.reason) == (3, "probe_malformed")
+
+
+def test_plan_never_raises_on_bad_rules():
+    probe = _conflict_probe([("uv.lock", "123", False)])
+    plan = conflict_plan(hint="conflicting", probe=probe, rules="junk")  # type: ignore[arg-type]
+    assert plan.tier == 3
+
+
+# ---------------------------------------------------------------------------
+# Purity
+# ---------------------------------------------------------------------------
+
+_ALLOWED_STDLIB = {"base64", "re", "dataclasses", "typing"}
+_ALLOWED_INTERNAL = {"models": {"MonitorState"}, "fsm": {"run_validation_gates"}}
+
+
+def test_conflicts_imports_only_allowed_modules():
+    tree = ast.parse(CONFLICTS_PY.read_text(encoding="utf-8"))
+    offenders: list[str] = []
+    for node in ast.walk(tree):
+        if isinstance(node, ast.Import):
+            for alias in node.names:
+                if alias.name.split(".")[0] not in _ALLOWED_STDLIB:
+                    offenders.append(f"import {alias.name}")
+        elif isinstance(node, ast.ImportFrom):
+            if node.level == 0:
+                if (node.module or "").split(".")[0] not in _ALLOWED_STDLIB:
+                    offenders.append(f"from {node.module} import ...")
+            else:
+                allowed = _ALLOWED_INTERNAL.get(node.module or "")
+                names = {a.name for a in node.names}
+                if node.level != 1 or allowed is None or not names <= allowed:
+                    offenders.append(
+                        f"from {'.' * node.level}{node.module} import {names}"
+                    )
+    assert not offenders, offenders
+
+
+def test_conflicts_makes_no_io_or_dynamic_calls():
+    tree = ast.parse(CONFLICTS_PY.read_text(encoding="utf-8"))
+    banned = {"open", "__import__", "exec", "eval", "compile", "input", "print"}
+    called = {
+        node.func.id
+        for node in ast.walk(tree)
+        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
+    }
+    assert not (called & banned)
diff --git a/tests/pr_submit/fixtures/merge_tree_conflict.z b/tests/pr_submit/fixtures/merge_tree_conflict.z
new file mode 100644
index 00000000..89b8742d
Binary files /dev/null and b/tests/pr_submit/fixtures/merge_tree_conflict.z differ
diff --git a/tests/pr_submit/test_static_grep.py b/tests/pr_submit/test_static_grep.py
index 251905d6..b9a53820 100644
--- a/tests/pr_submit/test_static_grep.py
+++ b/tests/pr_submit/test_static_grep.py
@@ -48,6 +48,8 @@ CORE_PURE_FILES = [
     PR_SUBMIT_PKG / "severity_router.py",
     PR_SUBMIT_PKG / "loop_guard.py",
     PR_SUBMIT_PKG / "ci.py",
+    # issue #305: the conflict core is pure (no version-control tokens)
+    PR_SUBMIT_PKG / "conflicts.py",
 ]
 
 AUGGIE_REVIEW_CMD = REPO_ROOT / "src" / "superclaude" / "commands" / "auggie-review.md"
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t3-tests.log b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t3-tests.log
new file mode 100644
index 00000000..8574ac38
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t3-tests.log
@@ -0,0 +1,17 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 333 items
+
+tests/pr_submit/test_conflicts_core.py ................................. [  9%]
+........................................................................ [ 31%]
+........................................................................ [ 53%]
+........................................................................ [ 74%]
+.................................................................        [ 94%]
+tests/pr_submit/test_static_grep.py ...................                  [100%]
+
+============================= 333 passed in 1.00s ==============================

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
