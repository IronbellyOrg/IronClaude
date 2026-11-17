# Adjudication result: slot X-15 (tasklist-medium-and-fidelity-vocab; synth-06 name C-15)

Run: `/sc:adversarial --compare proposal-a.md,proposal-b.md --depth standard --focus correctness,risk,test-coverage` (Mode A, no `--merge`, no `--interactive`). Orchestrated by the debate-orchestrator; the diff analyst, advocates, fault-finder, scorers and merge-executor were separate agents. Conflict: does the tasklist module treat Medium as blocking, and does the fidelity prompt become a module vocabulary under the core (conflict ids SV-6, CO-41, C-S3 tasklist default).

## Winner

**Variant B (Proposal B) as the base, merged as the hybrid the debate itself produced.** The debate's own base selection (`base-selection.md`): "Selected Base: Variant B (Proposal B; default model, default persona)". The merged resolution is `merged-output.md`: Proposal B's structure (module-data label map, nothing new in the core, fidelity prompt, gate, frontmatter and exit code left in `cli/tasklist/` outside the core, no pinned sentence edited) with Proposal A's Stage 7 grading block by consequence, dedup-highest and "grade higher when torn" rules, containment/parity test, static tests and measurements.

Neither proposal won as written. After two rounds the advocates agreed on 32 of 37 diff points. The question the slot names, whether the skill's Medium blocks (point C-001), is one of the five points the debate scored Unresolved (50%): Advocate B's final position (H+) keeps Medium blocking as a redefined second blocking class, with Advocate A's version (A+, Medium a non-blocking warning) only by a registered upgrade rule; Advocate A's final position (A+) is "adoption gated on measurement, fallback to H". The debate did not choose between them; `merged-output.md` section 10 records both final terms.

## Rationale (quoted from the debate's base selection and scores)

- Quantitative layer: A 0.9943, B 0.9328 (requirement coverage A 1.0000, B 0.9167; internal consistency A 0.9773, B 0.9677; specificity 1.0000 each; dependency completeness A 1.0000, B 0.9722; section coverage A 1.0000, B 0.8000).
- Qualitative layer (30 criteria, two position-bias passes, 7 of 60 pairs re-evaluated): A 25/30 = 0.8333, B 24/30 = 0.8000. Dimensions: Completeness 5/5 each; Correctness A 3/5, B 4/5; Structure A 5/5, B 4/5; Clarity A 4/5, B 3/5; Risk Coverage 3/5 each; Invariant & Edge Case 5/5 each.
- Combined: A 0.9138, B 0.8664. "Margin: 4.74% (below the 5% threshold)". "Tiebreaker applied: Yes, level 1 (debate performance): Variant B won 12 diff points in the Step 2 scoring matrix against 4 for Variant A."
- Both layers are reported: the quantitative layer and the qualitative layer both favoured Variant A by small margins; the debate-performance tiebreaker favours Variant B.
- The debate's stated reason: on the points that carry correctness and risk weight Advocate A conceded in Round 1 or Round 2: the union mitigation does not exist at Stage 7 (one grader per task slice, SK:1351-1368), Form 2 (a parse-edge severity table) is code the adjudicated shape excludes, the role-table claim is a design intention, the "one product" wording was loose, the S5 reading was wider than written, and A's edit list missed `commands/tasklist.md:113`. Variant B's losses were the S4 premise (B conceded the skill states no model before B's own edit), its line ranges, and an overstated reading of the archived reports.
- Convergence: 32 of 37 diff points agreed (86.5%) against an 80% threshold. Status BLOCKED_BY_INVARIANTS (see unaddressed invariants below).
- Matrix tally: Variant A 4 points, Variant B 12, Hybrid 6, Neither 4, Unresolved 5 (C-001, C-007, C-012, C-013, C-014).

## Conditions under which the winner holds (all stated in `merged-output.md`)

1. The choice between H+ and A+ rests on measurements that have not been run (F1: blind grade of the six archived Medium findings; F2: seeded defects under both blocks; F3: Stage 7 run twice, flip rate at both boundaries). Every threshold is a design choice, not evidence. Advocate B's rule: a measurement not run, or a threshold not met, leaves H+ in place; Advocate A's rule: if all pass adopt A+, if any fails adopt H. Invariant findings INV-017 and INV-020 contest that H+ is a neutral resting point.
2. The basis is the consequence test of `pragmatic.md:225` and `:231` applied by analogy. It is not S4 (the skill states no severity model today) and not S5 as written (it names no High/Medium/Low scale).
3. The shared core gets nothing: no `Medium` token, no new field, no parse-edge hook. The label map is module data (Form 1 only). This holds while C-01 (no core change, unknown keys open), C-02 (typed `blocking` stays the authority, CRITICAL floor) and C-03 (per-profile policy) stand; the debate states that if one is reopened this slot is reopened with it.
4. The fidelity prompt stays outside the core while no core code consumes the vocabulary (Stage 7 findings are prose today) and no module-declared role table exists. The only named later seam is a read-only adapter from a finished deviation report.
5. The only data about what the skill's Medium finds is two archived reports (six findings, one reader; both bundles report High 0). Reviewer compliance with a grading block is unmeasured.
6. The C-02 CRITICAL floor covers High (CRITICAL) and not Medium (MAJOR); under H+ a reviewer typing MAJOR with `blocking: false` drops the row (INV-016 residue of C-02, INV-003 here).
7. Under H+ the skill and the CLI disagree on one class (a criterion dropped or weakened: blocking in the skill, CLI MEDIUM at `prompts.py:62`); removing that divergence needs the PR:62 edit, which is an owner decision with its own unrun measurement.
8. Pin inventory: the pinned phrase "the unresolved High or Medium HALT resolves as blocked" lives in `src/superclaude/commands/tasklist.md:113`, read by `tests/skills/test_worker_contract.py:777` and `:1861`; H+ touches none of the 12 sweep rows, CMD:113 or the two pins, A+ rewrites all of them.

