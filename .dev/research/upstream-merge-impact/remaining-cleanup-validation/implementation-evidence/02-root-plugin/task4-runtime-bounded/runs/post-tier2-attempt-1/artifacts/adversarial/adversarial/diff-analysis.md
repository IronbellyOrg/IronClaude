# Diff Analysis: Tier-2 Reviewer Deviation Card Comparison

## Metadata
- Generated: 2026-10-24T21:21:47Z
- Variants compared: 2
  - Variant A = `variant-1-original.md` (reviewer-1: sc:reflect-reviewer, persona analyzer, slot sonnet, reported model claude-sonnet-5-5[1m])
  - Variant B = `variant-2-original.md` (reviewer-2: sc:reflect-reviewer, persona qa, slot haiku, reported model grok-4.7[1m])
- Mode: A (--compare), depth standard, focus correctness, coverage, deviation-classification
- Evidence root for falsifiability checks: `reviewer-snapshot/root` (frozen snapshot). Card paths are relative to it.
- Total differences found: 24 (plus 4 promoted [SHARED-ASSUMPTION] points, giving 28 debate points)
- Categories: structural (6), content (6), contradictions (3), unique (9), shared assumptions (8 enumerated; 4 UNSTATED promoted, 4 STATED, 0 CONTRADICTED)
- Taxonomy levels (S/C/X/A, 23 points): L1 = 3, L2 = 14, L3 = 6

Orchestrator neutrality note: this file records differences. It does not adjudicate them. Where a card made a claim that can be checked against the snapshot, the check result is recorded as an observation for the debate.

## Structural Differences

