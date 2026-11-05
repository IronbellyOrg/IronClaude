# Reviewer 2 brief (persona: qa)

Read-only reviewer. Audit the supplied hunks and matrix; you may Read/Grep/Glob the repo. Run nothing. Return findings only.

## T1 card excerpt

### Coverage section (verbatim from t1-card.md)

- Pass 1: 0 parsed IDs. Pass 2: the same 67 quote-pinned rows as round 1 (spec unchanged); 0 dropped.
- Containment match on the revised plan: 60 of 67; `coverage_pct_union = 0.8955`; `S_dev_density = 0.1045`; `coverage_degraded: parsed-sparse` (Tier-1 stop forbidden).
- Semantic read of the 7 string-unmapped rows:
  - INF-013 (source.md:215, labels never created): covered by plan Task 5 create.md bullet ("never created (B7)").
  - INF-020 (source.md:314, one manual smoke claim against a test task): covered by Task 16 (ClickUp smoke claim); matcher miss after the task was reworded.
  - INF-054 (source.md:408, PR via /sc:pr-submit): authorized exclusion in Constraints.
  - INF-058, INF-059, INF-062 (source.md:468, 469, 472: AC 2, 3, 6): recorded by Task 17 as run or pending with exact commands; not executed without user approval.
  - INF-061 (source.md:471, AC 5 skipped comment): the no-token path is executed by Task 2; the comment wording is pending in Task 17.


## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-04T07:10:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command projectPath=/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command

Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

Coverage matrix artifact: /home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command/.dev/reflect/pre-TASK-WF-scIssueCommand-20261104-064713-20261104081732/artifacts/coverage-matrix.json

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:1-10

````markdown
# Design: `/sc:issue` command and `sc-issue-protocol` skill

**Status:** Design only (nothing implemented). Next: `/sc:workflow` on this file, then `/sc:implement` on the plan it prints.
**Issue:** IronbellyOrg/IronClaude #302 ("[feat]sc-issue command"), body plus all three comments.
**Branch:** `ironbelly/feat-sc-issue-command`
**Source of truth:** `src/superclaude/` -> `make sync-dev` -> `.claude/` (never stage `.claude/`).
**Produced by:** `/sc:design sc-issue-command --type component --format spec`, 2026-11-04.

---

````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:11-19

````markdown
## 1. Purpose and scope

`/sc:issue` has two modes:

- **`--claim <number|url>`**: take an existing GitHub issue. Assign it to the current user on GitHub and, when it exists, on its ClickUp task; check whether the issue text is still accurate against today's code and the pull requests merged since the issue was opened; write a summary cheatsheet; build the next-step prompt (which commands to run, with which flags, on which model tier); post the results to the issue; then **stop**. It never starts the brainstorm, design, plan or implementation itself.
- **`--create "<description>"`**: turn a description into a GitHub issue built from one of four templates, with labels from a fixed set, and post it. GitHub only: no ClickUp task.

Out of scope: running the next-step chain, creating labels, creating ClickUp tasks, editing CLAUDE.md core rule 10 (which still governs issues filed without `/sc:issue`), and any interaction with an upstream parent repository.

````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:20-41

````markdown
## 2. Binding decisions (issue body + three comments)

Every row is binding. "Owner" is the issue author's comments of 2026-10-30; "Comment 1" is the 2026-10-26 gap-filling comment the owner accepted.

