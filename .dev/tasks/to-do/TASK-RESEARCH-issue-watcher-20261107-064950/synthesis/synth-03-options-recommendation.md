# Synthesis 03: Options Analysis and Recommendation (Report Sections 6 and 7)

**Issue:** IronbellyOrg/IronClaude#331 "Automated Github Issue / Task Watcher and Routing Service"
**Date:** 2026-11-07
**Status:** Complete
**Scope of this file:** report Section 6 (Options Analysis) and Section 7 (Recommendation) only.
**Binding owner decision (ADDENDUM 2, 2026-11-07T07:12Z):** Q1 = option A (workspace-side poller), Q2 = claim-only, Q3 = only an integer issue number reaches the session prompt. Coder#477 was filed assuming a push design; option A makes it unnecessary unless B or C is revisited.

## Source key and evidence tags

Every fact below comes from the research files. Citations use these short keys (all paths are under `.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/` unless noted):

| Key | File |
|---|---|
| R01 | `research/01-claim-flow-and-session-launch.md` |
| R02 | `research/02-github-surface-and-cli-patterns.md` |
| R03 | `research/03-governance-and-security-surface.md` |
| W01 | `research/web-01-github-events-projects-and-limits.md` |
| W02 | `research/web-02-coder-claude-dispatch-and-security.md` |
| GAPS | `gaps-and-questions.md` (rows are cited as "GAPS n") |
| NOTES | `research/research-notes.md` (ADDENDUM and ADDENDUM 2) |
| SUM | `.dev/issues/331/issue-summary.md` |

Section references such as "R01 §9" mean the numbered section of that file. Tags: [CODE-VERIFIED] traced in repo code or run locally; [CODE-CONTRADICTED] repo doc or issue text contradicted by code; [EXTERNAL-VERIFIED] confirmed on an official external page (web findings are external context and never override verified code behavior); [UNVERIFIED] not confirmed; [PROPOSAL] or [DERIVED] a design proposal or arithmetic taken from the research files, not a documented fact. The web research was done with WebSearch/WebFetch because Tavily was unavailable (W01, W02 headers).

---

## 6. Options Analysis

### 6.0 Basis for the analysis

**Requirements used for scoring.** They are taken from SUM ("What the issue asks for"), the binding addenda in NOTES and the sibling issue IronbellyOrg/Coder#477 as summarized in NOTES ADDENDUM point 2.

