# Merge Execution Log

## Metadata

- Base: Variant B (sonnet:refactorer), `variant-2-sonnet-refactorer.md`
- Plan: `refactor-plan.md` (Changes 1-25; Base Weaknesses and Fixes W1-W23; "INV-034: resolved (Change 25)", which supersedes the BLOCKED entry after it; MEDIUM and LOW open-question items; unresolved diff points kept as OPEN; Changes NOT Being Made)
- Incorporated: Variant A (opus:architect), Variant C (haiku:qa), the round-inv files and the INV-034 focused round, only where a change names them
- Output: `merged-output.md`
- Executor: merge-executor agent
- Changes applied: 25 of 25 planned
- Status: success
- Merge date: 2026-11-04

## Changes Applied

### Change 1: Restate the recommendation as the tier split

- **Status**: Applied
- **Source**: Round 2 consensus (R2-A A-prime as amended by R2-B M1-M6)
- **Target**: Base 1.1 and 1.3 (restructured); consistency edits in 3.2 R3, 5.1, 6.2, 11
- **Before**: One late hook (Wave 8a) for every tier; "no change to any push, gate or transition code"; sync and fix cycles only.
- **After**: Tier 0 report; Tier 1 at Wave 8a (no round, no re-trigger, P1); Tier 2 at `C-initial` through `(S2_CLASSIFY, "conflicting")` (re-trigger, one round, P2, dark); Tier 3 Wave 0 halt. The "no change" promise is withdrawn. A merge cycle (Tier 2) is defined beside fix and sync cycles. R3 narrowed to admit the one P2 edge; the out-of-scope re-trigger bullet narrowed to Tier 1.
- **Provenance tag**: `<!-- Source: Base (original, modified): restated as the tier split per Change #1; ... -->` (1.1, 1.3)
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 2: Mechanism inventory

- **Status**: Applied
- **Source**: Variant A, Section 3.1 (two refs, U-003); R2-B C-B4 (scripts)
- **Target**: Base 3.1, 3.3 (rows replaced); 1.1, 5.2, 13.2
- **Before**: One ref `refs/conflict-sync.md`; three scripts; no FSM edge in the inventory.
- **After**: `refs/conflict-mechanical.md` (Tier 1 and up) and `refs/conflict-intent.md` (Tier 2 only); P1 scripts `probe-merge.sh` (thin) and `finish-merge.sh`; `collect-conflict-evidence.sh` deferred to P2 or inline; new row A12 for the P2 edge; 3.3 counts updated (refs +2, scripts +2 in P1, FSM edges +1 in P2).
- **Provenance tag**: `<!-- Source: Base (original, modified): rows ... replaced per Changes #2, ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 3: `MechanicalRule` replaces `REGEN_RECIPES`

- **Status**: Applied
- **Source**: Variant A, Section 7.1 (A:391-407)
- **Target**: Base 4.2 rule 7 and notes, 3.1 A1, new 3.4, 6.5, FR-2, FR-9
- **Before**: `REGEN_RECIPES = {"uv.lock": "uv-lock"}` keyed by basename.
- **After**: `MechanicalRule(pattern, kind, sources, regenerate, check)` with one root-anchored `uv.lock` row (stage set `123`), applicable only when tracked and `uv` is on PATH; allowed-tools test generalised to every inline command and rule program (A-004). INV-025 closed.
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), Section 7 ... MechanicalRule per Change #3 (A:391-407) ... -->` (3.4); Base (original, modified) tags on 4.2 and 6.5
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 4: Explicit `BLOCKED` Tier 0 row

