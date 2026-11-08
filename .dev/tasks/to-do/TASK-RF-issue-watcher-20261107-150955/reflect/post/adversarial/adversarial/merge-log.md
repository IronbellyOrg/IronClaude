# Merge Execution Log

## Metadata
- Base: Variant 2 (haiku:qa), `variant-2-original.md`, selected in `base-selection.md`
- Executor: merge-executor agent
- Plan: `refactor-plan.md` (this directory)
- Merged artifact: `../merged-verdict.yaml` (one directory above this log)
- Changes applied: 19 of 19 register rows, plus 17 of 17 advisory rows, 6 of 6 Grounding Gaps, 9 of 9 rejected claims and 1 of 1 explicit ruling (late launch)
- Status: success
- Timestamp: 2026-11-08T06:01:59Z (merge started 2026-11-08T05:53:31Z, the time in the YAML header)
- Debate agreement: 56 / 67 = 0.836 (`scoring-matrix.md`, converged)
- Evidence rule: every file:line in the merged artifact was re-read with the Read tool in the live worktree by this executor; two plan citations were wrong and are corrected (see Corrected Citations); none is marked UNVERIFIED, because every cited line was found.

## Changes Applied
### Change 1: Header and verdict scalars
- **Status**: Applied
- **Source**: Plan Overview and Final Verdict (`refactor-plan.md:3-10`, `:120-126`); `invariant-probe.md:22-31`; `scoring-matrix.md` (agreement 0.836)
- **Target**: `merged-verdict.yaml` top-level keys `merge_method` to `judge_class_collision`
- **Before**: Variant 2 had a free-text verdict with no machine keys.
- **After**: `merge_method: adversarial`, `convergence_score: 0.836`, `reviewers: 3`, `base_variant: 'variant-2 (haiku:qa)'`, `verdict: FAIL`, `blocking_findings: [R-1]`, `invariant_probe {total 12, high_unaddressed 0, medium_unaddressed 1, blocked false}`, `judge_class_collision: true`.
- **Provenance tag**: `# provenance: base variant 2 ...`, `# provenance: incorporated variants 1 ... and 3 ...`, `# provenance: plan adversarial/refactor-plan.md ...`, `# provenance: debate agreement 56/67 = 0.836 ...`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 2: Blocking Regression R-1 (late launch)
- **Status**: Applied
- **Source**: Variant 2 row 1 (class and blocking flag); Variants 1 and 3 debate positions (LOW severity); plan row R-1 (`refactor-plan.md:20`)
- **Target**: `findings[0]` (R-1)
- **Before**: Variant 2 graded it Regression HIGH at `cycle.py:1048`.
- **After**: Regression LOW, blocking true, location `cycle.py:1060-1062` and `cycle.py:1048`, quoted criterion design :647 and AC-19 (design :892), remediation and verifier as in the plan. Evidence re-read: `cycle.py:1048-1049`, `:1060`, `:1061`, `:1062`, `:410-412`; design :647, :892; task :901.
- **Provenance tag**: `# provenance: base variant-2 row 1 ...; severity from variant-1 and variant-3 debate positions (LOW); plan row R-1`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 3: Non-blocking Regressions R-2 to R-7
- **Status**: Applied
- **Source**: Variant 1 rows 1, 2, 9, 12 and gap 12; Variant 2 rows 2 and 5; Variant 3 rows 1, 2, 7 and gap 4; plan rows R-2 to R-7 (`refactor-plan.md:21-26`)
- **Target**: `findings[1]` to `findings[6]`
- **Before**: Variant 2 had no rows for R-2, R-3, R-6, R-7; it had R-5 as Drift MEDIUM labelled Blocking and the R-4 imports as Authorized.
- **After**: Six Regression rows, each with its quoted criterion, blocking false; R-5 MEDIUM, R-7 "LOW (effectively unreachable)", the rest LOW. R-4 adds `record.py:183` as the use site of `valid_operation_id`; C-038 folded into R-4 as the plan states.
- **Provenance tag**: one `# provenance:` comment above each row, naming the variant rows and plan row
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 4: Drift rows D-1 to D-4
- **Status**: Applied
- **Source**: Variant 1 rows 4, 5, 6; Variant 3 rows 3, 4, 5, 6; plan rows D-1 to D-4 (`refactor-plan.md:27-30`)
- **Target**: `findings[7]` to `findings[10]`
- **Before**: Section did not exist in Variant 2.
- **After**: Four Drift rows, LOW, blocking false, each with the plan rationale and remediation. D-3 carries the cycle copy of C-009; D-4 carries the `stderr_fallback` part of C-012.
- **Provenance tag**: one `# provenance:` comment above each row
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 5: Necessary rows N-1 to N-3
- **Status**: Applied
- **Source**: Variant 1 rows 5 and 7; Variant 2 row 3; Variant 3 rows 8 and 10; plan rows N-1 to N-3 (`refactor-plan.md:31-33`)
- **Target**: `findings[11]` to `findings[13]`
- **Before**: Variant 2 had only C-030 (now N-2).
- **After**: Three Necessary rows, LOW, blocking false. N-1 location uses `audit.py:110-115` for `_fsync_dir` (corrected, see Corrected Citations) and adds `audit.py:200` for the audit copy of C-009 that the row names.
- **Provenance tag**: one `# provenance:` comment above each row
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 6: Authorized rows A-1 to A-5
- **Status**: Applied
- **Source**: Variant 1 rows 6, 8, 10; Variant 2 rows 4 and 5; Variant 3 rows 2, 9, 11; plan rows A-1 to A-5 (`refactor-plan.md:34-38`)
- **Target**: `findings[14]` to `findings[18]`
- **Before**: Variant 2 had C-031 (now A-4) and the record imports (now split into A-1 and R-4).
- **After**: Five Authorized rows, severity n/a, blocking false. A-5 cites DF register :156 for DF-29 (corrected, see Corrected Citations); the Variant 3 path `src/superclaude/main.py` is recorded as corrected to `src/superclaude/cli/main.py`.
- **Provenance tag**: one `# provenance:` comment above each row
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 7: Advisory gaps
- **Status**: Applied
- **Source**: Plan section Advisory Gaps (`refactor-plan.md:69-91`), drawn from Variants 1 and 3 and the invariant probe
- **Target**: `advisory_gaps` (17 rows)
- **Before**: Section did not exist in Variant 2.
- **After**: 17 rows with id, location, judge severity and the plan's verified flag (13 true, 4 false: C-019, C-024, INV-007, INV-009). None gates.
- **Provenance tag**: `# provenance: plan section Advisory gaps (17 rows); advisory rows never gate`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 8: Grounding Gaps
- **Status**: Applied
- **Source**: Plan Grounding Gaps line (`refactor-plan.md:93`); missing-evidence text from the not-agreed rows of `scoring-matrix.md` (lines 78-91)
- **Target**: `grounding_gaps` (6 entries: C-020, C-021, C-027, C-028, C-029, C-039) and a plan-note comment
- **Before**: Section did not exist in Variant 2.
- **After**: Six entries with id, topic, source, missing_evidence, lines_seen_by_executor and next_evidence_needed. The plan's note that X-009 / C-015 is not a defect (`cycle.py:693-694`, `:1033-1034`, both re-read) and that C-038 is folded into R-4 is kept as a YAML comment. None gates.
- **Provenance tag**: `# provenance: plan Grounding Gaps line; missing evidence from scoring-matrix.md not-agreed rows; grounding gaps never gate`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 9: Rejected claims
- **Status**: Applied
- **Source**: Plan section Changes NOT Being Made (`refactor-plan.md:95-107`)
- **Target**: `rejected_claims` (9 rows)
- **Before**: Section did not exist in Variant 2.
- **After**: Nine rows with proposer, change and the plan's rationale text. The `_fsync_dir` row cites `audit.py:110-115` (corrected from the plan's `audit.py:204-206`).
- **Provenance tag**: `# provenance: plan section Changes NOT being made (9 rows)`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 10: Late-launch ruling
- **Status**: Applied
- **Source**: Plan section Late-launch ruling (`refactor-plan.md:42-50`); Variant 2 row 1; `invariant-probe.md` INV-003 to INV-006
- **Target**: `late_launch_ruling`
- **Before**: Variant 2 named the defect without a fix order or restore rule.
- **After**: defect, severity LOW, blocking true, the three-step required fix (capture `prev` before `cycle.py:1060`; re-check after the save at `:1061` and restore, save, skip; FR-010 kept), and invariants INV-003 to INV-006. `record.py:206-207`, `:208-209` and `:638-639` re-read.
- **Provenance tag**: `# provenance: plan section Late-launch ruling (base variant-2 row 1, invariant-probe INV-003 to INV-006)`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: PASS. The artifact is YAML, not Markdown; `yaml.safe_load` (run with `uv run python`) parses it and returns the 13 top-level keys in the required order: merge_method, convergence_score, reviewers, base_variant, verdict, blocking_findings, invariant_probe, judge_class_collision, findings, advisory_gaps, grounding_gaps, rejected_claims, late_launch_ruling.
- Section ordering: PASS. `findings` holds 19 entries in register order R-1 to R-7, D-1 to D-4, N-1 to N-3, A-1 to A-5. Every entry has all 12 required fields (id, source_ids, category, severity, blocking, location, claim, evidence, authority, source_findings, debate_outcome, remediation), and every remediation has exactly file, change and verifier. No duplicate id.
- Document flow: PASS. Every finding has a `# provenance:` comment above it (27 provenance comments in the file in total, including the header and section comments). Multi-line text uses `>-`; evidence strings are quoted. No `TODO` or placeholder text remains (grep checked).

