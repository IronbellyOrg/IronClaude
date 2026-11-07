43df7a52349eaeccdd73172163b0d02c0be5ba6e
Review one task for spec compliance.

Task brief: ## Task 6: Add the `--merge-guard` flag

Depends on: Task 1

Edit `src/superclaude/pr_submit/fsm.py` following ./source.md section 4.3: `DEFAULT_MERGE_GUARD = "draft"`, a `--merge-guard` argument with `dest="merge_guard"` and `choices=["draft", "off"]` placed beside `--conflict-max-tier` in `build_arg_parser`, `SkillArgs.merge_guard: str = DEFAULT_MERGE_GUARD`, and `parse_args` passing `ns.merge_guard`. Leave `RunConfig` and `run_skill` unchanged. Add a test beside `test_conflict_max_tier_default_and_bounds` in `tests/pr_submit/test_skill_parse.py`.

Acceptance criteria:
- T6.AC1: `parse_args([]).merge_guard == "draft"`, `parse_args(["--merge-guard", "off"]).merge_guard == "off"`, `SkillArgs().merge_guard == "draft"`, and `--merge-guard label` exits with an argparse error (`SystemExit`).
- T6.AC2: `fsm.py` still contains no whole word `gh` or `git` (the static purity test passes) and every existing test in `tests/pr_submit/test_skill_parse.py` and `tests/pr_submit/test_autonomy_gates.py` passes unchanged.
Global constraints: - Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files. Use UV for every Python command (`uv run pytest ...`, `uv run ruff ...`).
- The new pure module `src/superclaude/pr_submit/merge_guard.py` and every file already listed in `CORE_PURE_FILES` of `tests/pr_submit/test_static_grep.py` (including `refs/state-machine.md` and `refs/loop-guard.md`) must contain no whole word `gh` or `git` on any line, comments included. The module must not import `recovery` (an import cycle through `run_log`).
- Protocol and command text must not contain the string `src/superclaude`; `SKILL.md` must keep exactly one python code fence; edits to `SKILL.md` and `refs/state-machine.md` are additive sentences, bullets and rows placed after, never inside, the sentences pinned by `tests/pr_submit/test_static_grep.py` and `tests/pr_submit/test_conflict_sync_protocol.py`. A new `SKILL.md` line must not name `evidence-validator` or `conflict-intent.md` (a line-content test allows those words only on lines that also say "Tier 2") and must not use wording that the forbidden-force-push line test rejects; Task 1 lists the exact line-content rules before any edit.
- Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superclaude/agents/` that contains `gh pr`, `gh api` or a git write verb needs one entry in `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py` (key: repo-relative path, verb text, exact stripped line; category `never-worker` with the standard pr-submit reason text of the neighbouring entries). Add each entry last in the task that writes the file, because editing a classified line later makes the entry stale and fails `test_classification_table_has_no_stale_entries`; run `uv run pytest tests/skills/test_worker_contract.py -q` in that task.
- Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, `CORE_PURE_FILES`, `WRITE_VERB_CLASSIFICATION`), never by line number, in plan text, task artifacts and the protocol prose this plan produces. Protocol prose carries no `file:NNN` pointers.
- No test or task may call GitHub. Script tests use a fake `gh` executable on `PATH`. The behaviour that needs a disposable fork PR (gates G1 live part, G2 live part, G4, G5 and G6 of ./source.md section 8) is recorded as OPEN and is a release gate, never claimed verified.
- Scope limits (non-goals of ./source.md): no labels, commit statuses or rulesets; ordinals 0 to 2 change only by one report line; conflict-merge cycles (Tier 1 and Tier 2) are never engaged; the guard is not held through re-review or CI; a second concurrent run on the same PR is unsupported.
- Owner decisions already accepted (listed in the ./source.md header and section 8) are fixed: draft not label; engage at the end of Wave 3; default on at `--monitor 3`; release on the confirmed push before replies and the re-trigger; unreadable timeline or unpublished exit keeps the PR draft; build now with no GitHub calls, release gate for G4 and G5.
- Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/`, because the full test suite runs `make verify-sync` through `tests/cli/test_verify_sync_hooks.py`.
Start sha: 43df7a52349eaeccdd73172163b0d02c0be5ba6e
Diff against the start snapshot: diff --git a/src/superclaude/pr_submit/fsm.py b/src/superclaude/pr_submit/fsm.py
index 00f85990..da314303 100644
--- a/src/superclaude/pr_submit/fsm.py
+++ b/src/superclaude/pr_submit/fsm.py
@@ -37,6 +37,9 @@ DEFAULT_SILENCE_TIMEOUT = 300
 # Tier 1 (`uv lock`) can run the PR's build code, so it is opt-in: the default
 # is detect-and-report only (PR #378 finding C5).
 DEFAULT_CONFLICT_MAX_TIER = 0
