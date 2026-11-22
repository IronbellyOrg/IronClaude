# QA Report - Gate 3 content verification (qualitative), cycle 2

**Phase:** report-validation verification (qualitative), tech-ref-qualitative
**Cycle:** 2
**Date:** 2026-11-20
**Status:** Complete
**Fix authorization:** false
**Document:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md
**Previous BLOCKING list:** qa/qa-consolidated-findings-c2.md (N-1)
**Fix log:** qa/qa-fix-cycle2-report.md

## Previous BLOCKING findings

| ID | Location | FIXED-OK / STILL-OPEN | Evidence |
|---|---|---|---|
| N-1 | L354 (2.4 row 6), L1258 (5.3 G2 rule 2 paragraph), L1448 (8.1 guard-stack row); fix log also edited L2241 | FIXED-OK | Snapshot `launch-level-guard.sh:480-484` is the allow-list; `:486` sends `- -` to ESCAPE; `:487-490` lets a call whose last segment word is `--help` or `-h` through when `LL_GLOB = 0` and `${#ws[@]} - i <= 4` (comment "orca, two verb words, help"), else ESCAPE; `:489` every other call ESCAPE. Test pins `tests/hooks/test_launch_level_guard_worker.py:226-230` allow `orca list --help` (3 words) and `orca agent launch -h` (4 words); the blocked pins `:206-210` include `orca * --help` (glob) and `orca agent launch --name w --help` (6 words), both consistent with the stated limit. Current text: L354 "... is blocked, except a short help call (`<verb words> --help` or `-h`, at most four words counting from `orca`, no glob character; `orca list --help` and `orca agent launch -h` pass)", evidence cell cites `:487-490` and `:226-230`; L1258 "every other orca call is ESCAPE (`GD:480-491`), except a short help call: ... (`GD:487-490`; pinned by `test_the_read_only_orca_forms_stay_allowed_for_a_bound_worker` ... `:226-230`)"; L1448 "every other `orca` call is ESCAPE, except a short help call (...)" with `:487-490` and `:226-230` in the evidence cell; L2241 "orca verbs off the allow-list blocked (a short `--help` or `-h` call stays allowed, `:226-230`)". The statement is exact against code and tests. |

## New BLOCKING findings

None. (Columns for the record: ID | Location | Problem | Evidence | carried-over/new | previously-rated-PASS; no rows.)

## Wording check across the document (grep `every other`, `allow-list`, `--help`, `ESCAPE`, `blocked`)

- Universal claim now qualified at all four places that stated it (L354, L1258, L1448, L2241). No remaining place says every non-allow-listed orca call is blocked without the exception.
- L646, L1236, L1321, L1906 (`GUARD:480-491`), L2138 name the allow-list or G2 rule 2 without a universal "blocked" claim: no contradiction.
- L1301 (G2-D `orca terminal send` blocked) and the L1258 pins (`orca orchestration dispatch ...`, `orca terminal send --text approved`, `orca worktree create`, `orca agent launch --name w`) are true under the exception: none ends in `--help`/`-h` within four words.
- `WORKER-CONTRACT.md:66` (cited at L354) says only that the guard blocks any `--to` from a bound worker: true (`:524`), no universal orca claim.
- PR 686 / rewrite design: exactly one sentence (L218); the other `686` hits are code line numbers (`cycle.py:685-686`, `record.py:654-686`, `SET:669-686`). No `docs/designs/orchestrator.md` citation.
- Edits kept line numbers stable (L218 still the PR 686 sentence, as the fix log states) and the two edited tables keep their column counts.

## Notes (MINOR, not blocking, not rechecked)

- M-1 (L1258, wording): the G2 rule 2 sentence lists "a bare word or a lone `--`" as ESCAPE; the code (`:532`) also sends any short `-x` option to ESCAPE. Under-statement, not a false claim.
- M-2 (L354, L1258, L1448, wording): "last word" is the last word of the shell segment (`ws` is split by segment), not of the whole command; a call such as `orca list --help; rm x` is judged per segment. Harmless for the claim as written.
- M-3 (wording): the exception also lets forms such as `orca terminal send --help` and `orca orchestration dispatch --help` through (both within four words); the document's `<verb words> --help` wording covers this, but only two examples are given.

## Checks performed

1. Re-read `launch-level-guard.sh:440-570` in the snapshot (allow-list `:480-484`, `- -` `:486`, help exception `:487-490`, `LL_SA` `:485`, G2 rule 2 `:496-537`): matches the L354, L1258, L1448 line cites and wording.
2. Re-read `tests/hooks/test_launch_level_guard_worker.py:195-275`: pins `:213` (blocked), `:230` (allowed forms, `:226-227` the two help examples), `:262` match the document; the parametrisation list `:197-210` was checked against the exception (glob and six-word help stay blocked).
3. Grepped the document for `every other|allow-list|--help|ESCAPE|orca ... blocked`: all hits classified above; no remaining universal claim.
4. Read L354, L1250-1260, L1440-1451, L1080-1083 in full and the long lines L329, L334, L553, L1229, L1286, L1301, L1805, L1967, L1976 (orca context): no contradiction with the exception.
5. Chain check: ledger row 6 (L354) -> Section 5.3 G2 rule 2 (L1258) -> Section 8.1 (L1448) -> Appendix test inventory (L2241) all state the same rule with the same cites (`:487-490`, `:226-230`). Section 14 D-25 and the `orca-ide` gap (L1260, L1976) unchanged and still true: `grep -c orca-ide` on the guard = 0; case arm `orca)` at `:457`.
6. Snapshot spot-checks (all true): the worker test file has 300 lines and 11 `def test_` (L2241 "300 | 11"); the `pending` test caller at `:287`; `test_design_table_holds_all_eighteen_ids` present in `tests/hooks/test_launch_level_guard.py`; 8192 bytes / 64 arguments at `:507` and `:511`; `--to`, `--run`, `--environment`, `--pairing-code` at `:524`; prefix test `:527`; block precedence `BIG TAMPER MERGE GHWRITE PROTECTED ESCAPE MCP UNKNOWN SUBMIT REPO PUSH PUSHFORM COMMIT TURN IMPL SKILL` at `:783`; `hooks.json` carries `timeout: 5` entries (L1256 claim).
7. PR 686 count: one (L218).

## Self-Audit

**(a) Reliance list:** relied on the cycle-1 structural verification PASS (qa-verification-structural-c1.md) and on the cycle-1 content verification FIXED-OK for G3-1..G3-9 (not rechecked; only N-1 and its edit neighbourhood were in scope for cycle 2).

**(b) Independent semantic checks:** the allow-list exception verified against the live snapshot code (`launch-level-guard.sh:480-491`) and the test pins (`:195-232` of the worker test), not against the fix log; four edit locations re-read in the document; document-wide grep for any other universal claim; ten behavioural spot-checks (check 6).

Confidence: Verified: 7 / 7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 9 | Grep: 4 | Glob: 0 | Bash: 2. No web research performed.

## Verdict: PASS

BLOCKING findings: 0

Status: Complete
