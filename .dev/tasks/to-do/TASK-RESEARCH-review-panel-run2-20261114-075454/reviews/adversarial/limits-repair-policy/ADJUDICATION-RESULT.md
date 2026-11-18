# Adjudication result: slot C-06 (limits-repair-policy)

Run: `/sc:adversarial --compare proposal-a.md,proposal-b.md --depth standard --focus correctness,risk,test-coverage` (Mode A, no `--merge`, no `--interactive`). Orchestrated by the debate-orchestrator; the diff analyst, both advocates (Round 1 and Round 2), the invariant fault-finder, both scorers, the re-evaluator, the plan reviewer and the merge-executor were separate agents.

## Winner

**Hybrid, with Variant B (Proposal B) as the base.** The debate's own base selection (`base-selection.md`): "Selected Base: Variant B (Proposal B; `variant-2-original.md`)". The merged resolution is `merged-output.md`: Proposal B's itemised drop record with a `blocking_state`, its dropped-blocking refusal with an acknowledgement exit and its pre-registered measurements, with Proposal A's cut of the three location fields (`anchor`, `anchor2`, citation `quote`) to 200 flattened characters in code behind a `repair=False` keyword, A's derived first-pass state carrier, A's stateless re-ask with a refusal-driven v1 transport, and A's cost-side re-merge and kill lines added. Neither proposal won as written: after two rounds both advocates' final tables name the same winner on 24 of 28 points (Variant 1: 2, Variant 2: 3, Hybrid: 15, Neither: 4), and four points are unresolved (below).

## Rationale (quoted from the debate's base selection and scores)

- Quantitative layer (`quant-score.py`, run twice with identical output): A 0.9598, B 0.9948 (requirement coverage 1.0000 each; internal consistency A 0.9725, B 0.9792; specificity 1.0000 each; dependency completeness 1.0000 each; section coverage A 0.7778, B 1.0000).
- Qualitative layer (30 criteria, two position-bias passes, 4 of 60 pairs re-evaluated): A 22/30 = 0.7333, B 27/30 = 0.9000. Dimensions: Completeness A 4/5, B 5/5; Correctness A 1/5, B 3/5; Structure A 4/5, B 5/5; Clarity 4/5 each; Risk Coverage A 4/5, B 5/5; Invariant & Edge Case 5/5 each (both clear the floor).
- Combined: A 0.8466, B 0.9474. "Margin: 10.08 percentage points ... above the 5% threshold." "Tiebreaker applied: No."
- The debate's stated reasons: B scores higher on Completeness (A declines the fail-closed rule and never evaluates raising the limits), Correctness, Structure (A's lone `### 4.1`) and Risk Coverage. A's Correctness losses are the manifest claim ("`manifest.py:371-372` raises `OutOfOrder` before the `complete` test"), "exact prefix" against the 297-plus-`...` claim cut, and "touches no field the limits do not name" against the copy-to-`refs` rule. B's Correctness losses are "5 of 5" against its own E3 row, "none of the 42 merges where a blocking row survived" against its own no-survivor rows, and the four-versus-five pin count.
- The debate's caveat: "the two proposals are not what the debate converged on", so the base needs a substantial merge from A, which the refactoring plan (16 changes) and the merge executed (16 of 16 applied, post-merge validation PASS).
- Convergence: 24 of 28 diff points agreed (85.7%) against an 80% threshold. Status BLOCKED_BY_INVARIANTS (see unaddressed invariants below). Both advocates moved toward the same hybrid between Round 1 and Round 2; no oscillation.

## Unresolved conflicts (the debate did not settle them; the merged text states both positions)

