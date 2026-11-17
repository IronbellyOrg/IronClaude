# Diff Analysis: reflect-pre reviewer cards (3 variants)

## Metadata
- Generated: 2026-11-13T03:41Z
- Variants compared: 3 (reviewer-1 analyzer/sonnet, reviewer-2 qa/haiku, reviewer-3 refactorer/opus)
- Total differences found: 21
- Categories: structural (1), content (8), contradictions (2), unique (8), shared assumptions (2)

## Structural Differences

| # | Area | Variant 1 (analyzer) | Variant 2 (qa) | Variant 3 (refactorer) | Severity |
|---|---|---|---|---|---|
| S-001 | Card shape | 8 findings, table-row lens (decision tables, fold) | 4 findings, coverage/AC lens (broad claims, fewer citations each) | 12 findings, dependency/convention lens (most citations per finding) | Low |

## Content Differences

| # | Topic | V1 approach | V2 approach | V3 approach | Severity |
|---|---|---|---|---|---|
| C-001 | Task 11 assertion gating | F1 MAJOR: first AC satisfied by defining 12 names; behaviours (retry, already_in_state, short timeline, moved head) ungated | F2 MAJOR blocking: same defect, wider list (crash before/after every request/settle, single retry, release_pending reporting) | — (not covered) | High |
| C-002 | Wave 0 bullet vs AC wording (H1) | F2 MINOR: tension; "gate wording" qualifier makes it implementable but a literal test author writes unpassable test | — | F1 MINOR: "Read literally, the real bullet fails"; spec has same tension | Medium |
| C-003 | Corrupt-line fold invariant (H4) | F6 MINOR (+ notes/auto_merge_armed also ungated) | F4 MINOR (Task 5 identifies no existing gating test) | F9 MINOR (same, cites Task 5 AC) | Low |
| C-004 | Byte-pin strength (start-text vs full sentence) | — | F3 MINOR: prefix constants cannot prove whole sentence unchanged | F5 MINOR: same defect, cites Task 1 AC + Task 10 AC | Low |
| C-005 | Clear-command literal text | F5 MINOR: Task 8/11 ACs assert reason/halt, not message content | — | F8 MINOR: three different literal forms across Tasks 8/12/13 | Medium |
| C-006 | Cycle-id minting duality | F8 MINOR: Task 10 bullet vs Task 8/O1 single place | — | F12 MINOR: same, no AC ties bullet to O1 place | Medium |
| C-007 | fold→guard_status cause wiring | F3 MINOR: fold table never sets disabled_cause user_override; Task 3 fold ACs omit row | — | F11 MINOR: RELEASE_PENDING not_applied case untested (fold that always returns HELD passes) | High |

## Contradictions

| # | Point of Conflict | Position A | Position B | Impact |
|---|---|---|---|---|
| X-001 | T1 card H3 "dependency completeness" | T1 card (orchestrator): every consumer declares its producers | V3 F2 MAJOR: Tasks 9, 10, 12, 13 read ./artifacts/pre-build-gate.md (Task 1 output) with no direct Depends on: Task 1 (only transitive via Task 8) | Medium — H3 overstated; direct-declaration rule (source.md:363) violated as written |
| X-002 | Blocking severity of Task 11 gating defect | V1 F1: MAJOR, blocking:false | V2 F2: MAJOR, blocking:true | High — merge must pick one |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V2 | F1 MAJOR blocking: Task 8 omits section 4.2 event-field construction (idempotency_key format, k increment); no AC gates event-field pairing | High |
| U-002 | V3 | F4 MAJOR: O2 front-matter script grant has no owning task; Task 9 edit list omits front matter | High |
| U-003 | V3 | F6 MINOR: two new test files absent from spec files-to-change table; section-7 tests relocated | Medium |
| U-004 | V3 | F7 MINOR: 12th named test narrowed vs its spec mapping (exit codes moved to Task 7 file) | Medium |
| U-005 | V3 | F10 MINOR: unordered tasks (5/7, 9/12) edit same files; parallel-run conflict risk | Medium |
| U-006 | V1 | F4 MINOR: guard_status halt→unavailable mapping has no owner; signature cannot see a halt | Medium |
| U-007 | V1 | F7 MINOR: Task 2 "grep 43" AC is a manual reading, no mechanical pass condition | Medium |
| U-008 | V3 | F3 MINOR: H2 confirmed — Task 13's Depends on Task 2 is a no-op superset | Low |

## Shared Assumptions

| # | Assumption | Source agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | The plan's ACs are the only gating mechanism; task-body prose that an AC does not verify is a plan defect (family: constraint without matching AC) | V1 F3/F4/F6, V2 F4, V3 F9/F11 all file findings on this basis; none questions it | Medium | UNSTATED (no reviewer cites the workflow executor's actual AC-vs-prose behavior) |
| A-002 | Frozen-pair audit vantage: all three reviewers audited the plan text as the artifact, ignoring landed HEAD code (attribution note followed) | Zero findings cite HEAD source | Low | STATED (attribution note in every brief) |

## Summary
- Structural: 1; Content: 7; Contradictions: 2; Unique: 8; Shared assumptions: 2 (1 UNSTATED promoted: A-001)
- Highest severity: C-001 (Task 11 assertion gating, High), X-002 (blocking flag conflict), C-007 (fold wiring, High), U-001, U-002
- Total diff points for convergence: S-001, C-001..C-007, X-001, X-002, A-001 = 12
