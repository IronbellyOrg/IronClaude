# Reviewer 3 brief (persona: refactorer)

Read-only reviewer. Audit the supplied hunks and matrix; you may Read/Grep/Glob the repo. Run nothing. Return findings only.

## T1 card excerpt

### Structural section (verbatim from t1-card.md)

- 6 phases, 17 tasks numbered contiguously; every `Depends on` names a lower task; no checkbox or numbered lines; no absolute or to-do-prefixed paths.


## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-04T07:10:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command projectPath=/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command

### .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/TASK-WF-scIssueCommand-20261104-064713.md:1-260

````markdown
---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-scIssueCommand-20261104-064713
version: "2"
priority: Medium
created_date: "2026-11-04"
---

# Implement the /sc:issue command, the sc-issue-protocol skill and its three pinned worker agents

Source: ./source.md
Goal: `/sc:issue --claim <number|url>` and `/sc:issue --create "<description>"` exist as an installed command, skill, three tier-pinned worker agents and two standard-library scripts, all pinned by passing tests, registered in the routing guide and documented, with `make sync-dev`, `make verify-sync`, `make lint` and the full `uv run pytest` suite passing. The live checks the source schedules (one spawn per worker, one ClickUp smoke claim) and the section 20 acceptance criteria that post to GitHub are recorded truthfully as run or pending; they may end pending when the environment or the user's approval is missing.

## Constraints

- UV only: run Python and tests with `uv run ...` (`uv run pytest`, `uv run --no-project python ...`); never `python -m`, bare `python script.py` or `pip install`.
- Edit only under `src/superclaude/`, `tests/`, `docs/` and the one plugin guide copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (source section 15 and section 17 item 1). Also allowed: this package's `./artifacts/` folder, the unstaged scratch folder `.dev/issues/smoke/` (Task 15), and one temporary Orca worktree for the master comparison (Task 14), which that task removes. `.claude/` is produced by `make sync-dev`; never edit it by hand and never `git add` any `.claude/` path except `.claude/settings.json` (never `git add -f` on `.claude/`).
- Inside the new primitives (command, skill, refs, templates, agents) every reference to another primitive uses its installed path (`~/.claude/commands/sc/<name>.md`, `~/.claude/skills/<name>/...`, `~/.claude/agents/<name>.md`) plus, for existence checks, the project `.claude/` copy; no `src/superclaude/...` path appears in them (source section 15, "Path rule").
- Never interact with the upstream parent `SuperClaude-Org/SuperClaude_Framework`: every `gh` command passes `--repo IronbellyOrg/IronClaude` (or, inside the shipped skill, `--repo <R>` resolved from `origin`), every `gh api` path spells `repos/<owner>/<repo>/...`, and the only fetch is `git fetch origin` (source section 13).
- Secrets: the executor never asks for, prints, echoes or inlines `CLICKUP_API_TOKEN` (no `echo`, `env`, `printenv` or `set -x` on it). When a live ClickUp run is needed, the user exports the variables in their own shell before starting the session (source section 12, "Never printed, logged or written to disk").
- Do not commit or push unless the user asks. `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included; staging is not committing.
- Out of scope for this plan (source section 1 and section 17 item 5): running any next-step chain, creating GitHub labels, creating ClickUp tasks, editing rule 10 of `src/superclaude/core/CLAUDE.md`, changing the level table, adding `plugins/superclaude/` command, agent or skill mirrors, listing the workers in `docs/user-guide/agents.md`, any `src/superclaude/cli/` code, and opening the pull request (done afterwards with `/sc:pr-submit --monitor 3 --head ironbelly/feat-sc-issue-command --title "..." --body "..."`).
- Live `/sc:issue --claim` or `--create` runs post directly to GitHub (source decision B1). Live checks in this plan are the two the source schedules (Task 15 worker spawns, Task 16 ClickUp smoke claim) and the section 20 acceptance record of Task 17. A run that stops before any GitHub or ClickUp write (section 20 item 4) may run without asking; any run that would assign, comment on or create a real GitHub issue needs the user's explicit approval at that moment.

## Phase 1: Deterministic helper scripts

## Task 1: Create the origin-repo resolver script and its tests

Create `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py` as specified in source section 13 and the `origin_repo.py` row of section 15: Python standard library only; it runs `git remote get-url origin` (reading only the `origin` remote, never `gh repo set-default` or any other remote) and prints `owner/repo`. It accepts `https://github.com/<owner>/<repo>`, `https://github.com/<owner>/<repo>.git`, `git@github.com:<owner>/<repo>` and `git@github.com:<owner>/<repo>.git`, tolerating a trailing `/`. A missing `origin` or a non-GitHub URL exits non-zero and prints `E-NO-ORIGIN`. Factor the URL parsing into a pure function so the tests can call it without a git checkout.

Create `tests/skills/test_issue_repo_resolution.py` (source section 16 row) that loads the script by path (the way `tests/skills/test_workflow_archive.py` loads `src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py`) and pins: https, ssh, `.git` suffix and trailing `/` all parse to `owner/repo`; a non-GitHub URL exits non-zero with `E-NO-ORIGIN`; a temporary git repository with no `origin` exits non-zero with `E-NO-ORIGIN`; a temporary repository with an `upstream` remote pointing at another GitHub repo and an `origin` remote still resolves to the `origin` value only.

