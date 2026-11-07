ccf70dbebc8311f1c98d0210bef93ea3c4e3f5e4
Review one task for spec compliance.

Task brief: ## Task 6: Add the text-presence test for the Review Loop

Depends on: Task 2
Depends on: Task 4
Depends on: Task 5

Create `tests/skills/test_spec_panel_review_loop.py` following section 9 of ./source.md. Import `CANONICAL_CAP_TEXT` and `AT_CAP_CLAUSES` from `tests.skills.test_review_severity_rule`; define a local whitespace flatten (`" ".join(text.split())`); resolve the repo root with `Path(__file__).resolve().parents[2]`. Parametrize over the two spec-panel files (`src/superclaude/commands/spec-panel.md`, `plugins/superclaude/commands/spec-panel.md`) for tests T1 to T9 (Usage tail, section position, seven single-line bullets in order, cap literals, vocabulary literals, project-first rf-qa lookup literal, the three literals from the spec review, the precedence sentence, no `src/superclaude` inside the section). Add test T10 for the guide sentence: in both HOW-WE-WORK copies the line containing `It only reports.` contains `--re-review`, `--baseline` and `save a copy of the PRD`, and `until no critical findings remain` appears in neither HOW-WE-WORK copy nor in the two release guides. Do not assert that the whole `spec-panel.md` lacks a `src/superclaude` path (line 218 names one).

Acceptance criteria:
- `uv run pytest tests/skills/test_spec_panel_review_loop.py` passes; output saved to ./artifacts/t6-new-test.log.
- Each literal is its own assertion or parametrized case. One mutation run is recorded in ./artifacts/t6-mutation.log: back up `src/superclaude/commands/spec-panel.md` to ./artifacts/, delete the phrase `never fall back to a first review` from the real file, run the new test and see only the matching case fail, then restore the file from the backup and confirm with `cmp` that it is identical to the backup.
- `uv run ruff format --check` with the repo's pinned ruff and `make lint` report no problem for the new test file.


AC ids in source order: T6.AC1 = bullet 1, T6.AC2 = bullet 2, T6.AC3 = bullet 3 of the Acceptance criteria block.
Evidence files (cite as ./artifacts/<name>), all in /home/coder/workspaces/worktrees/IronClaude/issue-346-review-loop-convergence/.dev/tasks/to-do/TASK-WF-specPanelReviewL-20261107-090418/artifacts/: t6-new-test.log, t6-mutation.log, t6-lint.log, spec-panel.md.backup (the backup copy).
Note: the mutation run happened before the new test file was reformatted with the pinned ruff (formatting only, no assertion changed); t6-new-test.log and t6-lint.log were regenerated after the reformat.
The design test table (source section 9) is in /home/coder/workspaces/worktrees/IronClaude/issue-346-review-loop-convergence/.dev/tasks/to-do/TASK-WF-specPanelReviewL-20261107-090418/source.md.
Global constraints: ## Constraints

- Edit canonical files under `src/superclaude/` and the named `plugins/superclaude/` mirrors by hand; run `make sync-dev` afterwards. Never stage anything under `.claude/`. Stage `.dev/tasks` with the work.
- Do not change `src/superclaude/output-styles/pragmatic.md`, any `sc-implement-protocol` file, or `WORKER-CONTRACT.md`. Do not touch `docs/user-guide/flags.md` or `commands/sc-help.md` (the generic `--iterations` rows).
- The literal bullet text comes from section 5 of ./source.md and must be copied byte for byte; each bullet is ONE line. If an existing matcher in `tests/skills/test_review_severity_rule.py` flags a bullet, change the minimum wording and keep the literals the new test asserts (source section 9, T3 to T8), updating the test in the same change.
- Installed primitives must not name `src/superclaude/` paths. Do not add a size limit, a monotonic halt or an installer change (source section 11).
- Handoff notes for the pull request, not tasks: the body uses `Refs` for issue 346 (the causal link is unproven), and it says that the new command text reaches an existing host only after `superclaude install --force` or `update`.
Start sha: ccf70dbebc8311f1c98d0210bef93ea3c4e3f5e4
Diff against the start snapshot: git status for the task files: tests/skills/test_spec_panel_review_loop.py is new (untracked); src/superclaude/commands/spec-panel.md is unchanged by this task (restored from backup, cmp identical).

