# Claim mode (`/sc:issue --claim <number|url>`)

Loaded at the start of claim mode. `<R>` is the origin repo (`owner/repo`), `<N>` the issue number, `<D>` = `.dev/issues/<N>/`, `<skill base>` the directory that holds this skill's `SKILL.md`.

Spawn workers with `subagent_type: issue-worker-t<N>` and never pass the `model` parameter.

Workers are `~/.claude/agents/issue-worker-t3.md`, `~/.claude/agents/issue-worker-t2.md` and `~/.claude/agents/issue-worker-t1.md` (Claude Code reads the project `.claude/agents/` copy first when one exists). Load `refs/tiers.md` before the first spawn. A worker that needs a codebase pass runs `/sc:analyze` by following `~/.claude/commands/sc/analyze.md` (project `.claude/commands/sc/analyze.md` in a checkout). Every file under `<D>` starts as a copy of its template under `templates/`.

Every GitHub CLI call on issues, pull requests or labels passes `--repo <R>`; every `gh api` path is `user` or starts with `repos/<R>/`, never a brace placeholder. Only the orchestrator writes to GitHub or ClickUp.

## Wave 0: prerequisites (orchestrator)

1. Resolve `<R>` and `<N>` in one call:
   `uv run --no-project python "<skill base>/scripts/origin_repo.py" --claim "<argument>"`
   It reads only the `origin` remote and prints `{"repo": "<owner/repo>", "number": <N>}`. Exit 1 = STOP `E-NO-ORIGIN` (no `origin`, or not a GitHub URL). Exit 3 = STOP `E-FOREIGN-REPO` (a URL naming any repo other than origin, B10). Exit 4 = STOP `E-NOT-AN-ISSUE` (a `/pull/<N>` URL, or not an issue number or URL). Print the script's stderr line with the STOP.
2. `gh auth status` must succeed; else STOP `E-GH-AUTH`.
3. Orca check: `uv run --no-project python "<skill base>/scripts/orca_worktree.py" preflight`. It prints `{"ok": true}` or `{"ok": false, "detail": "..."}`. `ok: false` is STOP `E-ORCA-REQUIRED`: print "/sc:issue --claim needs Orca running; start Orca and re-run" and then the script's `detail`. This is the only Orca call before Wave 7.
4. Resolve the default branch `<B>` with `gh repo view <R> --json defaultBranchRef -q .defaultBranchRef.name` (the repo is named explicitly).
5. Create `<D>`.

No GitHub or ClickUp write happens before Wave 3, and none happens before the Orca check passes.

## Wave 1: lookup (issue-worker-t3, B13)

Spawn `issue-worker-t3` before doing any lookup yourself, with the job "claim lookup", `<R>`, `<N>`, `<B>` and `<D>`. The worker:

