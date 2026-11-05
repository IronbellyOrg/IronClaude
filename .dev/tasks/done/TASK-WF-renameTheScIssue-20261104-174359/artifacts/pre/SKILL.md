---
name: sc:issue-protocol
description: "Behavioral protocol for /sc:issue: --claim assigns an existing GitHub issue on the origin repo (and its ClickUp task), checks its accuracy, writes a summary and a next-step prompt, then stops; --create files a templated GitHub issue with labels from a fixed set. Spawns tier-pinned worker agents for every lookup and draft; the orchestrator makes every GitHub and ClickUp write."
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, Skill, AskUserQuestion
---

<!-- Extended metadata (for documentation, not parsed):
category: workflow
complexity: advanced
mcp-servers: [auggie, codegraph]
-->

# /sc:issue protocol

Two modes, chosen by the command (`~/.claude/commands/sc/issue.md`), which has already validated the flags:

- **`--claim <number|url>`**: assign an existing issue of the origin repo to the current user on GitHub and, when one exists, on its ClickUp task; check whether the issue text is still accurate; write a summary cheatsheet and the next-step prompt; post two marked comments; then **stop**. The claim never runs a next-step command (B2).
- **`--create "<description>"`**: turn a description into a GitHub issue built from one of four templates, with labels from a fixed set, and post it. GitHub only: no ClickUp task and no self-assignment (B6).

For issues filed through `/sc:issue --create`, its four templates replace the `ISSUE-HANDOFF.md` / `ISSUE-BACKLOG.md` instruction of rule 10 in the distributed `CLAUDE.md`; rule 10 itself is unchanged and still governs issues filed without `/sc:issue`.

`<skill base>` below is the directory that holds this `SKILL.md` (`~/.claude/skills/sc-issue-protocol/` when installed; the project `.claude/skills/sc-issue-protocol/` copy in a dev checkout).

## Files of this skill

| Path (skill-relative) | Loaded or used |
|---|---|
| `refs/claim.md` | at the start of claim mode: Waves 0-6 in detail, the effort and complexity rubric, marker handling |
| `refs/create.md` | at the start of create mode: Waves 0-5, flag-settling table, depth-to-worker table, contradiction prompt rule |
| `refs/chains.md` | claim Wave 5: the six default next-step chains and the `/sc:recommend` goal format |
| `refs/labels.md` | create Wave 5: the fixed label set and the maintainer's one-time creation lines |
| `refs/tiers.md` | before the first worker spawn of either mode: tier map, pinning rule, `E-TIER-UNAVAILABLE` |
| `scripts/origin_repo.py` | Wave 0 of both modes: prints `owner/repo` from `origin`; with `--claim` also checks the claim argument against it |
| `scripts/clickup_claim.py` | claim Wave 3: assigns the matching ClickUp task |
| `templates/scout-report.md` | `scout.md` (both modes) |
| `templates/accuracy-check-comment.md` | `accuracy-check.md` (claim, posted) |
| `templates/summary.md` | `summary.md` (claim) |
| `templates/recommend-record.md` | `recommend.md` (claim) |
| `templates/next-steps.md` | `next-steps.md` (claim) |
| `templates/claim-comment.md` | `claim-comment.md` (claim, posted) |
| `templates/description.md` | `description.md` (create) |
| `templates/flags-decision.md` | `flags.md`, `flags-user.md`, `flags-t1.md` (create) |
| `templates/issue-feature-simple.md` | `issue-body.md` (create, feature, quick or standard) |
| `templates/issue-feature-complex.md` | `issue-body.md` (create, feature, deep) |
| `templates/issue-bug-simple.md` | `issue-body.md` (create, bug, quick or standard) |
| `templates/issue-bug-complex.md` | `issue-body.md` (create, bug, deep) |
| `templates/draft-notes.md` | `draft-notes.md` (create) |
| `templates/create-review-comment.md` | `create-review.md` (create, posted when needed) |

Every output file starts as a copy of its template (stub first) and is filled in place. `clickup.json` has no template: it is the script's machine output (default D15).

## Workers and the spawn rule

Spawn workers with `subagent_type: issue-worker-t<N>` and never pass the `model` parameter.

| Agent | Picker ID (frontmatter `model:`) | Installed file |
|---|---|---|
| `issue-worker-t3` | `claude-gw-tier3` | `~/.claude/agents/issue-worker-t3.md` |
| `issue-worker-t2` | `claude-gw-tier2` | `~/.claude/agents/issue-worker-t2.md` |
| `issue-worker-t1` | `claude-gw-tier1a` | `~/.claude/agents/issue-worker-t1.md` |

