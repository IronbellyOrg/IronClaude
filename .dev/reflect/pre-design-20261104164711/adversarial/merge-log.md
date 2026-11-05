# Merge Execution Log

## Metadata
- Base: Variant C (opus:refactorer) = `variant-3-original.md`, reviewer 3
- Non-base inputs: Variant A (sonnet:analyzer, `variant-1-original.md`), Variant B (glm-5.3:qa, `variant-2-original.md`), and positions no card held (calibrator finding CF-22, invariant probe INV-006 and INV-007, R-INV)
- Executor: merge-executor agent
- Plan: `refactor-plan.md` (11 planned changes, auto-approved 2026-11-04T18:48:52Z)
- Output: `merged-verdict.yaml` (artifact type: YAML reviewer card, so "sections" are top-level keys and findings)
- Changes applied: 11 of 11 planned
- Status: success
- Timestamp: 2026-11-04T19:04:05Z

Execution note: the plan edits a reviewer card, not a document with H2 headings. Changes were applied as record-level edits to the base card's `findings` list. Provenance is carried in a `provenance` list on each finding, a `# Source:` comment above each finding, and the header comment of the file (the YAML form of the template's `<!-- Source: ... -->` tags).

## Changes Applied

### Change 1: Re-key the findings to CF rows, one defect per row
- **Status**: Applied
- **Source**: `diff-analysis.md` equivalence map; debate S-001 (consensus, 80%)
- **Target**: Base `findings` list (restructure)
- **Before**: 11 base findings F-1..F-11. F-1 and F-5 each bundled two defects.
- **After**: 23 findings in table order: CF-01..CF-22 plus INV-007. Each has `id`, `cf_ref`, `severity`, `deviation_class`, `claim`, `evidence`, `recommendation`, `provenance`, and `qualifier` where the plan sets one. Every recommendation carries a `Verify:` sentence. Evidence paths imported from A and B are repo-relative.
- **Provenance tag**: `# Source:` comment above each finding, plus `provenance:` list
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 2: Apply the R-INV resolution for CF-05 and CF-06
- **Status**: Applied
- **Source**: Base F-1; A R2 (4b on Task 5); B R2 (Task 8 -> 4b); C R2 fallback (5 -> 4a, 9 -> 4b); `invariant-probe.md`; `round-inv-advocate-{A,B,C}.md`
- **Target**: Base F-1 recommendation (replace), now CF-05 and CF-06
- **Before**: F-1 split Task 4 into 4a and 4b but gave no edge set for Task 5, Task 8 or Task 9, and no document position for 4b.
- **After**: CF-05 lists the nine plan edits (4a heading; 4b heading and Depends-on line between Task 7 and Task 8 with a body sentence; split of P:92, P:93, P:99, P:100; re-pointed edges P:106, P:155, P:171; stale reference P:241; Task 3 on Task 1). It states the resulting document order and closure. CF-06 carries the split line and cross-refers to items 1 and 3 to 6.
- **Provenance tag**: `provenance:` list on CF-05 and CF-06 naming base F-1, A, B, C and R-INV
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (the edge set was rebuilt and checked, see Post-Merge Validation)

