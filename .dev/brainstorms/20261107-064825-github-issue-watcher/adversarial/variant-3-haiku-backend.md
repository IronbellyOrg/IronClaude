# GitHub Issue Watcher Requirements

Status: proposed requirements for issue #331; owner decisions D1–D3 are binding.

## 1 Purpose and scope

Replace the manual handoff of an eligible GitHub issue into its intended owner's workspace with a workspace-side polling command. Each running workspace checks GitHub every five minutes using its own authenticated GitHub login and starts a new top-level terminal session that receives exactly `/sc:issue --claim <N>`.

The watcher owns selection, identity verification, durable dispatch accounting, and launch submission; the existing claim command owns assignment, accuracy checking, posted summary, and `next-steps.md`. A successful launch does not prove a successful claim. The watcher must distinguish those outcomes rather than reporting implementation work as completed.

This specification defines the mock-testable repository implementation, not a deployment authorization. Proposed interfaces and policy choices below are requirements for a future implementation, not claims that those interfaces already exist. ASSUMPTION: deployment can nominate one active dispatch authority per GitHub login and repository with persistent local storage; without that restriction this design cannot promise cross-workspace at-most-once starts.

## 2 Fixed constraints and non-goals

- D1 is fixed: option A, workspace-side pull; no listener, inbound port, workspace-address registry, or privileged Coder control-plane credential.
- D2 is fixed: claim-only; do not select, execute, or retry a post-claim pipeline.
- D3 is fixed: only a validated integer issue number is variable prompt content; no issue title, body, comments, labels, or actor names enter it.
- Repository access targets only `IronbellyOrg/IronClaude`, verified against `origin`; never rely on GitHub CLI's default repository.
- `/sc:issue` is forbidden as an Orca worker; launch an ordinary top-level session in an existing worktree.
- Build no scheduled workflow, deployed daemon, live workspace call, or production label mutation here; no secrets enter tracked files.

Research compared existing primitives before recommending new code: the claim command, Orca launch, label relay, scheduled Actions, and a central service. Its readiness scoring counts supported criteria, not weighted preference:

| Alternative | Meets / partly | Disposition |
|---|---|---|
| A: workspace poller | 2 / 8 | Owner-selected; build mockable portion |
| B: Action plus listener | 1 / 9 | Follow-up only; higher exposure and effort |
| C: central service plus listener | 0 / 10 | Follow-up only; additional hosting and webhook responsibilities |
| D: label relay plus poller | 2 / 8 | First alternative if workspace Project access fails |

Revisit only when stopped workspaces cause excessive waiting, latency/API use becomes unacceptable, centralized approval/audit becomes necessary, duplicate claims persist, account binding becomes available, workspace tokens cannot read Projects, event-time Project changes matter, a shared ledger becomes necessary, or recurring workspace execution proves impossible. B/C do not automatically solve the last condition. Coder#477 is unnecessary under A unless push is reconsidered.

## 3 Definitions

**Tagged:** the current issue label set contains the configured trigger label's resolved node ID; proposed display name `watch:ready`. A similarly spelled name or text mentioning it does not qualify.

**Approved by a human:** the approval label is currently present, and its latest application event identifies an allow-listed GitHub account with non-bot account type; proposed display name `watch:approved`. The allow-list records trusted human account IDs, not display names. Missing actor metadata, an unauthorized latest reapplication, incomplete event history, or a bot fails approval. Accounts are administratively admitted only after verifying Triage-or-higher access; account compromise remains a risk. Approval authorizes this claim handoff, not execution of issue instructions.

**In a Project:** a non-archived item in the configured Projects v2 node ID references this repository's issue node ID. Draft items, pull requests, similarly named Projects, and membership in another Project do not count.

**Backlog:** that Project item's configured single-select Status field ID contains the configured Backlog option ID; the visible word alone is insufficient. Missing, renamed-with-new-ID, deleted, or ambiguous mappings fail closed.

**Intended owner:** proposed default is the sole current assignee, whose account ID matches the cycle's authenticated GitHub user; unassigned and multi-assignee issues are ineligible. Login text is retained for display and claim compatibility, while account ID anchors identity. This deliberately selects a stricter subset than the existing claim command permits.

