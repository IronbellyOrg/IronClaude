# QA Report: Docs gate, read-only-claims lens (T294)

**Date:** 2026-11-12
**Reviewer:** qa-docs-readonly-claims (adversarial, fix_authorization: false)
**Prompt:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/docs/prompts/T294-prompt.md`

<!-- sections below are appended as checks finish -->

## Method and scope

Read from disk now (each read at most 150 lines): `src/superclaude/commands/sweep.md` (1-68), `src/superclaude/skills/sc-sweep-protocol/SKILL.md` (1-64), `src/superclaude/cli/sweep/commands.py` (1-288), `report.py` (30-60, 380-470, 591-660), `classify.py` (440-510), `probes.py` (grep of allowlist, seams, every file open and subprocess call), `src/superclaude/output-styles/pragmatic.md` (1-100), `WORKER-CONTRACT.md` (23, 110, 272-279), `HOW-WE-WORK.md` (lines 334, 405 and the diff), `docs/user-guide/commands.md` (116), the developer guide (991), `CHANGELOG.md` (5-16 diff), `.gitignore` (255-256), `tests/commands/test_sweep_command.py` (1-170 plus grep), DESIGN `docs/designs/orchestrator-mode.md` (1-30, 645-754), the chat-output-exception `BUILD-REQUEST.md` and `design-addendum.md`, the OQ-3 addendum and OQ-6 decision, and `phase11/12/13-validation.md`.

Commands run (read-only): `cmp` guide vs plugin copy; `uv run pytest` on test_sweep_command, test_how_we_work_routing_table, test_routing_refresh, test_routing_plugin_parity (447 passed) and test_worker_contract (742 passed); `uv run ruff check` and `ruff format --check` on the sweep package and `tests/commands/test_sweep_command.py` (clean); `git check-ignore`; `git diff` of every doc file. No file other than this report was written; no live Orca, ccsession or Claude command was run. DESIGN is `docs/designs/orchestrator-mode.md` (the task folder holds no DESIGN file); the revised 7.6/8/9 text was read there plus the chat-output-exception addendum.

## Findings

No BLOCKING and no MAJOR finding. Three MINOR notes (they never fail the gate).

### F1 (MINOR): "the one file it adds" omits the folder and the transient temp file

- Evidence: `src/superclaude/commands/sweep.md:14` ("the report is the one file it adds") and `:66` ("write any file except the one report"); `src/superclaude/cli/sweep/commands.py:158` (`os.makedirs(output_dir, exist_ok=True)`) and `:168-170` (dot-prefixed `.<stem>.<pid>.tmp` created, then linked and unlinked at `:186`, `:203`). DESIGN section 1 (`orchestrator-mode.md:13`) states the true behaviour: one report "plus that directory when it is new", with a temp file during publication.
- What is wrong: the command text is slightly narrower than the code. A first run creates `<root>/.dev/sweeps/` and, during publication only, one temp file that is removed before success. Neither is an Orca, git or worktree change, and the temp file is gone on every success path (a failed unlink is exit 1 with no success JSON, `commands.py:202-207`).
- Smallest fix: optional wording, "the report is the one file it adds, plus the `.dev/sweeps/` folder when it is new". Not needed for the gate.

### F2 (MINOR): the "no stop, retry, release, merge or removal" pin covers the skill only

- Evidence: `tests/commands/test_sweep_command.py:34-36` (`_FORBIDDEN_ADVICE`) and `:167-168` (applied to `_SKILL` only). DESIGN 7.6 test bullet (`orchestrator-mode.md:666`) asks for the skill only, and DESIGN section 9 rules (`:728`) say R1 and R6 avoid those words without naming a check. I grepped `sweep.md`, `SKILL.md`, the R1 row (`HOW-WE-WORK.md:334`), R6 (`commands.md:116`) and the CHANGELOG entry: none of the five words occurs, so nothing is wrong today.
- Smallest fix (optional follow-up): apply the same regex to `sweep.md` and the two rows.

### F3 (MINOR, informational): guide bullet R2 says "on every wake", WC-16 says "wake or wait timeout"

- Evidence: `src/superclaude/core/HOW-WE-WORK.md:405` vs `src/superclaude/core/WORKER-CONTRACT.md:277`. The R2 bullet is byte-identical to DESIGN row R2 (`orchestrator-mode.md:716`; verified by a fixed-string match of the 334-byte bullet) as plan item 13.1 pins it, and the OQ-3 addendum (`phase-outputs/plans/OQ-3-addendum-wc16-wait-timeout-decision.md` line 27) says R2 stays as is. Not a read-only claim. Recorded only so later gates know the drift is known and approved.

## Check details

- C1 Code is read-only: `probes.py` has three `open(path, "rb")` reads (575, 826, 890) and the only subprocess seams are `_orca` (allowlist `ALLOWED_ORCA`, lines 47-57: `run-current`, `worker-list`, `worker-show`, `task-list`, `worktree ps/list/current`) and `_git` (one entry, `status --porcelain=v1 ...`, run with `--no-optional-locks` and `GIT_OPTIONAL_LOCKS=0`, lines 289-300). No Orca write verb, no git write. `grep` for write/unlink/rename/mkdir/link/Popen/system outside `commands.py` finds only docstrings and read opens. `--agent-wait` is allowlisted but "not called" (`probes.py:56-57`; no call site).
- C2 The one write: `commands.py:_publish` is the only writer; the report goes to `<root>/.dev/sweeps/` or below (`_check_output`, 99-123) and never overwrites (`os.link`, 186). Success prints one JSON object (277-278). Matches R1, R6, CHANGELOG and `sweep.md:14` apart from F1.
- C3 `sweep.md` allowed-tools `Skill` (line 9) equals DESIGN 7.6 (`orchestrator-mode.md:655`).
- C4 `SKILL.md` allowed-tools (line 4) equals the DESIGN 7.6 literal (`:661`) exactly: two `Bash(... sweep run:*)` forms plus `Read`. Nothing wider.
- C5 Skill steps match DESIGN 7.6 steps 1-5 (`SKILL.md:23-27` vs `orchestrator-mode.md:662`); the skill relays only `report_path` and `summary`, whose keys exist in `report.to_json`/`SweepResult.summary` (`report.py:591-660`, DESIGN 468).
- C6 No stop, retry, release, merge, removal, close, restart, nudge, message, send, dispatch or Orca write verb is recommended or implied in `sweep.md` or `SKILL.md`; the only hits are negations ("Will Not", "adds no recommendation") and the unrelated words "dispatched worker" and "stage a file" in a prohibition. Verified by case-insensitive grep of both files.
- C7 Report text carries no advice: `report.py:42-55` `NEXT_INSPECTION` values all start "read ..."; `Safe to close` and `Removable` cells are never "yes" (`classify.py:447-496`: values are "no" or "could not determine"), matching DESIGN 7.5 (`:643`, `:647`). "Recommends nothing" holds.
- C8 Guide row R1 (`HOW-WE-WORK.md:334`), the plugin copy, R6 (`commands.md:116`), R7 (dev guide `:991`), R8 (CHANGELOG 7-15) and the `.gitignore` entry (255-256) match DESIGN section 9 and 10 text; R1 and R6 avoid the five words. `cmp` of guide and plugin copy exit 0. `git check-ignore .dev/sweeps/x.md` matches line 256; `.dev/tasks/to-do/x.md` is not ignored.
- C9 R2 bullet byte-identical to DESIGN row R2 (fixed-string match, see F3).
- C10 WC-16 (`WORKER-CONTRACT.md:277`) opens "On every coordinator wake or wait timeout" (owner-approved record) and ends "`/sc:sweep` recommends nothing: no stop, retry, release, merge or removal" (a negation, as DESIGN 8 specifies). It says `/sc:sweep` does not update heartbeat records or run `worktree ps --agent-wait`; the code never calls that listing and records no heartbeat. `sweep.md:20` carries the 5-minute cap and the WC-16 pointer.
- C11 Never-as-worker line 23 and dev guide 991 both list `/sc:sweep` in the DESIGN order; `sweep.md:16` and `:68` say worker never runs it and there is no worker flag (`:40`), matching code (no such option in `commands.py:219-245`).
- C12 Style exception (`pragmatic.md:22-26`) and skill "Final reply" (`SKILL.md:31-51`) state the same five conditions and the same exclusions as the design addendum; both say it is a chat-presentation rule that adds no advice, no tool, no write and no JSON or report change. It does not widen what sweep writes or changes. Source anchor `pragmatic.md:22` now holds the scoped exception, as the prompt says.
- C13 Option and flag claims in `sweep.md:33-38` match code: `--run` regex `run_[0-9a-f]{12}` (`probes.py:44`), duplicates collapse (`commands.py:92`), no-binding message asks for `--run <id>` (`probes.py:358-361`), window `[1-9][0-9]{0,3}[hd]` at most 720h (`commands.py:45-49`), `--root` must hold `.git` (55-84), `--output` limits (99-123), default 6h (27).
- C14 Records: `phase11/12/13-validation.md` show PASS lines consistent with what I re-ran (test_sweep_command, routing and contract modules pass; ruff clean; no `src/superclaude` hit in the two primitives, which I also confirmed absent).

## Checks

| Check | Result |
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

Tool engagement: Read 26 | Grep 22 | Glob 2 | Bash 6. Confidence: Verified 14/14, Unchecked 0, Unverifiable 0.

Verdict: PASS

Blocking count: 0
