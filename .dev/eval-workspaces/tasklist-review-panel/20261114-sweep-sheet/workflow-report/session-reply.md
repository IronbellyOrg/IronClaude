| Status | Result |
|---|---|
| DONE | Wrote the plan: 33 tasks in 7 phases covering DESIGN steps 1 to 13. It passed the format checks and a read of every file and symbol it names. |
| DONE | Ran the advisory plan review (reflect). Verdict: **FAIL**, two blocking defects, report status partial. |
| NEXT | You decide one design question (below). Then fix the plan before running `/sc:implement`. |

Plan: `.dev/tasks/to-do/TASK-WF-implementHomeCod-20261114-200449/TASK-WF-implementHomeCod-20261114-200449.md`
Review report: `.dev/reflect/pre-TASK-WF-implementHomeCod-20261114-200449-20261114201211/REPORT.md`

The two blocking defects:
- **Single class fills 12 items (design contradiction):** `DESIGN.md` keeps only the top 8 candidates per class (line 316) but also says one triggered class can fill 12 (lines 321, 325). Task 19 copies "12", so its test cannot pass.
- **`git add` check (plan error):** the Task 27 check `grep "git tag\|git commit\|git add" SW/bin` fails any faithful sandbox builder, because the builder runs `git add` and a commit. Task 33 never re-runs the check.

Non-blocking findings:
- The `/tmp` override guard would refuse `SW_KILL_S=1`.
- Some test assertions and fixtures are not created by any task.
- Sub-step 0.5 is not folded into any task.

**Decision for you:** when only one class triggers, should the pre-pass attach evidence to the top 12 candidates (instead of 8) so the sheet can hold 12? I recommend yes: it is the smaller change, and the attach cost is bounded at 12 lookups. I have not measured its effect on the time budget. If you say yes, `DESIGN.md`, `TESTING.md:87` and `:190`, the `values.json` K entry, and Tasks 11 and 19 change together.

The review checked 74 citations and dropped one false claim. Both reviewers were of the same model class (the debaters were opus), so their agreement counts for less than it looks. The review never edits the plan, so every fix is yours to apply.

Outside the plan package:
- `.dev/reflect/pre-.../` holds the review artifacts (not gitignored).
- `docs/memory/reflect/deviation-patterns-eval-tasklist-review-panel.md` is a new untracked file in a tracked folder. This is the review's standard memory write.
- `.superclaude/memory/reflect/last-pass-...` and the `runs.jsonl` line are gitignored.

Nothing is staged. I left `.dev/tasks/` unstaged because your prompt says nothing is staged by the build, but the repo rule is that it is always staged. Stage the package with `git add .dev/tasks`.

RUNS: plan, source snapshot, return contract, review report. NOT BUILT: any step of the plan itself; plan generation does not implement it.
