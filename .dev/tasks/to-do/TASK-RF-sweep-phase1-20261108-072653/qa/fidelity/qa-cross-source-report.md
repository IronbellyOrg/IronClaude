# QA Report - Fidelity, cross-source contradiction lens (T342)

**Date:** 2026-11-13
**Reviewer:** rf-qa-qualitative (fix_authorization: false)
**Prompt:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/fidelity/prompts/T342-prompt.md`

## Section A - Authority map (DESIGN addendum, owner decisions)

Authority read from disk (each file read in chunks of at most 150 lines):

| Authority | What it governs | Evidence |
|---|---|---|
| DESIGN `docs/designs/orchestrator-mode.md` (1052 lines) | Wins over SPEC where section 13 (D1-D10) or an owner record says so | read 1-1052 |
| Resolved addendum `revisions/chat-output-exception-20261109-133150/design-addendum.md` | Normative only for 7.6, 15.2 GQ-63 mapping, 17 item 20 boundary and style rollback (addendum:9; DESIGN:1052) | read 1-45 |
| `OQ-6-GQ-63-done-next-decision.md` | Owner chose (b), exception; planning only (lines 32-35) | read |
| `OQ-1-agent-wait-decision.md` | Owner allowed `worktree ps --agent-wait` (lines 19-21); backs D10 | grep |
| `OQ-3-GQ-11-rule-id-decision.md` + `OQ-3-addendum-wc16-wait-timeout-decision.md` | WC-16 and its text; "wake or wait timeout" wording; sweep.md trigger line | read addendum, grep first |
| `OQ-17-cursor-template-decision.md` | Exactly 10 templates, no cursor template | grep |
| `OQ-7-D9-signoff-decision.md` | D9 signed off as written | grep |
| `FINAL-GATE-halt-resolution-decision.md` | Owner edit of DESIGN :491 and :760 (Rule 5 inert); revert FIN-F7 skill edit | read |
| `FINAL-GATE-cycle2-scope-decision.md` | Owner edit of DESIGN :614 (and :615 banner for unscanned `worktree ps`) | read |
| `FINAL-GATE-FIN-F7-ruling.md` | FIN-F7 (outage not shown in the exempt chat reply) is a documented Phase 1 limitation | read |

Style anchor check: `git diff -U0` of `src/superclaude/output-styles/pragmatic.md` shows `-22` held "No exceptions" and `+22..+26` hold the scoped exception; the other hunks are lines 57, 62, 64, 73, 84, 94 only. Nothing at or after `## Work discipline` (line 107) is in the diff.

## Section B - SPEC vs DESIGN disagreements and delivery position

Each row: SPEC text, DESIGN text, what the delivery on disk does, and the authority. "Follows" = the delivery follows DESIGN.

