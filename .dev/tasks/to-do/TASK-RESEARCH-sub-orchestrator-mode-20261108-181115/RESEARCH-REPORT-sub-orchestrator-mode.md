# Technical Research Report: Sub-orchestrator / coordinator mode for the proposed /sc:orchestrator

**Date:** 2026-11-09
**Depth:** Deep
**Status:** Assembly complete; final assembly read-back finished; independent report acceptance pending
**Research files:** 8 codebase + 4 web research
**Scope:** Coordinator/worker policy, liveness and reporting, Orca source mechanics, hooks and identity, session-launch precedents, decision history, conditional change surfaces and related issue requirements.

**Table of Contents**
- [1. Problem Statement](#1-problem-statement)
- [2. Current State Analysis](#2-current-state-analysis)
  - 2.1 Evidence conventions, source key and installation snapshots
    - Source key
    - Controlling installation-snapshot distinction
  - 2.2 Contract and role model
  - 2.3 Liveness and reporting
    - Signals and records
    - Twelve procedural states
    - Timing, response and acknowledgment limits
  - 2.4 Orca mechanics: historically traced routes and bounded new depth source
    - Depth and authority are separate
    - Native local helper flow in the researched snapshot
    - Distinct kinds of parentage
  - 2.5 Hooks, guards and identity
    - B1 - Literal-executable recognition ceiling
    - B2 - Required supervision probes are not blanket read exceptions
  - 2.6 Session-launch precedents
  - 2.7 Decision history and revisit evidence
    - Two D5 trigger texts
  - 2.8 Issues, pull requests and independent requirements
  - 2.9 Wording, tests and distribution surfaces
    - Stale descriptions and historical records
  - 2.10 Current-state summary and dedicated uncertainty register
    - Evidence classes
    - Dedicated uncertainty register
    - Research coverage and intentional consolidation
- [3. Target State](#3-target-state)
  - 3.1 Desired behavior and decision boundary
    - What the decision must establish
    - Behavior required if a subordinate capability were adopted
  - 3.2 Success criteria
  - 3.3 Constraints
- [4. Gap Analysis](#4-gap-analysis)
  - 4.1 Current defects and adoption gaps
  - 4.2 Stale and contradicted families: explicit dispositions
  - 4.3 External answers that narrow earlier unknowns
  - 4.4 Coverage of all 54 compiled gap families
  - 4.5 Source coverage, precedence and justified exclusions
- [5. External Research Findings](#5-external-research-findings)
  - 5.1 Claude Code cross-session messaging and permission modes
    - M01 - Default delivery compares permission classes, not identical mode names
    - M02 - Held messages are not already in the recipient's context
    - M03 - The sender-class question remains partly unanswered
    - M04 - Inbound acceptance is separate from execution permission
    - M05 - An incoming-message hook is documented, with deployment limits
    - M06 - Receiving-context fields are not authenticated peer authority
    - M07 - A hook that can block is not automatically fail-closed
    - M08 - Preserve each channel's actual guarantee
    - M09 - Typed text is not a secure application protocol
    - M10 - Idle notices are observations, not completion
    - M11 - Receipt and mode alignment cannot manufacture human consent
    - M12 - Subagents, teams and independent sessions differ
  - 5.2 Hierarchical orchestration patterns
    - H01 - Parallel research benefit does not prove another supervisory generation
    - H02 - Briefs, artifacts and stopping rules matter
    - H03 - Parallel work retains synchronization costs
    - H04 - Dynamic decomposition needs task-shape justification
    - H05 - Context, depth, concurrency and lifetime are separate
    - H06 - OTP teaches lifecycle, not semantic correctness
    - H07 - LangGraph demonstrates composition, not a benchmark winner
    - H08 - AutoGen conversation limits are not subtree budgets
    - H09 - CrewAI manager duties do not prove parallelism
    - H10 - Credible critiques favor bounded collaboration, not permanent prohibition
    - H11 - MAST identifies failure categories, not the best topology
    - H12 - Published numbers do not price an extra middle layer
    - H13 - Flat-versus-hierarchy tradeoffs remain conditional
    - H14 - Correcting historical premises does not change permission
    - H15 - A middle supervisor must own more than routing
  - 5.3 Capability-narrowing grants
    - G01 - Macaroons narrow through MAC-authenticated caveats
    - G02 - Checking proofs differs from acquiring them
    - G03 - Expiry is not immediate revocation
    - G04 - Biscuit separates verification, attenuation and authorization
    - G05 - Third-party Biscuit blocks are not macaroon discharges
    - G06 - Revoked ancestry still needs distribution and freshness
    - G07 - Signed nonce and session claim are insufficient
    - G08 - CaMeL addresses influence, not delegation-token selection
    - G09 - Available libraries are not a maintained, already-used winner
    - G10 - Credential feasibility is not grant or hook readiness
  - 5.4 Orca public documentation on depth and helpers
    - O01 - Metadata-led discovery identifies the relevant Orca project
    - O02 - One is not a permanent product mandate
    - O03 - Migration is a version-specific risk, not an effective-value observation
    - O04 - Historical native helpers have a parent-worker route
    - O05 - “Nested coordinator” wording is not a complete role contract
    - O06 - Public requests are plausible value, not local measurement
    - O07 - Each host's limit remains separate
    - O08 - Public helper stopping is qualified
    - O09 - Capability does not amend the local decision
  - 5.5 External research summary
  - 5.6 Every external finding mapped to the six options
  - 5.7 Coverage, deduplication and exclusions
- [6. Options Analysis](#6-options-analysis)
  - 6.1 Controlling facts and corrections
  - 6.2 O1 - Keep two tiers and no subordinate mode
  - 6.3 O2 - Independent person-opened peer coordinators
  - 6.4 O3 - Supervised middle worker with native helpers
  - 6.5 O4 - Ordinary launched handoff-owner subordinate
  - 6.6 O5 - Existing in-session Agent helpers
  - 6.7 O6 - Defer with explicit reconsideration gates
  - 6.8 Nine-criterion comparison
  - 6.9 Worker and coordinator compatibility
    - Numbered worker rules
    - Coordinator duties and safeguards
  - 6.10 Disposition of all 35 issue requirements
  - 6.11 Evidence and scope limits of the comparison
- [7. Recommendation](#7-recommendation)
  - Rationale
  - 7.1 Value
  - 7.2 Implications
  - 7.3 Conditional unlocks
  - 7.4 Rethinks
  - 7.5 Twenty-five testable approval conditions
    - Gate interpretation
  - 7.6 What would change the recommendation
  - 7.7 Source coverage and retained limits
- [8. Implementation Plan](#8-implementation-plan)
  - Change surface per option
    - What existing tests actually pin
    - O1 - Retain two tiers, with conditional wording clarification
    - O2 - Independent person-opened peers
    - O3 - Supervised middle worker with native helpers
    - O4 - Ordinary launched handoff-owner subordinate
    - O5 - Existing internal Agent helpers
    - O6 - Gated deferral
  - Sync and verification ripple
    - Distribution surfaces and ceilings
    - Per-option distribution consequences
  - Evidence reconciliation and retained limitations
  - Source coverage and exclusions
- [9. Open Questions](#9-open-questions)
  - 9.1 Established boundaries that are not open questions
  - 9.2 Seventy-one individual questions
  - 9.3 Seven evidence limitations, not new product prerequisites
  - 9.4 All 38 stale/interpretation families dispositioned
  - 9.5 All 54 compiled gap families mapped by meaning
  - 9.6 All 53 external gap groups mapped by meaning
    - W01 - Twelve messaging gap groups
    - W02 - Fifteen hierarchy gap groups
    - W03 - Twelve grant gap groups
    - W04 - Fourteen Orca gap groups
  - 9.7 Carry-forward and scope
- [10. Evidence Trail](#10-evidence-trail)
  - 10.1 Evidence inventory and interpretation
  - 10.2 Codebase research
  - 10.3 Web research
  - 10.4 Scope discovery and research notes
  - 10.5 Complete primary returned research
  - 10.6 Archival supplements and inventory captures
  - 10.7 Six synthesis pairs
  - 10.8 Controlling corrections, scope precedence and gaps log
  - 10.9 Procedural references and verification boundary

## 1. Problem Statement
- **The question:** Should the proposed `/sc:orchestrator` support a subordinate coordinator, possibly selected through `--sub`, that accepts assignments from an orchestrator above it, supervises external sessions of its own, and reports aggregate results upward? The answer must establish its additional value, implications, conditional unlocks and the existing decisions that would need reconsideration. This is a decision report, not authorization to implement the mode.

- **Why it matters:** Command-internal helpers, supervised Orca workers, ordinary agent launches, worktree ownership and person-opened coordinators have different authority and reporting contracts. A middle session needs an accountable relationship in both directions: permission and responsibility for children, and meaningful progress, questions, results and failure reporting to its own supervisor. Issue #339's flat supervision, recovery, attention and cleanup requirements, and issue #423's cross-workspace knowledge-sharing requirements, do not inherently require another supervisory generation.

- **Trigger:** Issue #444 requests evaluation without preselecting adoption. PR #449 introduced the ownership phrase “a coordinator under another orchestrator” while expressly preserving supervised-worker restrictions. Its scope record deferred WC-13 to the separate subordinate-coordinator issue: INF-027 says not to change the worker contract in that work, while INF-026 excludes supervised workers from the ownership change. This leaves a deliberately deferred rule defect, not an implemented middle role or an approved exception. D5 retained depth-one policy, person-opened coordinators and the worker-session fan-out prohibition. Issue #339's later hierarchy/security “v2” and issue #423's knowledge-sharing “v2” are different scopes.

**Evidence:** The assigned question and delivery requirements appear in `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115.md:291-293`. INF-026 and INF-027 appear in `.dev/reflect/pre-TASK-WF-enforceTheOwnerP-20261108-031809-20261108033529/REPORT.md:77-78`. The approved D5 outcome is recorded in `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:405`. Issue requirements and distinctions are preserved in `research/08-orchestrator-issues-requirements.md:19-133` and its complete returned companion, using the task-root convention below.

## 2. Current State Analysis
### 2.1 Evidence conventions, source key and installation snapshots

**[CODE-VERIFIED - source instruction]** identifies verified normative wording, not automatic enforcement or demonstrated compliance. **[CODE-VERIFIED - implementation]** identifies an implementation traced by the research, not successful live execution. Historical execution reports and issue requests remain records, not proof of present runtime behavior. **[CODE-CONTRADICTED]**, **[STALE DOC]** and **[UNVERIFIED]** retain their stated evidence limits.

This assembly uses the six synthesis indexes and their complete original returns, including all four replacement values nested inside synthesis 02's outer JSON text. It does not independently reopen the underlying archived sources or repeat whole-source validation.

#### Source key

Project-relative paths resolve beneath `REPO`; research-relative paths resolve beneath `TASK/research`. An alias followed by a line number identifies the corresponding file and line in the researched evidence.

| Alias | Location |
|---|---|
| `REPO` | `/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test` |
| `TASK` | `/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115` |
| `RESEARCH` | `TASK/research` |
| `GQ` | `TASK/gaps-and-questions.md` |
| `CORRECTION` | `TASK/synthesis/EVIDENCE-SNAPSHOT-CORRECTION.md` |
| `WC` | `REPO/src/superclaude/core/WORKER-CONTRACT.md` |
| `CORE` | `REPO/src/superclaude/core/CLAUDE.md` |
| `WT-HOOK` | `REPO/src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` |
| `GUARD` | `REPO/src/superclaude/hooks/scripts/launch-level-guard.sh` |
| `JOB` | `REPO/src/superclaude/hooks/scripts/launch-job-identity.sh` |
| `SPEC` | `REPO/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` |
| `D5-REC` | `REPO/.dev/orca-command-refactor/decisions/D5/RECOMMENDATION.md` |
| `APPROVED` | `REPO/.dev/orca-command-refactor/decisions/APPROVED.md` |
| `INF` | `REPO/.dev/reflect/pre-TASK-WF-enforceTheOwnerP-20261108-031809-20261108033529/REPORT.md` |
| `TEST-WC` | `REPO/tests/skills/test_worker_contract.py` |
| `GUIDE` | `REPO/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` |
| `ISSUE-LAUNCH` | `REPO/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` |
| `CLI` | `REPO/src/superclaude/cli` |
| `ORCA` | `/opt/Orca/resources/app.asar.unpacked/out` |
| `HISTORICAL-BUNDLE` | `/opt/Orca/resources/app.asar.unpacked/out/main/chunks/orcad-migration-source-retention-B_-OYaBD.js` |
| `LOCATED-REPLACEMENT` | `/opt/Orca/resources/app.asar.unpacked/out/main/chunks/orcad-migration-source-retention-B-HAVPZ-.js` |
| `DEPTH` | `/opt/Orca/resources/app.asar.unpacked/out/shared/nested-worker-depth.js` |
| `DEV-DELIVERY` | `/home/coder/workspaces/IronOrca/src/main/runtime/orchestration/db/messages/role-mailbox-delivery.ts` |

| Research reference | File beneath `RESEARCH` |
|---|---|
| R01 | `01-contract-authority-model.md` |
| R02 | `02-liveness-and-reporting-stack.md` |
| R03 | `03-orca-mechanics.md` |
| R04 | `04-hooks-guards-identity.md` |
| R05 | `05-precedents-session-launchers.md` |
| R06 | `06-decision-history-and-trigger-evidence.md` |
| R07 | `07-blast-radius-per-option.md` |
| R08 | `08-orchestrator-issues-requirements.md` |
| W01 | `web-01-claude-code-cross-session-messaging.md` |
| W02 | `web-02-hierarchical-orchestration-patterns.md` |
| W03 | `web-03-capability-narrowing-tokens.md` |
| W04 | `web-04-orca-nested-depth-helpers.md` |

Each research reference includes its complete `research/returned/NN-returned-findings.json` or `web-NN-returned-findings.json` companion. Those original investigations remain evidence; later controlling corrections govern superseded statements.

#### Controlling installation-snapshot distinction

The dated correction controls stale current-installation claims in both synthesis indexes and complete originals. It does not invalidate historical observations or establish whole-build equivalence. In particular, the old backend filename must not be replaced mechanically while retaining its historical offsets. **Evidence:** `CORRECTION:8-13,36-47`.

| Evidence class | Established statement | Limit and source |
|---|---|---|
| Project policy: one | D5 retains depth-one policy, a person-opened coordinator and the worker-session fan-out prohibition. | Native capability does not amend policy. `SPEC:405`; `WC:62,69`; `CORRECTION:18-23`. |
| Originally researched installation: one | R03 and W04 recorded source default/fallback one and a filtered stored-value observation of one. Historical build: `1.4.245-aidev02.780594c521aa`, commit `780594c521aaa2399b242b0022045017f4a77436`. | Historical stored data was not loaded-runtime proof and is not a current profile observation. No profile was reopened for the correction. `CORRECTION:20-23`. |
| Newly inspected installed source: two | The 2026-11-09 source observation establishes default/fallback two and guarded legacy-one-to-two migration. | Source contents do not establish effective settings, migration invocation or permission. `DEPTH:10-42`; `CORRECTION:25-34`. |
| Externally reported public baseline: four | W04 attributes default-four and migration behavior to public v1.4.251 material. | External, version-specific context, not a local installed or effective observation. W04; `CORRECTION:23`; external findings are developed in Section 5. |

The bounded new source observations are:

| Surface | Direct source observation | Evidence |
|---|---|---|
| Compiled-output metadata | Version `1.4.245-aidev02.9cfecdd30b2a`; commit `9cfecdd30b2a90c06e5178b1245cb31a97d11bac`. | `ORCA/package.json:5-6`. On-disk metadata, not running-process build proof. |
| Constants | Default maximum two; legacy constant one; root depth zero. | `DEPTH:10-14`. |
| Resolver | Retains numeric safe integers of at least one. Missing, nonnumeric, unsafe, noninteger or below-one input falls back to two. Explicit valid one remains accepted by the resolver. | `DEPTH:26-31`. |
| Migration | Resolves input first. Substitutes two only when `nestedWorkerMaxDepthDefaultedToTwo` is not true and the resolved value equals legacy one; otherwise retains the resolved value. Returns the marker as true. | `DEPTH:34-42`. Helper definition, not execution or persistence proof. |
| Intentional-one case | An intentional one without a true migration marker meets the same condition as legacy default one. Marked one and valid values above one remain; invalid input already resolves to two. | `DEPTH:11-12,26-42`. |
| Default construction | `nestedWorkerMaxDepth` uses the imported default constant; `nestedWorkerMaxDepthDefaultedToTwo` is true. | `ORCA/shared/default-global-settings.js:161-162`. Construction fields, not profile contents. |

The historical bundle's exact path returned no match during the recorded 2026-11-09 correction work. A replacement filename was located, but its existence does not certify equivalent depth enforcement, Task authority, routing, replies, handback, fencing, launch or shutdown behavior. Earlier targeted replacement-build observations remain in their own reports; they are not a repeated whole-build trace. **Evidence:** `CORRECTION:36-42`.

Consequently, all installed-mechanics tables and diagrams below describe **the original researched snapshot**, except for the explicitly dated depth-source observations above. They retain R03's attributed historical investigator observations, not a claim that this report independently reproduces every original source span. Narrow original tool results recovered during the Phase-6 correction support specific findings, but are not a complete historical bundle or ordinary-launch trace. `qa/qa-fix-log.md`, **FR-01/P01-P14**, records exact retained excerpts, original build/path, tool-result times and excerpt hashes. Historical `CODE-VERIFIED` labels throughout identify the original investigator's source reading; independent reproducibility extends only to the retained spans. Original offsets remain historical, and carrying them forward does not pass replacement-build route or exact-topology conditions. **Evidence:** R03 and its immutable return; `CORRECTION:42-51`; `qa/qa-fix-log.md`.

### 2.2 Contract and role model

**[CODE-VERIFIED - source instruction]** The contract places a person-opened coordinator above supervised workers. It does not define a worker that inherits coordinator authority. **Evidence:** `WC:11,60-69`.

| Boundary | Current rule | Meaning for the proposed role | Evidence |
|---|---|---|---|
| Worker identity | A live worker preamble carries Task and Dispatch IDs. User-started sessions are ordinary sessions. | Being unattended or inside Orca is not worker identity. The ordinary-session clause does not expressly classify every agent-launched nonworker. | `WC:11`. |
| Coordinator eligibility | Coordinator means an Orca coordinator session the person opened. | An agent-launched middle owner is not expressly admitted. | `WC:69`. |
| Command mode | Standalone `--unattended` selects the mode; commands do not detect Orca, the preamble or environment. | D1 concerns explicit mode selection, not a ban on every other command flag. | `WC:12-14`. |
| Command-side boundary | WC-8 names `worker-start`, `dispatch` and `task-create`; the opening separately says commands contain no Orca calls. | The shorter verb list is not a general exception for other Orca operations. | `WC:5,40`. |
| Worker-session fan-out | WC-13 prohibits those three routes, low-level dispatch, `worktree create --agent` and `agent launch`, at any depth setting. | Moving the call outside the command, changing the role name, opening another Run or raising native depth does not amend policy. | `WC:62`. |
| Internal helpers | Assigned commands run in the top-level worker session and may retain their own Agent-tool fan-out. Only the top-level worker sends lifecycle messages. | Helpers are not additional Orca lifecycle owners. | `WC:60`. |
| Visible-copy guard | The worker checks command copies it will actually see; mismatch or never-as-worker status causes refusal before work. | Source-tree conversion alone does not establish deployed eligibility. | `WC:16-23,216`. |
| Command chains | Several prewritten `Command:` lines may run continuously with handoffs. Task text never begins with `/sc:` because each command is a labelled `Command:` line (`WC:204`). A worker ends its turn only after `worker_done`, while blocked in the preamble's `ask`, or on `consumer_fenced`; the one exception is a coordinator interrupt that asks for a handoff (the S6 nudge), after which it ends its turn without `worker_done` (`WC:63`). | A chain does not authorize discretionary planning and dispatch of child Orca work. | `WC:63-64,204-216`. |
| Task ownership | A coordinator starts only Tasks it created. | Another coordinator's ready Task is not available for silent claiming. | `WC:246`. |
| Result admission | Failed or blocked results do not feed dependents. Partial usability requires an explicit decision; dependents follow admission. | Completion transport and permission to use a result differ. | `WC:239-246`. |

```text
Current source-instruction model
(not automatic enforcement)

Person-opened coordinator
    |
    +-- creates and owns Tasks
    +-- supervises workers
    +-- reads and admits results
            |
            +-- top-level worker
                    |
                    +-- runs assigned Command: lines directly
                    +-- retains each command's internal Agent helpers
                    +-- alone owns heartbeat / ask / check / worker_done
                    +-- reports newly discovered external work upward
                        rather than launching it
```

**Evidence for the diagram:** `WC:11,60-69,204-246`; R01:31-150.

Authority remains divided rather than inherited:

| Authority or safety boundary | Retained rule | Evidence |
|---|---|---|
| Local commit | Exact quoted human instruction for that Task, sole occupancy of the Orca child worktree, and succeeded command result are required. Grant ends at Task completion. | `WC:41-45,233`. |
| Human Ruling | Only the person gives a Ruling; an agent-written or relayed draft is not acceptance. | `WC:57,250-269`. |
| Frozen implementation | Halted worktree, baseline, handback and resume restrictions remain. | `WC:250-269`. |
| Outward work | Authorized coordinator retains outward actions, merge-back, cleanup and publication under the specified human-instruction conditions. | `WC:224-235`. |
| PR submission | Ordinary top-level session, not a dispatched worker. | `WC:229-235`. |
| Protected state | Worktrees, unread reports, unfinished ledgers, frozen plans and overlapping writers remain protected. | `WC:47,225,234,250-253`. |
| Fan-in | Inputs must be settled and admitted; merge ceiling is ten inputs and minimum is two admitted inputs. | `WC:273`. |

[CONTRADICTION: The ownership wording recorded in `CORE:52-59` and the worktree-hook explanation names “a coordinator under another orchestrator.” The same current guidance preserves supervised-worker restrictions, while `WC:62,69` prohibits worker-session fan-out and defines a person-opened coordinator. The ownership phrase supplies no subordinate eligibility, brief, upward protocol or grant. `INF:77-78` explicitly excluded supervised workers and deferred WC-13; that scope record explains but does not resolve the rule defect.]

R01's complete clause-by-option and section-4 matrices are retained in its original return, §§5.2-5.7. Their compatibility cells are not live passes. The decision-facing worker and coordinator duty matrices appear in Section 6.

### 2.3 Liveness and reporting

**[CODE-VERIFIED - source instruction]** The shipped supervision procedure distinguishes existence, semantic progress, questions, person prompts, reporting and admission. It is not an automatically executed state machine. **Evidence:** `WC:46-65,95-200,239-246`; R02:26-136.

#### Signals and records

| Signal or record | Meaning and required handling | Source |
|---|---|---|
| Heartbeat | Carries command index, on-disk progress counter and declared silence window. An unchanged token shows existence, not semantic progress. | `WC:65`. |
| Semantic progress | Substantive token, contract-file or transcript change; message arrival and identical rereads do not qualify. | `WC:110-114`. |
| Long step | Declared silence defers nudges and typed text, not read-only probes. An accepted internal-helper heartbeat gap is not death evidence. | `WC:46,120`. |
| Question | Uses the brief's blocked-gate policy and eligibility test; at most one per Task. Timeout resumes the same question ID. Rulings are excluded. | `WC:53-58`. |
| Completion | Own top-level `worker_done` exactly once. Status, handoff or reply is not completion; coordinator must not synthesize it. | `WC:59-60,108`. |
| Application acknowledgment | `applied`, `queued` or `refused` acknowledgment tied to message ID. Different from Delivery-batch receipt. | `WC:61,131-138`. |
| Delivery batch | Whole FIFO batch is handled and recorded before acknowledgment. Wake-type selection does not permit discarding other returned messages. | `WC:103-106`. |
| Attempt identity | Lifecycle and control messages are checked against current Task and Dispatch IDs; mismatches are quarantined. | `WC:106`. |
| Return contract | Result and artifact references are read before admission. | `WC:32-39,239-246`. |
| Handoff | At most 40 lines after each command, preserving command, lifecycle IDs, status, deliverables, decisions, applied IDs and next command. | `WC:64`. |
| Run notes | Preserve message handling, timing, lineage budgets, admission and runtime-split cost evidence. | `WC:97,104,146-179,242,246`. |

#### Twelve procedural states

| State | Classification and response | Source |
|---|---|---|
| S0 - Starting | Missing token/transcript after startup grace: probe, bounded beginning nudge, then human report. | `WC:118`. |
| S1 - Progressing | Recent token and semantic change: observe. | `WC:119`. |
| S2 - Long step | Declared silence or recent transcript activity: retain probes and defer typed intervention as specified. | `WC:120`. |
| S3 - Idle at prompt | Unchanged token, old final turn, empty prompt, no tool and no pending ask: bounded intervention; restart needs separate proof; a third idle episode goes to L5. | `WC:121`. |
| S4 - Person prompt | Capture the screen and report to the person (L5) at five minutes plus Orca's own delay, re-reported every fifteen minutes; never answer it. | `WC:122,155`. |
| S5 - Blocked in ask | Answer through the question path and follow the acknowledgment timeline. | `WC:123`. |
| S6 - Context exhausted | Matching screen evidence twice five minutes apart; use the handoff interrupt and permitted recovery path. | `WC:124`. |
| S7 - Unreachable | Report continuous `unverifiable`; do not restart solely for it. | `WC:125`. |
| S8 - Exited | Settle under WC-6 before restart or escalation. | `WC:126`. |
| S9 - Finished but unreported | Read the final-command contract, nudge for actual completion, then escalate. A `status` that names a report path or says the work is complete sets S9 only when the brief has no later `Command:` line; otherwise it is logged. | `WC:108,127`. |
| S10 - Settled | Completion received; no further liveness action under this state. | `WC:128`. |
| S11 - Unknown | Probe stale or unknown deciding evidence; do not type. | `WC:129`. |

#### Timing, response and acknowledgment limits

**Starting-value qualification:** Every time and cap in the v1 liveness rules is a starting value, not a measured one. The coordinator records the values it uses in run notes; a brief may override them, but a worker may not. A lineage is the original Task plus every replacement. **Evidence:** `WC:97,146`.

| Procedure | Stated boundary | Interpretation |
|---|---|---|
| Sweep | After wake/timeout, at most once per five minutes. | Starting value, not a measured detection guarantee. `WC:97,110-114`. |
| Deadline W | `max(10 min, 2 x the observed median heartbeat interval)`, or the worker's declared `expect_silence_min`, capped at 45 minutes. | Declared silence defers nudges and typed text, not read-only probes. `WC:112,120`. |
| No-progress response | Startup grace ten minutes; probe after ten minutes without semantic change; named state or L5 report by fifteen minutes after the last semantic change; unreachable report after ten minutes of continuous `unverifiable`. | Prescribed procedure, not demonstrated universal compliance. `WC:114`. |
| Response ladder | L0 observation, L1 probing, L2 nudging, L3 typed question, L4 proof-gated restart, L5 human escalation. | L0 has no cap; a person-only state, any cap reached or an exhausted ladder goes to L5; an S4 person prompt is re-reported every fifteen minutes. `WC:146-157`. |
| L1 probe | Read-only after a trigger; every sweep, at most two costly probes per triggered worker per sweep. | Costly probes are transcript tails and screen reads, not an unrestricted polling budget. `WC:110,151`. |
| L2 nudge | L1 confirms S3, S9 or S6 at an identified prompt; one per incident, two per lineage. A nudge with no turn start still counts. | Typed with `--wait-submit`; the S6 variant is an interrupt plus a handoff request. `WC:152`. |
| L3 ask | After L2 failed once and the state is still ambiguous: "Reply with `status`: current step, what you are waiting for". One per incident. | A typed status question, not permission to answer a person prompt. `WC:153,182-188`. |
| L4 restart | Only with an Orca stall proof, or person-directed cancellation with confirmed quiescence under WC-6 (no tool running, no input accepted, and two reads five minutes apart that agree); one per rolling 60 minutes, two per lineage. WC-6's three-failed-starts rule also applies, whichever is stricter. | Positive proofs are `exited`, process exit, or a transcript whose final agent turn sent no `worker_done`; nudges, asks, heartbeats, identical reads and context exhaustion are not stall proofs. `WC:75-79,154,157`. |
| Restart cause restrictions | Cause classes: `idle`, `context-exhausted`, `exited`, `unreachable-then-exited`. The same class twice means no plain restart. | For `context-exhausted`, the next Task reduces load by splitting `Command:` lines or narrowing inputs, or the coordinator goes to L5. `WC:159`. |
| Pending acknowledgment | Five-minute probe when needed; one conditional typed copy only at a positively idle prompt; human escalation at fifteen minutes. | Not a repeated resend loop. A duplicate acknowledgment is a harmless no-op, and an acknowledgment does not prove the answer was right. At settlement an unresolved pending acknowledgment closes as `unacked-at-settlement`, which is not evidence that the answer was applied. `WC:131-159`. |
| Silence | No stop, retry, release, failure marking, person answer, Ruling or forged lifecycle solely from silence, deadlines, exhaustion or `unverifiable`. | Non-destructive handling remains binding. `WC:73-79,157-192`. |
| Retry | New Task and report directory only after proper settlement of the earlier attempt. | Parent replacement does not erase predecessor state or caps. A restart's resume note sits after the guard line and before the `Command:` lines; the new Task gets its own report directory and the old one is read-only input; `/sc:implement`'s own `E-RESUME-NEEDED` re-run takes priority. The note carries the replaced Task and Dispatch IDs, lineage, completed `Command:` lines and contracts, the last progress token, the latest handoff file, applied answer IDs, uncertain effects, the load rule and the `Start at: Command:` line. `WC:73-79,167-179`. |

**Additional coordinator message-handling and sweep rules** (recovered from R01 §5.4-5.5 and R02 §§3-6). Contract rows carry R02's tag **[UNVERIFIED as runtime-enforced behavior]**: they are source-instruction wording, not demonstrated execution. The heartbeat-reconciliation row is **[CODE-VERIFIED]** only for the inspected Orca development checkout, which was not shown to match any installed build.

| Procedure | Stated boundary | Source |
|---|---|---|
| Escalation message | An `escalation` gets L1, then L5. | `WC:108`; R02 §4. |
| Unknown message type | The sender goes to S11 and the message is shown to the person; it is never silently acknowledged. | `WC:105`; R02 §4. |
| Heartbeats around an ask | No heartbeat is sent while blocked in `ask` (or `check --wait`); when `ask` returns, the worker sends one heartbeat at once. | `WC:58,65`; R02 §§4,6. |
| Heartbeat record reconciliation | In the inspected development checkout, heartbeats from an inactive Dispatch are suppressed, unauthorized senders are rejected, and heartbeat time is recorded only for the identified Dispatch. | R02 §3.1, `A-HEARTBEAT:119-162` (alias defined with the helper-route table in Section 2.4). |
| Liveness `stat` scope | Each sweep's `stat` reads only the worker's own contract path and report directory. | `WC:47,110`; R02 §6.3 (C-17). |
| Sweep accounting | One `worker-list`, one prompt-wait listing (`worktree ps --agent-wait`) and one `stat` per worker contract path, updating each worker's heartbeat record (arrival time, progress token, declared window). | `WC:110`; R02 §5. |

**[CODE-VERIFIED - implementation, development checkout]** The inspected Delivery implementation replays outstanding batches, fences mismatched consumer generations, separates wake-type checks from FIFO selection, and acknowledges a batch's IDs together. Duplicate acknowledgment is harmless. These are findings about `DEV-DELIVERY:27-169`, not whole development/installed equivalence.

**Research-record distinction:** R02 maps eight #431 incident families to the newer procedures and records PR #434 as a merged v1 contract-and-test response. It does not establish incident elimination. C1-C8 and C15-C17 remain represented; C9 was deleted; future C10-C14 monitor, hook, dashboard, context and persistent-budget proposals are not assumed delivered. **Evidence:** R02:100-136 and complete return, §§3-8.

**Historical incident observations (issue #431, research record).** R02 §8.1 records, as **[UNVERIFIED — historical runtime observations]**, eight reported cases from a run with six workers; the issue was OPEN in the fetched GitHub record (https://github.com/IronbellyOrg/IronClaude/issues/431). They are historical issue observations from the research. They were not reproduced here, and the right column names the contract response now present, not a claim that the procedures eliminate the case.

| # | Reported historical case | Corresponding contract response now present | Source |
|---|---|---|---|
| 1 | Timer heartbeats continued during context thrashing. | Progress token, independent transcript and screen probes, S6. | `WC:65,113,124`. |
| 2 | A worker ended a turn and sat idle for hours. | S3, bounded nudge/ask ladder, continuous-chain requirement. | `WC:63,121,152-153`. |
| 3 | One recent file modification was mistaken for current activity. | Scoped contract `stat` plus multiple evidence sources; substantive semantic-change definition. | `WC:47,110-113`. |
| 4 | A closing report sent as `status` was missed by a narrow wait. | All-types wait, S9 catch, completion only as `worker_done`. | `WC:59,101-108,127`. |
| 5 | Mailbox answers were not acted on for 35-40 minutes. | Application acknowledgment and the A1-A4 timeline, one conditional terminal copy. | `WC:61,131-138`. |
| 6 | A permission prompt was discovered late. | `agentWait`, screen capture, S4 and human escalation. | `WC:122`. |
| 7 | Workers stopped between chained steps. | WC-14, the chain brief line, handoff files. | `WC:63-64,210-213`. |
| 8 | A replacement worker repeated context exhaustion. | Bounded reads, cause classes, load reduction on a context-exhausted retry. | `WC:64,159,167-179`. |

The current instructions remain worker/command-oriented. They do not define a supervisor's own-versus-child progress, aggregate outcome, subtree admission checkpoint or complete child roster for recovery. Child completion is not parent completion; acknowledgment at one edge does not prove application at the next. **Evidence:** `WC:59-65,239-246`; R02:85-132.

### 2.4 Orca mechanics: historically traced routes and bounded new depth source

The route tables and diagrams in this subsection retain **[CODE-VERIFIED - implementation, historical installed snapshot]** as R03's original investigator classification. Phase-6 recovery found original-build tool-result excerpts, not the full bundle: depth/authority selections **P01/P02/P08-P10/P12**, local creator constraints/routing **P03-P05/P13-P14**, and reply/handback bodies **P06-P07**, all in `qa/qa-fix-log.md`. These make the selected source bytes independently inspectable. They do not reproduce every caller/callee edge or the complete ordinary-launch absence claim; **P11** retains only part of that launch chain. Uncovered conclusions remain attributed historical observations, not independently reproduced primary-source findings. The original path/offsets and historical findings are preserved; no replacement-build or live certification follows. The bounded new depth-source observations remain separate in Section 2.1. **Evidence:** R03:28-177 and its immutable return; `CORRECTION:8-13,36-51`; `qa/qa-fix-log.md`, FR-01.

#### Depth and authority are separate

| Examined route | Historical source result | Qualification and evidence |
|---|---|---|
| Local `worker-start` | Depth-fenced. Handler supplies caller identity/runtime maximum; creation resolves child depth before transaction commit. | Refusal rolls back the transaction. `HISTORICAL-BUNDLE:640,2589-2597`. |
| `dispatch` | Depth-fenced through Dispatch creation. | Historical creation trace; `HISTORICAL-BUNDLE:2698`. |
| Low-level dispatch with injection | Same creation path; injection follows creation. | `HISTORICAL-BUNDLE:2698`. |
| Dispatch dry-run | Explicitly resolves child depth before returning preview. | `HISTORICAL-BUNDLE:2698`. |
| `task-create` | No nested-depth check on the inspected path. | Independent coordinator authority and Run relationship checks remain. No depth check does not mean worker permission. `HISTORICAL-BUNDLE:388,2698`; R03:133-150. |
| Worktree creation with agent | General workspace/agent launch, not Dispatch creation. | General launch or older-host fallback on the examined path. `ORCA/cli/handlers/worktree-create-agent-launch.js:13-61`. Historical observation. |
| Ordinary agent launch | Does not automatically create Run, Task, Dispatch or worker preamble on examined paths. | `ORCA/cli/handlers/agent-launch.js:11-33`; `ORCA/cli/agent-launch-request.js:79-103`; R03 backend trace. Historical observation. |
| New Run or Run binding | Does not reset caller delegation depth. A worker cannot bind its own or an ancestor Run and cannot take over a Run; Run authority ancestry is derived by walking the active Dispatch `creator_dispatch_id` chain. | Run ownership/takeover are separate checks. `HISTORICAL-BUNDLE:383-388`; refusal also in the development checkout, R02 §3.1 `A-BIND:44-72` (alias defined below). |

The historical depth helper accepted safe integers of at least one, defaulted invalid input to one, and used root depth zero. The bounded 2026-11-09 replacement-source observation now establishes default/fallback **two**, retained explicit valid one, and guarded legacy-one migration. Neither observation proves the effective loaded maximum. Raising a finite maximum is not disabling its fence. **Evidence:** historical R03 depth trace; current `DEPTH:10-42`; `CORRECTION:20-34`.

**Additional depth-resolver cases** (R03 §§1 and 7, historical trace of the researched build, **[CODE-VERIFIED - implementation, historical installed snapshot]**; the last two rows carry R03's tag **[CODE-VERIFIED within the registered CLI surface]** or the control observation). These are bounded historical observations. They are not current-setting observations, and no equivalence is claimed for the replacement build (`CORRECTION:36-42`).

| Case | Historical source result | Evidence |
|---|---|---|
| Creator depth resolution | Creator depth comes from the active Dispatch depth and the applicable remote-attachment depth (`O4e`, registered as `resolveCreatorDepth`). Absence of any such delegation yields zero, and a `system` creator yields zero. | `HISTORICAL-BUNDLE:383`. |
| Creator is its own assignee | A Dispatch whose creator is its own assignee is bookkeeping and does not count as delegation (`mU` and `O4e`). | `HISTORICAL-BUNDLE:383`. |
| Multiple live remote attachments | One terminal matching multiple live remote attachments gives an ambiguous-parent refusal (`gU` throws `AmbiguousDispatchParentError`). | `HISTORICAL-BUNDLE:385-388`. |
| `worker-start` with remote placement on | Fenced at the Run home: `D5e` calls `createStartingWorkerDispatch` with the caller identity and runtime maximum before remote attachment. The ordinary worker-helper path separately rejects `--on`. | `HISTORICAL-BUNDLE:628`. |
| Legacy internal coordinator dispatch loop | Uses the depth-checked creation method with a `system` creator and the configured maximum. It is not the normal supported helper workflow. | `HISTORICAL-BUNDLE:2698`. |
| Desktop depth-setting control | A renderer control validates the same range and calls `updateSettings({nestedWorkerMaxDepth:…})`. It is integer-only with minimum one and no explicit maximum in that control. | `ORCA/renderer/assets/Settings-D8mQKKOP.js:4`; R03 §7. |
| CLI depth-setting surface | A bounded inspection of the registered CLI specifications found no nested-depth setting verb or flag. | `ORCA/cli/specs/index.js:32-60`; R03 §7. |

Transaction wording matters: R03 traced resolution **before commit with rollback on refusal**, not necessarily before transaction entry. **Evidence:** `HISTORICAL-BUNDLE:2589-2597`; synthesis 02 S37.

#### Native local helper flow in the researched snapshot

R03 established a same-Run helper path recording creator Dispatch and default parent Task, with same-host/new-agent constraints. Another Run, the inspected remote placement and reuse of another terminal were rejected on that local route. Helper instructions were offered only below the configured maximum. **Evidence:** `HISTORICAL-BUNDLE:640`; R03:62-81.

```text
Historical native local-helper source
(capability, not IronClaude permission or replacement-build certification)

Run
  |
  +-- creator Dispatch M
          |
          +-- helper Task / Dispatch W
                  |
                  +-- default reports and questions
                              |
                              v
                      Dispatch M mailbox
                      also receives coordinator follow-ups

If creator Dispatch is no longer active:
    new reports --------------------------> Run
    selected unread reports/questions ----> Run
    old outstanding deliveries are fenced
```

| Routing or handback property | Historically established behavior | Evidence |
|---|---|---|
| Creator selection | Same-Run creator must be pending or dispatched; otherwise recipient falls back to Run. | `HISTORICAL-BUNDLE:640`; R03:62-81. |
| Questions | Default ask uses creator selection; explicit owning-Run addressing may target the coordinator instead. | `HISTORICAL-BUNDLE:2698`. |
| Replies | Reply path recognizes the addressed active creator Dispatch. | `HISTORICAL-BUNDLE:2698`. |
| Reports | Installed send trace established creator-directed reporting, including exact-Dispatch completion and heartbeat routing. | R03 complete returned send trace. |
| Settlement handback | Selected unread `worker_done`, `escalation`, `status` and pending questions return to Run; old deliveries are fenced. | `HISTORICAL-BUNDLE:1267-1275`. |
| Excluded from selected unread-report list | Heartbeat. | Same handback trace. |
| Limit | Selected-mail handback is not complete supervision takeover or descendant quiescence. | R03:64-81,152-164; R02 dual-role analysis. |

**Additional helper-route properties.** *Historical* rows are R03's observations of the researched build (`HISTORICAL-BUNDLE`, **[CODE-VERIFIED - implementation, historical installed snapshot]**). *Development checkout* rows are R02 §3.1 findings, **[CODE-VERIFIED]** in the inspected Orca development checkout beneath `/home/coder/workspaces/IronOrca/src/main/runtime/` (the checkout of `DEV-DELIVERY`). The aliases are: `A-START` = `rpc/methods/orchestration/worker/worker-start-authority.ts`; `A-ROUTE` = `orchestration/dispatch-report-mailbox.ts`; `A-SEND` = `rpc/methods/orchestration/messaging/send-methods.ts`; `A-ASK` = `rpc/methods/orchestration/messaging/ask-methods.ts`; `A-ANSWER` = `rpc/methods/orchestration/messaging/helper-question-answerer.ts`; `A-BIND` = `orchestration/db/runs/worker-run-binding.ts`; `A-HEARTBEAT` = `orchestration/lifecycle-reconciliation.ts`. R02 marks this source trace **[UNVERIFIED]**: it was not exercised against the running application, and the development checkout must not be assumed to be the source revision of any installed build. No row is a current or live behavior claim for any other build.

| Property | Finding | Basis and evidence |
|---|---|---|
| Reuse of an existing Task | A helper start may reuse an existing Task only if it was last run/dispatched by that creator's helper; otherwise it is rejected. | Historical `HISTORICAL-BUNDLE:640` (`ott`); development checkout `A-START:50-69`. |
| Required-creator mismatch | `requiredCreatorDispatchId` is compared with the caller's currently resolved creator Dispatch; a mismatch throws `consumer_fenced`, a consumer-fenced refusal. | Historical `HISTORICAL-BUNDLE:2591`. |
| Creator-directed report types | The creator-directed set is the unspecified/default type, `worker_done`, `heartbeat`, `escalation` and `status`. `decision_gate` is not in it and does not become delegated approval. | Historical `HISTORICAL-BUNDLE:640` (`vet`); development checkout `A-ROUTE:4-12`. |
| Manually sent `question` | Not every message type uses the helper default; manually sending a `question` type is not the blocking `ask` workflow. | Historical `HISTORICAL-BUNDLE:640`. |
| Completion and heartbeat routing | For `worker_done` and `heartbeat` with a resolved Dispatch, routing comes from the active Dispatch even when an explicit recipient was supplied. | Historical `HISTORICAL-BUNDLE:2677`; development checkout `A-SEND:143-153`. |
| Blocking ask resume | The ask handler resumes only the active Dispatch's question. | Development checkout `A-ASK:91-137`. |
| Answer validation | `answerQuestion` validates the answering Dispatch and its consumer generation; the active Dispatch to which a helper's question was addressed is recognized as an eligible answerer. | Historical `HISTORICAL-BUNDLE:1288-1291`, `HISTORICAL-BUNDLE:2698` (`Kut`); development checkout `A-ANSWER:7-37`. |
| Heartbeat reconciliation | Heartbeats from an inactive Dispatch are suppressed, unauthorized senders are rejected, and heartbeat time is recorded only for the identified Dispatch. | Development checkout `A-HEARTBEAT:119-162`. |

This source evidence corrects the older universal root-Run prediction **for the historical native local route**. Live behavior and replacement-build equivalence remain separate. **Evidence:** R03:62-81; `CORRECTION:42-47`.

#### Distinct kinds of parentage

| Relationship | Historical source representation | What it does not establish | Evidence |
|---|---|---|---|
| Workspace lineage | Parent worktree/instance identifiers, with ID, host-boundary and instance validation. | Worker lifecycle authority. “Merely cosmetic” understates the validation. | `ORCA/shared/resolved-worktree-lineage.js:10-22`; R03:83-116. |
| Task hierarchy | Parent ID, Run membership and creator provenance. | Dispatch depth by itself. | R03:83-116 and full return. |
| Dispatch hierarchy | Creator Dispatch, retry ancestry, depth and consumer generation. | Human approval or inherited outward authority. | R03:83-116 and full return. |
| Run ownership | Coordinator identity and consumer generation; no direct parent-Run field in the inspected field set. Run authority derives ancestry through the creator-Dispatch chain (`M4e`/`vU` walk the active Dispatch's `creator_dispatch_id` ancestry to reject coordination of the worker's own or an ancestor Run). | A complete ordinary-owner upward supervision contract. | R03:98-116; `HISTORICAL-BUNDLE:388`. |

The historically inspected CLI exposes nine supported **message types**: `status`, `dispatch`, `worker_done`, `merge_ready`, `escalation`, `handoff`, `decision_gate`, `question`, `heartbeat`. They are not all settlement messages; arbitrary body labels do not add transport types or lifecycle semantics. **Evidence:** `ORCA/cli/specs/orchestration.js:73-80`; R03:170-177.

[CONTRADICTION: The blanket CLI/help description recorded in R03:170-177 says an active Dispatch's omitted recipient defaults to its owning Run. R03's historical implementation trace selects an active same-Run creator Dispatch for native local helpers, with Run fallback. The report retains this as a historical help-versus-implementation discrepancy, not proof that the replacement build retains either behavior.]

The version-matched guide inspected by R03 distinguished coordinator, dispatched worker, handoff owner, compatibility operator and ordinary terminal agent. A handoff owner used ordinary launch without supervision records; its no-monitor instruction was guide policy, not an automatic runtime prohibition. The remote/federated helper recipe was separate from the local same-Run recipe. **Evidence:** R03:28-177 and its complete return; the actual guide/reference/help acquisitions and selected retained output are recorded in Section 10.9, **A01-A16**. Those are historical retrieval records, not commands executed during this correction or current-guide verification.

### 2.5 Hooks, guards and identity

**[CODE-VERIFIED - implementation]** The three hooks inspect different inputs and enforce different conditions. None of the inspected bindings implements a coordinator/worker/parent/resource/action delegation model. **Evidence:** R04:38-79,87-146; `WT-HOOK:6-61`; `GUARD:185-203,254-271`; `JOB:2-18,424-481`.

| Mechanism | Actual input or binding | Established limit |
|---|---|---|
| Worktree-agent requirement | Bash command scanner tracks positional words, agent flags and help flags. | Agent syntax is not permission to create a worktree. Creator ownership and no-self-use remain instructions. |
| Launch-level guard | Validated top-level session identity and accepted launch-level binding record. Accepted level words are `worktree`, `full` and `full-submit`; a malformed or unreadable record selects the strictest level. | Launch levels are not orchestration roles or scoped parent grants. The parsed envelope and record carry no role, parent-owner, depth or delegation-scope field, so an arbitrary new role word in the record would currently invoke the strict fallback rather than grant a role. `GUARD:185-203,254-270`; R04 §§1-2. |
| Bash-job identity adapter | Validated session/tool envelope and governed state, followed by Bash-input rewrite. | Supported Linux same-user execution identity, not hierarchy authority or sandboxing. |

The worktree hook prints its ownership explanation after deciding to deny a bare creation. Its declared interpreter, subprocess, script, non-Bash and dependency/scanner ceilings belong to that hook; they must not be transferred to every hook. A quoted prompt value equal to the agent flag can also satisfy its lexical agent check. **Evidence:** `WT-HOOK:6-14,29-61,94-103,342-357`.

#### B1 - Literal-executable recognition ceiling

The launch classifier takes the executable basename and enters its Orca branch for literal `orca`. The `orca-ide` spelling observed by R03 does not match that branch. Other classifications may still deny a command; the mismatch is neither policy permission nor demonstrated live bypass. **Evidence:** `GUARD:450-478`; controlling R04:87-107.

| Recognized exception family | Listed forms | Evidence |
|---|---|---|
| General | Status, help, version. | `GUARD:475-478`. |
| Worktree | Current, list, show. | Same exception list. |
| Terminal | List, show, read. | Same exception list. |
| Orchestration | Check, inbox, run-current, task-list, worker-show. | Same exception list. |
| Trailing help | Specified help case. | Same classification branch. |

Other recognized pairs become ESCAPE, denied at every governed level, including approved-worktree and full-submit. An agent flag does not override that independent classification. **Evidence:** `GUARD:475-478,724-737`.

#### B2 - Required supervision probes are not blanket read exceptions

| Required operation | Contract duty | Result for recognized `orca` in a positively bound session |
|---|---|---|
| Worker enumeration | After empty waits and during sweeps. `WC:107,110`. | `worker-list` is unlisted and falls to ESCAPE. |
| Worker transcript read | L1 probe. `WC:151`. | `worker-read` is unlisted and falls to ESCAPE. |
| Worktree process/prompt-wait listing | Sweep duty. `WC:110`. | `worktree ps` is unlisted and falls to ESCAPE. |

**Evidence:** `GUARD:475-478`; R04 B2:93-107.

Thus the existing supervision sweep cannot run unchanged through those forms in a bound session. A person-opened peer is not automatically unbound, and retaining two tiers does not solve this integration defect. Launch, upward reporting and required supervision probes are separate policy surfaces; no expansion is authorized here. **Evidence:** R04:93-107; R07:188-194.

| Additional guard or adapter property | Meaning and limit | Evidence |
|---|---|---|
| Local/background Agent or Task branch | Does not itself assign ESCAPE; remote isolation does. The branch does not inspect prompt content. | `GUARD:681-687`. |
| SendMessage, Workflow, RemoteTrigger | Classified ESCAPE. | Same branch evidence. |
| Unbound session | Declared fail-open path is absence of this enforcement, not a worker-contract exemption. | `GUARD:390-395`. |
| Job adapter | Linux same-user identity, not sandbox; whole-input rewrite ordering unspecified; fresh-shell model does not supply persistent working-directory semantics. An existing session-record file is not rewrite authority; job identity is not inferred from agent ID, parent fields, working directory or environment, and checking an agent field's type is not role recognition. Killing the process supervisor leaves unknown execution state, and Monitor and pipeline execution are unsupported. | `JOB:2-18,424-481` (record `JOB:435-445`; identity inputs `JOB:429-450`). |
| Registration and installation | Three hooks have source-visible registration and installer inclusion. | `src/superclaude/hooks/hooks.json:105-133`; `CLI/install_hooks.py:86-93`. Registration is not successful live child enforcement. |

R04's embedded B1/B2 correction controls categorical older returns and their dependent R05/R07 summaries. U7's preamble/event visibility and U28's installation question remain distinct. **Evidence:** R04:87-107,167-176; R07:188-194.

### 2.6 Session-launch precedents

**[CODE-VERIFIED - implementation or explicitly identified source instruction]** Existing launchers offer useful components, but the inspected paths do not establish the complete relationship “receive an upper supervised assignment, supervise external children, return an admitted aggregate upward.” **Evidence:** R05:40-75 and complete fourteen-launcher/56-cell reuse matrix.

| Precedent | Established mechanism | Meaning and limit | Evidence |
|---|---|---|---|
| L1 - Issue claim external agent | Intentional two-stage create, prepare/pending record, then ordinary agent launch. The published launch-level word is `worktree`, `full` or `full-submit`; the child template delegates planning, implementation or opt-in commit/push/PR submission respectively, and the child never merges (template behavior **[UNVERIFIED: runtime]**). | Launch-level/receipt mechanism, not upper Task completion or subordinate authority. Claim-process preflight is not child-environment proof. | `ISSUE-LAUNCH:666-681,1300-1355`; level words `ISSUE-LAUNCH:1332-1336`; template `src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md:18-34`. |
| L2 - Issue lookup/drafting helpers | Narrow Agent assignments, returned artifact paths, one missing-output retry. | Internal specialists; skill retains GitHub/ClickUp mutations. Not Orca Dispatch supervision. | `src/superclaude/skills/sc-issue-protocol/SKILL.md:54-76`; R05:44-61. |
| L3 - Issue-watch | Valid claim prompt and ordinary launch argv in configured worktree; outcome returns to program. The origin check requires the fork; disabled, day-cap and deadline checks precede launch; pending state is saved before launch; the cycle records launched, unknown or spawn-error outcomes with audit lines (conservative treatment of a lost launch reply); candidate processing stops after a launch-step outcome. | Watcher/claim/agent process chain, not continuous upper-coordinator supervision. The launch-reply fields assumed for the installed Orca are **[UNVERIFIED]** (Q43). | `CLI/issue_watch/launch.py:84-116,233-251,326-370`; `CLI/issue_watch/cycle.py:812-834,1061-1112,1180-1210`. |
| L4 - PR session | Ordinary top-level carriage; attended main-session monitor. | Separate session boundary, not supervised middle worker. | `WC:229-235`; `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:36-49`; R05 source register. |
| L5 - PM | Specialist and parallel-phase orchestration instructions. | Workflow delegation, not concrete nested Orca authority/reporting. | `src/superclaude/skills/sc-pm-protocol/SKILL.md:56-84`; R05 source register. |
| L6 - Spawn | Explicit stopping boundary after decomposition. | Task hierarchy/assignments, not persistent-session execution. | `src/superclaude/commands/spawn.md:176-210`; R05 source register. |
| L7 - Agent | Current-session ownership and helper guidance. | Internal assistance, not defined external middle role. | `src/superclaude/commands/agent.md:23-50`; R05 source register. |
| L8 - Sprint phase | Configured Claude process polling with file-backed outputs/errors. | Program supervision, not delegated Orca coordinator identity. | `CLI/pipeline/process.py:140-218`. |
| L9 - Sprint task | Dependency waves, bounded thread pool, subprocesses, watchdogs, result collection and atomic handoff. | Reusable scheduling/durability; resume success requires task and gate success. | `CLI/sprint/executor.py:1328-1335,1683-1723,2126-2146`; `scheduler.py:85-104`; `handoff.py:35-66`. |
| L10 - Narrative helper | One-turn subprocess, timeout, empty-text failure fallback. | Bounded narrative work, not repository ownership; bypass invocation is not safe-authority precedent. | `CLI/sprint/summarizer.py:310-367`. |
| L11 - Checkpoint rerun | Narrow CLI recursion suppression and exit handling. | Scoped process delegation, not nested coordinator; shown subprocess has no timeout argument. | `CLI/sprint/rerun_tasks.py:1375-1387,1701-1719`. |
| L12 - Sprint tmux | Foreground child, recursion suppression, shared state directory. | Process packaging and exit coordination, not agent-side upward reporting. | `CLI/sprint/tmux.py:176-202`. |
| L13 - Swarm workers | Parallel text-transport requests with token/timeout/retry budgets and reduction. | Model-text fan-out, not persistent sessions with delegated repository tools/worktrees. | `CLI/swarm/dispatch.py:241-276,409-475`; `transports/openai_compat.py:379-402`; `reduce.py:350-375`. |
| L14 - Detached swarm | Saved-spec tmux CLI with missing-tool, empty-command and name-collision checks. | Durable job launch, not coordinator authority or worker lifecycle identity. | `CLI/swarm/commands.py:1297-1309`; `tmux.py:160-177`. |

The distinctions affecting reuse are:

| Finding | Consequence | Evidence |
|---|---|---|
| Issue skill's “orchestrator/worker” labels | Skill/subagent terminology does not establish layered Orca supervision. | R05:44-61; R08:117-125. |
| Intentional create-then-launch claim path | Qualifies a universal atomic create-with-agent interpretation, not worker permission to use the exception. | `ISSUE-LAUNCH:666-681,1300-1355`. |
| Sprint environment and bypass settings | Not evidence of a hard filesystem, spending or authority sandbox. | R05:63-75 and complete source register. |
| Swarm request payload | Model, user message and token limit do not confer a tool/worktree capability. | `CLI/swarm/transports/openai_compat.py:379-402`. |
| Governed L1 claim | B1/B2 recognition, reporting and probe qualifications apply; preflight is not first-tool binding proof. | R04:87-107; R05 dependency correction. |

[CONTRADICTION: The universal no-Orca-primitives description recorded in the developer guidance and R08 conflicts with the coordinator-only claim implementation at `ISSUE-LAUNCH:666-681,1351-1355`, which invokes worktree creation and agent launch. The implementation is a narrow precedent; it does not remove the normative command boundary or the worker-session prohibition.]

### 2.7 Decision history and revisit evidence

**[CODE-VERIFIED - approved record/source instruction]** D1-D5 and Git ownership have approved outcomes, not unresolved debate status. **Evidence:** `APPROVED:8-20`; `SPEC:396-407`; R06:52-157.

| Decision | Approved boundary | Source |
|---|---|---|
| D1 | Explicit unattended selector and worker-side brief guard; no command-side Orca detection. | `WC:12-23`; `APPROVED:8-20`. |
| D2 | Human Rulings only; no agent substitute or bypass of frozen-plan handback. | `WC:57,250-269`. |
| D3 | Ordinary top-level PR session, never dispatched PR worker. | `WC:229-235`. |
| D4 | No worker outward actions; narrowly quoted Task-specific local commits only. | `WC:41-45,233`. |
| D5 | Retain depth-one policy, person-opened coordinator and WC-13. | `SPEC:405`; `WC:62,69`. |
| Git ownership | Authorized coordinator owns outward work, merges and removal under human authority. | `WC:224-235`; approved Git record through R06. |

#### Two D5 trigger texts

| Condition | Applied `SPEC:405` | `D5-REC:49` |
|---|---|---|
| Composite brief defined in specification | Required. | Required. |
| Real run with split knowable only at runtime and material added coordinator round trip | Required. | Required. |
| Pre-raise AC-0.7 trace | Required. | Required. |
| Establish depth-two question/completion mailbox before raise | Not stated. | Required. |

**Evidence:** `SPEC:405`; `D5-REC:44-64`; R06 separate-text table.

The disposition record says the full replacement was superseded by a short decision record. That explains the record's form, not why the mailbox clause was omitted. No deliberate waiver is inferred. **Evidence:** `.dev/orca-command-refactor/review/disposition-round4.md:48-58`; R06:52-82.

[CONTRADICTION: `D5-REC:49` expressly includes establishing the depth-two mailbox before a raise, while the applied short row at `SPEC:405` omits that prerequisite. R06 does not establish whether this was an intentional scope change or summarization loss. Both texts remain visible; source routing evidence does not settle the record's intent.]

R06's bounded search found no combined record establishing runtime-only decomposition, coordinator-created follow-up Task and material extra coordination time. Follow-ups, runtimes, heartbeat gaps, compliance decisions and copy-drift refusals were not counted as that measurement. This is not a global absence claim. **Evidence:** R06:79-96; `WC:246`.

The final rejected alternative was **session-layer** depth two with a scoped helper limit and no command-file changes, not the original command-owned fan-out proposal. **Evidence:** R06:114-128; `D5-REC:44-64`.

| Historical cost | Corrected interpretation | Evidence |
|---|---|---|
| Undefined composite brief | Current prewritten chains weaken the old single-command premise, but do not authorize autonomous planning/dispatch. | `WC:204-216`; R06:114-128. |
| Second coordinator loop | Upward worker and downward supervisor responsibilities still lack a composed contract. | R02:85-132; R06:114-128. |
| Questions probably reach root | Contradicted for the historical native local default by creator-Dispatch routing. Replacement-build and live behavior are not thereby certified. | R03:62-81; `CORRECTION:42-47`. |
| WC-13 needs relaxation | No current approved exception follows from the ownership phrase or product capability. | `WC:62`; `CORE:52-59`. |
| Scoped brief versus broader maximum | Runtime/profile maximum is not per-Task permission. All-machine/all-profile claims exceed the bounded evidence. | R03:118-131; `CORRECTION:44-51`. |

The recorded benefit, fewer root wake/read/Task-creation round trips with separately tracked child work, is rationale, not a measured saving. **Evidence:** R06:116-126.

| Acceptance record | Correct interpretation | Evidence |
|---|---|---|
| P0 AC-0.7 | Accepted historical trace, not a current-build audit, attempted-refusal test or live depth-two success. | R06:81,98-112; R03 historical-evidence reconciliation. |
| P1 | Original FAIL was not final disposition; later approval accepted P1 while retaining actual Skill invocation as the requirement. | R06:98-112,175-201. |
| P2 | Static conversion and merge do not prove live phase acceptance. | R06:175-201; R08 related records. |

R03 resolved earlier slice-local route and call-classification unknowns **for its researched snapshot**. The dated correction prevents promoting that historical resolution into replacement-build certification. Neither source trace changes D5 policy. **Evidence:** R03:133-177; `CORRECTION:36-49`.

### 2.8 Issues, pull requests and independent requirements

These are recorded requests and source-backed interactions, not claims that requested capabilities have shipped. **Evidence:** R08:19-133 and its complete return. Section 10.9, **A17-A24**, records the actual original fork-explicit retrieval commands, selected fields/comments and retained output locations. Separately dated domain-review rechecks **A25-A27** are not evidence of the earlier remote state. No acquisition command was rerun during this correction.

| Record | Scope | Relationship to the subordinate-mode decision |
|---|---|---|
| #339 supervision | Ownership, updates/questions, sweeps, recovery, persistent attention, reporting, cleanup. | Mostly flat-applicable. Current worker procedures address parts, not the complete proposed all-session product. |
| #339 later security | Typed messages, validated identifiers, inert free text, scoped expiring grants, replay and destructive-action safeguards. | Later-release prerequisites, not current permission changes. |
| #339 hierarchy | Orchestrator of orchestrators and downward grant attenuation. | Directly hierarchical; dispatched-worker realization conflicts with current permission. |
| #423 | Catalogue, relevance, shared research/lessons, overlap detection and course correction. | Knowledge sharing, not child dispatch, authority, depth or aggregate upward acceptance. |
| #431 / #434 | Liveness incidents and merged procedural response. | Flat supervision already needs them; no middle-tier authority or incident-elimination proof. |
| #409 | Multi-coordinator/session/worktree observer. | Explicitly excludes scheduler/session-control functions. Synthetic scale is not validated capacity. |
| #326 | Git/PM integration later narrowed by approved decisions. | Depth one retained; central Git relay not adopted; remaining commit/submodule work independent. |
| #446 | Bounded index-lock rechecks without deleting/editing lock. | Independent follow-up. Current `WC:45` still says blocked with path, not the proposed retry sequence. |
| #422 | Observed merged static unattended conversion. | Historical open/unmerged claim stale; static merge is not live rollout acceptance. |
| #449 | Ownership guidance, syntax hook and intentional claim-launch exception. | No subordinate authority or aggregate protocol; WC-13 explicitly deferred. |

**Source anchors:** R08:19-85,89-133; `WC:45,62,69,229-246`; `INF:77-78`.

The complete 35-requirement dispositions are carried into Section 6. Their coverage includes:

| Requirement family | Distinct meanings retained |
|---|---|
| R01-R09 | Capacity target; routing; human-interaction limits; historical/recent-window sweeps; recovery; polling through closure; cleanup; valuable-state commit/push predicates. |
| R10-R17 | Evidence retention; conditional worktrees; persistent registry; report/style conflict; attention until satisfied; display interval; management server; skill integration. |
| R18-R19 | Hierarchy and reduced repeated-confirmation objective, without transitive consent. |
| R20-R24 | Mode classes; untrusted text; application types; trusted identifier validation; receiving-hook or validated-file research. |
| R25-R29 | Scoped grants; session/expiry/replay; attenuation; destructive state checks; removal safeguards. |
| R30-R35 | Sender-class identification; inbound interception; research ordering; library comparison; hierarchy prerequisites; proposed brainstorm/estimate. |

**Evidence:** R08 complete R01-R35 table; R08:19-85,89-133. This grouping does not replace the individual dispositions in Section 6.

| Source-backed conflict or existing mechanism | Meaning | Evidence |
|---|---|---|
| Absolute automation | Cannot replace human Rulings, permission prompts, ordinary PR placement or explicit outward authority. | `WC:41-47,57,229-269`. |
| Blanket disposal | Conflicts with protected work, unread reports, ledgers, frozen plans and task evidence. | `WC:225,234,250-253`; R08 conflict table. |
| Worktree per prompt | Overstates conditional writer isolation. | `WC:47,220-223`; R08. |
| Timeout-based recovery | Elapsed time alone does not authorize stop/retry/release. | `WC:73-79,182-192`. |
| Signed request | Authentication does not create human consent or prove clean/merged/settled destructive state. | `WC:41-45,57,224-235,250-269`; R08. |
| Existing Dispatch capability forwarding | Historical inspected send handler accepts an optional Dispatch capability and forwards it as orchestration capability. | `ORCA/cli/handlers/orchestration/message-send-handler.js:33-65`; R08:117-131. Not proof of complete proposed attenuation or current replacement-build equivalence. |

### 2.9 Wording, tests and distribution surfaces

**[CODE-VERIFIED - source instruction, tests and distribution implementation]** The ownership sentence spans multiple surfaces. Static tests protect different properties; they do not establish live recursive authority. **Evidence:** R07:11-41,65-153,188-198.

| Surface | Established relationship | Limit and evidence |
|---|---|---|
| Ownership guidance | Root/core and ccsession README carry creator-owner wording alongside worker restrictions. | `CORE:52-59`; R07:23-28. |
| Developer guide section 7.7 | Two-tier flat coordinator/worker summary. It does not mention WC-12 (pulled follow-ups), WC-13 (worker fan-out prohibition), WC-14 (continuous chains) or WC-15 (handoff files), nor any subordinate role; a Grep of the whole guide for WC-13, WC-12, WC-14, WC-15, sub-orchestrator and "coordinator under" returned zero matches **[CODE-VERIFIED by Grep count 0]**. | `GUIDE:972-1013`; `RESEARCH/research-notes.md` (guide row); `RESEARCH/scope/scope-01-contract-and-rules.md` §5. A documentation gap, not a rule change. |
| Worktree hook | Printed sentence is separate from scanner's agent-flag predicate. | `WT-HOOK:94-103,342-357`. |
| Exact message | Complete expected denial/stderr is embedded in test. | `tests/hooks/test_require_orca_worktree_agent.py:31-38`. Message change reaches this expectation. |
| Role/paragraph test | Required role words and appended-paragraph equality. | `tests/core/test_orca_session_launch_guidance.py:44-59`. Does not require exact subordinate phrase. |
| Contract tests | Phrase/content, eligibility, converted membership and unattended-section checks. | `TEST-WC:746,755-758,831-886,907-909`. Not whole-contract exact bytes or worker obedience. |
| Current unattended inventory | 31 command headings; populated derived expectations; 16 P1 plus 15 P2 in contract. | `WC:303-304`; R07. Declarations, not 31 live successful runs. |
| Hook mirror | Specified source/plugin byte equality. | `tests/cli/test_install_hooks.py:849-857`. Not universal hook/copy parity. |
| Routing guide | Source/plugin full-file parity and installation equality in a test target. | `tests/commands/test_routing_plugin_parity.py:29-38`; `tests/cli/test_how_we_work_install.py:23-33`. |
| Development sync | Copies distributable commands, skills, agents, hooks and templates. | `Makefile:108-184`. Not global core installation. |
| Plugin build | Packages plugin input tree. | `scripts/build_superclaude_plugin.py:15-18,69-76`. Does not synchronize source into plugin. |
| Global installation | Core/hook installers skip existing destinations without force. | `CLI/install_core.py:32-75`; `CLI/install_hooks.py:251-290`. No universal current freshness claim. |

Original existence observations for copies and installed references retain their observation-time scope. The vanished historical bundle is explicitly excluded from current-path certification. **Evidence:** `CORRECTION:36-45`; R07 inventory.

| Conditional topology | Implicated boundary, not a work order | Evidence |
|---|---|---|
| Retained two tiers with wording clarification | Prose, printed message, exact expectation and distribution relationships; no nested authority inherent. | R07:67-76. |
| Person-opened peers | Exclusive Task/writer ownership and explicit cross-peer boundaries; bound probe restrictions may still apply. | R07:78-88,190-192. |
| Supervised middle with helpers | Eligibility, autonomous brief, WC-13, dual progress/report/admission, retry/ack/failure, grants, placement and governed operation. WC-8 need not change if calls remain session-layer. | R07:90-102; R01 matrix. |
| Ordinary launched middle owner | New eligibility/upward contract; no inherited outward or cleanup authority. | R07:104-115. |
| Internal Agent helpers | Existing top-level lifecycle boundary; no inherent external-session policy change. | R07:117-126. |
| Deferral | Current authority retained; ambiguity, stale descriptions and existing guard/probe defects remain visible. | R07:128-145,188-198. |

#### Stale descriptions and historical records

| Description | Required treatment | Evidence |
|---|---|---|
| No unattended commands / empty set | Historical P0 wording, not current 31-heading inventory. | `GUIDE:978-991`; `WC:303-304`; R07:147-165. |
| Universal no-Orca primitives | Qualify against actual narrow coordinator-only claim implementation; retain worker prohibition. | `ISSUE-LAUNCH:666-681,1351-1355`; R08. |
| D5/CR-01 unapplied | Preserve drafting history; current applied rules exist. | R06:52-157; R07:147-165. |
| Revisit after P0 smoke | Superseded by composite brief plus material runtime-only split. | `SPEC:405`; R06. |
| One command per brief | Current chains exist; autonomous delegation remains different. | `WC:63-64,204-216`. |
| Universal root mailbox | Historical native local creator route corrects prediction; replacement-build behavior not certified. | R03:62-81; `CORRECTION:42-47`. |
| #422 still open | Research observed static merge; no new remote refresh or live acceptance inferred. | R08:106-125. |
| #446 line pointer | Current lock sentence is `WC:45`; requested waiting remains unimplemented there. | R08; R06. |
| Default setup-run / PR worker | Current skip-unless-authorized setup and ordinary PR placement govern. | `WC:221,232`; R01/R06. |
| Historical backend path/offsets | Retain historical filename and offsets. Do not relabel them as replacement-build evidence. | `CORRECTION:36-47`. |
| Old R07 partial status | Later approved active-source/tests/copies scope controls. | R07:11-15,168-198; `GQ:10-12`. |

R07's active inventory is complete under its approved scope. The frozen residual of **867 unread matching archival lines across 274 paths** remains excluded, unclassified background, not runtime evidence and not a new archival-audit prerequisite. No conclusion here depends on classifying those unread originals. **Evidence:** R07:168-198; both retained archival supplements; `GQ:10-12`.

### 2.10 Current-state summary and dedicated uncertainty register

#### Evidence classes

| Class | Established finding | Boundary |
|---|---|---|
| Repository instructions and implementation | Person-opened coordinator; explicit unattended/visible-copy guard; worker fan-out ban; retained internal helpers; own lifecycle; human Rulings; narrow Task grants; authorized outward/admission/retry/protected cleanup; real narrow claim launcher. | Verified text is policy, not automatic obedience. Narrow implementation precedent is not a blanket worker exception. Sources: Sections 2.2, 2.6-2.9. |
| Historical installed mechanics | Dispatch-depth paths; independent Task authority; caller-derived depth; creator routing and selected-mail handback; ordinary launch separated from supervised identity; fixed message vocabulary. | Attributed R03 trace; retained-source reproducibility is limited to FR-01/P01-P14, and the complete ordinary-launch negative is not independently reproduced. No transfer to replacement build or remote recipe. Sources: Section 2.4; `CORRECTION:36-47`; `qa/qa-fix-log.md`. |
| Dated new installed source | Default/fallback two, retained explicit valid one, guarded migration, metadata and construction fields. | Not stored/effective/running-process/migration-execution proof. Sources: Section 2.1; `DEPTH:10-42`. |
| Prose authority and procedure | Creator ownership, subordinate phrase, eligibility, human restrictions, liveness/ack/recovery instructions. | Syntax and phrase tests do not implement recursive authority or universal compliance; B1/B2 defects remain. Sources: Sections 2.2-2.5. |
| Open decisions and unverified behavior | Listed separately below. | Source-answered historical findings are not erased, but exact-target evidence is not invented. |

#### Dedicated uncertainty register

| Category | Residual uncertainty or decision | Evidence boundary |
|---|---|---|
| **[UNVERIFIED - live local lifecycle]** | Depth-two startup, question/reply, mixed mail, completion, early creator settlement, restart, fencing and recovery. | R03 historical source support is not live proof. G05-G06, G12, G17; `CORRECTION:47-51`. |
| **[UNVERIFIED - replacement-build equivalence]** | Full route, authority, reply, handback, fencing, launch and shutdown equivalence with the original researched build. | Located replacement filename and limited new source observations do not certify it. `CORRECTION:36-51`. |
| **[UNVERIFIED - current settings]** | Current stored value, loaded effective maximum, migration invocation/execution/persistence, running build, reload/profile/host propagation and safe lowering. | Historical stored one is not current profile evidence. No profile reopened. `CORRECTION:20-34,51`. |
| **[UNVERIFIED - concurrency/timing]** | Default wait wake behavior, missed answers, attention/detection delay, typed input during tools and concurrent mailbox consumers. | Development Delivery semantics and prescribed timings are not runtime experiments. G05/G23; `WC:194-200`. |
| **[UNVERIFIED - federation]** | Separate-Run remote authority, per-host depth, configuration and recovery. | Local helper findings do not certify remote behavior. G13; R03. |
| **[UNVERIFIED - live governance]** | Real hook event identity, child environment, first-tool binding, rewrite ordering, job attribution and working directory. | Claim preflight, registrations and hand-written events are not live inheritance proof. G28/G30/G31; R04. |
| **[UNVERIFIED - measured outcomes]** | Incident elimination, procedure compliance, hierarchical detection bounds and capacity. | #434's merged procedure and tests are not those measurements. G01/G25; R02/R08. |
| **Open policy decision** | Middle eligibility, autonomous brief, aggregate progress/results, question budgets, escalation, retry/freeze/cancel/admission/cleanup ownership. | Existing restrictions govern until deliberately changed. G02-G09/G19/G27/G34-G35. |
| **[UNVERIFIED - measured need]** | Qualifying unforeseen split, follow-up Task and material extra root round trip. | Not found in bounded search, not globally disproved. G10; R06. |
| **Open record interpretation** | Why applied D5 omitted recommendation's mailbox clause. | Historical routing evidence does not explain intent. G11; `SPEC:405`; `D5-REC:49`. |
| **Security/deployment boundary** | Authenticated sender/parent binding, deployed interception/fail-closed coverage, grants, replay, revocation and capability suitability. | Section 5 supplies documented external answers, including inbound-hook availability; it does not certify local deployment. G40-G43/G49. |
| **[UNVERIFIED - broader inspection claims]** | Whole development/install equivalence, universal copy freshness, provider limits, full lineage persistence and complete backend artifact validation. | Specific source findings retain bounded scope. G18/G20/G22/G24/G32. |
| **Independent proposed work** | #339 registry/server/attention/closure product; #409 remote implementation; #326/#446 follow-ups; P2 live acceptance; C10-C14 delivery. | Targets, requests and static merge are not completed operational acceptance. G26/G36-G39/G44-G48. |
| **[UNVERIFIED - excluded background]** | Unread archival originals. | 867 matching lines/274 paths remain excluded, not reopened or classified. G53; R07 approved scope. |

#### Research coverage and intentional consolidation

| Input | Distinct findings retained | Consolidation or limit |
|---|---|---|
| R01 and full return | Command/session/ownership separation; precise D1; six WC-13 routes; eligibility; grants, freezes, admission and noninherited authority. | Full decision compatibility matrices appear in Section 6; repeated clauses are not additional runtime observations. |
| R02 and full return | Signals, all twelve states, two acknowledgment layers, response ladder, caps, handoff limits, dual-role gaps and procedural #434 scope. | Development implementation is not whole-installed equivalence; C9 deleted and C10-C14 future mechanisms remain distinct. |
| R03 and full return | Per-route depth/authority, native local creator route, fallback, parentages, ordinary launch, vocabulary and settings boundaries. | Historical snapshot retained; bounded new source correction controls current-installation assertions. |
| R04 and full return | Distinct syntax/session/job inputs; no trusted role grant; literal-executable ceiling; omitted required probes; live governance limits. | Embedded B1/B2 overrides older categorical statements, not policy or observed runtime behavior. |
| R05 and full return | Fourteen launcher types and 56 reuse judgments; receipts versus results; narrow process/scheduling/durability patterns. | No launcher promoted into a complete middle supervisor; PM/agent/PR instructions not treated as execution. |
| R06 and full return | Approved outcomes, separate D5 texts, actual trigger, bounded need search, five historical cost corrections and P0/P1/P2 distinctions. | Historical source questions resolved by R03 remain historical, not replacement-build certification. |
| R07 and full return | Exact-message versus roles/parity pins; 31 declarations; option-specific surface breadth; distinct sync/build/install paths; approved archival exclusion. | Frozen search counts are provenance, not new independent findings or universal copy freshness. |
| R08 and full return | All 35 requirement dispositions; flat supervision/knowledge/hierarchy separation; conflicts, related issues and capability forwarding. | Estimates, requested interfaces and administrative release names are not delivered architecture. |

**Current-state conclusion:** The researched evidence supports retaining the present two-tier authority boundary and existing internal helpers while treating native supervised helpers as the provisional technical candidate on retained historical evidence for a separately justified future middle role. That is not approval: need, authority, aggregate admission, failure ownership and exact-target operational evidence remain distinct barriers. The bounded new source default of two changes capability evidence, not WC-13, human consent or the recommendation's authority basis. **Evidence:** R01/R02/R03/R06 conclusions; `CORRECTION:47-51`. The comparative decision is developed in Sections 6-7.

## 3. Target State
### 3.1 Desired behavior and decision boundary

The target is a decision-ready answer, not an enabled mode or an implementation plan. The report must establish whether a subordinate supervisor adds enough value to justify changing the present authority boundary, while separating **technical capability, permission and demonstrated operation**.

**Evidence conventions:** [CODE-VERIFIED] identifies source-traced implementation or, for normative documents, a verified instruction, not automatic enforcement. [CODE-CONTRADICTED] identifies an interpretation inconsistent with that evidence. [UNVERIFIED] marks unresolved behavior, proposed capability or missing measurement. External context supplements but does not override local source or approved policy.

The source aliases in Section 2.1 apply throughout. All references to R03's installed routes describe its **historical researched snapshot** unless expressly covered by the bounded 2026-11-09 observations in `CORRECTION:25-34`. The replacement source defines default/fallback two and guarded migration; current stored/effective settings, migration execution and replacement-build routing equivalence remain unverified. **Evidence:** `CORRECTION:8-13,36-51`.

#### What the decision must establish

| Decision question | Required answer | Evidence and present boundary |
|---|---|---|
| What is being proposed? | Distinguish a dispatched worker supervising native helpers, an agent-launched handoff owner, person-opened peers and command-internal Agent helpers. Do not collapse them into one `--sub` mode. | R01 role matrix; R03 §§2-4; R05 launcher inventory. Ordinary launches did not automatically create Run/Task/Dispatch records or worker preambles on the historically inspected paths. |
| What additional value is sought? | Identify coherent, independently checkable work discovered during execution and the material upper-coordinator round trip that local supervision would avoid. Separate this from parallelism already available under one coordinator. | R06 trigger evidence; W02. External guidance: https://www.anthropic.com/engineering/building-effective-agents and https://www.anthropic.com/engineering/multi-agent-research-system . No qualifying local measured saving was established. |
| Is the capability technically available? | Credit the historically traced same-Run ancestry, creator-directed reports/questions, reply validation, fencing and selected-mail handback. Keep exact-target source and successful live operation separate. | R03 §§1-3 resolves older root-only predictions for its researched snapshot. `CORRECTION:36-47` prevents transferring that trace to the replacement build. |
| Is its use authorized? | State current policy before considering an exception: WC-13 prohibits worker-session fan-out at any depth; section 4 admits a person-opened coordinator. Explicitly disposition the ownership-rule conflict. | `WC:62,69`; `CORE:52-59`; R01/R06; A01 and `INF:77-78`. Native support is not authorization. |
| What must change conceptually? | Decide eligibility, bounded planning/launch/retry authority, command-versus-session placement, exclusive Task ownership and any role flag's meaning. | R01's full rule-by-option matrix; R06 D1-D5; R07 change surfaces. These are responsibility decisions, not implementation steps. |
| What does completion mean? | Separate child completion, the middle session's own completion, aggregate outcome, artifact validation and result admission. Preserve failed/blocked/partial inputs and original child evidence. | R02 signal/state tables; R01 section-4 matrix; W02. Flat admission exists; recursive composition remains undefined. |
| Who remains responsible after failure? | Name the owner of children, questions, mixed deliveries, intervention budgets, freezes and cleanup through parent ask, fencing, exit, exhaustion and replacement. | R02 §§2-3; R03 historical handback trace. External analogy: https://www.erlang.org/doc/system/sup_princ.html . Mail handback is not complete monitoring transfer. |
| What does security require? | Separate inbound delivery, authenticated origin, permitted requests, pre-effect authorization, human consent, replay/revocation state and safe destructive-action predicates. | W01/W03. Delivered text or a valid credential is not a human Ruling, fan-out permission or proof that deletion is safe. |
| Which scopes remain independent? | Keep #339 flat supervision, #423 knowledge sharing and hierarchy/delegated authority separate. Preserve #409 as observation rather than control. | R08 requirements and issue comparisons. Shared release wording does not establish shared acceptance criteria. |

#### Behavior required if a subordinate capability were adopted

| Area | Conditional required behavior | Basis |
|---|---|---|
| Identity and scope | Bind the subordinate to a trusted parent, explicit role, permitted resources and bounded assignment. Names, worktree ancestry or absence of a worker preamble must not manufacture authority. | R01/R03/R04; `WC:11,62,69`. |
| Downward delegation | Permit only approved creation/start routes with explicit helper-count, depth, retry and write limits. Preserve exclusive ownership of self-created Tasks or deliberately replace that rule. | R01 matrix; R06; `WC:62,246`. |
| Upward reporting | For a native-helper variant, assess the historically established creator-Dispatch mechanism rather than presume missing transport. For an ordinary owner, define correlation, progress, questions, acknowledgments, completion and failure without impersonating worker lifecycle messages. | R02/R03/R05; exact-target qualification in `CORRECTION:42-47`. |
| Supervision | Distinguish own progress from child activity; service parent instructions and children; preserve complete mixed batches; separate Delivery receipt from application acknowledgment. | R02; `WC:61,103-114,131-143`. |
| Results | Read and admit child contracts/artifacts before aggregate success or dependents. Launch receipts, heartbeats, idle notices and status messages are insufficient. | R01/R02; `WC:239-246`. |
| Recovery and budgets | Preserve lineage limits, applied-message history, pending deliveries, uncertain effects and ownership through replacement. Parent settlement does not prove descendants stopped. | R02/R03; `WC:73-79,146-179`. |
| Human authority | Relay eligible clarification with provenance while retaining Rulings, permission prompts, frozen-plan handback and outward publication with their authorized human-facing owner. | R01/R06; `WC:41-45,53-58,229-269`. |
| Cleanup | Require settlement, admission, writer quiescence and protected-state checks independently of close requests or credentials. | R01/R08; `WC:224-235,250-269`. |
| Governed operation | Deliberately reconcile launch, reporting and required supervision probes. Do not use an executable-recognition ceiling as an authorized route. | R04 B1/B2; R05/R07 dependency corrections. |

These are adoption conditions, not findings that the role is implemented or approved. A complete decision investigation can conclude that adoption should be deferred.

### 3.2 Success criteria

Decision-artifact criteria can pass while adoption conditions remain unmet. None of these criteria authorizes a live experiment.

| ID | Testable pass condition | Failure condition or present evidence |
|---|---|---|
| **SC01 - Role classification** | Explicitly distinguish supervised middle workers, launched nonworker owners, person-opened peers and internal helpers. | Fail if launch operation, worktree parentage or role label is treated as Dispatch identity or coordinator authorization. R01/R03/R05. |
| **SC02 - Correct source baseline** | Credit historical native creator-Dispatch routing and independent Task-creation authority, while retaining exact-target and live uncertainty. | Fail if all helper reports are called root-directed, native upward routing is called absent, or Task creation is said to be constrained only by prose. Also fail if historical tracing is silently promoted to replacement-build equivalence. R03; GQ S17-S21; `CORRECTION:42-47`. |
| **SC03 - Rule-conflict disposition** | Record the PR #449 ownership/WC-13/person-opened conflict as a severity-rated defect, citing INF-027. | Fail if dismissed as documentation-only future work or treated as an approved worker exception. A01; `INF:77-78`. |
| **SC04 - D1 interpretation** | Preserve explicit `--unattended` command-mode selection and separately decide any subordinate topology/eligibility selector. | Fail if D1 is called a ban on all other flags, or environment/preamble detection silently replaces explicit selection. `WC:12-14`; R01/R06. |
| **SC05 - Command boundary** | Distinguish the broad no-Orca-command sentence, WC-8's three verbs, WC-13's six routes and the narrow claim-code tension. | Fail if the shorter WC-8 list becomes a loophole or an Orca-calling orchestrator command is assumed exempt. A04. |
| **SC06 - Measured need** | Reopening D5 has both an approved autonomous composite brief and a qualifying real-run record of runtime-only split and material extra round-trip cost. | Adoption condition not established. Prewritten chains are not discretionary delegation briefs; bounded search found no qualifying combined record. R06. |
| **SC07 - Depth and version evidence** | Separate project policy one, historical source/stored one, dated replacement-source default/fallback two with guarded migration, public four, effective settings, and local/remote behavior. | Fail if historical source answers are erased; stored one is treated as current/effective; source two proves migration execution; public four is substituted locally; a new Run is called a depth reset; or historical routes certify the replacement build. R03/W04; `CORRECTION:18-51`. |
| **SC08 - Aggregate admission** | An adopted role defines own-versus-child progress, outcome reduction and evidence-backed admission before aggregate completion/dependents. | Adoption condition unmet. Existing flat admission is not recursive semantics. A08. |
| **SC09 - Messaging and acknowledgments** | Identify one authoritative consumer/acknowledgment owner per stream, handle complete mixed batches and distinguish receipt from application. | Adoption condition unmet; no nested live handling or measured cross-level response bound established. A09. |
| **SC10 - Recovery** | Every child retains a supervisor through parent ask, fence, exit, exhaustion and replacement, with persistent budgets, freezes and cleanup responsibility. | Adoption condition unmet. Selected-mail handback and public shutdown statements are not full takeover or subtree quiescence. A10/A20. |
| **SC11 - Human and outward authority** | No role, relay or token substitutes for a human Ruling, fresh Task-specific commit instruction or publication/merge/removal authority. | Fail if a middle worker inherits root duties wholesale or a parent grant is assumed transferable. A11/A23/A27. |
| **SC12 - Governed compatibility** | Address trusted role binding, launch/report policy, literal-executable coverage and required probes separately. | Adoption condition unmet. Person-opened does not mean unbound; listed `worker-show` does not make `worker-list`, `worker-read` or `worktree ps` available. R04 B1/B2. |
| **SC13 - Transport/security precision** | Preserve documented inbound-hook support, partly unresolved sender-class mechanism, origin/fail-closed gaps and typed-text/token limits. | Fail if no inbound hook is claimed, all-bypass is called necessary, or schema/signature checks are called complete authorization. W01/W03; A21-A24. |
| **SC14 - Evidence fidelity** | Represent every compiled gap/stale family or explicitly justify deduplication; apply current corrections and scope approval to older returns. | Fail if research-gate Minor is reused as adoption-impact severity, unread archives become proof, superseded W02 metrics recur, or the snapshot correction is optional. |
| **SC15 - Scope separation** | Give #339 supervision, #423 knowledge, hierarchy and observer-only #409 distinct acceptance boundaries. | Fail if a “v2” name, synthetic dashboard target or knowledge catalogue counts as a functioning subordinate supervisor. A26/A29/A30. |
| **SC16 - Read-only decision delivery** | Provide complete decision content without implementation sequence, live evaluation or source/runtime/settings/permission changes. | No experiment or implementation is authorized by a criterion or suggested resolution. Document persistence is not implementation authority. |

### 3.3 Constraints

| Constraint | Binding interpretation |
|---|---|
| **1. D1 - Explicit mode** | `WC:12-14` and D1 require explicit unattended selection and prohibit command-side Orca, preamble or environment detection. Ordinary output/depth/other flags are not categorically banned. A supervision-granting `--sub` needs a separate authority/topology disposition. |
| **2. D2 - Human Rulings** | `WC:53-58,250-269` retain actual human acceptance. Parent reply or drafted Ruling is not acceptance; retry cannot bypass a freeze. |
| **3. D3 - PR carriage** | Named-PR submission remains ordinary top-level, never dispatched worker. A subordinate label does not change this. `WC:229-235`; R01/R06. |
| **4. D4 - Narrow local grant** | Local commit requires exact human Task-specific instruction, sole occupancy of the Orca child worktree and succeeded command result. Grant ends with that Task; no child or outward grant is inherited. `WC:41-45,233`. |
| **5. D5 - Reconsideration** | Retain depth-one policy/person-opened coordination/WC-13. Autonomous brief and qualifying material runtime-only split remain the two-part trigger. Historical AC-0.7 and later source tracing are different evidence. Preserve the `SPEC:405`/`D5-REC:49` mailbox omission without inferring waiver. |
| **6. Commands versus sessions** | Broad opening no-Orca rule, WC-8's three verbs and WC-13's six worker routes are separate. Moving calls out of a command does not evade WC-13. Narrow coordinator-only claim implementation is not general worker permission. `WC:5,40,62`; R01/R05/R08. |
| **7. Orca depth and authority** | R03 historically traced worker-start/dispatch/inject/dry-run fences, unfenced Task/ordinary launch routes, independent Task authority, caller-derived depth and no automatic supervised identity on ordinary launches. Preserve these answers for their snapshot; do not certify replacement-build paths from them. `CORRECTION:36-47`. |
| **8. Setting scope and migration** | Historical source/stored one is not current stored/effective evidence. New source default/fallback two and guarded legacy migration are source contents only. Current stored/effective values, migration execution, reload and lowering remain [UNVERIFIED]. Runtime/profile scope is not per-Run or all-profile proof; public four is not project policy. `CORRECTION:18-51`. |
| **9. Hook ceilings** | Syntax checking, positively bound launch-level identity and Linux same-user job identity differ. None is a sandbox or trusted hierarchy grant. Do not transfer one hook's ceilings to another or create authority through names. R04. |
| **10. Governed restrictions** | Recognized non-exempt Orca and SendMessage receive ESCAPE, denied at governed levels. Literal matching is not all-form coverage. Required enumeration/transcript/prompt-wait probes are separately unlisted. No alternate spelling, bypass or allowlist expansion is authorized. R04 B1/B2. |
| **11. Lifecycle and evidence** | Preserve top-level worker lifecycle ownership, current attempt identity, whole-batch processing, actual report reading, admission, bounded retry and non-destructive silence handling. Internal helpers do not become Orca lifecycle owners. R01/R02. |
| **12. Worktrees, Git and cleanup** | Preserve distinct writers, authorized setup, one outward/integration owner, protected worktrees, unread reports, ledgers, frozen plans and task evidence. Ancestry is not supervisory authority. `WC:47,220-269`. |
| **13. Distribution** | Canonical source, plugin mirrors, generated development copies, installed copies and packaged artifacts have separate relationships. Sync/build/install are not one automatic operation; installers may retain old copies. R07. |
| **14. Investigation scope** | No live launch, mailbox consumption/acknowledgment, settings/permission/model change, API write, implementation, source mutation, build, install or test is authorized here. Runtime unknowns remain evidence limits, not implied experiments. |
| **15. Evidence precedence** | R03 historical source traces govern older guesses for that snapshot; the dated snapshot correction governs contradictory current-installation claims. R04/R05/R07 corrections, approved R07 scope and W02's metric correction govern immutable originals. Web context never overrides local source or policy. |

## 4. Gap Analysis
**Severity grades conditional adoption and decision impact, not research completeness.**

- **Critical:** Unsafe authority, recovery or destructive-action conditions block endorsement of the affected capability.
- **Important:** Material policy, integration, operational or value evidence must be resolved before relying on the capability.
- **Minor:** Bounded historical, citation, administrative or background uncertainty.

These ratings do not assert a demonstrated exploit, deletion or data-loss incident. GQ's research-gate Minor dispositions remain unchanged: documenting a risk can complete research without making adoption safe.

### 4.1 Current defects and adoption gaps

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| **A01 - DEFECT: subordinate-role rule conflict** | Ownership wording names a coordinator under another orchestrator; WC-13 prohibits worker fan-out and section 4 defines a person-opened coordinator. The user-started ordinary-session clause does not promote every launched nonworker. | Coherent role definition or explicitly narrowed ownership wording, with supervised and nonworker cases dispositioned. | Important | G02/G51; R01/R06/R08; `CORE:52-59`; `WC:62,69`. `INF:78` expressly deferred WC-13; `INF:77` excluded supervised workers. This cited scope decision explains the in-scope contradictory/unwired rule defect but does not close it, implement the role or grant permission. Contradiction retained in Section 2.2. |
| **A02 - No approved delegation contract** | Fixed chains do not define discretionary child planning, launch scope, helper/question counts or an autonomous composite brief. Current D1-D4/WC-13 policy is established. | Approved eligibility, scope and bounds; deliberate WC-13/D5 amendment if a worker may supervise. | Critical | G03/G33; R01 full matrix/R06. Otherwise prohibited operations would occur under an undefined grant. This is a policy decision, not an experiment to discover whether current rules exist. |
| **A03 - Mode and subordinate-role selector** | Explicit unattended selection exists; a second authority/topology selector is undefined. D1 does not prohibit ordinary additional flags. | Distinguish command execution mode from subordinate session authority and specify any selector's eligibility and meaning. | Important | G35; R01 §2/R06 §5; `WC:12-14`. No environment/preamble detection or flag-implies-authority inference. |
| **A04 - Orca-calling command boundary** | Broad no-Orca-command text, WC-8's three verbs and WC-13's six routes coexist with actual narrow coordinator-only claim calls. No orchestrator-command exception is established. | Explicit coordinator-command boundary or session-only decision; preserve WC-8 unless deliberately amended. | Important | G35/S31; R01/R05/R08. Applies even to a root-only entry point. Shorter WC-8 wording is not a launch loophole. Contradiction retained in Section 2.6. |
| **A05 - Measured need not established** | Bounded search found no combined runtime-only split, Task identity and material measured extra coordination cost. Duration, follow-ups and public requests are not equivalent. | Evidence meeting the actual two-part trigger, or an explicitly approved replacement decision. | Important | G10; R06 trigger table; W02/W04. No global absence claim, local speedup or validated worker capacity follows. |
| **A06 - Mailbox prerequisite divergence** | Recommendation requires establishing the depth-two question/completion mailbox; applied short row omits it. Intent is unknown. | Authoritative disposition separating historical source destination, exact-target behavior and record intent. | Important | G11; R06 §2; `SPEC:405`; `D5-REC:49`. R03's historical route does not explain the omission or prove live recovery. Contradiction retained in Section 2.7. |
| **A07 - Ordinary-owner upward protocol** | Historical native helpers have an upward route. Ordinary launches did not automatically create supervised parent records on inspected paths; no complete ordinary-owner lifecycle was established. | Trusted parent/correlation, progress, questions, acknowledgments, completion, failure and admission without lifecycle impersonation. | Important | G19/G51; R02/R03/R05. Do not generalize to “all forms lack transport.” New agreed relationship is needed for this role; new transport/type is not proved necessary. Replacement-build claims require their own evidence. |
| **A08 - Recursive progress, outcome and admission** | Flat admission/fan-in exists. Own-versus-child progress, failed/blocked/partial reduction and subtree completion are undefined. Complete backend report-file validation was not traced. | Preserve required child statuses/artifacts; read and admit them before aggregate success or dependents. | Important | G04/G24; R01/R02/W02. Receipt, status, heartbeat or idle is not admission; correct children do not automatically make a correct aggregate. |
| **A09 - Mixed-mail scheduling and acknowledgment** | R03 historically traced shared parent/helper FIFO routing; development Delivery source supplies replay/fencing. Application scheduling and whole-batch ownership remain unverified. | One authoritative consumer handles/logs the whole batch before receipt acknowledgment; applied/queued/refused remain distinct on each edge. | Important | G05; R02/R03/W01. Wake filters are not separate semantic queues. Receiving an upstream answer does not prove child application. No live or replacement-build guarantee follows. |
| **A10 - Subtree recovery, retry, freeze and cleanup** | Historical selected-mail handback is not full takeover and excludes heartbeat from selected unread reports. Parent ask/fence/exit/exhaustion/replacement leaves child-duty allocation undefined. | Named child owner, settlement order, orphan handling, persistent lineage budgets, cancellation, freeze and cleanup responsibility through every transition. | Critical | G06/G07; R02/R03. G06 includes live behavior; G07 first needs policy. Newer public stop behavior retains preservation, uncertain-stop and remote qualifications: https://github.com/stablyai/orca/pull/38373 . Parent stopped is not subtree quiescent. |
| **A11 - Human escalation and non-transferable authority** | L5 reports to the person. Rulings, permissions, PR carriage, frozen handback and Task-specific commit grants retain their boundaries; no transitive grant exists. | Actual human provenance, authorized outward owner and relay acknowledgment/deadlines without agent-generated acceptance. | Critical | G08/G34; R01/R02/R06. External boundary: https://code.claude.com/docs/en/cross-session-messaging#how-a-session-treats-an-incoming-message . Forwarding or signing agent text does not make it consent. |
| **A12 - Trusted role signal absent** | Syntax hook, launch-level/session fields and job identity do not bind authorized parent, role, depth, resource and action scope. | Trusted scoped authority for any adopted exception, not names, prompt assertions or arbitrary binding-record words. | Important | G27; R04/W03. Not all hooks read only command text; additional input does not itself implement a hierarchy grant. |
| **A13 - Governed launch/report policy** | In positively bound sessions, recognized non-exempt Orca and independently SendMessage receive ESCAPE, denied at every governed level. | Deliberate scoped launch/report policy, child governance and destinations. | Important | G52; R04 B1/B2 and R05/R07 corrections. Agent syntax does not satisfy launch classification. No blanket exception or permission escalation follows. |
| **A14 - Literal-executable ceiling** | Orca branch recognizes basename `orca`; observed `orca-ide` does not match it. Other classifications may still deny. | Declared, assessed coverage before enforcement claims; no spelling workaround treated as permission or proof. | Important | G52; R04 B1. Correcting research wording does not fix the static ceiling. No alternate-spelling success or live bypass was demonstrated. |
| **A15 - Required-probe incompatibility** | Required `worker-list`, `worker-read` and `worktree ps` are absent from recognized exceptions; listed `worker-show` is not equivalent. | Coherent complete supervision policy, separately addressing launch and reporting. | Important | G52; R04 B2; `WC:107,110,151` versus `GUARD:475-478`. Also affects bound flat/peer supervisors. Person-opened does not mean unbound; no automatic allowlist expansion. |
| **A16 - Depth is not complete authority** | Historical tracing established worker-start/dispatch fences, unfenced Task/ordinary launch routes, independent Task authority and no automatic Dispatch identity for general launch. | Call-specific depth, role and runtime evidence for the exact target; bounds beyond depth alone. | Important | G17; R03 §§1/6; `CORRECTION:36-47`. Do not restore “only prose constrains Task creation” or “new Run resets depth.” Historical answers stand; replacement equivalence and live receipts remain unverified. Depth is not total-worker, spending or sandbox control. |
| **A17 - Effective setting, migration and reversal** | Historical default/fallback and stored observation were one. The researched build's desktop control accepted integers of at least one with no explicit maximum, and a bounded inspection of its registered CLI found no depth-setting verb or flag (Section 2.4; historical observations, no replacement-build equivalence). Dated replacement source defines default/fallback two and guarded legacy-one migration. Current stored/effective values, migration execution, reload and lowering remain [UNVERIFIED]. | Actual build/host/effective-scope evidence and an authorized, evidenced reversibility disposition. | Important | G14-G16; R03/W04; `CORRECTION:18-51`. Explicit valid one is accepted by resolver, but unmarked one meets migration's legacy condition; marked one and valid values above one remain. Runtime/profile evidence is not per-Run/all-profile proof. Public four/migration remains separate: https://github.com/stablyai/orca/pull/38348 . |
| **A18 - Live, federated and build-equivalence evidence** | R03 established local route/reply/fence/handback for its original build. Live depth-two lifecycle, remote separate-Run behavior, complete replacement-build equivalence and whole development/install equivalence remain unverified. | Separate scoped source and operational evidence for each claimed topology/build/host. | Important | G12/G13/G20; R03/W04; `CORRECTION:36-51`. Do not erase historical route answers or promote them to exact-target certification. Public remote closure does not prove owner-only setter or shared desktop allowance: https://github.com/stablyai/orca/issues/30141 . |
| **A19 - Procedures versus automation/outcomes** | Tokens, S0-S11, L0-L5, application acknowledgments and handoffs are prescribed. Universal compliance, incident elimination and measured timing are unproved; C10-C14 delivery elsewhere was not audited. | Separate instructions, measured behavior and delivered automation with per-edge evidence and non-destructive silence handling. | Important | G01/G23/G25/G26; R02. Retain five distinct unknowns: default wake behavior, missed-answer cause, attention/detection delay, input during tools, concurrent consumers. Future-tense proposals are not stale merely because unbuilt. |
| **A20 - Supervisor checkpoint sufficiency** | At-most-40-line worker handoff does not explicitly define subtree roster, deliveries, budgets, admissions/ownership or uncertain child effects. | Bounded sufficient supervisor recovery record, preserving artifact links and applied history without resetting budgets or redoing completed work. | Important | G09; R01/R02/W02. Interface/adequacy gap, not proof every existing worker handoff fails. |
| **A21 - Typed peer protocol and channel semantics** | W01 documents classes rather than exact mode equality, inbound controls and main-conversation hook support. Peer text and six proposed application types are not Orca's nine types or automatic settlement. | Channel-specific receipt/application/admission and validated protocol without treating text, paths or schemas as authority. | Important | G40/G41; W01. Sender-class wire details and historical configuration remain unknown. Holds, expiry/refusal/drop, noninterruption and idle notices matter: https://code.claude.com/docs/en/cross-session-messaging . Team mailbox-write/final-report guarantees do not transfer to peer/Orca channels. |
| **A22 - Authenticated origin and fail-closed integration** | Documented incoming hook can block, but receiving-context fields are not authenticated peer/parent grants. Researched source registration lacks the documented fail-closed option. Origin separation, real envelopes, rewrite order and first-tool child binding remain untested. | Trusted origin/request binding, failure/timeout policy and proven path coverage before inbound text carries authority. | Critical | G27/G28/G30/G31/G40; R04/W01. Feature availability is answered; deployment adequacy is not. U7/event identity and job/cwd behavior are not sandbox proof. No approval-laundering exploit was demonstrated. https://code.claude.com/docs/en/hooks#userpromptsubmit ; https://code.claude.com/docs/en/hooks#common-input-fields . |
| **A23 - Trusted effect authorization absent** | Attenuation is externally feasible; no complete grant verifier, trusted request binding, race-safe one-use state or revocation-freshness policy is established. Historical Dispatch forwarding exists, suitability untraced. | Separate integrity/narrowing, trusted-context authorization, complete pre-effect enforcement and credential lifecycle; retain human/destructive-state checks. | Critical | G34/G42/G43; W03. Nonce is not a ledger; offline verification cannot learn new revocation without fresh state; narrower derivative does not erase broader original. MAC/public-key trust and proof acquisition differ. https://doc.biscuitsec.org/reference/specifications.html ; https://www.biscuitsec.org/docs/guides/revocation/ ; https://www.rfc-editor.org/rfc/rfc9449.html . |
| **A24 - Library, literature and benefit readiness** | Availability/conditional feasibility is not an already-used, maintained, compatible library winner or completed adversarial choice. CaMeL is information-flow separation, not a signed-token alternative. No matched local middle-layer benchmark exists in the research. | Bounded maintenance/feature claims, correct denominators and explicit transfer limits, not security/performance certification. | Important | G42/G49; W02/W03. Biscuit public verification is a candidate advantage, not adoption. Python partial support remains material. Rounded CaMeL 77% versus 84% is task utility/completion, not attack-blocking rate or local guarantee. https://python.biscuitsec.org/basic-use ; https://arxiv.org/html/2503.18813v2 ; https://arxiv.org/html/2503.13657v3 . |
| **A25 - Distribution and enforcement readiness** | Targeted parity is not universal freshness. Development sync, plugin build/mirrors and global installation differ; existing copies may be skipped. U28 installation is separate from U7 visibility. | Actual worker-visible policy/copy/enforcement provenance without claiming one operation refreshes everything. | Important | G29/G32; R04/R07. No sync/build/install/test was run; no archive reopening is required. Original existence observations retain their date/scope; historical bundle is not a current existing path. `CORRECTION:36-45`. Documentation gap: developer guide section 7.7 (`GUIDE:972-1013`) is silent on WC-12 to WC-15 (pulled follow-ups, worker fan-out prohibition, continuous chains, handoff files); see Section 2.9. |
| **A26 - Independent flat-supervision product** | #339's 10-20 target, registry, default-six-hour recent-session sweep, persistent attention/static report, 3-5-minute display, management server and closure invariant are not established as one delivered product. | Distinct flat/ordinary-session acceptance without hierarchy dependency or scale claims from targets. | Important | G44; R08 R01-R17/R35. Credit existing worker procedures. Orchestration-skill integration and 40-hour estimate are proposals, not completion or schedule. Cleanup predicates separately A27. |
| **A27 - Unsafe cleanup/automation reading** | Blanket disposal, timeout stop/retry and authenticated close requests can conflict with protected work, unread evidence, freezes and settlement. Universal pushed/merged/closed predicates are unproved. | Preserve evidence/quiescence/admission and check destructive state independently of signatures or done labels. | Critical | G50/G44; R08 R06/R08-R10/R28-R29 and conflict table. Potential data-loss impact if adopted literally; no observed deletion/loss asserted. |
| **A28 - Overbroad interaction, placement and presentation** | No manual child interaction conflicts with human gates; worktree per prompt conflicts with conditional placement; replacing summary tables conflicts with inspected style policy. | Explicit requirement dispositions preserving human steps, appropriate placement and agreed presentation. | Important | G50; R08 R03/R11/R13. Presentation alone is minor; grouping retains material authority/scope conflicts. Not justification for worker fan-out. |
| **A29 - “v2” naming collision** | #339 uses v2 for security/hierarchy; #423 uses it for proactive knowledge sharing. Semantic separation is known; administrative numbering unresolved. | Distinct release and acceptance names. | Minor | G45; R08 §3. Knowledge exchange/duplicate detection does not own another coordinator's Tasks or satisfy subordinate acceptance. |
| **A30 - Observer is not control/capacity proof** | #409 excludes controls. Local prototype absent in research; remote version/schema/tests/live collection unverified; scale scenarios synthetic. | Bounded observation claims without implied approve/retry/spawn/merge/delete authority. | Minor | G46; R08 related records. Useful to peers or hierarchy, proof of neither and not enforcement. |
| **A31 - Independent Git/lock follow-ups** | Requested bounded lock wait is absent from current inspected rule; experiments not rerun. Remaining #326 Git/submodule/per-task-commit work unestablished. | Independent evidence and acceptance without lock deletion, freeze bypass or new middle-layer Git authority. | Important | G47; R08 #446/#326. Immediate blocked behavior remains; citation drift is separately S25. |
| **A32 - Historical/static/live acceptance** | P0 documentary compliance did not attempt forbidden calls; raw transcripts not independently replayed. P2 static merge is not live acceptance; qualifying phase evidence not found in bounded search. | Preserve historical acceptance, static source and actual live evidence separately; continue contract/artifact admission. | Important | G21/G24/G48; R03/R06/R08. Later P1 acceptance controls original FAIL, without waiving actual Skill invocation. |
| **A33 - Precedent and helper limits** | Fourteen launchers/56 reuse cells offer partial patterns, not complete middle supervision. Placement, helper tiers/roles, PM startup and watcher reply/error assumptions lack live validation. Provider limits and hard isolation are not established universally. | Reuse demonstrated mechanisms only; retain top-level lifecycle and separate helpers, external sessions, subprocesses and model-text requests. | Important | G18/G36-G39; R05/W01/W02. Public nesting/team limits are not installed Orca inheritance or permission. Neither universal no-nesting nor unlimited helpers is justified. |
| **A34 - Bounded provenance and background** | Lineage backing writer/table unlocated despite schema/projection/host-instance validation. Archives excluded. Some compressed terms need precision. Notebook/PDF extraction, source 404 and exact-four rationale incomplete. | Preserve limits without inventing content, reopening excluded work or restoring historically answered unknowns. | Minor | G22/G53/G54; R03/R07 supplements; W02-W04. 867 unread matching lines/274 paths remain excluded. 404 is not privacy/absence proof. Snapshot correction additionally prevents filename/offset substitution and universal current-path claims. |

### 4.2 Stale and contradicted families: explicit dispositions

All 38 GQ stale/interpretation families remain represented. Source-resolved interpretations are not reopened as absent capabilities; historical records are not rewritten into present permission. The snapshot correction qualifies installed-source wording throughout this table.

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| **S01 - Original command-owned alternative** | Original D5 alternative required command calls/rewrites; final scoped alternative was session-layer with no command-file changes. | Evaluate final scoped proposal, without calling it approved. | Minor | [STALE DOC]/historical interpretation; R01/R06; A02/A04. |
| **S02 - Raise removes fence** | Higher positive finite maximum and fallback do not remove the fence. | Describe a wider bounded ceiling. | Important | [STALE DOC]/[CODE-CONTRADICTED]; R03/R06; A16/A17. Dated source fallback two supersedes historical fallback one for new-source claims. |
| **S03 - Specification not edited** | Recommendation's statement is drafting history; applied D5/WC-13 text exists. | Preserve historical context, not present non-application. | Minor | R06/R07. |
| **S04 - No edits applied** | Broader none-applied status is contradicted as a current claim by application records/rules. | Use applied record. | Minor | R01/R06/R07; distinct from S03. |
| **S05 - Decisions running/Git stub** | Approved D1-D5/Git outcomes exist. | Treat settled unless explicitly reopened. | Minor | R06; not a new runtime question. |
| **S06 - Coordinator precondition unstated** | Person-opened eligibility is explicit. | Identify proposed extension against actual rule. | Important | R06; `WC:69`; A01/A02. |
| **S07 - No worker-session rule** | WC-13 expressly bans worker fan-out. | No historical loophole used. | Important | R06; `WC:62`; A02. |
| **S08 - Placement unapplied** | Placement/isolation instructions were applied. | Retain CR-01's old status as history. | Minor | R06. |
| **S09 - P0-smoke trigger** | Superseded by composite brief AND material runtime-only split. | Apply actual two-part trigger. | Important | R06; `SPEC:405`; A05. |
| **S10 - One command per brief** | Multiple labelled commands exist; autonomous dispatch authority does not follow. | Correct cost premise without inventing grant. | Important | R06/R07; `WC:204-216`; A02/A05. |
| **S11 - Old specification anchors** | Historical pointers no longer locate current sections. | Current anchors or explicitly historical labels. | Minor | R01/R06; citation drift, not changed authority. |
| **S12 - Default setup-run** | Older text conflicts with current skip/default-specific-authorization rule. | Follow current setup authorization. | Important | R01/R06/R08; no setup execution authorized. |
| **S13 - Never-worker list omits issue** | Older list is incomplete against current contract/tests. | Retain current inventory; no issue dispatch as worker. | Important | R01. |
| **S14 - PR-worker opt-in** | PR workers/old opt-in were rejected. | Ordinary top-level D3 carriage. | Important | R06/R08; A11. |
| **S15 - Unconditional linking** | Later fork/Orca-link restrictions qualify old guidance. | Fork-only and no upstream-resolving Orca links. | Important | R06; no remote interaction performed. |
| **S16 - Depth blocks every launch** | Historical tracing counts Dispatch generations; ordinary launches are outside depth checks; Task authority is separate. | Preserve actual route classification with snapshot limits. | Important | R03/R06; A16. Not replacement-build certification. |
| **S17 - Native helpers default to root** | R03's historical creator route contradicts universal root prediction. | Active same-Run creator else Run for that researched route. | Important | Historically source-reconciled, not absent transport. A18 retains exact-target/live limits. |
| **S18 - Task depth unknown** | R03 historically established no depth check on that path. | Retain static answer without mutation or replacement-build transfer. | Minor | R03; separate authority qualification in S19. |
| **S19 - Only WC-13 constrains Tasks** | Historical code includes independent coordinator authority. | No depth check must not imply worker permission. | Important | Source-reconciled R03; A16; `CORRECTION:42-47`. |
| **S20 - Cosmetic workspace lineage** | Host/instance validity checks were traced; lifecycle authority still does not follow. | Validated ancestry, not supervisor grant. | Minor | R03; backing persistence A34. Historical implementation scope retained. |
| **S21 - Blanket owning-Run default** | Historically inspected help omitted implemented native local exception. | Include creator route/fallback in historical interpretation. | Important | R03 help discrepancy; A07/A18. No replacement help/behavior equivalence inferred. |
| **S22 - Old bundle/offsets current** | Historical anchors are not current references. R03 was a later trace relative to older records, but is itself historical relative to the replacement. | Preserve accepted history and dated source observations separately; no filename substitution. | Minor | R01/R03/R06/R08; `CORRECTION:36-47`. AC-0.7 is not erased; vanished bundle is not currently certified. |
| **S23 - Old specification covers liveness** | Omits current chains, handoffs, pending acknowledgments, S11 and detail. | Use current instructions without automatic-monitoring claims. | Important | R02; A19. |
| **S24 - Old C-rule anchors** | Pointers moved. | Correct or qualify historical locations. | Minor | R02. |
| **S25 - Lock sentence old line** | Pointer drifted; substantive immediate-block rule remains. | Separate citation fix from unimplemented bounded wait. | Minor | R02/R06/R08; `WC:45`; A31. |
| **S26 - P1 original FAIL final** | Later PASS/accepted exceptions control closeout; actual Skill invocation remains required. | Preserve both history and controlling outcome, without waiver. | Minor | R06; A32. |
| **S27 - Unattended inventory empty** | P0-empty wording does not describe current populated set/31 headings. | Distinguish declarations, history and live runs. | Important | [STALE DOC]/[CODE-CONTRADICTED current inventory]; R07/R08. Not 31 demonstrated successes. |
| **S28 - Watcher WC-13 pointer** | Old location cited. | Citation qualification only. | Minor | R07. |
| **S29 - #422 still open** | R08 observed merged static scope. | Do not wait on obsolete state or claim live rollout from merge. | Minor | R08; A32. Historical observation, not new remote refresh. |
| **S30 - Old #339 liveness baseline** | Current procedure is newer; incident elimination unproved. | Credit procedures, retain outcome limits. | Important | R08/R02; A19/A26. |
| **S31 - Universal no-Orca implementation** | Narrow coordinator-only claim helper actually creates/launches. Worker ban remains. | Explicit architectural description/exception disposition. | Important | R08/R05; A04. Contradicted description is not disappearance of the normative rule. |
| **S32 - Universal atomic create-with-agent** | Claim intentionally creates then launches. | Qualify universal atomic reading without worker/bare-human-worktree permission. | Important | R05/R08; distinct from A01. |
| **S33 - Spawn execution prose** | Execution-oriented text coexists with explicit decomposition-only stop. | Classify by explicit boundary; retain qualified ambiguity. | Minor | R05. No complete persistent launcher established, not universal absence. |
| **S34 - Skill labels prove hierarchy** | Agent helper assignments and ordinary external launch are not nested Orca Dispatch supervision. | Describe actual mechanism. | Important | Source-reconciled R05/R08; A33. |
| **S35 - No preamble means coordinator** | User-started ordinary-session clause does not define every launched middle session as eligible. | No promotion through missing worker identity. | Important | R01/R08; A01/A07. |
| **S36 - All-executable/all-read guard** | B1/B2 corrections narrow original categorical claims. | Carry literal/probe qualifiers while retaining real defects. | Important | R04/R05/R07 addenda; A13-A15. Research wording fixed, not coverage/policy compatibility. |
| **S37 - Message/transaction precision** | All nine are supported message types, not all settlement types; depth checked before commit with rollback, not necessarily before transaction entry. | Precise vocabulary and ordering. | Minor | G54; no new runtime feature or reopened historical classification. |
| **S38 - Active inventory incomplete** | Later approved current-source/tests/copies scope controls old partial closing text. | Scoped completeness; excluded archives remain unread. | Minor | R07 approval governs earlier supplement continuation language. No repeat archive audit. |

### 4.3 External answers that narrow earlier unknowns

These are findings already present in the assigned web research. They are not new lookups, local deployment certification or authorization.

| Earlier question or interpretation | Established portion | Residual gap and source |
|---|---|---|
| Can incoming peer text be inspected/refused? | Official `UserPromptSubmit` documentation covers another session's main-conversation message and blocking before receipt. | A22 retains installed route coverage, trusted origin, timeout/failure and approval separation. Neither universal absence nor complete security readiness is accurate. W01: https://code.claude.com/docs/en/hooks#userpromptsubmit . |
| Must exact mode names match? | Default policy compares bypass/nonbypass classes, including the interactive-plan exception; inbound controls differ from execution mode. | A21 retains sender-class representation/verification, historical configuration and installed behavior. Matching classes do not guarantee receipt or authority. W01: https://code.claude.com/docs/en/cross-session-messaging#control-inbound-messages . |
| Is attenuation feasible or trustless? | Macaroons/Biscuit support restricted derivatives; verifier trust, third-party proof and authorization inputs differ. CaMeL addresses untrusted-data influence, not signed delegation tokens. | A23/A24 retain trusted request binding, complete enforcement, replay consumption, revocation freshness, maintenance/features and adversarial selection. W03: https://doc.biscuitsec.org/reference/specifications.html ; https://research.google/pubs/macaroons-cookies-with-contextual-caveats-for-decentralized-authorization-in-the-cloud/ ; https://arxiv.org/html/2503.18813v2 . |
| Are nested helpers inherently unsupported? | Public subagent docs permit bounded nesting; public Orca material describes helpers/nested-coordinator terminology. R03 independently traced native local helpers for its original build. | A01/A18/A33 retain policy, role, installed-provider, replacement-build and live limits. W02/W04: https://code.claude.com/docs/en/sub-agents ; https://github.com/stablyai/orca/pull/38348 . |
| Is one the permanent product default? | Public history calls one accidental carryover and later reports default four/migration. Dated local source now defines default/fallback two with guarded migration. | A17/A18/A34 retain effective settings, execution/persistence, remote scope, rollback and unexplained exact-four choice. Historical one and public four are not current loaded values. W04: https://github.com/stablyai/orca/releases/tag/v1.4.251 ; `CORRECTION:18-51`. |
| Do published numbers prove local hierarchy gains? | No inspected comparison isolates the incremental middle layer. W02's controlling correction reports approximately two detected bugs per Devin-authored PR reviewed by Devin Review; 58% of detected bugs severe; approximately eightfold usage growth over six months only in the largest-enterprises segment. Usage metric and absolute baseline are unspecified. | A05/A24 retain the distinction between operational review/adoption observations and causal topology evidence. Do not reuse broader population or ambiguous denominator. W02 correction: https://cognition.com/blog/multi-agents-working . |

### 4.4 Coverage of all 54 compiled gap families

The mappings preserve meaning rather than treating the presence of an ID as coverage. Grouped families are not independent-defect counts. Options and conditions in Sections 6-7, and unresolved questions in Section 9, carry the decision dispositions; Section 8 does not contain step-level fixes.

| GQ families | Substantive destination | Meaning preserved and reason for consolidation |
|---|---|---|
| G01, G23, G25, G26 | A19 | Procedure compliance, five runtime unknowns, incident outcomes and delivery of future automation remain separate within the liveness boundary. |
| G02, G51 | A01/A07/A33 | Role contradiction, ordinary-owner protocol and misleading launcher terminology are different problems, not one missing transport. |
| G03, G33 | A02 | Current rules are established; missing approved extension/autonomous authority is a new policy decision. |
| G04, G24 | A08/A32 | Aggregate progress/outcome and backend report validation concern actual results, not launch/send receipts. |
| G05 | A09 | Mixed-batch ownership, Delivery receipt, application acknowledgment and live handling retain distinct meanings. |
| G06, G07 | A10 | Parent-transition behavior and authority/budgets belong together, but live proof differs from policy definition. |
| G08, G34 | A11/A23 | Real-human escalation/non-transferable grants and cryptographic authorization remain separate. Freeze/Task-specific authority is not collapsed into token integrity. |
| G09 | A20 | Supervisor checkpoint sufficiency explicitly includes roster, budgets, deliveries, applied decisions, admission and uncertain effects. |
| G10, G11 | A05/A06 | Measured local need and interpretation of the missing mailbox prerequisite are separate decisions. |
| G12, G13, G20 | A18 | Live local lifecycle, separate federation and whole-build equivalence remain individually qualified. Historical trace is not replacement-build equivalence. |
| G14, G15, G16 | A17 | Effective loading/reload, safe lowering and bounded per-Run-override absence remain separate settings/reversal issues. Source migration definition is not migration execution. |
| G17 | A16 | Historical route classification is answered; exact-target identity, refusal and behavior still require appropriate evidence. |
| G18, G36, G37, G38, G39 | A33 | Provider limits; ordinary PR placement; helper roles/tiers/startup; watcher uncertain receipts/errors; subprocess isolation are retained, not promoted into Orca supervision. |
| G19 | A07 | Ordinary-owner reporting relationship remains unresolved despite historical native helper routing. |
| G21, G48 | A32 | Historical transcript limits and static-versus-live rollout acceptance are not new tests or missing historical decisions. |
| G22, G53, G54 | A34 | Backing persistence, excluded archives and precision are bounded evidence limitations, not absence of native capability. |
| G27, G28, G30, G31 | A12/A22 | Missing trusted hierarchy binding differs from real hook envelopes, rewrite/job/cwd behavior and first-tool child governance. |
| G29, G32 | A25 | Installation and copy freshness differ from preamble visibility; matching tokens and registered paths do not prove deployment. |
| G35 | A03/A04 | Role selector/D1 interpretation and no-Orca-command packaging need separate dispositions. |
| G40, G41 | A21/A22 | Documentation answers feature availability partly; authenticated application protocol and actual deployed coverage remain unproved. |
| G42, G43, G49 | A23/A24 | Credential feasibility, existing capability reuse, library maintenance/selection and benchmark transfer are distinct from readiness. |
| G44 | A26/A27 | Flat registry/sweep/attention/report/server/closure scope is retained; destructive cleanup predicates receive independent treatment. |
| G45, G46, G47 | A29/A30/A31 | Release numbering, observer provenance and independent Git/lock work are not invented hierarchy prerequisites. |
| G50 | A02/A27/A28 | Fan-out authority, destructive disposal/recovery, human interaction, placement and presentation retain different consequences. |
| G52 | A13/A14/A15 | Fixed research overstatement does not fix launch/report policy, executable coverage or omitted supervision probes. |

### 4.5 Source coverage, precedence and justified exclusions

| Source | Load-bearing findings represented | Scope or consolidation boundary |
|---|---|---|
| **R01 and complete return** | A01-A04/A07-A12; D1-D5; admission, grants, retry, placement, freezes and human authority. | Full clause matrices inform adoption conditions and Section 6. Compatible safeguards are not new defects; compatibility is not live success. |
| **R02 and complete return** | A08-A11/A18-A20/A32; own/child signals, mixed batches, states, budgets, human relay, #431/#434 limits. | S0-S11, A1-A4 and L0-L5 remain procedures, not a newly executed state machine or measured hierarchy deadline. |
| **R03 and complete return** | A07/A09/A16-A18/A34; route/Task authority, parentages, ordinary launch, settings and historical/source/live distinctions. | Answers older guesses for its snapshot. Dated correction prevents current-installation transfer; S37 preserves transaction/message precision. |
| **R04 and complete return** | A12-A15/A22/A25; distinct inputs/bindings, ceilings and live/deployment questions. | B1/B2 governs older categorical returns. No alternate-spelling success, universal enforcement or automatic expansion inferred. |
| **R05 and complete return** | A04/A07/A25/A33; receipts versus supervision; partial scheduling/results/durability patterns. | Fourteen launcher types and 56 reuse judgments inform analysis; not repeated as new requirements or complete O3 precedent. |
| **R06 and complete return** | A01-A06/A11/A17/A32; approved decisions, trigger, textual divergence and historical acceptance. | R03 resolves earlier slice-local unknowns historically; neither trace establishes live behavior, replacement equivalence or measured need. |
| **R07, complete return and supplements** | A12-A17/A25/A34/S27/S38; source/copy/test surfaces and distribution. | Approved active inventory is complete; 867 matching archival lines/274 paths remain unread background. No archive reopening or implementation sequence. |
| **R08 and complete return** | A01-A04/A11/A21-A33; all 35 requirement dispositions, independent scopes and conflicts. | Extraction is not delivery. #409 remains observer-only, #423 gets no control authority, #446/#326 stay independent. |
| **W01 and complete return** | A09/A11/A21/A22/A33; inbound hook, mode classes, channel guarantees, origin/fail-closed questions. | SDK/community examples do not certify a validator; official plan-class wording controls discrepancy. No new lookup or settings change. |
| **W02 and complete return** | A05/A08-A10/A19/A20/A24/A33/A34; flat baseline, context/cost tradeoffs, lifecycle analogy and no matched local hierarchy result. | All 17 findings and numeric caveats feed Section 5. Nonlocal numbers are not local forecasts. Cognition correction governs population/denominators; unseen notebook internals excluded. |
| **W03 and complete return** | A11/A12/A23/A24/A34; narrowing, verifier trust, authorization, replay/revocation, enforcement and CaMeL. | No adopted dependency or debate winner. Full original macaroon PDF extraction was not established; readable evidence retains its limit. |
| **W04 and complete return** | A01/A16-A18/A34; public helper/depth, migration, host/version and shutdown distinctions. | Public terminology is not full role contract. Public defaults/stop behavior are not backported; source 404 remains unexplained. |
| **GQ** | All G01-G54 and S01-S38. | Research dispositions preserved. Adoption-impact severity does not mutate the register or authorize fixes. |
| **Controlling snapshot correction** | SC07; settings, route/equivalence and path claims throughout A07/A09/A10/A16-A18/A25/A34 and stale-source dispositions. | Bounded new source observations only. Historical filename/offsets retained, vanished path excluded from current certification. No current profile/effective/runtime claim added. |

**Decision significance:** Historical native helper evidence is stronger than the old root-mailbox prediction, and the new source default/fallback two is stronger than a stale current-default-one claim. Neither establishes approved authority, measured need, aggregate admission, complete recovery or exact-target operation. An evidence-complete deferral therefore remains possible without pretending the adoption gaps are solved. It does not close A01 or erase INF-027's explicit scope record.

**Limits:** No new implementation sequence, source validation campaign, external research, archived-original reopening, live nesting, settings change, test, build, sync or installation was performed for these sections. The unresolved questions are evidence and policy requirements, not authorization to conduct the proposed evaluations.

## 5. External Research Findings
External research supplies context and alternatives. It does not override verified project policy or establish installed behavior, implementation readiness or permission.

This section preserves 46 individual findings from the complete synthesis: M01-M12, H01-H15, G01-G10 and O01-O09. Reliability ratings concern the cited evidence, not deployment certainty. Local comparisons are attributed to the researchers who made them; this assembly performs no new external research or implementation validation.

**Controlling corrections:**

- W02's numerical correction controls its immutable original: Cognition's severity denominator is **detected bugs**, and the approximately eightfold usage increase concerns only its **largest enterprises segment**.
- `CORRECTION` controls all current-installation claims. R03/W04's original build, source-default-one and stored-one observations are historical. The dated replacement-source observation establishes default/fallback **two** and guarded migration, not current stored/effective values, migration execution or replacement-build equivalence.
- Public default **four**, provider capabilities and newer shutdown announcements remain separately attributed external evidence.
- Historical backend filenames and offsets remain historical. The vanished bundle is not certified as a current existing file, and its replacement filename is not substituted automatically.

**Evidence:** W02 controlling addendum; `CORRECTION:8-51`; `qa/qa-consolidated-findings-phase5.md:25-32`.

### 5.1 Claude Code cross-session messaging and permission modes

#### M01 - Default delivery compares permission classes, not identical mode names

**Finding - external context:** Official documentation separates sessions that bypass permission prompts from other sessions. It places `auto`, `acceptEdits` and `dontAsk` in the prompting class, with an interactive-terminal plan-mode exception when bypass permissions are available. Under permission-derived defaults, messages crossing classes are held; matching classes ordinarily allow delivery subject to other controls. Exact mode-name equality is neither the documented requirement nor a complete delivery guarantee. The community guide's conflicting plan-mode classification does not override the official matrix. Historical effective modes remain unobserved.

| Field | Assessment |
|---|---|
| Sources | https://code.claude.com/docs/en/cross-session-messaging#control-inbound-messages ; https://cc.bruniaux.com/guide/workflows/cross-session-messaging/ |
| Relevance | HIGH for official matrix; LOW for community discrepancy. |
| Reliability | HIGH official documentation; MEDIUM community guide. |
| Relationship | **Extends** the held-message explanation and **contradicts** exact-mode-equality interpretation, not the historical sessions' unknown configuration. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### M02 - Held messages are not already in the recipient's context

**Finding - external context:** Delivered, Held and Refused differ. A held message does not reach the recipient model until approval or an applicable later setting/mode change. Under the default interactive policy, approval delivers; denial or dismissal drops; the default dialog deadline is five minutes. Explicit `hold` differs: those messages do not expire and may be released by an applicable `accept` setting. The interactive deadline must not be generalized to detached-background sessions without an attached terminal, where it can be deferred. The held queue has capacity 100 with oldest-message dropping; the accepted queue's capacity 50 is a different limit.

| Field | Assessment |
|---|---|
| Sources | https://code.claude.com/docs/en/cross-session-messaging#control-inbound-messages ; https://code.claude.com/docs/en/cross-session-messaging#non-interactive-sessions ; https://code.claude.com/docs/en/settings-reference#dialogexpiry |
| Relevance | HIGH. |
| Reliability | HIGH official behavior descriptions. Background/queue qualifications are carried from `qa/phase4-boundary-numbers.md`, finding **numbers4-11**, not newly runtime-tested. |
| Relationship | **Supports** a plausible hold mechanism and **extends** unattended-delivery risks; does not reproduce the reported incident. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### M03 - The sender-class question remains partly unanswered

**Finding - external context:** Session permission controls are documented, including activating bypass versus merely making it selectable. The reviewed pages do not establish exact per-message representation/verification of the sender's permission class or a supported per-send class-assertion argument. Message text is not a documented identity mechanism. Historical sender mode and receiving settings were not observed. Messaging availability is version-dependent; installed support was not established.

| Field | Assessment |
|---|---|
| Sources | https://code.claude.com/docs/en/permission-modes ; https://code.claude.com/docs/en/cli-reference#cli-flags ; https://code.claude.com/docs/en/tools-reference ; https://code.claude.com/docs/en/cross-session-messaging#availability ; https://github.com/IronbellyOrg/IronClaude/issues/339#issuecomment-6659559030 |
| Relevance | HIGH. |
| Reliability | HIGH supported interfaces and primary issue wording; internal class-identification protocol and historical configuration **[UNVERIFIED]**. |
| Relationship | **Extends** #339 question 1 without closing its internal-protocol or deployment questions. |
| Local launcher selection (local baseline, not an external finding) | **[CODE-VERIFIED]** The local launcher selects bypass flags when `CCSESSION_PERMISSIONS` is unset, omits the bypass flag for `default`, rejects other values, and lets explicit `CC_CLAUDE_FLAGS` override the defaults. This is a starting-flag selection, not proof of the effective mode of any historical or current session. Evidence: `src/superclaude/skills/ccsession-tag/ccsession:135-141`; W01. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### M04 - Inbound acceptance is separate from execution permission

**Finding - external context:** `crossSessionInbound` documents `accept`, `hold` and `refuse`. Precedence checks managed, explicit and user settings for the first applicable value; project/local settings may tighten rather than loosen the result. This is not a documented named-parent trust list. Independently, `isolatePeerMachines` at any scope requires approval for beyond-machine messages, including in bypass mode. Universal bypass is therefore not the only documented response to class-derived holds, and acceptance does not authorize actions.

| Field | Assessment |
|---|---|
| Sources | https://code.claude.com/docs/en/settings-reference#crosssessioninbound ; https://code.claude.com/docs/en/settings-reference#isolatepeermachines |
| Relevance | HIGH. |
| Reliability | HIGH official documentation. |
| Relationship | **Extends** decision alternatives while preserving approved settings, trusted sender binding and separate action authorization. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### M05 - An incoming-message hook is documented, with deployment limits

**Finding - external context:** `UserPromptSubmit` expressly includes another session's message to the main conversation. It receives prompt text and can block before the model receives it through documented blocking results or exit behavior. The feature-level answer to #339 question 2 is **documented yes**, not “no inbound hook exists.” This does not prove installed coverage across active/idle, remote, teammate or nested-recipient routes, or a complete authenticated authorization layer.

| Field | Assessment |
|---|---|
| Source | https://code.claude.com/docs/en/hooks#userpromptsubmit |
| Relevance | HIGH. |
| Reliability | HIGH documented behavior; installed coverage **[UNVERIFIED]**. |
| Relationship | **Extends** the incoming-hook answer while leaving deployed event coverage and security adequacy open. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### M06 - Receiving-context fields are not authenticated peer authority

**Finding - external context:** Common hook fields describe receiving execution context: current session, permission mode and applicable subagent/teammate identifiers. `prompt` and optional `session_title` do not establish authenticated peer identity, parent Dispatch or grant lineage. Transcripts may lag asynchronous writes. Additional trusted origin metadata might exist but was not established. The official SDK example demonstrates generic registration and denial, not a complete receiving-peer validator.

| Field | Assessment |
|---|---|
| Sources | https://code.claude.com/docs/en/hooks#common-input-fields ; https://code.claude.com/docs/en/hooks#userpromptsubmit-input ; https://github.com/anthropics/claude-agent-sdk-python/blob/main/examples/hooks.py |
| Relevance | HIGH identity boundary; MEDIUM SDK example. |
| Reliability | HIGH documented fields/primary example; additional runtime metadata **[UNVERIFIED]**. |
| Relationship | **Supports** the trusted-origin gap and **extends** parent-bound validation requirements. Does not establish universal absence of authenticated metadata. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### M07 - A hook that can block is not automatically fail-closed

**Finding - external context:** Explicit blocking differs from timeout/failure handling. Ordinary prompt-hook timeout can discard output and continue. Command/HTTP `onFailure: block` is a separate feature with documented minimum **2.1.295**; installed applicability remains unverified. SDK callback timeout behavior is separately documented. The researcher's local-source comparison recorded a five-second registration without that setting; a shell trap was not considered proof of host-timeout handling. Ordering, installation freshness and peer-versus-human approval-envelope separation remain untested. No approval-laundering exploit was demonstrated.

| Field | Assessment |
|---|---|
| Sources | https://code.claude.com/docs/en/hooks#userpromptsubmit ; https://code.claude.com/docs/en/hooks#pretooluse ; https://code.claude.com/docs/en/hooks#posttooluse ; https://code.claude.com/docs/en/hooks#permissionrequest ; https://code.claude.com/docs/en/hooks#notification |
| Relevance | HIGH. |
| Reliability | HIGH documented distinctions/researcher source comparison. Minimum-version qualifier comes from `qa/phase4-boundary-provenance.md`, **provenance4-N2**; not independently rechecked in assembly. |
| Relationship | **Extends** enforcement conditions; does not certify the existing hook as a fail-closed message validator. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

| External hook | Supported role | Limit |
|---|---|---|
| `PreToolUse` matching a send | Inspect sender action before execution. | Not universal receiving-side interception. |
| `PostToolUse` | Inspect executed call/result. | Cannot unsend an executed message. |
| `PermissionRequest` | Handle tool permission decision. | Not every incoming message. |
| `Notification` | Observe notifications. | Cannot block or modify them. |

This table inherits M07's sources and ratings; it is not an installed-coverage claim.

#### M08 - Preserve each channel's actual guarantee

**Finding - external context:** Peer messages, team mail and final subagent reports have different guarantees. Neither “send success means processed” nor “nothing is guaranteed” is accurate across them.

| Field | Assessment |
|---|---|
| Sources | https://code.claude.com/docs/en/cross-session-messaging#message-delivery ; https://code.claude.com/docs/en/errors#cross-session-message-was-dropped-at-the-recipient-sessions-inbox ; https://code.claude.com/docs/en/agent-teams#architecture ; https://code.claude.com/docs/en/permission-modes#eliminate-prompts-with-auto-mode |
| Relevance | HIGH. |
| Reliability | HIGH official documentation. |
| Relationship | **Supports** separate transport, application-acknowledgment and result-admission evidence. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

| External channel | Documented behavior/guarantee | What it does not establish |
|---|---|---|
| Independent cross-session messages | Active recipients read between tool calls; tools are not interrupted. Idle recipients start a turn. Refusal, `Not sent`, holds, expiry and recipient drops remain possible. | Universal positive send-return guarantee of reading, applying, eventual execution or completion. |
| Agent-team mail | Sent means mailbox-file write succeeded; failed writes return error. | Reading, accepting, applying or completing work. |
| Final subagent handback in auto mode | Flagged final report is delivered with warning, or verification note when classifier is unavailable. | Equivalent delivery for blocked outbound SendMessage. |

The table inherits M08's sources/ratings. Team mailbox-write semantics do not transfer to peer or Orca transport.

#### M09 - Typed text is not a secure application protocol

**Finding - external context:** Independent peer transport is plain text; structured team protocols remain inside their team. File/MCP mentions attach no contents; slash commands arrive as text rather than autoexecuting. Naming types/resources in an envelope does not authenticate origin, authorize effects, prevent replay, ensure safe parsing or settle lifecycle. Schema-valid files likewise do not establish producer identity, freshness or safe admission.

| Field | Assessment |
|---|---|
| Sources | https://code.claude.com/docs/en/cross-session-messaging#limitations ; https://code.claude.com/docs/en/cross-session-messaging#how-a-session-treats-an-incoming-message |
| Relevance | HIGH. |
| Reliability | HIGH transport behavior; application implications are attributed researcher analysis. |
| Relationship | **Extends** typed-message/file-report proposals without treating either as implemented authorization. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### M10 - Idle notices are observations, not completion

**Finding - external context:** Idle subscriptions are one-shot, main-conversation-only, same-machine and inbound-controlled; they expire after 12 hours without a notice. Trigger is a turn ending with nothing queued or session exit. It does not prove successful work, admitted evidence, settled descendants, clean worktree or closure authority.

| Field | Assessment |
|---|---|
| Source | https://code.claude.com/docs/en/cross-session-messaging#get-a-notice-when-another-session-goes-idle |
| Relevance | MEDIUM. |
| Reliability | HIGH official documentation. |
| Relationship | **Supports** liveness/progress/completion separation and **extends** observation signals without replacing supervision. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### M11 - Receipt and mode alignment cannot manufacture human consent

**Finding - external context:** Peer text cannot approve permissions, supply human consent or authorize changes to permission settings, configuration or `CLAUDE.md`. Recipient actions remain permission-bound; denied work cannot be routed to another session. Auto-mode outbound review may block a message, unlike M08's final-report handback. Bypass is neither injection protection nor isolation.

| Field | Assessment |
|---|---|
| Sources | https://code.claude.com/docs/en/cross-session-messaging#how-a-session-treats-an-incoming-message ; https://code.claude.com/docs/en/agent-teams#messages-between-agents ; https://code.claude.com/docs/en/permission-modes |
| Relevance | HIGH. |
| Reliability | HIGH official documentation. |
| Relationship | **Supports** human-only authority and **contradicts** interpreting accepted/signed text or aligned modes as a trustless grant. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### M12 - Subagents, teams and independent sessions differ

**Finding - external context:** Public documentation permits bounded subagent nesting, describes experimental teams without nested teams, and separately describes peer messaging. Child subagent permissions remain constrained by main-conversation mode; definitions cannot arbitrarily elevate them. Those rules do not establish independently launched Orca sessions' permission inheritance, ownership or recovery. Internal decomposition is not automatically another external supervision tier.

| Field | Assessment |
|---|---|
| Sources | https://code.claude.com/docs/en/sub-agents ; https://code.claude.com/docs/en/agent-teams#limitations ; https://code.claude.com/docs/en/cross-session-messaging |
| Relevance | HIGH. |
| Reliability | HIGH public documentation; installed applicability **[UNVERIFIED]**. |
| Relationship | **Supports** separating O5 from O3/O4. Corrects blanket no-nesting premises, not project policy. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

### 5.2 Hierarchical orchestration patterns

#### H01 - Parallel research benefit does not prove another supervisory generation

**Finding - external context:** Anthropic's research system uses one lead and parallel independent specialists. That demonstrates flat supervised research fan-out, not an additional middle coordinator. Extensive shared context and tightly coupled coding are described as poorer fits than independently explorable research.

| Field | Assessment |
|---|---|
| Source | https://www.anthropic.com/engineering/multi-agent-research-system |
| Relevance | HIGH. |
| Reliability | HIGH own-system architecture/observations; MEDIUM transfer. |
| Relationship | **Supports** flat baseline and bounded investigation, not demonstrated O3/O4 gains. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### H02 - Briefs, artifacts and stopping rules matter

**Finding - external context:** Vague delegation caused overlap, gaps and inconsistent interpretation. Explicit objectives, deliverables, tools/sources and boundaries improve clarity. Artifact references reduce repeated transfer and summary degradation. Overspawning, excessive updates, prolonged search and prompt sensitivity create waste; no isolated effect size is established for each safeguard.

| Field | Assessment |
|---|---|
| Source | https://www.anthropic.com/engineering/multi-agent-research-system |
| Relevance | HIGH. |
| Reliability | HIGH first-party engineering observations. |
| Relationship | **Supports** scoped briefs, evidence-preserving admission and bounds; **extends** them to any middle layer. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### H03 - Parallel work retains synchronization costs

**Finding - external context:** The reported system waits at synchronous batch boundaries and cannot redirect active workers; a slow worker can delay the lead. Asynchronous operation is future work with reconciliation, consistency and failure-propagation problems, not measured improvement.

| Field | Assessment |
|---|---|
| Source | https://www.anthropic.com/engineering/multi-agent-research-system |
| Relevance | HIGH. |
| Reliability | HIGH for reported system. |
| Relationship | **Extends** latency/blocked-parent concerns; parallelism alone does not prove another supervisor reduces time. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### H04 - Dynamic decomposition needs task-shape justification

**Finding - external context:** Guidance favors the simplest adequate workflow and distinguishes predefined independent work from subtasks that cannot reasonably be determined beforehand. The researcher identifies coherent newly discovered work and local informational advantage as a plausible middle-role opportunity, not task size, agent count or worktree ancestry alone.

| Field | Assessment |
|---|---|
| Sources | https://www.anthropic.com/engineering/building-effective-agents ; https://www.langchain.com/blog/langgraph-multi-agent-workflows |
| Relevance | HIGH. |
| Reliability | HIGH architectural guidance; MEDIUM decision transfer. |
| Relationship | **Supports** runtime-discovered split/material avoided-round-trip evidence rather than assumed benefit. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### H05 - Context, depth, concurrency and lifetime are separate

**Finding - external context:** Fresh subagents reduce parent clutter but need reconstruction; forks inherit conversation. Usage remains shared, and returns consume parent context. Published documentation describes up to three layers below main and a separate default concurrency 20 with exceptions. The concurrency feature's cited minimum is 2.1.217; no nesting-introduction version was established. A fork tool-visibility exception does not prevent spawn errors at the cap. Some print/SDK background behavior allows a nested child to outlast its spawning subagent and return to main. None establishes installed Orca lifecycle.

| Field | Assessment |
|---|---|
| Source | https://code.claude.com/docs/en/sub-agents |
| Relevance | HIGH. |
| Reliability | HIGH published mechanics; installed applicability **[UNVERIFIED]**; MEDIUM lifecycle transfer. |
| Relationship | **Extends** O5 tradeoffs and **contradicts** universal provider no-nesting, not WC-13. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### H06 - OTP teaches lifecycle, not semantic correctness

**Finding - external context:** OTP supports worker/supervisor children, restart strategies (restart only the failed child, restart the entire sibling group, or restart the failed child plus later-started dependents), ordered startup and reverse shutdown. Nested restart intensities multiply: its 10-by-10 example permits 100 within relevant restart-intensity behavior/windows, not a lifetime LLM allowance. Its smaller upper-level example is not an LLM recommendation. Finite shutdown may kill a supervisor before descendants settle; unlimited cleanup may hang; synchronous ancestor termination requests may deadlock in the described waiting relationship. These are mechanisms and analogies, not observed local failures.

| Field | Assessment |
|---|---|
| Source | https://www.erlang.org/doc/system/sup_princ.html |
| Relevance | HIGH lifecycle; MEDIUM LLM transfer. |
| Reliability | HIGH OTP mechanisms; MEDIUM transfer. Window qualification also recorded in `qa/phase4-boundary-numbers.md`, **numbers4-10**. |
| Relationship | **Extends** lineage resources, cancellation, takeover and ownership. Restart is not correct results, preserved human authority or safe repeated effects. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### H07 - LangGraph demonstrates composition, not a benchmark winner

**Finding - external context:** The January 2024 explanation distinguishes shared scratchpads, separate histories under a supervisor and nested graphs. The supervisor repository describes compiled subteams, full-history/final-message returns, separate handoff/return controls and forwarding without paraphrase. The retrieved repository was archived/read-only and recommended direct tool-calling supervision for most new work; in-memory checkpoint examples do not prove durability. Current guidance distinguishes per-invocation/persistent state and blocking/background work requiring job/status/result infrastructure. The old notebook was a moved-file stub; partial historical extraction did not establish unseen adapter internals.

| Field | Assessment |
|---|---|
| Sources | https://www.langchain.com/blog/langgraph-multi-agent-workflows ; https://github.com/langchain-ai/langgraph-supervisor-py ; https://docs.langchain.com/oss/python/langchain/multi-agent/subagents ; https://raw.githubusercontent.com/langchain-ai/langgraph/main/examples/multi_agent/hierarchical_agent_teams.ipynb ; https://raw.githubusercontent.com/langchain-ai/langgraph/23961cff61a42b52525f3b20b4094d8d2fba1744/docs/docs/tutorials/multi_agent/hierarchical_agent_teams.ipynb |
| Relevance | HIGH composition/context; MEDIUM package status/historical artifacts. |
| Reliability | HIGH observed descriptions/status; MEDIUM historical-example applicability; unseen internals **[UNVERIFIED]**. |
| Relationship | **Extends** context/monitoring choices, not framework adoption or measured hierarchy superiority. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### H08 - AutoGen conversation limits are not subtree budgets

**Finding - external context:** AutoGen 0.2 encapsulates individual/group chats behind summaries; carryover accumulates and the outer response defaults to the final nested summary. Its trigger excludes internal participants to avoid recursion. `max_turns` and `max_round` differ in scope; last-message/model summaries differ too. Toy traces and costs, including missed targets, do not establish comparative latency or reliability.

| Field | Assessment |
|---|---|
| Source | https://microsoft.github.io/autogen/0.2/docs/tutorial/conversation-patterns/ |
| Relevance | HIGH encapsulation/bounds; MEDIUM examples. |
| Reliability | HIGH versioned mechanics; LOW performance evidence. |
| Relationship | **Extends** composite/summary-loss questions and **supports** whole-task limits rather than reset local allowances. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### H09 - CrewAI manager duties do not prove parallelism

**Finding - external context:** CrewAI describes a required automatic/custom manager assigning, checking and determining completion, plus planning, context, rate and iteration controls. Reviewed pages do not establish concurrent delegation, shared monetary/token ceiling or measured superiority over flat alternatives.

| Field | Assessment |
|---|---|
| Sources | https://docs.crewai.com/en/learn/hierarchical-process ; https://docs.crewai.com/en/concepts/processes |
| Relevance | HIGH. |
| Reliability | HIGH mechanics and bounded limitation. |
| Relationship | **Extends** middle-role duties and **supports** separating management, parallel execution and aggregate budgets. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### H10 - Credible critiques favor bounded collaboration, not permanent prohibition

**Finding - external context:** Cognition's June 2025 critique emphasizes lost consequential decisions and incompatible parallel coding choices. Its April 2026 follow-up reports useful author/reviewer loops, consultation and hierarchical coordination, while retaining information-sharing and granularity questions. The worktree implication is explicitly the researcher's inference: isolated files avoid direct collisions without ensuring compatible assumptions or cheap integration. Neither article establishes a universal failure rate.

| Field | Assessment |
|---|---|
| Sources | https://cognition.com/blog/dont-build-multi-agents ; https://cognition.com/blog/multi-agents-working |
| Relevance | HIGH. |
| Reliability | MEDIUM practitioner/operational report, not controlled topology study. |
| Relationship | **Supports** bounded collaboration, context continuity and explicit integration/admission ownership, not unrestricted fan-out or timeless multi-agent rejection. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### H11 - MAST identifies failure categories, not the best topology

**Finding - external context:** MAST v3, revised October 26, 2025, reports 14 failure modes across over 1,600 traces/seven frameworks: context loss, repetition, unclear stopping, missing clarification, withheld information, premature termination and defective verification among them. Most corpus labels were machine-produced, with smaller expert sets. Categories are not independent per-task probabilities; interventions vary by model/benchmark. No controlled hierarchy-versus-flat effect was isolated.

| Field | Assessment |
|---|---|
| Sources | https://arxiv.org/abs/2503.13657 ; https://arxiv.org/html/2503.13657v3 |
| Relevance | HIGH. |
| Reliability | HIGH primary study, bounded by systems, labels and evaluation scale. |
| Relationship | **Supports** stopping, clarification and aggregate verification. Managers can relocate rather than remove errors. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### H12 - Published numbers do not price an extra middle layer

**Finding - external context:** The following nine observation groups retain their original baselines. None estimates the incremental middle supervisor over this project's flat arrangement.

| Field | Assessment |
|---|---|
| Sources | https://www.anthropic.com/engineering/multi-agent-research-system ; https://www.erlang.org/doc/system/sup_princ.html ; https://arxiv.org/html/2503.13657v3 ; https://cognition.com/blog/multi-agents-working |
| Relevance | HIGH evidence boundary; row-specific ratings below. |
| Reliability | HIGH primary reported observations except MEDIUM Cognition operational report; transfer limited. |
| Relationship | **Extends** context and **supports** local measurement requirements. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

| External observation | Baseline and permitted interpretation | Relevance / reliability / relationship | Source |
|---|---|---|---|
| Anthropic 90.2% outperformance | Opus 4 lead/Sonnet 4 workers versus single-agent Opus 4 on internal research evaluation. Not percentage-point accuracy or extra-depth gain. | HIGH / HIGH report, MEDIUM transfer / extends. | https://www.anthropic.com/engineering/multi-agent-research-system <!-- web-provenance: provider=WebSearch reason=tavily-unavailable --> |
| Approximately 4× agent and 15× multi-agent tokens | Both relative to ordinary chat, not 15× single-agent research, dollars or hierarchy penalty. | HIGH / HIGH observational / extends. | https://www.anthropic.com/engineering/multi-agent-research-system <!-- web-provenance: provider=WebSearch reason=tavily-unavailable --> |
| Up to 90% research-time reduction; 3-5 workers, 3+ tools each | Combined parallelization on complex queries; no isolated topology contribution or typical/percentile guarantee. | HIGH / HIGH first-party report / supports parallelism, not extra depth. | https://www.anthropic.com/engineering/multi-agent-research-system <!-- web-provenance: provider=WebSearch reason=tavily-unavailable --> |
| 80% variance explained by tokens; 95% jointly by tokens/tools/model | BrowseComp association, not accuracy increases or causal architecture effects. | MEDIUM / HIGH reported analysis / extends evidence limits. | https://www.anthropic.com/engineering/multi-agent-research-system <!-- web-provenance: provider=WebSearch reason=tavily-unavailable --> |
| 40% completion-time reduction; roughly 20-request initial evaluation; illustrative 30%→80% | Tool-description intervention, evaluation scale and illustration respectively, not separate overall/hierarchy benchmarks. | MEDIUM / HIGH wording, limited methods / supports brief/tool quality. | https://www.anthropic.com/engineering/multi-agent-research-system <!-- web-provenance: provider=WebSearch reason=tavily-unavailable --> |
| OTP 10×10=100 restarts | Restart-intensity example within relevant windows, not lifetime LLM budget or suggested allowance. | HIGH / HIGH mechanism / supports lineage accounting. | https://www.erlang.org/doc/system/sup_princ.html <!-- web-provenance: provider=WebSearch reason=tavily-unavailable --> |
| MAST 25.0%, 34.4%, 40.6% | ChatDev baseline/prompt/topology on 32 custom ProgramDev-v0 tasks; 9.4/15.6 percentage-point differences. HumanEval differed. Not general gains or clean hierarchy comparison. | MEDIUM / HIGH primary, limited scale / extends. | https://arxiv.org/html/2503.13657v3 <!-- web-provenance: provider=WebSearch reason=tavily-unavailable --> |
| MAST p=0.4 versus p=0.03 | Model-dependent AG2 interventions. Annotation API spend is not task-execution cost. | MEDIUM / HIGH / supports caution. | https://arxiv.org/html/2503.13657v3 <!-- web-provenance: provider=WebSearch reason=tavily-unavailable --> |
| Cognition approximately two detected bugs per Devin-authored PR reviewed by Devin Review; approximately 58% of detected bugs severe; approximately 8× usage growth over six months in largest enterprises segment | **Controlling corrected wording.** Severity denominator is detected bugs, not PRs. Growth population is largest enterprises only; usage metric/absolute baseline unspecified. Not causal hierarchy, net-quality, false-positive, cost or latency evidence. | LOW numerical relevance / MEDIUM operational report / supports evidence limits. | https://cognition.com/blog/multi-agents-working <!-- web-provenance: provider=WebSearch reason=tavily-unavailable --> |

The Cognition qualification is controlled by W02's correction and the original population finding **numbers4-04** in `qa/phase4-boundary-numbers.md`; the uncorrected original remains provenance only.

#### H13 - Flat-versus-hierarchy tradeoffs remain conditional

**Finding - external context:** Potential benefits and costs can be compared qualitatively without inventing local estimates.

| Field | Assessment |
|---|---|
| Sources | https://www.anthropic.com/engineering/multi-agent-research-system ; https://code.claude.com/docs/en/sub-agents ; https://www.erlang.org/doc/system/sup_princ.html ; https://arxiv.org/html/2503.13657v3 ; https://docs.langchain.com/oss/python/langchain/multi-agent/subagents ; https://cognition.com/blog/multi-agents-working |
| Relevance | HIGH. |
| Reliability | HIGH mechanisms; MEDIUM transfer. |
| Relationship | **Extends** O3/O4 assessment against flat baseline; no winning topology established. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

| Dimension | Flat supervision | Additional middle layer | External basis |
|---|---|---|---|
| Cost | Direct workers, briefs and root synthesis already consume resources. | Adds planning/reporting/context; coherent encapsulation might reduce root reconstruction. No matched estimate. | https://www.anthropic.com/engineering/multi-agent-research-system ; https://code.claude.com/docs/en/sub-agents <!-- web-provenance: provider=WebSearch reason=tavily-unavailable --> |
| Latency | Direct independent workers already run concurrently. | May avoid unforeseen-work round trip; adds serial planning/aggregation and slow-child waits. | https://www.anthropic.com/engineering/multi-agent-research-system ; https://docs.langchain.com/oss/python/langchain/multi-agent/subagents <!-- web-provenance: provider=WebSearch reason=tavily-unavailable --> |
| Error propagation | Root can misdecompose/admit wrong results. | Middle can catch errors or propagate wrong interpretation/premature success. | https://arxiv.org/html/2503.13657v3 <!-- web-provenance: provider=WebSearch reason=tavily-unavailable --> |
| Context loss | One delegation edge can already lose evidence. | More isolation and more boundaries for losing constraints/decisions/questions. | https://code.claude.com/docs/en/sub-agents ; https://cognition.com/blog/dont-build-multi-agents <!-- web-provenance: provider=WebSearch reason=tavily-unavailable --> |
| Coordination | Root monitors/adopts direct results. | Less root detail can mean more acknowledgments, questions, reconciliation and dual monitoring. | https://docs.langchain.com/oss/python/langchain/multi-agent/subagents ; https://microsoft.github.io/autogen/0.2/docs/tutorial/conversation-patterns/ <!-- web-provenance: provider=WebSearch reason=tavily-unavailable --> |
| Recovery | Fewer supervisory ownership transitions. | Useful failure domain requires cancel/settlement/takeover; otherwise children can be stranded. | https://www.erlang.org/doc/system/sup_princ.html <!-- web-provenance: provider=WebSearch reason=tavily-unavailable --> |
| Budgets | Direct fan-out easier to count centrally. | Independent allowances multiply without lineage accounting. | https://www.erlang.org/doc/system/sup_princ.html ; https://microsoft.github.io/autogen/0.2/docs/tutorial/conversation-patterns/ <!-- web-provenance: provider=WebSearch reason=tavily-unavailable --> |
| Coupled writes | Integration owner can preserve shared decisions. | File isolation does not ensure compatible assumptions or cheap integration. | https://cognition.com/blog/dont-build-multi-agents ; https://cognition.com/blog/multi-agents-working <!-- web-provenance: provider=WebSearch reason=tavily-unavailable --> |

All rows inherit H13's HIGH relevance, HIGH mechanism reliability/MEDIUM transfer and **extends** relationship.

#### H14 - Correcting historical premises does not change permission

**Finding - attributed researcher comparison:** Command chains weaken the old one-command premise; historically traced creator routing corrects a universal root-mailbox prediction. Neither supplies autonomous authority, recursive admission or recovery. Dual duties, policy exception and broader-setting/scoped-brief questions remain. Literal executable coverage and omitted required probes are additional integration limits, not bypass permission. Development-source comparisons and historical installed traces are not complete replacement-build certification.

| Field | Assessment |
|---|---|
| Sources | https://www.anthropic.com/engineering/building-effective-agents ; https://www.erlang.org/doc/system/sup_princ.html ; https://code.claude.com/docs/en/sub-agents ; file:///home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/.dev/orca-command-refactor/decisions/D5/RECOMMENDATION.md ; file:///home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/src/superclaude/core/WORKER-CONTRACT.md ; file:///home/coder/workspaces/IronOrca/src/main/runtime/orchestration/dispatch-report-mailbox.ts ; file:///home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/src/superclaude/hooks/scripts/launch-level-guard.sh |
| Relevance | HIGH. |
| Reliability | HIGH recorded researcher source comparisons; MEDIUM transfer. No independent source reread by assembly. |
| Relationship | **Extends** corrected D5 reasoning and **contradicts** obsolete premises, not current prohibition. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

| Historical cost | Preserved qualification |
|---|---|
| Undefined composite brief | Chains are not discretionary decomposition/dispatch authority. |
| Second coordinator | Upward worker and downward supervisor duties need explicit composition. |
| Questions probably reach root | Historical creator route exists; exact-target/live mixed-mail/recovery evidence remains separate. |
| WC-13 exception | Public capability does not make policy decision. |
| Scoped brief inside broader setting | Effective propagation, per-brief limits and reversal remain unverified; current source default two is not effective-state proof. |

#### H15 - A middle supervisor must own more than routing

**Finding - external context and unresolved implications:** Routing does not define aggregate failed/blocked/partial success, own-versus-child progress, service during parent blocking/replacement, complete checkpoint or actual-human escalation. Cancellation, uncertain effects, pending deliveries, resources and replacement ownership require explicit treatment. Flat admission is not recursive admission. No qualifying local savings, validated capacity, incident elimination or safe active-depth change was established.

| Field | Assessment |
|---|---|
| Sources | https://www.erlang.org/doc/system/sup_princ.html ; https://arxiv.org/html/2503.13657v3 ; https://microsoft.github.io/autogen/0.2/docs/tutorial/conversation-patterns/ ; https://www.anthropic.com/engineering/multi-agent-research-system |
| Relevance | HIGH. |
| Reliability | HIGH mechanisms/failure categories; MEDIUM project transfer; local outcomes **[UNVERIFIED]**. |
| Relationship | **Extends** aggregate, monitoring, recovery, handoff and value gates, not readiness. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

### 5.3 Capability-narrowing grants

The G01-G10 labels in this subsection identify external findings, not the similarly numbered compiled GQ gap families.

#### G01 - Macaroons narrow through MAC-authenticated caveats

**Finding - external context:** Macaroons use chained MACs, including HMAC, not ordinary public-key signatures. Holders add restrictions without issuer reminting. The inspected JavaScript verifier needs root key and meaningful caveat checks; callbacks must reject unsatisfied/unrecognized conditions. Copying session/resource facts from untrusted text does not authenticate them. The full original PDF was not readable; evidence is primary abstract, indexed passages and readable implementations.

| Field | Assessment |
|---|---|
| Sources | https://research.google/pubs/macaroons-cookies-with-contextual-caveats-for-decentralized-authorization-in-the-cloud/ ; https://theory.stanford.edu/~ataly/Papers/macaroons.pdf ; https://github.com/go-macaroon/js-macaroon ; https://github.com/ecordell/pymacaroons |
| Relevance | HIGH. |
| Reliability | HIGH abstract; MEDIUM indexed extraction; MEDIUM-HIGH implementation corroboration. |
| Relationship | **Supports** attenuation feasibility and **extends** quoted-grant comparison, not existing verifier or trustless system. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### G02 - Checking proofs differs from acquiring them

**Finding - external context:** Macaroon third-party caveats use discharge credentials, binding to primary credentials and recursive collection in the reviewed implementation. Supplied proofs can be checked locally using required keys/predicate inputs; obtaining fresh third-party evidence may still require contact.

| Field | Assessment |
|---|---|
| Sources | https://theory.stanford.edu/~ataly/Papers/macaroons.pdf ; https://github.com/go-macaroon/js-macaroon |
| Relevance | HIGH. |
| Reliability | MEDIUM paper extraction; MEDIUM-HIGH readable implementation. |
| Relationship | **Extends** offline-chain sketch without resolving trusted session binding/interception. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### G03 - Expiry is not immediate revocation

**Finding - external context:** Extracted revocation discussion includes expiry, state checks, lists, epochs and short discharges. A disconnected verifier cannot learn newly published withdrawal without fresh state. Bounded validity is not immediate withdrawal of a still-valid credential.

| Field | Assessment |
|---|---|
| Source | https://theory.stanford.edu/~ataly/Papers/macaroons.pdf |
| Relevance | HIGH. |
| Reliability | MEDIUM bounded indexed extraction; disconnected-verifier implication explicitly inferential. |
| Relationship | **Extends** freshness/outage questions. Written Task-completion termination is not distributed revocation infrastructure. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### G04 - Biscuit separates verification, attenuation and authorization

**Finding - external context:** Biscuit chains verify against expected root public key. Holders append restrictions without root private key; earlier blocks cannot simply be removed while retaining verification. Provenance/default trust scopes stop ordinary later facts becoming issuer grants. Signature verification is separate from authorizing trusted request facts, policy and current time. A narrower derivative does not erase broader original credentials.

| Field | Assessment |
|---|---|
| Sources | https://doc.biscuitsec.org/reference/specifications.html ; https://doc.biscuitsec.org/reference/datalog.html ; https://python.biscuitsec.org/basic-use |
| Relevance | HIGH. |
| Reliability | HIGH official specification/authorization model; retained-authority implication explicitly researcher inference. |
| Relationship | **Supports** holder attenuation and **extends** independent-verifier comparison. Public verification is conditional fit, not automatic authorization or compromise containment. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### G05 - Third-party Biscuit blocks are not macaroon discharges

**Finding - external context:** External signer blocks bind signing context and require appropriate signer trust. Application policy must require intended attestation; format/signature compatibility matters. This differs from acquiring/binding discharge credentials.

| Field | Assessment |
|---|---|
| Sources | https://doc.biscuitsec.org/reference/specifications.html ; https://github.com/go-macaroon/js-macaroon |
| Relevance | HIGH. |
| Reliability | HIGH specification and documented comparison. |
| Relationship | **Extends** evaluation beyond a binary third-party-support checkbox. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### G06 - Revoked ancestry still needs distribution and freshness

**Finding - external context:** Per-block revocation identifiers permit rejecting descendants of a revoked ancestor; branch revocation needs the right identifier. Publication, storage, distribution and refresh remain deployment duties. Local snapshots do not reveal later revocation immediately.

| Field | Assessment |
|---|---|
| Sources | https://www.biscuitsec.org/docs/guides/revocation/ ; https://doc.biscuitsec.org/reference/specifications.html |
| Relevance | HIGH. |
| Reliability | HIGH official guide/specification. |
| Relationship | **Supports** subtree-revocation feasibility and **extends** freshness, outage and branch-selection questions. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### G07 - Signed nonce and session claim are insufficient

**Finding - external context:** RFC 9449 distinguishes proof IDs, bounded acceptance windows and duplicate tracking. As security precedent, not an OAuth implementation proposal, it supports race-safe trusted one-use state across receivers/retries. A bearer session claim does not authenticate the presenter as that session.

| Field | Assessment |
|---|---|
| Sources | https://www.rfc-editor.org/rfc/rfc9449.html ; https://python.biscuitsec.org/basic-use ; https://doc.biscuitsec.org/reference/specifications.html |
| Relevance | HIGH. |
| Reliability | HIGH standard/token model; project application inferential. |
| Relationship | **Extends** replay/concurrency/presentation conditions. Nonce field alone does not satisfy them. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### G08 - CaMeL addresses influence, not delegation-token selection

**Finding - external context:** CaMeL separates trusted planning from untrusted tool-returned data. A separate data-processing model lacks tools; restricted interpreter tracks provenance/readers and checks policy before tool calls, with stricter control dependencies in stricter mode. It is not a signed offline holder-attenuated token protocol. Rounded abstract 77% versus 84% concerns task completion/utility, with benign undefended comparison, not a 77% attack-blocking rate or same-attack completion comparison. Rounded figures must not be mixed with finer-precision utility/attack results. Guarantees depend on threat model/policy; implementation is not formally verified, officially supported or promised maintenance.

| Field | Assessment |
|---|---|
| Sources | https://arxiv.org/html/2503.18813v2 ; https://arxiv.org/abs/2503.18813v2 ; https://github.com/google-research/camel-prompt-injection |
| Relevance | HIGH architectural separation; LOW token substitute; MEDIUM numbers. |
| Reliability | HIGH primary paper/results/disclaimer; no local assurance. Precision/comparator qualification retained from `qa/phase4-boundary-numbers.md`, **numbers4-05**. |
| Relationship | **Supports** data/authority separation and **contradicts** token-only injection protection; does not select library. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### G09 - Available libraries are not a maintained, already-used winner

**Finding - external context:** Observed Biscuit Python 0.4.0 release was September 26, 2025; implementation matrix marks Python third-party support partial despite examples. Node/WASM exists, but README version is not latest-release proof. Reviewed pymacaroons 0.13.0 dates to February 21, 2018; age alone proves neither abandonment nor current security support. JavaScript APIs exist without established recent maintenance assurance. Bounded manifest/lock/source search did not establish either family already used locally; it was not a universal dependency audit.

| Field | Assessment |
|---|---|
| Sources | https://pypi.org/project/biscuit-python/ ; https://github.com/eclipse-biscuit/biscuit-python ; https://github.com/eclipse-biscuit/biscuit ; https://github.com/eclipse-biscuit/biscuit-wasm ; https://doc.biscuitsec.org/usage/nodejs.html ; https://pypi.org/project/pymacaroons/0.13.0/ ; https://github.com/ecordell/pymacaroons ; https://github.com/go-macaroon/js-macaroon |
| Relevance | HIGH Python; MEDIUM Node alternatives. |
| Reliability | HIGH observed metadata/docs; maintenance, compatibility and full feature support **[UNVERIFIED]**. |
| Relationship | **Extends** feasibility. Biscuit is a researcher comparison preference, not adoption or adversarial winner. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### G10 - Credential feasibility is not grant or hook readiness

**Finding - attributed researcher comparison:** Authenticity/attenuation, trusted-fact authorization, complete pre-effect enforcement and credential lifecycle are four different questions. Local comparison found narrow human-origin Task-specific commit grants, not transferable authority. Hooks have different inputs/recognition ceilings; launch guard is not command-text-only, but neither reviewed guard implements the proposed parent/resource/action verifier. Historical Dispatch forwarding exists; suitability/attenuation remains unestablished. Authenticating close requests does not prove safe state or authorize destruction.

| Field | Assessment |
|---|---|
| Sources | https://python.biscuitsec.org/basic-use ; https://arxiv.org/html/2503.18813v2 ; https://github.com/IronbellyOrg/IronClaude/issues/339 ; file:///home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/src/superclaude/core/WORKER-CONTRACT.md ; file:///home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/src/superclaude/hooks/scripts/launch-level-guard.sh ; file:///home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/src/superclaude/hooks/scripts/require-orca-worktree-agent.sh ; file:///opt/Orca/resources/app.asar.unpacked/out/cli/handlers/orchestration/message-send-handler.js |
| Relevance | HIGH. |
| Reliability | HIGH recorded source comparisons/authorization model; universal/live enforcement **[UNVERIFIED]**. Installed comparisons retain historical snapshot scope under `CORRECTION`. |
| Relationship | **Supports** human-origin/destructive safeguards and **contradicts** token feasibility as permission for hierarchy. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

### 5.4 Orca public documentation on depth and helpers

O01-O09 identify external findings; O1-O6 identify decision options. All originally inspected installed mechanics below retain historical-build scope unless the dated correction expressly refreshes them.

#### O01 - Metadata-led discovery identifies the relevant Orca project

**Finding - external context and historical metadata:** Research followed installed root-archive homepage to `stablyai/orca`, not a guessed repository. Original compiled-output version was `1.4.245-aidev02.780594c521aa`, without homepage/repository/docs fields there. The dated correction records replacement compiled version `1.4.245-aidev02.9cfecdd30b2a`; that is on-disk metadata, not running-process proof. Public landing/docs were accessible; discovered source path returned 404, which proves neither privacy nor implementation absence. No authenticated access was attempted.

| Field | Assessment |
|---|---|
| Sources | https://github.com/stablyai/orca ; https://www.onorca.dev/docs/cli/orchestration ; https://github.com/stablyai/orca/blob/main/src/main/runtime/orchestration/preamble.ts ; file:///opt/Orca/resources/app.asar.unpacked/out/package.json ; `CORRECTION:18-34`. |
| Relevance | HIGH. |
| Reliability | HIGH metadata identity/observed pages; inaccessible implementation **[UNVERIFIED]**. |
| Relationship | **Supports** version-aware discovery, not whole-source access, running-build identity or equivalence. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### O02 - One is not a permanent product mandate

**Finding - external context:** Original depth PR links restriction to worker Run attachment; later maintainer PR calls one accidental carryover, raises public default to four and retains finite recursion ceiling. Why exactly four was not established. Historical local source default/fallback was one, root zero. The dated replacement source instead defines default/fallback two, root zero and guarded legacy-one migration. Project policy remains one. These are separate source/version/policy observations, not contradictory readings of one effective runtime.

| Field | Assessment |
|---|---|
| Sources | https://github.com/stablyai/orca/pull/16668 ; https://github.com/stablyai/orca/pull/38348 ; file:///opt/Orca/resources/app.asar.unpacked/out/shared/nested-worker-depth.js ; `CORRECTION:18-34`. |
| Relevance | HIGH. |
| Reliability | HIGH rationale/history/source contents; MEDIUM author-reported execution. |
| Relationship | **Extends** mechanics and **contradicts** permanent flat-only product endorsement, not current IronClaude policy. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### O03 - Migration is a version-specific risk, not an effective-value observation

**Finding - external context and dated correction:** Public v1.4.251 reports default four and one-time migration of unmarked stored ones, including intentional earlier ones indistinguishable from legacy default. Values above one and later explicit one are described as retained. Unversioned docs/retrieved v1.4.255 release listing are not the researched installation. Historical stored one did not prove effective loading and is not a current profile observation. Separately, new local source resolves valid safe integers ≥1, defaults invalid input to two, and migrates resolved one only when its migration marker is not true; marked one and valid higher values remain. Definition does not prove invocation/persistence.

| Field | Assessment |
|---|---|
| Sources | https://github.com/stablyai/orca/releases/tag/v1.4.251 ; https://github.com/stablyai/orca/pull/38348 ; https://www.onorca.dev/docs/cli/orchestration ; https://github.com/stablyai/orca/releases ; `DEPTH:26-42`; `CORRECTION:18-34,51`. |
| Relevance | HIGH. |
| Reliability | HIGH release/migration wording and bounded source contents; MEDIUM unexecuted operational behavior. |
| Relationship | **Extends** migration risk and **contradicts** treating public four, or local source two, as current loaded value. Current stored/effective value, execution/persistence, propagation and reversal remain **[UNVERIFIED]**. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### O04 - Historical native helpers have a parent-worker route

**Finding - external context and historical source:** Public material describes eligible helper instructions. R03's original installed `SUB-DISPATCH` recipe uses the parent Dispatch's Run and `worker-start --from`; questions/escalations/completions reach parent check alongside coordinator mail, with helper completion before parent completion. Own-Run variant is distinct. Recipient selection uses active same-Run creator else Run; inspected remote/terminal variants are rejected on local route. This is historical source support, not live execution or replacement-build equivalence. The old bundle is now absent; its offsets cannot be relabeled with a replacement filename.

| Field | Assessment |
|---|---|
| Sources | https://github.com/stablyai/orca/pull/38348 ; https://github.com/stablyai/orca/blob/main/skill-guides/orchestration.md ; file:///opt/Orca/resources/app.asar.unpacked/out/main/chunks/orcad-migration-source-retention-B_-OYaBD.js ; `CORRECTION:36-47`. |
| Relevance | HIGH. |
| Reliability | HIGH historical source/guide; MEDIUM public author execution reports. |
| Relationship | **Supports** native-helper candidacy and **contradicts** universal root-only routing for researched route; not permission, live correctness or exact-target certification. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### O05 - “Nested coordinator” wording is not a complete role contract

**Finding - external context:** Public docs mention child-Run mailboxes for nested coordinators; issue discusses phase-local coordinators. Bounded inspection found no separate complete authority/report/recovery contract. Historical installed table named coordinator, dispatched worker, handoff owner, compatibility operator and ordinary terminal agent; guide surfaces differed. Negative search does not prove universal absence, and historical table is not current replacement-build certification.

| Field | Assessment |
|---|---|
| Sources | https://github.com/stablyai/orca/blob/main/docs/site/content/docs/cli/orchestration.mdx ; https://github.com/stablyai/orca/issues/24970 ; file:///opt/Orca/resources/app.asar.unpacked/out/cli/bundled-skill-guides.js ; file:///opt/Orca/resources/app.asar.unpacked/out/cli/specs/orchestration.js |
| Relevance | HIGH. |
| Reliability | HIGH wording/historical table; MEDIUM requests. |
| Relationship | **Extends** role discussion, not transitive grant; handoff owner and supervised coordinator differ. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### O06 - Public requests are plausible value, not local measurement

**Finding - external context:** Requests seek phase-local reviewers/helpers and remote lead delegation without root-mediated launches. These are plausible avoided-round-trip cases, not measured local latency/token/correctness improvements or qualifying runtime-only split records.

| Field | Assessment |
|---|---|
| Sources | https://github.com/stablyai/orca/issues/24970 ; https://github.com/stablyai/orca/issues/30141 |
| Relevance | HIGH. |
| Reliability | MEDIUM first-hand requests, not controlled measurement. |
| Relationship | **Supports** plausible value and **extends** examples; D5 need remains open. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### O07 - Each host's limit remains separate

**Finding - external context:** Remote issue reports desktop raise did not change remote default one. PR says hosts enforce own limits and older hosts retain old behavior until updated. Closure does not prove owner-only setter/per-Run override. Current remote effective settings, propagation and recovery remain unverified; the bounded local source-two observation supplies no remote inheritance.

| Field | Assessment |
|---|---|
| Sources | https://github.com/stablyai/orca/issues/30141 ; https://github.com/stablyai/orca/pull/38348 |
| Relevance | HIGH. |
| Reliability | MEDIUM reported behavior; HIGH PR-stated boundary. |
| Relationship | **Supports** separate federation uncertainty, not generalized local conclusions. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### O08 - Public helper stopping is qualified

**Finding - external context:** Newer release says helpers stop with worker; PR follows creator-Dispatch descendants. Preserved helpers/descendants may remain; unconfirmed stopping is uncertain; remote stopping requires contact; interrupted initialization may need retry; terminal closure does not universally kill detached processes. Neither original nor replacement local build receives these guarantees by assumption.

| Field | Assessment |
|---|---|
| Sources | https://github.com/stablyai/orca/releases/tag/v1.4.251 ; https://github.com/stablyai/orca/pull/38373 |
| Relevance | HIGH. |
| Reliability | HIGH release wording; MEDIUM detailed author behavior reports. |
| Relationship | **Extends** cancel/orphan risks, not subtree-quiescence guarantee. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

#### O09 - Capability does not amend the local decision

**Finding - attributed researcher policy comparison:** WC-13 prohibits fan-out at any native setting; person-opened eligibility and preserved worker restrictions remain. D5 requires autonomous composite brief plus real material runtime-only split, with AC-0.7 trace before raise. Historical trace acceptance is retained, but exact-target conditions remain separate. Public requests, role labels, source default two and public four supply no exception, human consent or authorization to evaluate.

| Field | Assessment |
|---|---|
| Sources | https://github.com/stablyai/orca/pull/38348 ; https://github.com/stablyai/orca/issues/24970 ; file:///home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/src/superclaude/core/WORKER-CONTRACT.md ; file:///home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/src/superclaude/core/CLAUDE.md ; file:///home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md ; `CORRECTION:47-51`. |
| Relevance | HIGH. |
| Reliability | HIGH inspected instruction/decision; compliance and qualifying need **[UNVERIFIED]**. AC-0.7 identification retained from Phase-4 qualification. |
| Relationship | **Supports** capability/authority/ownership separation and **contradicts** present-permission inference. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

### 5.5 External research summary

Bounded delegation is technically credible. The research does not establish net benefit from another supervisory generation, complete authority or reliable exact-target operation. Flat supervision and permitted self-contained helpers remain distinct from a gated middle-role choice. This is decision context, not implementation authorization.

**Sources:** https://www.anthropic.com/engineering/multi-agent-research-system ; https://www.anthropic.com/engineering/building-effective-agents ; https://github.com/stablyai/orca/pull/38348 . **Relevance:** HIGH. **Reliability:** HIGH mechanisms, MEDIUM transfer. **Relationship:** supports caution and extends evaluation.

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

| Takeaway | Findings carrying its evidence |
|---|---|
| Incoming blocking is documented; authenticated origin/deployed coverage are not established. Sender controls are known, native class protocol remains partly open. | M03-M07. |
| Mode class, inbound policy, execution permission, authority and consent differ. | M01-M04, M11. |
| Send, mailbox write, idle, apply and completion retain different guarantees. | M08-M10. |
| Subagents, teams, peers and Orca workers have different boundaries. | M12, H05, O02-O05, O09. |
| Flat specialist research is demonstrated pattern; extra depth has unmeasured local tradeoffs. | H01-H05, H10-H13. |
| Aggregate verification, child service, resources, cancellation and takeover need owners. | H06-H09, H11, H14-H15, O04, O08. |
| Attenuation is not trusted authorization, complete enforcement, replay state or fresh revocation. | G01-G07, G10. |
| Biscuit preference is conditional; CaMeL addresses influence, not token choice. | G08-G10. |
| Policy one, historical source/stored one, dated source two and public four remain separate. Public shutdown is not local quiescence. | O01-O03, O07-O09; `CORRECTION`. |
| Correct old chain/root-routing premises without changing WC-13 or certifying replacement build. | H14-H15, O04-O06, O09. |

### 5.6 Every external finding mapped to the six options

**O1:** retain two tiers/no sub mode. **O2:** person-opened independent peers. **O3:** supervised middle worker with native helpers. **O4:** launched handoff-owner subordinate. **O5:** existing internal Agent helpers. **O6:** defer with explicit gates.

Mapping is relevance, not approval.

| Finding | Options informed | Decision significance |
|---|---|---|
| M01 | O2, O3, O4, O6 | Evaluate class-derived holds without exact-name/universal-delivery assumptions. |
| M02 | O2, O3, O4, O6 | Preserve hold, expiry, queue and unattended distinctions. |
| M03 | O2, O3, O4, O6 | Keep sender internals, historical configuration and installed availability open. |
| M04 | O2, O3, O4, O6 | Separate inbound policy, tool permission and parent trust. |
| M05 | O2, O3, O4, O6 | Documented hook is not deployed security certification. |
| M06 | O2, O3, O4, O6 | Trusted origin cannot be replaced by receiving-context fields. |
| M07 | O1, O2, O3, O4, O6 | Timeout, version, ordering and approval origin are separate checks. |
| M08 | O2, O3, O4, O5, O6 | Retain actual channel guarantee and separate application/admission. |
| M09 | O2, O3, O4, O6 | Typed text/file schema does not authenticate or authorize. |
| M10 | O1, O2, O3, O4, O6 | Idle observation is not supervision/completion. |
| M11 | O1, O2, O3, O4, O5, O6 | Preserve human consent; no denied-work routing. |
| M12 | O1, O2, O3, O4, O5, O6 | Keep mechanisms' nesting/permission models distinct. |
| H01 | O1, O3, O4, O5, O6 | Flat research gains do not prove extra supervisory depth. |
| H02 | O1, O2, O3, O4, O5, O6 | Clear briefs, artifacts, stops and bounds remain needed. |
| H03 | O1, O3, O4, O5, O6 | Include batch waits and reconciliation costs. |
| H04 | O1, O3, O4, O5, O6 | Dynamic delegation needs genuinely runtime-discovered work. |
| H05 | O3, O4, O5, O6 | Separate context, depth, concurrency and lifetime. |
| H06 | O3, O4, O6 | Define failure policy, lineage resources and descendant settlement. |
| H07 | O3, O4, O5, O6 | Compare context controls without package/durability assumptions. |
| H08 | O3, O4, O5, O6 | Local conversation caps are not total subtree budget. |
| H09 | O3, O4, O6 | Manager routing does not establish concurrency/spend ceiling. |
| H10 | O1, O2, O3, O4, O5, O6 | Bound collaboration and integration/shared decisions. |
| H11 | O1, O2, O3, O4, O5, O6 | Require clarification, stops and verification at boundaries. |
| H12 | O1, O3, O4, O5, O6 | Preserve numerical baselines; no local speed/cost promise. |
| H13 | O1, O2, O3, O4, O5, O6 | Conditional trades, not universal winner. |
| H14 | O1, O3, O4, O6 | Correct premises without policy amendment or build transfer. |
| H15 | O3, O4, O6 | Define aggregate success, child service, checkpoint and takeover. |
| G01 | O2, O3, O4, O6 | Feasible attenuation under secret-verifier/predicate model. |
| G02 | O2, O3, O4, O6 | Offline checking differs from obtaining fresh proofs. |
| G03 | O2, O3, O4, O6 | Distinguish expiry and fresh revocation. |
| G04 | O2, O3, O4, O6 | Public verification/attenuation differs from authorization. |
| G05 | O2, O3, O4, O6 | Compare third-party protocols and compatible features. |
| G06 | O2, O3, O4, O6 | Ancestor revocation needs distribution/freshness. |
| G07 | O2, O3, O4, O6 | Authenticate presenter and enforce race-safe consumption. |
| G08 | O1, O2, O3, O4, O5, O6 | Data cannot become authority; tokens do not replace influence control. |
| G09 | O3, O4, O6 | No already-used, maintained or debate-winner assumption. |
| G10 | O1, O2, O3, O4, O5, O6 | Preserve human grants and complete-enforcement distinction. |
| O01 | O3, O4, O6 | Correct project/version identity and bounded access evidence. |
| O02 | O1, O3, O4, O6 | Historical default is not permanent architecture mandate. |
| O03 | O1, O3, O4, O6 | Migration/source contents are not effective-setting observations. |
| O04 | O3, O4, O6 | Credit historical native route; separate variants/exact-target claims. |
| O05 | O2, O3, O4, O6 | Terminology/mailboxes do not define authority/recovery. |
| O06 | O3, O4, O6 | Plausible demand does not satisfy local need gate. |
| O07 | O3, O4, O6 | Host depth and remote lifecycle require separate evidence. |
| O08 | O3, O4, O6 | Parent stopping is not confirmed descendant quiescence. |
| O09 | O1, O2, O3, O4, O5, O6 | Capability does not waive policy, consent or revisit conditions. |

### 5.7 Coverage, deduplication and exclusions

| Input or issue | Treatment |
|---|---|
| W01's 13 findings, summaries and recommendations | M01-M12 retain all material distinctions. SDK example combined into M06; community classification discrepancy into M01. Hook/channel/authority distinctions remain separate. |
| W02's 17 findings, comparison, numbers and five-cost reassessment | H01-H15 consolidate related OTP, LangGraph, AutoGen and Cognition observations without dropping qualifications. H12 retains all nine numerical groups; H13 all eight tradeoff dimensions; H14 all five cost corrections. |
| W03's 12 findings, feasibility/library comparison and recommendations | G01-G10 retain predicate checking, proof acquisition, trust models, authorization, lifecycle, CaMeL and selection limits. Related mechanisms are combined, not silently removed. |
| W04's nine findings and negative evidence | O01-O09 retain public terminology, historical local comparisons, migration, host boundaries, shutdown and source-access limits. |
| Repeated takeaways/recommendations | Consolidated into findings/summary rather than counted as independent empirical evidence. |
| Superseded Cognition wording | Excluded as controlling evidence. Correct detected-bug denominator and largest-enterprise population govern H12 and all dependent conclusions. |
| CaMeL precision/comparator | Rounded abstract utility retained; finer figures and attack results not mixed. Benign undefended comparator is not same-attack completion. |
| Notebook/PDF extraction | Unseen notebook internals and unread full PDF not reconstructed. Explicit access limits remain in H07/G01-G03. |
| Local baseline repetitions | M07, H14-H15, G10 and O09 are attributed researcher comparisons, not new source validation. |
| Installation-snapshot change | Historical build/default/stored/route evidence remains historical. New source default/fallback two and migration are bounded contents only. Public four remains separately attributed. No current stored/effective/running-build/live/equivalence claim or automatic filename substitution. |
| Minor citation/provenance notes | M02 names **numbers4-11**; M07 names **provenance4-N2**. Numeric qualifications retain numbers4-04/05/10. Fallback comments sit beside findings/tables rather than relying only on section-level inheritance, consistent with provenance4-N1. |
| Unsupported forecasts | No new hierarchy speedup, dollar cost, capacity, incident-elimination, deployment-security or effort estimate introduced. |

**Evidence limits:** Public features, version minima, library metadata and reported behavior remain observation-time research, not fresh verification. Live messaging, installed feature applicability, credential enforcement, nested lifecycle, effective settings and local performance remain untested here. No framework/library adoption, settings change, upgrade or evaluation is authorized.

## 6. Options Analysis
**Decision scope:** Whether to add a session that accepts an upper orchestrator's assignment, supervises external sessions of its own, and returns an aggregate result upward. This is not a decision about parallelism generally, child-worktree placement or retaining existing command-internal helpers.

**Evidence conventions:**

- **[CODE-VERIFIED - normative]** means verified instruction or approved decision, not automatic enforcement.
- **[CODE-VERIFIED - static]** means source-traced implementation, not live execution.
- **[UNVERIFIED]** identifies unresolved runtime behavior, proposed capability or missing measurement.
- Effort, risk and comparison ratings are analytical judgments for the stated option, not measured estimates or the cost of the entire proposed orchestrator.
- External context informs the comparison but grants no local permission.
- R03's installed-mechanics findings are attributed historical observations with partial original-source recovery, not a complete independently reproducible source baseline. Section 2.4 and `qa/qa-fix-log.md`, FR-01/P01-P14, delimit the recovered spans. The dated replacement-source default/fallback two and guarded migration do not establish route equivalence, effective settings or migration execution.

The research and source aliases defined in Section 2.1 apply. R01's complete clause matrices and R05's complete launcher-reuse assessments inform the analysis; their compatibility or reuse judgments are not execution results.

### 6.1 Controlling facts and corrections

| Question | Controlling evidence | Consequence |
|---|---|---|
| Is supervised worker fan-out already permitted? | **[CODE-VERIFIED - normative]** `WC:62` prohibits six routes at any depth; `WC:69` defines a person-opened coordinator. `CORE:52-59` preserves worker restrictions. R01:33-60,86-105. | O3 requires explicit policy change. O4 is not a worker-side escape route. |
| Does native upward routing exist? | **[CODE-VERIFIED - static, historical snapshot]** R03:62-81 traced creator-Dispatch questions/reports, Run fallback and selected-mail handback; `HISTORICAL-BUNDLE:640,2677-2698,1267-1275`. | Reject universal root-only or necessarily missing-transport premises. Historical support does not certify replacement-build or live behavior. |
| Does unfenced Task creation permit arbitrary worker Tasks? | **[CODE-VERIFIED - static, historical snapshot]** Task creation lacks a depth check but has independent coordinator authority. R03:133-150. | Depth and authority differ. O3 cannot assume unrestricted Task creation. Exact-target equivalence remains unverified. |
| Does D1 prohibit all additional flags? | **[CODE-VERIFIED - normative]** `WC:12-14` requires explicit unattended selection and forbids command-side Orca/environment detection. R01:62-80. | Another flag is not automatically prohibited; it also cannot silently grant authority or replace the mode selector. |
| Do chains satisfy the composite-brief trigger? | **[CODE-VERIFIED - normative]** `WC:204-216` supports prewritten chains, not autonomous child planning/dispatch. R06:75-82,114-128. | Old single-command premise is stale; autonomous composite authority remains undefined. |
| Do guards cover every executable and permit all reads? | **[CODE-VERIFIED - static]** `GUARD:450-478` recognizes literal `orca`; required `worker-list`, `worker-read` and `worktree ps` are unlisted. R04:87-107 controls older categorical wording. | Universal coverage and unchanged bound-supervision compatibility are not established. Launch, reporting and probes need separate dispositions. |
| Are person-opened peers automatically unrestricted? | **[CODE-VERIFIED - static]** Binding status determines guard enforcement, not who opened the session. R04:103-105. | O2 fits role eligibility, not necessarily every governed configuration. |
| Does ordinary launch ancestry establish supervision? | **[CODE-VERIFIED - static, historical snapshot]** Ordinary launch did not automatically create Run/Task/Dispatch; claim/watcher receipts are not aggregate completion. R03:83-100; R05:63-73. | O4 needs role and reporting contracts. Existing process chains do not supply them. |
| Is AC-0.7 missing? | Historical acceptance exists; R06:81,98-112. R03 independently traced later call classifications for its own researched build. | Preserve accepted history without treating old references as current execution or replacement-build proof. |
| Is depth simply one or four? | Project policy one; historical source/stored one; dated replacement-source default/fallback two with guarded migration; externally reported public four. `CORRECTION:18-34`. | Current stored/effective values, running build, migration execution/persistence, propagation and safe lowering remain **[UNVERIFIED]**. |
| Does the located replacement bundle inherit the old trace? | Old path is absent; replacement filename was located. Existence does not establish equivalent routing, authority, fencing, launch or shutdown. `CORRECTION:36-47`. | No automatic filename substitution or historical offsets applied to a new build. Current-target route/lifecycle gates remain unsatisfied by the old trace alone. |
| Is R07 incomplete within approved scope? | R07:13 records approved current-source/tests/distributed-copy scope. | Active inventory is usable. Older partial language does not reopen excluded archives. |
| Do external numbers prove another manager helps? | W02 provides no matched incremental middle-layer comparison. Corrected Cognition denominator/population control its original wording. | No local speedup, capacity or quality forecast selects an option. |

**Ranking-weight limit (FR-01):** Specific retained source spans support historical local routing and depth/authority findings; the complete ordinary-launch absence claim remains attributed to R03. All O3-over-O4 reuse and lifecycle comparisons below, including table cells and recommendation rationale, are therefore **provisional inferences under that historical account**, not an established technical ranking on an independently reproduced end-to-end baseline. This supports considering O3, not rejecting O4 or claiming current superiority. O6 rests independently on established current policy and unmet need, authority, admission and recovery conditions. **Evidence:** Sections 2.1/2.4; `qa/qa-fix-log.md`, FR-01.

**External version context:** Public default/migration and helper-stop changes identify version-specific questions, not local effective behavior. Sources: https://github.com/stablyai/orca/pull/38348 ; https://github.com/stablyai/orca/releases/tag/v1.4.251 ; https://github.com/stablyai/orca/pull/38373 . W04 rates primary wording HIGH reliability; unexecuted operational details remain qualified.

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

### 6.2 O1 - Keep two tiers and no subordinate mode

**Description:** Retain the person-opened coordinator over direct workers, with clarified PR #449 ownership wording so it cannot be mistaken for a worker exception.

**How it works:** The coordinator owns Task creation, dispatch, admission and further-work decisions. Workers retain command-internal helpers and report newly discovered external work upward. Worktree nesting remains placement, not another supervisory tier. **[CODE-VERIFIED - normative]** `WC:47,60-69,220-246`.

| Aspect | Assessment |
|---|---|
| Effort | **S** for wording/distribution clarification. Retaining topology adds no runtime mechanism; this is not the v1 orchestrator estimate. |
| Risk | **Low incremental.** Existing liveness and bound-probe defects remain; O1 does not solve them. |
| Reuse of existing code | Existing identity, Run/Dispatch messages, contracts, admission, retries, freezes and internal helpers. Installed source observations retain their historical scope. |
| Files/systems affected | Conditional Section 8 O1 surfaces: root/core guidance, ccsession README, source/plugin hook message, exact-message expectation and distributed copies. Role/parity test may remain unchanged if its assertions still hold. R07:67-76. |
| Value and unlocks | One supervision/admission edge with direct parallel workers, without additional delegated authority. |
| Rules to rethink | Retain WC-13/D5. Clarify ownership meaning; separately decide any Orca-calling command boundary. |
| Evidence | R01:62-80,86-127; R02:123-136; R07:67-76; `WC:5,40,60-69,239-246`. |
| Pros | Smallest external supervision model; no invented upward protocol; preserves human and Git ownership. |
| Cons | Runtime-discovered external splits still need root round trip; internal helpers lack separate Orca lifecycle records. Permanent rejection exceeds current benefit evidence. |

### 6.3 O2 - Independent person-opened peer coordinators

**Description:** Several person-opened coordinators own separate workstreams rather than supervise one another.

**How it works:** Each owns its Tasks, workers, admission and authorized outward actions. Findings may be shared as evidence, but peers do not silently claim one another's Tasks, consume mailboxes, approve halts or publish work. No automatic upper/lower completion follows. **[CODE-VERIFIED - normative]** `WC:69,200,229-246`; R01:133-146.

| Aspect | Assessment |
|---|---|
| Effort | **S** for genuinely independent peers with explicit work division. Shared registry or automated cross-peer control is additional, unestimated scope. |
| Risk | **Medium.** Overlapping ownership, writes, dependencies and intervention require boundaries. |
| Reuse of existing code | Root/worker machinery, separate Run mailboxes, durable reports and placement rules. Mechanism evidence is not universal deployment certification. |
| Files/systems affected | Conditional Section 8 O2 contract/routing/developer explanations. No inherent depth or blanket never-as-worker change. Governed launch/report/probe policy remains conditional. R07:78-88. |
| Value and unlocks | Persistent independent owners without converting workers into supervisors; compatible with #409's multiple-coordinator observation premise. |
| Rules to rethink | Preserve WC-13/D5; define peer boundaries rather than transitive control. Multiple peers do not explain PR #449's subordinate phrase. |
| Evidence | R01:84-105,133-146; R02:126; R04:103-105; R07:78-88; R08:106. |
| Pros | Fits person-opened eligibility; no extra Dispatch generation inherent; separates persistent ownership. |
| Cons | Does not fulfill supervised upper assignment/aggregate reporting. Person-opened is not unbound; communication is not admission or human approval. |

**External context:** Peer text exchange distinguishes acceptance, application and completion; it does not supply an Orca peer-control contract. W01:44-48,53; https://code.claude.com/docs/en/cross-session-messaging#message-delivery .

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

### 6.4 O3 - Supervised middle worker with native helpers

**Description:** A dispatched worker becomes a bounded supervisor while retaining its own upper-facing worker identity. This is the final scoped **session-layer** D5 alternative, not the superseded command-owned dispatch proposal.

**How it works:** The candidate would use native local helper ancestry, individual child Tasks/Dispatches and creator-directed reporting, separately reporting its own outcome upward. That mechanism was established for R03's historical build. Exact-target source/lifecycle evidence, approved composite brief, WC-13 exception and bounds remain required. Source default two supplies none of those permissions. **Evidence:** R03:62-81; R06:114-128; `CORRECTION:36-51`.

```text
Candidate relationship only
(not approved, live-verified or replacement-build-certified)

Person-opened root coordinator
               |
         middle Dispatch
           /        \
   child Dispatch  child Dispatch
```

| Aspect | Assessment |
|---|---|
| Effort | **XL** for complete authorized mode: role/brief semantics, dual monitoring, aggregate results, enforcement, recovery and deployment evidence. Native reuse reduces invention, not these obligations. |
| Risk | **High.** A stalled or compromised middle affects upper assignment and descendants. |
| Reuse of existing code | Provisional native supervised fit: historically traced same-Run ancestry, creator questions/reports, fences and selected-mail handback. Flat admission/retry are reusable constraints, not a completed recursive contract. Replacement equivalence is unverified. |
| Files/systems affected | Section 8 O3: eligibility/brief/report/retry/admission/placement; contract tests; guides/ownership; applicable governed launch/report/probes; approved decision and distribution. WC-8 may remain if calls stay session-layer. R07:90-102. |
| Value and unlocks | Potentially avoids root wake/read/Task-creation round trip for genuinely unforeseen decomposition while preserving tracked children. Saving **[UNVERIFIED]**. |
| Rules to rethink | Explicit WC-13/eligibility/D5 decision; autonomous planning, helper/question/retry limits, outcomes and root-retained outward authority. Preserve D1, D2 and D3. |
| Evidence | R01:86-148; R02:85-132; R03:43-81,133-164; R06:75-82,114-142; R07:90-102; `CORRECTION:47-51`. |
| Pros | Retained original-source routing snippets support a native supervised fit; its comparative advantage over ordinary-owner lifecycle remains provisional. |
| Cons | Currently prohibited. Composite authority, mixed-mail service, aggregate admission, blocked-parent/replacement ownership, effective settings and lowering unresolved. Historical local route was same-host/new-agent; remote is separate. Current source/lifecycle equivalence is not established. |

**External context:** Local-reviewer/helper and remote delegation requests establish plausible demand, not measured IronClaude savings or D5 satisfaction. W04:37-41; https://github.com/stablyai/orca/issues/24970 ; https://github.com/stablyai/orca/issues/30141 . Demand reliability: MEDIUM.

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

### 6.5 O4 - Ordinary launched handoff-owner subordinate

**Description:** Use ordinary agent/worktree launch for a non-dispatched owner, then explicitly define its upper-assignment/reporting relationship.

**How it works:** Historically inspected launch paths created an agent surface/receipt, not automatic Run/Task/Dispatch or worker preamble. New eligibility/authority and correlation, progress, questions, application acknowledgment, results, admission and failure contracts are central. A new transport/type is not necessarily required. **Evidence:** R03:83-116; R02:128-132; `CORRECTION:42-45`.

| Aspect | Assessment |
|---|---|
| Effort | **XL.** Existing launch mechanics do not supply the missing owner/upward lifecycle contract. |
| Risk | **High.** Treating ordinary launch as Dispatch can hide stale ownership, absent supervision or excessive authority. |
| Reuse of existing code | Launch, receipts, watcher durable intent (pending state saved before launch) and audit and artifact returns are partial components, not complete subordinate-owner protocol. Installed comparisons remain historical. |
| Files/systems affected | Section 8 O4: role eligibility/upward reporting, ownership/outward boundaries, guides, copies/tests and governed policy. New command eligibility is separate and conditional. R07:104-115. |
| Value and unlocks | Potential persistent delegated domain owner outside one-Task worker lifecycle; ordinary launch itself need not add Dispatch generation. |
| Rules to rethink | Person-opened definition, owner authority/reporting and division of duties. Worker initiation still violates WC-13. A numeric D5 raise is not the separate O4 decision. |
| Evidence | R01:53-58,129-148; R02:128-132; R03:83-116; R05:40-75; R07:104-115; R08:117-125. |
| Pros | Reuses real launch mechanisms; distinguishes persistent ownership from one-Task worker. |
| Cons | No inherited worker lifecycle, coordinator eligibility, grant rights or human authority. Handoff-owner guide is not monitored subordinate contract. Greater lifecycle invention than O3 is a provisional comparison, not an independently reproduced negative. |

“New upward channel” means a new agreed **reporting relationship**, not absent generic transport. Historically validated host/instance ancestry is more than cosmetic, but is not that relationship. **Evidence:** R03:85-100.

### 6.6 O5 - Existing in-session Agent helpers

**Description:** Keep decomposition within assigned command/session using already permitted internal helpers, not another external supervision tier.

**How it works:** Assigned command/Skill runs top-level, collects its helpers and propagates nested results under existing rules. Only enclosing worker sends Orca lifecycle/completion. Wrapping the entire assigned command in a helper is excluded. **[CODE-VERIFIED - normative]** `WC:24-25,46,60`.

| Aspect | Assessment |
|---|---|
| Effort | **XS** for supported existing patterns. No generic wrapper or changed protocol included. |
| Risk | **Medium** context/output/helper behavior; less new authority than O3/O4. |
| Reuse of existing code | Command-to-Skill activation, helper dispatch/collection and nested-result propagation; strongest direct specialist precedent. |
| Files/systems affected | No inherent policy change. Actual new wrapper would conditionally affect declarations, unattended expectations and nested checks; wording cleanup separate. Section 8 O5; R07:117-126. |
| Value and unlocks | Bounded parallel research/review with reduced parent-context clutter, without external supervisory relationship. |
| Rules to rethink | No WC-13/D5 reversal for existing helpers. Retain actual top-level Skill invocation, lifecycle ownership, nested failure propagation and human boundaries. |
| Evidence | R01:77,93-101; R02:129; R03:163; R05:44-61,71-75; R07:117-126. |
| Pros | Existing narrow mechanism; no new Orca ownership/upward protocol. Local/background Agent branch does not itself receive ESCAPE. |
| Cons | No independent child Orca lifecycle/retry records or persistent external owner. Accepted heartbeat gaps remain. Provider/adapter limits are not universally disproved. |

**External context:** Published bounded subagent nesting is not installed-harness proof or Orca fan-out authority. Fresh context has briefing/reconstruction costs, not automatic lower cost or latency. W01:48; W02 findings 5-6; https://code.claude.com/docs/en/sub-agents .

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

### 6.7 O6 - Defer with explicit reconsideration gates

**Description:** Do not add or authorize a subordinate mode on present evidence. Retain operating boundaries and make missing evidence/decisions explicit.

**How it works:** Current flat supervision and allowed internal helpers continue under their rules. Later adoption needs applicable Section 7.5 conditions; source feasibility alone is not policy approval. Deferral is neither permanent rejection nor authority to build another product scope.

| Aspect | Assessment |
|---|---|
| Effort | **S** for decision/gate record only. Later gate-satisfaction effort is not included or scheduled. |
| Risk | **Low incremental**, with opportunity cost of delaying unmeasured benefit. Existing defects remain visible. |
| Reuse of existing code | Current model/helpers; historical native findings; dated source correction; `WC:246` follow-up/time evidence channel. |
| Files/systems affected | Section 8 O6: conditional decision/gate documentation, no inherent runtime/guard relaxation. Separately adopted wording has O1 surface. R07:128-145. |
| Value and unlocks | Preserves credible O3 candidate while preventing a role label acquiring launch, approval, publication or cleanup authority. |
| Rules to rethink | No silent changes. D5 trigger, mailbox discrepancy, command packaging and future WC-13 exception remain explicit decisions. |
| Evidence | R01:113-148; R03:152-164; R06:54-82,130-142; R07:128-145; R08:127-133; GQ G02-G19/G27-G35; `CORRECTION:47-51`. |
| Pros | Fits current authority/evidence; reversible; separates historical feasibility, dated source observations and operational readiness. |
| Cons | No subordinate external supervisor delivered now. Concrete conditions needed to avoid indefinite, unfalsifiable “later.” |

### 6.8 Nine-criterion comparison

Ratings concern stated options, not the full v1 product. Existing source, instructions or historical implementation do not mean demonstrated live compliance.

| Criterion | O1 Two tiers | O2 Independent peers | O3 Supervised middle | O4 Launched owner | O5 Internal helpers | O6 Gated deferral |
|---|---|---|---|---|---|---|
| **Effort** | S | S independently; shared control extra | XL | XL | XS existing use | S record only |
| **Risk** | Low incremental; existing gaps | Medium ownership overlap | High dual-role/recovery | High authority/new lifecycle | Medium context/output | Low incremental; opportunity cost |
| **Maintainability** | Fewest supervisory edges | Existing mechanisms, more owner boundaries | Native reuse helps; recursive contract broad | New owner/reporting contract | Existing protocols; no external tier | No new runtime; maintain evidence gates |
| **Integration complexity** | Low topology change | Low independently; higher shared control | High policy/mail/admission/recovery/guards | High eligibility/reporting/monitoring/grants | Low in supported patterns | Low now |
| **Reuse potential** | High current model | High root machinery | High historically traced native ancestry/routing; target equivalence open | Partial launch/audit/result reuse | High helper patterns | High policy/evidence channels |
| **Liveness/reporting fit** | Single-edge procedure; not automatic proof | Independent loops; no upward completion | Provisional native nested fit; aggregate, blocked-parent and recovery open | No equivalent complete upward lifecycle established | Parent result; no child Orca lifecycle | Preserve baseline and expose limits |
| **Authority fit** | Current-policy fit | Fits genuinely independent peers | WC-13/eligibility conflict | New eligibility; not worker bypass | WC-7-compatible boundary | Current-policy fit without permanent prohibition |
| **Enforceability** | Partial; B1/B2 remain | Same if bound | Historical depth/identity machinery, no current scoped-role grant or replacement certification | Ordinary launch is not Dispatch authority; no current role scope | Local branch compatible; live inheritance open | No new enforcement claimed |
| **Value delivered** | Direct parallel supervision | Persistent independent owners | Conditional tracked local autonomy | Conditional persistent delegation | Local specialist decomposition | Reversible decision; no new hierarchy |

**Comparison conclusion:** O3 is the provisional technical candidate on retained historical evidence if subordinate supervision becomes justified. Native transport evidence does not make it approved or operationally ready. The historical account suggests O4 needs more lifecycle invention; O2 and O5 solve different relationships. O6 fits unresolved authority, measured need and recovery, not an obsolete claim of technical impossibility. **Evidence:** R01/R02/R03/R04/R06/R08; `CORRECTION:47-51`.

### 6.9 Worker and coordinator compatibility

The matrices preserve the complete synthesis's clause-family meanings from R01's original §§5.2-5.7.

| Mark | Meaning |
|---|---|
| **H** | Requirement can remain compatible under the stated option; not a live pass. |
| **B** | Defining behavior conflicts with current rule. |
| **U** | Cross-level behavior or ownership remains undefined. |
| **C** | Compatible only under the stated restriction. |
| **\*** | Separate B2 bound-probe defect applies. |

For O4, compatibility with worker protections does not promote an ordinary launched owner to an eligible coordinator. No matrix cell approves a policy exception, external effect or experiment.

#### Numbered worker rules

| Rule and source | O1 | O2 | O3 | O4 | O5 | O6 | Preserved meaning |
|---|---|---|---|---|---|---|---|
| WC-2: no person-blocking command step; `WC:31` | H | H | H | H | H | H | Extra levels do not justify unattended approval prompts. |
| WC-3: eligibility, once-per-Task, late answers; `WC:53-58` | H | H | U | U | H | H | Define answer owner at each edge; retain person-only exceptions. |
| WC-4: known report/every outcome; `WC:32-39` | H | H | U | U | H | H | Composite/ordinary reports need identity and outcome definitions. |
| WC-5: own completion/outcome mapping; `WC:59` | H | H | U | U | H | H | Child completion is not aggregate completion; no impersonation. |
| WC-6: new retry Task; `WC:71-79` | H | H | U | U | H | H | Allocate exclusive settlement/retry author. |
| WC-7: top-level command/Skill/lifecycle; `WC:60` | H | H | H | H | H | H | O5 cannot wrap assigned command or send lifecycle messages. |
| WC-8: no command fan-out; `WC:40` | H | H | C | C | H | H | Session-layer variant can preserve it; direct command dispatch needs separate exception. |
| WC-9: outward ban/Task grant; `WC:41-45` | H | H | H | U | H | H | O3 stays worker-bound; O4 gets no inherited outward grant. |
| WC-10: waits/helper gap; `WC:46` | H | H | U | U | H | H | Child activity cannot replace middle's own liveness. |
| WC-11: writers/placement; `WC:47` | H | H | H | H | H | H | Preserve actual isolation, not names alone. |
| WC-12: pulled follow-ups/batch/application ack/fence; `WC:61` | H | H | U | U | H | H | Mixed-mail/fencing duties need allocation. |
| WC-13: worker-session fan-out; `WC:62` | H | H | B | C | H | H | O4 only compatible when not worker-initiated/operated as workaround. |
| WC-14: continuous chains; `WC:63` | H | H | U | U | H | H | Own command end does not define subtree completion. A worker ends its turn only after `worker_done`, while blocked in the preamble's `ask`, on `consumer_fenced`, or for the S6 handoff interrupt (no `worker_done`). |
| WC-15: bounded reads/handoff; `WC:64` | H | H | U | U | H | H | Worker checkpoint is not complete supervisor state. |

#### Coordinator duties and safeguards

| Clause family and source | O1 | O2 | O3 | O4 | O5 | O6 | Preserved obligation or unresolved allocation |
|---|---|---|---|---|---|---|---|
| Person-opened coordinator; `WC:69` | H | H | B | B | H | H | Explicit new eligibility required. |
| No retry-of; immutable brief; new Task/directory/replaced ID; `WC:73,78` | H | H | U | U | H | H | Retain immutability; allocate child retry author. |
| Three unchanged failed starts; settled/verified predecessor; `WC:75-79` | H | H | U | U | H | H | Caps/settlement survive supervisor replacement. |
| Human cancellation/quiescence; late-attempt quarantine; `WC:79` | H | H | H | H | H | H | No silence/stale-attempt authority. Confirmed quiescence means no tool running, no input accepted, and two reads five minutes apart that agree. |
| Exact command/report/policy/grant/placement; `WC:85-91` | H | H | U | U | H | H | Unique outputs/no outward default retained; composite scope undefined. |
| Read report before release/reuse; `WC:93` | H | H | U | U | H | H | Define child and upper aggregate admission. |
| Timing values/override ownership; `WC:97` | H | H | U | U | H | H | Workers cannot independently extend deadlines. |
| All-type wait/FIFO replay/write-before-ack; `WC:99-104` | H | H | U | U | H | H | One owner; failed note write means no acknowledgment. |
| Unknown S11/current attempt; `WC:105-106` | H | H | H | H | H | H | No invented types or stale identity acceptance. |
| Empty-wait inventory/sweep; `WC:107,110` | H* | H* | U* | U* | H | H* | Recognized bound Orca probes retain B2 defect. |
| Per-type status/completion/question/escalation/handoff; `WC:108` | H | H | U | U | H | H | Retain sender/result scope; no synthesized completion. |
| Human decision/merge boundary; `WC:108` | H | H | H | H | H | H | Receipt is not approval. |
| Progress/silence window/deadlines/probe budget; `WC:110-114,151` | H | H | U | U | H | H | Track each edge; arrival is not progress. Section 2.3 states W, its ceiling and the per-triggered-worker probe cap. |
| S0 startup; `WC:118` | H | H | U | U | H | H | Separate startup clocks. |
| S1/S2/S11; `WC:119-120,129` | H | H | H | H | H | H | Retain evidence/no-typing-in-unknown limits. |
| S3 idle/S4 person prompt/S5 ask; `WC:121-123` | H | H | U | U | H | H | Parent block cannot suspend child service/human escalation silently. |
| S6 exhaustion/S7 unreachable/S8 exit; `WC:124-126` | H | H | U | U | H | H | Parent failure is not subtree quiescence. |
| S9 unreported/S10 settled; `WC:127-128` | H | H | U | U | H | H | Separate own report, child settlement, admitted aggregate. |
| A1-A4/settlement acknowledgments; `WC:131-143` | H | H | U | U | H | H | Separate batch receipt and applied/queued/refused on each edge. |
| No resend; idle-only typed copy; no-terminal exception; harmless duplicate; `WC:131-138` | H | H | H | H | H | H | All input vetoes remain; ack is not correctness. |
| L0-L5/cause classes/lineage caps; `WC:146-164` | H | H | U | U | H | H | One intervention owner; no nested budget reset. Section 2.3 states the incident/lineage caps, rolling restart budget, repeated-cause restriction and context-exhaustion load rule. |
| Resume location/directory/priority/fields; `WC:167-179` | H | H | U | U | H | H | Preserve outputs, completed work, uncertainty; add subtree state if adopted. The resume note sits after the guard line and before the `Command:` lines; the old report directory is read-only input to the replacement; `/sc:implement`'s own `E-RESUME-NEEDED` re-run takes priority over the replacement route; the note carries completed `Command:` lines and contracts, the last progress token and the `Start at:` line. |
| Never on silence; `WC:182-192` | H | H | H | H | H | H | No stop/retry/release/failure/person answer/Ruling/lifecycle synthesis from silence. |
| Runtime unknowns; `WC:194-200` | H | H | H | H | H | H | Do not assume wake/attention/typing/multi-consumer behavior. |
| Visible-copy guard/labels/chains/token-preserving rerun; `WC:204-216` | H | H | U | U | H | H | Preserve guard discipline; define discretionary child authority separately. Task text never begins with `/sc:`; each command is a labelled `Command:` line. |
| Placement/setup/map/report/slugs/resume child; `WC:220-223` | H | H | U | U | H | H | Authorized setup, sole writers and absolute report identity remain. Worktrees are created by Orca at its default location, never with raw Git or under the retired location; a child is dispatched only after its setup has succeeded; concurrent `/sc:implement` runs in different worktrees use distinct plan slugs. |
| Merge/discard/remove/conflict; `WC:224` | H | H | B if assumed by worker | U | H | H | Explicit authorized integration/removal owner required. A merge conflict is stopped and reported, never resolved automatically. |
| Protected removal/no duplicate managed package; `WC:225` | H | H | H | H | H | H | Roles/tokens/completion do not erase protection. |
| Named outward work/fork/posts/ordinary PR/unseen commits/PR owner; `WC:229-235` | H | H | C | U | H | H | O3 must retain root outward ownership; no inherited publication. Progress posts (issue comments, project fields) are outward actions made from contracts the coordinator has read; workers report progress only through heartbeats and `worker_done`. |
| Task grant expiry/quiescent Git/staging/hooks; `WC:233-234` | H | H | U | U | H | H | Parent grant is not child consent; frozen/running state protected. Working-tree status is compared with the settled contracts and unlisted paths are reported; commits stage explicit paths plus `.dev/tasks`, use `git commit --only`, and the coordinator stops and reports on a hook rewrite, hook failure or conflict, never bypassing hooks. |
| Outcome admission/dependents/guard-refusal retries; `WC:239-245` | H | H | U | U | H | H | Explicit partial usability; failed/blocked inputs do not start dependents. A brief-guard refusal is fixed in a changed new Task, never re-created unchanged, with at most two brief fixes for the same work; a third refusal escalates to the person. |
| Self-created Tasks/unknown Tasks/runtime-split evidence; `WC:246` | H | H | U | U | H | H | Preserve exclusive ownership and actual added-cost record. A ready Task the coordinator did not create is not started; it is reported to the person with its spec text. |
| Freeze/handback/E-RESUME exception; `WC:250-260` | H | H | U | U | H | H | No automatic Ruling; relevant writers/Git state frozen. A plan is frozen when its latest implement contract is `blocked`, or `failed` with a STOP code other than `E-RESUME-NEEDED`, or when the ledger shows an unresolved halted task. Only `E-RESUME-NEEDED` may be re-run without the person, as the same command in the same worktree and only when the ledger shows no freeze. Lifting a freeze needs the person's explicit hand-back recorded in the coordinator's run notes and the matching ledger state: "session ended" needs the halted task `complete`, a parseable ledger last line and a re-recorded drift baseline; after a stop with no halted task only the person's recorded instruction lifts it, and the person makes no further edit in that worktree until the resume Task settles. |
| Ruling/settlement/baseline/no-force/same-worktree; `WC:261-269` | H | H | H | H | H | H | Mandatory checks cannot be replaced by parent approval. The coordinator reads the ledger and worktree, never edits either, and reports any failed resume condition. Only a matching post-halt Ruling line with the required task identity and line format is eligible. A dispute, or a latest halt reason of `no-evidence`, `no-snapshot` or `head-moved`, prohibits this resume route. `HEAD` and the graded paths must be unchanged, and a missing baseline fails the resume. |
| Admitted fan-in/limits/replacements/drops/minimum; `WC:273` | H | H | U | U | H | H | Maximum ten; replacement not addition; minimum two admitted inputs. |

**Coverage qualification:** This matrix groups clause families rather than reproducing every individual predicate; the concrete deadline and intervention baseline is stated in Section 2.3. The worked example at `WC:275-281` restates represented rules and supplies no separate grant. Historical P0-only brief/report behavior remains a historical conditional, not current command behavior. No safeguard is excluded because it obstructs O3/O4. **Evidence:** R01:107-125 and complete returned matrix.

### 6.10 Disposition of all 35 issue requirements

These R01-R35 IDs identify **requirements extracted in research R08**, not the numbered research-file aliases. They are proposal dispositions, not delivered-feature or authorization claims.

Primary records: https://github.com/IronbellyOrg/IronClaude/issues/339 ; https://github.com/IronbellyOrg/IronClaude/issues/339#issuecomment-6659516712 ; https://github.com/IronbellyOrg/IronClaude/issues/339#issuecomment-6659559030 .

“Flat-applicable” does not move later security work into v1.

| ID | Requirement | Decision disposition |
|---|---|---|
| R01 | Manage 10-20 sessions. | Flat-applicable target, not validated capacity or proof another tier is needed. |
| R02 | Root routes updates/questions. | Existing worker flow relevant; persistent all-session identity/routing unestablished. |
| R03 | No manual child interaction. | Reject absolute reading: human Rulings and ordinary PR sessions remain. |
| R04 | Hour/two sweeps. | Flat-applicable; differs from more frequent current worker procedure. No all-session implementation inferred. |
| R05 | Configurable recent-window sweep, default six hours. | Separate inventory interface, not live worker sweep; implementation unverified. |
| R06 | Close finished work/recover timeout or refusal/remind human. | Retain goal; timeout/refusal alone cannot cancel, retry or release. |
| R07 | Poll through completion, cleanup and closure. | Separate end-to-end invariant; existing waits do not prove delivery. |
| R08 | Strict worktree/branch cleanup. | Retain admission/protected-state checks and named owner; independent of hierarchy. |
| R09 | Commit valuable files/push before deletion. | Preserve value; universal pushed/closure predicates need decision/evidence, not assumption from `WC:225`. |
| R10 | Disposable logs/artifacts/reports/plans. | Reject blanket exclusion. Task packages, unread reports and unfinished ledgers are protected. |
| R11 | Worktree/branch whenever possible. | Preference is not universal isolation; current placement conditional. |
| R12 | Permanent orchestrator flag/inform future sessions. | Broader unimplemented registry requirement; role labels are not trusted authority. |
| R13 | Static report replaces summary tables. | Separate presentation-policy conflict; no style exception granted. |
| R14 | Attention until satisfied. | Distinguish sent, acknowledged, applied and resolved; persistent all-session display separate. |
| R15 | Report every 3-5 minutes/#409. | Observer/display requirement, not hierarchy need or measured service guarantee. |
| R16 | Relay to management server. | Endpoint, owner and authority unspecified; not included in subordinate approval. |
| R17 | Incorporate orchestration skill. | Integration decision remains; discovery stub is not completed product. |
| R18 | Orchestrator of orchestrators. | Direct hierarchy requirement; O6 defers it. O2/O5 do not silently satisfy it. |
| R19 | Hierarchical safeguards without repeated confirmation. | Only explicitly authorized scope; human-only consent cannot become transitive for convenience. |
| R20 | Same permission class/isolated workspace. | Classes, not exact mode names; no all-bypass remedy or permission change here. |
| R21 | Untrusted text stays data. | Security condition retained; prompt wording/detail field is not enforcement. |
| R22 | Six fixed application types. | Distinguish from nine historical Orca-supported types; explicit mapping, no invented settlement. |
| R23 | Validate identifiers/worktree/branch/inert detail. | Trusted request binding and safe processing, not schema alone. |
| R24 | Receiving hook or script-validated files. | Main-conversation hook documented yes; deployed coverage/origin/fail-closed conditions remain. |
| R25 | Signed expiring per-child grants. | Mechanisms feasible; no local adoption, complete enforcement or transferred human permission established. |
| R26 | Session binding/nonce/offline checks. | Separate integrity, trusted context, consumption and revocation freshness. Nonce is not one-use state. |
| R27 | Middle may only narrow grants. | Hierarchy-specific condition; authority not automatically transferable; retained broader originals remain risk. |
| R28 | Destructive caveats/clean-merged-closed checks. | Authenticated request is not execution approval or safe-state proof. Human/freeze/removal rules remain. |
| R29 | Preserve dangerous-removal safeguard. | Retain requirement; effectiveness untested. Cryptography does not prevent poisoned instructions. |
| R30 | Sender identifies bypass class. | Mode controls documented; native class representation/verification partly unresolved. |
| R31 | Incoming hook inspects/refuses. | Documented yes, not universal absence. Deployment/authenticated metadata unverified. |
| R32 | Research transport before security layer. | Research narrows questions; does not certify deployed readiness. |
| R33 | Maintained Python/Node library and adversarial comparison. | No already-used, supported winner or completed selection. Biscuit remains candidate. |
| R34 | Typed validation/scoped grants prerequisite to hierarchy. | Approval conditions retained, not build sequence. |
| R35 | Deep brainstorm suggestion/estimate. | Planning suggestion, not acceptance or execution authority. Quoted estimate is not schedule. |

**Evidence:** R08:19-85,89-133; W01:37-49; W03:36-58. External context: https://code.claude.com/docs/en/cross-session-messaging#control-inbound-messages ; https://code.claude.com/docs/en/hooks#userpromptsubmit ; https://python.biscuitsec.org/basic-use ; https://www.rfc-editor.org/rfc/rfc9449.html .

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

### 6.11 Evidence and scope limits of the comparison

| Source | Distinct contribution retained | Limit |
|---|---|---|
| R01 complete matrix | Worker rules, all coordinator duty families, grants/freezes/admission/human authority. | Repeated quotations/example consolidated; no compatibility mark is a live pass. |
| R02 complete tables | All states, acknowledgment layers, ladder, dual service, checkpoint and parent failure. | #434 is procedural response, not automatic compliance or incident elimination. C9 deleted; C10-C14 not assumed delivered. |
| R03 complete mechanics | Historical native routing, route-specific depth/authority, parentage and ordinary launch distinctions. | No live/federation/effective/lowering guarantee or replacement-build transfer. |
| R04 corrections | Trusted-role gap, literal recognition, missing probes, event/order limits. | No universal guard claim, alternate-spelling success or automatic expansion; U7/U28 separate. |
| R05 complete 56-cell reuse matrix | Narrow launch, result, scheduling, handoff and text-reduction patterns. | No complete O3/O4 precedent; bypass subprocess is not safety model. |
| R06 | Applied decisions, actual trigger, historical trace, final scoped D5 alternative, human/Git constraints. | P1 original FAIL not final; P2 static acceptance not live. Historically answered source questions stay answered for their snapshot. |
| R07 and supplements | Per-option files/tests/copies, exact-message versus role/parity pins, distribution. | Approved inventory complete; 867 unread archival lines/274 paths excluded, not fresh runtime evidence. |
| R08 all 35 requirements | Flat/knowledge/hierarchy separation, conflicts and independent issue boundaries. | No dashboard, server, capacity, lock or Git work bundled into this decision. |
| W01 | Mode classes, inbound hook, channel guarantees, origin/fail-closed and consent. | Documentation is not deployed interception or authenticated metadata. |
| W02 | Conditional cost/context/latency/failure/budget trades and simpler alternatives. | No matched hierarchy benefit or numeric option scoring; corrected Cognition population/denominator governs; notebook internals not inferred. |
| W03 | Feasible attenuation, trust/authorization/enforcement/replay/revocation and CaMeL distinction. | No dependency adoption, maintenance guarantee, adversarial winner or token-based human approval; PDF limit retained. |
| W04 | Public demand/terminology, migration, host/version and shutdown qualifications. | Public four not local effective value; inaccessible source not absence/privacy proof; public stop not local quiescence. |
| Dated snapshot correction | Policy one; historical one; source two; public four; absent old bundle and exact-target limits. | No current stored/effective/running-build/migration-execution/equivalence claim. No automatic filename substitution or operational authorization. |

The supported comparative judgment is O6, with O3 retained as the provisional candidate for a later bounded decision, not an approved route now. Detailed rationale and testable approval conditions follow in Section 7. No implementation, launch, upgrade, permission change or evaluation is authorized by this comparison.

## 7. Recommendation
**Recommended approach: O6 - defer a new subordinate-coordinator mode with explicit reconsideration gates.**

Retain the current operating contract. This is not permanent selection of O1 against all future hierarchy. O3 remains the provisional technical candidate on retained historical evidence because the historical research established real native ancestry and creator-directed reporting. The dated replacement-source default/fallback two changes capability evidence, not authority, demonstrated need or lifecycle readiness. Exact-target routing and operation are not certified by the historical trace. **Evidence:** R03:62-81; R06:54-82,114-142; `CORRECTION:47-51`.

### Rationale

The Section 6 comparison favors O6 on **current authority fit, incremental risk and integration burden**. The retained historical account suggests stronger native supervised reuse for O3 than O4, but neither has the required policy and operational conditions established. No external benchmark isolates this project's incremental benefit from another supervisory generation.

| Alternative | Why it is not the recommended answer |
|---|---|
| **O1 - Permanent two-tier selection** | Appropriate operating baseline, but permanent rejection is stronger than current evidence. Historical native routing and public demand make bounded reconsideration credible. |
| **O2 - Independent peers** | Useful persistent owners, but not the requested upper-assignment/aggregate-reporting relationship. |
| **O3 - Native supervised middle** | Provisional future technical candidate; currently conflicts with WC-13/eligibility and lacks approved autonomous brief, qualifying need, recursive admission and verified recovery. Exact-target source/lifecycle evidence remains necessary. |
| **O4 - Ordinary launched owner** | Requires a different eligibility/authority/upward contract with less ready-made lifecycle reuse. Avoiding a depth check is not authorized delegation. |
| **O5 - Internal helpers** | Existing useful decomposition, but not independent Orca child lifecycle, retry records or persistent external ownership. |

This recommendation does not rely on obsolete premises that all helper reports reach root, briefs contain one command, D1 bans every additional flag, or every executable spelling is mechanically blocked. It rests on the remaining authority, value, aggregate-result, failure-ownership and enforcement gaps. **Evidence:** R01 full compatibility matrix; R02:85-132; R03 historical mechanics; R04:87-107; R06 trigger analysis; R08 requirements; `CORRECTION`.

### 7.1 Value

| Value question | Evidence-based answer |
|---|---|
| What unique benefit could justify O3? | A coherent split discovered during execution, independently tracked as child work, may avoid root wake/read/Task-creation round trip. This is a conditional opportunity, not measured saving. R06:116-126; R03:62-81. |
| What is already available without it? | Direct parallel workers, flat fan-in, internal specialists and independently owned person-opened workstreams. R01:86-125; R05:40-75. |
| Is incremental saving demonstrated? | **[UNVERIFIED]** No qualifying combined runtime-only-discovery/material-cost record was found in the bounded search. Not a global absence claim. R06:79-96. |
| What does deferral deliver? | Avoids authority by ambiguous wording, preserves credible native candidacy and makes reconsideration falsifiable rather than an indefinite “later.” |
| What is not value evidence? | Duration, heartbeat gaps, follow-up work alone, worker count, public support and single-agent-versus-multi-agent vendor metrics do not isolate another manager's contribution. R06; W02/W04. |

**External context:** Task-shape guidance supports dynamic decomposition when work cannot reasonably be specified before dispatch, not merely because the task is large. Source: https://www.anthropic.com/engineering/building-effective-agents . Reliability HIGH as guidance; local transfer is inference, not benchmark.

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

### 7.2 Implications

| Area | Decision implication |
|---|---|
| Role and authority | Explicitly define allowed decisions, parent, children and resources. Worktree ownership, Dispatch identity and supervision authority differ. |
| Upward reporting | Credit the historical creator route; define application handling and aggregate admission. Do not presume a missing transport or replacement-build equivalence. |
| Liveness | The middle owes progress upward and service downward. Child heartbeats, mail or monitoring activity cannot substitute for its own semantic progress. |
| Blocking and failure | Upstream ask, human prompt, fence, exhaustion or exit must leave children with a known owner. Selected-mail handback is not full takeover. |
| Evidence and completion | Send, receipt, application, command result, settlement, admitted aggregate and safe cleanup remain different. No ancestor synthesizes worker completion. |
| Retry and resources | Count helpers, attempts, questions, probes and recovery across lineage. Replacement cannot reset budgets or redo completed work. |
| Human authority | Parent text, credentials and accepted messages are not human Rulings, fresh Task grants, publication approval or settings consent. |
| Governed sessions | Literal recognition, launch/report policy and required probes need separate treatment. B1 is a ceiling, B2 a compatibility defect; neither authorizes bypass or mandates expansion. |
| Version and settings | Separate policy one, historical source/stored one, dated source default/fallback two and guarded migration, public four, and effective runtime facts. Source migration is not invocation or persistence. |
| Distribution | Source, development copies, plugin mirrors, installed core and package assets have separate update paths. Sync/build does not prove universal freshness. |

**Evidence:** R01/R02/R03/R04/R06/R07/R08 as cited in Section 6; R07:141-145; `CORRECTION:18-51`.

**External context:** OTP illustrates compounded retry limits and parent-stop/subtree-stop distinction, not an observed local OTP defect: https://www.erlang.org/doc/system/sup_princ.html . Peer-message authority limits: https://code.claude.com/docs/en/cross-session-messaging#how-a-session-treats-an-incoming-message .

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

### 7.3 Conditional unlocks

| Conditional unlock | Required boundary | Not unlocked |
|---|---|---|
| Phase/domain-local helper selection | Local informational advantage, approved autonomous scope, bounded native route supported for exact target. | Unrestricted recursion or authority from role name. |
| Independently checkable child work | Correct ancestry, actual artifact reading, child admission and aggregate evidence. | One middle-session success standing for every child's success. |
| Less root reconstruction | Direct evidence links and summaries preserving decisions, constraints, alternatives and unresolved failures. | Hidden child failures, stale assumptions or lost uncertainty. |
| Persistent delegated ownership through O4 | Separately approved owner role and upward contract. | Promotion of every launched nonworker. |
| Existing specialist parallelism through O5 | Top-level assigned command/Skill and existing helper boundaries. | Independent Orca child records, transferable grants or human approval. |

**Evidence:** R01/R02/R03/R05/R06; Section 6 assessments.

**External context:** Composition and context controls in LangGraph, AutoGen and CrewAI demonstrate patterns, not universal superiority or adopted frameworks. Sources: https://www.langchain.com/blog/langgraph-multi-agent-workflows ; https://microsoft.github.io/autogen/0.2/docs/tutorial/conversation-patterns/ ; https://docs.crewai.com/en/learn/hierarchical-process . Context isolation can save clutter while adding reconstruction and omission risk.

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

### 7.4 Rethinks

| Rule, decision or proposal | Treatment under deferral |
|---|---|
| **WC-13** | Retain prohibition. Any future O3 exception must name eligible session, helper route, scope, counts, budgets and retained bans. Native depth allowance is not policy permission. |
| **WC-8 and command/session boundary** | Keep ordinary commands Orca-free. Session-layer helper authority does not require command dispatch. Any Orca-calling orchestrator entry point needs bounded architectural disposition, including root-only versions. Claim code is narrow precedent. |
| **D1** | Preserve explicit unattended selection and no command-side environment/preamble detection. Other flags are not categorically banned. Role interface is a separate decision. |
| **D5 outcome/trigger** | Current policy remains. Approved autonomous brief and qualifying material runtime-only split are not established. Preserve accepted historical AC-0.7 and R03's historical source answers without treating them as replacement-build acceptance. |
| **D5 mailbox record** | `SPEC:405` omits `D5-REC:49` mailbox clause. Do not infer waiver. Historical route answer, exact-target/live lifecycle and record intent remain distinct. |
| **PR #449 ownership phrase** | Disposition: gap A01 stays open as an Important defect (INF-027). The contract owner decides whether to narrow the phrase now as a separate wording change or leave it with the conflict recorded; the two choices, their consequences, the decider and the evidence step are in the Recommended next action block at the end of Section 7.6. Explicit WC-13 deferral did not implement a subordinate or approve a grant. |
| **#339 v1** | Flat supervision, attention, reporting and safe cleanup do not require hierarchy. No implementation authorization follows. Dispose of absolute automation, disposal and placement conflicts explicitly. |
| **#423 knowledge “v2”** | Catalogue, research sharing, overlap detection and course correction do not supply supervision/grants/lifecycle. Administrative numbering remains open. |
| **Never-as-worker eligibility** | Retain agent, git, help, issue, pm, spawn and swarm-wizard exclusions, plus D3's pr-submit exclusion. New coordinator-only entry point needs consistent eligibility treatment; O3 is not permission to dispatch these commands. |
| **D2/D3/D4 and Git ownership** | Preserve actual human Rulings, ordinary PR sessions, exact Task-specific conditional commits and authorized outward/integration/removal owner. No transitive approval. |
| **#431/#434 liveness** | Credit shipped procedures, not automatic enforcement or incident elimination. C10-C14 are not assumed delivered. |
| **#409/#446/#326** | Observer is not controller; lock waiting is not new Git authority; remaining Git/submodule/commit work is not bundled into hierarchy. |

**Evidence:** R01:62-80,129-156; R02:100-136; R06:54-82,130-142; R07:90-145; R08:72-133; `CORRECTION:47-51`. Existing authority remains binding until an explicit authorized decision changes it.

### 7.5 Twenty-five testable approval conditions

These are **approval conditions**, not phases, ordered implementation steps, a schedule or permission to experiment. Normative conditions need explicit authorized decisions; operational claims need appropriate evidence from separately authorized evaluation.

**Present disposition:** The complete applicable set is not passed. Historical native feasibility is established; replacement-source depth contents are bounded observations; current stored/effective settings, migration execution and exact-target lifecycle remain unverified. Applicability exclusions must identify omitted capability and cannot certify it.

| Gate ID | What must be true before a subordinate mode is built | Pass/fail test | Evidence satisfying the condition | Options blocked |
|---|---|---|---|---|
| **DG-01** | Need beyond planned flat fan-out/internal helpers. | **PASS only** with original Task, discovered split, why not reasonably knowable before dispatch, follow-up Task and measured extra coordination time accepted as material. Missing any element fails. | Timestamped run notes and Task/report references. Not established. R06:79-96; `WC:246`. | O3; O4 when using same latency rationale. |
| **DG-02** | Approved autonomous composite brief. | **PASS only** with discretionary planning scope, allowed children/actions, outputs, stops and bounds. Fixed command chain alone fails. | Approved brief/role definition reconciled with `SPEC:405` and `WC:204-216`. Not defined. | O3. |
| **DG-03** | Explicit role and eligibility. | **PASS only** when dispatched middle, launched owner and person-opened peer have distinct duties, parent identity and authority. No-preamble promotion fails. | Approved role/authority table against current or explicitly amended `WC:11,62,69`. | O3/O4. |
| **DG-04** | Explicit authorized policy amendment. | **PASS only** if any WC-13/person-opened exception and retained prohibitions are named. Flag, preamble or larger depth alone fails. | Authorized decision traced to contract and test expectations. | O3; O4 eligibility. |
| **DG-05** | Coherent command packaging and D1. | **PASS only** with declared session-versus-Orca-calling command boundary, explicit unattended selection and bounded exception if needed. Environment-detected mode fails. | Approved entry-point/eligibility decision and static protocol review. | O3/O4; any Orca-calling O1/O2 entry point. |
| **DG-06** | Exact target-build depth/authority routes known. | **PASS only** with target evidence for worker-start, dispatch/inject/dry-run, Task creation and ordinary launches, retaining independent Task authority. All-fenced/all-free interpretations fail. | Version-bound target trace. R03 supplies historical classifications; AC-0.7 remains historical acceptance. Located replacement filename/default-two helper does not certify replacement routes. `CORRECTION:36-47`. | O3/O4. |
| **DG-07** | Effective setting, scope, migration and reversal established where required. | **PASS only** with loaded maximum, affected runtime/profile/hosts and authorized evidenced lowering/recovery disposition for existing descendants/questions. Stored/public/source-default value alone fails. | Target getter/storage/settings evidence and separately authorized observation where needed. Current stored/effective values, migration invocation/persistence and safe lowering unverified. | O3; O4 for depth/settings/equivalence claims. |
| **DG-08** | Exact-topology upward lifecycle established. | **PASS only** with recipients and behavior for asks, replies, status, completion, fences and creator settlement; remote included/excluded explicitly. | R03 historical local route is credited, not transferred. Exact-target source and lifecycle evidence required for current/runtime claims; replacement equivalence unverified. | O3/O4. |
| **DG-09** | Full mixed-mail handling without lost duties. | **PASS only** with one authoritative consumer, complete handling/logging before batch acknowledgment, parent/child identity and stale-generation rejection. Competing filtered-copy assumptions fail. | Consumer-ownership contract plus replay, mixed batch, note-write failure and fencing evidence. | O3; O4 sharing such mailbox. |
| **DG-10** | Receipt and application acknowledgments compose. | **PASS only** with sent/received/applied/queued/refused/settled distinctions, safe duplicates and late/unresolved handling. Parent acknowledgment as child application fails. | Two-edge protocol cases and message-ID trace, including late answers. | O3/O4. |
| **DG-11** | Aggregate progress, outcomes and admission defined. | **PASS only** with own/child progress and success/partial/blocked/failed/missing-child rules. Heartbeats or all children merely settled are insufficient. | Outcome table, child artifact references, dropped-input reasons and independent upper admission. | O3/O4. |
| **DG-12** | Children retain owner when middle cannot act. | **PASS only** when upstream ask, human prompt, exhaustion, fence, exit and replacement each retain named service/intervention owner without overlap. Mail transfer alone fails. | Transition-ownership cases and authorized takeover or safe-escalation evidence. | O3/O4. |
| **DG-13** | Retry/cancel/resources bounded across lineage. | **PASS only** with failed starts, nudges, questions, restarts and helper counts retained across replacement, predecessor settlement and quiescence. Manager budget reset fails. | Persistent accounting and duplicate-start/replacement cases preserving WC-6 and ladder restrictions. | O3/O4. |
| **DG-14** | Sufficient supervisor checkpoint. | **PASS only** if successor recovers children, attempts, paths, Deliveries, applied answers, admissions, budgets, uncertain effects and next work without redo. Omitting them in worker-only summary fails. | Defined checkpoint and separately authorized recovery artifact consistent with WC-15 or approved amendment. | O3/O4. |
| **DG-15** | Human-only decisions stay non-transitive. | **PASS only** if parent/peer text, relays and credentials cannot replace Ruling, permission approval or genuine human handback; escalation reaches actual person. | Provenance decision and negative cases for relay, frozen retry and human prompts. Another agent claiming approval cannot satisfy this. | O3/O4. |
| **DG-16** | Grants remain within authorized policy. | **PASS only** with explicit issuance/attenuation, resources/actions, expiry and Task scope, retaining required human commit instruction or separately approved replacement. Copied parent grant fails. | Approved grant policy and existing Dispatch-capability semantics before assuming new mechanism necessary. | O3/O4. |
| **DG-17** | Trusted presenter and request identity. | **PASS only** if role, parent, presenter, Task/Dispatch/session, worktree/branch and action bind to trusted evidence. Self-assertion or receiver mistaken for sender fails. | Binding design and spoofed/foreign/stale identity rejection cases. | O3/O4; O2 automated cross-control. |
| **DG-18** | Incoming reports stay untrusted until validation/admission. | **PASS only** with enforced boundary on every selected path, safe malformed/unknown rejection and inert text. Schema/prompt alone fails. | Channel-specific validator, trusted producer and validated-file alternative if selected. Documented hook is not deployed proof. | O3/O4. |
| **DG-19** | Security boundary fails safely and separates origin. | **PASS only** with target timeout/error handling, installation, event coverage, ordering and peer-not-human approval verified. Registration alone fails. | Exact-target envelopes and failure/ordering evidence. No existing successful laundering exploit is assumed. | O3/O4 where hooks carry boundary. |
| **DG-20** | Channel compatibility without default tool widening. | **PASS only** when holds, refusal, expiry, drops and authorized inbound choices are accounted for. Exact-name equality, all-bypass or successful send alone fails. | Actual channel/mode/settings evidence and approval for any choice. Sender-class internals partly open. | O4; O3/O2 native peer-text paths. |
| **DG-21** | Replay/revocation safety beyond authenticity. | **PASS only** with trusted time/expiry, revocation freshness/outage policy and race-safe duplicate/one-use state. Valid chain plus nonce alone fails. | Verifier/request-context, concurrent replay/revocation cases and scoped library decision if credentials selected. | O3/O4 grant variants. |
| **DG-22** | Enforcement coverage and required probes reconciled. | **PASS only** with declared executable/forms/bound status, approved complete supervision route and denial of unauthorized effects within stated boundary. Alternate spelling is not a solution. | B1/B2 coverage/compatibility disposition and exact-target evidence. Existing probe gap is not solved here. | O3/O4; bound O1/O2. |
| **DG-23** | Exclusive write/Git/freeze/cleanup ownership. | **PASS only** with authorized setup/placement, sole writers, protected evidence, same-worktree resume, unseen-commit review and removal predicates. Parent done/token possession is not safe deletion. | Ownership map, admission records and negative conflict/freeze/removal cases. | O3/O4. |
| **DG-24** | Distribution/evaluation evidence matches claim. | **PASS only** with relevant canonical/plugin/dev/installed/visible command agreement and static pins distinguished from live acceptance. Unsupported remote/provider variants explicitly excluded. | Copy/version/parity record and scoped operational acceptance where claimed. Historical path checks are not universal freshness; vanished bundle is not existing current target. | O3/O4; new O5 wrapper claims. |
| **DG-25** | D5 record and issue scope dispositioned. | **PASS only** if mailbox omission is resolved without inferred waiver and hierarchy/security remain separate from #339 flat supervision and #423 knowledge. “V2 complete” alone fails. | Authorized record cross-referencing `SPEC:405`, `D5-REC:49` and all 35 requirement dispositions. | O3; O4 claiming same hierarchy decision. |

#### Gate interpretation

| Boundary | Required interpretation |
|---|---|
| Revisit trigger | DG-01 and DG-02 preserve D5's two-part trigger; the numbers are references, not ordering. |
| Historical evidence | DG-06 retains AC-0.7 and historical classifications. It does not pretend traces were absent or certify replacement paths. |
| Source versus operation | DG-08 separates historical source-supported route, exact-target source applicability and unverified live lifecycle. |
| Settings | Source default/fallback two and migration definition do not pass DG-07. Explicit valid one remains accepted by resolver, while unmarked resolved one meets migration's legacy condition; execution/persistence remains unverified. |
| Human authority | DG-15/DG-16 cannot pass from an agent's assertion that the user approved. |
| Transport/security | DG-18-DG-21 preserve channel-specific validation/grant conditions without equating transports or selecting a library. |
| Applicability | Excluding a capability must name it. Excluding remote helpers cannot support remote readiness. |
| Evaluation | Conditions that require observations are not authorization to collect them. Separate permission remains necessary. |

**Evidence:** Complete synthesis 04 gate table; `WC:11,41-79,97-179,204-273`; R01-R08; W01-W04; `CORRECTION:18-51`.

**Present status of the 25 conditions.** All 25 approval conditions are open and none is claimed as passed here: Section 7.5 states that the complete applicable set is not passed, and only 7 of the 25 rows carry a status in their own text while the other 18 record none.

| Condition(s) | Status stated in the Section 7.5 row | Count |
|---|---|---|
| DG-01 | Not established. | 1 |
| DG-02 | Not defined. | 1 |
| DG-06, DG-08 | Historical evidence is credited, not transferred; replacement-build routes are not certified and replacement equivalence is unverified. | 2 |
| DG-07 | Current stored/effective values, migration invocation/persistence and safe lowering are unverified. | 1 |
| DG-20 | Sender-class internals are partly open. | 1 |
| DG-24 | Historical path checks only; they are not universal freshness. | 1 |
| DG-03, DG-04, DG-05, DG-09 to DG-19, DG-21 to DG-23, DG-25 | No status recorded: each row gives the test and the evidence that would satisfy it, and none records satisfying evidence. Not passed. | 18 |

### 7.6 What would change the recommendation

| New evidence or decision | Effect |
|---|---|
| Approved autonomous brief plus qualifying material runtime-only split record. | Removes need/brief barriers to reconsider O3; does not settle authority or recovery alone. |
| Applicable authority, lifecycle, enforcement and human conditions pass for exact native-local scope. | Supports changing O6 to O3 for that bounded evidenced variant, not unrestricted recursion. |
| Demonstrated persistent-owner need that native Dispatch helpers cannot adequately serve, plus O4-specific eligibility/upward conditions. | Could justify distinct O4 owner role, not depth workaround. |
| Work needs only self-contained investigation/review. | Existing O5 addresses use case; not justification for external subordinate mode. |
| Independent persistent owners without upper/lower control. | O2 fits that work; does not establish hierarchy. |
| Measured middle planning/context/reconciliation/recovery cost exceeds saved root work. | Strengthens durable O1 selection for that workload. |
| Upgrade changes defaults, migration or shutdown. | Reassess affected mechanism conditions; no automatic authority change. The present source replacement already requires snapshot separation, not assumed equivalence. |
| A condition cannot be met without weakening human decisions, protected work or bounded recovery. | Keep O6 or reject variant. Convenience does not create transitive consent. |

**Recommended next action.** This names one decision and one evidence step. Nothing here is started, built or authorized, and no condition is claimed as passed.

1. **The one decision: gap A01 (Important), the PR #449 phrase "a coordinator under another orchestrator".** Choose between (a) narrowing the phrase now, as a wording change separate from any subordinate mode, and (b) leaving the wording as shipped and keeping A01 recorded as a deferred defect. Under (a), the Section 8 O1 wording surface applies, each item only if that wording is selected. That surface is `CLAUDE.md`, `src/superclaude/core/CLAUDE.md`, the ccsession README, the worktree-hook message with its exact-message test, and their copies. The report sizes O1's wording and distribution clarification as S effort with low incremental risk for O1 as a whole (6.2). Option (a) is the "explicitly narrowed ownership wording" form of A01's target state (4.1), which also asks that supervised and nonworker cases be dispositioned. Under (b), the contradiction with `WC:62,69` stays in current guidance (Section 2.2) and A01 stays open and visible (6.7, Q01). Nothing is granted either way: the WC-13 deferral did not implement a subordinate or approve a grant (7.4), and neither choice changes that. *Inference, not a finding:* the report does not choose between (a) and (b). Reading 6.2, 6.7 and Section 8 together, (a) looks the cheaper way to retire an Important defect, because those sections treat wording clarification as a separately adopted change (6.7).
2. **Who decides.** The contract owner: the person with authority over the worker contract and the PR #449 wording. The report names no individual. It says only that existing authority "remains binding until an explicit authorized decision changes it" (7.4).
3. **Cheapest evidence step for DG-01 and DG-02.** DG-01 passes only with the original Task, the discovered split, why it could not reasonably be known before dispatch, the follow-up Task and measured extra coordination time accepted as material. The existing rule `WC:246` already tells a coordinator to record in its run notes each follow-up Task created because a worker's result showed work that could not be planned before dispatch, with the extra time that cost. Following that rule in ordinary coordinator runs adds a record, not a run. It does not by itself supply the acceptance as material that DG-01 also requires. DG-02 moves only by a decision approving an autonomous composite brief (planning scope, allowed children and actions, outputs, stops, bounds; see Q04), not by a run. Deliberately running a trial to produce a DG-01 record is a live Orca evaluation. It needs separate authorization, which this report does not give and does not start.

### 7.7 Source coverage and retained limits

| Source | Contribution to recommendation | Qualification |
|---|---|---|
| R01 full clause matrix | Role distinction, all worker/coordinator duties, grants, freezes, admission and human authority. | Compatible protections are not permission or live passes. Repeated quotations/worked example consolidated. |
| R02 full state/ack/ladder tables | Dual service, own/child progress, mixed mail, parent failure, resources and checkpoints. | No automatic #434 enforcement or incident elimination. C9 deleted; C10-C14 not assumed delivered. |
| R03 complete mechanics | Historical native route, per-call authority/depth, parentage and ordinary-launch distinctions. | No live, federation, effective setting, safe lowering or complete replacement equivalence. |
| R04 controlling corrections | Literal coverage, missing probes, trusted-role gap and real-event/rewrite limits. | No bypass permission or automatic expansion. U7/U28 separate. |
| R05 full reuse matrix | Fourteen launchers/56 judgments as partial helper/scheduling/report patterns. | No complete middle-supervisor precedent; subprocess bypass not security pattern. |
| R06 | Approved history, actual trigger, final scoped alternative, accepted trace and human/Git boundaries. | P1 original FAIL not final; P2 static merge not live. Historical source answers not erased or transferred. |
| R07 with supplements | Conditional files/tests/copies and distinct sync/build/install relationships. | Approved current inventory complete; 867 matching archival lines/274 paths remain unread/excluded. |
| R08 all requirements | All 35 dispositions; #339/#423/#409/#446/#326 separation. | No unbuilt product, scale, server, observer-control or Git scope bundled into approval. |
| W01 | Documented inbound hook, mode classes, channels and consent boundary. | No authenticated deployed origin/fail-closed certification; examples/community wording not substitutes. |
| W02 | Conditional cost/latency/context/error/budget trades and no matched hierarchy benefit. | Corrected Cognition denominators/population; no numeric scoring or forecast; unseen notebook excluded. |
| W03 | Attenuation feasibility versus trusted authorization/enforcement/lifecycle; CaMeL distinction. | No adopted dependency, support assurance, debate winner or token-based human consent; PDF limits retained. |
| W04 | Public demand, terminology, migration, host and shutdown qualifications. | Public four not local effective value; source 404 not privacy/absence; public stop not quiescence. |
| Dated snapshot correction | Separates policy one, historical one, source two and public four; constrains exact-target claims. | No profile reopened; current stored/effective, running build, migration execution and live equivalence remain unverified. Historical bundle not replaced by name in citations. |

**Decision:** Retain O6 for the proposed subordinate mode. The applicable conditions are falsifiable prerequisites for a later authorized decision, not an implementation sequence. No implementation, launch, upgrade, source change, permission/settings change or live trial is authorized. Live nesting, delivery, recovery, effective settings and tests remain evidence limits, not passed conditions.

## 8. Implementation Plan
N/A as an implementation plan — the requester asked for a decision report, not a plan.

### Change surface per option

These tables describe **conditional consequences of choosing an option**, not instructions to edit the listed files. “No inherent change” means the option can retain that boundary. There are no implementation phases, ordered steps, effort schedule or integration checklist.

Project-relative paths resolve beneath `/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test`. Absolute global and Orca paths identify separate installations. R01/R03/R04/R07 and GQ resolve through Section 2.1.

The inventory records observation-time existence, not universal current existence, parity or permission. In particular:

- R03's installed route, authority, parentage and launch findings remain historical.
- `/opt/Orca/resources/app.asar.unpacked/out/main/chunks/orcad-migration-source-retention-B_-OYaBD.js` is a **historical, now-absent reference**, not a current edit target.
- Locating a replacement bundle does not transfer historical offsets or certify equivalent behavior.
- The dated source default/fallback two and migration definition do not establish effective settings, migration execution or required Orca edits.

**Evidence:** R07:11-15,168-198; R04:87-107; GQ:10-12,68-70,110-119; `CORRECTION:8-51`.

#### What existing tests actually pin

The pin identifiers below resolve the option tables' “Pinned by” entries.

| Pin | Test file | Actual assertion and limit |
|---|---|---|
| **P-contract** | `tests/skills/test_worker_contract.py` | Separate phrase/content checks for no command fan-out and no worker-session fan-out, plus brief, rules and eligibility. `NEVER_AS_WORKER`, `UNATTENDED_EXPECT`, heading equality and unattended scans are distinct. Not exact whole-contract bytes or live nesting. |
| **P-message** | `tests/hooks/test_require_orca_worktree_agent.py` | Exact expected denial/stderr, including subordinate-coordinator sentence. Changed emitted message affects expectation. |
| **P-governed** | `tests/hooks/test_require_orca_worktree_agent_governed.py` | Denial prefix and example launch form, not whole ownership sentence. Uses original command; not live rewrite-order proof. |
| **P-roles** | `tests/core/test_orca_session_launch_guidance.py` | Required launch/ownership phrases, role words “orchestrator” and “coordinator,” and appended-paragraph equality. Does not pin exact “under another orchestrator” phrase. |
| **P-guard** | `tests/hooks/test_launch_level_guard.py` | Classified launch/dispatch/create examples and separately listed reads. Hand-written subagent envelopes do not prove live identity inheritance. |
| **P-hooks** | `tests/cli/test_install_hooks.py` | Registration, packaging/executable and installation checks; specified worktree-hook source/plugin byte equality. Not universal hook/registry parity. |
| **P-guide** | `tests/commands/test_routing_plugin_parity.py` | Whole source/plugin routing-guide parity and specified skill-tree relationship. Wording can change without changing assertion if compared copies agree. |
| **P-install** | `tests/cli/test_how_we_work_install.py` | Guide shipping/equality in test target, not every existing global installation's freshness. |

**Sources:** R07:27-33,71-76,143-145; R01:152-156; R04:137-146. An affected regression surface is not automatically a required test edit. None of these tests was run for this investigation.

#### O1 - Retain two tiers, with conditional wording clarification

| Option | File or area | Kind | Why it would change | Pinned by | Source |
|---|---|---|---|---|---|
| O1 | `CLAUDE.md` | Rule text | Only selected ownership clarification. Retaining topology itself requires no new policy; broad owner wording does not authorize workers. | No exact project-root wording pin identified. | R07:67-76; R01:31-60. |
| O1 | `src/superclaude/core/CLAUDE.md`; `src/superclaude/skills/ccsession-tag/README.md` | Rules/README | Selected clarification affects paired paragraphs; worker restriction can remain. | P-roles; test need not change if valid phrase/role/equality requirements remain. | R07:23,28,71-74. |
| O1 | `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh`; `plugins/superclaude/hooks/scripts/require-orca-worktree-agent.sh` | Hook/mirror | Printed explanation only if wording selected. Scanner is not hierarchy authority and need not change. | P-message; P-hooks byte equality; P-governed narrower. | R07:24,27,31,72; R04:38-47. |
| O1 | `tests/hooks/test_require_orca_worktree_agent.py`; `tests/core/test_orca_session_launch_guidance.py` | Test surfaces | Exact expectation changes with emitted message; role/parity test is affected, not automatically edited. | Exact-message versus P-roles distinction. | R07:27-28,72-73. |
| O1 | `.claude/skills/ccsession-tag/README.md`; `.claude/hooks/require-orca-worktree-agent.sh`; `/home/coder/.claude/CLAUDE.md`; `/home/coder/.claude/skills/ccsession-tag/README.md`; `/home/coder/.claude/hooks/require-orca-worktree-agent.sh` | Generated/installed copies | Distribution dependencies only for corresponding wording change, not additional canonical edit targets. Global equality not asserted. | Makefile source/dev relationship; specified P-hooks scope. | R07:23-24,74,143-145. |
| O1 | `src/superclaude/core/WORKER-CONTRACT.md`; `src/superclaude/core/HOW-WE-WORK.md` | Rules | No inherent nested-policy change. Retain WC-13/person-opened model; separate Orca-calling entry point still raises command boundary. | P-contract/P-guide/P-install. | R07:75,88; R01:62-80. |
| O1 | `src/superclaude/hooks/scripts/launch-level-guard.sh`; `tests/hooks/test_launch_level_guard.py` | Hook/test | Conditional bound-supervision policy surface. Required recognized probes cannot run unchanged under B2. O1 role fit does not solve mismatch or authorize expansion. | P-guard; contract probes separately required. | R04:93-107; R07:190-192. |
| O1 | `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`; `docs/designs/issue-watcher.md` | Documentation | Independent stale empty-inventory implication and WC-13 citation drift, not changes forced by O1. | P-contract supports populated set; no exact prose pin identified. | R07:147-165. |

#### O2 - Independent person-opened peers

| Option | File or area | Kind | Why it would change | Pinned by | Source |
|---|---|---|---|---|---|
| O2 | `src/superclaude/core/WORKER-CONTRACT.md`; `/home/coder/.claude/WORKER-CONTRACT.md` | Rules/installed copy | Conditional independent Task/writer/admission clarification; no inherent WC-13 reversal or shared-inbox authority. Installed dependency is not parity proof. | P-contract ownership/admission/rules. | R07:78-88; R01:113-125,135-148. |
| O2 | `src/superclaude/core/HOW-WE-WORK.md`; `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; `/home/coder/.claude/HOW-WE-WORK.md` | Rule/mirror/installed | Selected routing explanation separates peers from upper/lower relationship. Opening peers does not supply new upward lifecycle. Packaged copies listed below. | P-guide/P-install. | R07:26,82-83; R03:170-171. |
| O2 | `CLAUDE.md`; `src/superclaude/core/CLAUDE.md`; `src/superclaude/skills/ccsession-tag/README.md`; `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` | Rules/README/hook | Conditional if peer interpretation is adopted for ambiguous wording. No scanner change inherent; O1 distribution effects apply only to changed wording. | P-roles/P-message where applicable; no exact root pin. | R07:71-74,84. |
| O2 | `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | Documentation | Conditional independent-owner/internal-helper/worker explanation. New coordinator-only command is separate eligibility choice. | P-contract underlying policy; no exact guide prose pin. | R07:85-86. |
| O2 | `tests/skills/test_worker_contract.py`; `src/superclaude/core/WORKER-CONTRACT.md` | Test/rules | No inherent never-worker or unattended-set change. Relevant only if actual command eligibility/inventory changes; Orca-calling command boundary remains separate. | P-contract's distinct list/heading/scan checks. | R07:29,86; R01:64-80. |
| O2 | `src/superclaude/hooks/scripts/launch-level-guard.sh`; `tests/hooks/test_launch_level_guard.py` | Hook/test | Conditional launch/report/probe policy. Person-opened is not unbound; B1 literal coverage and B2 probe gap apply when bound. | P-guard; no automatic permission/expansion. | R07:87,190-192; R04:93-107. |
| O2 | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; `.dev/orca-command-refactor/decisions/APPROVED.md` | Decision records | No depth reversal inherent to independent peers. Historical decisions do not become different merely because peers are chosen. | No exact decision-text pin identified; shipped rules have P-contract. | R07:88,102; R01:71-80. |

#### O3 - Supervised middle worker with native helpers

This is the final scoped session-layer alternative. Native helper mechanisms are historically source-established; present worker policy prohibits their use for this role. Replacement-build equivalence and effective configuration remain unverified.

| Option | File or area | Kind | Why it would change | Pinned by | Source |
|---|---|---|---|---|---|
| O3 | `src/superclaude/core/WORKER-CONTRACT.md` | Rules | Approved O3 would affect eligibility/WC-13, autonomous brief/helper limits, questions, own/child completion, aggregate results, admission, retries and chains. Existing multiple commands are not composite authority. | P-contract rule/brief/result checks; broader than one sentence. | R07:90-96,163; R01:84-127. |
| O3 | `src/superclaude/core/WORKER-CONTRACT.md` | Rules | Conditional dual-service allocation: mixed mail, Delivery/application acknowledgments, progress/states, pending answers, intervention owner, budgets, fencing/failure and handoff. Historical handback is not full recovery. | P-contract liveness/follow-up/chain/handoff; not live scheduling proof. | R01:113-120,143-146; R03:64-81; GQ:20-25. |
| O3 | `src/superclaude/core/WORKER-CONTRACT.md`; `src/superclaude/skills/sc-implement-protocol/refs/qa.md` | Rules/acceptance boundary | Preserve Task-specific grant provenance, outward owner, human Rulings, exclusive creators, setup/writers, admission/fan-in, protected removal, freezes and resume. Middle worker cannot assume root merge/outward duties. QA reference is not automatically edited. | P-contract WC-9/WC-11/safety; QA rejects other-agent acceptance. | R01:121-148; R07:94,102. |
| O3 | `src/superclaude/core/WORKER-CONTRACT.md`; `tests/skills/test_worker_contract.py` | Rules/test | WC-8 can remain for session-layer fan-out. Orca-calling command additionally affects broad opening rule and unattended scans. D1 is mode selection, not all-flags ban. | P-contract command rule, delimiter, Orca scan/content. | R07:95; R01:62-80,154-156. |
| O3 | `tests/skills/test_worker_contract.py` | Test | Actual new/reclassified command conditionally affects never-worker membership, expectations, headings, flags/phrases and nested results. No blanket change inherent to session role. | P-contract distinct positive/negative/content checks. | R07:29,96; R01:152-156. |
| O3 | `CLAUDE.md`; `src/superclaude/core/CLAUDE.md`; `src/superclaude/skills/ccsession-tag/README.md` | Rules/README | Approved exception affects explicit worker-create prohibition and owner explanation; labels/depth alone are not approval. | P-roles; no exact root pin. | R07:99; R01:31-60. |
| O3 | `src/superclaude/core/HOW-WE-WORK.md`; `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | Rules/mirror/docs | Approved eligibility/routing explanation changes; repeated WC-8 text is not permission for command dispatch. | P-guide/P-contract; no exact developer prose pin. | R07:97-98; R01:68-80. |
| O3 | `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh`; `plugins/superclaude/hooks/scripts/require-orca-worktree-agent.sh` | Hook/mirror | Conditional printed explanation. Scanner does not bind parent grant/count/scope/role; no scanner edit inherent to policy decision. | P-message/P-governed/P-hooks with distinct reach. | R07:100; R04:38-64,113-119. |
| O3 | `src/superclaude/hooks/scripts/launch-level-guard.sh`; `tests/hooks/test_launch_level_guard.py`; `docs/designs/sc-issue-launch-level-hook.md` | Hook/test/docs | Separate bound launch/report/probe decision. Recognized non-exempt Orca is ESCAPE; required probes also conflict. Literal coverage and trusted parent/scope binding differ. No all-spelling block or successful bypass established. | P-guard; U7 visibility and U28 installation remain separate. | R04:53-64,87-107,167-176; R07:101,188-194. |
| O3 | `src/superclaude/hooks/scripts/launch-job-identity.sh`; `src/superclaude/hooks/hooks.json`; `src/superclaude/cli/install_hooks.py` | Identity/registration/install | Conditional only if child governance/integration changes. Job identity/registration is not hierarchy grant, actual envelope, rewrite order or first-tool binding. No mandatory edit to all three. | P-hooks specified scope; P-governed/P-guard not live proof. | R04:38-47,113-146,167-176. |
| O3 | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; `.dev/orca-command-refactor/decisions/APPROVED.md`; `.dev/orca-command-refactor/decisions/D5/RECOMMENDATION.md`; `.dev/orca-command-refactor/decisions/D5/debate/adversarial/merged-output.md` | Decision records | New approved decision would amend retained outcome, not rewrite rejection/draft status as prior permission. Final session-layer alternative differs from original command proposal. | No exact decision-text pin; P-contract shipped restrictions. | R07:102,159-166; R01:162-176. |
| O3 | `/opt/Orca/resources/app.asar.unpacked/out/main/chunks/orcad-migration-source-retention-B_-OYaBD.js`; `/opt/Orca/resources/app.asar.unpacked/out/shared/nested-worker-depth.js`; `/opt/Orca/resources/app.asar.unpacked/out/cli/specs/orchestration.js` | Historical capability/source references | Not prescribed Orca edits or current-path certification. Historical same-host/new-agent ancestry, creator route/reply/fences/handback remain evidence. Effective adequate maximum matters; raising is not removing fence. Dated source default/fallback two/migration does not prove loaded value or execution. | No IronClaude test proves exact-target nested lifecycle/safe lowering. | R03:28-81,118-150,170-177; `CORRECTION:25-51`. |

#### O4 - Ordinary launched handoff-owner subordinate

| Option | File or area | Kind | Why it would change | Pinned by | Source |
|---|---|---|---|---|---|
| O4 | `src/superclaude/core/WORKER-CONTRACT.md`; `/home/coder/.claude/WORKER-CONTRACT.md` | Rules/installed | Explicit launched-owner eligibility needed. No preamble does not prove person-opened coordinator identity. Worker initiation still violates WC-13. Global parity not asserted. | P-contract identity/WC-13/owner/admission. | R07:104-108; R01:53-60,84-105. |
| O4 | `src/superclaude/core/WORKER-CONTRACT.md`; `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | Rules/docs | New ordinary upward contract for correlation, liveness, aggregate result, questions/acks, admission and failure/recovery, not worker impersonation. No complete existing O4 channel test identified. | P-contract existing lifecycle, not new owner protocol. | R07:109,115; R01:113-127; R03:98-116. |
| O4 | `src/superclaude/core/WORKER-CONTRACT.md`; `src/superclaude/skills/sc-implement-protocol/refs/qa.md` | Rules/acceptance boundary | Ownership does not transfer consent, commits, outward/PR/merge/removal/Ruling authority. Placement, freezes, admission, fan-in and resume retained. QA reference not automatic edit. | P-contract safety; rejection of other-agent acceptance. | R07:110,115; R01:121-148. |
| O4 | `CLAUDE.md`; `src/superclaude/core/CLAUDE.md`; `src/superclaude/skills/ccsession-tag/README.md`; `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` | Rules/README/hook | Conditional precise ordinary/supervised ownership explanation. Printed sentence supplies neither trusted parent nor reporting protocol; copies remain separate. | P-roles/P-message/P-hooks where applicable. | R07:111; R04:38-64. |
| O4 | `src/superclaude/core/HOW-WE-WORK.md`; `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | Rules/mirror/docs | Selected O4 introduces eligibility outside current person-opened summary. Different owner model, not O3 without depth. | P-guide/P-install/P-contract. | R07:112; R03:83-116,173. |
| O4 | `src/superclaude/hooks/scripts/launch-level-guard.sh`; `tests/hooks/test_launch_level_guard.py`; `docs/designs/sc-issue-launch-level-hook.md` | Hook/test/docs | Conditional bound launch/report/probes. Calling launch “handoff” does not change classification. B1 ceiling is not bypass; B2 still affects supervisor. | P-guard; no current role exception inferred. | R07:113,190-192; R04:87-107. |
| O4 | `src/superclaude/hooks/scripts/launch-job-identity.sh`; `src/superclaude/hooks/hooks.json`; `src/superclaude/cli/install_hooks.py` | Identity/registration/install | Conditional child-governance changes only. Identity/registration/install does not prove role or inheritance; real envelopes/timing/order unverified. | P-hooks specified scope; other pins retain live limits. | R04:38-64,113-146,167-176. |
| O4 | `tests/skills/test_worker_contract.py`; `src/superclaude/core/WORKER-CONTRACT.md` | Test/rules | New coordinator-only command conditionally affects eligibility; Orca-calling command boundary separate. No hypothetical command path assumed. | P-contract never-worker and unattended scans. | R07:114; R01:71-80. |
| O4 | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; `.dev/orca-command-refactor/decisions/APPROVED.md` | Decision records | New eligibility/authority decision, not retrospective alteration of D1-D5/Git permission. | No complete O4 channel test/exact decision pin. | R07:115; R01:129-150. |
| O4 | `/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/agent-launch.js`; `/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/worktree-create-agent-launch.js`; `/opt/Orca/resources/app.asar.unpacked/out/shared/resolved-worktree-lineage.js` | Historical installed references | Not edit targets or new-build certification. Historical launch lacked automatic worker records; validated ancestry is not lifecycle authority and operation ID is not Dispatch ID. | No complete owner→children→upward lifecycle test identified. | R03:83-116,173; `CORRECTION:42-45`. |

#### O5 - Existing internal Agent helpers

| Option | File or area | Kind | Why it would change | Pinned by | Source |
|---|---|---|---|---|---|
| O5 | `src/superclaude/core/WORKER-CONTRACT.md`; `/home/coder/.claude/WORKER-CONTRACT.md` | Rules/installed | No inherent change. Assigned command top-level, enclosing lifecycle, nested results and accepted heartbeat gaps retained. Global content not asserted. | P-contract WC-7/results/waits. | R07:117-125; R01:58,77,88-101. |
| O5 | `src/superclaude/commands/adversarial.md`; `src/superclaude/skills/sc-adversarial-protocol/SKILL.md` | Existing reuse surfaces | Activation, helper collection/failure and merge delegation exist. Selecting reuse requires neither edits nor claim of successful execution. | P-contract adversarial expectations, not live helper run. | R07:37,122; full return §§4,9. |
| O5 | `src/superclaude/core/HOW-WE-WORK.md`; `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | Rules/mirror/docs | Optional internal-versus-external clarification. No per-helper Orca Task/Dispatch/retry records follow. | P-guide/P-install/P-contract WC-7/WC-8. | R07:123; R03:174. |
| O5 | `tests/skills/test_worker_contract.py` | Test | Actual new/changed wrapper declarations conditionally affect expectations, heading equality and nested checks. Existing helpers do not expand inventory automatically. | P-contract expectations/set/tokens/nested paths. | R07:124; full return §9. |
| O5 | `src/superclaude/hooks/scripts/launch-level-guard.sh`; `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh`; `tests/hooks/test_launch_level_guard.py` | Hooks/test | No external-launch exception inherent to local/background helpers; remote isolation differs. Classification not live inheritance, unrestricted provider or absence of other limits. | P-guard; syntax hook separate for actual worktree forms. | R04:78-79,107,143-146; R03:163,174,187. |
| O5 | `CLAUDE.md`; `src/superclaude/core/CLAUDE.md`; `src/superclaude/skills/ccsession-tag/README.md` | Rules/README | Independent wording cleanup only if chosen. Internal helpers do not define disputed external subordinate. | P-roles; P-message only for separate hook wording. | R07:126. |

#### O6 - Gated deferral

| Option | File or area | Kind | Why it would change | Pinned by | Source |
|---|---|---|---|---|---|
| O6 | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; `.dev/orca-command-refactor/decisions/D5/RECOMMENDATION.md` | Decision records | Conditional clarification of autonomous brief/material split, historical/current-target traces and additional mailbox clause. Omission is not proven waiver; documented prerequisite is not passed prerequisite. | No exact D5 sentence pin; P-contract retained prohibition. | R07:128-134,164; R01:175-176; GQ:26-28; `CORRECTION:47`. |
| O6 | `src/superclaude/core/WORKER-CONTRACT.md` | Rules | No inherent change. Follow-up/time-record duty can supply evidence but does not prove qualifying material run record exists. | P-contract text, not actual run-note sufficiency. | R07:133; R01:160,176; GQ:26. |
| O6 | `src/superclaude/core/WORKER-CONTRACT.md`; `src/superclaude/core/HOW-WE-WORK.md`; `tests/skills/test_worker_contract.py` | Rules/test | Retain fan-out, command/session and eligibility boundaries; no second authority mode or transferable grant. | P-contract/P-guide/P-install; no mandatory expectation change. | R07:134; R01:71-80,138-148. |
| O6 | `CLAUDE.md`; `src/superclaude/core/CLAUDE.md`; `src/superclaude/skills/ccsession-tag/README.md`; `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` | Rules/README/hook | Independent wording decision, not forced or resolved by deferral. O1 copy/test consequences if adopted. | P-message versus P-roles; P-hooks specified mirror. | R07:135. |
| O6 | `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`; `docs/designs/issue-watcher.md` | Documentation | Independent stale inventory/citation issues remain. Current 31 declarations are neither zero nor 31 successful runs; P0 history can be labelled historical. | P-contract populated set; no exact prose pin. | R07:136,147-165. |
| O6 | `src/superclaude/hooks/scripts/launch-level-guard.sh`; `tests/hooks/test_launch_level_guard.py`; `docs/designs/sc-issue-launch-level-hook.md` | Hook/test/docs | No relaxation inherent. Recognition/probe/role-binding/live identity/rewrite limits remain, not new approved work. | P-guard static scope. | R07:137,188-194; R04:87-107,167-176. |

### Sync and verification ripple

These are distribution relationships, **not an execution sequence**. Make targets, installers and tests were inspected, not run.

#### Distribution surfaces and ceilings

| Relationship | Specific files/copies | Established boundary | Source |
|---|---|---|---|
| Source/development | `Makefile`; `.claude/skills/ccsession-tag/README.md`; `.claude/hooks/require-orca-worktree-agent.sh`; `.claude/hooks/launch-level-guard.sh`; `.claude/hooks/launch-job-identity.sh` | Defined sync-dev/verify-sync source/dev relationships. Not global core install or universal plugin/global parity. Dev copies generated, not canonical edit sources. | R07:36,143-145. |
| Specified hook mirror | `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh`; `plugins/superclaude/hooks/scripts/require-orca-worktree-agent.sh`; `tests/cli/test_install_hooks.py` | Explicit byte equality for this pair. Matching selected tokens elsewhere is not whole-copy equality. | R07:31,143; R04:123-135. |
| Conditional guard/identity mirrors | `plugins/superclaude/hooks/scripts/launch-level-guard.sh`; `plugins/superclaude/hooks/scripts/launch-job-identity.sh`; `plugins/superclaude/hooks/hooks.json` | Inventoried counterparts for actual mechanism/registration change, not mandatory changes for every policy choice. | R04:121-135. |
| Routing guide | `src/superclaude/core/HOW-WE-WORK.md`; `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; `/home/coder/.claude/HOW-WE-WORK.md`; P-guide/P-install files above | Source/plugin full parity; test-target installation equality. No project `.claude` guide found in inventory; global equality not assumed. | R07:26,32,143. |
| Packaged guide copies | `.venv/lib/python3.11/site-packages/superclaude/_src/superclaude/core/HOW-WE-WORK.md`; `.venv/lib/python3.11/site-packages/superclaude/_plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; `pyproject.toml` | Inventoried wheel/environment artifacts including source/plugin trees. Not independent edit targets, fresh-build proof or whole-install parity. | R07:26,36,143; full return §11. |
| Plugin build | `Makefile`; `scripts/build_superclaude_plugin.py` | Packages plugin input tree, not source-to-plugin synchronizer; can package stale mirror. No build run. | R07:36,143-145. |
| Core/global install | `src/superclaude/cli/install_core.py`; `/home/coder/.claude/CLAUDE.md`; `/home/coder/.claude/WORKER-CONTRACT.md`; `/home/coder/.claude/HOW-WE-WORK.md` | Separate from dev sync. Existing targets skipped without force. Behavioral description, not overwrite advice or current-content proof. | R07:36,143; R01:154. |
| Hook/global and README | `src/superclaude/cli/install_hooks.py`; `/home/coder/.claude/hooks/require-orca-worktree-agent.sh`; `/home/coder/.claude/hooks/launch-level-guard.sh`; `/home/coder/.claude/hooks/launch-job-identity.sh`; `/home/coder/.claude/skills/ccsession-tag/README.md` | Original inventory identified copies. Hook copy skips existing scripts without force; no general README overwrite/freshness guarantee inferred. | R07:23-24,36,143-145; R04:127-135. |
| Mutation-prone verification test | `tests/cli/test_verify_sync_hooks.py` | Intentionally mutates actual checkout files. Inspected only, not executed under read-only assignment. | R07:33,145. |

Original path observations retain their scope and date; this section does not re-certify every path's current existence. The historical Orca bundle is explicitly excluded from current existence certification. **Evidence:** `CORRECTION:36-45`.

#### Per-option distribution consequences

| Option | Source/development sync | Verification relationship | Plugin mirror/build | Installed copies | Routing-guide copies | Source |
|---|---|---|---|---|---|---|
| O1 | `Makefile`: actual selected README/hook wording affects named dev copies; root/core not globally installed by sync. | Covered source/dev comparison only; no result claimed. | Selected message affects specified hook mirror. Builder packages plugin, not agreement. | Conditional global CLAUDE/ccsession README/worktree hook; no refresh/parity claimed. | No guide change inherent to topology or narrow message cleanup. | R07:71-76,143-145; full return §11. |
| O2 | No sync inherent to opening peers; separately changed distributables retain normal relationships. | Actual changed components only; not peer ownership/mail certification. | Changed source guide implicates named plugin guide; build separate. | Global guide, conditionally contract/ownership copies, are dependencies of chosen clarification. | Actual source/plugin/global/two package paths remain distinct; no imagined project guide. | R07:82-88,143-145. |
| O3 | Actual command/skill/hook changes affect dev copies; core role/contract install separate. | Source/dev agreement is not policy correctness, plugin parity or visible-command eligibility. | Existing guide/hooks conditional; no new command/skill mirror path invented. | Global contract/guide/ownership/hooks conditional. Brief guard checks actual visible project/global command copies, not source alone. | Eligibility/routing affects named source/plugin relation and separate global/package artifacts. | R07:94-102,143-145; R01:120,154. |
| O4 | Actual distributed mechanisms only; core definitions separate. | Not owner lifecycle/upward protocol/child governance proof. | Existing mirrors conditional; packaging cannot supply missing contract. | Named global contract/guide/launch copies are semantic dependencies, not behavior equivalence. | Agent-launched eligibility summary and package/global distribution remain distinct. | R07:108-115,143-145. |
| O5 | Existing helpers need no sync. Actual adversarial-skill change has its skill/dev relationship. | Actual components only; not Orca child/provider proof. | No hook mirror inherent; optional guide explanation retains parity; build does not synchronize. | No wrapper path presumed. Existing global contract is not current-parity proof. | Optional clarification; not mandatory all-copy change. | R07:121-126,143-145. |
| O6 | No behavior sync inherent; independent wording has O1 relationships. | Preserved behavior is not successful verification. | No inherent behavior change; actual clarification retains specific mirror. | Dev sync does not refresh global contract/CLAUDE/guide. | No automatic guide edit; actual clarification has real copy relationships only. | R07:132-145. |

### Evidence reconciliation and retained limitations

| Finding | Controlling evidence | Consequence |
|---|---|---|
| Active inventory versus old partial status | R07:13; GQ:12,69,112. | Approved current-source/tests/copies inventory usable; archives remain excluded, not reopened. |
| Guard overstatement versus B1/B2 | R04:87-107; R07:188-194. | Bound literal `orca` scope only; observed alternate mismatch is not permission or live bypass. Listed worker-show not required enumeration/transcript/process probes. |
| Root-only/unknown route versus historical native helpers | R03:64-81; `CORRECTION:42-47`. | O3 has historical creator-route evidence; mixed-mail ownership/application/recovery and exact-target equivalence remain open. O4 lacks equivalent complete upward lifecycle. |
| Depth versus authority | R03:28-60,133-150; R01:31-80. | Historical worker-start/dispatch fences coexist with independent Task authority and unfenced ordinary launches. New Run not reset; WC-13 still applies. No current-build transfer. |
| Source setting versus safe operation | R03:118-131,154-164; `CORRECTION:18-34,51`. | Historical one, dated source two and public four separate. Current stored/effective, migration execution, propagation/lowering/recovery unverified. Runtime/profile is not per-Run/all-profile proof. |
| Ordinary ancestry versus supervision | R03:83-116. | Historical no automatic worker records; validated lineage not cosmetic, still not authority. Body labels do not create transport/lifecycle types. |
| P0/draft history versus current permission | R01:162-172; R03:133-150,197-207; R07:147-165. | Accepted documentary history is not attempted-refusal/depth-two/live proof. Draft statuses, single-command premises and old offsets not current facts. |
| Pins versus behavior/parity | R07:27-41,143-145; R04:133-146; GQ:36,48. | Exact text, roles, phrases, bytes and installation-target assertions differ. Registration/correspondence is not live behavior or universal freshness. |
| Historical bundle versus located replacement | `CORRECTION:36-47`. | Old filename/offsets preserved as history; absent old path is not existing target. Located replacement does not prove equivalent route/authority/recovery; no automatic substitution. |

### Source coverage and exclusions

| Source | Findings retained | Consolidation or exclusion |
|---|---|---|
| R01 complete evidence | Ownership/authority, command/session/D1, eligibility/WC-13, aggregate reports/admission, questions/acks, liveness/handoff/retry, grants/Git, placement/setup, freezes/resume/fan-in. | Full compatibility matrix in Section 6; grouped here by file/duty, not every safeguard prescribed for change. |
| R03 complete evidence | Historical per-route authority/depth, native route/handback/local limits, ordinary launches, parentages/types, setting scope and live/remote/reversal uncertainty. | No source bodies, discovery commands, profile contents or every offset reproduced as edit targets. Historical answers retained without replacement certification. |
| R04 complete evidence/corrections | Distinct syntax/session/job identity, missing trusted role, launch/report/probes, literal ceiling, unlisted probes, local/remote classification, registrations/install, event/order/first-tool limits, U7/U28 separation. | Older blanket claims superseded; scanner limits not transferred among hooks; no automatic role exception. |
| R07 complete evidence | Six options, pin differences, canonical/dev/plugin/global/package distinctions, eligibility/inventory relationships, independent stale docs and distribution ceilings. | Search counts/repeated old copies are provenance, not new findings or edits. 31 command stems not individually restated: populated expectation/heading relation is relevant. |
| GQ | Authority, aggregation, mail, recovery, settings, identity, freshness, measured need and stale-source limits. | Research Minor labels are not adoption safety ratings. Unrelated product/literature questions do not become file-change instructions. |
| Snapshot correction | Historical/current-source/effective distinctions and conditional installed-reference limits. | No profile or archived-original reopening; no universal current existence, parity, migration execution or target-equivalence assertion. |

No change to any listed surface is authorized by these tables. No tests, Make targets, build, install, settings change or live experiment was performed for this section.

## 9. Open Questions
These questions separate **unresolved policy decisions, unverified execution and evidence limitations**. They do not reopen established policy or erase source answers for the historical snapshot. Section 9.2 ends with a triage index that gives each question's type (policy decision, evidence needed or live Orca run needed) and the Section 7.5 approval conditions whose subject matches it.

R01-R08, W01-W04, GQ and `CORRECTION` resolve through Section 2.1 and the Evidence Trail. Research references include their complete original returns. G01-G54 and S01-S38 identify compiled gap and stale/interpretation families.

**Scope:** Suggested resolutions identify decisions or evidence needed, not implementation steps. Every live Orca/harness evaluation, message consumption, acknowledgment, failure injection, settings change, launch or shutdown requires separate authorization and is out of scope here. Proposed capabilities and unproved behavior remain **[UNVERIFIED]**; existing policy remains binding.

### 9.1 Established boundaries that are not open questions

| Reference | Established finding | Remaining boundary |
|---|---|---|
| **C1 - Guard scope** | R04 B1/B2, carried through R05/R07, establishes positively bound/literal-`orca` classification and required probes absent from exceptions. | No universal executable coverage or successful bypass proved. Launch, reporting and probe compatibility remain separate. |
| **C2 - Historical Orca mechanics** | R03 traced local helper selection of an active same-Run creator Dispatch, Run fallback, selected-mail handback, route-specific depth, independent Task authority and validated lineage for its original build. | “Active” describes source state selection, not a live experiment. Older slice-local unknowns do not erase that trace. `CORRECTION:36-47` prevents replacement-build transfer; exact-target and live evidence remain open. |
| **C3 - Incoming hook and mode classes** | W01 documents main-conversation `UserPromptSubmit` interception/blocking and class-based rather than exact-mode-name default delivery. | Installed coverage, authenticated origin, fail-closed handling and safe authorization remain open. https://code.claude.com/docs/en/hooks#userpromptsubmit ; https://code.claude.com/docs/en/cross-session-messaging#control-inbound-messages . |
| **C4 - Existing authority** | Worker fan-out prohibition, person-opened eligibility, explicit mode, human Rulings, ordinary PR carriage and Task-specific commit conditions are established by R01/R06. | Extension is a new decision, not uncertainty about whether current restrictions exist. |
| **C5 - Four depth baselines** | Policy one; historical researched source/stored one; dated replacement-source default/fallback two with guarded legacy migration; public default-four statements. | Historical stored one is not current profile evidence. Source two does not prove migration invocation/persistence, effective loaded maximum, running build, propagation, lowering or shutdown. `CORRECTION:18-51`; https://github.com/stablyai/orca/pull/38348 . |
| **C6 - Corrected numbers** | W02 controls: approximately two detected bugs per reviewed Devin-authored PR; approximately 58% of detected bugs severe; approximately eightfold usage growth in largest enterprises segment only, metric/baseline unspecified. | Operational observations, not hierarchy comparison or local forecast. https://cognition.com/blog/multi-agents-working . |
| **C7 - Approved inventory** | R07's later scope approval governs current-source/tests/distributed-copy inventory, not its older partial closing language. | Historical residual remains excluded and unverified; no renewed archival audit prerequisite. |

<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

### 9.2 Seventy-one individual questions

| # | Question | Impact | Suggested Resolution |
|---|---|---|---|
| **Q01** | What precise subordinate role would the ownership phrase denote, and how would an agent-launched nonworker qualify? R01/R08; G02/G51; W04. | Consistent PR #449 interpretation and topology choice. | Explicit eligibility, upper owner, planning, child ownership and reporting definition. Preserve A01/INF-027 as deferred defect, not permission. |
| **Q02** | What full upward contract would O4 have, and how would O2 peers divide work without controlling each other's Tasks? R01-R03/R05-R08; G19/G33/G51. | Ordinary launch/peer exchange as supervised assignment. | Written correlation, acknowledgments, results, admission, failure and closure ownership. Launch receipt is not completion. |
| **Q03** | Is entry point an Orca-calling coordinator command, external session role or internal-helper wrapper? R01/R07/R08; G35. | Command boundary, D1, eligibility and never-worker treatment, including root-only use. | Explicit architecture decision addressing broad command rule, narrow claim precedent and eligibility lists. |
| **Q04** | What does autonomous composite brief authorize: planning, counts, writes, questions and results? R01/R06/R08; G03. | D5 reconsideration and bounded O3. | Approved scope/limits/stops and completion/admission duties. Prewritten chain is not discretionary dispatch grant. |
| **Q05** | Is there a qualifying runtime-only split with measured material extra root round trip? R06; G10; W02/W04. | Demonstrated need/value. | Original Task, discovered split, why unforeseeable, follow-up Task and added-time record; retain bounded-not-found qualification. |
| **Q06** | Was D5 mailbox-clause omission deliberate or summarization loss? R06 §2; G11. | Unambiguous reconsideration conditions. | Authoritative textual disposition. Neither inferred waiver nor historical routing as live proof. |
| **Q07** | What is middle's own progress versus child activity, repeated mail or monitoring? R02; G04; W02. | Meaningful progress and supervision. | Attributable own/subtree semantics, including blocked/idle parent with active children. |
| **Q08** | How do success, usable partial, failure, blocked and dropped children reduce to aggregate outcome? R01/R02/R08; G04. | Aggregate completion/dependents/integration. | Recursive admission contract preserving child evidence, exclusions, uncertain effects and named owner. |
| **Q09** | Who handles mixed FIFO mail and batch versus application acknowledgments on both edges? R02/R03; G05; W02. | Lost instructions, premature ack and false child application. | One handling/ack owner per mailbox and mixed-batch acceptance evidence. Live consumption/ack out of scope. |
| **Q10** | Who services children during parent ask/block/fence/exhaustion/exit/replacement? R02/R03; G06. | Unattended descendants or overlapping supervisors. | Service/takeover policy preserving pending mail and explicit transfer. Live failure/replacement checks out of scope. |
| **Q11** | How are helpers, starts, attempts, restarts, probes, time and resources counted across lineage? R01/R02/R06; G07; W02/W04. | Bounded autonomy and multiplied allowances. | Persistent lineage budget separating depth, concurrency, retries and total use; no replacement reset. |
| **Q12** | Who may cancel/settle/release/clean subtree, and what proves quiescence/orphan disposition? R01/R02/R08; G07; W02/W04. | Safe recovery and destruction. | Named authority per operation, positive evidence and uncertain/preserved-child handling. Parent termination is not settlement. |
| **Q13** | How does freeze reach descendant writers and survive replacement? R01/R06/R08; G07/G34. | Safe resume/Git and halted evidence. | Explicit freeze/report-only scope, actual human handback and original worktree/plan/baseline preservation. |
| **Q14** | How does escalation reach the actual person through unattended middle? R01/R02/R06; G08; W02. | Human authority and bounded escalation. | Origin, receipt, deadline, owner and final human-visibility relay contract. |
| **Q15** | What commit/PR/outward/merge/removal authority could pass without widening human instruction? R01/R06/R08; G33/G34; W03. | Transitive consent/publication/cleanup claims. | Separate authority decision retaining Task provenance/expiry; parent role/token is not fresh instruction or Ruling. |
| **Q16** | Is compact handoff sufficient for roster, budgets, Deliveries, applied decisions, admissions and uncertain effects? R02; G09; W02. | Recovery without lost work/redo. | Supervisor-checkpoint sufficiency against all fields; retain omissions until evidenced. |
| **Q17** | Does exact-target native local topology work through start, ask/reply, mixed mail, completion, fence, early settlement and recovery? R03; G12; W02/W04; correction. | Operational O3 claim and historical-to-current transfer. | Target-build source applicability and separately authorized versioned lifecycle record. Historical route remains credited. Live run out of scope. |
| **Q18** | What are complete remote authority/depth/separate-Run reporting/recovery guarantees per host? R03; G13; W04. | Extending local findings or desktop limits remotely. | Host-specific source/guide, configuration owner and separately authorized end-to-end evidence. Live federation out of scope. |
| **Q19** | What is current stored and loaded maximum, backing storage, reload/profile/host propagation and running-build relationship? R03; G14; W04; correction. | Effective-scope and configuration claims. | Getter/storage/provenance trace and separately authorized observations if needed. Historical stored one/new source two are insufficient; no settings mutation here. |
| **Q20** | Is lowering safe with deeper workers/questions/unsettled effects? R03; G15. | Reversal/rollback claim. | Authorized record for existing/new helpers, questions, settlement and recovery. Live lowering out of scope. |
| **Q21** | What lies outside bounded public CLI/schema evidence about overrides/settings scope? R03; G16; W04. | Universal no-override/all-profile assertions. | Preserve bounded result; further authoritative interface/storage evidence only if material. No invented per-Run switch. |
| **Q22** | What caller identities, target route classifications and refusal receipts apply to evaluated sessions? R03; G17; correction. | Promoting historical classification into current source/refusal/success. | Exact-build/caller evidence and separately authorized receipts where needed; no live dispatch or alternate-launch probes. |
| **Q23** | Do historical/replacement installed builds and separately inspected development checkout match to the extent claimed? R02/R03; G20; correction. | Whole-build or replacement-route equivalence. | Revision/build provenance and bounded comparisons. Do not erase historical source answers or infer new equivalence from filename. |
| **Q24** | Which provider/adapter/permission/concurrency/background-child limits apply to installed harness? R03; G18; W01/W02/W04. | Unlimited-helper/public-default-local assertions. | Installed version/capability and adapter evidence; live harness evaluation out of scope. |
| **Q25** | How does default wait wake without explicit types? R02; G23. | Wait/detection assumptions. | Authoritative current behavior or separately authorized observation. No live consuming wait here. |
| **Q26** | Why were answers missed, and is non-application reliably detected? R02; G23. | Incident diagnosis/fix claim. | Separate delivery, wake, read, apply and ack evidence. Live reproduction out of scope. |
| **Q27** | Which attention categories and prompt/exhaustion detection delays apply? R02; G23. | Measured bounds and unknown versus evaluated-null. | Actual-build category/timing record. Live prompt/attention checks out of scope. |
| **Q28** | What happens to input during active tool? R02; G23. | Expanding idle-only typing boundary. | Separately authorized runtime evidence before reliance. No typing experiment here. |
| **Q29** | How do simultaneous consumers behave in running build? R02/R03; G05/G23. | Multi-consumer/replacement safety. | Explicit concurrency/generation acceptance. No live consume/ack experiment here. |
| **Q30** | How consistently are sweep/token/ack/chain/handoff/timing procedures followed? R01/R02/R05/R06/R08; G01. | Universal compliance/automatic-monitoring claims. | Scoped behavioral evidence, not phrase tests. Live workers out of scope. |
| **Q31** | Are all eight #431 incident families eliminated and bounds met? R02/R08; G25. | #434 merge as proven incident resolution. | Incident-specific acceptance and timing. Live reproduction/tests out of scope. |
| **Q32** | Which C10-C14 monitor/hook/dashboard/context/budget mechanisms shipped elsewhere? R02; G26. | Deterministic/durable automation claims. | Bounded delivery/deployment inventory; distinguish proposals, current procedures and stale documents. |
| **Q33** | What writes/persists lineage beyond inspected validation/projection? R03; G22. | Full storage/recovery claims. | Targeted persistence trace if material; retain historical host/instance validation. |
| **Q34** | What complete backend checks apply to report/artifact files? R02; G24. | Receipt/settlement as validation. | Complete trace before assigning guarantee; explicit supervisor reading/admission remains. |
| **Q35** | What trusted binding identifies role, parent, child scope and report destination? R01/R04/R07/R08; G27/G51/G52. | Scoped role authority. | Authority/binding evidence for launch, reports and probes separately, not names/unbound status/matcher mismatch. |
| **Q36** | What real Orca preamble/parent/session identity reaches hook and nested events? R04; G28; W01/W04. | U7 and fixture-to-runtime inference. | Actual envelope/provenance. Live event capture out of scope. |
| **Q37** | What resolves U28 Orca-hooks/L2 pre-push installation? R04; G29; W04. | Install capability assumed or conflated with U7. | Specific independent installation/runtime evidence. |
| **Q38** | How do whole-input rewrites, cwd and Linux job attribution behave concurrently? R04; G30. | Rewrite/process-identity reliability. | Ordering/context evidence with detach/daemon ceilings. No live job/rewrite experiment. |
| **Q39** | Is child governed before first consequential tool in its eventual environment? R04/R05; G31. | Claim preflight as child enforcement. | Claim-to-binding/first-tool acceptance record. No live claim launch here. |
| **Q40** | Which canonical/plugin/dev/package/global copies agree for exact deployment? R04/R05/R07/R08; G32. | Universal freshness/parity/success. | Bounded copy/provenance record; separately authorized execution if needed. No sync/build/install/test here; vanished bundle not current path. |
| **Q41** | Is ordinary session per named PR automatic and consistent? R05; G36. | Policy as launcher guarantee. | Implementation/placement evidence retaining D3. Live placement checks out of scope. |
| **Q42** | Do PM/agent/issue helpers meet roles/outputs/tiers, and is PM startup registered? R05; G37. | Instructions as execution/coordinator precedent. | Registration/resolution and bounded records. No live helper/model operation here. |
| **Q43** | Are watcher operation fields/errors/lost-reply assumptions valid for target API? R05; G38. | Deduplication/uncertain launch recovery. | Authoritative contract and authorized compatibility evidence. No live launch/lost-response experiment. |
| **Q44** | What actually constrains subprocess effects/isolation? R05; G39; W04. | Environment/bypass/depth as sandbox. | Explicit containment and threat model before authority inference. |
| **Q45** | How is native sender permission class represented/verified? R08; G40; W01. | Full answer to #339 question 1. | Authoritative protocol/interface; no invented per-send field or text identity. |
| **Q46** | What historical sender/receiver modes/settings caused reported hold? W01; G40. | Proven incident cause/configuration. | Historical receipts/configuration or retain unreproduced. Reproduction out of scope. |
| **Q47** | Which messaging/hook features apply across installed active/idle/remote/nested paths? W01/W02; G40. | Deployed support/universal interception. | Version/route evidence; documented main hook remains yes. No live message/event test. |
| **Q48** | What authenticated sender/parent metadata and genuine per-parent acceptance exist? W01/W03; G27/G40/G42. | Narrow parent trust. | Trusted presentation contract; receiver fields/text are not authenticated sender. |
| **Q49** | Does incoming validation fail closed on timeout/error/order failures? W01; G40. | Dependable security boundary. | Installed mechanism/failure/order evidence. No live fault injection. |
| **Q50** | Does actual envelope separate peer text from human plan approval/Rulings? W01; G08/G34/G40. | Consent laundering prevention. | Approval-parser/origin evidence. No exploit established; live security evaluation out of scope. |
| **Q51** | What complete typed/file protocol enforces identity, scope, freshness, inert text, acks and admission? R08; G41; W01/W03. | Schema/text/path as authority or success. | Trusted producer/validator contract with deliberate mapping to transport semantics. |
| **Q52** | What request/action/attenuation policy avoids transferring human-only authority? R08; G34/G42; W03. | Grant layer/downward authority. | Policy separates requests, effects, issuer/verifier, resources/actions and destructive preconditions. |
| **Q53** | What are Dispatch capability semantics, attenuation/lifecycle and suitability? R08; G43; W03. | Reuse versus new credentials. | Complete target-appropriate trace before absent/equivalent/insufficient claims. |
| **Q54** | Where is trusted authorization enforced before every relevant effect? R04; G42/G52; W03/W04. | Non-bypassable/token security claims. | Effect/enforcement map and threat model; integrity is not interception/context/authorization. |
| **Q55** | How is one-use atomic across receivers/retries/duplicates? W03; G42. | Replay prevention. | Consumption/idempotency/failure contract. Nonce is not ledger. |
| **Q56** | What clock/expiry/key/discharge/attestation/revocation/freshness/outage policy applies? W03; G42. | Credential life after offline use/cancel. | Separate chain check, fresh proof acquisition, new revocation knowledge and broader original credentials. |
| **Q57** | Which maintained compatible Python/Node implementation/features and separate adversarial result fit? R08; G42; W03. | #339 question 3/dependency choice. | Supported versions/security/features including third-party support and separately authorized comparison. Preference not winner. |
| **Q58** | What workload/outcomes validate 10-20-session target? R08; G44; W02. | Capacity/scalability. | Local supervision/outcome evidence, not vendor or synthetic dashboard numbers. |
| **Q59** | How do registry/routing cover ordinary/later sessions and multiple owners? R08; G44. | Permanent all-session role. | Eligibility/ownership/exception contract. Dispatch identity not universal registry. |
| **Q60** | What is historical-session/six-hour sweep versus live worker loop? R08; G44. | Proposed interface as existing liveness. | Separate inventory and ongoing-supervision acceptance. |
| **Q61** | How remain attention visible until satisfied and periodic reporting accurate? R08; G44. | Persistent attention/static report. | Display/closure/cadence and style disposition. Ack not resolution. |
| **Q62** | What server/endpoint/data-versus-control boundary is intended? R08; G44. | Management relay/integration ownership. | Identified service and authority contract. |
| **Q63** | What proves pushes, admission, evidence retention and session closure before deletion? R08; G44; W01/W03/W04. | Safe cleanup. | Explicit predicates/checker retaining human, merge, freeze, unread-report and ledger protection. Idle/signature insufficient. |
| **Q64** | How are absolute automation/disposal/placement/style/fan-out conflicts dispositioned? R08; G50. | Consistent product/hierarchy criteria. | Explicit policy/requirement decisions; no silent role-based exception. |
| **Q65** | How distinguish release ownership/numbers for supervision, #423 knowledge and hierarchy/security? R08; G45. | Administrative acceptance/release claims. | Record allocation; semantic distinction already established. |
| **Q66** | What actual remote version/schema/tests/live contract backs #409? R08; G46. | Observer proposal/synthetic data as deployed API/controller/capacity. | Separately scoped source/provenance evidence, preserving observer-only boundary. |
| **Q67** | What proves #446 experiments and remaining #326 Git/submodule/commit work? R08; G47. | Independent follow-ups as shipped/new authority. | Issue-specific acceptance; preserve lock/freeze/ownership and separate hierarchy. |
| **Q68** | Where is P2 live acceptance beyond static merge? R06/R08; G48. | Live rollout/later readiness. | Applicable acceptance record or bounded-not-found qualification. |
| **Q69** | What local comparison/threat evidence establishes benefit/security/recovery beyond external mechanisms? G49; W02/W03/W04. | Speed/cost/reliability/trustless or measured delivery promises. | Local comparison and threat model using correct populations/denominators. Vendor adoption/CaMeL utility not local proof. |
| **Q70** | What has the source-defined migration actually done, and what would future upgrade do per profile/host? W04; correction. | Intentional old one retained, migration executed or public four active claims. | Authorized version/profile/host evidence separating definition, invocation, persistence and loading. No profile reopening, upgrade or setting mutation here. |
| **Q71** | Which descendant-stop/preserve/uncertain/interrupted-start/detached-process behavior applies to exact build? W04; G06/G07; correction. | Public stop as complete local termination. | Build-specific source and authorized recovery/shutdown acceptance. No live stop/cleanup here. |

**Triage index for Q01-Q71.** Of the 71 questions, 21 need a live Orca run, 24 are policy decisions and 26 need evidence. "Live Orca run needed" copies the "Needs a live Orca run = yes" flag of the gap rows (G-numbers) the question cites in `gaps-and-questions.md`. "Policy decision" and "evidence needed" are read from each remaining row's own Suggested Resolution wording, because the gaps file carries no such type. A "yes" flag does not authorize a run: every live run stays out of scope under the Section 9 scope paragraph. The report links no question to a condition by number, so the last column lists only conditions whose Section 7.5 subject matches the question's subject. "None" means no clear subject match was found; it is not a statement that no Section 7.5 condition applies to that question.

| Question(s) | Type (flag from the cited gap rows) | Section 7.5 condition(s) with a matching subject |
|---|---|---|
| Q01-Q04 | Policy decision (G02, G19, G33, G35, G03, G51: no) | Q01 DG-03, DG-04; Q02 DG-08, DG-10, DG-11; Q03 DG-05; Q04 DG-02, DG-04 |
| Q05 | Evidence needed (G10: no) | DG-01 |
| Q06-Q08 | Policy decision (G11, G04: no) | Q06 DG-25; Q07 and Q08 DG-11 |
| Q09-Q10 | Live Orca run needed (G05, G06: yes) | Q09 DG-09, DG-10; Q10 DG-12 |
| Q11-Q16 | Policy decision (G07, G08, G09, G33, G34: no) | Q11 DG-13; Q12 DG-13, DG-23; Q13 DG-23; Q14 DG-15; Q15 DG-16; Q16 DG-14 |
| Q17-Q20 | Live Orca run needed (G12, G13, G14, G15: yes) | Q17 and Q18 DG-08; Q19 and Q20 DG-07 |
| Q21 | Evidence needed (G16: no) | None |
| Q22 | Live Orca run needed (G17: yes) | DG-06 |
| Q23-Q24 | Evidence needed (G20, G18: no) | Q23 DG-06, DG-08; Q24 none |
| Q25-Q31 | Live Orca run needed (G23, G05, G01, G25: yes) | Q29 DG-09; the others none |
| Q32-Q35 | Evidence needed (G26, G22, G24, G27, G51, G52: no) | Q35 DG-17; the others none |
| Q36 | Live Orca run needed (G28: yes) | None |
| Q37 | Evidence needed (G29: no) | None |
| Q38-Q39 | Live Orca run needed (G30, G31: yes) | None |
| Q40 | Evidence needed (G32: no) | DG-24 |
| Q41-Q43 | Live Orca run needed (G36, G37, G38: yes) | None |
| Q44-Q47 | Evidence needed (G39, G40: no) | Q45 and Q46 DG-20; Q44 and Q47 none |
| Q48 | Policy decision (G27, G40, G42: no) | DG-17 |
| Q49-Q50 | Evidence needed (G40, G08, G34: no) | Q49 DG-19; Q50 DG-15, DG-19 |
| Q51-Q52 | Policy decision (G41, G34, G42: no) | Q51 DG-18; Q52 DG-16 |
| Q53-Q54 | Evidence needed (G43, G42, G52: no) | Q53 DG-16; Q54 DG-22 |
| Q55-Q56 | Policy decision (G42: no) | DG-21 |
| Q57-Q58 | Evidence needed (G42, G44: no) | Q57 DG-21; Q58 none |
| Q59 | Policy decision (G44: no) | None |
| Q60 | Evidence needed (G44: no) | None |
| Q61-Q65 | Policy decision (G44, G50, G45: no) | Q63 DG-23; Q65 DG-25; Q61, Q62 and Q64 none |
| Q66-Q70 | Evidence needed (G46, G47, G48, G49: no; Q70 cites no gap row) | Q70 DG-07; the others none |
| Q71 | Live Orca run needed (G06: yes) | None |

### 9.3 Seven evidence limitations, not new product prerequisites

| Reference | Limitation and disposition | Source |
|---|---|---|
| **B01 - Historical P0** | Raw transcripts not independently replayed; documentary compliance is not attempted-refusal proof. AC-0.7 acceptance, R03's historical trace, dated new source and live nesting remain separate. | G21; R03 §6; R06 acceptance records; correction. |
| **B02 - Archival residual** | 867 unread matching lines across 274 paths remain excluded/unclassified background. Not incomplete approved active inventory or demand for new archive audit. | G53; R07 approval/ledger/two supplements. |
| **B03 - Notebook** | Moved stub/partial extraction does not establish unseen supervisor/context-adapter internals. Retain inspected architectural context only. | W02 original gap 14. |
| **B04 - Macaroon PDF** | Full body not readable. Preserve abstract/indexed passages/readable implementation boundary, not complete-paper claim. | W03 original gap 7. |
| **B05 - Source 404** | Unknown reason for inaccessible public implementation; no privacy, absence or content inference. | W04 original gap 13. |
| **B06 - Why exactly four** | Finite-ceiling rationale does not explain exact public value. Not basis for local limit or prerequisite to retain policy. | W04 original gap 6. |
| **B07 - Estimates/unrun checks** | Issue estimates, old test counts and inspected tests/sync/package/install are not new execution or readiness. Original existence checks retain time/scope; vanished historical bundle excluded from current existence. | R05/R07/R08; G32/G44/G47/G48; correction. |

### 9.4 All 38 stale/interpretation families dispositioned

These preserve the meanings already presented in Section 4 without falsely reopening their answered portions.

| Family | Disposition | Residual destination |
|---|---|---|
| S01 | Final scoped session-layer proposal, not original command-owned alternative. | Q03/Q04/Q15. |
| S02 | Higher valid finite maximum is not fence removal. | Q19-Q22. |
| S03 | “Spec not edited” is drafting history. | No missing application status; Q06 is actual discrepancy. |
| S04 | “None applied” is historical broader status. | Applied policy retained; Q06 separate. |
| S05 | D1-D5/Git decisions exist and are authoritative. | Future delegation Q15. |
| S06 | Person-opened eligibility is explicit. | New role Q01/Q04. |
| S07 | Worker-session ban is explicit. | New exception Q01/Q04. |
| S08 | Placement/isolation applied; CR-01 status historical. | Future cleanup/ownership Q12/Q63. |
| S09 | Composite brief/material runtime split replaces smoke trigger. | Q04/Q05. |
| S10 | Fixed chains exist, not autonomous dispatch authority. | Q04. |
| S11 | Old specification pointers historical, not current locations. | Citation limit, not new architecture question. |
| S12 | Current authorized setup-skip default governs older setup-run. | No setup authorized; extension Q15. |
| S13 | Current eligibility inventory includes issue exclusion. | Actual new entry point Q03. |
| S14 | Ordinary top-level PR policy supersedes worker/opt-in proposal. | Behavior Q41, not policy status. |
| S15 | Fork-only/upstream-link restrictions qualify old linking guidance. | No linking permission added. |
| S16 | Historical depth is Dispatch-specific; Task authority separate. | Exact-target/receipt Q22. |
| S17 | Historical creator route corrects universal root prediction. | Exact-target/live Q17/Q23; remote Q18. |
| S18 | Historical Task path lacks depth check. | Retain answer; target applicability Q22/Q23. |
| S19 | Independent coordinator check makes only-prose account overbroad. | Target applicability Q22/Q23, not worker permission. |
| S20 | Validated host/instance ancestry is real, not lifecycle grant. | Backing persistence Q33. |
| S21 | Historical blanket help omits creator exception. | Historical discrepancy retained; target/live Q17/Q23. |
| S22 | Historical bundles/offsets stay historical; R03 itself predates replacement correction. | B01/Q17/Q22/Q23; no filename substitution. |
| S23 | Current liveness includes later chains/handoff/acks/S11. | Compliance/outcomes/delivery Q30-Q32. |
| S24 | C-rule map pointers drifted. | Citation qualification only. |
| S25 | Lock pointer drift not implementation of bounded wait. | Independent Q67. |
| S26 | Later P1 acceptance governs old FAIL; actual Skill still required. | No false final-status question. |
| S27 | Populated 31 headings, not current empty set or live successes. | Q40/Q68/B07. |
| S28 | Watcher WC-13 pointer drifted. | Citation qualification only. |
| S29 | Research observed static #422 merge, not current open state. | Live Q68; no fresh remote claim. |
| S30 | Current procedures postdate old #339 baseline. | Incident/automation Q31/Q32. |
| S31 | Narrow coordinator claim code qualifies universal no-Orca description. | Architecture Q03. |
| S32 | Intentional two-stage claim qualifies atomic launch wording, not worker ban. | First-tool governance Q39; packaging Q03. |
| S33 | Decomposition-only stop controls spawn precedent. | No invented launcher; role Q01-Q04. |
| S34 | Skill/helper labels do not prove layered Orca supervision. | Q01/Q02/Q35. |
| S35 | Missing preamble does not promote launched nonworker. | Q01/Q02. |
| S36 | B1/B2 corrections control old categorical guard claims. | Q35/Q54; no bypass/expansion. |
| S37 | Nine supported messages, not all settlement types; depth before commit/rollback, not necessarily before transaction entry. | Precision only; historical implementation scope retained. |
| S38 | Later approved active inventory scope controls old partial status. | B02, no repeat archive audit. |

### 9.5 All 54 compiled gap families mapped by meaning

| Family | Meaning retained | Destination |
|---|---|---|
| G01 | Actual compliance with existing procedures. | Q30. |
| G02 | Subordinate-role conflict/eligibility. | Q01/Q02. |
| G03 | Autonomous composite authority. | Q04. |
| G04 | Own/subtree progress and aggregate outcomes. | Q07/Q08. |
| G05 | Mixed mail, receipt/application and concurrency. | Q09/Q29. |
| G06 | Parent transition and child recovery/stop behavior. | Q10/Q17/Q71. |
| G07 | Lineage budgets, cancellation, freeze and quiescence policy. | Q11/Q12/Q13. |
| G08 | Actual-human escalation and approval origin. | Q14/Q50. |
| G09 | Complete supervisor checkpoint. | Q16. |
| G10 | Qualifying measured runtime-only split. | Q05. |
| G11 | Mailbox-clause record intent. | Q06. |
| G12 | Exact-target local lifecycle beyond historical source support. | Q17/C2. |
| G13 | Remote/federated per-host scope. | Q18. |
| G14 | Current stored/loaded setting and propagation. | Q19/Q21/C5. |
| G15 | Safe lowering with existing descendants. | Q20. |
| G16 | Bounded override/schema/settings-scope absence. | Q21. |
| G17 | Route identity/refusal and exact-target applicability. | Q22/C2. |
| G18 | Installed provider/helper limits. | Q24. |
| G19 | Ordinary-owner upward relationship. | Q02. |
| G20 | Development/historical/replacement equivalence. | Q23. |
| G21 | Historical documentary versus attempted-refusal proof. | B01. |
| G22 | Lineage storage writer/persistence. | Q33. |
| G23 | Wake, missed answers, attention, active input, concurrent consumers. | Q25-Q29. |
| G24 | Full backend report/artifact validation. | Q34. |
| G25 | Eight incident outcomes and measured bounds. | Q31. |
| G26 | C10-C14 actual delivery elsewhere. | Q32. |
| G27 | Trusted role/parent/scope binding. | Q35/Q48. |
| G28 | Actual hook/subagent envelope identity. | Q36. |
| G29 | U28 installation independent of U7. | Q37. |
| G30 | Rewrite/cwd/job behavior. | Q38. |
| G31 | Child first-tool governance. | Q39. |
| G32 | Copy/deployment provenance and unrun procedures. | Q40/B07. |
| G33 | Current authority answered; future ordinary-owner/delegation choice. | C4; Q02/Q15. |
| G34 | Freeze/non-transferable human grants and future grant policy. | Q13/Q15/Q52. |
| G35 | Command/session/role selector architecture. | Q03. |
| G36 | Actual ordinary PR placement. | Q41. |
| G37 | Helper role/tier/output and PM registration. | Q42. |
| G38 | Watcher API and uncertain launch receipts. | Q43. |
| G39 | Subprocess containment, not assumed sandbox. | Q44. |
| G40 | Hook/classes documented; sender/history/deployment/origin/failure still open. | C3; Q45-Q50. |
| G41 | Complete typed/validated-file application protocol. | Q51. |
| G42 | Grants, effect authorization, replay, freshness and library selection. | Q52/Q54-Q57. |
| G43 | Existing capability reuse/suitability. | Q53. |
| G44 | Capacity, registry, sweeps, attention, server, closure and estimates. | Q58-Q63/Q69/B07. |
| G45 | Release allocation/naming, not semantic confusion. | Q65. |
| G46 | Observer implementation/provenance, not control. | Q66. |
| G47 | Independent lock/Git/submodule evidence. | Q67. |
| G48 | P2 live versus static acceptance. | Q68. |
| G49 | Local benefit/security limits and bounded literature evidence. | Q57/Q69/C6/B03/B04. |
| G50 | Absolute automation/disposal/placement/style/fan-out conflicts. | Q64. |
| G51 | Role wording, owner protocol and trusted recognition. | Q01/Q02/Q35. |
| G52 | Resolved research overstatement versus remaining launch/report/probe/enforcement defects. | C1/Q35/Q54. |
| G53 | Excluded unread archival evidence. | B02. |
| G54 | Message vocabulary and transaction precision. | C2/S37; not new capability. |

### 9.6 All 53 external gap groups mapped by meaning

The group numbers identify rows in each web report's **original Gaps and Questions table**, in order. They are coverage references, not additional researcher-authored finding IDs.

#### W01 - Twelve messaging gap groups

| Group | Meaning and disposition | Destination |
|---|---|---|
| 1 | Sender-class representation/verification remains unresolved. | Q45. |
| 2 | Historical sender/receiver configuration not observed. | Q46. |
| 3 | Installed feature/version equivalence not established. | Q47. |
| 4 | Receiving-route coverage is not universal from documentation. | Q47. |
| 5 | Authenticated sender metadata not supplied by receiving fields. | Q48. |
| 6 | Genuine per-parent trust differs from broad acceptance. | Q48. |
| 7 | Fail-closed install, timeout and ordering remain unverified. | Q49. |
| 8 | Peer origin must not become human approval. | Q50. |
| 9 | Exact-name equality corrected to documented classes. | C3. |
| 10 | Blanket executable/read claims corrected; actual defects retained. | C1. |
| 11 | Typed messages, grants and files need complete trusted protocol. | Q51-Q57. |
| 12 | Hierarchy needs explicit role, service, result and recovery contract. | Q01-Q16. |

#### W02 - Fifteen hierarchy gap groups

| Group | Meaning and disposition | Destination |
|---|---|---|
| 1 | Qualifying local saving not measured. | Q05/Q69. |
| 2 | Autonomous composite brief not defined. | Q04. |
| 3 | Own/child progress not composed. | Q07. |
| 4 | Aggregate success/admission not defined. | Q08. |
| 5 | Blocked/fenced/replaced parent needs child-service owner. | Q10. |
| 6 | Cancellation/restart/quiescence and total budgets need policy. | Q11/Q12. |
| 7 | Mixed mail/application acknowledgments need ownership and evidence. | Q09/Q29. |
| 8 | Compact checkpoint sufficiency unresolved. | Q16. |
| 9 | Escalation must reach actual person. | Q14. |
| 10 | Bound-session probe compatibility distinct from launch/report. | C1/Q35. |
| 11 | Universal root routing corrected for historical local source. | C2. |
| 12 | Exact installed/live/replacement recovery not certified. | Q17/Q23. |
| 13 | Published provider nesting does not establish local applicability. | Q24/Q47. |
| 14 | Unseen historical notebook internals excluded. | B03. |
| 15 | No general hierarchy superiority, validated capacity or incident elimination. | Q31/Q58/Q69. |

#### W03 - Twelve grant gap groups

| Group | Meaning and disposition | Destination |
|---|---|---|
| 1 | Trusted session/request binding not self-assertion. | Q48/Q52. |
| 2 | Complete pre-effect enforcement distinct from token integrity. | Q54. |
| 3 | Concurrent one-use requires atomic state. | Q55. |
| 4 | Revocation needs freshness/outage policy. | Q56. |
| 5 | Existing capability suitability not traced fully. | Q53. |
| 6 | Library maintenance/features/compatibility uncertain. | Q57. |
| 7 | Full original-paper extraction not claimed. | B04. |
| 8 | Token feasibility does not authorize hierarchy. | C4. |
| 9 | Blanket hook/executable/probe statements corrected. | C1. |
| 10 | Prompt-free delivery is not unconditional; documented controls separated from deployment. | C3/Q47. |
| 11 | Human authority does not become transitive. | Q15/Q52. |
| 12 | Separate adversarial selection not completed. | Q57. |

#### W04 - Fourteen Orca gap groups

| Group | Meaning and disposition | Destination |
|---|---|---|
| 1 | Effective loaded limit unverified. | Q19. |
| 2 | Public default not local effective observation; dated source two also bounded. | C5. |
| 3 | Historical local route not live/exact-target acceptance. | Q17. |
| 4 | Historical root prediction corrected without build transfer. | C2. |
| 5 | Public role words not full authority/report/recovery contract. | Q01. |
| 6 | Exact-four rationale unknown, not local prerequisite. | B06. |
| 7 | Local quantified benefit not established. | Q05/Q69. |
| 8 | Actual/future migration effects need profile/host evidence. | Q70. |
| 9 | Remote setting/per-Run override not inferred from closure. | Q18/Q21. |
| 10 | New public shutdown not backported guarantee. | Q71. |
| 11 | Depth does not provide budget, containment or effect authorization. | Q11/Q44/Q54. |
| 12 | Agent limits, hook identity/install and copies remain distinct. | Q24/Q36/Q37/Q40. |
| 13 | Inaccessible source does not prove privacy/absence. | B05. |
| 14 | Product helpers do not amend worker permission. | C4. |

### 9.7 Carry-forward and scope

For #339, question 1 remains partly open at Q45, with historical/deployed evidence separated at Q46-Q49. Question 2 is **documented yes** at C3; remaining uncertainty is deployment, trusted origin and adequacy. Question 3 remains Q57. V1, reporting, cleanup, security and hierarchy requirements remain represented at Q01-Q16 and Q51-Q65, not silently delivered.

The controlling correction narrows current claims without erasing historical facts or adding a new product prerequisite: no current stored/effective/running-build/migration-execution or replacement-equivalence assertion follows from the bounded source observation. Original archives remain unopened; all suggested live resolutions still require separate authorization.

## 10. Evidence Trail
All task-relative paths below resolve beneath:

`/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/`

The inventory was checked with Glob during assembly. The assembler read all six synthesis indexes and all six complete synthesis returns, including synthesis 02's four nested replacement values, plus the controlling snapshot correction. Underlying research documents and original-source reads remain attributable to their producing investigations; this assembly does not claim to have repeated them.

### 10.1 Evidence inventory and interpretation

| Evidence class | Files | Interpretation |
|---|---:|---|
| Numbered codebase investigations | 8 | Substantive codebase research, with assignment roles distinguished from registered agent type. |
| Web investigations | 4 | External context with source, reliability, extraction and version limits. |
| Scope discovery | 4 | Initial hypotheses/discovery; later substantive research and corrections control. |
| Research notes | 1 | Scope and assignment/planning record. |
| Complete primary research returns | 12 | Eight codebase and four web originals; immutable provenance, subject to explicit later corrections. |
| Archival supplements | 2 | Original inventory accounting, not certification that excluded originals were read. |
| Inventory captures | 4 | Discovery/accounting evidence, not new runtime observations. |
| Synthesis indexes | 6 | Section mapping and substantive indexes. |
| Complete synthesis returns | 6 | Mandatory full assembly components, not optional background. |
| Controlling synthesis snapshot correction | 1 | Supersedes stale current-installation assertions in every synthesis representation. |
| Gaps log | 1 | Compiled 54 gap and 38 stale/interpretation families. |
| **Total listed research/scope/synthesis evidence artifacts** | **49** | Excludes task instructions, procedural QA records and assembled deliverables. |
| Standalone research fix-addendum Markdown files | 0 | No matching file appeared in the research inventory; embedded corrections and the actual synthesis correction below are listed explicitly. |

The header's **8 codebase + 4 web** count refers to substantive investigations, not all supporting artifacts. No research or returned original is discarded by assembly.

### 10.2 Codebase research

The registered agent type for these eight investigations was **rf-task-researcher**. Architecture/tracing/integration/pattern/document labels describe assignment roles, not eight different registered agent types.

| File | Topic | Agent type / assignment |
|---|---|---|
| `research/01-contract-authority-model.md` | R01: roles, command/session boundaries, complete compatibility matrices and authority allocation. | rf-task-researcher; architecture assignment. |
| `research/02-liveness-and-reporting-stack.md` | R02: signals, states, acknowledgments, intervention limits, admission and two-edge supervision. | rf-task-researcher; code-tracing assignment. |
| `research/03-orca-mechanics.md` | R03: historically inspected depth, routing, parentages, Task authority, ordinary launch and settings boundaries. | rf-task-researcher; integration assignment. |
| `research/04-hooks-guards-identity.md` | R04: hook inputs/bindings, recognition/probe ceilings, registration and live identity limits; embedded B1/B2 correction. | rf-task-researcher; integration assignment. |
| `research/05-precedents-session-launchers.md` | R05: fourteen launcher precedents, 56 reuse judgments and dependent guard correction. | rf-task-researcher; pattern assignment. |
| `research/06-decision-history-and-trigger-evidence.md` | R06: D1-D5, separate recommendation/applied records, trigger search and historical acceptance. | rf-task-researcher; document-analysis assignment. |
| `research/07-blast-radius-per-option.md` | R07: approved active-source/test/copy inventory, six option surfaces, test pins, distribution and archival accounting. | rf-task-researcher; architecture assignment. |
| `research/08-orchestrator-issues-requirements.md` | R08: all 35 requirements, issue/PR scope, conflicts, release distinctions and capability forwarding. | rf-task-researcher; document-analysis assignment. |

### 10.3 Web research

| File | Topic |
|---|---|
| `research/web-01-claude-code-cross-session-messaging.md` | W01: permission classes, holds/refusal/delivery, inbound hooks, channel guarantees, origin and deployed-enforcement limits. |
| `research/web-02-hierarchical-orchestration-patterns.md` | W02: flat/hierarchical mechanisms, context/cost/failure tradeoffs, numerical baselines and controlling Cognition correction. |
| `research/web-03-capability-narrowing-tokens.md` | W03: macaroons, Biscuit, CaMeL, trusted authorization, replay/revocation and library-selection limits. |
| `research/web-04-orca-nested-depth-helpers.md` | W04: public depth/helper history, migration, version/host distinctions, role terminology and shutdown qualifications. |

External findings remain supplementary. Their original WebSearch fallback provenance is preserved beside findings and source-qualified tables in Section 5; no new web search or fetch was performed during assembly.

### 10.4 Scope discovery and research notes

| File | Evidence role |
|---|---|
| `research/scope/scope-01-contract-and-rules.md` | Initial contract, ownership and rule/test discovery; later research controls. |
| `research/scope/scope-02-decision-history-d5.md` | Initial D5/placement/P0 history and mechanics questions. |
| `research/scope/scope-03-enforcement-surface.md` | Initial hook, test, depth and helper discovery, subsequently refined. |
| `research/scope/scope-04-issues-prs-and-prior-analysis.md` | Initial fork issue/PR and prior-analysis discovery, including deliberate WC-13 deferral. |
| `research/research-notes.md` | Scope, existing-file register, six options, decision-only boundary and synthesis assignments. |

Scope files do not record a distinct agent type in their contents. Their presence does not override approved policy, later code tracing or controlling corrections.

### 10.5 Complete primary returned research

| File | Required evidence content and qualification |
|---|---|
| `research/returned/01-returned-findings.json` | Complete authority/rule-by-option and coordinator-duty matrices, gaps and stale-source register. |
| `research/returned/02-returned-findings.json` | Complete signal/state/response/acknowledgment/C-rule tables and original gaps. |
| `research/returned/03-returned-findings.json` | Complete historical installed trace, route classifications, creator routing and source/live reconciliation. Not replacement-build certification. |
| `research/returned/04-returned-findings.json` | Original hook investigation; categorical executable/read claims are governed by embedded B1/B2 correction. |
| `research/returned/05-returned-findings.json` | Fourteen launchers and 56 reuse assessments; dependent guard correction controls superseded assertions. |
| `research/returned/06-returned-findings.json` | Separate D5 texts, trigger search, phase-evidence distinctions and historical discrepancy register. |
| `research/returned/07-returned-findings.json` | Original six-option file/test/copy/distribution inventory; later approved scope and corrections govern. |
| `research/returned/08-returned-findings.json` | Issue quotations, all 35 dispositions, conflicts, bounded negatives and original gaps. |
| `research/returned/web-01-returned-findings.json` | Complete messaging/hook/channel findings, URLs and 12 original external gap groups. |
| `research/returned/web-02-returned-findings.json` | Seventeen findings, numerical baselines, five-cost reassessment and 15 external gap groups. Superseded Cognition wording is provenance only. |
| `research/returned/web-03-returned-findings.json` | Mechanism/library comparisons, extraction limits, sources and 12 external gap groups. |
| `research/returned/web-04-returned-findings.json` | Local/public version register, migration/shutdown, negative-search limits and 14 external gap groups. |

Returned text is not interchangeable with an index. Original observations are retained without treating superseded portions as controlling current evidence.

### 10.6 Archival supplements and inventory captures

| File | Evidence role |
|---|---|
| `research/returned/07-archival-supplement-1.json` | Original inspected archival sets, duplicate qualifications and remaining boundary; earlier partial status retained historically. |
| `research/returned/07-archival-supplement-2.json` | Frozen reconciliation and exact-residual reference; unread originals remain unverified. |
| `research/returned/inventory-captures/call_25d4f84924964fde84384a6c1dd3686c.txt` | Preserved path/line/term discovery capture. |
| `research/returned/inventory-captures/call_70b584e0ac584c3198ea0273159a402f.txt` | Frozen file-discovery list. |
| `research/returned/inventory-captures/call_19d64d1d820348199f8ed311879166ee.txt` | Per-file matching-line counts. |
| `research/returned/inventory-captures/bw1hpg0xz.txt` | Exact excluded unread residual and reconciliation output. |

The upstream synthesis records reading the supplements and inspecting capture accounting, not a fresh complete read of every capture or matched original. Assembly confirms the listed paths, not those original contents. **867 unread matching archival lines across 274 paths remain excluded background** under approved R07 scope.

### 10.7 Six synthesis pairs

All six indexes and all six full returns were read for this assembly.

| Synthesis index | Mandatory complete companion | Report contribution |
|---|---|---|
| `synthesis/synth-01-problem-current-state.md` | `synthesis/returned/synth-01-returned-sections.json` | Sections 1-2: problem, source register, current instructions, historical mechanics, liveness, launchers, decisions, issues and limits. |
| `synthesis/synth-02-target-gaps.md` | `synthesis/returned/synth-02-returned-sections.json` | Sections 3-4: desired behavior, 16 criteria, 15 constraints, 34 adoption gaps, 38 stale families and semantic coverage. Its outer text contains structured JSON with four complete replacement values; selector keys are not deliverable placeholders. |
| `synthesis/synth-03-external-findings.md` | `synthesis/returned/synth-03-returned-sections.json` | Section 5: 46 findings, metadata/URLs, hook/channel distinctions, numbers, tradeoffs and option mapping. |
| `synthesis/synth-04-options-recommendation.md` | `synthesis/returned/synth-04-returned-sections.json` | Sections 6-7: six assessments, nine-criterion comparison, compatibility meanings, 35 requirements, O6 recommendation and 25 approval conditions. |
| `synthesis/synth-05-change-surface.md` | `synthesis/returned/synth-05-returned-sections.json` | Section 8: exact decision-only N/A statement, six conditional surfaces, eight test pins and distribution relationships. |
| `synthesis/synth-06-questions-evidence.md` | `synthesis/returned/synth-06-returned-sections.json` | Sections 9-10: 71 questions, seven established boundaries, seven evidence limits, 54/38/53 coverage meanings and evidence inventory. |

Delivery preambles, persistence instructions and DONE/NEXT wrappers from original returns are excluded from substantive report content. Findings and evidence qualifications are retained.

### 10.8 Controlling corrections, scope precedence and gaps log

| File | Controlling content |
|---|---|
| `research/04-hooks-guards-identity.md` | Embedded B1/B2: literal-executable ceiling and required-but-unlisted probes. |
| `research/05-precedents-session-launchers.md` | Embedded B1/B2 dependency qualification for launcher/option conclusions. |
| `research/07-blast-radius-per-option.md` | Approved current-source/tests/copy scope, archival ledger and dependent B1/B2 correction. |
| `research/web-02-hierarchical-orchestration-patterns.md` | Controlling numerical correction: detected-bug severity denominator, largest-enterprise growth population and measurement limits. |
| `synthesis/EVIDENCE-SNAPSHOT-CORRECTION.md` | Controls stale current-default/build/stored/existing-path assertions in all six indexes and full originals, including nested synthesis 02. Separates policy one, historical one, dated source two and public four. |
| `gaps-and-questions.md` | All 54 compiled gap and 38 stale/interpretation families, with source/live and approved-scope distinctions. Section 9 additionally dispositions all 53 original external gap groups. |

The snapshot correction preserves historical traces and filenames, records the old bundle's absence and limits the located replacement to observed existence. It does not certify running build, current profile, effective maximum, migration execution/persistence, route equivalence, live operation or safe shutdown.

### 10.9 Procedural references and verification boundary

These records establish task requirements, gate history or presentation qualifications. They are **not additional research investigations** and are excluded from the 49-artifact inventory above.

| Record | Role |
|---|---|
| `TASK-RESEARCH-sub-orchestrator-mode-20261108-181115.md`, Step 6.1 at line 373 | Assembly template, ten sections, decision-only Section 8 and consistency-note requirements. |
| `/home/coder/.claude/skills/tech-research/SKILL.md` | Installed Report Structure, Assembly Process and Content Rules, applied with the task-specific decision-only adaptation. |
| `qa/qa-gate-phase5-final-verdict.md` | Encoded synthesis-gate history, separate from executor boundary and final report acceptance. |
| `qa/phase5-boundary-final-verdict.md` | Separate synthesis-boundary disposition accepting the controlling snapshot correction for assembly input. |
| `qa/qa-consolidated-findings-phase5.md` | Minor presentation notes: provenance pointers, table pipes, typography, citations and readable wording. |
| `qa/phase4-boundary-numbers.md` | Exact numerical qualification pointers carried into Section 5, including numbers4-04/05/10/11. |
| `qa/phase4-boundary-provenance.md` | Fact-adjacent provenance and minimum-version qualification, including provenance4-N1/N2. |

**Historical read-only acquisition register (FR-02)**

These are inert records of actual tool invocations, not instructions or authorization to run them. Original R03/R08 observations were made on **2026-11-09, 02:39-02:44 UTC**; R03's selected executable reported **`1.4.245-aidev02.780594c521aa`** at A01. Later domain-review records are separately dated below. No retrieval was rerun for this correction; rerunning a command now would observe a different time/build/remote state, not reproduce the historical response.

The retained JSONL files are beneath `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-fix-flaky-parallel-thread-test/952cee73-732b-4629-bd21-afa7a36058dd/subagents/`: **L03** = `agent-ae16c0141219b265f.jsonl`, **L08** = `agent-add9bff6b59ec565f.jsonl`, **LDA** = `agent-aa7ac7bb2fce883da.jsonl`. Locators below are physical JSONL record lines, not original source offsets. `qa/qa-fix-log.md` binds every acquisition ID to its exact tool-call ID and observation time. Selected output is deliberately bounded; full original tool results remain in those logs.

| ID | Actual read-only invocation | Selected retained output | Retained result |
|---|---|---|---|
| A01 | `orca-ide --version` | `1.4.245-aidev02.780594c521aa` | L03:164 |
| A02 | `orca-ide skills get orca-cli --json` | JSON `name` = `orca-cli`, with `full` and `markdown` fields. | L03:87 |
| A03 | `orca-ide skills get --help` | `--reference <name>` prints one bundled reference. | L03:110 |
| A04 | `orca-ide skills get orchestration` | Role table: coordinator, dispatched worker, handoff owner, compatibility operator, ordinary terminal agent. | L03:113 |
| A05 | `orca-ide skills get orchestration --reference worker-contract` | `# Worker contract`; helper questions, escalations and completion arrive in the worker's own check. | L03:140 |
| A06 | `orca-ide skills get orchestration --reference coordinator-loop` | `# Coordinator loop`. | L03:143 |
| A07 | `orca-ide orchestration --help` | `Usage: orca orchestration <command> [options]`. | L03:116 |
| A08 | `orca-ide orchestration worker-start --help` | Usage distinguishes `--task`, `--spec`, `--agent` and `--terminal`. | L03:146 |
| A09 | `orca-ide orchestration dispatch --help` | Usage includes `--inject` and `--dry-run`. | L03:149 |
| A10 | `orca-ide orchestration task-create --help` | Usage includes `--parent`, `--run` and `--from`. | L03:152 |
| A11 | `orca-ide orchestration send --help` | “From an active Dispatch, an omitted recipient defaults to its owning Run mailbox.” Historical help discrepancy retained in Section 2.4. | L03:155 |
| A12 | `orca-ide orchestration ask --help` | “From an active Dispatch, a new question defaults to its owning Run mailbox.” Same historical qualification. | L03:158 |
| A13 | `orca-ide orchestration check --help` | Usage includes `--ack`, `--peek` and `--wait`. | L03:161 |
| A14 | `orca-ide agent launch --help` | Usage includes `--worktree`, `--prompt`, `--surface` and `--retry-launch`. | L03:222 |
| A15 | `orca-ide worktree create --help` | Usage includes `--agent`, `--parent-worktree` and `--no-parent`. | L03:225 |
| A16 | `orca-ide --help` | `Usage: orca <command> [options]`. | L03:311 |
| A17 | `gh issue view 339 --repo IronbellyOrg/IronClaude --json number,title,body,state,url,comments` | `state=OPEN`; comments include `6659516712`, `6659559030`, `6703399956`, `6703934716`, `6703934983`. | L08:77 |
| A18 | `gh issue view 423 --repo IronbellyOrg/IronClaude --json number,title,body,state,url,comments` | `state=OPEN`; body explicitly separates the future knowledge-sharing release from v1. | L08:80 |
| A19 | `gh issue view 431 --repo IronbellyOrg/IronClaude --json number,title,body,state,url,comments` | `state=OPEN`; title describes weak alive-check signals. No incident reproduction. | L08:83 |
| A20 | `gh issue view 409 --repo IronbellyOrg/IronClaude --json number,title,body,state,url` | `state=OPEN`; title: `[FEATURE] TUI Dashboard to Manage Orchestration at Scale`. | L08:86 |
| A21 | `gh issue view 326 --repo IronbellyOrg/IronClaude --json title,body,comments,state,url` | `state=OPEN`; comments include approved-contract comment `6590983517`. | L08:132 |
| A22 | `gh issue view 446 --repo IronbellyOrg/IronClaude --json title,body,comments,state,url` | `state=OPEN`; body requests rechecks after 1, 2, 3 and 4 seconds without editing the lock. | L08:135 |
| A23 | `gh pr view 449 --repo IronbellyOrg/IronClaude --json title,body,state,mergedAt,url,comments` | `state=MERGED`; `mergedAt=2026-11-08T07:05:30Z`; body/comments retained. | L08:138 |
| A24 | `gh pr view 422 --repo IronbellyOrg/IronClaude --json number,state,mergedAt,url` | `state=MERGED`; `mergedAt=2026-11-07T14:15:58Z`. | L08:443 |

**Separately dated domain-review rechecks, not original R03/R08 retrievals**

| ID | Actual read-only invocation | Selected retained output | Observation time and retained result |
|---|---|---|---|
| A25 | `gh pr view 434 --repo IronbellyOrg/IronClaude --json number,state,mergedAt,title` | `state=MERGED`; `mergedAt=2026-11-08T01:53:33Z`. | 2026-11-09T18:18:24.668Z; LDA:164 |
| A26 | `gh issue view 444 --repo IronbellyOrg/IronClaude --json number,state,title,body` | `state=OPEN`; title requests the subordinate-mode evaluation. | 2026-11-09T18:18:57.411Z; LDA:188 |
| A27 | `gh pr view 434 --repo IronbellyOrg/IronClaude --json number,state,body` | `state=MERGED`; body retained separately from A25's metadata. | 2026-11-09T18:22:02.142Z; LDA:539 |

The earlier original acquisitions behind R02's #434 account and the prior #444 investigation were **not recovered by this bounded R03/R08-log search**. A25-A27 record only the domain reviewer's later observations; they do not reconstruct those earlier commands or independently prove an earlier remote state. Other unlisted invocations are not invented. These logs and `qa/qa-fix-log.md` are supplemental provenance/procedural records, not additions to the 49 research/scope/synthesis artifacts. Original returns, prior verdicts, excluded archives and current-target gates remain unchanged.

Assembly integrity is not independent content validation, source-document fidelity, anti-omission acceptance or operational approval. Those distinctions remain explicit even where earlier input gates permitted assembly. No live operation, permission change, implementation or new plan is authorized.
