# Diff Analysis: reflect reviewer-card comparison

## Metadata

- Generated: 2026-11-06T21:56:30Z
- Mode: A (`--compare`), 3 variants, depth standard, focus: correctness, coverage, deviation-classification
- Prerequisites validated: output path is under `.dev/reflect/`, not under `.claude/{skills,agents,commands}/`; all 3 inputs exist (WARN: inputs are YAML cards, not markdown; proceeding)
- Variants:
  - Variant 1 (`variant-1-original.md`): reviewer 1, analyzer lens, sonnet slot. 6 findings (R1-1..R1-6), blind calibration 0.85
  - Variant 2 (`variant-2-original.md`): reviewer 2, qa lens, haiku slot. 2 findings (QA-1, QA-2), blind calibration 0.82
  - Variant 3 (`variant-3-original.md`): reviewer 3, refactorer lens, opus slot. 5 findings (R3-1..R3-5) + 3 advisory (R3-A1..A3), blind calibration 0.82
- Subject under review (all variants): plan `.dev/tasks/to-do/TASK-WF-workerContractFo-20261106-214402/TASK-WF-workerContractFo-20261106-214402.md` against `source.md` in the same package
- Total differences found: 16
- Categories: structural (1), content (10), contradictions (3), unique (8), shared assumptions (2)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Card shape | findings + checked_and_found_clean (11 items) + blind_calibration | findings + checked_and_found_clean (5) + limitations + blind_calibration | findings + separate `correctness_gaps_advisory_non_gating` block + checked_clean + not_checked + blind_calibration | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | Task 1 acceptance criterion 3 (write-verb scan on WORKER-CONTRACT.md) is vacuous | R1-3, P3: replace with `test_every_repo_setup_line_is_gated` + `RULE_PHRASES['WC-4']` pins | QA-2, P2: targeted WRITE_VERB_RE assertion on the new sentence, with a synthetic negative | R3-2, P3: grep the WC-4 lines for `git add`, or drop the criterion | Low (agree on the defect; differ on priority and fix) |
| C-002 | How the planned WC-4 assertion isolates WC-4 | R1-4, P3: slice `"- **WC-4."` .. `"\n- **WC-8."` | not raised | R3-3, P3 (calibrated P2): same slice | Low |
| C-003 | WC-4 "the report names where those files were written" vs workflow's report | R1-2, P2: reword conditionally or keep a workflow note; owner note | not raised | R3-A1, advisory (calibrated P2) | Medium |
| C-004 | Task 4 test.md `artifacts` clause pin | R1-6, P3: placement after the `artifacts` token | QA-1, P1: pin must require the ignored-path exclusion and report-location wording, plus a negative | R3-4, P3: keep only "left out per WC-4", drop "which the test report names instead" | High |
| C-005 | Task 5 init-lite status assertion | R1-1, P2 (calibrated P1): also assert "when the audit finished" absent | checked clean: "Task 5 can change the status wording without changing the existing init-lite artifacts clauses" | not checked | High |
| C-006 | Scope of the search for other WC-4 copies | checked clean: "No other test or mirror pins WORKER-CONTRACT text" | not raised | R3-1, P2: design spec `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:72` restates WC-4 | Medium |
| C-007 | Remaining duplicated rule text in build/test | not raised | not raised | R3-4, P3 | Low |
| C-008 | return-contract.md pointer followability and `src/superclaude/` paths | not raised | not raised | R3-5, P3 | Low |
| C-009 | init-lite exit-code semantics (dry-run, partial scaffold, audit failure, in-skill fallback, report_path) | R1-5, P3 | not raised | R3-A3, advisory (.dev/ ignored in other projects) | Low |
| C-010 | report_path inside an ignored path under a WC-9 grant | not raised | not raised | R3-A2, advisory, out of brief | Low |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Impact |
|---|-------------------|--------------------|--------------------|--------------------|--------|
| X-001 | Should the test.md `artifacts` clause carry the exclusion and report-location wording itself? | R1-6: only placement matters | QA-1: "require an explicit ignored-path exclusion and report-location wording within the extracted artifacts clause" | R3-4: "Task 4: write the coverage paths as 'left out per WC-4' and drop 'which the test report names instead'" | Medium |
| X-002 | Priority of the vacuous Task 1 AC3 | P3 (R1-3) | P2 (QA-2) | P3 (R3-2) | Low |
| X-003 | Are there other copies of WC-4 text the plan must keep consistent? | "No other test or mirror pins WORKER-CONTRACT text. Grep found no plugin copy" | not addressed | "The live design spec has a full copy of WC-4 ... the plan never mentions it" (R3-1) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 1 | R1-1: the "exited 0" check passes with the old contradicting status sentence still present | High |
| U-002 | 1 | R1-5: verified init_lite.py exit paths (dry-run :348-352, scaffold FileExistsError, ClickException :247-262) | Medium |
| U-003 | 1 | R1-6: `_artifacts_clause` placement hazard for test.md | Low |
| U-004 | 2 | QA-1: Task 4 pin does not require the exclusion itself | High |
| U-005 | 3 | R3-1: design spec copy of WC-4 | Medium |
| U-006 | 3 | R3-4: build/test still restate parts of the rule after the change | Low |
| U-007 | 3 | R3-5: installed ref `return-contract.md` cannot follow a bare "WC-4" | Low |
| U-008 | 3 | R3-A2/R3-A3: report_path and init-lite scaffold paths vs the new exclusion in other projects | Low |

## Shared Assumptions

Agreement points scanned: all three agree the plan covers the brief, that `_artifacts_clause` returns the rest of the first matching line (STATED by V1 and V2), and that `/sc:implement` runs tasks in order (STATED by V1 and V3).

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | Every variant writes its `exact_change` as an edit to the plan file, but the caller (`/sc:workflow` Wave 4) runs reflect as advisory and never edits the plan; the changes can only land through the executor (`/sc:implement`) applying them in-task or through a regenerated plan. No variant says which. | All cards' `exact_change` fields target plan task text | Medium: decides whether the findings change anything | UNSTATED, promoted [SHARED-ASSUMPTION] |
| A-002 | Each variant grades priority as if the planned test assertions are the only guard against wrong text; none counts the per-task acceptance-criteria QA review that `/sc:implement` runs after each task as a second guard (validation rule / guard condition). | P1/P2 grades on R1-1, QA-1, QA-2, R3-3 | Medium: affects P1 vs P2 calibration | UNSTATED, promoted [SHARED-ASSUMPTION] |

## Summary

- Total structural differences: 1
- Total content differences: 10
- Total contradictions: 3
- Total unique contributions: 8
- Total shared assumptions surfaced: 4 (UNSTATED: 2, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-004, C-005
- Similarity check: differences are well above 10% of comparable items; debate proceeds
- Taxonomy pre-tags: L1 = S-001, C-007; L2 = C-003, C-006, C-008, C-010, X-003, A-001; L3 = C-001, C-002, C-004, C-005, C-009, X-001, X-002, A-002
