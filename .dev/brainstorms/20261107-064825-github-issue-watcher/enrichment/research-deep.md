# Research deep: condensed copy of the research for issue #331 (GitHub issue watcher), 2026-11-07

Condensed copy of `RESEARCH-REPORT-issue-watcher.md`. The full report is authoritative; where this copy and the report differ, the report governs. Every statement is condensed from the report; nothing is new.

## Pointer to the full report

- Full report: `.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/RESEARCH-REPORT-issue-watcher.md`
- Evidence trail: `.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/research/` and `.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/synthesis/`

## Recommendation

**Option A, the workspace-side poller (pull). Decided by the owner (ADDENDUM 2).**

- Each workspace polls GitHub every 5 minutes with its own `gh` login and starts the claim with `orca agent launch`.
- There is no listener, no inbound port and no address registry.
- Why: it is the only option besides D with no inbound exposure, it needs no privileged Coder token, it has the lowest effort (M) of the options that start a session, and it uses the identity the claim already uses (`--add-assignee @me`).
- Polling cost is about 0.24 percent of the 5,000 an hour user allowance per call type (12 polls an hour).
- Where B and C are structurally stronger (one allow-list copy, a central audit trail, a single decision point) is recorded as revisit conditions, not as scored credit (Section 7.2).

**Claim-only scope (D2, decided by the owner).** The watcher's job ends at starting `/sc:issue --claim <N>`. The claim stops by design at `next-steps.md`; the pipeline after it stays manual. Only a validated integer reaches the prompt (D3).

**Intended-owner filter.** A workspace's poller must take only issues meant for its own `gh` login. The choice is still open: no addendum names a candidate. The research supports candidate 1 (issue already assigned to the own login; the claim already continues on its own login and stops on another, `claim.md:41-42`). The shared predicate is "skip an issue assigned to a login other than the own login". The plan implements candidate 1 behind one replaceable function. Other candidates: per-person label, Project field, unassigned first-come (the only racy one). The same-login multi-workspace case stays open under every candidate.

**Security model for tying a workspace to a GitHub account (Section 7.3).**

- Identity: each workspace uses its own `gh` login, read each cycle with `gh api user -q .login`; the poller does not assume the Coder owner equals it.
- Prompt: `"/sc:issue --claim " + str(int(number))`, with `number` from the `gh` JSON `number` field, anything not a positive integer rejected, passed as one argv element, no shell.
- Fields read: `number,labels,assignees,state` only, never title, body or comments; every repository-scoped call carries `--repo IronbellyOrg/IronClaude`, never gh's default repo.
- Approval: "human-approved" is a GitHub-side act by a Triage-or-higher account (3 accounts today); the poller compares the actor of the latest `labeled` event of the approval label with an approver allow-list (location and rule open).
- Launch: an ordinary top-level session through `orca agent launch`; the poller is a plain process, never a worker Task and never run inside a Claude session.
- Residual risk, stated and not solved: the integer-only rule protects the prompt, not the session; the claim reads title, body and comments live in a public repo and nothing registered constrains the launched session.

## Options table

| Option | How it works (one line) | Effort | Risk | Inbound exposure | Workspace-to-account binding | Verdict |
|---|---|---|---|---|---|---|
| A: workspace poller (pull) | A plain process in each workspace polls GitHub every 5 minutes with its own `gh` login and runs `orca agent launch ... "/sc:issue --claim <int>"` | M: one Click package, tests, design doc, label instructions; no workflow | Medium: open launch, scheduler, scope and race facts | None: no listener, no inbound port | The workspace's own `gh` login equals the claim's `@me`; owner equals login is unchecked | Recommended; decided by the owner (D1) |
| B: GitHub Action plus workspace listener (push) | A scheduled or `issues` workflow selects issues and calls an authenticated listener in the owner's workspace | L in this repo plus unsized Coder#477 work; first `schedule:` workflow in the repo | High: inbound path, privileged tokens, dropped runs | Listener reachable through the Coder control plane (`share` must not be `public`) | GitHub login to Coder user to workspace chain, documented per link only; privileged Coder token held outside the workspace | Documented alternative; revisit conditions only |
| C: central microservice plus listener (push) | A GitHub App with org webhooks feeds a service that routes to the same workspace listener | XL: new service to host (hosting not established), App, listener | High: inbound endpoint, privileged tokens, no automatic webhook redelivery | Webhook endpoint reachable by GitHub plus the workspace listener | As B | Documented alternative; revisit conditions only |
| D: hybrid label relay | A scheduled Action writes a "ready" label; each workspace polls that marker as in A | L: A in full plus a workflow, a secret and a label | Medium: no inbound surface; best-effort central step | None | As A | Not chosen; first fallback for revisit condition 6 (workspace token cannot read the org Project) |

