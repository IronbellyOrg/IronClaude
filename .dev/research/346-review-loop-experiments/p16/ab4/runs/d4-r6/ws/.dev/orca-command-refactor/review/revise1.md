# Revise 1 (REVISE prompt; blocking ids M1-M7)

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (edited in place). Prior version kept at `.dev/orca-command-refactor/specs/history/spec-v1.md` (identical to the candidate before editing, `cmp` clean). Inputs read: `review/round1.md`, the spec, `README.md`, `~/.claude/rules/prompts/document_review_loop_prompts.md`. The inventories were not re-read: every repair uses only text already in the spec, so no new inventory citation was added. No Medium or minor finding was touched. No verdict is claimed.

## Byte accounting

- Before: 57763 bytes. After: 59868 bytes. Net +2105.
- Over the whole file: 2250 bytes added, 145 bytes deleted (character-level diff of v1 against the candidate; most edits extend a cell, so deletions are small). No section was added.
- Net bytes per finding id (each edit is attributed to the id that calls for it; the column sums to +2105):

| Id | Net bytes | Edits |
|---|---|---|
| M2 | +412 | WC-4 location rule, including the M4 fixed-path sentence (+350), 2.3 "output path" wording (+62) |
| M4 | +283 | AC-0.4 (+63), step 3 (+95), step 4 (+67 and +58) |
| M5 | +224 | tdd (+65), release-split (+32), troubleshoot (+32) small fixes, P2 scope cell (+70), 3.1 intro (+25) |
| M6 | +535 | AC-2.2 |
| M7 | +168 | P1 load cell (+34), AC-1.2 (+19), AC-1.4 (+52 and +63) |
| M1, M3, M7 shared | +483 | section 3 intro sentence (+168), P1 Scope cell (+56), AC-1.1 (+259) |

Largest additions are AC-2.2 (M6) and AC-1.1 (M1/M3/M7); both replace a check that could not pass with one that can.

## Findings

| Id | Disposition | Where applied (spec, post-edit line numbers) | Reason |
|---|---|---|---|
| M1 | Applied | P1 Scope cell, line 159 (flag only for "the eight needs-change commands named here"; P2-P4 commands "in their own phase"); section 3 intro, line 76 (section only for 3.2 commands except load and the four 3.1 commands with a (P2) fix); AC-1.1, line 195 (test covers the eight P1 commands; "before P4 none of implement, post-release, pr-submit has one") | Removes the conflict between `:159`/`:195` and `:109,113,114,162,240`. pr-submit, implement and post-release get no section before P4, so D3 (a) holds and P1 no longer decides D2-D4. Narrowing, no new rule. |
| M2 | Applied | WC-4, line 62 (contract is `return-contract.yaml` in the directory passed; where `--output` names a file, `<file-stem>.return-contract.yaml` beside it; init-lite, with no contract phase, reports its 3.1 file); 2.3, line 73 ("output path", "contract path is known before dispatch"); line 76 ("Contract" is the file at the path WC-4 gives) | One rule for where the contract goes when `--output` is a file, as the finding's fix direction asks. It covers the tdd row (line 90) and 7.2 step 3 (see M4). |
| M3 | Applied | Same edits as M1 (lines 76, 159, 195), plus the P1 Commands cell (line 159: "load (usage line only: no flag, no section, no contract)") | Scope sentence, Commands cell and AC-1.1 now name the same set: the eight P1 needs-change commands (analyze, build, business-panel, design, document, explain, index, test). Later phases add the same assertion for their commands when the phase lands (AC-1.1 text), as the recommendation says. |
| M4 | Applied | WC-4, line 62 (a section 3 row may name a different fixed path, adversarial and workflow; workflow's `<id>` comes from the worker's `--report-path`); 3.1 intro, line 79 ("until the command's own phase adds the contract"); 7.2 step 3, line 182 (contract path WC-4 gives, or before the command's phase the 3.1 "Report today" file); 7.2 step 4, line 183 (YAML assertion only for a command that writes a YAML contract in the phase under test, otherwise `test -s <report file>`); AC-0.4, line 194 (step 4 is `test -s` on the existing report file, no YAML assertion) | Fixes (a) troubleshoot's contract "arrives in P1" (now the command's own phase; the P2 row adds it, see M5), (b) workflow's unknown `<id>`, (c) adversarial's `<output>/adversarial/` path, and the `yaml.safe_load` on markdown `REPORT.md` failure. |
| M5 | Applied | Section 3.1 small-fix cells for release-split (line 89), tdd (line 90, `<file-stem>.return-contract.yaml` beside `--output`) and troubleshoot (line 91); P2 Scope cell, line 160 | The three commands that no phase made write a contract now do, in P2, using the WC-4 text only. The `--output <file>` location comes from the M2 rule, so two tdd workers writing different files in one directory no longer share one fixed filename (WC-11). |
| M6 | Applied | AC-2.2, line 200 | The blocked-outcome check is scoped to the nine P2 commands whose row says "blocked" (recommend, cli-eval, cli-portify, review-translation, spec-panel, task, tdd, troubleshoot, release-split). The six default-applying commands (auggie-review, cleanup, improve, research, reflect, tasklist) get a check for `--outcome succeeded` with the row's default visible (flags implied, items listed unapplied, strategy pinned, headless rule followed, `--unattended` passed to reflect). Their rows (`:100,103,110,116,88,122`) were not changed. |
| M7 | Applied | P1 Commands cell, line 159 ("no flag, no section, no contract"); AC-1.1, line 195 (`load` has no section); AC-1.2, line 196 ("each of the eight P1 commands"); AC-1.4, line 198 (grep for `--checkpoint` in `src/superclaude/commands/load.md`; pass: its Usage line lists it) | `load` leaves AC-1.1/AC-1.2 and is checked by its usage-line fix only, as the recommendation says. The Decisions row at `:265` (use it inside a brief; no report file) now agrees with the phase and test text. |

## Not changed, and why

- Section 4, section 5, D1-D5, the Decisions table and the UNVERIFIED list were not touched: no listed finding names them.
- The 10 / 27 / 6 split and the inventory counts are unchanged; only the "who gets the section" rule moved.
- No new `path:line` citation to an inventory or source file was added; new text refers to spec lines and finding ids, so nothing new is UNVERIFIED.

## Procedure note

One `mkdir -p` with a relative path that went one level above the sandbox created an empty directory `runs/.snap` by mistake; it was removed at once with `rmdir`, before any edit. A helper script `d4-r6/edit.py` applied the edits and was then deleted; it is not part of the output.
