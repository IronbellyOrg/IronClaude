45ec8b667454251e6599c1b8e2ae9043577e1d97
Review one task for spec compliance.

Task brief: ## Task 6: Pin the blocker check in tests/skills/test_issue_protocol.py

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5

Edit `tests/skills/test_issue_protocol.py` and add the checks at the end of the file, after `test_stage_claim_skips_recommend_and_plain_claim_keeps_it`, in the style of the existing `plan_section_problems` helper and its mutation tests. Reuse `_text`, `_wave`, `REFS`, `SKILL`, `COMMANDS` and `ROOT` from the top of the file. Add a helper `blocker_check_problems(claim: str) -> list[str]` that returns a list of what is wrong with the claim text: the Wave 2 section lacks `repos/<R>/issues/<N>/dependencies/blocked_by` or `E-BLOCKED`; the blocker item is not after the closed-issue item of Wave 2; the Wave 3 section contains `dependencies/blocked_by` or lacks `--add-assignee`; or the Final output section lacks `Blocker check: could not run`. Add these tests: one that asserts the helper returns an empty list for `REFS / "claim.md"`; one that removes the blocker item from a copy of the claim text (use `tmp_path` or string replacement, never edit the real file) and asserts the helper reports a problem; one that asserts Wave 2 states an open blocker stops with `E-BLOCKED` naming each one and "no GitHub, ClickUp or Orca write", that none or only closed continues as today, and that an unreadable list continues; one (A2) that asserts Wave 2 writes the failure order: a line matching `^#[0-9]+ https://` stops with `E-BLOCKED` whatever the exit status, otherwise a non-zero exit or any non-matching output is "could not run" and the claim continues, otherwise there are no open blockers, with the matching-line rule written before the could-not-run rule; one that asserts `SKILL.md` carries `E-BLOCKED` in its Claim mode list and in the `## Error handling` table together with the `Blocker check: could not run` row; and one that asserts `commands/issue.md` contains `E-BLOCKED` and that the `/sc:issue` row of `src/superclaude/core/HOW-WE-WORK.md` mentions "blocked by" and equals the same row of `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. These static tests pin the written contract; they do not show a live model following it, so name that limit in a one-line comment above the new tests. Task 6 also edits `tests/skills/test_worker_contract.py` (A1): add one `WRITE_VERB_CLASSIFICATION` entry with category `read-only` and a one-line reason, keyed by the exact stripped text of the final line Task 1 adds to `refs/claim.md` that holds the `gh api` call, in the same edit as that line or after it; in Python the jq text `\(` is written `\\(`.

Acceptance criteria (ids added by the orchestrator):
- T6.AC1: `uv run pytest tests/skills/test_issue_protocol.py tests/commands/test_routing_plugin_parity.py -q` passes with the new tests included.
- T6.AC2: Reverting only Task 1's Wave 2 item in a scratch copy makes the helper test report a problem, shown by the mutation test passing.
- T6.AC3: The A2 order test passes, showing `refs/claim.md` Wave 2 states the matching-line rule first, the could-not-run rule second and no open blockers last.
- T6.AC4: The other readers of the changed text still pass: `uv run pytest tests/commands/test_issue_command.py tests/issue_pipeline/test_brief.py tests/issue_watch/test_marker_contract.py tests/skills/test_issue_orca_worktree.py tests/skills/test_worker_contract.py tests/core/test_how_we_work_routing_table.py tests/cli/test_how_we_work_install.py -q` shows no new failure compared with the same run before Task 1.
- T6.AC5: `make lint` reports no error for `tests/skills/test_issue_protocol.py` and `tests/skills/test_worker_contract.py` (A1).
Global constraints: ## Constraints

- Change only what the source asks: the blocker read and `E-BLOCKED` stop in the claim, their description in four places, and the tests. Not the issue watcher, not dependency links, and not any other claim behaviour.
- Edit only the canonical files under `src/superclaude/`, the plugin guide copy and the tests. Do not edit or stage anything under `.claude/`; the generated copies come from `make sync-dev`.
- Inside the skill files and the command file under `src/superclaude/skills/sc-issue-protocol/` and `src/superclaude/commands/issue.md`, never write the text `src/superclaude/` (two existing tests forbid it), never write `{owner}/{repo}`, and keep every `gh api` path spelled `repos/<R>/...`.
- Do not touch the paragraph that begins "Coordinator handoff for `--pipeline none`:"; it must stay identical in `refs/claim.md`, `SKILL.md` and `commands/issue.md`.
- Do not add fields to the claim return contract in `SKILL.md`; a test pins its exact keys. A failed read is reported as one line of the final output.
- `SKILL.md` must stay under 500 lines.
Start sha: 45ec8b667454251e6599c1b8e2ae9043577e1d97
Diff against the start snapshot: 
diff --git a/tests/skills/test_issue_protocol.py b/tests/skills/test_issue_protocol.py
index 3026a7080..3de7aa626 100644
--- a/tests/skills/test_issue_protocol.py
+++ b/tests/skills/test_issue_protocol.py
@@ -1178,3 +1178,150 @@ def test_stage_claim_skips_recommend_and_plain_claim_keeps_it():
     )
     assert "`Default row not used` line is not written" in claim
     assert "a `--stage` claim never calls it" in claim
+
+
+# --- the blocked-by check of the claim (issue 848) ------------------------------------
+# Static tests of the written contract in the skill text. They do not show that a live
+# model follows it.
+
+BLOCKER_PATH = "repos/<R>/issues/<N>/dependencies/blocked_by"
+GUIDE = ROOT / "src/superclaude/core/HOW-WE-WORK.md"
+PLUGIN_GUIDE = ROOT / "plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md"
+
+
+def _wave2_item_lines(claim: str) -> list[str]:
+    return [ln for ln in _wave(claim, 2).splitlines() if re.match(r"^\d+\. ", ln)]
+
+
+def _line_index(lines: list[str], needle: str) -> int | None:
+    return next((i for i, ln in enumerate(lines) if needle in ln), None)
+
+
+def blocker_check_problems(claim: str) -> list[str]:
+    """What is wrong with the blocker check in the text of refs/claim.md (empty: nothing)."""
+    items = _wave2_item_lines(claim)
+    blocker = _line_index(items, BLOCKER_PATH)
+    if blocker is None:
+        return [f"Wave 2 has no item that reads {BLOCKER_PATH}"]
+    problems = []
+    if "E-BLOCKED" not in items[blocker]:
+        problems.append("the Wave 2 blocker item does not name E-BLOCKED")
+    for name, needle in (
+        ("closed-issue", "`state` is `CLOSED`"),
+        ("assigned-to-someone-else", "Assigned to anyone other than"),
+        ("already-assigned", "Already assigned to the current login"),
+    ):
+        index = _line_index(items, needle)
+        if index is None or index > blocker:
+            problems.append(f"the blocker item is not after the {name} item of Wave 2")
+    wave3 = _wave(claim, 3)
+    if BLOCKER_PATH in wave3:
+        problems.append("Wave 3 reads the blocked-by list")
+    if "--add-assignee" not in wave3:
+        problems.append("Wave 3 lost the assignment")
+    if "Blocker check: could not run" not in claim.split("## Final output", 1)[1]:
+        problems.append("the Final output has no could-not-run line rule")
+    return problems
+
+
+def _claim_with_blocker_item_moved(claim: str, after_needle: str | None) -> str:
+    """Copy of the claim text with the blocker item removed, or put after a line."""
+    lines = claim.splitlines(keepends=True)
+    i = next(i for i, ln in enumerate(lines) if ln.startswith("5. Blocker check"))
+    item = lines.pop(i)
+    if after_needle is not None:
+        j = next(j for j, ln in enumerate(lines) if after_needle in ln)
+        lines.insert(j + 1, item)
+    return "".join(lines)
+
+
+def test_blocker_check_in_the_claim_ref_has_no_problems():
+    assert blocker_check_problems(_text(REFS / "claim.md")) == []
+
+
+def test_blocker_check_fails_when_the_item_is_removed():
+    claim = _claim_with_blocker_item_moved(_text(REFS / "claim.md"), None)
+    assert blocker_check_problems(claim)
+
+
+@pytest.mark.parametrize(
+    "after_needle, name",
+    [
+        ("`state` is `CLOSED`", "assigned-to-someone-else"),
+        ("Assigned to anyone other than", "already-assigned"),
+    ],
+)
+def test_blocker_check_fails_when_the_item_sits_before_an_assignee_item(
+    after_needle, name
+):
+    claim = _claim_with_blocker_item_moved(_text(REFS / "claim.md"), after_needle)
+    assert any(f"not after the {name} item" in p for p in blocker_check_problems(claim))
+
+
+def test_blocker_check_fails_when_wave_3_reads_the_list():
+    claim = _text(REFS / "claim.md").replace(
+        "## Wave 3: assign (orchestrator)\n",
+        f"## Wave 3: assign (orchestrator)\n\n{BLOCKER_PATH}\n",
+        1,
+    )
+    assert "Wave 3 reads the blocked-by list" in blocker_check_problems(claim)
+
+
+def test_blocker_check_fails_without_the_final_output_line():
+    head, tail = _text(REFS / "claim.md").split("## Final output", 1)
+    claim = head + "## Final output" + tail.replace("Blocker check: could not run", "x")
+    assert "the Final output has no could-not-run line rule" in blocker_check_problems(
+        claim
+    )
+
+
+def test_wave2_blocker_item_states_the_three_outcomes_in_order():
+    claim = _text(REFS / "claim.md")
+    assert "every STOP here makes no GitHub, ClickUp or Orca write (B9)" in _wave(
+        claim, 2
+    )
+    items = _wave2_item_lines(claim)
+    item = items[_line_index(items, BLOCKER_PATH)]
+    first = item.index("First, any output line that matches `^#[0-9]+ https://`")
+    second = item.index("Second, otherwise a non-zero exit")
+    third = item.index("Third, otherwise there are no open blockers")
+    assert first < second < third
+    # an open blocker stops the claim whatever the exit status, naming each one
+    assert "whatever the exit status" in item[first:second]
+    assert "STOP `E-BLOCKED`" in item[first:second]
+    assert "<each #number and link>" in item[first:second]
+    # an unreadable list continues and is reported in the final output
+    assert "continue" in item[second:third]
+    assert (
+        "Blocker check: could not run (<reason>); the claim went ahead without it."
+        in item[second:third]
+    )
+    # none, or only closed blockers: the claim runs as today
+    assert "continue as today" in item[third:]
+
+
+def test_skill_and_command_describe_the_blocker_stop():
+    skill = _text(SKILL)
+    claim_mode = skill.split("## Claim mode", 1)[1].split("## Create mode", 1)[0]
+    rows = [
+        ln
+        for ln in skill.split("## Error handling", 1)[1].splitlines()
+        if ln.startswith("|")
+    ]
+    assert "E-BLOCKED" in claim_mode
+    assert any("E-BLOCKED" in r and "no writes" in r for r in rows)
+    assert any("Blocker check: could not run" in r for r in rows)
+    assert "E-BLOCKED" in _text(COMMANDS / "issue.md")
+
+
+def _guide_issue_row(path: Path) -> str:
+    return next(
+        ln for ln in _text(path).splitlines() if ln.startswith("| `/sc:issue` |")
+    )
+
+
+def test_guide_row_mentions_the_blocker_check_and_the_plugin_copy_matches():
+    row = _guide_issue_row(GUIDE)
+    assert '"blocked by"' in row
+    assert "does not stop the claim" in row
+    assert row == _guide_issue_row(PLUGIN_GUIDE)
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index 019966285..ad42e1c2f 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -2966,6 +2966,14 @@ WRITE_VERB_CLASSIFICATION = {
         "never-worker",
         "/sc:issue is on the never-as-worker list; its assign, comment and issue writes run only in the coordinator or person session",
     ),
+    (
+        "src/superclaude/skills/sc-issue-protocol/refs/claim.md",
+        "gh api",
+        "5. Blocker check (read only; it runs before the first write of Wave 3): run `gh api --paginate repos/<R>/issues/<N>/dependencies/blocked_by --jq '.[] | select(.state == \"open\") | \"#\\(.number) \\(.html_url)\"'`. Apply the outcomes in this order. First, any output line that matches `^#[0-9]+ https://` is an open blocker, whatever the exit status: STOP `E-BLOCKED`: \"Issue #N is blocked by open issue(s): <each #number and link>; not claimed.\" Second, otherwise a non-zero exit (for example no access or an endpoint that is not served) or any output that does not match means the check could not run: continue, and hold the line `Blocker check: could not run (<reason>); the claim went ahead without it.` for the final output. Third, otherwise there are no open blockers (no output, or only closed ones): continue as today. The check applies to a re-claim and to every `--pipeline` value.",
+    ): (
+        "read-only",
+        "a read: the Wave 2 blocker check is a GET of the issue's blocked-by list, run by the orchestrator before the first write",
+    ),
     (
         "src/superclaude/skills/sc-issue-protocol/refs/claim.md",
         "gh api",

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
