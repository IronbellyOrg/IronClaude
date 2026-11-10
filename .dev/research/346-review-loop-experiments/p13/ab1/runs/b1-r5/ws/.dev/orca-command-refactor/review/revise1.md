# Revise 1

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Input: `review/round1.md` (Reviser brief, lines 258-262: L1, L2, L16). No spec-panel was run. Citations to spec lines are post-edit line numbers of the candidate; `round1.md:N` for the review. Citations to files outside the workspace (`.dev/codegraph-migration/...`, `src/...`) are UNVERIFIED.

## Byte accounting

Before 57763 bytes, after 59544 bytes (`wc -c`), net +1781. Added/deleted bytes per finding id (character-level diff of each replaced span, UTF-8):

| id | added | deleted | note |
|---|---|---|---|
| L1 | 1794 | 268 | contract path, status mapping, retries, P0/P1 consistency, checks |
| L2 | 355 | 266 | SA-2 sentence, AC-C1 moved to a code block |
| L16 | 188 | 22 | section 1.4 (1), E3 |
| total | 2337 | 556 | net +1781 |

## Finding rows

| id | action | where / reason |
|---|---|---|
| L1 t1b F1 (adversarial path) | applied | adversarial row (section 3.1) now says `<output>/return-contract.yaml`, the WC-4 path. |
| L1 t1b F2, t3-1 F5 (AC-1.1 vs load, brainstorm) | applied | AC-1.1 asserts the section for the commands section 6 lists for P1, except `/sc:load`; P1 list gains brainstorm and init-lite (`round1.md:41-45,139-143`). |
| L1 t1b M2, t2 F6, t3-1 F2 (retry overwrite) | applied | WC-6 and section 2.3 make the brief give every attempt a new path; init-lite row says so. |
| L1 t1b M3, t2 F12 (flag before gate) | applied | P1 row: flag and section only on the commands P1 lists; gated commands get it in P2-P4. |
| L1 t1b M4, t3-1 F8 (path unknown, pre-creation STOP) | applied | WC-4 path rule; workflow row adds `--output <dir>`; research row adds `--output <dir>`. |
| L1 t1b M5 (status values) | applied | WC-4: an existing differing status field is kept under its own name. |
| L1 t2 F1, t3-2 F2 (2.3 vs P0) | applied | Section 2.3: `--unattended` from P1 for P1 commands; P0 runs without it. |
| L1 t2 F3, t3-1 F9, t3-2 F1 (status-less contract = succeeded) | applied | WC-5: absent, empty, unparseable, missing or unknown status maps to failed. |
| L1 t2 F7, t3-1 F1 (AC-0.4 step 3/4) | applied | AC-0.4 and 7.2 steps 3-4 give a P0 form: section 3.1 "Report today" file and `test -s`. |
| L1 t2 F8 (optional ask) | applied | AC-2.2 brief forbids `ask`. |
| L1 t2 F9, t3-1 F3 (no dir, `--output <file>`) | applied | WC-4: `<file>.return-contract.yaml` beside a file output; a command with no output option gets one in its row. |
| L1 t2 F13 (skills) | applied | Section 2.1 and AC-2.1: gate edited and asserted where written (command or skill). |
| L1 t2 F16 (absent agentWait) | applied | 7.2 step 2, citing `CAPS:129`. |
| L1 t3-1 F4 (WC-3 vs implement Ruling) | applied | WC-3 exception for rows that say stop (D2). |
| L1 t3-2 F4 (WC-7 untested) | applied | 7.2 step 5 also searches for an Agent-tool call carrying the command line. |
| L1 t2 F15, t3-1 F10, F11 (coordinator timeouts, write order, ask cap) | rejected | Requirements the text never states (missing-requirement, Medium under the grading check, `document_review_loop_prompts.md` FIRST-REVIEW grading); the brief forbids adding rules no blocking finding needs. |
| L1 t2 F17 (schema version), F18 (two truths) | rejected | Missing requirement, Medium; not stated text that does harm. |
| L1 t3-1 F12 (WORKER-CONTRACT.md not installed) | rejected | Missing requirement, Medium. |
| L1 t3-1 F13 (spec-panel row stale) | rejected | The review marks it UNVERIFIED which copy is current (`round1.md:195-197`); not checkable here. |
| L2 (AC-C1) | applied | AC-C1 now a fenced block with plain `|` alternation, scanning commands, skills and agents only (not core); SA-2 reworded so the contract file under core may name Orca. AC-C4, AC-C5 and AC-0.3 keep `\|` inside table cells (not named by L2). |
| L16 (1.4 vs E3) | applied | Section 1.4 (1) states both facts and marks the route UNVERIFIED; E3 carries the same mark. Inventory side: `INV-A:13,35` says direct; unchanged. |

## Fix map

```fixmap-v1
{"id": "L1", "action": "applied", "reason": "Contract path, status mapping, retry paths, P0/P1 scope, AC-0.4, AC-1.1 and 7.2 steps 2-5 repaired; Medium missing-requirement sub-claims left alone."}
{"id": "L2", "action": "applied", "reason": "AC-C1 moved to a code block with real alternation and no core scan; SA-2 wording aligned so the contract file may name Orca."}
{"id": "L16", "action": "applied", "reason": "Section 1.4 (1) and E3 now agree that the route of the PR #329 run is UNVERIFIED."}
```
