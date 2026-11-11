# Revise 1

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (edited in place). IDS: M1, M2, M4, M5, M6. Baseline copy: specs/history/spec-v1.md (57763 bytes).

## Byte accounting
- Before: 57763 bytes. After: 58254 bytes. Net +491.
- Per finding id (bytes added / deleted; M4 shares M1's edit, counted once under M1):

| id | added | deleted |
|---|---|---|
| M1 (and M4) | 66 | 19 |
| M2 | 193 | 96 |
| M5 | 213 | 124 |
| M6 | 332 | 74 |
| M4 | 0 (same edit as M1) | 0 |

(Added/deleted measured as the differing span of each replaced string; sum of net = 491.)

## Findings
| id | disposition |
|---|---|
| M1 | Applied, AC-1.1 (spec:195) narrowed to P1 commands except `load`; spec:76 and spec:159 say `load` gets no section. Cites the reviewer's own preferred narrowing; load row (spec:112) and Decisions (spec:265) left unchanged. |
| M2 | Applied, AC-0.4 (spec:194): steps 1-2 and 5-7 as written; step 3 passes on exactly one `worker_done` with the command's existing report file as report path (spec:182 left as is for later phases). |
| M4 | Applied by the M1 edit (same contradiction: AC-1.1 vs spec:112/265); no separate text. |
| M5 | Applied: AC-1.1 and AC-1.2 (spec:195-196), the P1 flag rule (spec:159) and spec:76 scoped to P1 commands, so implement, post-release and pr-submit (P4, spec:109,113,114) and P2/P3 commands get their section in their own phase and D2-D4 are not pre-empted (spec:154,162). |
| M6 | Applied: one coordinator-supplied directory flag `--report-dir` for workflow, research and tdd added to WC-4 (spec:62), the workflow, tdd and research rows (spec:90,92,116) and the AC-2.2 example (spec:200); workflow writes pre-creation STOP contracts there. Not applied: the review's out-of-workspace `CMD:460` corroboration (UNVERIFIED, not relied on, as verify-1.md noted); stale `--output` claim at spec:120 untouched (not named by a blocking finding). |

M3 was rejected by the verifier (verify-1.md) and left alone, as were Medium/minor items. No PASS is claimed.