### Internal References
- Total references: 17
- Resolved: 17
- Broken: 0
- The 17 references:
  1. `blocking_findings: [R-1]` to finding R-1.
  2. R-1 debate_outcome "see rejected_claims" to the `rejected_claims` section.
  3. R-1 remediation "see late_launch_ruling" to the `late_launch_ruling` section.
  4. R-4 claim "the other imports are A-1" to A-1.
  5. R-4 debate_outcome "Authorized ... (A-1)" to A-1.
  6. A-1 claim "valid_operation_id is R-4" to R-4.
  7. A-1 evidence "see R-4" to R-4.
  8. D-3 claim "the audit copy is N-1" to N-1.
  9. D-4 claim "the runner part is A-2" to A-2.
  10. D-4 debate_outcome "split into D-4 (Drift) and A-2" to A-2.
  11. Header comment `adversarial/refactor-plan.md` to the plan file (exists).
  12. Header comment `adversarial/scoring-matrix.md` to the scoring file (exists).
  13. Header comment `adversarial/merge-log.md` to this log (exists).
  14-17. `late_launch_ruling.invariants` INV-003, INV-004, INV-005, INV-006 to `invariant-probe.md:11-14` (all four rows exist).
- Items 4 to 10 were found by a regex scan for register ids inside other findings' text fields; every match resolves to an existing id.