diff --git a/tests/skills/test_spec_panel_review_loop.py b/tests/skills/test_spec_panel_review_loop.py
new file mode 100644
index 00000000..d4ab0c7c
--- /dev/null
+++ b/tests/skills/test_spec_panel_review_loop.py
@@ -0,0 +1,174 @@
+"""Static pins for the /sc:spec-panel ``## Review Loop`` section (issue 346).
+
+Enforcement type: STATIC - assertions over the text of the two spec-panel
+copies, the two routing-guide copies and the two release guides. They prove the
+text is present and in the right order, not that a reviewer obeys it.
+"""
+
+from __future__ import annotations
+
+import re
+from pathlib import Path
+
+import pytest
+
+from tests.skills.test_review_severity_rule import AT_CAP_CLAUSES, CANONICAL_CAP_TEXT
+
+_REPO = Path(__file__).resolve().parents[2]
+
+SPEC_PANELS = (
+    "src/superclaude/commands/spec-panel.md",
+    "plugins/superclaude/commands/spec-panel.md",
+)
+HOW_WE_WORK = (
+    "src/superclaude/core/HOW-WE-WORK.md",
+    "plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md",
+)
+RELEASE_GUIDES = (
+    "docs/guides/prd-skill-release-guide.md",
+    "docs/guides/tdd-skill-release-guide.md",
+)
+HEADING = "## Review Loop"
+BULLET_NAMES = (
+    "Mode",
+    "Grading",
+    "Verdict",
+    "Cap",
+    "Re-review output",
+    "Reviser contract",
+    "Precedence",
+)
+OLD_SENTENCE = "until no critical findings remain"
+
+
+def _flat(text: str) -> str:
+    return " ".join(text.split())
+
+
+def _lines(rel: str) -> list[str]:
+    return (_REPO / rel).read_text(encoding="utf-8").splitlines()
+
+
+def _section_lines(rel: str) -> list[str]:
+    """Raw lines between the Review Loop heading and the next ``## `` heading."""
+    lines = _lines(rel)
+    start = lines.index(HEADING) + 1
+    end = next(
+        (i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines)
+    )
+    return lines[start:end]
+
+
+def _section(rel: str) -> str:
+    return _flat("\n".join(_section_lines(rel)))
+
+
+spec_panel = pytest.mark.parametrize("rel", SPEC_PANELS)
+
+
+@spec_panel
+def test_t1_usage_line_names_the_re_review_flags(rel):
+    usage = next(line for line in _lines(rel) if line.startswith("/sc:spec-panel "))
+    assert "[--re-review <prior-findings-file> --baseline <saved-copy>]" in _flat(usage)
+
+
+@spec_panel
+def test_t2_section_exists_once_before_output_formats(rel):
+    lines = _lines(rel)
+    assert lines.count(HEADING) == 1
+    assert lines.index(HEADING) < lines.index("## Output Formats")
+
+
+@spec_panel
+def test_t3_seven_single_line_bullets_in_order(rel):
+    body = [line for line in _section_lines(rel) if line.strip()]
+    bullets = [line for line in body if re.match(r"^[1-7]\. \*\*", line)]
+    assert body == bullets, (
+        "every non-blank line of the section must be one of the seven bullets"
+    )
+    assert [re.match(r"^(\d)\. \*\*([^*]+)\*\*", b).groups() for b in bullets] == [
+        (str(i), name) for i, name in enumerate(BULLET_NAMES, start=1)
+    ]
+
+
+CAP_LITERALS = (CANONICAL_CAP_TEXT, AT_CAP_CLAUSES[1])
+VOCABULARY = (
+    "resolved|open|regressed",
+    "origin=changed|unchanged",
+    "verdict: PASS",
+    "verdict: FAIL",
+    "review: N of 3",
+    "Reviser brief",
+    "byte size before and after",
+)
+LOOKUP_ORDER = (
+    "the project `.claude/agents/rf-qa.md` first, else `~/.claude/agents/rf-qa.md`"
+)
+SPEC_REVIEW_FIXES = (
+    "ignores `--iterations`",
+    "`regressed` = a finding the prior report marked resolved that fails again",
+    "never fall back to a first review",
+)
+PRECEDENCE = (
+    "a brief may narrow this scope; it may not widen it past the changed lines and the prior blocking findings, "
+    "and may not grade a minor finding as blocking"
+)
+
+
+@spec_panel
+@pytest.mark.parametrize("literal", CAP_LITERALS, ids=["t4-cap-text", "t4-at-cap-halt"])
+def test_t4_cap(rel, literal):
+    assert literal in _section(rel)
+
+
+@spec_panel
+@pytest.mark.parametrize(
+    "literal", VOCABULARY, ids=[f"t5-{i}" for i in range(len(VOCABULARY))]
+)
+def test_t5_vocabulary(rel, literal):
+    assert literal in _section(rel)
+
+
+@spec_panel
+def test_t6_project_rf_qa_lookup_comes_first(rel):
+    section = _section(rel)
+    assert LOOKUP_ORDER in section
+    assert section.index(".claude/agents/rf-qa.md") < section.index(
+        "~/.claude/agents/rf-qa.md"
+    )
+
+
+@spec_panel
+@pytest.mark.parametrize(
+    "literal",
+    SPEC_REVIEW_FIXES,
+    ids=["t7-iterations", "t7-regressed", "t7-no-first-review"],
+)
+def test_t7_spec_review_fixes(rel, literal):
+    assert literal in _section(rel)
+
+
+@spec_panel
+def test_t8_precedence_sentence(rel):
+    assert PRECEDENCE in _section(rel)
+
+
+@spec_panel
+def test_t9_section_names_no_source_path(rel):
+    # Scoped to the section: the whole file names one such path elsewhere and must not be asserted.
+    assert "src/superclaude" not in _section(rel)
+
+
+@pytest.mark.parametrize("rel", HOW_WE_WORK)
+@pytest.mark.parametrize(
+    "literal", ("--re-review", "--baseline", "save a copy of the PRD")
+)
+def test_t10_routing_guide_sentence_carries_the_new_flags(rel, literal):
+    reporting = [line for line in _lines(rel) if "It only reports." in line]
+    assert reporting, "routing guide lost the 'It only reports.' sentence"
+    assert all(literal in _flat(line) for line in reporting)
+
+
+@pytest.mark.parametrize("rel", HOW_WE_WORK + RELEASE_GUIDES)
+def test_t10_old_sentence_is_gone(rel):
+    assert OLD_SENTENCE not in _flat("\n".join(_lines(rel)))

(artifact ./artifacts/t6-new-test.log):
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
SuperClaude: 5.0.0
rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-346-review-loop-convergence
configfile: pyproject.toml
plugins: superclaude-5.0.0, anyio-4.16.0
collected 46 items

tests/skills/test_spec_panel_review_loop.py ............................ [ 60%]
..................                                                       [100%]

============================== 46 passed in 0.10s ==============================
exit=0

(artifact ./artifacts/t6-mutation.log):
backup: .dev/tasks/to-do/TASK-WF-specPanelReviewL-20261107-090418/artifacts/spec-panel.md.backup
occurrences before: 1
occurrences after mutation: 0
FAILED tests/skills/test_spec_panel_review_loop.py::test_t7_spec_review_fixes[t7-no-first-review-src/superclaude/commands/spec-panel.md]
========================= 1 failed, 45 passed in 0.11s =========================
restore: cmp identical (exit 0)
occurrences after restore: 1

(artifact ./artifacts/t6-lint.log):
pinned ruff (pyproject.toml ruff==0.15.20): ruff 0.15.20
1 file already formatted
format-check exit=0
All checks passed!
pinned-check exit=0
Running linter...
uv run ruff check .
All checks passed!
make-lint exit=0
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
