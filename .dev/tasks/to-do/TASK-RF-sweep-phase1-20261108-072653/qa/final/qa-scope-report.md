# QA Report: Final gate, scope lens

**Date:** 2026-11-12
**Reviewer:** qa-final-scope lens (adversarial, fix_authorization: false)
**Base commit:** 5dc29d23b15eb7db4ead50623bb409f696a0d7d3

## Findings

All paths are relative to `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`. `$BASE` is `5dc29d23b15eb7db4ead50623bb409f696a0d7d3` (`.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/base-commit.txt`).

Result: no BLOCKING and no MAJOR finding. Four MINOR notes (recorded, never fail the gate).

### Blocking and major findings

None. Each of the five BLOCKING predicates in the lens was tested against the files on disk (C4 to C9 below).

### MINOR notes

| id | severity | evidence | what is wrong | smallest fix |
|---|---|---|---|---|
| S-m1 | MINOR | `src/superclaude/skills/sc-sweep-protocol/SKILL.md:26` and `:43` (the `(not observed in Phase 1)` mark on the stalled (proved) and fenced counts); `src/superclaude/output-styles/pragmatic.md:23` (exempt reply "contains the summary counts and the report path", no mark); DESIGN `docs/designs/orchestrator-mode.md:662` step 4 and `design-addendum.md:13` (counts and path only) | The skill adds a presentation detail that DESIGN 7.6 step 4 and the revision addendum do not list, and the style text does not mention it, so a session that follows the style alone could drop it. It came from the docs gate fix DOC-F2 (`qa/docs/fix-log-cycle1.md:27`), it is tested (`tests/commands/test_sweep_command.py`, `_PHASE1_MARK` at line 520), and it is already listed in `.dev/implement/task-rf-sweep-phase1-202-c7ea3265/followups.md:17`. It adds no option, flag or code path. | In a later change, say the mark in `pragmatic.md:23` too, or drop it from the skill. No change needed to pass this gate. |
| S-m2 | MINOR | `src/superclaude/cli/sweep/probes.py:477-488` (`_WAIT_TIME_KEYS = ("since", "waitingSince", "timestamp", "at", "createdAt", "startedAt")`, `_wait_since` takes the earliest) and `:461-474` (looks for `agentWait` in two holders); DESIGN `docs/designs/orchestrator-mode.md:996` (open item 6: names UNVERIFIED, "rule 5 cannot match; rows fall to the fallback") | A guessed list of key names for a field no live capture has shown (all five captured workers had exited, `tests/sweep/fixtures/SOURCES.md:41`). DESIGN does not name these keys. It is labelled UNVERIFIED in the code comment, serves SPEC SP-15 (the age of a wait) and only affects the age shown and the sort order, so it is not a new option or abstraction. | When a live `agentWait` is captured, replace the guess by the one real key; until then it may stay. |
| S-m3 | MINOR | `tests/sweep/fixtures/captured-tab-map-1.json` to `-5.json`, `captured-worktree-list.json`, `captured-worktree-current.json`: `grep` of `tests/sweep/*.py` and `tests/commands/test_sweep_command.py` finds no reader (the `captured-worker-show-{n}` ones are read through an f-string at `tests/sweep/test_probes_allowlist.py:326`) | Seven captured fixtures are read by no test. They are called for by DESIGN 15.1 (`docs/designs/orchestrator-mode.md:898`, "sanitized samples ... are copied under `tests/sweep/fixtures/`"), by plan item 7.18 and by `tests/sweep/fixtures/SOURCES.md`, so they are in scope, but they are dead test data. Already recorded as TST-F37 in `qa/tests/consolidated-findings-cycle0.md:102`. | Either read them in a test or leave them; no scope change. |
| S-m4 | MINOR | `git status --porcelain --untracked-files=all -- .dev` lists `.dev/issues/465/{description,draft-notes,flags,issue-body,scout}.md` (mtimes 2026-11-09 02:34 to 02:41, after the baseline at 2026-11-08 20:12; not in `artifacts/baseline-git-status.txt`) | Unrelated untracked output of a separate `/sc:issue --create` run (a worker-stall issue). It is not task output, not in `final-inventory.md` and not called for by the GOAL. | Do not stage it with the Phase 1 change set; the person decides what to do with it. |