- runs `gh issue view <N> --repo <R> --json number,title,body,state,assignees,labels,comments,createdAt,url,author` and `gh api user -q .login`;
- lists pull requests merged since `createdAt` with `gh pr list --repo <R> --state merged --search "merged:>=<createdAt date>" --limit 200 --json number,title,mergedAt,files,url` (gh's default limit is 30) and records in `scout.md` whether the result reached the 200 limit;
- runs `git fetch origin` (origin only; no other remote is added or fetched), then `git log --since=<createdAt> --name-only origin/<B>` for the recent commits on the default branch;
- finds an earlier claim by this user: a comment authored by the current login whose body contains `<!-- sc:issue:claim -->`, and likewise `<!-- sc:issue:accuracy-check -->`. The comment ID used for editing is the number after `#issuecomment-` in that comment's `url`. When more than one comment carries the same marker, the latest one is used;
- writes `<D>/scout.md` from `templates/scout-report.md` (claim section): state, `url`, `is_pull_request` (true when `url` contains `/pull/`), assignees, current login, earlier comment IDs, the merged pull requests and changed files since creation and whether that list was truncated, a first complexity guess (`simple|medium|complex`) and a type guess (`feature|bug`), each with a one-line reason;
- returns the path.

Worker returns no file or an empty one: retry that worker once, then STOP `E-WORKER-NO-OUTPUT` naming `<D>/scout.md`.

## Wave 2: edge cases (orchestrator reads `<D>/scout.md`)

Checked in this order; every STOP here makes no GitHub or ClickUp write (B9):

1. `is_pull_request` is true -> STOP `E-NOT-AN-ISSUE`: "#N is a pull request, not an issue; not claimed."
2. `state` is `CLOSED` -> STOP: "Issue #N is closed; not claimed."
3. Assigned to anyone other than the current login -> STOP: "Issue #N is assigned to @<login>; not claimed."
4. Already assigned to the current login -> continue (re-claim is allowed and idempotent).
5. Earlier claim or accuracy-check comment IDs present -> remember them; Wave 6 edits those comments instead of posting new ones (B9, D18).

## Wave 3: assign (orchestrator)

1. `gh issue edit <N> --repo <R> --add-assignee @me`. Failure -> STOP `E-ASSIGN-FAILED`; ClickUp is not touched and no comment is posted.
2. Run the ClickUp script and write its stdout to `<D>/clickup.json`:
   `uv run --no-project python "<skill base>/scripts/clickup_claim.py" --issue-url <url> --issue-number <N> --repo <R> > "<D>/clickup.json"`
   Every outcome it prints (`assigned`, `already_assigned`, `skipped`, `not_found`, `ambiguous`, `error`) is non-fatal and is reported in the claim comment. `error` with reason `page_cap` means the search reached `CLICKUP_MAX_PAGES` before the last page, so nothing was assigned; the claim comment says so and names the remedy (raise `CLICKUP_MAX_PAGES` or set `CLICKUP_LIST_IDS`). Exit 2 means the skill passed bad arguments: STOP and print the script's usage message; the GitHub assignment stays. Never print, echo or inline `CLICKUP_API_TOKEN`.

## Wave 4: accuracy check and summary

Spawn `issue-worker-t2`, or `issue-worker-t1` when `scout.md` sizes the issue `complex` (default D8), with the job "accuracy check and summary", `<R>`, `<N>` and `<D>`. The worker assumes the issue text is out of date and:

- checks each concrete claim in the issue body and comments (paths, symbols, behaviours, flags) against today's code, and checks each merged pull request and changed file from `scout.md` for relevance;
- writes `<D>/accuracy-check.md` from `templates/accuracy-check-comment.md` with the verdict `current` or `out_of_date` and the evidence for each changed claim;
- when `out_of_date`: runs `/sc:analyze` on the paths the issue touches (`--depth deep` when complex, no `--depth` otherwise) and saves the report as `<D>/analysis/analyze-<scope>.md` (`<scope>` in this file name is the last segment of the main path the issue touches; no file under `<D>/analysis/` has a name that starts with analysis, report, summary or findings);
- always writes `<D>/issue-summary.md` from `templates/issue-summary.md`: what the issue asks for, the relevant files and systems (the cheatsheet), type, complexity, the effort estimate in hours using the rubric below (B3), and links to anything under `<D>/analysis/` (default D22);
- returns both paths.

Missing or empty file: retry the worker once, then STOP `E-WORKER-NO-OUTPUT` naming the missing path.

### Effort and complexity rubric (default D5)

| Complexity | Rule |
|---|---|
| simple | up to 4 hours of work in one area |
| medium | over 4 and up to 16 hours |
| complex | over 16 hours, or more than one subsystem, or a security or data-migration change |

Effort is always recorded in hours.

## Wave 5: next steps (orchestrator)

Load `refs/chains.md`.

1. Invoke `Skill sc-recommend` with the goal format of `refs/chains.md`: issue URL, type, complexity, the summary path and the default chain row for that type and complexity as the suggested route. `/sc:recommend` picks the starting chain and depth (B4). Save its output verbatim to `<D>/recommend.md` from `templates/recommend-record.md`.
2. Write `<D>/next-steps.md` from `templates/next-steps.md`: the `/model` tier line first (simple -> `claude-gw-tier2`, medium and complex -> `claude-gw-tier1a`, default D6), then the commands in order with their flags and the inputs each needs (`@.dev/issues/<N>/issue-summary.md`), the effort estimate, and, when `/sc:recommend` chose differently from the default row, one line naming the default row and why it was not used (default D23). When `/sc:recommend` asks a question or finds no route, record that in `recommend.md` and use the default row, saying so.
3. Set the plan boundary. `next-steps.md` carries the line `Plan boundary: after step <K>` under its title. `<K>` is the number of the last step before the first step whose command is `/sc:implement` or `/task` (default D7); when the first step is itself the implementation step the line reads `Plan boundary: before step 1`. Level `worktree` stops there until a human approves; `--pipeline full` ignores the line.
4. Render the launch prompt, for `--pipeline` `worktree` or `full` (not `none`): `uv run --no-project python "<skill base>/scripts/orca_worktree.py" prompt --template "<skill base>/templates/launch-prompt.md" --level <L> [--submit] --number <N> --repo <R> --out "<D>/launch-prompt.md"`, where `<L>` is the `--pipeline` value. It is written before Wave 7 so the copy into the worktree carries it. When `<D>/worktree.json` already has a `launch` entry (a re-claim after an agent was launched), do not rewrite `<D>/launch-prompt.md`: the running agent reads it.
5. Do not run any of the steps of `next-steps.md` (B2): the launched agent runs them, at the level the user chose.

## Wave 6: post (orchestrator, directly, B1)

1. Accuracy-check comment, body `<D>/accuracy-check.md` (it ends with `<!-- sc:issue:accuracy-check -->`). If Wave 2 remembered an earlier accuracy-check comment ID, edit it:
   `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<D>/accuracy-check.md`
   otherwise post a new one:
   `gh issue comment <N> --repo <R> --body-file <D>/accuracy-check.md`
2. Claim comment: write `<D>/claim-comment.md` from `templates/claim-comment.md`: who claimed it, the ClickUp result from `clickup.json`, the summary overview, effort estimate, complexity, accuracy verdict, the first next step, and repo-relative links to `<D>/issue-summary.md`, `<D>/next-steps.md` and `<D>/analysis/` with the one-line note that they open on GitHub only after someone commits and pushes the files (default D9). It ends with `<!-- sc:issue:claim -->`. Edit the earlier claim comment with `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<D>/claim-comment.md`, or post it with `gh issue comment <N> --repo <R> --body-file <D>/claim-comment.md`.
3. A post or edit that fails -> STOP `E-POST-FAILED`; the files stay in `<D>`, and a re-run edits rather than duplicates because of the markers.
4. After both comments are posted, run Wave 7, then Wave 8. A STOP anywhere in Waves 0 to 6, including `E-POST-FAILED`, means no Orca call after the Wave 0 check. Do not stage or commit `.dev/issues/` (default D24).

## Wave 7: worktree (orchestrator, no worker)

Runs for every `--pipeline` value, after both comments are posted:

`uv run --no-project python "<skill base>/scripts/orca_worktree.py" worktree --repo <R> --number <N> --base origin/<B> --source <D>`

Read the one JSON object it prints: `status` (`created`, `reused` or `failed`), `path`, `branch`, `match_key`, `warning`, `detail`, `tracked_files` and `tracked_known`. Every failure is a warning, never a STOP: the assignment and the comments cannot be undone, so the claim `status` stays `success`. The script copies `<D>` into `<wt>/.dev/issues/<N>/` (it never copies `worktree.json`) and writes `<D>/worktree.json`. The skill itself runs no `git worktree` command and no other `orca` command here. Remedy lines of the worktree warning codes (printed in the final output below):

| Code | Remedy line |
|---|---|
| `W-ORCA-LIST-FAILED` | check Orca, re-run the claim |
| `W-ORIGIN-BASE-MISSING` | `git fetch origin`, re-run |
| `W-ORIGIN-BASE-STALE` | `git fetch origin`, rebase in `<wt>` |
| `W-WORKTREE-CREATE-FAILED` | re-run; a finished create is reused |
| `W-WORKTREE-AMBIGUOUS` | remove the extra worktrees, re-run |
| `W-WORKTREE-STALE` | `git worktree prune`, then `orca worktree rm` |
| `W-WORKTREE-COPY-FAILED` | copy the named files by hand |

## Wave 8: launch (orchestrator, no worker)

Runs only when `--pipeline` is not `none` and the Wave 7 `status` is `created` or `reused`. It is never attempted for a `failed` worktree, and never for `none`.

`uv run --no-project python "<skill base>/scripts/orca_worktree.py" launch --number <N> --source <D> --level <L> [--submit]`

Read the one JSON object it prints: `status` (`launched`, `already_launched` or `failed`), `warning`, `detail`, `terminal`, `launched_at`, `enforcement_hook` and `hand_command`. The script starts one agent behind the ccsession shim in the worktree and records the level where the enforcement hook of issue 394 can read it. A `launch` entry in `<D>/worktree.json` makes it return `already_launched` without calling Orca. Every failure is a warning, never a STOP: the claim `status` stays `success`. Remedy lines of the launch codes:

| Code | Remedy line |
|---|---|
| `W-LAUNCH-FAILED` | re-run the claim; the hand command is printed for reference (an agent started by hand is not governed by the hook) |
| `W-LAUNCH-NOT-CCSESSION` | this agent is NOT behind the ccsession shim, or could not be verified; close it. Orca's Claude command must be the ccsession-orca wrapper |
| `W-ENFORCEMENT-ABSENT` | the level is an instruction in the prompt only until the launch-level hook (#394) ships; do not use `full` or `--submit` on a real issue yet |

## Final output (replaces "print the path and STOP")

Print, in this order:

1. The `next-steps.md` path, then `Worktree: <path> (<status>)`, adding `, matched by <match_key>` when `match_key` is not null (a newly created worktree has none). For `match_key` `basename` or `branch` add "reused a worktree not created by /sc:issue". For `record` after `W-ORCA-LIST-FAILED` add "unverified: Orca could not be listed".
2. "`.dev/issues/<N>/` in the worktree is untracked: do not stage it" only when `tracked_known` is true and `tracked_files` is empty. When `tracked_known` is false, print nothing about tracking. Add "run `make sync-dev` there first" when `<wt>/.claude/` is absent and a step of `next-steps.md` needs a primitive that is not synced into the worktree.
3. The launch result:
   - `launched`: "Agent launched in <wt> (level <L>[, submit]). It stops at the plan boundary and waits; reply `approved` in its tab to let it continue." For `full`: "It runs every step and stops after implementation." For `full` with `--submit`: "It then commits, pushes <branch> and opens the PR through /sc:pr-submit; it never merges."
   - `already_launched`: "agent already launched at <launched_at>" plus the script's `detail`, which names the two files that hold the `launch` entry (`<D>/worktree.json` and a file in the worktree's git directory); the user removes the entry from both to launch again.
   - `--pipeline none`: "No agent launched. Open <wt> and run .dev/issues/<N>/next-steps.md there."
4. Every warning, the worktree one first: the code, its `detail`, and its remedy line from the two tables above. For `W-LAUNCH-FAILED`, also print the launch JSON's `hand_command` when it is not null (the remedy line promises it), and tell the user that an agent started by hand is not governed by the enforcement hook.
5. The return contract (`SKILL.md`) and STOP.
