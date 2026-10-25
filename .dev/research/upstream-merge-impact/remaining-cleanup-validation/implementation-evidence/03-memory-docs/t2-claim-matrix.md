# Task 2 claim matrix (live source, read 2026-10-24)

| Claim in the sample file or the guides | Live source / evidence |
|---|---|
| Sample rows use the fields the lookup reads: error_type, error_message, test_name (signature) and solution, root_cause, prevention (returned) | src/superclaude/pm_agent/reflexion.py:153-170, 206-215 |
| Each sample row is one valid JSON object with useful solution/root_cause/prevention, no old-layout keys, no credential or personal-data pattern, ISO timestamps, `"synthetic": true` | t2-sample-check.out (99 PASS, 0 FAIL) |
| Sample row 1 equals the guides' example row plus the synthetic marker | t2-sample-check.out (both guides) |
| The `synthetic` marker is written by nobody: the recorder appends only the dictionary it is given; the lookup builds its signature from three keys and ignores the rest | reflexion.py:127-132, 153-170 |
| The recorder does not validate the dictionary (so no schema-validation claim is made for the sample) | reflexion.py:110-136 |
| The guides' worked examples (9/10 = 0.90, 7/10 = 0.70, 6/12 = 0.50) are recomputed from sample row 1 | t2-sample-check.out; reflexion.py:235-244 |
| Behavioral check, separate from static parsing: the existing ReflexionPattern, pointed at an isolated copy of the sample under the evidence folder, matches the 0.90 and 0.70 pairs, rejects the 0.50 and JWT pairs, and reports 6 rows / 6 with solutions | t2-reader-smoke.out (7 PASS); storage rooted at t2-isolated/docs/memory, sibling t2-isolated/docs/mistakes (reflexion.py:78) |
| Production memory and mistake data and all code/guards are unchanged | t2-hash-compare.out (baseline-hashes.txt vs now, three docs files excluded) |