| # | Area | Variant A | Variant B | Severity | Level |
|---|------|-----------|-----------|----------|-------|
| S-001 | Empty deviations-table row | Single row `none \| n/a \| n/a \| ...` with `n/a` severity. No separate precedence walk. | Single row of `—` cells, then a paragraph walking the precedence order (Regression > Drift > Necessary > Authorized). | Low | L1 (presentation/formatting) |
| S-002 | Grounding-gaps artifact format | Markdown table, IDs `GG-1` and `GG-2`. Columns: id, hunk_ref, evidence_missing, why_not_classifiable, next_evidence_needed, owner. No `decision_needed_by_user` field. | Fenced YAML list, no IDs. Fields follow the taxonomy schema, including `decision_needed_by_user` (true on the first entry, false on the second). | Medium | L2 (artifact interface/schema conformance) |
| S-003 | Per-requirement coverage section | None. Coverage appears only in the "Adherence summary" bullets. | Dedicated "Coverage findings (acceptance lens)" table, F-001 to F-004, with a Tag column (Grounded / unevidenced). | Medium | L2 (organization) |
| S-004 | Section order and challenge layout | Deviations, Grounding gaps, Challenge to T1 (numbered 1-6 with Agree/Sharpened/Mostly agree labels), Correctness gaps, Adherence, Risks, Recommendations, Notes. Confidence is inline at the end. | Opening verdict paragraph, Deviations, Coverage findings, T1 challenge (split into "Agreed" and "Challenged" lists), Grounding gaps, Adherence, Risks, Recommendations, Notes, then a separate "Self-reported confidence" section. | Low | L1 (section ordering/presentation) |
| S-005 | Advisory correctness-gap section | Present. Two-row table "Correctness gaps (advisory — non-gating)" with a "Sibling disagreement" column. | Absent on purpose. One sentence explains why ("No advisory correctness-gap section"). The same two subjects appear as Risks #3 and #4. | Medium | L2 (organization of the report's component sections) |
| S-006 | Risks and recommendations format | Risks: numbered list of 3, no tags. Recommendations: 3-row table (File / Change / Verifier). | Risks: 4-row table with a Grounded/[INFERRED] Tag column. Recommendations: numbered list of 4 in **File/Change/Verifier** form. | Low | L1 (formatting) |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity | Level |
|---|-------|-------------------|-------------------|----------|-------|
| C-001 | How the grounding gaps are split | Two gaps, divided by what is missing. GG-1: T-103 completion claim has no diff backing (`completed.md:8` vs `changes.patch:1-9`). GG-2: R-003 tests were never executed (`spec.md:11-12`). Both owner `user`. | Two gaps, divided differently. Gap 1 combines the missing execution and the missing diff provenance for `tests/test_greeting.py:1-13` (`decision_needed_by_user: true`). Gap 2 is new: the `status: done` stamp has no task log behind it (`completed.md:2`, `:6-8`), with `decision_needed_by_user: false`. | High | L3 (completion-state / status-gating classification) |
| C-002 | Patch citation ranges | Gives the patch evidence as `changes.patch:5-9` in the deviations row, and `changes.patch:7-9` for R-001 and R-002. | Says the body is `changes.patch:6-9` and line 5 is the `@@` header. Uses `changes.patch:1-4` for the file header. Also says "`changes.patch` is 10 lines". Snapshot observation: `changes.patch` has 9 lines (wc -l = 9, final newline present). Line 5 is `@@ -0,0 +1,4 @@` and lines 6-9 are the body. So B's line-count claim is falsified, while its body-range claim matches the snapshot. A's `:5-9` includes the header line. | Medium | L2 (default; citation correctness) |
| C-003 | How far the T1 "no divergence" headline reaches | Limits the zero-deviation result to `src/greeting.py` ("not to the whole change"). Says it "can read as a clean pass". | Calls the T1 headline "ledger-true and acceptance-false" (`__run_evidence__/t1-card.md:22`), states "QA does not sign the work off", and says S_dev_density 0/1 "does not mean requirement acceptance is 100%". | Low | L2 (default) |
| C-004 | Import-path remediation | Recommends running both `python -m pytest` and plain `pytest` from the project root. Does not assess T1 recommendation 3. | Same two runs, plus: only if plain pytest exits 2, set `pythonpath = .` (or similar) in root pytest config, and do not treat `tests/__init__.py` as the fix (rejects T1 recommendation 3). | Medium | L2 (module/dependency resolution) |
| C-005 | R-003 and regression accounting | "R-003: presence confirmed ... Execution is unverified and diff backing is absent (GG-1, GG-2)." Deviation counts are all 0. No explicit `regression_present` field. | Adds "Unclassifiable (grounding gaps): 1 (R-003 / T-103)" and `regression_present: false`, and gives the conditions under which Regression could not be minted. | Low | L2 (default) |
| C-006 | Self-reported confidence | Split: 0.8 for zero deviations on `src/greeting.py`, about 0.5 for the change overall. Overall status `partial` + `needs_human_decision`. | Single value 0.76, capped by missing R-003 execution, missing test-file provenance, and the inferred import outcome. | Medium | L2 (default; calibration structure) |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact | Level |
|---|-------------------|-------------------|-------------------|--------|-------|
| X-001 | Whether the T-103 no-hunk gap could later be reclassified as Drift | GG-1: "A completion claim with no diff backing could be an unmapped change (Drift) or a claim about pre-existing or out-of-scope work." Risks #2: "It could turn out to be unmapped work, which would make it Drift." | "Not upgraded to Drift: Drift requires an unmapped diff hunk. T-103 is a task with no hunk, which is missing provenance, not extra work." | Medium | L3 (classification boundary between Grounding Gap and Drift) |
| X-002 | Evidence tag for the missing package/config files (`src/__init__.py`, conftest, pyproject, etc.) | Challenge #4: "the absence of `src/__init__.py` cannot be treated as evidence about the live project. The snapshot cannot support 'Grounded for file absence'. That tag should be [INFERRED]." | Risk #2: "Grounded for the import line and for the missing config files (snapshot file list). `[INFERRED]` for the failure mode." Also counts "8 snapshot files; none of those". Snapshot observation: the snapshot does contain 8 files and none of the listed config files. Neither card shows whether the live root has them, because the live root was out of bounds for both. | Medium | L2 (evidence grounding / dependency config) |
| X-003 | Whether the `if not name` falsy-guard behaviour counts as an advisory correctness gap | Correctness gap #1: "Falsy vs. truthy input handling is inconsistent ... The guard enforces a 'name required' intent (`src/greeting.py:3`) that the f-string at `:4` does not enforce for type or whitespace." (listed under "Sibling disagreement") | Risk #3: "Not a contradiction, not a sibling-symbol correctness gap (`greet` has no sibling)." Also: "No advisory correctness-gap section ... Spec silence on whitespace and non-strings is not a sibling-contract split." | Medium | L3 (guard / input-validation rule) |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | Argues that the T1 metric `S_dev_density = 0/1` cannot see T-103, because it counts only hunks that exist. So the metric says nothing about the one place a deviation could hide. | Medium |
| U-002 | A | Notes that the snapshot holds selected inputs only, so file absence in the snapshot says nothing about the live project layout. (This is the basis of A's side of X-002.) | High |
| U-003 | B | Per-requirement acceptance table F-001 to F-004, with evaluation at the semantic level (for example, "`not \"\"` is true, so an empty string raises `ValueError`"), plus spec, task and diff citations for each requirement. | Medium |
| U-004 | B | Rejects T1 recommendation 3: `tests/__init__.py` "does not put the project root on `sys.path`". Offers a conditional `pythonpath = .` fix as the alternative. | High |
| U-005 | B | Corrects T1's "both files are 4 lines" and its `:5-9` body range to `:6-9`. Note: this item also contains B's claim that `changes.patch` is 10 lines, which the snapshot falsifies (see C-002). | Medium |
| U-006 | B | Checks reachability and runtime surface: `greet` is an undecorated function and is not on the runtime-surface allowlist, so empty `runtime_surface_requirements` is correct and skipping reachability is not a gap. | Low |
| U-007 | B | Walks the classification precedence explicitly (Regression > Drift > Necessary > Authorized) and sets `regression_present: false`, with stated reasons. | Medium |
| U-008 | B | Discloses model identity: the haiku slot resolves to `grok-4.7[1m]` through an alias. This matters for whether the reviewers really are heterogeneous. | Medium |
| U-009 | B | States that static closure of R-001 does not depend on the unexecuted test. The f-string is deterministic, and `tests/test_greeting.py:5` is a second oracle that was never run. | Low |

## Shared Assumptions

Agreement points scanned:
- Zero 4-class deviations.
- H1 maps to T-101 and T-102.
- R-001 and R-002 are adherent on a static reading.
- R-003 execution is unverified.
- Non-empty grounding gaps force `partial` + `needs_human_decision`.
- Shared pytest exit-code mapping: 0 closes the gap, 1 is Regression, 2/3 is a Grounding Gap, 5 is Drift/coverage.
- Whitespace and non-string inputs are not spec contradictions.
- `test_empty` is a weaker oracle that still satisfies R-002.
- The reuse audit says `distinct`.
- Both recommend running `python -m pytest` and plain `pytest`.
- Both recommend amending the spec for R-002.

### Enumerated preconditions

| # | Agreement Source | Assumption | Classification | Promoted | Level |
|---|------------------|------------|----------------|----------|-------|
| A-001 | Zero deviations; H1 is the only code hunk | Restricting the diff to `--scope src` hides nothing except `tests/test_greeting.py`. No other out-of-scope files were changed by the audited work, so the scope boundary leaves no other unmapped hunks. | UNSTATED | Yes | L3 (scope boundary) |
| A-002 | R-001 adherent | `spec.md:6` "the exact string Hello, Ada! for Ada." means the literal `Hello, Ada!` with the `!`, and the final `.` ends the sentence rather than being part of the string. | UNSTATED | Yes | L2 |
| A-003 | Shared exit-code mapping | The taxonomy's pytest exit-code table is the authoritative classifier for any future R-003 run. | STATED (both cite the taxonomy table) | No | L2 |
| A-004 | Status forced to partial | A non-empty grounding-gaps artifact forces `status: partial` and `needs_human_decision: true`. (Snapshot-adjacent check: `plugin/skills/sc-reflect-protocol/refs/deviation-taxonomy.md:149-153` says this.) | STATED | No | L3 (return-contract state) |
| A-005 | R-002 adherent; whitespace not a contradiction | R-002 "empty" means `""` (and other falsy values) only, so the `if not name` guard satisfies it, and whitespace-only or non-string names are outside the validation rule. | STATED (both note `spec.md:9` says only "empty" and recommend a spec amendment) | No | L3 (guard / validation rule) |
| A-006 | All citations | The five core files in `reviewer-snapshot/root` (`spec.md`, `completed.md`, `changes.patch`, `src/greeting.py`, `tests/test_greeting.py`) are faithful byte copies of the live `audit_repo_root` files at audit time. | UNSTATED (both say the live root was not read; neither states snapshot fidelity, though both depend on it) | Yes | L2 |
| A-007 | R-001 deterministic f-string; R-002 behaviour | Tests and code run under a Python 3 interpreter (3.6+ for f-strings) whose `not` / f-string semantics match the static reading. No interpreter or dependency version is stated anywhere. | UNSTATED | Yes | L2 (runtime dependency) |
| A-008 | R-003 execution unverified | No test results exist anywhere for this run. The "verification triangle not run" statement (`__run_evidence__/artifacts/task-to-diff-map.md`, verification section) is accurate and complete. | STATED | No | L2 |

### Promoted [SHARED-ASSUMPTION] points

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | [SHARED-ASSUMPTION] The `--scope src` boundary hides no out-of-scope change other than `tests/test_greeting.py`. | Zero deviations / single mapped hunk | High: if false, unmapped hunks could exist, which is a Drift signal that neither card evaluated. | Open for debate |
| A-002 | [SHARED-ASSUMPTION] R-001's "exact string" is `Hello, Ada!`, with the sentence-final `.` excluded. | R-001 adherent | Low: the natural reading, but neither card states it. | Open for debate |
| A-006 | [SHARED-ASSUMPTION] The snapshot core files are byte-faithful to the live audit root. | All citations | Medium: every Grounded tag in both cards rests on it. A provenance manifest exists (`reviewer-snapshot/provenance-manifest.json`) but neither card cites it as checked. | Open for debate |
| A-007 | [SHARED-ASSUMPTION] Python 3.6+ runtime semantics apply. | R-001 / R-002 static adherence | Low: the fixture is trivial, but no runtime version is evidenced. | Open for debate |

CONTRADICTED assumptions: none found. The snapshot checks made (8-file listing, patch hunk layout, `t1-card.md:22` "no divergence found", taxonomy lines 149-153) do not contradict any precondition that both variants depend on. The only falsified factual claim (B: "`changes.patch` is 10 lines") belongs to Variant B alone and is recorded under C-002 / U-005.

## Summary
- Total structural differences: 6
- Total content differences: 6
- Total contradictions: 3
- Total unique contributions: 9 (A: 2, B: 7)
- Total shared assumptions surfaced: 8 (UNSTATED: 4, STATED: 4, CONTRADICTED: 0)
- Total debate points (S + C + X + U + promoted A): 28
- Taxonomy coverage (S/C/X/A points): L1 = 3 (S-001, S-004, S-006); L2 = 14 (S-002, S-003, S-005, C-002, C-003, C-004, C-005, C-006, X-002, A-002, A-003, A-006, A-007, A-008); L3 = 6 (C-001, X-001, X-003, A-001, A-004, A-005). All three levels have coverage.
- Highest-severity items: C-001 (High), A-001 (High impact); High-value unique items: U-002, U-004
- Verdict-level agreement: both variants report 0 Authorized / 0 Necessary / 0 Drift / 0 Regression, R-001 and R-002 statically adherent, R-003 unresolved, and final status `partial` + `needs_human_decision`. Disagreements concern the shape of the gaps, classification boundaries (X-001, X-003), evidence tagging (X-002), citation precision (C-002), and remediation (C-004).

## Similarity Check
- Comparable items: 24 differences + 15 agreement points (the 11 listed under Shared Assumptions, plus: H1/T-101/T-102 mapping citations, the test_empty oracle note, the T-103 widen-scope/task-log recommendation, and "live root not read") = 39.
- Difference ratio: 24 / 39 = 61.5%.
- Threshold: below 10% means "substantially identical".
- Result: NOT substantially identical (61.5% ≥ 10%). Do not skip the debate. Steps 2-3 should proceed.
