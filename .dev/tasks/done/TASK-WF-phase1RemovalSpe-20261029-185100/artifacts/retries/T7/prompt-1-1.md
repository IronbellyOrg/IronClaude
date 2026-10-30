0cb8c606fcfa93ec905015048ed099f3879071d5
Review one task for spec compliance.

Task brief: ## Task 7: Remove Serena tokens from the reflect verdict contract

Depends on: Task 6

Implements ./source.md §8 T6, rule G7, rule G8 and rows S42-S44, S58-S86. In `src/superclaude/cli/reflect/contract.py` drop `"serena"` and `"serena:context-excluded"` from `_DEGRADED_COMPONENTS_HALT_SET` and fix the comment (`:28-34`), removing every Serena token from it including `get_current_config` at `:30` (Task 12's repo-wide search and Task 18's residual search both reject it); delete the `serena_summary_corroboration` key in `src/superclaude/cli/reflect/ensemble.py:824` and its line in the 24 fixtures listed as S58-S82 (except S65); delete `tests/cli/reflect/fixtures/degraded_serena.yaml`; in `degraded_with_drift.yaml` replace `- serena` with `- auggie`; delete `test_degraded_serena` and `test_serena_summary_corroboration_unavailable_not_degraded` and edit the token list at `tests/cli/reflect/test_verdict_mapping.py:245`; repoint `tests/cli/reflect/test_runner_e2e.py:71` to `degraded_tier1.yaml` and keep its exit-11 assertion; reword `src/superclaude/cli/reflect/config.py:162,199`, `tests/cli/reflect/test_ensemble_unit.py:345`, `tests/cli/reflect/test_verify_denylist_git_mutations.py:11`. Commit `refactor(reflect): drop Serena tokens and the serena_summary_corroboration field from the verdict contract (#323)`.

Acceptance criteria:
- T7.AC1: `uv run pytest tests/cli/reflect -q -p no:cacheprovider` passes (W2 predicts about 270 tests).
- T7.AC2: `rg -n -i 'serena' src/superclaude/cli/reflect tests/cli/reflect` prints nothing and `rg -n 'get_current_config' src/superclaude/cli/reflect` prints nothing.

`$PKG` = /home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init/.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100 (repo root: the git top-level of that directory). The source spec for anything the brief says is in `$PKG/source.md`; the plan is `$PKG/TASK-WF-phase1RemovalSpe-20261029-185100.md`.

