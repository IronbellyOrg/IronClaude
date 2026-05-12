[roadmap] Input type: spec (spec=.dev/test-fixtures/test-spec-user-auth.md, tdd=None, prd=.dev/test-fixtures/test-prd-user-auth.md)
[roadmap] Starting step: extract
[roadmap] Step extract  PASS (attempt 1, 94s)
[roadmap] Starting step: generate-opus-architect
[roadmap] Starting step: generate-haiku-architect
[roadmap] Step generate-opus-architect  PASS (attempt 1, 487s)
[roadmap] Step generate-haiku-architect  PASS (attempt 1, 461s)
[roadmap] Starting step: diff
[roadmap] Step diff  PASS (attempt 1, 122s)
[roadmap] Starting step: debate
[roadmap] Step debate  PASS (attempt 1, 123s)
[roadmap] Starting step: score
[roadmap] Step score  PASS (attempt 1, 66s)
[roadmap] Starting step: merge
[roadmap] Step merge  PASS (attempt 1, 357s)
[roadmap] Starting step: anti-instinct
[roadmap] Step anti-instinct  FAIL (attempt 1, 0s)
           Reason: Semantic check 'integration_contracts_covered' failed: uncovered_contracts must be 0; integration contracts lack explicit wiring tasks in roadmap
[roadmap] Step wiring-verification  PASS (attempt 1, 1s)
ERROR: Roadmap pipeline halted at step 'anti-instinct' (attempt 1/2)
  Gate failure: Semantic check 'integration_contracts_covered' failed: uncovered_contracts must be 0; integration contracts lack explicit wiring tasks in roadmap
  Output file: /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/results/test2-spec-prd/anti-instinct-audit.md
  Output size: 1037 bytes (43 lines)
  Step timeout: 30s | Elapsed: 0s

Completed steps: extract (PASS, attempt 1), generate-opus-architect (PASS, attempt 1), generate-haiku-architect (PASS, attempt 1), diff (PASS, attempt 1), debate (PASS, attempt 1), score (PASS, attempt 1), merge (PASS, attempt 1), wiring-verification (PASS, attempt 1)
Failed step:     anti-instinct (FAIL, attempt 1)
Skipped steps:   test-strategy, spec-fidelity, deviation-analysis, remediate, certify

To retry from this step:
  superclaude roadmap run /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/test-spec-user-auth.md --resume

To inspect the failing output:
  cat /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/results/test2-spec-prd/anti-instinct-audit.md