| # | Decision | Source |
|---|---|---|
| B1 | Posts go up directly (assigning, comments, new issues). The user is not shown each post first. | Comment 1 |
| B2 | `--claim` stops after writing the next-step prompt to `.dev/issues/<number>/next-steps.md` and links it in the issue comment. | Comment 1 |
| B3 | "Time" is an effort estimate in hours, recorded in the summary. | Comment 1 |
| B4 | `/sc:recommend` picks the starting chain and depth; downstream skills size their own work. | Comment 1 |
| B5 | Every output comes from a template and is saved under `.dev/issues/<number>/`: four issue-body templates, the summary doc, the accuracy-check comment. Issue templates start from GFxAI `ISSUE_TEMPLATE/bug_report.md` and `feature_request.md`. | Comment 1 |
| B6 | `--create` makes the GitHub issue only, no ClickUp task. | Comment 1 |
| B7 | Labels come from a fixed set defined in this spec; none are created on the fly. | Comment 1 |
| B8 | Agent definitions pin a model by its picker ID (for example `claude-gw-tier1`). | Comment 1 |
| B9 | Claim edge cases: assigned to someone else -> stop and say so; closed -> stop; claimed before -> update the earlier comment, no duplicate. | Comment 1 |
| B10 | The repo is always the one `origin` points at, never an upstream parent. | Comment 1 |
| B11 | `/sc:brainstorm --handoff tasklist` feeds `/sc:tasklist`, not `/sc:workflow`, so the simple-feature path ends the brainstorm with no handoff and then runs `/sc:workflow`. `--handoff design` only prints a suggestion, so the medium path runs `/sc:design` as its own step. | Comment 1 |
| B12 | ClickUp: the REST API with each person's own token (option 1), not the MCP server. | Owner, 2026-10-30 01:49 |
| B13 | Claiming or creating starts by spawning a sub-agent on the Haiku-class T3 tier that does the lookup work and reports back; it must be pinned so an alias cannot change it. | Owner, 2026-10-30 14:15 |
| B14 | Brainstorm and implement work after a claim runs on T1 or T2 by complexity. | Owner, 2026-10-30 14:15 |
| B15 | Order of work for this feature: `/sc:design`, then `/sc:workflow`, then `/sc:implement` (the issue body's "before invoking Brainstorm" is superseded). | Coordinator brief carrying the owner instruction |

````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:42-56

````markdown
## 3. Corrections to the issue text

| Issue text | Problem (verified) | This design |
|---|---|---|
| Simple feature: `/sc:brainstorm --depth quick --handoff tasklist` then `/sc:workflow` | `--handoff tasklist` invokes `sc-tasklist-protocol` (`~/.claude/commands/sc/brainstorm.md`, Related Commands), not `/sc:workflow` | Brainstorm with no `--handoff` (default `none`), then `/sc:workflow` (B11) |
| Medium feature: `/sc:brainstorm --handoff design --blind` then `sc:design` | `--handoff design` is "text-only" (`brainstorm.md`, Related Commands) | Drop `--handoff design`; run `/sc:design` as its own step (B11) |
| Complex feature: `--handoff design then sc:workflow` | Same text-only handoff; the issue skips `/sc:design` here | Same fix as medium: `/sc:design` runs as its own step (default D7) |
| Complex feature: `---research deep` | Typo | `--research deep` |
| Feature/bug "T0 models" for medium/complex, "T1" for simple | Owner later limited brainstorm and implement work to T1 or T2 (B14) | Simple -> T2, medium and complex -> T1 (default D6) |
| `/sc:analyze` "standard" depth | `/sc:analyze` accepts only `--depth quick|deep` | Standard runs `/sc:analyze` with no `--depth` |
| Example picker ID `claude-gw-tier1` | No such tier ships; tiers are `tier0`, `tier1a`, `tier1b`, `tier2`, `tier3`, `tier4` (`src/superclaude/skills/ccsession-tag/ccsession-models.json`) | T1 -> `claude-gw-tier1a` (default D3) |
| "spawn ... with Haiku" | The `haiku` alias follows `ANTHROPIC_DEFAULT_HAIKU_MODEL`; on this workspace it is `glm-5.3`, not Haiku. The Agent tool's `model` parameter takes only aliases | Pin `claude-gw-tier3` in agent frontmatter and never pass `model` on the Agent call (section 6) |
| Rule 10 of the distributed `CLAUDE.md` (file issues from `ISSUE-HANDOFF.md` / `ISSUE-BACKLOG.md`) | Different templates | Unchanged; `/sc:issue --create` uses its own four templates (B5). Rule 10 still covers issues filed outside `/sc:issue` |
| `tests/cli/test_issue_body_templates.py::test_no_issue_skill_or_command_added` | Asserts no `sc-issue*` skill and no `issue.md` command exist | Replace that one test (section 16) |

````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:57-80

````markdown
## 4. Command interface

```text
/sc:issue --claim <number|url>
/sc:issue --create "<description>" [--depth quick|standard|deep] [--mode feature|bug] [--type <type>]
```

| Flag | Mode | Default | Values | Meaning |
|---|---|---|---|---|
| `--claim` | claim | - | issue number (`302`, `#302`) or issue URL on the origin repo | Claim this issue |
| `--create` | create | - | free text, or `@path` to a file holding the description | Description of the feature or bug |
| `--depth` | create | `quick` | `quick`, `standard`, `deep` | How hard the command checks the flags and fills the body (section 8) |
| `--mode` | create | chosen by a worker when omitted | `feature`, `bug` | Picks the feature or bug template and the `enhancement` / `bug` label |
| `--type` | create | chosen by a worker when omitted | `cicd`, `command`, `skill`, `agent`, `hook`, `cli`, `core`, `docs`, `tests`, `install`, `other` | Area of the change; maps to a `type: <value>` label |

STOP rules (in the command file, before Activation):

- Exactly one of `--claim` / `--create` is required; both or neither -> STOP with the usage block.
- `--depth`, `--mode` or `--type` with `--claim` -> STOP (`E-CREATE-ONLY-FLAG`).
- An unknown value for `--depth`, `--mode` or `--type` -> STOP listing the allowed values.
- Empty `--create` description -> STOP.

There is no `--repo` flag (B10), no dry-run flag and no preview flag (B1).

````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:81-111

````markdown
## 5. Component architecture

```text
User: /sc:issue ...
  |
  v
commands/issue.md  (thin: flags, usage, STOP rules, Activation)
  |  Skill sc:issue-protocol
  v
skills/sc-issue-protocol/SKILL.md  (orchestrator; the only place that writes to GitHub)
  |-- refs/claim.md, refs/create.md, refs/chains.md, refs/labels.md, refs/tiers.md  (loaded per wave)
  |-- templates/*.md  (every output file starts from one of these)
  |-- scripts/clickup_claim.py  (stdlib-only ClickUp REST client; claim only)
  |-- scripts/origin_repo.py   (prints owner/repo from the origin remote; both modes)
  |
  |-- Agent: issue-worker-t3  (model: claude-gw-tier3)  lookup on claim and create; quick-depth body
  |-- Agent: issue-worker-t2  (model: claude-gw-tier2)  accuracy check, summary; quick flag choice (flag missing); standard flag validation (flags given); standard body
  |-- Agent: issue-worker-t1  (model: claude-gw-tier1a) complex accuracy check; standard/deep flag choice (flag missing); deep flag variant; deep body
  |-- Skill: sc-recommend     (picks the starting chain and depth; claim only)
  |-- Skill: sc:adversarial-protocol (create --depth deep with all flags given)
  v
.dev/issues/<number>/  (every artifact)      GitHub issue on the origin repo (assign, comments, new issue)
                                              ClickUp task (assignee only, claim only)
```

Responsibilities:

- The **command** parses and validates flags and hands off. No protocol logic.
- The **skill** resolves the repo, spawns workers, reads their files from disk, makes every GitHub mutation (assign, comment, edit comment, create issue) and runs the ClickUp script. Keeping all writes here means the origin-repo pin and the duplicate-comment markers are enforced in one place.
- **Workers** read GitHub and the codebase, run `/sc:analyze` by following `~/.claude/commands/sc/analyze.md` (a command with no backing skill), and write their result files under `.dev/issues/<...>/`. Workers never write to GitHub or ClickUp and never edit source code. Each returns only the path of the file it wrote.

````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:112-136

````markdown
## 6. Model tiers and how each sub-agent is pinned

Tier map (default D3):

| Tier | Picker ID pinned in agent frontmatter | Used for |
|---|---|---|
| T3 | `claude-gw-tier3` | `issue-worker-t3`: the first lookup on every claim and create (B13); quick-depth issue body |
| T2 | `claude-gw-tier2` | `issue-worker-t2`: accuracy check and summary on simple/medium claims; flag choice at quick depth when a flag is missing; validation of user-given flags at standard depth; standard-depth body. Next-step chains for simple work (B14) |
| T1 | `claude-gw-tier1a` | `issue-worker-t1`: accuracy check and summary on complex claims; flag choice at standard/deep depth when a flag is missing; the independent flag variant for the deep adversarial check; deep body. Next-step chains for medium and complex work (B14) |

How pinning works (verified against the Claude Code subagent docs, `https://code.claude.com/docs/en/sub-agents`, read 2026-11-04):

1. Claude Code resolves a subagent's model in this order: the Agent call's `model` parameter, then the agent file's `model:` frontmatter, then `CLAUDE_CODE_SUBAGENT_MODEL`, then the main session's model.
2. The Agent call's `model` parameter accepts only the aliases `sonnet`, `opus`, `haiku`, `fable`. It cannot carry a picker ID, and if passed it overrides the frontmatter.
3. Frontmatter `model:` accepts an alias, a full model ID ("the same values as the `--model` flag") or `inherit`.
4. The `haiku` alias resolves through `ANTHROPIC_DEFAULT_HAIKU_MODEL`, which on this Coder workspace is `glm-5.3`. So "spawn with haiku" does not guarantee the T3 tier, which is the owner's concern in B13.

Therefore:

- Each worker agent file sets `model: claude-gw-tier<N>` (one agent file per tier, because frontmatter is the only place a picker ID can be pinned).
- `SKILL.md` and every ref state: spawn workers with `subagent_type: issue-worker-t<N>` and **never pass the `model` parameter**.
- An installed mod whose `agent.spawn` hook sets a model overrides the pin (same docs page). The skill does not try to detect this; `refs/tiers.md` states it so an operator knows where to look.
- If a spawn fails because the picker ID is not served (for example, outside a ccsession tier workspace), the skill STOPs with `E-TIER-UNAVAILABLE`, naming the agent file and picker ID. It does not fall back to an alias (default D4).
- The T1/T2 tier for the next-step chains is written into `next-steps.md` as a `/model claude-gw-tier1a` or `/model claude-gw-tier2` line before the chain, because the user runs the chain in their own session (B2, B14).

````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:137-181

````markdown
## 7. `--claim` flow

Load `refs/claim.md` at the start of this mode. `<R>` is the origin repo (`owner/repo`), `<N>` the issue number, `<D>` = `.dev/issues/<N>/`.

**Wave 0: prerequisites (orchestrator).**
1. Resolve `<R>` from `git remote get-url origin` (section 13). STOP `E-NO-ORIGIN` if missing or not a GitHub URL.
2. Parse `<N>` from the argument. A URL must point at `<R>`; otherwise STOP `E-FOREIGN-REPO` (B10).
3. `gh auth status` must succeed; else STOP `E-GH-AUTH`.
4. Create `<D>`.

**Wave 1: lookup (issue-worker-t3, B13).** The orchestrator spawns `issue-worker-t3` before doing any lookup itself. The worker:
- runs `gh issue view <N> --repo <R> --json number,title,body,state,assignees,labels,comments,createdAt,url,author` and `gh api user -q .login`;
- lists pull requests merged since `createdAt` with `gh pr list --repo <R> --state merged --search "merged:>=<createdAt date>" --json number,title,mergedAt,files,url` and recent commits on the default branch since that date (`git log --since=<createdAt> --name-only` on `origin/<default branch>` after `git fetch origin`; the fetch targets `origin` only);
- finds an earlier claim by this user: a comment authored by the current login whose body contains `<!-- sc:issue:claim -->` (and likewise `<!-- sc:issue:accuracy-check -->`), recording each comment ID;
- writes `<D>/scout.md` from `templates/scout-report.md`: state, assignees, current login, earlier comment IDs, the list of merged PRs and changed files since creation, a first complexity guess (`simple|medium|complex`) and type guess (`feature|bug`) with one-line reasons;
- returns the path.

**Wave 2: edge cases (orchestrator reads `<D>/scout.md`).**
- `state` is `CLOSED` -> STOP: "Issue #N is closed; not claimed." No GitHub or ClickUp write (B9).
- Assigned to anyone other than the current login -> STOP: "Issue #N is assigned to @<login>; not claimed." No write (B9).
- Already assigned to the current login -> continue (re-claim is allowed and idempotent).
- Earlier claim / accuracy-check comment IDs present -> remember them; Wave 6 edits them instead of posting new ones (B9).
- The number is a pull request -> STOP `E-NOT-AN-ISSUE`.

**Wave 3: assign (orchestrator).**
1. `gh issue edit <N> --repo <R> --add-assignee @me`. Failure -> STOP `E-ASSIGN-FAILED` (ClickUp is not touched).
2. Run the ClickUp script (section 12). Its result is written to `<D>/clickup.json`. Any ClickUp outcome other than an argument error is non-fatal and is reported in the claim comment.

**Wave 4: accuracy check and summary (issue-worker-t2, or issue-worker-t1 when `scout.md` says `complex`).** The worker assumes the issue text is out of date (issue body) and:
- checks each concrete claim in the issue body and comments (paths, symbols, behaviours, flags) against today's code, and checks each merged PR and changed file from `scout.md` for relevance;
- writes `<D>/accuracy-check.md` from `templates/accuracy-check-comment.md` with verdict `current` or `out_of_date` and the evidence for each changed claim;
- when `out_of_date`: runs `/sc:analyze` by following `~/.claude/commands/sc/analyze.md` on the paths the issue touches (`--depth deep` when complex, no `--depth` otherwise), saving the report under `<D>/analysis/`;
- always writes `<D>/summary.md` from `templates/summary.md`: what the issue asks for, relevant files and systems (the cheatsheet), type, complexity, **effort estimate in hours** (B3) using the rubric in `refs/claim.md`, and links to anything under `<D>/analysis/`;
- returns both paths.

**Wave 5: next steps (orchestrator).**
1. Invoke `Skill sc-recommend` with a goal built from `summary.md`: issue URL, type, complexity, the summary path, and the default chain row for that type and complexity from `refs/chains.md` (section 9) as the suggested route. `/sc:recommend` picks the starting chain and depth (B4). Save its output verbatim to `<D>/recommend.md`.
2. Write `<D>/next-steps.md` from `templates/next-steps.md`: the `/model` line for the tier (B14, section 9), then the commands in order with their flags, the inputs each needs (`@.dev/issues/<N>/summary.md`), the effort estimate, and, when `/sc:recommend` chose differently from the default row, one line naming the default row and why it was not used.
3. The orchestrator does not run any of those commands (B2).

**Wave 6: post (orchestrator, directly, B1).**
1. Accuracy-check comment: body = `<D>/accuracy-check.md` (it carries `<!-- sc:issue:accuracy-check -->`). If an earlier one exists, edit it with `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<D>/accuracy-check.md`; otherwise `gh issue comment <N> --repo <R> --body-file <D>/accuracy-check.md`.
2. Claim comment: write `<D>/claim-comment.md` from `templates/claim-comment.md`: who claimed it, ClickUp result, the summary overview, effort estimate, complexity, and repo-relative links to `<D>/summary.md`, `<D>/next-steps.md` and `<D>/analysis/` (default D9). It carries `<!-- sc:issue:claim -->`. Post or edit it the same way as step 1.
3. Print the `next-steps.md` path and STOP.

````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:182-220

````markdown
## 8. `--create` flow

Load `refs/create.md` at the start of this mode. Files are written to `<D>` = `.dev/issues/draft-<YYYYMMDD-HHMMSS>-<slug>/` until the issue exists, then the directory is renamed to `.dev/issues/<N>/` (default D10).

**Wave 0: prerequisites.** Same repo, auth and directory steps as claim Wave 0. Write the description to `<D>/description.md`.

**Wave 1: lookup (issue-worker-t3, B13).** The worker lists the repo's labels (`gh label list --repo <R> --limit 200 --json name`), searches for possible duplicates (`gh issue list --repo <R> --state all --search "<keywords>" --json number,title,state,url --limit 10`), and writes `<D>/scout.md` (same template as claim, create section). Possible duplicates do not stop the run; they go into the body's related-issues section (default D11).

**Wave 2: settle the flags.** "All flags given" means both `--mode` and `--type` were passed. When only one was passed, the given one is kept and the missing one is chosen as in the "missing" rows (default D12).

| Depth | All flags given | A flag missing |
|---|---|---|
| quick | Take the user's flags at face value | `issue-worker-t2` reads the description and `scout.md` and chooses |
| standard | `issue-worker-t2` runs a quick validation of the user's flags; differences become a pushback comment posted after the issue (Wave 5) | `issue-worker-t1` chooses |
| deep | Two variants debated: `<D>/flags-user.md` (the user's flags) and `<D>/flags-t1.md` (an independent choice by `issue-worker-t1`), then `Skill sc:adversarial-protocol` with `--compare <D>/flags-user.md,<D>/flags-t1.md --depth quick`; differences become the pushback comment (default D13) | `issue-worker-t1` runs `/sc:analyze` on the code the description touches, then chooses |

Complexity follows depth, as the issue body pairs them: `quick` = simple, `standard` = medium, `deep` = complex. Every choice is written to `<D>/flags.md` from `templates/flags-decision.md` (mode, type, complexity, reasons). The flags the issue is filed with are the user's flags when the user gave them (the pushback comment explains any disagreement; the issue is not silently relabelled), else the worker's choice.

**Wave 3: pick the template.** Mode selects feature or bug; depth selects simple or complex: `quick` and `standard` -> simple template, `deep` -> complex template (issue body).

**Wave 4: draft the body.**

| Depth | Worker | Codebase pass |
|---|---|---|
| quick | `issue-worker-t3` | `/sc:analyze --depth quick` on the touched area |
| standard | `issue-worker-t2` | `/sc:analyze` (no `--depth`) |
| deep | `issue-worker-t1` | `/sc:analyze --depth deep` |

The worker fills the chosen template into `<D>/issue-body.md`, keeping every heading and writing "Not known yet" where the description and the codebase pass give nothing (no invented facts). It lists, in `<D>/draft-notes.md`, any **new material** it added beyond the description and any **contradiction** between the description and the code.

If `draft-notes.md` lists new material or a contradiction, the orchestrator asks the user one question (AskUserQuestion) naming each item, with choices "keep all", "drop the new material", "edit" (issue body: "result in a prompt to the user to confirm"). If it lists nothing, the issue is posted without any prompt. The full body is never shown for approval (B1; default D14 explains how the two rules fit together).

**Wave 5: post (orchestrator, directly).**
1. Labels = the mode label + `type: <type>` + `complexity: <simple|medium|complex>`, intersected with the labels that exist in `<R>` (section 11). Missing ones are listed in the final output, never created (B7).
2. `gh issue create --repo <R> --title "<prefix><title>" --body-file <D>/issue-body.md --label <label> ...` with prefix `[FEATURE] ` or `[BUG] ` (from the GFxAI templates).
3. Rename `<D>` to `.dev/issues/<N>/`.
4. Standard or deep with all flags given and a disagreement in Wave 2: post `.dev/issues/<N>/create-review.md` (from `templates/create-review-comment.md`, marker `<!-- sc:issue:create-review -->`) with `gh issue comment <N> --repo <R> --body-file ...`.
5. Print the issue URL and the directory. No ClickUp call (B6). No self-assignment.

````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:221-239

````markdown
## 9. Next-step chains (what `next-steps.md` may contain)

These are the default rows `refs/chains.md` carries and passes to `/sc:recommend` as the suggested route. `/sc:recommend` makes the final pick (B4). `<S>` = `.dev/issues/<N>/summary.md`; `<symptom>` is the bug's one-line symptom from the summary (at least 10 words); `<scope>` is the main path from the summary. Every flag below is checked in section 19.

| Type / complexity | Tier line | Chain |
|---|---|---|
| Feature, simple | `/model claude-gw-tier2` | 1. `/sc:brainstorm "<topic> @<S>" --depth quick --models opus,sonnet` (no `--handoff`)<br>2. `/sc:workflow <brainstorm dir>/merged-requirements.md --depth quick --handoff none`<br>3. `/sc:implement <plan path printed by step 2>` |
| Feature, medium | `/model claude-gw-tier1a` | 1. `/sc:brainstorm "<topic> @<S>" --blind --models opus,sonnet`<br>2. `/sc:design <brainstorm dir>/merged-requirements.md --type <architecture\|api\|component\|database> --format spec`<br>3. `/sc:workflow <design doc> --depth standard --handoff none`<br>4. `/sc:implement <plan path>` |
| Feature, complex | `/model claude-gw-tier1a` | 1. `/sc:brainstorm "<topic> @<S>" --depth deep --research deep --codebase --blind --models opus,sonnet`<br>2. `/sc:design <merged-requirements.md> --type <...> --format spec`<br>3. `/sc:workflow <design doc> --depth deep --handoff none`<br>4. `/sc:implement <plan path>` |
| Bug, simple | `/model claude-gw-tier2` | 1. `/sc:troubleshoot "<symptom>" --depth quick --context <S> --scope <scope>`<br>2. `/sc:implement <REPORT.md path printed by step 1>` |
| Bug, medium | `/model claude-gw-tier1a` | 1. `/sc:troubleshoot "<symptom>" --fix --context <S> --scope <scope>` (plan route: after the report it offers to build the `/sc:workflow` package; the user accepts, and it then prints the `/sc:implement` command)<br>2. `/sc:implement <plan path printed by step 1>` |
| Bug, complex | `/model claude-gw-tier1a` | 1. `/sc:troubleshoot "<symptom>" --depth deep --fix --context <S> --scope <scope>` (MDTM route: after the report it offers to build the task file with `task-builder`; the user accepts, and it then prints the `/task` command)<br>2. `/task <task file path printed by step 1>` |

Notes:
- `--depth quick` with `--fix` is a STOP in `/sc:troubleshoot`, so the simple bug row has no `--fix` and hands the report to `/sc:implement` (issue body: "Hand the output directly off ... /sc:implement").
- `/sc:troubleshoot --depth deep` STOPs on a description under 10 words without `--scope`; the rows always pass `--scope`.
- `/sc:brainstorm --models` defaults to `opus,sonnet,haiku`, rotated across proposals, and takes aliases only. Every brainstorm row passes `--models opus,sonnet` so no proposal runs on the `haiku` alias, which on this workspace resolves to `glm-5.3` (section 6), below T2 (B14). Aliases cannot name a picker ID, so this is the closest the chain can get to B14 inside a brainstorm; the session tier itself is pinned by the `/model` line (default D25).
- `/sc:design --type` is chosen per issue by `/sc:recommend` from the four values the command accepts.

````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:240-271

````markdown
## 10. Output files and templates

All files live in the issue's directory. Each starts as a copy of its template (stub first) and is filled in place.

| File in `.dev/issues/<N>/` | Mode | Written by | Template (`~/.claude/skills/sc-issue-protocol/templates/`) |
|---|---|---|---|
| `scout.md` | both | issue-worker-t3 | `scout-report.md` |
| `clickup.json` | claim | `scripts/clickup_claim.py` | none: machine output of a script, not a document (default D15) |
| `accuracy-check.md` (posted) | claim | worker t2/t1 | `accuracy-check-comment.md` |
| `analysis/` | claim, when out of date | worker t2/t1 via `/sc:analyze` | the report format of `/sc:analyze` |
| `summary.md` | claim | worker t2/t1 | `summary.md` |
| `recommend.md` | claim | orchestrator (verbatim `/sc:recommend` output) | `recommend-record.md` (header + verbatim block) |
| `next-steps.md` | claim | orchestrator | `next-steps.md` |
| `claim-comment.md` (posted) | claim | orchestrator | `claim-comment.md` |
| `description.md` | create | orchestrator | `description.md` |
| `flags.md` | create | the worker that settles the flags (Wave 2), or the orchestrator when quick depth takes the user's flags as given | `flags-decision.md` |
| `flags-user.md`, `flags-t1.md` | create, deep with all flags given | orchestrator (user's flags), issue-worker-t1 (independent choice) | `flags-decision.md` |
| `issue-body.md` (posted) | create | worker t3/t2/t1 | one of `issue-feature-simple.md`, `issue-feature-complex.md`, `issue-bug-simple.md`, `issue-bug-complex.md` |
| `draft-notes.md` | create | worker | `draft-notes.md` |
| `create-review.md` (posted, when needed) | create | orchestrator | `create-review-comment.md` |

The four issue-body templates, adapted from GFxAI `.dev/proj_mgmt/clickup-integration/templates/ISSUE_TEMPLATE/{bug_report,feature_request}.md` (IronbellyGroup/GFxAI, read 2026-11-04). The adaptation drops the ClickUp sections (B6: no ClickUp task exists to reference), the GPU/hardware fields and the "Automatic Labels" footer (labels come from section 11), and replaces "Person-weeks" with hours (B3):

| Template | Sections kept from GFxAI, in order |
|---|---|
| `issue-bug-simple.md` | Bug Summary; Environment (OS, version); Current Behavior; Expected Behavior; Steps to Reproduce; Impact Assessment (Severity, Blast Radius); Error Messages; Codebase Context (from `/sc:analyze`); Related Issues; Testing Notes |
| `issue-bug-complex.md` | all of the simple sections, plus Frequency; User Impact; Business Impact; Cascading Effects; Logs and Stack Trace; Attempted Solutions; Proposed Solution; For Development Team (Root Cause Analysis, Fix Approach, Verification Plan) |
| `issue-feature-simple.md` | Feature Summary; Problem Statement; User Story; Proposed Solution; Acceptance Criteria; Out of Scope; Components Affected (from `/sc:analyze`); Related Issues/PRs |
| `issue-feature-complex.md` | all of the simple sections, plus Success Metrics; Architecture Impact; Dependencies; Testing Strategy; Documentation Needs; Alternatives Considered; Impact Analysis (Blast Radius, Integration Impact); Risks & Mitigation; Effort Estimate (hours) and Complexity |

Every posted template ends with its hidden marker line (`<!-- sc:issue:claim -->`, `<!-- sc:issue:accuracy-check -->`, `<!-- sc:issue:create-review -->`, `<!-- sc:issue:create template=<name> -->`).

````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:272-283

````markdown
## 11. Label set

The only labels `/sc:issue` ever applies (B7). It never creates a label.

| Group | Labels | Applied by |
|---|---|---|
| Mode | `bug`, `enhancement` | `--create` (GitHub's default labels; present on IronbellyOrg/IronClaude, checked 2026-11-04) |
| Type | `type: cicd`, `type: command`, `type: skill`, `type: agent`, `type: hook`, `type: cli`, `type: core`, `type: docs`, `type: tests`, `type: install`, `type: other` | `--create` |
| Complexity | `complexity: simple`, `complexity: medium`, `complexity: complex` | `--create` |

At run time the skill applies only the labels from this set that already exist in `<R>` and lists the rest as "not applied: label missing in repo". `refs/labels.md` holds the one-time `gh label create "<name>" --repo <owner/repo>` lines a maintainer may run by hand to add them (default D16). `--claim` changes no labels.

````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:284-315

````markdown
## 12. ClickUp lookup and assignment

Claim only (B6). REST API v2 with the user's own personal token (B12). No MCP server. The MCP route was rejected because its limit (300 calls per rolling 24 hours per workspace, shared by the team) would be hit; the REST API allows 100 requests per minute per token (Comment 1).

**Script:** `src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py`, Python standard library only (`urllib`), run as
`uv run --no-project python "<skill base>/scripts/clickup_claim.py" --issue-url <url> --issue-number <N> --repo <owner/repo>`
(the same invocation pattern as `sc-implement-protocol`'s `scripts/archive_workspace.py`). The skill writes stdout to `.dev/issues/<N>/clickup.json`.

**Configuration (environment only, same names as GFxAI's `.dev/proj_mgmt/clickup-integration/.env.example`):**

| Variable | Required | Meaning |
|---|---|---|
| `CLICKUP_API_TOKEN` | yes | The person's own token (`pk_...`). Never printed, logged or written to disk |
| `CLICKUP_WORKSPACE_ID` | yes | Workspace (team) ID |
| `CLICKUP_LIST_IDS` | no | Comma-separated list IDs to narrow the search |
| `CLICKUP_MAX_PAGES` | no, default `20` | Page cap for the search (100 tasks per page) |

**Steps:**
1. Token or workspace missing -> `{"status": "skipped", "reason": "no_token"|"no_workspace"}`, exit 0.
2. `GET https://api.clickup.com/api/v2/user` -> the token owner's ClickUp user ID.
3. Page through `GET https://api.clickup.com/api/v2/team/{CLICKUP_WORKSPACE_ID}/task?page=<p>&subtasks=true&include_markdown_description=true` (plus `list_ids[]=` when set) until an empty page or the page cap. Closed tasks are excluded (API default).
4. **Match (design default D2):**
   - Rule 1, GitHub link: a task whose markdown description or any custom field value contains the issue URL `https://github.com/<owner>/<repo>/issues/<N>` (compared case-insensitively, trailing `/` or `#...` ignored).
   - Rule 2, issue number in the title: only if rule 1 found nothing; a task whose name contains `#<N>` as a whole token (not followed by a digit).
   - Exactly one match under the first rule that matches -> that task. More than one -> `{"status": "ambiguous", "candidates": [...]}`, no assignment. None -> `{"status": "not_found"}`.
5. Already an assignee -> `{"status": "already_assigned", ...}`. Else `PUT https://api.clickup.com/api/v2/task/{task_id}` with `{"assignees": {"add": [<user id>]}}` -> `{"status": "assigned", "task_id", "task_url", "rule": "github_link"|"title_number"}`.
6. HTTP 401/403 -> `{"status": "error", "reason": "auth"}`; 429 -> one wait of the `Retry-After` seconds, one retry, then `{"status": "error", "reason": "rate_limited"}`; other failures -> `{"status": "error", "reason": "<short>"}`. Exit 0 for every outcome above; exit 2 only for bad arguments.

Worst case per claim: 1 + 20 + 1 = 22 requests, inside the 100-per-minute limit.

Implementation-time check: the response shapes of `GET /user` and the task list are taken from the ClickUp v2 reference (`developer.clickup.com/reference/getfilteredteamtasks`, `.../updatetask`); the unit tests pin them with recorded fixtures, and the implementation plan includes one manual smoke claim against a test task.

````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:316-322

````markdown
## 13. Repository resolution and GitHub call rules

- `<R>` is parsed from `git remote get-url origin`, accepting `https://github.com/<owner>/<repo>(.git)` and `git@github.com:<owner>/<repo>(.git)`. Nothing else is consulted: not `gh repo set-default`, not `gh`'s fork-parent default, not a `--repo` flag (B10).
- Every `gh issue`, `gh pr` and `gh label` call passes `--repo <R>`; every `gh api` path spells `repos/<R>/...`, never `{owner}/{repo}`. This matches the fork rule in the project `CLAUDE.md` and how `/sc:pr-submit` pins its target.
- Workers make read-only `gh` calls only. All writes (`gh issue edit`, `gh issue comment`, `gh api -X PATCH`, `gh issue create`) happen in the orchestrator.
- `git fetch origin` is the only fetch; no other remote is added or fetched.

````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:323-343

````markdown
## 14. Error handling

| Scenario | Behavior |
|---|---|
| Both or neither of `--claim` / `--create`; bad flag value; empty description | Command STOPs with usage before Activation |
| No `origin`, or not GitHub | STOP `E-NO-ORIGIN` |
| Claim URL on another repo | STOP `E-FOREIGN-REPO` |
| `gh` not authenticated | STOP `E-GH-AUTH` |
| Issue closed | STOP, message "closed; not claimed", no writes |
| Assigned to someone else | STOP, message names the assignee, no writes |
| Number is a pull request | STOP `E-NOT-AN-ISSUE` |
| Worker spawn fails because the picker ID is not served | STOP `E-TIER-UNAVAILABLE` naming agent file and picker ID; no alias fallback |
| Worker returns no file, or an empty one | Retry that worker once; then STOP `E-WORKER-NO-OUTPUT` with the path expected |
| `gh issue edit --add-assignee` fails | STOP `E-ASSIGN-FAILED` before ClickUp and before any comment |
| ClickUp skipped, not found, ambiguous, already assigned or error | Continue; the claim comment states the outcome |
| `/sc:recommend` asks a question or finds no route | Record it in `recommend.md`; `next-steps.md` uses the default row from `refs/chains.md` and says so |
| Comment post or edit fails | STOP `E-POST-FAILED`; files stay in `.dev/issues/<N>/`; a re-run edits rather than duplicates because of the markers |
| `gh issue create` fails | STOP `E-CREATE-FAILED`; the draft directory is kept |
| A label in the fixed set is missing in the repo | Skip it; list it in the final output |
| `codegraph` / `auggie` unavailable for `/sc:analyze` | The worker continues on Grep/Glob/Read and records it in its file |

````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:344-383

````markdown
## 15. Files to create or change

All under `src/superclaude/` unless stated. Nothing under `.claude/` is edited or staged; `make sync-dev` produces it.

**Create**

| Path | Content |
|---|---|
| `src/superclaude/commands/issue.md` | Thin command (~100-150 lines): frontmatter (`name: issue`, `category: workflow`, `complexity: advanced`, `mcp-servers: [auggie, codegraph]`, `personas: [analyzer]`, `argument-hint`), Usage, Options table (section 4), STOP rules, Examples, Boundaries, `## Activation` -> `Skill sc:issue-protocol`, naming `~/.claude/skills/sc-issue-protocol/SKILL.md` |
| `src/superclaude/skills/sc-issue-protocol/SKILL.md` | `name: sc:issue-protocol`; `allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, Skill, AskUserQuestion`; waves of sections 7 and 8 at the WHAT/WHEN level; per-wave ref loading; spawn rule (never pass `model`); return contract (`status`, `mode`, `issue_number`, `issue_url`, `dir`, `clickup_status`, `labels_applied`, `labels_missing`, `next_steps_path`); error table (section 14); Will / Will Not. Under 500 lines |
| `src/superclaude/skills/sc-issue-protocol/refs/claim.md` | Claim waves in detail; effort and complexity rubric (default D5); marker handling |
| `src/superclaude/skills/sc-issue-protocol/refs/create.md` | Create waves; flag-settling table; depth-to-worker table; contradiction prompt rule |
| `src/superclaude/skills/sc-issue-protocol/refs/chains.md` | The six default chains of section 9 and the `/sc:recommend` goal format |
| `src/superclaude/skills/sc-issue-protocol/refs/labels.md` | The fixed label set and the maintainer's one-time `gh label create` lines |
| `src/superclaude/skills/sc-issue-protocol/refs/tiers.md` | Tier map, the pinning rule and its verified reason, `E-TIER-UNAVAILABLE` |
| `src/superclaude/skills/sc-issue-protocol/templates/` | `issue-feature-simple.md`, `issue-feature-complex.md`, `issue-bug-simple.md`, `issue-bug-complex.md`, `summary.md`, `accuracy-check-comment.md`, `claim-comment.md`, `next-steps.md`, `scout-report.md`, `recommend-record.md`, `description.md`, `flags-decision.md`, `draft-notes.md`, `create-review-comment.md` |
| `src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py` | Section 12; standard library only; no secrets in output |
| `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py` | Section 13: runs `git remote get-url origin` and prints `owner/repo`; standard library only; exits non-zero with `E-NO-ORIGIN` otherwise. Wave 0 of both modes calls it, so the parsing is tested code rather than prose |
| `src/superclaude/agents/issue-worker-t3.md` | `model: claude-gw-tier3`; `tools: Read, Grep, Glob, Write, Bash`; read-only on GitHub and code; writes only under `.dev/issues/`; returns its file path |
| `src/superclaude/agents/issue-worker-t2.md` | Same shape, `model: claude-gw-tier2` |
| `src/superclaude/agents/issue-worker-t1.md` | Same shape, `model: claude-gw-tier1a` |

Path rule: inside these primitives every reference to another primitive uses the installed path (`~/.claude/commands/sc/analyze.md`, `~/.claude/skills/sc-issue-protocol/...`, `~/.claude/agents/issue-worker-t3.md`) and, for existence checks, also accepts the project `.claude/` copy (agents: project `.claude/agents/` wins; skills: `~/.claude/skills/` wins). No `src/superclaude/...` path appears in them; the pre-commit check is `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}`.

**Change**

| Path | Change |
|---|---|
| `src/superclaude/core/HOW-WE-WORK.md` | One row in the "Other commands" table: `/sc:issue` (claim: assign, accuracy check, summary, next-step prompt, then stop; create: a templated GitHub issue on the origin repo; both post directly to GitHub) |
| `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | Byte-for-byte copy of the edited guide (required by `tests/commands/test_routing_plugin_parity.py`) |
| `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | Section 4.1: the optional `model:` field also takes a full model ID or picker ID, and the Agent call's `model` parameter (aliases only) overrides it, so a skill that needs a pinned tier must not pass `model`. Section 4.3: one line saying the `<model>` in agent specs is an alias |
| `docs/user-guide/commands.md` | One row in "8. UTILITIES" (`/sc:issue`, "Changes files? Yes (posts to GitHub; writes `.dev/issues/`)") and a `/sc:issue` section with usage and examples |
| `tests/cli/test_issue_body_templates.py` | Replace `test_no_issue_skill_or_command_added` (section 16) |
| `tests/core/test_how_we_work_routing_table.py` | Add `"sc:issue"` to `_OTHER_COMMANDS` |
| `tests/recommend/test_routing_refresh.py` | Add `"issue"` to `_POST_REFRESH_ADDITIONS` (line 32 today), the same way `graph` and `impact` were added; otherwise `test_command_dispositions_trace_appendix_c_and_inventory` fails because it compares every `src/superclaude/commands/*.md` against the frozen active-command list |

Not changed: `src/superclaude/core/CLAUDE.md` (rule 10 stays; no level-table change), the `plugins/superclaude/` command, agent and skill mirrors (they are partial today and no test requires new entries), `docs/user-guide/agents.md` (internal worker agents are not listed there today, for example `evidence-validator`).

No CLI (`src/superclaude/cli/`) code: the only program is the skill's own script.

````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:384-401

````markdown
## 16. Tests

New and changed tests, all run with `uv run pytest`.

| Test file | What it pins |
|---|---|
| `tests/commands/test_issue_command.py` (new) | Command frontmatter fields; Options table lists exactly `--claim`, `--create`, `--depth`, `--mode`, `--type` with the allowed values of section 4; Activation names `Skill sc:issue-protocol`; no `src/superclaude/` path; no `--repo` flag; the command file and `SKILL.md` each carry the one-line rule-10 note of D26 |
| `tests/skills/test_issue_protocol.py` (new) | `SKILL.md` frontmatter and size (<500 lines); every ref and template named in `SKILL.md` exists and vice versa; the spawn rule text ("never pass the `model` parameter") is present; every posted template ends with its marker; the four issue templates carry the section headings of section 10 in order and contain no `ClickUp` text; every `/sc:*` flag in `refs/chains.md` exists in the installed-or-source command file it names (same check style as `test_every_notes_flag_exists_in_its_command`); `refs/chains.md` contains no `--handoff tasklist` and no `--handoff design` on a brainstorm step; no `src/superclaude/` path in any file of the skill |
| `tests/skills/test_issue_worker_agents.py` (new) | The three agent files exist with `model:` equal to `claude-gw-tier3`, `claude-gw-tier2`, `claude-gw-tier1a`; each picker ID's tier key exists in `src/superclaude/skills/ccsession-tag/ccsession-models.json`; tools exclude `Edit`; body states read-only GitHub and write-only-under-`.dev/issues/` |
| `tests/skills/test_clickup_claim.py` (new) | `clickup_claim.py` with `urllib` patched: skipped without token; skipped without workspace; GitHub-link match beats title match; title match only as a whole `#N` token (`#3020` does not match `#302`); ambiguous returns candidates and makes no PUT; already-assigned makes no PUT; assign sends `{"assignees": {"add": [id]}}`; 401 -> `auth`; 429 retried once; page cap honoured; the token never appears in stdout or stderr; bad arguments exit 2 |
| `tests/skills/test_issue_repo_resolution.py` (new) | `scripts/origin_repo.py`: https, ssh, `.git` suffix and trailing `/` parsed to `owner/repo`; non-GitHub URL and missing `origin` exit non-zero; it reads only `origin` |
| `tests/cli/test_issue_body_templates.py` (changed) | `test_no_issue_skill_or_command_added` becomes `test_issue_command_and_skill_are_the_only_issue_primitives`: `src/superclaude/commands/issue.md` and `src/superclaude/skills/sc-issue-protocol/` exist, and no other `sc-issue*` skill or `issue.md` command exists |
| `tests/core/test_how_we_work_routing_table.py` (changed) | `_OTHER_COMMANDS` includes `sc:issue`; the existing live-reference check then proves the command file exists |

| `tests/recommend/test_routing_refresh.py` (changed) | `_POST_REFRESH_ADDITIONS` includes `issue`; the existing inventory test then accepts the new command file |

Run before commit: `uv run pytest tests/commands tests/core tests/skills tests/recommend tests/cli/test_issue_body_templates.py`, then `make test`.

````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:402-409

````markdown
## 17. Sync, routing registration and documentation

1. Edit only under `src/superclaude/` (plus the tests, the plugin guide copy and the docs listed in section 15).
2. `make sync-dev`, then `make verify-sync`. Never `git add` anything under `.claude/` except `.claude/settings.json`.
3. Copy `src/superclaude/core/HOW-WE-WORK.md` byte-for-byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; run `uv run pytest tests/core tests/commands` (developer guide section 3.6).
4. Run `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` and justify any new hit (there should be none from this feature).
5. Open the PR only with `/sc:pr-submit --monitor 3 --head ironbelly/feat-sc-issue-command --title "..." --body "..."` (fork target IronbellyOrg/IronClaude).

````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:410-443

````markdown
## 18. Defaults chosen by this design

Each is a **design default**: a choice made where the issue and comments are silent or need reconciling. None is an open question; change one by editing this table before `/sc:workflow` runs.

| ID | Default | Why |
|---|---|---|
| D1 | This design lives at `docs/designs/sc-issue-command.md` | The existing design-doc folder (`docs/designs/prd-spec-flag.md`) |
| D2 | ClickUp task match: (1) the issue URL in the task description or a custom field, then (2) `#<N>` as a whole token in the title; exactly one match required, else no assignment | Owner asked for a default; a GitHub link is the least ambiguous signal, the title number is the common fallback, and a title text search was rejected as too loose |
| D3 | T3 = `claude-gw-tier3`, T2 = `claude-gw-tier2`, T1 = `claude-gw-tier1a` | `claude-gw-tier1` does not exist; `tier1a` is the first T1 tier in `ccsession-models.json` |
| D4 | No alias fallback when a picker ID is not served: STOP `E-TIER-UNAVAILABLE` | A fallback to `haiku` can land on a non-Claude model (`glm-5.3` here), defeating B13 |
| D5 | Complexity and effort rubric: simple = up to 4 hours in one area; medium = over 4 up to 16 hours; complex = over 16 hours, more than one subsystem, or a security/data-migration change. Effort is recorded in hours | B3 needs hours; the bands give the worker a fixed scale |
| D6 | Next-step tier: simple -> T2, medium and complex -> T1 (bugs and features alike) | B14 ("T1 or T2 by complexity") replaces the issue body's T0 rows |
| D7 | The complex-feature chain also runs `/sc:design` as its own step | Same text-only `--handoff design` problem as B11's medium path |
| D8 | Claim accuracy check and summary run on T2, or T1 when the T3 lookup sizes the issue complex | The issue names no tier for this step; B14's split applied |
| D9 | Comment links to `.dev/issues/<N>/...` are repo-relative paths; the command never commits or pushes them. Consequence: on GitHub the links do not open until someone commits and pushes those files; the claim comment says so in one line, and its overview carries the key facts (effort, complexity, verdict, first next step) inline so it is useful without the links | "path links" (issue body); committing is outside the command's job |
| D10 | `--create` drafts in `.dev/issues/draft-<timestamp>-<slug>/`, renamed to `.dev/issues/<N>/` after the issue exists | B5 needs `<number>`, which exists only after creation |
| D11 | Possible duplicates found on create are listed in the body's related-issues section; they do not stop the run | Not specified; B1 favours posting directly |
| D12 | One of `--mode` / `--type` given: keep it, choose the other as in the "flag missing" row | Not specified |
| D13 | Create, deep, all flags given: two variants (user's flags, T1's independent choice) debated with `/sc:adversarial --compare ... --depth quick` | The issue's "parallel agents each invoke `/sc:adversarial --depth quick`" needs at least two variants to compare; this is the smallest form |
| D14 | Create asks the user one question only when the drafter found new material or a contradiction; otherwise it posts without any prompt; the full body is never previewed | The issue body requires that confirmation; B1 forbids routine previews. The two do not conflict once the prompt is limited to those findings |
| D15 | `clickup.json` has no template | It is a script's machine output, not a document |
| D16 | Missing labels from the fixed set are skipped and reported; `refs/labels.md` gives the maintainer's one-time creation lines | B7 forbids creating labels at run time |
| D17 | On create, complexity follows depth (quick = simple, standard = medium, deep = complex) | The issue body pairs them |
| D18 | Two marked comments on claim (accuracy check, claim overview); a re-claim edits both | B5 names the accuracy-check comment; B9 forbids duplicates |
| D19 | Picker IDs are written without the `[1m]` context suffix | Comment 1's example form; the suffix belongs to session launch, not to subagent pinning. The plan's smoke step confirms one spawn per worker |
| D20 | `--type` values: `cicd`, `command`, `skill`, `agent`, `hook`, `cli`, `core`, `docs`, `tests`, `install`, `other` | The issue lists "CICD, skill, agent, etc."; the rest follow this repo's component kinds |
| D21 | Title prefixes `[FEATURE] ` and `[BUG] ` | Taken from the GFxAI templates |
| D22 | `summary.md` is written on every claim; `/sc:analyze` runs only when the issue is out of date | The issue sizes and summarizes every claim; the analysis is the expensive part |
| D23 | When `/sc:recommend` differs from the default chain, `next-steps.md` follows `/sc:recommend` and names the unused default row | B4 makes `/sc:recommend` the authority |
| D24 | `/sc:issue` never stages or commits `.dev/issues/` | Not asked; CLAUDE.md's always-staged rule covers `.dev/tasks/` only |
| D25 | Every brainstorm step in `next-steps.md` passes `--models opus,sonnet` | Removes the `haiku` alias (here `glm-5.3`) from proposals, keeping brainstorm work at T1/T2 class as far as aliases allow (B14) |
| D26 | The command file and `SKILL.md` each state in one line that, for issues filed through `/sc:issue --create`, its four templates replace the `ISSUE-HANDOFF.md` / `ISSUE-BACKLOG.md` instruction of rule 10 in the distributed `CLAUDE.md`; rule 10 itself is not edited | Without that line an agent sees two conflicting instructions; editing rule 10 would break `test_claude_md_has_exactly_one_issue_rule_line` and change behaviour outside `/sc:issue` |
| D27 | Worker read-only behaviour on GitHub and code is enforced by the agent text and by giving workers no `Edit` tool; `Bash` is not narrowed further | Workers need `gh` and `git` reads and `/sc:analyze` tool runs; the orchestrator holds every write command. A static test checks the agent files carry no `Edit` and state the rule |

````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:444-464

````markdown
## 19. Flags cited, verified against the real command files

Checked on 2026-11-04 against the installed files `~/.claude/commands/sc/<name>.md` (their Options tables or Usage lines) and `gh <cmd> --help`.

| Command | Flags this design uses | Where verified |
|---|---|---|
| `/sc:brainstorm` | `"<topic>"` with `@<path>`, `--depth quick\|deep` (default `standard`), `--research deep`, `--codebase`, `--blind`, `--handoff` (default `none`; `design` is text-only, `tasklist` invokes `sc-tasklist-protocol`), `--models opus,sonnet` (aliases only; default `opus,sonnet,haiku`) | `brainstorm.md` Options table, Related Commands |
| `/sc:design` | `[target]`, `--type architecture\|api\|component\|database`, `--format spec` | `design.md` Usage |
| `/sc:workflow` | `<path-or-prompt>`, `--depth quick\|standard\|deep`, `--handoff none` | `workflow.md` Options table |
| `/sc:implement` | `<path>` (plan, report or spec) | `implement.md` Usage |
| `/sc:troubleshoot` | `"<description>"`, `--depth quick\|deep`, `--fix`, `--context <path>`, `--scope <path>`; `quick` + `--fix` is a STOP; `deep` needs 10+ words or `--scope` | `troubleshoot.md` Options table, Required Input |
| `/sc:analyze` | `[target]`, `--depth quick\|deep` (no `standard`) | `analyze.md` Usage |
| `/sc:recommend` | goal text only; activates `Skill sc-recommend` | `recommend.md` Usage, Activation |
| `/sc:adversarial` | `--compare <a>,<b>`, `--depth quick` | `adversarial.md` Options table |
| `/sc:pr-submit` | `--monitor 3`, `--head`, `--title`, `--body` | `pr-submit.md` Options table |
| `/task` | `<task file path>` (this is the `task` skill, not `/sc:task`) | `~/.claude/skills/task/` installed; `troubleshoot.md` names "`/task <path>`" as the MDTM route's user step |
| `gh issue edit` | `--add-assignee @me`, `--repo` | `gh issue edit --help` |
| `gh issue create` | `--title`, `--body-file`, `--label` (repeatable), `--repo` | `gh issue create --help` |
| `gh issue comment` | `--body-file`, `--repo` (`--edit-last` deliberately not used: it edits the user's last comment, not necessarily the claim comment) | `gh issue comment --help` |
| `gh issue view`, `gh label list` | `--json <fields>`, `--repo` | `gh issue view --help`, `gh label list --help` |

````

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md:465-475

````markdown
## 20. Acceptance criteria for the implementation

1. `/sc:issue --claim <N>` on an open, unassigned issue of the origin repo: the T3 worker runs first; the issue is assigned to the current user; `.dev/issues/<N>/` holds `scout.md`, `clickup.json`, `accuracy-check.md`, `summary.md` (with an hours estimate), `recommend.md`, `next-steps.md`, `claim-comment.md`; two marked comments are posted; the command stops without running any next-step command.
2. Running the same claim again edits both comments; the comment count on the issue does not grow.
3. A closed issue, or one assigned to someone else, stops with the stated message and makes no GitHub or ClickUp write.
4. A claim URL for any repo other than origin stops with `E-FOREIGN-REPO`; no `gh` call is made without `--repo <origin repo>`.
5. With `CLICKUP_API_TOKEN` unset the claim completes and the comment says ClickUp was skipped; with a token and a task that links the issue URL, that task gains the user as assignee.
6. `/sc:issue --create "<text>" --mode bug --type cli` at each depth posts an issue whose body follows the selected template's headings, with only labels from section 11 that exist in the repo; at `standard`/`deep` a disagreement produces one marked pushback comment; no ClickUp call is made.
7. Each worker agent file pins its picker ID, and the skill never passes `model` on an Agent call (static test); one manual smoke run per worker shows it was served by the pinned tier.
8. `next-steps.md` contains only commands and flags listed in section 19, starts with the `/model` tier line of section 9, and never contains `--handoff tasklist` or `--handoff design` on a brainstorm step.
9. `make verify-sync` passes; the tests of section 16 pass; `uv run pytest tests/core tests/commands` passes; the `src/superclaude` path grep shows no new hit in the new primitives.
````

## Coverage slice

| Requirement | Citation | Method | Best task | Ratio |
|---|---|---|---|---|
| INF-001: Exactly one of `--claim` / `--create` is required; both or neither -> STOP with the usage block. | source.md:74 | containment | Task 8 | 0.8571 |
| INF-002: `--depth`, `--mode` or `--type` with `--claim` -> STOP (`E-CREATE-ONLY-FLAG`). | source.md:75 | containment | Task 8 | 1.0 |
| INF-003: There is no `--repo` flag (B10), no dry-run flag and no preview flag (B1). | source.md:79 | containment | Task 8 | 0.75 |
| INF-004: Each worker agent file sets `model: claude-gw-tier<N>` (one agent file per tier, because frontmatter is the only place a picker ID can be pinned). | source.md:131 | containment | Task 15 | 0.6875 |
| INF-005: `SKILL.md` and every ref state: spawn workers with `subagent_type: issue-worker-t<N>` and **never pass the `model` parameter**. | source.md:132 | containment | Task 5 | 1.0 |
| INF-006: the skill STOPs with `E-TIER-UNAVAILABLE`, naming the agent file and picker ID. It does not fall back to an alias (default D4). | source.md:134 | containment | Task 5 | 0.7333 |
| INF-007: The T1/T2 tier for the next-step chains is written into `next-steps.md` as a `/model claude-gw-tier1a` or `/model claude-gw-tier2` line before the chain | source.md:135 | containment | Task 4 | 0.6471 |
| INF-008: `gh issue edit <N> --repo <R> --add-assignee @me`. Failure -> STOP `E-ASSIGN-FAILED` (ClickUp is not touched). | source.md:162 | containment | Task 6 | 0.6875 |
| INF-009: If an earlier one exists, edit it with `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<D>/accuracy-check.md` | source.md:178 | containment | Task 5 | 0.8889 |
| INF-010: Print the `next-steps.md` path and STOP. | source.md:180 | containment | Task 6 | 0.8333 |
| INF-011: Files are written to `<D>` = `.dev/issues/draft-<YYYYMMDD-HHMMSS>-<slug>/` until the issue exists, then the directory is renamed to `.dev/issues/<N>/` (default D10). | source.md:184 | containment | Task 5 | 0.8824 |
| INF-012: If it lists nothing, the issue is posted without any prompt. | source.md:212 | containment | Task 5 | 0.6667 |
| INF-013: Missing ones are listed in the final output, never created (B7). | source.md:215 | none | Task 2 | 0.5 |
| INF-014: No ClickUp call (B6). No self-assignment. | source.md:219 | containment | Task 5 | 1.0 |
| INF-015: Every posted template ends with its hidden marker line | source.md:270 | containment | Task 4 | 0.8333 |
| INF-016: holds the one-time `gh label create | source.md:282 | containment | Task 3 | 0.6 |
| INF-017: --issue-url <url> --issue-number <N> --repo <owner/repo> | source.md:289 | containment | Task 2 | 1.0 |
| INF-018: Never printed, logged or written to disk | source.md:296 | containment | Task 2 | 1.0 |
| INF-019: Exit 0 for every outcome above; exit 2 only for bad arguments. | source.md:310 | containment | Task 2 | 1.0 |
| INF-020: the unit tests pin them with recorded fixtures, and the implementation plan includes one manual smoke claim against a test task. | source.md:314 | none | Task 2 | 0.5333 |
| INF-021: Nothing else is consulted: not `gh repo set-default`, not `gh`'s fork-parent default, not a `--repo` flag (B10). | source.md:318 | containment | Task 5 | 0.6667 |
| INF-022: Every `gh issue`, `gh pr` and `gh label` call passes `--repo <R>` | source.md:319 | containment | Task 5 | 1.0 |
| INF-023: `git fetch origin` is the only fetch; no other remote is added or fetched. | source.md:321 | containment | Task 3 | 1.0 |
| INF-024: `src/superclaude/commands/issue.md` / Thin command (~100-150 lines) | source.md:352 | containment | Task 8 | 1.0 |
| INF-025: `name: sc:issue-protocol`; `allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, Skill, AskUserQuestion` | source.md:353 | containment | Task 6 | 1.0 |
| INF-026: Claim waves in detail; effort and complexity rubric (default D5); marker handling | source.md:354 | containment | Task 5 | 1.0 |
| INF-027: Create waves; flag-settling table; depth-to-worker table; contradiction prompt rule | source.md:355 | containment | Task 5 | 1.0 |
| INF-028: The six default chains of section 9 and the `/sc:recommend` goal format | source.md:356 | containment | Task 5 | 1.0 |
| INF-029: The fixed label set and the maintainer's one-time `gh label create` lines | source.md:357 | containment | Task 5 | 0.8889 |
| INF-030: Tier map, the pinning rule and its verified reason, `E-TIER-UNAVAILABLE` | source.md:358 | containment | Task 5 | 0.875 |
| INF-031: `issue-feature-simple.md`, `issue-feature-complex.md`, `issue-bug-simple.md`, `issue-bug-complex.md`, `summary.md` | source.md:359 | containment | Task 4 | 1.0 |
| INF-032: Section 12; standard library only; no secrets in output | source.md:360 | containment | Task 2 | 0.8333 |
| INF-033: runs `git remote get-url origin` and prints `owner/repo`; standard library only; exits non-zero with `E-NO-ORIGIN` otherwise. | source.md:361 | containment | Task 1 | 0.9375 |
| INF-034: `model: claude-gw-tier3`; `tools: Read, Grep, Glob, Write, Bash`; read-only on GitHub and code; writes only under `.dev/issues/`; returns its file path | source.md:362 | containment | Task 3 | 1.0 |
| INF-035: `src/superclaude/agents/issue-worker-t2.md` / Same shape, `model: claude-gw-tier2` | source.md:363 | containment | Task 3 | 0.9231 |
| INF-036: `src/superclaude/agents/issue-worker-t1.md` / Same shape, `model: claude-gw-tier1a` | source.md:364 | containment | Task 3 | 0.9231 |
| INF-037: No `src/superclaude/...` path appears in them | source.md:366 | containment | Task 2 | 0.8 |
| INF-038: One row in the "Other commands" table | source.md:372 | containment | Task 3 | 1.0 |
| INF-039: Byte-for-byte copy of the edited guide (required by `tests/commands/test_routing_plugin_parity.py`) | source.md:373 | containment | Task 10 | 1.0 |
| INF-040: Section 4.1: the optional `model:` field also takes a full model ID or picker ID | source.md:374 | containment | Task 11 | 1.0 |
| INF-041: One row in "8. UTILITIES" | source.md:375 | containment | Task 12 | 1.0 |
| INF-042: Replace `test_no_issue_skill_or_command_added` (section 16) | source.md:376 | containment | Task 9 | 1.0 |
| INF-043: Add `"sc:issue"` to `_OTHER_COMMANDS` | source.md:377 | containment | Task 10 | 1.0 |
| INF-044: Add `"issue"` to `_POST_REFRESH_ADDITIONS` | source.md:378 | containment | Task 9 | 1.0 |
| INF-045: `tests/commands/test_issue_command.py` (new) | source.md:390 | containment | Task 8 | 0.8 |
| INF-046: `tests/skills/test_issue_protocol.py` (new) | source.md:391 | containment | Task 7 | 0.8 |
| INF-047: `tests/skills/test_issue_worker_agents.py` (new) | source.md:392 | containment | Task 3 | 0.8 |
| INF-048: `tests/skills/test_clickup_claim.py` (new) | source.md:393 | containment | Task 2 | 0.8 |
| INF-049: `tests/skills/test_issue_repo_resolution.py` (new) | source.md:394 | containment | Task 1 | 0.8 |
| INF-050: `test_no_issue_skill_or_command_added` becomes `test_issue_command_and_skill_are_the_only_issue_primitives` | source.md:395 | containment | Task 9 | 0.6667 |
| INF-051: Run before commit: `uv run pytest tests/commands tests/core tests/skills tests/recommend tests/cli/test_issue_body_templates.py`, then `make test`. | source.md:400 | containment | Task 14 | 0.8667 |
| INF-052: `make sync-dev`, then `make verify-sync`. | source.md:405 | containment | Task 13 | 1.0 |
| INF-053: Run `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` and justify any new hit | source.md:407 | containment | Task 13 | 0.7692 |
| INF-054: Open the PR only with `/sc:pr-submit --monitor 3 | source.md:408 | none | Task 3 | 0.5 |
| INF-055: The plan's smoke step confirms one spawn per worker | source.md:434 | containment | Task 4 | 0.625 |
| INF-056: The command file and `SKILL.md` each state in one line that | source.md:441 | containment | Task 5 | 1.0 |
| INF-057: `/sc:issue --claim <N>` on an open, unassigned issue of the origin repo: the T3 worker runs first | source.md:467 | containment | Task 5 | 0.75 |
| INF-058: Running the same claim again edits both comments; the comment count on the issue does not grow. | source.md:468 | none | Task 5 | 0.5 |
| INF-059: A closed issue, or one assigned to someone else, stops with the stated message and makes no GitHub or ClickUp write. | source.md:469 | none | Task 5 | 0.5833 |
| INF-060: A claim URL for any repo other than origin stops with `E-FOREIGN-REPO` | source.md:470 | containment | Task 5 | 0.875 |
| INF-061: With `CLICKUP_API_TOKEN` unset the claim completes and the comment says ClickUp was skipped | source.md:471 | none | Task 2 | 0.5 |
| INF-062: at `standard`/`deep` a disagreement produces one marked pushback comment; no ClickUp call is made. | source.md:472 | none | Task 5 | 0.4 |
| INF-063: one manual smoke run per worker shows it was served by the pinned tier. | source.md:473 | containment | Task 15 | 1.0 |
| INF-064: `next-steps.md` contains only commands and flags listed in section 19 | source.md:474 | containment | Task 4 | 0.8889 |
| INF-065: `make verify-sync` passes; the tests of section 16 pass | source.md:475 | containment | Task 14 | 0.875 |
| INF-066: Every brainstorm row passes `--models opus,sonnet` | source.md:237 | containment | Task 5 | 1.0 |
| INF-067: Not changed: `src/superclaude/core/CLAUDE.md` (rule 10 stays; no level-table change) | source.md:380 | containment | Task 6 | 0.6667 |
