# Diff Analysis: cut-list verdict comparison

Variants: V1 = opus:architect (ponytail maximalist), V2 = sonnet:qa (guard protector), V3 = opus:analyzer (evidence auditor).
Files: `variant-1-opus-architect.md`, `variant-2-sonnet-qa.md`, `variant-3-opus-analyzer.md` in this folder.
Taxonomy level (AD-5): L1 surface (wording, pointer, bookkeeping), L2 structural (module, component, organization), L3 state-mechanics (guard, invariant, state, boundary, redaction). Each point carries exactly one level.

## Metadata
- Generated: 2026-11-16 (orchestrator, read-only comparison of the three variant files)
- Variants compared: 3
- Items per variant: 39 (source brief says 36; its own ID list R1-R10, T1-T10, S1-S6, D1-D13 is 39; see X-014)
- Total diff points (S + C + X + A): 61
- Categories: structural (3), content (39), contradictions (14), unique (14), shared assumptions (5 promoted)

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|------|----|----|----|----------|
| S-001 | Scope-cell precision | Exact file:line ranges, per-test edit lists | Prose scope plus line ranges | Exact ranges plus "false parts" list | Low |
| S-002 | Use of CUT | 2 rows (T9, S2) | 1 row (S2) | 0 rows; "CUT only when every claim verifies", so everything partial is CUT-SMALLER | Medium |
| S-003 | Extra-findings layout | 17 numbered findings | Grouped: false claims, interactions, untracked files, missed, not verified | 25 false/stale claims plus 6 missed | Low |

## Content Differences (one row per item; verdict then confidence)

Severity: Low = same verdict and same scope; Medium = same verdict family, different scope or the owner-vs-agent split; High = verdicts differ in kind (KEEP vs CUT-SMALLER, or CUT vs KEEP).