+# Issue #375: at --monitor 3 the merge guard holds the PR as a draft while a fix
+# cycle runs. The flag is accepted and inert below ordinal 3; ``off`` disables it.
+DEFAULT_MERGE_GUARD = "draft"
 
 POLL_INTERVAL_ERROR = "minimum is 30 seconds"
 MAX_ROUNDS_ERROR = "--max-rounds hard cap is 5"
@@ -67,6 +70,7 @@ class SkillArgs:
     resume: str | None = None
     pr: int | None = None
     conflict_max_tier: int = DEFAULT_CONFLICT_MAX_TIER
+    merge_guard: str = DEFAULT_MERGE_GUARD
 
     @property
     def armed(self) -> bool:
@@ -107,6 +111,12 @@ def build_arg_parser() -> argparse.ArgumentParser:
         choices=[0, 1, 2],
         default=DEFAULT_CONFLICT_MAX_TIER,
     )
+    parser.add_argument(
+        "--merge-guard",
+        dest="merge_guard",
+        choices=["draft", "off"],
+        default=DEFAULT_MERGE_GUARD,
+    )
     return parser
 
 
@@ -143,6 +153,7 @@ def parse_args(argv: list[str]) -> SkillArgs:
         resume=ns.resume,
         pr=ns.pr,
         conflict_max_tier=ns.conflict_max_tier,
+        merge_guard=ns.merge_guard,
     )
 
 

diff --git a/tests/pr_submit/test_skill_parse.py b/tests/pr_submit/test_skill_parse.py
index f34c8de5..0de87e01 100644
--- a/tests/pr_submit/test_skill_parse.py
+++ b/tests/pr_submit/test_skill_parse.py
@@ -13,6 +13,7 @@ import pytest
 from superclaude.pr_submit.fsm import (
     DEFAULT_CONFLICT_MAX_TIER,
     DEFAULT_MAX_ROUNDS,
+    DEFAULT_MERGE_GUARD,
     DEFAULT_MONITOR,
     DEFAULT_TIMEOUT,
     POLL_INTERVAL_ERROR,
@@ -117,3 +118,20 @@ def test_conflict_max_tier_default_and_bounds():
     for bad in ("3", "x"):
         with pytest.raises(SystemExit):
             parse_args(["--conflict-max-tier", bad])
+
+
+def test_merge_guard_default_and_choices():
+    """Issue #375: `--merge-guard` defaults to `draft`, accepts `draft` and `off`
+    at any `--monitor` ordinal, and rejects every other value."""
+    assert parse_args([]).merge_guard == DEFAULT_MERGE_GUARD == "draft"
+    assert SkillArgs().merge_guard == "draft"
+    assert parse_args(["--merge-guard", "off"]).merge_guard == "off"
+    assert parse_args(["--merge-guard", "draft"]).merge_guard == "draft"
+    for ordinal in (0, 1, 2, 3):
+        args = parse_args(["--monitor", str(ordinal), "--merge-guard", "off"])
+        assert (args.monitor, args.merge_guard) == (ordinal, "off")
+    for bad in ("label", "on", "", "OFF"):
+        with pytest.raises(SystemExit):
+            parse_args(["--merge-guard", bad])
+    with pytest.raises(SystemExit):
+        parse_args(["--merge-guard"])

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
