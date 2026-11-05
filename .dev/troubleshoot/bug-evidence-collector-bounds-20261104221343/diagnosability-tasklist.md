# Diagnosability tasklist (informational; verdict partial, trivial)
discriminator-required: no
## Emitter search
- none required: both defects are observed directly by probe-evidence.out (EVIDENCE_FAIL token, elapsed seconds).
## Pending rows
- P-1: regression test, no `timeout` on PATH and a git read that hangs past the budget: expect `EVIDENCE_FAIL timeout` within the budget plus a small margin, no temp dir left, exactly one stdout line. re-run permitted: yes
- P-2: regression test / ref check, a restart attempt collects into a fresh per-attempt directory and succeeds. re-run permitted: yes
## Discriminator rows
- D-1 (timeout absent, read hangs): unfixed elapsed=65s exit=2 (probe-evidence.out:7-8); draft elapsed=61s exit=2 (probe-evidence.out post-fix section); P-1 test_without_timeout_a_hung_read_is_stopped_at_the_budget passed. Status: observed
- D-2 (timeout absent, no hang): test_without_timeout_a_normal_run_still_succeeds passed. Status: observed
- D-3 (timeout present, read hangs): test_a_command_hitting_the_time_bound_is_timeout passed (stub exit 124; token mapping only, no real wall-time hang). Status: observed (partial)
- D-4 (timeout present, no hang): E1-E3 success tests passed. Status: observed