| # | Item (level) | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | R1 dead code (L2) | CS 85: cut all but read_questions stub; also cuts `CODES` | CS 75: same, but KEEP `adapter.CODES` (moving it makes the closed-set assert circular) | CS 80: cut all, `CODES` moved into test; `CLOSURE_EVIDENCE` too; unused imports | Medium |
| C-002 | R2 panel slim (L2) | CS 80: delete `count_text` only | KEEP 80 | CS 65: delete `count_text` only | High |
| C-003 | R3 unrecognised keys (L3) | CS 55: drop 5 row fields, keep their key paths in known tree | KEEP 80: dropping fields makes every row count 5 unrecognised | CS 70: drop only the two aggregate counters `ParsedPage.unrecognised_keys` and `Coverage.unrecognised_keys` | High |
| C-004 | R4 inspector scroll (L2) | KEEP 75 | KEEP 70 (note for owner) | DEFER-OWNER 80 | Medium |
| C-005 | R5 width table (L2) | KEEP 70 | KEEP 70 | KEEP 80 | Low |
| C-006 | R6 counts strip (L3) | KEEP 75 | KEEP 75 | KEEP 75 | Low |
| C-007 | R7 CycleResult fields (L2) | KEEP 80 | KEEP 80 | KEEP 75 | Low |
| C-008 | R8 question gate constant (L3) | KEEP 85 | KEEP 85 | KEEP 85 | Low |
| C-009 | R9 error mapping helper (L3) | KEEP 65 | KEEP 65 (needs new question-path tests first) | CS 55: share the exception-mapping block only | Medium |
| C-010 | R10 evicted-key list (L3) | KEEP 75 | KEEP 85 | KEEP 90 | Low |
| C-011 | T1 golden 5 to 2 variants (L2) | KEEP 75 | KEEP 80 | KEEP 75 | Low |
| C-012 | T2 recorder-script tests (L2) | CS 65: delete :333-366 and :596-638 | CS 60: delete :333-365 only | DEFER-OWNER 75: will the recorders be rerun | Medium |
| C-013 | T3 pty key tests (L3) | KEEP 60 | KEEP 75 | CS 75: drop burst (:133-151) and resize (:208-222) only | High |
| C-014 | T4 fixture-content tests (L2) | CS 65: delete :226-230, :258-278, :291-297 | CS 60: delete :258-297 | CS 70: delete :258-297 | Medium |
| C-015 | T5 fake-mailbox tests (L3) | CS 70: delete :148-171 and :192-203 | CS 55: same | CS 75: delete :192-203 only (:148-171 is a real Collector test) | Medium |
| C-016 | T6 source-text greps (L3) | CS 65: cut 3 (test_view, test_export, test_collector) | CS 70: cut 1 (test_view :864-869) | CS 65: cut 4 (adds test_terminal :214-231) | Medium |
| C-017 | T7 duplicate leak scans (L2) | CS 75: merge into test_fixtures :185 | CS 65: remove only the SENSITIVE loop (about 6 lines) | CS 65: fold in, four extras not two | Medium |
| C-018 | T8 vacuous assertion (L3) | CS 90: fix `or True`, keep 27 | CS 85: same | CS 85: same | Low |
| C-019 | T9 no-blink duplicate (L3) | CUT 70: delete test_terminal :64-70, keep test_render :182-190 | KEEP 80 | CS 55: if one goes, drop test_terminal :65-71 | High |
| C-020 | T10 variant parametrization (L2) | KEEP 75 | KEEP 75 | KEEP 75 | Low |
| C-021 | S1 drop snapshot questions group (L3) | DEFER-OWNER 80 | DEFER-OWNER 60 | KEEP 80 | Medium |
| C-022 | S2 schema check at import (L2) | CUT 85 | CUT 70 | CS 70: keep `SCHEMA_VERSION` (used at export.py:195) | Low |
| C-023 | S3 write-back doc pointer (L1) | KEEP 80 | KEEP 90 | DEFER-OWNER 80 | Medium |
| C-024 | S4 collection counters (L3) | KEEP 85 | KEEP 80 | KEEP 85 | Low |
| C-025 | S5 opt-in live snapshot (L2) | DEFER-OWNER 80 | KEEP 80 | DEFER-OWNER 85 | Medium |
| C-026 | S6 trim snapshot doc (L1) | KEEP 70 | KEEP 80 | CS 65: delete Options table only | Medium |
| C-027 | D1 one list of owner questions (L1) | CS 60: ODR survives, fix 6 and 8, pointers | CS 65: fix stale rows in place, no collapse | CS 70: fix 6 and 8, replace prd 12.1 by pointer | Medium |
| C-028 | D2 stale status sweep (L1) | CS 75: QUESTION-OBSERVATION lines only (plus rendering-rules.md:89, commands.py:453) | CS 75: same set | CS 75: same set | Low |
| C-029 | D3 archive final-review rounds (L2) | DEFER-OWNER 80 | DEFER-OWNER 65 | DEFER-OWNER 80 | Low |
| C-030 | D4 brainstorm adversarial (L2) | DEFER-OWNER 85 | KEEP 90 | DEFER-OWNER 90 | Medium |
| C-031 | D5 spine copy (L2) | DEFER-OWNER 75 | DEFER-OWNER 60 | DEFER-OWNER 80 | Low |
| C-032 | D6 UX folders (L2) | DEFER-OWNER 80 | KEEP 80 | DEFER-OWNER 80 | Medium |
| C-033 | D7 PRD scaffolding (L2) | DEFER-OWNER 75 | DEFER-OWNER 60 | DEFER-OWNER 80 | Low |
| C-034 | D8 register rows (L1) | CS 55: remove rows :51 and :64 only | KEEP 70 | CS 55: remove :45 and :52 only | High |
| C-035 | D9 handoff snapshots (L1) | DEFER-OWNER 75 | KEEP 80 | DEFER-OWNER 80 | Medium |
| C-036 | D10 twin owner-decisions file (L1) | KEEP 75 | KEEP 75 | KEEP 70 | Low |
| C-037 | D11 binary packages (L2) | KEEP 85 | KEEP 85 | KEEP 90 | Low |
| C-038 | D12 DIRECTION-SELECTED gate (L3) | DEFER-OWNER 90 | DEFER-OWNER 90 | DEFER-OWNER 90 | Low |
| C-039 | D13 acceptance-tests bookkeeping (L1) | CS 60: mark not built, do not strike | CS 70: same | CS 70: same | Low |

