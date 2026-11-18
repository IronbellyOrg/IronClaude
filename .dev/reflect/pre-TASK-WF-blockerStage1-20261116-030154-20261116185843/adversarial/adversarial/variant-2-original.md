persona: qa
model_class: haiku
model: claude-gw-tier2[1m]
model_observed: OpenAI GPT-5 (exact deployment variant unavailable) (self-report of the reviewer; does not match the haiku pin: identity_mismatch_suspected)

Card text below is the reviewer's hand-back, saved verbatim (de-indented). Its aliases: PLAN = the plan file, SPEC = `merged-requirements.md`, SOURCE = the plan's `source.md`, MATRIX = `artifacts/coverage-matrix.yaml` of this run folder (absolute paths in the original text were left as the reviewer wrote them).

# Reflect Reviewer — Deviation Findings

**Reviewer persona:** qa
**Grounding root:** `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel`
**Diff scope:** Pre-execution review of the supplied stage 1 plan; no Git diff supplied.
**Timestamp:** 2026-11-16
**Total deviations:** 2

Citation aliases (all absolute):
- **PLAN:** `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md`
- **SPEC:** `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`
- **SOURCE:** `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md`
- **MATRIX:** `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/reflect/pre-TASK-WF-blockerStage1-20261116-030154-20261116185843/artifacts/coverage-matrix.yaml`

## Findings

### R2-F1
**blocking:** yes
**claim:** Task 9 says the scale-map lookup key is “taken from the `origin` of the ledger row,” but the ledger contract defines `origin` as the protocol name plus original finding id, not one of Task 3’s twelve family keys. Following that instruction literally makes a valid, known-scale ledger finding look like an unknown family and return UNSET, preventing the intended reviewer-label comparison.
**evidence:** PLAN:151 specifies the lookup and unknown-family result; PLAN:62 specifies keys such as `lens-scale` and `reflect`; SPEC:353 defines `origin`, and SPEC:355 defines the separate provenance-bearing `source`. PLAN:179–186 tests direct family keys but adds no ledger-to-family integration case.
**repair:** Specify how the caller derives the family key from provenance without replacing the original provenance fields. Add an integration fixture containing a contract-valid ledger row, including its protocol and original finding id, and assert that its native label resolves through the correct scale-map row.

### R2-F2
**blocking:** yes
**claim:** Task 12 assigns only the classifier-column update—“write the same text into that row’s `classifier` column”—and never assigns the required `unsettled` tag for SHOW_USER. Its acceptance tests can therefore pass while an existing Medium row receiving SHOW_USER remains an ordinary follow-up instead of entering the needs-your-decision count and ordering.
**evidence:** PLAN:192 and PLAN:197–199 define the command’s writes and tests; PLAN:87 requires the reference to describe the tags but does not implement their production. SPEC:369 defines `unsettled` as the SHOW_USER tag and requires its inclusion in `show_user`; SPEC:596 explicitly requires tagging while retaining the reviewer’s label.
**repair:** Assign SHOW_USER tagging to Task 12 through the sole ledger writer. Add a command-level fixture asserting that SHOW_USER preserves the native label, adds `unsettled` without clearing existing tags, and moves the row into `show_user` counting.

### R2-F3
**blocking:** no
**claim:** The coverage matrix omits requirement-bearing Revision 3 spans rather than merely failing to match them: SOURCE:51’s before-creation entry gate, SOURCE:52’s acceptance/name corrections, and SOURCE:53’s prohibition on the two existing threshold-constant names have no corresponding retained or dropped requirement rows. These requirements are present in the plan, so this is an audit-coverage defect, not an additional plan defect.
**evidence:** SOURCE:51–53; MATRIX:508–547 retains only the importer end point and lint additions from line 53, while MATRIX:548–635 contains neither source lines 51–52 nor the threshold-name requirement. PLAN:36, PLAN:52, PLAN:72, PLAN:151, PLAN:192 and PLAN:234 contain the relevant corrections.
**repair:** Add quote-pinned coverage rows for those spans and map them to their actual tasks; do not count a nearby requirement on the same source line as covering the omitted instruction.