Acceptance criteria:
- `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py` exists and imports only standard-library modules.
- `uv run pytest tests/skills/test_issue_repo_resolution.py -v` passes, with at least one test each for https, ssh, `.git` suffix, trailing `/`, non-GitHub URL, missing `origin`, and origin-only resolution when another remote exists.
- `uv run --no-project python src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py` run in this checkout prints `IronbellyOrg/IronClaude`; the output is saved to `./artifacts/t1-origin-repo.txt`.

## Task 2: Create the ClickUp claim script and its tests

Create `src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py` exactly as source section 12 specifies: standard library only (`urllib`); arguments `--issue-url <url> --issue-number <N> --repo <owner/repo>`; configuration only from the environment variables `CLICKUP_API_TOKEN`, `CLICKUP_WORKSPACE_ID`, `CLICKUP_LIST_IDS` (optional, comma-separated, sent as `list_ids[]=`) and `CLICKUP_MAX_PAGES` (optional, default `20`). Steps, in order: token or workspace missing prints `{"status": "skipped", "reason": "no_token"|"no_workspace"}` and exits 0; `GET https://api.clickup.com/api/v2/user` for the token owner's user ID; page through `GET https://api.clickup.com/api/v2/team/{CLICKUP_WORKSPACE_ID}/task?page=<p>&subtasks=true&include_markdown_description=true` until an empty page or the page cap; match by rule 1 (the issue URL `https://github.com/<owner>/<repo>/issues/<N>` in the markdown description or any custom field value, case-insensitive, trailing `/` or `#...` ignored), and only if rule 1 found nothing, rule 2 (`#<N>` as a whole token in the task name, not followed by a digit) (source default D2); more than one match prints `{"status": "ambiguous", "candidates": [...]}` with no PUT; none prints `{"status": "not_found"}`; already an assignee prints `{"status": "already_assigned", ...}` with no PUT; otherwise `PUT https://api.clickup.com/api/v2/task/{task_id}` with body `{"assignees": {"add": [<user id>]}}` and print `{"status": "assigned", "task_id": ..., "task_url": ..., "rule": "github_link"|"title_number"}`. HTTP 401/403 prints `{"status": "error", "reason": "auth"}`; HTTP 429 waits the `Retry-After` seconds once, retries once, then prints `{"status": "error", "reason": "rate_limited"}`; any other failure prints `{"status": "error", "reason": "<short>"}`. Exit 0 for every outcome above; exit 2 only for bad arguments. The token is never printed, logged or written to disk. Take the `GET /user`, task-list and update-task response shapes and the first page number of the task list from the ClickUp v2 reference (`developer.clickup.com/reference/getfilteredteamtasks`, `.../updatetask`, read through Context7 or the web) and record them in the script's module docstring. Define and document in the docstring what the script does when `CLICKUP_MAX_PAGES` is not a positive integer.

Create `tests/skills/test_clickup_claim.py` (source section 16 row) with `urllib` patched and recorded JSON fixtures for the three response shapes. Every test clears `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` with `monkeypatch.delenv(..., raising=False)` before setting the values it needs, so an exported real token never reaches a test. Fixtures hold made-up values only. The tests pin: skipped without token; skipped without workspace; GitHub-link match beats title match; title match only as a whole `#N` token (`#3020` does not match `#302`); ambiguous returns candidates and makes no PUT; already-assigned makes no PUT; assign sends `{"assignees": {"add": [id]}}`; 401 gives `auth`; 429 is retried exactly once (with the sleep patched); the page cap from `CLICKUP_MAX_PAGES` is honoured and the first requested page is the documented first page; the documented behaviour for a non-positive or non-integer `CLICKUP_MAX_PAGES`; the token value never appears in stdout or stderr in any test; bad arguments exit 2.

Acceptance criteria:
- `src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py` exists, imports only standard-library modules, and its docstring names the ClickUp v2 endpoints, the response fields and the first page number it relies on.
- `uv run pytest tests/skills/test_clickup_claim.py -v` passes, with one test per behaviour listed above.
- `env -u CLICKUP_API_TOKEN -u CLICKUP_WORKSPACE_ID uv run --no-project python src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py --issue-url https://github.com/IronbellyOrg/IronClaude/issues/302 --issue-number 302 --repo IronbellyOrg/IronClaude` prints `{"status": "skipped", "reason": "no_token"}` and exits 0; output saved to `./artifacts/t2-clickup-skipped.txt`.

## Phase 2: Tier-pinned worker agents

## Task 3: Create the three issue worker agents and their tests

