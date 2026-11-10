# Merge Execution Log

## Metadata
- Base: Variant 2 (`variant-2-original.md`, reviewer-2, qa persona, haiku)
- Non-base: Variant 1 (`variant-1-original.md`, reviewer-1, analyzer persona, sonnet), plus the Round 2 consensus (debate-transcript.md) and the Round 2.5 invariant probe (`invariant-probe.md`)
- Plan: `refactor-plan.md` (31 changes, auto-approved 2026-11-08T18:59:26Z)
- Executor: merge-executor agent
- Merged output: `merged-verdict.yaml` (stub written first, then filled)
- Changes applied: 31 of 31 planned
- Status: success
- Timestamp: 2026-11-08T19:05:37Z

## Changes Applied

Provenance for every finding sits in its `source:` field (YAML has no HTML comments; the template's `<!-- Source: ... -->` tags are carried as `source:` values ending "merged per Change #N"). The file header carries the three provenance comments.

### Part A: Corrections to base findings

### Change 1: Reclassify QA-001 as Regression, HIGH
- **Status**: Applied
- **Source**: Round 2 consensus (both rebuttals)
- **Target**: Base `findings:` QA-001
- **Before**: `class: Drift`, HIGH; evidence without source.md:275; fix without cross-reference.
- **After**: `class: Regression`, HIGH; `source.md:275` added to `evidence:`; finding gains "source.md:154 is a test-case list, not the rule; the rule at source.md:29, :40, :149 limits deferral to review 2 on."; fix gains "See INV-027 ..."; `related: [INV-027]`.
- **Provenance tag**: `source: "Variant 2 QA-001 (base; ...); merged per Change #1"`
- **Validation**: Structural integrity OK | References OK (INV-027 resolves) | Contradictions none

### Change 2: Relabel QA-002 as Drift (subtype: coverage gap)
- **Status**: Applied
- **Source**: Round 2, V2 rebuttal disputed row 1
- **Target**: Base QA-002
- **Before**: `class: Drift`, MEDIUM, no subtype; fix without placement.
- **After**: `subtype: coverage gap` added; fix extended: sentence written by `diffgate.py` into `deferred.md` (a Task 4 AC), not the Close text, so the Diffgate bullet 6 pin stays verbatim. INV-025 (probe, LOW) named in `source:` as the origin of the placement constraint.
- **Provenance tag**: `source: "Variant 2 QA-002 (base; ... INV-025, LOW); merged per Change #2"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 3: Remove QA-003 from the findings; keep it as a coverage-artifact note
- **Status**: Applied
- **Source**: Round 2, both rebuttals; S-004
- **Target**: Base `findings:` (delete), `notes:` (append), `calibration.per_finding` (delete QA-003)
- **Before**: QA-003, Drift / coverage gap, MEDIUM, citing coverage-matrix.json:230-239; calibration entry QA-003.
- **After**: QA-003 absent from `findings:` and `calibration.per_finding`; `notes:` item "Coverage artifact (not a plan finding; formerly QA-003, ...)" with the plan's wording (C1-C12, source.md:133, :144; plan:37, :42, :49; recompute 28/35).
- **Provenance tag**: note text names "formerly QA-003, removed from findings per Change #3"
- **Validation**: Structural integrity OK | References OK (no finding references QA-003) | Contradictions: removes the base's one internal contradiction

### Change 4: Relabel QA-004 as Drift (subtype: coverage gap); cross-reference INV-029
- **Status**: Applied
- **Source**: Round 2, V2 rebuttal disputed row 1; C-002
- **Target**: Base QA-004
- **Before**: `class: Drift`, MEDIUM, no subtype; fix ending "never fabricate result-r3.json".
- **After**: `subtype: coverage gap`; fix keeps "never fabricate result-r3.json" and appends "The value read for an early terminal review is the owner's call (INV-029, source.md:280); until ruled, README must state the open question instead of picking a value."; `related: [INV-029]`.
- **Provenance tag**: `source: "Variant 2 QA-004 (base; ...); merged per Change #4"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 5: Merge F4 into QA-005 with the corrected exception list
- **Status**: Applied
- **Source**: V1 F4 + base QA-005; X-001, C-001; negative case from INV-031
- **Target**: Base QA-005 (`finding:`, `fix:`, citations replaced; `merged_from:` added)
- **Before**: QA-005 finding on Diffgate bullets unpinned; fix "Extend Task 7 to pin all six Diffgate bullets exactly, plus a negative test on one behavioral clause."; single citation plan:103. F4 a separate V1 LOW finding with the wrong exception list.
- **After**: finding adds the `## Usage` drift-guard gap (spec-panel.md:19-24, plan:97); fix pins all six Diffgate bullets, adds a Diffgate-bullet negative test, and states exceptions (a) Usage, (b) Review Loop, (c) Diffgate, (d) Tool Coordination, (e) Unattended mode absent, plus "Resolve INV-024 before pinning bullet 4."; citations plan:103, :110, :114, source.md:86-96, src/superclaude/commands/spec-panel.md:19-24; `merged_from: [F4]`; `related: [INV-024]`; F4's calibrator entry nested under QA-005 as `merged_F4`. MEDIUM, Drift.
- **Provenance tag**: `source: "Variant 2 QA-005 (base) + Variant 1 F4 ... INV-031; merged per Change #5"`
- **Validation**: Structural integrity OK | References OK (F4 is a merged alias; INV-024 resolves) | Contradictions none (F4 no longer listed separately)

### Part B: Incorporations from Variant 1

### Change 6: Add F1 as Drift (subtype: coverage gap), MEDIUM
- **Status**: Applied
- **Source**: V1 F1; Round 2; A-005
- **Target**: `findings:` MEDIUM block
- **Before**: Not in base. In V1: Regression, MEDIUM, citation test file :36-56.
- **After**: Drift / coverage gap, MEDIUM; citation `[plan:89, plan:104, plan:149, plan:25, tests/skills/test_review_severity_rule.py:28-51]`; finding names test_a (172), test_f (320), test_i (448), test_k (506) and records the PR CI severity rationale; fix per plan (`git add -N` on new `src/` files only, never `.claude/`; `tests/` not in `_SCAN_TREES`; step in each AC).
- **Provenance tag**: `source: "Variant 1 F1 (...); merged per Change #6"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 7: Add F2 as Drift, MEDIUM
- **Status**: Applied
- **Source**: V1 F2; C-003
- **Target**: `findings:` MEDIUM block
- **Before**: Not in base. In V1: Regression, MEDIUM, title only.
- **After**: Drift, MEDIUM; title kept; `finding:` states the plan:83 vs plan:86 self-contradiction; fix kept. The INV-026 note is in `source:`. A first draft put it in `fix:`; post-merge validation flagged INV-026 there as an id that is not a finding, so it was moved to `source:`, where probe ids are provenance.
- **Provenance tag**: `source: "Variant 1 F2 (...); invariant-probe INV-026 (ADDRESSED) ...; merged per Change #7"`
- **Validation**: Structural integrity OK | References OK (after the move) | Contradictions none

### Change 8: Add F3 as Drift, LOW
- **Status**: Applied
- **Source**: V1 F3; Round 2 consensus
- **Target**: `findings:` LOW block
- **Before**: Not in base. In V1: MEDIUM, title with the hedge ".dev/tasks may be absent in CI".
- **After**: LOW; hedge dropped from the title and finding; verified premise only (source.md moves to `.dev/tasks/done/`; plan:110 embeds Task 7's text, plan:86 silent for Task 5); fix kept.
- **Provenance tag**: `source: "Variant 1 F3 (...); merged per Change #8"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 9: Add F5 as Drift, LOW, narrowed
- **Status**: Applied
- **Source**: V1 F5; calibrator partial
- **Target**: `findings:` LOW block
- **Before**: Not in base. In V1: fix "Do not ship T10-R3-reviser.txt as a template ...".
- **After**: finding adds "plan:172 and :174 already route T10 to the coordinator; the residual gap is that the template ships ready to dispatch."; fix replaced with the plan's two-option fix.
- **Provenance tag**: `source: "Variant 1 F5 (...); merged per Change #9"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 10: Add F6 as Drift, LOW, retitled
- **Status**: Applied
- **Source**: V1 F6; calibrator
- **Target**: `findings:` LOW block
- **Before**: Not in base. In V1: title "insertion point ambiguous".
- **After**: title "Reviser line is appended after the 'Finish with worker_done' instruction (placement)"; finding states placement, not ambiguity; fix aligned with the Task 12 diff AC (plan:178).
- **Provenance tag**: `source: "Variant 1 F6 (...); merged per Change #10"`
- **Validation**: Structural integrity OK | References OK | Contradictions: removes V1's F6 contradiction

### Change 11: Add F7 as Drift (subtype: coverage gap), LOW
- **Status**: Applied
- **Source**: V1 F7; Round 2
- **Target**: `findings:` LOW block
- **Before**: Not in base. In V1: Regression, LOW.
- **After**: Drift / coverage gap, LOW; fix kept. The plan says to add `source.md:209` to the citation; V1's citation already held it, so the citation stays `[plan:173-174, source.md:209, source.md:229]` with no duplicate.
- **Provenance tag**: `source: "Variant 1 F7 (...); merged per Change #11"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 12: Add F8 as Drift, LOW
- **Status**: Applied
- **Source**: V1 F8; calibrator partial
- **Target**: `findings:` LOW block
- **Before**: Not in base. In V1: fix led with the stub output.
- **After**: fix reordered so validation in `main` before dispatch comes first, then the stub output.
- **Provenance tag**: `source: "Variant 1 F8 (...); merged per Change #12"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 13: Add F9 as Authorized expansion, LOW, with the Round 2 fix
- **Status**: Applied
- **Source**: V1 F9; C-006; Round 2 disputed row 3
- **Target**: `findings:` LOW block
- **Before**: Not in base. In V1: title includes "base-commit 2cb683f5 classification claim unverified"; fix lists Constraints / draft marking.
- **After**: new title per plan; citation per plan; fix "Amend the plan:19 scope line ..."; every claim that 2cb683f5 is unverified removed from the finding. The V1 calibrator reason kept in `calibration.per_finding.F9` ("... so 'unverified' is overstated") rebuts that claim and does not make it, so it stays as the calibrator's record.
- **Provenance tag**: `source: "Variant 1 F9 (...); merged per Change #13"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 14: Add F10 as Drift (subtype: coverage gap), LOW
- **Status**: Applied
- **Source**: V1 F10; calibrator note
- **Target**: `findings:` LOW block
- **Before**: Not in base. In V1: Drift, LOW.
- **After**: Drift / coverage gap, LOW; fix kept (`make lint`, output under `./artifacts/`).
- **Provenance tag**: `source: "Variant 1 F10 (...); merged per Change #14"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 15: Add the 35-case floor as advisory ADV-1
- **Status**: Applied
- **Source**: V1 `correctness_gaps_advisory`; INV-014 ADDRESSED
- **Target**: new top-level block after `findings:`
- **Before**: No advisory block in base.
- **After**: one item `{id: ADV-1, text: ..., source: ...}` with the plan's text. The block is named `advisory:` (the caller's output contract) instead of the plan's `correctness_gaps_advisory:`; the content and position are as planned.
- **Provenance tag**: `source: "Variant 1 correctness_gaps_advisory (...); merged per Change #15"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 16: Add V1's `confirmed_ok` block
- **Status**: Applied
- **Source**: V1 `confirmed_ok` (7 items); S-002
- **Target**: new top-level block after `advisory:`
- **Before**: No such block in base.
- **After**: the seven items copied verbatim (single-quoted YAML strings), with a comment that they were true at audit time and were not re-verified by the merge.
- **Provenance tag**: block comment "Source: Variant 1 confirmed_ok, copied verbatim per Change #16"
- **Validation**: Structural integrity OK | References n/a | Contradictions none

### Part C: New findings from the debate

### Change 17: Add M-01, LOW
- **Status**: Applied
- **Source**: Round 2 V1 rebuttal; V2 A-008; closes INV-009
- **Target**: `findings:` LOW block
- **Before**: Not present.
- **After**: Drift / coverage gap, LOW; citation `[plan:29, plan:133, plan:155, plan:173, plan:178]`; finding and fix (grep AC for `--unattended`, output under `./artifacts/`) per plan.
- **Provenance tag**: `source: "Round 2 ...; merged per Change #17"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 18: Add M-02, LOW; remove `unraised_gaps`
- **Status**: Applied
- **Source**: base calibrator `unraised_gaps`; U-017
- **Target**: `findings:` LOW block; `calibration.unraised_gaps` (removed)
- **Before**: gap listed only in base `calibration.unraised_gaps`.
- **After**: Drift / coverage gap, LOW; citation `[plan:37, plan:42, source.md:144]`; fix per plan; `related: [INV-007]`; `unraised_gaps` no longer present.
- **Provenance tag**: `source: "Variant 2 calibrator unraised_gaps (...); merged per Change #18"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Part D: Invariant findings

### Change 19: Add INV-001 as HIGH
- **Status**: Applied
- **Source**: invariant-probe.md INV-001 (blocking)
- **Target**: `findings:` HIGH block, after INV-010
- **Before**: Not present.
- **After**: Drift, HIGH; citation per plan; finding and probe fix per plan; `source:` labels it "raised by the Round 2.5 probe, not calibrator-verified".
- **Provenance tag**: `source: "invariant-probe.md INV-001 (...); merged per Change #19"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 20: Add INV-010 as HIGH, needs owner ruling
- **Status**: Applied
- **Source**: invariant-probe.md INV-010 (blocking)
- **Target**: `findings:` HIGH block
- **Before**: Not present.
- **After**: Drift, HIGH, `needs_owner_ruling: true`, `provisional_class:` with the plan's Regression-or-withdrawn note; citation, finding and probe fix per plan, ending "Execution of Tasks 2, 4 and 12 waits on that ruling."
- **Provenance tag**: `source: "invariant-probe.md INV-010 (...); merged per Change #20"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 21: Add INV-002, MEDIUM
- **Status**: Applied
- **Before / After**: not present -> Drift, MEDIUM; citation `[plan:71, plan:74, source.md:262]`; fix direction per plan; `related: [INV-001]`.
- **Provenance tag**: `source: "invariant-probe.md INV-002 (...); merged per Change #21"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 22: Add INV-003, MEDIUM
- **Status**: Applied
- **Before / After**: not present -> Drift, MEDIUM; citation `[plan:71, plan:74, source.md:27, source.md:239]`; fix direction per plan (`closed` with `halt: escalate`, next `begin` exits 4).
- **Provenance tag**: `source: "invariant-probe.md INV-003 (...); merged per Change #22"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 23: Add INV-006, MEDIUM
- **Status**: Applied
- **Before / After**: not present -> Drift / coverage gap, MEDIUM; citation `[plan:71, plan:74, source.md:49, source.md:112]`; fix direction per plan (three exit-5 guards).
- **Provenance tag**: `source: "invariant-probe.md INV-006 (...); merged per Change #23"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 24: Add INV-007, MEDIUM
- **Status**: Applied
- **Before / After**: not present -> Drift, MEDIUM; citation `[plan:37, plan:42, source.md:144, source.md:254, source.md:264]`; fix direction per plan (stale-lock rule); `related: [M-02]`.
- **Provenance tag**: `source: "invariant-probe.md INV-007 (...); merged per Change #24"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 25: Add INV-011, MEDIUM
- **Status**: Applied
- **Before / After**: not present -> Drift, MEDIUM; citation `[plan:41, plan:49, plan:52, source.md:125, source.md:149]`; fix direction per plan (old-side numbering, `side=old` test).
- **Provenance tag**: `source: "invariant-probe.md INV-011 (...); merged per Change #25"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 26: Add INV-018, MEDIUM
- **Status**: Applied
- **Before / After**: not present -> Drift, MEDIUM; citation per plan (7 lines); fix direction per plan (reword "the single line", review-2 PASS test).
- **Provenance tag**: `source: "invariant-probe.md INV-018 (...); merged per Change #26"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 27: Add INV-021, MEDIUM
- **Status**: Applied
- **Before / After**: not present -> Drift, MEDIUM; citation `[plan:49, source.md:39, source.md:81, source.md:149]`; finding uses the plan's `R<k>.<j>` vs `R<N>.<j>` wording; fix direction per plan.
- **Provenance tag**: `source: "invariant-probe.md INV-021 (...); merged per Change #27"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 28: Add INV-024, MEDIUM
- **Status**: Applied
- **Before / After**: not present -> Drift, MEDIUM; citation `[plan:21, plan:103, source.md:91, source.md:94]`; fix direction per plan (dual-surface bullet 4, recorded as a Necessary deviation, then pinned); "Resolve before the QA-005 pin."; `related: [QA-005]`.
- **Provenance tag**: `source: "invariant-probe.md INV-024 (...); merged per Change #28"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 29: Add INV-027, MEDIUM
- **Status**: Applied
- **Before / After**: not present -> Drift / coverage gap, MEDIUM; citation `[plan:49, source.md:120, source.md:125, source.md:149]`; fix direction per plan (review-1 FINDING form); `related: [QA-001]`.
- **Provenance tag**: `source: "invariant-probe.md INV-027 (...); merged per Change #29"`
- **Validation**: Structural integrity OK | References OK | Contradictions none

### Change 30: Add INV-029, MEDIUM
- **Status**: Applied
- **Before / After**: not present -> Drift, MEDIUM; citation per plan (6 lines); fix direction per plan (same owner confirmation as INV-010); `related: [QA-004, INV-010]`. `needs_owner_ruling: false`: the plan sets that field only on INV-010 (Change 20 and the target table); INV-029's fix routes the question into INV-010's ruling instead of carrying a separate flag.
- **Provenance tag**: `source: "invariant-probe.md INV-029 (...); merged per Change #30"`
- **Validation**: Structural integrity OK | References OK | Contradictions: see re-scan note on the verdict_note

### Part E: Card-level update

### Change 31: Update header, notes, calibration and verdict
- **Status**: Applied
- **Source**: Round 2 consensus; convergence assessment; both calibrators
- **Target**: base header, `notes:`, `calibration:`, `verdict:`
- **Before**: `reviewer: reviewer-2`, `persona: qa`, `model_class: haiku`, `self_confidence: 0.94`, calibration with 5 per_finding entries and `unraised_gaps`, `verdict: refactor`, 3 notes.
- **After**: `reviewer: "merged (reviewer-2 base + reviewer-1)"`; `provenance:` list (reviewer-2 qa haiku, calibrated 0.85; reviewer-1 analyzer sonnet, calibrated 0.81; probe INV-NNN; Round 2 M-01; reviewer-2 calibrator M-02); each reviewer's calibration dimensions moved under its provenance entry; `self_confidence` dropped; `notes:` keeps the 3 base items, adds the BLOCKED_BY_INVARIANTS note and the QA-003 note; `calibration.per_finding` keeps QA-001, QA-002, QA-004, QA-005 (with F4 nested), adds V1's F1, F2, F3, F5-F10, and marks every INV-NNN and M-01 "not calibrator-verified" (M-02 marked as raised by the reviewer-2 calibrator); `unraised_gaps` dropped; `verdict: refactor` with the plan's `verdict_note`. Caller-required keys added: `merge_method: adversarial` (first key), `base_variant`, `counts`, `convergence`.
- **Provenance tag**: header comments + `provenance:` list
- **Validation**: Structural integrity OK | References OK | Contradictions none

## Post-Merge Validation

### Structural Integrity
- YAML parses: OK. Verified by reading the file back with PyYAML 6.0.3 (`yaml.safe_load`) after the last edit.
- Key order: OK. `merge_method` is the first key; all caller-required keys are present (`merge_method`, `base_variant`, `verdict`, `findings`, `notes`, `advisory`, `confirmed_ok`, `counts`, `convergence`), plus the plan's `reviewer`, `mode`, `grounding_root`, `provenance`, `verdict_note`, `calibration`.
- Provenance header: OK. The first three lines are `# Provenance: produced by /sc:adversarial`, `# Base: Variant 2`, `# Merge date: 2026-11-08T19:05:37Z`.
- Finding ordering: OK. HIGH, then MEDIUM, then LOW; inside a severity, the plan's target-table order (lowest task number first).
- Required fields: OK. All 27 findings carry `id`, `class`, `severity`, `needs_owner_ruling`, `citation`, `finding`, `fix`, `source`. Every `class` is one of the four taxonomy classes, every `subtype` is `coverage gap`, and every `source` ends with "merged per Change #N".
- `needs_owner_ruling: true` only on INV-010.

### Internal References
- References checked: `related:` and `merged_from:` ids, finding ids named in `finding:`/`fix:` text, `calibration.per_finding` keys, `convergence.blocking_items`.
- Resolved: all. F4 resolves as merged into QA-005 (`merged_from`); QA-003 resolves to the notes item.
- Broken: 0, after one fix. The first validation run flagged INV-026 in F2's `fix:` (a probe id, not a finding id); it was moved to F2's `source:` (see Change 7) and the re-run passed.
- Probe ids cited only as provenance in `source:` fields (they resolve to `invariant-probe.md`, not to findings): INV-009, INV-025, INV-026, INV-031.
- Every finding has a `calibration.per_finding` entry; every key there is a finding id.

### Contradiction Re-Scan
- Duplicate ids: 0 (27 unique).
- Contradictory duplicates: none. The overlapping pairs complement each other and cross-reference: QA-001 / INV-027 (rule vs grammar), QA-004 / INV-029 (missing branch vs owner value), M-02 / INV-007 (lock test vs recovery rule), QA-005 / INV-024 (pin vs text to pin), INV-001 / INV-002 (replay copy vs degraded replay).
- F4 is not listed separately from QA-005; QA-003 is not a finding.
- One point for the orchestrator to note, not a contradiction: `verdict_note` says Tasks 2, 4 and 12 wait for the owner to rule on INV-010 and INV-029, while INV-029 carries `needs_owner_ruling: false` because the plan sets the flag only on INV-010 and routes INV-029 into that ruling (Change 30). If INV-029 should carry its own flag, that is a plan change.
- New contradictions introduced: 0.

### Counts
- Declared `counts: {HIGH: 3, MEDIUM: 15, LOW: 9}`; counted from the list: HIGH 3, MEDIUM 15, LOW 9. Match. These equal the plan's target totals. Advisory: 1 (ADV-1), kept outside `findings:`.
- `convergence: {diff_point_agreement: 1.0, status: BLOCKED_BY_INVARIANTS, blocking_items: [INV-001, INV-010]}`.

## Summary
- Total changes planned: 31
- Successfully applied: 31
- Failed: 0
- Skipped: 0
- Plan items adjusted in form only (content kept): Change 15 block named `advisory:` per the caller's output contract; Change 11 citation already contained source.md:209; Change 7 INV-026 note placed in `source:`.
- Post-merge validation: PASS
