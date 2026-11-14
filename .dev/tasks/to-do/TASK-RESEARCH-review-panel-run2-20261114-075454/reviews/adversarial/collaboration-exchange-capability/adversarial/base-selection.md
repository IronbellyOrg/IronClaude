# Base Selection Report (slot C-12, collaboration-exchange-capability)

Variant A = Proposal A (`variant-1-original.md`), Variant B = Proposal B (`variant-2-original.md`). Scoring passes: `scoring-pass1.md` (input order A, B), `scoring-pass2.md` (reverse order B, A), `scoring-reeval.md` (re-evaluation of the 8 disagreements). The variants are scored as written; the debate is used only as evidence of which claims are right or wrong (no Round 2 concession is credited to a variant whose original text lacks it).

## Quantitative Scoring (50% weight)

Quantitative metrics were computed independently by both passes with the stated counting methods. The table gives the mean of the two passes (per-metric values of each pass are in the scoring files); the passes differ by less than 0.01 on the total.

| Metric | Weight | Variant A (Proposal A) | Variant B (Proposal B) |
|--------|--------|------------------------|------------------------|
| requirement_coverage | 0.30 | 1.0000 (15/15 in both passes) | 0.9333 (14/15 in both passes; act-rate range, item 11, absent) |
| internal_consistency | 0.25 | 0.9610 (pass 1: 1 - 3/79; pass 2: 1 - 3/75) | 0.9712 (pass 1: 1 - 2/71; pass 2: 1 - 2/68) |
| specificity_ratio | 0.15 | 0.9560 (pass 1: 76/79; pass 2: 38/40) | 0.9609 (pass 1: 69/71; pass 2: 38/40) |
| dependency_completeness | 0.15 | 0.9283 (pass 1: 20/22; pass 2: 18/19) | 0.8826 (pass 1: 16/19; pass 2: 12/13) |
| section_coverage | 0.15 | 1.0000 (9 H2 / 9) | 1.0000 (9 H2 / 9) |
| **quant_score** | | **0.9729** (pass 1 0.9712, pass 2 0.9746) | **0.9493** (pass 1 0.9450, pass 2 0.9536) |