### Change 3: Add the INV-007 row
- **Status**: Applied
- **Source**: `invariant-probe.md` INV-007; R-INV E4 (A, B and C ACCEPT)
- **Target**: Base, new finding after CF-22 (append)
- **Before**: Section did not exist.
- **After**: `INV-007`, severity low, class left as "unassigned" (never assigned in debate), recommendation "P:66 Task 3 becomes Depends on: Task 1, Task 2".
- **Provenance tag**: `# Source: invariant-probe.md INV-007; R-INV E4`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 4: Add CF-22 and the A-002 method note
- **Status**: Applied
- **Source**: `calibration-t2.yaml` missed lists; A-001 and A-002 (ACCEPT by all three)
- **Target**: Base, new finding CF-22 plus one sentence in `summary` (append)
- **Before**: Neither existed. No card found the Task 10 / Task 11 / Task 18 consumers of Task 4a.
- **After**: CF-22 (P:184 Task 10 becomes "Depends on: Task 3, Task 4a"). `summary` carries "Edge audit expands spec test-case IDs and export lists (S:741-749) into the functions they use, and computes closures from the plan graph, not by name matching."
- **Provenance tag**: `provenance:` on CF-22; `shared_assumptions` entries A-001 and A-002
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 5: Rewrite the edge findings CF-01, CF-02, CF-03, CF-04 and CF-17
- **Status**: Applied
- **Source**: Base F-2, F-3, F-4, F-5; B Q-4 (grep); A-4 / Q-8 (Task 6 named); debate C-001, C-002, C-003, U-001, A-006
- **Target**: Base F-2..F-5 (replace)
- **Before**: F-5 bundled Task 15 and Task 20. F-2 required Tasks 6, 13 and 14 for Task 19. F-3 had no header-match check. F-4 offered "minimum: Task 13 Depends on Task 10".
- **After**: F-5 split into CF-02 (Task 15 on 4a, 12) and CF-04 (Task 20 on 6, 9, 18, 19). F-2 cut to CF-17 (Task 13 required; Tasks 6 and 14 optional). CF-03 gets Task 6 and the header-match grep from B. CF-01 keeps the chain 10 -> 11 -> 12 -> 13 and drops the "minimum" alternative.
- **Provenance tag**: `provenance:` lists on each of the five rows
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 6: Apply the INV-006 regrade with its qualifier
- **Status**: Applied
- **Source**: `invariant-probe.md` INV-006; round-inv E5 (A, B and C QUALIFY)
- **Target**: Severity fields of CF-01, CF-02, CF-03 (edge part only), CF-04, CF-17 and CF-22, plus one sentence in `summary`
- **Before**: The base rated the edge findings Medium, on the premise that the executor follows Depends-on order (A-003).
- **After**: Those rows are Low and each carries a `qualifier:` stating "Low only while /sc:implement runs sequentially in document order with no parallel-marked set (IMPL:79, IMPL:97); a graph-order or parallel executor reverts it to Medium." CF-03 stays Medium for the header-match check and says so. The same sentence is in `summary`.
- **Provenance tag**: `qualifier:` field; `shared_assumptions` entry A-003
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (see item 4 of the re-scan)

