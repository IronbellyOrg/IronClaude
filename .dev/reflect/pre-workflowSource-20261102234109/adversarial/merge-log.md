# Merge Log (sc:adversarial Step 5)

## Metadata

- Base: `variant-1-original.md` (V1, reviewer 1, analyzer, sonnet)
- Plan: `refactor-plan.md` (PC-01..PC-22, auto-approved 2026-11-03T00:18:24Z)
- Other inputs: `variant-2-original.md` (V2), `variant-3-original.md` (V3), `invariant-probe.md`, `debate-transcript.md`, `base-selection.md`
- Output: `merged-verdict.yaml`
- Executor: merge-executor
- Merge date: 2026-11-03T00:23:38Z
- Convergence: 1.0 (13/13 diff points); status BLOCKED_BY_INVARIANTS (INV-001, INV-002, INV-008); verdict FAIL

## Placement decisions (shape requested by the orchestrator)

- The plan's `consistency_notes:` (PC-10, PC-11) and `reviewer_artifact_notes:` (PC-12) are one `notes:` list, told apart by `kind: consistency` / `kind: reviewer_artifact`, each with `class: none` and no severity.
- The invariant texts that the plan targets at R1-F1's recommendation (PC-04 to PC-09) are held once, under `required_remedy_additions:` (one entry per invariant, `applies_to: R1-F1`). R1-F1's recommendation item (4) points to them. This keeps one copy of each text and avoids drift between two copies.
- Split findings get suffixed ids: R1-F5a/R1-F5b (PC-18), R1-F8b (PC-15), R1-F9b (PC-14). Imported findings keep their source ids: R3-F6, R3-F7, R3-F9.

## Changes Applied

| PC | Target | Status | Before -> After | Source |
|---|---|---|---|---|
| PC-01 | header, `routing:`, `status:`, `verdict:` | Applied with correction (escalated) | No routing/status -> `routing:` (SKILL.md:60, quality-gates.md:22), `status: partial (...)`, `verdict: FAIL` kept. The plan text says "remedy additions PC-03..PC-05", but INV-001/002/008 are PC-04/05/06 in the same plan; written as PC-04..PC-06. Orchestrator should confirm. | A-001, A-002 |
| PC-02 | R1-F1 claim, citation, recommendation | Applied | R2-F1 evidence and implement.md:11 added; "Add a final task" option and final-make-test.log removed; ranked items (1) Task 66 AC, (2) Constraint line; R3-F1 Task 67 concession recorded under `concessions:` | V2 R2-F1, V1, V3 |
| PC-03 | R1-F1 recommendation | Applied | New item (3): Task 26 smoke AC (tasklist:255-258); "PC-21" reference written as "finding R3-F9" | V3 R3-F1 |
| PC-04 | R1-F1 / `routing:` | Applied | `required_remedy_additions` INV-001 (qa.md:15, implement.md:91); routing states re-run-only delivery. The "remove Round-2 equivalence wording" step had nothing to remove in the base card (V1 had no such wording); satisfied by the INV-001 text | invariant-probe INV-001 |
| PC-05 | R1-F1 | Applied | `required_remedy_additions` INV-002 (baseline log, "no failures beyond the baseline") | INV-002 |
| PC-06 | R1-F1, verdict note | Applied | `required_remedy_additions` INV-008 and `verdict_note:`; references to "PC-04/PC-05/PC-07" written as the invariant ids INV-001/INV-002/INV-003 they implement | INV-008 |
| PC-07 | R1-F1 | Applied | Single log -> three named logs (t26-smoke, t66-smoke, t66-make-test) with path:line evidence; INV-003 | INV-003 |
| PC-08 | R1-F1 item (3) | Applied | INV-004: Task 26 also runs tests/unit/test_cli_install.py | INV-004 |
| PC-09 | R1-F1 | Applied | INV-006: smoke on Tasks 2, 13, 29 and D02 | INV-006 |
| PC-10 | R1-F11 | Applied | `findings` (class authorized) -> `notes` (class none); claim now "except B-W22.6 (see finding R1-F9b, C-003)" | V1 concession, S-002 |
| PC-11 | notes | Applied | R3-F10 added, class none | V3 concession |
| PC-12 | notes | Applied | R2-F5 added as `kind: reviewer_artifact`, class none; count corrected to 66 as recommendation | V2 concession |
| PC-13 | R1-F10 | Applied | grounding-gap -> drift; CONSOLIDATED-PLAN.md:636, tasklist:19, source.md:36 added; one Constraint sentence | C-006, V2 R2-F6 |
| PC-14 | R1-F9, new R1-F9b | Applied | B-W22.6 removed from R1-F9's sub-item list (citation kept verbatim); new drift/minor R1-F9b with V3 citations and remedy and the V2 imprecision note (tasklist:426) | C-003 |
| PC-15 | new R1-F8b | Applied | drift/minor: Task 37 omits B-W12 #6; remedy fold into Task 47 (tasklist:424) | C-004, V3 R3-F4 |
| PC-16 | R1-F8 | Applied | grounding-gap kept; forward-link case and CONSOLIDATED-PLAN.md:249 (via tasklist:67), :308 added; "list full dependency sets on 47 and 66" appended; R3-F5 drift class and tasklist:65 discarded | C-005 |
| PC-17 | R1-F3 recommendation | Applied | "check all three" -> per-linking-file grep AC; R2-F2 deviations alternative | C-002 |
| PC-18 | R1-F5 | Applied | Split: R1-F5a `necessary` (pin, .pre-commit-config.yaml:74-77); R1-F5b `drift` (relaxation clause, tasklist:28 and :74-78 qualification; base :74-88 kept) | C-007, X-002 |
| PC-19 | R1-F4 citation | Applied | tasklist:143,146,265,281 -> tasklist:143,146,265,273,281. Checked against the tasklist: :273 is in Task 28 (install --fresh), :281 is in Task 29, so :281 stays | V1 calibration |
| PC-20 | new R3-F6 after R1-F4 | Applied | Imported verbatim, drift/minor | V3 U-010 |
| PC-21 | new R3-F9 after R1-F1 | Applied | Imported, grounding-gap/minor, citation Makefile:109-157 -> Makefile:109; Makefile:166; source.md:43, tasklist:88 in recommendation | V3 U-012 |
| PC-22 | new R3-F7 after R1-F8b | Applied | Imported, drift/minor | V3 U-011 |

