# Merge Log

## Metadata
- Base: Variant 1 (`variant-1-original.md`, reviewer-1 analyzer card)
- Plan: `refactor-plan.md` (8 planned changes, 4 rejected)
- Sources for incorporated items: `variant-2-original.md`, `variant-3-original.md`, `invariant-probe.md`
- Output: `../merged-verdict-card.md`
- Executor: merge-executor
- Changes applied: 8 of 8
- Status: SUCCESS
- Timestamp: 2026-11-08

## Changes Applied

### Change 1: severity corrections (base modify) — applied
- F2 (C-001) blocking -> minor; F1 (C-002) blocking -> minor; F7 (C-007) minor -> not-a-defect; F12 (C-008) stays minor.
- Claims, evidence and recommendations of these findings are unchanged from variant 1.
- Provenance: `[base: variant-1 F1, F2, F7, F12; severity per scoring matrix C-001, C-002, C-007]`

### Change 2: C-003 rewrite (base modify) — applied
- F3 (C-003) stays the only blocking finding.
- Claim rewritten with the Round 2 mechanism: without `--re-review` the ratchet is off and the per-claim late-found assertion fails; with it, `begin` exits 5 for lack of a sentinel prior. Blocking reason restated per INV-003 (fixture list names no prior report and the assertion can never pass, not merely an unstated design). INV-001 (first seal exits 3 on 28 real changed hunks) and INV-002 (expected split taken from the code under test; quote-line rule unstated) folded in.
- Recommendation extended: name the prior report in Task 7's fixture list; seal a second time or add checked lines for the 28 hunks; fix the quote-line rule as the line the report cites, record it per claim, do not derive the expected split from the code under test.
- Evidence: F3's list plus `plan:99`, `plan:60`, `plan:77`, `source.md:193`, all copied from INV-001/002/003 rows.
- Provenance: `[base: variant-1 F3] + [invariant-probe INV-001, INV-002, INV-003]`

### Change 3: C-004 extension (base modify) — applied
- F4 (C-004) stays minor. Added: Task 10's equality test treats the Usage line as inherited, so it locks the line in (R3-1); the `E-SKILL-MISSING` rule as its own line is not in Task 10's replaced-block list (INV-004). Recommendation extended accordingly.
- Evidence added: `src/superclaude/commands/spec-panel.md:456`, `:459` (R3-1), `source.md:115` (INV-004).
- Provenance: `[base: variant-1 F4] + [variant-3 R3-1] + [invariant-probe INV-004]`

### Change 4: insert C-009 — applied
- New minor finding from V2 R2-QA-002 (card severity blocking; merged at the debate's minor). Claim, evidence and recommendation verbatim.
- Provenance: `[variant-2 R2-QA-002]`

### Change 5: insert V3 minor findings and extend F11 — applied
- Inserted C-014 (R3-3), C-015 (R3-4), C-016 (R3-5), C-018 (R3-10), C-020 (R3-12), C-021 (R3-A1), each with verbatim claim, evidence and recommendation.
- R3-A1 is an advisory with no category or recommendation in the source: category set to `advisory`, recommendation restates the advisory as an action citing source.md:104 (no new evidence).
- F11 (C-013) extended with R3-6 claim text, evidence (`plan:25`, `plan:57`, `plan:135`) and recommendation.
- Provenance: `[variant-3 R3-3, R3-4, R3-5, R3-10, R3-12, R3-A1]`; C-013 `[base: variant-1 F11] + [variant-3 R3-6]`

### Change 6: insert invariant-probe items — applied
- Inserted INV-005, INV-006, INV-007, INV-008, INV-009 as minor (probe MEDIUM, UNADDRESSED). Category is the probe's category; claims are excerpts of the probe's evidence column; evidence copied from the same row.
- The probe rows carry no recommendation field; each recommendation restates the gap the probe names as the action to close it (no new evidence).
- Provenance: `[invariant-probe INV-005 .. INV-009]`

### Change 7: confirmed deviation classification (base keep) — applied
- `confirmed_deviations`: Unattended-section removal = authorized (owner ruling, V1 A3); test_routing_refresh.py edit = necessary (V1 A2); section-5 templates = drift (C-018).
- `deviation_counts` changed from base `{authorized: 1, necessary: 1, drift: 0, regression: 0}` to `{authorized: 1, necessary: 1, drift: 1, regression: 0}`.
- Not carried: base `confirmed` items A4, Q2, Q5 and the base `calibration` block, because the requested card schema has no key for them. They remain in `variant-1-original.md`.
- Provenance: `[base: variant-1 confirmed] + [variant-3 R3-10 drift]`

### Change 8: header — applied
- Provenance header comments (Base: Variant 1 reviewer-1 analyzer; merge date 2026-11-08), `merged_from`, `convergence_score: 0.97`, `blocking_findings: [C-003]`, and a `# Source:` comment before every finding.
- Base `plan:` and `spec:` path keys kept.
- Provenance: `[refactor-plan Change 8]`

### Not made (per plan)
- C-017 (R3-7), C-019 (R3-11), C-007 as a defect (F7, kept at not-a-defect), V2 R2-QA-001 as blocking drift (merged as F12 minor). Recorded under `not_made`.

## Post-Merge Validation
- YAML parses: PASS (re-read and parsed with PyYAML `safe_load`; keys: merged_from, plan, spec, convergence_score, blocking_findings, findings, confirmed_deviations, deviation_counts, not_made).
- Every finding has id, severity, evidence: PASS (24 findings, 0 missing; no duplicate ids).
- Exactly one blocking finding, C-003: PASS (`blocking_findings: [C-003]` matches the only finding with severity blocking).
- No evidence entry absent from the sources: PASS (every entry found literally, or as a `file` plus `:N` shorthand on the same source line, in variant-1/2/3 or invariant-probe; 0 missing).
- Severity values: blocking, minor, not-a-defect only.
- Structural integrity: one fenced yaml block; finding order is base order (F1..F12), then Change 4, Change 5, Change 6 insertions.
- New contradictions introduced: 0. C-007 appears in `findings` as not-a-defect and in `not_made` as a rejected defect, which is consistent with Change 1.

## Summary
| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 8 | 8 | 0 | 0 |