| ID | Requirement | Source |
|---|---|---|
| R1 | The issue is tagged (a trigger label) | SUM; NOTES |
| R2 | The issue is human-approved | SUM; NOTES |
| R3 | The issue is in a GitHub Project | SUM |
| R4 | The Project status is Backlog | SUM |
| R5 | The issue is meant for the developer whose workspace acts on it (intended-owner filter; for option A, how a workspace's poller decides an issue is meant for its own `gh` login so that workspaces do not race; for B, C and D, the routing step) | NOTES ADDENDUM 2; R01 §9; R02 §2c; GAPS 3 |
| R6 | The session starts in the right developer's workspace | SUM; Coder#477 (NOTES point 2) |
| R7 | The workspace is securely bound to one GitHub account | SUM; Coder#477 (NOTES point 2) |
| R8 | Senders are authenticated and authorized; no unauthenticated port is exposed | Coder#477 (NOTES point 2) |
| R9 | There is an audit trail of routing and access decisions | Coder#477 (NOTES point 2) |
| R10 | Exactly one session starts per issue (at-most-once) | NOTES (at-most-once patterns); R01 §10; R03 §7 |

**The three questions every option must answer** (from the issue and Coder#477): (Q-a) how the workspace is bound to a GitHub account, (Q-b) what the Coder-side listener is, (Q-c) what happens when the workspace is stopped.

**Facts all four options share** (so they are not repeated per option):

| Fact | Evidence |
|---|---|
| `/sc:issue --claim <N>` claims only: assigns `@me`, optional ClickUp, accuracy check, summary, two marked comments, then stops at `next-steps.md`; it never runs the next steps | R01 §1, §3 [CODE-VERIFIED] |
| The issue text expects `/sc:issue --claim` to kick off the full orchestration path | [CODE-CONTRADICTED] by `issue.md:15, :79, :83`, `claim.md:80` (R01 tagged claims; GAPS 20) |
| `/sc:issue` is on the never-as-worker list, so the session must be an ordinary top-level session, not a dispatched worker Task; WC-13 forbids `agent launch` from inside a worker session, so the launcher must be a plain process | `WORKER-CONTRACT.md:23, :61` (R01 §7; R03 §5) [CODE-VERIFIED]; that a poller-launched session is outside the list is the researcher's reading, [UNVERIFIED] as owner intent (R01 §7; GAPS 24) |
| The claim never reads labels or Projects; the watcher must do the tagged / approved / Project / Backlog gating itself | `labels.md:7`; R01 §3 [CODE-VERIFIED] |
| The claim does not move an issue out of Backlog, so a Backlog filter keeps seeing a claimed issue | R01 §3 [CODE-VERIFIED] |
| The claim has no mutual exclusion: check, then `--add-assignee @me`, which adds rather than replaces | R01 §9; R03 §7 [CODE-VERIFIED by reading]; GitHub assignment is additive with no compare-and-set (W02 G1 [EXTERNAL-VERIFIED]) |
| The claim reads issue title, body and comments live at claim time, so the integer-only prompt protects the launch prompt but not the session | R01 §13; R03 §3.2 [CODE-VERIFIED]; policy for these reads is open (GAPS 13) |
| The repo `IronbellyOrg/IronClaude` is PUBLIC (project CLAUDE.md calls it private) | R03 §3.3 [STALE DOC found; live check 2026-11-07] |
| Only 9 default labels exist on the fork; no trigger or approval label exists and `/sc:issue` never creates labels | R02 §2, §2b [CODE-VERIFIED]; GAPS 12 |
| No approver allow-list exists; label-applying authority is GitHub Triage role or higher (3 accounts today) | R03 §4.2, §4.3 [OBSERVED] |
| The observed workspace `gh` token lacks `read:project` (`gh project list` failed) | R03 §4.2 [OBSERVED]; GAPS 5 |
| `/sc:issue --claim` needs a checkout whose `origin` is the issue's repo, `uv`, `gh` auth, installed skills/agents and a gateway serving the `claude-gw-tier3/2/1a` picker IDs, else it stops at Wave 1 before any GitHub write | R01 §2, §11 [CODE-VERIFIED] |

**Contradictions and corrections noted between research files**

| # | Contradiction | Which finding is stronger |
|---|---|---|
| 1 | Option letters. W01 and W02 sometimes call the Action-based alternative "C" (W01 §2 "documented alternative C (an Action reacting to `labeled`)", §14.5 "Scheduled-Action alternative (C-lite)"; W02 H2 "Option C (an Action calls the listener) would fit OIDC well; option B (another service) would not"). The binding naming in NOTES ADDENDUM 2 is B = Action plus listener, C = central microservice plus listener | The binding naming governs. This file maps every web finding by its description (Action versus microservice), never by the web file's letter |
| 2 | R02 §2b (before amendment) said "skip issues that already have an assignee"; R01 §9 and R03 §4.3 select issues assigned to the own login | Resolved in R02 §2c: the single predicate is "skip an issue assigned to a login other than the own login"; routing candidates differ (see Section 7.4) |
| 3 | W02 J3 item 2 says GitHub rate-limit numbers "were not researched here: [UNVERIFIED]", while W02 K and W01 §4, §14.2 give the official limits (5,000 REST requests or GraphQL points per hour per user) | W01 §4, §14.2 and W02 K [EXTERNAL-VERIFIED] are stronger; the J3 remark is superseded |
| 4 | `claude -p` and slash commands: the current official page says custom commands and skills expand in `-p`; an old third-party mirror says they are interactive-only | Official page (W02 C1) is stronger; the mirror is a stale third-party doc |
| 5 | Project CLAUDE.md calls the fork private; live check shows PUBLIC | Live check (R03 §3.3) |
| 6 | `docs/designs/sc-issue-launch-level-hook.md:23` states `launch-level-guard.sh` as enforcing; the file does not exist | Code (R03 §1.2): B-CTX gates only a later `--pipeline` extension, not a claim-only watcher |

### 6.1 Option A: Workspace-side poller (pull). Decided by the owner (ADDENDUM 2)

**Description.** A scheduled job in each Coder workspace polls GitHub every 5 minutes with the workspace's own `gh` login, filters, then starts a local top-level Claude session through `orca agent launch` with the single-line prompt `/sc:issue --claim <integer>`. There is no listener, no inbound port and no address registry (NOTES ADDENDUM 2).

**How it works.**

| Step | What happens | Evidence |
|---|---|---|
| 1 | The Coder template runs the poller as a `coder_script` with `cron = "0 */5 * * * *"` (six fields, seconds first; the provider's own example is a five-minute job). The poller is a plain process outside any Claude session and should hold a lock (`flock`) so a slow run cannot overlap the next | W02 A1 [EXTERNAL-VERIFIED]; lock is [PROPOSAL]; overlap behavior [UNVERIFIED] (W02 A1); plain-process rule R01 §7, R03 §5 |
| 2 | Each cycle it reads its own login with `gh api user -q .login` (it does not assume the Coder owner equals the `gh` login) | W02 recommendation 4 [PROPOSAL]; R01 §9 |
| 3 | It reads candidates with `gh` (read-only), requesting only `number,labels,assignees,state` (never title or body) and passing an explicit `--limit` (default is 30) and explicit `--repo IronbellyOrg/IronClaude` | R02 §3.3; W01 §7, §10 [EXTERNAL-VERIFIED] |
| 4 | It checks "human-approved" from the latest `labeled` event actor of the approval label against an approver allow-list | W01 §11; W02 G2 [EXTERNAL-VERIFIED]; allow-list is open (GAPS 14) |
| 5 | It applies the intended-owner filter and its dispatch record (GitHub assignee plus the claim marker comment as durable record; a local file as throttle) | R01 §9, §10; W02 A4, G6 [PROPOSAL] |
| 6 | It builds the prompt as `"/sc:issue --claim " + str(int(number))` from the JSON `number` field, passes it as one argv element (no shell) | R01 §13 [CODE-VERIFIED] |
| 7 | It writes the dispatch record before the launch, then runs `orca agent launch --agent claude --worktree path:<abs> --surface terminal --prompt "<prompt>"`. A lost reply is retried with `--retry-launch <operationId>`, never as a fresh launch | R01 §12 [CODE-VERIFIED] |
| 8 | The session is an ordinary top-level session (no Orca preamble, so not a worker run); the claim runs its Waves 0 to 6 and stops at `next-steps.md` | R01 §7, §3 |

```
 coder_script cron "0 */5 * * * *"  (while the workspace runs)         [W02 A1]
            |
            v
   poller (plain process, flock)  --gh api user -q .login--> own login
            |
            |-- gh read-only: trigger label, Project / Backlog (or label-only), owner filter
            |       (fields: number,labels,assignees,state; --limit explicit)
            |-- approver check: latest `labeled` event actor in allow-list       [W01 §11]
            |-- dispatch record + claim-marker comment check                      [W02 G6]
            v
   int(number) --> "/sc:issue --claim <int>"   (argv element, no shell)           [R01 §13]
            |
            v
   orca agent launch --agent claude --worktree path:<abs> --surface terminal --prompt ...
            |
            v
   ordinary top-level session --> claim Waves 0-6 --> STOP at next-steps.md        [R01 §3]
   (no inbound port, no listener, no registry; GitHub is the only network peer)
```

**Assessment**

| Criterion | Rating and justification |
|---|---|
| Effort | **M.** Repo-side deliverable: one new Click package modeled on `src/superclaude/cli/recommend/` (12 files, 1,784 lines) or, for a one-verb poller, the single-file form of `cli/init_lite.py` (359 lines); one registration block after `main.py:561`; tests under `tests/<pkg>/`; one design doc under `docs/designs/`; label setup instructions in the `refs/labels.md:22-42` format. No workflow, no `pyproject.toml` change, no `.claude/` mirror step (R02 §1, §4.1, §4.2, §6). The poller needs its own injectable `gh` and `orca` runner because no Python `gh` wrapper exists (R02 §3.2) |
| Risk | **Medium.** No new attack surface (no listener), but open facts: the leading `/sc:issue` slash command as an initial `--prompt` is not shown to execute (R01 §12; GAPS 1), the scheduler/state location in the target template is unverified (GAPS 9; W02 A4), the Project read scope is missing on the observed token (GAPS 5), and the same-login race is unresolved (GAPS 3) |
| Reuse of existing code | `origin_repo.py` shape (argv list, `check=False`, typed errors, exit-code table, stdlib only); `cli/recommend/` package layout and CliRunner registration test; PATH-stub `gh` test pattern from five files under `tests/pr_submit/`; `refs/labels.md` setup-line format; `docs/designs/sc-issue-command.md` design-doc skeleton (R02 §3.2, §3.4, §4.2, §7) |
| Files / systems affected | New: `src/superclaude/cli/<pkg>/`, `tests/<pkg>/`, `docs/designs/<name>.md`, label setup instructions. Changed: `src/superclaude/cli/main.py` (one block). Not changed: workflows, `pyproject.toml`, `.claude/` (R02 §4.2, §6). Follow-up in the Coder repo, not here: the `coder_script` cron entry (W02 A1) |
| Pros | No inbound port, no registry, no privileged Coder token (contrast Coder's `create-task-action`, which needs an organization-wide token, W02 E1); uses the identity the claim already uses (`@me`, R01 §9); state is read from GitHub so a restarted workspace recovers (W01 §14.5); cost is 12 calls per hour per call type, 0.24% of the 5,000/hour user allowance, and allowances are separate per developer login (W01 §14.2 [DERIVED]); documented in-workspace scheduler primitive (W02 A1) |
| Cons | Latency floor of the 5-minute cadence; no polling while the workspace is stopped (W02 A2, A3); each poller needs its own Project read scope (R03 §4.2); one allow-list copy per workspace (W02 J3 item 3); no central audit trail (R03 §7); no atomic exclusion across logins (W02 G1, G7); a cron or background process is not Coder "activity", so it does not keep a workspace alive (W02 A3) |

**Answers to the three issue questions (option A)**

| Question | Answer | Evidence |
|---|---|---|
| Q-a Workspace-to-GitHub-account binding | The binding is the workspace's own `gh` login: the poller reads it with `gh api user -q .login` and the claim assigns `@me` of the same login. No Coder-side mapping is needed. Residual: nothing checks that the Coder workspace owner and that login are the same person (GAPS 19), and the `gh` token file is readable by the session | R01 §9; R03 §7; W02 B3, I4 |
| Q-b What the Coder-side listener is | There is none. The poller is the whole "Coder-side" component and it only makes outbound calls (workspace agents connect outbound; no fixed inbound workspace port) | NOTES ADDENDUM 2; W02 B1 [EXTERNAL-VERIFIED] |
| Q-c Workspace stopped | Nothing polls while the workspace is stopped, because the agent and its cron scripts stop with it; issues approved meanwhile wait on GitHub and are picked up after the next start, since the state lives on GitHub. Whether the cron scheduling resumes after start is an inference from two documented facts | W02 A2 (inference [PROPOSAL]); W01 §14.5 |

**Launch-route variant (not scored separately).** W02 C1 to C3 record that `claude -p "/sc:issue --claim <int>"` with `--allowedTools`, `--max-turns` and `--max-budget-usd` (without `--bare`, which skips custom commands and hooks) is documented to be possible, and is a bounded, exit-coded alternative with no visible interactive session. It changes only the launch step, not selection, binding, listener or at-most-once, so it does not change any score below. The owner decided the Orca route; the headless route stays a documented alternative. Whether `/sc:issue --claim` completes under `-p` is untested (R01 §12, Plain headless row; GAPS 8).

### 6.2 Option B: GitHub Action plus workspace listener (push). Documented alternative

**Description.** A GitHub Actions workflow (on a `schedule` and/or an `issues` event) selects eligible issues and calls an authenticated endpoint on the owner's workspace. A listener in that workspace hands the request to the project's orchestrator to start a new session. The listener, its registration and its transport are the scope of IronbellyOrg/Coder#477 and live in the Coder repo, not in IronClaude. This repo's part would be the selector/sender side and the contract it needs from the listener (NOTES ADDENDUM point 2). This option is not the owner's choice; it is documented as an alternative and for its revisit conditions.

**How it works** (the sender contract is a [PROPOSAL] in W02 J1 to J2; the platform facts are [EXTERNAL-VERIFIED]).

| Step | What happens | Evidence |
|---|---|---|
| 1 | A workflow runs on `schedule` (shortest interval 5 minutes; may be delayed; queued runs may be dropped; default branch only; auto-disabled after 60 days without activity in a public repo) or on `issues` activity such as `labeled` | W01 §1, §2 |
| 2 | It reads the org Project with a PAT or GitHub App token, because the repository `GITHUB_TOKEN` has no Projects permission and cannot read an organization Project | W01 §9 (explicit "cannot" sentence only from the secondary gh-aw docs) |
| 3 | No workflow trigger reacts to a Project Status change, so Backlog status has to be read by polling inside the scheduled run | W01 §2, §3 [EXTERNAL-VERIFIED by absence] |
| 4 | It checks the approver (latest `labeled` actor against one allow-list) and resolves the target workspace (GitHub login to Coder user to workspace) | W01 §11; W02 I4 [PROPOSAL; each link documented, the chain is not documented as a feature] |
| 5 | It sends a request with only fixed, validated fields (`repository`, integer `issue_number`, `approval_event_id`, `requested_at`, `request_id`), an `Idempotency-Key` derived from `repository|issue_number|approval_event_id`, and a signature or OIDC token | W02 J1 [PROPOSAL]; no title, body or comment text |
| 6 | The request reaches the workspace only through the Coder control plane (a `coder_app` with `share = "owner"`, or `coder ssh` / `coder port-forward`), authenticated with a Coder token | W02 B1, B2, I1, I2 |
| 7 | The listener (Coder#477) validates, then starts the claim through `orca agent launch ... "/sc:issue --claim <int>"` from a plain process (never a worker Task) | NOTES point 2; WORKER-CONTRACT.md:23, :61 (R01 §7) |

```
 GitHub Actions: schedule (>= 5 min, may drop) / issues:labeled         [W01 §1, §2]
        |  org Project read needs PAT or App token, not GITHUB_TOKEN     [W01 §9]
        v
   select: trigger label + approver actor + Project Backlog + owner
        |  route: GitHub login -> Coder user -> workspace                [W02 I4]
        v
   HTTPS POST {repository, issue_number(int), approval_event_id, request_id}
        |  Coder-Session-Token + HMAC / GitHub OIDC; Idempotency-Key     [W02 H, J1]
        v
   Coder control plane / app proxy  (coder_app share="owner")            [W02 I1, I2]
        v
   workspace listener  (IronbellyOrg/Coder#477, Coder repo)
        v
   orca agent launch ... "/sc:issue --claim <int>"  -> claim Waves 0-6 -> STOP
```

**Assessment**

| Criterion | Rating and justification |
|---|---|
| Effort | **L** in this repo, plus the Coder#477 work, which no research file sizes (Coder#477 states interface, registration mechanism, credentials, topology and audit implementation are "not known yet", NOTES point 2). In this repo: the first `schedule:`/`issues:` workflow (none exists; R02 §1), its entry in `.github/workflows/README.md` ("Adding a New Workflow"), a secret for Project read, the sender contract and the poller-equivalent selection logic with the same label and allow-list setup as option A |
| Risk | **High.** New inbound surface through the Coder control plane; a privileged or per-owner Coder token held outside the workspace (Coder's `create-task-action` needs organization-wide user-read and authority to launch tasks for other users, W02 E1); scheduled runs can be dropped (W01 §1); the sender-to-workspace path has unverified pieces: mTLS through Coder (W02 H3) and the `Coder-Session-Token` header for non-browser app callers, seen only in Go package docs (W02 I2) |
| Reuse of existing code | Workflow skeleton and conventions (`actions/checkout@v4`, `astral-sh/setup-uv@v10.3.2`, Python 3.10, least-privilege `permissions`, `persist-credentials: false`) from `.github/workflows/test.yml` (R02 §1); prior art for GitHub-user-to-Coder-user mapping in `coder/create-task-action` (W02 E1); GitHub OIDC claims (`repository`, `ref`, `job_workflow_ref`, `actor`) for sender authentication (W02 H2). No existing listener code in IronClaude |
| Files / systems affected | This repo: new `.github/workflows/<name>.yml`, `.github/workflows/README.md`, secrets, selection/sender code. Coder repo (not here): `templates/VSCode-AIDev02/{main.tf,Dockerfile.coder,startup.tf,scripts/startup.sh,catalogue/orca/module.tf,catalogue/orca-pair.sh,orca/runtime.mjs}` as named by Coder#477 (NOTES point 2) |
| Pros | One org-level credential with Projects read, so no per-developer `read:project` scope (W01 §14.5, §9); one copy of the approver allow-list and one decision point for audit and dedupe (W02 J3 items 3, 4); GitHub OIDC needs no shared secret (W02 H2); can wake a stopped workspace through `coder ssh`, which auto-starts it unless `--disable-autostart` (W02 B2) at the price of a privileged token |
| Cons | Needs the listener, registration and transport of Coder#477 (unbuilt); first schedule workflow in the repo; the `issues` event cannot see Project Status changes (W01 §2); an Action runs on a GitHub runner and cannot itself start a local Orca session (W02 D1); public-repo schedules are auto-disabled after 60 days of inactivity (W01 §1); a privileged Coder token or one token per owner must be stored in GitHub secrets (W02 E1, I2) |

**Answers to the three issue questions (option B)**

| Question | Answer | Evidence |
|---|---|---|
| Q-a Binding | A push design must map the GitHub login to the Coder user (the OAuth link that `create-task-action` uses), then to that user's workspace, with `coder_app share = "owner"` so only the owner's token reaches it. Every link is documented individually; the end-to-end chain is not documented as a feature. That the Coder workspace owner always equals the workspace's `gh` login is not established | W02 B3, E1, I1, I4 |
| Q-b Listener | A process in every workspace, registered with the "monitor", that receives authorized requests and hands them to the project's orchestrator to start a new session; exposed through `coder_app` or `coder ssh` / `port-forward`. This is IronbellyOrg/Coder#477 (Coder repo). Its interface is not known yet | NOTES point 2; W02 I1, B2 |
| Q-c Workspace stopped | Nothing listens, so the request is undeliverable; the sender must treat "unreachable" as "not delivered, retry later" (an idempotent retry is safe) and may start the workspace via `coder ssh` auto-start (which endpoint to use for a build start is [UNVERIFIED]). For the webhook variant GitHub does not automatically redeliver failed deliveries | W02 J2 table, B2; W01 §12 |

### 6.3 Option C: Central microservice plus listener (push). Documented alternative

**Description.** A central microservice, run on a host outside the workspaces, receives GitHub events (organization webhooks) or polls, selects issues, resolves the target developer's workspace and calls the same kind of workspace listener as option B (Coder#477, Coder repo). It is not the owner's choice; it is documented as an alternative and for its revisit conditions. Research on C is thinner than on A and B: no research file establishes where such a service would be hosted or operated [UNVERIFIED, open].

**How it works.**

| Step | What happens | Evidence |
|---|---|---|
| 1 | A GitHub App with the organization "Projects" read permission receives `projects_v2_item` webhooks (organization availability; `edited` carries a `changes` object for single-select values such as Status) and `issues` webhooks (labeled) | W01 §3, §2, §9 [EXTERNAL-VERIFIED] |
| 2 | The service must expose an HTTPS endpoint reachable by GitHub, verify `X-Hub-Signature-256` (HMAC-SHA-256, constant-time compare), answer 2XX within 10 seconds and deduplicate on `X-GitHub-Delivery` | W01 §12 [EXTERNAL-VERIFIED] |
| 3 | It checks the approver, applies the intended-owner routing and calls the workspace listener exactly as in option B (steps 4 to 7 of 6.2), with the same integer-only contract | W02 J1, J2 [PROPOSAL] |
| 4 | Because GitHub does not automatically redeliver failed deliveries, missed events after downtime need a manual or scripted redelivery request | W01 §12 [EXTERNAL-VERIFIED] |

```
 GitHub org webhooks: projects_v2_item (Status changes), issues:labeled     [W01 §3, §2]
        |  X-Hub-Signature-256 HMAC, X-GitHub-Delivery (dedupe key)          [W01 §12]
        v
   central microservice (host not established)  + GitHub App (Projects read) [W01 §9]
        |  approver check -> route (login -> Coder user -> workspace)        [W02 I4]
        v
   same authenticated request as option B:  {repository, issue_number(int), approval_event_id, request_id}
        v
   Coder control plane -> workspace listener (Coder#477) -> orca agent launch -> claim -> STOP
```

**Assessment**

| Criterion | Rating and justification |
|---|---|
| Effort | **XL.** A new service to build, host and operate (hosting not established), a GitHub App, the webhook receiver, the routing table, and the Coder#477 listener (unsized). No existing service code, workflow or listener in IronClaude (R02 §1; W02 header scope note) |
| Risk | **High.** Inbound endpoint exposed to GitHub plus the workspace-side inbound path; privileged App and Coder credentials; webhook ordering and redelivery window are unverified (W01 §12); no prior code in the repo |
| Reuse of existing code | Coder's `create-task-action` user-mapping pattern (W02 E1); Coder Agents Chats API with a scoped automation key as a recorded alternative runtime, not the Orca-plus-Claude route (W02 E2); webhook signature and delivery-id facts (W01 §12); claim idempotence on the workspace side (R01 §10) |
| Files / systems affected | A new service repo or directory (location not decided in any research file); GitHub App and org webhook configuration; Coder repo files of Coder#477; label and allow-list setup as in option A |
| Pros | The only option that reacts to a Project Status change at event time and sees change history (`projects_v2_item` `changes`; W01 §3, §14.5); push latency (GitHub recommends webhooks over polling, W01 §5); one decision point for approver policy, audit and dedupe (W02 J3 items 3, 4); an App installation token has its own 5,000/hour base allowance, independent of developer tokens (W01 §4) |
| Cons | Everything B needs from Coder, plus a service to run; GitHub-reachable inbound endpoint; no automatic redelivery of missed webhooks, so a stopped workspace or downed service loses events unless redelivery is scripted (W01 §12); delivery ordering not documented (W01 §12 [UNVERIFIED]); OIDC does not fit a non-Action sender, so HMAC or Coder tokens are the sender-authentication choices (W02 H2, H5) |

**Answers to the three issue questions (option C)**

| Question | Answer | Evidence |
|---|---|---|
| Q-a Binding | As option B: a central mapping (GitHub login to Coder user to workspace) held by the service or resolved through Coder's OAuth link, with `coder_app share = "owner"` on the workspace side. Not documented end to end | W02 E1, I1, I4 |
| Q-b Listener | The same Coder#477 listener, registered with the central "monitor" (the service), plus the service's own inbound webhook endpoint | NOTES point 2; W01 §12 |
| Q-c Workspace stopped | As option B (unreachable means not delivered; wake via `coder ssh` auto-start is possible with a privileged token), and webhook deliveries missed while the service or workspace is down are not redelivered automatically | W02 B2, J2; W01 §12 |

### 6.4 Option D: Hybrid label relay (Action writes "ready", workspaces poll)

**Description.** A GitHub Action or small scheduled job only evaluates the central conditions and writes a "ready" label or a Project field change; each workspace polls for that marker exactly as in option A, so no workspace address is ever needed (NOTES SOLUTION_RESEARCH item 4). The research supports it as the answer to one condition: a workspace `gh` token that cannot read the org Project while a central token can (W01 §14.5; GAPS 5). With label-only selection the workspace needs no Project read (W01 §14.3 fallback; R02 Gaps 9).

**How it works.**

| Step | What happens | Evidence |
|---|---|---|
| 1 | A scheduled Action with a PAT or App secret (not `GITHUB_TOKEN`) runs one Project items query with a server-side filter for Backlog and the trigger label, then checks the approver allow-list | W01 §9, §8, §11 |
| 2 | For each issue that passes it writes a "ready" label (or Project field change) | NOTES SOLUTION_RESEARCH item 4 |
| 3 | Each workspace poller selects on the "ready" marker plus its intended-owner filter and runs steps 5 to 8 of option A | 6.1 |

```
 scheduled Action (PAT/App secret)                                    [W01 §1, §9]
   Project query: Backlog + trigger label + approver check
        |  writes "ready" label / Project field                       [NOTES]
        v
   GitHub (the only shared state)
        ^
        |  gh read-only, label-only selection (no Project scope)      [W01 §14.3]
   workspace poller (as option A) -> orca agent launch -> claim -> STOP
```

**Assessment**

| Criterion | Rating and justification |
|---|---|
| Effort | **L.** Option A's poller in full, plus the first scheduled workflow (R02 §1), a PAT or App secret, a new label and its README entry. The Action adds work and removes none of the poller |
| Risk | **Medium.** No inbound surface. Scheduled runs are best effort and can be dropped (W01 §1); two moving parts; the "ready" label can itself be applied by any Triage-or-higher account (R03 §4.2), so the workspace must still check who applied it [DERIVED] |
| Reuse of existing code | Everything reused by option A, plus the workflow skeleton of `.github/workflows/test.yml` (R02 §1) |
| Files / systems affected | Option A's files plus `.github/workflows/<name>.yml`, `.github/workflows/README.md`, one more label, one secret |
| Pros | Workspaces need no `read:project` scope (label-only selection); central evaluation of Project, Backlog and approver; no workspace address, listener or registry; state stays on GitHub so stopped workspaces lose nothing |
| Cons | Still needs a poller in every workspace; adds a best-effort central step; does not provide atomic exclusion (workspaces poll independently); when the workspace token can already read the Project, D adds a component without removing a requirement, so it collapses to A |

**Answers to the three issue questions (option D)**

| Question | Answer | Evidence |
|---|---|---|
| Q-a Binding | As option A: the workspace's own `gh` login, no Coder-side mapping | R01 §9; R03 §7 |
| Q-b Listener | None; the Action never calls a workspace | NOTES SOLUTION_RESEARCH item 4 |
| Q-c Workspace stopped | As option A: no polling while stopped; the "ready" marker stays on GitHub and is picked up after the next start | W02 A2; W01 §14.5 |

**Further hybrids considered and not scored.** (1) The headless `claude -p` launch is a launch-route variant of A (see 6.1), not a selection architecture. (2) A "wake a stopped workspace" hybrid is only mentioned as a benefit of B or C (`coder ssh` auto-start, W02 J3 item 1); no research file evaluates it as a separate design, so it is excluded from scoring and listed under Carried to Open Questions.

### Requirement Scoring

**Scoring convention (one rule for all four options and all ten requirements).** Levels are Meets / Partly / Does not meet. They rate each design on what exists today; none of the four is built. **Meets** only when the requirement is satisfied by something that exists today, or by the option's own described in-repo mechanism (code, tests, workflow file, design doc, label-setup lines), with no dependency on anything unbuilt outside this repo (the Coder#477 listener and registry, a GitHub App, a hosted service, a new organization secret or token-scope grant) and with no [UNVERIFIED] fact or open rule in the cell. Otherwise **Partly**. **Does not meet** only when the option's own mechanism cannot satisfy the requirement. A Partly cell stays Partly even when one setup step or one live check would close it; "Reading the scores" lists those steps for every option alike. No cell is credited for a "design level" mechanism that depends on an unbuilt component (Coder#477's interface is "not known yet", NOTES point 2). The owner decided option A; this table reports the scores as the rule gives them, including where A scores equal to or below another option, because it is what the owner can revisit.

| Requirement | A: workspace poller (decided) | B: Action + listener | C: microservice + listener | D: label relay hybrid |
|---|---|---|---|---|
| R1 Tagged | **Meets.** Select by trigger label with `gh issue list --label`; the label does not exist yet (fork has 9 default labels), so one-time `gh label create` instructions are needed (R01 §9; R02 §2) | **Meets.** `issues: labeled` is a documented activity type (W01 §2); same label setup (R02 §2) | **Partly.** The `issues` webhook event with `labeled` is documented (W01 §2, §12), but receiving it needs the central service and its public webhook endpoint, which are unbuilt with hosting not established (6.3; W01 §12); same label setup | **Meets.** The Action selects on the label; workspaces see the "ready" marker (NOTES SOLUTION_RESEARCH item 4; W01 §14.3) |
| R2 Human-approved | **Partly.** Derived from the latest `labeled` event actor against an allow-list (W01 §11; W02 G2), but no allow-list exists, its location is open (GAPS 14), and every poller holds its own copy (W02 J3 item 3) | **Partly.** One workflow could hold a single allow-list; the write-access gate of `claude-code-action` is an analogue, not a mechanism of this option (W02 D2, J3 item 3). No allow-list exists and its location and rule are open (GAPS 14) | **Partly.** One service could hold a single allow-list (W02 J3 item 3), but the service is unbuilt and the allow-list location and rule are open (GAPS 14) | **Partly.** The Action checks centrally, but the "ready" label is appliable by any Triage-or-higher account (R03 §4.2), so each workspace must still check its actor [DERIVED] |
| R3 In a GitHub Project | **Partly.** Needs `read:project` on every polling login; the observed token lacks it and `gh project list` failed (R03 §4.2; W01 §7); the label-only fallback drops this check (W01 §14.3) | **Partly.** Needs one PAT or App secret with org Projects read, which does not exist; `GITHUB_TOKEN` cannot read an org Project (W01 §9); organization token policies are [UNVERIFIED] (W01 Gaps 7) | **Partly.** Needs a GitHub App with org "Projects" read (user and installation tokens) (W01 §9) and `projects_v2_item` webhooks (W01 §3); the App and the service are unbuilt; organization policies are [UNVERIFIED] (W01 Gaps 7) | **Partly.** The central token reads the Project and workspaces use label-only selection (W01 §14.3, §9), but the central PAT or App secret does not exist and organization token policies are [UNVERIFIED] (W01 Gaps 7) |
| R4 Status is Backlog | **Partly.** `status:Backlog` is documented for UI filtering; acceptance by `gh project item-list --query` or the REST `q` parameter is [UNVERIFIED] (W01 §8, §13, gap 3); issue search has no Status qualifier (W01 §10); the claim leaves the item in Backlog, so an own dedupe record is needed (R01 §3) | **Partly.** Same unverified server-side filter; no workflow trigger reacts to a Status change, so the scheduled run must poll (W01 §2, §3, §8) | **Partly.** `projects_v2_item` `edited` carries the changed single-select value and field id and change history is visible (W01 §3, §14.5), but it is an organization webhook event, so reading it needs the unbuilt App and service (W01 §3, §9) | **Partly.** Same unverified filter inside the Action (W01 §8); the claim still leaves Backlog unchanged (R01 §3) |
| R5 Intended owner (A: poller decides an issue is meant for its own `gh` login; B/C/D: routing step) | **Partly.** Four candidates: assigned to own login (fits claim semantics, no new label), per-person label, Project field, first-come; the choice is not settled by any file; first-come races; the same-login multi-workspace case is not solved (R01 §9; R02 §2c; W01 §14.4; GAPS 3, 15) | **Partly.** A central routing step removes the cross-workspace race (W02 J3 item 4) but needs a GitHub login to Coder user to workspace mapping that is documented per link only (W02 I4, E1) and a registration mechanism that is "not known yet" (NOTES point 2) | **Partly.** Same as B: one decision point, same unbuilt mapping and registry (W02 I4, J3 item 4) | **Partly.** Same four candidates as A for the workspace filter; the Action could add a per-person label [DERIVED]; same-login case unsolved (W01 §14.4) |
| R6 Session starts in the right workspace | **Partly.** Right workspace by construction (own checkout and login); needs a running Orca runtime and an existing worktree, and execution of a leading `/sc:issue` given as `--prompt` is unverified (R01 §12; GAPS 1, 4) | **Partly.** Needs the Coder#477 listener to deliver; the end-to-end chain is not documented as a feature (W02 I4); the same launch step and the same unverified slash-command execution (R01 §12) | **Partly.** Same as B | **Partly.** Same as A (R01 §12; GAPS 1, 4) |
| R7 Workspace bound to one GitHub account | **Partly.** The binding is the workspace's own `gh` login and the claim assigns `@me` (R01 §9; R03 §7); nothing verifies the Coder owner equals that login (GAPS 19; W02 B3); the token file is readable by the session (R03 §2.3) | **Partly.** Chain of documented links (OAuth link, `share = "owner"`) not documented end to end (W02 I4); privileged Coder token stored outside the workspace (W02 E1) | **Partly.** Same as B (W02 I4, E1) | **Partly.** Same as A (R01 §9; GAPS 19) |
| R8 Senders authenticated and authorized; no unauthenticated port | **Meets.** There is no listener, no sender and no inbound port to protect; workspace agents connect outbound (NOTES ADDENDUM 2; W02 B1) | **Partly.** Mechanisms exist (Coder token with `share = "owner"`, HMAC with timestamp, GitHub OIDC; W02 H1, H2, H4, I1) but the listener is unbuilt; mTLS through Coder and the app-proxy token header for non-browser callers are [UNVERIFIED] (W02 H3, I2) | **Partly.** Same mechanisms except OIDC, which fits an Action sender and not a microservice (W02 H2, H5); listener unbuilt | **Meets.** No listener or inbound port; the Action only writes to GitHub (NOTES SOLUTION_RESEARCH item 4) |
| R9 Audit trail of routing and access decisions | **Partly.** GitHub keeps events with actor and time for labels, assignment and Project changes, and the claim posts marker comments; no record of the poller's own decision and no central trail unless each poller writes one (R03 §7) | **Partly.** A central workflow run would record the sender side, but the audit fields in W02 J2 [PROPOSAL] sit in the listener-side log, and the listener (Coder#477, which asks for this trail) is unbuilt | **Partly.** A single service is the natural audit point (W02 J2, J3 item 3), but it is unbuilt and its hosting is not established | **Partly.** The Action run records the "ready" decision [DERIVED]; routing and dispatch records are per workspace as in A (R03 §7) |
| R10 Exactly one session per issue | **Partly.** No atomic exclusion across logins: assignment is additive with no compare-and-set (W02 G1, G7); best effort only (assignee, claim marker, local record, pre-launch re-read); same-login case and claim Wave 1 to 3 window remain (R01 §9, §10; GAPS 15) | **Partly.** One sender decision plus a durable idempotency key `(repository, issue, approval event id)` would be stored at the receiver (W02 G3, G7, J1), but the receiver is the unbuilt Coder#477 listener; Actions `concurrency` alone is not exactly-once (W02 G5) | **Partly.** A single decision point "would fix" duplicate claims (W02 J3 item 4; G7), but the service and the receiving listener are unbuilt | **Partly.** Workspaces still poll independently; the central label gives no exclusion (W02 G7) |

**Tally (a count, not a weighted score).**

| Option | Meets | Partly | Does not meet |
|---|---|---|---|
| A | 2 (R1, R8) | 8 | 0 |
| B | 1 (R1) | 9 | 0 |
| C | 0 | 10 | 0 |
| D | 2 (R1, R8) | 8 | 0 |

The tally counts what each option satisfies today under the one scoring rule above. It does not weigh the requirements and it is not a measure of design quality: B and C score low here because their cells depend on unbuilt components outside this repo, not because their designs fail the requirements.

**Reading the scores honestly.**

- By count under the one rule, A and D have 2 Meets (R1, R8), B has 1 (R1) and C has 0. The count does not show three properties in which B and C are structurally stronger than A if their unbuilt component is built: R2 (one allow-list copy instead of one per workspace), R9 (a central audit trail) and R10 (a single decision point, so a durable idempotency key). A cannot close those three by setup, because it has no central component (W02 J3 items 3 and 4); they are revisit conditions 3 and 4, not scored credit.
- Several Partly cells are closable by setup or a live check rather than by a design change, and the same holds for every option that has the cell. For A: R3 and R4 (one `gh auth refresh -s read:project` per developer, command form from W01 §13, plus one owner-run live call to confirm the `--query` filter), R5 (the owner picks one routing candidate), R6 (one owner-run live launch test, R01 §12). For B, C and D: R3 (a new PAT or App secret or a GitHub App with Projects read, and the organization policies of W01 Gaps 7) and R4 (the same live filter call, or the unbuilt App and service for C). R7 depends on a Coder-side fact (GAPS 19) for all options. Under the one rule each of these stays Partly until its step is done.
- B's and C's Partly cells on R6, R7 and R8 are not closable inside this repo: they depend on Coder#477, which lives in the Coder repo and is unsized.
- R8 is the one requirement where A and D score highest: they remove the surface (no listener, no inbound port) instead of securing it.
- No option scores Does not meet on any requirement, and no option settles R5 (the choice of routing rule is open).

### Options Comparison

| Criterion | A: workspace poller (decided) | B: Action + listener | C: microservice + listener | D: label relay hybrid |
|---|---|---|---|---|
| Effort | M: one CLI package, tests, design doc, label instructions; no workflow (R02 §4, §6) | L here plus unsized Coder#477 work (R02 §1; NOTES point 2) | XL: new service to host plus App plus Coder#477 (R02 §1; W01 §12) | L: A in full plus first scheduled workflow and a secret (R02 §1; W01 §9) |
| Risk | Medium: no new surface; open launch, scheduler, scope and race facts (R01 §12; GAPS 1, 3, 5, 9) | High: inbound path, privileged tokens, dropped runs (W02 E1, I2; W01 §1) | High: inbound endpoint, privileged tokens, webhook redelivery gaps (W01 §12) | Medium: no inbound surface; best-effort central step (W01 §1) |
| Maintainability | One small package in this repo; template wiring later in the Coder repo; allow-list copy per workspace (R02 §4.2; W02 A1, J3 item 3) | Workflow here, listener and registry in the Coder repo, secrets to rotate: two repos to keep in step (NOTES point 2) | A service to operate plus the listener: highest ongoing cost; hosting not established | Two moving parts (workflow and poller) |
| Integration complexity | Low: plain process plus `gh` plus `orca agent launch` (R01 §12) | High: workflow, secret, Coder token, app proxy, listener, registration (W02 B, I) | Highest: all of B plus webhook receiver and App (W01 §12) | Medium: A plus a workflow and a label |
| Reuse potential | High: `origin_repo.py` shape, `cli/recommend/`, PATH-stub tests, label-instruction format (R02 §3.2, §3.4, §4.2) | Medium: workflow skeleton, `create-task-action` prior art, OIDC pattern; no listener code (R02 §1; W02 E1, H2) | Low to medium: `create-task-action` mapping pattern, webhook facts; no service code (W02 E1; W01 §12) | High: everything from A plus workflow skeleton (R02 §1) |
| Security posture: account binding | Workspace's own `gh` login equals the claim's `@me`; owner-equals-login unchecked (R01 §9; GAPS 19) | Needs GitHub-to-Coder-user-to-workspace chain; privileged Coder token outside the workspace (W02 I4, E1) | Same as B | As A |
| Security posture: untrusted input | Integer-only prompt built with `int()`; claim still reads issue text; policy open (R01 §13; R03 §3.2; GAPS 13) | Same: fixed-field request, no title or body (W02 J1); claim still reads issue text | Same as B | As A |
| Inbound exposure (one scored criterion, not a pre-filter) | None: no listener, no inbound port (NOTES ADDENDUM 2; W02 B1) | Listener reachable through the Coder control plane; `share` must not be `public` (W02 I1, I2) | Webhook endpoint reachable by GitHub plus the workspace listener (W01 §12; W02 I1) | None (NOTES SOLUTION_RESEARCH item 4) |
| At-most-once | Best effort: assignee, claim marker, local record, pre-launch re-read; no atomic exclusion (W02 G1, G7; R01 §10) | Idempotency key at the receiver plus one sender decision, once the unbuilt Coder#477 listener exists (W02 G3, J1) | Single decision point, once the unbuilt service exists (W02 J3 item 4) | As A: independent pollers (W02 G7) |
| Fit with never-as-worker and claim-stops-after-next-steps | Fits: ordinary top-level session via `orca agent launch`, claim-only, stops at `next-steps.md` (WORKER-CONTRACT.md:11, :23, :61; R01 §7) | Fits only if the listener ends in `orca agent launch` from a plain process; "hand to the orchestrator" must not mean a worker Task, which `/sc:issue` may never be (WORKER-CONTRACT.md:23) [DERIVED] | Same as B | Fits as A |
| Latency | 5-minute floor by decision | Schedule: 5-minute floor, delay and drops possible (W01 §1); `issues` events are immediate for labels (W01 §2) | Event time (webhook) (W01 §3, §5) | 5-minute floor on both steps (W01 §1) |
| Behavior with a stopped workspace | No polling; issues wait on GitHub (W02 A2) | Undeliverable; wake via `coder ssh` possible with privileged token (W02 B2, J2) | Same as B; missed webhooks not redelivered automatically (W01 §12) | As A |

### Revisit conditions for options B and C

The owner decided option A. The decision would be revisited if one of these conditions is shown to hold. Each is taken from the research files; none has been observed today.

| # | Condition | Option it would favor | Evidence or source |
|---|---|---|---|
| 1 | Workspaces are mostly stopped, so approved issues wait too long for a poll, and the owner wants a design that can start a stopped workspace | B or C (wake through the Coder control plane with `coder ssh` auto-start, at the price of a privileged token). Note the counter-fact: a push design does not recover missed webhooks by itself | W02 J3 item 1, B2; W01 §12, §14.5 |
| 2 | Poll latency or GitHub API use becomes a problem: many workspaces share one login, or a very large unfiltered Project is read, or only GraphQL polling is possible | B or C (push, or one central selector) | W02 J3 item 2; W01 §14.2 (exhaustion is "not a realistic trigger" at normal sizes: 12 polls per hour is about 0.24% of 5,000) |
| 3 | A requirement for central audit and one approver policy across developers that per-workspace pollers cannot enforce consistently | B or C | W02 J3 item 3; R03 §7 (no central trail under A) |
| 4 | Double claims by the same login in several workspaces, or by two logins, occur in practice despite the best-effort checks | B or C (a single decision point plus a durable idempotency key) | W02 J3 item 4, G1, G7; W01 §14.5; R01 §9 |
| 5 | Coder (or the Coder repo) ships the workspace-to-account binding as a platform feature, making a push design cheap | B or C | W02 J3 item 5, E1 |
| 6 | The workspace `gh` token cannot read the org Project (for example an organization policy blocks classic tokens, requires approval of fine-grained tokens or SSO authorization, or developers decline `read:project`), while a central credential can | D first (central Project read, workspaces label-only); B or C if a GitHub App with org Projects read is preferred | W01 §14.5, §9; W02 J3 item 6; R03 §4.2; GAPS 5. The organization policies themselves are [UNVERIFIED] (W01 Gaps 7) |
| 7 | A requirement to react to a Project Status change at event time, or to see who moved an issue to Backlog and when | C (`projects_v2_item` webhook with `changes`) | W01 §3, §14.5; GitHub recommends webhooks over polling (W01 §5) |
| 8 | A need for a shared at-most-once ledger across logins or workspaces | B or C | W01 §14.5 |
| 9 | Workspaces cannot run a recurring poller (the `coder_script` cron primitive is not usable in the target template, or state cannot persist) | Not settled by the research: no file evaluates an alternative host for the poller. The only supported inference is that a central selector (B, C, or a central poller) would be considered | W02 A1, A4, A5 (systemd and system cron availability [UNVERIFIED]); GAPS 9. The cron primitive is documented, so this condition is not expected [DERIVED] |

If none of these holds, option A stays and Coder#477 is unnecessary (W02 J3 closing line; NOTES ADDENDUM 2).

---

## 7. Recommendation

### 7.1 Recommendation

**Option A, the workspace-side poller, decided by the owner (ADDENDUM 2).** Each workspace polls GitHub every 5 minutes with its own `gh` login and starts the claim with `orca agent launch`; there is no listener, no inbound port and no address registry. Scope is claim-only (Q2) and only a validated integer issue number reaches the session prompt (Q3). The implementation plan targets A.

The repo-side deliverable named by the owner (NOTES ADDENDUM 2): a design doc, a tested poller script or CLI (mock `gh` and mock `orca agent launch`; nothing run live), and trigger/approval label setup instructions. Options B and C, and any live deployment, are recorded as follow-up.

### 7.2 Rationale

This section refers to the Requirement Scoring and Options Comparison tables above and states the trade-offs, including where A scores lower.

| Point | What the evidence says | Source |
|---|---|---|
| What favors A | It is the only option other than D with no inbound exposure and R8 = Meets; it needs no listener, no registry and no privileged Coder token; it has the lowest Effort (M) and Integration complexity among the options that start a session; it uses the identity the claim already uses; it has high Reuse (shared with D); its polling cost is 0.24% of the user allowance per call type | Requirement Scoring R8; Options Comparison; R01 §9; W01 §14.2 [DERIVED]; W02 A1, E1 |
| Where B and C are structurally stronger than A | The scoring rule counts only what exists today, so these do not show in the Tally: R2 (one allow-list copy per workspace under A), R9 (no central audit trail) and R10 (no single decision point; no atomic exclusion) are structurally lower under A and stay Partly by design. Latency has a 5-minute floor, and there is no polling while the workspace is stopped | Requirement Scoring R2, R9, R10; W02 J3 items 3, 4; W02 A2, A3 |
| Where A is Partly but closable | R3 and R4 (grant `read:project` per developer and confirm the server-side filter in one live call), R5 (choose one routing candidate), R6 (one live launch test). B, C and D carry the equivalent Partly cells on R3 and R4 (a new secret or App grant, the same filter call) under the same rule | W01 §13, §8; R01 §12; GAPS 1, 5 |
| Where B and C are Partly and not closable here | R6, R7, R8 depend on the Coder#477 listener, which lives in the Coder repo and is unsized | NOTES point 2; W02 I4 |
| Why not D now | D adds a workflow, a secret and a label and keeps A's poller in every workspace; it pays off only when workspace tokens cannot read the org Project. It is the first fallback in the revisit conditions (condition 6) | W01 §14.3, §14.5; Revisit table |
| What the score does and does not say | Under the one rule, A and D count 2 Meets, B 1 and C 0 (see Tally). The count rates only what exists today, so it does not credit B or C for the central allow-list, audit trail and decision point that an unbuilt component would give (revisit conditions 3 and 4), and it does not credit A for setup steps not yet done. The owner's decision rests on removing the listener, inbound port and registry, which the R8, Effort, Risk and Integration rows reflect. The scoring is reported as it is so that the owner can revisit it | Requirement Scoring Tally; NOTES ADDENDUM 2 |

### 7.3 Claim-only scope and the security model

**Claim-only (Q2).** The watcher's job ends at starting `/sc:issue --claim <N>`; the pipeline after the claim stays manual. This matches what the code can do: `/sc:issue --claim` stops by design (B2) at `next-steps.md` and never runs a next-step command, and `--claim --pipeline <level>` is design only (no `--pipeline` in `issue.md`; `launch-level-guard.sh` absent; B-CTX open, which gates only that later extension) (R01 §3, §11; R03 §1.2, §1.3) [CODE-VERIFIED]. The issue text's expectation that the claim kicks off the full pipeline is [CODE-CONTRADICTED] (GAPS 20).

**Security model for option A.**

| Control | Rule | Source |
|---|---|---|
| Identity | Each workspace uses its own `gh` login; no listener, no inbound port, no address registry. The poller reads its login with `gh api user -q .login` each cycle and does not assume the Coder owner equals it | NOTES ADDENDUM 2; W02 recommendation 4 [PROPOSAL]; R01 §9 |
| Prompt (Q3) | Only an integer reaches the session prompt: the poller builds `"/sc:issue --claim " + str(int(number))` from the `number` field of `gh` JSON, rejects anything that is not a positive integer (sanity bound; `origin_repo.py` accepts any size), and passes it as one argv element with no shell. `origin_repo.py` validation runs inside the session after the prompt arrived, so it is a second check, not the first | R01 §5, §13 [CODE-VERIFIED]; R03 §3.1; W02 F4 [PROPOSAL pattern `^[1-9][0-9]{0,8}$`] |
| Fields read | The poller requests `number,labels,assignees,state` only, never title, body or comments, and always passes `--repo IronbellyOrg/IronClaude` (never gh's default repo) | R02 §3.3; CLAUDE.md fork rule (R02 §3.3 Convention B warning) |
| Approval | "Human-approved" is a GitHub-side act by a Triage-or-higher account (3 accounts today). The poller takes the actor of the latest `labeled` event of the approval label and compares it with an approver allow-list | R03 §4.2, §4.3; W01 §11; W02 G2 [PROPOSAL]. Allow-list location and rule are open (GAPS 14) |
| Launch | Ordinary top-level session with `orca agent launch`; the poller is a plain process, never a worker Task and never run inside a Claude session (WC-13) | WORKER-CONTRACT.md:23, :61 (R01 §7); R03 §5 |

**Honest residual risk (stated, not solved by A).** The integer-only rule protects the launch prompt, not the session: `/sc:issue --claim` itself reads the issue title, body and comments live (Waves 1 and 4) and posts worker-written files to a public issue without review, so approval does not freeze the text the claim reads (R03 §3.2, §3.3) [CODE-VERIFIED]. The repo is public, so title, body and comments are authored by the public (R03 §3.3). Nothing registered constrains a launched session: no permission rules, no hook on `gh`, `git` or file reads, `master` unprotected, the `gh` token (scopes `repo, workflow, read:org, gist`) is a readable file, and Orca's default `--dangerously-skip-permissions` removes the permission prompts that Claude's own security page names as the main protection (R03 §2.3, §6; W02 F1) [OBSERVED / EXTERNAL-VERIFIED]. The "lethal trifecta" framing applies: untrusted content, private data and external communication are all present in a workspace session (W02 F3, a practitioner blog, not a standard). The mitigating facts: the initial prompt is fixed text plus an integer; the claim ends after `next-steps.md` and never runs next-step commands; the claim refuses foreign repos, PRs, closed issues and issues assigned to someone else (R03 §6). An explicit decision on the claim's own reads of untrusted text is required and is open (GAPS 13).

### 7.4 Intended-owner filter (how each workspace takes only issues meant for its own `gh` login)

`@me` in the claim is whichever account `gh auth` holds in the session (`--add-assignee @me`), so the filter has to decide "this issue is meant for this login" before launch (R01 §9). Candidates found by the research:

| Candidate | What it reads or needs | Strengths | Weaknesses | Source |
|---|---|---|---|---|
| 1. Issue is already assigned to this login | `gh issue list --assignee "@me"` plus the trigger and approval criteria; the claim already continues on "already assigned to the current login" (`claim.md:42`) and stops on a different assignee (`claim.md:41`) | Best fit to claim semantics; no new label, no claim change, no Project read; cost-free in the same query; a mis-routed launch cannot take another person's issue (Wave 2 stops) | A Triage-or-higher person must assign before the poller sees the issue; assignment persists after the claim, so it cannot be the dispatch marker and a separate record is needed; a claim that fails after Wave 3 leaves the issue selected every cycle, so a retry cap is needed; one person with several workspaces (same login) is not separated | R01 §9, §10; R02 §2c; R03 §4.3; W01 §14.4 |
| 2. Per-person label | Label such as `owner:<login>` | Costless in the same query; the label can serve as dispatch marker | New labels per person created by a maintainer; the approver check must cover this label too; a poller write is needed to swap or remove it | R01 §9; W01 §14.4; R03 §4.3 |
| 3. Project field | `assignee:` filter or a custom field in the Project items query | Keeps ownership in one editable place | Needs the Project read token; server-side filtering on a custom field is [UNVERIFIED]; larger response | R01 §9; W01 §14.4 |
| 4. Unassigned, first workspace to take it | `no:assignee` plus the dispatch record | No pre-assignment needed | A race: the claim has no mutual exclusion and `--add-assignee` adds; a failure after Wave 3 strands the issue (assigned, no claim comment, never re-selected) | R01 §9; R02 §2c; W02 G1 |

The single predicate all candidates share is: skip an issue assigned to a login other than the own login (the claim would stop anyway) (R02 §2c).

**Which one the research supports:** candidate 1 (assigned to the own login). R01 calls it the best fit to claim semantics, R03 calls the assignee "the one routing input the claim already enforces", and W01 §14.4 finds candidates 1 and 2 cost nothing extra and candidate 4 the only racy one. **The choice itself is marked open:** no addendum names a candidate, and R02 §2c states that which candidate the owner picks is not shown by any file. The optional poller-side reservation for candidate 4 (add `@me`, re-read the assignees, back off if not sole assignee, deterministic tie-break) is a design suggestion in R01 §9, [UNVERIFIED] and untested. The same-login multi-workspace case is open under every candidate (GAPS 3).

### 7.5 Why a new session per issue through `orca agent launch`, not typing into a live coordinator session

| Route | What the research shows | Source |
|---|---|---|
| New top-level session per issue with `orca agent launch --agent claude --worktree path:<abs> --surface terminal --prompt "/sc:issue --claim <int>"` | Isolated (a failed claim affects only its own session), clean context, no competition with a person, auto-named from the prompt (the name question is not asked when a prompt is carried), its own `.dev/issues/<N>/` output. Costs: one more tab and Claude process per issue (tabs may accumulate, an inference), and no coordinator visibility because it is not a worker run. The prompt is submitted, not left as a draft | R01 §12 [CODE-VERIFIED]; analysis F4 |
| `orca orchestration send` into a live coordinator | Durable but pull-only: "Enqueue is durable but does not interrupt you, so nothing arrives unless you look", so the claim would not start until the session looks; a message is not known to run as `/sc:issue` | R01 §12 (Orca guide text `bundled-skill-guides.js:3158`, `orca-capabilities.md:66`) [CODE-VERIFIED for the text]; slash-command execution [UNVERIFIED] |
| `orca terminal send` into a live terminal | Immediate, but types into whatever is on the terminal and collides with a person's input and context | R01 §12 (judgement from the help text) |
| Dispatch `/sc:issue` as a worker through `worker-start` | Forbidden: the never-as-worker list names `/sc:issue` and the brief guard refuses it | WORKER-CONTRACT.md:23 (R01 §7) [CODE-VERIFIED] |

Needed to proceed: one owner-run live test that a leading `/sc:issue` given as the initial `--prompt` is executed, and whether the prompt is delivered as argv or as a typed paste (R01 §12; GAPS 1, 2). This research ran nothing live.

### 7.6 Repo fit: what the deliverable looks like in this repo

All items are taken from R02 and R01; the design choices inside them are for the plan.

| Item | Fit | Source |
|---|---|---|
| Package | New `src/superclaude/cli/<pkg>/` modeled on `cli/recommend/` (thin `commands.py` with the Click group, pure-logic modules for selection, runner seam and dedupe state), or a single file like `cli/init_lite.py` for a one-verb poller | R02 §4.2 |
| Registration | One block after `main.py:561` with the `# noqa: E402,I001` deferred-import marker and `main.add_command(<group>, name="<verb>")`; no `pyproject.toml` change; no `.claude/` mirror (only commands, skills, agents, hooks, templates are mirrored) | R02 §4.1, §4.2, §6 |
| Subprocess seam | The poller needs its own injectable runner for `gh` and `orca`: no Python `gh` wrapper exists (`ci.py` is a pure classifier, [CODE-CONTRADICTED] as a wrapper); `origin_repo.py` is the shape to copy (argv list, `check=False`, typed errors, JSON stdout, exit-code table, stdlib only) | R02 §3.1, §3.2 |
| Tests | `tests/<pkg>/` with pure unit tests over JSON fixtures, injectable-runner tests asserting that no write-shaped `gh` call happens and that the only issue-derived launch argument is the integer, and one or two CliRunner tests with PATH-stub `gh` and `orca`; only declared pytest markers (`--strict-markers`) | R02 §3.4, §5 |
| Mock contract for `orca agent launch` | Accept the argv, record `--agent`, `--worktree`, `--surface`, `--prompt`; succeed with exit 0 and JSON; fail with exit 1; simulate the unknown-outcome error carrying an `operationId`; simulate "cwd not inside an Orca workspace" | R01 §12 (real JSON error body [UNVERIFIED]) |
| Design doc | `docs/designs/<name>.md` following `docs/designs/sc-issue-command.md` (purpose, binding decisions Q1 to Q3, architecture, interface, GitHub call rules, error handling, files, tests, defaults, acceptance criteria) plus the UNVERIFIED section style of `sc-issue-launch-level-hook.md`; record Coder#477 and options B and C as follow-up and revisit conditions | R02 §7 |
| Label setup instructions | Ship `gh label create "<name>" --repo IronbellyOrg/IronClaude` lines in the house format of `refs/labels.md:22-42`; `/sc:issue` never creates labels | R02 §2b |
| Checks to pass | `ruff check src/ tests/`, `ruff format --check src/ tests/`, full pytest, `make lint-architecture`, `make verify-deps`; Python 3.10-compatible (`from __future__ import annotations`); `make sync-dev` and `make verify-sync` only if a command, skill, agent or template is added | R02 §6 |

Poller rules the research supports ([PROPOSAL] unless a code citation is given): sequential calls; honor `retry-after` and `x-ratelimit-reset`; exponential backoff with a retry cap; treat `incomplete_results: true` as "unknown", not "empty"; an explicit `--limit` above the default 30 (W01 §5, §10); where REST is used, store an ETag per query and send `if-none-match` so an unchanged poll (304) consumes no primary quota, noting that GraphQL conditional requests are not documented and the ETag behavior of the Projects items route is [UNVERIFIED] (W01 §5, §6, §8); a per-cycle launch cap and a per-issue retry cap (W02 recommendation 7); the dispatch record written before the launch and a lost reply treated as "dispatched", retried only with `--retry-launch <operationId>` (R01 §12 [CODE-VERIFIED]); select the worktree with `path:` and not `issue:<n>` until the Orca linking behavior is tested (R03 §5; GAPS 16); a lost local record must never cause a second launch of an issue that already carries the claim marker comment (W02 recommendation 3).

### 7.7 IronbellyOrg/Coder#477

IronbellyOrg/Coder#477 ("Workspace listener, monitor registration and secure prompt routing for every Coder workspace", open, read 2026-11-07) is a sibling dependency in the Coder repo. It was filed assuming a push design, and option A makes it unnecessary unless option B or C is revisited. Its listener, registration and transport live in the Coder repo, not in IronClaude; the only follow-up A needs in the Coder repo is the `coder_script` cron entry that runs the poller and, if the template does not already persist `$HOME`, a persisted path for the dispatch record (NOTES ADDENDUM and ADDENDUM 2; W02 A1, A4). If B or C is revisited, the contract in W02 J1 to J2 (fixed integer-only fields, derived idempotency key, response codes 200/202/400/401/403/409/422/429) is the starting point, and the sender-authentication options are compared in W02 H5.

### 7.8 Revisit conditions

The conditions under which the decision would be revisited for B or C are in the table "Revisit conditions for options B and C" above (nine conditions, with option favored and source). D is the first fallback for condition 6.

### 7.9 Details the addenda do not settle (all remain open)

| # | Open detail | Why it is open | Source |
|---|---|---|---|
| 1 | **[OPEN]** The intended-owner rule: which routing candidate (7.4) and how the same-login multi-workspace case is handled | No addendum names a candidate | R02 §2c; GAPS 3, 15 |
| 2 | **[OPEN]** The approver allow-list: where it is kept (repo file, org team, CODEOWNERS-like list) and the rule "latest `labeled` event by an allow-listed account" | The repo has none | R03 §4; GAPS 14 |
| 3 | **[OPEN]** Trigger and approval label names, the Project and Status mapping, and whether the Project and Backlog checks are used or the selection is label-only | No such label or mapping is defined anywhere; the fork has only the 9 default labels | R02 §2; GAPS 12, 5 |
| 4 | **[OPEN]** Policy for the claim's own reads of issue title, body and comments: accept as a documented risk, restrict to approved authors by `author_association`, lock the conversation on approval, or change the claim to read less | The integer-only rule does not cover this path | R03 §3.2, §3.3; GAPS 13 |
| 5 | **[OPEN]** The permission mode of the launched session | Depends on ccsession flags, Orca `agentDefaultArgs` and the command Orca runs, per host; whether `orca agent launch` applies `agentDefaultArgs` is untraced | R03 §2.2, §2.3; GAPS 4 |
| 6 | **[OPEN]** At-most-once design: local dedupe state versus "assigned to my login and no claim marker comment of mine", the per-cycle launch cap, the per-issue retry cap and any lease length | The race window between claim Wave 1 and Wave 3 was not measured | GAPS 15; W02 G4 |
| 7 | **[OPEN]** Where the poller runs and keeps its dispatch record in the target Coder template: scheduler availability, survival of stop and start, a persisted `$HOME` | The target template (`VSCode-AIDev02`) is known only through the sibling issue text | GAPS 9; W02 A4, A5 |
| 8 | **[OPEN]** One owner-run live test: a leading `/sc:issue` as the initial `--prompt` executes; argv versus typed paste; real JSON shape and error body of `agent launch` | Not shown by any file; this research ran nothing live | GAPS 1, 2 |
| 9 | **[OPEN]** Coder workspace facts: Orca runtime reachable by the poller, `ccsession-orca` configured, `claude-gw-tier*` picker IDs served, `gh` authenticated as the person, ClickUp variables | Unverified per host | GAPS 4 |
| 10 | **[OPEN]** Whether the Coder workspace owner and the `gh` login are always the same person | Not checkable in this repo | GAPS 19; W02 B3 |
| 11 | **[OPEN]** Whether the poller's token may read the org Project (`read:project`) and whether the server-side Backlog filter works through `gh project item-list --query` or the REST `q` parameter | Not exercised | GAPS 5, 11; W01 §8, §13 |
| 12 | **[OPEN]** Whether one person runs several workspaces that all poll with one login | Not known | GAPS 3 |
| 13 | **[OPEN]** Whether a claim re-run tolerates an already existing `.dev/issues/<N>/` directory | `claim.md:18` says only "Create `<D>`"; matters for a retry after a partial claim | GAPS 7; R01 §10 |
| 14 | **[OPEN]** Whether the `issue:<n>` worktree selector triggers the Orca-to-GitHub linking the project rule forbids, and how the poller learns its worktree path (there is no `--repo` flag) | Not tested | GAPS 16; R01 §12 |
| 15 | **[OPEN]** Detecting an issue-body edit after approval | No documented API field; a body hash recorded at approval is a [PROPOSAL] | GAPS 10; W02 G2 |

---

## Coverage of research-file key findings

Every key finding in the Summary and Key Takeaway sections of the assigned research files appears in Sections 6 and 7 or is excluded here with a reason.

| Source | Key finding | Where used, or exclusion rationale |
|---|---|---|
| R01 | Command is explicit-only; first message must be the literal `/sc:issue --claim <N>` | 6.1 step 6; 7.3 (Prompt) |
| R01 | Only `origin_repo.py` validates the argument in code; a bare integer is strictest; build the prompt with `int()`; the script is a second check | 7.3 (Prompt) |
| R01 | Claim never runs the pipeline; the issue text's expectation is [CODE-CONTRADICTED] | 6.0 shared facts; 7.3 (Claim-only) |
| R01 | Claim writes `.dev/issues/<N>/` into the checkout, so the workspace must be a checkout of origin | 6.0 shared facts |
| R01 | No machine-readable result file; completion is visible only on GitHub and in `.dev/issues/<N>/` | Excluded as plan-level detail; the GitHub-side dispatch record rule in 6.1 step 5 and 7.6 covers it |
| R01 | Stops in Waves 0 to 2 write nothing; Wave 3 is the first write; claim does not gate on labels or Projects and leaves Backlog unchanged | 6.0 shared facts; Requirement Scoring R4; 7.4 |
| R01 | `claude-gw-tier*` picker IDs are a hard prerequisite; Wave 1 failure would repeat every cycle without a dispatch record | 6.0 shared facts; 7.9 item 9; 7.6 (retry cap) |
| R01 | No trigger or approval label exists; labels are an output of `--create` only | 6.0 shared facts; 7.6 (label instructions) |
| R01 | Race between logins; same-login race; no mutual exclusion; at-most-once must be built in the poller; dispatch record before launch; launch reply can be lost | Requirement Scoring R5, R10; 7.4; 7.6 |
| R01 | ClickUp is optional and never blocks the claim | Excluded: does not change any option's score; the claim comment reports "skipped" (R01 §6); listed under 7.9 item 9 as a per-host fact |
| R01 | Never-as-worker list; a poller-launched ordinary session is outside it (interpretation); poller must be a plain process (WC-13) | 6.0 shared facts; 7.5; Options Comparison (fit row) |
| R01 | Entry points and the `orca agent launch` contract; prompt submitted; existing worktree required; exit 1 on error; `--retry-launch`; leading slash command execution unverified | 6.1; 7.5; 7.6; 7.9 item 8 |
| R01 | Integer-only protects the prompt, not the claim's own reads of issue text | 7.3 (residual risk); 7.9 item 4 |
| R02 | No schedule or issue-event workflow exists; option A needs none; B would be the first | 6.1, 6.2, 6.4 (Effort rows) |
| R02 | Existing labels cannot express approval or readiness; new labels need `gh label create` instructions | 6.0; 7.6; 7.9 item 3 |
| R02 | `ci.py` is not a `gh` wrapper; no Python `gh` wrapper exists; nearest pattern `origin_repo.py`; mocking is PATH-stub executables | 6.1 (Effort, Reuse); 7.6 |
| R02 | Click registration block, package model, test layout, Makefile and CI gates, `.claude/` mirror scope | 6.1 (Effort); 7.6 |
| R02 | Design-doc house format | 7.6 |
| R02 | Reconciled assignee predicate (skip assigned-to-others) and per-candidate consequences | 7.4; contradiction 2 in 6.0 |
| R02 | Convention B `gh repo view` fallback is unsafe for the fork; always pass `--repo IronbellyOrg/IronClaude` | 7.3 (Fields read) |
| R02 | Stale-doc items: `mock_gh` description, frozen-snapshot comment in `tests/cli/test_cli_registration.py`, Orca-inherited issue forms | Excluded: do not affect any option's score or the recommendation; recorded in GAPS 23 |
| R03 | Only the Bash job-identity adapter exists; guard script, `--pipeline`, marker binding and pre-push layer are design only; B-CTX gates only a later pipeline extension | 6.0 contradiction 6; 7.3 (Claim-only) |
| R03 | Nothing registered constrains a launched session; permission posture undefined; `master` unprotected; readable token; repo is public | 7.3 (residual risk); 6.0 shared facts |
| R03 | The identity hook is not installed on this host | Excluded: the hook is dormant and does not affect a claim-only watcher (R03 §1.3) |
| R03 | The claim reads issue title, body and comments live and posts unreviewed output; approval does not freeze the text | 7.3 (residual risk); 7.9 items 4, 15 |
| R03 | Approval authority is GitHub Triage or higher (3 accounts); the label-event actor allows a poller-side check; assignee is the one routing input the claim enforces | 7.3 (Approval); 7.4; 7.9 item 2 |
| R03 | Worker Contract does not govern a plain `orca agent launch` session; the contract has no category for a standing authorization by an approver's label | 6.0 shared facts; 7.5. The policy gap is carried: the approver's label as authorization and the claim's writes as its full extent are a decision for the design doc (7.6 design doc, Binding decisions) |
| R03 | Security properties provided versus missing (at-most-once, audit, pre-launch integer validation, permission-mode decision) | Requirement Scoring R7 to R10; 7.3; 7.9 |
| R03 | Stale docs: hooks README, `launch-level-guard.sh` present-tense statement, "private fork" | 6.0 contradictions 5 and 6 and shared facts; the hooks README item is excluded (not decision relevant) |
| W01 | Scheduled Action: 5-minute floor, delay, drops, default branch, 60-day disable | 6.2; Revisit table |
| W01 | No `issues` type for a Project Status change; `projects_v2_item` is an organization webhook event and not a workflow trigger (by absence) | 6.2 step 3; 6.3; Scoring R4 |
| W01 | Read tokens for Projects v2; `GITHUB_TOKEN` cannot read an org Project | 6.2 step 2; 6.4; Scoring R3 |
| W01 | REST `q` filter, `gh project item-list --query`, issue search has no Status qualifier | Scoring R4; 7.9 item 11 |
| W01 | Rate limits and cost arithmetic; ETag/304; secondary limits; `incomplete_results` | 6.1 (Pros); 7.6 (poller rules); Revisit condition 2 |
| W01 | Who applied the label from issue events or timeline; `author_association`; Triage can label | 7.3 (Approval); 7.4 |
| W01 | Webhook facts for B and C (HMAC, delivery id, 10 seconds, no automatic redelivery) | 6.3; Options Comparison (stopped workspace row) |
| W01 | Actions minutes cost | Excluded: option A runs no Action, and standard runners are free in public repositories (W01 §13) |
| W01 | Intended-owner candidates costed (`assignee:@me`, label, Project field, first-come) | 7.4 |
| W02 | `coder_script` cron, workspace stop behavior, activity, durable state, systemd availability | 6.1 (steps, Q-c); 7.7; 7.9 item 7 |
| W02 | Agents connect outbound; no fixed inbound port; `coder ssh`, `port-forward`, `external-auth access-token`; `coder exec` not found | 6.2; Scoring R8; Q-a, Q-b |
| W02 | Coder external auth does not guarantee the workspace owner's identity | Q-a (all options); 7.9 item 10 |
| W02 | `claude -p` expands custom commands; Manual mode default; `--bare` skips them; old mirror is stale | 6.1 (variant); 6.0 contradiction 4 |
| W02 | `claude-code-action` runs on runners, needs write access, defenses are partial | 6.2 (Cons, Reuse); Scoring R2 (analogue) |
| W02 | Comparable dispatchers: `create-task-action`, Coder Agents Chats API | 6.1 (Pros), 6.2, 6.3. Copilot coding agent, OpenHands and Codex are excluded: context only, they run on vendor infrastructure and are not usable for the Orca flow (W02 E3 to E5); Sweep-style bots were not researched |
| W02 | Prompt-injection guidance and mitigations | 7.3 |
| W02 | At-most-once patterns (assign is not a lock, marker comment, idempotency key, lease, `concurrency`) | Scoring R10; Comparison; 7.4; 7.9 item 6 |
| W02 | Sender authentication options and `coder_app` sharing | 6.2; Scoring R8; 7.7 |
| W02 | Minimal watcher-to-listener contract and revisit conditions J3 | 7.7; Revisit table |
| GAPS | All 24 rows | Rows 1 to 5, 7 to 17, 19 to 22 are used above or in 7.9; row 6 (tests pinning the stop text) is excluded because claim-only leaves the stop text unchanged; row 18 (governance files not read) and the stale-doc rows are carried below |

## Carried to Open Questions

These [UNVERIFIED], [PROPOSAL] or open items were used in the ratings above. None is the sole basis of the recommendation: the recommendation rests on the owner's decision (ADDENDUM 2) and on [CODE-VERIFIED] and [EXTERNAL-VERIFIED] facts (the claim flow, the Worker Contract, the `orca agent launch` contract, the `coder_script` cron documentation).

| # | Item | Used in | Source |
|---|---|---|---|
| 1 | A leading `/sc:issue` given as `orca agent launch --prompt` executes as a slash command; argv versus typed paste; real JSON shape and error body | 6.1 Risk; Scoring R6; 7.5; 7.9 item 8 | R01 §12; GAPS 1, 2 |
| 2 | Poller host in the Coder template: scheduler overlap behavior, survival of stop and start, persisted `$HOME`, systemd or system cron | 6.1; 7.9 item 7 | W02 A1, A4, A5; GAPS 9 |
| 3 | Whether an Orca-launched session counts as Coder "activity" | 6.1 (Cons) | W02 Gaps 5 |
| 4 | Poller token can read the org Project (`read:project`); server-side Backlog filter through `gh project item-list --query` or REST `q`; `projectItems` status schema; ETag behavior of the Projects route and GraphQL | Scoring R3, R4; 7.6 | W01 Gaps 3 to 6; GAPS 5, 11 |
| 5 | Organization token policies (classic token restrictions, fine-grained approval, SSO authorization) | Revisit condition 6 | W01 Gaps 7 |
| 6 | GitHub multi-assignee behavior in a real double claim (derived from code and the additive API, not observed) | Scoring R10; 7.4 | R01 §9; W02 G1; GAPS 3, 24 |
| 7 | Whether one person has several workspaces polling with one login | Scoring R5, R10; 7.9 item 12 | GAPS 3 |
| 8 | A poller-launched ordinary session is outside the never-as-worker list as owner intent | 6.0 shared facts; Comparison (fit row) | R01 §7; GAPS 24 |
| 9 | Coder workspace owner always equals the `gh` login | Scoring R7; 7.9 item 10 | GAPS 19; W02 B3 |
| 10 | Permission mode of the launched session per host; whether `orca agent launch` applies `agentDefaultArgs` | 7.3; 7.9 item 5 | R03 §2.2; GAPS 4 |
| 11 | Detecting a post-approval issue-body edit; issue-event retention; whether a Projects v2 Status change appears in the timeline | 7.9 item 15; Scoring R4 (C) | GAPS 10; W01 Gaps 9 |
| 12 | Whether organization owners outside the collaborator list can label; permission to edit another user's issue body | 7.3 (Approval) | GAPS 17 |
| 13 | B and C only: mTLS through Coder, the app-proxy token header for non-browser callers, the workspace start endpoint, webhook redelivery window and delivery ordering, hosting of a central service | 6.2, 6.3; Scoring R8 | W02 Gaps 7 to 9; W01 Gaps 10; W02 H3, I2 |
| 14 | `claude -p "/sc:issue --claim <N>"` end-to-end behavior | 6.1 (variant) | GAPS 8; W02 Gaps 15 |
| 15 | Whether `--worktree issue:<n>` triggers Orca-to-GitHub linking | 7.6 poller rules; 7.9 item 14 | GAPS 16 |
| 16 | Whether a claim re-run tolerates an existing `.dev/issues/<N>/` | 7.9 item 13 | GAPS 7 |
| 17 | The explicit statement that `GITHUB_TOKEN` cannot read an organization Project comes from a secondary source (the gh-aw docs); the primary evidence is the absence of a Projects permission key | 6.2 step 2; Scoring R3 | W01 Gaps 1, 2 |
| 18 | A "wake a stopped workspace" hybrid is mentioned for B and C only and was not evaluated as its own design | 6.4 (further hybrids) | W02 J3 item 1 |
| 19 | Governance file bodies not read (`freshness-pre-edit.sh`, `sc-recommend-phase0.sh`, `issue-worker-t2.md`, `issue-worker-t1.md`, `tests/cli/test_install_hooks.py`) | 7.3 | GAPS 18 |
| 20 | Alternative runtimes and dispatchers not researched or only from search snippets (Copilot assignment steps, Codex issue path, Sweep) | Coverage table | W02 Gaps 11 |
