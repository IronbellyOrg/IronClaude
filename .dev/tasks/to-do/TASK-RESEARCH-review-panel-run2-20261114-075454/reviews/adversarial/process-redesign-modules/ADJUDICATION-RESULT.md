# Adjudication result: slot X-13 (process-redesign-modules; synth-06 name C-13; conflict rows CO-23, CO-24)

Run: `/sc:adversarial --compare proposal-a.md,proposal-b.md --depth standard --focus correctness,risk,test-coverage` (Mode A, no `--merge`, no `--interactive`). Orchestrated by the debate-orchestrator; advocates (Round 1 and Round 2), the invariant fault-finder, both scorers, the re-evaluation scorer, the plan reviewer and the merge-executor were separate agents.

## Winner

**Variant A (Proposal A, Sweep-Sheet-shaped) as the base, merged as the hybrid the debate itself produced.** The debate's own base selection (`base-selection.md`): "Selected Base: Variant A (Proposal A, Sweep-Sheet-shaped; `variant-1-original.md`)". The merged resolution is `merged-output.md`. Neither proposal won as written: after two rounds both advocates named the same winner on 28 of the 29 diff points (Variant A 5, Variant B 4, Hybrid 13, Neither 6, unresolved 1).

The hybrid, as the two Round 2 advocate files state it and `merged-output.md` records it:
- Built now, all optional for a module (with no cards declared the run equals today's run by hash): a card format with loader and validator (module data, no class constants, `requires_tools` and tool-keyed `search_forms`, no `extractor` field until one exists); a record-only reviewer row block `rows-v1` that is the source of `observed`; one entry point that writes `panel/coverage.json` and a separate advisory `panel/rowcheck.json` (`review-rowcheck/1`) so `review-precheck/1` and `reread_set` stay byte-identical; counts-only telemetry with a leak test; uniform per-module card binding; a card-to-tool lint (no shell for read-only reviewers).
- Reserved in the document only, nothing built, no schema key: slot-keyed binding (not named `recipes`), script extractors per class (C4 and C8 first) each behind its own offline gate, a `ran` cross-check via the C-08 transcript adapter, demotion and promotion (G-4 plus three prerequisites: per-row persistence across rounds, a merge hook, a v2 severity rewrite).
- Not built: demotion, promotion, overlay, profile value, CB-2 in the core, additive item-evidence flags in `precheck.json`, any change to findings v1 or v2, `review-ledger/1`, `derive_verdict`, reflect contract 1.8.0 or its 36-test matrix, reviewer-side shell, class constants.
- Placement of the row block: before the findings block in the v1 spec loop, after it in v2 (agreed in Round 2). Modules: spec loop v1 (cards plus row block, advisory rowcheck on `quote_plan` against the candidate); tasklist and workflow via reflect UC-1 v2; reflect default and UC-2 none; PR review and rf-qa reserved.

## Rationale (quoted from the debate's base selection and scores)

- Quantitative layer: A 0.9370, B 0.9516 (requirement coverage 1.0000 each; internal consistency A 0.8148, B 0.8065; specificity 1.0000 each; dependency completeness 1.0000 each; section coverage A 0.8889, B 1.0000).
- Qualitative layer (30 criteria, two position-bias passes, 7 of 60 pairs re-evaluated): A 24/30 = 0.8000, B 23/30 = 0.7667. Dimensions: Correctness A 2/5, B 0/5; Structure A 4/5, B 5/5; Completeness 5/5 each; Clarity 4/5 each; Risk Coverage 4/5 each; Invariant & Edge Case 5/5 each. Both variants meet the edge-case floor.
- Combined: A 0.8685, B 0.8591. "Margin: 0.94 percentage points ... below the 5% threshold." "Tiebreaker applied: Yes." Level 1 (debate performance): Variant A won 5 points against 4 for Variant B (3.4 percentage points apart, within 5%, so Level 2 was also applied); Level 2 (correctness criteria count): A 2, B 0. Both levels select Variant A.
- The debate's stated reason: Variant A leads on Correctness, where the debate verified fewer wrong statements about code in A than in B (B's own advocate conceded that no brief renderer exists in `cli/review`, that the `ledger.py:468` route lists the wrong set, that the `recipes` name collides with `cli/swarm/recipes/`, and that the sidecar key is the card stem and not `<slot_id>-<i>`). A won the points that decide the core of the conflict (no demotion or promotion in the core, X-002 at 95% and X-003 at 80%; CB-2 outside the core, C-010 and X-006; the model-free per-class gate, X-008, conditional). B won the carrier-side points (separate rowcheck file, C-004 at 90%; the rf-qa mark mapping, C-012; the evidence table and non-claims section, S-002 and S-003).
- Both layers are reported: the quantitative layer favoured B (driven by section coverage, 9 vs 8 H2 sections), the qualitative layer favoured A.
- Convergence: 28 of 29 diff points agreed (96.55%) against an 80% threshold (after Round 1: 17 of 29, 58.62%). Status BLOCKED_BY_INVARIANTS (see below). Taxonomy gate passed (L1 4 points, L2 15, L3 10, all covered).

