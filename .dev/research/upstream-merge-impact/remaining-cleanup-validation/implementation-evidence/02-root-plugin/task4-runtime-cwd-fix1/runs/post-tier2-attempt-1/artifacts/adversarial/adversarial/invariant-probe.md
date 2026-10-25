# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

- Fault-finder: Task(subagent_type general-purpose, model opus), independent (not an advocate), read-only, agentId a21dfc43696df09af, completed first try. No Stage 1 branch-trace.md exists; sufficiency_challenge evidence uses inline source-file enumeration.
- Input: Round 2 emerging consensus (17/17 agreed), debate-transcript.md (R1 + R2), diff-analysis.md, both variants, frozen snapshot S, deviation-taxonomy.md, sc-reflect-protocol SKILL.md contract.
- Orchestrator verification: re-read deviation-taxonomy.md:56-68, :100-115, :140-176 and sc-reflect-protocol SKILL.md:1130-1160, :1370-1376, :1484-1490. The citations INV-004 (:149-152), INV-005 (:145), INV-006 (:105-113; SKILL.md:1374, :1487) and INV-011 (:58, :62, :65, :67, :109) depend on match the files.
- Orchestrator normalisation: the fault-finder's first count line was self-inconsistent and it corrected itself. The counts below are the orchestrator's direct count from the rows. MERGE_ACTION text is condensed from the agent output and kept as the refactor-plan input.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | `changes.patch` can be regenerated to "include tests/" without losing the existing H1 hunk | UNADDRESSED | MEDIUM | git-inventory.txt:2-9: everything is untracked and there is no HEAD. The t1-card.md:88 recipe `git add -N tests && git diff` would emit only tests/ and drop H1 (task-diff-map.yaml:6-9, 14, 20). V1:86 and V2:44 do not require H1 to be kept. Merge action: require one patch covering src/ and tests/; the verifier checks that H1 still maps to T-101/T-102 and that a new hunk maps to T-103. |
| INV-002 | state_variables | Setting `completed.md` frontmatter to `partial` brings the audited input and the audit state back into line | UNADDRESSED | MEDIUM | completed.md:2 `status: done` and completed.md:8 `[x] T-103`. V2:51-53 changes only the frontmatter. The snapshot copy is byte-identical to the audit root, so editing the audit root makes S stale. Contract status comes from deviation-taxonomy.md:149-151, not from completed.md. Merge action: cover line 8 too; owner is user; re-snapshot after any edit. |
| INV-003 | state_variables | Snapshot S matches the audit root for every verdict-bearing file (A-001) | ADDRESSED | LOW | The audit-root listing has no `__init__.py`/conftest/pyproject/pytest.ini/.gitignore. `cmp` shows changes.patch and completed.md are identical. Only proposed.md is missing (git-inventory.txt:5) and it adds no MUST (transcript R2). Merge action: cite git-inventory.txt:2-8 for G2 absence. |
| INV-004 | guard_conditions | G3 can be "non-gating" while it stays a `grounding_gaps` row | UNADDRESSED | MEDIUM | deviation-taxonomy.md:149-152: any non-empty grounding-gaps forces `status: partial` + `needs_human_decision: true`, with no exemption for `decision_needed_by_user: false` (:146). The advisory channel (:163) needs siblings (:175). The verdict is unchanged today only because G1/G2 also force it. Merge action: do not call G3 "non-gating"; state that it forces partial and that `decision_needed_by_user: false` only marks it as not urgent. |
| INV-005 | guard_conditions | The A-002 "owner could be the orchestrator" reading can go into gap rows | UNADDRESSED | MEDIUM | deviation-taxonomy.md:145 allows `owner: user` (default) or `reviewer`; `orchestrator` is not legal. Merge action: keep `owner: user` and put the `--scope src/` point (task-diff-map.yaml:27) in `next_evidence_needed` / `why_not_classifiable`. |
| INV-006 | guard_conditions | V1's verifier map (0 clears / 1 = Regression / 2-3 = Grounding Gap) is a complete and correct guard for the pytest run that both advocates agreed to graft | UNADDRESSED | HIGH | deviation-taxonomy.md:109 (exit 5 -> Drift/coverage), :111 (124 -> Grounding Gap), :112 (retry flaky before Regression), :113 (unmapped -> Grounding Gap) are all missing from V1:91. sc-reflect-protocol SKILL.md:1487 says exit 1 is only a Regression *candidate*. There is no HEAD (git-inventory.txt:9) and no prior run (execution.log:5). `python -m pytest` exits 1 when pytest is missing, and that would falsely set the machine-consumed `regression_present: true` (SKILL.md:1374 forces the Tier-3 path). Merge action: point to the full table deviation-taxonomy.md:105-113; exit 1 counts as Regression only if tests were collected, ran, and an assertion failed; retry once for flakiness; if the two invocations disagree, G2 stays open. |
| INV-007 | count_divergence | `tasklist_completion_pct` 0.667 is consistent across sources | ADDRESSED | LOW | task-diff-map.yaml:34 = 0.667; contract `<float 0.0-1.0> \| null` (SKILL.md:1136); V2:64. Claimed 3/3 (completed.md:6-8) against 2/3 diff-backed is the false-completion signal. |
| INV-008 | count_divergence | Status is "forced by G1, G2" (V1:101) and the gap count is consistent | UNADDRESSED | LOW | deviation-taxonomy.md:149 forces on any non-empty file, i.e. 3 rows including G3. Merge action: say "forced by non-empty grounding_gaps (3 rows)". |
| INV-009 | count_divergence | "Executed coverage 0/3" uses the same denominator as completion | ADDRESSED | LOW | spec.md:6/9/12 (3 MUSTs) map one-to-one to completed.md:6-8 (task-diff-map.yaml:11-28). Nothing was executed (execution.log:5; task-diff-map.yaml:38). |
| INV-010 | count_divergence | Advocate tallies match the per-point table | ADDRESSED | LOW | Orchestrator notes in the transcript correct both advocate tally sentences; the R2 table sums to 12 + 3 + 2 = 17. |
| INV-011 | collection_boundaries | The "Drift needs an unmapped hunk" graft (deviation-taxonomy.md:62) can be written as the definition of Drift | UNADDRESSED | MEDIUM | :58 is the definition and :62 is one signal among :62/:65/:67/:109. Exit 5 (:109) lands on T-103 (`mapped_hunks: []`, task-diff-map.yaml:26). Merge action: reword to "with no verification run (task-diff-map.yaml:38) and `unmapped_hunks: []` (:29), none of the Drift signals at :62/:65/:67/:109 fire". |
| INV-012 | collection_boundaries | Empty collections are emitted unambiguously | UNADDRESSED | LOW | `findings: []`, `unmapped_hunks: []`. One hunk maps to two tasks. `deviation_count_by_class` is not stated (SKILL.md:1138-1142). G1-G3 are ordinal labels (the schema has no id field). Merge action (optional): state the zero counts per class; note that the labels are ordinal. |
| INV-013 | collection_boundaries | A single-function module has no siblings, so the correctness-gaps channel cannot apply | ADDRESSED | LOW | src/greeting.py:1-4 has one def; reuse-audit.yaml neighbours []; deviation-taxonomy.md:175. Resolved in C-001/X-002. |
| INV-014 | interaction_effects | V1's exit-code map and V2's conditional `src/__init__.py`/pythonpath remedy (V2:48) combine without conflict | UNADDRESSED | MEDIUM | A new marker or config file maps to no task (completed.md:6-8) or spec line, so it becomes an unmapped hunk and a Drift signal in the next audit (deviation-taxonomy.md:62). The V2 advocate conceded it is a product change the spec does not require. Merge action: prefer the invocation change (`python -m pytest` from the root); adding a file needs a recorded user decision or a tasklist amendment. |
| INV-015 | interaction_effects | The C-009 tie leaves a usable target for the regeneration recommendation | UNADDRESSED | MEDIUM | V2:43 bare `changes.patch` resolves under the frozen snapshot (V2:2). The audited diff is the audit-root changes.patch (task-diff-map.yaml:3). Merge action: target the audit-root absolute path and state that S is read-only. |
| INV-016 | interaction_effects | "Do not edit src/greeting.py until spec.md:9 is clarified" and V2's "align src/greeting.py:2" can both stay in the base | ADDRESSED | LOW | The C-007 tie settled the order (spec first). Merge action: reword V2:55-58 as spec clarification first, code and assertions only after. |
| INV-017 | sufficiency_challenge | (a) Regenerating changes.patch closes G1; (b) running both pytest invocations clears G2; (c) setting completed.md to partial fixes false completion; (d) V2 base + V1 grafts is correct and complete | UNADDRESSED | MEDIUM | Inline enumeration: S = spec.md(12 lines), completed.md(8), changes.patch(9, single src hunk), src/greeting.py(4), tests/test_greeting.py(13), execution.log(5), __run_evidence__/{t1-card.md, task-diff-map.yaml(38), git-inventory.txt(9), reuse-audit.yaml(27)}; audit root = same files + proposed.md + .git. Falsifiers: (a) same `--scope src/` reproduces G1 (task-diff-map.yaml:27), a tests-only intent-to-add drops H1, the frozen copy gets regenerated, or the map is not rebuilt; (b) the invocations disagree, pytest is missing (exit 1), or exit 5; a green G2 closes neither G1 nor G3; (c) completed.md:8 stays, and G3 still forces partial; (d) open INV-004/006/008/011/014/015, and `needs_human_decision: true` (deviation-taxonomy.md:152) is not stated in either verdict block. Merge action: present each claim as necessary but not sufficient, and add `needs_human_decision: true`. |

