# Qualitative QA reviewer card

Verdict: FAIL for immediate execution, PASS for concept direction.

Findings:

1. The spec contradicts itself on `unreachable` proof. This undermines the product promise of never-false Regression (`merged-requirements.md:26`, `merged-requirements.md:92`, `merged-requirements.md:126-132`).
2. Legacy compatibility and rollback are overstated. `unproven` becomes Grounding Gap (`merged-requirements.md:93`), and the current contract halts on `status: partial` / `needs_human_decision` (`contract.py:311-320`).
3. The implementation plan is prose-heavy and producer-light. It specifies documentation/protocol insertions and fixture-verdict tests (`merged-requirements.md:107-270`) but leaves actual Step 5.6 detection to an underspecified eval artifact (`merged-requirements.md:395-423`).
4. Cost and rollout risk are undercounted: the spec claims zero added turns (`merged-requirements.md:251-258`) despite semantic classification, symbol lookups, oracle comparison, and optional real boot (`merged-requirements.md:77-86`, `merged-requirements.md:119-129`).