| Points | Position A | Position B |
|---|---|---|
| C-001 (claim part) and C-009: is the claim cut | Cut to 297 plus `...` with a marker, a "shortened from N" row note and `original_sha256`, kept unless K2 fails (more than 20 percent of blocking claims judged to lose a decision-relevant clause) | No claim cut by default (no verdict or floor outcome on P273 needs it; a claim limit of 450 reproduces cut-all; claim meaning unmeasured); allowed only if K2 passes |
| C-002: which eligibility rule decides clearing and quorum | `ok`/`complete` stays the parser verdict on the repaired lines; C-03 may count only `repaired == 0` blocks for its floor (default off) | Derived eligibility: tolerates dropped `blocking: false` lines, fails on block-level faults or unresolved `true`/`unknown` drops; no `repaired == 0` knob |
| C-012: provenance of a stored member that is not a byte copy | Derived copy with `original_sha256` plus the existing `report_sha256` | Same mechanism for a cut anchor (a flattened-form substring); the byte-copy objection applies only to a claim cut |

## Conditions under which the winner holds (all stated in `merged-output.md`)

1. The cut of the three location fields rests on replays on single-line tasklist rows: 70 of 70 and 89 of 89 over-limit `anchor`/`anchor2` fields that occur verbatim keep a unique same-span prefix. The `quote` cut has no location measurement; no multi-line or PR-code corpus exists; kill line K1 drops to 75 percent for such a corpus. M1 and M2 are not yet run.
2. The policy depends on the C-02 and C-03 `block_ok` semantics (A-004): today's bare `ok` puts 10 of 273 merges (P273) or at least 7 of 264 (audit-D, three-reviewer panels only) below the C-03 floor; which eligibility rule applies is C-002 above.
3. The `SKILL.md:343` sentence is reflect-only and pinned; the text adds one sentence and needs the owner to confirm that package code is not "the orchestrator". If it is, the v2 call sites stay at `repair=False` and the v1 `merge` keeps the cut.
4. The dropped-blocking refusal is insurance: it fires on 3 of 264 merges without the cut and 0 with it (0 of 264 derived from `flags.tsv` reason text; 0 of 273 executed on P273). In v1 a lost blocking line is never recovered in a merge that succeeds with another blocking row standing (36 of 39 on P273).
5. Re-ask recovery is unmeasured on gateway models: E1 shows four confirmed re-asks of five (Agent path, one length cause). In v1 the re-ask is driven by a refusal because no pre-merge command exists; in reflect it is recorded before the `collected` commit for a non-`complete` earlier attempt.
6. The audit-D and P273 populations differ (264/92/49/80 against 273/90/46/79) and are adequate for ordering the policies but not for a recovery percentage; reviewer behaviour is not stationary (the decided CO-8 brief change alters the claim rate).
7. The shadow-mode safety argument holds only while shadow lasts; leaving shadow requires `first_pass_state` to be carried and the exit script re-checked.
8. The raise-the-limits lever is a claim-only raise to 450, a separate owner decision that widens the findings-v1 grammar (INV-C); anchors are never raised.
9. The kill lines K1-K5 and the pre-registered measurements are proposals; the owner may change the numbers before the first run.

## Invariants the debate left unaddressed

From `adversarial/invariant-probe.md` and the return contract: 26 findings, 6 ADDRESSED, 20 UNADDRESSED (HIGH 4, MEDIUM 12, LOW 4). Convergence was blocked by the four HIGH items; standard depth has no Round 3, so none was resolved. All 20 are listed in `merged-output.md` section 10.3 and are not closed by it.