### Contradiction Re-Scan
- New contradictions introduced: 0
- No register id has two categories: PASS. Each of the 19 ids carries exactly one category.
- Four source ids appear under two categories, each by an explicit plan split, and each half names the other half in its claim: X-003 and C-005 (R-4 Regression and A-1 Authorized, `refactor-plan.md:23`, `:34`, `:59`); C-009 (D-3 Drift for the cycle copy and N-1 Necessary for the audit copy, `:29`, `:31`); C-012 (D-4 Drift for `stderr_fallback` and A-2 Authorized for the runner clock, `:30`, `:35`). These are splits the plan made, not contradictions.
- Every blocking finding is a Regression: PASS. The only finding with `blocking: true` is R-1 (category regression); `blocking_findings` is `[R-1]` and agrees.
- Counts (machine-counted from the parsed YAML), all PASS against `refactor-plan.md:126`:
  - Regression 7 (1 blocking)
  - Drift 4
  - Necessary 3
  - Authorized 5
  - Advisory 17
  - Grounding Gaps 6
  - Rejected claims 9 (against the 9 rows at `refactor-plan.md:99-107`)
- Verdict FAIL agrees with one surviving blocking Regression (`refactor-plan.md:122-124`). `invariant_probe.blocked: false` agrees with 0 HIGH UNADDRESSED invariants (`invariant-probe.md:27`, `:31`).