## Deviations

| # | Category | Location | What diverged | Evidence | Severity |
|---|----------|----------|---------------|----------|----------|
| R2-F1 | Drift | PLAN:151 | Treats provenance as a scale-family key without defining the conversion | PLAN:62; SPEC:353–355 | MEDIUM |
| R2-F2 | Drift | PLAN:192 | Leaves SHOW_USER ledger tagging unassigned and untested | PLAN:197–199; SPEC:369,596 | MEDIUM |

R2-F3 concerns this review’s coverage artifact and is not counted as an implementation-plan deviation.

## Earlier findings check

Live-line references below all refer to **PLAN**.

- **F1 / M-F1:** fixed, line 129—Python-only grep, empty-result-compatible wording and end points.
- **F2:** fixed, lines 64,70,234,241–242—installed-only exemption carried into T4.
- **F3:** fixed, lines 66,74—both code-assigned files included.
- **F4:** fixed, lines 22,124,128,248—separate ledger decision, adapter ownership and owner report.
- **F5 / M-F2:** grammar fixes present, lines 62,71,151,234,241; the newly specified provenance lookup has R2-F1.
- **F6 / F7:** fixed, lines 164,177–185,204–211—dependencies and function/test ownership align.
- **F8 / F9:** fixed, lines 56,82,88,192—full grep path, named commands and ninth state.
- **M-F3:** lookup assigned, line 124—cross-run declined/filed/resolved matching and test.
- **M-F4:** fixed, lines 166,171,179,185,192,198—M precheck, D inputs, permitted-question tests and four counts.
- **M-F5:** storage/update fixes present, lines 124,192,199; SHOW_USER tagging remains separately unassigned under R2-F2.
- **M-F6:** fixed, lines 137,141—injected resolver and default by-path-loader test.
- **M-F7:** fixed, lines 82,90,99–100,115—reference-path restrictions and checks.
- **M-F8:** fixed, line 36—entry gate precedes file creation.
- **M-F9:** fixed, lines 52,72,192,234—grep wording, recount, command name and T3 wording.
- **M-F10:** fixed, lines 129,151,160,173,200,213—importer end point, constant names and lint acceptance.

## Adherence summary

- Work units audited: **16 task definitions**, including their acceptance criteria.
- Fully adherent at the reviewed task-definition level: **14**.
- Authorized expansion: **0** | Necessary deviation: **0** | Drift: **2** | Regression: **0**.
- All eleven stage 1 exit tests have assigned tasks: T1–T4 → Task 15; T6/T11 → Task 11; T7 → Task 7; T8 → Task 8; T12 → Tasks 11/13; T13 → Task 14; T17 → Task 13.
- The skill folder, codec/reader/writer, adapters, fixture judge, property tests, filing tests and install check all have task owners. Task numbering is contiguous and declared dependencies point backward.

## Notes

This was a static pre-execution review, not evidence that the planned tests pass. No commands or tests were run and no files were changed. The two blocking findings concern missing or incompatible integration instructions that the listed unit tests would not necessarily expose.

## Verdict

**NEEDS-REVISION**
**confidence:** 0.87
**blocking ids:** `[R2-F1, R2-F2]`

Recommended action: repair the two classifier-to-ledger integration requirements and add their command-level fixtures before execution; correct the coverage omissions alongside them.

reviewer_model_self_report: OpenAI GPT-5 (exact deployment variant unavailable)

## Calibration (blind, opus class)
```yaml
calibrated_C: 0.82
per_dimension: {citation_grounding: 0.90, coverage_completeness: 0.85, deviation_classification_clarity: 0.75, risk_surface_coverage: 0.75, recommendation_actionability: 0.85}
verified_citations: 14 re-read, all held
blocking_grade_support: {R2-F1: yes, R2-F2: partly}
note: the card marks R2-F1 blocking but rates it MEDIUM in its own Deviations table
calibrator_model_class: opus
```
