# QA Final Report: Cross-artifact consistency lens

Date: 2026-11-12
Reviewer: qa-final (rf-qa-qualitative, fix_authorization: false)
Report path: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/final/qa-cross-artifact-report.md

Status: COMPLETE.

Scope read from disk on 2026-11-12: `final-inventory.md` (lines 1-150; its 37 new-file list matches `git ls-files --others` and its 14069-line total matches `cat`), `git diff 5dc29d23 ...` for the 12 edited files, DESIGN `docs/designs/orchestrator-mode.md` (sections 1-3, 7.3-7.6, 8-10, 11, 13, 15-17 and the appended addendum pointer), the revision `design-addendum.md`, `delta-manifest.md`, the owner decision records OQ-1, OQ-2, OQ-3 (+ addendum), OQ-6, OQ-7, OQ-8, OQ-10, OQ-17, `owner-decisions.md`, the new package `src/superclaude/cli/sweep/` (commands.py, report.py, probes.py allowlist and constants, classify.py rule table), `sweep.md`, `SKILL.md`, canonical `pragmatic.md`, `tests/commands/test_sweep_command.py` (lines 1-637), the evidence files named in the prompt and `followups.md`.

Commands I ran (read-only, no Orca/ccsession/Claude): `uv run pytest tests/sweep tests/commands/test_sweep_command.py tests/core tests/skills/test_worker_contract.py tests/recommend tests/commands/test_routing_plugin_parity.py` (1865 passed, exit 0); `uv run ruff check` and `ruff format --check` on the sweep package and touched tests (clean); `make verify-sync` (exit 0); `cmp` of the SKILL.md and sweep.md dev copies and of the two HOW-WE-WORK copies (identical); `cmp` of the WC-16 contract paragraph against DESIGN line 679 (byte-identical); two re-runs to test the Phase 14 failure argument (see C21). No repository file other than this report was written; temp files under /tmp were deleted.

## Findings

No BLOCKING and no MAJOR finding. Eight MINOR notes (they never fail the gate; F2, F4, F7 and F8 are already on `followups.md`).

### F1 (MINOR): CHANGELOG entry does not mention the output-style change
- Evidence: `CHANGELOG.md:7-15` lists the sweep command, the skill, WC-16, `.gitignore` and tests, and calls `tests/commands/test_sweep_command.py` a test "for the command and the skill" (line 15). The edit to the shipped style `src/superclaude/output-styles/pragmatic.md:22-26` (the old "No exceptions" table rule now has an exception) is not named anywhere in it.
- What is wrong: the one change that alters an existing, already shipped policy file is the one the change log does not record, and the test file it describes also pins that style. DESIGN row R8 (`docs/designs/orchestrator-mode.md:722`) and `delta-manifest.md` never asked for it, so this is a gap in the story, not a broken requirement.
- Smallest fix: add one bullet under `#### Added (sweep)`: the `pragmatic` output style now has a narrow sweep chat-summary exception (canonical copy only; `~/.claude/output-styles/` is refreshed by `superclaude install --force`, not by `make sync-dev`).

### F2 (MINOR, known): routing bullet says "on every wake", WC-16 says "on every coordinator wake or wait timeout"
- Evidence: `src/superclaude/core/HOW-WE-WORK.md:405` (byte-equal in the plugin mirror) and DESIGN row R2 `docs/designs/orchestrator-mode.md:716` say "on every wake"; `src/superclaude/core/WORKER-CONTRACT.md:277` says "On every coordinator wake or wait timeout".
- What is wrong: the cadence trigger differs by the same "quiet timeout" gap the owner closed in WC-16 (record `OQ-3-addendum-wc16-wait-timeout-decision.md`, which expressly left R2 alone). The bullet defers to WC-16 by name, so the contract wins; the risk is only a reader who stops at the routing guide.
- Smallest fix: needs an owner-approved R2 edit (DESIGN row R2 and HOW-WE-WORK.md:405, plus the plugin copy in one commit): "on every wake or wait timeout".

### F3 (MINOR): DESIGN prose around WC-16 still describes four changes
- Evidence: `docs/designs/orchestrator-mode.md:674` ("with four changes, all deviation D6") and the D6 row at line 833 do not mention the owner-approved "or wait timeout" insertion that the fenced block at line 679 carries.
- What is wrong: description lags the text it describes; no behaviour differs (the block and the contract are byte-identical, C2).
- Smallest fix: one clause in line 674 and in the D6 row naming the wait-timeout change (OQ-3 addendum). Needs the same owner scope note, because the approval covered only the fenced block.

