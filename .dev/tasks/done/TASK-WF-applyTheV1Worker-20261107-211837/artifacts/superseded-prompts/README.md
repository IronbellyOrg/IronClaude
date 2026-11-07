# Superseded reviewer prompts

| Moved file | Old path | Flagged by | Replacing prompt |
|---|---|---|---|
| `T7-prompt-1-1.md` | `.dev/tasks/to-do/TASK-WF-applyTheV1Worker-20261107-211837/artifacts/retries/T7/prompt-1-1.md` | `FINAL: issues evidence=.dev/tasks/to-do/TASK-WF-applyTheV1Worker-20261107-211837/artifacts/retries/T7/prompt-1-1.md:95 state=992e180d9552480b1be9cd7d3866193b65039a201a051b38d51f31b186138783` | `.dev/tasks/to-do/TASK-WF-applyTheV1Worker-20261107-211837/artifacts/retries/T7/prompt-1-2.md` |

Why: `prompt-1-1.md` (95 lines) lacked the last two lines of the closed reviewer template. The recovery re-review r1-2 ran from the template-exact `prompt-1-2.md` (98 lines). That re-review found a confirmed blocker (F1.1 in `retries/T7/review-1.md`: `artifacts/ruff-format.log` ends in `exit=1`), so no new T7 complete line was appended and the archive stays blocked until the operator acts.
