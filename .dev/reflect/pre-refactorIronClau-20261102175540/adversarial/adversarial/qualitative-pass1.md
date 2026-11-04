# Qualitative scoring — Pass 1 (input order 1, 2, 3)

Returned by a read-only scoring agent; persisted by the orchestrator. Every MET verdict carried a file:line or finding-id citation in the agent's tables; only the NOT MET verdicts are reproduced in full here, with the summary.

## NOT MET verdicts
- Variant 1: C1 (accepts the grep as full scope, inferred:77; misses eval_runner.py); L3 (R1-2 headline is two sentences, variant-1:19); E1 (no empty/single/max analysis).
- Variant 2: C1 (`missing_requirements: []` at line 39 wrong given eval_runner.py:143); C5 (no out-of-scope statement); K1 (R2-F4 misquotes .gitignore:129); K3 (R2-F4 calls a constraint copying a CLAUDE.md absolute rule "drift"); L4 ("INF-007" at line 24 used before INF is defined); R3 (document-level only, no runtime failure/recovery); R4 (Orca CLI assumed, no failure handling); E1; E4 (no count-mismatch analysis).
- Variant 3: C1 (does not check `.claude` staging or "keeps working without Orca"); K3 (all six labelled drift); L4 ("INF-003" never defined); E1.

## Citations verified by the agent
CLAUDE.md:64, :66, :251; POST-REFLECT-TASK.md:6, :576; .gitignore:132, :240-242; test_sc_recommend_routing_contract.py:27, :29, :130; sc-post-release-protocol/SKILL.md:91; sc-pr-submit-protocol/SKILL.md:267; test_implement_retry_revert.py:613; scripts/eval_runner.py:138, :143. One misquote: Variant 2's .gitignore:129.

## Summary
| Variant | Completeness | Correctness | Structure | Clarity | Risk | Invariant | Total/30 |
|---|---|---|---|---|---|---|---|
| 1 | 4/5 | 5/5 | 5/5 | 4/5 | 5/5 | 4/5 | 27 |
| 2 | 3/5 | 3/5 | 5/5 | 4/5 | 3/5 | 3/5 | 21 |
| 3 | 4/5 | 4/5 | 5/5 | 4/5 | 5/5 | 4/5 | 27 |

Edge-case floor (>= 1/5 invariant): all three eligible.
