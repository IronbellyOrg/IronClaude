# Owner answers (dated record)

One row per answer the owner gave in this session. Only the owner writes or changes a row. A changed answer voids the unsent drafts and grants that rest on it (merged spec section 3, "Decision lifetime").

| Q | Date | Owner's words | What it settles | What it leaves open | What it does NOT authorize |
|---|---|---|---|---|---|
| Q1 (a) | 2026-11-13 | "Q1 = fix" | The git-config hole in the sweep's `git status` (INV-008) is to be fixed before PR #539 merges. Option F3 (accept the risk and caveat every "read-only" text) is off the table. | (a2) the fix shape: F1 neutralise the config channels, F2 refuse a worktree that defines them and report it as `unscanned`, or a stated combination. (b) the channel scope: `filter.<driver>.process`, `include.path` / `includeIf`, `GIT_CONFIG_*` and inherited environment, per-worktree config (all six measured on 2026-11-13 to run a command during the sweep's `git status`). | Any push, any edit to the allow-list or its tests, any merge. Those need their own grants (merged spec 6.8). It does not choose the code. |

Effect on the plan (from the merged spec): SW-01 (the ruling) is partly answered. SW-02 (the fix and its regression test) cannot start until (a2) and (b) are answered. TB-GIT (the git-safety gate on the #539 merge and on every sweep run) is satisfied only when SW-02's test lands and covers every channel the ruling puts in scope.