- **Status**: Applied
- **Source**: Variant C, C:55 (U-023)
- **Target**: Base 4.2 tier table (row inserted)
- **Before**: No `BLOCKED` row.
- **After**: `mergeStateStatus == BLOCKED` with `mergeable == MERGEABLE` is Tier 0 with its own parametrized row (FR-2 AC).
- **Provenance tag**: `<!-- Source: Base (original, modified): ... BLOCKED row per Change #4 (Variant C, C:55) ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 5: New Core API section with a single router

- **Status**: Applied
- **Source**: Variant A, Section 7 (A:363-451), `conflict_action` (A:419), FR-C6 (A:473)
- **Target**: New base 3.4 "Core API (`superclaude.pr_submit.conflicts`)", inserted after 3.3; FR-26
- **Before**: Section did not exist; routing spread over 5.4, 5.5 and 6.3.
- **After**: Data block and function table: `parse_stage_records`, `mergeability_hint`, `classify_conflicts`, `conflict_action` (tier x ordinal x hook x entering outcome x budget x cap, fail-closed default row, QA-4), `merge_parent_ok`, `merge_preflight_ok`, `evaluate_sync_decision`, `sync_fail_state`, `crash_resume_plan`, `is_conflict_cycle`, `resolution_record_ok`; related `ci.classify_checks` keyword.
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), Section 7 (A:363-451) and FR-C6 (A:473): merged per Change #5; ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 6: Placement and ordinal table

- **Status**: Applied
- **Source**: Variant A, Section 5.1 (`C-initial`); R2-B M2, M3, M4; inv-A/B/C INV-003
- **Target**: Base 5.1, 5.2, 5.4, 5.5 (restructured); 5.3 detection order; FR-6, FR-27
- **Before**: Detect at Wave 0 (probe always), act only at Wave 8a; report-only after `HALT_MAX_ROUNDS` / `TERMINAL_AUGMENT_NO_RESPONSE` (OQ-4); OQ-11 open.
- **After**: Unconditional Wave 0 local operation check (INV-004; reason code OPEN, default `foreign_op_in_progress`); GitHub read first with 3 re-reads 10 s apart on `UNKNOWN`; probe only on `CONFLICTING` or persistent `UNKNOWN`; Tier 3 at L3 halts at Wave 0 (`conflict_tier3`); M4 table with one acting site per tier per ordinal; Tier 1 acts on all four armed outcomes; L2 sets S4' only from `clean` / `REPORT_ONLY`, otherwise reports and keeps the preserved terminal. OQ-4 and OQ-11 closed.
- **Provenance tag**: `<!-- Source: Base (original, modified): replaced by the one-acting-site-per-tier table per Change #6 (R2-B M4); ... -->` and siblings on 5.1, 5.2, 5.5
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 7: Thin probe, stage parsing in the core

- **Status**: Applied
- **Source**: Variant A, AD-6 (A:51) and the captured fixture (A:557)
- **Target**: Base 5.3 (output schema replaced); base Appendix B folded into 5.3 (exit contract table) and 6.4 step 9
- **Before**: Probe emitted a parsed `conflicts` array; Appendix B nested under "13. Index".
- **After**: Probe emits the raw `-z` listing (`stage_records`) unparsed; `parse_stage_records` parses it, tested against `fixtures/merge_tree_conflict.z`; exit contract table now in 5.3.
- **Provenance tag**: `<!-- Source: Base (original, modified): thin probe with raw -z listing per Change #7 (Variant A, AD-6); ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 8: Rounds, caps and re-trigger per tier

- **Status**: Applied
- **Source**: Variant A, Sections 5.4-5.5 (A:222-247); R2-B M5; R2-C QA-3
- **Target**: Base 5.6 (restructured) and the section 8 test plan; FR-28
- **Before**: One sync behaviour: no round, no re-trigger, `SYNC_CAP = 2`.
- **After**: Tier 1 `kind: "sync"`: no round, no re-trigger, no reply or resolve, `SYNC_CAP = 1`. Tier 2 `kind: "merge"`: ticks `round_counter` on the INV-001 edge (P2). S5a trigger widened in `fsm.py:1137` and `SKILL.md:274` to `applied_edits > 0 or kind == "merge"` between the pins at `test_static_grep.py:689` and `:750`; new static pin plus the zero-edit-pair test; configured-reviewer substitution at `C-initial` pinned (INV-030, in part).
- **Provenance tag**: `<!-- Source: Base (original, modified): rounds, caps and re-trigger per tier per Change #8 (Variant A, Sections 5.4-5.5; R2-B M5; R2-C QA-3); ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 9: One sibling gate for both tiers

