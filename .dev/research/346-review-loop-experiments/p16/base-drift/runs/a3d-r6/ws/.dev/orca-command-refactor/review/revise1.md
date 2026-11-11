# Revise round 1: orca-worker-contract-spec.md

Prompt followed: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md`. Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Blocking ids: F1, F2 (`review/round1.md:120-121`). Context read first: `.dev/orca-command-refactor/README.md`. Not re-reviewed; no PASS claimed.

## Byte accounting (candidate)
- Before: 57763 bytes. After: 58141 bytes. Net +378.
- Added 608 bytes, deleted 230 bytes (four replaced fragments; a fragment serving two ids is split below only by which id it mainly repairs).

| Finding | Where | Added | Deleted |
|---|---|---|---|
| F2 | P1 scope cell, spec line 159 | 269 | 112 |
| F2 and F1 | AC-1.1 command set, spec line 195 | 149 | 39 |
| F1 and F2 | AC-1.1 negative clause, spec line 195 | 94 | 39 |
| F1 | AC-1.2, spec line 196 | 96 | 40 |

Per id (shared fragments split evenly): F1 added 169 / deleted 79; F2 added 439 / deleted 151.

## Findings
| Id | Disposition | Where applied |
|---|---|---|
| F1 | Applied | AC-1.1 (`:195`) now covers only the eight section 3.2 P1 commands other than `load` and states `load` has no section; AC-1.2 (`:196`) runs only on those commands, noting `load` writes no contract. This matches the `load` row (`:112`) and the Decisions row (`:265`), which say it gets no report file. No other text changed. |
| F2 | Applied | P1 scope (`:159`) no longer says the flag is accepted by every command in 3.1 and 3.2; it names the eight commands whose 3.2 row phase is P1 (analyze, build, business-panel, design, document, explain, index, test) and adds one clause that each later phase adds flag and section with its own gate rows. AC-1.1 negative clause (`:195`) says no P2-P4 command has the section yet. The P1 Commands cell (`:159`) was not edited: it already lists these eight plus `load` (usage line) and the ready-command fixes. |

## Notes
- Only `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` and this file were written. A temporary byte-comparison copy was made inside the sandbox and removed.
- Medium findings M1-M10 and minor notes were not touched.
- Line numbers are those of the edited file; edits did not shift line numbering (all within existing table rows).
- Evidence checked: only the review report and spec in the workspace. Citations to `src/...`, `CLAUDE.md` etc. are UNVERIFIED here and were neither added nor changed.
