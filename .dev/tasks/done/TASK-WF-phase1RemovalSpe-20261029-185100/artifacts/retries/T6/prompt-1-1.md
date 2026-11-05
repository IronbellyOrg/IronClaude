ac909267c7d2c58272b86e12b13b888e8bf6971a
Review one task for spec compliance.

Task brief: ## Task 6: Delete the codebase-memory installer module and its test file

Depends on: Task 5

Implements ./source.md §8 T5 and row C1. `git rm src/superclaude/cli/install_codebase_memory.py tests/cli/test_install_codebase_memory.py` (deletion only). Commit `refactor(cli)!: delete the codebase-memory installer module (#323)`, then post the G1 issue-#323 comment (Constraints).

Acceptance criteria:
- T6.AC1: `rg -n "install_codebase_memory|codebase_memory" src tests -g '!src/superclaude/cli/install_retired_mcp.py' -g '!tests/cli/test_install_retired_mcp.py'` prints nothing.
- T6.AC2: `uv run pytest tests/cli tests/unit tests/recommend tests/docs -q -p no:cacheprovider --ignore=tests/cli/eval -rfE` has no failing test id that is not in `$PKG/artifacts/baseline/full.txt`.
- T6.AC3: `uv run ruff check src/superclaude/cli tests/cli` passes and `bash $PKG/artifacts/acceptance-search.sh cbm src tests` prints `ACCEPTANCE_SEARCH_OK cbm`.
- T6.AC4: The G1 issue comment URL (or the recorded `gh` error) is in `$PKG/progress.md`.

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
Start sha: ac909267c7d2c58272b86e12b13b888e8bf6971a
Diff against the start snapshot: Work is already committed as HEAD b319cc07 (git show --stat HEAD). Touched files: src/superclaude/cli/install_codebase_memory.py (deleted), tests/cli/test_install_codebase_memory.py (deleted), tests/cli/test_install_mcp_cli.py (one test renamed and its codebase-memory string assertion dropped, so the search gate passes). Observed by the implementer (verify yourself): the test gate output is saved at $PKG/artifacts/g1/t6-tests.txt (1583 passed, 3 skipped, 1 xpassed; no failing id outside $PKG/artifacts/baseline/full.txt); ruff via 'uv run --with ruff==0.15.20 ruff check src/superclaude/cli tests/cli' passes because ruff is not installed in the venv (decision 4 in $PKG/decisions.md); the G1 comment is https://github.com/IronbellyOrg/IronClaude/issues/323#issuecomment-6510924087 recorded at $PKG/artifacts/issue-comments.md:4. PENDING LEDGER WRITE appended to $PKG/progress.md only if this review passes (the ledger is append-only): 'T6: complete verdict=compliant ac=T6.AC1,T6.AC2,T6.AC3,T6.AC4 evidence=...,https://github.com/IronbellyOrg/IronClaude/issues/323#issuecomment-6510924087,T6.AC4@./artifacts/issue-comments.md:4' (the URL goes into the complete line evidence because the ledger accepts no free text; decision 1).

    refactor(cli)!: delete the codebase-memory installer module (#323)
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 .../artifacts/g1/t6-tests.txt                      | 136 ++++
 .../artifacts/retries/T6/q0-head                   |   1 +
 .../decisions.md                                   |   2 +
 .../progress.md                                    |   1 +
 src/superclaude/cli/install_codebase_memory.py     | 759 -------------------
 tests/cli/test_install_codebase_memory.py          | 830 ---------------------
 tests/cli/test_install_mcp_cli.py                  |   3 +-
 7 files changed, 141 insertions(+), 1591 deletions(-)
diff --git a/tests/cli/test_install_mcp_cli.py b/tests/cli/test_install_mcp_cli.py
index f8500bac..38e3e2c7 100644
--- a/tests/cli/test_install_mcp_cli.py
+++ b/tests/cli/test_install_mcp_cli.py
@@ -95,13 +95,12 @@ def mcp_cli(monkeypatch, isolated_home):
     return state
 
 
-def test_mcp_list_shows_every_registry_server_and_no_retired_one(mcp_cli):
+def test_mcp_list_shows_every_registry_server(mcp_cli):
     result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp", "--list"])
     assert result.exit_code == 0, result.output
     for name in mcp_cli.module.MCP_SERVERS:
         assert name in result.output
     assert "airis-mcp-gateway" in result.output
-    assert "codebase-memory-mcp" not in result.output
     assert mcp_cli.calls == [] and not any(
         cmd[:3] == ["claude", "mcp", "add"] for cmd in mcp_cli.processes
     )
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
