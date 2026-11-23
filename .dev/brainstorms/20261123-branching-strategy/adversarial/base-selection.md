# Base Selection Report

## Metadata

- Step: /sc:adversarial Step 3 (hybrid scoring and base selection), reconciliation of two independent passes.
- Written: 2026-11-23, by the reconciler. Folder: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261123-branching-strategy/adversarial/`.
- Inputs read in full: `scoring-pass-1.md` (input order V1, V2, V3, V4), `scoring-pass-2.md` (reverse order V4, V3, V2, V1), `debate-transcript.md` (Metadata, Round 2 design and positions of advocates 1 and 4, Scoring Matrix, Convergence Assessment), `invariant-probe.md`, `diff-analysis.md`, the four variants `variant-1-original.md` to `variant-4-original.md`, `../CONTEXT.md`, `~/.claude/skills/sc-adversarial-protocol/SKILL.md` (Step 3) and `refs/scoring-protocol.md`, `refs/artifact-templates.md` (Section 3).
- Variants: V1 = release line with story branches, local merges (owner's model); V2 = trunk on `integration`, dark landing; V3 = release train, PR-gated batch; V4 = GFxAI approach adapted.
- Convention: "CEV" = Claim (the rubric criterion applied to the variant), Evidence (quote or section), Verdict (MET = 1, NOT MET = 0). No partial credit; a MET without citable evidence is NOT MET. No em dashes; hyphens only.
- Read-only checks run by the reconciler on the four variant files: H2 and H3 counts, a grep for the protocol's vague-term list (0 hits in all four), a grep for "upstream" and "SuperClaude-Org" (0 hits in all four), a count of "Proposal N" cross-document references, and a re-read of the V4 lines behind the two V4 contradictions. No git or GitHub action was taken.

## Quantitative Scoring (50% weight)

### Final metric values (trusted values; the passes' own values are shown for comparison)

| Metric | Weight | V1 | V2 | V3 | V4 |
|--------|--------|----|----|----|----|
| requirement_coverage (RC) | 0.30 | 0.9565 (22/23) [P1 0.9091, P2 0.8261] | 0.9130 (21/23) [P1 0.9091, P2 0.8696] | 0.9130 (21/23) [P1 0.9091, P2 0.8696] | 0.8696 (20/23) [P1 0.9091, P2 0.8696] |
| internal_consistency (IC) | 0.25 | 1.0000 (0 contradictions) [P1 1.0, P2 1.0] | 1.0000 [P1 1.0, P2 1.0] | 1.0000 [P1 1.0, P2 1.0] | 0.9666 (2 contradictions) [P1 0.9767 on 86 claims, P2 0.9565 on 46 claims; average] |
| specificity_ratio (SR) | 0.15 | 1.0000 (0 vague hits) | 1.0000 (0 vague hits) | 1.0000 (0 vague hits) | 1.0000 (0 vague hits) |
| dependency_completeness (DC) | 0.15 | 1.0000 (11/11 internal refs) | 1.0000 (3/3) | 1.0000 (6/6) | 1.0000 (3/3) |
| section_coverage (SC) | 0.15 | 0.8889 (8 of 9 H2) | 0.8889 (8 of 9) | 1.0000 (9 of 9) | 0.3333 (3 of 9) |
| **quant_score** | | **0.9703** | **0.9572** | **0.9739** | **0.8525** |

Passes' own quant_scores for reference: P1 V1 0.9561, V2 0.9561, V3 0.9727, V4 0.8669; P2 V1 0.9312, V2 0.9442, V3 0.9609, V4 0.8500. Straight average of the two passes: V1 0.9437, V2 0.9502, V3 0.9668, V4 0.8585. The ranking by quant differs only in V1 versus V2 (see the RC note); V3 is first and V4 last under every variant of the count.

### Which count is trusted, metric by metric

**RC (the metric the passes disagreed on most).** CONTEXT.md has no formal requirement IDs, so the protocol's edge case applies (topic matching). P1 used 22 items and P2 used 23, with different judgements on the same facts, so averaging two lists that are not the same list is not meaningful. I rebuilt one list of 23 and applied one rule to all four variants: an item is matched when the variant states a rule, a mechanism, or a disclosed departure that addresses it; silence is N; quality is left to the qualitative layer. The 23 items are the nine questions (Q1 to Q9; all four variants answer each with a concrete rule, so 9 of 9 for everyone) and 14 facts: F1 ref-name conflict; F2 Orca `ironbelly/` prefix; F3 conflict is stopped and reported, never resolved automatically; F4 two parallel stories, disjoint paths, serial merges; F5 `/sc:pr-submit` is the only PR path, never rewrites a published branch, takes `--base`; F6 CI only for PRs into `master` and `integration`; F7 owner merges every PR; F8 `worker-start` has no `--branch`, exact names need `orca worktree create --branch`; F9 no commit on `master`, never touch the upstream repository; F10a `.dev/` records on the release branch; F10b ledger on the release branch; F10c planning of release n+1 starts from `master`; F11 release numbers are dashboard numbers, not package versions; F12 AI-speed volume as a design driver. F1, F2, F4 to F7 and F10a are Y for all four. The rows that differ or were contested:

| Item | V1 | V2 | V3 | V4 | Why (the contested ones) |
|------|----|----|----|----|--------------------------|
| F3 | Y | Y | Y | Y | One of the two judgement calls P1 flagged. V2 (P1 said N): Q2 says "The coordinator never merges in this model, so it never has to stop on a conflict; it assigns the fix to the worker". That is a reasoned departure that keeps the worker-contract rule intact (the coordinator never resolves a conflict), so Y under the stated rule. |
| F8 | Y | Y | N | Y | The other judgement call. V3 (P1 N, P2 N): sec 2 only says "If Orca adds `ironbelly/` in front when `--branch` is given" and step 2 says "Orca worktree from the train tip"; it never gives the `orca worktree create --branch` command or says `worker-start` lacks `--branch`. A conditional mention is not a mechanism. N stands. |
| F9 | N | N | N | N | Grep: 0 hits for "upstream" and "SuperClaude-Org" in all four. A variant that never mentions the upstream rule does not violate it, but does not state it either; identical for all four, so it moves the level, not the order. |
| F10b | Y | Y | Y | N | V2 states its relation to the ledger (Q7 "a real mismatch"; a disclosed departure). V4 says "recorded in the ledger" (rule 7) but never says where the ledger lives. P2 gave V4 a Y; P1 scored the same gap as NOT MET in Completeness 1. N. |
| F10c | Y | N | Y | N | V1 step 1 cuts the line from `master` and puts the planning `.dev/` records on it, which implements "planning starts from master" (P2 said N because the sentence about release n+1 is not written). V3 states the change to `integration` (Y, disclosed). V2 and V4 are silent. |
| F11 | Y | Y | Y | Y | All four use a tag marker in its own namespace (`dash/1.3` or `dash-1.3`) and treat 1.1 and 1.105 as dashboard releases; only V4 writes "the package is 6.1.0". P1 scored all Y, P2 only V4. Under the stated rule (a mechanism counts) all Y. |
| F12 | Y | Y | Y | Y | V1 risk 3 "AI stories are fast, human review of the final PR is not"; V2 sec 5 cites the 15 to 60 PR bursts; V3 Q3 "at AI speed"; V4 Q5 "at AI speed: UNSPECIFIED". Only V2 cites the figure. |
| Matched | 22 | 21 | 21 | 20 | of 23 |

Sensitivity of RC to a stricter reading (an explicit statement is required for F10c, F11 and F12; this is close to P2's list): V1 falls to 19/23 = 0.8261, V2 and V3 to 20/23 = 0.8696, V4 to 19/23 = 0.8261. Quant would then be V1 0.9312, V2 0.9442, V3 0.9609, V4 0.8395, so V1 would drop below V2 and V3 on the quantitative layer. Combined with the final qualitative scores below, V1 would still lead V3 (0.9156 against 0.9138, a 0.0018 margin, so the debate tiebreaker would decide, exactly as it does in the main result). Every flipped RC item moves a quant_score by 0.013.

**IC.** Contradictions are the same in both passes (V4: 2, others: 0). I re-read the two V4 contradictions in `variant-4-original.md`: (1) line 37 "Not through `integration`" and Q8 "a dashboard release does not pass through it" against line 32 "merge, never rebase, `master` and `integration` into `release/dash1.3`" and Q8 "`integration` is merged into `release/dash1.3` before the release pull request" (confirmed by the scratch test in the debate, X-003 and A-017); (2) line 36 "CI and the two reviewers run once, at that point" against Q2 "By pull request from the story branch into `release/dash1.3`, with the tests for that level and at least one review" and line 66 "add `release/**` to its pull-request branch list" (X-008). Both stand. The claim denominators differ because both are regex proxies (P1: sentence count 86, an upper bound that includes non-claims; P2: concrete non-vague units 46, closer to the protocol's "specific, falsifiable" but it drops claims without a digit, backticked token or named entity). The truth lies between, so I use the average of the two V4 values (0.9666). The gap between the two extremes is 0.0202 on V4's IC and 0.005 on its quant. Disclosed clashes with a CONTEXT fact (V2 ledger "does not fit", V3 Open decision A) are not counted: IC is "within the same variant", and both are penalised under Correctness 2 and Completeness instead. Sensitivity if they were counted: V2 IC 0.9915, V3 IC 0.9921, quant lower by about 0.002.

**SR.** Both passes: 1.0000 for all four. Confirmed: my grep of the protocol's vague list (appropriate, as needed, properly, adequate, should consider, might, various, etc., best practices, industry standard) returns 0 hits in each variant. The metric is degenerate: it cannot separate anything. P1's soft-hedge sensitivity (probably, may, could, roughly, ...) gives 0.9912, 0.9776, 0.9835, 0.9936; applying it would lower quant by 0.0013, 0.0034, 0.0025, 0.0010 and change no ranking. Not applied, because the protocol fixes the lexicon.

**DC.** Both passes: 1.0000 for all four. The protocol says "External references (URLs, other documents) are EXCLUDED". A "Proposal N" mention points to another variant file, so it is excluded. My count of "Proposal N" strings (title included): V1 2, V2 1, V3 11, V4 1, which matches P2's excluded cross-document counts (V3 10, V1 1, V2 0, V4 0) once the titles are removed. I follow the protocol, with the caveat that this exclusion is worth 0.094 of quant to V3 (DC 6 of 16 = 0.375 if counted, quant 0.8802) and 0.0125 to V1 (DC 11 of 12, quant 0.9578). V3 is the variant written most as a member of a set. See "Risk to the Selection".

**SC.** Same in both passes and re-counted by me (`grep -c '^## '`): V1 8, V2 8, V3 9, V4 3 (plus 9 H3 that hold V4's nine answers). Following the protocol (H2 only), V4's 0.3333 is a formatting choice, not missing content; counting H3 would give V4 SC 1.0 and quant 0.9525, which would still leave V4 last in combined score (0.8096).

### What the quantitative layer can and cannot say

It separates V4 from the rest (SC and IC) and nothing else with confidence. V1, V2 and V3 sit within 0.0167 of each other (0.9572 to 0.9739); RC, IC, SR and DC are tied or near-tied, and the only real separator among them is one extra H2 heading in V3. One flipped RC item moves a variant by 0.013, which is most of that spread. The decision between V1, V2 and V3 therefore rests on the qualitative layer and the debate, not on this table.

## Qualitative Scoring (50% weight) - Additive Binary Rubric

Final verdicts after reconciliation (M = MET, N = NOT MET). Rows where P1 and P2 agreed carry the evidence both passes cited (full CEV text in `scoring-pass-1.md` section 2 and `scoring-pass-2.md` section 2). The 15 rows where they disagreed were re-evaluated by the reconciler against the variant text; their CEV lines are in "Position-Bias Mitigation" below and marked (R) here.

### Completeness (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | Evidence basis |
|-----------|----|----|----|----|----------------|
| C1 Covers all explicit requirements | M (R) | M (R) | M (R) | N | V1 to V3 answer Q1 to Q9 and satisfy or openly disclose the ledger and planning-base facts. V4 never states the release branch base, the ledger home or the planning base. |
| C2 Edge cases and failure scenarios | M | M | M | M | Q9 in each: V1 `git revert -m 1`, V2 revert one squash commit or flag off, V3 three-layer revert, V4 revert the squash commit. |
| C3 Dependencies and prerequisites | M | M | M | M | V1 Q2(b) foundation story; V2 shared files in a first slice; V3 sec 5 `test.yml` edit; V4 closing "what this proposal needs". |
| C4 Success and completion criteria | M | M | M | M | V1 step 3 "settled"; V2 step 5; V3 sec 1 departure; V4 rule 4 and rule 7. |
| C5 Explicit out of scope | N (R) | N (R) | N (R) | N (R) | No variant has a scope-exclusion statement; "Flags are not used", "stacks not assumed", "UNSPECIFIED" are design choices or deferred decisions. |
| **Subtotal** | **4/5** | **4/5** | **4/5** | **3/5** | |

### Correctness (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | Evidence basis |
|-----------|----|----|----|----|----------------|
| K1 No factual errors | M | M | M | M | Ref-conflict rule matches CONTEXT line 8; V1 sort claim holds ("/" 0x2F sorts before "0" 0x30); CI scope claims match CONTEXT line 11. GFxAI and S-ID figures were not independently re-checked by either pass or by me. |
| K2 Feasible with stated constraints | M | N | M (R) | N | V1 needs no change to CI, settings or standing rules. V2 itself says the ledger convention "does not fit" with no fallback that keeps it. V3's dependencies are owner decisions with a stated fallback inside the constraints. V4 has two incompatible CI statements and no fallback. |
| K3 Terminology consistent | M | M | M | M | Defined terms reused unchanged in each. |
| K4 No internal contradictions | M | M | M | N | V4 only: the `integration` path and when CI runs (re-read by me, see IC note above). |
| K5 Claims supported | M | M | M | M | S-ID citations or GFxAI "FROM PRACTICE" marks with reasons. |
| **Subtotal** | **5/5** | **4/5** | **5/5** | **3/5** | |

### Structure (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | Evidence basis |
|-----------|----|----|----|----|----------------|
| S1 Logical ordering | M | M | M | M | Names before flow before questions (V1 to V3); V4 follows the question order. |
| S2 Consistent hierarchy | M | M | M | M | 8, 8, 9 H2 with no H3; V4 3 H2 plus 9 H3 under one H2. |
| S3 Separation of concerns | M | M | M | M | Costs, beneficiaries, risks in separate sections (V4: source versus adaptation marks). |
| S4 Navigation aids | M | M | M | M | "(section 4, Q2)", "See section 2", "(question 3)". |
| S5 Artifact-type conventions | M | M | M | N | V4 has no costs, beneficiaries, risks or sources section, no diagram, no step list (diff S-003, S-005). |
| **Subtotal** | **5/5** | **5/5** | **5/5** | **4/5** | |

### Clarity (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | Evidence basis |
|-----------|----|----|----|----|----------------|
| L1 Unambiguous language | M | M | M | M | 0 hits for the protocol lexicon in all four (my grep). |
| L2 Concrete | M | M | M | M | Exact commands and patterns: V1 `orca worktree create --branch dash1.3/s04-... --base-branch dash1.3/release`, V2 `--base integration`, V3 `--base train/dash1.3`, V4 `dash1.3/story/01-widget-grid`. |
| L3 Clear purpose per section | M | M | M | M | Section titles state purpose. |
| L4 Terms defined on first use | M (R) | M (R) | M (R) | N | V1 defines "settled", "foundation story", "leaf"; V2 "dark", "slice"; V3 "train", "sync branch". V4 imports "Tier 1 + Tier 2 + Tier 3", "UAT sign-off", "Interface-First design", "Tech-Lead emergency override" undefined. "CI" is used undefined by all four (shared project vocabulary). |
| L5 Actionable next steps | M | M | M | M | V1 steps 1 to 6; V2 Q5 first test; V3 Open decisions A to C; V4 closing needs list. |
| **Subtotal** | **5/5** | **5/5** | **5/5** | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | Evidence basis |
|-----------|----|----|----|----|----------------|
| R1 At least 3 risks with probability and impact | N | N | N | N | V1 to V3 list six risks each with no probability or impact rating; V4 has no risk section. Same reading in both passes. |
| R2 Mitigation for each risk | N | N | N | N | Each of V1 to V3 leaves at least two listed risks unmitigated (V1 risks 4 and 6; V2 risks 1, 3, 4; V3 risks 2, 3, 4, 6). |
| R3 Failure modes and recovery | M | M | M | M | Q9 in each. |
| R4 External dependencies and failure | M | M | M | M | V1 Orca prefix risk 4; V2 `integration` red, merge queue plan; V3 CI filter risk 5, bot behaviour risk 6; V4 `--branch` UNVERIFIED, `test.yml` trigger (thinner). |
| R5 Monitoring or validation | M | M | M | M | V1 `git merge-tree` trial and local suite; V2 CI on every slice; V3 per-story CI and bots; V4 test tiers and beta freeze. |
| **Subtotal** | **3/5** | **3/5** | **3/5** | **3/5** | |

### Invariant and Edge Case Coverage (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | Evidence basis |
|-----------|----|----|----|----|----------------|
| E1 Collection boundaries (empty, single, maximum) | M | N (R) | M | N (R) | V1 Q6 one-story release skips the line, Q4 split if open over a week; V3 Q6 "no train branch for a batch of one", Q5 time box. V2 and V4 describe size concern but state no rule or trigger at a boundary. |
| E2 State interactions across component boundaries | M | M | M | M (R) | V1 Q3 merge `master` in, never `integration`; V2 sync PR after promotion; V3 merge-in and sync branch; V4 rule 3 "never mid-merge". V4's `integration` error is charged once, under K2 and K4. |
| E3 Guard condition gaps | M | M | M | M | V1 trial merge before touching the tip; V2 "base is another slice's branch gets no CI"; V3 risk 5 "no CI while everyone assumes they have it"; V4 rule 2 clash with `/sc:pr-submit`. |
| E4 Count divergence | M | N | N | N (R) | Only V1 names a real divergence: "a future `1.10` would sort wrongly" (1.1 is a prefix of 1.105). Zero-padding (`s01` to `s99`, V2, V3, V4) is a sort convention, not a divergence scenario. |
| E5 Interaction effects | M | M | M | M | V1 Q3 Clay's unreleased work carried into `master`; V2 Q4 promotion carries Clay's work; V3 risk 3; V4 rule 2 rebase-only versus pr-submit. |
| **Subtotal** | **5/5** | **3/5** | **4/5** | **3/5** | |

### Qualitative Summary

| Dimension | V1 | V2 | V3 | V4 |
|-----------|----|----|----|----|
| Completeness | 4 | 4 | 4 | 3 |
| Correctness | 5 | 4 | 5 | 3 |
| Structure | 5 | 5 | 5 | 4 |
| Clarity | 5 | 5 | 5 | 4 |
| Risk Coverage | 3 | 3 | 3 | 3 |
| Invariant and Edge Case | 5 | 3 | 4 | 3 |
| **Total met / 30** | **27** | **24** | **26** | **20** |
| **qual_score** | **0.9000** | **0.8000** | **0.8667** | **0.6667** |

(P1 totals 26, 24, 25, 21; P2 totals 27, 24, 25, 21.)

### Edge Case Floor Check

| Variant | Invariant and Edge Case score | Eligible as base |
|---------|-------------------------------|------------------|
| V1 | 5/5 | Yes |
| V2 | 3/5 | Yes |
| V3 | 4/5 | Yes |
| V4 | 3/5 | Yes |

No variant is below 1/5, so the floor excludes nobody and no suspension warning is needed.

## Position-Bias Mitigation

Comparison of 120 criterion-variant pairs (30 criteria x 4 variants). Passes agreed on 105 pairs and disagreed on 15. Each disagreement was re-evaluated once by the reconciler against the variant text, with one rule applied to all four variants (so a criterion cannot be read loosely for one variant and strictly for another). The re-evaluation verdict is final.

- Disagreements found: 15 (V1 3, V2 4, V3 4, V4 4).
- Final verdict equals pass 1 on 10 rows and pass 2 on 5 rows. Rows changed relative to pass 1: 5. Rows changed relative to pass 2: 10. Rows that match neither: 0 (verdicts are binary).
- Net effect on met totals: V1 26 / 27 (P1 / P2) to 27; V2 24 / 24 to 24; V3 25 / 25 to 26; V4 21 / 21 to 20.
- Pattern check: V3 gains on three rows and V4 loses on three, so I checked that each of those rows follows a rule that is also applied to V1, V2 and the other variants (stated per row). V1 moves by the same kind of rows as V3 (C1, C5, L4).

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | CEV for the re-evaluation |
|-----------|---------|--------|--------|-----------|-------|---------------------------|
| C1 Covers all explicit requirements | V1 | M | N | DISAGREE | **M** | Rule: all nine questions answered with a concrete rule, and every CONTEXT fact the design touches is satisfied or disclosed with a path. Evidence: Q1 to Q9 in sec 4; ledger and `.dev/` on the release branch (Q7); line cut from `master` (step 1). P2 applied "RC must equal 1.0", which no variant meets because none states F9; that makes the criterion a constant. |
| C1 | V2 | M | N | DISAGREE | **M** | Same rule. Q1 to Q9 answered; ledger conflict disclosed (Q7 "a real mismatch ... biggest process cost"). |
| C1 | V3 | M | N | DISAGREE | **M** | Same rule. Q1 to Q9 answered; planning-base change disclosed (Q8), `test.yml` edit and merge authority disclosed (sec 5, Open decisions A and C). |
| C5 Out of scope | V1 | N | M | DISAGREE | **N** | Rule: a statement of what the document does not cover. Evidence offered by P2: "Flags are not used", "`integration`: not merged into the release branch" are design decisions, scored under Completeness 2 and Correctness. No scope statement found in sec 1, 5, 7. |
| C5 | V2 | N | M | DISAGREE | **N** | "so this proposal does not depend on it" (merge queue) and "Dependent slices are not stacked" are design choices. |
| C5 | V3 | N | M | DISAGREE | **N** | "unfinished work is 'not in the train'" and "stacked pull requests feature is not assumed" are design choices; Open decisions A to C are deferred decisions, not exclusions. |
| C5 | V4 | N | M | DISAGREE | **N** | "UNSPECIFIED = the source has no answer and I add none" marks gaps in the source, not limits of this proposal's scope. Same rule as the other three. Moves all four equally. |
| K2 Feasible with stated constraints | V3 | M | N | DISAGREE | **M** | Rule: no part of the design is impossible under CONTEXT as written, and every dependency on a changed rule or setting is an owner decision with a fallback that stays inside the constraints. Evidence: Open decision A "No: use Proposal 1 or accept the owner as the merge lane"; Open decision C (edit `test.yml` or not; without the edit, story PRs get no CI, which V3 risk 5 says to test first). Degraded, not infeasible. V2 fails the same rule (its own Q7: the ledger convention cannot be kept with no release branch, and no fallback keeps it); V4 fails (two incompatible CI statements, no fallback). Borderline row: see "Risk to the Selection". |
| L4 Defined on first use | V1 | N | M | DISAGREE | **M** | Rule: terms and acronyms the proposal introduces are defined in place; "CI" and project vocabulary shared with the stated audience (owner and coordinator, per CONTEXT) are not penalised for any variant. Evidence: "settled" defined in step 3, "foundation story" in Q2, "leaf" in sec 2. |
| L4 | V2 | N | M | DISAGREE | **M** | "dark" defined in sec 1 ("the code is in `integration` but nothing reaches it until ... wires it in or flips a flag"); "slice" in step 1. |
| L4 | V3 | N | M | DISAGREE | **M** | "train" defined in sec 1 ("one batch branch `train/dash1.3`, cut from `integration`"); "sync branch" in the names table. V4 stays N under the same rule (imports four source terms undefined). |
| E1 Collection boundaries | V2 | M | N | DISAGREE | **N** | Rule: a stated rule or trigger at a boundary (one-item, empty or maximum). V2 sec 1 "one or more small pull requests" and Q4 "Release size is bounded by the slices" describe, they do not set a rule or trigger. V1 and V3 pass the same rule (one-story skip; time box or split after a week). |
| E1 | V4 | M | N | DISAGREE | **N** | The size warning (PR #147, 1,384 files) is evidence of the maximum-size problem; "keep stories short-lived" (Q5) is not a trigger. Same rule as V2. |
| E2 State interactions | V4 | M | N | DISAGREE | **M** | Rule: at least one correct rule for state moving across a component boundary. Evidence: rule 3 "done by the coordinator between two story merges (never mid-merge)"; rule 2 conflicts stopped and reported to the coordinator. The wrong `integration` handling is the same defect already charged under K2 and K4 (both passes agree N) and is not charged a third time here. |
| E4 Count divergence | V4 | N | M | DISAGREE | **N** | Rule: a divergence scenario (off-by-one, ordering, inclusive range). V4's "two-digit story number (zero padded so they sort)" is the same convention as V2's `s01` to `s99` and V3's `s<NN>`, both N in both passes. Only V1 names a real case: "a future `1.10` would sort wrongly" (and `dash1.1` is a prefix of `dash1.105`, invariant probe INV-018). |

Agreed rows that carry the rest of the table (105 pairs): all MET or all NOT MET as shown in the qualitative tables above. The ones that matter for the ranking: K4 and S5 and L4 are NOT MET for V4 only (both passes); R1, R2 and C5-style rows are NOT MET for everyone; K2 is NOT MET for V2 and V4 (both passes).

## Combined Scoring

### Scores

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Rank |
|---------|---------------|--------------|-----------------|------|
| V1 (release line, local merges) | 0.4851 (quant 0.9703) | 0.4500 (qual 0.9000, 27/30) | **0.9351** | 1 |
| V3 (release train) | 0.4870 (quant 0.9739) | 0.4333 (qual 0.8667, 26/30) | **0.9203** | 2 |
| V2 (trunk, dark landing) | 0.4786 (quant 0.9572) | 0.4000 (qual 0.8000, 24/30) | **0.8786** | 3 |
| V4 (GFxAI adapted) | 0.4263 (quant 0.8525) | 0.3333 (qual 0.6667, 20/30) | **0.7596** | 4 |

**Margin (V1 over V3)**: 0.0149, which is 1.5 percentage points of the score range (1.6 percent relative to V3). It is below the 5 percent (0.05) threshold, so the tiebreaker protocol applies. V2 is 5.6 points behind V1 and V4 17.5 points behind.

### Tiebreaker (top two: V1 and V3)

**Level 1, debate performance: decides.** Diff points won in the Step 2 scoring matrix, counted over the 41 competing points (S-001 to S-006, C-001 to C-025, X-001 to X-010; the 17 shared-assumption rows carry a verdict, not a variant winner, and the 18 unique contributions are keep-or-drop, so neither is counted). A variant is credited when it is named in the Winner column, alone or in a combined winner; "sole" counts only points where it is the only variant named.

| Variant | Points credited (of 41) | Share | Sole winner | Examples |
|---------|-------------------------|-------|-------------|----------|
| V1 | 27 | 65.9% | 16 | C-002, C-003, C-006, C-008, C-009, C-010, C-014, C-015, C-018, C-020; X-001, X-002, X-003, X-005, X-007, X-009 |
| V3 | 9 | 22.0% | 0 | shares C-001, C-004, C-011, C-012, C-013, C-021, X-006, S-003, S-005 |
| V2 | 7 | 17.1% | 1 | C-007; shares C-001, C-011, C-021, C-022, S-003, S-005 |
| V4 | 6 | 14.6% | 2 | C-016, C-024; shares S-002, C-001, C-019, C-023 |

Nine points have no variant winner (S-001, S-004, S-006, C-005, C-017, C-025, X-004, X-008, X-010). V1 leads V3 by 43.9 percentage points, far outside the 5 percent band, so Level 2 is not needed. For the record, Level 2 (correctness criteria MET): V1 5, V3 5, V2 4, V4 3, a tie between the top two; Level 3 (input order) would also favour V1.

Unique contributions kept from each variant, for context (not part of the count): V1 4 of 5 (U-001, U-002, U-003, U-005), V3 3 of 4 (U-010, U-012, U-013; U-011 reserve only), V4 4 of 5 (U-014, U-015, U-017, U-018 reduced), V2 1 of 4 (U-006 as a planning rule only).

**Tiebreaker applied: Yes (Level 1). Winner: V1.**

### Edge Case Floor result

All four variants pass the floor (5/5, 3/5, 4/5, 3/5). V1 is eligible.

### Robustness table (what happens to the margin under other defensible readings)

| Reading | V1 | V3 | Margin | Tiebreaker needed | Selected |
|---------|----|----|--------|-------------------|----------|
| Main result (above) | 0.9351 | 0.9203 | 0.0149 | Yes | V1 |
| Quant = straight average of the passes (V1 0.9437, V3 0.9668) | 0.9219 | 0.9167 | 0.0051 | Yes | V1 |
| Strict RC (explicit statements only; V1 0.9312, V3 0.9609) | 0.9156 | 0.9138 | 0.0018 | Yes | V1 |
| V3 Correctness 2 flipped to NOT MET (V3 qual 25/30) | 0.9351 | 0.9036 | 0.0315 | Yes | V1 |
| C1 strict for all four (RC must be 1.0: V1 26, V2 23, V3 25, V4 20) | 0.9185 | 0.9036 | 0.0149 | Yes | V1 |
| Cross-document references counted in DC (V1 DC 11/12, V3 DC 6/16) | 0.9289 | 0.8734 | 0.0555 | No | V1 |
| Soft hedges counted in SR (P1 sensitivity) | 0.9345 | 0.9190 | 0.0155 | Yes | V1 |

V1 ranks first under every reading. In six of seven the margin is below 0.05, so the debate points (V1 27, V3 9) are what carries the decision; the scores alone would not.

## Selected Base: Variant 1 (release line, story branches, local merges; architect persona)

### Selection Rationale

V1 is selected on five pieces of evidence, none of which is the quantitative layer (which does not separate V1, V2 and V3):

1. **Highest combined score**: 0.9351 against V3 0.9203, V2 0.8786, V4 0.7596; top on qualitative score (27/30) and the only variant at 5/5 on both Correctness and Invariant and Edge Case Coverage.
2. **Tiebreaker, Level 1**: 27 of 41 debate points credited to V1 (16 as sole winner) against 9 for V3. V1's lead is not a few large points: it holds the unanimous rows that define the shape of the answer. The base of the line (cut from `master`: C-002, X-001, 95 percent), the landing path (one PR into `master`, not through `integration`: C-003, X-002, 92 percent), keeping Clay's unreleased work out of the release PR (C-018, X-003, 96 to 97 percent), merge `master` only (C-008, 90 percent), no cherry-pick or back-port (C-015, 93 percent), ledger and `.dev/` on the line with planning from `master` (C-020, X-009, 96 percent) were all conceded by the advocates of V2, V3 and V4 in Round 2.
3. **It is the only variant that fits CONTEXT.md as written**: the owner's model (release line, story sub-branches, one landing, CONTEXT line 7), ledger on the release branch (line 14), local coordinator merges (lines 9 and 11), no change to CI or repository settings (V1 sec 6). V2 states its own mismatch with the ledger convention (Q7) and needs the owner to click every slice; V3 needs a standing-rule change, a `test.yml` edit and a planning-base move; V4 contradicts itself twice and never states its base.
4. **The combined designs written in Round 2 use V1 as the base** (A1R2 and A4R2 both label theirs "base V1"; I read those two in full, and A4R2 describes V1 as "the base of every combined design"; A2 and A3 conceded C-002, C-003, C-008 and C-018 to V1 in the matrix). Convergence was 87.9 percent (51 of 58), above the 80 percent threshold.
5. **Its weaknesses are the kind other variants can patch without changing the design**: the review-size risk (cap, digest, optional review-only story PRs, outside dispatch run), no freeze rule, no forward-only push, no stated revert-then-redo procedure, no explicit remote-branch deletion. A1 conceded all of these in Round 2 and adopted the patches (A1R2 items 1 to 5), which is why the list of strengths to incorporate below is long and specific.

What V1 does not win, and the merge must supply from elsewhere: the Orca-safe names (C-001), a freeze rule (C-016), per-unit review and CI latency (C-007, C-021), the time box (U-010, C-013), and the tooling limit on very large release PRs (invariant probe INV-017, below).

Margin note: the combined-score margin is 0.0149 and the selection depends on the debate tiebreaker, so the rationale rests on points 2 to 4, not on the scores.

### Strengths to Preserve from Base

Each item: what to keep, where it is in V1, the diff id that records the debate outcome, and the CONTEXT.md question it answers.

1. **Release line cut from `master`, one pull request into `master` at the end, by `/sc:pr-submit --monitor 3 --base master`, merge commit, owner merges** (V1 sec 1, sec 3 steps 1 and 5, Q4). C-002, C-003, X-001, X-002 (unanimous). Answers Q3 and Q4.
2. **`integration` is never merged into the release line; `master` is merged in at start, between stories (never mid-merge) and before the PR; merge only, never rebase after the first push** (V1 Q3). C-008, C-009, C-018, X-003, X-007, A-017 REJECT (unanimous). Answers Q3 and Q8. This is the piece V4 got wrong and all four advocates reject.
3. **Local `--no-ff` merge by the coordinator, one story at a time; no PR per story as the default** (V1 sec 3 step 3, Q2). C-004, C-006, X-005 (unanimous on the default; the owner's confirmation in chat is still required, A-014). Answers Q2.
4. **Ref-conflict leaf rule as the stated invariant**: a branch name may never be the folder part of another branch name; the bare release token is never a branch (V1 sec 2 first paragraph). C-001 (the shapes change, the invariant stays). Answers Q1.
5. **No flags in the base design; no cherry-pick or back-port step** (V1 Q5, Q6). C-012, C-015 (unanimous). Answers Q5 and Q6.
6. **Ledger, `sprint-status.yaml` and `.dev/` records on the release line; BMAD planning of release n+1 starts from `master`** (V1 Q7, step 1). C-020, X-009 (unanimous). Answers Q7 and CONTEXT line 14.
7. **Guards before the merge**: read-only `git merge-tree` trial of the story branch onto the line tip, "if it would conflict, stop" (V1 step 3; U-001), path-claim comparison with open `integration` PRs at release start (V1 Q3; U-003), shared files owned by one story or a first foundation story (V1 Q2(b)). Adopted by all four (80 percent). Answers Q2 and Q8.
8. **Per-story digest (ledger lines plus `git log --merges`) in the release PR body as the release-size control** (V1 Q4; U-002, adopted by all four). Answers Q4.
9. **Rollback**: `git revert -m 1 <story merge commit>`, revert dependent stories in reverse order, revert PR of the release merge commit on `master`, prefer a bug-fix release line (V1 Q9; U-005, C-022 "V1 at release and story level"). Answers Q9.
10. **Explicit deletion of story and line branches and worktrees after the ledger records the merge**, because `delete_branch_on_merge` is false (V1 Q7; C-023, unanimous, evidence A4 E6). Answers Q7.
11. **The exact-name creation command and the warning that `worker-start` has no `--branch`** (V1 sec 2 last paragraph; CONTEXT line 12): `orca worktree create --branch <name> --base-branch <ref> --parent-worktree <selector> --agent claude`. Answers Q1.
12. **Sort caution for release tokens** ("a future `1.10` would sort wrongly", V1 sec 2); it is the only count-divergence case in any variant (Invariant 4). A4R2 adds "write 1.10 as 1.100". Answers Q1.
13. **Honest cost, who-it-favours and risk sections**, and the document layout (sec 1 to 8: summary, names, flow diagram with six steps, nine questions, costs, favours, risks, sources) (S-003, S-005: V1, V2 and V3 won; V4 conceded).

### Strengths to Incorporate from Non-Base Variants

Each item: source variant and section, diff id (outcome in the Scoring Matrix), CONTEXT.md question it answers, and how it joins the base (insert / append / replace). "Converged" means the Round 2 matrix shows all four advocates (or all but one, with the rest not contesting) at that position.

**From V4 (GFxAI adapted)**

1. **`release/<rel>` folder for the release line** (V4 rule 1 "Release branch: `release/dash1.3`"; C-001, 3 of 4, 72 percent). Q1. Replace V1's `dash1.3/release`. Keeps the ref-conflict invariant because no story branch is under `release/`.
2. **Freeze after the last planned story: only `-fix` branches until the PR is merged** (V4 rule 6 "Beta freeze"; C-016, unanimous, 90 percent). Q6. Insert into V1 Q6; V1 had no freeze rule.
3. **Tag `dash-1.3`** (V4 rule 4; C-024, 3 of 4, 72 percent; trivial). Q1, Q4. Replace V1's `dash/1.3` (same value without a `dash/` folder, and V4 states why it is not `v1.3.0`: the package is 6.1.0).
4. **Explicit clean-up rule that also deletes the remote branch, with the reason** (V4 rule 7: GFxAI left 6 `backup/...` branches and a stale `release/v0.1`; C-023, unanimous, 92 percent). Q7. Append to V1 Q7. Verified: `delete_branch_on_merge` is false and 170 remote heads exist (invariant probe INV-014), so a sweep or checklist item is also needed.
5. **Release-PR size evidence** (V4 rule 4: PR #147, 34 commits, 1,384 files, +242,976 lines; with in-repo #640, #664, #31) (U-015, keep as size evidence with no precedent weight, 72 percent). Q4. Append to V1 Q4 as the reason for the cap.
6. **Reduced acceptance gate for the release PR**: freeze, full local suite, green `workflow_dispatch` run on the final tip, PR CI and both bots, the owner; not the source's three test tiers or two approvers (V4 rule 4; U-018, reduced, 58 percent). Q4. Append to V1 Q4. Note INV-026: a dispatch run does not run the PR-only workflows, so it is necessary but not sufficient.
7. **Provenance marks** FROM SOURCE / FROM PRACTICE / MY ADAPTATION / UNSPECIFIED, applied to the merged text as evidence marks (V4 line 5; U-014, S-002, 78 percent). Document format. Append.
8. **Wording of the merge-right rule**: the coordinator never merges into `master`; a local merge into the release line is a separate, smaller class (V4 rule 2; U-017, 72 percent). Q2. Insert next to V1's Q2 "Where". It supports the owner's confirmation in chat (A-014).
9. **The sync is the price of landing on `master`** (V4 rule 4 "then `master` is merged back into `integration`"; C-019, unanimous, 62 percent). Q8. Already in V1 Q8; keep V1's text and add V4's statement of why.

**From V2 (trunk, dark landing)**

10. **Flat story branch names** `dash1.3-s04-<slug>` (V2 sec 2; C-001, U-004 "Drop" for story folders). Q1. Replace V1's `dash1.3/s04-<slug>`. Reason (A4 M1, A2 N5): without `--branch`, Orca names the branch `ironbelly/<worktree name>`, and a worktree called `dash1.3` then blocks `ironbelly/dash1.3/s04-...` ("cannot lock ref"). Flat names cannot be a folder of anything.
11. **Outside CI per story without a workflow edit: `workflow_dispatch` on the pushed line after any story that touches shared or risky paths, and always on the final tip** (V2 Q2 "CI on every slice runs against the real `integration`" as the goal; C-007, C-011, unanimous with qualification; evidence A4 M2 two dispatch runs on 2026-11-05, M3 median 9.2 minutes, A1R2 `test.yml` has an unconditional `workflow_dispatch`). Q2. Append to V1 Q2 as the default outside gate. Owner approves the CI minutes (owner decision 3).
12. **Slice-level undo and flags as the third rung of the ladder, after a pilot on one story** (V2 step 1 slice classification, Q5 flags; U-006 planning rule only, U-008, U-009, C-022 "V2 at slice level"). Q5, Q9. Append to V1 Q5 as the last fallback; never the base (the base has no flags, C-012).
13. **Shared-file list for the coordinator** (the debate's addition: `CHANGELOG.md`, `CLAUDE.md`, `README.md`, `PROJECT_INDEX.json`, `PROJECT_INDEX.md`, docs index files, from the #662 stat, A4R2 Q2) joined to V2 Q2 "shared files in their own first slice". Q2. Insert into V1 Q2(b). Gap: INV-019 shows identical edits to a pinned count (for example `n=47` to `n=48`) merge cleanly and give a wrong value, so count-pinned tests and the dependency baseline also belong on the list.

**From V3 (release train)**

14. **Time box with floating scope: "the scope floats, the time does not"; stories not merged at the time box ride the next release** (V3 Q5; U-010, C-012, C-013, X-006, unanimous, 86 to 95 percent). Q5. Insert into V1 Q4 and Q5 as the justification for a long-lived line (V1's own justification was conceded by A1 as weaker). Starting numbers about six stories or seven days are estimates, not measurements; the owner sets them.
15. **Ladder of fallbacks: line only; then optional review-only story PRs; then dark-by-construction slices after a pilot** (V3 Q5 "If trains routinely run past the time box, move toward Proposal 2"; V1 Q5 "switch to Proposal 3"; C-013, X-006). Q5. Append to V1 Q5.
16. **Optional review-only story PR into the release line**, so Augment and Codex see one story at a time (V3 Q2; C-004, C-007, C-021 optional layer, 60 to 72 percent). Q2, Q4. Append to V1 Q2 as an owner-chosen layer. Verified: bots reviewed PRs on the non-default base `346Claude-integration` (#484, #490, #491; A-012 ACCEPT, 96 percent) but CI did not run there; the line must be pushed first and the local merge must be a merge commit for GitHub to show the PR as merged (A4R2 point on V3, UNVERIFIED; test b below). Price: no CI on those PRs, one top-level `/sc:pr-submit` session per story (A3-C10).
17. **One owner decision list at the end of the document** (V3 sec 8; U-012, unanimous). Document format. Append; the merged text carries the five decisions in "Open points" below.
18. **Throwaway tests before first reliance** (V3 risk 5 "Check by opening one test pull request first"; U-013, unanimous, 96 percent). Q1, Q2, Q4. Append as a pre-release checklist. The tests the debate named: (a) `--branch` keeps the exact name, and what a ref-conflicting name does (A-007, A-011); (b) a review-only story PR against `release/...`: both bots review, GitHub shows it merged after a local `--no-ff` merge and push; (c) the release PR at `--monitor 3` with the draft guard (A4 M10); (d) one dispatch run on the pushed line; (e) the two-parent (merge commit) check in closeout.
19. **`dash1.3-sync<N>` conflict branch, as a reserve only** (V3 sec 2; U-011, reserve only, 70 percent). Q3. Do not add to the base; keep as a written fallback in case `integration` is ever merged in.
20. **One-story release skips the line** (V3 Q6; V1 Q6 already has it; C-017 area). Q6. Keep the one rule.

**From the debate itself (new pieces no variant had; all four adopted)**

21. **Forward-only push of the release line after each story merge** as a backup, not a review request (A1R2 item 1, A4R2 point 8). Q2, Q9. Insert into V1 sec 3 step 3, replacing "Nothing is pushed". Needed because V1 as written is one local copy.
22. **"Revert the revert first" before re-merging a reverted story or line** (A1R2 item 3, scratch test: direct re-merge conflicts, `DU s.txt`; revert-then-merge is clean; C-005 trap, C-022). Q9. Replace V1 risk 5 ("unverified general git behaviour") with a stated procedure.
23. **"Merge this pull request with a merge commit, not squash" in the release PR body, plus a closeout two-parent check (new work, needs building)** (A-006 ACCEPT, 96 percent: all three merge methods are allowed, nothing technical stops a wrong click; precedent #658, reverted by #662, redone as #664). Q4. Insert into V1 Q4.
24. **First-parent bisect over `--no-ff` story merges** (A4 M5, scratch test names "merge s4"). Q9. Append to V1 Q9.

**Must-address items from the invariant probe, for the merge (not strengths of a variant)**

25. **INV-017 (HIGH, UNADDRESSED): a very large release PR cannot be read by the tools in the loop.** `gh pr diff` fails above 300 files and `gh pr view --json files` returns only 100; `.dev/` records alone can reach that (record-only PRs #728 and #730 changed 453 and 292 files, INV-011). V1 puts the whole release in one PR, so V1 is the variant most exposed. The probe lists no fix; options it names are keeping `.dev/` records out of the release PR or capping files as well as stories. This is not a score input, but under SKILL.md (convergence gate) a HIGH UNADDRESSED invariant makes the run BLOCKED_BY_INVARIANTS until the merge answers it. The orchestrator owns that status; I record it here so Step 4 carries it.
26. The MEDIUM items that land on V1's design and should get a line in the merged text: INV-003 (what coordinators do while the release PR waits for the owner), INV-005 (the release head must stay fixed while `--monitor 3` runs; the coordinator shares the release worktree), INV-006 and INV-007 (post-merge local tests are not the CI gate: `lint` job, `make sync-dev`, `make verify-sync`; 9 of the last 40 PR runs failed), INV-008 (`contract3-generator-constraint-lint.yml` needs the `## Generator-Constraint Considered` heading for PRs touching `gates.py`, `structural_checkers.py` or `*_validator.py`), INV-009 (merge method is enforced by a sentence only), INV-011 (file count versus story count), INV-019 (cleanly merging identical edits), INV-025 and INV-026 (no cap number; a dispatch run is not the PR run).

### Base elements the merge replaces

Where the debate showed the base lost the point, and the merge should change it (these feed the refactoring plan as "base weaknesses"):

| Base element | What was found | Replace with | Diff id |
|--------------|----------------|--------------|---------|
| Names `dash1.3/release` and `dash1.3/s04-slug` (V1 sec 2) | Orca names a worktree's branch `ironbelly/<worktree name>` unless `--branch` is given, and a worktree called `dash1.3` blocks every `ironbelly/dash1.3/...` branch; V1 itself rates the prefix behaviour UNVERIFIED (risk 4) | `release/dash1.3` plus flat `dash1.3-s04-<slug>`, in-release fix `dash1.3-fix01-<slug>`, shipped-code fix `fix/<issue>-<slug>`; tag `dash-1.3`; throwaway create first | C-001 (3 of 4), C-024, U-004 Drop, A-007, A-011 |
| "Nothing is pushed for review until the release is complete" (V1 sec 1) | One local copy of the release; the coordinator's disk is the only backup | Forward-only push after each story merge, as a backup and not a review request | A1R2 item 1 (conceded in full) |
| No freeze rule | New stories could keep landing while `/sc:pr-submit --monitor 3` runs | Freeze after the last planned story, `-fix` branches only | C-016 |
| Risk 5, revert-then-remerge "unverified" | A procedure was missing, not a structural defect | "Revert the revert first" rule | A1R2 item 3 |
| No outside gate per story; one big review at the end (V1 sec 5, risk 1, risk 6) | Release-sized PRs landed in 17 to 43 minutes (A2 N2), which proves speed, not review depth | Cap, digest, dispatch run, optional review-only story PRs, time box | C-007, C-021, U-002, U-010 |
| Justification of the long-lived line by Driessen and Fowler only (V1 Q5) | A1 conceded V3's time box is the better justification | Time box with floating scope | U-010, C-013 |
| Wrong merge click possible; the "closeout checks the merge method" idea | `branch-landed.sh` asserts no merge method (A4 M4) | PR body sentence plus a new two-parent check | A-006 |

### Open points: which position should win

These are the seven points the debate left unresolved (Convergence Assessment). For each: the split, which position should win in the merged design, and whether it needs the owner.

| Point | Question it touches | Split (latest positions) | Recommended position for the merge | Owner decision? |
|-------|---------------------|--------------------------|-------------------------------------|-----------------|
| C-005 and X-004 (one open point seen twice) | Q2: merge method of a story into the line | A1 V1 `--no-ff` narrowly (55); A2 and A3 no winner (50); A4 no winner, leans `--no-ff` (55) | **V1: `--no-ff` as the written default.** Reasons: the re-merge trap has a verified remedy (revert the revert first); `git bisect --first-parent` names the bad story (A4 M5); the story's own commits stay reachable; the optional review-only story PR needs a merge commit for GitHub to show it as merged. Squash (V4, V2) gives a simpler plain revert. The release PR is a merge commit in every design (A-006). | **Yes**: owner decision 5 in A4R2 ("`--no-ff` or squash"). Present `--no-ff` as the default with the squash trade-off in one line. |
| C-017 | Q6: 1.1 bug-fix and 1.105 test-only releases | A1 and A4: ordinary release lines with a one-story skip; A2 and A3: no line, small direct PRs into `master` (two lanes) | **V1 and V4's position as the default**: one rule set, the ledger convention stays (C-020), a one-story release skips the line (V1 Q6, V3 Q6). V2 and V3 reached the two-lane view from designs that lost the base question, and many direct PRs would add owner clicks (A-003). | **Yes, for 1.105 only**: may a test-only release also skip the line? (A4R2 asks it as an owner question.) The bug-fix 1.1 case follows the default. |
| A-008 | Q4, Q2: does the `test.yml` edit reach the workflow copy GitHub reads for a `pull_request` run | A1 and A2 ACCEPT (V3 and V4 only dependency); A3 and A4 QUALIFY (the dispatch default avoids the edit) | **QUALIFY (A3 and A4).** The base needs no edit: the release PR goes into `master`, which already triggers CI, and the default outside gate is `workflow_dispatch` (A4 M2 precedent). The question matters only if the owner wants CI on review-only story PRs. Where GitHub reads the workflow file is UNVERIFIED (A3 E7, secondary sources). | **No**, unless the owner wants per-story CI. If wanted, settle with the throwaway test, not by opinion. |
| A-011 | Q1: does `orca worktree create --branch` keep the exact name | A1 and A2 ACCEPT; A3 and A4 QUALIFY (A4 M1 reports exact and unprefixed; "a taken name gets a numeric suffix") | **QUALIFY (A4).** All four plan the same throwaway check. Whether a ref-conflicting name counts as "taken" is UNVERIFIED. Flat names remove the ref-conflict case anyway. | **No**: a coordinator test before the first release (test a). |
| A-013 | Q4, Q2: the owner accepts editing `test.yml` triggers | A1 and A2 ACCEPT; A3 and A4 QUALIFY | **QUALIFY (A3 and A4)**, same reason as A-008: only needed for CI on story PRs. | **Only if** per-story PR CI is wanted (A4R2 decision 3: CI minutes for dispatch runs, and whether review-only story PRs are wanted and above what size). |
| A-015 | Q8: someone runs the `master` into `integration` sync | A1 and A2 QUALIFY; A3 and A4 ACCEPT (A2 changed to QUALIFY in Round 2) | **ACCEPT the obligation (A3 and A4), assign it explicitly to the coordinator**, as V1 step 6 and Q8 already say: it is the price of landing on `master` (C-019). Who does it today is UNVERIFIED (A4 E4 lists five manual sync commits by clayphi, 2026-11-17 to 11-19). | **Yes, a small one**: confirm the assignment and answer whether `integration` is still the branch Clay works from (`master` 26 commits ahead; newest `integration` commit 2026-11-18, A4 M11; the debate also cites 2026-11-19 for the last merged PR). |
| A-014 (not on the unresolved list, but the base depends on it) | Q2: the standing rule "owner merges every PR" and local coordinator merges | Unanimous QUALIFY | Keep V1's local merge as a smaller authority class (U-017 wording), subject to the owner's chat confirmation. CONTEXT line 11 itself says "to be confirmed". | **Yes**: owner decision 1. If refused, the design moves to V3's per-story PR (the V1 Q5 fallback). |

The remaining owner decisions in A4R2 section 5: story cap and time box (decision 2); CI minutes and review-only story PRs (decision 3); is `integration` still in use (decision 4). Together with the rows above these are the list the merged document should end with (U-012).

## Risk to the Selection

**How robust the choice is.** V1 ranks first under all seven readings tested in the robustness table, but the score margin over V3 is 0.0149 (0.0018 to 0.0315 across readings, 0.0555 in one), so the scores alone would not carry the selection. What carries it is the debate tiebreaker (V1 27 points of 41, V3 9, a gap of 43.9 points) and the content of those points: the shape-defining questions (base, landing path, Clay's unreleased work, ledger and planning base) were conceded to V1 by the advocates of V2, V3 and V4.

**What would flip it to V3.**
1. The owner declines to let the coordinator merge into the release line (A-014, C-006). V1's central mechanism then does not exist, and V3's PR-gated batch (with the coordinator or the owner merging story PRs) becomes the nearest design. The base would then be V3 re-cut from `master` (not `integration`), which is a different design from V3 as written.
2. The owner wants CI and both bots on every story as a requirement rather than an option. V1's optional layers (dispatch run, review-only PR) deliver bots without CI and CI without bots; V3 delivers both only after a `test.yml` edit and a merge-authority decision.
3. A throwaway test fails: if bots do not review PRs into the release line, or GitHub does not show a locally merged story PR as merged (tests b, d), the V3 and V2 per-unit review ideas lose their cheap form.
4. The release PR cannot be reviewed at its size (INV-017). This is the one finding that hits V1's own core. It does not move the ranking, because every variant except V2 lands release-sized PRs and V2's promotion carries all of `integration`, but it can force a design change (cap by files, `.dev/` out of the PR, or the third-rung ladder), and under SKILL.md it blocks convergence status until the merge answers it.

**What does not flip it.** The quantitative layer: V1, V2 and V3 are within 0.0167 of each other and one RC item is worth 0.013. SR and DC are 1.0 for everyone, and the DC result depends on the protocol's exclusion of cross-document references (counting them would drop V3 to 0.8802 and strengthen V1).

**Borderline qualitative rows.** K2 for V3 (final MET; if NOT MET, V3 is 0.9036 and the margin 0.0315), C1 and L4 (rules chosen to be uniform across the four variants; a strict reading of C1 costs V1 and V3 each one point and leaves the margin at 0.0149), C5 (NOT MET for all four; a lenient reading adds one point to each and changes nothing). E1 and E4 favour V1 and V3 over V2 and V4 and are the reason V2 sits third.

**The researcher agent's pre-debate expectation (variant 3 as the likely base).** Recorded, not used. The evidence agrees in part and disagrees in part. Agrees: V3 has the highest quantitative score (0.9739, entirely from section count and the DC exclusion) and finishes second on the combined score, 0.0149 behind. Disagrees: V3 loses the questions that decide a base. A3 conceded the base (cut from `integration` against `master`, C-002, X-001), the landing path (through the `integration` promotion that none of the owner's recent 130 PRs used, C-003, X-002; `integration` has had no merged PR since about 2026-11-18 or 11-19 and `master` is 26 commits ahead), the planning-base change (C-020, X-009), and the coupling to Clay's unreleased work (C-018). What survives of V3 is a set of additions to the base (time box, open decisions list, throwaway tests, optional review-only story PRs, a reserve sync branch), not its structure.

**Reconciler confidence.** High that V1 is the right base for this use case; moderate that the score margin alone would reproduce it. I did not re-run the debate or open the research-notes evidence (S1 to S22), and the GFxAI facts (PR #147 and others) were not re-checked by either scoring pass or by me.