| # | SPEC (merged-requirements.md) | DESIGN (as it stands) | Delivery evidence | Authority | Grade |
|---|---|---|---|---|---|
| 1 | Module table :199-200, :448: `write_report` in `report.py` | No `write_report`; `commands._publish` is the one write (3.1) | `commands.py:153` `_publish`, `:275` call; grep finds no sweep `write_report` | DESIGN D1 | authorized, no note |
| 2 | :174-175, :453: exclusive create, partial file tolerated | temp + fsync + `os.link` commit point, exit-1 rule 3.4 | `commands.py:186` `os.link`; `:199` name-space message | DESIGN D2 | authorized |
| 3 | FR-002/FR-019 message without reason | `Orca unavailable (<reason>); ...` | `probes.py:369` | DESIGN D3 | authorized |
| 4 | No cell limit | `CELL_MAX` 200 | `report.py:24`, `:603-605` | DESIGN D4 | authorized |
| 5 | No future-timestamp rule | note `timestamp in the future` | `classify.py:82` `NOTE_FUTURE`, used `:233` | DESIGN D5 | authorized |
| 6 | WC-14 text (:405-407): "On every coordinator wake ... sweeps on every wake" | WC-16, 5-minute cap, `/sc:sweep` an added read, SP-27 sentence (7.4 final text, DESIGN:680) | `WORKER-CONTRACT.md:277` equals DESIGN:680 byte for byte (shell string compare printed `WC16_TEXT_IDENTICAL`); new heading at `:275` after the fan-in paragraph `:273` | DESIGN D6 and `OQ-3-GQ-11-rule-id-decision.md`; "or wait timeout" words by `OQ-3-addendum-wc16-wait-timeout-decision.md:21-22` | authorized (see N1) |
| 7 | Rule 5 (:253; FR-006 AC at :100: "each class name is reached at least once") | Rule 5 inert until open item 6 closes (:491), `working` case expects fallback, every class but `working` reached (:760) | `classify.py:251-257` `_rule_working` returns None, four conditions kept as comment; `tests/sweep/test_classify.py:368,372-376` | Owner edit of DESIGN :491/:760 by `FINAL-GATE-halt-resolution-decision.md` (item 2); section 13 deliberately unchanged | authorized, MINOR note N2 |
| 8 | `unpushed N` (:335) | `bool or None` (D8) | `models.py:179`, `probes.py:886` | DESIGN D8 | authorized |
| 9 | SP-29 / FR-010 (:104) | D9 narrowing | not re-audited here (fidelity partition of other agents); sign-off exists | DESIGN D9, `OQ-7-D9-signoff-decision.md:40-42` | authorized |
| 10 | NFR-003/014: eight templates, `worktree ps` never `--agent-wait` | ten templates, `FORBIDDEN_TOKENS` only `--include-remote` | `probes.py:49-62` (10 tuples, set of one token) | DESIGN D10; `OQ-1-agent-wait-decision.md:19-21`; `OQ-17-cursor-template-decision.md:37-38` | authorized |
| 11 | Header: one banner `child worktrees not discovered: Orca unavailable ...` (:369) | two banners, the second for Orca answered but `worktree ps` unscanned (:614-615) | `report.py:33`, `:36-37`, `:169-176`; pins `test_report.py:650,665,683`, `test_cli_contract.py:443` | Owner edit of DESIGN :614/:615 by `FINAL-GATE-cycle2-scope-decision.md` (FIN-F5) | authorized, MINOR note N3 |
| 12 | FR-017 (:111): failed publication exits 1 | exit 1 also when unlinking the temp file fails after the commit point, no success JSON (3.2 step 7) | `commands.py:206` | DESIGN "Not counted as deviations" (:846), its own joint reading of FR-017 and NFR-001; no owner record | follows DESIGN, MINOR note N4 |
| 13 | FR-022/B4: skill "only runs the CLI, reads report_path and summarises" (:209) | 7.6 step 4: print counts and path; addendum: exempt final reply is counts and path only | Skill `SKILL.md:25-27,31-51`; style `pragmatic.md:22-26` | Addendum :13-21, :27-29; OQ-6 decision :32-35 | authorized (see N5) |
| 14 | Style `pragmatic.md:22` "No exceptions" (pre-7.10 anchor) | Scoped exception, seven sites | `git diff -U0`: `-22`; `+22..+26`; `57,62,64,73,84,94` qualified with the literal `Except for the sweep chat-summary exception above,` (6 lines) | Addendum :13-27 | authorized |
| 15 | FR-023 `RULE_PHRASES["WC-14"]` | `"WC-16"` pin, 9-entry never-as-worker, rename, `UNATTENDED_COMMANDS` assertion | `git diff -U0 tests/skills/test_worker_contract.py` shows exactly those four hunks | D6 | authorized |

Addendum-versus-style comparison (addendum :13-27 against `pragmatic.md:22-26,57,62,64,73,84,94`): the five conditions, "final successful reply only", the "no table, wrapper, recommendation, advice, gloss" list, the assignment-source rule, the person-run exclusion, the three same-message/independent-coordinator cases, the unknown/revoked/conflicting rule, the exclusion list and the scope paragraph all appear; the six later restatements are qualified exactly six times (ADD:27); template intro says templates are non-exempt (`:62`). No contradiction found.

