035669d4cd06c330df6a4fef7edf16362ffa3aae
Review one task for spec compliance.

Task brief: ## Task 5: Add the flag, `should_retrigger`, push-triad keywords and the P2 edge to `fsm.py`

Depends on: Task 4

Implement step 4 of source section 13 in `src/superclaude/pr_submit/fsm.py` per source section 6.1 items 1 to 8:

- `DEFAULT_CONFLICT_MAX_TIER = 1`; `SkillArgs.conflict_max_tier` appended last; `--conflict-max-tier` in `build_arg_parser` with `choices=[0, 1, 2]`; `parse_args` passes it through.
- `should_retrigger(applied_edits, push_kind=None)` after `push_fail_state`.
- `build_push_triad` keyword-only `push_kind`, `base_sha`, `review_terminal`, `expect_checks` (defaults `None`; byte-identical output when all are `None`; `ValueError` on an unknown `push_kind`; predicates from `decision.audit_predicates` for a non-`PushDecision`).
- The `(S2_CLASSIFY, "conflicting")` edge right after the `findings` edge; the `fsm.py:1137` condition becomes `should_retrigger(result.applied_edits)`.
- Tests per source section 12.2: `test_conflict_max_tier_default_and_bounds` in `tests/pr_submit/test_skill_parse.py`; `test_transition_conflicting_edge` in `tests/pr_submit/test_autonomy_gates.py`; `test_should_retrigger_zero_edit_pair` in `tests/pr_submit/test_loop_guard.py`; the Triad cases of source section 12.1 in `tests/pr_submit/test_conflicts_core.py` (the default call equals a literal three-record list captured from the current `build_push_triad` before editing it).

Acceptance criteria:
- `parse_args([]).conflict_max_tier == 1`; `--conflict-max-tier 3` and `x` raise `SystemExit`.
- `transition(S2_CLASSIFY, "conflicting")` gives `S3_FIXING` at L3 with budget, `HALT_MAX_ROUNDS` on a spent budget, `PROPOSED` at L1, `HALT_HUMAN` with `needs_human_decision`; `(S2_CLASSIFY, "findings")` still gives `S2B_VERIFY`.
- `should_retrigger(0, "merge")` is true and false for `fix`, `None`, `sync`, `ci`; `run_skill` zero-edit rows keep `rereview_request_count == 0`.
- The default `build_push_triad` call equals the recorded pre-change output; a `sync` call adds `kind`, `base_sha`, `review_terminal` and `expect_checks` where source section 6.1 says.
- `git diff` of `fsm.py` shows no change inside `evaluate_push_decision`, `push_fail_state`, `push_idempotency_key`, `push_parent_ok` or `needs_rebase`; T-N50 passes.
- `uv run pytest tests/pr_submit -q` passes; log saved to `./artifacts/t5-tests.log`.
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
Start sha: 035669d4cd06c330df6a4fef7edf16362ffa3aae
Diff against the start snapshot: diff --git a/src/superclaude/pr_submit/fsm.py b/src/superclaude/pr_submit/fsm.py
index 2f310a4f..58c9ed97 100644
--- a/src/superclaude/pr_submit/fsm.py
+++ b/src/superclaude/pr_submit/fsm.py
@@ -34,6 +34,7 @@ HARD_CAP_MAX_ROUNDS = 5
 MIN_POLL_INTERVAL = 30
 DEFAULT_TIMEOUT = 600
 DEFAULT_SILENCE_TIMEOUT = 300
+DEFAULT_CONFLICT_MAX_TIER = 1
 
 POLL_INTERVAL_ERROR = "minimum is 30 seconds"
 MAX_ROUNDS_ERROR = "--max-rounds hard cap is 5"
@@ -63,6 +64,7 @@ class SkillArgs:
     output_dir: str | None = None
     resume: str | None = None
     pr: int | None = None
+    conflict_max_tier: int = DEFAULT_CONFLICT_MAX_TIER
 
     @property
     def armed(self) -> bool:
@@ -96,6 +98,13 @@ def build_arg_parser() -> argparse.ArgumentParser:
     parser.add_argument("--output-dir", dest="output_dir", default=None)
     parser.add_argument("--resume", default=None)
     parser.add_argument("--pr", type=int, default=None)
+    parser.add_argument(
+        "--conflict-max-tier",
+        dest="conflict_max_tier",
+        type=int,
+        choices=[0, 1, 2],
+        default=DEFAULT_CONFLICT_MAX_TIER,
+    )
     return parser
 
 
