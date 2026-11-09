90b0e63ddb160d55b332ea9efc74fd82dd2d7278
Review one task for spec compliance.

Task brief: ## Task 7: Update the existing protocol tests for the new contract

Depends on: Task 3, Task 4, Task 5, Task 6

Edit `tests/skills/test_issue_protocol.py`. Source section: 3.2 "Existing tests to update". In `test_st10_claim_return_contract_has_the_ten_fields_and_keeps_the_old_ones` (around lines 492 to 520) the Return contract section now holds three YAML blocks: change `len(blocks) == 2` to 3, keep the first two key lists exactly as they are, add an assertion that the third block's keys equal `["issue_type", "complexity_field", "classification_missing"]`, and assert that the sentence "Create mode adds these three fields after the claim block" is present in the section. Keep the existing assertion that claim mode's block says "create mode prints none of them". Re-run the Will / Will Not test (`test_skill_will_and_will_not_match_the_command_file`, line 527) and the five-ref inventory tests (lines 209 to 216, 233, 277); they must pass unchanged. Search the file for any other assertion on the old label wording ("fixed set", "type:", "complexity:", "relabelled") and update only those.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_protocol.py -v` passes with the updated return-contract test.
- The updated test fails if the third YAML block is removed or a key is renamed (confirmed by reading the assertions: exact list equality, not a subset check).
- No test asserts the old label wording, and the five-ref inventory tests still count exactly five refs.

AC ids:
T7.AC1: `uv run pytest tests/skills/test_issue_protocol.py -v` passes with the updated return-contract test.
T7.AC2: The updated test fails if the third YAML block is removed or a key is renamed (confirmed by reading the assertions: exact list equality, not a subset check).
T7.AC3: No test asserts the old label wording, and the five-ref inventory tests still count exactly five refs.
Global constraints: - Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`. Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits.
- Text inside the skill, command and agent files must not contain the string `src/superclaude/` (an installed-path rule; a test scans the skill folder for it).
- Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`. No file may contain a brace placeholder for owner and repo; use `<owner>` and `<R>`.
- `--claim` behaviour and text stay unchanged, including its two-block part of the return contract. The T1 and T2 worker files, `refs/tiers.md`, `scripts/*.py` and the four issue-body templates stay unchanged.
- The skill never creates a label, an issue type or an issue field. It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST).
- Nothing in this plan writes to GitHub while it is executed. The POST body, the `--type` flag and the silent-drop behaviour come from GitHub's docs and `gh` help and are UNVERIFIED by a real run; Task 12 leaves the owner a manual check for that.
- Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit.
- Decisions taken as defaults (the owner may reverse them later): the T3 worker may read exactly `orgs/<owner of R>/issue-fields`; the `--type` area flag and its 11 values stay but no longer produce a label; the `bug` / `enhancement` mode labels stay.
Start sha: 90b0e63ddb160d55b332ea9efc74fd82dd2d7278
Diff against the start snapshot: 
diff --git a/tests/skills/test_issue_protocol.py b/tests/skills/test_issue_protocol.py
index 678e7f4e..6e4a17f1 100644
--- a/tests/skills/test_issue_protocol.py
+++ b/tests/skills/test_issue_protocol.py
@@ -493,7 +493,7 @@ def test_st10_claim_return_contract_has_the_ten_fields_and_keeps_the_old_ones():
     skill = _text(SKILL)
     section = skill.split("## Return contract", 1)[1].split("## Error handling", 1)[0]
     blocks = re.findall(r"```yaml\n(.*?)```", section, re.S)
-    assert len(blocks) == 2
+    assert len(blocks) == 3
     assert _yaml_keys(blocks[0]) == [
         "status",
         "mode",
@@ -517,7 +517,13 @@ def test_st10_claim_return_contract_has_the_ten_fields_and_keeps_the_old_ones():
         "launch_warning",
         "enforcement_hook",
     ]
+    assert _yaml_keys(blocks[2]) == [
+        "issue_type",
+        "complexity_field",
+        "classification_missing",
+    ]
     assert "create mode prints none of them" in section
+    assert "Create mode adds these three fields after the claim block" in section
 
 
 def test_st11_no_source_tree_path_in_the_command_file():

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
