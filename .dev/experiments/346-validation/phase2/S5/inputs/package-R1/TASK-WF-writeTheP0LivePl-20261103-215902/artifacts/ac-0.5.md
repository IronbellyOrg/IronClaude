# AC-0.5: launch time of the first worker (live check 1, /sc:troubleshoot)

Source: `./artifacts/lc1-step1.txt` and `./artifacts/lc1-worker-start.json`.

| Field | Value | Where |
|---|---|---|
| worker-start exit code | 0 | `lc1-step1.txt:3` |
| `state` | `ready` | `lc1-worker-start.json:8` |
| `stage` / `turnStart` | `input_accepted` / `observed` | `lc1-worker-start.json:9-10` |
| Elapsed seconds (`date +%s.%N` before and after worker-start) | 41.995 s (t0 = 1793772142.380195195, t1 = 1793772184.374752090) | `lc1-step1.txt:4-5` |
| Requested launch | agent `claude`, model `null`, effort `null` | `lc1-worker-start.json:21-24` |
| Effective launch | agent `claude`, model `null`, effort `null` | `lc1-worker-start.json:26-29` |
| Mode | `terminal` (reason `user_default`) | `lc1-worker-start.json` (`mode`) |
| Orca `timeoutMs` for the start | 60000 | `lc1-worker-start.json:37` |

Limit: worker-start exits 0 with `state: ready` in under 45 s.

Verdict: **PASS** (exit 0, `state: ready`, 41.995 s is under 45 s).

Margin note: the margin is 3.0 s. Only one launch was measured; the measured time includes Orca creating the terminal and accepting the dispatch prompt (`stages: input_accepted, turn_started`).
