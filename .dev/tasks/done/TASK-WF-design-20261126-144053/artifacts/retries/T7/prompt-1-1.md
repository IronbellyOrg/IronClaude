54bac7420ae38add9f17af63f76ad374803f2568
Review one task for spec compliance.

Task brief: ## Task 7: Add the guide, mirror and onboarding tests to the policy file

Depends on: Task 6

In `tests/core/test_how_we_work_worktree_policy.py` add the helper `_section()` (the text of the guide from the line `## Worktrees and branches` up to the next line that starts with `## `; it fails with a clear message when the heading is missing or appears more than once) and the tests of section 5 of `./source.md` that read the repository files: `test_section_exists_once_before_orca_coordination`, `test_section_is_at_most_400_words`, `test_section_is_pure_ascii_and_has_no_banned_phrase`, `test_section_states_each_rule` (parametrized over the fifteen key phrases listed in Task 1), `test_every_backticked_branch_example_in_the_section_passes` (at least one example exists), `test_deletion_is_detected` (removes one key phrase from a copy of the section and asserts the check reports it), `test_mirror_is_byte_identical`, `test_pointer_names_the_section` and `test_deck_card_is_replaced_and_neighbours_untouched` (it asserts what Task 4's first acceptance bullet states, which overrides `./source.md` line 106, a page-wide absence check that cannot pass) (D-1). These tests read `src/superclaude/core/HOW-WE-WORK.md`, the mirror and `docs/onboarding/ironclaude-onboarding.html` as changed by Tasks 1 to 5.

Acceptance criteria:
T7.AC1: `uv run pytest tests/core/test_how_we_work_worktree_policy.py -v` passes and lists the thirteen tests of section 5 of `./source.md` (the four from Task 6 and the nine added here, the parametrized ones counted once each).
T7.AC2: Removing any one of the fifteen key phrases from a copy of the guide section makes `test_section_states_each_rule`'s check report it, and `test_deletion_is_detected` proves that.
T7.AC3: `uv run pytest tests/core/test_how_we_work_worktree_policy.py tests/core/test_how_we_work_routing_table.py tests/core/test_claude_md_worktree_rule.py tests/core/test_orca_session_launch_guidance.py tests/core/test_claude_md_routing_block.py tests/docs/test_onboarding_deck.py tests/commands/test_worktrees_command.py tests/commands/test_help_command.py tests/commands/test_routing_plugin_parity.py tests/skills/test_review_prompt_overrides.py tests/skills/test_sc_recommend_routing_contract.py tests/skills/test_issue_protocol.py tests/skills/test_review_brief_placement.py tests/skills/test_spec_panel_review_loop.py tests/cli/test_how_we_work_install.py tests/recommend -q` passes.
T7.AC4: `uv run ruff check tests/core/test_how_we_work_worktree_policy.py` and `uv run ruff format --check tests/core/test_how_we_work_worktree_policy.py` pass.
T7.AC5: From the repository root, `git status --short -- . ':(top,exclude).dev'` lists only the guide, the mirror, the onboarding page and the new test file; `git diff --cached --name-only | grep -E '^(\.claude/|\.dev/issues/)'` prints nothing; `git status --short -- .dev/tasks` lists only paths under `.dev/tasks` (a plain `git status --short` is not used because the untracked `.dev/` folders are always listed) (D-2).
Global constraints: ## Constraints

- Scope is five deliverables: the new guide section and the removal-timing pointer in `src/superclaude/core/HOW-WE-WORK.md`, the byte-identical mirror `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, the worktree card and build footer of `docs/onboarding/ironclaude-onboarding.html`, and the new `tests/core/test_how_we_work_worktree_policy.py`. No production code changes.
- Out of scope: the claim launcher and its `issue-<N>` naming, the cleanup script and its rules, the issue watcher, the `CLAUDE.md` examples at lines 318-341, the issue 290 card, the slide introduction at lines 516-518, and any tool that extracts lessons. Section 1 of `./source.md` lists them.
- The open owner questions of section 7 of `./source.md` (dropping the words from a name, lessons of issue-less worktrees, whether the watcher or the claim should refuse an issue that already has a worktree, the slide introduction, the `CLAUDE.md` examples, the footer rule) are not decided by this plan and are not written into the guide. They belong in the pull request body.
- The guide is a shared file: the level-table, routing-table and other-commands marker comments and every other section stay as they are, and every line the change adds is ASCII (plain hyphens, no en dashes).
- The mirror is never edited by hand: it is a copy of the guide after the guide's last edit.
- Python and tests run through uv (`uv run pytest`, `uv run ruff`); never `python -m` or bare `pip`.
- The tasks run in a straight line and the new test file comes last (the design's section 6 puts it first) so that the acceptance criteria of every task can pass the moment that task is done.
- Stage the changed files and `.dev/tasks`; never stage anything under `.claude/` or `.dev/issues/`. Staging is not committing.
- Where this plan and `./source.md` disagree this plan wins: it overrides source.md line 106 (page-wide absence of "is being worked out in") and lines 53 and 108 (the list of 13 key phrases, now 15), as stated in Tasks 1, 4 and 7 (D-1, D-3).
Start sha: 54bac7420ae38add9f17af63f76ad374803f2568
Diff against the start snapshot: --- a/tests/core/test_how_we_work_worktree_policy.py
+++ b/tests/core/test_how_we_work_worktree_policy.py
@@ -114,3 +114,115 @@
     if expected >= 1:
         assert branch_errors(f"{bare}-{'b' * expected}") == []
         assert branch_errors(f"{bare}-{'b' * (expected + 1)}")
+
+
+_SECTION_HEADING = "## Worktrees and branches"
+_ORCA_HEADING = "## Orca coordination"
+_BANNED_PHRASES = [
+    "Every verb is a dry run",
+    "every verb is a dry run",
+    "Verbs (a dry run unless --apply is given)",
+]
+# One exact phrase per rule of the section; each occurs once in it.
+_KEY_PHRASES = [
+    "new worktree and branch",
+    "One writer per worktree",
+    "original worktree while it still exists",
+    "--ff-only",
+    "stop and ask",
+    "/sc:issue --claim",
+    "at most 24 characters",
+    "no spaces",
+    "no run of 2 to 4 digits",
+    "create nothing and ask the owner",
+    "Lessons comment",
+    "pins the worktree",
+    "checks that comment first",
+    "is exempt",
+    "handoff of unfinished work",
+]
+
+
+def _section() -> str:
+    """The guide from the section heading up to the next line that starts with `## `."""
+    lines = _GUIDE.read_text(encoding="utf-8").splitlines()
+    starts = [i for i, line in enumerate(lines) if line == _SECTION_HEADING]
+    assert len(starts) == 1, (
+        f"the guide needs exactly one {_SECTION_HEADING!r} line, found {len(starts)}"
+    )
+    end = next(
+        (i for i in range(starts[0] + 1, len(lines)) if lines[i].startswith("## ")),
+        len(lines),
+    )
+    return "\n".join(lines[starts[0] : end])
+
+
+def _missing_phrases(section: str) -> list[str]:
+    """The key phrases that a section text does not contain."""
+    return [phrase for phrase in _KEY_PHRASES if phrase not in section]
+
+
+def test_section_exists_once_before_orca_coordination():
+    section = _section()  # fails unless the heading occurs exactly once
+    lines = _GUIDE.read_text(encoding="utf-8").splitlines()
+    assert lines.index(_SECTION_HEADING) < lines.index(_ORCA_HEADING)
+    assert "<!--" not in section
+
+
+def test_section_is_at_most_400_words():
+    assert len(_section().split()) <= 400
+
+
+def test_section_is_pure_ascii_and_has_no_banned_phrase():
+    section = _section()
+    assert section.isascii()
+    assert [phrase for phrase in _BANNED_PHRASES if phrase in section] == []
+
+
+@pytest.mark.parametrize("phrase", _KEY_PHRASES)
+def test_section_states_each_rule(phrase):
+    section = _section()
+    assert phrase not in _missing_phrases(section)
+    assert section.count(phrase) == 1
+
+
+def test_every_backticked_branch_example_in_the_section_passes():
+    examples = re.findall(r"`([^`<>]*/issue-[^`<>]*)`", _section())
+    assert examples, "the section needs at least one backticked branch example"
+    for example in examples:
+        assert branch_errors(example) == [], example
+
+
+@pytest.mark.parametrize("phrase", _KEY_PHRASES)
+def test_deletion_is_detected(phrase):
+    section = _section()
+    assert _missing_phrases(section) == []
+    assert _missing_phrases(section.replace(phrase, "")) == [phrase]
+
+
+def test_mirror_is_byte_identical():
+    assert _GUIDE.read_bytes() == _TWIN.read_bytes()
+
+
+def test_pointer_names_the_section():
+    rows = [
+        line
+        for line in _GUIDE.read_text(encoding="utf-8").splitlines()
+        if line.startswith("| `/sc:worktrees` |")
+    ]
+    assert len(rows) == 1
+    assert "Worktrees and branches" in rows[0]
+    assert "item 4 of issue 289" not in rows[0]
+
+
+def test_deck_card_is_replaced_and_neighbours_untouched():
+    deck = _DECK.read_text(encoding="utf-8")
+    assert "Worktree and branch protocol" in deck
+    assert "clayphi/issue-289-wtrule" in deck
+    assert "how they are named is being worked out" not in deck
+    assert "issues/289" not in deck
+    sentences = [line for line in deck.splitlines() if "is being worked out in" in line]
+    assert len(sentences) == 1
+    assert "issues/290" in sentences[0]
+    assert "Contributing rules" in deck
+    assert re.search(r"Built from HOW-WE-WORK\.md at commit [0-9a-f]{7,40}\b", deck)


Codegraph context
index_state: fresh
checked_at: 2026-11-26T14:52:15Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-289
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-289
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents (floor: Grep): the test file reads src/superclaude/core/HOW-WE-WORK.md, plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md and docs/onboarding/ironclaude-onboarding.html, all changed by Tasks 1 to 5; nothing imports the test file. The full related-suite list of this task ran: 688 passed (artifacts/t7-suites.log); the file alone: 61 cases of 13 tests passed (artifacts/t7-policy-tests.log). Context only.

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