## Section C - Python report and unrelated action/worker rules unchanged

- Exception text location: a repository-wide count of `chat-summary exception|Except for the sweep` over `src`, `plugins`, `docs`, `tests` finds it only in `pragmatic.md` (8), `SKILL.md` (2), `test_sweep_command.py` (11) and DESIGN (1). It is absent from `report.py`, `commands.py`, `models.py`, `WORKER-CONTRACT.md` and `sweep.md`, so the exception edits no Python report code and no worker rule.
- Python report: `report.py` `SECTIONS` (`:545-558`) holds the twelve functions in DESIGN 7.5 order (header ... footer); the footer ends `Inspection only.` then `Report complete` (`:542`); `CELL_MAX` 200, `sanitize` and `cell` present. The only report change beyond DESIGN 7.5's original text is the owner-authorized second banner (row 11), not the chat exception. The sweep tree is untracked, so a `git diff` against HEAD is not available; this conclusion rests on the greps above and on 3245 passing tests.
- Worker and action rules: `git diff -U0 src/superclaude/core/WORKER-CONTRACT.md` shows only line 23 (adds `/sc:sweep` to the never-as-worker list) and the new WC-16 block `:275-277`; nothing else in the contract moved. `HOW-WE-WORK.md` has exactly two added lines (`:334` row, `:405` bullet); the plugin copy is byte-equal (`cmp` printed `PARITY_OK`). `main.py` gains the four-line `sweep_group` registration. `.gitignore` gains the two `.dev/sweeps/` lines.
- Command and skill authority limits: `sweep.md:9` `allowed-tools: Skill`; `SKILL.md:4` exact literals `Bash(superclaude sweep run:*), Bash(uv run --frozen --no-sync superclaude sweep run:*), Read`; steps 1-2 keep PATH first, "command not found" only, timeout 120000 ms; `SKILL.md:61-64` Will Not list keeps no advice, no edit/stage/delete, no extra tool; no `src/superclaude/` substring (phase11-validation grep exit 1).
- Severity modules: `tests/skills/test_review_severity_rule.py` and `tests/skills/test_implement_severity_static.py` do not appear in `git status` as modified; phase11-validation.md ran them inside the 718-test command.
- Fresh runs by this reviewer: `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend -q` gave `3245 passed in 61.29s`, exit 0; `uv run ruff check .` gave `All checks passed!`, exit 0. No file was edited by those runs; the two temp output files in /tmp were deleted.

## Findings

No BLOCKING or MAJOR finding. Every SPEC/DESIGN disagreement found is either a DESIGN section 13 row (D1-D10) or is covered by a named owner record. MINOR notes:

| id | severity | evidence | what is wrong | smallest fix |
|---|---|---|---|---|
| N1 | MINOR | DESIGN `:717` (R2 bullet) says "on every wake"; DESIGN `:680` and `WORKER-CONTRACT.md:277` say "on every coordinator wake or wait timeout"; `HOW-WE-WORK.md:405` carries the R2 wording | Small wording gap inside DESIGN itself. Authorized: `OQ-3-addendum-wc16-wait-timeout-decision.md:27` says R2 and every other sentence stay as they are | None required; optionally align R2 in the follow-up issue |
| N2 | MINOR | SPEC `:100` FR-006 AC vs DESIGN `:491`, `:760`; `classify.py:251-257` | FR-006's "each class reached" is not met for `working` in Phase 1. Authorized: `FINAL-GATE-halt-resolution-decision.md` item 2 (DESIGN edit by the owner, section 13 unchanged on purpose) | None; restore Rule 5 when open item 6 closes |
| N3 | MINOR | SPEC `:369` vs DESIGN `:614-615`; `report.py:36-37,169-176` | Second header banner differs from SPEC. Authorized: `FINAL-GATE-cycle2-scope-decision.md` (FIN-F5, DESIGN `:614` edit by the owner) | None |
| N4 | MINOR | DESIGN `:846` vs SPEC `:111`; `commands.py:206` | Exit 1 on temp-file unlink failure after the commit point rests on DESIGN's own "joint reading" and has no owner record. DESIGN wins over SPEC and the delivery follows it | None; could be listed as D11 in a later DESIGN edit |
| N5 | MINOR | Addendum `:13` "summary counts and report path" vs `SKILL.md:26,43` (`(not observed in Phase 1)` mark on the stalled and fenced counts; "total is a lower bound" sentence) | The exempt reply carries two short caveats that the style (`pragmatic.md:23`) does not mention, although the skill calls itself "the same rule". Neither is advice or a wrapper, both keep the counts truthful, and the owner ruling `FINAL-GATE-FIN-F7-ruling.md:11` itself says "the lower-bound note still prints with the counts". Tests pin them (`test_sweep_command.py` DOC-F2 cases) | None blocking; one clause in the style or addendum naming the caveats would remove the asymmetry |
| N6 | MINOR | `FINAL-GATE-FIN-F7-ruling.md:15-16`; `SKILL.md:25` (step 3 takes only `report_path` and `summary`, matching DESIGN `:663`) | In the exempt reply an exit 0 run during an Orca outage looks like a normal run; the report at the printed path states the outage and the skill reads it to its last line first | Documented Phase 1 limitation by owner ruling; fix list recorded in that file for the follow-up issue |

## Checks

| Check | Result |
|---|---|
| C1 Style anchor: `pragmatic.md:22` pre-7.10 text unqualified, now scoped (git diff) | PASS |
| C2 Addendum common rule vs style lines 22-26 (all conditions, exclusions, scope) | PASS |
| C3 Six later restatements qualified exactly six times, templates marked non-exempt, work discipline untouched | PASS |
| C4 Addendum vs skill `## Final reply` (same rule, same limits, installed-path wording) | PASS (note N5) |
| C5 DESIGN 7.6 steps and allowed-tools vs `SKILL.md` and `sweep.md` | PASS |
| C6 D1-D5 and D8 delivery follows DESIGN over SPEC | PASS |
| C7 D6 WC-16: contract text byte-identical to DESIGN `:680`; pins match | PASS (note N1) |
| C8 D10 and OQ-1/OQ-17: ten templates, one forbidden token | PASS |
| C9 Rule 5 inert vs SPEC FR-006: authorized by halt-resolution record | PASS (note N2) |
| C10 Second header banner vs SPEC: authorized by cycle-2 record | PASS (note N3) |
| C11 DESIGN `:846` unlink-failure exit 1 | PASS (note N4) |
| C12 FIN-F7 limitation consistent with DESIGN 7.6 `:663` and ruling | PASS (note N6) |
| C13 Python report (12 SECTIONS, footer, CELL_MAX, no exception text) unchanged by the exception | PASS |
| C14 Worker/action rules: WORKER-CONTRACT diff limited to line 23 and WC-16; HOW-WE-WORK two lines, byte-equal plugin copy | PASS |
| C15 Severity test modules not modified | PASS |
| C16 `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend -q` | PASS (3245 passed) |
| C17 `uv run ruff check .` | PASS |

Self-audit: independently verified against source this session: the 15 disagreement rows above (greps of `commands.py`, `probes.py`, `report.py`, `classify.py`, `models.py`; byte comparison of WC-16; `git diff -U0` of style, contract, routing, tests), plus the full reads of DESIGN, SPEC, addendum, BUILD-REQUEST, skill, command, three owner FINAL-GATE records and OQ-3 addendum. Not independently checked here: the D9 join behaviour and other fidelity partitions (other agents' lenses), and the test file lines 301-637 (only the first 300 lines and the evidence summary were read; the passing run covers them). Tool use: Read 22, Grep 5, Bash 6, Glob 0; no web research. Live model adherence to the exception is not proven by any static test (stated by addendum :37).

Verdict: PASS
Blocking count: 0