Create `src/superclaude/agents/issue-worker-t3.md`, `src/superclaude/agents/issue-worker-t2.md` and `src/superclaude/agents/issue-worker-t1.md` (source section 15 rows, section 6, defaults D3, D19 and D27). Frontmatter: `name` equal to the file stem, a one-line `description`, `model: claude-gw-tier3` / `model: claude-gw-tier2` / `model: claude-gw-tier1a` respectively (no `[1m]` suffix), and `tools: Read, Grep, Glob, Write, Bash` (no `Edit`). Follow the frontmatter shape of existing agents such as `src/superclaude/agents/evidence-validator.md`. The body states: the worker's jobs for its tier (section 5 architecture diagram and section 6 tier table); it makes read-only `gh` calls only, always with `--repo <R>` as given by the orchestrator, and its only git write is `git fetch origin` (no other remote is added or fetched; source section 7 Wave 1 and section 13); it never writes to GitHub or ClickUp and never edits source code; it writes only under `.dev/issues/`; every file it writes starts from the named template under `~/.claude/skills/sc-issue-protocol/templates/` (project `.claude/skills/sc-issue-protocol/templates/` as the in-checkout copy); it runs `/sc:analyze` by following `~/.claude/commands/sc/analyze.md` when its job needs a codebase pass, falling back to Grep/Glob/Read when codegraph or auggie is unavailable and recording that in its file (section 14 last row); it returns only the path of the file it wrote.

Create `tests/skills/test_issue_worker_agents.py` (source section 16 row) pinning: the three files exist with `model:` equal to `claude-gw-tier3`, `claude-gw-tier2`, `claude-gw-tier1a`; each picker ID's tier key (`tier3`, `tier2`, `tier1a`) exists under `tiers` in `src/superclaude/skills/ccsession-tag/ccsession-models.json`; the `tools` list excludes `Edit`; each body states read-only GitHub access, the `git fetch origin`-only rule and writing only under `.dev/issues/`; every `gh issue`, `gh pr` and `gh label` line in a body carries `--repo`; no body contains `src/superclaude/`.

Acceptance criteria:
- The three agent files exist under `src/superclaude/agents/` with the exact `model:` values above and no `Edit` tool.
- `uv run pytest tests/skills/test_issue_worker_agents.py -v` passes.
- `grep -rn 'src/superclaude' src/superclaude/agents/issue-worker-t1.md src/superclaude/agents/issue-worker-t2.md src/superclaude/agents/issue-worker-t3.md` prints nothing.

## Phase 3: Skill package

## Task 4: Create the fourteen output templates

Create these files under `src/superclaude/skills/sc-issue-protocol/templates/` (source sections 10 and 15): `issue-feature-simple.md`, `issue-feature-complex.md`, `issue-bug-simple.md`, `issue-bug-complex.md`, `summary.md`, `accuracy-check-comment.md`, `claim-comment.md`, `next-steps.md`, `scout-report.md`, `recommend-record.md`, `description.md`, `flags-decision.md`, `draft-notes.md`, `create-review-comment.md`.

Content rules:
- The four issue-body templates carry, in this order, exactly the section headings listed for them in the source section 10 template table (bug simple: Bug Summary; Environment (OS, version); Current Behavior; Expected Behavior; Steps to Reproduce; Impact Assessment (Severity, Blast Radius); Error Messages; Codebase Context (from `/sc:analyze`); Related Issues; Testing Notes. Bug complex: all of those plus Frequency; User Impact; Business Impact; Cascading Effects; Logs and Stack Trace; Attempted Solutions; Proposed Solution; For Development Team (Root Cause Analysis, Fix Approach, Verification Plan). Feature simple: Feature Summary; Problem Statement; User Story; Proposed Solution; Acceptance Criteria; Out of Scope; Components Affected (from `/sc:analyze`); Related Issues/PRs. Feature complex: all of those plus Success Metrics; Architecture Impact; Dependencies; Testing Strategy; Documentation Needs; Alternatives Considered; Impact Analysis (Blast Radius, Integration Impact); Risks & Mitigation; Effort Estimate (hours) and Complexity). They contain no `ClickUp` text, no GPU/hardware fields, no "Automatic Labels" footer, and use hours instead of person-weeks (B3, B6). Each placeholder says to write "Not known yet" when nothing is known. Each ends with `<!-- sc:issue:create template=<template stem> -->`.
- `accuracy-check-comment.md` carries a verdict field (`current` or `out_of_date`) and per-claim evidence rows, and ends with `<!-- sc:issue:accuracy-check -->`.
- `claim-comment.md` carries: who claimed it, the ClickUp result, the summary overview with effort (hours), complexity, accuracy verdict and first next step inline, repo-relative links to `.dev/issues/<N>/summary.md`, `.dev/issues/<N>/next-steps.md` and `.dev/issues/<N>/analysis/`, and the one-line note that those links open on GitHub only after someone commits and pushes the files (default D9). It ends with `<!-- sc:issue:claim -->`.
- `create-review-comment.md` carries the user's flags, the worker's choice and the reasons for each difference, and ends with `<!-- sc:issue:create-review -->`.
- `summary.md` carries: what the issue asks for, relevant files and systems (the cheatsheet), type, complexity, effort estimate in hours, links to `analysis/` (section 7 Wave 4).
- `next-steps.md` starts with the `/model claude-gw-tier2` or `/model claude-gw-tier1a` tier line, then the ordered commands with flags and inputs, the effort estimate, and an optional line naming the unused default row when `/sc:recommend` chose differently (section 7 Wave 5, defaults D6 and D23).
- `scout-report.md` has a claim section (state, assignees, current login, earlier claim and accuracy-check comment IDs, merged PRs and changed files since creation and whether that list was truncated, complexity and type guesses with one-line reasons) and a create section (repo labels, possible duplicates) (sections 7 and 8 Wave 1).
- `recommend-record.md` is a header plus one verbatim block; `description.md` holds the raw description; `flags-decision.md` holds mode, type, complexity and reasons; `draft-notes.md` has a "New material" list and a "Contradictions" list (section 8 Waves 2 and 4).