- **Status**: Applied
- **Source**: R2-B M5 (extends base 6.3)
- **Target**: Base 6.3; FR-13
- **Before**: `evaluate_sync_decision` for sync only, cap `prior_sync_cycles < SYNC_CAP`.
- **After**: Covers both tiers; predicates ordinal >= 3, validated, tier allowed and no halt, under cap; for Tier 2 "under cap" also requires `round_counter < max_rounds`; no `applied_edits` predicate; cross-gate property test against `evaluate_push_decision`.
- **Provenance tag**: `<!-- Source: Base (original, modified): one sibling gate for both tiers per Change #9 (R2-B M5); ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 10: Push records and kind-aware recovery

- **Status**: Applied
- **Source**: inv-A/B/C INV-001; Variant C, C:83 (C-030); Variant A, A:594 (additive kwargs); R1-B concession 4
- **Target**: Base 5.7, 5.8, 3.1 A9; 6.4 step 11; FR-14, FR-17
- **Before**: `build_sync_triad`; `kind: "sync"` on sync records only; Branch A of a sync returned `S2_CLASSIFY` (B:299).
- **After**: `build_sync_triad` dropped; `build_push_triad` gains `push_kind` and `base_sha`; `kind` in `{fix, merge, sync, ci}` on all three records (default `fix`); `push_initiated` for `sync`/`ci` records the preserved terminal; recovery key tuple gains `kind`; pure `crash_resume_plan` (inv-A name) returns the Wave 8 CI-wait directive for `sync`/`ci` Branch A and B, never S4/S5a/S5, `resume_unrepresentable` on a missing terminal; `fix`/`merge`/absent byte-equal; B:299 withdrawn explicitly.
- **Provenance tag**: `<!-- Source: Base (original, modified): dangling-push row replaced by the kind-aware resume rule per Change #10 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 11: VAL rules

- **Status**: Applied
- **Source**: R2-C R-C7; A-003
- **Target**: Base 6.7
- **Before**: Tier 1 added `uv lock --check` to VG-1; VG-2 forced for `pr_submit/` or `pyproject.toml`.
- **After**: Tier 1 VAL = `uv lock --check` + VG-3 + VG-4; no-tests cap at Tier 1 with the report line; VG-2 at Tier 2 kept from base and marked OPEN (X-019/C-028); INV-014 baseline recorded as an open question.
- **Provenance tag**: `<!-- Source: Base (original, modified): Tier 1 VAL and the no-tests cap per Change #11 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 12: Clean-tracked-tree preflight

- **Status**: Applied
- **Source**: Variant A, A:288; inv-A/B/C INV-008
- **Target**: Base 5.3 (`index_clean` -> `tree_clean`), 6.4 steps 2, 5, 9, A5 (`finish-merge.sh`), FR-7, FR-11, 8.1
- **Before**: `index_clean` (`git diff --cached --quiet`); unstaged operator edits tolerated; halt `sync_dirty_index`.
- **After**: Act only when `git status --porcelain=v1 --untracked-files=no -z` is empty; untracked tolerated; dirty -> HALT `merge_preflight_dirty` naming the files (shape of `fix_commit_failed`); clean tree re-asserted right before the regenerate; after the commit both `status --untracked-files=no` empty and `git diff --quiet HEAD`; real-git dirty `pyproject.toml` test.
- **Provenance tag**: `<!-- Source: Base (original, modified): tree-clean preflight and post-commit assertions per Change #12 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 13: Create path