**Eligible issue:** an open, non-pull-request issue in the approved repository satisfies every definition above, has no recognized prior claim marker, has no consumed dispatch slot, and passes the same predicates on immediate pre-launch refresh. Ineligibility has a recorded reason; absent or unreadable evidence is not positive evidence. Mutable GitHub fields cannot be atomically locked with a local launch, so eligibility is guaranteed only at the last completed refresh.

## 4 Functional requirements

**FR-001:** The CLI shall reject a worktree whose parsed `origin` does not identify the allowed repository before any launch.
Acceptance: Given mocked git returning another repository, when `once` runs, then mocked Orca receives no invocation and configuration failure is returned.

**FR-002:** Each cycle shall fetch the authenticated account and refuse any mismatch with configured dispatch authority.
Acceptance: Given mocked `gh` returning a different account ID, when the cycle begins, then no candidate is dispatched and identity failure is logged.

**FR-003:** The GitHub adapter shall explicitly scope repository calls and retrieve complete structured selection evidence without ingesting narrative fields into selection logic.
Acceptance: Given stubbed repository calls, when discovery runs, then argv contains the explicit repository argument or literal repository API path, requests are read-only, and fixtures containing titles do not alter decisions.

**FR-004:** The selector shall apply all section 3 predicates and return a stable machine-readable rejection reason for each examined issue.
Acceptance: Given fixtures independently missing each predicate, when selection runs, then each receives its corresponding rejection and no launch occurs.

**FR-005:** Approval verification shall identify the latest approval-label application and validate actor ID and account type against trusted configuration.
Acceptance: Given an allowed application followed by removal and unauthorized reapplication, when evaluated, then approval fails despite the label being present.

**FR-006:** Incomplete pagination, unknown Project schema, or missing Project authorization shall block affected selection rather than substitute label-only eligibility.
Acceptance: Given mocked truncation or permission denial, when reading Project evidence, then no dependent launch occurs and the CLI reports incomplete evidence.

**FR-007:** Candidate processing shall persist least-recently-examined ordering and obey the configured examination cap.
Acceptance: Given more candidates than the cap and repeated identical responses, when cycles repeat, then previously unexamined candidates advance before repeated rejects.

**FR-008:** The poller shall refresh issue, approval, ownership, and Project evidence immediately before reserving a launch.
Acceptance: Given a qualifying discovery followed by a refreshed removed approval or changed assignee, when dispatch is attempted, then no launch slot is consumed and no Orca call occurs.

**FR-009:** The prompt builder shall accept only a positive JSON integer, rejecting booleans, strings, fractional numbers, and out-of-range values.
Acceptance: Given invalid number fixtures including command-like strings, when building a prompt, then validation fails without Orca execution; a valid integer yields only the fixed command plus decimal digits.

**FR-010:** Dispatch shall durably consume the launch slot before submitting a shell-free argv launch in the configured existing worktree.
Acceptance: Given injected failure before commit, when dispatch runs, then Orca is untouched; after commit, its single prompt argument matches FR-009 and its worktree selector is `path:<absolute-path>`.

**FR-011:** Launch handling shall distinguish confirmed acceptance, explicit non-start, and unknown outcome without fresh retry after slot consumption.
Acceptance: Given timeout or malformed launch output, when processing resumes, then the record is `unknown` and another ordinary launch is absent; a returned operation ID permits only reconciliation of that operation.

**FR-012:** Reconciliation shall mark `claimed` only from recognized existing claim evidence, never from assignment alone or launch acceptance.
Acceptance: Given own assignment without the protocol's marked posted summary, when reconciling, then status remains unconfirmed; recognized evidence changes it to `claimed` without another launch.

**FR-013:** The CLI shall expose dry-run decisions and dispatch inspection without launching or modifying GitHub.
Acceptance: Given eligible mocked issues, when dry-run or inspection runs, then output includes eligibility or stored state while Orca and GitHub mutation call counts remain zero.

## 5 Non-functional requirements

**NFR-001 — Security:** All subprocess calls shall use argv arrays without shell interpretation, trusted executable resolution, fixed repository targeting, and redacted diagnostics; adversarial fixture values must create no extra argument or leaked credential.

