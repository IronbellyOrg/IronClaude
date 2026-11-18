# Coverage matrix (UC-1, Step 1B.0)

Spec: `.dev/tasks/to-do/TASK-WF-removeThePrdComm-20261117-200005/source.md:1` (one paragraph; no labeled requirement IDs, so Pass 1 found 0 rows).
Matching: Pass-2 rule of `refs/coverage-mapping.md` (case-folded content-word containment, threshold 0.6, stopwords removed, best single task). Script: run once in this session, output reproduced here.

| Row | source | Quote (source.md:1) | Best task | Containment | Mapped (>= 0.6) | Constraints-section containment |
|---|---|---|---|---|---|---|
| INF-001 | inferred | "`superclaude prd` is gone and `superclaude --help` does not list it" | Task 1 | 0.80 | yes | 0.40 |
| INF-002 | inferred | "the interactive prd skill still installs" | Task 8 | 0.50 | no | 0.75 |
| INF-003 | inferred | "no file outside the historical records names the removed pipeline" | Task 10 | 0.57 | no | 0.29 |
| INF-004 | inferred | "0 new test failures and the pass count drops only by the removed tests" | Task 9 | 0.62 | yes | 0.25 |
| INF-005 | inferred | "lint, format, verify-sync and git diff --check stay green" | Task 4 | 0.29 | no | 0.00 |

Result: parsed 0, inferred 5, mapped 2 of 5. `coverage_pct` (parsed-only) = null; `coverage_pct_union` = 0.40; `S_dev_density` (union) = 0.60.
