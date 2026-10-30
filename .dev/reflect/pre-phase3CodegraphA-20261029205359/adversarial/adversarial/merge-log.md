# Merge Log: merged reviewer card (Phase 3 codegraph plan, UC-1, Tier 2)

## Metadata

- Base: Variant 1 (`variant-1-original.md`, reviewer-1 card, sonnet/analyzer), score 0.842
- Incorporated: Variant 2 (`variant-2-original.md`, reviewer-2 card, glm-5.3/qa); both calibration blocks; Round 2.5 invariant amendments (`invariant-probe.md`)
- Plan: `refactor-plan.md` (auto-approved 2026-10-29T21:45:00Z)
- Executor: merge-executor
- Output: `merged-reviewer-card.md` (same folder)
- Changes applied: 9 of 9 (0 skipped, 0 escalated)
- Status: complete
- Timestamp: 2026-10-29T21:50:00Z

Every finding's eight fields (From, Sev, Class, Origin, plan_ref, spec_ref, Claim, Exact fix) were copied from the plan's "Final finding text" table, which the plan marks as authoritative. Escaped `\|` in table cells was converted back to a plain `|` (affects M-01 only).

## Changes

### Change #1: Reclassify base findings per debate consensus

- Status: applied
- Before: R1-01, R1-02, R1-04..R1-12, R1-14, R1-15 carried V1's original class labels and no origin field.
- After: each carries the M-NN class and origin from the plan table (M-01, M-02, M-04..M-07, M-08/M-09, M-10..M-14). R1-03 kept its Regression class (M-03), as the plan does not list it.
- Provenance tag used: `<!-- Source: Base (original, modified) — R1-NN; reclassified ... per Change #1 ... -->`

### Change #2: Correct fixes

- Status: applied
- M-01: fix replaced (`--body "$(cat ...)"` → plain placeholder `--body` plus `gh pr edit --body-file`), per INV-001.
- M-06: fix replaced with a setup step before `/sc:implement` starts, per INV-002, INV-003.
- M-07: fix narrowed to loading the new commands in a fresh session.
- Provenance tags used: `... fix amended per INV-001 (Change #2)` (M-01), `... fix amended per INV-002, INV-003 (Change #2)` (M-06), `... fix narrowed per Change #2` (M-07).

### Change #3: Narrow R1-06 and R1-07

- Status: applied
- M-06 drops the slots-ledger check (plan:40 already checks it); M-07 drops the guide half (source.md:247 fallback). The R1-07 guide half is listed under Dropped card items.
- Provenance tags used: `... narrowed per Change #3 ...` (M-06, M-07).

### Change #4: Fold R2-05 into R1-08 (M-08) and R1-14 into R1-08 part 2 (M-09)

- Status: applied
- M-08 = R1-08 part 1 + R2-05; M-09 = R1-08 part 2 + R1-14. No standalone R1-14 or R2-05 section remains.
- Provenance tags used: `<!-- Source: Base (original, modified) — R1-08 part 1; Variant 2 (reviewer-2 card), R2-05 — merged per Change #4; ... -->` (M-08), `<!-- Source: Base (original, modified) — R1-08 part 2 and R1-14 — merged per Change #4; ... -->` (M-09).

### Change #5: Incorporate R2-01, R2-02 (narrowed), R2-06 and U-016

- Status: applied
- M-15 (R2-01, fix corrected per DES:478), M-16 (R2-02, narrowed), M-18 (R2-06 + U-016) appended.
- Provenance tags used: `<!-- Source: Variant 2 (reviewer-2 card), R2-01 — appended per Change #5; fix corrected per DES:478 -->`, `<!-- Source: Variant 2 (reviewer-2 card), R2-02 — appended per Change #5; narrowed ... -->`, `<!-- Source: Variant 2 (reviewer-2 card), R2-06, plus Variant 2 calibration block (R2 calibrator note), U-016 — appended per Change #5 -->`.

### Change #6: Incorporate calibrator U-012 as M-17