Record drift (not a finding): the owner decision record `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-3-addendum-wc16-wait-timeout-decision.md:23` and the lens prompt call the cap line "sweep.md line 20"; the approved sentence is at `src/superclaude/commands/sweep.md:22` (line 20 is the `## Triggers` heading). The approved text itself is present and exact.

## Check evidence

| id | what was checked and how | result |
|---|---|---|
| C1 | Inventory equals the real change set. `git ls-files --others --exclude-standard -- src tests docs plugins` minus `artifacts/baseline-untracked.txt` gave 37 paths; `final-inventory.md` lists 37 new plus 13 edited paths (12 from `git diff --stat "$BASE" -- . ':(exclude).dev'` plus `docs/designs/orchestrator-mode.md`). `comm` in both directions: no path in the real set missing from the inventory, and the only inventory paths absent from the untracked set are the 13 edited ones. `git diff --name-only HEAD` outside `.dev` lists exactly the 12 edited files. | PASS |
| C2 | Every edited file is called for. `.gitignore` (+2 lines, DESIGN section 10); `CHANGELOG.md` (+10, R8); `docs/user-guide/commands.md` (+1 row, R6); `docs/developer-guide/...Agents.md` (1 line, R7); `src/superclaude/core/HOW-WE-WORK.md` (+2, R1 and R2) and its plugin copy (byte-equal, `cmp` printed SAME, R3); `tests/core/test_how_we_work_routing_table.py` (+1, R4); `tests/recommend/test_routing_refresh.py` (1 line, R5); `src/superclaude/cli/main.py` (+4, after line 565, GOAL); `src/superclaude/core/WORKER-CONTRACT.md` (hunks at lines 23 and 275 only: never-as-worker list and WC-16, GOAL); `tests/skills/test_worker_contract.py` (five hunks: lines 89, 173, 400, 922, 1333 = the five pins plus rename, DESIGN section 8); `src/superclaude/output-styles/pragmatic.md` (revision authority, C11). | PASS |
| C3 | Every new file is called for. `src/superclaude/cli/sweep/{__init__,models,classify,probes,report,commands}.py` are the six GOAL modules and nothing else; `commands/sweep.md` and `skills/sc-sweep-protocol/SKILL.md` are the GOAL command and skill; `tests/sweep/` holds `__init__.py` (required by the GOAL), `conftest.py` and six test modules (DESIGN section 11: "seven new files") plus 19 `captured-*.json` fixtures and `SOURCES.md` (DESIGN 15.1, item 7.18); `tests/commands/test_sweep_command.py` is named in the GOAL. See S-m3 for seven unread fixtures. | PASS |
| C4 | No changed file outside the inventory or outside the approved areas. `git ls-files --others --exclude-standard` outside `src tests docs plugins` and `.dev`: empty. `git status` shows no change to `pyproject.toml`, `uv.lock`, `Makefile`, `.claude/settings.json` or any hook. `git diff --cached --name-only` has 0 `.claude/` paths. The three `docs/designs/orchestrator-mode-review-*.md` files are older (2026-11-08 07:xx) than the baseline (20:12), so unchanged. See S-m4 for unrelated `.dev/issues/465/`. | PASS |
| C5 | WC-9 lock-retry code or text (IronbellyOrg/IronClaude#446). `grep -rniE 'WC-9\|lock.?retry\|retry.*lock\|#446\|flock\|EAGAIN'` over `src/superclaude/cli/sweep`, `sweep.md`, `SKILL.md`, `tests/sweep`, `tests/commands/test_sweep_command.py`, `.gitignore`, `CHANGELOG.md`, `main.py`: no match. In DESIGN: no match for `WC-9`, `lock retr`, `#446`, `index.lock`. In `WORKER-CONTRACT.md` every WC-9 line (34, 41, 59, 306) lies outside the two changed hunks (`git diff -U0` hunks `@@ -23` and `@@ -274,0 +275,4`). The only lock-related code is `git --no-optional-locks` and `GIT_OPTIONAL_LOCKS=0` in the read seam, which DESIGN 2.1 (`orchestrator-mode.md:47`) specifies and which is not a retry. | PASS |
| C6 | `WORKER-CONTRACT.md` line 110 untouched. `git diff -U0 "$BASE" -- src/superclaude/core/WORKER-CONTRACT.md` has only the hunks `@@ -23 +23 @@` (one line replaced, no shift) and `@@ -274,0 +275,4 @@` (after line 110); no removed line contains "The sweep"; line 110 still begins `**The sweep.**` (read with `sed -n 108,112p`). | PASS |
| C7 | `UNATTENDED_EXPECT` stays 31. `sed -n 448,755p tests/skills/test_worker_contract.py` has 31 top-level keys; none is `sweep`; the diff has no hunk inside lines 448-755 (hunks at 89, 173, 400, 922, 1333). `grep -n 'Unattended mode'` on `sweep.md` and `SKILL.md`: no match. | PASS |
| C8 | Speculative option or abstraction in the CLI. `commands.py` has exactly the four options of DESIGN 7.1 (`--run`, `--window`, `--root`, `--output`, lines 220-241) and `__getattr__` in `__init__.py` returns only `sweep_group`; `sweep.md` Options table and `SKILL.md` Inputs list the same four. Environment reads in the package are `ORCA_CLI_COMMAND` (DESIGN 7.1), `GIT_OPTIONAL_LOCKS` (DESIGN 2.1) and `XDG_STATE_HOME` (DESIGN test plan, line 753). Function and class names in `probes.py`, `classify.py`, `report.py`, `models.py` match DESIGN 7.1 and 7.2; the private helpers are the design's rules, joins and sections. No flag, mode, config key or extension hook beyond the design. | PASS |
| C9 | Allowlist breadth. `probes.py:47-58` has 10 templates: the eight of DESIGN plus `worktree ps --agent-wait` with and without `--json`, "not called in Phase 1". Authority: owner decision OQ-1 (`phase-outputs/plans/OQ-1-agent-wait-decision.md:19-23`, directly confirmed by the owner 2026-11-12) and OQ-17 (cursor template refused, stays at 10). `grep agent-wait src/superclaude/cli/sweep` finds only the two allowlist lines and an unrelated report label; no code path issues them; tests assert zero argv for them (`tests/sweep/test_probes_allowlist.py:567`). | PASS |
| C10 | Speculative code in the data path. Read `probes.py:38-77`, `:460-490`, all of `commands.py`. One guessed-key heuristic found (S-m2), bounded and labelled UNVERIFIED, serving SPEC SP-15; no new surface. | PASS (note S-m2) |
| C11 | Canonical style edit bounded by the revision. `git diff -U0` hunks of `pragmatic.md`: lines 22 (rule plus four sub-bullets), 57, 62, 64, 73, 84, 94, all above `## Work discipline` (line 107); 6 occurrences of the qualifier, one per later restatement, as the addendum (`design-addendum.md:27`) and plan item 7.10 require (item 7.10 also says to label the examples non-exempt, so the four `non-exempt example` labels are authorized). Content matches the addendum common rule (`design-addendum.md:13-21`). The edit adds no general coordinator, all-skill or file exemption. Style text in `step-7.10-style-exception.md:42-68` equals the diff. | PASS |
| C12 | WC-16 and the owner-approved edits. A word-by-word `diff` of DESIGN section 8 "Final text" paragraph (`orchestrator-mode.md:679`) against `WORKER-CONTRACT.md:277` printed nothing (302 words each); WC-16 opens "On every coordinator wake or wait timeout, at most once every 5 minutes" as approved in `OQ-3-addendum-wc16-wait-timeout-decision.md:21`; `sweep.md:22` carries the approved cap sentence (`:23` of that record). The WC-16 text holds no lock sentence. | PASS |
| C13 | Routing and doc rows R1 to R8 each appear once and no more. R1 and R2 and R3 (diff hunks of `HOW-WE-WORK.md` at base lines 331 and 401, one added row and one added bullet; copy byte-equal), R4, R5, R6, R7, R8 verified in the `git diff "$BASE"` output; no row removed or reworded; the level table untouched (no hunk near it). | PASS |
| C14 | Revision authority respected: no runtime detector or Python change from the exception. `grep -rniE 'chat-summary\|exempt\|coordinator assignment' src/superclaude/cli/sweep`: 0 matches; `src/superclaude/commands/sweep.md` and the skill hold 0 `src/superclaude` strings (grep count 0); installed HOME style `~/.claude/output-styles/pragmatic.md` (mtime 2026-11-11 16:25, before the 7.10 authorization at 2026-11-11T20:26Z) differs from the edited canonical file and is not written by this task. | PASS |
| C15 | DESIGN edits are the five required fixes plus the owner decisions and the scoped addendum. `git diff --no-index -U0 artifacts/design-base.md docs/designs/orchestrator-mode.md` (64 hunks) read in full: R3-B1, R3-B2, R3-B3, R4 (renumbering, cadence, line re-anchors), R5 (owner decision, D10), step 1.0a and 1.16a text, the "Fix cycle 3" log, and the appended scoped addendum (`orchestrator-mode.md:1049-1051`, which names the early-edit exception, 11.3 and 11.4 only). The "Run not confirmed" fifth case and the extra fixtures come from the gate fixes recorded in the R3-B3 and R5 log rows. No edit outside these. | PASS |
| C16 | Evidence files checked, not trusted. `phase14-scoped-pytest.md` (3220 passed) re-run here: `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend -q -p no:cacheprovider` gave 3220 passed in 58.46 s. `uv run ruff check` on the sweep package, `main.py`, the new and edited tests: all checks passed. `make verify-sync`: "All components in sync." `uv run ruff format --check src/ tests/`: 12 files would be reformatted, all Markdown or fixtures with Python code blocks (listed: `src/superclaude/examples/release-spec-template.md` and 11 more), none of them a file this task changed (set difference with the change set is empty); the cause is ruff 0.17.3 on PATH against the `pyproject.toml:54` pin of 0.15.20. | PASS |
| C17 | The 3 failures of `phase14-full-pytest.md` argued as pre-existing. Two ruff tests (`tests/cli/eval/test_claude_process_adapter.py:417` and the next): `.venv` holds no ruff module or script (`ls .venv/bin` count 0, site-packages count 0), and `git diff --stat "$BASE"` over `src/superclaude/cli/eval tests/cli/eval tests/hooks src/superclaude/hooks pyproject.toml uv.lock Makefile` is empty, so the claim holds. The timing test `tests/hooks/test_launch_level_guard.py::test_speed_large_commands[1MB-big]` (line 1252): same empty diff over its inputs; I did not re-run it (the lens limits runs to the sweep, commands, core, skills and recommend folders), so its "passes alone" claim stays the producer's. Nothing in the change set reaches those paths. | PASS (timing claim not re-run) |
| C18 | Pipx decision (A). `OQ-10-pipx-decision.md:20-23` records option (A) from the owner's message; `artifacts/sweep-help-pipx.txt` shows `pipx run --spec` output (the "already on your PATH ... Downloading and running anyway" notice, `sweep --help`, `exit=0`); no `pipx install --force` appears anywhere in the change set. | PASS |
| C19 | Staging and mirrors. `git diff --cached --name-only` has 0 `.claude/` entries; `.claude/{agents,commands,hooks,skills,templates}` show only as ignored (`!!`); `.dev/sweeps/` is ignored (`git check-ignore -v` names `.gitignore:256`) and holds only two older live-check reports. | PASS |

## Checks

| id | result |
|---|---|
| C1 | PASS |
| C2 | PASS |
| C3 | PASS |
| C4 | PASS |
| C5 | PASS |
| C6 | PASS |
| C7 | PASS |
| C8 | PASS |
| C9 | PASS |
| C10 | PASS |
| C11 | PASS |
| C12 | PASS |
| C13 | PASS |
| C14 | PASS |
| C15 | PASS |
| C16 | PASS |
| C17 | PASS |
| C18 | PASS |
| C19 | PASS |

## Self-audit

Tool calls that back the verdict: `git diff "$BASE"` over all 12 edited files read in full; the 64-hunk DESIGN diff read in full; `comm` of real versus inventory paths; word-level diff of WC-16 (design versus contract); counted keys of `UNATTENDED_EXPECT`; greps for WC-9 and lock-retry text in code, primitives, tests, docs and design; `commands.py` read in full; `probes.py` header, allowlist and `agentWait` helpers read; `sweep.md` and `SKILL.md` read in full; the revision `BUILD-REQUEST.md`, `design-addendum.md`, `delta-manifest.md`, the OQ-1, OQ-3 addendum and OQ-10 records, `owner-decisions.md`, `step-7.10-style-exception.md`, `test-sweep-command-summary.md`, `phase11-validation.md`, `phase14-*.md` and `followups.md` read; the scoped pytest, ruff check and `make verify-sync` re-run. Not done: reading every line of `classify.py`, `report.py`, `models.py` and the 12,000 lines of tests (this lens judges scope, not correctness; their public names and options were compared with DESIGN 7.1 and 7.2); the timing test was not re-run. A zero blocking result here means every one of the five lens predicates was tested and none held.

## Verdict

Verdict: PASS
Blocking count: 0
