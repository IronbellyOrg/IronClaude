# Evidence validation (Wave 5, final gate)

validator: evidence-validator agent (model sonnet alias), read-only, full re-read (citation_budget_policy: full_reread, stricter than the sampled policy that applies above 20 citations)
checked: 139 (Part A: 43 findings-v2 citations incl. 4 quotes; Part B: about 62 inline plan:/spec:/base-file citations in prose; Part C: 34 inferred-requirement rows, every quote a verbatim substring of its cited spec line)

dropped (1):
- Part B | merged-output.md M2 evidence bullet 2, `plan:138` | "The plan's narrower test description on the same Task 9 paragraph (plan:138) ..." | plan line 138 is blank; the quoted wording sits on line 137. The citation is dropped from REPORT.md; the claim is restated against plan:137, which the validator had already confirmed.

doubtful but kept (validator notes):
- M7 `test_worker_contract.py:1166`: key-shape comment is on line 1165, line 1166 is `WRITE_VERB_CLASSIFICATION = {` (off by one, claim true).
- M6 `plan:166-168`: the test name `test_guard_release_failure_retries_once_and_reports` is on plan line 169 (REPORT.md cites 166-169).
- M4 Task 13 `plan:195, plan:199`: Task 13 says "base-commit record of Task 1", not the file name.
- M5 `plan:33`: line 33 defines O1; line 37 says O1 names the single mint place.
- M10 `plan:166`: lists some exit cases, not a full enumeration; claim holds in substance.
not checkable from files: debate point ids, probe ids and percentages.

mapping used for panel/kept-ids.txt: the validator ran over the merged report; every card finding is represented in M1..M10 and the merged findings-v2 citations all passed, so all 14 card finding ids are kept.
