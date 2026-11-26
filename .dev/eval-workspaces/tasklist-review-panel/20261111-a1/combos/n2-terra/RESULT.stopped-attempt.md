# n2-terra RESULT (Batch 3 re-run): STOPPED, INVALID, no merge

Row: t2b-1=muse-wonder-1.0, t4-1=claude-haiku-5-5, t4-2=grok-4.7, t2-1=gpt-6.1-terra.

## Why it stopped
Per the SPEC re-run rule ("if any reviewer fails the observed-model check twice, STOP that worker and report it ... do not silently drop a base reviewer"):
the muse-wonder-1.0 slot (t2b-1) failed the observed-model check on both attempts on the first package, TASK-WF-designSpec-20261107-075614.
- attempt 1: observed gpt-6.1-terra, 20 s, 406 output tokens
- attempt 2: observed gpt-6.1-terra, 16 s, 372 output tokens
- stderr of attempt 1: `[claude-code:unrecognized_model] {"model":"muse-wonder-1.0"}`. The gateway served terra for the muse request again, even with only one run of mine active.
- Output was also thin/incomplete ("source.md missing" incomplete report).

Driver was run sequentially (1 reviewer at a time). It moved on to t4-1 (haiku) before I killed it; that run was aborted after seconds and produced only t4-1.attempt1.json/.err (partial, unusable). No other reviewer completed; the other two packages were not started.

## Per-package tables

### TASK-WF-designSpec-20261107-075614
| reviewer | model | observed model | attempts | wall s | output tokens | flag | findings (blocking) |
|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | gpt-6.1-terra | 2 | 36 | 778 | INVALID (observed model mismatch x2) | n/a |
| t4-1 | claude-haiku-5-5 | not run (aborted) | 0 | - | - | NOT RUN | n/a |
| t4-2 | grok-4.7 | not run | 0 | - | - | NOT RUN | n/a |
| t2-1 | gpt-6.1-terra | not run | 0 | - | - | NOT RUN | n/a |

merged-1.md: INVALID, reason above (muse slot contaminated; degraded panel not merged).

### TASK-WF-makeTheAliasOnly-20261105-051649
Not started. merged-1.md: INVALID (worker stopped).

### TASK-WF-design-20261108-041415
Not started. merged-1.md: INVALID (worker stopped).

Total wall / tokens: designSpec 36 s / 778 tokens (invalid only); others none.

No scoring. Files are under .../designSpec package reviews/combos/n2-terra/ (t2b-1.attempt1/2.*).
