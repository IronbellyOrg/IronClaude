499e149a33ef63db13e4960e37214eaeb62c09f2
Review one task for spec compliance.

Task brief: ## Task 5: Pin the command-file wording in test_worker_contract.py

Depends on: Task 3

In `tests/skills/test_worker_contract.py`, `UNATTENDED_EXPECT["brainstorm"]` is the entry that starts at line 286; its `phrases` list opens at line 288 and holds `research enrichment is off`, `exactly as passed`, `never reused`, `nested/analyze-`, `nested/adversarial-` and `dry-run`.

First, before editing, save the output of `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_worker_contract.py -p no:cacheprovider --collect-only -q -k brainstorm` to `./artifacts/t5-collect-before.txt`. Today the summary line reports 17 collected cases, but that number is not a constant; the saved file is the baseline.

Then add the two phrases `writes no nested directory and no nested contract` and ``only by a `/sc:analyze` call`` to that `phrases` list. The removed-token tests (`_removals`, built from `UNATTENDED_EXPECT`) pick up both phrases and add one case for each; do not add a separate mutation by hand. The mutation list near line 711 (lines 704 to 724) rewrites a made-up section and does not read the real brainstorm text, so it needs no change.

Acceptance criteria:
- `UNATTENDED_EXPECT["brainstorm"]["phrases"]` in `tests/skills/test_worker_contract.py` contains `writes no nested directory and no nested contract` and ``only by a `/sc:analyze` call``.
- The collect-only command above, run again after the edit, reports a collected count equal to the count in `./artifacts/t5-collect-before.txt` plus 2; the plan does not hard-code that number.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_worker_contract.py -q -p no:cacheprovider` passes.
- `git show HEAD:src/superclaude/commands/brainstorm.md | grep -c 'writes no nested directory and no nested contract'` prints 0, and `git cat-file -e HEAD:src/superclaude/commands/brainstorm.md` exits 0, which shows the new phrase fails on the pre-change command file.
Global constraints: ## Constraints

- Background: the P1 live check lc10 failed because the codebase-enrichment wave ran on `quality_tier: fallback_1` (the auggie tool was not available in the worker session) and wrote no `nested/analyze-1/` directory, while the live plan expected one. The owner decided on 2026-11-05 that the check wording was wrong, not the worker. The archived record is in `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/` (`artifacts/lc10-result.md`, `artifacts/p1-owner-decisions-20261105.md`); those files are read, never edited.
- This plan replaces two earlier plans for the same work, packages `TASK-WF-brainstormFixBri-20261106-001016` and `TASK-WF-brainstormFixBri-20261106-021737`. An independent review found the first not ready to run (its Task 6 wording decided the nested folder by `quality_tier`, its Task 7 status check could not pass on the current tree, and the owner rule was not fully pinned). A second review found that the second plan's live-check sentence required the folder whenever any `Skill`, `Agent` or `Task` call passed the flag text, so a `Task` prompt followed by an auggie or `fallback_1` scan would fail a correct run; the owner amended the brief's Part 4 on 2026-11-06 and this plan carries the amended text. Both earlier packages are left as they are.
- Edit only these six files: `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`, `src/superclaude/commands/brainstorm.md`, `tests/skills/test_brainstorm_protocol.py`, `tests/skills/test_worker_contract.py` and `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. `make sync-dev` also rewrites the gitignored copies under `.claude/`; those are output, not edits, and are never staged.
- `src/superclaude/` is the source of truth. `plugins/superclaude/commands/brainstorm.md` is a copy that already differs from the `src` file, and no test requires the two to match (`tests/commands/test_routing_plugin_parity.py` covers only the `sc-recommend` skill). It is not edited. This is this plan's resolution of spec open item 8 for `brainstorm.md`. Task 7 confirms nothing under `plugins/` changed.
- No new text in the installed files (the skill, its refs, the command file) may name a `src/superclaude/` path or an Orca command; `tests/skills/test_worker_contract.py` (`_check_unattended_section`) fails on both.
- UV for every Python command: `uv run pytest ...`, `uv run python ...`. Test runs use `-p no:cacheprovider` and `PYTHONDONTWRITEBYTECODE=1`. No `superclaude install` (the owner updates the installed copies under `~/.claude/` later). No git commit, push, merge or PR.
- The edits reach the next live plan only after the owner commits and merges them; this plan does not commit.
- Open conflict, no change planned here: from phase P2 brainstorm's research enrichment also passes a nested report directory, and the research-deep fallback is itself a nested command. The corrected wording covers only the codebase-enrichment wave. This is an open conflict for the owner and the P2 live-plan author.
- Starting state: the working tree already holds uncommitted edits to `src/superclaude/cli/install_core.py` and `tests/cli/test_how_we_work_install.py` that are not part of this work, and a staged archive of the earlier live plan under `.dev/tasks/done/`. Task 1 records this state before any edit and Task 7 compares against it.
Start sha: 499e149a33ef63db13e4960e37214eaeb62c09f2
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t5-checks.txt b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t5-checks.txt
new file mode 100644
index 00000000..78985e58
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t5-checks.txt
@@ -0,0 +1,15 @@
+== collect before
+=============== 17/394 tests collected (377 deselected) in 0.05s ===============
+== collect after
+=============== 19/396 tests collected (377 deselected) in 0.08s ===============
+== new cases
+== phrases present in UNATTENDED_EXPECT brainstorm
+10:            "writes no nested directory and no nested contract",
+11:            "only by a `/sc:analyze` call",
+== HEAD brainstorm.md count (expect 0)
+0
+== cat-file -e
+exit=0
+== ruff
+All checks passed!
+ruff_exit=0
diff --git a/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t5-collect-after.txt b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t5-collect-after.txt
new file mode 100644
index 00000000..31743f82
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t5-collect-after.txt
@@ -0,0 +1,35 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 396 items / 377 deselected / 19 selected
+
+<Dir OrcaCLICommandRefactor-P1>
+  <Package tests>
+    <Package skills>
+      <Module test_worker_contract.py>
+        <Function test_unattended_section_content[brainstorm]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:flag:--output]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:flag:-o]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:flag:--interactive]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:flag:-i]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:phrase:research enrichment is off]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:phrase:exactly as passed]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:phrase:never reused]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:phrase:nested/analyze-]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:phrase:nested/adversarial-]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:phrase:dry-run]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:phrase:writes no nested directory and no nested contract]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:phrase:only by a `/sc:analyze` call]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:nested:nested/analyze-]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:nested:nested/adversarial-]>
+        <Function test_ac_1_4_assertion_holds[brainstorm-section]>
+        <Function test_ac_1_4_check_fails_when_phrase_removed[brainstorm-section:research enrichment is off]>
+        <Function test_nested_propagation_text_matches_the_nested_list[brainstorm]>
+        <Function test_only_brainstorm_lists_nested_commands>
+
+=============== 19/396 tests collected (377 deselected) in 0.08s ===============
+exit=0
diff --git a/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t5-collect-before.txt b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t5-collect-before.txt
new file mode 100644
index 00000000..023d5752
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t5-collect-before.txt
@@ -0,0 +1,33 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 394 items / 377 deselected / 17 selected
+
+<Dir OrcaCLICommandRefactor-P1>
+  <Package tests>
+    <Package skills>
+      <Module test_worker_contract.py>
+        <Function test_unattended_section_content[brainstorm]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:flag:--output]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:flag:-o]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:flag:--interactive]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:flag:-i]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:phrase:research enrichment is off]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:phrase:exactly as passed]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:phrase:never reused]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:phrase:nested/analyze-]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:phrase:nested/adversarial-]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:phrase:dry-run]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:nested:nested/analyze-]>
+        <Function test_unattended_section_check_fails_when_token_removed[brainstorm:nested:nested/adversarial-]>
+        <Function test_ac_1_4_assertion_holds[brainstorm-section]>
+        <Function test_ac_1_4_check_fails_when_phrase_removed[brainstorm-section:research enrichment is off]>
+        <Function test_nested_propagation_text_matches_the_nested_list[brainstorm]>
+        <Function test_only_brainstorm_lists_nested_commands>
+
+=============== 17/394 tests collected (377 deselected) in 0.05s ===============
+exit=0
diff --git a/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t5-pytest.log b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t5-pytest.log
new file mode 100644
index 00000000..3cf2be0f
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t5-pytest.log
@@ -0,0 +1,19 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 396 items
+
+tests/skills/test_worker_contract.py ................................... [  8%]
+........................................................................ [ 27%]
+........................................................................ [ 45%]
+........................................................................ [ 63%]
+........................................................................ [ 81%]
+........................................................................ [ 99%]
+.                                                                        [100%]
+
+============================= 396 passed in 0.69s ==============================
+exit=0
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index 06c13334..94ab3caa 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -292,6 +292,8 @@ UNATTENDED_EXPECT: dict = {
             "nested/analyze-",
             "nested/adversarial-",
             "dry-run",
+            "writes no nested directory and no nested contract",
+            "only by a `/sc:analyze` call",
         ],
         "nested": ["analyze", "adversarial"],
     },
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
