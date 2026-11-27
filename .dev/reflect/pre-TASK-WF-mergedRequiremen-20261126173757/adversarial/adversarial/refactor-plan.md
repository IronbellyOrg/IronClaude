# Refactoring Plan (base = variant-2-original.md, reviewer 2's card)

All paths: folder `/home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/reflect/pre-TASK-WF-mergedRequiremen-20261126173757/adversarial/adversarial/`: base `variant-2-original.md`, donor `variant-1-original.md`, evidence `diff-analysis.md`, `round1-advocate-v1.md`, `round1-advocate-v2.md`, `round2-advocate-v1.md`, `round2-advocate-v2.md`, `invariant-probe.md`. Plan under review: `.dev/tasks/to-do/TASK-WF-mergedRequiremen-20261126-173239/TASK-WF-mergedRequiremen-20261126-173239.md`; its spec: `.dev/tasks/to-do/TASK-WF-mergedRequiremen-20261126-173239/source.md`.

## Overview
The merged output is ONE review card (a verdict plus a findings table plus a coverage check), not a new plan. It takes the base card's findings and exact citations, replaces its grades with the debate's final grades, adds the donor card's findings, and adds the invariant-probe findings. 6 Blocking, 9 Medium, 12 Note after merging. Approval: auto-approved.

## Planned Changes
1. Verdict line: FAIL (blocking findings exist). Add that all three HIGH invariants of Round 2.5 are included as findings and that convergence was BLOCKED_BY_INVARIANTS.
2. Findings table, Blocking (6), each with the fix the debate settled on, using REAL plan line numbers (re-Read before citing; the donor card's lines are 31 too high and must not be copied):
   - B-1 (C-001, V1 F1, V2 QA-4): Task 2 acceptance says `ledger.py` does not import `probes.py`; Task 3 imports `RUN_ID_RE` (plan :44 and :50). Grade Blocking (Decision). Fix: `ledger.py` makes no Orca call through `probes` and imports only the names `RUN_ID_RE` and `parse_time` from it, checked by a named test (AST check of the `from ... probes import` names). (Merges INV-016.)
   - B-2 (C-005, V1 F5, V2 QA-5): Task 10 acceptance "every command and flag the doc names exists in `sweep ledger --help`" cannot hold (plan :124 vs :128). Blocking (Decision). Fix: limit the check to `superclaude` commands and flags.
   - B-3 (C-006, X-003, V1 F8, V2 QA-6): no step stages `.dev/tasks` although spec :133 requires it. Blocking (Missing). Fix: Task 11 gets a final step `git add .dev/tasks` (staging is not committing), after the last artifact write; also name that `./artifacts/` is the package folder and not the project-root `artifacts/`. (Merges INV-004.)
   - B-4 (INV-001, HIGH): Task 6 appends a hint to the "no Run bound" and "Orca unavailable" messages (plan :82) while plan :86 says the exit-2 cases of `tests/sweep/test_cli_contract.py` still pass; those tests assert the exact stderr (test_cli_contract.py:190-192, :375-389, :478-490). Blocking (Decision). Fix: Task 6 updates the expected text of those cases to include the hint and the acceptance says so (spec :83 asks for the hint, so the tests, not the spec, change).
   - B-5 (INV-002, HIGH): adding `run-ledger-record.sh` to `_FRESHNESS_SCRIPTS` fails the many existing install tests unless the seed list in `tests/cli/test_install_hooks.py` (about :89-108) also names it (install_hooks.py :267-280, :245). Blocking (Decision). Fix: Task 9 adds the script name to that seed list.
   - B-6 (INV-006, HIGH): no rule says how to parse Orca timestamps; Orca emits SQLite `YYYY-MM-DD HH:MM:SS` and ISO with `Z` or an offset (`probes.parse_time`, probes.py :413-437), so a string compare mis-orders `new`, the 24 h fallback, `added_at >= generated_at` and Task age. Blocking (Decision). Fix: Tasks 1 to 3 compare parsed UTC datetimes through `probes.parse_time` (the one allowed import of B-1), and a test feeds both forms.
3. Findings table, Medium (9):
   - M-1 (C-002, X-002, F4): plan :102 cites "the brief" with no quote; fix: Task 8 quotes the brief's sentence verbatim, and Task 11's owner-decision list names that the scratch Run was run on that authority.
   - M-2 (C-003, X-001, F2, INV-010): Task 1 `decide(..., hook_entries)` is dead (no hook entry newer than `generated_at` can be in the previous ledger) and Task 3 `merge_hook_entries` has no dedupe by id. Fix: drop `hook_entries` from `decide`; the merge replaces an existing row with the same id, names the winner and unions the reasons, and recomputes `counts` after the merge.
   - M-3 (C-004, F3, INV-012): Task 8 when `run-create` cannot be made: end with `Decision: deliver` marked UNVERIFIED; the file records zero scratch Runs created, the fixture source, and an UNVERIFIED marker separate from the `Decision:` line.
   - M-4 (C-007, QA-2): stale age must come from the Task's own timestamp; when the field is absent record the flag as null (unavailable), never fall back to the Run's `updated_at`.
   - M-5 (C-008, QA-3): `main_checkout_only` = admitted only through a main-checkout worktree (reasons are exactly live_worktree; at least one matched worktree; all matched are main).
   - M-6 (C-009, F6, INV-013): a valid ledger with an empty `runs` list: sweep proceeds with an empty Scope, header line, exit 0; Task 6 gets a named test.
   - M-7 (INV-003): Task 11 must run the ledger-path sweep from a terminal where `bind_run` fails, or assert from the `run_source` header that the ledger path was taken; the scratch Run binds this terminal.
   - M-8 (INV-014): Task 6 validates ledger ids with `fullmatch` and reuses `_check_run_ids` (or dedupes in `read_ledger`).
   - M-9 (INV-016 remainder): Task 2's check becomes the names allowlist of B-1 (merged there; counted once, listed for traceability).
4. Findings table, Notes (12): C-010 (spec path wrong, plan right), C-011 (test placement), C-012, C-013 (donor line numbers), C-015, INV-004 (merged into B-3), INV-005, INV-007, INV-008, INV-009, INV-011, INV-015.
5. Coverage check: keep the base card's grouped verdicts; update INF-020, INF-040, INF-041, INF-051 to the final findings (M-5/M-4, M-1/M-3, B-3); add that INV-001, INV-002, INV-006 concern plan text outside the matrix rows (A-003 QUALIFY).
6. Provenance tags per row (V1, V2 or probe) and the final counts: blocking 6, medium 9, note 12 (INV items merged into their parent rows are not counted twice).

## Changes NOT Being Made
- The base card's Blocking (Safety) grade on the scratch Run (QA-1): downgraded to Medium by both advocates once the owner's brief was supplied.
- The base card's Blocking grades on the stale-age fallback and the `main_checkout_only` predicate: both advocates settled on Medium.
- The donor card's Medium grade on the Task 10 check and Note grade on staging: both advocates settled on Blocking.
- The donor card's plan line numbers.

## Risk Summary
Low: the merged output is a document; nothing executes it. Rollback: keep the two original cards under `reviewer-cards/`.

## Review Status
auto-approved
