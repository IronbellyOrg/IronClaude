# Limit selection (Task 5) — measurements, rule evaluation, recommendation

# COMMAND USED (executor-added): D1/D4/D2/D3 per artifacts/d1-serial-idle.md:2, d4-xdist1-idle.md:2, d2-serial-loaded.md:2, d3-suite-auto.md:2; D5 via uv run pytest .dev/tasks/to-do/TASK-WF-remediationSou-20261108-061734/artifacts/d5-wrapper-probe.py -p no:xdist -q (times in d5-wrapper-times.txt)

## Measurements (all four cases: heredoc-git-words-64KB / backslash-lines-64KB / git-status-lines-64KB / 1MB-big)

| Condition | Median (ms) | Max (ms) | Worst 64 KB max |
|---|---|---|---|
| D1 serial idle | 526.5 / 510.4 / 761.1 / 451.0 | 675.9 / 605.0 / 893.9 / 544.1 | 893.9 ms |
| D4 xdist-1 idle (plumbing probe) | 520.2 / 503.5 / 745.3 / 449.0 | 627.4 / 592.5 / 840.2 / 541.1 | 840.2 ms (within noise of D1; xdist itself adds nothing) |
| D2 serial, 56 busy loops (2x oversubscription) | 1695.0 / 1694.3 / 2422.1 / 1614.8 | 4199.0 / 2991.6 / 5536.1 / 3828.5 | 5536.1 ms |
| D3 full suite -n auto, 28 workers on 28 CPUs (1x, CI-shaped) | 557.6 / 517.6 / 762.7 / 450.1 | 998.6 / 659.1 / 923.9 / 506.8 | 998.6 ms |
| CI pre-skip job log 128512582247 (assert active, 4 workers on 4 vCPUs = 1x) | 849.4 / n.a. / 716.1 / n.a. | 1082.7 / (passed) / 1166.0 / (passed) | 1166.0 ms |
| D5 10x wrapper, idle serial (seconds, one timing per case) | 5.234 / 5.245 / 7.620 / 4.495 | - | min 64 KB wrapper 5.234 s |

## Literal rule evaluation -> no-viable-limit

Rule (source.md as amended): smallest value that (a) is >= 2x the worst 64 KB max across D1-D3, (b) is exceeded by every 64 KB case's D5 wrapper time, (c) stays <= 2.5 s.

- (a) with D2 included: worst 64 KB max across D1/D2/D3 = 5536.1 ms -> required limit >= 11.072 s.
- (c) cap = 2.5 s. 11.072 s > 2.5 s -> no value satisfies (a) and (c) together.

outcome: no-viable-limit
Blocking numbers: D2 worst 64 KB max 5536.1 ms (git-status-lines-64KB, under 56 busy loops = 2x CPU oversubscription); 2x = 11.072 s > 2.5 s cap. Under that load three of the four case maxima exceeded 3.8 s (backslash-lines-64KB maxed at 2991.6 ms) and the worst exceeded 5.5 s, so no limit <= 5.0 s (the hook timeout itself) makes the 2x-oversubscription arm false-failure-free.

## Owner stopping-rule evaluation -> recommended LARGE_LIMIT_S = 2.5