**NFR-002 — At-most-once:** A durable repository/issue dispatch key shall permit at most one ordinary launch submission within the stated single-authority boundary; concurrent-process and crash-injection tests must never produce a second submission.

**NFR-003 — Integrity:** Transactions shall preserve consumed slots across process death and reject corrupt, incompatible, missing-after-initialization, or nonpersistent state; injected write and recovery failures must produce zero new launches.

**NFR-004 — Rate limits:** Rate exhaustion and retry hints shall persist a next-permitted-request time, with no busy retry; fake-clock tests must show no GitHub call before that time and bounded retries afterward.

**NFR-005 — Observability:** Every examined candidate and cycle termination shall emit structured, secret-free events containing repository, issue number where applicable, cycle ID, decision, reason, state transition, elapsed time, and exit code; fixture tests must match those fields without narrative issue text.

**NFR-006 — Failure handling:** Authentication, schema, identity, and storage errors shall fail closed, while a candidate-local malformed response shall be isolated and reported; mixed-fixture tests must distinguish skipped candidates from a clean successful cycle.

**NFR-007 — Performance:** A cycle shall terminate within a configurable budget, proposed 240 seconds, with proposed 30-second subprocess deadlines; fake-clock timeout tests must prevent overlapping launch attempts and leave unfinished work for later polling.

**NFR-008 — Cost:** The default cycle shall examine at most the proposed 10 candidates and initiate at most the proposed one new session, while emitting request and launch counts; cap tests must prove those ceilings and include pagination calls in cost reporting.

**NFR-009 — Scheduling:** The command shall execute one bounded cycle and exit, supporting the fixed five-minute external cadence; repeat-invocation tests must preserve backoff and dispatch state without requiring an in-process daemon.

## 6 Security model

Trust local operator configuration, installed binaries, and protected state storage; distrust all GitHub content and subprocess output until schema-validated. Repository metadata reads exclude title/body. Claim-marker reconciliation may inspect bounded comment content solely to recognize the existing protocol's exact marker and authenticated author, never to construct prompts or commands. A marker from an unrelated author cannot establish successful claim evidence.

| Asset | Threat | Control | Residual risk |
|---|---|---|---|
| Session prompt | Injection through issue content | Fixed template; strict integer validator; argv boundary | Claim later reads public issue text |
| Workspace identity | Wrong GitHub account claims work | Account-ID binding each cycle; sole-assignee routing | Coder owner equivalence is not proven |
| Approval decision | Forged marker or bot-applied label | Current label plus latest actor event; human allow-list | Compromised approved human account |
| Dispatch ledger | Duplicate starts through deletion or races | Durable unique key; process lock; no automatic slot reset | Independent state directories cannot coordinate |
| Credentials | Token leakage in logs or files | Existing authenticated CLI; no token config; diagnostic redaction | Host compromise exposes authenticated tools |
| Repository boundary | Default-repository confusion | Origin verification; explicit repository scoping | A compromised local git configuration remains trusted input |
| Launch authority | Issue-driven privileged execution | Claim-only command allowlist; top-level launch only | Launch exposes no verified permission-mode control |

Deployment must remain disabled until the owner accepts the claim's live narrative-read risk and verifies an acceptable session permission policy. Do not describe integer-only prompt validation as full protection from instructions encountered inside the launched session. No inbound sender-authentication mechanism is needed under A because no inbound endpoint exists.

## 7 Dispatch record and at-most-once semantics

Proposed storage is SQLite on an operator-configured persistent local path, protected by an exclusive cycle lock. Initialization is explicit; routine polling never silently replaces missing initialized storage. A unique key `(repository_node_id, issue_node_id)` survives login changes, label removal, reopening, and worktree changes. Number and login remain validated attributes, not the uniqueness boundary.

Record fields: `schema_version`, `repository_node_id`, `issue_node_id`, `issue_number`, `owner_account_id`, `workspace_authority_id`, `worktree_path`, `state`, `attempt_count`, `launch_count`, `lease_owner`, `lease_expires_at`, `created_at`, `updated_at`, `last_examined_at`, `approval_event_id`, `eligibility_digest`, `operation_id`, `session_id`, `last_error_code`, and `next_retry_at`. Store UTC timestamps and hashes of selection metadata, not issue narrative or credentials. An append-only transition table records previous state, next state, reason, and cycle ID in the same transaction.

