# Base Selection (Step 3): D05 position papers

Scope note: base selection scores the two papers as documents (completeness, correctness, structure, clarity, risk coverage, edge cases). It picks the base for the merged output. It does NOT decide the debate; the per-point outcomes in `debate-transcript.md` decide that, and the owner weighting rule is applied in VERDICT.md.

## Quantitative Scoring (50% weight)

Computed by `scripts/quant.py` (deterministic, run with `uv run python -I`). Requirements are the six elements the brief asks of a position paper (no formal requirement IDs exist, so section-level matching is used).

| Metric | Weight | Variant 1 (OURS) | Variant 2 (CLAY) | Computation |
|---|---|---|---|---|
| RC requirement coverage | 0.30 | 1.0000 | 1.0000 | 6 of 6 elements present; 9 cited facts, inside the 5 to 10 range, both |
| IC internal consistency | 0.25 | 0.8462 | 1.0000 | 1 - contradictions / claims; claims 13 each (9 facts + 4 mechanism items); contradictions: OURS 2 (X-001, X-003, both conceded in Round 2), CLAY 0 |
| SR specificity ratio | 0.15 | 1.0000 | 1.0000 | concrete 221 and 209, vague 0 and 0. Limit: the vague-word list never fires on these dense papers, so SR does not separate them |
| DC dependency completeness | 0.15 | 1.0000 | 1.0000 | 2 and 3 internal references, all resolve |
| SC section coverage | 0.15 | 1.0000 | 1.0000 | 6 H2 sections each |
| quant_score |  | 0.9615 | 1.0000 |  |

## Qualitative Scoring (50% weight): additive binary rubric

Two independent evaluators scored all 30 criteria with the Claim-Evidence-Verdict protocol. Every CEV row (verdict plus quoted evidence) is in `rounds/qual-pass-1.md` (input order: V1 then V2) and `rounds/qual-pass-2.md` (reverse order: V2 then V1). Those two files are the evidence tables and are not copied here (one governing source).

### Qualitative Summary (per dimension, order: Completeness, Correctness, Structure, Clarity, Risk Coverage, Invariant and Edge Case; computed by `scripts/qualcompare.py`)

| Variant | Pass 1 | Pass 2 | Final after re-evaluation |
|---|---|---|---|
| V1 OURS | [3, 3, 5, 4, 3, 4] = 22 | [3, 3, 5, 4, 2, 4] = 21 | [3, 3, 5, 4, 2, 4] = 21 of 30 (0.700) |
| V2 CLAY | [3, 5, 4, 4, 3, 4] = 23 | [4, 4, 5, 3, 3, 4] = 23 | [4, 4, 5, 3, 3, 4] = 23 of 30 (0.767) |

### Edge Case Floor Check

Invariant and Edge Case Coverage: V1 4 of 5, V2 4 of 5. Both clear the floor (at least 1 of 5); both are eligible as base.

## Position-Bias Mitigation

Dual pass: the two evaluators ran in parallel and independently (pass 2 was told not to read pass 1). Disagreements: 5 of 60 criterion-variant pairs; each was re-evaluated with both evidence cells side by side and the re-evaluation is final. Verdicts changed from one pass: 5 (each resolution equals one pass and differs from the other).

| Criterion | Variant | Pass 1 | Pass 2 | Final | Reason |
|---|---|---|---|---|---|
| Completeness 4 (success criteria) | V2 | NOT MET | MET | MET | Mechanism 2 names a failing test as the pass condition for "never launches through the claim" (K4, D:1226) |
| Correctness 1 (no factual errors) | V2 | MET | NOT MET | NOT MET | Cited fact 1 says DQ7 "adds no new exposure that the owner's own text did not already describe" and cites `issue-pipeline-guard-g2.md:9`, whose own clause says "Before any other issue ... must be bound"; the source contradicts the use. Also fact 2 counted OB-H1 item 8, later shown parked by the owner (conceded Round 2) |
| Structure 3 (separation of concerns) | V2 | NOT MET | MET | MET | Costs (exposure of the position) and Risks (open items of its controls) hold different content; the K22 overlap is minor |
| Clarity 1 (unambiguous language) | V2 | MET | NOT MET | NOT MET | The Claim says the risk is "left for the owner (decision OD1)" while fact 8 says OD1 is "Decided by ruling 3"; "owner" names two different people in the sources |
| Risk Coverage 3 (failure modes and recovery) | V1 | MET | NOT MET | NOT MET | The paper states failure behaviours (LL-BROKEN, fail-open) but no recovery path |

## Combined Scoring

| Variant | quant (x0.50) | qual (x0.50) | Final score |
|---|---|---|---|
| V1 OURS | 0.9615 x 0.5 = 0.4808 | 0.7000 x 0.5 = 0.3500 | 0.8308 |
| V2 CLAY | 1.0000 x 0.5 = 0.5000 | 0.7667 x 0.5 = 0.3833 | 0.8833 |

Margin: 0.0525 (5.25 points). The tiebreaker window is under 5 points, so no tiebreaker applies.

Sensitivity (stated, not hidden): the margin rests mainly on the IC input. IC counts the two conceded OURS-side tensions (X-001, X-003) and none for CLAY. If both were scored IC = 1.0, V1 would score 0.8500 against 0.8833, a margin of 3.3 points; the tiebreaker would then apply, and level 1 (diff points won in the debate: OURS C-001, C-007, C-009, X-002 against CLAY X-001, X-003) would pick Variant 1. So the base choice is close and does not say who won the debate.

## Selected Base: Variant 2 (CLAY, `variant-2-original.md`)

Selection rationale: the higher computed score (0.8833 against 0.8308), from fewer conceded internal tensions (quant IC) and two more qualitative criteria met (23 against 21), mainly Risk Coverage and Completeness. This is a document-quality result only.

Strengths to preserve from the base: the closed list of orchestrator-side controls with test hooks (`refuse(argv)`, head-pinned merge, audit AU1 to AU8: facts 3 and 7); the friction finding on `/sc:pr-submit` (fact 5); the plain statement that binding of a `worker-start` worker has never been observed (fact 6); the R33 observation that only `--pipeline none` launches (fact 3).

Strengths to incorporate from the non-base (Variant 1, OURS): the one-issue scope of the owner's G1 acceptance and the "before any other issue" clause (fact 2); level FS equals Clay's own OD1 policy and enforces its three prohibitions (Mechanism 3); that the audit cannot see a push with no pull request (fact 5); K22 and U42 as a session-scoped-hook precedent (fact 4); the live PASS evidence (fact 6); binding machinery still on master (fact 3); the live `protected: false` re-read.

Corrections the merge must apply (from the debate): `publish_pending` is at `orca_worktree.py:1488` and `cmd_pending` at `:1515`; the G2 collisions and the `.ok` release apply only to a plain worker held at level W, not at FS; first-prompt binding fails closed with LL-NOBIND when a marker arrives; "one marker line" is true of the hook and false of the whole job; "the owner (Clay)" in D:3 and D:1152 is the account `clayphi`, not the repository owner `ironbelly`; R33 gates only the watcher's claim launches.
