## Position summary
Variant 2 is the right readiness call. The spec says every acceptance bullet must fail a wrong edit (`source.md:38`). As written, Task 5, Task 6, and Task 8 can pass a bad edit, and Task 6's stub can fail a correct one. That is not ready. Variant 1 found two of those holes and missed the README one.

## Steelman of Variant 1
Variant 1's best point is that the plan's shape is already decided and disclosed, so the defects are acceptance bullets, not a new user gate. `source.md:35` and `source.md:44` already say one paragraph and change nothing else. The tasklist records the contradictory neighbors as leftovers (`TASK-WF-spec-20261022-211556.md:26`, `:150`). Variant 1 also caught failure modes Variant 2 missed: the `::warning` check never requires advisory wording (`TASK-WF-spec-20261022-211556.md:90`), the sync step never diffs the unchanged `run:` body including `git add -f docs/.framework-sync-commit` (`pull-sync-framework.yml:103-109` vs `TASK-WF-spec-20261022-211556.md:112-113`), a throwaway repo on `main` breaks Task 4 (`TASK-WF-spec-20261022-211556.md:67`), and a non-ancestor `BASE_SHA` makes a correct Task 5 render fail (`TASK-WF-spec-20261022-211556.md:84`, `:94`).

## Strengths claimed (numbered, with citations)
1. Task 8 passes a wrong README. The boundary paragraph only needs the word `advisory`, and the sync paragraph only needs `sync/framework` and `pull request` (`TASK-WF-spec-20261022-211556.md:143`). A sentence that still says the job blocks merges passes. The badge check never requires `test.yml` (`TASK-WF-spec-20261022-211556.md:141`); the instruction does (`TASK-WF-spec-20261022-211556.md:135`, `source.md:34`). Today the badge still points at `SuperClaude-Org` (`/.github/workflows/README.md:30`) and the boundary blurb never says it cannot block (`/.github/workflows/README.md:35`).
2. The Task 6 stub replaces `git` (`TASK-WF-spec-20261022-211556.md:114`), but the step also runs `git config`, `git add`, `git diff --cached`, and `git commit` (`pull-sync-framework.yml:89-109`). A log-only `git` fails a correct script. The stub must exec real git for every subcommand except `push`.
3. Header and summary checks are pinned to line slices (`TASK-WF-spec-20261022-211556.md:88`, `:91`). The gating sentence is exactly lines 19-20 and item 3 is lines 66-67 (`boundary-guard.yml:19-20`, `:66-67`). Moving `gates` or `branch protection must require` onto the next line passes.
4. Later tasks tell the executor to run placeholders. `<decided file input>` is still in the Codecov check (`TASK-WF-spec-20261022-211556.md:124`), and `<t1-head>` is never defined as `./artifacts/t1-head.txt` (`TASK-WF-spec-20261022-211556.md:39`, `:87`). A literal command fails a correct edit.
5. `Depends on` must be a real chain (`source.md:40`). Codecov research does not gate the GitHub API check or the throwaway proof (`TASK-WF-spec-20261022-211556.md:53`, `:65`). Task 7 needs Task 2's `Decision:` line (`TASK-WF-spec-20261022-211556.md:49`, `:121`), not Task 6 (`TASK-WF-spec-20261022-211556.md:119`).
6. The backslash check is not a runnable bullet. `grep -c '\\`'` sits inside a broken code span (`TASK-WF-spec-20261022-211556.md:94`). If the executor skips it, a render that still has a backslash before a backtick passes, which `source.md:24` and `source.md:38` forbid.

## Weaknesses in Variant 1 (numbered, with citations)
1. It never looks at Task 8. Keyword checks at `TASK-WF-spec-20261022-211556.md:141-143` fail the same "wrong edit still passes" rule Variant 1 applies to Task 5.
2. It calls the dependency lines optional (`source.md:40` says real chains). Task 7 depending on Task 6 (`TASK-WF-spec-20261022-211556.md:119`) misstates the real predecessor, which is Task 2.
3. `ready_with_notes` treats `source.md:38` as a note. An executor who follows the bullets can drop the state-file add (`pull-sync-framework.yml:103-104`) and still pass Task 6 (`TASK-WF-spec-20261022-211556.md:113`).
4. It stops the placeholder fix at `<t1-head>` and misses `<decided file input>` (`TASK-WF-spec-20261022-211556.md:124`).

