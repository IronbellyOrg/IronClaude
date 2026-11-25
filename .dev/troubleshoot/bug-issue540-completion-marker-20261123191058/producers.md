observation-kind: trace

## Producers

| id | line | statement | exit statement | before/after started marker | wall-time compatible | cheap observable | surviving=yes/no |
|---|---|---|---|---|---|---|---|

## Enumeration scope
The symptom is a missing filesystem artifact, not an ambiguous emitted enum/status token. The primary failing datum is the independently observed done_exists=false after CLI exit. Categorical-token producer enumeration therefore does not apply; zero producer rows and no exclusion claims. Write boundaries inspected directly: reduce.emit_done_sentinel (normal validated marker), commands._emit_killed_done_sentinel (operator kill only). Completion continuations are run_cmd and _run_resume_branch, with detached invoking run_cmd in its child. No independent passing CLI arm or CONTROL-PROOF is claimed.
producer-count: not_applicable (trace)
grep-hit-count: not_applicable (not a categorical token enumeration)
discriminator-required: no (missing artifact state directly captured, no competing token producers)