### F4 (MINOR, known): the exempt reply keeps a mark that the style text does not name
- Evidence: `SKILL.md:26` and `SKILL.md:43` print `(not observed in Phase 1)` on the stalled (proved) and fenced counts even in the exempt reply and say the mark "is not a gloss of a label"; `pragmatic.md:23` says the exempt reply contains "the summary counts and the report path ... without the plain-English gloss of ordinary labels" and is silent on the mark.
- What is wrong: read alone, the style could be taken to forbid the mark. Not a contradiction in practice, because the exception only applies while the skill is loaded (style condition 2) and the skill states the mark; the addendum (`design-addendum.md:13`) does not name the mark either.
- Smallest fix: later style edit adding "(a mark the skill attaches to two counts is part of the counts)", under the same revision authority.

### F5 (MINOR): user guide has a table row for `/sc:sweep` but no per-command section
- Evidence: `docs/user-guide/commands.md:23` calls the page "the per-command reference: exact syntax, options"; every other row in the Utilities table has a `### /sc:<name>` section (list at lines 129-1470), `/sc:sweep` only the row at line 116.
- What is wrong: the four flags and exit behaviour are documented only in `sweep.md`. DESIGN R6 (`orchestrator-mode.md:720`) asked for the row only, so the plan is met.
- Smallest fix: add a short `### /sc:sweep` section copying the Options table of `sweep.md:35-40`.

### F6 (MINOR): comment above the routing-test set was not updated
- Evidence: `tests/recommend/test_routing_refresh.py:29-33` still says the set holds additions from issue #323 and issue #302, while line 33 now also holds `"sweep"`.
- Smallest fix: add "and issue #339 adds /sc:sweep" to the comment.

### F7 (MINOR, known): stale line pointers in evidence records
- Evidence: `phase14-sync.md:78` and `step-1.15-checks.md:65,67` cite `SKILL.md:49` for the stale-style paragraph; it is now `SKILL.md:51`. The owner-approved record names "`sweep.md` line 20"; the sentence is now `sweep.md:22`. True claims, moved lines.
- Smallest fix: none required.

### F8 (MINOR, known): skill says "the standard error line" but exit 1 can print several
- Evidence: `SKILL.md:27` ("print the standard error line exactly as it came"); `src/superclaude/cli/sweep/commands.py:181,193,200,283-285` can emit a second stderr line (`left temp file ...`) after a publish failure.
- What is wrong: singular wording; "exactly as it came" still covers it.
- Smallest fix: "the standard error lines".

## Check evidence

