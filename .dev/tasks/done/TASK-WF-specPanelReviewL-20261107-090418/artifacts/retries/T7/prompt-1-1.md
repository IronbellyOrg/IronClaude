51d1133dd3057a8fcf4215f1374d27d2c9effa37
Review one task for spec compliance.

Task brief: ## Task 7: Sync the dev copies and confirm repository state

Depends on: Task 6

Run `make sync-dev` so the changed command is copied into the untracked `.claude/` tree, then `make verify-sync`. Run `make lint` and the repo's pinned ruff format check on the changed Python file. Run the keep-green tests named in section 9 of ./source.md: `tests/skills/test_review_severity_rule.py`, `tests/commands/test_routing_plugin_parity.py`, `tests/core/test_how_we_work_routing_table.py`, `tests/core/test_claude_md_routing_block.py`, `tests/skills/test_primitive_dual_surface_lookup.py`, `tests/docs/test_onboarding_deck.py`, `tests/skills/test_worker_contract.py`.

Acceptance criteria:
- `make verify-sync`, `make lint` and the ruff format check pass; their output is saved to ./artifacts/t7-sync-lint.log.
- All seven keep-green test files pass together with the new test file; output saved to ./artifacts/t7-tests.log.
- From the repo root, run `git diff --name-only HEAD -- . ':!.dev'` and `git ls-files --others --exclude-standard -- . ':!.dev'`; save their combined, de-duplicated list (`sort -u`) and both exit codes to ./artifacts/t7-changed-files.txt in this package's `artifacts/` folder (not the repo-root `artifacts/`). Every listed path is one of these 8: `src/superclaude/commands/spec-panel.md`, `plugins/superclaude/commands/spec-panel.md`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `docs/guides/prd-skill-release-guide.md`, `docs/guides/tdd-skill-release-guide.md`, `tests/skills/test_spec_panel_review_loop.py`, `docs/designs/spec-panel-review-loop.md` (plus `tests/skills/test_review_severity_rule.py` only if the Task 1 log records a Constraints matcher wording change). The 7 delivery paths (all of the 8 except the design doc) are all listed; the design doc may be absent only because it was committed before Task 1 started. No listed path is under `.claude/`, ends in `pragmatic.md` or `WORKER-CONTRACT.md`, contains `sc-implement-protocol`, or is `docs/user-guide/flags.md` or `commands/sc-help.md`. `git diff --cached --name-only -- .claude` prints nothing, and its output is appended to the same file.


AC ids in source order: T7.AC1 = bullet 1, T7.AC2 = bullet 2, T7.AC3 = bullet 3 of the Acceptance criteria block.
Evidence files (cite as ./artifacts/<name>), all in /home/coder/workspaces/worktrees/IronClaude/issue-346-review-loop-convergence/.dev/tasks/to-do/TASK-WF-specPanelReviewL-20261107-090418/artifacts/: t7-sync-lint.log, t7-tests.log, t7-changed-files.txt.
Task 7 changes no tracked file by design (it syncs the gitignored .claude/ tree and records logs). The keep-green run also included tests/recommend/test_routing_refresh.py and tests/cli/test_how_we_work_install.py as extras. The Task 1 log (./artifacts/t1-section-diff.txt) is empty, so no matcher wording change was recorded.
Global constraints: ## Constraints

- Edit canonical files under `src/superclaude/` and the named `plugins/superclaude/` mirrors by hand; run `make sync-dev` afterwards. Never stage anything under `.claude/`. Stage `.dev/tasks` with the work.
- Do not change `src/superclaude/output-styles/pragmatic.md`, any `sc-implement-protocol` file, or `WORKER-CONTRACT.md`. Do not touch `docs/user-guide/flags.md` or `commands/sc-help.md` (the generic `--iterations` rows).
- The literal bullet text comes from section 5 of ./source.md and must be copied byte for byte; each bullet is ONE line. If an existing matcher in `tests/skills/test_review_severity_rule.py` flags a bullet, change the minimum wording and keep the literals the new test asserts (source section 9, T3 to T8), updating the test in the same change.
- Installed primitives must not name `src/superclaude/` paths. Do not add a size limit, a monotonic halt or an installer change (source section 11).
- Handoff notes for the pull request, not tasks: the body uses `Refs` for issue 346 (the causal link is unproven), and it says that the new command text reaches an existing host only after `superclaude install --force` or `update`.
Start sha: 51d1133dd3057a8fcf4215f1374d27d2c9effa37
Diff against the start snapshot: No tracked product file is changed by this task. Artifacts written by this task:

(artifact ./artifacts/t7-sync-lint.log):
== make sync-dev
   Skills:    39 directories
   Agents:    48 files
   Commands:  46 files
   Hooks:     14 files
   Templates: 52 files
sync-dev exit=0
== make verify-sync

=== Installer Registration ===
  ✅ _FRESHNESS_SCRIPTS matches src/superclaude/hooks/scripts/*.sh and *.js

=== Hooks Cross-Consistency ===
  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes

✅ All components in sync.
verify-sync exit=0
== make lint
Running linter...
uv run ruff check .
All checks passed!
lint exit=0
== pinned ruff format check (ruff 0.15.20)
1 file already formatted
format-check exit=0

(artifact ./artifacts/t7-tests.log):
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
SuperClaude: 5.0.0
rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-346-review-loop-convergence
configfile: pyproject.toml
plugins: superclaude-5.0.0, anyio-4.16.0
collected 860 items

tests/skills/test_spec_panel_review_loop.py ............................ [  3%]
..................                                                       [  5%]
tests/skills/test_review_severity_rule.py .............................. [  8%]
................................                                         [ 12%]
tests/commands/test_routing_plugin_parity.py .....                       [ 13%]
tests/core/test_how_we_work_routing_table.py ........................... [ 16%]
....................................................                     [ 22%]
tests/core/test_claude_md_routing_block.py ......                        [ 23%]
tests/skills/test_primitive_dual_surface_lookup.py ...                   [ 23%]
tests/docs/test_onboarding_deck.py ...                                   [ 23%]
tests/skills/test_worker_contract.py ................................... [ 27%]
........................................................................ [ 36%]
........................................................................ [ 44%]
........................................................................ [ 52%]
........................................................................ [ 61%]
........................................................................ [ 69%]
.....                                                                    [ 70%]
tests/recommend/test_routing_refresh.py ................................ [ 73%]
........................................................................ [ 82%]
........................................................................ [ 90%]
........................................................................ [ 99%]
                                                                         [ 99%]
tests/cli/test_how_we_work_install.py ........                           [100%]

============================= 860 passed in 5.78s ==============================
exit=0

(artifact ./artifacts/t7-changed-files.txt):
# git diff --name-only HEAD -- . ':!.dev' exit=0
# git ls-files --others --exclude-standard -- . ':!.dev' exit=0
# combined sort -u:
docs/designs/spec-panel-review-loop.md
docs/guides/prd-skill-release-guide.md
docs/guides/tdd-skill-release-guide.md
plugins/superclaude/commands/spec-panel.md
plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
src/superclaude/commands/spec-panel.md
src/superclaude/core/HOW-WE-WORK.md
tests/skills/test_spec_panel_review_loop.py
# git diff --cached --name-only -- .claude (exit follows, output between markers):
<<<
>>> exit=0
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
