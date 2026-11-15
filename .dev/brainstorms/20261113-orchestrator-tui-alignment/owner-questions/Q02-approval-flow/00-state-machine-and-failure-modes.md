# Q2 approval flow: state machine and failure modes (shared input to proposals A, B and C)

Status: input to the debate, written 2026-11-14 by the Q2 approval-flow worker. Advice only; the owner decides.

## Terms used here

- **Watcher**: `superclaude issue-watch`, the built issue poller (issue #331). Every 5 minutes (once a cron entry exists, which it does not yet) it looks for an approved issue and starts one top-level Claude session that runs `/sc:issue --claim <N>`.
- **Claim session**: that session. It assigns the issue, posts two marked comments and, at the default level the owner chose (Q2 option 3), creates the Orca worktree `issue-<N>` and launches a second agent there.
- **Governed agent**: the second agent in worktree `issue-<N>`. At the `worktree` level it runs `next-steps.md` up to a plan boundary, prints `Waiting for approval`, and waits.
- **Coordinator**: a person-opened Orca session that supervises workers under `~/.claude/WORKER-CONTRACT.md` (WC-12: answers are pulled by the worker and acknowledged; WC-16: the coordinator loop). No coordinator is attached to watcher or claim sessions today.
- **Observer / TUI**: `superclaude observe`, the built read-only terminal dashboard (issue #409). "Decision Desk" is its planned, gated release 3 (work item OB-09).
- **Plan version**: the SHA-256 of the plan file's bytes. Used below to tie an approval to the exact plan a person read.
- Work-item ids (WA-01 to WA-07 watcher, OB-09 observer Decision Desk, SW-13 sub-orchestrator design, XC-01 owner ledger) come from `merged-requirements.md` section 2.

## What exists today versus what the owner's flow adds (read in code and docs on 2026-11-14)

| Piece | Exists today? | Evidence |
|---|---|---|
| Watcher trigger: trigger label, approval label applied by an allow-listed **User** account id after the trigger, issue unchanged since approval, assignee exactly the watcher's own login, Project Status exactly `Backlog` | Yes | `src/superclaude/cli/issue_watch/predicates.py` `approval_of`, `unchanged_since`, `is_intended_owner`, `project_check` |
| Watcher reads the actor of a **label** event (id, login, type) | Yes | `github.py` `EVENTS_JQ` |
| Watcher reads who changed the **Project Status** field | No. It reads only the current Status value (`PROJECT_ITEMS_QUERY`, `fieldValueByName(name: "Status")`). Whether GitHub exposes the actor of a Project status change through an API the watcher could call is UNVERIFIED | `github.py` `PROJECT_ITEMS_QUERY` |
| Watcher writes anything to GitHub or the Project | No, by design (NG-2, NG-3) | `docs/designs/issue-watcher.md` section 2.4 |
| At-most-once launch per issue: `dispatch.json` entry written `pending` (fsynced) before `agent launch`; `claimed` is terminal; `unknown` never relaunched without `reset --forfeit-guarantee` | Yes, claim stage only | `issue-watcher.md` sections 7.3, 7.4 |
| Watcher reacts to any stage after the claim (a Status move out of Backlog, a review state) | No. A non-Backlog Status is a skip (`project_mismatch`); a `claimed` entry is terminal | `predicates.py` `project_check`; `issue-watcher.md` 7.3 |
| Claim posts: assignment, accuracy-check comment, claim comment with marker `<!-- sc:issue:claim -->` | Yes | `~/.claude/skills/sc-issue-protocol/SKILL.md` Wave 3, Wave 6; `templates/claim-comment.md` |
| Claim sets labels or moves Project Status | No ("Write any issue field other than Complexity" is a Will Not) | `src/superclaude/commands/issue.md` Boundaries |
| Claim touches ClickUp | Assignment only, when `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` are set; never a ClickUp status | `scripts/clickup_claim.py` (PUT `assignees.add` only) |
| `next-steps.md` posted to the issue | No. It stays in `.dev/issues/<N>/` (copied into the worktree); the claim comment only links its repository path, which "open[s] on GitHub only after someone commits and pushes the files" | `templates/claim-comment.md` |
| Plan approval today | In the governed agent's own session only: "A human approves by replying `approved` in this session or by running the printed implement command." Nothing is recorded on GitHub, in a ledger or in Orca | `templates/launch-prompt.md` worktree block |
| Plan posted as an issue reply, issue moved to a review state, assignee mentioned | Not built | none found |
| Coordinator attached to the governed agent, or a watcher-to-coordinator handoff | Not built (WA-07 and SW-13 are DEFERRED; watcher sessions are Run-less) | `merged-requirements.md` 2.3 WA-07, SW-13 |
| TUI approval | Not built. The observer forbids `send`, `ask`, `reply` and every other write verb (`observe/adapter.py` `FORBIDDEN_PREFIXES`); its questions read is switched off (`QUESTION_GATE_PASSED = False`); write-back is a "future stage" needing a #409 boundary change | `observe/commands.py`; `.dev/issues/409/bmad/spec-orca-observer/release-gates.md` |
| Permission mode | Launched sessions on this host run with permission checks off; they read issue text anyone who can edit the issue controls | `merged-requirements.md` 2.3 current state |
| One GitHub account on the host | The runbook allows the approver to be the watcher's own login ("If the approver is a different person, that person runs the last command"); the claim session, the governed agent and any coordinator use the host's `gh` login (UNVERIFIED that no second login is configured) | `docs/designs/issue-watcher-setup.md` section 4; FU-6 "Do not add a second approver before FU-6" |

## The owner's flow as a state machine (plain words)

| # | Stage | Entered when | Who may move it there | Where it is recorded | Built? |
|---|---|---|---|---|---|
| S0 | Ready to claim | Trigger label, then approval label by an allow-listed account, assigned to the watcher's login, Status `Backlog` | A person (labels, assignee, Project) | GitHub labels and label events, assignee, Project Status | Yes (read by the watcher) |
| S1 | Claimed | The watcher wrote `pending`, launched, and later saw the claim marker | Watcher (launch) and claim session (marker) | `dispatch.json` entry `claimed`; claim marker comment; assignee; ClickUp assignee | Yes |
| S2 | Planning | Claim session created `issue-<N>` and launched the governed agent | Claim session | `.dev/issues/<N>/worktree.json`; Orca worktree and agent | Yes (default level) |
| S3 | Plan ready | Governed agent printed `Waiting for approval` | Governed agent | Only on the agent's screen | Partly (no record anywhere) |
| S4 | In review | Plan posted as an issue reply, issue moved to a review state, assignee mentioned | NEW: whoever is given the job (the owner says the coordinator is instructed to do it) | NEW: issue comment, Project Status (value names UNVERIFIED), mention | No |
| S5 | Approved | The assignee moves the issue to the next state, or approves in the Orca session or TUI | A person (the assignee) | NEW: GitHub Status move, or Orca-side record; today only a typed `approved` in the agent session | No (as a recorded stage) |
| S6 | In progress | The governed agent is told to continue past the plan boundary | NEW: the coordinator, per the owner | Agent session; NEW ledger row | No (today the person types directly) |
| S7 | Finished | Work done; at the `worktree` level no commit, push or PR | Governed agent | Worktree files | Partly |

Backward moves the owner did not describe but which can happen: S5 back to S4 (approval withdrawn), S6 back to S4 (issue moved back after work started), any stage to closed.

Places a stage could be recorded once the flow exists: (1) GitHub labels and label events; (2) GitHub Project Status field; (3) issue comments (plan reply, mention, approval comment); (4) the watcher's `dispatch.json`; (5) the claim's `worktree.json`; (6) the Orca Run mailbox and the governed agent's session; (7) the observer snapshot (read-only copy of Orca); (8) the coordinator's ledger (format in `merged-requirements.md` 6.8, not built for this flow); (9) ClickUp, only if someone adds status mirroring (today assignment only).

## Failure modes of two approval channels

| id | Failure | One-line scenario | Harm |
|---|---|---|---|
| F1 | Double start | The owner approves in Orca; the coordinator moves the issue to the next state and starts the agent; the watcher sees the move 5 minutes later and asks the coordinator to start the same work | Two runs of the same stage: duplicate commits in one worktree, two PRs, double cost, conflicting edits |
| F2 | Approval while the coordinator is down | The assignee moves the issue on GitHub at night; no coordinator is running | Nothing starts (safe) or, worse, a second path starts it and the coordinator later starts it again on restart |
| F3 | Same-account echo | The coordinator and the person both act as the host's single `gh` login; the watcher sees a Status move by that login | The watcher cannot tell the coordinator's own mirror write from a fresh human approval, so it re-triggers (F1) or ignores a real approval |
| F4 | Plan edited after approval | The agent rewrites `plan.md` after the person approved it | Work proceeds on a plan nobody approved |
| F5 | Moved backwards after start | The assignee moves the issue back to review while the agent is implementing | The agent keeps going, or two systems disagree on whether to stop; a later forward move restarts finished work |
| F6 | Delayed or lost events, polling lag | GitHub returns the old Status for a while; the watcher runs every 5 minutes; an Orca message is not acknowledged | The two places disagree for minutes; event-triggered logic fires late, twice, or never |
| F7 | Two approvals at the same moment | The owner approves in the TUI while a second coordinator session (or the person in the agent's own session) approves too | Two starts, or one start with the other approval's record lost |
| F8 | Someone else, or the agent itself, moves it | A collaborator with Project write access drags the card; or the permission-free governed agent, steered by issue text, runs `gh` to move its own issue or types `approved` | Unauthorised start; with permission checks off on one shared account, a forged approval looks identical to a real one |
| F9 | Stale TUI | The TUI shows "In review" from a 45-second-old snapshot (observer STALE threshold) after approval already happened, and the person approves again | A second approval for the same stage, or approval of an outdated plan |
| F10 | ClickUp as a third place | Someone mirrors stage into the ClickUp task status and a person changes it there | A third source of truth that nothing reconciles; today the claim writes only the ClickUp assignee, so this exists only if added |