Owner guidance: "Set up a much looser limit that will bring the risk down as close to zero until the diminishing returns are too much to warrant loosening it any more." The 56-loop arm is 2x oversubscription; no CI condition runs above 1x (CI: 4 workers on 4 vCPUs; local -n auto: 28 on 28). Treating the CI-representative arms as the noise the limit must clear (D1 idle 893.9 ms, D3 CI-shaped 998.6 ms, CI's own asserted pre-skip worst 1166.0 ms):

- (a') 2x the CI-representative worst = 2 x 1166.0 ms = 2332 ms <= 2500 ms. Margin of 2.5 s over CI's own worst observed failing max: 2500 / 1166.0 = 2.14x; over local CI-shaped worst: 2500 / 998.6 = 2.50x; over idle worst: 2500 / 893.9 = 2.80x.
- (b) every 64 KB wrapper exceeds 2.5 s: 5.234 s (2.09x), 5.245 s (2.10x), 7.620 s (3.05x). The exempt 1MB-big wrapper (4.495 s) also exceeds it, informationally.
- (c) 2.5 s = exactly half the 5 s hook timeout (design section 8), the cap all three Tier 2 lens cards converged on.
- Diminishing returns (why one more doubling is rejected): doubling to 5.0 s reaches the fail-open timeout (a run at 5 s is killed and the governed call goes ahead, design :216) and still does not clear the 2x-oversubscription arm (5536.1 ms > 5000 ms), so it buys ~zero additional false-failure protection where protection is possible, while halving sensitivity (a 2.5 s limit catches a uniform slowdown of about 2.9x over the CI median; 5.0 s would catch only about 5.9x). Intermediate values (3.0-4.0 s) add no CI-representative risk reduction (2.5 s already gives 2.14x over the worst number CI itself ever produced) and only delay the catch of a real regression.
- Residual risk, stated honestly: a CI runner slower than every observed one, or colocated contention beyond 1x, could still exceed 2.5 s. The 56-loop arm shows what 2x oversubscription does (6.2x the idle tail); if the coordinator wants the test to survive that regime, no honest limit exists and the guard's speed becomes the follow-up issue (GUARD_FOLLOW_UP at test :1011-1013).

recommended: superseded by the DECISION below.

## DECISION (coordinator, on behalf of the owner) — 2026-11-08, msg_ba1737055bfb / answer msg_b1de962c2c75

**LARGE_LIMIT_S = 3.5 s**, asserted on every run including xdist workers, implemented as one named constant. Rejected: 2.5 s (thin margin for unseen runner variance), the serial-CI-step fallback, and no-viable-limit-stop.

- Rule actually used (owner's stopping rule, not the plan's literal D1-D3 rule): "a much looser limit that brings the risk down as close to zero until the diminishing returns are too much to warrant loosening it any more". With nothing observed between CI's worst (1.166 s) and the 2x-oversubscribed arm (5.54 s), 3.5 s gives 3.00x margin over CI's own observed worst failing max (3500/1166), 3.50x over the local CI-shaped worst (3500/998.6) and 3.92x over the idle worst (3500/893.9), at almost no cost in sensitivity.
- 10x wrapper check at 3.5 s: every 64 KB wrapper still exceeds it (5.234 s = 1.50x, 5.245 s = 1.50x, 7.620 s = 2.18x); the exempt 1MB-big wrapper (4.495 s = 1.28x) also still exceeds it.
- Under the 5 s fail-open hook timeout with 1.5 s of margin; 5.0 s rejected (reaches the timeout, still does not clear the 2x-oversubscription arm, halves sensitivity), so the diminishing-returns stop is at 3.5 s.
- **Deviation from the plan's literal rule, stated plainly:** the plan's literal condition (a) (>= 2x the worst 64 KB max across D1-D3, i.e. >= 11.072 s including the 56-loop arm) was NOT met and cannot be met under any limit <= 5 s. The 56-busy-loop arm (2x CPU oversubscription, worst 5.54 s) is not a CI condition — CI runs 4 workers on 4 vCPUs, local `-n auto` runs 28 on 28, both 1x — and is treated as the contention-mechanism probe it was designed to be. This deviation was decided by the coordinator applying the owner's rule (decision recorded above, 2026-11-08).
- Residual risk: a CI runner under >1x oversubscription or unseen variance could exceed 3.5 s (the 56-loop arm shows 2x oversubscription produces maxima up to 5.54 s). If that ever fires, the guard's speed becomes the follow-up issue (GUARD_FOLLOW_UP at test :1011-1013).
- Revisit trigger: if any CI run shows T-SPD-5 above 2 s, re-measure.

final: LARGE_LIMIT_S = 3.5