## Invariants the debate left unaddressed

From `adversarial/invariant-probe.md` and the return contract: 20 findings, 3 ADDRESSED (INV-006, INV-015, INV-016), 17 UNADDRESSED. Convergence was blocked by the two HIGH items; standard depth has no Round 3, so none was resolved.

| ID | Severity | Category | What is unaddressed |
|----|----------|----------|---------------------|
| INV-017 | HIGH | sufficiency_challenge | "Nothing loosens before measurement, so H+ is behaviour-preserving" does not hold: H+'s block lands immediately and routes its Low class (insufficient detail, ambiguity, estimate, equivalent method, formatting, wording) away from SK:1439, :1537, :1571, :1608 and :1614, which count Medium today; a real omission described as "insufficient detail" can be graded Low, and FC(H+) is measured only after the block lands. |
| INV-018 | HIGH | sufficiency_challenge | "Grading block + tie-break-up + dedup-highest makes the boundary safe" does not hold: SK:1608 re-runs the full Stage 7 set with fresh agents and `F_k`, SK:1610 and SK:1611 compare separate samples; dedup (SK:1410) acts inside one run on disjoint slices, so it cannot reduce between-sample variance; the only evidence is F3 on 2 samples. |
| INV-001 | MEDIUM | state_variables | `ValidationReport.md` is written once from the first Stage 7 merge; a Medium or Low first seen at a re-run is listed nowhere. |
| INV-003 | MEDIUM | guard_conditions | No CRITICAL floor exists in code yet and it covers CRITICAL only; H+ puts the dropped-criterion class in unprotected MAJOR; Stage 7 findings are prose, so a map pinned "as data" is read by nothing. |
| INV-004 | MEDIUM | guard_conditions | SK:1410 leaves "the same issue on the same task" to the model; keep-highest may drop the entry whose `Exact fix` covers the defect. |
| INV-005 | MEDIUM | guard_conditions | The containment test T2(a) and (b) cannot pass as written; a static test catches deleted phrases, not changed meaning. |
| INV-007 | MEDIUM | count_divergence | `F_k` counts post-dedup findings while the loop works on task ids; a re-grade can lower `|F_k|` with no patch; the loop gives up to 3 samples and F3 compares 2. |
| INV-008 | MEDIUM | count_divergence | SK:1703, :1705, :1716, :1766 and the totals line SK:1462 state severities, are in neither edit list and are unpinned. |
| INV-010 | MEDIUM | collection_boundaries | (A+ only) the clean template has a slot for Low notes only; a Medium-only bundle's report is unspecified. |
| INV-011 | MEDIUM | collection_boundaries | F1 to F3 rest on two archived bundles and per-finding thresholds; no threshold fixes bundles, repeats or unit. |
| INV-013 | MEDIUM | interaction_effects | Tie-break-up enlarges the blocking set; a Low-graded PASS item re-graded Medium trips the regression halt; a `blocked` retry re-samples the graders. |
| INV-014 | MEDIUM | interaction_effects | H+ keeps SK:1421-1422 MEDIUM while the adopted block calls omissions High; A+ regrades them High but the CLI keeps missing TDD coverage MEDIUM. |
| INV-019 | MEDIUM | sufficiency_challenge | Eleven filters sit between a Stage 7 finding and the verdict; seven are "not shown" until measured or specified. |
| INV-020 | MEDIUM | sufficiency_challenge | F1 cannot fail H+ by construction and cannot test the High/Medium line (both archived bundles have High 0); no registered outcome withdraws the Low class. |
| INV-002 | LOW | state_variables | The byte-equal fixture guard skips when the plan copy is absent, does not assert the 12-row group; an insertion after SK:1391 shifts every SK line cite. |
| INV-009 | LOW | count_divergence | The "76 lines in 10 files" against "88 lines in 14 files" count is unreconciled. |
| INV-012 | LOW | collection_boundaries | A one-task phase has one grader, so dedup and tie-break-up cannot act. |

Return contract `unaddressed_invariants` (HIGH only): INV-017, INV-018.

## Return contract

Status `partial`; convergence score 0.86 (32 of 37 = 0.8649); base variant `variant-2 (Proposal B; default model, default persona)`; unresolved conflicts 5 (C-001, C-007, C-012, C-013, C-014); fallback mode false; failure stage null; invocation method `task-agent`.

## Artifact paths

Output folder: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/tasklist-medium-and-fidelity-vocab/`

- Merged file: `.../tasklist-medium-and-fidelity-vocab/merged-output.md`
- Artifacts folder `.../tasklist-medium-and-fidelity-vocab/adversarial/`:
  - `variant-1-original.md`, `variant-2-original.md` (variant copies)
  - `diff-analysis.md`
  - `debate-transcript.md` (with `round1-advocate-A.md`, `round1-advocate-B.md`, `round2-advocate-A.md`, `round2-advocate-B.md`)
  - `invariant-probe.md` (with `round2.5-fault-finder-raw.md`)
  - `base-selection.md` (with `score-pass1.md`, `score-pass2.md`, `score-reeval.md`, `quant-score.py`, `quant-score-output.json`)
  - `refactor-plan.md`
  - `merge-log.md`
  - `return-contract.yaml`