## Summary

- **Total findings**: 17 (all 6 categories covered: state_variables 3, guard_conditions 3, count_divergence 4, collection_boundaries 3, interaction_effects 3, sufficiency_challenge 1)
- **ADDRESSED**: 6 (INV-003, INV-007, INV-009, INV-010, INV-013, INV-016)
- **UNADDRESSED**: 11
  - HIGH: 1 (INV-006)
  - MEDIUM: 8 (INV-001, INV-002, INV-004, INV-005, INV-011, INV-014, INV-015, INV-017)
  - LOW: 2 (INV-008, INV-012)

## Invariant Probe Gate (orchestrator)

```
CONVERGENCE BLOCKED: 1 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-006
These invariant violations must be resolved before convergence can be declared.
Action: Address the flagged items in a subsequent debate round or acknowledge as accepted risk.
```

```
WARNING: 8 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-001, INV-002, INV-004, INV-005, INV-011, INV-014, INV-015, INV-017
These items do not block convergence but should be reviewed.
```

- Gate result: diff-point agreement 1.00 >= 0.80 and taxonomy covered (L1/L2/L3 all > 0), but 1 HIGH UNADDRESSED -> **BLOCKED_BY_INVARIANTS**.
- No subsequent debate round is available: Round 3 needs `--depth deep` (this run is `--depth standard`). The run is non-interactive, so no user acknowledgement of accepted risk was obtained. The orchestrator does NOT treat INV-006 as resolved.
- Continuation: per the error-handling matrix `no_convergence` row ("Force-select by score, document non-convergence, flag for user review"), the pipeline proceeds to Step 3 force-selection. The refactor plan carries the fault-finder's INV-006 merge action as a planned change, so the merged card does not propagate the defective verifier. INV-006 is still reported in `unaddressed_invariants` because the debate did not adjudicate it.
