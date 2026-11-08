# Merge Execution Log

## Metadata
- Base: Variant 3 (reviewer-3-card.yaml, opus:refactorer)
- Executor: merge-executor agent (opus)
- Changes applied: 16 of 16 planned (14 applied as written, 2 applied with a correction: #8 and #11)
- Status: partial. The merge is complete, but convergence is BLOCKED_BY_INVARIANTS (HIGH: INV-001, INV-004, INV-005; MEDIUM warnings: INV-002, INV-003, INV-006, INV-008, INV-010)
- Timestamp: 2026-11-07T20:15:00Z
- Output: `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/pre/adversarial/merged-verdict.yaml`

Path shorthand: TF = the task file `TASK-RF-issue-watcher-20261107-150955.md`, D = `docs/designs/issue-watcher.md`, R06 = `research/06-gap-fill-decisions.md` under the task folder.

## Changes Applied

### Change 1: M-001 remediation after the single commit (blocking, sequencing)
- **Status**: Applied
- **Source**: variant-3 R3-001 (base), variant-1 R1-002 (co-source); INV-001, INV-002, INV-003
- **Target**: findings[0], M-001
- **Before**: R3-001 offered two options (report-only, or a full re-gate); R1-002 proposed G-1/G-5 then HALT.
- **After**: a single fix: Step 10.6 becomes report-only (no `--remediate`). Any Regression or unauthorized Drift HALTs the task and is reported to the owner, with no source edit and no second commit. INV-001, INV-002 and INV-003 are carried as YAML comments. The evidence adds TF:854, TF:851, TF:860 and remediation-handoff.md:32.
- **Provenance tag**: `# provenance: base variant-3 R3-001; co-source variant-1 R1-002; debate X-001 95% VALID-BLOCKING; plan change #1`
- **Validation**: Structural integrity PASS | References PASS (8/8 evidence lines re-Read) | Contradictions PASS

### Change 2: M-002 lint/test exit 0 against recorded-not-fixed (blocking, contradiction)
- **Status**: Applied
- **Source**: variant-3 R3-002 (base); INV-004, INV-005, INV-006, INV-007
- **Target**: findings[1], M-002
- **Before**: R3-002 cited G-4/G-5 (TF:699, 702) and the gate record (TF:735, 745) only.
- **After**: the claim covers lint, format and affected tests. The fix has parts (a) to (e): P1 baseline, one PASS-baseline verdict referenced at every site, prompt carve-outs, a separate lint-architecture row, and a pinned ruff. Each site was re-Read and holds the pattern:
  - G-2: TF:693
  - G-4/G-5: TF:699 and TF:702
  - Gate record and lens: TF:735 and TF:745
  - Per-phase G-4: TF:260, 390 and 517
  - Gate A-D re-runs: TF:306, 321, 433, 448, 560, 575, 657 and 672
  - Final/M4 re-runs: TF:778, 793, 821 and 836
  - Gate C lens: TF:530
  - Makefile:48, Makefile:50 and Makefile:489
  - R06:32
- **Corrections**:
  - The per-phase G-4 site TF:259 (INV-004) is at TF:260.
  - Makefile:500 (INV-006) is in the `eval-skill` target, not `lint-architecture` (lines 362-493). It was dropped; Makefile:489 is kept.
- **Not added**: TF:514 (P7 test run, "investigated for causality") and TF:729/732 (re-runs of Steps 9.4-9.16) hold related text but are outside the plan's site list. They are recorded as a YAML comment only.
- **Provenance tag**: `# provenance: base variant-3 R3-002; debate X-008 95% VALID-BLOCKING; attack A-004 rejected 3/3; plan change #2`
- **Validation**: Structural integrity PASS | References PASS (25/25 kept; 1 corrected, 1 dropped) | Contradictions PASS

### Change 3: M-003 cycle stderr fallback untested (minor, coverage_gap)
- **Status**: Applied
- **Source**: variant-2 R2-002
- **Target**: findings, M-003
- **Before**: v2 markdown deviation labelled MEDIUM / Drift.
- **After**: binary severity minor, category coverage_gap. Evidence is D:887, D:722, TF:460, TF:472 and TF:212. The fix adds an injected-OSError case to Step 6.6 (TF:472). INV-008 is carried as a comment.
- **Provenance tag**: `# provenance: variant-2 R2-002; debate X-006 unanimous VALID-MINOR 95%; plan change #3`
- **Validation**: Structural integrity PASS | References PASS (5/5) | Contradictions PASS

### Change 4: M-004 revalidation cases untested (minor, coverage_gap)
- **Status**: Applied
- **Source**: variant-2 R2-001
- **Target**: findings, M-004
- **Before**: v2 markdown deviation.
- **After**: minor coverage_gap. Evidence is D:879, TF:460 and TF:475. The fix adds the lost-label, voided-approval and changed-Project-status cases to Step 6.7. INV-008 and INV-009 are carried as comments.
- **Provenance tag**: `# provenance: variant-2 R2-001; debate X-007 unanimous VALID-MINOR 95%; plan change #4`
- **Validation**: Structural integrity PASS | References PASS (3/3) | Contradictions PASS

### Change 5: M-005 T-2 attempts < 3 conjunct dropped (minor, coverage_gap)
- **Status**: Applied
- **Source**: variant-1 R1-001
- **Target**: findings, M-005
- **Before**: v1 finding.
- **After**: minor coverage_gap with evidence D:479 and TF:336. The fix restores the conjunct at TF:336. T-2 stays covered in coverage_resolution.
- **Provenance tag**: `# provenance: variant-1 R1-001; debate X-002 unanimous VALID-MINOR 95%; plan change #5`
- **Validation**: Structural integrity PASS | References PASS (2/2) | Contradictions PASS

### Change 6: M-006 withdrawn-commit branch has no audit argument (minor, contradiction)
- **Status**: Applied
- **Source**: variant-1 R1-003; INV-010
- **Target**: findings, M-006
- **Before**: v1 finding.
- **After**: minor contradiction. Evidence is TF:848, TF:860 (twice) and TF:875. The fix gives explicit substitution text for the withdrawn branch and forbids an empty HEAD..HEAD audit. INV-010 is carried as a comment.
- **Provenance tag**: `# provenance: variant-1 R1-003; debate C-001 95% minor; plan change #6`
- **Validation**: Structural integrity PASS | References PASS (4/4) | Contradictions PASS

### Change 7: M-007 xdist citation names a different mechanism (minor, wrong_citation)
- **Status**: Applied
- **Source**: variant-1 R1-004
- **Target**: findings, M-007
- **Before**: v1 finding.
- **After**: minor wrong_citation. Evidence is TF:611 (rationale and command) and .github/workflows/test.yml:29.
- **Provenance tag**: `# provenance: variant-1 R1-004; debate C-002 95% minor; plan change #7`
- **Validation**: Structural integrity PASS | References PASS (3/3) | Contradictions PASS

### Change 8: M-008 G-10 does not see staged pyproject.toml/Makefile changes (minor, gate_weakness)
- **Status**: Applied, with a correction to the plan wording
- **Source**: variant-1 R1-005; INV-014 (ADDRESSED)
- **Target**: findings, M-008
- **Before**: the plan said "add the two paths to G-10 at TF:723".
- **After**: the re-Read shows TF:723 already names `pyproject.toml Makefile`. The defect is the comparison base: `git diff` without `HEAD` misses staged changes, and the gate is re-run in P10 after staging. The fix follows R1-005's own fix, `git diff --exit-code HEAD -- pyproject.toml Makefile .github/`. The correction is recorded as a YAML merge note.
- **Provenance tag**: `# provenance: variant-1 R1-005; debate C-003 95% minor; plan change #8`
- **Validation**: Structural integrity PASS | References PASS (3/3) | Contradictions PASS

### Change 9: M-009 uncapped per-phase re-run loop (minor, gate_weakness)
- **Status**: Applied
- **Source**: variant-3 R3-003; INV-013
- **Target**: findings, M-009
- **Before**: base finding.
- **After**: minor. Evidence is TF:690 and TF:778. The fix caps TF:690 to match the TF:778 HALT rule. A comment records that INV-013 keeps it minor only if M-002 lands.
- **Provenance tag**: `# provenance: base variant-3 R3-003; debate C-004 95% minor; plan change #9`
- **Validation**: Structural integrity PASS | References PASS (2/2) | Contradictions PASS

### Change 10: M-010 stale outputs after fix cycles (minor, sequencing)
- **Status**: Applied
- **Source**: variant-3 R3-004, broadened by INV-012
- **Target**: findings, M-010
- **Before**: the base named final-change-set.md only.
- **After**: final-change-set.md (TF:742), final-gate-record.md (TF:735) and ac-trace.md (TF:729) are regenerated before M4 (TF:800). Evidence: TF:742, 778, 729, 735 and 800.
- **Provenance tag**: `# provenance: base variant-3 R3-004, broadened by INV-012; debate C-005 95% minor; plan change #10`
- **Validation**: Structural integrity PASS | References PASS (5/5) | Contradictions PASS

### Change 11: M-011 record -> predicates import departs from D:239 (minor, contradiction)
- **Status**: Applied, with a citation correction
- **Source**: variant-3 R3-005; INV-011
- **Target**: findings, M-011
- **Before**: the plan targets "the TF:800 M4 exemption lists".
- **After**: TF:800 is the Step 9.M1 design-fidelity prompt ("OUTPUT UNDER REVIEW: the FULL change set listed in") and holds no departure list. The 29-departure text is at TF:797 (the M4 preamble), TF:806 (9.M3), TF:818 and TF:833. The evidence and fix cite TF:797 and TF:806, and the fix names all four sites. Evidence: TF:330, D:239, TF:751, TF:797 and TF:806. The v2 BLOCKING dissent is recorded in debate_outcome.
- **Provenance tag**: `# provenance: base variant-3 R3-005; debate C-006 67% minor, variant-2 dissent BLOCKING (outvoted 2/3); plan change #11`
- **Validation**: Structural integrity PASS | References PASS (5/5; 1 corrected) | Contradictions PASS

### Change 12: M-012 format hit in main.py (minor, contradiction)
- **Status**: Applied
- **Source**: variant-3 R3-007
- **Target**: findings, M-012
- **Before**: base finding.
- **After**: minor. Evidence is TF:502, TF:520 (twice) and TF:517. The fix makes TF:502 and TF:520 agree through the PASS-baseline verdict.
- **Provenance tag**: `# provenance: base variant-3 R3-007; debate C-008 95% minor; plan change #12`
- **Validation**: Structural integrity PASS | References PASS (4/4) | Contradictions PASS

### Change 13: M-013 Done kept after a staging failure (minor, gate_weakness)
- **Status**: Applied
- **Source**: variant-3 R3-008; INV-015 (ADDRESSED)
- **Target**: findings, M-013
- **Before**: base finding.
- **After**: minor. Evidence is TF:875. The fix logs a staging failure as an owner follow-up. The v2 BLOCKING dissent is recorded.
- **Provenance tag**: `# provenance: base variant-3 R3-008; debate C-009 67% minor, variant-2 dissent BLOCKING (outvoted 2/3); plan change #13`
- **Validation**: Structural integrity PASS | References PASS (1/1) | Contradictions PASS

### Change 14: coverage_resolution (UNION of S-002)
- **Status**: Applied
- **Source**: v1 T rows, v2 AC rows, v3 INF register
- **Target**: coverage_resolution
- **After**:
  - covered: T-2 and INF-016.
  - partially_covered: INF-123 and INF-155 (DF-05 declared, R06:28), INF-146, AC-14, AC-6, and INF-138 (aligned with AC-6 per INV-009).
- **Provenance tag**: `# provenance: UNION of S-002 (v1 T rows, v2 AC rows, v3 INF register); plan change #14`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (INF-138 and AC-6 now agree)

### Change 15: dropped_findings
- **Status**: Applied
- **Source**: debate C-007
- **Target**: dropped_findings
- **After**: R3-006 is dropped with the reason "declared deviation DF-46 (R06:180); conceded 3/3 in debate (C-007)". R06:180 was re-Read and holds the DF-46 text. No other finding lost all of its evidence on re-Read, so none was added.
- **Provenance tag**: `# provenance: base variant-3 R3-006; debate C-007 conceded 3/3; plan change #15`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 16: header and unresolved
- **Status**: Applied
- **Target**: top-level keys and top comment
- **After**: `merge_method: adversarial`, `convergence_score: 1.00`, `reviewers: 3`, `unresolved: [INV-001, INV-004, INV-005]`. The top comment records status BLOCKED_BY_INVARIANTS, the HIGH items and the MEDIUM warnings INV-002, INV-003, INV-006, INV-008 and INV-010.
- **Provenance tag**: `# provenance: invariant probe Round 2.5 gate result; plan change #16`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

## Post-Merge Validation

### Structural Integrity
- Schema: PASS. The YAML has every required top-level key (merge_method, convergence_score, reviewers, findings, dropped_findings, coverage_resolution, unresolved). Each finding has id, severity, category, claim, evidence, source_findings, debate_outcome and fix.
- Enums: PASS. Severities are blocking or minor. Categories are coverage_gap, contradiction, wrong_citation, gate_weakness or sequencing.
- Ordering: PASS. The blocking findings (M-001, M-002) come first, then the minor ones (M-003 to M-013).
- Parse check: `yaml.safe_load` returns 13 findings: 2 blocking, 11 minor.

### Internal References
- Evidence entries in the merged verdict: 70. A programmatic check confirmed each one is a substring of its cited line and is at most 25 words: 70 passed, 0 failed.
- Citations re-Read during the merge, including invariant-probe and plan citations that were checked but not carried as evidence: 74.
- Corrected:
  - TF:259 became TF:260 (INV-004, per-phase G-4).
  - "TF:800 M4 exemption list" became TF:797 and TF:806, plus TF:818 and TF:833 in the fix (plan change #11, INV-011).
  - Plan change #8's "add the two paths": TF:723 already names them, so the fix targets the comparison base.
- Dropped: Makefile:500 (INV-006). It sits in the `eval-skill` target, not lint-architecture.
- Findings moved to dropped_findings for lack of evidence: none.

### Contradiction Re-Scan
- New contradictions introduced: 0.
- Checked:
  - The M-001 fix (report-only plus HALT) does not conflict with DF-07 (R06:30), because it adds no commit.
  - The M-009 and M-012 fixes reference the M-002 PASS-baseline verdict and do not define a second one.
  - INF-138 and AC-6 are both partially_covered (INV-009).
  - R3-006 appears only in dropped_findings.

## Summary
- Total changes planned: 16
- Successfully applied: 16. Changes #8 and #11 were applied with the plan's target text corrected after re-Read.
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS (the merged artifact). Convergence stays BLOCKED_BY_INVARIANTS: INV-001, INV-004 and INV-005 are listed under `unresolved`.