Acceptance criteria:
- All fourteen template files exist at the paths above.
- The four issue templates' `##` headings match the source section 10 order exactly, and `grep -il clickup` over them prints nothing.
- Every posted template (`accuracy-check-comment.md`, `claim-comment.md`, `create-review-comment.md` and the four issue templates) has its marker as its last non-empty line.
- No template contains `src/superclaude/`.

## Task 5: Create the five skill refs

Depends on: Task 4

Create under `src/superclaude/skills/sc-issue-protocol/refs/`:
- `claim.md`: claim Waves 0 to 6 of source section 7 in detail, the gh commands exactly as written there (each with `--repo <R>`), with one addition: the merged-PR query `gh pr list --repo <R> --state merged ...` also passes `--limit 200` and the worker records in `scout.md` when the result hit that limit (gh's default is 30). Wave 1 also carries the git commands as written there: `git fetch origin` (origin only; no other remote is added or fetched) followed by `git log --since=<createdAt> --name-only` on `origin/<default branch>`. Also: the edge-case STOPs of Wave 2 (closed, assigned to someone else, pull request number, re-claim allowed), the marker handling that edits an earlier `<!-- sc:issue:claim -->` / `<!-- sc:issue:accuracy-check -->` comment with `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<file>` instead of posting a duplicate (B9, D18), the ClickUp script call `uv run --no-project python "<skill base>/scripts/clickup_claim.py" --issue-url <url> --issue-number <N> --repo <R>` writing stdout to `.dev/issues/<N>/clickup.json`, and the effort and complexity rubric of default D5 (simple up to 4 hours in one area; medium over 4 up to 16 hours; complex over 16 hours, more than one subsystem, or a security/data-migration change; effort recorded in hours).
- `create.md`: create Waves 0 to 5 of source section 8, the draft directory `.dev/issues/draft-<YYYYMMDD-HHMMSS>-<slug>/` renamed to `.dev/issues/<N>/` after creation (D10), the flag-settling table of Wave 2 (including D12 and D13: deep with all flags given runs `Skill sc:adversarial-protocol` with `--compare <D>/flags-user.md,<D>/flags-t1.md --depth quick`), complexity following depth (D17), the template choice of Wave 3, the depth-to-worker table of Wave 4, the one-question contradiction prompt rule (D14), duplicates listed in related issues without stopping (D11), labels intersected with the repo's labels and never created (B7), title prefixes `[FEATURE] ` / `[BUG] ` (D21), no ClickUp call and no self-assignment (B6).
- `chains.md`: the six default chains of source section 9 copied exactly (tier lines and chains, every brainstorm step with `--models opus,sonnet` and no `--handoff`), the four notes under that table, and the `/sc:recommend` goal format of section 7 Wave 5 step 1 (issue URL, type, complexity, summary path, suggested default row).
- `labels.md`: the fixed label set of source section 11 and one `gh label create "<name>" --repo <owner/repo>` line per label for a maintainer to run by hand (D16), with the statement that the skill never runs them.
- `tiers.md`: the tier map of source section 6, the four verified pinning facts (resolution order; the Agent call's `model` parameter takes aliases only and overrides frontmatter; frontmatter accepts a full model ID; `haiku` follows `ANTHROPIC_DEFAULT_HAIKU_MODEL`), the note that an installed mod's `agent.spawn` hook can override the pin, and `E-TIER-UNAVAILABLE` with no alias fallback (D4).

Every one of the five refs carries the sentence "Spawn workers with `subagent_type: issue-worker-t<N>` and never pass the `model` parameter." (source section 6: "`SKILL.md` and every ref state"). Each ref names agents and the analyze command by installed path (`~/.claude/agents/issue-worker-t<N>.md`, project `.claude/agents/` first; `~/.claude/commands/sc/analyze.md`) and templates by their path relative to the skill base.

Acceptance criteria:
- The five ref files exist at the paths above.
- `grep -n -- '--handoff' src/superclaude/skills/sc-issue-protocol/refs/chains.md` shows no `--handoff tasklist` and no `--handoff design`; every `/sc:brainstorm` line in it carries `--models opus,sonnet`.
- `grep -rIn 'src/superclaude' src/superclaude/skills/sc-issue-protocol/refs` prints nothing.
- `grep -L 'never pass the `model` parameter' src/superclaude/skills/sc-issue-protocol/refs/*.md` prints nothing (all five refs carry the phrase).
- `refs/claim.md` contains `git fetch origin` and `--limit 200` on the merged-PR query.

## Task 6: Write the orchestrator SKILL.md

Depends on: Task 1, Task 2, Task 3, Task 5

Create `src/superclaude/skills/sc-issue-protocol/SKILL.md` (source section 15 row, sections 5, 7, 8, 13, 14, D26). Frontmatter: `name: sc:issue-protocol`, a one-line `description`, `allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, Skill, AskUserQuestion`. Body, fewer than 500 lines as counted by `len(text.splitlines())`, at the WHAT/WHEN level: the two modes; Wave 0 of both modes calls `uv run --no-project python "<skill base>/scripts/origin_repo.py"` to resolve `<R>` (STOP `E-NO-ORIGIN`); per-wave ref loading (`refs/claim.md` for claim, `refs/create.md` for create, `refs/chains.md` in claim Wave 5, `refs/labels.md` in create Wave 5, `refs/tiers.md` before the first spawn); the claim waves and the create waves as short steps pointing at their refs; the spawn rule ("spawn workers with `subagent_type: issue-worker-t<N>` and never pass the `model` parameter"); the orchestrator is the only place that writes to GitHub or ClickUp, and every `gh` call carries `--repo <R>` while every `gh api` path spells `repos/<R>/...` (section 13); `/sc:recommend` invoked as `Skill sc-recommend` with its output saved verbatim to `.dev/issues/<N>/recommend.md`; the claim stops after posting and printing the `next-steps.md` path, never running a next-step command (B2); the return contract fields `status`, `mode`, `issue_number`, `issue_url`, `dir`, `clickup_status`, `labels_applied`, `labels_missing`, `next_steps_path`; the full error table of source section 14 with every STOP code (`E-NO-ORIGIN`, `E-FOREIGN-REPO`, `E-GH-AUTH`, `E-NOT-AN-ISSUE`, `E-TIER-UNAVAILABLE`, `E-WORKER-NO-OUTPUT`, `E-ASSIGN-FAILED`, `E-POST-FAILED`, `E-CREATE-FAILED`); the D26 one-line note that for issues filed through `/sc:issue --create` its four templates replace the `ISSUE-HANDOFF.md` / `ISSUE-BACKLOG.md` instruction of rule 10 in the distributed `CLAUDE.md`; `.dev/issues/` is never staged or committed by the skill (D24); Will / Will Not. Every ref and template the skill uses is named in `SKILL.md` by its skill-relative path (`refs/...`, `templates/...`, `scripts/...`).

Acceptance criteria:
- `src/superclaude/skills/sc-issue-protocol/SKILL.md` exists, has fewer than 500 lines by the `len(text.splitlines())` rule (the same rule Task 7's test uses), and has the frontmatter above.
- Every `refs/*.md`, `templates/*.md` and `scripts/*.py` file in the skill directory is named in `SKILL.md`, and every such path named in `SKILL.md` exists.
- `SKILL.md` contains "never pass the `model` parameter", every STOP code listed above, and the D26 rule-10 line.
- `grep -n 'src/superclaude' src/superclaude/skills/sc-issue-protocol/SKILL.md` prints nothing.

## Task 7: Add the skill package tests

Depends on: Task 6

Create `tests/skills/test_issue_protocol.py` (source section 16 row) pinning:
- `SKILL.md` frontmatter (`name: sc:issue-protocol`, the `allowed-tools` list) and size: fewer than 500 lines by `len(text.splitlines())`.
- Every ref, template and script named in `SKILL.md` exists, and every file in `refs/`, `templates/` and `scripts/` is named in `SKILL.md`.
- The text "never pass the `model` parameter" is present in `SKILL.md` and in every `refs/*.md` file.
- Every posted template ends with its marker (`accuracy-check-comment.md`, `claim-comment.md`, `create-review-comment.md`, and `<!-- sc:issue:create template=<stem> -->` on the four issue templates).
- The four issue templates carry the source section 10 headings in order and contain no `ClickUp` text (case-insensitive).
- Every `/sc:*` flag in `refs/chains.md` exists in the command file it names, read from `src/superclaude/commands/<name>.md` (the `_command_text` source used by `test_every_notes_flag_exists_in_its_command` in `tests/core/test_how_we_work_routing_table.py`), and `/task` is checked against `src/superclaude/skills/task/SKILL.md`. Reading only the source copies is a deliberate narrowing of source section 16's "installed-or-source" wording so the test does not depend on the machine's `~/.claude` install; say so in the test's docstring.
- `refs/chains.md` contains no `--handoff tasklist` and no `--handoff design` on a `/sc:brainstorm` step, and every `/sc:brainstorm` step passes `--models opus,sonnet`.
- Fork safety (source section 13 and section 20 item 4): every line in `SKILL.md`, `refs/*.md` and the three `src/superclaude/agents/issue-worker-t*.md` bodies that runs `gh issue`, `gh pr` or `gh label` carries `--repo`, and no file in the skill or the three agents contains the `{owner}/{repo}` placeholder.
- No text file under `src/superclaude/skills/sc-issue-protocol/` contains `src/superclaude/`; the scan skips `__pycache__/` and files that do not decode as UTF-8.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_protocol.py -v` passes.
- Deleting the marker line from a copy of `templates/claim-comment.md` in a temporary directory makes the marker test fail, and a temporary copy of a ref with a `gh issue view` line lacking `--repo` makes the fork-safety test fail (shown by parametrised negative cases or helper unit tests inside the same file).

## Phase 4: Command file and inventory tests

## Task 8: Create the /sc:issue command file and its test

Depends on: Task 6

Create `src/superclaude/commands/issue.md` (source section 4 and the `issue.md` row of section 15), about 100 to 150 lines: frontmatter `name: issue`, a one-line `description`, `category: workflow`, `complexity: advanced`, `mcp-servers: [auggie, codegraph]`, `personas: [analyzer]`, `argument-hint`; Usage block (the two lines of section 4); Options table listing exactly `--claim`, `--create`, `--depth`, `--mode`, `--type` with the defaults and allowed values of section 4 (`--depth quick|standard|deep`, `--mode feature|bug`, `--type cicd|command|skill|agent|hook|cli|core|docs|tests|install|other`); STOP rules before Activation (exactly one of `--claim` / `--create`; `--depth`/`--mode`/`--type` with `--claim` is `E-CREATE-ONLY-FLAG`; unknown values list the allowed values; empty description); the statement that there is no `--repo`, dry-run or preview flag; Examples; Boundaries; the D26 one-line rule-10 note; `## Activation` reading "Skill sc:issue-protocol" and naming `~/.claude/skills/sc-issue-protocol/SKILL.md`. Follow the shape of an existing thin command such as `src/superclaude/commands/workflow.md`.

Create `tests/commands/test_issue_command.py` (source section 16 row) pinning: the frontmatter fields above; the Options table lists exactly the five flags with the allowed values of section 4; Activation names `Skill sc:issue-protocol`; no `src/superclaude/` path; no `--repo` flag row and no `--dry-run`/`--preview` flag; the command file and `src/superclaude/skills/sc-issue-protocol/SKILL.md` each carry the D26 rule-10 line.

Acceptance criteria:
- `src/superclaude/commands/issue.md` exists with the frontmatter, Options table, STOP rules and Activation above.
- `uv run pytest tests/commands/test_issue_command.py -v` passes.

## Task 9: Replace the no-issue-command guard and register the command in the refresh inventory

Depends on: Task 8

In `tests/cli/test_issue_body_templates.py`, replace `test_no_issue_skill_or_command_added` (it asserts that no `sc-issue*` skill and no `issue.md` command exist under `src/superclaude` or `plugins/superclaude`) with `test_issue_command_and_skill_are_the_only_issue_primitives`: `src/superclaude/commands/issue.md` and the directory `src/superclaude/skills/sc-issue-protocol/` exist; under `src/superclaude/skills` the only `sc-issue*` entry is `sc-issue-protocol`; under `src/superclaude/commands` the only `issue.md` is the top-level one; under `plugins/superclaude` no `sc-issue*` skill and no `issue.md` command exist (no mirrors are added, source section 15 "Not changed"). Leave the other tests in the file, including `test_claude_md_has_exactly_one_issue_rule_line`, unchanged (source section 3 last row, section 16, D26).

In `tests/recommend/test_routing_refresh.py`, add `"issue"` to `_POST_REFRESH_ADDITIONS` (currently `{"graph", "impact"}`) and extend the comment above it to name issue #302 as the source of `/sc:issue`, the same way `graph` and `impact` were added (source section 15 row).

Acceptance criteria:
- `grep -n 'test_no_issue_skill_or_command_added' tests/cli/test_issue_body_templates.py` prints nothing and `test_issue_command_and_skill_are_the_only_issue_primitives` exists.
- `uv run pytest tests/cli/test_issue_body_templates.py tests/recommend/test_routing_refresh.py -v` passes, including `test_command_dispositions_trace_appendix_c_and_inventory`.

## Phase 5: Routing registration and documentation

## Task 10: Register /sc:issue in the routing guide and its plugin copy

Depends on: Task 8

In `src/superclaude/core/HOW-WE-WORK.md`, add one row for `/sc:issue` to the "Other commands" table between `<!-- other-commands:v1 -->` and `<!-- /other-commands -->` (source section 15 row): claim assigns the issue, checks its accuracy, writes a summary and a next-step prompt, then stops; create files a templated GitHub issue on the origin repo; both post directly to GitHub and write `.dev/issues/`. Keep the table's existing row style. The row is ASCII only (`test_guide_is_ascii_except_the_ruling_example`) and backticks no `/...` token other than `/sc:issue` unless it names an existing command (`test_other_commands_membership_and_live_references`), both in `tests/core/test_how_we_work_routing_table.py`. The level table is not changed, so `src/superclaude/core/CLAUDE.md` is not changed.

Copy the edited `src/superclaude/core/HOW-WE-WORK.md` byte-for-byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (required by `tests/commands/test_routing_plugin_parity.py`; source section 17 item 3).

In `tests/core/test_how_we_work_routing_table.py`, add `"sc:issue"` to `_OTHER_COMMANDS` (source section 16 row); the existing live-reference check then proves the command file exists.

Acceptance criteria:
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` reports no difference.
- `_OTHER_COMMANDS` in `tests/core/test_how_we_work_routing_table.py` contains `"sc:issue"`.
- `uv run pytest tests/core tests/commands -v` passes; its output is saved to `./artifacts/t10-core-commands.log`.

## Task 11: Document picker-ID pinning in the developer guide

In `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (source section 15 row, section 6):
- Section 4.1 "Anatomy of an Agent File": state that the optional `model:` field takes an alias, a full model ID or picker ID (for example `claude-gw-tier3`), or `inherit`; that the Agent call's `model` parameter accepts aliases only and overrides the frontmatter; so a skill that needs a pinned tier spawns the agent by `subagent_type` and must not pass `model`.
- Section 4.3 "Agent Spec Format (Dynamic Instantiation)": add one line saying the `<model>` in agent specs is an alias.

Acceptance criteria:
- Section 4.1 of the developer guide contains the picker-ID sentence and the "must not pass `model`" rule; section 4.3 contains the alias line.
- `git diff -U0 -- docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` shows hunks only between the `### 4.1` heading and the `### 4.4` heading.

## Task 12: Document /sc:issue in the user command reference

Depends on: Task 8

In `docs/user-guide/commands.md` (source section 15 row):
- Add a row to the "8. UTILITIES" table: `/sc:issue`, purpose "Claim a GitHub issue (assign, accuracy check, summary, next-step prompt) or create a templated issue", file `issue.md`, "Changes files?" = "Yes (posts to GitHub; writes `.dev/issues/`)". Link it to the new section anchor the way `/sc:graph` is linked.
- Add a `### /sc:issue - GitHub Issue Claim and Create` section under "Detailed Description of Each Command", in the same shape as the neighbouring command sections: what it does, the usage lines of source section 4, the Options table, two or three examples (`/sc:issue --claim 302`, `/sc:issue --create "..." --mode bug --type cli --depth standard`), and the facts that it posts directly to GitHub, never creates labels, assigns the ClickUp task only on claim when `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` are set, and stops after writing `next-steps.md`.

Acceptance criteria:
- `docs/user-guide/commands.md` has the UTILITIES row and the `/sc:issue` section; the row's anchor link resolves to that section's heading.
- Every flag named in the new section exists in `src/superclaude/commands/issue.md`'s Options table.

## Phase 6: Sync, full-suite pass, scheduled smoke checks and acceptance record

## Task 13: Regenerate the dev copies and check sync and installed-path hygiene

Depends on: Task 7, Task 9, Task 10, Task 11, Task 12

Run `make sync-dev`, then `make verify-sync` (source section 17 item 2). Run `grep -rIn 'src/superclaude' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core src/superclaude/hooks` (source section 17 item 4; `-I` skips binary files such as `__pycache__` bytecode) and compare its hits with the fork's master: `git fetch origin`, then `git grep -n 'src/superclaude' origin/master -- src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core src/superclaude/hooks` (`git stash` is not used). Stage nothing under `.claude/`.

Acceptance criteria:
- `make verify-sync` exits 0; output saved to `./artifacts/t13-verify-sync.log`.
- The path grep shows no hit in `src/superclaude/commands/issue.md`, `src/superclaude/skills/sc-issue-protocol/` or `src/superclaude/agents/issue-worker-t*.md`; both grep outputs are saved to `./artifacts/t13-path-grep.txt` with any pre-existing hit marked as pre-existing.
- `git status --porcelain .claude` shows no staged `.claude/` path other than `.claude/settings.json`.

## Task 14: Make the full test suite, lint and sync check pass

Depends on: Task 13

Run the full suite and checks the source names (section 16 last line, section 20 item 9): `uv run pytest tests/commands tests/core tests/skills tests/recommend tests/cli/test_issue_body_templates.py`, then the full suite `uv run pytest` (`make test` runs the same command), then `make lint`, then `make verify-sync`. Fix every failure caused by this feature in the file that causes it (re-running `make sync-dev` after any `src/superclaude/` fix). A failure that also occurs on master without this feature's changes is not fixed here: show that by running the same failing test on master in a temporary Orca worktree (`orca worktree create --name issue302-master-check --base-branch origin/master`; never a raw `git worktree add`), record it as pre-existing with the test ID and error line, then remove the worktree with `orca worktree rm --worktree name:issue302-master-check`.

Acceptance criteria:
- `./artifacts/t14-targeted.log`, `./artifacts/t14-full-pytest.log`, `./artifacts/t14-lint.log` and `./artifacts/t14-verify-sync.log` exist and hold the command outputs with their exit codes.
- `uv run pytest` reports no failure caused by this feature; `make lint` and `make verify-sync` exit 0.
- Every remaining failure is listed in `./artifacts/t14-failures.md` with the test ID, the error line and the evidence that it also fails on master; if there are none, the file says so.
- `orca worktree list` shows no `issue302-master-check` worktree.
- `git add .dev/tasks` has been run so this package and its `artifacts/` are staged; nothing is committed or pushed.

## Task 15: Smoke-spawn each worker agent on its pinned tier

Depends on: Task 14

The source schedules one manual smoke spawn per worker to confirm that the pinned picker ID is served (source section 6, section 20 item 7, default D19). Agent definitions load when a Claude Code session starts, so this check needs a session started after Task 13. If the current session started before Task 13, stop here and ask the user to start a new session in this checkout and re-run the same `/sc:implement` command; it resumes at this task. In that session, spawn `issue-worker-t3`, `issue-worker-t2` and `issue-worker-t1` once each with the Agent tool using only `subagent_type` and never the `model` parameter, with a harmless prompt that writes one file under `.dev/issues/smoke/`. Served-model evidence must come from a source outside the worker: the gateway or proxy request log entry for the call, or the model field of the subagent's transcript; the worker's own statement of its model is recorded but is not accepted as evidence. A spawn that fails because the picker ID is not served is recorded as `E-TIER-UNAVAILABLE` with the agent file and picker ID, not worked around with an alias. `.dev/issues/smoke/` is never staged; delete it afterwards only with the user's approval.

Acceptance criteria:
- `./artifacts/t15-tier-smoke.md` exists with one row per worker giving the spawn outcome and one of: served (with the external evidence source and the picker ID it shows), `E-TIER-UNAVAILABLE` (with the reason), or pending (with the reason the session could not run it). The row states the truth; a pending or unavailable row is a valid result of this task.
- `git add .dev/tasks` has been run after writing the artifact.

## Task 16: Run the manual ClickUp smoke claim against a test task

Depends on: Task 14

The source schedules one manual smoke claim against a ClickUp test task (source section 12, last paragraph; section 20 item 5). It needs a ClickUp test task whose description links a test GitHub issue URL on `IronbellyOrg/IronClaude`, and `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` exported by the user in their own shell before the session started. Ask the user only for the test issue URL and task ID; never ask for, print, echo or inline the token or workspace values. If the variables are not exported, record the task as pending and stop. Otherwise run `uv run --no-project python src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py --issue-url <test issue url> --issue-number <N> --repo IronbellyOrg/IronClaude` twice (the second run should report `already_assigned`). Compare the live response shapes with the fixtures in `tests/skills/test_clickup_claim.py` by key paths only, without printing or copying live values; never copy live values into fixtures. If the shapes differ, update the fixtures with made-up values and the script, then re-run `uv run pytest tests/skills/test_clickup_claim.py -v`, `make sync-dev`, `make verify-sync` and `make lint`.

Acceptance criteria:
- `./artifacts/t16-clickup-smoke.md` records either both runs' status fields (first `assigned` with `rule: github_link`, second `already_assigned`), the test task ID and whether the live key paths matched the fixtures, or "pending" with the reason (variables not exported, or no test task). The token and workspace values appear nowhere in it.
- If the script or fixtures changed: `uv run pytest tests/skills/test_clickup_claim.py -v` passes and `make verify-sync` and `make lint` exit 0, with outputs saved under `./artifacts/t16-*.log`.
- `git add .dev/tasks` has been run after writing the artifact.

## Task 17: Record the section 20 acceptance criteria as run or pending

Depends on: Task 14

Write `./artifacts/t17-acceptance.md` with one row per source section 20 acceptance criterion (items 1 to 9). Each row says run (with the evidence: a test name, artifact path or command output) or pending live verification (with the exact command a user would run and what it needs). Items 7 and 9 point at the Task 3, Task 7, Task 14 and Task 15 evidence; item 5's ClickUp half points at Task 2 and Task 16. Item 4 (a claim URL for another repo stops with `E-FOREIGN-REPO`) stops in Wave 0 before any GitHub or ClickUp write, so run it once in a session that has the skill loaded (after Task 13) as `/sc:issue --claim https://github.com/octocat/Hello-World/issues/1` and record the output. Items 1, 2, 3, 6 and 8 assign, comment on or create real issues or need a worker spawn; leave them pending with their exact commands unless the user approves a run against a test issue at that moment (source decision B1; an incorrect Wave 2 guard would reach `gh issue edit --add-assignee`).

Acceptance criteria:
- `./artifacts/t17-acceptance.md` has nine rows, each run or pending, with evidence or the exact command.
- The item 4 row shows `E-FOREIGN-REPO` from a real run, or pending with the reason the session could not run it.
- No GitHub issue was assigned, commented on or created without the user's approval in this task.
- `git add .dev/tasks` has been run after writing the artifact.
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
| INF-014: No ClickUp call (B6). No self-assignment. | source.md:219 | containment | Task 5 | 1.0 |
| INF-015: Every posted template ends with its hidden marker line | source.md:270 | containment | Task 4 | 0.8333 |
| INF-016: holds the one-time `gh label create | source.md:282 | containment | Task 3 | 0.6 |
| INF-017: --issue-url <url> --issue-number <N> --repo <owner/repo> | source.md:289 | containment | Task 2 | 1.0 |
| INF-018: Never printed, logged or written to disk | source.md:296 | containment | Task 2 | 1.0 |
| INF-019: Exit 0 for every outcome above; exit 2 only for bad arguments. | source.md:310 | containment | Task 2 | 1.0 |
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
| INF-055: The plan's smoke step confirms one spawn per worker | source.md:434 | containment | Task 4 | 0.625 |
| INF-056: The command file and `SKILL.md` each state in one line that | source.md:441 | containment | Task 5 | 1.0 |
| INF-057: `/sc:issue --claim <N>` on an open, unassigned issue of the origin repo: the T3 worker runs first | source.md:467 | containment | Task 5 | 0.75 |
| INF-060: A claim URL for any repo other than origin stops with `E-FOREIGN-REPO` | source.md:470 | containment | Task 5 | 0.875 |
| INF-063: one manual smoke run per worker shows it was served by the pinned tier. | source.md:473 | containment | Task 15 | 1.0 |
| INF-064: `next-steps.md` contains only commands and flags listed in section 19 | source.md:474 | containment | Task 4 | 0.8889 |
| INF-065: `make verify-sync` passes; the tests of section 16 pass | source.md:475 | containment | Task 14 | 0.875 |
| INF-066: Every brainstorm row passes `--models opus,sonnet` | source.md:237 | containment | Task 5 | 1.0 |
| INF-067: Not changed: `src/superclaude/core/CLAUDE.md` (rule 10 stays; no level-table change) | source.md:380 | containment | Task 6 | 0.6667 |