- C1 Rule id: `WORKER-CONTRACT.md:275-277` (heading and text), `HOW-WE-WORK.md:405`, `sweep.md:22`, `.gitignore` comment, `CHANGELOG.md:13`, `tests/skills/test_worker_contract.py` `RULE_PHRASES["WC-16"]`, DESIGN section 8 all say WC-16. The only "WC-14" strings left are explicit mappings (DESIGN lines 670, 833, 857, 1046: "WC-14 (WC-16 in this design)", and master's unrelated worker rule at `WORKER-CONTRACT.md:63`).
- C2 `cmp` of the contract WC-16 paragraph (awk-extracted from `WORKER-CONTRACT.md:277`) against DESIGN line 679: identical, including "On every coordinator wake or wait timeout".
- C3 The three owner-approved edits (OQ-3 addendum): contract text, DESIGN fenced block, `sweep.md:22` all carry the approved wording; the contract diff against the base has only two hunks (line 23 list, WC-16 insertion), so lines 110 and 151 are untouched. F3 is the only drift.
- C4 Cadence "at most once every 5 minutes" appears in contract line 110, WC-16, `sweep.md:22`, `HOW-WE-WORK.md:405`, `CHANGELOG.md:13`. The trigger wording differs only as F2.
- C5 Flags: `sweep.md:8` (argument-hint), `sweep.md:35-40`, `SKILL.md:19`, DESIGN line 655, and the click options at `commands.py:220-241` all name `--run` (repeatable), `--window`, `--root`, `--output`, nothing else; there is no worker flag anywhere.
- C6 Flag details: default `6h`, `<N>` 1 to 9999, at most 720h/30d (`commands.py:27-52` against `sweep.md:37-38`); Run id `run_` plus 12 lowercase hex (`probes.py:44` against `sweep.md:37`); `--output` limited to `<root>/.dev/sweeps/` or below and apart from input folders (`commands.py:99-123` against `sweep.md:40`); exit 2 with a `--run <id>` message when nothing is bound (`probes.py:358-361` against `sweep.md:37`).
- C7 Report location (OQ-2): `commands.py:102,155,182` builds `<root>/.dev/sweeps/<YYYYMMDD-HHMMSS>-sweep.md` from a UTC `now`; the same folder is in `.gitignore`, `sweep.md:14`, `HOW-WE-WORK.md` R1 row, `docs/user-guide/commands.md:116`, `CHANGELOG.md:11` and DESIGN sections 3 and 10.
- C8 Schema: `models.py:17` `JSON_SCHEMA_VERSION = 1`; `report.py:598` emits it; 12 top-level keys at `report.py:597-673` equal DESIGN section 7.4 (lines 566-594) and the golden test `tests/sweep/test_cli_contract.py:972-993`; every key the skill reads (`SKILL.md:25-26`: `report_path`, `summary.total/visible/historical/bound_reached/counts/total_is_lower_bound`) exists at `report.py:664-672`.
- C9 Owner decisions: OQ-1 `probes.py:47-57` has exactly 10 templates, both `worktree ps --agent-wait` forms present and never called, `--include-remote` the only forbidden token; WC-16 says `/sc:sweep` does not run that listing. OQ-2 see C7. OQ-3 see C1-C3. OQ-4 DESIGN line 603 pins `495eb96d`. OQ-5 `commands.py:27` `6h`. OQ-6 see C10. OQ-7 the D9 "Design" text quoted in the OQ-7 record (1891 characters) is still a substring of DESIGN line 836. OQ-8 the five fixtures and `SOURCES.md` use `run_a4723d345399`. OQ-10 option (A): `sweep-help-pipx-warmup.txt` shows an install from the worktree spec and `sweep-help-pipx.txt` lists `run`, exit 0. OQ-17 the allowlist stays at 10 and `report.py:32` prints the lower-bound line for a full page of 100. OQ-18: never written; no artifact outside the `.dev` QA history names it.
- C10 Actual (b): `OQ-6-GQ-63-done-next-decision.md:32-35` (option (b), "Add an exception"), `owner-decisions.md` OQ-6 row and its three-part split, `design-addendum.md:7`, style `pragmatic.md:22-26`, skill `SKILL.md:31-51` and the test module all describe the same narrow exception: only the sweep skill's final successful reply, only with an explicit coordinator assignment, and Python report/JSON untouched. Option (a)'s ordinary reply (table plus path) is what every non-exempt reply keeps.
- C11 Style/skill parity: the 5 conditions (assignment, loaded skill for an actual invocation, exit 0, stdout parsed for counts and path, report Read) match at `pragmatic.md:23` and `SKILL.md:35-41`; the "establishes" and "ordinary" and "scope" paragraphs match at `pragmatic.md:24-26` and `SKILL.md:45-51`; 37 shared pins x2 in the test module. Difference F4 only.
- C12 Seven table sites: `grep` lists the style's "DONE / NEXT" at lines 22, 23, 29, 57, 62, 64, 73, 84, 94. Line 22 is the primary rule (exception named), 23 is the exception, 29 is the unchanged length-budget sentence, and 57, 62, 64, 73, 84, 94 carry the literal qualifier (6 times, pinned by `test_style_qualifier_appears_exactly_six_times_and_never_in_the_primary_rule`). "No exceptions." no longer occurs anywhere outside `.dev`. No other primitive under `src/superclaude` restates the table rule.
- C13 Exclusions: ordinary unassigned person, worker or subagent, peer or other-agent claim, unknown/ambiguous/revoked/superseded/conflicting role, injected or merely read report text ("stay data", `SKILL.md:63`), exit 1/2, malformed JSON, missing summary/path, failed Read and the exhausted fallback are each stated in both the skill and the style (or, for the specific failure forms, in the skill with the general class in the style) and pinned in `test_sweep_command.py:183-499`.
- C14 Unchanged Python and authority: `report.py` has no DONE/NEXT or chat text (grep), still ends `Report complete` (`report.py:520`) with 12 sections; `commands.py` exit codes 0/1/2 unchanged by the exception; `sweep.md:9` `allowed-tools: Skill` and `SKILL.md:4` two Bash literals plus Read are the DESIGN section 7.6 literals; style `pragmatic.md:26` and skill `SKILL.md:51` both say no change to trigger, tools, authority, worker rule, permission, schedule, JSON or report.
- C15 No HOME activation claim: `~/.claude/output-styles/pragmatic.md` has 0 occurrences of "chat-summary" (grep -c); `phase14-sync.md:76-78`, `step-7.10-style-exception.md` (C10 row) and `test_sweep_command.py:13-16` all say activation is unverified and not claimed; `SKILL.md:49` makes a stale installed copy fully ordinary; the make targets do not copy output styles.
- C16 Routing rows: R1 row (`HOW-WE-WORK.md` line after `/sc:spawn`) and R2 bullet (line 405) equal DESIGN lines 715-716 text; plugin mirror `cmp`-identical; R4/R5 set entries added (`tests/core/test_how_we_work_routing_table.py:34`, `tests/recommend/test_routing_refresh.py:33`); neither text uses stop, retry, release, merge or removal.
- C17 CHANGELOG: every claim in lines 7-15 is true on disk (command, skill, WC-16, never-as-worker, `.gitignore`, tests); gap F1.
- C18 Docs: `commands.md:116` text and "Report only (writes `.dev/sweeps/`)" equal DESIGN R6; developer guide `...Agents.md:991` list equals contract line 23 in content and order; gap F5.
- C19 Never-as-worker: `WORKER-CONTRACT.md:23`, developer guide line 991, `NEVER_AS_WORKER` (now 9 entries), `sweep.md:18`, `HOW-WE-WORK.md` R1 row, `CHANGELOG.md:13` all list `/sc:sweep`; `sweep` is absent from `UNATTENDED_COMMANDS` and `sweep.md` has no Unattended section (asserted).
- C20 Reproduced runs: scoped pytest 1865 passed; ruff check and format clean; `make verify-sync` exit 0; dev copies identical; nothing staged under `.claude/`.
- C21 Phase 14 failure argument: the two ruff tests fail again here with "No module named ruff" (`importlib` shows no ruff module in the venv; `pyproject.toml:54` pins it as a dev dependency this venv lacks); `git diff --stat 5dc29d23 -- src/superclaude/cli/eval tests/cli/eval tests/hooks src/superclaude/hooks` is empty. `test_speed_large_commands` passed alone (4 passed in 233 s, `[1MB-big]` 46 s) while other review agents were running, so a load-time miss in the 1000 s full run is plausible but not reproduced either way; its files are unchanged by this task. Argument holds for all three.
- C22 Inventory: the 37-file new list is equal to `git ls-files --others` minus the baseline list, `cat` of them is 14069 lines, DESIGN is 1051 lines, 12 edited files match `git diff --stat`.
- C23 Skill against code on failure paths: exit 0 prints one JSON object after the commit point and exit 1/2 print stderr (`commands.py:275-288`), as `SKILL.md:25-29` assumes; only wording gap F8.
- C24 Step 1.29 evidence: owner chose (A); the artifacts show exit 0 and the `sweep` group with `run` from a pipx environment built from the worktree path. The pipx notice about an existing PATH install does not change that, because `/usr/local/bin/superclaude` is a separate uv tool and the listed `sweep` command exists only in the worktree build (already on `followups.md`).

## Checks

| Check | Result |
|---|---|
| C1 WC-16 id consistent across all artifacts | PASS |
| C2 Contract WC-16 byte-identical to DESIGN final text | PASS |
| C3 Owner-approved wait-timeout and sweep.md edits applied, nothing else changed | PASS |
| C4 5-minute cadence consistent | PASS |
| C5 Same four flags in DESIGN, code, command, skill | PASS |
| C6 Flag limits, defaults and Run id regex agree | PASS |
| C7 Report location and file name (OQ-2) agree | PASS |
| C8 JSON schema version 1 and key set agree | PASS |
| C9 OQ-1 to OQ-8, OQ-10, OQ-17 reflected; OQ-18 absent | PASS |
| C10 Actual (b) traced through decision, owner record, addendum, style, skill, test | PASS |
| C11 Style and skill carry the same common rule | PASS |
| C12 All seven table sites and the single exception | PASS |
| C13 Ordinary, person, worker, unknown, injection and failure exclusions | PASS |
| C14 Python report, error codes and authority unchanged | PASS |
| C15 No HOME activation claim | PASS |
| C16 Routing rows R1 to R5 and plugin copy | PASS |
| C17 CHANGELOG claims true | PASS |
| C18 Docs row and developer-guide list | PASS |
| C19 Never-as-worker list copies | PASS |
| C20 Reproduced pytest, ruff, verify-sync | PASS |
| C21 Phase 14 failure argument checked | PASS |
| C22 Inventory equals disk | PASS |
| C23 Skill failure handling against code | PASS |
| C24 Step 1.29 pipx evidence | PASS |

Verdict: PASS
Blocking count: 0