### Change 7: Add the acceptance-criteria findings CF-07, CF-08, CF-09, CF-10, CF-13 and CF-14
- **Status**: Applied
- **Source**: Variant A (A-10b, A-6b, A-6a, A-7, A-8c, A-8d); B Q-6 and Q-7
- **Target**: Base, new findings (append)
- **Before**: Section did not exist (the base covered 13 of the 22 canonical findings).
- **After**: Six rows as written in the plan table. CF-14 has class `spec defect` and CF-07 class `advisory (not a deviation)`. CF-08 and CF-09 are Medium; the rest are Low.
- **Provenance tag**: `provenance:` list on each row
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 8: Add CF-11 and CF-12 as two findings
- **Status**: Applied
- **Source**: Variant B Q-5; A-8a and A-8b
- **Target**: Base, new findings (append)
- **Before**: Section did not exist.
- **After**: CF-11 (Task 19 capability skip) and CF-12 (fixed author and committer in P:29), both Medium and citing S:1316, naming the F9, F10, X1 and X3 breakage.
- **Provenance tag**: `provenance:` lists "B Q-5b, A A-8a" and "B Q-5a, A A-8b"
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 9: Lower CF-15
- **Status**: Applied
- **Source**: Base F-6; A-9; X-002 / C-009
- **Target**: Base F-6 (replace)
- **Before**: Severity Medium; recommendation added the reflect test to Task 9 and Task 20; Q-1 cited S:1392.
- **After**: Severity Low, class `authorized`. The reflect test goes into Task 20 only (Task 9 dropped). The log's first line reads "make test (VG-2) not run per orchestrator brief". Evidence cites S:1408.
- **Provenance tag**: `provenance:` "C (base) F-6, A A-9, B Q-1, debate C-009"
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 10: Correct labels and claims in CF-16, CF-20 and CF-21
- **Status**: Applied
- **Source**: Base F-9, F-10, F-11; X-003, X-004, C-010
- **Target**: Base F-9, F-10, F-11 (replace)
- **Before**: F-9 class `necessary`; F-10 claimed Tasks 5 and 8 on Task 4 were stricter than spec and said "optionally drop"; F-11 said "optionally tighten Task 17 to net +15".
- **After**: CF-20 (was F-9) class `drift`, anchors kept. CF-21 (was F-10) claim rewritten to "only Task 9 -> Task 6 is stricter", recommendation "Keep the edge", class `necessary`. CF-16 (was F-11) recommendation "No change", the optional tightening deleted.
- **Provenance tag**: `provenance:` on each row naming the debate point
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 11: Update the card header, summary and verdict
- **Status**: Applied
- **Source**: All three cards; `calibration-t2.yaml`
- **Target**: Base header comment, `verdict`, `self_reported_confidence`, `summary`
- **Before**: Base header "persisted by the orchestrator from the read-only reflect-reviewer return"; summary of 11 findings.
- **After**: Header "Merged by sc:adversarial Mode A from reviewers 1-3; base reviewer 3." `verdict: ready-with-fixes`. `self_reported_confidence: 0.82` (the base value, equal to its calibrated value). `summary` states 22 CF rows plus INV-007, five Medium, the 4a/4b split with 4b between Task 7 and Task 8, no regression, the A-002 method sentence and the Change 6 qualifier sentence.
- **Provenance tag**: file header comment
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Additions required by the task brief, outside the 11 plan changes
These come from the merge brief, not from `refactor-plan.md`. They add no new findings.
- `calibrated_confidence: 0.807`, the mean of the calibrated confidences in `../artifacts/calibration-t2.yaml` (A 0.82, B 0.78, C 0.82; 2.42 / 3 = 0.8067). `calibration-t1.yaml` (0.86) grades the Tier-1 reflection card and is not an input. The inputs are stated in a comment next to the key.
- `shared_assumptions`: A-001 ACCEPT, A-002 ACCEPT, A-006 QUALIFY, plus A-003, A-004 and A-005 as recorded in the debate.
- `unresolved_points`: S-004, S-005, S-006, C-013, each with a reason.
- `invariants`: the probe summary (18 findings: 11 ADDRESSED, 7 UNADDRESSED) and the state after R-INV (17 addressed, 1 moot, 0 unaddressed), with the per-item resolution.

## Post-Merge Validation

### Structural Integrity
- YAML parse: ✅ `uv run python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" <abs path>/merged-verdict.yaml` (run from the repo root) exited 0 and printed `YAML_PARSE_OK`.
- Top-level keys: ✅ `merge_method`, `base_variant`, `convergence_score`, `verdict`, `calibrated_confidence`, `findings`, `shared_assumptions`, `unresolved_points`, `invariants` all present (plus `self_reported_confidence` and `summary`). `merge_method` is `adversarial`, `base_variant` is `opus:refactorer`, `convergence_score` is 0.852, `verdict` is `ready-with-fixes`.
- Findings list: ✅ 23 entries, ids exactly CF-01..CF-22 then INV-007, no duplicates, in the plan table order.
- Required fields: ✅ every finding has non-empty `id`, `cf_ref`, `severity`, `deviation_class`, `claim`, `evidence` (a non-empty list), `recommendation` and `provenance`. `id` equals `cf_ref` on every row. The 6 qualified rows have `qualifier`.
- Severity count: ✅ 5 Medium (CF-03, CF-08, CF-09, CF-11, CF-12) and 18 Low. This matches the plan: 5 Medium, no High.
- `Verify:` clause: ✅ present in all 23 recommendations.
- `unresolved_points`: ✅ [S-004, S-005, S-006, C-013], each with a reason.
- Document flow: ✅ header comment, scalars, summary, findings, shared assumptions, unresolved points, invariants.

