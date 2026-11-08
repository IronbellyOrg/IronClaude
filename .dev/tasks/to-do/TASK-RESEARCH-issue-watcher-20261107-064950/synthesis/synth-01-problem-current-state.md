# Synthesis 01: Problem Statement and Current State Analysis

**Date:** 2026-11-07
**Report sections covered:** 1 (Problem Statement), 2 (Current State Analysis)
**Sources (task folder `.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/`):**
- `research/01-claim-flow-and-session-launch.md` (cited as "R01 section N")
- `research/02-github-surface-and-cli-patterns.md` (cited as "R02 section N")
- `research/03-governance-and-security-surface.md` (cited as "R03 section N")
- `gaps-and-questions.md` (cited as "GQ #N")
- `research/research-notes.md`, sections "ADDENDUM 2026-11-07T07:03Z" and "ADDENDUM 2 2026-11-07T07:12Z" (binding)
- `BUILD-REQUEST.md`, `GOAL` and `WHY` lines only

**Rules applied:** every Section 2 claim cites the file path and line number the research files give. File paths inside Section 2 are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/` unless absolute. Tags: [CODE-VERIFIED], [CODE-CONTRADICTED], [UNVERIFIED]. No web research is used in this file; every `[UNVERIFIED]` item is listed under "Carried to Open Questions" at the end.

---

## 1. Problem Statement

- **The question:** GitHub issue #331 of `IronbellyOrg/IronClaude` asks for a watcher that finds issues that are tagged, human-approved, in a GitHub Project and in Backlog status, and makes the right developer's Coder workspace start a new session running `/sc:issue --claim <N>` (BUILD-REQUEST `GOAL`). The issue asks three things, and the research task exists to answer them with existing solutions first (BUILD-REQUEST `WHY`):

  | # | Question asked by issue #331 | Answer in the research, after the owner decision |
  |---|---|---|
  | 1 | Microservice versus GitHub Action | Owner chose neither of the push designs: option A, a workspace-side poller (see "Owner decisions" below). B (GitHub Action plus workspace listener) and C (central microservice plus listener) remain documented alternatives and revisit conditions (`research/research-notes.md`, ADDENDUM 2). |
  | 2 | How to securely tie each workspace to a GitHub account | Under A the tie is the workspace's own `gh` login, which both the poller and `/sc:issue --claim` use (R03 section 7, "Authentication of workspace to GitHub account" row). Whether the Coder workspace owner is the same person as that `gh` login is not checkable inside this repo [UNVERIFIED] (R03 Gaps 14, GQ #19). |
  | 3 | What the Coder-side listener is | Under A there is no listener, no inbound port and no address registry (ADDENDUM 2). The 5-minute poller is the whole "Coder-side listener" (R01 Gaps 9, R03 Gaps 15, GQ #9); where it runs and keeps its state is not established by any repo file [UNVERIFIED]. |

- **Why it matters:**
  - Nothing starts a claim automatically today: `/sc:issue` triggers are "Explicit only: the user types `/sc:issue --claim ...`" (`src/superclaude/commands/issue.md:24`, R01 section 1). A watcher is therefore new machinery, not a configuration of an existing one.
  - The repository `IronbellyOrg/IronClaude` is PUBLIC (`gh repo view ... --json visibility,isPrivate,isFork` returned `PUBLIC`, `isPrivate: false`, `isFork: true`, 2026-11-07; R03 section 3.3). Issue titles, bodies and comments are therefore written by the public, and the claim reads them live (`src/superclaude/skills/sc-issue-protocol/refs/claim.md:26`, R03 section 3.2). An automated trigger starts that read without a person present.
  - No label, Project field or code today expresses "human-approved" or "ready" (the fork has only the 9 default labels, R02 section 2; `refs/labels.md:7-13`, R01 section 4), so the trigger and approval criteria have to be defined and set up as part of the work.
- **Trigger:** Issue #331 itself, which instructs researching existing solutions first, and whose findings feed a `/sc:brainstorm` (then spec-panel, design, task list, execution) for the same issue (BUILD-REQUEST `WHY`). The issue text and the sibling issue `IronbellyOrg/Coder#477` describe a push design (watcher, then an API/MCP layer, then a Coder-side listener) (`research/research-notes.md`, ADDENDUM 2026-11-07T07:03Z, point 1 first sentence).

### 1.1 Owner decisions (binding; ADDENDUM 2, 2026-11-07T07:12Z)

The owner decided (relayed by the coordinator, message sent 2026-11-07T07:04:56Z). ADDENDUM 2 supersedes the earlier "keep A, B and C open" rule.

| Decision | Content | Effect on this research |
|---|---|---|
| Q1 | Option A, the workspace-side poller: each workspace polls GitHub every 5 minutes with its own `gh` login and starts the claim via `orca agent launch`; no listener, no inbound port, no address registry | The Recommendation is option A, decided by the owner; the implementation plan targets A. B, C and hybrids are still evaluated fairly as the documented alternatives and the revisit conditions. |
| Q2 | Claim-only: the watcher's job ends at starting `/sc:issue --claim <N>`; the pipeline after the claim stays manual (ADDENDUM 2026-11-07T07:03Z, point 3) | The scope matches what the code can do today (Section 2.1). |
| Q3 | Only a validated integer issue number reaches the session prompt, never issue title or body text (ADDENDUM 2026-11-07T07:03Z, point 3) | The prompt is exactly `/sc:issue --claim <positive integer>` (R01 section 13). |

Repo-side deliverable decided by the owner: a design doc, a tested poller script or CLI (mock `gh` and mock `orca agent launch`, nothing run live), and trigger/approval label setup instructions. B/C and any live deployment are recorded as follow-up.

### 1.2 Sibling issue IronbellyOrg/Coder#477 and the repo boundary