- **Status**: Applied
- **Source**: Variant A, AD-7 (A:53); R2-A R-4/R-5
- **Target**: Base Appendix A (retired), 11 bullet 4, OQ-7 (closed); 1.2 AD-7, 8.2, 8.4, 9 (precursor row), FR-31
- **Before**: Clarify-only wording (Appendix A); both HALT fragments in the byte-identical list.
- **After**: Separate precursor change: at L1+ the create path neither rebases nor halts when behind base (Tier 0 report); L0 keeps the rebase byte for byte (`test_static_grep.py:649-657` unchanged); only the L1+ HALT pins at `:658` and `:660` rewritten (verified against the test file: `:658` and `:660` are the two HALT fragments). Those two fragments moved out of the 8.4 list.
- **Provenance tag**: `<!-- Source: Base (original, modified): fragments 3 and 4 moved out ... (Change #13) -->`, plus tags on 1.2, 11, 12, 13.2
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 14: `pr_conflicting` CI-wait skip

- **Status**: Applied
- **Source**: Variant A, A:220, FR-C23 (U-004)
- **Target**: Base 5.5 (inserted); FR-29
- **Before**: Section did not exist.
- **After**: Wave 8 entered on a still-conflicting PR with no merge pushed (L1, L2, tier above cap, preflight halt) skips the CI wait with reason `pr_conflicting` (INV-024).
- **Provenance tag**: `<!-- Source: Base (original, modified): ... CI-wait skip inserted per Change #14 (Variant A, A:220, FR-C23) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 15: Flag rename

- **Status**: Applied
- **Source**: Variant A, A:76 (name); Variant B, B:97 (default)
- **Target**: Base 1.1, 7.1 FRs, 9; every other occurrence for consistency (3.1 A10, 4.2, 5.7 payload, 6.3, 8.2, OQ-1)
- **Before**: `--sync-tier {0,1,2}`, field `sync_tier_cap`.
- **After**: `--conflict-max-tier {0,1,2}`, default 1; payload field `conflict_max_tier`. No `--sync-tier` remains.
- **Provenance tag**: carried in the 1.1, 3.1, 6.3 and 9 tags
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 16: Output contract and counting

- **Status**: Applied
- **Source**: R2-B M6; R2-C QA-1, QA-2; inv-A INV-018
- **Target**: Base 7.1 FR-19, 5.6; FR-16; 8.2
- **Before**: Sync pushes into `sync_push_count`; prose bounds at `SKILL.md:239` and `:275` unreconciled.
- **After**: `push_count` excludes kind `sync` only; `sync_push_count` <= `SYNC_CAP`; `push_kind` on records; kind-aware fold at `run_log.py:238-239`; reconcile `SKILL.md:239` with `:275`; behavioural `rebuild_state` test with a conflict push (QA-1) and a report-contract test (QA-2).
- **Provenance tag**: `<!-- Source: Base (original, modified): ... counting per Change #16 (R2-B M6, R2-C QA-1/QA-2, INV-018) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 17: Wait-only sentences carve-out

- **Status**: Applied
- **Source**: inv-A/B/C INV-009
- **Target**: Base 6.9 (inserted) and 8.2/8.3 edit lists; FR-20, FR-33; OQ-20
- **Before**: Section did not exist.
- **After**: Rewrite `refs/state-machine.md:144-146`, `refs/ci-poll.md:28-29`, `SKILL.md:277` so "never an additional push" covers model-authored fixes, with the single Tier 1 sync push as the only exception; new `test_static_grep.py` pin; exact wording OPEN, meaning agreed.
- **Provenance tag**: `<!-- Source: Base (original, modified): wait-only carve-out inserted per Change #17 (inv-A, inv-B, inv-C INV-009) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 18: Rejected-push handling

- **Status**: Applied
- **Source**: A-001; inv-A and inv-B INV-035
- **Target**: Base 6.4 steps 10 and 12, 5.8; FR-30
- **Before**: No handling of a rejected live push; merge-method fields not read.
- **After**: Advisory read of `mergeCommitAllowed`, `rebaseMergeAllowed`, `squashMergeAllowed` before the first merge push (never a halt); post-push `BLOCKED` reported; a rejected push appends `push_aborted_or_not_landed{rejected: true, stderr_tail}` and halts `push_rejected`; Branch B never re-drives a `rejected` record. The P1-gate requirement for a real PR reading `MERGEABLE` is covered by gate (b) of 8.5.
- **Provenance tag**: `<!-- Source: Base (original, modified): ... rejected-push handling and merge-method advisory per Change #18 (A-001, INV-035) ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 19: Risk register format and rows