Verdict counts: V1 CUT 2 / CS 13 / DEFER 9 / KEEP 15. V2 CUT 1 / CS 10 / DEFER 5 / KEEP 23. V3 CUT 0 / CS 17 / DEFER 11 / KEEP 11.

## Contradictions (factual or scope conflicts)

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|---|---|---|---|---|
| X-001 | Is `adapter.CODES` movable into the test? (L2) | Yes (R1 scope) | No: the set pins a closed-set check; moving it makes assert at test_adapter.py:719 circular | Yes, moved into test | Medium |
| X-002 | Which no-blink test is redundant, and does R1's test range swallow one? (L3) | R1 range :57-82 swallows :65-71; T9 as proposed deletes the other; delete test_terminal copy, keep test_render | Keep both | R1 range swallows :65-71; if one goes drop test_terminal :65-71 | High (all copies gone if both cuts run as written) |
| X-003 | What in R3 is dead? (L3) | Five row fields (keeps key paths) | Nothing: removing fields raises every row to 5 unrecognised | Only the two aggregate counters; parse.py:91-93 is `_BLOCK_FIELDS` (sanitizer block mode), not counter code | High |
| X-004 | Is test_question_quiet_scope.py:148-171 a test of the fake or of the Collector? (L3) | Test of the fake (cut) | Spy test that duplicates the fake's own assertion (cut) | Runs the real Collector over LiveSource, asserts no consuming token (keep) | Medium |
| X-005 | Are burst and resize pty tests spec-backed? (L3) | Yes: SPEC/ARCHITECTURE-SPINE.md:154 | Yes (burst: stable keyboard; resize: only repaint check) | Cut them; only SIGTSTP/restore tests carry binding rule 1 | Medium |
| X-006 | Which UX folder is current? (L2) | Unverified, probably r2 | ux-orca-observer is current (EXPERIENCE.md:8 updated 2026-11-12) | Same as V2 | Low (resolved by V2/V3) |
| X-007 | Size and count of final-review (D3) (L2) | 660K, 36 files | 660K, 36 files | about 520 KB, about 33 files | Low |
| X-008 | Is write-back-future-stage.md a duplicate of tuibbs-review/write-back-stage.md? (L1) | Treats as duplicate but target untracked | Not byte duplicates (5069 vs 8271 bytes) | Same; 55 refs in 26 files, not about 20 | Medium |
| X-009 | S6 replacement text "Rows are in ledger order" (L1) | False: sorted newest first (view.py:842) | False (same) | False (same) | Medium (source claim false) |
| X-010 | T8 "27 cases could be 12" (L3) | Spec T16 is 27 renders | Same | Same | Medium (source claim false) |
| X-011 | R10 "the `evicted` integer stays" without the list (L3) | Dropping list inflates `evicted` again | Same | Same (reverts 2083db2ae) | Medium (source claim false) |
| X-012 | D1 which owner decisions are stale (L1) | 6 and 8 | 6 and 8 | 6 and 8 (source says 5 and 6) | Low (source claim false) |
| X-013 | D6/R2/D12 provenance: owner decision 2026-11-12 location; "2026-11-10 authorization" (L1) | Not in owner files; R2 rule sits in SPEC/rendering-rules.md:51; D12 authorization in no file | R2 decision in ux EXPERIENCE.md:36 | Same plus .memlog.md:36; D12 same | Low |
| X-014 | Item count (L1) | 39 not 36 | 39 not 36 | 39 not 36 | Low (source claim false) |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | V1 | R1 test ranges too wide (test_questions :46-98 swallows T11/T12; test_fixtures :139-151 is T34 and must be rewritten through `parse_page` + `apply_frozen`) | High |
| U-002 | V1 | R4: the `e` record lacks the inspector fields, so the "clip and export" smaller option is unsound | Medium |
| U-003 | V1 | Zip size on disk (14,438,526) differs from issue-body.md:23 (14,435,766) | Low |
| U-004 | V1/V3 | commands.py:453 `--questions` help and rendering-rules.md:89 are also stale (D2) | Medium |
| U-005 | V2 | R9 refactor needs new tests first: question-path RunnerFailure/OSError/overrun are untested | High |
| U-006 | V2 | D13: T7 as written is unsatisfiable (commands.py:177-178 refuses `--questions` with `--fixture`) | Medium |
| U-007 | V2 | D3 keep list omits owner-decision-pack.md (REPORT.md:40) | Medium |
| U-008 | V2 | D11: attachment-status.json says zip upload did not happen; committed zip is the only delivery path | Medium |
| U-009 | V2 | R2/S1/S4 interaction: do S1 first, then re-judge R2; S2+S1 touch the same test imports | Medium |
| U-010 | V3 | S1: golden has 0 `questions` keys, so no regeneration is needed | Medium |
| U-011 | V3 | S2: `SCHEMA_VERSION` (export.py:23) is used at :195 | Medium |
| U-012 | V3 | T10: test_collector.py:372 runs 8 variants, not 10; T2 range starts at :530 | Low |
| U-013 | V3 | acceptance-tests.md:62 (T56) wording stale: constant is permanently True | Low |
| U-014 | V1/V2/V3 | Owner file `owner-decisions-20261108.md`, `live-test-guide.md`, `tuibbs-review/`, `handoff-mvp-brainstorm.md` and the brainstorm folder are untracked | High |