## Corrected Citations
Two plan citations pointed at the wrong lines. Both were re-read and corrected in the merged artifact; no category, severity or blocking ruling changed.

| # | Plan citation | Corrected to | What the plan line actually holds | Where applied in `merged-verdict.yaml` |
|---|---|---|---|---|
| 1 | `audit.py:204-206` for the audit copy of `_fsync_dir` (`refactor-plan.md:31`, `:106`) | `audit.py:110-115` | `audit.py:204-206` is `_ENTRY_STATES = frozenset({...})`; `_fsync_dir` is defined at `audit.py:110-115` (same four-line body as `record.py:310-315`) | N-1 location and evidence; the `_fsync_dir` row of `rejected_claims` |
| 2 | DF register `:208` for DF-29 in A-5 (`refactor-plan.md:38`; also `scoring-matrix.md:87`) | DF register `:156` | `:208` is the P7 phase row, which only mentions DF-29; the DF-29 decision row itself is at `:156` | A-5 evidence and authority |

Additions, not corrections: N-1 also cites `audit.py:200` (`_UTC_TS_FORMAT`, the audit copy of C-009 that the plan row names but does not locate); R-4 also cites `record.py:183` (the use site of `valid_operation_id`).

Range note: R-3 evidence cites `tests/issue_watch/test_audit.py:214-220` (the whole `test_reasons_pin_59_names` test); its verifier keeps the plan's `:215-219`, which lies inside that range. Not a correction.

UNVERIFIED citations: none. Every file:line in the artifact was found on re-read.

## Plan Concerns
The plan was applied unchanged on every category, severity and blocking ruling. These points are recorded for the orchestrator; none was acted on beyond what is stated.

1. **R-5 file count.** The plan remediation says "Those four test files", but the five skip sites are in three files: `test_cli.py` (`:967`, `:1070`), `test_record.py` (`:739`) and `test_cycle.py` (`:735`, `:4694`). The artifact names the three files.
2. **INV-001 design line.** `invariant-probe.md:5` and `:9` cite design `:21` for the single-store guarantee; the plan uses design `:17`. The executor re-read both and the plan's `:17` holds the guarantee sentence; the artifact keeps `:17`.
3. **INV-007 evidence.** The probe's claim that "paged re-reads may exhaust" the reserved budget is not shown by `github.py:448-454` alone. The artifact keeps it as advisory LOW with `verified: false`, as the plan says.
4. **D-1 exit 2 path.** The plan cites `cli.py:169` for the `status` exit 2. Line 169 only calls `_load_config(config_path, platform=False)`; the exit 2 itself comes from the config-error path at `cli.py:77-91`. The artifact's evidence says so; the plan's verifier text is kept.
5. **Grounding Gap detail is partly executor-derived.** The plan's Grounding Gaps line (`refactor-plan.md:93`) gives only labels. `missing_evidence` was taken from `scoring-matrix.md:78-91` (and the C-029 list of departures from `diff-analysis.md:59`, which names five of the seven). The fields `lines_seen_by_executor` and `next_evidence_needed` were written by this executor to meet the requested field list; they are derived, not plan text, and do not reclassify any gap.
6. **Judge independence.** `judge_class_collision: true` (`refactor-plan.md:118`): the judge shares a model class with the variants. The plan's mitigation, a review of this Step 5 merge by a fresh context, has not been run; this executor cannot review its own output as the gate.

## Summary
- Total changes planned: 10 change groups (19 register rows, 17 advisory rows, 6 Grounding Gaps, 9 rejected claims, 1 ruling, header scalars)
- Successfully applied: 10 of 10
- Failed: 0
- Skipped: 0
- Citations corrected: 2 (`audit.py:204-206` to `audit.py:110-115`; DF register `:208` to `:156`)
- Post-merge validation: PASS
- Verdict carried: FAIL, one blocking Regression (R-1, late launch after the 120 s cutoff); becomes PASS-with-deviations once the R-1 fix and its verifier test land (`refactor-plan.md:124`).
