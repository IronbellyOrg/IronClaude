[roadmap] Input type: tdd (spec=.dev/test-fixtures/test-tdd-user-auth.md, tdd=None, prd=.dev/test-fixtures/test-prd-user-auth.md)
NOTE: TDD input detected. The pipeline's deviation-analysis step (DEVIATION_ANALYSIS_GATE) is not yet TDD-compatible and may fail. All other steps (extract through spec-fidelity) will work correctly.
[roadmap] Starting step: extract
[roadmap] Step extract  PASS (attempt 1, 327s)
[roadmap] Starting step: generate-opus-architect
[roadmap] Starting step: generate-haiku-architect
[roadmap] Step generate-opus-architect  PASS (attempt 1, 137s)
[roadmap] Step generate-haiku-architect  PASS (attempt 2, 220s)
[roadmap] Starting step: diff
[roadmap] Step diff  PASS (attempt 1, 76s)
[roadmap] Starting step: debate
[roadmap] Step debate  PASS (attempt 1, 129s)
[roadmap] Starting step: score
[roadmap] Step score  PASS (attempt 1, 91s)
[roadmap] Starting step: merge
[roadmap] Step merge  PASS (attempt 1, 392s)
[roadmap] Starting step: anti-instinct
[roadmap] Step anti-instinct  FAIL (attempt 1, 0s)
           Reason: Semantic check 'no_undischarged_obligations' failed: undischarged_obligations must be 0; scaffolding obligations lack discharge in later phases
[roadmap] Step wiring-verification  PASS (attempt 1, 1s)
ERROR: Roadmap pipeline halted at step 'anti-instinct' (attempt 1/2)
  Gate failure: Semantic check 'no_undischarged_obligations' failed: undischarged_obligations must be 0; scaffolding obligations lack discharge in later phases
  Output file: /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/results/test1-tdd-prd/anti-instinct-audit.md
  Output size: 1224 bytes (53 lines)
  Step timeout: 30s | Elapsed: 0s

Completed steps: extract (PASS, attempt 1), generate-opus-architect (PASS, attempt 1), generate-haiku-architect (PASS, attempt 2), diff (PASS, attempt 1), debate (PASS, attempt 1), score (PASS, attempt 1), merge (PASS, attempt 1), wiring-verification (PASS, attempt 1)
Failed step:     anti-instinct (FAIL, attempt 1)
Skipped steps:   test-strategy, spec-fidelity, deviation-analysis, remediate, certify

To retry from this step:
  superclaude roadmap run /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/test-tdd-user-auth.md --resume

To inspect the failing output:
  cat /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/results/test1-tdd-prd/anti-instinct-audit.md
