# Reflect deviation patterns - issue-339-orchestrator-mode

## reflect-post-20261112T192600Z-TASK-RF-sweep-phase1 (UC-2, sweep Phase 1)
- Verdict: PASS-with-deviations (tier 2, convergence 1.00, calibrated 0.67). 1 contested regression, 11 drift, 4 authorized, 1 necessary; no blocking finding.
- Recurring pattern: **the SPEC names a mechanism, the DESIGN names only the result, the code takes the shortcut, and nobody records it.** SPEC section 8 asked for Popen with chunked reads and a kill at 8 MiB and the code used subprocess.run with an after-the-fact check; the plan item's stated reason (the test guard only catches run) was false because the guard patches Popen too. Same family: ledger head+tail read vs tail only. Check mechanism sentences in the SPEC against the code, not only the result sentences.
- Recurring pattern: **test names claim more than they assert** (`..._still_publish` stops at render; `..._read_as_head_and_tail` asserts a tail value; an FR-010 case passes the flag directly). Read test bodies for the rows a design says a test pins.
- Recurring pattern: **a decision record updates one document and leaves its siblings stale** (DESIGN header and Open Questions still PENDING after the owner decisions; DESIGN section 13 not told about the inert Rule 5). Check status lines after every owner decision.
- Reviewer behaviour: haiku and sonnet graded static-only readings as Regression/blocking; both blind calibrators and the debate lowered them. A Regression label needs a contradicted criterion or an explicit constraint with an observable difference.
- Process: a sonnet reviewer hit its 50-turn limit with no card; resuming it with "return the YAML now" worked.