- **Status**: Applied
- **Source**: Variant C, Section 10 (S-014); R2-C QA-10
- **Target**: Base 10 (columns restructured; rows appended)
- **Before**: K1-K13 with one "Likelihood / impact" column.
- **After**: Separate Likelihood and Impact columns; K14 = C's R14 ("Certain, partially"); K15 = QA-10 S5a re-narrowing; K16-K25 = INV-005, 010, 011, 012, 013, 014, 022, 027, 030, 031. K2, K8, K9 aligned with Changes 1 and 6; K1 reworded per W20.
- **Provenance tag**: `<!-- Source: Base (original, modified): Likelihood and Impact split into two columns per Change #19 (Variant C, Section 10; R2-C QA-10); ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 20: Definitions section

- **Status**: Applied
- **Source**: Variant C, Section 2 (C:16-24; U-020)
- **Target**: New base 1.4 "Definitions"
- **Before**: Section did not exist; VAL and FSM never expanded.
- **After**: FSM, VAL, conflict state, unmerged path, tier, sync cycle, merge cycle, fix cycle, hook points, resolution record, marker line, HALT; adapted to the split (Clarity-4 fixed).
- **Provenance tag**: `<!-- Source: Variant C (haiku:qa), Section 2: merged per Change #20, adapted to the tier split; ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 21: Cycle-id prefixes

- **Status**: Applied
- **Source**: A-005; QA-8
- **Target**: Base 5.7 and 7.1 FR-15; 3.4
- **Before**: Only `sync-` mentioned, not reserved.
- **After**: `sync-` and `conflict-` reserved; pure `is_conflict_cycle`; one test that the fix-cycle id rule can produce neither prefix.
- **Provenance tag**: `<!-- Source: Base (original, modified): ... cycle-id prefixes per Change #21 (A-005, QA-8); ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 22: Test plan additions and removals

- **Status**: Applied
- **Source**: Variant A, A:557; R2-C QA-1 to QA-10; Variant C, Section 9.3 (U-021); C:161 (U-024); R1-B concession 6
- **Target**: Base 8.1-8.6; new 8.7; NFR-9, NFR-14
- **Before**: No parser fixture, no router table test, `SKILL.md <= 346` assertion.
- **After**: Captured-fixture parser test; `conflict_action` table test; QA-1 to QA-10; new 8.7 "deliberately no automated test" limited to the live push, the live re-trigger POST and real-GitHub reads; `== 41` sweep and `models.py:23` docstring; per-tier call ceilings as NFR-14; line-count assertion removed; byte-identical fragment test kept.
- **Provenance tag**: `<!-- Source: Variant C (haiku:qa), Section 9.3 (U-021): merged per Change #22, ... -->` (8.7) and Base (original, modified) tags on 8.1, 8.2, 7.2
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 23: P1 gate rewrite and the no-op statement