Claude Code reads the project `.claude/agents/` copy first when one exists. The Agent call's `model` parameter takes aliases only and overrides the frontmatter, so passing it would lose the pin (`refs/tiers.md`). A spawn that fails because the picker ID is not served is STOP `E-TIER-UNAVAILABLE`; there is no alias fallback.

Workers make read-only GitHub and git calls, write only under `.dev/issues/`, run `/sc:analyze` by following `~/.claude/commands/sc/analyze.md` when their job needs a codebase pass, and return only the paths they wrote. Read each returned file from disk. A worker that returns no file or an empty one is retried once, then STOP `E-WORKER-NO-OUTPUT` with the expected path.

Every spawn prompt names each exact path the job must write under `.dev/issues/` and states that these are input files for the orchestrator's next tool calls, not report files: the worker writes them with the Write tool, and returning their content as text counts as no output (`E-WORKER-NO-OUTPUT`).

## Repository and GitHub call rules

- `<R>` is the `origin` repo, printed by `uv run --no-project python "<skill base>/scripts/origin_repo.py"`. Nothing else is consulted: not `gh repo set-default`, not gh's fork-parent default, not a `--repo` flag (B10). There is no `--repo` option on the command.
- Every GitHub CLI call on issues, pull requests or labels passes `--repo <R>`; every `gh api` path is `user` or spells `repos/<R>/...`, never a brace placeholder.
- The orchestrator (this skill) is the only place that writes to GitHub or ClickUp: `gh issue edit <N> --repo <R> --add-assignee @me`, `gh issue comment <N> --repo <R> --body-file <file>`, `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<file>`, `gh issue create --repo <R> ...` and `scripts/clickup_claim.py`. Workers never write to either.
- `git fetch origin` is the only fetch; no other remote is added or fetched.
- Posts go up directly (B1); the full body or comment is never shown for approval. The only user prompt is the create-mode contradiction question (`refs/create.md`, default D14).
- `.dev/issues/` is never staged or committed by this skill (default D24).
- `CLICKUP_API_TOKEN` is never printed, echoed or inlined.

## Claim mode

Load `refs/claim.md` now. `<N>` is the issue number, `<D>` = `.dev/issues/<N>/`.

1. **Wave 0, prerequisites.** `uv run --no-project python "<skill base>/scripts/origin_repo.py" --claim "<argument>"` resolves `<R>` and `<N>`: exit 1 STOP `E-NO-ORIGIN`, exit 3 STOP `E-FOREIGN-REPO`, exit 4 STOP `E-NOT-AN-ISSUE`. Then `gh auth status` (else STOP `E-GH-AUTH`), the default branch, and create `<D>`.
2. **Wave 1, lookup.** Load `refs/tiers.md`. Spawn `issue-worker-t3` first (B13); it writes `<D>/scout.md` from `templates/scout-report.md`.
3. **Wave 2, edge cases** from `scout.md`: a pull request is STOP `E-NOT-AN-ISSUE`; closed or assigned to someone else stops with the stated message and no write (B9); re-claim continues; earlier marked comment IDs are kept for Wave 6.
4. **Wave 3, assign.** `gh issue edit <N> --repo <R> --add-assignee @me` (failure STOP `E-ASSIGN-FAILED`, before ClickUp and any comment), then `scripts/clickup_claim.py` with stdout to `<D>/clickup.json`; every ClickUp outcome except an argument error is non-fatal.
5. **Wave 4, accuracy check and summary.** Spawn `issue-worker-t2`, or `issue-worker-t1` when `scout.md` says `complex`; it writes `<D>/accuracy-check.md`, `<D>/summary.md` (effort in hours) and, when out of date, `<D>/analysis/`.
6. **Wave 5, next steps.** Load `refs/chains.md`. Invoke `Skill sc-recommend` with the goal format of `refs/chains.md`; save its output verbatim to `<D>/recommend.md` from `templates/recommend-record.md`. Write `<D>/next-steps.md` from `templates/next-steps.md`, starting with the `/model` tier line.
7. **Wave 6, post.** Post or edit (by marker) the accuracy-check comment and the claim comment (`templates/claim-comment.md`). Print the `next-steps.md` path and STOP. Never run a next-step command (B2).

## Create mode

Load `refs/create.md` now. `<D>` = `.dev/issues/draft-<YYYYMMDD-HHMMSS>-<slug>/` until the issue exists, then `.dev/issues/<N>/` (default D10).