@@ -131,6 +140,7 @@ def parse_args(argv: list[str]) -> SkillArgs:
         output_dir=ns.output_dir,
         resume=ns.resume,
         pr=ns.pr,
+        conflict_max_tier=ns.conflict_max_tier,
     )
 
 
@@ -219,6 +229,15 @@ def push_fail_state(decision: PushDecision) -> MonitorState:
     return MonitorState.REPORT_ONLY
 
 
+def should_retrigger(applied_edits: int, push_kind: str | None = None) -> bool:
+    """S5a re-trigger rule: a cycle that applied grounded edits, or a Tier 2
+    merge cycle (push kind "merge"), which applies no finding edit but publishes
+    authored code that the reviewers must see (issue #305, P2)."""
+    return (
+        isinstance(applied_edits, int) and applied_edits > 0
+    ) or push_kind == "merge"
+
+
 # --------------------------------------------------------------------------- #
 # L3 write-ahead push triad (spec §12.1 / INV-007)
 # --------------------------------------------------------------------------- #
@@ -245,6 +264,10 @@ def build_push_triad(
     target_branch: str,
     target_remote: str,
     decision: PushDecision,
+    push_kind: str | None = None,
+    base_sha: str | None = None,
+    review_terminal: str | None = None,
+    expect_checks: bool | None = None,
 ) -> list[dict]:
     """Build the ordered write-ahead push triad records (spec §12.1, verbatim order).
 
@@ -254,7 +277,20 @@ def build_push_triad(
     actual push side-effect (the version-control push of ``<sha>:<branch>`` to the
     remote) is the SKILL's job. The idempotency key is on every record so recovery
     can match the triad.
+
+    Issue #305: the four keyword-only extras default to ``None``; with all four
+    ``None`` the output is byte-identical to the pre-#305 records. ``push_kind``
+    (one of ``fix``, ``merge``, ``sync``, ``ci``; anything else raises
+    :class:`ValueError`) and ``base_sha`` join every record after ``target_remote``;
+    ``review_terminal`` and ``expect_checks`` join ``push_initiated`` after
+    ``remote_ref``, and ``expect_checks`` joins ``push_completed``, each only when
+    not ``None``. A :class:`PushDecision` keeps its five-key predicate dict; any
+    other decision supplies ``audit_predicates`` (the conflict sync gate, read by
+    attribute so this module never imports the conflict core). A decision with
+    neither shape raises :class:`AttributeError`.
     """
