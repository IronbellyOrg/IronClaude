# Base Selection (Step 3: hybrid scoring)

Scored by the orchestrating session. Quantitative layer: `scripts/quant.py` (stdlib, deterministic; run output below). Qualitative layer: two independent evaluator agents, forward order (`rounds/qual-pass-1-forward.md`, opus) and reverse order (`rounds/qual-pass-2-reverse.md`, sonnet), with per-criterion disagreements re-evaluated by the orchestrator. V1 = `variant-1-opus-architect.md`, V2 = `variant-2-sonnet-analyzer.md`, V3 = `variant-3-haiku-backend.md`. Variants are scored AS WRITTEN (before the debate).

## Quantitative Scoring (50% weight)

Command: `uv run --no-project python -I scripts/quant.py . --contradictions V1=2,V2=1,V3=1`. Required-item list (57 items): K1..K10, eight required section names, D01..D15, Q01..Q03, 21 interface or contract names. Contradictions fed to IC: V1 2 (the "unbound and flagged" rule against the owner's G2 sentence; "readers ignore unknown keys" against the loader), V2 1 (K14 against S15, X-003), V3 1 (package-canonical plan check against D12 and D15 R-2).

| Metric | Weight | V1 | V2 | V3 |
|---|---|---|---|---|
| RC requirement coverage | 0.30 | 0.982 (56 of 57; missing "preconditions" as a lower-case word, "Preconditions" present) | 0.965 (55 of 57; missing "rollback", "preconditions" lower-case) | 0.895 (51 of 57; missing Q02, "go entry", `held_incomplete`, `held_backlog`, "rollback", "preconditions") |
| IC internal consistency | 0.25 | 0.990 | 0.997 | 0.993 |
| SR specificity ratio | 0.15 | 1.000 (1,384 concrete, 0 vague) | 1.000 (1,987 concrete, 0 vague) | 1.000 (361 concrete, 0 vague) |
| DC dependency completeness | 0.15 | 0.916 (76 of 83 ids defined) | 0.897 (70 of 78) | 0.871 (27 of 31) |
| SC section coverage | 0.15 | 1.000 (8 H2) | 1.000 (8 H2) | 1.000 (8 H2) |
| **quant_score** | | **0.9797** | **0.9732** | **0.9472** |

Notes: SR saturates at 1.0 because no variant uses a vague-indicator word (appropriate, as needed, might, etc.); it does not separate them. RC is the main discriminator: V3 never names Q02, the go entry, `held_incomplete` or `held_backlog`. The script does not read meaning, only tokens.

## Qualitative Scoring (50% weight): 30-criterion additive binary rubric

Dimension subtotals after position-bias resolution (final), with the two raw passes beside them.

| Dimension (5 criteria) | V1 final (p1 / p2) | V2 final (p1 / p2) | V3 final (p1 / p2) |
|---|---|---|---|
| Completeness | 5 (4 / 5) | 4 (4 / 4) | 4 (4 / 5) |
| Correctness | 4 (5 / 4) | 3 (4 / 3) | 5 (5 / 5) |
| Structure | 5 (5 / 5) | 5 (5 / 5) | 5 (5 / 5) |
| Clarity | 4 (4 / 4) | 4 (4 / 4) | 3 (3 / 3) |
| Risk coverage | 3 (4 / 3) | 3 (4 / 3) | 4 (4 / 4) |
| Invariant and edge case | 4 (4 / 4) | 5 (5 / 5) | 5 (5 / 5) |
| **Total of 30** | **25** (26 / 25) | **24** (26 / 24) | **26** (26 / 27) |
| qual_score | 0.8333 | 0.8000 | 0.8667 |

Criteria lost in the final verdicts:
- V1 (5 lost): R3 (the label "K12" means "close after merge" in section 3 and "unprotected master" in RK-2 and OA-5), L4 (MR-2, C-INV-1, U54 undefined at first use), K1 (risk table has severity only, no likelihood), K2 (RK-3, RK-4, RK-8 list a test but no mitigation), I4 (no rule for which states count toward the cap or for duplicate counters).
- V2 (6 lost): C5 (no out-of-scope list), R3 (K12 and R9 each carry two meanings), R4 (K14 against S15; rows 4 and 22 cited but absent), L4, K1, K2 (R3, R7, R8, R11 give a test but no mitigation).
- V3 (4 lost): C1 (stages S6 to S8 and S10 name no files or PRs), L1 (owner actions telegraphic, "Cap 0: uncapped"), L4, K1.

### Edge Case Floor Check
Dimension I (invariant and edge case): V1 4 of 5, V2 5 of 5, V3 5 of 5. All three clear the floor (below 1 of 5 is ineligible). No suspension needed.

## Position-Bias Mitigation

Dual pass: forward order V1, V2, V3 (opus evaluator) and reverse order V3, V2, V1 (sonnet evaluator). Both evaluators spot-checked code citations (about 19 and 12 locations); none was a hallucination. Raw totals differ (26, 26, 26 against 25, 24, 27), a sign of the order effect and of the stricter second reader.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final (orchestrator re-evaluation, evidence) |
|---|---|---|---|---|---|
| C5 out of scope | V1 | NOT MET | MET | no | MET: V1 line 3 states "D16 has no VERDICT.md, so it is left out"; section 6 marks issue 409 DESIGN ONLY and issue 689 deferred; an explicit, if short, exclusion |
| R3 terminology | V1 | MET | NOT MET | no | NOT MET: V1 section 3 K12 "close after merge" against RK-2 "(K12)" for the unprotected-master risk of D05 |
| K2 mitigation per risk | V1 | MET | NOT MET | no | NOT MET: RK-3 "None fully proves it", RK-4 and RK-8 give only a test; the rubric says each risk |
| R3 terminology | V2 | MET | NOT MET | no | NOT MET: V2 K12 (session name) against "K12" as the D05 risk; "R9" is a risk row and a rule id |
| K2 mitigation per risk | V2 | MET | NOT MET | no | NOT MET: R3, R7, R8, R11 give a proving test only |
| C1 success criteria | V3 | NOT MET | MET | no | NOT MET: S6, S7, S8, S10 rows name no files or PRs, which the brief's "files or PRs" requirement asks for |

Disagreements found: 6 criterion-variant pairs of 90 (6.7 percent). Every final verdict equals one of the two passes (no verdict equals neither): 5 of the 6 equal pass 2 (V1 C5, R3, K2; V2 R3, K2), 1 equals pass 1 (V3 C1). So the re-evaluation changed the pass 1 verdict in 5 cases and the pass 2 verdict in 1 case (verdicts_changed = 6 of 6 disagreements resolved toward one side). The re-evaluation applied one rule: cite evidence in the variant text or the criterion is NOT MET.

## Combined Scoring

| Variant | quant (x0.50) | qual (x0.50) | Combined | Rank |
|---|---|---|---|---|
| V3 haiku:backend | 0.4736 | 0.4333 | **0.9069** | 1 |
| V1 opus:architect | 0.4898 | 0.4167 | **0.9065** | 2 |
| V2 sonnet:analyzer | 0.4866 | 0.4000 | **0.8866** | 3 |

Margin V3 over V1: 0.0004 (0.04 percent). Top two are within 5 percent: tiebreaker protocol applies.

### Tiebreaker
- Level 1, debate performance (points won in the Step 2 scoring matrix, sole or shared wins in `debate-transcript.md`): V3 5 (C-003, C-008, C-010, X-002, X-003), V1 4 (S-002, C-002, C-004 shared with V2, X-004 shared with V2). V3 leads: **tiebreaker applied, level 1**.
- Levels 2 and 3 not needed.

## Selected Base: Variant 3 (haiku:backend)

Selection rationale: V3 has the highest combined score by a hair and wins the level 1 tiebreaker. Its qualitative lead comes from correctness (5 of 5: no factual error, no internal contradiction, "K" labels disambiguated) and risk coverage (a safe-failure column per risk). Its quantitative score is the lowest of the three (it names fewer required items). The base is therefore a recovery and operations contract to be completed, not a finished document.

Strengths to preserve from the base (V3): at-least-once framing; save the claim attempt before launch; unknown receipt never relaunched; delivery intent saved with claim evidence, wake published from the saved intent, replay with the same wake id, retarget with a linked new id; ack only after the matching state exists; integrity rules (stable action id, exclusive create, temp plus rename, flush file and parent directory, reject symlinks and oversize JSON, lock order, producer releases its lock before delivery); a merge result that is uncertain is reconciled against the exact head before a go is reused, and a restart never restores a consumed go; real issues stay off until the worker binding is proved; a failure table with a required test per row; "narrows, not closes" wording; the D15 integrity conditions kept.

Strengths to incorporate from non-base variants (feeds `refactor-plan.md`):
- From V1: the end-state diagram with the owner's chat lane; machine state outside git in the per-repo state root and human records on the `coordinators` branch; the 22 owner questions with one line per answer; the `waiting_reapproval` state; `coordinator_autostart`; K11 to K15; the claim-by switch as the named reversal; the interface rows with a built column.
- From V2: the [B] [P] [C] [N] [D] tags; the ten mechanical merge checks MC-1..MC-10; the S6 revert dry run bound to a recorded master sha, the `git apply --check` of the planb patch, and the per-host diff rule; the early lane 3 (sweep fields and saved JSON); the evidence column of the built ledger; `coordinator_session` and `wake_enabled` keys; the rollback warning that a loader rejects unknown keys; the nuance that label creation is a person-run init write.
- From the debate: INV-001..INV-027 of the invariant probe as spec lines; the poll-claims-first rule with the named reversal; schema version 1 with a widened key list and a separate store migration; D15's order O0..O7 and "PR 686 stays one adapted draft".
