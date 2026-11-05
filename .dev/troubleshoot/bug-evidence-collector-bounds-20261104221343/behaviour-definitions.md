| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | bash foreground command without `timeout` | the shell waits for the command to return; SECONDS checks run only after it | observed in this run (probe-evidence.out:7, elapsed=65s > 60 s budget) | n/a (observed) | observed:probe-evidence.out:7 |
| 2 | collect-conflict-evidence.sh --out rule | a non-empty --out fails EVIDENCE_FAIL out_not_empty, exit 2 | observed in this run | n/a (observed) | observed:probe-evidence.out:4-5 |
| 3 | bash `kill -0 <pid>` / `kill <pid>` | `kill -0` tests that the process exists without signalling; `kill` sends TERM | bash builtin (not fetched; used by the proposed fix, verified by its regression test) | n/a | unobserved:verified by fix test P-1 |