+    if push_kind is not None and push_kind not in ("fix", "merge", "sync", "ci"):
+        raise ValueError(f"unknown push_kind: {push_kind!r}")
     key = push_idempotency_key(run_id, cycle_id, pre_push_sha, target_branch)
     common = {
         "run_id": run_id,
@@ -265,26 +301,42 @@ def build_push_triad(
         "target_branch": target_branch,
         "target_remote": target_remote,
     }
+    if push_kind is not None:
+        common["kind"] = push_kind
+    if base_sha is not None:
+        common["base_sha"] = base_sha
+    if isinstance(decision, PushDecision):
+        predicates = {
+            "p1_ordinal": decision.predicate_1_ordinal,
+            "p2_validated": decision.predicate_2_validated,
+            "p3_no_human": decision.predicate_3_no_human,
+            "p4_under_cap": decision.predicate_4_under_cap,
+            "p5_applied_edits": decision.predicate_5_applied_edits,
+        }
+    else:
+        predicates = dict(decision.audit_predicates)
+    initiated_extra: dict = {}
+    if review_terminal is not None:
+        initiated_extra["review_terminal"] = review_terminal
+    completed_extra: dict = {}
+    if expect_checks is not None:
+        initiated_extra["expect_checks"] = expect_checks
+        completed_extra["expect_checks"] = expect_checks
     return [
         {
             "event_type": "push_decision",
             "round_counter": round_counter,
             "authorized": decision.authorized,
-            "predicates": {
-                "p1_ordinal": decision.predicate_1_ordinal,
-                "p2_validated": decision.predicate_2_validated,
-                "p3_no_human": decision.predicate_3_no_human,
-                "p4_under_cap": decision.predicate_4_under_cap,
-                "p5_applied_edits": decision.predicate_5_applied_edits,
-            },
+            "predicates": predicates,
             **common,
         },
         {
             "event_type": "push_initiated",
             "remote_ref": f"{target_remote}/{target_branch}",
+            **initiated_extra,
             **common,
         },
-        {"event_type": "push_completed", **common},
+        {"event_type": "push_completed", **completed_extra, **common},
     ]
 
 
@@ -746,6 +798,15 @@ def transition(
         ):
             return MonitorState.HALT_MAX_ROUNDS
         return MonitorState.S2B_VERIFY
+    if edge == (MonitorState.S2_CLASSIFY, "conflicting"):
+        # Issue #305 (P2): a Tier 2 merge cycle at C-initial. Same round gate as
+        # findings; then the G-edit ceiling (S3_FIXING at L2+, else PROPOSED).
+        if should_halt_rounds(
+            int(ctx.get("round_counter", 0)),
+            int(ctx.get("max_rounds", DEFAULT_MAX_ROUNDS)),
+        ):
+            return MonitorState.HALT_MAX_ROUNDS
+        return MonitorState.S3_FIXING if gate_edit(ordinal) else MonitorState.PROPOSED
     if edge == (MonitorState.S2B_VERIFY, "verified"):
         return MonitorState.S3_DIAGNOSE
     if edge == (MonitorState.S2B_VERIFY, "unverified"):
@@ -1134,7 +1195,7 @@ def run_skill(config: RunConfig | None = None, **overrides) -> SkillResult:
         # re-trigger comment (the trigger token lives in the bash script, never the core),
         # but ONLY when this cycle actually pushed (applied_edits > 0). The re-trigger
         # itself does NOT tick round_counter (INV-R1).
-        if result.applied_edits > 0:
+        if should_retrigger(result.applied_edits):
             # S5a: visibly enter the re-trigger state, then post the comment (the state
             # is overwritten by S5_AWAITING_REREVIEW below — materialized for topology
             # fidelity with transition()'s RESOLVING→S5A→S5 edges).
diff --git a/tests/pr_submit/test_skill_parse.py b/tests/pr_submit/test_skill_parse.py
index f67f4d0c..1d8cba46 100644
--- a/tests/pr_submit/test_skill_parse.py
+++ b/tests/pr_submit/test_skill_parse.py
@@ -11,6 +11,7 @@ from __future__ import annotations
 import pytest
 
 from superclaude.pr_submit.fsm import (
+    DEFAULT_CONFLICT_MAX_TIER,
     DEFAULT_MAX_ROUNDS,
     DEFAULT_MONITOR,
     DEFAULT_TIMEOUT,
@@ -103,3 +104,13 @@ def test_yes_flag_removed():
     """`--yes` never did anything and is no longer accepted."""
     with pytest.raises(SystemExit):
         parse_args(["--yes"])
+
+
+def test_conflict_max_tier_default_and_bounds():
+    """Issue #305: `--conflict-max-tier` defaults to 1, accepts 0-2, rejects 3 and non-ints."""
+    assert parse_args([]).conflict_max_tier == DEFAULT_CONFLICT_MAX_TIER == 1
+    for tier in (0, 1, 2):
+        assert parse_args(["--conflict-max-tier", str(tier)]).conflict_max_tier == tier
+    for bad in ("3", "x"):
+        with pytest.raises(SystemExit):
+            parse_args(["--conflict-max-tier", bad])
diff --git a/tests/pr_submit/test_autonomy_gates.py b/tests/pr_submit/test_autonomy_gates.py
index 744a3a33..8d1364e8 100644
--- a/tests/pr_submit/test_autonomy_gates.py
+++ b/tests/pr_submit/test_autonomy_gates.py
@@ -11,7 +11,12 @@ from __future__ import annotations
 
 import pytest
 
-from superclaude.pr_submit.fsm import PROPOSE_PROMPT, RunConfig, run_skill
+from superclaude.pr_submit.fsm import (
+    PROPOSE_PROMPT,
+    RunConfig,
+    run_skill,
+    transition,
+)
 from superclaude.pr_submit.models import Finding, MonitorState
 
 
@@ -152,3 +157,40 @@ def test_zero_edit_no_push(load_fixture):
     assert result.push_decision is not None
     assert result.push_decision.authorized is False
     assert result.push_decision.predicate_5_applied_edits == 0
+
+
+@pytest.mark.autonomy
+def test_transition_conflicting_edge():
+    """Issue #305 (P2): `(S2_CLASSIFY, "conflicting")` uses the findings round gate,
+    then the G-edit ceiling; the needs_human pre-gate still applies first."""
+    ms = MonitorState
+    budget = {"round_counter": 0, "max_rounds": 2}
+    assert (
+        transition(ms.S2_CLASSIFY, "conflicting", {"monitor_ordinal": 3, **budget})
+        == ms.S3_FIXING
+    )
+    assert (
+        transition(
+            ms.S2_CLASSIFY,
+            "conflicting",
+            {"monitor_ordinal": 3, "round_counter": 2, "max_rounds": 2},
+        )
+        == ms.HALT_MAX_ROUNDS
+    )
+    assert (
+        transition(ms.S2_CLASSIFY, "conflicting", {"monitor_ordinal": 1, **budget})
+        == ms.PROPOSED
+    )
+    assert (
+        transition(
+            ms.S2_CLASSIFY,
+            "conflicting",
+            {"monitor_ordinal": 3, "needs_human_decision": True, **budget},
+        )
+        == ms.HALT_HUMAN
+    )
+    # The findings edge is unchanged.
+    assert (
+        transition(ms.S2_CLASSIFY, "findings", {"monitor_ordinal": 3, **budget})
+        == ms.S2B_VERIFY
+    )
diff --git a/tests/pr_submit/test_loop_guard.py b/tests/pr_submit/test_loop_guard.py
index bcadd6a4..bd6bdde0 100644
--- a/tests/pr_submit/test_loop_guard.py
+++ b/tests/pr_submit/test_loop_guard.py
@@ -11,7 +11,7 @@ from __future__ import annotations
 
 import pytest
 
-from superclaude.pr_submit.fsm import RunConfig, run_skill
+from superclaude.pr_submit.fsm import RunConfig, run_skill, should_retrigger
 from superclaude.pr_submit.loop_guard import RoundCounter, should_halt, user_label
 from superclaude.pr_submit.models import Finding, MonitorState
 
@@ -225,3 +225,33 @@ def test_fallback_round_counter_cap_one():
         )
     )
     assert result.fallback_round_counter == 1