## Conditions under which the winner holds (all stated in `merged-output.md`)

1. The base was selected by the tiebreaker, not by a clear score margin (0.94%); the two scoring layers disagreed.
2. The resolution is the hybrid of the two Round 2 advocate files, not Proposal A as written: Proposal A's additive item-evidence flags in `precheck.json` were withdrawn by A's advocate, and A's "existing mechanism" for an item with no finding was conceded as hollow.
3. Every gate and threshold stays a design choice that no recorded run can evaluate. The gates are ordered G-0 (code tests, no model, no harness), G-1 (per-class offline recall; needs ground truth and the X-14 pre-registration rule), G-2 (compliance spike), G-3 (arms Z0, K, RL, SS; RL must beat K by the pre-registered margin or K wins), G-4 (demotion safety). A-001 (a measurement harness, ground truth and pre-registration, slot X-14) is a precondition for every effect claim; D2 (0.12 x 14 = 1.68 items) exceeds both designs' own central estimates (+1.33 and +1.05 items) and is a pre-registration choice for the owner.
4. The rows give a hard consequence only for an empty findings block (`findings_v2.py:291-298`); one finding plus zero rows is valid, so the row block does not prove examination, and `ran` stays unverified until the C-08 adapter exists.
5. Quote exactness is measured by the advocates on recorded findings-v2 citations (31 of 313 quoted citations, 9.9 percent per quote; 18.8 percent for a two-quote row which assumes the failures are independent, while the advocate notes independence is low; 472 of 510 recorded flags are `not-in-snapshot`); transfer to row quotes is an assumption. Any future consequence of a failed row quote needs data on row quotes first; the check stays advisory.
6. The built-now set is dormant until a module declares cards and the prose wiring exists (INV-019); wiring of the v1 loop is gated on G-2 and G-3 per Variant B and is one prose edit per Variant A (D-5, open).
7. The v1 loop has no snapshot, sidecar, cluster or precheck step anywhere (verified by absence by both advocates); each such step is a new prose edit of a primitive, and the mirror pins on the loop prompt exist (IP INV-015).
8. Open and not resolved by the debate: S-004 (format of the consistency and invariant presentation); D-1 (does the row duty crowd out the free review), D-2 (do script-made items beat card-derived rows on C4 and C8), D-5 (is a row block worth wiring on the v1 loop), D-6 (does UNSURE count as observed), D-7 (editing reflect step 5 under the frozen contract); who computes `observed` (A's component 2 fills `assigned` only, B's also computes `observed`; both agree it must never be orchestrator-declared). D-3 and D-4 were closed by agreement.

## Invariants the debate left unaddressed

From `adversarial/invariant-probe.md` and the return contract: 20 findings, 4 ADDRESSED (INV-003, INV-012, INV-013, INV-018), 16 UNADDRESSED. Convergence was blocked by the two HIGH items; standard depth has no Round 3, so none was resolved.