1. **Wave 0, prerequisites.** `uv run --no-project python "<skill base>/scripts/origin_repo.py"` resolves `<R>` (STOP `E-NO-ORIGIN`); `gh auth status` (else STOP `E-GH-AUTH`); create `<D>`; write `<D>/description.md` from `templates/description.md`.
2. **Wave 1, lookup.** Load `refs/tiers.md`. Spawn `issue-worker-t3` first (B13): repo labels and possible duplicates into `<D>/scout.md`.
3. **Wave 2, settle the flags** by the depth table of `refs/create.md`; complexity follows depth; the result goes to `<D>/flags.md` from `templates/flags-decision.md`. Deep with all flags given runs `Skill sc:adversarial-protocol` with `--compare <D>/flags-user.md,<D>/flags-t1.md --depth quick`.
4. **Wave 3, pick the template**: mode selects feature or bug; `quick`/`standard` select the simple template, `deep` the complex one.
5. **Wave 4, draft the body** with the depth's worker into `<D>/issue-body.md` and `<D>/draft-notes.md`. Ask one question only when `draft-notes.md` lists new material or a contradiction.
6. **Wave 5, post.** Load `refs/labels.md`. Apply only the labels of the fixed set that exist in `<R>`; `gh issue create --repo <R> --title "[FEATURE] <title>"` or `"[BUG] <title>"` with `--body-file <D>/issue-body.md` (failure STOP `E-CREATE-FAILED`); rename `<D>` to `.dev/issues/<N>/`; post the pushback comment from `templates/create-review-comment.md` when Wave 2 found a disagreement at standard or deep. Print the issue URL, the directory and the labels not applied. No ClickUp call (B6).

## Return contract

Print this block last, in both modes, including after a STOP (fields that do not apply are `null`):

```yaml
status: success | stopped | failed
mode: claim | create
issue_number: <N or null>
issue_url: <url or null>
dir: <.dev/issues/<N>/ or the draft directory>
clickup_status: <status field of clickup.json, or null on create>
labels_applied: [<label>, ...]
labels_missing: [<label>, ...]
next_steps_path: <.dev/issues/<N>/next-steps.md, or null on create>
```

On a STOP, also print the STOP code and its message.

## Error handling

| Scenario | Behavior |
|---|---|
| Both or neither of `--claim` / `--create`; bad flag value; empty description; `--depth`, `--mode` or `--type` with `--claim` (`E-CREATE-ONLY-FLAG`) | The command STOPs with usage before Activation |
| No `origin`, or `origin` is not GitHub | STOP `E-NO-ORIGIN` |
| Claim URL on another repo | STOP `E-FOREIGN-REPO` |
| `gh auth status` fails | STOP `E-GH-AUTH` |
| Issue closed | STOP, message "Issue #N is closed; not claimed.", no writes |
| Assigned to someone else | STOP, message names the assignee, no writes |
| Number or URL is a pull request | STOP `E-NOT-AN-ISSUE` |
| Worker spawn fails because the picker ID is not served | STOP `E-TIER-UNAVAILABLE` naming the agent file and picker ID; no alias fallback |
| Worker returns no file, or an empty one | Retry that worker once; then STOP `E-WORKER-NO-OUTPUT` with the path expected |
| `gh issue edit <N> --repo <R> --add-assignee @me` fails | STOP `E-ASSIGN-FAILED` before ClickUp and before any comment |
| ClickUp skipped, not found, ambiguous, already assigned or error | Continue; the claim comment states the outcome |
| `/sc:recommend` asks a question or finds no route | Record it in `recommend.md`; `next-steps.md` uses the default row from `refs/chains.md` and says so |
| `gh issue comment <N> --repo <R>` or the `gh api -X PATCH repos/<R>/issues/comments/<id>` edit fails | STOP `E-POST-FAILED`; files stay in `.dev/issues/<N>/`; a re-run edits rather than duplicates because of the markers |
| `gh issue create --repo <R>` fails | STOP `E-CREATE-FAILED`; the draft directory is kept |
| A label of the fixed set is missing in the repo | Skip it; list it in the final output |
| codegraph or auggie unavailable for `/sc:analyze` | The worker continues on Grep, Glob and Read and records it in its file |

## Will

- Resolve the repo from `origin` only and pass it explicitly on every GitHub call.
- Spawn the T3 worker before any lookup of its own, and pin every worker by `subagent_type`.
- Write every artifact under `.dev/issues/` from its template.
- Post directly, and edit an earlier marked comment instead of posting a duplicate.
- Stop a claim after writing `next-steps.md`.

## Will Not

- Run any next-step command, brainstorm, design, plan or implementation.
- Create a label, a ClickUp task or a GitHub repository setting.
- Pass the `model` parameter on an Agent call, or fall back to an alias.
- Touch any repository other than `origin`, or fetch any other remote.
- Stage or commit `.dev/issues/`, or edit source code.
- Print the ClickUp token.