- **Status**: Applied
- **Source**: inv-A/B/C INV-033
- **Target**: Base 9 P1 row and 8.5 (gate text replaced); 1.3 note
- **Before**: P1 gate "a real `uv.lock` conflict end to end at L3"; manual run "on a scratch fork".
- **After**: Note that P1's Tier 1 rule is a no-op here (`uv.lock` gitignored, `.gitignore:169`, `:222`) and what P1 still pays for; gate (a) mandatory hermetic real-git test in a pytest temporary directory with `gh` mocked; gate (b) one manual live L3 run on a separate repository under `IronbellyOrg`, never upstream (also exercises INV-034); `uv.lock` not un-ignored.
- **Provenance tag**: `<!-- Source: Base (original, modified): P1 gate text replaced per Change #23 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 24: Structural clean-up of the base

- **Status**: Applied
- **Source**: Variant A, Section 2 decision-record form (S-005); S-013
- **Target**: Base 1.2 and 13
- **Before**: Debt table plus reject list in 1.2; Appendix A and B nested under "13. Index".
- **After**: 1.2 is a decision record AD-1 to AD-7, each with choice and rejected alternatives; Appendix B folded into 5.3 and 6.4 (Change 7); Appendix A retired (Change 13); no appendix under 13.
- **Provenance tag**: `<!-- Source: Base (original, modified): debt table and reject list restated as AD-style decision entries per Change #24; ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 25: INV-034 `expect_checks` (supersedes the BLOCKED entry)

