144a59010a10aebfa2258099ae1a7bb1dab06f3a
Review one task for spec compliance.

Task brief: ## Task 9: Replace the no-issue-command guard and register the command in the refresh inventory

Depends on: Task 8

In `tests/cli/test_issue_body_templates.py`, replace `test_no_issue_skill_or_command_added` (it asserts that no `sc-issue*` skill and no `issue.md` command exist under `src/superclaude` or `plugins/superclaude`) with `test_issue_command_and_skill_are_the_only_issue_primitives`: `src/superclaude/commands/issue.md` and the directory `src/superclaude/skills/sc-issue-protocol/` exist; under `src/superclaude/skills` the only `sc-issue*` entry is `sc-issue-protocol`; under `src/superclaude/commands` the only `issue.md` is the top-level one; under `plugins/superclaude` no `sc-issue*` skill and no `issue.md` command exist (no mirrors are added, source section 15 "Not changed"). Leave the other tests in the file, including `test_claude_md_has_exactly_one_issue_rule_line`, unchanged (source section 3 last row, section 16, D26).

In `tests/recommend/test_routing_refresh.py`, add `"issue"` to `_POST_REFRESH_ADDITIONS` (currently `{"graph", "impact"}`) and extend the comment above it to name issue #302 as the source of `/sc:issue`, the same way `graph` and `impact` were added (source section 15 row).

Acceptance criteria:
- `grep -n 'test_no_issue_skill_or_command_added' tests/cli/test_issue_body_templates.py` prints nothing and `test_issue_command_and_skill_are_the_only_issue_primitives` exists.
- `uv run pytest tests/cli/test_issue_body_templates.py tests/recommend/test_routing_refresh.py -v` passes, including `test_command_dispositions_trace_appendix_c_and_inventory`.

AC ids: T9.AC1 = first acceptance bullet (old test name gone, new test exists); T9.AC2 = second bullet (pytest passes including test_command_dispositions_trace_appendix_c_and_inventory). Log: .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t9-pytest.log.
Design source: .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md sections 3 (last row), 15 (Change rows for these two tests and "Not changed"), 16.

Global constraints: ## Constraints