## Shared Assumptions (AD-2)

All three variants agree on these points: R5-R8 and R10 KEEP, T1 and T10 KEEP, S4 KEEP, D3/D5/D7 need the owner, D10/D11 KEEP, D12 owner-only, D2 sweep limited to QUESTION-OBSERVATION lines, T8 fix only the assertion, and "no deletion of untracked files".

| # | Agreement Source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | R1, S2, T2-T7, D2 (all CUT-SMALLER cuts) | The cuts keep the 694-test baseline and lint clean. No variant ran pytest or ruff; every "test still passes" is read-only reasoning. | UNSTATED as a precondition of the cut (each variant notes it did not run tests) | Yes (L3) |
| A-002 | T4-T7, T9, R1 test edits | A test named by an acceptance-test row (T2, T16, T35, T37, T51, T56 in SPEC/acceptance-tests.md) is not deletable unless its row is edited in the same change. | UNSTATED | Yes (L2) |
| A-003 | D1, D2, D13, S6 | Editing tracked specification documents (not deleting or moving them) needs no owner approval; only binding rules 3 and 4 limit documents. | UNSTATED | Yes (L3) |
| A-004 | S1, S4, S6, R2 | The 2026-11-08 owner rule "versioned, additive-only JSON snapshot" (schema says removal needs schemaVersion 2) covers the exported questions group and the collection counters. | UNSTATED | Yes (L3) |
| A-005 | R1, S2, T1, S4 | The line numbers and "no caller" facts verified on 2026-11-16 still hold at execution time (several reviewers were active in the same worktree). T47 golden was recorded from release-1 source and cannot be regenerated from current code. | UNSTATED | Yes (L3) |

## Summary
- Total structural differences: 3
- Total content differences: 39 (High 5: C-002, C-003, C-013, C-019, C-034; Medium and Low per the per-row column)
- Total contradictions: 14
- Total unique contributions: 14
- Total shared assumptions surfaced: 5 (UNSTATED: 5, STATED: 0, CONTRADICTED: 0)
- Total diff points for convergence: 3 + 39 + 14 + 5 = 61 (A-NNN included per AD-2)
- Highest-severity items: C-002, C-003, C-013, C-019, C-034, X-002, X-003, U-014
- Taxonomy coverage: L1 points C-023, C-026, C-027, C-028, C-034, C-035, C-036, C-039, X-008, X-009, X-012, X-013, X-014; L2 points C-001, C-002, C-004, C-005, C-007, C-011, C-012, C-014, C-017, C-020, C-022, C-025, C-029-C-033, C-037, X-001, X-006, X-007, A-002; L3 points C-003, C-006, C-008, C-009, C-010, C-013, C-015, C-016, C-018, C-019, C-021, C-024, C-038, X-002, X-003, X-004, X-005, X-010, X-011, A-001, A-003, A-004, A-005.