- **Status**: Applied
- **Source**: INV-034 focused round: R-034' text (Variant A advocate), the timeout correction (Variant B advocate), the tests (Variant C advocate)
- **Target**: New base 6.10 (the "CI wait" section), 3.4 (related change), 3.1 A13, 6.4 step 13, FR-18, FR-32, 8.1, 8.2
- **Before**: Section did not exist; the plan's BLOCKED options A/B/C.
- **After**: `classify_checks(payload, *, wait_sha=None, expect_checks=False)`; set once per push, recorded for `--resume`; true on (a) earlier checks, (b) `pre_push_sha` checks, (c) `base_sha` checks, via `poll-ci-checks.sh --evidence-sha` (`-1` fails closed); an empty list is `clean` only when all three read zero; expiry is the Wave 8 `timed_out` result with reason `ci_not_started`; `refs/ci-poll.md:21` and `SKILL.md:277` amended; the listed tests. The superseded BLOCKED entry and its options were not merged.
- **Provenance tag**: `<!-- Source: INV-034 focused round (round-inv034-advocate-A/B/C.md): merged per Change #25; ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Other plan items

| Item | Status | Where |
|---|---|---|
| W1-W19, W21-W23 | Applied through the changes the table names | as listed per change |
| W20 (reword "evidence-validator confirms" to "grounding checked" in 1.3, 6.4 and K1) | Applied | 1.3, 6.4 step 6, K1 (also A7 and FR-23) |
| MEDIUM items INV-005, 010, 011, 012, 013, 014, 022, 027, 030 (part), 031 | Applied as risk rows K16-K25 and open questions OQ-21 to OQ-30 | 10, 12 |
| LOW items INV-016, 019, 020, 021, 025, 032 | Applied as one-line notes; INV-025 marked handled | 12 |
| INV-010 three-way split | Applied as OQ-21 with all three options, plus K17 | 12, 10 |
| Unresolved diff points C-028/X-019, C-029/X-011, X-009 | Base text kept, marked OPEN | 6.7, 5.7, 6.4 step 10, OQ-16 to OQ-18 |
| C-027/X-021 (from Changes NOT Being Made) | Not applied; base 6.8 kept with OPEN marker | 6.8, OQ-19 |
| INV-008 (A extra), INV-035 (A extra) | Recorded as open hardening questions | OQ-31, OQ-32 |
| S-001..S-004, S-007 | No action, per plan | n/a |
| Changes NOT Being Made (all other rows) | Not applied, per plan | n/a |
| INV-034 BLOCKED entry | Not applied; superseded by Change 25 | n/a |

### Executor notes (literal renderings flagged for review)

1. Change 12 says `finish-merge.sh` re-asserts the clean tree "right before the regenerate", while the script runs at step 9, after the regenerate (step 5). Rendered literally in 3.1 A5 and 6.4 step 5 ("`finish-merge.sh` performs this re-check"); how the script is invoked twice is left to the implementer.
2. To give Change 12's post-commit assertions a failure token, `FINISH_FAIL tree_dirty` was added to the exit contract, mapped to the existing reason `merge_preflight_dirty`.
3. The thin probe (Change 7) still emits `binary_paths` as raw data, because 4.2 rule 6 needs a binary fact and the plan does not move it elsewhere; the raw listing travels in a `stage_records` JSON field to keep the one-JSON-line contract.
4. FR-26 to FR-33 restate Changes 5, 6, 8, 13, 14, 17, 18 and 25 as requirement rows so the FR list covers every adopted behaviour; they add no behaviour beyond the plan.
5. Phase placement of items the plan does not phase (Wave 0 operation check, wait-only carve-out, rejected-push handling, cycle prefixes) is P1, beside the P1 behaviour each one guards; the `pr_conflicting` skip is P1 per Change 23's note.
6. Risk rows K15-K25 use "Not rated" for likelihood where no source rates it; impact follows the probe severity (MEDIUM) or the plan's Risk Summary (Change 8: High).
7. The `conflict_action` action vocabulary uses Variant A's names (`none`, `report`, `propose`, `resolve_local`, `resolve_push`) plus `halt` with reasons, since the plan names the router but not its outputs.
8. OQ-14 lost the clause "only used on the create path", which no longer holds once the L1+ create path reports behind-base.

## Post-Merge Validation

### Structural Integrity

- Heading hierarchy: PASS. One H1, 13 numbered H2 sections, H3 subsections only under their H2; no level gaps (checked mechanically over all 56 headings); no orphaned subsections; the document starts with H1 after the front matter and provenance header.
- Section ordering: PASS. Base order kept; new sections inserted where the plan targets them (1.4 after 1.3, 3.4 after 3.3, 6.10 after 6.9, 8.7 after 8.6); Appendix A and B removed from under 13.
- Document flow: PASS. Definitions precede first use of tier, cycle and hook names; the Core API (3.4) precedes the sections that call it; no placeholder markers remain (0); no em or en dashes (0).

### Internal References

- Total references: 185 distinct targets (373 occurrences, including definition sites): section numbers (31), FR (33), NFR (14), OQ (32), AD (7), K (25), G (19), adopt rows A1-A13 (13), reject rows R1/R4/R5/R12 (4), 6.4 step numbers (7).
- Resolved: 185
- Broken: 0. References to `state-machine.md` sections 5.1, 5.2c and 5.2d point to an external file and were not counted as internal.

### Contradiction Re-Scan

- New contradictions introduced: 0
- Checked: stale terms (`--sync-tier`, `index_clean`, `build_sync_triad`, `REGEN_RECIPES`, `conflict-sync.md`, `SYNC_CAP = 2`, `sync_tier_cap`, `sync_dirty_index`, Appendix references) appear only in decision-record rejections or provenance comments; Branch A "returns `S2_CLASSIFY`" appears only as a withdrawn rule; "no change to push/gate/transition code" removed; the wait-only rule and the Tier 1 exception reconciled in 6.9; GitHub-first detection and "local is truth for action" reconciled in 5.3 and K2; the counting contract (`push_count` with Tier 2 counted, `sync_push_count` for Tier 1) consistent across 1.1, 5.6, FR-16, FR-19.
- Pre-existing wording residue (not new, not targeted by the plan): 4.3 Tier 2 criterion (g) still says "`evidence-validator` confirms every entry", while W20 rewords the same claim to "grounding checked" in 1.3, 6.4 and K1. Flagged for review.

## Summary

- Total changes planned: 25
- Successfully applied: 25
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS (structural integrity PASS, internal references PASS, contradiction re-scan PASS with one pre-existing wording residue flagged)
