6e0b016b684c58705af408e64706e564c816b50e
Review one task for spec compliance.

Task brief: ## Task 8: Add the new rule tests

Depends on: Task 7

Add tests to `tests/skills/test_issue_protocol.py`, using the file's existing helpers (`_text`, `SKILL`, `REFS`, `TEMPLATES`, `AGENTS`, `SKILL_DIR`) and its conventions. Source section: 3.2 "New tests". Write one test per rule, each failing when the behaviour breaks. First, `labels.md` contains no `type:` label, no `complexity:` label and no `gh label create` line for either. Second, every `orgs/` path found by regex in the skill folder files and the `AGENTS` files equals `orgs/<owner of R>/issue-fields` or `orgs/<owner>/issue-fields` and appears only in `create.md`, `SKILL.md` and `issue-worker-t3.md`. Third, the skill folder and the agents contain `-X POST` together with `issue-field-values` and no `-X PUT`. Fourth, `create.md` and `labels.md` carry the three exact line formats `not applied: label missing in repo:`, `not set: issue type` and `not set: field Complexity`. Fifth, `issue-worker-t3.md` names `issue-types` and `issue-fields`, and `scout-report.md` has the headings `### Repo issue types` and `### Complexity field`. Sixth, `labels.md` states Feature, Bug, Test and Simple, Medium, Complex. Add one self-check test in the style of `test_fork_safety_scan_fails_on_a_ref_without_repo` (line 642) that feeds the `orgs/` scanner a text with `orgs/other/issue-fields` and expects it to be reported.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_protocol.py -v` passes and the new tests are collected (the count of collected tests rises by at least seven).
- Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red: each new test asserts on the text that task adds.
- The existing fork-safety scans (`test_every_gh_issue_pr_label_mention_carries_repo`, `test_no_brace_placeholder`, `test_no_source_tree_path_in_skill_files`) still pass.

AC ids:
T8.AC1: `uv run pytest tests/skills/test_issue_protocol.py -v` passes and the new tests are collected (the count of collected tests rises by at least seven).
T8.AC2: Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red: each new test asserts on the text that task adds.
T8.AC3: The existing fork-safety scans (`test_every_gh_issue_pr_label_mention_carries_repo`, `test_no_brace_placeholder`, `test_no_source_tree_path_in_skill_files`) still pass.
Global constraints: - Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`. Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits.
- Text inside the skill, command and agent files must not contain the string `src/superclaude/` (an installed-path rule; a test scans the skill folder for it).
- Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`. No file may contain a brace placeholder for owner and repo; use `<owner>` and `<R>`.
- `--claim` behaviour and text stay unchanged, including its two-block part of the return contract. The T1 and T2 worker files, `refs/tiers.md`, `scripts/*.py` and the four issue-body templates stay unchanged.
- The skill never creates a label, an issue type or an issue field. It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST).
- Nothing in this plan writes to GitHub while it is executed. The POST body, the `--type` flag and the silent-drop behaviour come from GitHub's docs and `gh` help and are UNVERIFIED by a real run; Task 12 leaves the owner a manual check for that.
- Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit.
- Decisions taken as defaults (the owner may reverse them later): the T3 worker may read exactly `orgs/<owner of R>/issue-fields`; the `--type` area flag and its 11 values stay but no longer produce a label; the `bug` / `enhancement` mode labels stay.
Start sha: 6e0b016b684c58705af408e64706e564c816b50e
Diff against the start snapshot: 
diff --git a/tests/skills/test_issue_protocol.py b/tests/skills/test_issue_protocol.py
index 6e4a17f1..964ac37a 100644
--- a/tests/skills/test_issue_protocol.py
+++ b/tests/skills/test_issue_protocol.py
@@ -668,3 +668,130 @@ def test_no_source_tree_path_in_skill_files():
         if "src/superclaude/" in text:
             hits.append(str(path.relative_to(ROOT)))
     assert hits == []
