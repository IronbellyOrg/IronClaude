# Base Selection

## Quantitative Scoring (50% weight)

Orchestrator counts over the card text and the debate record (no scorer agent). The variants are reviewer cards, so "requirement coverage" is measured against five audit questions: (1) accuracy of the requested sentence, (2) soundness of the acceptance criteria, (3) anchor and placement, (4) code evidence for the `--force` behavior, (5) fallout on other docs and tests. These counts are an estimate by one reader, not a formula run by a tool: [INFERRED] for SR, which depends on judging "concrete" versus "vague".

| Metric (weight) | V1 | V2 | V3 | Basis |
|---|---|---|---|---|
| RC requirement coverage (0.30) | 0.80 | 0.20 | 0.60 | V1 covers questions 1-4; V2 covers 2 (partly); V3 covers 1, 3, 5 |
| IC internal consistency (0.25) | 0.71 | 0.67 | 0.83 | claims later contradicted in the debate: V1 2 of 7, V2 1 of 3, V3 1 of 6 |
| SR specificity (0.15) | 0.95 | 0.85 | 0.95 | all three cite file:line; V2 has two "no change needed" findings |
| DC dependency completeness (0.15) | 1.00 | 1.00 | 1.00 | every cited file:line exists |
| SC section coverage (0.15) | 0.80 | 0.40 | 1.00 | findings per card 4 / 2 / 5, max 5 |
| **quant_score** | **0.830** | **0.565** | **0.830** | |

## Qualitative Scoring (50% weight): 30-criterion additive binary rubric

Two independent scorer agents (pass 1 in order V1, V2, V3; pass 2 in order V3, V2, V1) used the Claim-Evidence-Verdict form. Criteria are listed in the scorer prompts; evidence is in each scorer's return (not stored separately).

### Position-bias mitigation

| Variant | Criteria where the passes disagreed | Final ruling (re-evaluated by the orchestrator, final) |
|---|---|---|
| V1 | K5 (pass 1 MET, pass 2 NOT MET); S3 (pass 1 NOT MET, pass 2 MET) | K5 NOT MET: F1 cites install_hooks.py:250 for a settings.json claim it does not support and F3 is tagged inferred with a wrong argument. S3 MET: F1 wording, F2 mechanism, F3 criterion, F4 anchor are distinct concerns |
| V2 | L2 (pass 1 NOT MET, pass 2 MET); L5 (pass 1 NOT MET, pass 2 MET) | L2 MET: cites source.md:1 and plan:29-30. L5 MET: F2 says to inspect the sentence and diff against the criteria during execution |
| V3 | C1 (pass 1 MET, pass 2 NOT MET); R4 (NOT MET, MET); E1 (NOT MET, MET); E3 (MET, NOT MET) | C1 NOT MET: criterion 2 is never examined. R4 NOT MET: checks other docs but discusses no failure of them. E1 NOT MET: "one changed line" is stated, not analysed. E3 NOT MET: no guard-condition gap named |

Disagreements found: 8. Verdicts changed from at least one pass: 8 of 8 resolved by re-evaluation (each ruling matches one pass or sets the criterion NOT MET).

### Dimension subtotals (final)

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 5 | 1 | 4 |
| Correctness | 3 | 4 | 3 |
| Structure | 5 | 5 | 5 |
| Clarity | 4 | 4 | 5 |
| Risk coverage | 4 | 0 | 2 |
| Invariant and edge case | 5 | 0 | 2 |
| **Total (of 30)** | **26** | **14** | **21** |
| **qual_score** | **0.867** | **0.467** | **0.700** |

### Edge Case Floor Check (threshold 1/5)

V1 5/5 eligible. V3 2/5 eligible. V2 0/5 **ineligible as base** (the floor is not suspended: other variants meet it).

## Combined Scoring

| Variant | 0.50 x quant | 0.50 x qual | Combined |
|---|---|---|---|
| V1 | 0.415 | 0.433 | **0.849** |
| V3 | 0.415 | 0.350 | 0.765 |
| V2 | 0.283 | 0.233 | 0.516 (ineligible) |

Margin V1 over V3: 0.084 (8.4 points), above the 5% tiebreaker band. Tiebreaker applied: No. The quantitative layer tied V1 and V3 at 0.830; debate performance also favors V1 (wins C-001, C-002, C-003, X-001 versus none for V3).

## Selected Base: Variant 1 (sonnet:analyzer)

**Rationale.** Highest combined score, the only card that traced `--force` through the installers and tested the diff-based acceptance criterion, and the winner of four of eight debate points with the rest tied. Its errors are known and bounded: the staged-files argument in F3, the "never touched" phrasing in F1, and the wrong install_hooks.py:250 citation.

**Strengths to preserve.** F1 seed-file and codegraph findings (install_hooks.py:89-95, main.py:52); F2 force-flow confirmation (main.py:178-236, install_core.py:69); F4 anchor check; the `git diff --word-diff -- README.md` check idea.

**Strengths to incorporate from non-base variants.**
- From V3: the fallout check (installation.md:283, :591, upgrading.md:56-60, tests/docs/test_retired_docs_absent.py:39-49) and the "framework files" anchoring to README.md:75 and main.py:38.
- From V3 (Round 2): the exact replacement sentence for Task 1 and the baseline-aware replacement text for criterion 2.
- From V2: the confirmation that INF-001 covers the whole spec sentence and that the plan has no missing requirement.
- From the debate (all three, Round 2): installation.md:593 and install_skill.py:47-48 (the skill-folder delete-and-re-copy and the lack of a backup) as a correction to V1's and V3's preservation claims.
