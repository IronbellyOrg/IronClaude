# Codegraph grounding for TASK-WF-designRev1-20261126-141220

## Run state

- index_state: fresh
- checked_at: 2026-11-26T13:06:55Z (the one readiness check of this /sc:workflow run, made for the first plan TASK-WF-design-20261126-130537 and reused for this regenerated plan; it is not repeated)
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-837
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-837
- access: mcp (lookup tools listed: search, node, callers, callees, impact, files)
- degraded tokens: none. Note: the JSON and Markdown files this plan changes are not indexed (the graph covers Python and YAML only), so their lookups use Glob, Grep and Read, which is the permanent floor, not a degradation.
- Index summary at the check: 3773 files, 0 added, 0 modified, 0 removed since the index. No file under the source tree has changed since: the only new files in this worktree are under `.dev/`.

## Resolved symbols

| Source names | Resolved to | How |
|---|---|---|
| `tests/docs/test_branch_protection_rulesets.py` | 10 symbols: `_REPO` (:8), `_RULESETS` (:9), `_GUIDE` (:10), `_ADMIN_PR_BYPASS` (:13), `_BRANCH_FILES` (:19), `_load` (:25), `test_branch_rulesets` (:30, parametrized at :29 on `"name,ref"`), `test_tag_ruleset` (:47), `test_no_default_branch_token_anywhere` (:66, its glob at :67), `test_guide_has_apply_and_check_commands` (:71) | `codegraph_node {file, symbolsOnly:true}` at the first check; every line read again with Read during the review of the first plan |
| `.github/rulesets/protect-master.json`, `protect-integration.json`, `protect-release-tags.json` | three existing files, read directly (JSON is not indexed) | Glob, Read |
| `docs/developer-guide/branch-protection.md` | 67 lines; headings: What is protected, Apply, Check, Break glass, Tests (the pinned strings are on lines 9-11, 34, 45 and 56) | Read, Grep |
| `.dev/issues/837/accuracy-check.md` line 13 | records commit 206abea1c (pull request 844) and the live ruleset 28081842 with `update` | Read |

## Dependents

| Changed item | Dependents found | Confidence |
|---|---|---|
| `_load` in the test | `test_branch_rulesets` (:30) and `test_tag_ruleset` (:47) call it; both call sites were read directly, so they are call-site-verified. `_load` itself stays unchanged by this plan. | verified |
| `test_no_default_branch_token_anywhere` (:66) | `codegraph_impact` depth 1: only itself. | graph row, lead only |
| `tests/docs/test_branch_protection_rulesets.py` as a whole | `codegraph_node` says no other indexed file depends on it. An empty graph answer is not proof, and the test is run by pytest discovery, not by import. | lead only |
| `docs/developer-guide/branch-protection.md` | Links to it, found with Grep (not edited by this plan beyond the new section and one sentence of "Tests"): `CONTRIBUTING.md:70`, `docs/developer-guide/README.md:59`, `docs/developer-guide/documentation-index.md:37` and `:168`, `docs/developer-guide/release-procedure.md:24` and `:215`. They link to the page; the plan keeps every existing section, heading and command, so the links and descriptions stay true. | Grep, read directly |
| `.github/rulesets/` | The only readers found with Grep outside `.dev/`: the test file, the guide, `docs/developer-guide/release-procedure.md:215` and `CONTRIBUTING.md:70`. No workflow or script reads the folder. | Grep |
| `make lint` | `Makefile:48-50`: `lint` runs `lint-architecture` and `uv run ruff check .`; `.dev/` and `docs/` are outside ruff's scope, so only an old failure elsewhere could fail it. | Read |

## Pre-check

Run after the gate passed (14 tasks, 4 phases). Advisory: it changes neither `TASK-WF-designRev1-20261126-141220.md` nor its status.

| Check | Result |
|---|---|
| Files named by tasks exist | Present: the three `.github/rulesets/*.json` files, `docs/developer-guide/branch-protection.md`, `tests/docs/test_branch_protection_rulesets.py`, `CONTRIBUTING.md`, `docs/developer-guide/README.md`, `docs/developer-guide/documentation-index.md`, `docs/developer-guide/release-procedure.md`, `.dev/issues/837/issue-summary.md`, `.dev/issues/837/accuracy-check.md` and the merged requirements in the brainstorm folder. Not yet present, created by tasks: `.github/rulesets/other-repos/` (Tasks 1 and 2), `.dev/issues/837/audit/`, `.dev/issues/837/private/`, `gates.md`, `handoff-ryan.md`, `apply-runbook.md`, `pr-body.md` (Tasks 5 to 14). |
| Symbols named by tasks resolve | `_load`, `_RULESETS`, `_BRANCH_FILES`, `test_branch_rulesets` (:30), `test_tag_ruleset` (:47), `test_no_default_branch_token_anywhere` (:66), `test_guide_has_apply_and_check_commands` (:71): all resolved. The four new test names of Task 4 are created by that task. |
| Dependents named by tasks are real | The six guide links were read at those lines during the review of the first plan. The two callers of `_load` are real. |
| Dependents of touched symbols that no task names | None found. `_RULESETS` is used only by `_load` and `test_no_default_branch_token_anywhere`; the change from `glob` to `rglob` touches only the latter. `tests/docs/test_release_procedure.py` does not mention the guide or the ruleset files. |
| Commands named by acceptance criteria exist | `uv run pytest tests/docs/...` targets exist; `--collect-only -q` is a pytest option; `make lint` exists (`Makefile:48-50`) and is run and recorded by Task 14 and the runbook, with the one-file ruff check as Task 4's own check. |
| Unplanned item | The Phase 2 and Phase 3 steps of the source design (stage, commit, push, SHA, issue comment, pull request, apply) are not plan tasks by design; Task 13 turns them into a runbook and Task 14 drafts the pull request body. |
| Private detail | The plan and `source.md` contain none of the file name, folder or function names of the private repository's release tooling (grep, 0 hits); Task 5 writes `.dev/issues/837/private/guard-patterns.txt` for the staging guard. |