Scoring note (Section 6, a count and not a weighted score): A and D 2 Meets and 8 Partly; B 1 Meets and 9 Partly; C 0 Meets and 10 Partly; no Does-not-meet cells. The count rates only what exists today, so it does not credit B or C for components that are not built.

## Answers to the three questions of issue #331

1. **Microservice versus GitHub Action.** Neither. The owner chose option A, a poller in each workspace. B (Action plus listener) and C (microservice plus listener) remain documented alternatives with nine revisit conditions (Section 6).
2. **Binding each workspace to a GitHub account.** Under A the binding is the workspace's own `gh` login; the poller reads it each cycle and the claim assigns `@me` of the same login. Whether the Coder workspace owner is the same person as that login is not checkable in this repo [UNVERIFIED].
3. **The Coder-side listener.** There is none under A: no listener, no inbound port, no registry. The 5-minute poller is the whole Coder-side component, run by a `coder_script` cron entry that lives in the Coder repo. Where it runs and keeps its state in the target template is [UNVERIFIED].

## Verified facts that constrain the design

1. The claim stops after writing `next-steps.md` and never runs a next-step command: `src/superclaude/commands/issue.md:15`, `:83`; `src/superclaude/skills/sc-issue-protocol/refs/claim.md:80`, `:90`. The issue text's expectation of a full pipeline is contradicted by these lines.
2. `/sc:issue` is on the never-as-worker list (`src/superclaude/core/WORKER-CONTRACT.md:23`) and a worker session never calls `agent launch` (`:61`), so the launched session is an ordinary top-level session started by a plain process.
3. `--claim --pipeline` is design only: `issue.md:35-41` has no `--pipeline`; `docs/designs/sc-issue-launch-level-hook.md:34` says the current claim code does not implement it; `launch-level-guard.sh` does not exist. The B-CTX gate (design section 19.1) blocks only a later pipeline extension.
4. The claim has no mutual exclusion: it reads (`claim.md:26`), checks (`:41-42`), then adds `--add-assignee @me` (`:47`), and it never reads or moves a Project item, so the issue stays in Backlog. GitHub assignment is additive with no compare-and-set (https://docs.github.com/en/rest/issues/assignees).
5. The repository is PUBLIC (`gh repo view`, 2026-11-07) and the claim reads title, body and comments live (`claim.md:26`). The only integer check runs inside the session (`src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:74`, `:102-153`), so it is a second check, not a prompt-boundary validator.
6. `orca agent launch` (`/opt/Orca/resources/app.asar.unpacked/out/cli/specs/agent-launch.js:9-33`; `agent-launch-request.js:63-65`) submits the prompt, needs an existing worktree, has no `--repo` flag and no permission-mode or allowed-tools flag, and a lost reply is retried only with `--retry-launch <operationId>`, never as a fresh launch. Whether a leading `/sc:issue` runs as a slash command is UNVERIFIED.
7. No approval or trigger label exists (the fork has the 9 default labels; `refs/labels.md:7`: `/sc:issue` never creates labels). Triage is the lowest role that can label (https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization) and `labeled` events carry `actor` (https://docs.github.com/en/rest/issues/events).
8. Reading a Project needs `read:project` (https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects); the observed workspace token lacks it. `gh project item-list` defaults to 30 items (https://cli.github.com/manual/gh_project_item-list), so the poller sets `-L 100`.
9. Rate limits: 5,000 REST requests an hour per user, shared across that login's tokens (https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api). The shortest scheduled-workflow interval is 5 minutes and runs can be dropped (https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows).
10. A poller can run as a `coder_script` with `cron = "0 */5 * * * *"` (six fields, seconds first; https://registry.terraform.io/providers/coder/coder/latest/docs/resources/script). Processes stop with the workspace, so a stopped workspace polls nothing and approved issues wait on GitHub.

## Owner decisions, Coder#477 and unverified items

**Decided by the owner (Sections 1.1 and 9.1).**

- D1: option A, the workspace-side poller; no listener, no inbound port, no address registry.
- D2: claim-only; the pipeline after the claim stays manual.
- D3: only a validated integer issue number reaches the session prompt, never title or body text.
- Repo-side deliverable: a design doc, a tested poller CLI (mock `gh`, mock `orca agent launch`, nothing run live) and trigger/approval label setup instructions. B, C and any live deployment are follow-up.

**IronbellyOrg/Coder#477.** The listener and registration live in the Coder repo, not in IronClaude. It was filed assuming a push design. Option A makes it unnecessary unless B or C is revisited. Under A the only Coder-repo follow-up is the `coder_script` cron entry that runs the poller and, if the template does not persist `$HOME`, a persisted path for the dispatch record.

**Revisit conditions (nine in the report, Section 6 table).**

- B: revisit if workspaces are mostly stopped and approved issues wait too long, poll latency or API use becomes a problem, central audit and one approver policy are needed, double claims occur despite best-effort checks, Coder ships the account binding, or a shared at-most-once ledger is needed (conditions 1 to 5 and 8; condition 6, a workspace token that cannot read the org Project, points to D first).
- C: revisit for the same conditions, and specifically if the need is to react to a Project Status change at event time or to see who moved an issue to Backlog (condition 7, the `projects_v2_item` webhook). Condition 9 (workspaces cannot run a recurring poller) is not settled by the research.

**Open decisions (not decided anywhere).**

- Intended-owner routing candidate and the same-login multi-workspace case (Q4, Q14).
- Approver allow-list location and rule (Q10).
- Trigger and approval label names, Project and Status mapping, label-only fallback (Q9).
- Policy for the claim's own reads of issue text (Q12) and the basis for a label-triggered outward action (Q36).
- At-most-once parameters: lease, attempt cap, launch cap (the plan proposes 60 minutes, 3 and 1 as [PROPOSAL] values) (Q13).

**UNVERIFIED items (each one line; full table in Section 9.2).**

- Q1: a leading `/sc:issue` given as the initial `orca agent launch --prompt` runs as a slash command.
- Q2: argv versus typed paste for `--prompt`; the JSON shape of success output and the error body.
- Q3: whether the target host's Orca follows the documented `--retry-launch` rule.
- Q5: per-host facts: Orca runtime reachable, `ccsession-orca` configured, `claude-gw-tier*` IDs served, `gh` as the person, ClickUp variables.
- Q6: permission mode of the launched session; `orca agent launch` cannot set it and whether it applies `agentDefaultArgs` is not traced.
- Q7: the poller's token can read the org Project (`read:project`).
- Q8: `gh project item-list --query "status:Backlog ..."` is accepted and the JSON schema of the items.
- Q11: a post-approval body edit is detectable; event retention; the REST comment author field name.
- Q14: same-login double claims and multi-assignee behavior, derived from code and not observed.
- Q15: where the poller runs and keeps state in the target template (cron overlap, `$HOME` persistence, systemd, Orca session as Coder activity).
- Q16: the Coder workspace owner and the `gh` login are the same person.
- Q17: which Orca checkout the launch uses, and whether `issue:<n>` triggers Orca-to-GitHub linking.
- Q18: a claim re-run tolerates an existing `.dev/issues/<N>/` directory.
- Q20: `/sc:issue --claim` works under `claude --print` (headless variant only).
- Q21: a poller-launched ordinary session is outside the never-as-worker list as owner intent; started sessions stay open after the claim.
- Q23 and Q24: rate-limit handling through `gh`; organization token policies.
- Q25 and Q34: org owners outside the collaborator list can label; the ClickUp identity and the `gh` login are the same person.
- Q22, Q26 to Q29: governance files not read; push-design details, external-context gaps and unresearched dispatchers (context only).
- Late edits unverified by a further review: Gate 3 fixes F1 and F2 (closed by owner-approved exception after the third review) and Gate 5 edits B1 and B2 (closed by owner-approved exception after the monotonicity halt). B1 limits the race-window estimate "seconds to minutes ... possible but not frequent" to a race between two different logins; the same-login window runs to the Wave 6 comment and has no estimate.

## Corrections to earlier notes

- **`src/superclaude/pr_submit/ci.py` is NOT a `gh` subprocess wrapper.** It imports only `re`, `.classifier` and `.models` (`ci.py:10-15`) and consumes an already-fetched payload. No Python file under `src/superclaude` builds a `gh` call, so a poller needs its own small injectable subprocess runner (plan step 2.2). The earlier research notes and `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/codebase-context.md` said otherwise; `codebase-context.md` was corrected on this point (line 21, "CORRECTION (2026-11-07, research alignment check)"), as the report records it, and so was `research/research-notes.md` (lines 30 and 37).
- **`orca agent launch` argument contract.** `--agent` is required; the checkout is chosen only by `--worktree <selector>` (no `--repo` flag; use `path:<abs>`, not `issue:<n>`); it needs an existing worktree; `--prompt` is submitted, and the prompt is one free-text argument with no permission-mode or allowed-tools flag; an unconfirmed outcome returns `agent_session_operation_unknown` with an `operationId`, retried only with `--retry-launch`.
- **`orca orchestration send` versus a new session.** `orchestration send` is durable but pull-only (the claim would not start until the session looks) and `terminal send` collides with a person's input; neither is known to run `/sc:issue`. A new top-level session per issue is isolated and is what the plan uses; its costs are one more tab and Claude process per issue and no coordinator visibility.
- The project `CLAUDE.md` calls `origin` a "private fork"; the live check shows `IronbellyOrg/IronClaude` is PUBLIC.

## Top plan steps (Section 8, nothing is run live)

| Step | Action | Files |
|---|---|---|
| 1.1 | Create the design doc in the house format with the header block and the purpose and binding-decision sections | `docs/designs/issue-watcher.md` (NEW) |
| 2.2 | Create the injectable command runner seam (`CommandResult`, `Runner`, `run_command` with an argv list, never a shell) | `src/superclaude/cli/issue_watch/runner.py` (NEW) |
| 3.2 | Create the integer-only prompt builder `build_claim_prompt` (accepts only an `int` from 1 to 999999999) | `src/superclaude/cli/issue_watch/launch.py` (NEW) |
| 3.4 | Create the launch function: prove the Orca executable, build the `orca agent launch` argv, map outcomes to `started`, `unknown` or `failed` | `src/superclaude/cli/issue_watch/launch.py` (NEW) |
| 4.2 | Create the read-only GitHub layer (own login, discovery, snapshot, label events, own claim marker) with `--repo IronbellyOrg/IronClaude`, `--method GET` and fail-closed truncation | `src/superclaude/cli/issue_watch/github.py` (NEW) |
| 5.2 | Create the poll cycle: five filters, claim-marker check, record written before launch, pre-launch re-read, caps, audit line (the `once` verb that exposes it is step 5.3) | `src/superclaude/cli/issue_watch/cycle.py` (NEW) |
| 6.5 | Run the gates: pytest for `tests/issue_watch/`, ruff check and format, `make sync-dev` then full pytest then `make verify-sync`, `make lint-architecture`, `make verify-deps` | `tests/issue_watch/` (NEW), `Makefile` targets |
| 7.1 | Write the trigger and approval label creation lines (`gh label create ... --repo IronbellyOrg/IronClaude`) into the design doc | `docs/designs/issue-watcher.md` (NEW) |

Registration (step 2.4) adds one block after the `reflect` registration in `src/superclaude/cli/main.py`; no `pyproject.toml` change and no `.claude/` mirror.