| State | Entry and permitted transition |
|---|---|
| `pending` | Eligible candidate acquired under lock; refresh may cancel reservation or advance to launch intent |
| `unknown` | Durable launch intent committed before external call, or outcome ambiguous; may become `launched`, `failed`, `claimed`, or `abandoned` |
| `launched` | Validated acceptance with stable session/operation evidence; may become `claimed` or `abandoned` |
| `failed` | Explicit failure evidence; pre-submission failures may return to `pending`, consumed slots may not |
| `claimed` | Recognized claim summary evidence; terminal for automatic dispatch |
| `abandoned` | Operator disposition or exhausted safe retries; terminal for automatic dispatch |

The `pending` lease is 60 minutes [PROPOSAL]; expiry permits another local process to refresh only if the launch slot is unconsumed. Maximum safe pre-submission attempts are 3 [PROPOSAL], ordinary submissions per issue are 1 [PROPOSAL], examined candidates per cycle are 10 [PROPOSAL], and fresh submissions per cycle are 1 [PROPOSAL]. Consuming the slot and entering `unknown` is one durable transaction before external I/O. Expiry never releases a consumed slot.

A crash between commit and submission can permanently suppress an otherwise eligible issue; accept that lost-work risk instead of risking duplication. A lost reply with an operation ID allows `--retry-launch <operationId>` only for the same stored operation, never a new ordinary launch. Missing operation ID means operator investigation, not retry. Do not automatically purge terminal keys. Multiple independently configured workspaces for one login are unsupported; GitHub assignment and marker checks are not distributed locks.

## 8 Repo-side deliverables testable with mocks

Proposed package: `src/superclaude/cli/issue_watch/`, registered in `src/superclaude/cli/main.py` without changing existing claim behavior.

- `runner.py`: injectable `Runner` returning exit status, bounded stdout/stderr, and timeout classification.
- `github.py`: identity, discovery, Project pagination, issue refresh, label-event provenance, and marker recognition adapters.
- `selection.py`: pure predicates returning eligibility plus reason codes.
- `store.py`: SQLite schema, transactions, locks, transitions, and fairness bookkeeping.
- `launch.py`: integer-only `build_claim_prompt`, existing-worktree validation, argv construction, and launch-result classification.
- `cycle.py` and `cli.py`: bounded orchestration and proposed `superclaude issue-watch once`, `status`, and explicit `init-state` verbs; `once --dry-run` performs read-only decisions without consuming slots.

Proposed exit codes: `0` complete cycle or ordinary no-match; `2` configuration/schema/identity failure; `3` transient dependency or rate-limit deferral; `4` storage integrity failure; `5` unknown launch requiring attention; `6` overlapping cycle skipped. These are new contracts, not existing exit-code claims. Unknown launch takes precedence over ordinary transient errors.

`tests/issue_watch/` must cover each FR/NFR, subprocess PATH stubs, fake clocks, malformed JSON, full-page ambiguity, bot approval, account rename, revoked approval, concurrent invocations, and crash boundaries. No test may contact GitHub or start a real session.

`docs/designs/issue-watcher.md` must document schema, exit codes, limitations, recovery, and setup: label creation, allow-list governance, Project IDs, token permissions, persistent storage, and single-authority nomination. Instructions are reviewed text, not executed deployment. Use UV for Python checks; canonical distributable edits remain under `src/superclaude/`.

## 9 Follow-up not built here

Coder-side work owns the five-minute `coder_script` schedule and a persistent dispatch path if the template does not preserve home storage. Verify cron overlap, workspace shutdown behavior, and whether launched sessions affect workspace lifetime before enabling it.

An owner-run controlled test must establish that an initial slash-command prompt executes correctly, record actual launch success/error JSON, and confirm operation retry semantics. Host validation must cover installed tools, existing worktree, runtime reachability, authenticated account, Project-read scope, and session permission policy. Current Project query/schema compatibility is unverified; implement an adapter tested against fixtures but do not label it production-validated.