| ID | Severity | Category | What is unaddressed |
|----|----------|----------|---------------------|
| INV-001 | HIGH | state_variables | The dropped-blocking refusal sees only the current round's drops; a blocking line lost in a FAIL round can be forgotten when a later round passes (no cross-round list of unresolved dropped lines). |
| INV-017 | HIGH | interaction_effects | A 200-character prefix can locate at more than one place while the full anchor locates once; `annotate` takes the first and `anchor_ambiguous` is read nowhere, so a new blocking defect can be matched to a deferred row and pass with nothing dropped (shown by the probe on a synthetic two-row document). |
| INV-018 | HIGH | interaction_effects | In reflect, `cluster_cmd` and `verify_cmd` run at step 6, after the `collected` commit of steps 3-4, so the re-ask, the attempt-2 record and the first-pass carrier cannot be driven as written. |
| INV-023 | HIGH | sufficiency_challenge | Cut plus itemise plus refusal does not alone close the PASS-by-loss defect and the v2 loss unit: a forgotten cross-round drop (INV-001), a prefix absorbed by a deferred row (INV-017) and a truncated block (INV-025) each falsify it. |
| INV-002 | MEDIUM | state_variables | The manifest `completion` value is a third first-pass carrier that the text does not name. |
| INV-003 | MEDIUM | state_variables | A refused v1 merge records nothing, so the refusal-driven re-ask leaves no ledger trace and K4/K5 are not measurable live. |
| INV-005 | MEDIUM | guard_conditions | `blocking_state` from the line's own `blocking` flag is untrusted (CRITICAL with `blocking: false` is accepted by both checkers). |
| INV-006 | MEDIUM | guard_conditions | The acknowledgement is not bound to the dropped item ids or hashes. |
| INV-007 | MEDIUM | guard_conditions | A dropped `prior` line (a lost veto) has no stated `blocking_state`. |
| INV-008 | MEDIUM | guard_conditions | Both checkers return the first fault only; a line with two faults is dropped again after the single re-ask and "residual by rule" undercounts. |
| INV-010 | MEDIUM | count_divergence | A cut can invent a reference token (`FR-12` cut to `FR-1`) and change `refs_norm`, `fp` and `same_defect`. |
| INV-016 | MEDIUM | collection_boundaries | A rescued line whose prefix does not locate becomes a kept row with no span that no fix can touch (same defect as C-01 INV-015). |
| INV-019 | MEDIUM | interaction_effects | The unchanged Normalize text and the additive sentence use "invalid" for two different states. |
| INV-024 | MEDIUM | sufficiency_challenge | The cut removes the v2 loss unit only for the length share. |
| INV-025 | MEDIUM | sufficiency_challenge | A truncated block loses its tail with no line to itemise; truncation stays outside the guard. |
| INV-026 | MEDIUM | sufficiency_challenge | After the cut the refusal fires on 0 of 264, so K5 passes trivially and the code path is not exercised. |
| INV-004 | LOW | state_variables | Additive keys carry no parser or policy version; `block_ok` changes meaning. |
| INV-011 | LOW | count_divergence | `original_chars`, `kept_chars` and `repaired_lines_rate` have no single unit. |
| INV-020 | LOW | interaction_effects | Two refusals can occur in sequence (quorum, then `dropped_blocking`, both exit 12) and record nothing. |
| INV-022 | LOW | interaction_effects | `card_convert.py` has its own claim cut; two implementations if a claim cut is adopted. |

Return contract `unaddressed_invariants` (HIGH only): INV-001, INV-017, INV-018, INV-023.

## Return contract

Status `partial`; convergence score 0.8571 (24 of 28); base variant `variant-2 (Proposal B; default model, default persona)`; unresolved conflicts 4 (C-001 claim part, C-002, C-009, C-012); fallback mode false; failure stage null; invocation method `task-agent`.

## Artifact paths

Output folder: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/limits-repair-policy/`

- Merged file: `.../limits-repair-policy/merged-output.md`
- Artifacts folder `.../limits-repair-policy/adversarial/`:
  - `variant-1-original.md`, `variant-2-original.md` (variant copies)
  - `diff-analysis.md`
  - `debate-transcript.md` (with `round1-advocate-A.md`, `round1-advocate-B.md`, `round2-advocate-A.md`, `round2-advocate-B.md`)
  - `invariant-probe.md` (with `round2.5-fault-finder-raw.md`)
  - `base-selection.md` (with `score-pass1.md`, `score-pass2.md`, `score-reeval.md`, `quant-score.py`, `quant-score-output.json`)
  - `refactor-plan.md` (with the independent review `plan-review.md`)
  - `merge-log.md`
  - `return-contract.yaml`