+
+
+# --- issue type and Complexity field (issue 438) -------------------------------------
+
+AGENT_T3 = AGENTS[0]
+_ALLOWED_ORGS = re.compile(r"orgs/<owner(?: of R)?>/issue-fields")
+_ANY_ORGS_PATH = re.compile(r"orgs/[A-Za-z0-9_<{.-][^\s`]*")
+
+
+def _skill_and_agent_texts() -> dict[str, str]:
+    """Every markdown file of the skill package and the three worker files."""
+    paths = [*sorted(SKILL_DIR.rglob("*.md")), *AGENTS]
+    return {p.name: _text(p) for p in paths if "__pycache__" not in p.parts}
+
+
+def orgs_paths_other_than_allowed(text: str) -> list[str]:
+    """Return every ``orgs/...`` path that is not the one allowed lookup.
+
+    A bare ``orgs/`` token (prose such as "no other `orgs/` path") is not a path.
+    """
+    return _ANY_ORGS_PATH.findall(_ALLOWED_ORGS.sub("", text))
+
+
+def test_orgs_path_is_the_single_allowed_read_and_sits_in_three_files():
+    holders = set()
+    for name, text in _skill_and_agent_texts().items():
+        assert orgs_paths_other_than_allowed(text) == [], name
+        if _ALLOWED_ORGS.search(text):
+            holders.add(name)
+    assert holders == {"SKILL.md", "create.md", "issue-worker-t3.md"}
+
+
+def test_orgs_scanner_reports_a_second_path_and_ignores_prose():
+    text = (
+        "read `orgs/<owner of R>/issue-fields` only; no other `orgs/` path is allowed.\n"
+        "Never read orgs/other/issue-fields."
+    )
+    assert orgs_paths_other_than_allowed(text) == ["orgs/other/issue-fields."]
+
+
+def test_labels_md_has_no_area_or_complexity_label_and_creates_only_the_mode_labels():
+    text = _text(REFS / "labels.md")
+    assert not re.search(r"`(?:type|complexity): [a-z]+`", text)
+    assert re.findall(r'gh label create "([^"]+)"', text) == ["bug", "enhancement"]
+
+
+def test_field_value_write_is_a_post_and_no_file_uses_a_put():
+    post = "gh api -X POST repos/<R>/issues/<N>/issue-field-values --input"
+    for path in (SKILL, REFS / "create.md", REFS / "labels.md"):
+        assert post in _text(path), path.name
+    for name, text in _skill_and_agent_texts().items():
+        assert "-X PUT" not in text, name
+
+
+OUTPUT_LINES = [
+    "not applied: label missing in repo: <name>",
+    "not set: issue type <name>: <type missing in repo | lookup failed | not applied after create>",
+    "not set: field Complexity <value>: <field not found in org | option not found | lookup failed | write failed (<error>) | not applied after create>",
+]
+
+
+def test_labels_md_carries_the_three_output_lines_exactly():
+    lines = _text(REFS / "labels.md").splitlines()
+    for line in OUTPUT_LINES:
+        assert line in lines
+
+
+def test_create_md_uses_the_output_line_prefixes_and_the_type_and_field_reasons():
+    text = _text(REFS / "create.md")
+    for needle in (
+        "not applied: label missing in repo",
+        "not set: issue type <name>: type missing in repo",
+        "not set: issue type <name>: not applied after create",
+        "not set: field Complexity <value>: write failed (",
+        "not set: field Complexity <value>: not applied after create",
+        "not set: field Complexity <value>: field not found in org",
+    ):
+        assert needle in text, needle
+
+
+def test_t3_lookup_scout_template_and_flags_cover_issue_types_and_the_complexity_field():
+    t3 = _text(AGENT_T3)
+    assert "issue-types" in t3 and "issue-fields" in t3
+    scout = _text(TEMPLATES / "scout-report.md")
+    assert "### Repo issue types" in scout and "### Complexity field" in scout
+    flags = _text(TEMPLATES / "flags-decision.md")
+    assert "| Issue type | <Feature | Bug | Test> |" in flags
+    assert "<Simple | Medium | Complex>" in flags
+    assert "not reclassified" in _text(TEMPLATES / "create-review-comment.md")
+
+
+@pytest.mark.parametrize(
+    "row",
+    [
+        "| bug | any | Bug |",
+        "| feature | tests | Test |",
+        "| feature | any other area | Feature |",
+        "| quick | Simple |",
+        "| standard | Medium |",
+        "| deep | Complex |",
+    ],
+)
+def test_labels_md_states_the_issue_type_and_complexity_rules(row):
+    assert row in _text(REFS / "labels.md").splitlines()
+
+
+def test_skill_md_states_the_create_rules_of_the_issue_type_and_field():
+    skill = _text(SKILL)
+    for needle in (
+        "create mode adds `--type <name>`",
+        "gh api -X POST repos/<R>/issues/<N>/issue-field-values --input <file>",
+        "Write any issue field other than Complexity.",
+        "The wanted issue type is missing in the repo",
+        "The Complexity field or its option is missing",
+    ):
+        assert needle in skill, needle
+    assert "fixed set" not in skill
+
+
+def test_command_and_skill_agree_on_the_new_create_boundaries():
+    command = _text(COMMANDS / "issue.md")
+    skill = _text(SKILL)
+    assert "Write any issue field other than Complexity." in command
+    assert "Write any issue field other than Complexity." in skill
+    assert "issue types, issue fields" in command
+    assert "an issue type, an issue field" in skill
+    assert "fixed set" not in command

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