- **Issue:** `IronbellyOrg/Coder#477`, "[FEATURE] Workspace listener, monitor registration and secure prompt routing for every Coder workspace" (OPEN, read 2026-11-07 via `gh issue view 477 --repo IronbellyOrg/Coder`) (`research/research-notes.md`, ADDENDUM 2026-11-07T07:03Z, point 2).
- **What it asks for:** a listener running in every Coder workspace; each workspace and listener registered with the "monitor"; authorized monitor requests reach the intended workspace and are handed to its project's orchestrator to start a new session; the workspace address and port securely associated with the right GitHub account; authentication and authorization on senders, unauthorized requests rejected, no unauthenticated port exposed; protected transport and an audit trail of routing and access decisions. Interface, registration mechanism, credentials, network topology and audit implementation are "not known yet" in that issue.
- **Candidate integration points it names (Coder repo, not this repo):** `templates/VSCode-AIDev02/{main.tf,Dockerfile.coder,startup.tf,scripts/startup.sh,catalogue/orca/module.tf,catalogue/orca-pair.sh,orca/runtime.mjs}` and `.github/workflows/orca-upstream-monitor.yml` (a distinct upstream-version monitor). Prior art there: the closed Automatic Orca Pairing issue #195.
- **Repo boundary:** the listener, registration and transport live in the Coder repo (#477), not in IronClaude. The #331 deliverable in this repo is the watcher, selection and dispatch side, and the contract it needs from a listener if one ever exists.
- **Status under the owner decision:** `IronbellyOrg/Coder#477` was filed assuming a push design. Option A makes #477 unnecessary unless B or C is revisited. The spec must record this statement (ADDENDUM 2).

---

## 2. Current State Analysis

Section 2 describes verified current state only. Findings trace to source reads recorded in the research files; items that rest on documentation alone are tagged [UNVERIFIED — doc-only, no code confirmation] and are kept out of the diagram in 2.5.

### 2.1 Claim flow today

**Command and trigger**

| Fact | Evidence | Tag |
|---|---|---|
| `/sc:issue --claim <number\|url>` is explicit-only; a watcher-started session must be given the literal slash command as its first message | `src/superclaude/commands/issue.md:24`, `:37`, `:89-93` (R01 section 1) | [CODE-VERIFIED] |
| `--claim` accepts an issue number (`302`, `#302`) or an issue URL on the origin repo; there is no repository option, no dry-run and no preview option | `src/superclaude/commands/issue.md:37`, `:43` | [CODE-VERIFIED] |
| Both modes post to GitHub directly; nothing is shown for approval first | `src/superclaude/commands/issue.md:18`; matches `src/superclaude/skills/sc-issue-protocol/SKILL.md:74` | [CODE-VERIFIED] |
| Command-level STOP rules (exactly one of `--claim`/`--create`, no create-only flags with `--claim`, non-empty claim argument) are prose run by the model; none checks that the argument is an integer | `src/superclaude/commands/issue.md:45-51` | [CODE-VERIFIED] |
| Activation is mandatory: `Skill sc:issue-protocol` before any protocol step | `src/superclaude/commands/issue.md:89-93` | [CODE-VERIFIED] |

**Claim waves** (R01 section 3; `src/superclaude/skills/sc-issue-protocol/refs/claim.md` against `SKILL.md:82-88`)

| Wave | What happens | Writes or posts |
|---|---|---|
| 0 prerequisites | `origin_repo.py --claim "<argument>"` resolves `{"repo","number"}`; exit 1 `E-NO-ORIGIN`, 3 `E-FOREIGN-REPO`, 4 `E-NOT-AN-ISSUE` (`claim.md:13-15`); `gh auth status` else `E-GH-AUTH` (`claim.md:16`); default branch lookup (`claim.md:17`); create `.dev/issues/<N>/` (`claim.md:18`) | local directory only; "No GitHub or ClickUp write happens before Wave 3" (`claim.md:20`) |
| 1 lookup (`issue-worker-t3`, read-only) | `gh issue view <N> --repo <R> --json number,title,body,state,assignees,labels,comments,createdAt,url,author` and `gh api user -q .login` (`claim.md:26`); merged PRs since `createdAt`, limit 200 (`claim.md:27`); `git fetch origin` then `git log` (`claim.md:28`); earlier marked comment by this login (`claim.md:29`) | `.dev/issues/<N>/scout.md` (`claim.md:30`) |
| 2 edge cases | in order: pull request, STOP `E-NOT-AN-ISSUE` (`claim.md:39`); closed, STOP (`claim.md:40`); assigned to anyone other than the current login, STOP "not claimed" (`claim.md:41`); already assigned to the current login, continue, "re-claim is allowed and idempotent" (`claim.md:42`) | no GitHub or ClickUp write on any STOP (`claim.md:37`) |
| 3 assign | `gh issue edit <N> --repo <R> --add-assignee @me`; failure is `E-ASSIGN-FAILED` (`claim.md:47`); then `clickup_claim.py`, all outcomes non-fatal (`claim.md:48-50`) | GitHub assignee (first GitHub write); ClickUp assignee only when configured |
| 4 accuracy check and summary | `issue-worker-t2`, or `t1` when complex (`claim.md:54`); writes `accuracy-check.md`, `issue-summary.md`, optional `analysis/analyze-<scope>.md` (`claim.md:57-59`) | files only |
| 5 next steps | `Skill sc-recommend`, saved to `recommend.md`; `next-steps.md` written; "Do not run any of those commands (B2)" (`claim.md:78-80`) | files only |
| 6 post | accuracy-check comment and claim comment edited by marker id or posted (`claim.md:84-88`); `E-POST-FAILED` on failure (`claim.md:89`); "Print the `next-steps.md` path and STOP" (`claim.md:90`) | two marked GitHub comments |

**What the claim does not do** (all [CODE-VERIFIED] unless noted)

- **Stops by design after `next-steps.md`.** The command says it "then stops. It never runs the next-step commands" (`src/superclaude/commands/issue.md:15`), lists "Run any next-step command (brainstorm, design, workflow, implement, troubleshoot)" under Will Not (`issue.md:83`), and hands the steps to a person: "run its commands in your own session, in order" (`issue.md:71`). The same is stated at `SKILL.md:17`, `:88`, `:146`, `:150`, `refs/claim.md:80`, `:90` and `templates/next-steps.md:5` (R01 sections 1 and 11).
- **The issue text's expectation is CODE-CONTRADICTED.** The expectation that `/sc:issue --claim` orchestrates a pipeline is contradicted by `issue.md:15`, `:79`, `:83`, `claim.md:80` and `templates/next-steps.md:5`: the claim stops after writing `next-steps.md`. The owner's claim-only decision (Q2) matches the code.
- **`--claim --pipeline` is design only.** `issue.md` contains no occurrence of "pipeline" (Grep count 0; argument-hint `:8` and Options `:35-41` list none); the design says "current claim code does not implement this proposed pipeline interface" (`docs/designs/sc-issue-launch-level-hook.md:34`) and "Full enforcement is not runtime-approved" (`:17`); `launch-level-guard.sh`, listed as "proposed" at design `:40`, does not exist (R01 section 11; R03 section 1.2). Running the next steps would need B2 removed in `issue.md`, `SKILL.md` and `claim.md` plus the tests that pin it, the proposed `--pipeline` interface, and a launch-level guard (R01 section 11).
- **No label or Project handling.** `refs/labels.md:7` says "`--claim` changes no labels"; Wave 1 only records labels into `scout.md` (`claim.md:26`, `:30`). A Grep for `gh project|projectV2|graphql` over `src/superclaude/skills/sc-issue-protocol` returned no match, so the claim neither reads nor moves a Project item and an issue stays in Backlog after a claim (R01 section 3). The "tagged, approved, in a Project, Backlog" gating is not done by the claim.
- **No machine-readable result.** The return contract is chat text printed last (`SKILL.md:101-117`), not a file. The on-disk completion signals are `.dev/issues/<N>/next-steps.md` and the GitHub-side assignee and marked comments (R01 section 2). Output files of a claim: `scout.md`, `clickup.json`, `accuracy-check.md`, `issue-summary.md`, optional `analysis/analyze-<scope>.md`, `recommend.md`, `next-steps.md`, `claim-comment.md` (`issue.md:68`).
- **No user questions.** Claim mode never uses `AskUserQuestion` (`SKILL.md:74`; Grep finds it only at `SKILL.md:4` and `refs/create.md:59`); `/sc:recommend` questions go into `recommend.md` and the default row is used (`claim.md:79`; `SKILL.md:134`) (R01 section 11).
- **No tests found that pin the stop text.** `tests/commands/test_issue_command.py` has no hit for "never runs", "Will Not", "B2" or "stop after"; other test files were not read [UNVERIFIED] (R01 section 11, GQ #6).

**Argument validation in code** (`src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py`, 196 lines; R01 section 5)

| Input | Result | Evidence |
|---|---|---|
| `302`, `#302` | accepted as integer; `_NUMBER = ^#?(?P<n>[1-9][0-9]*)$`; no upper bound | `origin_repo.py:74`, `:102-110` |
| `https://github.com/<origin owner>/<origin repo>/issues/302` (trailing `/`, `#fragment`, `?query` ignored) | accepted | `origin_repo.py:25-27`, `:126`, `:143-146` |
| `owner/repo#N`, `0`, `007`, `-5`, `302 extra words`, any other text | `E-NOT-AN-ISSUE`, exit 4 | `origin_repo.py:120-124` |
| URL on another host, or GitHub URL naming another repo | `E-FOREIGN-REPO`, exit 3 | `origin_repo.py:114-119`, `:127-140` |
| `/pull/<N>` URL, another path on origin | `E-NOT-AN-ISSUE`, exit 4 | `origin_repo.py:147-153` |
| `origin` unreadable or not a GitHub URL | `E-NO-ORIGIN`, exit 1; `read_origin()` runs `git remote get-url origin` with no `cwd`, so it reads the repo of the current directory | `origin_repo.py:156-174` |

The check runs inside the session, in Wave 0, on the string the model passes in `--claim "<argument>"` (`claim.md:14`), so it is a second check and not a prompt-boundary validator (R01 section 5; R03 section 3.1). It does not check that the issue exists, is open, or is an issue rather than a PR for a bare number; that is Wave 2 (`claim.md:39`).

**Which login assigns, and the assignee rules**

- The claim assigns `--add-assignee @me` (`SKILL.md:72`, `:85`; `claim.md:47`). `gh issue edit --help` on the research machine states: `--add-assignee login  Add assigned users by their login. Use "@me" to assign yourself` [CODE-VERIFIED by running help] (R01 section 9). The login is whichever account `gh auth` holds in the session environment; Wave 1 also reads it with `gh api user -q .login` (`claim.md:26`).
- The claim's own pre-filter, taken from `claim.md:41-42`: an issue assigned to a login other than the current one stops the claim without a write; an issue assigned to the current login or to nobody does not stop it. R02 section 2c reconciles the three research files on this single predicate: a poller skips an issue assigned to another login; routing by assignee selects the own login; first-come selects only unassigned issues (R02 section 2c; R01 section 9).
- **No mutual exclusion.** The claim is check-then-act (lookup `claim.md:26`, edge check `:41-42`, then `--add-assignee @me` `:47`); `--add-assignee` adds a user and does not replace the list. Reading the code, two workspaces with different logins can both pass Wave 2 and both assign themselves [derived from code, not observed; GitHub's allowance of several assignees on one issue is not shown in this repo, UNVERIFIED]. Two workspaces with the same login both pass `claim.md:42` and both post new comments, because the marker lookup is in Wave 1 (`claim.md:29`) and the post in Wave 6 (`claim.md:84-88`) (R01 section 9).

**Idempotence and failure shapes** (R01 section 10)

- Marked comments end with `<!-- sc:issue:accuracy-check -->` (`templates/accuracy-check-comment.md:17`) and `<!-- sc:issue:claim -->` (`templates/claim-comment.md:23`); a re-run by the same login edits the latest earlier marked comment with `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<file>` instead of posting (`claim.md:29`, `:84-88`; `SKILL.md:135`, `:145`).
- Re-claim by the same login is allowed (`claim.md:42`); ClickUp is idempotent, `already_assigned` (`scripts/clickup_claim.py:230-231`). A full re-run is not idempotent in cost: workers, the merged-PR lookup and the ClickUp search (up to 20 pages, `clickup_claim.py:74`, `:184`) repeat. Whether an existing `<D>` directory is tolerated is not stated (`claim.md:18`) [UNVERIFIED].
- Failures before Wave 3 write nothing to GitHub (`claim.md:20`). After Wave 3 the issue is assigned even if Waves 4-6 fail, leaving the issue assigned with no claim comment; a re-run is the repair (`claim.md:42-43`; `SKILL.md:135`) (R01 sections 2 and 10).
- The claim comment is posted last (Wave 6), so it is a late record: the assignment precedes it by the duration of Waves 4-5 (R01 section 10).
- At-most-once across workspaces is not provided by the claim (R01 section 10; R03 section 7).

**Environment a claim needs** (R01 section 11)

| Need | Evidence |
|---|---|
| A checkout of `IronbellyOrg/IronClaude` whose `origin` is a GitHub URL, because the repo is read from the session's current directory | `origin_repo.py:156-174` |
| `uv` (`uv run --no-project python ...`) and `gh auth status` succeeding, with rights to read the issue, edit assignees and comment; `git fetch origin` access | `claim.md:14`, `:16`, `:28` |
| The skill and command installed, the three issue-worker agents, and the `sc-recommend` skill | `issue.md:93`; `SKILL.md:58-60`; `claim.md:78` |
| A session that serves the tier picker IDs `claude-gw-tier3`, `claude-gw-tier2`, `claude-gw-tier1a`; otherwise STOP `E-TIER-UNAVAILABLE` at Wave 1 with "no alias fallback", which writes nothing to GitHub, so a misconfigured workspace would fail every issue without assigning it | `SKILL.md:52-66`, `:130`; `refs/tiers.md:32-40`; `claim.md:20` |
| ClickUp variables only if ClickUp assignment is wanted; otherwise the claim comment states "skipped" and the claim continues. The ClickUp identity is the personal token in the environment, independent of the `gh` login; no code ties the two to one person [inference, UNVERIFIED as an enforced rule] | `clickup_claim.py:8-19`, `:10`; `SKILL.md:133`; `claim.md:47` |

**Never-as-worker and the Worker Contract** (R01 section 7; R03 section 5)

- `/sc:issue` is on the never-as-worker list: "Never-as-worker list: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers" (`src/superclaude/core/WORKER-CONTRACT.md:23`) [CODE-VERIFIED]. `issue.md` has no `## Unattended mode` section (it goes from Activation `:87-93` to Related Commands `:95-100`).
- A "worker run" is a session that received an Orca preamble carrying a Task ID and a Dispatch ID; a session the user started is an ordinary session (`WORKER-CONTRACT.md:11`). The brief guard (`:16-20`, case 3) refuses a never-as-worker command only inside a session with a live Orca preamble.
- WC-8 and WC-13: a command never calls `worker-start`, `dispatch` or `task-create` (`WORKER-CONTRACT.md:39`); a worker's session never calls `worker-start`, `dispatch`, `task-create`, `orca-cli worktree create --agent` or `agent launch` (`:61`). WC-9: under `--unattended` every outward default (push, PR, GitHub post) is off (`:40`), applies to worker runs only.
- Consequence: a poller that starts an ordinary top-level session with `orca agent launch --prompt` does not create a worker run, so the list does not stop it; the session gets no heartbeats, no `worker_done`, no `return-contract.yaml` and no coordinator visibility. Dispatching `/sc:issue` through `worker-start` would violate `:23` and be refused. That a poller-launched ordinary session is outside the list is an interpretation of `:11` and `:23`, not an owner statement [UNVERIFIED] (GQ #24). The poller must run as a plain process outside any Claude session; whether a Coder workspace offers cron, systemd or survival across autostop, and where durable state can live, is not shown by any repo file [UNVERIFIED] (R01 section 7 and Gaps 9, GQ #9).
- The coordinator rule that outward git/GitHub actions need the user's instruction in the live conversation (`WORKER-CONTRACT.md:112`) has no category for a standing authorization by an approver's label; this is a policy gap, not a code defect (R03 section 5).

**Key findings of 2.1**

- The claim is non-interactive and claim-only; the pipeline is design only and blocked (B-CTX), so claim-only is what the code can do today.
- Stops in Waves 0-2 write nothing; Wave 3 is the first write; the claim never gates on labels or Project status, so the watcher must do that gating itself.
- Nothing in the claim prevents two workspaces from both claiming an unassigned issue; at-most-once has to be built in the poller.

### 2.2 Ways to start a top-level session

**Local entry points** (R01 section 12)

| Entry point | Evidence | Requires | Notes for a poller |
|---|---|---|---|
| `orca agent launch --agent claude --worktree <selector> --prompt "<text>" --surface terminal [--json]` | `orca agent launch --help` run locally; `/opt/Orca/resources/app.asar.unpacked/out/cli/specs/agent-launch.js:9-33`; handler `.../handlers/agent-launch.js:11-35`; request `.../agent-launch-request.js:38-117`; repo rule `src/superclaude/core/CLAUDE.md` section "Orca session launches" (L45-53) and `src/superclaude/skills/ccsession-tag/README.md:228-237` | A running Orca runtime (`client.call`, handler L23-35); an existing Orca workspace (`createsWorktree: false`, handler L12-14) | The path the owner decision names |
| `ccsession-orca` as Orca's Claude command | `ccsession-tag/README.md:211-226`; `~/.local/bin/ccsession-orca` is a symlink to `~/.claude/skills/ccsession-tag/ccsession-orca` (249 lines) | Orca Settings > Agents > Claude > Command set to its absolute path, one executable with no arguments (README:216-223) | Optional for function, adds session names. On the research machine `agentCmdOverrides` is `{}` (not configured); the Coder value is [UNVERIFIED] |
| Plain `claude` (headless `claude --print`) | `src/superclaude/cli/pipeline/process.py:134-166` (`claude --print --verbose --dangerously-skip-permissions --no-session-persistence --tools default --max-turns N --output-format stream-json`, prompt on stdin per docstring L137-138); `max_turns` default 100 (L91) | `claude` on PATH | A one-shot run, no session to attach to, not resumable (`--no-session-persistence`, L152); `ccsession-tag/README.md:278` says print mode is untagged. Whether `/sc:issue` runs correctly under `--print` is [UNVERIFIED] (GQ #8) |
| `orca orchestration send` into a live coordinator | `orca orchestration send --help` run locally (`--to <run:id\|dispatch:id\|legacy_handle>`, `--subject`, `--body`, `--type`); `.dev/orca-command-refactor/inventory/orca-capabilities.md:66` | A coordinator Run or Dispatch to address | "Enqueue is durable but does not interrupt you, so nothing arrives unless you look": [CODE-VERIFIED] in Orca's guide text `/opt/Orca/resources/app.asar.unpacked/out/cli/bundled-skill-guides.js:3158` (also `:2413`, "best-effort attention only and does not prove the recipient read or accepted it") |
| `orca terminal send --terminal <handle> --text <text> --enter` | `orca terminal send --help` run locally: "Send input to a live terminal" | A runtime-issued terminal handle (needs a prior `terminal list`) | Types immediately into whatever is on that terminal, competing with a person or an unfinished prompt |

**Tradeoff: new top-level session per issue versus typing into a live coordinator session** (R01 section 12; analysis finding F4 at `.dev/issues/331/analysis/analyze-sc-issue-protocol.md:35`)

| Aspect | New session per issue (`orca agent launch`) | Typing into a live session (`orchestration send` or `terminal send`) |
|---|---|---|
| Delivery | Submitted prompt starts a new session (request.js:63-65) | `orchestration send` is durable but pull-only: the claim does not start until the session looks (`orca-capabilities.md:66`; `bundled-skill-guides.js:3158`). `terminal send` is immediate. |
| Competition with a person | None: its own tab and context window | `terminal send` collides with a person's input and puts the claim's output and context into a session the person is using; judgement from the help text ("live terminal") and the pull-only guide text, not from a run |
| Failure isolation | A failed claim affects only its own session | A failed claim sits inside the live session |
| Known to run `/sc:issue` | Not shown by any file [UNVERIFIED], see argument contract below | A message is not a prompt that the session is known to run as `/sc:issue` [UNVERIFIED] |
| Costs | One more tab and Claude process per issue; nothing in the claim closes the session after it stops (`SKILL.md:88`), so tabs accumulate [inference, not observed]; not a worker run, so no coordinator visibility | The WORKER-CONTRACT coordinator rules (`WORKER-CONTRACT.md:66`) describe a coordinator that plans and dispatches, not one that runs claims |
| Session naming | Auto-named from the prompt's first words; the name question is not asked when a prompt is carried (`ccsession-tag/README.md:272`; `ccsession-orca` lines 56-125 set `task_carried=1`) | not applicable |

The research evidence supports F4's conclusion for the new-session route: a new top-level session per issue is simpler and isolates failures, and typing into a live coordinator session is durable only in the pull-only sense (R01 section 12). F4's first half, that `/sc:issue` cannot be an Orca worker, is [CODE-VERIFIED] (`WORKER-CONTRACT.md:23`); the second half is a design judgement (R01 section 8).

**`orca agent launch` argument contract** (R01 section 12, for the poller's injectable launch function and its mock)

| Part of the contract | What the files show | Tag |
|---|---|---|
| Invocation | `orca agent launch --agent <id> [--worktree <selector>] [--prompt <text>] [--model <id>] [--effort <level>] [--surface chat\|terminal] [--focus] [--retry-launch <operationId>] [--json]` (`.../specs/agent-launch.js:9`; help output) | [CODE-VERIFIED] |
| Agent id | `--agent` is required; an unknown TUI agent is `invalid_argument` "Unknown TUI agent" (request.js:32-37); `claude` is known (`shared/tui-agent-config.js:15`) | [CODE-VERIFIED] |
| Which worktree or repo | `--worktree <selector>` (`identity:`, `id:<repo-id>::<path>`, `name:`, `branch:`, `issue:<n>`, `path:<abs>`, `active`, `current`). Omitted, `active` or `current` resolves from the caller's cwd (handler.js:18-22; `agent-workspace-selector.js:10-48`). A remote server requires `--worktree` (handler.js:15-17). There is no `--repo` flag: the checkout is chosen only by the worktree | [CODE-VERIFIED] |
| Needs an existing worktree | Yes: target `{kind: 'existing', worktree}` and `createsWorktree: false` (handler.js:12-14, :30-33); a new checkout needs `orca worktree create --agent` (spec note L24) | [CODE-VERIFIED] |
| Terminal versus chat | `--surface terminal` always runs the agent CLI; without it the host's Chat UI setting decides (spec note L22-23; request.js:2); a `--surface` other than chat or terminal is refused (request.js:21-30) | [CODE-VERIFIED] |
| How the initial prompt is passed | `--prompt <text>` becomes `{text, delivery: 'submit'}` (request.js:63-65): submitted, not left as a draft. An empty or whitespace-only prompt is dropped silently and the agent starts with no prompt (request.js:63). A valueless `--prompt` is rejected (request.js:51). A host without the prompt-carry capability is refused with `incompatible_runtime` (request.js:84-86) | [CODE-VERIFIED] |
| Mechanism by which Claude receives the prompt (argv versus paste) | `tui-agent-config.js:15-21` gives Claude `promptInjectionMode: 'argv'` and `draftPromptFlag: '--prefill'`; `orca-capabilities.md:47` says the task is passed on the command line for Claude on the `worker-start` path. Which path `agent launch` takes lives in the host runtime, not in the unpacked CLI directory | [UNVERIFIED] |
| Whether Claude Code runs a leading `/sc:issue` given this way as a slash command | Not shown by any file. `WORKER-CONTRACT.md:93` arranges that "the Task text never starts with `/sc:`" without stating why | [UNVERIFIED]; needs one owner-run live test in the live-plan phase |
| Agent command | Orca runs the configured Claude command, `ccsession-orca` only when set in Orca Settings (README:216-223); locally `agentCmdOverrides` is `{}` | [CODE-VERIFIED] locally; Coder [UNVERIFIED] |
| Name question | Not asked when a prompt is carried (README:272; `ccsession-orca` lines 56-125) | [CODE-VERIFIED] |
| Success output | text lines `agent: terminal` or `agent: chat session`, `handle`, `sessionId` (chat only), `worktreeId`, `operationId`, `why`, `prompt: <outcome>`, `warning` (request.js:105-117); with `--json` the result object `{outcome{kind,handle,sessionId?}, receipt{detail}, worktreeId, operationId, prompt{outcome}, warning}` via `printResult` (handler.js:34) | [CODE-VERIFIED] for fields; exact JSON key nesting printed by `printResult` not read: [UNVERIFIED] |
| Exit status | Error: `reportCliError(...)` then `process.exitCode = 1` (`cli/index.js:128-137`); success leaves the default 0 | [CODE-VERIFIED] by reading; not executed |
| Lost reply | `--retry-launch <operationId>` replays the same launch; "Never retry as a fresh launch" (spec note L27). On an unconfirmed outcome the CLI throws `agent_session_operation_unknown` with `launchOutcome: 'unknown'`, `retrySafe`, `operationId`, `recoveryCommand`, `nextSteps` and the message "the agent may already be running and the prompt may already be submitted" (`agent-launch-recovery.js:54-64`) | [CODE-VERIFIED] |
| Other refusals | `incompatible_runtime` when the host cannot start agents or lacks surface or focus capability (handler.js:24-29; request.js:87-92); `Setup decision required for this repository` passes through (recovery.js:21-24) | [CODE-VERIFIED] |
| JSON error body of `reportCliError` | not read | [UNVERIFIED] |

(All `handler.js`, `request.js`, `recovery.js` and `specs/` paths are under `/opt/Orca/resources/app.asar.unpacked/out/cli/`, as given in R01 section 12.)

**What the mock of `orca agent launch` must do** (derived by R01 section 12 from the sources above; the real JSON error body is [UNVERIFIED]): accept exactly that argv as a list and never a shell string; record `--agent`, `--worktree`, `--surface` and `--prompt`; succeed with exit 0 and JSON; fail with exit 1; simulate the unknown-outcome error that carries an `operationId`; let a test assert that the recorded prompt equals `/sc:issue --claim <int>` and nothing else; and simulate "the cwd is not inside an Orca workspace" (selector resolution failure), because a poller started outside an Orca workspace has no `--worktree` default.

**Prompt contract for the integer-only rule** (R01 section 13)

- The launch side accepts any text in `--prompt` (request.js:50, :63-65); `ccsession-orca` takes a positional argument as the task and starts a session without a question (lines 56-125; README:272); the command accepts `--claim <number>` with nothing else (`issue.md:29`, `:37`). On the files read, the single line `/sc:issue --claim <N>` is a valid initial prompt; live behaviour of a leading slash command given as an initial prompt is [UNVERIFIED].
- The poller must build the prompt as `"/sc:issue --claim " + str(int(number))`, with `number` taken from the `number` field of `gh ... --json number` output, reject anything that is not a positive integer, and pass the prompt as one element of an argument list (no shell). A prompt starting with `/` is not read as an option by `ccsession-orca`: its loop treats `-*` as options at `ccsession-orca:110`, and only a first positional word equal to `mcp`, `config`, `doctor`, `update` and similar is a subcommand (line 116); any other positional becomes the task (line 119). [CODE-VERIFIED by reading `/home/coder/.claude/skills/ccsession-tag/ccsession-orca`] (R01 section 13).
- `ccsession-orca` scans arguments and treats the first non-flag word, `--prefill <text>` or a word after `--` as the task text (`ccsession-orca:66-122`); whether `--prompt` reaches Claude as an auto-submitted positional prompt or as a `--prefill` that waits for Enter is [UNVERIFIED], and a prefilled prompt would not run unattended (R03 section 3.1 and Gaps 4).
- Integer-only protects the launch prompt, not the claim's own reads: see 2.4.

**Launch-session environment facts** (R01 section 11; R03 section 2.2)

- Permission mode of a launched session is decided by three inputs together: ccsession's `CCSESSION_PERMISSIONS` or `CC_CLAUDE_FLAGS`, the flags Orca passes from `agentDefaultArgs`, and whether Orca runs `ccsession-orca` at all. `src/superclaude/skills/ccsession-tag/ccsession:136-141` adds `--dangerously-skip-permissions --allowedTools=Grep` unless `CCSESSION_PERMISSIONS=default`; but flags the caller passes, "such as Orca's default `--dangerously-skip-permissions` option", still apply (`ccsession-tag/README.md:534`). On the research machine Orca's `agentDefaultArgs.claude` is `--dangerously-skip-permissions` (`/home/coder/.config/orca/profiles/local-default/orca-data.json`) and Orca falls back to it for `claude` (`/opt/Orca/resources/app.asar.unpacked/out/shared/agent-launch-profile.js:12-14`, `.../shared/tui-agent-permissions.js:16`). Whether the `orca agent launch` CLI route applies `agentDefaultArgs`, and the values on a Coder host, are [UNVERIFIED].
- Orca hazard: `orca worktree current --json` showed the upstream project id on 2026-11-02 (project `CLAUDE.md`), so `--issue` and `--pr` link flags must not be passed; `--worktree issue:<number>` may trigger the same linking, untested, so `path:` or `name:` is the safe selector [UNVERIFIED whether `issue:<n>` links] (R03 section 5, GQ #16).

**Key findings of 2.2**

- `orca agent launch` is installed and documented locally, submits the prompt, needs an existing worktree and a running Orca, signals failure with exit 1 and a recoverable unknown-outcome error. The delivery mechanism and whether a leading slash command is executed need one live check that this research did not run.
- The launch reply can be lost after the session started, so the poller's dispatch record must exist before the launch and a lost reply must be treated as "dispatched", never relaunched fresh (R01 section 12).
- The poller needs a way to know its worktree (`--worktree path:<abs>`) because there is no repo option.

### 2.3 GitHub surface and house CLI/test/doc patterns

**Workflows** (R02 section 1)

| File | Trigger lines | Detail |
|---|---|---|
| `.github/workflows/test.yml` | 3-8 | `push` branches `[master, integration]` (l.4-5); `pull_request` same branches (l.6-7); `workflow_dispatch` (l.8) |
| `.github/workflows/boundary-guard.yml` | 25-33 | `pull_request` with a `paths:` filter on 5 swarm merge files; advisory-only job (header l.19-20) |
| `.github/workflows/contract3-generator-constraint-lint.yml` | 22-29 | `pull_request`, `types: [opened, edited, synchronize, reopened]`, `paths:` for `**/gates.py`, `**/structural_checkers.py`, `**/*_validator.py` |

- [CODE-VERIFIED] No `schedule:`, `cron:`, `issues:`, `workflow_run:` or `pull_request_target:` appears in any workflow file (grep over `.github/workflows/*.yml`, zero hits); `workflow_dispatch` exists only at `test.yml:8`. `.github/workflows/` holds exactly `README.md`, `boundary-guard.yml`, `contract3-generator-constraint-lint.yml`, `test.yml`.
- Job skeleton to copy for any new workflow: `runs-on: ubuntu-latest`; `actions/checkout@v4` (`test.yml:17`); `astral-sh/setup-uv@v10.3.2` with `python-version: "3.10"` (`test.yml:20-23`); `uv pip install -e ".[dev]"` (`test.yml:29`, `:72`, `:98`); `make sync-dev` (`test.yml:38`). Least-privilege precedent: `permissions: contents: read` (`test.yml:151-152`) and `persist-credentials: false` (`test.yml:156-158`).
- `test-summary` (`test.yml:191-200`) has `needs: [test, swarm-marker-matrix, lint, doctor-check]` (l.194); a new job in `test.yml` must be added there to be covered by the aggregate gate. `.github/workflows/README.md` documents three workflows and its "Adding a New Workflow" (l.120-125) asks for documentation there.
- Under option A no GitHub workflow is required; none of the three existing workflows has a schedule or issue trigger to extend (R02 section 1).

**Issue forms and labels** (R02 section 2)

| File | Name / title prefix | `type:` | `labels:` |
|---|---|---|---|
| `.github/ISSUE_TEMPLATE/bug_report.yml` | "Bug report", `[Bug]: ` (l.1-3) | `Bug` (l.4) | `bug` (l.5-6) |
| `.github/ISSUE_TEMPLATE/feature_request.yml` | "Feature request", `[Feature]: ` (l.1-3) | `Feature` (l.4) | `enhancement` (l.5-6) |
| `.github/ISSUE_TEMPLATE/other.yml` | "Other", `[Other]: ` (l.1-3) | none | none |
| `.github/ISSUE_TEMPLATE/config.yml` | `blank_issues_enabled: false` (l.1) | - | - |

- No form carries a field or label for approval or readiness; the forms look inherited from Orca (placeholder text, `orca_version` at `bug_report.yml:29,41-43`) (R02 section 2). An issue created through `other.yml` has no label, so a label-based poller must not assume `bug` or `enhancement` is present.
- Live label list of the fork (`gh label list --repo IronbellyOrg/IronClaude`, 2026-11-07, read-only): exactly the 9 GitHub defaults `bug`, `documentation`, `duplicate`, `enhancement`, `good first issue`, `help wanted`, `invalid`, `question`, `wontfix`. No approval or readiness label exists. The fork also has none of the `type: *` or `complexity: *` labels that `/sc:issue --create` expects, so `--create` reports them as `not applied: label missing in repo` (`refs/labels.md:20`) (R02 section 2b).
- `/sc:issue` applies only the fixed label set at `refs/labels.md:9-13` (mode, type, complexity), never creates a label and `--claim` changes none (`labels.md:7`); `labels.md:22-42` gives one-time maintainer `gh label create "<name>" --repo <owner/repo>` lines, the house format for label setup instructions (R01 section 4; R02 section 2b).
- Whether `gh issue list --json` exposes a native issue-type field [UNVERIFIED]; the Project v2 Status field needs `gh project`/GraphQL access and a token scope that is [UNVERIFIED] in R02 and observed missing in R03 (Section 2.4).

**Where `gh` is actually invoked** (R02 section 3)

- **[CODE-CONTRADICTED]** The earlier claim that `src/superclaude/pr_submit/ci.py` is a mockable `gh` subprocess wrapper: `ci.py` imports only `re`, `.classifier`, `.models` (`ci.py:10-15`), its docstring says it is pure and consumes an already-fetched payload (`ci.py:1-8`), and it never builds or runs a `gh` command. The same wrong claim in `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/codebase-context.md` has been corrected there (line 21, "CORRECTION (2026-11-07, research alignment check)") and in `research/research-notes.md` (EXISTING_FILES row for `ci.py`, line 30, and the GitHub-access pattern, line 37).
- **[CODE-VERIFIED] No Python `gh` wrapper exists.** No module of `src/superclaude/pr_submit/` imports or calls `subprocess` (grep returned no match); a search over all of `src/superclaude` found no Python module that builds or runs a `gh` call; the only `.py` hit for a literal `gh` is a docstring at `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:14`; `shutil.which("gh")` appears nowhere in `src` or `tests`. No Python code under `src/superclaude` calls `orca` either (`cli/doctor.py:61-77` checks the `ccsession-orca` file on disk only). A poller therefore needs its own small injectable subprocess runner for `gh` and for `orca`.
- The only "gh seam" in the package is `detection._fetch_payload(pr_num)` (`src/superclaude/pr_submit/detection.py:273-275`), a stub returning `{"reviews": [], "comments": []}`; its comment (l.267-270) says "The real fetch lives in the bash poller." Tests patch it with `monkeypatch.setattr(detection, "_fetch_payload", recorder.fetch)` (`tests/pr_submit/conftest.py:58`; `tests/pr_submit/test_rate_limit.py:63`). **[STALE DOC]** `tests/pr_submit/conftest.py:3-4` describes `mock_gh` as a monkeypatch of a gh-wrapper seam that records argv to assert the `--repo` pin; the code (l.38-59) patches a payload-fetch function and records `pr_num` values, with no `--repo` pin.
- Real `gh` I/O lives in bash scripts and agent-run protocol prose: `src/superclaude/skills/sc-pr-submit-protocol/scripts/{poll-augment-review.sh,poll-ci-checks.sh,retrigger-review.sh,reply-resolve-thread.sh}` ("All gh I/O is isolated here (NFR-6)", `retrigger-review.sh:16`, `reply-resolve-thread.sh:15`) and `sc-issue-protocol` (`SKILL.md:71`, `refs/claim.md:9`, `refs/create.md:9`).
- Convention A (skills): every `gh` call on issues, PRs or labels passes `--repo <R>`, and every `gh api` path is `user` or spells `repos/<R>/...` (`SKILL.md:71`, `claim.md:9`, `create.md:9`), matching the repo-level CLAUDE.md rule. Convention B (pr-submit scripts, `poll-augment-review.sh:22`, `poll-ci-checks.sh:44`, `retrigger-review.sh:50`, `reply-resolve-thread.sh:57`) falls back to `gh repo view --json nameWithOwner` when `--repo` is absent, which can resolve through gh's default selection; a watcher must always pass an explicit `--repo IronbellyOrg/IronClaude` and never use that fallback. That the fallback resolves to the upstream in practice is [UNVERIFIED]; only the risk is documented.
- Nearest Python subprocess pattern: `origin_repo.py` (standard library only; `tests/skills/test_issue_repo_resolution.py:281` `test_script_imports_only_standard_library`): `read_origin()` (l.156-174) runs `subprocess.run(["git","remote","get-url","origin"], capture_output=True, text=True, check=False)`, catches `OSError` and non-zero returns and maps them to `ClaimError(code, exit_code, message)` (l.77-83); `main(argv)` (l.177-191) returns an int exit code and prints a JSON line. Its subprocess call is hard-wired and not injectable, and its tests run real `git`. Other patterns: `src/superclaude/cli/swarm/tmux.py` (242 lines; `has_session` l.126, `launch_detached` l.140, `list_swarm_sessions` l.221-230; error classes l.87, l.91; `is_tmux_available()` l.95); `cli/sprint/notify.py:21,25` (`subprocess.run(cmd, timeout=5, check=False)`); injectable callables as parameters have precedent (`cli/reflect/fallback.py:39`, `cli/audit/tool_orchestrator.py:105`, `cli/audit/batch_retry.py:87`).
- Read-only minimum for a pure poller: `gh issue list`/`gh issue view`/`gh api repos/IronbellyOrg/IronClaude/...`; for a list the safest minimum fields are `number,labels,assignees,state`, and title and body should not be requested, to honor the integer-only prompt rule (R02 section 3.3).

**How tests build or stub `gh`** (R02 section 3.4; all under `tests/pr_submit/`)

| File:line | What it does |
|---|---|
| `test_conflict_e2e.py:118-129,132-146,166-169` | `_GH_STUB` bash text records `"$*"` to a calls file, serves `pr view` from a JSON file, fails with `unexpected gh call` otherwise; `install_gh_stub(repos)` writes it to `repos.bin_dir / "gh"` and `chmod(0o755)`; `_run` (l.101-106) uses `subprocess.run(argv, cwd=cwd, env=env, text=True, capture_output=True, timeout=timeout)` |
| `test_conflict_scripts.py:161-200` (and `:1697`) | `make_repos(tmp_path, ...)` creates `bin_dir`, writes a recording `gh` stub (l.171-177), and prepends it to `PATH` (l.179); `Repos.gh_call_lines()` (l.155-158) reads the call log |
| `test_codex_reviews.py:554-581` | fixture `fake_gh(tmp_path)` writes `FAKE_GH`, runs a skill script via `subprocess.run` with `PATH` prefixed, returns `(result, calls)` from `calls.jsonl` |
| `test_static_grep.py:341-378`, `:399`, `:442` | writes a `gh` bash stub switching on `$1`/`$2`, `PATH` prefixed (l.363), runs `[POLL_SCRIPT, "--pr","188","--repo","IronbellyOrg/IronClaude"]`; l.555-574 stub both `git` and `gh` |
| `test_cosmos_poll.py:100-190` | fixture `adapter(tmp_path)` writes a configurable `gh` stub that logs argv to `calls.jsonl`, rejects calls lacking `--repo acme/widgets` (exit 91), PATH prefixed at l.185 |

- [CODE-VERIFIED] The PATH-stub pattern is the repo's actual way of mocking `gh`: a bash executable named `gh` in a temp directory, that directory prepended to `PATH` in the child env, the code run as a real subprocess, the stub recording argv to a log the test reads back; stubs fail loudly on unexpected calls. `assert_no_retrigger_call` (`test_conflict_e2e.py:178-186`) rejects write-shaped tokens. `tests/pr_submit/test_conflict_sync_protocol.py:40` pins `ALLOWED_PROGRAMS = frozenset({"git","gh","uv","make","jq"})`; `test_static_grep.py:30,106,167,225` assert every `gh` command line is repo-scoped by a whole-token `--repo`.
- The in-process Python seam (`detection._fetch_payload`) patches a payload function, not a `gh` call; the repo has no existing Python-level injectable-runner test for `gh`; `mock_gh` is used in 3 test files only (R02 section 3.1). `tests/pr_submit/conftest.py:3-8` states the in-process monkeypatch is "preferred over a PATH-shim for unit speed", yet the PATH-shim is what the five gh-calling test files use.

**CLI registration and package layout** (R02 section 4)

- Console script `superclaude = "superclaude.cli.main:main"` (`pyproject.toml:70-71`). Deferred registrations follow `main.py:519-561` in the shape `from superclaude.cli.<pkg> import <group>  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports` then `main.add_command(<group>, name="<verb>")` (example `main.py:519-521`); 11 registrations in file order: `sprint` (519-521), `roadmap` (523-525), `cleanup-audit` (527-529), `tasklist` (531-533), `cli_portify_group` with no `name=` (535-537), `prd` (539-541), `eval` (543-545), `swarm` (547-549), `recommend` (551-553), `init-lite` (single `click.command`, 555-557), `reflect` (559-561). Ruff selects `["E","F","I","N","W","TID"]` (`pyproject.toml:183-184`).
- Model packages: `src/superclaude/cli/recommend/` (12 files, 1,784 lines; lazy export in `__init__.py:12-20`; `@click.group("recommend")` at `commands.py:34-35`; nested groups l.51, 145, 196) and the single-file `src/superclaude/cli/init_lite.py` (359 lines; `@click.command("init-lite")` l.285; registered `main.py:555-557`). `cli/cleanup_audit/commands.py:24-90` shows option style and a `--dry-run` that returns before any side effect (l.85-87). `pyproject.toml:78-79` packages `src/superclaude`, so a new `src/superclaude/cli/<pkg>/` ships without `pyproject.toml` changes; runtime deps already include `click`, `rich`, `pyyaml`, `httpx` (`pyproject.toml:34-43`).
- Registration tests: `tests/cli/test_cli_registration.py:31-49` freezes `EXPECTED_TOP_LEVEL_COMMANDS`; its check at l.95-106 only runs `<name> --help`, so adding a group does not break it. **[CODE-CONTRADICTED]** its comment at l.28-30 ("intentionally a frozen snapshot — adding or removing a top-level command should force a deliberate test update"): `swarm` and `reflect` are registered (`main.py:547-549, 559-561`) but absent from the set, and nothing forces an update. Per-group registration tests are the convention (`tests/recommend/test_cli_registration.py`; `tests/swarm/test_cli_registration.py:74`).

**Tests, gates and the `.claude/` mirror** (R02 sections 5 and 6)

- Layout: package-named directories (`tests/recommend/`, `tests/swarm/`, `tests/tasklist/`, `tests/pr_submit/`) and `tests/cli/` (`test_init_lite.py`, nested `prd/`, `eval/`, `reflect/`). `pyproject.toml:107-116` sets `testpaths = ["tests"]`, addopts `-v --strict-markers --tb=short`; only declared markers are allowed. `tests/conftest.py` has a session-scoped autouse `_pollution_snapshot` guarding `docs/mistakes` and `docs/memory/solutions_learned.jsonl`. `tests/pr_submit/test_ci_classify.py` (331 lines) is the pure-function JSON-fixture model.
- Gates: `make test` (`Makefile:13-16`; CI `test.yml:46-47`), `make lint` (`:48-50`; CI `test.yml:100-102` `ruff check src/ tests/`), `make format` (`:53-55`; CI `test.yml:104-106` `ruff format --check`), `make sync-dev` (`:109`), `make verify-sync` (`:166`), `make lint-architecture` (`:362`; CI `test.yml:133-135`), `make verify-deps` (`:356-359`; CI `test.yml:116-123`). Python must be 3.10-compatible (`pyproject.toml:16`; CI `test.yml:21-22`); ruff `line-length = 88`, `exclude = ["docs/"]`, `extend-exclude = [".dev/", ...]` (`pyproject.toml:173-181`).
- `.claude/` mirror: `.gitignore:127-128` ignores `.claude/*` except `.claude/settings.json`. A pure Python CLI package under `src/superclaude/cli/` is not mirrored (sync-dev copies only skills, agents, commands, hooks, templates). A command, skill, agent or template would need `make sync-dev` and `make verify-sync`, the `sc-<name>-protocol` pairing (`lint-architecture` Checks 1/2), and would trip `tests/recommend/test_routing_refresh.py` and `tests/core/test_how_we_work_routing_table.py` (as recorded at `docs/designs/sc-issue-command.md:378-380`).

**House design-doc format** (R02 section 7)

- `docs/designs/` holds `prd-spec-flag.md`, `sc-issue-command.md` (477 lines) and `sc-issue-launch-level-hook.md`; they use three different headers. `sc-issue-command.md` is the best model for a command or CLI design: a bold-label header block (`**Status:**` l.3, `**Issue:**` l.4, `**Branch:**` l.5, `**Source of truth:**` l.6, `**Produced by:**` l.7) then numbered sections 1 to 20 (Purpose and scope; Binding decisions `B1..B15`; Corrections to the issue text; Command interface; Component architecture; ... Files to create or change; Tests; Sync and routing; Defaults `D1..D27`; Flags cited; Acceptance criteria). `sc-issue-launch-level-hook.md` uses YAML front matter and has sections for Open decisions, Residual risks and UNVERIFIED items (section 16), a better fit for open items. The design's own header names the path "design -> workflow -> implement" (`sc-issue-command.md:3`).

**Key findings of 2.3**

- No scheduled or issue-event workflow exists; option A needs none; option B would be the first (R02 section 1).
- No Python `gh` wrapper exists; `ci.py` is a pure classifier; the poller needs its own injectable runner; `origin_repo.py` is the nearest pattern; PATH-stub executables are the repo's `gh` mocking technique.
- Existing labels cannot express "human-approved" or "ready"; new labels or a Project field must be created and documented; `/sc:issue` will not create them.
- A new CLI group is one lazy-import block after `main.py:561` plus a package; no `pyproject.toml` change and no `.claude/` mirror.

### 2.4 Governance and security surface

**Launch-level hook design versus code** (R03 section 1)

| Doc claim (`docs/designs/sc-issue-launch-level-hook.md`) | Tag | Evidence |
|---|---|---|
| Status of the design: "design draft; scoped job identity foundation implemented; full enforcement pending" (`:6`); "Full enforcement is not runtime-approved" (`:17`); `planning_status` "conditional: B-CTX feasibility gate must precede enforcement implementation" (`:9-10`) | self-description | design front matter and banner |
| `launch-level-guard.sh` enforces the level (`:23`) | **[CODE-CONTRADICTED]** (the doc marks it "proposed" at `:40`) | Glob `**/launch-level-guard*` over the worktree returned no files; only `src/superclaude/hooks/scripts/launch-job-identity.sh` exists |
| `hooks.json` gets two `launch-level-guard.sh` entries (`:339-345`) | **[CODE-CONTRADICTED]** | `src/superclaude/hooks/hooks.json` has no such entry; the only launch entry is `PreToolUse` matcher `Bash` to `~/.claude/hooks/launch-job-identity.sh`, timeout 5 (`hooks.json:96-105`) |
| `/sc:issue --claim --pipeline <level>` exists (`:23`) | **[CODE-CONTRADICTED]** (the doc says at `:34` the current claim code does not implement it) | `issue.md:35-41` Options table has no `--pipeline`; Grep of `src/` for `--pipeline\|sc-launch\|launch-level` matched nothing under `skills/sc-issue-protocol/` |
| `[sc-launch:v1:<nonce>]` marker prompt and `pending/<nonce>` store (`:52`, `:71`, `:77`, `:349-350`) | [UNVERIFIED — doc-only, no code confirmation] | no producer or consumer in code; `launch-job-identity.sh` never reads a marker (takes `session_id` from the hook envelope, `:429-431`) |
| `UserPromptSubmit` binding and `.ok` approval file (`:57-58`, `:186-194`) | [UNVERIFIED — doc-only, no code confirmation] | `hooks.json:44-62` UserPromptSubmit has only `freshness-user-prompt.sh` and `ccsession-tag/hooks/session-name.sh` |
| L2 shared `hooks/pre-push` (`:41`, section 19) | [UNVERIFIED — doc-only, no code confirmation] | no pre-push script among the 14 files under `src/superclaude/hooks/scripts/` |
| Bash job identity foundation implemented (section 19.7, `:547-565`) | **[CODE-VERIFIED]** | `src/superclaude/hooks/scripts/launch-job-identity.sh` (566 lines): `hook()` 414-489, `execute()` 492-522, `run()` 362-398, `supervise()` 291-359, `identify()` 215-247, `governed()` 177-186; registered at `hooks.json:96-105`; "same-user job identity, not a sandbox" at script line 2; adapter returns `updatedInput` without `permissionDecision` (`:479-482`); ordinary or unbound sessions untouched (fast exit when `$HOME/.claude/state/launch-level` is absent, lines 20-24; non-Bash tool 427-428; invalid session id 430-431; missing `sessions/<sid>` 435-437) |

- Levels W, WA, F, FS (design `:25-30`); no level authorizes a merge or a push to master/main (`:32`). Threat model TH1 honest drift and TH2 specified one-step workarounds; TH3 deliberate evasion is out of scope; "Same-user guardrail, not a sandbox" (`:32`); R12 "hostile agent: out of scope" (`:450`).
- **B-CTX gate** (design section 19.1, `:491-506`): git's pre-push hook receives no Claude session id (`:493`), so a structural pre-push layer cannot tell an agent's push from the human's in the same worktree; completion evidence is a log-only probe (`:504`); "B-CTX remains OPEN/BLOCKING" (`:506`); order-of-work step 0 (`:359`). B-CTX gates only the pipeline levels W/WA/F/FS; a claim without `--pipeline` is unaffected (design `:349`, `:355`), so a claim-only watcher is not blocked by B-CTX.
- Nothing in the repo creates the `~/.claude/state/launch-level/sessions/<sid>` record the identity adapter needs, so today no launch level constrains any session started by any trigger (R03 section 1, Key Takeaways).
- Plugin mirror: `plugins/superclaude/hooks/scripts/launch-job-identity.sh` is byte-identical to the `src` copy [CODE-VERIFIED by `cmp`]; `tests/hooks/test_launch_job_identity.py` exists (contents not read); installer coverage in `tests/cli/test_install_hooks.py` is [UNVERIFIED] (R03 section 7 addendum).

**Hooks and permission settings registered today** (R03 section 2)

| Surface | File:lines | Registers |
|---|---|---|
| Project settings (checked in) | `.claude/settings.json:1-28` | PreToolUse `Write\|Edit` to `reject-workspace-writes.sh` (l.4-14); PreToolUse `Skill` to `sc-recommend-phase0.sh` (l.15-25). No `permissions` key, no allow/deny list, no `defaultMode` |
| Packaged hook set | `src/superclaude/hooks/hooks.json:1-163` | SessionStart (3-43); UserPromptSubmit (44-63); PreToolUse `Edit\|Write` freshness-pre-edit (76-85), `Bash` block-bare-python (86-95), `Bash` launch-job-identity (96-105); PostToolUse (107-129); SubagentStart/Stop (130-161). No `permissions` key |
| Installer list | `src/superclaude/cli/install_hooks.py:42-88` | `launch-job-identity.sh` in `_FRESHNESS_SCRIPTS` (line 87); merge into `settings.json` is additive (module doc lines 5-12, merge code from line 267) |
| Global settings on the research workspace | `/home/coder/.claude/settings.json` (read 2026-11-07) | No `permissions` key; `skipDangerousModePermissionPrompt: true`; PreToolUse entries only `Edit\|Write` freshness-pre-edit, `Bash` block-bare-python and one Orca `*` hook |

- **[CODE-CONTRADICTED] by the installed state (observed on one workspace):** `hooks.json:96-105` and `install_hooks.py:87` say the identity adapter ships and registers on install, but `/home/coder/.claude/hooks/launch-job-identity.sh` does not exist, the script is not registered in `/home/coder/.claude/settings.json`, and `/home/coder/.claude/state/launch-level` does not exist. The cause is not established (the install not being re-run after PR #414 is the likely reading, UNVERIFIED); a watcher host may differ (R03 section 2.1, GQ #21).

| Control | What it does (evidence) | Constrains an unattended watcher session? |
|---|---|---|
| `block-bare-python.sh` | blocks a Bash command whose command word is `python`, `python3`, `pip`, `pip3` (`src/superclaude/hooks/scripts/block-bare-python.sh:2-14`, block at 338-344); fails open without `jq`/`awk` (67-74); documented ceilings at 48-61 | A UV-style gate, not a security control |
| `freshness-pre-edit.sh` | forces Read-before-Edit for Edit/Write (observed live; script body not read) | Not a security control |
| `reject-workspace-writes.sh` | blocks Edit/Write to `.claude/skills/<x>-workspace/**` and repo-root `prd-<slug>/` (`src/superclaude/hooks/scripts/reject-workspace-writes.sh:28-37`, `:51-62`) | Irrelevant to GitHub or secret access |
| `sc-recommend-phase0.sh` | fail-open reminder injection when `sc-recommend` is invoked (`.claude/settings.json:17`, `install_hooks.py:69-78`); body not read | Does not block |
| `launch-job-identity.sh` | dormant: acts only when a governed `sessions/<sid>` record exists; never denies on policy | No |
| `launch-level-guard.sh`, L2 pre-push | do not exist | No |
| ccsession launch flags | `ccsession:119-141` and `README.md:534-535`: `--dangerously-skip-permissions --allowedTools=Grep` unless `CCSESSION_PERMISSIONS=default`; flags the caller passes still apply; a non-empty `CC_CLAUDE_FLAGS` replaces the wrapper's flags | Permission mode is decided by ccsession variables, Orca default args and whether Orca runs `ccsession-orca` (see 2.2); per-host values [UNVERIFIED] |

- No permission allow/deny list exists at any level read. In default permission mode an unattended Claude would stop at the first tool-permission prompt; the shipped ccsession path avoids that by bypassing permissions, and `CCSESSION_PERMISSIONS=default` alone does not produce the stalled case because Orca's default `--dangerously-skip-permissions` still applies (`ccsession-tag/README.md:534`). A stalled case needs ccsession's bypass and Orca's default arguments both absent, which no file shows on any host [UNVERIFIED per host]. The repo has no middle option such as an allow list for `/sc:issue --claim` (R03 section 2.3).
- No hook restricts `gh`, `git`, file reads or network use. The fork's `master` is unprotected: `gh api repos/IronbellyOrg/IronClaude/branches/master/protection` returned HTTP 404 "Branch not protected", `rulesets` is `[]`, `rules/branches/master` is `[]` (read 2026-11-07, token is repo admin) (R03 section 2.3).
- The `gh` OAuth token lives in `/home/coder/.config/gh/hosts.yml` (mode 600, owner `coder`; value not read); active scopes are `gist, read:org, repo, workflow` (`gh auth status`); any Bash or Read call in the session runs as the same user and can read it. `ccsession.env` can hold proxy URL and auth tokens (`ccsession:127`) (R03 section 2.3).

**Untrusted issue text: the paths into a claim session** (R03 section 3)

| Path | Evidence | Untrusted text involved |
|---|---|---|
| 1. The launch prompt | `/sc:issue --claim <N>`; digits are first checked in Wave 0 by `origin_repo.py:74`, `:102-153`, `:177-191`, which runs inside the session after the prompt reached it, so it is not a prompt-boundary validator; `_NUMBER` has no upper bound on digits | none if the poller builds the prompt from an integer (owner rule Q3) |
| 2. Wave 1 lookup (`issue-worker-t3`) | `refs/claim.md:24-31`; `gh issue view <N> --repo <R> --json number,title,body,state,assignees,labels,comments,createdAt,url,author` at `claim.md:26` and `src/superclaude/agents/issue-worker-t3.md:21` | title, body, all comments, author login |
| 3. Wave 4 accuracy check | `claim.md:54-60`: the worker "assumes the issue text is out of date and checks each concrete claim in the issue body and comments (paths, symbols, behaviours, flags) against today's code"; runs `/sc:analyze` on "the paths the issue touches" (`claim.md:58`) | body and comments choose which local paths are read and quoted into `accuracy-check.md` and `issue-summary.md` |
| 4. Wave 5 | `claim.md:78`; `refs/chains.md:28-37` | the summary (derived from issue text) becomes the goal sent to `/sc:recommend`; text lands in command lines in `next-steps.md` for a person; nothing executes them (`claim.md:80`) |
| 5. Wave 6 post | `claim.md:82-90`; `SKILL.md:72`, `:74` | the orchestrator posts worker-written files to the issue with `gh issue comment --body-file` and `gh api -X PATCH ... -F body=@file`, "directly (B1); the full body or comment is never shown for approval" |
| 6. Wave 3 ClickUp | `claim.md:48-50`; `clickup_claim.py:149-159` | uses number and URL, not title or body |

- Worker tool sets: `issue-worker-t3` has `tools: Read, Grep, Glob, Write, Bash` (`src/superclaude/agents/issue-worker-t3.md:5`); the agent registry lists the same set for `t2` and `t1` (their files were not read, GQ #18). The "read-only on GitHub", "write only under `.dev/issues/`" and "`git fetch origin` only" limits are prompt text (`issue-worker-t3.md:27-29`; `SKILL.md:64`, `:72`), not tool-level enforcement.
- The repository is PUBLIC (see Section 1), so anyone with a GitHub account can open issues and comment (role Read suffices). **[STALE DOC]** The project `CLAUDE.md` "PR Target = Fork" section calls `origin` the user's "private fork"; the live check on 2026-11-07 shows it public (R03 Stale Documentation).
- The approval label controls only whether the watcher fires. The claim reads the issue live at claim time, including comments added after approval and a body edited after approval, so approval does not freeze the text the claim reads. Whether a poller can detect a post-approval body edit is [UNVERIFIED] (the events listing read did not show body edits). The issue payload carries `author_association` (observed on #331: `MEMBER`); comment `author_association` was not checked [UNVERIFIED] (R03 section 3.3).
- Integer-only therefore protects the launch prompt, not the session. The research files raise the policy for the claim's own reads of title, body and comments as an open decision: accept as a documented risk, restrict to approved authors by `author_association`, lock the conversation on approval, or change the claim to read less (R03 Gaps 6, GQ #13).

**Who decides "human-approved" and "intended owner"** (R03 section 4)

- No approval or routing mechanism exists in code. The only "approved" concept in the repo is the typed `approved` prompt of the launch-level design (`docs/designs/sc-issue-launch-level-hook.md:186-195`), which is unimplemented [UNVERIFIED — doc-only, no code confirmation].

| Action | Minimum role | Source |
|---|---|---|
| Open an issue, comment | Read | GitHub repository-roles table (WebFetch of docs.github.com repository-roles page) |
| Apply or dismiss a label | Triage | same page; docs.github.com managing-labels |
| Create, edit, delete labels | Write | search result summarising the roles page; not separately fetched |
| Close, reopen and assign all issues | Triage | same page |
| Move a Project item or set Project Status | not stated | [UNVERIFIED] |
| Edit another user's issue title or body | not stated | [UNVERIFIED] |

- Collaborator roles on `IronbellyOrg/IronClaude` (via `gh api repos/IronbellyOrg/IronClaude/collaborators`, caller is admin): 1 admin, 2 maintain, 8 read, 0 triage, so at least 3 accounts can apply an approval label or assign an issue. Organization owners not listed as collaborators were not enumerated [OBSERVED].
- Issue #331 events (`gh api repos/IronbellyOrg/IronClaude/issues/331/events`) include `labeled`, `issue_type_added`, `added_to_project_v2`, `project_v2_item_status_changed`, `issue_field_added`, `assigned`, each with `actor.login` and `created_at`; whether the status event payload shows "Backlog" is [UNVERIFIED] [OBSERVED].
- `gh project list --owner IronbellyOrg` failed on the research workspace with "your authentication token is missing required scopes [read:project]"; the Project and Status criteria therefore cannot be evaluated with that token [OBSERVED].
- Routing inputs and who can set them (R03 section 4.3; reconciled in R02 section 2c):

| Input | Who can set it | Interaction with the claim code | Weakness |
|---|---|---|---|
| Assignee equals the workspace's `gh` login | Triage or higher (the `assigned` event records the actor) | Claim enforces it: other assignee stops (`claim.md:41`); own login continues (`claim.md:42`); `--add-assignee @me` (`claim.md:47`) | A Read-role user can be assigned but cannot self-assign; an unassigned issue has no owner, so every polling workspace sees it |
| Per-person label | create: Write; apply: Triage | none in the repo | new labels need a maintainer; `/sc:issue` will not create them (`labels.md:7`) |
| Project custom field or Project assignee | Project role [UNVERIFIED] | none | needs `read:project` scope on every workspace token (not granted on the research workspace) |

- A mis-routed launch cannot take another person's issue because Wave 2 stops on a different assignee (`claim.md:41`); it can still claim an unassigned issue for the wrong login because Wave 3 checks then adds (`claim.md:47`) (R03 section 4.3).
- The 4 routing candidates of R01 section 9 (assigned to own login; per-person label; Project field; unassigned first-come) and their selector, dedupe and failure shapes are carried as a decision for the plan: no file shows which candidate the owner picks, and ADDENDUM 2 names none (R02 section 2c). Candidate 1 needs no new label and no Project read; candidates 2 and 3 need new setup; candidate 4 is a race with no mutual exclusion (R01 section 9).

**What a prompt-injected issue could make a watcher-started session do today** (R03 section 6; derived from configuration and code, nothing was attempted or run live)

| Capability | Why it is available | Evidence |
|---|---|---|
| Read any file the workspace user can read, including the `gh` token file and `ccsession.env` | no deny rules, no Read hook; claim workers have Read/Grep/Glob/Bash | settings files (no `permissions`), `issue-worker-t3.md:5`, `ccsession:127` |
| Run arbitrary shell commands | ccsession default flag `--dangerously-skip-permissions`; hooks cover few commands | `ccsession:136-141`; `block-bare-python.sh:338-344` |
| Use `gh` with scopes `repo, workflow, read:org, gist` as the workspace owner | the token is the owner's | `gh auth status` |
| Publish content to a public place | `gh issue comment` is part of the sanctioned flow; `gist` scope allows `gh gist create` | `SKILL.md:72`, `:74` |
| Push branches or to `master` | no pre-push guard; `master` unprotected, no rulesets | R03 section 2.3 |
| Modify workflows | `workflow` scope | `gh auth status` |
| Use the ClickUp token | `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` read from the environment when set | `claim.md:48-50` |

Mitigating facts that hold today: the launch prompt is fixed text plus an integer; the claim ends after `next-steps.md` and never runs a next-step command (`claim.md:80`, `SKILL.md:88`), so injected text cannot chain into brainstorm or implement through the skill's own flow; claim mode refuses a foreign repo URL, a PR number, a closed issue and an issue assigned to someone else (`origin_repo.py:102-153`; `claim.md:37-43`); the design's threat model excludes deliberate evasion and a hostile agent (`sc-issue-launch-level-hook.md:32`, `:450`), so prompt injection of a bypass-mode agent is the TH3 case the design does not claim to stop.

**Security properties: provided versus missing** (R03 section 7)

| Property | Provided today | Missing |
|---|---|---|
| Authentication of workspace to GitHub account | By construction under option A: poller and claim both use the workspace's own `gh` login (`claim.md:16`; `issue-worker-t3.md:21`); the claim assigns `@me` (`claim.md:47`) | No check that the Coder workspace owner is the `gh` login's owner (Coder-side, the scope of Coder#477, unnecessary under option A) [UNVERIFIED outside this repo]; token stored in a file the session can read |
| Authorization of who may approve | None in code | A poller-side approver allow-list read from the label-event actor; GitHub's Triage-or-higher gate is the only barrier |
| Authorization of who may route (assignee) | Claim stops on a different assignee (`claim.md:41`) | Nothing stops a Triage account assigning any user; Wave 3 claims an unassigned issue for whoever runs it |
| At-most-once claim | Not provided: check-then-act; re-claim by the same login is idempotent (`claim.md:42`) and Wave 6 edits earlier marked comments (`claim.md:84-89`) | The claim sets no label or Project status (`labels.md:7`), so a 5-minute poller sees the issue as still eligible; it needs its own dedupe state, or a rule that the issue is assigned to its own login and carries no claim marker comment of its own |
| Auditability | GitHub events with actor and time (observed on #331); claim comments with markers (`claim.md:29`, `:84-89`); local artifacts under `.dev/issues/<N>/` (`issue.md:68`) | No record of the poller's decision (issue, login, approver event, time); no central trail of routing (a #477 requirement) |
| Containment of the launched session | Dormant identity hook only | No guard script, no permission policy, no branch protection |
| Input validation of the number | In-session `_NUMBER` regex (`origin_repo.py:74`) | A pre-launch validator in the poller |

**Open governance decisions recorded by the research** (R03 Gaps 10, 11; GQ #14, #15): the repo has no approver allow-list (where the poller keeps one, and whether the rule is "label applied by an allow-listed account, latest `labeled` event"); and at-most-once as local dedupe state versus "issue assigned to my login and no claim marker comment of mine", with the real race window between claim Wave 1 and Wave 3 not measured. These are listed as open items, not decided here.

**Key findings of 2.4**

- The only launch-governance code that exists is the dormant per-Bash-job identity adapter, not even installed on the research workspace; the guard, the `--pipeline` interface, the marker binding and the pre-push layer are design only; B-CTX blocks only those pipeline levels.
- Nothing registered constrains a watcher-started session; the repository is public; the `gh` token is a readable file with `repo, workflow, read:org, gist` scopes; `master` is unprotected.
- The integer-only prompt rule is necessary but not sufficient: the claim reads title, body and all comments and posts worker-written files without review.
- Approval and routing authority rest on GitHub roles (3 accounts can label or assign today); the label-event actor and the assignee are the available inputs; at-most-once, approver allow-listing, pre-launch integer validation and a permission-mode decision must all be built into the poller and its launch.
- The Worker Contract does not govern a plain `orca agent launch` session; its "instruction in the live conversation" basis for outward actions does not describe an automated trigger, so the design must state its own basis (R03 section 5).

### 2.5 Current State Summary

| Area | Verified current state | Exists today? | Key evidence |
|---|---|---|---|
| Automatic trigger of a claim | None; `/sc:issue` is explicit-only | No | `src/superclaude/commands/issue.md:24` |
| Watcher / poller code | No Python module under `src/superclaude` calls `gh` or `orca`; no workflow with `schedule:` or `issues:` | No | R02 sections 1, 3.2 |
| Selection by "tagged, human-approved, in a Project, Backlog" | Not done by the claim; no trigger or approval label (9 default labels only); Project read missing the `read:project` scope on the research token | No | `refs/labels.md:7-13`; R02 section 2; R03 section 4.2 |
| Claim behaviour | Non-interactive, claim-only: assign `@me`, optional ClickUp, accuracy check, summary, two marked comments, stops at `next-steps.md` | Yes | `claim.md:13-90`; `issue.md:15`, `:79`, `:83` |
| Issue text's expectation that the claim orchestrates a pipeline | CODE-CONTRADICTED; `--claim --pipeline` is design only | No | `issue.md:15`; design `:34`; `launch-level-guard.sh` absent |
| Prompt validation | In-session only (`origin_repo.py` `_NUMBER`); no pre-launch validator | Partly | `origin_repo.py:74`, `:102-153` |
| Starting a top-level session with a prompt | `orca agent launch --agent claude --worktree path:<abs> --surface terminal --prompt ...` documented and installed locally; slash-command execution of the prompt not verified | Mechanism yes, end-to-end unverified | R01 section 12 |
| Dispatch route for `/sc:issue` | Never-as-worker; ordinary top-level session only | Yes (as a constraint) | `WORKER-CONTRACT.md:23`, `:11` |
| At-most-once / mutual exclusion | Not provided by the claim; same-login and cross-login races derived from code | No | `claim.md:26-47`; R01 sections 9-10 |
| Result visible to a poller | Only GitHub (assignee, marked comments) and `.dev/issues/<N>/`; no result file; ClickUp step can take up to 20 pages at 30 s per request | No machine-readable result | `SKILL.md:101-117`; `clickup_claim.py:74`, `:76` |
| Repo-to-checkout mapping | The claim reads only `origin` of the current directory, so a multi-repo watcher needs a repo-to-checkout map (analysis finding F5) | n/a (single repo) | `origin_repo.py:156-174`; `SKILL.md:70` |
| Governance of the launched session | Only a dormant identity hook (not installed on the research workspace); no permission rules; `master` unprotected; public repo | No effective constraint | R03 sections 1, 2 |
| Approver / routing authority | GitHub roles only; 3 accounts can label or assign; label-event actor available; no allow-list | Partly | R03 section 4 |
| Test technique for `gh` | PATH-stub executables with logged argv (5 files under `tests/pr_submit/`) | Yes (reusable pattern) | R02 section 3.4 |
| CLI registration, tests, gates | `main.py` lazy-import block after l.561; `tests/<pkg>/`; ruff, pytest, `lint-architecture`, `verify-deps`; no `.claude/` mirror for pure CLI code | Yes (pattern) | R02 sections 4-6 |
| Design doc format | `docs/designs/sc-issue-command.md` skeleton plus the launch-level doc's UNVERIFIED section | Yes (pattern) | R02 section 7 |
| Coder listener / registration (Coder#477) | Lives in the Coder repo; filed assuming a push design; unnecessary under option A | Out of repo | `research/research-notes.md`, ADDENDUM and ADDENDUM 2 |

**Flow from a labeled issue to a claim as it works today** (only code-verified parts are drawn; doc-only items are excluded)

```
  GitHub (public repo IronbellyOrg/IronClaude)
  +-----------------------------------------------------------+
  | Issue #N created (forms add bug/enhancement or no label)  |
  | A Triage+ person could label/assign (3 accounts today)    |
  +-----------------------------------------------------------+
        |
        |  [DOES NOT EXIST] trigger/approval label (only 9 default labels)
        |  [DOES NOT EXIST] watcher/poller: every 5 min, own `gh` login,
        |                   select by label / Project / Backlog, approver
        |                   check, integer-only prompt, dispatch record
        |  [DOES NOT EXIST] automated `orca agent launch ... --prompt
        |                   "/sc:issue --claim <int>"` (mechanism documented,
        |                   slash-command execution UNVERIFIED)
        v
  Today: a person types `/sc:issue --claim <N>` in a session   (issue.md:24)
        |
        v
  Wave 0  origin_repo.py: integer / #N / origin URL accepted;
          gh auth status; mkdir .dev/issues/<N>/                (claim.md:13-20)
        v
  Wave 1  issue-worker-t3 reads issue title/body/comments       (claim.md:26)
          -> scout.md                  (needs claude-gw-tier* IDs, SKILL.md:58-62)
        v
  Wave 2  STOP (no write) if PR / closed / assigned to other    (claim.md:39-41)
          continue if unassigned or assigned to own login       (claim.md:42)
        v
  Wave 3  gh issue edit --add-assignee @me  <== FIRST GitHub write
          (+ ClickUp assign if configured)                      (claim.md:47-50)
        v
  Wave 4  accuracy-check.md, issue-summary.md                   (claim.md:54-59)
  Wave 5  recommend.md, next-steps.md                           (claim.md:78-80)
        v
  Wave 6  post/edit 2 marked comments; STOP                     (claim.md:84-90)
        |
        v
  next-steps.md is run by a person, never by /sc:issue          (issue.md:71)
  [DOES NOT EXIST] claim --pipeline, launch-level-guard.sh      (design :34, :40)
  [NOT SET BY CLAIM] labels, Project status: issue stays in Backlog
```

### Carried to Open Questions

Items tagged [UNVERIFIED] in Section 2 or listed in `gaps-and-questions.md`; none is presented as fact above.

| # | Item | Source | Tag |
|---|---|---|---|
| 1 | Whether `/sc:issue --claim <N>` runs as a slash command when given as the initial prompt of `orca agent launch --prompt`; needs one owner-run live test in the live-plan phase | R01 Gaps 1; GQ #1 | UNVERIFIED |
| 2 | Whether `agent launch` passes the prompt as argv or as a typed `--prefill` paste (a prefilled prompt would not run unattended); exact JSON key nesting of `--json` output and the real JSON error body of `reportCliError` | R01 Gaps 2; R03 Gaps 4; GQ #2 | UNVERIFIED |
| 3 | Same-login race (one person with several workspaces polling with one login) and the cross-login double-claim, both derived from code and not observed; GitHub's multi-assignee behaviour | R01 Gaps 3; R02 Gaps 10; GQ #3 | UNVERIFIED (derived) |
| 4 | Coder workspace facts: Orca runtime reachable, `ccsession-orca` configured, `claude-gw-tier*` IDs served, permission mode and whether `orca agent launch` applies `agentDefaultArgs`, `gh` authenticated as the person, ClickUp variables | R01 Gaps 4; R03 Gaps 5; GQ #4 | UNVERIFIED per host |
| 5 | Whether the workspace `gh` token can read the org Project (`read:project` missing on the research token); Project and Status access, and the `gh issue list --json` field set including a native issue type | R01 Gaps 5; R02 Gaps 2, 9; R03 Gaps 8; GQ #5, #11 | UNVERIFIED |
| 6 | Whether tests pin the claim-stops-after-`next-steps.md` text (one test file searched, others unread) | R01 Gaps 6; GQ #6 | open question |
| 7 | Whether an existing `<D>` directory is tolerated on a claim re-run | R01 Gaps 7; GQ #7 | UNVERIFIED |
| 8 | Whether `--claim` works under `claude --print` (only for a headless route) | R01 Gaps 8; GQ #8 | UNVERIFIED |
| 9 | Where the 5-minute poller runs (cron, systemd or a shell loop in a Coder workspace), whether it survives autostop and restart, and where its dispatch record lives; under option A this is the whole "Coder-side listener" | R01 Gaps 9; R03 Gaps 15; GQ #9 | UNVERIFIED |
| 10 | Whether `labeled` events are a trustworthy "who approved" signal; comment `author_association`; detectability of a post-approval body edit | R02 Gaps 3; R03 Gaps 7; GQ #10 | UNVERIFIED |
| 11 | Trigger and approval label names and the Project/Status mapping are defined nowhere; the fork lacks the `type:*`/`complexity:*` labels `/sc:issue --create` expects | R02 Gaps 7, 8; GQ #12 | open question |
| 12 | Policy for the claim's own reads of issue title, body and comments | R03 Gaps 6; GQ #13 | open decision |
| 13 | Approver allow-list: where it lives and the exact rule | R03 Gaps 10; GQ #14 | open decision |
| 14 | At-most-once design: local dedupe state versus "assigned to my login and no claim marker of mine"; per-cycle launch cap and retry cap; the real race window between Wave 1 and Wave 3 was not measured | R03 Gaps 11; R02 section 2c; R01 sections 9-10; GQ #15 | open decision |
| 15 | Whether `--worktree issue:<number>` triggers the Orca-to-GitHub linking that the project rule forbids (use `path:` until tested) | R03 Gaps 12; GQ #16 | UNVERIFIED |
| 16 | Whether org owners outside the collaborator list can label; GitHub permission to edit another user's issue body; Project permissions | R03 Gaps 9; GQ #17 | UNVERIFIED |
| 17 | Governance files not read: `freshness-pre-edit.sh`, `sc-recommend-phase0.sh`, `issue-worker-t2.md`, `issue-worker-t1.md`, `tests/cli/test_install_hooks.py` | R03 Gaps 13; GQ #18 | NOT READ |
| 18 | Whether the Coder workspace owner and the workspace's `gh` login are always the same person (Coder-side tie; Coder#477 scope) | R03 Gaps 14; GQ #19 | UNVERIFIED outside the repo |
| 19 | Reading that a poller-launched ordinary session is outside the never-as-worker list is an interpretation of `WORKER-CONTRACT.md:11` and `:23`, not an owner statement; whether Orca-started Claude sessions stay open after the claim stops (inference from `SKILL.md:88`) | R01 tagged claims; GQ #24 | UNVERIFIED |
| 20 | Why `launch-job-identity.sh` is registered in the packaged `hooks.json` but not installed on the research workspace (cause not established) | R03 Gaps 3; GQ #21 | CODE-CONTRADICTED on this host; cause UNVERIFIED |
| 21 | Whether the ClickUp identity (personal token) and the `gh` login belong to the same person; no code ties them | R01 section 6 | UNVERIFIED as an enforced rule |

### Findings carried versus excluded

- Carried: every Key Takeaway and Summary finding of R01, R02 and R03 appears in Sections 2.1 to 2.5 or in the Open Questions list above.
- Excluded with rationale: the research-file material on Actions schedule limits, Projects v2 token types, rate limits, Coder primitives and option B/C listener contracts (`web-01-github-events-projects-and-limits.md`, `web-02-coder-claude-dispatch-and-security.md`) is external context assigned to later sections, not current-state facts; R02's recommended test shapes and Makefile detail beyond the gate list are plan-level and left for the options and plan sections.
- Contradictions between research files: the earlier R02 text "skip issues that already have an assignee" contradicted R01 and R03; it was amended in fix cycle 1 and R02 section 2c holds the reconciled predicate used above (stronger evidence: `claim.md:41-42`, read directly).
