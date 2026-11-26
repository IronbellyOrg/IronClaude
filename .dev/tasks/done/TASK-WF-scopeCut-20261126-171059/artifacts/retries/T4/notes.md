ad5823289c69c2eccf6aa4e4a7a7e9b51616b0d5
A1 r1-1 F1.1 note scripts/apply_org_rulesets.py:595 ac=T4.AC2 amiss=n,false=n,harm=n,constraint=n a 403 on branch protection is handled as unknown, which refuses and writes nothing; no test covers that case
A1 r1-1 F1.2 note tests/org_rulesets/test_apply.py:365 ac=T4.AC7 amiss=n,false=n,harm=n,constraint=n the no-PUT-no-DELETE assertion sits in one test only; the Runner allowlist enforces it for every test