### Internal References
- Edge-graph rebuild from the recommendations of CF-01 to CF-05, CF-17, CF-22 and INV-007: ✅
  - Every edge points to an earlier task in the document order 1, 2, 3, 4a, 5, 6, 7, 4b, 8, 9, 10-20, so there is no cycle.
  - Task 9's closure is {1, 2, 3, 4a, 4b, 5, 6, 7}, which includes both 4a and 4b (INV-001 and INV-002 hold).
  - Task 20's closure covers every other node (CF-04). Task 19 reaches Task 13 (CF-17). Task 16 reaches Tasks 6 and 13 (CF-03). Task 15 reaches 4a (CF-02). Tasks 11 and 18 reach 4a (CF-22). The chain 10 -> 11 -> 12 -> 13 holds (CF-01).
- CF-05 recommendation text contains all edge strings the plan names ("Task 4a, Task 5, Task 7", "Task 4b, Task 7", "Task 4b, Task 5, Task 6", the t4a and t4b logs, and the resulting order).
- Cross-references inside the card (CF-06 -> CF-05 items 1 and 3-6; CF-09 -> CF-08; CF-05 item 9 -> INV-007; shared_assumptions -> CF-03, CF-15, CF-17): ✅ all targets exist.
- Plan and spec line cites: spot-read against the sources on this run (P:27-29, 51, 53, 84-100, 186-191, 215-222, 239-246, 287-307; S:728-731, 1316, 1410-1429). They match what the findings quote. The remaining cites are copied from the refactor plan, which re-read every P line number.
- Broken references found: 0. (The edge-graph check is scripted; the cross-reference and line-cite checks above were done by reading, so no total is claimed.)

### Contradiction Re-Scan
- New contradictions introduced: 0
- Checks run:
  1. Severity scale: one rule for the missing-edge rows (all Low under the qualifier, CF-03's header check Medium). No row mixes Medium and Low for one defect type without a stated reason.
  2. Task naming: every remaining bare "Task 4" describes the plan as it stands today or quotes old text being replaced (CF-02 claim and quote, CF-05 claim and item 7, CF-06 claim, CF-21 claim, CF-22 claim, summary, header note). Every recommended edit names 4a or 4b. No recommended edge points at a bare "Task 4".
  3. Classes: CF-20 is `drift` (no residual `necessary`); CF-21 is the only `necessary` row; CF-14 is `spec defect`; CF-07 is `advisory`; CF-15 and CF-16 are `authorized`.
  4. Qualifier consistency: the same sentence appears in `summary` and on all 6 qualified rows, and A-003 in `shared_assumptions` says the same. No row states the regrade without the qualifier.
  5. CF-05 vs CF-06: CF-06 refers to items 1 and 3-6; the 4a/4b log names and ACs match between the two.
  6. Optional wording: the plan removed "optionally" from CF-21 and CF-16. CF-17 still says Tasks 6 and 14 are optional, as the plan table states. CF-07 is advisory by design. No other hedged recommendation remains.
- Open items for the caller (not contradictions): S-004, S-005, S-006 and C-013 are unresolved points carried through as the plan specifies.

## Summary
- Total changes planned: 11
- Successfully applied: 11
- Failed: 0
- Skipped: 0
- Plan-listed "Changes NOT being made": respected (no import of A-5's move to Task 8, A-10a, C's own 5-on-4b edge set, B's R1 "necessary Medium", F-2's Task 6 and 14 as required edges, "9 suffices", the Task 9 import smoke, the P:19 reword, "net +15", Q-1's S:1392 cite, or B's 21-INF-row caveat as consensus)
- Post-merge validation: PASS