Base items with no planned change, carried unchanged: R1-F2, R1-F6, R1-F7.

## Post-Merge Validation

- YAML parse: `uv run python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" merged-verdict.yaml` succeeded.
- Shape: header line present; merge_method, convergence_score 1.0, convergence_status, blocking_invariants [INV-001, INV-002, INV-008], verdict FAIL all match. 16 findings, all with id, source_variants, claim, citation, class (from the allowed set), severity, recommendation; 3 notes with class none and no severity; 6 required_remedy_additions, of which the 3 marked blocking equal `blocking_invariants`.
- Provenance: every list item has a `# provenance:` comment; all 22 PC ids appear in the file.
- Citation trace: 115 file:line tokens parsed from the citation fields; all 115 found in a source card, invariant-probe.md or refactor-plan.md (0 untraced). tasklist:65 is cited nowhere.
- Rejected content absent: no "Add a final task" or final-make-test.log in any recommendation; no verification-only Task 67; B-W22.6 not in R1-F9.
- Contradiction re-scan: none found. Exactly one blocking finding (R1-F1), matching the verdict note. R1-F11 no longer claims full coverage against R1-F9b. R1-F5a (necessary) and R1-F5b (drift) cover separate parts. R1-F8's "47 on 3,17,43-46" and R1-F8b's "Task 47 already depends on Task 46" agree (direct predecessor only). R1-F1 item (3) and R3-F9 agree that sync checks are not verification.

## Escalation

- PC-01 internal reference: the plan writes "PC-03..PC-05" for the INV-001/002/008 additions; the same plan defines them as PC-04, PC-05 and PC-06. Applied as PC-04..PC-06. No other plan item needed correction.

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 22 | 22 (1 with a reference correction, PC-01) | 0 | 0 |