Contradictions counted (both passes agree on the count): A 3 (4.2 "no exchange arm has a matching control row" vs its 4.3 counted rows; 3.3 "H1 reaches reflect through the reflect brief, no call-site change" vs sections 2 and 5 "no change to cli/reflect"; 6.4 brief bytes equal today's vs 3.1 item 1 H1 ships unconditionally). B 2 (2.2 "registered in hooks.json" vs 2.2/2.4 baked `--settings` and "off emits no --settings"; 1 "cost is zero by construction" vs 2.2 "one installed hook script").

## Qualitative Scoring (50% weight) - Additive Binary Rubric

Final verdicts: where both passes agreed, the agreed verdict; for the 8 disagreements, the re-evaluator's final verdict. Evidence is condensed from the passes (full CEV text in `scoring-pass1.md` / `scoring-pass2.md` / `scoring-reeval.md`). MET = 1, NOT MET = 0.

### Completeness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| Covers all explicit requirements | MET | RC 15/15 | NOT MET | RC 14/15: no act-rate figures anywhere in 3 or 6 |
| Addresses edge cases/failures | MET | 4.3 `k` 0, E9 hang guard, section 5 mitigations | MET | 6.4 fault injection, 3.F `k` 0 and late delivery, 5 untrusted anchor |
| Dependencies/prerequisites | MET | section 2 dependency column, 3.1 item 2 served-model check | MET | 2.3 C-07, 4 C-08, 8 concession |
| Success/completion criteria | MET | 6.1 wrong-if/right-if rule, 6.4-6.6 | MET | 6.1, 6.2, 6.7 "fewer than half of the cells" |
| Out-of-scope | MET | 3.2 "does not build now" | MET | 1 boundary (F4/F7 out), 2.5-2.7 |
| **Subtotal** | **5/5** | | **4/5** | |

### Correctness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| No factual errors | NOT MET | 4.4 `--resume` "not evidenced" stale at pinned tip (X-002); 8 "about 150 ms" overstated (X-004); 4.2 overstated | NOT MET | 2.2 "registered in hooks.json" wrong (X-006); 1 "zero cost by construction" falsified (A-002) |
| Feasible with stated constraints | NOT MET | 3.3 H1 via reflect brief with "no call-site change" (`ensemble.py:601-630`, INV-005); H2 re-ask inside pure `parse_block` (INV-009) | MET (re-eval, bar: whole-design reading) | one coherent adapter path in 2.3-2.4; the hooks.json phrase is a stray resolved by 2.2/2.4; C-07 dependency disclosed |
| Terminology consistent | MET (re-eval) | "Unconditional" defined in 1; "matching control" read with 6.1/8(3) | MET (re-eval) | exchange/switch/off state/kinds one referent each; "H1/H2" undefined is a Clarity matter |
| No internal contradictions | NOT MET | IC found 3 | NOT MET | IC found 2 |
| Claims supported by evidence | MET | 4.1 table E1-E12 with tags | MET | 3.A-3.F file:line with tags |
| **Subtotal** | **2/5** | | **3/5** | |

### Structure (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| Logical ordering | MET | sections 0-8 | MET | sections 0-8 (the brief's own order) |
| Consistent hierarchy | MET | H3 only under 3 and 4 | MET | H3 A-F only under 3 |
| Separation of concerns | MET | evidence 4, invariants 5, tests 6 | MET | 3.F isolates [POST-BASELINE] |
| Navigation aids | MET | "see 3.4", E-rows, measurement numbers | MET | "(section 3.D)", lettered A-F |
| Artifact conventions | MET | all 8 brief elements | MET | all 8 brief elements |
| **Subtotal** | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| Unambiguous language | MET (re-eval) | no unlabelled hedge in a rule; 6.2 cap value deferred to a named owner | MET (re-eval) | hedges labelled [UNVERIFIED]; rules determinate (2.4, 6.1, 6.5, 6.7) |
| Concrete, not abstract | MET | `kit: on|off`, file:line, n >= 4 | MET | files:lines, 600-byte cap, 0.1 s |
| Section purpose | MET | each H2 opens with its purpose | MET | each H2 opens with its purpose |
| Terms defined on first use | MET | H1-H4 in 1; minor gap "A1" | NOT MET | "H1/H2", "EL2/HL2", "k", "S0/S2" never defined |
| Actionable next steps | MET | 6.1-6.7, 7 "What would change this" | MET | 6.1-6.8, 8 concession shrink path |
| **Subtotal** | **5/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| At least 3 risks with probability and impact | NOT MET (re-eval) | only INV-G and cost carry both impact and likelihood: 2, not 3 | NOT MET (re-eval) | time budget and wasted spend carry both: 2, not 3 |
| Mitigation for each risk | MET | lint, `kit: off` for reflect, verify-sync coverage, cost gate | NOT MET | Bash-launcher risk passed to C-07; untrusted text "not closed" |
| Failure modes and recovery | MET | 8 answer (5), 3.2 retrofit path | MET | fault injection, seal fails closed, concession fallback |
| External dependencies | MET | section 2 residue, 4.4 runtime facts | MET | C-07, C-08, session-persistence pins, 3.B |
| Monitoring/validation | MET | 6.4, 6.5, 6.2 per-module cost record | MET | 6.5 p95, 6.8 alarms, `collab` record |
| **Subtotal** | **4/5** | | **3/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| Collection boundaries | MET | anchor 200 / claim 300 limits, n = 2 vs 4 | MET | 600-byte cap, anchor 12-200, parallel calls |
| State across boundaries | MET | `origin` means three things; sidecar vs in-line | MET | 2.5 in-line key dropped before ledger, sidecar |
| Guard condition gaps | MET | non-`off` value refused; lint; r2 `agent_id` | MET | r2 no `agent_id` branch; forbidden verdict keys |
| Count divergence | MET | test counts 103,163,89,90,82 vs 138,358,89,106,108 | MET (re-eval) | `/lib/` counts 0 vs 3/7/11, 36 `def test_` vs parametrize |
| Interaction effects | MET | peer finding not an independent vote; C-03 quorum | MET | exchange vs C-02 quorum; persistence vs pins |
| **Subtotal** | **5/5** | | **5/5** | |

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 5/5 | 4/5 |
| Correctness | 2/5 | 3/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 5/5 | 4/5 |
| Risk Coverage | 4/5 | 3/5 |
| Invariant & Edge Case | 5/5 | 5/5 |
| **qual_score** | **26/30 = 0.8667** | **24/30 = 0.8000** |

### Edge Case Floor Check
Variant A 5/5 (eligible); Variant B 5/5 (eligible, after the re-evaluation of B Invariant 4; pass 2 alone had 4/5, still above the floor).

## Position-Bias Mitigation

Per-criterion string, final (order: Completeness 1-5, Correctness 1-5, Structure 1-5, Clarity 1-5, Risk 1-5, Invariant 1-5):
A pass 1 `MMMMMNNMNMMMMMMMMMMMMMMMMMMMMM`, pass 2 `MMMMMNNNNMMMMMMNMMMMNMMMMMMMMM`. B pass 1 `NMMMMNNNNMMMMMMMMMNMMNMMMMMMMM`, pass 2 `NMMMMNMMNMMMMMMNMMNMNNMMMMMMNM`.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Correctness 3 (terminology) | A | MET | NOT MET | DISAGREE | MET |
| Clarity 1 (unambiguous) | A | MET | NOT MET | DISAGREE | MET |
| Risk 1 (3 risks, prob. and impact) | A | MET | NOT MET | DISAGREE | NOT MET |
| Correctness 2 (feasible) | B | NOT MET | MET | DISAGREE | MET |
| Correctness 3 (terminology) | B | NOT MET | MET | DISAGREE | MET |
| Clarity 1 (unambiguous) | B | MET | NOT MET | DISAGREE | MET |
| Risk 1 (3 risks, prob. and impact) | B | MET | NOT MET | DISAGREE | NOT MET |
| Invariant 4 (count divergence) | B | MET | NOT MET | DISAGREE | MET |

Disagreements re-evaluated: 8 of 60 criterion-variant pairs (A 3, B 5). Final verdicts equal pass 1 in 4 pairs and pass 2 in 4 pairs. The re-evaluator applied one stated bar per criterion to both variants (`scoring-reeval.md`, "Standards applied"). Sensitivity: pass 1 alone gives margin 7.97% (A leads), pass 2 alone 4.38% (A leads); both passes and the re-evaluation put A ahead.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (Proposal A) | 0.4865 | 0.4333 | **0.9198** | 12 points won of 25 (48%) |
| B (Proposal B) | 0.4747 | 0.4000 | **0.8747** | 5 points won of 25 (20%) |

**Margin**: 4.51% (below the 5% threshold).
**Tiebreaker applied**: Yes.
- Level 1 (debate performance, Step 2 scoring matrix): Variant A won 12 diff points, Variant B 5 (Merge 2, Tie 2, Unresolved 1). The gap is 28 percentage points, not within 5%, so level 1 decides: Variant A.
- For the record, level 2 (correctness criteria MET) would have favoured Variant B (3 vs 2); it is not reached.

## Selected Base: Variant A (Proposal A)

### Selection Rationale
Variant A has the higher combined score (0.9198 vs 0.8747) and wins the tiebreaker on debate performance (12 vs 5 points). Its lead comes from requirement coverage (15/15 vs 14/15), completeness, clarity (terms defined) and risk mitigation coverage; Variant B scores higher on correctness (3 vs 2 criteria MET) and internal consistency. The debate's own conclusion is that the evidence does not support building the exchange transport now (no launcher at HEAD: `review-tiers.default.json:25-29` `"launch": {}`; no `--settings` in `src/superclaude/**/*.py`; no family with a clean measured success), which is Variant A's position; Advocate B conceded the build-now question in Round 2. The debate also showed that the right answer is a staged form of Variant A (a trigger with owner and expiry, and B's design as binding preconditions), not Variant A unchanged: Variant A's gate was ownerless and conflated building the measuring instrument with enabling the capability.

### Strengths to Preserve from Base
1. H1 (driving documents by role, path, sha256), H2 (one repair step), H3 (per-module snapshot base), H4 principle; catalogue as one data source per module.
2. `kit: on|off` per profile with a per-module cost gate (C-003, A 73%); kit defaults `off` until measurement 2 and 7 pass (Advocate A Round 2 position).
3. Core builds no hook script, adapter, board, validator code or `collab` record now (X-001, C-001, C-004).
4. A's tests: brief lint for read-only lanes, kit cost per panel at n >= 4, catalogue hold-out of >= 4 unseen defects, one common act-rate probe, off-state equality, existing pins.

### Strengths to Incorporate from Non-Base Variants
1. From Variant B, section 2.1 and 5 (C-010, B 79%): the `panel-msg/1` validator table (forbidden keys, 600-byte cap, located-anchor rule, harness-authored kinds only) and the untrusted-anchor channel analysis, as a binding design note that must be satisfied before `exchange: off` is lifted (not as code).
2. From Variant B, section 2.5 (C-006): a mandatory harness-written sidecar for the peer-origin tag, key not named `origin`, quorum counts over own-origin lines only.
3. From Variant B, section 6 tests 4 and 6 (C-007): fault injection (seal fails closed, review fails open) and the single-copy hook replay with an `agent_id` call and two parallel calls, plus the adversarial-anchor test both advocates added; as specifications.
4. From Variant B, section 3.A (X-005): the single-correct-copy requirement list (`agent_id` skip, timed lock, seal before first delivery) and the package name `exchange/` because `.gitignore:13` is `lib/`.
5. From Variant B, section 8 concession (U-013): the shrink path if slot C-07 yields no launcher.
6. From both advocates' Round 2 (debate product, not in either variant): the staged build trigger (C-07 adjudicated to a launcher with persistence and a per-session activation channel named by capability; X-14 metric and C-08 served-model record; named owner with expiry and the state "unmeasured, not rejected") and the enable trigger (pre-registered two-sided gain-and-cost rule against A2 on module-matched ground truth with hold-out >= 4 and a power calculation).
7. Corrections to the base required by the debate: X-002 (`--resume` on gateway ids is recorded at the pinned tip), X-004 (57 to 85 ms fits 0.1 s, small sample), 4.2 wording "no matching A2 control", and the stricter off-state test (no new file under `~/.claude/hooks/`, no hooks.json or merged-settings diff, no new run-record key, named installed-file-set diff).