Actual labels, Project mapping, approver governance, deployment credentials, central audit aggregation, distributed coordination, and any post-claim pipeline remain external acceptance tasks. No listener or registration work from Coder#477 is required for A.

## 10 Open decisions

Recommended defaults below require policy approval; none reopens D1–D3.

| Decision | Recommended default and reason |
|---|---|
| Owner routing | Sole existing assignee equals authenticated account; avoids first-come assignment races |
| Same-login workspaces | Nominate one enabled authority and persistent ledger; local state cannot coordinate independent hosts |
| Labels | `watch:ready` and `watch:approved`, resolved to IDs; separates selection intent from approval |
| Approver policy | Operator-managed account-ID allow-list outside issue-controlled content; rejects bots and untrusted reapplications |
| Project mapping | Explicit Project, Status-field, and Backlog-option IDs; names are mutable and ambiguous |
| Dispatch durability | Persistent local SQLite with no automatic terminal-record deletion; preserves uniqueness after restart |
| Capacity | Adopt section 7 proposals initially; limits unattended session accumulation |
| Text and permissions | Block activation pending explicit narrative-risk acceptance and verified session policy; integer validation is insufficient |
| State loss | Fail closed and restore validated backup; recreating an empty ledger could duplicate every claim |
| Number range | Proposed upper bound 999999999; reject rather than coerce unexpected API values |

## 11 Risks

GitHub approval can change between refresh and launch; no API transaction spans GitHub and Orca. Claim assignment is additive, not compare-and-set, and Backlog remains unchanged, so neither substitutes for the ledger. A stopped workspace introduces unbounded wait until restart. Missing Project permissions can prevent every launch. Public issue content remains an instruction-injection surface inside claim execution. A successful claim marker establishes a posted claim, not proof that all local artifacts finished writing. Strict at-most-once submission sacrifices automatic recovery after ambiguous crashes. Independent workspace ledgers, cloned backups, or operator resets invalidate the uniqueness boundary; document these as operational hazards rather than claiming global exactly-once behavior.

## 12 Traceability

Sources are the supplied `seed-brief.md` (S), `enrichment/research-deep.md` (R), and `enrichment/codebase-context.md` (C); headings identify evidence without fragile line references. Policy defaults and stronger safeguards are derived proposals, not previously verified repository behavior.

| Requirements | Source fact and derivation |
|---|---|
| FR-001 | S Constraints: origin-only repository targeting; R security model |
| FR-002 | S Constraints: claim assigns workspace login; R intended-owner and identity model |
| FR-003 | S Enrichment: injectable argv runner; R security model and repository scope |
| FR-004 | S Success Criteria and Enrichment: selection filters; definitions are proposed resolutions |
| FR-005 | S Enrichment: latest labeled-event actor and missing approval policy |
| FR-006 | S Enrichment: missing Project scope and truncation risk; R verified fact 8 |
| FR-007 | S Enrichment: considered map and least-recently-examined ordering |
| FR-008 | S Enrichment: pre-launch re-read; R claim has no mutual exclusion |
| FR-009 | S D3; R security model and plan prompt builder |
| FR-010 | S dispatch-before-launch fact; R launch contract and plan |
| FR-011 | S Enrichment: unknown outcome and same-operation retry rule |
| FR-012 | S Known Context: marked claim comments; R claim-only boundary |
| FR-013 | S Constraints: mock-only build; inspection is a derived operational safeguard |
| NFR-001 | S security constraint and D3; R injectable runner and residual risk |
| NFR-002, NFR-003 | S dispatch record requirement; R no assignment mutex and open same-login problem |
| NFR-004 | R verified rate-limit fact; S polling cost fact |
| NFR-005 | S cycle audit-line requirement; R centralized-audit revisit condition |
| NFR-006 | S unresolved Project/schema facts; fail-closed behavior is derived |
| NFR-007 | S fixed cadence; deadlines are proposed operational budgets |
| NFR-008 | S proposed candidate and launch caps; R session-tab/process cost |
| NFR-009 | S D1; R Coder scheduling and stopped-workspace behavior |

