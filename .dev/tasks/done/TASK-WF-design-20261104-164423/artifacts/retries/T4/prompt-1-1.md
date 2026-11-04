6398d3f75b6a801a6f83c3f0d3440e5dfb515e18
Review one task for spec compliance.

Task brief: ## Task 4: Add routing, gates, records, messages and resume planners to `conflicts.py`

Depends on: Task 3

Extend `src/superclaude/pr_submit/conflicts.py` with the remaining functions of source section 5.3 and their tests in `tests/pr_submit/test_conflicts_core.py`:

- `conflict_action` with the domain guard, the L0 row and every row of the `wave0`, `c_initial` and `wave8a` tables of source section 4.4 (including `tier1_l1_preserved` and `tier1_l2_preserved`).
- `merge_preflight_ok`, `merge_parent_ok`, `evaluate_sync_decision`, `sync_fail_state`, `conflict_validation_status`, `conflict_cycle_id`, `is_conflict_cycle`, `prior_conflict_cycles`, `finish_manifest`, `parse_resolution_record`, `resolution_record_ok`, `merge_commit_message`.
- `crash_resume_plan` (source section 4.8 second table, plus the `sync` / `ci` rules below it) and `conflict_resume_plan` (source section 4.8 first table in evaluation order: rows 1, 2, 3, 3b, 4c, 4, 4b, 4b', 5, 6, 7, 8, with the closing rule and the `prior_conflict_cycles` rule). Both are pure: they append nothing.
- Tests: the Router, Gates, Cycle ids, Record and message, and Resume cases of source section 12.1 (resume tests build `state` dicts directly; the run-log integration is Task 8). Include the ordinal-monotonicity property exactly as stated in source section 4.4, the `c_initial` default-row assertion, the Wave 8a Tier 1 preserved column, the `merge_parent_ok` matrix and the disjointness property with `fsm.push_parent_ok`, the `evaluate_sync_decision` truth tables and cross-gate property, the branch-literal equality with `recovery.BRANCH_A_LANDED` / `BRANCH_B_NOT_LANDED` / `BRANCH_C_AMBIGUOUS`, and `REPORT_REASONS & HALT_REASONS` equal to the eight-reason set of source section 5.2.

Acceptance criteria:
- Every reachable router row is asserted against a literal expected table; every domain violation returns `ConflictAction("halt", "router_unreachable", "terminal_halted", skip_ci=True)`.
- The monotonicity property passes over the full product of in-domain inputs for hooks `wave0` and `wave8a`.
- `merge_parent_ok` accepts only `[pre_push_sha, base_sha]` in that order with distinct 40-hex ids; `push_parent_ok` is false for every list `merge_parent_ok` accepts.
- `conflict_resume_plan` returns the source section 4.8 directive for each row, with `cycle_id`, `hook`, `review_terminal`, `target_sha` and `expect_checks` (true when missing) populated as specified; `prior_conflict_cycles(["sync-1"], "sync-1") == 0`.
- `uv run pytest tests/pr_submit/test_conflicts_core.py -q` passes; log saved to `./artifacts/t4-tests.log`.
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
Start sha: 6398d3f75b6a801a6f83c3f0d3440e5dfb515e18
Diff against the start snapshot: diff --git a/src/superclaude/pr_submit/conflicts.py b/src/superclaude/pr_submit/conflicts.py
index a13177da..414c7521 100644
--- a/src/superclaude/pr_submit/conflicts.py
+++ b/src/superclaude/pr_submit/conflicts.py
@@ -1,7 +1,10 @@
 """The pure merge-conflict core for sc:pr-submit (issue #305, design section 5).
 
 This module parses the read-only probe output, classifies every conflicted path
-into a tier and builds the conflict plan the SKILL reports before any edit.
+into a tier and builds the conflict plan the SKILL reports before any edit. It also
+holds the only conflict routing decision (``conflict_action``), the merge and sync
+gates, the validation status, cycle ids, the resolution record and commit message
+helpers, and the two pure resume planners.
 
 Module rules (design section 5.1):
 
@@ -22,6 +25,7 @@ import base64
 import re
 from dataclasses import dataclass
 
+from .fsm import run_validation_gates
 from .models import MonitorState
 
 # ---------------------------------------------------------------------------
@@ -787,3 +791,760 @@ def conflict_plan(
     if all(pc.cls.startswith("regen:") for pc in classes):
         return _plan(hint, 1, "regen_only", probe=parsed, paths=classes)
     return _plan(hint, 3, "probe_malformed")
+
+
+# ---------------------------------------------------------------------------
+# Routing (design section 4.4)
+# ---------------------------------------------------------------------------
+
+DEFAULT_ACTION = ConflictAction(
+    "halt", "router_unreachable", "terminal_halted", skip_ci=True
+)
+# Plan reasons the router may echo back: tier None at every hook, tier 0 at wave0.
+_ECHO_PLAN_REASONS: dict[int | None, frozenset[str]] = {
+    None: frozenset({"probe_failed", "merge_tree_unsupported"}),
+    0: frozenset({"no_conflict", "behind_only", "blocked"}),
+}
+
+
+def _is_int(value: object) -> bool:
+    return isinstance(value, int) and not isinstance(value, bool)
+
+
+def _router_domain_ok(
+    hook: object,
+    plan_tier: object,
+    ordinal: object,
+    entering: object,
+    conflict_max_tier: object,
+    round_counter: object,
+    max_rounds: object,
+    prior_conflict_cycles: object,
+    github_conflicting: object,
+    plan_reason: object,
+) -> bool:
+    if hook not in HOOKS:
+        return False
+    if not (_is_int(ordinal) and 0 <= ordinal <= 3):
+        return False
+    if not (_is_int(conflict_max_tier) and 0 <= conflict_max_tier <= 2):
+        return False
+    if not (plan_tier is None or (_is_int(plan_tier) and 0 <= plan_tier <= 3)):
+        return False
+    if not all(
+        _is_nonneg_int(v) for v in (round_counter, max_rounds, prior_conflict_cycles)
+    ):
+        return False
+    if not isinstance(github_conflicting, bool):
+        return False
+    if hook == "wave8a":
+        if entering not in ENTERING_OUTCOMES:
+            return False
+    elif entering is not None:
+        return False
+    if hook == "c_initial" and ordinal != 3:
+        return False
+    echoed = plan_tier is None or (plan_tier == 0 and hook == "wave0")
+    if echoed and plan_reason not in _ECHO_PLAN_REASONS[plan_tier]:
+        return False
+    return True
+
+
+def _route_wave0(plan_tier: int | None, ordinal: int, cap: int, reason: str):
+    if plan_tier is None or plan_tier == 0:
+        return ConflictAction("report", reason)
+    if plan_tier == 1:
+        if cap < 1:
+            return ConflictAction("report", "tier_above_cap")
+        return ConflictAction("report", "tier1_planned")
+    if plan_tier == 2:
+        if cap < 2:
+            return ConflictAction("report", "tier_above_cap")
+        if ordinal < 3:
+            return ConflictAction("report", "tier2_report_only")
+        return ConflictAction("report", "tier2_planned")
+    if ordinal < 3:
+        return ConflictAction("report", "conflict_tier3")
+    return ConflictAction("halt", "conflict_tier3", "terminal_halted")
+
+
+def _route_c_initial(
+    plan_tier: int | None,
+    cap: int,
+    round_counter: int,
+    max_rounds: int,
+    prior: int,
+    reason: str,
+):
+    if plan_tier is None:
+        return ConflictAction("report", reason)
+    if plan_tier == 0:
+        return ConflictAction("none", "no_conflict")
+    if plan_tier == 1:
+        return ConflictAction("none", "tier1_deferred")
+    if plan_tier == 2:
+        if cap < 2:
+            return ConflictAction("report", "tier_above_cap")
+        if max_rounds - round_counter < 2:
+            return ConflictAction("report", "no_round_budget")
+        if prior >= SYNC_CAP:
+            return ConflictAction("report", "sync_cap")
+        return ConflictAction(
+            "resolve_push", "tier2_merge", fsm_event="conflicting", push_kind="merge"
+        )
+    return ConflictAction("halt", "conflict_tier3", "terminal_halted")
+
+
+def _route_wave8a(
+    plan_tier: int | None,
+    ordinal: int,
+    entering: str,
+    cap: int,
+    prior: int,
+    github_conflicting: bool,
+    reason: str,
+):
+    preserved = entering in PRESERVED_OUTCOMES
+    status = None if preserved else "terminal_halted"
+    stop = "report" if preserved else "halt"
+
+    def end(why: str) -> ConflictAction:
+        return ConflictAction(stop, why, status, skip_ci=True)
+
+    if plan_tier is None:
+        return end(reason)
+    if plan_tier == 0:
+        if not github_conflicting:
+            return ConflictAction("none", "no_conflict", skip_ci=False)
+        return end("github_disagrees")
+    if plan_tier == 1:
+        if cap < 1:
+            return end("tier_above_cap")
+        if prior >= SYNC_CAP:
+            return end("sync_cap")
+        if ordinal == 1:
+            if preserved:
+                return ConflictAction("report", "tier1_l1_preserved", skip_ci=True)
+            return ConflictAction("propose", "tier1_proposed", "proposed", skip_ci=True)
+        if ordinal == 2:
+            if preserved:
+                return ConflictAction("report", "tier1_l2_preserved", skip_ci=True)
+            return ConflictAction(
+                "resolve_local", "tier1_local", "halt_before_push", skip_ci=True
+            )
+        return ConflictAction("resolve_push", "tier1_sync", push_kind="sync")
+    if plan_tier == 2:
+        if cap < 2:
+            return end("tier_above_cap")
+        return end("late_conflict")
+    return end("conflict_tier3")
+
+
+def conflict_action(
+    *,
+    hook: str,
+    plan_tier: int | None,
+    ordinal: int,
+    entering: str | None,
+    conflict_max_tier: int,
+    round_counter: int,
+    max_rounds: int,
+    prior_conflict_cycles: int,
+    github_conflicting: bool,
+    plan_reason: str = "",
+) -> ConflictAction:
+    """The only conflict routing decision (design section 4.4). Never raises.
+
+    The domain guard runs first: any input outside its domain (including a plan
+    reason this router would echo that is not a plan reason of that tier) gives
+    ``DEFAULT_ACTION``. Then ordinal 0 gives ``ConflictAction("none", "l0")``, and
+    the hook's table decides, rows top to bottom. ``prior_conflict_cycles`` is
+    ``prior_conflict_cycles(conflict_cycles, cycle_id)``.
+    """
+    if not _router_domain_ok(
+        hook,
+        plan_tier,
+        ordinal,
+        entering,
+        conflict_max_tier,
+        round_counter,
+        max_rounds,
+        prior_conflict_cycles,
+        github_conflicting,
+        plan_reason,
+    ):
+        return DEFAULT_ACTION
+    if ordinal == 0:
+        return ConflictAction("none", "l0")
+    if hook == "wave0":
+        return _route_wave0(plan_tier, ordinal, conflict_max_tier, plan_reason)
+    if hook == "c_initial":
+        return _route_c_initial(
+            plan_tier,
+            conflict_max_tier,
+            round_counter,
+            max_rounds,
+            prior_conflict_cycles,
+            plan_reason,
+        )
+    return _route_wave8a(
+        plan_tier,
+        ordinal,
+        entering,  # type: ignore[arg-type]
+        conflict_max_tier,
+        prior_conflict_cycles,
+        github_conflicting,
+        plan_reason,
+    )
+
+
+# ---------------------------------------------------------------------------
+# Gates (design section 5.3)
+# ---------------------------------------------------------------------------
+
+_HEX40_ANY_CASE = re.compile(r"[0-9a-fA-F]{40}")
+_STATUS_CODES = frozenset(" MTADRCU?!")
+_UNPARSABLE_STATUS = "<unparsable status>"
+
+
+def _is_sha(value: object) -> bool:
+    return isinstance(value, str) and _HEX40_ANY_CASE.fullmatch(value) is not None
+
+
+def merge_preflight_ok(porcelain: object) -> tuple[bool, list[str]]:
+    """Whether the tracked tree is clean before the merge (untracked files tolerated).
+
+    ``porcelain`` is the decoded NUL-separated porcelain v1 status listing, taken
+    without untracked files. ``(True, [])`` for the empty string; otherwise
+    ``(False, paths)`` naming every path (both paths of a rename or copy record).
+    A ``??`` record is ignored. A non-string, or a record that cannot be parsed,
+    gives ``(False, ["<unparsable status>"])``.
+    """
+    if not isinstance(porcelain, str):
+        return False, [_UNPARSABLE_STATUS]
+    if porcelain == "":
+        return True, []
+    if not porcelain.endswith("\0"):
+        return False, [_UNPARSABLE_STATUS]
+    fields = porcelain[:-1].split("\0")
+    paths: list[str] = []
+    i = 0
+    while i < len(fields):
+        record = fields[i]
+        i += 1
+        if len(record) < 4 or record[2] != " ":
+            return False, [_UNPARSABLE_STATUS]
+        code, path = record[:2], record[3:]
+        if not set(code) <= _STATUS_CODES or code == "  ":
+            return False, [_UNPARSABLE_STATUS]
+        if code == "??":
+            continue
+        paths.append(path)
+        if "R" in code or "C" in code:
+            if i >= len(fields) or fields[i] == "":
+                return False, [_UNPARSABLE_STATUS]
+            paths.append(fields[i])
+            i += 1
+    if not paths:
+        return True, []
+    return False, paths
+
+
+def merge_parent_ok(
+    target_parents: list[str] | None, pre_push_sha: str | None, base_sha: str | None
+) -> bool:
+    """Whether the commit to push is exactly the merge of the base tip into the PR head.
+
+    True iff ``target_parents`` is a list of exactly two full 40-hex ids, the first
+    equal to ``pre_push_sha`` and the second to ``base_sha`` (case-insensitive), and
+    ``pre_push_sha != base_sha``. Disjoint from ``fsm.push_parent_ok`` by parent count.
+    """
+    if not isinstance(target_parents, list) or len(target_parents) != 2:
+        return False
+    ids = (target_parents[0], target_parents[1], pre_push_sha, base_sha)
+    if not all(_is_sha(v) for v in ids):
+        return False
+    first, second, pre, base = (v.lower() for v in ids)  # type: ignore[union-attr]
+    return first == pre and second == base and pre != base
+
+
+def evaluate_sync_decision(
+    *,
+    monitor_ordinal: int,
+    validation_status: str,
+    tier: int,
+    conflict_max_tier: int,
+    halt_reason: str | None,
+    prior_conflict_cycles: int,
+    round_counter: int,
+    max_rounds: int,
+) -> SyncDecision:
+    """The four-predicate conflict push gate (design section 5.3).
+
+    ``p1`` ordinal at least 3; ``p2`` validated; ``p3`` tier 1 or 2, within the cap
+    and no halt reason; ``p4`` under ``SYNC_CAP`` (earlier cycles, the current one
+    excluded) and, for tier 2, ``round_counter < max_rounds``. Non-int inputs make the
+    affected predicate false.
+    """
+    tier_ok = _is_int(tier) and tier in (1, 2)
+    p1 = _is_int(monitor_ordinal) and monitor_ordinal >= 3
+    p2 = validation_status == "validated"
+    p3 = (
+        tier_ok
+        and _is_int(conflict_max_tier)
+        and tier <= conflict_max_tier
+        and halt_reason is None
+    )
+    p4 = _is_nonneg_int(prior_conflict_cycles) and prior_conflict_cycles < SYNC_CAP
+    if p4 and tier_ok and tier == 2:
+        p4 = (
+            _is_nonneg_int(round_counter)
+            and _is_nonneg_int(max_rounds)
+            and round_counter < max_rounds
+        )
+    return SyncDecision(
+        predicate_1_ordinal=p1,
+        predicate_2_validated=p2,
+        predicate_3_tier_allowed=p3,
+        predicate_4_under_cap=p4,
+        authorized=p1 and p2 and p3 and p4,
+        kind="merge" if tier_ok and tier == 2 else "sync",
+    )
+
+
+def sync_fail_state(decision: SyncDecision) -> MonitorState:
+    """Map a blocked ``SyncDecision`` to its fail route; never a push state.
+
+    ``p3`` false: ``HALT_HUMAN``; otherwise ``REPORT_ONLY`` (``p4`` false is reported
+    as ``sync_cap``). A non-``SyncDecision`` gives ``HALT_HUMAN``.
+    """
+    if not isinstance(decision, SyncDecision):
+        return MonitorState.HALT_HUMAN
+    if not decision.predicate_3_tier_allowed:
+        return MonitorState.HALT_HUMAN
+    return MonitorState.REPORT_ONLY
+
+
+def conflict_validation_status(tier: int, results: dict[str, bool]) -> str:
+    """``run_validation_gates(results)``; tier 2 also needs ``VG-2`` green.
+
+    Any tier other than 1 or 2, or a non-dict ``results``, gives ``"failed"``.
+    """
+    if not (_is_int(tier) and tier in (1, 2)) or not isinstance(results, dict):
+        return "failed"
+    status = run_validation_gates(results)
+    if tier == 2 and results.get("VG-2") is not True:
+        return "failed"
+    return status
+
+
+# ---------------------------------------------------------------------------
+# Cycle ids (design sections 4.7 and 4.8)
+# ---------------------------------------------------------------------------
+
+
+def conflict_cycle_id(tier: int, n: int) -> str:
+    """``"sync-<n>"`` for tier 1, ``"conflict-<n>"`` for tier 2; ``ValueError`` otherwise."""
+    if not (_is_int(n) and n >= 1):
+        raise ValueError("cycle number must be an int >= 1")
+    if _is_int(tier) and tier == 1:
+        return f"sync-{n}"
+    if _is_int(tier) and tier == 2:
+        return f"conflict-{n}"
+    raise ValueError("conflict cycles exist only for tier 1 or 2")
+
+
+def is_conflict_cycle(cycle_id: object) -> bool:
+    """True only for a string starting with a reserved conflict-cycle prefix."""
+    return isinstance(cycle_id, str) and cycle_id.startswith(CONFLICT_CYCLE_PREFIXES)
+
+
+def prior_conflict_cycles(conflict_cycles: object, cycle_id: object) -> int:
+    """Distinct string ids in ``conflict_cycles`` other than ``cycle_id``.
+
+    A non-list input returns ``SYNC_CAP`` (fail closed: the cap is treated as reached).
+    """
+    if not isinstance(conflict_cycles, list):
+        return SYNC_CAP
+    return len({c for c in conflict_cycles if isinstance(c, str) and c != cycle_id})
+
+
+# ---------------------------------------------------------------------------
+# Finish manifest, resolution record and commit message (design section 5.3)
+# ---------------------------------------------------------------------------
+
+
+def finish_manifest(listing: MergeTreeListing, resolved_paths: list[str]) -> str:
+    """One ``<stage-1 oid or ->\\t<path>\\n`` line per resolved path, in listing order.
+
+    ``ValueError`` when a resolved path is not in the listing, appears twice, or
+    contains a control character.
+    """
+    if not isinstance(listing, MergeTreeListing):
+        raise ValueError("listing is not a MergeTreeListing")
+    if not isinstance(resolved_paths, (list, tuple)):
+        raise ValueError("resolved_paths is not a list")
+    wanted: set[str] = set()
+    for path in resolved_paths:
+        if not isinstance(path, str) or path == "":
+            raise ValueError("resolved path is not a non-empty string")
+        if _has_control_char(path):
+            raise ValueError(f"resolved path contains a control character: {path!r}")
+        if path in wanted:
+            raise ValueError(f"resolved path appears twice: {path!r}")
+        wanted.add(path)
+    order: list[str] = []
+    base_oid: dict[str, str] = {}
+    for rec in listing.records:
+        if rec.path not in order:
+            order.append(rec.path)
+        if rec.stage == 1:
+            base_oid[rec.path] = rec.oid
+    missing = wanted.difference(order)
+    if missing:
+        raise ValueError(f"resolved path not in the listing: {sorted(missing)!r}")
+    return "".join(f"{base_oid.get(p, '-')}\t{p}\n" for p in order if p in wanted)
+
+
+def parse_resolution_record(text: str) -> dict[str, dict[str, str]]:
+    """Parse ``resolution.md``: ``## <path>`` headings, then ``<field>: <value>`` lines.
+
+    Blank lines are skipped. ``ValueError`` on a duplicate heading, a duplicate
+    field, an unknown field (any other non-blank line), an empty heading, or a field
+    line before the first heading.
+    """
+    if not isinstance(text, str):
+        raise ValueError("record text is not a string")
+    record: dict[str, dict[str, str]] = {}
+    current: dict[str, str] | None = None
+    for line in text.splitlines():
+        if line.strip() == "":
+            continue
+        if line.startswith("## "):
+            path = line[3:].strip()
+            if path == "":
+                raise ValueError("empty heading")
+            if path in record:
+                raise ValueError(f"duplicate heading: {path!r}")
+            current = record[path] = {}
+            continue
+        name, sep, value = line.partition(":")
+        name = name.strip()
+        if current is None:
+            raise ValueError("field line before the first heading")
+        if not sep or name not in RECORD_FIELDS:
+            raise ValueError(f"unknown field: {name!r}")
+        if name in current:
+            raise ValueError(f"duplicate field: {name!r}")
+        current[name] = value.strip()
+    return record
+
+
+_SENTENCE_FIELDS = ("ours_intent", "theirs_intent", "behavior_after")
+_SENTENCE_STOP = re.compile(r"[.!?](?=\s|$)")
+_KEEP_BOTH_ORDER = re.compile(r"keep_both\(\s*\S.*\)")
+
+
+def _one_sentence(value: str) -> bool:
+    if "\n" in value or "\r" in value:
+        return False
+    text = value.strip()
+    return text[-1:] in (".", "!", "?") and len(_SENTENCE_STOP.findall(text)) == 1
+
+
+def resolution_record_ok(
+    record: dict[str, dict[str, str]], text_paths: tuple[str, ...]
+) -> list[str]:
+    """Problems with a parsed resolution record; empty when it is valid (section 5.3)."""
+    if not isinstance(record, dict):
+        return ["record is not a mapping"]
+    if not isinstance(text_paths, (tuple, list)):
+        return ["text paths are not a sequence"]
+    problems: list[str] = []
+    for path in text_paths:
+        if path not in record:
+            problems.append(f"{path}: missing entry")
+    for path, entry in record.items():
+        if path not in text_paths:
+            problems.append(f"{path}: extra entry")
+            continue
+        if not isinstance(entry, dict):
+            problems.append(f"{path}: entry is not a mapping")
+            continue
+        for name in entry:
+            if name not in RECORD_FIELDS:
+                problems.append(f"{path}: unknown field {name}")
+        for name in RECORD_FIELDS:
+            value = entry.get(name)
+            if not isinstance(value, str) or value.strip() == "":
+                problems.append(f"{path}: {name} is missing or empty")
+                continue
+            if name in _SENTENCE_FIELDS and not _one_sentence(value):
+                problems.append(f"{path}: {name} is not exactly one sentence")
+            elif name == "kind":
+                if value == "semantic":
+                    problems.append(f"{path}: kind semantic means Tier 3")
+                elif value not in RECORD_KINDS:
+                    problems.append(f"{path}: unknown kind {value}")
+            elif name == "resolution" and not (
+                value in RECORD_RESOLUTIONS or _KEEP_BOTH_ORDER.fullmatch(value)
+            ):
+                problems.append(f"{path}: unknown resolution {value}")
+    return problems
+
+
+def _one_line(value: object, what: str) -> str:
+    if not isinstance(value, str) or value.strip() == "" or _has_control_char(value):
+        raise ValueError(f"{what} must be a non-empty single-line string")
+    return value
+
+
+def merge_commit_message(
+    *,
+    base_ref: str,
+    head_branch: str,
+    tier: int,
+    rule_patterns: tuple[str, ...] = (),
+    record: dict[str, dict[str, str]] | None = None,
+    lock_changes: str = "",
+) -> str:
+    """The merge commit message without the attribution lines (the SKILL appends them).
+
+    Subject ``Merge <base_ref> into <head_branch> (sc:pr-submit sync, tier <t>)``.
+    Tier 1 body: one line per rule path naming its sources, then ``lock_changes``.
+    Tier 2 body: one line per path with ``kind``, ``resolution`` and ``dropped``.
+    Labels only, never file content. ``ValueError`` on a tier other than 1 or 2, a
+    tier 2 call without a record, or an unknown rule pattern.
+    """
+    subject = (
+        f"Merge {_one_line(base_ref, 'base_ref')} into "
+        f"{_one_line(head_branch, 'head_branch')} (sc:pr-submit sync, tier {tier})"
+    )
+    lines: list[str] = []
+    if _is_int(tier) and tier == 1:
+        if not isinstance(rule_patterns, (tuple, list)) or not isinstance(
+            lock_changes, str
+        ):
+            raise ValueError("rule_patterns must be a tuple and lock_changes a string")
+        rules = {r.pattern: r for r in MECHANICAL_RULES}
+        for pattern in rule_patterns:
+            rule = rules.get(pattern) if isinstance(pattern, str) else None
+            if rule is None:
+                raise ValueError(f"unknown rule pattern: {pattern!r}")
+            lines.append(
+                f"{rule.pattern} regenerated from the merged {', '.join(rule.sources)}"
+            )
+        if lock_changes.strip():
+            lines.append(lock_changes.strip())
+    elif _is_int(tier) and tier == 2:
+        if not isinstance(record, dict) or not record:
+            raise ValueError("a tier 2 merge commit message needs a resolution record")
+        for path, entry in record.items():
+            if not isinstance(entry, dict):
+                raise ValueError(f"record entry for {path!r} is not a mapping")
+            labels = [
+                _one_line(entry.get(k), f"{path} {k}")
+                for k in ("kind", "resolution", "dropped")
+            ]
+            lines.append(
+                f"{_one_line(path, 'path')}: kind {labels[0]}, "
+                f"resolution {labels[1]}, dropped {labels[2]}"
+            )
+    else:
+        raise ValueError("tier must be 1 or 2")
+    if not lines:
+        return subject + "\n"
+    return subject + "\n\n" + "\n".join(lines) + "\n"
+
+
+# ---------------------------------------------------------------------------
+# Resume planners (design section 4.8)
+# ---------------------------------------------------------------------------
+
+_BRANCHES = (BRANCH_LANDED, BRANCH_NOT_LANDED, BRANCH_AMBIGUOUS)
+_RESUME_STATE_KEYS = (
+    "sync_push_count",
+    "conflict_cycles",
+    "open_conflict_cycle",
+    "push_rejected",
+)
+
+
+def _sha_or_none(value: object) -> str | None:
+    return value if _is_sha(value) else None
+
+
+def crash_resume_plan(
+    dangling: dict, branch: str, fsm_state: MonitorState
+) -> ResumePlan:
+    """Map a settled crash window to a resume directive (design section 4.8, table 2).
+
+    ``kind`` is the record's ``kind`` (absent means ``fix``). ``fix`` and ``merge``
+    keep today's states; ``sync`` and ``ci`` re-enter the Wave 8 CI wait and never
+    resume into a push or review state. An unknown branch or kind, or an unusable
+    record, gives ``halt`` / ``resume_unrepresentable``. Pure: appends nothing.
+    """
+    if not isinstance(dangling, dict):
+        return ResumePlan("halt", reason="resume_unrepresentable")
+    raw_kind = dangling.get("kind") or "fix"
+    kind = raw_kind if raw_kind in PUSH_KINDS else None
+    cycle_id = dangling.get("cycle_id")
+    common = {
+        "cycle_id": cycle_id if isinstance(cycle_id, str) else None,
+        "kind": kind,
+        "target_sha": _sha_or_none(dangling.get("target_sha")),
+        "base_sha": _sha_or_none(dangling.get("base_sha")),
+    }
+
+    def halt(reason: str, state: MonitorState | None = None) -> ResumePlan:
+        return ResumePlan("halt", state=state, reason=reason, **common)
+
+    if kind is None or branch not in _BRANCHES:
+        return halt("resume_unrepresentable")
+    if branch == BRANCH_AMBIGUOUS:
+        return halt("ambiguous_remote_tip", MonitorState.HALT_HUMAN)
+    if kind in ("fix", "merge"):
+        if branch == BRANCH_LANDED:
+            if not isinstance(fsm_state, MonitorState):
+                return halt("resume_unrepresentable")
+            return ResumePlan("fsm", state=fsm_state, **common)
+        return ResumePlan(
+            "fsm",
+            state=MonitorState.S4_PUSHING,
+            check_merge_parent=kind == "merge",
+            **common,
+        )
+    review_terminal = dangling.get("review_terminal")
+    if review_terminal not in ENTERING_OUTCOMES or common["target_sha"] is None:
+        return halt("resume_unrepresentable")
+    if kind == "sync" and common["base_sha"] is None:
+        return halt("resume_unrepresentable")
+    expect = dangling.get("expect_checks")
+    wave8 = {
+        "wait_sha": common["target_sha"],
+        "review_terminal": review_terminal,
+        "expect_checks": expect if isinstance(expect, bool) else True,
+    }
+    if branch == BRANCH_LANDED:
+        return ResumePlan("wave8_ci_wait", **common, **wave8)
+    return ResumePlan(
+        "redrive_then_wave8",
+        rerun_guard=True,
+        check_merge_parent=kind == "sync",
+        **common,
+        **wave8,
+    )
+
+
+def conflict_resume_plan(
+    state: dict,
+    *,
+    foreign_op: str | None,
+    merge_head_sha: str | None,
+    local_head_sha: str | None,
+    local_head_parents: list[str] | None,
+    dangling: dict | None,
+) -> ResumePlan:
+    """The ``--resume`` directive for an open conflict cycle (design section 4.8, table 1).
+
+    Rows in table order, first match wins: 1, 2, 3, 3b, 4c, 4, 4b, 4b', 5, 6, 7, 8.
+    Every halt plan that finds an open cycle carries its ``cycle_id`` so the SKILL
+    closes it once; restart rows carry the open cycle's ``cycle_id``, ``hook`` and
+    ``review_terminal``. ``local_head_parents`` never changes the outcome: a local
+    two-parent commit no push record covers still reaches row 8. A ``state``
+    without the run-log keys of design section 6.3 gives ``halt`` /
+    ``resume_unrepresentable``. Pure: the SKILL appends the events the rows name.
+    """
+    unrepresentable = ResumePlan("halt", reason="resume_unrepresentable")
+    if not isinstance(state, dict) or any(k not in state for k in _RESUME_STATE_KEYS):
+        return unrepresentable
+    open_cycle = state["open_conflict_cycle"]
+    if (
+        not isinstance(state["push_rejected"], bool)
+        or not isinstance(state["conflict_cycles"], list)
+        or not _is_nonneg_int(state["sync_push_count"])
+        or not (open_cycle is None or isinstance(open_cycle, dict))
+    ):
+        return unrepresentable
+    cycle_id = open_cycle.get("cycle_id") if open_cycle is not None else None
+    cycle_id = cycle_id if is_conflict_cycle(cycle_id) else None
+
+    def halt(reason: str, **extra: object) -> ResumePlan:
+        return ResumePlan("halt", reason=reason, cycle_id=cycle_id, **extra)  # type: ignore[arg-type]
+
+    # Row 1
+    if state["push_rejected"]:
+        return halt("push_rejected")
+    # Rows 2 and 3
+    if open_cycle is None:
+        if foreign_op is None:
+            return ResumePlan("none")
+        return ResumePlan("halt", reason="foreign_op_in_progress")
+    if cycle_id is None:
+        return unrepresentable
+    # Row 3b
+    if open_cycle.get("superseded") is not False:
+        return halt("resume_unrepresentable")
+    # Row 4c
+    hook = open_cycle.get("hook")
+    review_terminal = open_cycle.get("review_terminal")
+    if (
+        hook not in ("wave8a", "c_initial")
+        or (hook == "wave8a" and review_terminal not in ENTERING_OUTCOMES)
+        or (hook == "c_initial" and review_terminal is not None)
+    ):
+        return halt("resume_unrepresentable")
+    kind = open_cycle.get("kind")
+    kind = kind if kind in ("sync", "merge") else None
+    target_sha = _sha_or_none(open_cycle.get("target_sha"))
+    base_sha = _sha_or_none(open_cycle.get("base_sha"))
+    cycle = {"cycle_id": cycle_id, "hook": hook, "review_terminal": review_terminal}
+    pushed = open_cycle.get("push_completed") is True
+    initiated = open_cycle.get("push_initiated") is True
+    # Row 4
+    if pushed:
+        if kind is None or target_sha is None:
+            return halt("resume_unrepresentable", target_sha=target_sha)
+        expect = open_cycle.get("expect_checks")
+        return ResumePlan(
+            "complete_after_push",
+            state=MonitorState.S5A_RETRIGGER_REVIEW if kind == "merge" else None,
+            kind=kind,
+            wait_sha=target_sha if kind == "sync" else None,
+            target_sha=target_sha,
+            base_sha=base_sha,
+            expect_checks=expect if isinstance(expect, bool) else True,
+            **cycle,
+        )
+    # Rows 4b and 4b'
+    if initiated:
+        if isinstance(dangling, dict) and dangling.get("cycle_id") == cycle_id:
+            return ResumePlan(
+                "crash_window",
+                kind=kind,
+                target_sha=target_sha,
+                base_sha=base_sha,
+                **cycle,
+            )
+        return halt("resume_unrepresentable", target_sha=target_sha)
+    # Row 5
+    if (
+        foreign_op == "MERGE_HEAD"
+        and _is_sha(merge_head_sha)
+        and base_sha is not None
+        and merge_head_sha.lower() == base_sha.lower()  # type: ignore[union-attr]
+    ):
+        return ResumePlan("abort_and_restart", kind=kind, base_sha=base_sha, **cycle)
+    # Row 6
+    if foreign_op is not None:
+        return halt("sync_foreign_operation")
+    # Row 7
+    pre_push_sha = open_cycle.get("pre_push_sha")
+    if (
+        _is_sha(local_head_sha)
+        and _is_sha(pre_push_sha)
+        and local_head_sha.lower() == pre_push_sha.lower()  # type: ignore[union-attr]
+    ):
+        return ResumePlan("restart", kind=kind, base_sha=base_sha, **cycle)
+    # Row 8
+    return halt("resume_unrepresentable")
diff --git a/tests/pr_submit/test_conflicts_core.py b/tests/pr_submit/test_conflicts_core.py
index beaf7e37..7b17541d 100644
--- a/tests/pr_submit/test_conflicts_core.py
+++ b/tests/pr_submit/test_conflicts_core.py
@@ -24,22 +24,28 @@
 # Result: one content conflict f.txt (stages 1/2/3) and one modify/delete d.txt
 # (stages 1/2: deleted on main, modified on pr), captured with git 2.47.3.
 """Pure conflict core tests (design section 5; section 12.1 Hint, Parse, Classify,
-Plan and Purity cases). Task 4 adds the router, gate, record and resume cases."""
+Plan, Router, Gates, Cycle ids, Record and message, Resume and Purity cases)."""
 
 from __future__ import annotations
 
 import ast
 import base64
+import itertools
 from pathlib import Path
 
 import pytest
 
 from superclaude.pr_submit import conflicts as c
+from superclaude.pr_submit import recovery
 from superclaude.pr_submit.conflicts import (
+    DEFAULT_ACTION,
     MECHANICAL_RULES,
+    ConflictAction,
     ConflictEntry,
     MergeTreeListing,
+    ResumePlan,
     StageRecord,
+    SyncDecision,
     classify_path,
     conflict_plan,
     group_entries,
@@ -49,6 +55,8 @@ from superclaude.pr_submit.conflicts import (
     parse_probe,
     parse_stage_records,
 )
+from superclaude.pr_submit.fsm import evaluate_push_decision, push_parent_ok
+from superclaude.pr_submit.models import MonitorState
 
 FIXTURE = Path(__file__).parent / "fixtures" / "merge_tree_conflict.z"
 CONFLICTS_PY = (
@@ -811,6 +819,1443 @@ def test_plan_never_raises_on_bad_rules():
     assert plan.tier == 3
 
 
+# ---------------------------------------------------------------------------
+# Router (design section 4.4)
+# ---------------------------------------------------------------------------
+
+A = ConflictAction
+T = "terminal_halted"
+
+
+def _route(
+    hook,
+    tier,
+    ordinal,
+    *,
+    entering=None,
+    cap=2,
+    rc=0,
+    mr=3,
+    prior=0,
+    gc=True,
+    reason="",
+):
+    return c.conflict_action(
+        hook=hook,
+        plan_tier=tier,
+        ordinal=ordinal,
+        entering=entering,
+        conflict_max_tier=cap,
+        round_counter=rc,
+        max_rounds=mr,
+        prior_conflict_cycles=prior,
+        github_conflicting=gc,
+        plan_reason=reason,
+    )
+
+
+def test_default_action_literal():
+    assert DEFAULT_ACTION == A("halt", "router_unreachable", T, skip_ci=True)
+
+
+# (plan_tier, ordinal, conflict_max_tier, plan_reason, expected)
+_WAVE0_ROWS = [
+    (None, 1, 2, "probe_failed", A("report", "probe_failed")),
+    (None, 3, 2, "probe_failed", A("report", "probe_failed")),
+    (None, 2, 0, "merge_tree_unsupported", A("report", "merge_tree_unsupported")),
+    (0, 1, 2, "no_conflict", A("report", "no_conflict")),
+    (0, 2, 0, "behind_only", A("report", "behind_only")),
+    (0, 3, 1, "blocked", A("report", "blocked")),
+    (1, 1, 0, "", A("report", "tier_above_cap")),
+    (1, 3, 0, "", A("report", "tier_above_cap")),
+    (1, 1, 1, "", A("report", "tier1_planned")),
+    (1, 3, 2, "", A("report", "tier1_planned")),
+    (2, 3, 1, "", A("report", "tier_above_cap")),
+    (2, 1, 2, "", A("report", "tier2_report_only")),
+    (2, 2, 2, "", A("report", "tier2_report_only")),
+    (2, 3, 2, "", A("report", "tier2_planned")),
+    (3, 1, 2, "", A("report", "conflict_tier3")),
+    (3, 2, 0, "", A("report", "conflict_tier3")),
+    (3, 3, 2, "", A("halt", "conflict_tier3", T)),
+    (3, 3, 0, "", A("halt", "conflict_tier3", T)),
+]
+
+
+@pytest.mark.parametrize("tier,ordinal,cap,reason,expected", _WAVE0_ROWS)
+def test_router_wave0_rows(tier, ordinal, cap, reason, expected):
+    assert _route("wave0", tier, ordinal, cap=cap, reason=reason) == expected
+
+
+# (plan_tier, conflict_max_tier, round_counter, max_rounds, prior, plan_reason, expected)
+_C_INITIAL_ROWS = [
+    (None, 2, 0, 3, 0, "probe_failed", A("report", "probe_failed")),
+    (None, 2, 0, 3, 0, "merge_tree_unsupported", A("report", "merge_tree_unsupported")),
+    (0, 2, 0, 3, 0, "no_conflict", A("none", "no_conflict")),
+    (1, 2, 0, 3, 0, "", A("none", "tier1_deferred")),
+    (1, 0, 0, 3, 1, "", A("none", "tier1_deferred")),
+    (2, 1, 0, 3, 0, "", A("report", "tier_above_cap")),
+    (2, 2, 2, 3, 0, "", A("report", "no_round_budget")),
+    (2, 2, 0, 1, 0, "", A("report", "no_round_budget")),
+    (2, 2, 0, 3, 1, "", A("report", "sync_cap")),
+    (
+        2,
+        2,
+        1,
+        3,
+        0,
+        "",
+        A("resolve_push", "tier2_merge", fsm_event="conflicting", push_kind="merge"),
+    ),
+    (3, 2, 0, 3, 0, "", A("halt", "conflict_tier3", T)),
+    (3, 0, 0, 3, 5, "", A("halt", "conflict_tier3", T)),
+]
+
+
+@pytest.mark.parametrize("tier,cap,rc,mr,prior,reason,expected", _C_INITIAL_ROWS)
+def test_router_c_initial_rows(tier, cap, rc, mr, prior, reason, expected):
+    got = _route(
+        "c_initial", tier, 3, cap=cap, rc=rc, mr=mr, prior=prior, reason=reason
+    )
+    assert got == expected
+
+
+# (plan_tier, ordinal, entering, conflict_max_tier, prior, github_conflicting,
+#  plan_reason, expected)
+_WAVE8A_ROWS = [
+    (None, 1, "clean", 2, 0, True, "probe_failed", A("halt", "probe_failed", T, True)),
+    (
+        None,
+        3,
+        "no_response",
+        2,
+        0,
+        True,
+        "merge_tree_unsupported",
+        A("report", "merge_tree_unsupported", None, True),
+    ),
+    (0, 2, "clean", 2, 0, False, "no_conflict", A("none", "no_conflict")),
+    (0, 3, "halt_max_rounds", 0, 1, False, "", A("none", "no_conflict")),
+    (0, 1, "report_only", 2, 0, True, "", A("halt", "github_disagrees", T, True)),
+    (
+        0,
+        1,
+        "halt_max_rounds",
+        2,
+        0,
+        True,
+        "",
+        A("report", "github_disagrees", None, True),
+    ),
+    (1, 3, "clean", 0, 0, True, "", A("halt", "tier_above_cap", T, True)),
+    (1, 3, "no_response", 0, 0, True, "", A("report", "tier_above_cap", None, True)),
+    (1, 3, "clean", 1, 1, True, "", A("halt", "sync_cap", T, True)),
+    (1, 2, "halt_max_rounds", 1, 1, True, "", A("report", "sync_cap", None, True)),
+    (
+        1,
+        1,
+        "halt_max_rounds",
+        1,
+        0,
+        True,
+        "",
+        A("report", "tier1_l1_preserved", None, True),
+    ),
+    (
+        1,
+        1,
+        "no_response",
+        2,
+        0,
+        True,
+        "",
+        A("report", "tier1_l1_preserved", None, True),
+    ),
+    (1, 1, "clean", 1, 0, True, "", A("propose", "tier1_proposed", "proposed", True)),
+    (
+        1,
+        1,
+        "report_only",
+        2,
+        0,
+        True,
+        "",
+        A("propose", "tier1_proposed", "proposed", True),
+    ),
+    (
+        1,
+        2,
+        "halt_max_rounds",
+        1,
+        0,
+        True,
+        "",
+        A("report", "tier1_l2_preserved", None, True),
+    ),
+    (
+        1,
+        2,
+        "clean",
+        1,
+        0,
+        True,
+        "",
+        A("resolve_local", "tier1_local", "halt_before_push", True),
+    ),
+    (1, 3, "clean", 1, 0, True, "", A("resolve_push", "tier1_sync", push_kind="sync")),
+    (
+        1,
+        3,
+        "halt_max_rounds",
+        1,
+        0,
+        False,
+        "",
+        A("resolve_push", "tier1_sync", push_kind="sync"),
+    ),
+    (2, 3, "clean", 1, 0, True, "", A("halt", "tier_above_cap", T, True)),
+    (
+        2,
+        3,
+        "halt_max_rounds",
+        1,
+        0,
+        True,
+        "",
+        A("report", "tier_above_cap", None, True),
+    ),
+    (2, 3, "clean", 2, 0, True, "", A("halt", "late_conflict", T, True)),
+    (2, 1, "no_response", 2, 0, True, "", A("report", "late_conflict", None, True)),
+    (3, 3, "clean", 2, 0, True, "", A("halt", "conflict_tier3", T, True)),
+    (
+        3,
+        2,
+        "halt_max_rounds",
+        2,
+        0,
+        True,
+        "",
+        A("report", "conflict_tier3", None, True),
+    ),
+]
+
+
+@pytest.mark.parametrize(
+    "tier,ordinal,entering,cap,prior,gc,reason,expected", _WAVE8A_ROWS
+)
+def test_router_wave8a_rows(tier, ordinal, entering, cap, prior, gc, reason, expected):
+    got = _route(
+        "wave8a",
+        tier,
+        ordinal,
+        entering=entering,
+        cap=cap,
+        prior=prior,
+        gc=gc,
+        reason=reason,
+    )
+    assert got == expected
+
+
+@pytest.mark.parametrize("entering", c.PRESERVED_OUTCOMES)
+def test_router_wave8a_tier1_preserved_column(entering):
+    by_ordinal = {
+        o: _route("wave8a", 1, o, entering=entering, cap=1, prior=0) for o in (1, 2, 3)
+    }
+    assert by_ordinal == {
+        1: A("report", "tier1_l1_preserved", None, True),
+        2: A("report", "tier1_l2_preserved", None, True),
+        3: A("resolve_push", "tier1_sync", push_kind="sync"),
+    }
+
+
+@pytest.mark.parametrize(
+    "hook,entering", [("wave0", None), ("wave8a", "clean"), ("wave8a", "no_response")]
+)
+@pytest.mark.parametrize("tier", [None, 0, 1, 2, 3])
+def test_router_l0_row(hook, entering, tier):
+    reason = {None: "probe_failed", 0: "no_conflict"}.get(tier, "")
+    got = _route(hook, tier, 0, entering=entering, reason=reason)
+    assert got == A("none", "l0")
+
+
+_DOMAIN_VIOLATIONS = [
+    {"hook": "wave1"},
+    {"hook": None},
+    {"hook": "WAVE0"},
+    {"ordinal": -1},
+    {"ordinal": 4},
+    {"ordinal": "3"},
+    {"ordinal": True},
+    {"ordinal": 3.0},
+    {"conflict_max_tier": -1},
+    {"conflict_max_tier": 3},
+    {"conflict_max_tier": True},
+    {"conflict_max_tier": "1"},
+    {"plan_tier": 4},
+    {"plan_tier": -1},
+    {"plan_tier": True},
+    {"plan_tier": "1"},
+    {"round_counter": -1},
+    {"round_counter": "0"},
+    {"max_rounds": -1},
+    {"max_rounds": None},
+    {"prior_conflict_cycles": -1},
+    {"prior_conflict_cycles": 1.5},
+    {"prior_conflict_cycles": False},
+    {"entering": "clean"},
+    {"hook": "c_initial", "entering": "clean"},
+    {"hook": "wave8a", "entering": None},
+    {"hook": "wave8a", "entering": "junk"},
+    {"hook": "c_initial", "ordinal": 1},
+    {"github_conflicting": None},
+    {"github_conflicting": "yes"},
+    {"plan_tier": None, "plan_reason": "junk"},
+    {"plan_tier": None, "plan_reason": "no_conflict"},
+    {"plan_tier": 0, "plan_reason": ""},
+    {"plan_tier": 0, "plan_reason": "probe_failed"},
+    {"hook": "wave8a", "entering": "clean", "plan_tier": None, "plan_reason": ""},
+]
+
+
+@pytest.mark.parametrize("override", _DOMAIN_VIOLATIONS)
+def test_router_domain_violation_reaches_default_row(override):
+    kwargs = {
+        "hook": "wave0",
+        "plan_tier": 1,
+        "ordinal": 3,
+        "entering": None,
+        "conflict_max_tier": 1,
+        "round_counter": 0,
+        "max_rounds": 3,
+        "prior_conflict_cycles": 0,
+        "github_conflicting": True,
+        "plan_reason": "",
+    }
+    kwargs.update(override)
+    assert c.conflict_action(**kwargs) == DEFAULT_ACTION
+
+
+_TIER_REASONS = [
+    (None, "probe_failed"),
+    (None, "merge_tree_unsupported"),
+    (0, "no_conflict"),
+    (0, "behind_only"),
+    (0, "blocked"),
+    (1, ""),
+    (2, ""),
+    (3, ""),
+]
+_RANK = {
+    "none": 0,
+    "report": 1,
+    "halt": 1,
+    "propose": 2,
+    "resolve_local": 3,
+    "resolve_push": 4,
+}
+
+
+def _in_domain_product(hook):
+    enterings = [None] if hook == "wave0" else list(c.ENTERING_OUTCOMES)
+    return itertools.product(
+        _TIER_REASONS,
+        enterings,
+        (0, 1, 2),  # conflict_max_tier
+        (0, 1, 2, 3),  # round_counter
+        (0, 1, 3),  # max_rounds
+        (0, 1, 2),  # prior_conflict_cycles
+        (False, True),  # github_conflicting
+    )
+
+
+@pytest.mark.parametrize("hook", ["wave0", "wave8a"])
+def test_router_ordinal_monotonicity(hook):
+    checked = 0
+    for (tier, reason), entering, cap, rc, mr, prior, gc in _in_domain_product(hook):
+        actions = [
+            _route(
+                hook,
+                tier,
+                o,
+                entering=entering,
+                cap=cap,
+                rc=rc,
+                mr=mr,
+                prior=prior,
+                gc=gc,
+                reason=reason,
+            )
+            for o in range(4)
+        ]
+        for act in actions:
+            assert act != DEFAULT_ACTION
+            assert act.action in c.ACTIONS
+            assert act.reason in c.REPORT_REASONS
+        ranks = [_RANK[a.action] for a in actions]
+        assert ranks == sorted(ranks), (tier, entering, cap, rc, mr, prior, gc, actions)
+        checked += 1
+    assert checked > 1000
+
+
+def test_router_c_initial_below_l3_is_default_row():
+    for (tier, reason), cap, rc, mr, prior, gc in itertools.product(
+        _TIER_REASONS, (0, 1, 2), (0, 1, 3), (0, 1, 3), (0, 1), (False, True)
+    ):
+        for ordinal in (0, 1, 2):
+            got = _route(
+                "c_initial",
+                tier,
+                ordinal,
+                cap=cap,
+                rc=rc,
+                mr=mr,
+                prior=prior,
+                gc=gc,
+                reason=reason,
+            )
+            assert got == DEFAULT_ACTION
+
+
+def test_report_and_halt_reasons_overlap_in_exactly_eight():
+    assert c.REPORT_REASONS & c.HALT_REASONS == {
+        "tier_above_cap",
+        "conflict_tier3",
+        "probe_failed",
+        "merge_tree_unsupported",
+        "github_disagrees",
+        "sync_cap",
+        "late_conflict",
+        "router_unreachable",
+    }
+
+
+# ---------------------------------------------------------------------------
+# Gates
+# ---------------------------------------------------------------------------
+
+PRE = SHA_A
+BASE = SHA_B
+
+
+@pytest.mark.parametrize(
+    "parents,pre,base,expected",
+    [
+        ([PRE, BASE], PRE, BASE, True),
+        ([PRE.upper(), BASE.upper()], PRE, BASE, True),
+        ([PRE, BASE], PRE.upper(), BASE.upper(), True),
+        ([PRE + "\n", BASE], PRE, BASE, False),
+        ([PRE, BASE + "\n"], PRE, BASE, False),
+        ([" " + PRE, BASE], PRE, BASE, False),
+        ([PRE, BASE], " " + PRE, BASE, False),
+        ([BASE, PRE], PRE, BASE, False),
+        ([PRE, PRE], PRE, PRE, False),
+        ([PRE, PRE.upper()], PRE, PRE, False),
+        ([], PRE, BASE, False),
+        ([PRE], PRE, BASE, False),
+        ([PRE, BASE, SHA_C], PRE, BASE, False),
+        (None, PRE, BASE, False),
+        ((PRE, BASE), PRE, BASE, False),
+        (f"{PRE} {BASE}", PRE, BASE, False),
+        ([PRE[:7], BASE], PRE[:7], BASE, False),
+        ([PRE, BASE[:12]], PRE, BASE[:12], False),
+        ([PRE, BASE], None, BASE, False),
+        ([PRE, BASE], PRE, None, False),
+        ([PRE, None], PRE, BASE, False),
+        ([PRE, 123], PRE, BASE, False),
+        ([PRE, SHA_C], PRE, BASE, False),
+        (["null", BASE], "null", BASE, False),
+    ],
+)
+def test_merge_parent_ok_matrix(parents, pre, base, expected):
+    assert c.merge_parent_ok(parents, pre, base) is expected
+
+
+def test_merge_parent_ok_disjoint_from_push_parent_ok():
+    pool = [SHA_A, SHA_B, SHA_C, SHA_A.upper(), SHA_A[:7], SHA_A + "\n", "", None, 5]
+    accepted = 0
+    for n in range(4):
+        for combo in itertools.product(pool, repeat=n):
+            parents = list(combo)
+            for pre, base in ((SHA_A, SHA_B), (SHA_A.upper(), SHA_C), (SHA_A, SHA_A)):
+                merge_ok = c.merge_parent_ok(parents, pre, base)
+                push_ok = push_parent_ok(parents, pre)
+                assert not (merge_ok and push_ok), parents
+                if merge_ok:
+                    accepted += 1
+                    assert push_parent_ok(parents, pre) is False
+    assert accepted > 0
+
+
+@pytest.mark.parametrize(
+    "porcelain,expected",
+    [
+        ("", (True, [])),
+        ("M  a.py\0", (False, ["a.py"])),
+        (" M b.py\0", (False, ["b.py"])),
+        ("MM a.py\0 D gone.py\0", (False, ["a.py", "gone.py"])),
+        ("R  new.py\0old.py\0", (False, ["new.py", "old.py"])),
+        ("C  copy.py\0orig.py\0 M x.py\0", (False, ["copy.py", "orig.py", "x.py"])),
+        ("?? untracked.txt\0", (True, [])),
+        ("?? untracked.txt\0 M b.py\0", (False, ["b.py"])),
+        (None, (False, ["<unparsable status>"])),
+        (b"", (False, ["<unparsable status>"])),
+        (["M  a.py"], (False, ["<unparsable status>"])),
+        ("M  a.py", (False, ["<unparsable status>"])),
+        ("garbage\0", (False, ["<unparsable status>"])),
+        ("ZZ a.py\0", (False, ["<unparsable status>"])),
+        ("M\0", (False, ["<unparsable status>"])),
+        ("R  new.py\0", (False, ["<unparsable status>"])),
+        ("   a.py\0", (False, ["<unparsable status>"])),
+    ],
+)
+def test_merge_preflight_ok_rows(porcelain, expected):
+    assert c.merge_preflight_ok(porcelain) == expected
+
+
+def _sync(**overrides):
+    kwargs = {
+        "monitor_ordinal": 3,
+        "validation_status": "validated",
+        "tier": 1,
+        "conflict_max_tier": 2,
+        "halt_reason": None,
+        "prior_conflict_cycles": 0,
+        "round_counter": 0,
+        "max_rounds": 3,
+    }
+    kwargs.update(overrides)
+    return c.evaluate_sync_decision(**kwargs)
+
+
+_BOOLS4 = list(itertools.product((True, False), repeat=4))
+
+
+@pytest.mark.parametrize("p1,p2,p3,p4", _BOOLS4)
+def test_evaluate_sync_decision_truth_table_tier1(p1, p2, p3, p4):
+    got = _sync(
+        tier=1,
+        monitor_ordinal=3 if p1 else 2,
+        validation_status="validated" if p2 else "failed",
+        halt_reason=None if p3 else "sync_tier3",
+        prior_conflict_cycles=0 if p4 else 1,
+        round_counter=3,  # no round term for tier 1
+        max_rounds=3,
+    )
+    assert got == SyncDecision(p1, p2, p3, p4, p1 and p2 and p3 and p4, "sync")
+
+
+@pytest.mark.parametrize("p4_via", ["prior", "rounds"])
+@pytest.mark.parametrize("p1,p2,p3,p4", _BOOLS4)
+def test_evaluate_sync_decision_truth_table_tier2(p1, p2, p3, p4, p4_via):
+    blocked_prior = not p4 and p4_via == "prior"
+    blocked_rounds = not p4 and p4_via == "rounds"
+    got = _sync(
+        tier=2,
+        monitor_ordinal=3 if p1 else 1,
+        validation_status="validated" if p2 else "failed",
+        conflict_max_tier=2 if p3 else 1,
+        prior_conflict_cycles=1 if blocked_prior else 0,
+        round_counter=3 if blocked_rounds else 2,
+        max_rounds=3,
+    )
+    assert got == SyncDecision(p1, p2, p3, p4, p1 and p2 and p3 and p4, "merge")
+
+
+@pytest.mark.parametrize("tier", [0, 3, None, True, "1", 1.0])
+def test_evaluate_sync_decision_invalid_tier(tier):
+    got = _sync(tier=tier)
+    assert got.predicate_3_tier_allowed is False
+    assert got.authorized is False
+    assert got.kind == "sync"
+
+
+@pytest.mark.parametrize(
+    "override,predicate",
+    [
+        ({"monitor_ordinal": "3"}, "predicate_1_ordinal"),
+        ({"monitor_ordinal": True}, "predicate_1_ordinal"),
+        ({"conflict_max_tier": "2"}, "predicate_3_tier_allowed"),
+        ({"prior_conflict_cycles": "0"}, "predicate_4_under_cap"),
+        ({"prior_conflict_cycles": -1}, "predicate_4_under_cap"),
+        ({"tier": 2, "round_counter": "0"}, "predicate_4_under_cap"),
+        ({"tier": 2, "max_rounds": None}, "predicate_4_under_cap"),
+    ],
+)
+def test_evaluate_sync_decision_non_int_inputs_fail_the_predicate(override, predicate):
+    got = _sync(**override)
+    assert getattr(got, predicate) is False
+    assert got.authorized is False
+
+
+def test_evaluate_sync_decision_audit_predicates():
+    assert _sync().audit_predicates == {
+        "p1_ordinal": True,
+        "p2_validated": True,
+        "p3_tier_allowed": True,
+        "p4_under_cap": True,
+    }
+
+
+@pytest.mark.parametrize("ordinal", [0, 1, 2, 3, 4])
+@pytest.mark.parametrize("status", ["validated", "failed", "", "VALIDATED"])
+def test_sync_and_push_gates_agree_on_ordinal_and_validation(ordinal, status):
+    sync = _sync(monitor_ordinal=ordinal, validation_status=status)
+    push = evaluate_push_decision(
+        monitor_ordinal=ordinal,
+        validation_status=status,
+        needs_human_decision=False,
+        round_counter=0,
+        max_rounds=3,
+        applied_edits=1,
+    )
+    assert sync.predicate_1_ordinal == push.predicate_1_ordinal
+    assert sync.predicate_2_validated == push.predicate_2_validated
+
+
+@pytest.mark.parametrize(
+    "decision,expected",
+    [
+        (
+            SyncDecision(True, True, False, False, False, "sync"),
+            MonitorState.HALT_HUMAN,
+        ),
+        (
+            SyncDecision(True, True, False, True, False, "merge"),
+            MonitorState.HALT_HUMAN,
+        ),
+        (
+            SyncDecision(True, True, True, False, False, "sync"),
+            MonitorState.REPORT_ONLY,
+        ),
+        (
+            SyncDecision(False, True, True, True, False, "sync"),
+            MonitorState.REPORT_ONLY,
+        ),
+        (
+            SyncDecision(True, False, True, True, False, "merge"),
+            MonitorState.REPORT_ONLY,
+        ),
+        (SyncDecision(True, True, True, True, True, "sync"), MonitorState.REPORT_ONLY),
+        (None, MonitorState.HALT_HUMAN),
+        ("blocked", MonitorState.HALT_HUMAN),
+    ],
+)
+def test_sync_fail_state_mapping(decision, expected):
+    assert c.sync_fail_state(decision) is expected
+
+
+_GREEN = {"VG-1": True, "VG-3": True, "VG-4": True}
+
+
+@pytest.mark.parametrize(
+    "tier,results,expected",
+    [
+        (1, _GREEN, "validated"),
+        (1, {**_GREEN, "VG-5": True}, "validated"),
+        (1, {**_GREEN, "VG-2": False}, "failed"),
+        (1, {"VG-1": True, "VG-3": True}, "failed"),
+        (2, _GREEN, "failed"),
+        (2, {**_GREEN, "VG-2": True}, "validated"),
+        (2, {**_GREEN, "VG-2": False}, "failed"),
+        (2, {**_GREEN, "VG-2": 1}, "failed"),
+        (2, {"VG-2": True, "VG-1": True}, "failed"),
+        (0, {**_GREEN, "VG-2": True}, "failed"),
+        (3, {**_GREEN, "VG-2": True}, "failed"),
+        (True, _GREEN, "failed"),
+        (1, None, "failed"),
+        (1, [("VG-1", True)], "failed"),
+    ],
+)
+def test_conflict_validation_status(tier, results, expected):
+    assert c.conflict_validation_status(tier, results) == expected
+
+
+# ---------------------------------------------------------------------------
+# Cycle ids
+# ---------------------------------------------------------------------------
+
+
+def test_conflict_cycle_id_values():
+    assert c.conflict_cycle_id(1, 1) == "sync-1"
+    assert c.conflict_cycle_id(2, 1) == "conflict-1"
+    assert c.conflict_cycle_id(2, 3) == "conflict-3"
+
+
+@pytest.mark.parametrize(
+    "tier,n",
+    [(0, 1), (3, 1), (1, 0), (2, -1), (True, 1), (1, True), ("1", 1), (1, "1")],
+)
+def test_conflict_cycle_id_rejects(tier, n):
+    with pytest.raises(ValueError):
+        c.conflict_cycle_id(tier, n)
+
+
+@pytest.mark.parametrize(
+    "cycle_id,expected",
+    [
+        ("sync-1", True),
+        ("conflict-2", True),
+        ("c1", False),
+        ("cB", False),
+        ("round-0", False),
+        ("cycle-1", False),
+        ("3f2b8a64-1c2d-4e5f-9a0b-1c2d3e4f5a6b", False),
+        ("SYNC-1", False),
+        ("", False),
+        (None, False),
+        (1, False),
+    ],
+)
+def test_is_conflict_cycle(cycle_id, expected):
+    assert c.is_conflict_cycle(cycle_id) is expected
+
+
+@pytest.mark.parametrize(
+    "cycles,cycle_id,expected",
+    [
+        (["sync-1"], "sync-1", 0),
+        (["sync-1"], "sync-2", 1),
+        ([], "sync-1", 0),
+        (["sync-1", "sync-1", "conflict-2"], "sync-3", 2),
+        ([1, None, "sync-1"], "sync-2", 1),
+        (None, "sync-1", c.SYNC_CAP),
+        ("sync-1", "sync-1", c.SYNC_CAP),
+        (("sync-1",), "sync-2", c.SYNC_CAP),
+    ],
+)
+def test_prior_conflict_cycles(cycles, cycle_id, expected):
+    assert c.prior_conflict_cycles(cycles, cycle_id) == expected
+
+
+# ---------------------------------------------------------------------------
+# Record and message
+# ---------------------------------------------------------------------------
+
+_LISTING = MergeTreeListing(
+    TREE,
+    (
+        StageRecord("100644", SHA_A, 1, "f.txt"),
+        StageRecord("100644", SHA_B, 2, "f.txt"),
+        StageRecord("100644", SHA_C, 3, "f.txt"),
+        StageRecord("100644", OID, 2, "new.txt"),
+        StageRecord("100644", SHA_B, 3, "new.txt"),
+        StageRecord("100644", SHA_C, 1, "d.txt"),
+        StageRecord("100644", SHA_B, 2, "d.txt"),
+    ),
+)
+
+
+def test_finish_manifest_lines_in_listing_order():
+    got = c.finish_manifest(_LISTING, ["d.txt", "new.txt", "f.txt"])
+    assert got == f"{SHA_A}\tf.txt\n-\tnew.txt\n{SHA_C}\td.txt\n"
+    assert c.finish_manifest(_LISTING, ["d.txt"]) == f"{SHA_C}\td.txt\n"
+    assert c.finish_manifest(_LISTING, []) == ""
+
+
+def test_finish_manifest_on_captured_fixture():
+    listing = parse_stage_records(FIXTURE.read_bytes().decode("utf-8"))
+    base = {r.path: r.oid for r in listing.records if r.stage == 1}
+    order = list(dict.fromkeys(r.path for r in listing.records))
+    assert sorted(order) == ["d.txt", "f.txt"]
+    got = c.finish_manifest(listing, ["f.txt", "d.txt"])
+    assert got == "".join(f"{base[p]}\t{p}\n" for p in order)
+
+
+@pytest.mark.parametrize(
+    "paths", [["x.txt"], ["f.txt", "f.txt"], ["f\tx.txt"], ["f.txt\n"], [""], [None]]
+)
+def test_finish_manifest_rejects(paths):
+    with pytest.raises(ValueError):
+        c.finish_manifest(_LISTING, paths)
+
+
+def test_finish_manifest_rejects_non_listing():
+    with pytest.raises(ValueError):
+        c.finish_manifest("listing", ["f.txt"])  # type: ignore[arg-type]
+
+
+_RECORD_TEXT = """\
+## src/a.py
+kind: additive
+root_cause: both sides added an import block
+ours_intent: Ours adds request logging.
+theirs_intent: Theirs adds a metrics counter.
+resolution: keep_both(ours first)
+behavior_after: Requests are logged and counted.
+dropped: none
+evidence: stage files 1, 2 and 3 of src/a.py
+
+## docs/b.md
+kind: competing
+root_cause: both sides reworded one sentence
+ours_intent: Ours names the new flag.
+theirs_intent: Theirs fixes a typo.
+resolution: synthesized
+behavior_after: The sentence names the flag without the typo.
+dropped: none
+evidence: stage files of docs/b.md
+"""
+
+
+def _good_entry(**overrides):
+    entry = {
+        "kind": "additive",
+        "root_cause": "both sides added an import block",
+        "ours_intent": "Ours adds request logging.",
+        "theirs_intent": "Theirs adds a metrics counter.",
+        "resolution": "keep_both(ours first)",
+        "behavior_after": "Requests are logged and counted.",
+        "dropped": "none",
+        "evidence": "stage files 1, 2 and 3",
+    }
+    entry.update(overrides)
+    return entry
+
+
+def test_parse_resolution_record_valid():
+    record = c.parse_resolution_record(_RECORD_TEXT)
+    assert list(record) == ["src/a.py", "docs/b.md"]
+    assert record["src/a.py"] == _good_entry(
+        evidence="stage files 1, 2 and 3 of src/a.py"
+    )
+    assert record["docs/b.md"]["resolution"] == "synthesized"
+    assert c.resolution_record_ok(record, ("src/a.py", "docs/b.md")) == []
+
+
+@pytest.mark.parametrize(
+    "text",
+    [
+        "## a.py\nkind: additive\n## a.py\nkind: additive\n",  # duplicate heading
+        "## a.py\nkind: additive\nkind: competing\n",  # duplicate field
+        "## a.py\ncolour: blue\n",  # unknown field
+        "## a.py\nthis line has no field\n",  # not a field line
+        "kind: additive\n## a.py\n",  # field before the first heading
+        "## \nkind: additive\n",  # empty heading
+    ],
+)
+def test_parse_resolution_record_rejects(text):
+    with pytest.raises(ValueError):
+        c.parse_resolution_record(text)
+
+
+def test_parse_resolution_record_rejects_non_string():
+    with pytest.raises(ValueError):
+        c.parse_resolution_record(None)  # type: ignore[arg-type]
+
+
+@pytest.mark.parametrize(
+    "record,text_paths,expected",
+    [
+        ({"a.py": _good_entry()}, ("a.py",), []),
+        ({"a.py": _good_entry(resolution="keep_both")}, ("a.py",), []),
+        ({"a.py": _good_entry(ours_intent="Ours uses the v1.2 API.")}, ("a.py",), []),
+        ({"a.py": _good_entry()}, ("a.py", "b.py"), ["b.py: missing entry"]),
+        (
+            {"a.py": _good_entry(), "z.py": _good_entry()},
+            ("a.py",),
+            ["z.py: extra entry"],
+        ),
+        (
+            {"a.py": _good_entry(root_cause="  ")},
+            ("a.py",),
+            ["a.py: root_cause is missing or empty"],
+        ),
+        (
+            {"a.py": _good_entry(ours_intent="Ours logs. It also counts.")},
+            ("a.py",),
+            ["a.py: ours_intent is not exactly one sentence"],
+        ),
+        (
+            {"a.py": _good_entry(theirs_intent="Theirs adds\na counter.")},
+            ("a.py",),
+            ["a.py: theirs_intent is not exactly one sentence"],
+        ),
+        (
+            {"a.py": _good_entry(behavior_after="Requests are logged")},
+            ("a.py",),
+            ["a.py: behavior_after is not exactly one sentence"],
+        ),
+        (
+            {"a.py": _good_entry(kind="semantic")},
+            ("a.py",),
+            ["a.py: kind semantic means Tier 3"],
+        ),
+        (
+            {"a.py": _good_entry(kind="mystery")},
+            ("a.py",),
+            ["a.py: unknown kind mystery"],
+        ),
+        (
+            {"a.py": _good_entry(resolution="take_both")},
+            ("a.py",),
+            ["a.py: unknown resolution take_both"],
+        ),
+        (
+            {"a.py": _good_entry(resolution="keep_both()")},
+            ("a.py",),
+            ["a.py: unknown resolution keep_both()"],
+        ),
+        (
+            {"a.py": {k: v for k, v in _good_entry().items() if k != "dropped"}},
+            ("a.py",),
+            ["a.py: dropped is missing or empty"],
+        ),
+        ({"a.py": "kind: additive"}, ("a.py",), ["a.py: entry is not a mapping"]),
+        ("## a.py", ("a.py",), ["record is not a mapping"]),
+        (None, ("a.py",), ["record is not a mapping"]),
+    ],
+)
+def test_resolution_record_ok_problems(record, text_paths, expected):
+    assert c.resolution_record_ok(record, text_paths) == expected
+
+
+def test_merge_commit_message_tier1():
+    msg = c.merge_commit_message(
+        base_ref="origin/master",
+        head_branch="feat/x",
+        tier=1,
+        rule_patterns=("uv.lock",),
+        lock_changes="requests 2.31.0 -> 2.32.0",
+    )
+    assert msg == (
+        "Merge origin/master into feat/x (sc:pr-submit sync, tier 1)\n"
+        "\n"
+        "uv.lock regenerated from the merged pyproject.toml\n"
+        "requests 2.31.0 -> 2.32.0\n"
+    )
+
+
+def test_merge_commit_message_tier2_labels_only():
+    secret = "SENTINEL_FILE_CONTENT"
+    record = {
+        "src/a.py": _good_entry(
+            ours_intent=f"Ours adds {secret}.",
+            theirs_intent=f"Theirs adds {secret}.",
+            behavior_after=f"Runs {secret}.",
+            root_cause=secret,
+            evidence=secret,
+        )
+    }
+    msg = c.merge_commit_message(
+        base_ref="origin/master", head_branch="feat/x", tier=2, record=record
+    )
+    assert msg == (
+        "Merge origin/master into feat/x (sc:pr-submit sync, tier 2)\n"
+        "\n"
+        "src/a.py: kind additive, resolution keep_both(ours first), dropped none\n"
+    )
+    assert secret not in msg
+
+
+@pytest.mark.parametrize(
+    "kwargs",
+    [
+        {"tier": 2},
+        {"tier": 2, "record": {}},
+        {"tier": 2, "record": "## a.py"},
+        {"tier": 3},
+        {"tier": 0},
+        {"tier": True},
+        {"tier": 1, "rule_patterns": ("pkg/uv.lock",)},
+        {"tier": 1, "base_ref": ""},
+        {"tier": 1, "head_branch": "feat\nx"},
+        {"tier": 2, "record": {"a.py": _good_entry(dropped="line one\nline two")}},
+    ],
+)
+def test_merge_commit_message_rejects(kwargs):
+    full = {"base_ref": "origin/master", "head_branch": "feat/x", **kwargs}
+    with pytest.raises(ValueError):
+        c.merge_commit_message(**full)
+
+
+# ---------------------------------------------------------------------------
+# Resume: crash_resume_plan (design section 4.8, table 2)
+# ---------------------------------------------------------------------------
+
+
+def test_branch_literals_equal_recovery():
+    assert c.BRANCH_LANDED == recovery.BRANCH_A_LANDED
+    assert c.BRANCH_NOT_LANDED == recovery.BRANCH_B_NOT_LANDED
+    assert c.BRANCH_AMBIGUOUS == recovery.BRANCH_C_AMBIGUOUS
+
+
+_ABSENT = object()
+_DANGLING = {
+    "event_type": "push_initiated",
+    "run_id": "r1",
+    "cycle_id": "sync-1",
+    "pre_push_sha": SHA_A,
+    "target_sha": SHA_C,
+    "target_branch": "feat/x",
+    "target_remote": "origin",
+    "base_sha": SHA_B,
+    "review_terminal": "clean",
+    "expect_checks": False,
+}
+_FSM_STATE = MonitorState.S5A_RETRIGGER_REVIEW
+_COMMON = {"cycle_id": "sync-1", "target_sha": SHA_C, "base_sha": SHA_B}
+_WAVE8 = {"wait_sha": SHA_C, "review_terminal": "clean", "expect_checks": False}
+_A, _B, _C = c.BRANCH_LANDED, c.BRANCH_NOT_LANDED, c.BRANCH_AMBIGUOUS
+
+
+def _dangling(kind=_ABSENT, **overrides):
+    record = dict(_DANGLING)
+    if kind is not _ABSENT:
+        record["kind"] = kind
+    record.update(overrides)
+    return record
+
+
+def _ambiguous(kind):
+    return ResumePlan(
+        "halt",
+        state=MonitorState.HALT_HUMAN,
+        reason="ambiguous_remote_tip",
+        kind=kind,
+        **_COMMON,
+    )
+
+
+def _unrep(kind):
+    return ResumePlan("halt", reason="resume_unrepresentable", kind=kind, **_COMMON)
+
+
+_CRASH_TABLE = {
+    ("fix", _A): ResumePlan("fsm", state=_FSM_STATE, kind="fix", **_COMMON),
+    ("fix", _B): ResumePlan(
+        "fsm", state=MonitorState.S4_PUSHING, kind="fix", **_COMMON
+    ),
+    ("fix", _C): _ambiguous("fix"),
+    ("fix", "junk"): _unrep("fix"),
+    (_ABSENT, _A): ResumePlan("fsm", state=_FSM_STATE, kind="fix", **_COMMON),
+    (_ABSENT, _B): ResumePlan(
+        "fsm", state=MonitorState.S4_PUSHING, kind="fix", **_COMMON
+    ),
+    (_ABSENT, _C): _ambiguous("fix"),
+    (_ABSENT, "junk"): _unrep("fix"),
+    ("merge", _A): ResumePlan("fsm", state=_FSM_STATE, kind="merge", **_COMMON),
+    ("merge", _B): ResumePlan(
+        "fsm",
+        state=MonitorState.S4_PUSHING,
+        kind="merge",
+        check_merge_parent=True,
+        **_COMMON,
+    ),
+    ("merge", _C): _ambiguous("merge"),
+    ("merge", "junk"): _unrep("merge"),
+    ("sync", _A): ResumePlan("wave8_ci_wait", kind="sync", **_COMMON, **_WAVE8),
+    ("sync", _B): ResumePlan(
+        "redrive_then_wave8",
+        kind="sync",
+        rerun_guard=True,
+        check_merge_parent=True,
+        **_COMMON,
+        **_WAVE8,
+    ),
+    ("sync", _C): _ambiguous("sync"),
+    ("sync", "junk"): _unrep("sync"),
+    ("ci", _A): ResumePlan("wave8_ci_wait", kind="ci", **_COMMON, **_WAVE8),
+    ("ci", _B): ResumePlan(
+        "redrive_then_wave8",
+        kind="ci",
+        rerun_guard=True,
+        check_merge_parent=False,
+        **_COMMON,
+        **_WAVE8,
+    ),
+    ("ci", _C): _ambiguous("ci"),
+    ("ci", "junk"): _unrep("ci"),
+    ("rebase", _A): _unrep(None),
+    ("rebase", _B): _unrep(None),
+    ("rebase", _C): _unrep(None),
+    ("rebase", "junk"): _unrep(None),
+}
+
+
+@pytest.mark.parametrize(
+    "kind,branch",
+    list(_CRASH_TABLE),
+    ids=[f"{'absent' if k is _ABSENT else k}-{b}" for k, b in _CRASH_TABLE],
+)
+def test_crash_resume_plan_table(kind, branch):
+    dangling = _dangling(kind)
+    before = dict(dangling)
+    got = c.crash_resume_plan(dangling, branch, _FSM_STATE)
+    assert got == _CRASH_TABLE[(kind, branch)]
+    assert dangling == before  # pure: the record is not touched
+    if kind in ("sync", "ci"):
+        assert got.state not in (
+            MonitorState.S4_PUSHING,
+            MonitorState.S5A_RETRIGGER_REVIEW,
+            MonitorState.S5_AWAITING_REREVIEW,
+        )
+
+
+@pytest.mark.parametrize("kind", ["sync", "ci"])
+@pytest.mark.parametrize("branch", [_A, _B])
+@pytest.mark.parametrize("review_terminal", [_ABSENT, None, "junk", "CLEAN"])
+def test_crash_resume_plan_bad_review_terminal_halts(kind, branch, review_terminal):
+    dangling = _dangling(kind)
+    if review_terminal is _ABSENT:
+        del dangling["review_terminal"]
+    else:
+        dangling["review_terminal"] = review_terminal
+    got = c.crash_resume_plan(dangling, branch, _FSM_STATE)
+    assert (got.directive, got.reason) == ("halt", "resume_unrepresentable")
+
+
+@pytest.mark.parametrize("branch", [_A, _B])
+@pytest.mark.parametrize("base_sha", [_ABSENT, None, SHA_B[:7], "null"])
+def test_crash_resume_plan_sync_without_base_sha_halts(branch, base_sha):
+    dangling = _dangling("sync")
+    if base_sha is _ABSENT:
+        del dangling["base_sha"]
+    else:
+        dangling["base_sha"] = base_sha
+    got = c.crash_resume_plan(dangling, branch, _FSM_STATE)
+    assert (got.directive, got.reason) == ("halt", "resume_unrepresentable")
+
+
+def test_crash_resume_plan_ci_needs_no_base_sha():
+    dangling = _dangling("ci")
+    del dangling["base_sha"]
+    got = c.crash_resume_plan(dangling, _A, _FSM_STATE)
+    assert got.directive == "wave8_ci_wait"
+    assert got.base_sha is None
+
+
+@pytest.mark.parametrize("expect", [_ABSENT, None, "no", 0])
+@pytest.mark.parametrize("kind", ["sync", "ci"])
+def test_crash_resume_plan_missing_expect_checks_reads_true(expect, kind):
+    dangling = _dangling(kind)
+    if expect is _ABSENT:
+        del dangling["expect_checks"]
+    else:
+        dangling["expect_checks"] = expect
+    assert c.crash_resume_plan(dangling, _A, _FSM_STATE).expect_checks is True
+
+
+def test_crash_resume_plan_ambiguous_wins_over_record_checks():
+    dangling = _dangling("sync")
+    del dangling["review_terminal"]
+    assert c.crash_resume_plan(dangling, _C, _FSM_STATE) == ResumePlan(
+        "halt",
+        state=MonitorState.HALT_HUMAN,
+        reason="ambiguous_remote_tip",
+        kind="sync",
+        **_COMMON,
+    )
+
+
+def test_crash_resume_plan_fails_closed_on_bad_inputs():
+    assert c.crash_resume_plan(None, _A, _FSM_STATE) == ResumePlan(  # type: ignore[arg-type]
+        "halt", reason="resume_unrepresentable"
+    )
+    got = c.crash_resume_plan(_dangling("fix"), _A, "S5_AWAITING_REREVIEW")  # type: ignore[arg-type]
+    assert (got.directive, got.reason) == ("halt", "resume_unrepresentable")
+
+
+# ---------------------------------------------------------------------------
+# Resume: conflict_resume_plan (design section 4.8, table 1)
+# ---------------------------------------------------------------------------
+
+
+def _open_cycle(**overrides):
+    entry = {
+        "event_type": "sync_started",
+        "run_id": "r1",
+        "cycle_id": "sync-1",
+        "tier": 1,
+        "kind": "sync",
+        "hook": "wave8a",
+        "base_ref": "origin/master",
+        "base_sha": SHA_B,
+        "pre_push_sha": SHA_A,
+        "merge_tree_oid": TREE,
+        "conflict_max_tier": 1,
+        "review_terminal": "clean",
+        "paths": ["uv.lock"],
+        "resumed": False,
+        "push_initiated": False,
+        "push_completed": False,
+        "target_sha": None,
+        "expect_checks": None,
+        "superseded": False,
+    }
+    entry.update(overrides)
+    return entry
+
+
+_MERGE_CYCLE = {
+    "cycle_id": "conflict-1",
+    "tier": 2,
+    "kind": "merge",
+    "hook": "c_initial",
+    "review_terminal": None,
+}
+
+
+def _state(open_cycle=None, *, rejected=False):
+    cycles = [open_cycle["cycle_id"]] if isinstance(open_cycle, dict) else []
+    return {
+        "push_count": 0,
+        "sync_push_count": 0,
+        "conflict_cycles": cycles,
+        "open_conflict_cycle": open_cycle,
+        "push_rejected": rejected,
+    }
+
+
+def _resume(
+    state,
+    *,
+    foreign_op=None,
+    merge_head_sha=None,
+    local_head_sha=SHA_A,
+    local_head_parents=None,
+    dangling=None,
+):
+    return c.conflict_resume_plan(
+        state,
+        foreign_op=foreign_op,
+        merge_head_sha=merge_head_sha,
+        local_head_sha=local_head_sha,
+        local_head_parents=local_head_parents,
+        dangling=dangling,
+    )
+
+
+_SYNC_IDS = {"cycle_id": "sync-1", "hook": "wave8a", "review_terminal": "clean"}
+_MERGE_IDS = {"cycle_id": "conflict-1", "hook": "c_initial", "review_terminal": None}
+
+
+def test_resume_row1_push_rejected_without_open_cycle():
+    assert _resume(_state(rejected=True)) == ResumePlan("halt", reason="push_rejected")
+
+
+def test_resume_row1_push_rejected_closes_open_cycle():
+    state = _state(_open_cycle(push_initiated=True, target_sha=SHA_C), rejected=True)
+    assert _resume(state) == ResumePlan(
+        "halt", reason="push_rejected", cycle_id="sync-1"
+    )
+
+
+def test_resume_row2_no_open_cycle_no_foreign_op():
+    assert _resume(_state()) == ResumePlan("none")
+
+
+@pytest.mark.parametrize("op", c.FOREIGN_OPS)
+def test_resume_row3_no_open_cycle_foreign_op(op):
+    assert _resume(_state(), foreign_op=op, merge_head_sha=SHA_B) == ResumePlan(
+        "halt", reason="foreign_op_in_progress"
+    )
+
+
+def test_resume_row3b_superseded_cycle_halts_before_row4():
+    state = _state(
+        _open_cycle(
+            superseded=True, push_initiated=True, push_completed=True, target_sha=SHA_C
+        )
+    )
+    assert _resume(state) == ResumePlan(
+        "halt", reason="resume_unrepresentable", cycle_id="sync-1"
+    )
+
+
+@pytest.mark.parametrize(
+    "overrides",
+    [
+        {"hook": _ABSENT},
+        {"hook": "wave0"},
+        {"hook": None},
+        {"review_terminal": _ABSENT},
+        {"review_terminal": None},
+        {"review_terminal": "junk"},
+        {"hook": "c_initial", "review_terminal": "clean"},
+    ],
+)
+def test_resume_row4c_invalid_hook_or_review_terminal_halts(overrides):
+    entry = _open_cycle(push_initiated=True, push_completed=True, target_sha=SHA_C)
+    for key, value in overrides.items():
+        if value is _ABSENT:
+            del entry[key]
+        else:
+            entry[key] = value
+    assert _resume(_state(entry)) == ResumePlan(
+        "halt", reason="resume_unrepresentable", cycle_id="sync-1"
+    )
+
+
+def test_resume_row4c_c_initial_without_review_terminal_key_is_valid():
+    entry = _open_cycle(**_MERGE_CYCLE)
+    del entry["review_terminal"]
+    assert _resume(_state(entry)).directive == "restart"
+
+
+def test_resume_row4_sync_complete_after_push():
+    state = _state(
+        _open_cycle(
+            push_initiated=True,
+            push_completed=True,
+            target_sha=SHA_C,
+            expect_checks=False,
+        )
+    )
+    assert _resume(state) == ResumePlan(
+        "complete_after_push",
+        kind="sync",
+        wait_sha=SHA_C,
+        target_sha=SHA_C,
+        base_sha=SHA_B,
+        expect_checks=False,
+        **_SYNC_IDS,
+    )
+
+
+@pytest.mark.parametrize("expect", [_ABSENT, None, "false", 0])
+def test_resume_row4_missing_expect_checks_reads_true(expect):
+    entry = _open_cycle(push_initiated=True, push_completed=True, target_sha=SHA_C)
+    if expect is _ABSENT:
+        del entry["expect_checks"]
+    else:
+        entry["expect_checks"] = expect
+    assert _resume(_state(entry)).expect_checks is True
+
+
+def test_resume_row4_merge_resumes_at_retrigger():
+    state = _state(
+        _open_cycle(
+            push_initiated=True,
+            push_completed=True,
+            target_sha=SHA_C,
+            expect_checks=True,
+            **_MERGE_CYCLE,
+        )
+    )
+    assert _resume(state) == ResumePlan(
+        "complete_after_push",
+        state=MonitorState.S5A_RETRIGGER_REVIEW,
+        kind="merge",
+        target_sha=SHA_C,
+        base_sha=SHA_B,
+        expect_checks=True,
+        **_MERGE_IDS,
+    )
+
+
+@pytest.mark.parametrize("overrides", [{"kind": "fix"}, {"target_sha": None}])
+def test_resume_row4_unusable_push_record_halts(overrides):
+    entry = _open_cycle(push_initiated=True, push_completed=True, target_sha=SHA_C)
+    entry.update(overrides)
+    got = _resume(_state(entry))
+    assert (got.directive, got.reason, got.cycle_id) == (
+        "halt",
+        "resume_unrepresentable",
+        "sync-1",
+    )
+
+
+def test_resume_row4b_matching_dangling_is_crash_window():
+    state = _state(_open_cycle(push_initiated=True, target_sha=SHA_C))
+    dangling = {"event_type": "push_initiated", "cycle_id": "sync-1", "kind": "sync"}
+    assert _resume(state, dangling=dangling) == ResumePlan(
+        "crash_window", kind="sync", target_sha=SHA_C, base_sha=SHA_B, **_SYNC_IDS
+    )
+
+
+@pytest.mark.parametrize(
+    "dangling", [None, {"cycle_id": "c7"}, {"cycle_id": "conflict-1"}, "sync-1"]
+)
+def test_resume_row4b_prime_unmatched_dangling_halts(dangling):
+    state = _state(_open_cycle(push_initiated=True, target_sha=SHA_C))
+    assert _resume(state, dangling=dangling) == ResumePlan(
+        "halt", reason="resume_unrepresentable", cycle_id="sync-1", target_sha=SHA_C
+    )
+
+
+@pytest.mark.parametrize("merge_head", [SHA_B, SHA_B.upper()])
+def test_resume_row5_own_merge_aborts_and_restarts(merge_head):
+    state = _state(_open_cycle())
+    got = _resume(
+        state, foreign_op="MERGE_HEAD", merge_head_sha=merge_head, local_head_sha=SHA_A
+    )
+    assert got == ResumePlan(
+        "abort_and_restart", kind="sync", base_sha=SHA_B, **_SYNC_IDS
+    )
+
+
+def test_resume_row5_c_initial_cycle_carries_its_hook():
+    state = _state(_open_cycle(**_MERGE_CYCLE))
+    got = _resume(state, foreign_op="MERGE_HEAD", merge_head_sha=SHA_B)
+    assert got == ResumePlan(
+        "abort_and_restart", kind="merge", base_sha=SHA_B, **_MERGE_IDS
+    )
+
+
+@pytest.mark.parametrize(
+    "op,merge_head",
+    [("MERGE_HEAD", SHA_C), ("MERGE_HEAD", None), ("rebase-apply", SHA_B)],
+)
+def test_resume_row6_other_foreign_op_halts(op, merge_head):
+    state = _state(_open_cycle())
+    assert _resume(state, foreign_op=op, merge_head_sha=merge_head) == ResumePlan(
+        "halt", reason="sync_foreign_operation", cycle_id="sync-1"
+    )
+
+
+@pytest.mark.parametrize("head", [SHA_A, SHA_A.upper()])
+def test_resume_row7_head_at_pre_push_restarts(head):
+    assert _resume(_state(_open_cycle()), local_head_sha=head) == ResumePlan(
+        "restart", kind="sync", base_sha=SHA_B, **_SYNC_IDS
+    )
+
+
+def test_resume_row7_c_initial_restart_carries_its_hook():
+    got = _resume(_state(_open_cycle(**_MERGE_CYCLE)), local_head_sha=SHA_A)
+    assert got == ResumePlan("restart", kind="merge", base_sha=SHA_B, **_MERGE_IDS)
+    assert got.hook == "c_initial"
+
+
+@pytest.mark.parametrize(
+    "head,parents",
+    [(SHA_C, [SHA_A, SHA_B]), (SHA_C, None), (None, None), (SHA_A[:7], [SHA_A])],
+)
+def test_resume_row8_anything_else_halts(head, parents):
+    got = _resume(
+        _state(_open_cycle()), local_head_sha=head, local_head_parents=parents
+    )
+    assert got == ResumePlan("halt", reason="resume_unrepresentable", cycle_id="sync-1")
+
+
+@pytest.mark.parametrize(
+    "state",
+    [
+        None,
+        {},
+        {"open_conflict_cycle": None, "push_rejected": False},
+        {k: v for k, v in _state().items() if k != "sync_push_count"},
+        {**_state(), "push_rejected": "yes"},
+        {**_state(), "conflict_cycles": None},
+        {**_state(), "sync_push_count": -1},
+        {**_state(), "open_conflict_cycle": "sync-1"},
+        _state(_open_cycle(cycle_id="c1")),
+        _state(_open_cycle(cycle_id=None)),
+    ],
+)
+def test_resume_unusable_state_halts(state):
+    assert _resume(state) == ResumePlan("halt", reason="resume_unrepresentable")
+
+
+def test_resume_planners_are_pure():
+    entry = _open_cycle(push_initiated=True, target_sha=SHA_C)
+    state = _state(entry)
+    dangling = {"cycle_id": "sync-1", "kind": "sync"}
+    snapshot = (repr(state), repr(dangling))
+    _resume(state, dangling=dangling)
+    _resume(state, foreign_op="MERGE_HEAD", merge_head_sha=SHA_B)
+    assert (repr(state), repr(dangling)) == snapshot
+
+
 # ---------------------------------------------------------------------------
 # Purity
 # ---------------------------------------------------------------------------
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t4-tests.log b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t4-tests.log
new file mode 100644
index 00000000..4b0420a9
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t4-tests.log
@@ -0,0 +1,23 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 760 items
+
+tests/pr_submit/test_conflicts_core.py ................................. [  4%]
+........................................................................ [ 13%]
+........................................................................ [ 23%]
+........................................................................ [ 32%]
+........................................................................ [ 42%]
+........................................................................ [ 51%]
+........................................................................ [ 61%]
+........................................................................ [ 70%]
+........................................................................ [ 80%]
+........................................................................ [ 89%]
+........................................................................ [ 99%]
+.......                                                                  [100%]
+
+============================= 760 passed in 1.24s ==============================

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
