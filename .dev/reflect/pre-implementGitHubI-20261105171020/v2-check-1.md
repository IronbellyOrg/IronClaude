# Fresh check 1 of the corrected plan (version 2): condensed record

Checker: reflect-reviewer agent, opus class, read-only, fresh context (not the plan author). Subject: the first draft of `.dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-184607/TASK-WF-implementGitHubI-20261105-184607.md` (10 tasks). The checker's full YAML was returned as a message; this file keeps its verdicts and findings, condensed. Nothing was executed; every claim is reasoned from the code.

## Verdict: FAIL (1 blocking, 6 minor new findings); all ten original findings fixed except M-F10 (partly)

Part 1 (original findings): M-F1 to M-F9 fixed and the fixes work against the real code; M-F10 partly (the D08 clause fix is right; the new citation `ccsession:109-114,124` would be stale after the header edit). All six user-accepted defaults are in the plan and work against the code.

New findings and how the plan was changed (second draft, 9 tasks):

| ID | Severity | Finding | Change made |
|---|---|---|---|
| NF-1 | blocking | Task 5's green and isolation criteria need Task 1's `--help` text test, which can only pass after Task 6 adds the header text; Task 5's diff rule forbade that edit. | Header text merged into Task 5 (edit a: flag-default block; edit b: header text); diff rule widened to those two regions; old Task 6 removed. |
| NF-2 | minor | "Line 109 still starts with ..." cannot hold after inserting lines above it. | Criterion now: `grep -n '^# The wrapper always runs'` finds exactly one line and `show_help` is unchanged. |
| NF-3 | minor | Line numbers (124, 1652, 109) go stale after the edits; Task 8 would write a stale citation again. | Constraints say "line 124 before this plan"; guides cite line numbers found with `grep -n` after Task 5; Task 8 depends on Task 5. |
| NF-4 | minor | `_run_ccsession` uses `cwd=tmp_path/"work"` but never creates it. | Helper creates `work` and `home` with `mkdir(parents=True, exist_ok=True)`. |
| NF-5 | minor | The docs claim caller flags, add-on profile and env-file flags still apply; no test covers them. | Two tests added to Task 1 (caller-passed `--dangerously-skip-permissions` via `--claude-args`; env-file `CC_CLAUDE_FLAGS`); add-on profile mentions removed from the docs and Goal. |
| NF-6 | minor | The usage entry sat inside the "Coder workspaces (tier mode)" block, and wording with `--tier tier0` would break existing help tests. | Entry goes after "In tier mode --profile is not used...", before `ccsession --refresh-models`; text must avoid `--tier tier`, `--tier tier0`, `--tier tier1a`. |
| NF-7 | minor | Task 4 said "passes before and after Task 5" but runs before Task 5. | Task 4 checks "before"; Task 5's isolation log proves "after". |

Not checked by the checker: no test, `bash -n`, `--help` or `git diff` was run; hooks and orca behavior under a bad value beyond the cited lines; Makefile `sync-dev` and `verify-sync` coverage of the ccsession skill.