- UV only: run Python and tests with `uv run ...` (`uv run pytest`, `uv run --no-project python ...`); never `python -m`, bare `python script.py` or `pip install`.
- Edit only under `src/superclaude/`, `tests/`, `docs/` and the one plugin guide copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (source section 15 and section 17 item 1). Also allowed: this package's `./artifacts/` folder, the unstaged scratch folder `.dev/issues/smoke/` (Task 15), and one temporary Orca worktree for the master comparison (Task 14), which that task removes. `.claude/` is produced by `make sync-dev`; never edit it by hand and never `git add` any `.claude/` path except `.claude/settings.json` (never `git add -f` on `.claude/`).
- Inside the new primitives (command, skill, refs, templates, agents) every reference to another primitive uses its installed path (`~/.claude/commands/sc/<name>.md`, `~/.claude/skills/<name>/...`, `~/.claude/agents/<name>.md`) plus, for existence checks, the project `.claude/` copy; no `src/superclaude/...` path appears in them (source section 15, "Path rule").
- Never interact with the upstream parent `SuperClaude-Org/SuperClaude_Framework`: every `gh` command passes `--repo IronbellyOrg/IronClaude` (or, inside the shipped skill, `--repo <R>` resolved from `origin`), every `gh api` path spells `repos/<owner>/<repo>/...`, and the only fetch is `git fetch origin` (source section 13).
- Secrets: the executor never asks for, prints, echoes or inlines `CLICKUP_API_TOKEN` (no `echo`, `env`, `printenv` or `set -x` on it). When a live ClickUp run is needed, the user exports the variables in their own shell before starting the session (source section 12, "Never printed, logged or written to disk").
- Do not commit or push unless the user asks. `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included; staging is not committing.
- Out of scope for this plan (source section 1 and section 17 item 5): running any next-step chain, creating GitHub labels, creating ClickUp tasks, editing rule 10 of `src/superclaude/core/CLAUDE.md`, changing the level table, adding `plugins/superclaude/` command, agent or skill mirrors, listing the workers in `docs/user-guide/agents.md`, any `src/superclaude/cli/` code, and opening the pull request (done afterwards with `/sc:pr-submit --monitor 3 --head ironbelly/feat-sc-issue-command --title "..." --body "..."`).
- Live `/sc:issue --claim` or `--create` runs post directly to GitHub (source decision B1). Live checks in this plan are the two the source schedules (Task 15 worker spawns, Task 16 ClickUp smoke claim) and the section 20 acceptance record of Task 17. A run that stops before any GitHub or ClickUp write (section 20 item 4) may run without asking; any run that would assign, comment on or create a real GitHub issue needs the user's explicit approval at that moment.

Start sha: 144a59010a10aebfa2258099ae1a7bb1dab06f3a
Diff against the start snapshot: diff --git a/tests/cli/test_issue_body_templates.py b/tests/cli/test_issue_body_templates.py
index 7ba3ceb7..fb1ae6a5 100644
--- a/tests/cli/test_issue_body_templates.py
+++ b/tests/cli/test_issue_body_templates.py
@@ -75,11 +75,19 @@ def test_claude_md_has_exactly_one_issue_rule_line():
     )
 
 
-def test_no_issue_skill_or_command_added():
-    for root in ("src/superclaude", "plugins/superclaude"):
-        skills = _REPO / root / "skills"
-        if skills.is_dir():
-            assert not list(skills.glob("sc-issue*")), root
-        commands = _REPO / root / "commands"
-        if commands.is_dir():
-            assert not list(commands.rglob("issue.md")), root
+def test_issue_command_and_skill_are_the_only_issue_primitives():
+    """Issue #302 adds /sc:issue and sc-issue-protocol, and nothing else.
+
+    No plugin mirror is added (design section 15, "Not changed").
+    """
+    src = _REPO / "src/superclaude"
+    assert (src / "commands/issue.md").is_file()
+    assert (src / "skills/sc-issue-protocol").is_dir()
+    assert sorted(p.name for p in (src / "skills").glob("sc-issue*")) == ["sc-issue-protocol"]
+    commands = src / "commands"
+    assert [p.relative_to(commands) for p in commands.rglob("issue.md")] == [Path("issue.md")]
+    plugins = _REPO / "plugins/superclaude"
+    if (plugins / "skills").is_dir():
+        assert not list((plugins / "skills").glob("sc-issue*"))
+    if (plugins / "commands").is_dir():
+        assert not list((plugins / "commands").rglob("issue.md"))
diff --git a/tests/recommend/test_routing_refresh.py b/tests/recommend/test_routing_refresh.py
index 956d009f..428e5487 100644
--- a/tests/recommend/test_routing_refresh.py
+++ b/tests/recommend/test_routing_refresh.py
@@ -27,9 +27,10 @@ _COMMANDS = _REPO / "src/superclaude/commands"
 _SKILLS = _REPO / "src/superclaude/skills"
 _PACKAGE = "TASK-RESEARCH-recommend-refresh-20261024-044336"
 # Commands shipped after the frozen routing-refresh research package was written:
-# issue #323 (codegraph adoption, Phase 3) adds /sc:graph and /sc:impact. The
-# package is frozen, so the shipped set is compared minus these additions.
-_POST_REFRESH_ADDITIONS = {"graph", "impact"}
+# issue #323 (codegraph adoption, Phase 3) adds /sc:graph and /sc:impact, and
+# issue #302 adds /sc:issue. The package is frozen, so the shipped set is
+# compared minus these additions.
+_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue"}
 
 _TOKEN_RE = re.compile(r"`/([a-z][a-z0-9:-]*)")
 _FLAG_RE = re.compile(r"--[a-z][a-z0-9-]*")
diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t9-pytest.log b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t9-pytest.log
new file mode 100644
index 00000000..e517ea7f
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t9-pytest.log
@@ -0,0 +1,269 @@
+$ grep -n 'test_no_issue_skill_or_command_added' tests/cli/test_issue_body_templates.py
+exit=1 (grep exit 1 = no match)
+$ uv run pytest tests/cli/test_issue_body_templates.py tests/recommend/test_routing_refresh.py -v
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command/.venv/bin/python
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collecting ... collected 255 items
+
+tests/cli/test_issue_body_templates.py::test_body_files_shipped_and_installed_flat PASSED [  0%]
+tests/cli/test_issue_body_templates.py::test_body_file_has_exactly_its_four_headings[ISSUE-BACKLOG.md] PASSED [  0%]
+tests/cli/test_issue_body_templates.py::test_body_file_has_exactly_its_four_headings[ISSUE-HANDOFF.md] PASSED [  1%]
+tests/cli/test_issue_body_templates.py::test_body_file_names_no_execution_key_or_clickup[ISSUE-BACKLOG.md] PASSED [  1%]
+tests/cli/test_issue_body_templates.py::test_body_file_names_no_execution_key_or_clickup[ISSUE-HANDOFF.md] PASSED [  1%]
+tests/cli/test_issue_body_templates.py::test_claude_md_has_exactly_one_issue_rule_line PASSED [  2%]
+tests/cli/test_issue_body_templates.py::test_issue_command_and_skill_are_the_only_issue_primitives PASSED [  2%]
+tests/recommend/test_routing_refresh.py::test_fixture_schema_and_completeness PASSED [  3%]
+tests/recommend/test_routing_refresh.py::test_every_mapped_test_function_exists PASSED [  3%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S01] PASSED [  3%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S02] PASSED [  4%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S03] PASSED [  4%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S04] PASSED [  5%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S05] PASSED [  5%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S06] PASSED [  5%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S07] PASSED [  6%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S08] PASSED [  6%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S09] PASSED [  7%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S10] PASSED [  7%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S11] PASSED [  7%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S12] PASSED [  8%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S13] PASSED [  8%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S14] PASSED [  9%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S15] PASSED [  9%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S16] PASSED [  9%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S17] PASSED [ 10%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S18] PASSED [ 10%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S19] PASSED [ 10%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S20] PASSED [ 11%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S21] PASSED [ 11%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S22] PASSED [ 12%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S23] PASSED [ 12%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S24] PASSED [ 12%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S25] PASSED [ 13%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S26] PASSED [ 13%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S27] PASSED [ 14%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S28] PASSED [ 14%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S29] PASSED [ 14%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S01] PASSED [ 15%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S02] PASSED [ 15%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S03] PASSED [ 16%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S04] PASSED [ 16%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S05] PASSED [ 16%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S06] PASSED [ 17%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S07] PASSED [ 17%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S08] PASSED [ 18%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S09] PASSED [ 18%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S10] PASSED [ 18%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S11] PASSED [ 19%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S12] PASSED [ 19%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S13] PASSED [ 20%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S14] PASSED [ 20%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S15] PASSED [ 20%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S16] PASSED [ 21%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S17] PASSED [ 21%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S18] PASSED [ 21%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S19] PASSED [ 22%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S20] PASSED [ 22%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S21] PASSED [ 23%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S22] PASSED [ 23%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S23] PASSED [ 23%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S24] PASSED [ 24%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S25] PASSED [ 24%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S26] PASSED [ 25%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S27] PASSED [ 25%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S28] PASSED [ 25%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S29] PASSED [ 26%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S01] PASSED [ 26%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S02] PASSED [ 27%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S03] PASSED [ 27%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S04] PASSED [ 27%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S05] PASSED [ 28%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S06] PASSED [ 28%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S07] PASSED [ 29%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S08] PASSED [ 29%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S09] PASSED [ 29%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S10] PASSED [ 30%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S11] PASSED [ 30%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S12] PASSED [ 30%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S13] PASSED [ 31%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S14] PASSED [ 31%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S15] PASSED [ 32%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S16] PASSED [ 32%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S17] PASSED [ 32%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S18] PASSED [ 33%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S19] PASSED [ 33%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S20] PASSED [ 34%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S21] PASSED [ 34%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S22] PASSED [ 34%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S23] PASSED [ 35%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S24] PASSED [ 35%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S25] PASSED [ 36%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S26] PASSED [ 36%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S27] PASSED [ 36%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S28] PASSED [ 37%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S29] PASSED [ 37%]
+tests/recommend/test_routing_refresh.py::test_flag_value_check_rejects_undeclared_enumerated_value PASSED [ 38%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S01] PASSED [ 38%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S02] PASSED [ 38%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S03] PASSED [ 39%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S04] PASSED [ 39%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S05] PASSED [ 40%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S06] PASSED [ 40%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S07] PASSED [ 40%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S08] PASSED [ 41%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S09] PASSED [ 41%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S10] PASSED [ 41%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S11] PASSED [ 42%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S12] PASSED [ 42%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S13] PASSED [ 43%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S14] PASSED [ 43%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S15] PASSED [ 43%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S16] PASSED [ 44%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S17] PASSED [ 44%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S18] PASSED [ 45%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S19] PASSED [ 45%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S20] PASSED [ 45%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S21] PASSED [ 46%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S22] PASSED [ 46%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S23] PASSED [ 47%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S24] PASSED [ 47%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S25] PASSED [ 47%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S26] PASSED [ 48%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S27] PASSED [ 48%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S28] PASSED [ 49%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S29] PASSED [ 49%]
+tests/recommend/test_routing_refresh.py::test_route_check_rejects_other_route_for_a_routed_command PASSED [ 49%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S01] PASSED [ 50%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S02] PASSED [ 50%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S03] PASSED [ 50%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S04] PASSED [ 51%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S05] PASSED [ 51%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S06] PASSED [ 52%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S07] PASSED [ 52%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S08] PASSED [ 52%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S09] PASSED [ 53%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S10] PASSED [ 53%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S11] PASSED [ 54%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S12] PASSED [ 54%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S13] PASSED [ 54%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S14] PASSED [ 55%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S15] PASSED [ 55%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S16] PASSED [ 56%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S17] PASSED [ 56%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S18] PASSED [ 56%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S19] PASSED [ 57%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S20] PASSED [ 57%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S21] PASSED [ 58%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S22] PASSED [ 58%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S23] PASSED [ 58%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S24] PASSED [ 59%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S25] PASSED [ 59%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S26] PASSED [ 60%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S27] PASSED [ 60%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S28] PASSED [ 60%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S29] PASSED [ 61%]
+tests/recommend/test_routing_refresh.py::test_positional_check_rejects_a_dropped_required_spec_path PASSED [ 61%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S01] PASSED [ 61%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S02] PASSED [ 62%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S03] PASSED [ 62%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S04] PASSED [ 63%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S05] PASSED [ 63%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S06] PASSED [ 63%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S07] PASSED [ 64%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S08] PASSED [ 64%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S09] PASSED [ 65%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S10] PASSED [ 65%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S11] PASSED [ 65%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S12] PASSED [ 66%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S13] PASSED [ 66%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S14] PASSED [ 67%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S15] PASSED [ 67%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S16] PASSED [ 67%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S17] PASSED [ 68%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S18] PASSED [ 68%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S19] PASSED [ 69%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S20] PASSED [ 69%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S21] PASSED [ 69%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S22] PASSED [ 70%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S23] PASSED [ 70%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S24] PASSED [ 70%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S25] PASSED [ 71%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S26] PASSED [ 71%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S27] PASSED [ 72%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S28] PASSED [ 72%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S29] PASSED [ 72%]
+tests/recommend/test_routing_refresh.py::test_mandatory_flag_check_rejects_omitted_or_altered_entries PASSED [ 73%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S01] PASSED [ 73%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S02] PASSED [ 74%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S03] PASSED [ 74%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S04] PASSED [ 74%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S05] PASSED [ 75%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S06] PASSED [ 75%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S07] PASSED [ 76%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S08] PASSED [ 76%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S09] PASSED [ 76%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S10] PASSED [ 77%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S11] PASSED [ 77%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S12] PASSED [ 78%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S13] PASSED [ 78%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S14] PASSED [ 78%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S15] PASSED [ 79%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S16] PASSED [ 79%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S17] PASSED [ 80%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S18] PASSED [ 80%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S19] PASSED [ 80%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S20] PASSED [ 81%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S21] PASSED [ 81%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S22] PASSED [ 81%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S23] PASSED [ 82%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S24] PASSED [ 82%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S25] PASSED [ 83%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S26] PASSED [ 83%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S27] PASSED [ 83%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S28] PASSED [ 84%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S29] PASSED [ 84%]
+tests/recommend/test_routing_refresh.py::test_tdd_activation_uses_the_tdd_skill_not_a_guessed_protocol PASSED [ 85%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S01] PASSED [ 85%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S02] PASSED [ 85%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S03] PASSED [ 86%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S04] PASSED [ 86%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S05] PASSED [ 87%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S06] PASSED [ 87%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S07] PASSED [ 87%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S08] PASSED [ 88%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S09] PASSED [ 88%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S10] PASSED [ 89%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S11] PASSED [ 89%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S12] PASSED [ 89%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S13] PASSED [ 90%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S14] PASSED [ 90%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S15] PASSED [ 90%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S16] PASSED [ 91%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S17] PASSED [ 91%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S18] PASSED [ 92%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S19] PASSED [ 92%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S20] PASSED [ 92%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S21] PASSED [ 93%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S22] PASSED [ 93%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S23] PASSED [ 94%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S24] PASSED [ 94%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S25] PASSED [ 94%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S26] PASSED [ 95%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S27] PASSED [ 95%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S28] PASSED [ 96%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S29] PASSED [ 96%]
+tests/recommend/test_routing_refresh.py::test_unmatched_cache_expectation_rejects_unconditional_wording PASSED [ 96%]
+tests/recommend/test_routing_refresh.py::test_conditional_step_guard_rejects_incidental_only PASSED [ 97%]
+tests/recommend/test_routing_refresh.py::test_cache_expectation_follows_the_guide_block PASSED [ 97%]
+tests/recommend/test_routing_refresh.py::test_matched_routes_bypass_cache_so_seeded_rows_cannot_win PASSED [ 98%]
+tests/recommend/test_routing_refresh.py::test_unmatched_cache_hints_are_consulted_then_rejected PASSED [ 98%]
+tests/recommend/test_routing_refresh.py::test_example_only_flags_are_not_declared_or_routed PASSED [ 98%]
+tests/recommend/test_routing_refresh.py::test_retired_identities_have_no_shipped_command PASSED [ 99%]
+tests/recommend/test_routing_refresh.py::test_command_dispositions_trace_appendix_c_and_inventory PASSED [ 99%]
+tests/recommend/test_routing_refresh.py::test_analyst_reports_and_disposition_appendix_are_retained PASSED [100%]
+
+============================= 255 passed in 1.40s ==============================
+rc=0

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