- Status: applied
- M-17 appended, text as rewritten per INV-004 and INV-005.
- Provenance tag used: `<!-- Source: Base calibration block (R1 calibrator note), U-012 — appended per Change #6; rewritten per INV-004, INV-005 -->`

### Change #7: Add M-19 from INV-006

- Status: applied
- Provenance tag used: `<!-- Source: Invariant probe (Round 2.5), INV-006 (fault-finder; both advocates ACCEPT) — appended per Change #7 -->`

### Change #8: Fold the LOW and MEDIUM invariant amendments in

- Status: applied
- INV-007 → M-04, INV-008 and INV-009 → M-08, INV-010 → M-14, INV-011 → M-13, INV-012 → M-03, INV-013 → M-12. The amended text is the plan table text for each row.
- Provenance tags used: `... INV-NNN folded in per Change #8` on M-03, M-04, M-08, M-12, M-13, M-14.

### Change #9: Drop R1-13, R2-03 and R2-04, with reasons

- Status: applied
- The plan's "Changes NOT Being Made" table (7 rows: R1-13, R2-03, R2-04, R2-02 troubleshoot half, R2-02 new-commands half, R1-07 guide half, R1-04 "pipeline text not visible" half) is reproduced verbatim under `## Dropped card items`.
- Provenance tag used: `<!-- Source: refactor-plan.md "Changes NOT Being Made" — applied per Change #9 -->`

## Post-merge validation

Checks were run mechanically against both files (field-by-field comparison of every plan table row with its card section, plus heading and reference scans).

| Check | Result | Details |
|---|---|---|
| Structural integrity | PASS | Heading levels used: `#` (1, the title), `##` (Findings, Dropped card items, Calibration carried forward), `###` (19 finding sections, all under `## Findings`). No level is skipped and no `###` sits outside a `##` parent. Order matches the requested order: provenance header, title and metadata, Findings, Dropped card items, Calibration. |
| Plan fidelity | PASS | 19 plan rows compared with 19 card sections across 8 fields each: 0 mismatches. The Dropped table (header, separator and 7 rows) appears verbatim. |
| Internal references | PASS | `### M-NN` sections counted: 19 (M-01..M-19). Every `M-NN` string in the card (including M-01 cited in M-08 and M-04 cited in M-19) resolves to an existing section; dangling references: none. |
| Contradiction rescan: PR body path | PASS | M-01 and M-02 both name `.dev/codegraph-migration/progress/P3-pr-body.md`. M-08 names `P3-pr-body.md` in its commit list and uses "the body file" from M-01 for `gh pr edit`, so it uses the same file. M-09 does not name the file but stages `.dev/codegraph-migration/progress`, the folder that holds it. No finding names a different body path; the old `./artifacts/pr-body.md` appears only in M-02's claim as the defect. |
| Contradiction rescan: baseline file | PASS | M-04 defines the single test-path set and names no failures file. M-19 names `.dev/codegraph-migration/experiments/P3-baseline-failures.txt` and says the baseline is taken over M-04's single path set. The two agree; no second baseline file or path set appears. |
| Contradiction rescan: other shared plan lines | PASS | plan:218/:221 (M-01, M-02, M-08): M-08's step 2 calls M-01's procedure and its step 6 stages M-02's body file, so the fixes compose. plan:26 (M-02, M-09): M-02 adds the body file to Task 14's commit; M-09 widens the per-task commit rule; no conflict. plan:122 (M-10, M-11, M-16): each targets a different file or step (task.md, sc-task-protocol STRICT step 7 and `allowed-tools`, reflect.md row 40 scope). plan:187/:190 (M-03, M-11, M-19): routing test constant, STRICT step 7, and pytest criterion are separate edits. plan:37 (M-04, M-06, M-17): path set, worktree checks, and G3/G5 routing are separate. plan:67 (M-05, M-13, M-15): installer wording, sentinel scan, degraded-token text are separate. |
| Severity counts | PASS | important = 9 (M-01, M-02, M-03, M-04, M-05, M-06, M-07, M-08, M-19); minor = 10 (M-09..M-18); critical = 0. Matches the metadata line (19 findings). M-07 keeps its "(V2 dissent: minor)" note but counts as important. |