Global constraints (plan `## Constraints`, verbatim):
- Work on branch `ironbelly/feat-codememory-codegraph-init`, base commit `55d40308`. Do not open a pull request to `master` for Phase 1 alone and do not push to `upstream`; Phases 1 and 2 merge as one unit (./source.md §2.2, D9).
- `$PKG` in every command below means this package's directory as the executor resolves it at run time (the folder that holds this plan); never hardcode it. Evidence goes under `$PKG/artifacts/`; handoff notes for other repos go under `$PKG/handoffs/`.
- One commit per task, conventional commit message as given in each task, ending with the attribution line the executor's session requires. Every commit stages the task package with `git add .dev/tasks` (package, `progress.md` and `artifacts/` included). Never stage or commit `.claude/` content (only `.claude/settings.json` is tracked, and Phase 1 does not touch it). Never use `git add -f` on a `.claude/` path.
- Every edit to a `src/superclaude/...` primitive is mirrored by hand, in the same commit, in its `plugins/superclaude/...` twin and its root `commands/sc-*.md` / `agents/sc-*.md` copy where ./source.md §1.2 lists one (D15).
- After editing `src/superclaude/core/HOW-WE-WORK.md`, copy it byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; if the edit touches the block between `<!-- level-table:v1 -->` and `<!-- /level-table -->`, re-copy that block into `src/superclaude/core/CLAUDE.md`.
- Use `uv run` for Python; standalone scripts run with `uv run --no-project python -I`. Every pytest run uses `-p no:cacheprovider`. Full-suite runs always set `T02_15_PERF_REPORT=/tmp/p1-perf.json` so the tracked `.dev/releases/current/cliEval/evidence/T02.15/perf.json` is not rewritten. After every test run, `git status --short` must list only files the task intends to change; restore any tracked file a test changed.
- Test baseline: the full suite already has failures at the base (W1 saw 27 failed and 16 errors). "Passes" for a targeted command means no failing test id that is not in `$PKG/artifacts/baseline/full.txt` (compare with the `comm -13` form in Task 18); never assume a clean suite.
- Never run the real `./update.sh`, `superclaude install` (including `--list`) or `claude mcp add/remove` against the real `HOME`; every environment check runs in a sandbox `HOME` made with `mktemp -d` (./source.md §10, D8). Never delete user data (`~/.serena`, project `.serena/` folders outside this repo, `~/.cache/codebase-memory-mcp`). Never edit another repository.
- Progress reporting (./source.md §9): at the end of each task group (Phases 1-6 below, i.e. groups G0-G5) post exactly one comment on issue #323 of the fork, and only there. First run `gh repo view --json nameWithOwner -q .nameWithOwner` (must print `IronbellyOrg/IronClaude`; otherwise run `gh repo set-default IronbellyOrg/IronClaude`), then `gh issue comment 323 --repo IronbellyOrg/IronClaude --body "Phase 1 progress: <group id and name> committed on ironbelly/feat-codememory-codegraph-init at <short sha>. Tasks: <task ids>. Checks: <exact commands> -> <result>. Decisions logged: <count, path in task package>. Next: <next group>."`. Never use a bare `gh issue comment` and never `--repo SuperClaude-Org/...`. If `gh` is unauthenticated or fails, record the exact error and the intended body in `$PKG/progress.md` and continue (not a blocker).
- Decision rules (./source.md §10), never stop to ask the user: a simple decision (one obvious option, or one the source already constrains) is made by the executor and logged as one line in `$PKG/decisions.md` (decision, options, method `self`, rationale). A mid-level decision (two or more viable options with real trade-offs inside one task) writes each option to `$PKG/decisions/<task>-<slug>/option-<x>.md`, spawns an agent that runs `/sc:adversarial --compare <option files> --depth quick`, follows its recommendation and logs method `adversarial quick` with the merged-recommendation path. A complex decision (an architectural change to the source's design: retire-step scope, memory store layout, merge order, deleting a file the source keeps) does the same with `/sc:adversarial --compare <option files>` (standard depth) and logs method `adversarial full`.
- A blocked task stays blocked with its reason in `$PKG/progress.md`; continue with tasks that do not depend on it. If a task's acceptance fails, fix it within the task's files; if the fix needs a file another task owns, pull that edit forward and log it in `$PKG/decisions.md`. A task may not need a later task to go green.
- Scope limits (./source.md §2.1, §2.3): existing `.dev/` files outside `$PKG` are never edited; the only other `.dev/` writes are the new files `.dev/codegraph-migration/handoffs/phase3-codegraph-slots.md` and `.dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md`, and each task that writes one stages that exact file (`git add <path>`, never the folder). No task uninstalls the `serena-agent` uv tool or removes `~/.local/bin/{serena,serena-agent,serena-hooks}`, the Coder `/usr/local/bin/codebase-memory-mcp` binary, bundle markers, upstream companions or `~/.local/bin/install.sh`; those are handed off, not removed by Phase 1.
- This plan was corrected after an advisory `/sc:reflect --mode pre` review (`.dev/codegraph-migration/review/F1-result.md`). Where a task's text here differs from `./source.md`, the task text wins.
- Human actions the executor must not attempt: merging Phases 1 and 2 to `master` (Phase 2's PR via `/sc:pr-submit`) and running the real `./update.sh` on a live workspace after that merge (Phase 2 owns that live check).
Start sha: 0cb8c606fcfa93ec905015048ed099f3879071d5
Diff against the start snapshot: Touched files: src/superclaude/cli/reflect/{contract,ensemble,config}.py, tests/cli/reflect/{test_verdict_mapping,test_runner_e2e,test_ensemble_unit,test_verify_denylist_git_mutations}.py, 24 fixtures under tests/cli/reflect/fixtures (the serena_summary_corroboration line removed), fixtures/degraded_with_drift.yaml (also '- serena' -> '- auggie'), fixtures/degraded_serena.yaml (deleted). Spec: $PKG/source.md section 8 T6 (lines 698-702) and section 8.1 row T6. Observed by the implementer (verify yourself): uv run pytest tests/cli/reflect gives 269 passed, 1 xpassed; both rg checks print nothing; ruff check and format pass.

 tests/cli/reflect/test_verdict_mapping.py          | 25 +------------------
 .../reflect/test_verify_denylist_git_mutations.py  |  4 ++--
 33 files changed, 12 insertions(+), 88 deletions(-)

diff --git a/src/superclaude/cli/reflect/config.py b/src/superclaude/cli/reflect/config.py
index a4a4e6e0..5e9938b2 100644
--- a/src/superclaude/cli/reflect/config.py
+++ b/src/superclaude/cli/reflect/config.py
@@ -159,7 +159,7 @@ def create_review_snapshot(config) -> tuple[Path | None, str | None]:
     free of any raw ``subprocess`` import (NFR-1 thinness guard). Returns
     ``(snapshot_path, None)`` on success, or ``(None, stop_reason)`` on a
     precondition STOP. NEVER falls back to the live tree. Uses a REAL worktree
-    checkout (NOT an archive) so serena/auggie stay indexed (A-2).
+    checkout (NOT an archive) so auggie stays indexed (A-2).
 
     Lifecycle:
       1. PRE-CLEAN a leftover ``<output>/_review-snapshot`` via ``git worktree
@@ -196,7 +196,7 @@ def create_review_snapshot(config) -> tuple[Path | None, str | None]:
         return (None, "no-committable-ref")
     if current_head != config.head:
         return (None, "head-moved-precondition")
-    # (3) Real worktree checkout (NOT archive) so serena/auggie stay indexed.
+    # (3) Real worktree checkout (NOT archive) so auggie stays indexed.
     config.output_dir.mkdir(parents=True, exist_ok=True)
     try:
         _git(git_cwd, "worktree", "add", "--detach", str(snapshot), current_head)
diff --git a/src/superclaude/cli/reflect/contract.py b/src/superclaude/cli/reflect/contract.py
index 391a577b..52b00bba 100644
--- a/src/superclaude/cli/reflect/contract.py
+++ b/src/superclaude/cli/reflect/contract.py
@@ -26,11 +26,10 @@ from .models import ReflectResult, Verdict
 # ---------------------------------------------------------------------------
 
 # FR-11 chain-critical subset: EXACT membership (NOT substring) so benign
-# fail-open tokens (search_deps:lsp_unindexed, serena:onboarding-parse,
-# serena:pre-v1.5-no-rename-propagation, get_current_config,
-# neighbour-search:auggie_unavailable) do NOT over-HALT.
+# fail-open tokens (search_deps:lsp_unindexed, neighbour-search:auggie_unavailable)
+# do NOT over-HALT.
 _DEGRADED_COMPONENTS_HALT_SET = frozenset(
-    {"serena", "auggie", "env-aliases", "evidence-validator", "serena:context-excluded"}
+    {"auggie", "env-aliases", "evidence-validator"}
 )
 
 # verification_ran == False is exempt (NOT degradation) for these skip reasons.
diff --git a/src/superclaude/cli/reflect/ensemble.py b/src/superclaude/cli/reflect/ensemble.py
index beb9dc0f..a5964ada 100644
--- a/src/superclaude/cli/reflect/ensemble.py
+++ b/src/superclaude/cli/reflect/ensemble.py
@@ -821,7 +821,6 @@ def build_reflect_contract(
         "unauthorized_deviation_present": unauthorized_deviation_present,
         "needs_human_decision": needs_human_decision,
         "user_decision_required": False,  # seam emits no user-decision signal; honest default (R2-F3, supersedes R6 Step 2.5 mirror mandate)
-        "serena_summary_corroboration": "unavailable",
         "degraded_components": degraded_components,
         # L2 reviewer-isolation telemetry (pure telemetry; not verdict-bearing —
         # the STOP happens in the runner before derive_verdict, so audit_tree_dirty
diff --git a/tests/cli/reflect/fixtures/degraded_with_drift.yaml b/tests/cli/reflect/fixtures/degraded_with_drift.yaml
index 0f4931e5..90f73969 100644
--- a/tests/cli/reflect/fixtures/degraded_with_drift.yaml
+++ b/tests/cli/reflect/fixtures/degraded_with_drift.yaml
@@ -23,6 +23,5 @@ regression_present: false
 unauthorized_deviation_present: false
 needs_human_decision: false
 user_decision_required: false
-serena_summary_corroboration: unavailable
 degraded_components:
-  - serena
+  - auggie
diff --git a/tests/cli/reflect/test_ensemble_unit.py b/tests/cli/reflect/test_ensemble_unit.py
index f65c116c..3f49b0d8 100644
--- a/tests/cli/reflect/test_ensemble_unit.py
+++ b/tests/cli/reflect/test_ensemble_unit.py
@@ -342,7 +342,7 @@ def test_u11_build_reflect_contract_threads_regression_fields() -> None:
 def test_r2f2_build_reflect_contract_emits_honest_verification_fields() -> None:
     """R2-F2 (PR#199 round-2): the Tier-2 seam emits honest verification fields.
 
-    The headless Tier-2 ensemble runs NO grounded/serena verification triangle, so
+    The headless Tier-2 ensemble runs NO grounded verification triangle, so
     hard-coding ``verification_ran=True`` was factually false and made the
     ``verification-skipped`` DEGRADE structurally unreachable on every Tier-2
     contract (clean runs bypassed the verification-integrity gate). The seam now
diff --git a/tests/cli/reflect/test_runner_e2e.py b/tests/cli/reflect/test_runner_e2e.py
index 5ae8abc5..15be5fde 100644
--- a/tests/cli/reflect/test_runner_e2e.py
+++ b/tests/cli/reflect/test_runner_e2e.py
@@ -68,7 +68,7 @@ def test_e2e_degraded(
     temp_tasklist, patch_git, patch_runner_env, make_claude_process_stub
 ) -> None:
     config = _config(temp_tasklist)
-    factory = make_claude_process_stub("degraded_serena.yaml", rc=0)
+    factory = make_claude_process_stub("degraded_tier1.yaml", rc=0)
     with patch(_PATCH_TARGET, side_effect=factory) as mock_cls:
         result = ReflectRunner(config).run()
     assert result.verdict is Verdict.DEGRADED
diff --git a/tests/cli/reflect/test_verdict_mapping.py b/tests/cli/reflect/test_verdict_mapping.py
index a0cd720a..c6175d87 100644
--- a/tests/cli/reflect/test_verdict_mapping.py
+++ b/tests/cli/reflect/test_verdict_mapping.py
@@ -90,18 +90,6 @@ def test_halted_regression() -> None:
     assert result.verdict.exit_code == 10
 
 
-def test_degraded_serena() -> None:
-    """degraded_components contains serena -> degraded / exit 11."""
-    result = derive_verdict(
-        _load("degraded_serena.yaml"),
-        expected_tier=2,
-        allow_single_vendor=False,
-        child_rc=0,
-    )
-    assert result.verdict is Verdict.DEGRADED
-    assert result.verdict.exit_code == 11
-
-
 def test_degraded_expected_t2_ran_t1() -> None:
     """status success but tier_reached 1 while expecting 2 -> degraded / 11."""
     result = derive_verdict(
@@ -190,17 +178,6 @@ def test_tolerant_unknown_field_1x() -> None:
     assert result.verdict.exit_code == 0
 
 
-def test_serena_summary_corroboration_unavailable_not_degraded() -> None:
-    """serena_summary_corroboration: unavailable must NOT route to degraded."""
-    contract = _load("pass.yaml")
-    contract["serena_summary_corroboration"] = "unavailable"
-    result = derive_verdict(
-        contract, expected_tier=2, allow_single_vendor=False, child_rc=0
-    )
-    assert result.verdict is Verdict.PASS
-    assert result.verdict.exit_code == 0
-
-
 def test_verification_skip_exemption_not_degraded() -> None:
     """verification_ran False with an exempted skip reason must NOT degrade."""
     contract = _load("pass.yaml")
@@ -242,7 +219,7 @@ def test_benign_degraded_component_does_not_over_halt() -> None:
     contract = _load("pass.yaml")
     contract["degraded_components"] = [
         "search_deps:lsp_unindexed",
-        "serena:onboarding-parse",
+        "neighbour-search:auggie_unavailable",
     ]
     result = derive_verdict(
         contract, expected_tier=2, allow_single_vendor=False, child_rc=0
diff --git a/tests/cli/reflect/test_verify_denylist_git_mutations.py b/tests/cli/reflect/test_verify_denylist_git_mutations.py
index 78e09d97..54059550 100644
--- a/tests/cli/reflect/test_verify_denylist_git_mutations.py
+++ b/tests/cli/reflect/test_verify_denylist_git_mutations.py
@@ -7,8 +7,8 @@ verbs are enumerated as a defense-in-depth backstop, while the pre-existing
 entries (``git commit``/``git push``, ``pip install``, ``rm``) are retained.
 
 L3 is defense-in-depth: control (b)'s allowlist already rejects every git verb
-(closed set, ``git`` absent), and §6.1.1 governs the ``execute_shell_command``/
-serena path, NOT the Bash-tool/L1 incident vector. This test guards the
+(closed set, ``git`` absent), and §6.1.1 governs the verification-envelope
+path, NOT the Bash-tool/L1 incident vector. This test guards the
 denylist TEXT (there is no ``verify`` subcommand to exercise the gate at runtime).
 
 Falsifier discipline: fails-before (the git verbs were absent from the denylist)

Fixture line removals: use: git diff 0cb8c606fcfa93ec905015048ed099f3879071d5 --stat -- tests/cli/reflect/fixtures
Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (none)

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