+
+
+@pytest.mark.loop_guard
+@pytest.mark.parametrize("max_rounds", [1, 2, 5])
+def test_should_retrigger_zero_edit_pair(max_rounds):
+    """Issue #305 (P2, QA-3b): only a Tier 2 merge cycle re-triggers with zero edits.
+
+    A zero-edit fix cycle never re-triggers, so `run_skill` (fix cycles only) keeps
+    `rereview_request_count == 0` when nothing was applied.
+    """
+    assert should_retrigger(0, "merge") is True
+    for kind in ("fix", None, "sync", "ci"):
+        assert should_retrigger(0, kind) is False
+    assert should_retrigger(1) is True
+    # run_skill zero-edit rows: a verified finding outside the diff applies nothing
+    # (the finding-ungroundable.json shape, T-ZERO-EDIT-NO-PUSH).
+    ungroundable = Finding(
+        path="src/legacy/helper.py",
+        line=5,
+        body="no applicable edit",
+        in_diff=False,
+        verification_status="verified",
+        comment_id=4242,
+    )
+    result = run_skill(
+        RunConfig(monitor_ordinal=3, max_rounds=max_rounds, findings=[ungroundable])
+    )
+    assert result.applied_edits == 0
+    assert result.push_count == 0
+    assert result.rereview_request_count == 0
diff --git a/tests/pr_submit/test_conflicts_core.py b/tests/pr_submit/test_conflicts_core.py
index 7b17541d..6368025e 100644
--- a/tests/pr_submit/test_conflicts_core.py
+++ b/tests/pr_submit/test_conflicts_core.py
@@ -31,6 +31,7 @@ from __future__ import annotations
 import ast
 import base64
 import itertools
+import json
 from pathlib import Path
 
 import pytest
@@ -55,7 +56,11 @@ from superclaude.pr_submit.conflicts import (
     parse_probe,
     parse_stage_records,
 )
-from superclaude.pr_submit.fsm import evaluate_push_decision, push_parent_ok
+from superclaude.pr_submit.fsm import (
+    build_push_triad,
+    evaluate_push_decision,
+    push_parent_ok,
+)
 from superclaude.pr_submit.models import MonitorState
 
 FIXTURE = Path(__file__).parent / "fixtures" / "merge_tree_conflict.z"
@@ -2256,6 +2261,183 @@ def test_resume_planners_are_pure():
     assert (repr(state), repr(dangling)) == snapshot
 
 