## Concessions
Variant 2 missed the two highest-cost false passes: the warning bullet does not require advisory text (`TASK-WF-spec-20261022-211556.md:90`), and Task 6 never compares the unchanged commit body, `if`, `working-directory`, or `--base`/`--head` (`TASK-WF-spec-20261022-211556.md:112-113`, `source.md:11-13`). It also missed `git init -b master` plus a commit identity (`TASK-WF-spec-20261022-211556.md:67`) and the non-ancestor render SHA (`TASK-WF-spec-20261022-211556.md:84`). Asking the user before Task 9 reopens a decision `source.md:35` and `source.md:44` already closed; disclose it, do not block on it. Calling the 300-vs-3000 note a "session report" names no artifact. `INF-045` as partial with no location is a gap, not a partial. Medium on the broken grep span was too high if a careful executor can still recover the count.

## Shared assumptions (A-001..A-004: ACCEPT|REJECT|QUALIFY + reason)
- A-001 QUALIFY. Task 3 already says a failed `gh api` blocks Fix 1 and does not change the setting (`TASK-WF-spec-20261022-211556.md:55-58`). Auth is still unstated, so a missing token and a real `false` look the same unless the log keeps the raw error.
- A-002 QUALIFY. Tasks 5-7 require `uv run python` to import PyYAML (`TASK-WF-spec-20261022-211556.md:87`, `:111`, `:124`). This pass did not confirm that import, so a missing module fails a correct edit.
- A-003 QUALIFY. The pytest bullet (`TASK-WF-spec-20261022-211556.md:95`, `source.md:22`) only supports "the edit is safe" if that test already passed on `a88f100b`. Neither card ran it.
- A-004 QUALIFY. No high finding is fair. "Structure is sound, so only notes" is not. `source.md:38` makes a bullet that passes a wrong edit a gate, and three tasks have one.

## Per-point positions (table: point | winner V1/V2/tie | one-line evidence)
| Point | Winner | Evidence |
|---|---|---|
| S-001 | tie | Variant 1 splits more failure modes; Variant 2 keeps one claim per finding, which is the cleaner classification. |
| S-002 | V1 | Absolute paths re-check without guessing package vs worktree; both still hit the same lines. |
| C-001 | V2 | `TASK-WF-spec-20261022-211556.md:94` is not a command an executor can copy, so the `source.md:24` check can be skipped. |
| C-002 | V1 | Both require real git for non-push (`pull-sync-framework.yml:89-109`); only Variant 1 also sets `GITHUB_REPOSITORY`, `bash -eo pipefail`, and a clean third-run index. |
| C-003 | V2 | `sed -n '19,20p'` and the two-line item 3 (`TASK-WF-spec-20261022-211556.md:88`, `:91`) pass if the forbidden phrase wraps past `boundary-guard.yml:20` or `:67`. |
| C-004 | V2 | Variant 1 defines `<t1-head>` only; `<decided file input>` is still literal at `TASK-WF-spec-20261022-211556.md:124`. |
| C-005 | V2 | `source.md:40` wants real chains; Task 7's predecessor is Task 2 (`TASK-WF-spec-20261022-211556.md:121`), not Task 6 (`:119`). |
| C-006 | V1 | `source.md:35` and `:44` already forbid editing the neighbors; `TASK-WF-spec-20261022-211556.md:26` and `:150` already disclose them. |
| C-007 | V1 | `source.md:47` needs a quote plus a user question; Task 3 and `t9-leftovers.md` exist, and Variant 2's "session report" does not. |
| C-008 | tie | Variant 1 owns the warning and unchanged sync body; Variant 2 owns Task 8 (`TASK-WF-spec-20261022-211556.md:141-143`). Neither covers the other. |
| X-001 | V2 | `source.md:38` is a gate. Bullets at `TASK-WF-spec-20261022-211556.md:90`, `:113`, and `:143` can pass a wrong edit, so `not_ready` beats `ready_with_notes`. |
| X-002 | V1 | The one-paragraph scope is a decision (`source.md:35`, `:44`), not an open question. |
| X-003 | V1 | `INF-041` partial is fair, but `INF-045` partial with no location hides a real gap (`source.md:47`). |