| ID | Severity | Category | What is unaddressed |
|----|----------|----------|---------------------|
| INV-001 | HIGH | state_variables | `observed` is said to have one writer (the new entry point, from parsed rows), but `SKILL.md:345` still tells the orchestrator to write `panel/coverage.json` itself ("the rows its card reports"); the two Round 2 lists also disagree on whether the writer computes `observed`. |
| INV-019 | HIGH | sufficiency_challenge | The built-now set alone cannot make process-catchable defects get examined: no module declares cards before G-2 and G-3, no brief renderer exists, `_SLOT_KEYS` stays closed, so only prose edits reach a reviewer; compliance, row grammar, consequence and reader are not shown. |
| INV-002 | MEDIUM | state_variables | In reflect the file the entry point would parse is the orchestrator-assembled `panel/cards/reviewer-<N>.md`; a model-made verbatim copy can drop, merge or invent a row; a fourth reviewer-id space (`-card` stem) exists. |
| INV-004 | MEDIUM | state_variables | Step 4 parses the card (and decides the one re-ask and the first-pass compliance rate) before the sidecar is written at step 6; a compliant clean reviewer can be judged invalid. |
| INV-005 | MEDIUM | state_variables | The entry point writes fixed paths with no round or review-kind argument; a re-run overwrites round 1 evidence and assigns rows to a re-review reviewer. |
| INV-006 | MEDIUM | guard_conditions | No row-id grammar or type rule; recorded ids include slugs, a `/`, a range token; a non-string id aborts a whole command. |
| INV-007 | MEDIUM | guard_conditions | The check rules need a path and a quote kind that no row field carries; `ran` has no bound; unknown row keys unspecified. |
| INV-009 | MEDIUM | count_divergence | `assigned`, `observed`, `rows_total`, the module row cap and the 12 of E2 are inconsistent: 21 of 69 recorded entries exceed 12 assigned rows (max 48); uniform binding multiplies rows by reviewer count. |
| INV-010 | MEDIUM | count_divergence | Row quote boundaries disagree: the 12-character minimum vs C4/C8 short literals; whole-candidate test vs the line-window basis of the measured failure rates; `quote_other` short quotes silently unchecked. |
| INV-011 | MEDIUM | count_divergence | The consensus does not state that compliance feeds quorum arithmetic only through the empty-block rule; paths differ by engine (v1 truncation of the findings block behind a longer row block; v2 invalid clean reviewers drop out of `complete_reviewers`). |
| INV-014 | MEDIUM | collection_boundaries | What `assigned` holds per card, what the loader does with a bad card, and the rule for duplicate row ids are unspecified. |
| INV-015 | MEDIUM | interaction_effects | The v1 loop edit is the rules file plus its plugin byte copy, not `commands/spec-panel.md`; the pinned "last section" sentence and insertion order constrain a row block before the findings block. |
| INV-016 | MEDIUM | interaction_effects | In shadow mode the card body still reaches the legacy debate; the manifest freezes the sha256 of `refs/reviewer-spec.md` as a policy input; the order of a row block against the `reviewer_model_self_report` line is unstated. |
| INV-017 | MEDIUM | interaction_effects | `review-telemetry/1` reviewer records are closed; new counters fit only in `context` or a new schema version; the leak test is trivially true if the counters go nowhere. |
| INV-020 | MEDIUM | sufficiency_challenge | Advisory checks are safe but need a reader and a route to the fix: the v1 merge report prints ledger rows only; the v2 host is opt-in shadow mode that feeds nothing; `rows_missing` and the PROBLEM-without-finding list have no named reader. |
| INV-008 | LOW | guard_conditions | UNSURE counts as observed, so an all-UNSURE clean report passes the guard (open as D-6). |

ADDRESSED: INV-003 (HIGH; three reviewer-id spaces and the id map), INV-012 (LOW; line bases, deferred with extractors reserved), INV-013 (MEDIUM; zero cards and the `{}` entry), INV-018 (LOW; non-interference with the C-01, C-02, C-03 outcomes; residual path is truncation, INV-011).

Return contract `unaddressed_invariants` (HIGH only): INV-001, INV-019.

## Return contract

Status `partial`; convergence score 0.9655 (28 of 29); base variant `variant-1 (Proposal A; default model, default persona)`; unresolved conflicts 1 (S-004); fallback mode false; failure stage null; invocation method `task-agent`.

## Artifact paths

Output folder: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/process-redesign-modules/`

- Merged file: `.../process-redesign-modules/merged-output.md`
- Artifacts folder `.../process-redesign-modules/adversarial/`:
  - `variant-1-original.md`, `variant-2-original.md` (variant copies)
  - `diff-analysis.md`
  - `debate-transcript.md` (with `round1-advocate-A.md`, `round1-advocate-B.md`, `round2-advocate-A.md`, `round2-advocate-B.md`)
  - `invariant-probe.md` (with `round2.5-fault-finder-raw.md`)
  - `base-selection.md` (with `score-pass1.md`, `score-pass2.md`, `score-reeval.md`, `quant-score.py`, `quant-score-output.json`)
  - `refactor-plan.md` (with `plan-review.md`)
  - `merge-log.md`
  - `return-contract.yaml`