+# ---------------------------------------------------------------------------
+# Triad (fsm.build_push_triad keyword-only extras, design section 6.1 item 6)
+# ---------------------------------------------------------------------------
+
+# Captured from the pre-#305 build_push_triad (fsm.py:238-288) for _TRIAD_ARGS with
+# the authorized evaluate_push_decision below, before the function was edited.
+_RECORDED_TRIAD = [
+    {
+        "event_type": "push_decision",
+        "round_counter": 0,
+        "authorized": True,
+        "predicates": {
+            "p1_ordinal": True,
+            "p2_validated": True,
+            "p3_no_human": True,
+            "p4_under_cap": True,
+            "p5_applied_edits": 1,
+        },
+        "run_id": "run-1",
+        "cycle_id": "c1",
+        "idempotency_key": "push:run-1:c1:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:feat/x",
+        "pre_push_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
+        "target_sha": "cccccccccccccccccccccccccccccccccccccccc",
+        "target_branch": "feat/x",
+        "target_remote": "origin",
+    },
+    {
+        "event_type": "push_initiated",
+        "remote_ref": "origin/feat/x",
+        "run_id": "run-1",
+        "cycle_id": "c1",
+        "idempotency_key": "push:run-1:c1:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:feat/x",
+        "pre_push_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
+        "target_sha": "cccccccccccccccccccccccccccccccccccccccc",
+        "target_branch": "feat/x",
+        "target_remote": "origin",
+    },
+    {
+        "event_type": "push_completed",
+        "run_id": "run-1",
+        "cycle_id": "c1",
+        "idempotency_key": "push:run-1:c1:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:feat/x",
+        "pre_push_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
+        "target_sha": "cccccccccccccccccccccccccccccccccccccccc",
+        "target_branch": "feat/x",
+        "target_remote": "origin",
+    },
+]
+
+_TRIAD_ARGS = {
+    "run_id": "run-1",
+    "cycle_id": "c1",
+    "round_counter": 0,
+    "pre_push_sha": SHA_A,
+    "target_sha": SHA_C,
+    "target_branch": "feat/x",
+    "target_remote": "origin",
+}
+
+
+def _fix_decision():
+    return evaluate_push_decision(
+        monitor_ordinal=3,
+        validation_status="validated",
+        needs_human_decision=False,
+        round_counter=0,
+        max_rounds=2,
+        applied_edits=1,
+    )
+
+
+def _sync_decision(tier=1):
+    return c.evaluate_sync_decision(
+        monitor_ordinal=3,
+        validation_status="validated",
+        tier=tier,
+        conflict_max_tier=2,
+        halt_reason=None,
+        prior_conflict_cycles=0,
+        round_counter=0,
+        max_rounds=2,
+    )
+
+
+def test_triad_default_call_is_byte_identical_to_recorded_output():
+    out = build_push_triad(**_TRIAD_ARGS, decision=_fix_decision())
+    assert out == _RECORDED_TRIAD
+    # Key order too: the JSONL bytes the run log writes are unchanged.
+    assert json.dumps(out) == json.dumps(_RECORDED_TRIAD)
+
+
+def test_triad_explicit_none_extras_equal_the_default_call():
+    out = build_push_triad(
+        **_TRIAD_ARGS,
+        decision=_fix_decision(),
+        push_kind=None,
+        base_sha=None,
+        review_terminal=None,
+        expect_checks=None,
+    )
+    assert json.dumps(out) == json.dumps(_RECORDED_TRIAD)
+
+
+def test_triad_sync_call_adds_kind_base_and_push_extras():
+    decision = _sync_decision(tier=1)
+    out = build_push_triad(
+        **{**_TRIAD_ARGS, "cycle_id": "sync-1"},
+        decision=decision,
+        push_kind="sync",
+        base_sha=SHA_B,
+        review_terminal="clean",
+        expect_checks=True,
+    )
+    assert [r["event_type"] for r in out] == [
+        "push_decision",
+        "push_initiated",
+        "push_completed",
+    ]
+    for record in out:
+        assert record["kind"] == "sync"
+        assert record["base_sha"] == SHA_B
+        # kind and base_sha follow target_remote.
+        keys = list(record)
+        assert keys[keys.index("target_remote") + 1 :] == ["kind", "base_sha"]
+    dec, init, done = out
+    assert "review_terminal" not in dec and "expect_checks" not in dec
+    assert list(init)[:4] == [
+        "event_type",
+        "remote_ref",
+        "review_terminal",
+        "expect_checks",
+    ]
+    assert init["review_terminal"] == "clean" and init["expect_checks"] is True
+    assert "review_terminal" not in done
+    assert done["expect_checks"] is True
+    assert dec["authorized"] is True
+
+
+def test_triad_sync_decision_yields_the_four_p_predicates():
+    decision = _sync_decision(tier=2)
+    out = build_push_triad(
+        **_TRIAD_ARGS, decision=decision, push_kind="merge", base_sha=SHA_B
+    )
+    assert out[0]["predicates"] == {
+        "p1_ordinal": True,
+        "p2_validated": True,
+        "p3_tier_allowed": True,
+        "p4_under_cap": True,
+    }
+    assert out[0]["predicates"] == decision.audit_predicates
+    assert out[0]["predicates"] is not decision.audit_predicates
+    assert all(r["kind"] == "merge" for r in out)
+    assert "expect_checks" not in out[1] and "review_terminal" not in out[1]
+
+
+def test_triad_each_optional_extra_is_independent():
+    out = build_push_triad(**_TRIAD_ARGS, decision=_fix_decision(), push_kind="fix")
+    assert all(r["kind"] == "fix" and "base_sha" not in r for r in out)
+    out = build_push_triad(**_TRIAD_ARGS, decision=_fix_decision(), expect_checks=False)
+    assert out[1]["expect_checks"] is False and out[2]["expect_checks"] is False
+    assert all("kind" not in r for r in out)
+
+
+@pytest.mark.parametrize("kind", ["", "Sync", "rebase", "push", 1])
+def test_triad_invalid_push_kind_raises(kind):
+    with pytest.raises(ValueError):
+        build_push_triad(**_TRIAD_ARGS, decision=_fix_decision(), push_kind=kind)
+
+
+def test_triad_decision_of_neither_shape_raises_attribute_error():
+    class _Shapeless:
+        authorized = True
+
+    with pytest.raises(AttributeError):
+        build_push_triad(**_TRIAD_ARGS, decision=_Shapeless())
+
+
 # ---------------------------------------------------------------------------
 # Purity
 # ---------------------------------------------------------------------------
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t5-tests.log b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t5-tests.log
new file mode 100644
index 00000000..0d42f845
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t5-tests.log
@@ -0,0 +1,67 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 1487 items
+
+tests/pr_submit/test_auggie_fallback.py ............                     [  0%]
+tests/pr_submit/test_augment_review_remediation.py .......               [  1%]
+tests/pr_submit/test_autonomy_gates.py ........                          [  1%]
+tests/pr_submit/test_ci_classify.py ....................                 [  3%]
+tests/pr_submit/test_codex_reviews.py .................................. [  5%]
+..........................                                               [  7%]
+tests/pr_submit/test_conflicts_core.py ................................. [  9%]
+........................................................................ [ 14%]
+........................................................................ [ 19%]
+........................................................................ [ 23%]
+........................................................................ [ 28%]
+........................................................................ [ 33%]
+........................................................................ [ 38%]
+........................................................................ [ 43%]
+........................................................................ [ 48%]
+........................................................................ [ 52%]
+........................................................................ [ 57%]
+..................                                                       [ 59%]
+tests/pr_submit/test_contract_setup_diagnosis.py ..............          [ 59%]
+tests/pr_submit/test_contract_setup_evidence.py .....................    [ 61%]
+tests/pr_submit/test_contract_setup_pr_submit_integration.py ......      [ 61%]
+tests/pr_submit/test_contract_setup_questions.py .........               [ 62%]
+tests/pr_submit/test_contract_setup_validation.py .............          [ 63%]
+tests/pr_submit/test_contract_setup_writer.py ................           [ 64%]
+tests/pr_submit/test_cosmos_poll.py .................................... [ 66%]
+...............................................................          [ 71%]
+tests/pr_submit/test_cosmos_protocol.py ...............                  [ 72%]
+tests/pr_submit/test_cosmos_review.py .................................. [ 74%]
+........................................................................ [ 79%]
+....                                                                     [ 79%]
+tests/pr_submit/test_crash_recovery.py ................                  [ 80%]
+tests/pr_submit/test_detection_contract.py ............................. [ 82%]
+.....                                                                    [ 82%]
+tests/pr_submit/test_edge_cases.py ...................                   [ 84%]
+tests/pr_submit/test_finding_verify.py ...                               [ 84%]
+tests/pr_submit/test_gate_helper_coverage.py ...........                 [ 85%]
+tests/pr_submit/test_gate_helper_differentials.py ...................... [ 86%]
+                                                                         [ 86%]
+tests/pr_submit/test_idempotency.py ......                               [ 86%]
+tests/pr_submit/test_loop_guard.py ................                      [ 87%]
+tests/pr_submit/test_monitor_arm.py ...                                  [ 88%]
+tests/pr_submit/test_pre_pr_checks.py .................................. [ 90%]
+.....                                                                    [ 90%]
+tests/pr_submit/test_rate_limit.py ....                                  [ 91%]
+tests/pr_submit/test_reply_resolve.py ..........                         [ 91%]
+tests/pr_submit/test_review_retrigger.py .......                         [ 92%]
+tests/pr_submit/test_run_log.py ............                             [ 93%]
+tests/pr_submit/test_setup_questions_resolution.py ....                  [ 93%]
+tests/pr_submit/test_severity_router.py ............................     [ 95%]
+tests/pr_submit/test_silence.py .................                        [ 96%]
+tests/pr_submit/test_skill_parse.py ...............                      [ 97%]
+tests/pr_submit/test_static_grep.py ...................                  [ 98%]
+tests/pr_submit/test_timeout.py .....                                    [ 98%]
+tests/pr_submit/test_troubleshoot_seed.py ....                           [ 99%]
+tests/pr_submit/test_validated_not_verified.py ...                       [ 99%]
+tests/pr_submit/test_validation_gate.py .........                        [100%]
+
+============================ 1487 passed in 18.33s =============================
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t5-fsm-diff.txt b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t5-fsm-diff.txt
new file mode 100644
index 00000000..99018579
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t5-fsm-diff.txt
@@ -0,0 +1,97 @@
+diff --git a/src/superclaude/pr_submit/fsm.py b/src/superclaude/pr_submit/fsm.py
+index 2f310a4f..58c9ed97 100644
+--- a/src/superclaude/pr_submit/fsm.py
++++ b/src/superclaude/pr_submit/fsm.py
+@@ -36,0 +37 @@ DEFAULT_SILENCE_TIMEOUT = 300
++DEFAULT_CONFLICT_MAX_TIER = 1
+@@ -65,0 +67 @@ class SkillArgs:
++    conflict_max_tier: int = DEFAULT_CONFLICT_MAX_TIER
+@@ -98,0 +101,7 @@ def build_arg_parser() -> argparse.ArgumentParser:
++    parser.add_argument(
++        "--conflict-max-tier",
++        dest="conflict_max_tier",
++        type=int,
++        choices=[0, 1, 2],
++        default=DEFAULT_CONFLICT_MAX_TIER,
++    )
+@@ -133,0 +143 @@ def parse_args(argv: list[str]) -> SkillArgs:
++        conflict_max_tier=ns.conflict_max_tier,
+@@ -221,0 +232,9 @@ def push_fail_state(decision: PushDecision) -> MonitorState:
++def should_retrigger(applied_edits: int, push_kind: str | None = None) -> bool:
++    """S5a re-trigger rule: a cycle that applied grounded edits, or a Tier 2
++    merge cycle (push kind "merge"), which applies no finding edit but publishes
++    authored code that the reviewers must see (issue #305, P2)."""
++    return (
++        isinstance(applied_edits, int) and applied_edits > 0
++    ) or push_kind == "merge"
++
++
+@@ -247,0 +267,4 @@ def build_push_triad(
++    push_kind: str | None = None,
++    base_sha: str | None = None,
++    review_terminal: str | None = None,
++    expect_checks: bool | None = None,
+@@ -256,0 +280,11 @@ def build_push_triad(
++
++    Issue #305: the four keyword-only extras default to ``None``; with all four
++    ``None`` the output is byte-identical to the pre-#305 records. ``push_kind``
++    (one of ``fix``, ``merge``, ``sync``, ``ci``; anything else raises
++    :class:`ValueError`) and ``base_sha`` join every record after ``target_remote``;
++    ``review_terminal`` and ``expect_checks`` join ``push_initiated`` after
++    ``remote_ref``, and ``expect_checks`` joins ``push_completed``, each only when
++    not ``None``. A :class:`PushDecision` keeps its five-key predicate dict; any
++    other decision supplies ``audit_predicates`` (the conflict sync gate, read by
++    attribute so this module never imports the conflict core). A decision with
++    neither shape raises :class:`AttributeError`.
+@@ -257,0 +292,2 @@ def build_push_triad(
++    if push_kind is not None and push_kind not in ("fix", "merge", "sync", "ci"):
++        raise ValueError(f"unknown push_kind: {push_kind!r}")
+@@ -267,0 +304,21 @@ def build_push_triad(
++    if push_kind is not None:
++        common["kind"] = push_kind
++    if base_sha is not None:
++        common["base_sha"] = base_sha
++    if isinstance(decision, PushDecision):
++        predicates = {
++            "p1_ordinal": decision.predicate_1_ordinal,
++            "p2_validated": decision.predicate_2_validated,
++            "p3_no_human": decision.predicate_3_no_human,
++            "p4_under_cap": decision.predicate_4_under_cap,
++            "p5_applied_edits": decision.predicate_5_applied_edits,
++        }
++    else:
++        predicates = dict(decision.audit_predicates)
++    initiated_extra: dict = {}
++    if review_terminal is not None:
++        initiated_extra["review_terminal"] = review_terminal
++    completed_extra: dict = {}
++    if expect_checks is not None:
++        initiated_extra["expect_checks"] = expect_checks
++        completed_extra["expect_checks"] = expect_checks
+@@ -273,7 +330 @@ def build_push_triad(
+-            "predicates": {
+-                "p1_ordinal": decision.predicate_1_ordinal,
+-                "p2_validated": decision.predicate_2_validated,
+-                "p3_no_human": decision.predicate_3_no_human,
+-                "p4_under_cap": decision.predicate_4_under_cap,
+-                "p5_applied_edits": decision.predicate_5_applied_edits,
+-            },
++            "predicates": predicates,
+@@ -284,0 +336 @@ def build_push_triad(
++            **initiated_extra,
+@@ -287 +339 @@ def build_push_triad(
+-        {"event_type": "push_completed", **common},
++        {"event_type": "push_completed", **completed_extra, **common},
+@@ -748,0 +801,9 @@ def transition(
++    if edge == (MonitorState.S2_CLASSIFY, "conflicting"):
++        # Issue #305 (P2): a Tier 2 merge cycle at C-initial. Same round gate as
++        # findings; then the G-edit ceiling (S3_FIXING at L2+, else PROPOSED).
++        if should_halt_rounds(
++            int(ctx.get("round_counter", 0)),
++            int(ctx.get("max_rounds", DEFAULT_MAX_ROUNDS)),
++        ):
++            return MonitorState.HALT_MAX_ROUNDS
++        return MonitorState.S3_FIXING if gate_edit(ordinal) else MonitorState.PROPOSED
+@@ -1137 +1198 @@ def run_skill(config: RunConfig | None = None, **overrides) -> SkillResult:
+-        if result.applied_edits > 0:
++        if should_retrigger(result.applied_edits):
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t5-triad-pre-change.txt b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t5-triad-pre-change.txt
new file mode 100644
index 00000000..7a197460
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t5-triad-pre-change.txt
@@ -0,0 +1,33 @@
+[{'event_type': 'push_decision',
+  'round_counter': 0,
+  'authorized': True,
+  'predicates': {'p1_ordinal': True,
+                 'p2_validated': True,
+                 'p3_no_human': True,
+                 'p4_under_cap': True,
+                 'p5_applied_edits': 1},
+  'run_id': 'run-1',
+  'cycle_id': 'c1',
+  'idempotency_key': 'push:run-1:c1:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:feat/x',
+  'pre_push_sha': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
+  'target_sha': 'cccccccccccccccccccccccccccccccccccccccc',
+  'target_branch': 'feat/x',
+  'target_remote': 'origin'},
+ {'event_type': 'push_initiated',
+  'remote_ref': 'origin/feat/x',
+  'run_id': 'run-1',
+  'cycle_id': 'c1',
+  'idempotency_key': 'push:run-1:c1:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:feat/x',
+  'pre_push_sha': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
+  'target_sha': 'cccccccccccccccccccccccccccccccccccccccc',
+  'target_branch': 'feat/x',
+  'target_remote': 'origin'},
+ {'event_type': 'push_completed',
+  'run_id': 'run-1',
+  'cycle_id': 'c1',
+  'idempotency_key': 'push:run-1:c1:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:feat/x',
+  'pre_push_sha': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
+  'target_sha': 'cccccccccccccccccccccccccccccccccccccccc',
+  'target_branch': 'feat/x',
+  'target_remote': 'origin'}]
+[['event_type', 'round_counter', 'authorized', 'predicates', 'run_id', 'cycle_id', 'idempotency_key', 'pre_push_sha', 'target_sha', 'target_branch', 'target_remote'], ['event_type', 'remote_ref', 'run_id', 'cycle_id', 'idempotency_key', 'pre_push_sha', 'target_sha', 'target_branch', 'target_remote'], ['event_type', 'run_id', 'cycle_id', 'idempotency_key', 'pre_push_sha', 'target_sha', 'target_branch', 'target_remote']]

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
