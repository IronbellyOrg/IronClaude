# Synthesis: Problem and Current State

> **Controlling installation-snapshot correction, 2026-11-09:** Read [EVIDENCE-SNAPSHOT-CORRECTION.md](EVIDENCE-SNAPSHOT-CORRECTION.md) with this index and complete original companion. It supersedes contradictory current-default, current-build, stored-observation and existing-path wording in both representations. Earlier installed mechanics/build/stored observations and old backend citations are historical only; newly inspected source default/fallback is two, not an observed effective value. Originals remain unchanged. No nesting permission or gate PASS follows.

**Date:** 2026-11-09
**Status:** Complete (paired current-state synthesis; independent synthesis QA pending)
**Template:** tech-research Report Structure, task Step5.1
**Delivery:** Approved parent persistence of complete returned synthesis.

## 1. Problem Statement
- **The question:** Should the proposed `/sc:orchestrator` support a subordinate coordinator, possibly `--sub`, which takes upper assignments, supervises its own sessions and reports upward? Establish value, implications, unlocks and required reconsideration. This is a decision report, not implementation authorization or a build plan.
- **Why it matters:** Internal command helpers, supervised Orca workers, ordinary launches, worktree ownership and person-opened coordinators have different authority/reporting. A middle session needs both downward permission and accountable upward results. Issue339 flat supervision and issue423 knowledge sharing do not inherently depend on hierarchy.
- **Trigger:** Issue444 asks for evaluation without preselecting adoption. PR449 introduced a subordinate-coordinator ownership phrase while preserving the worker restriction. Its recorded INF-027 deliberately deferred WC-13, leaving a rule defect rather than implementing a middle role. D5 retained depth1/person-opened coordinator/worker fan-out ban. Issue339's later hierarchy/security v2 differs from issue423's knowledge-sharing v2.

**Evidence:** task Step5.1:291-293; `.dev/reflect/pre-TASK-WF-enforceTheOwnerP-20261108-031809-20261108033529/REPORT.md:77-78`; `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:405`; research08§1-4 and complete return.

**Required paired synthesis:** [returned/synth-01-returned-sections.json](returned/synth-01-returned-sections.json), complete460-line text, is mandatory alongside this substantive index for assembly, QA, fidelity and anti-omission. It preserves every rule/signal/state/launcher/issue table, source-alias register, dedicated uncertainty categories and eight-source coverage/exclusion notes. All eight numbered research reports and full returns were consumed; scope files were hypotheses only. No web findings were used. CODE-VERIFIED instruction means current normative wording, **not automatic enforcement**; implementation means traced source, **not live execution**. Unknowns appear only in the dedicated summary/uncertainty category, not as architecture facts.

## 2. Current State Analysis
**Source key:** project-relative paths resolve beneath `/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test`. WC=`src/superclaude/core/WORKER-CONTRACT.md`; CORE=`src/superclaude/core/CLAUDE.md`; GUARD=`src/superclaude/hooks/scripts/launch-level-guard.sh`; WT-HOOK=`src/superclaude/hooks/scripts/require-orca-worktree-agent.sh`; JOB=`src/superclaude/hooks/scripts/launch-job-identity.sh`; SPEC=`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; REC=`.dev/orca-command-refactor/decisions/D5/RECOMMENDATION.md`; APPROVED=`.dev/orca-command-refactor/decisions/APPROVED.md`; CLI=`src/superclaude/cli`; ISSUE-LAUNCH=`src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`; ORCA=`/opt/Orca/resources/app.asar.unpacked/out`; BUNDLE=`/opt/Orca/resources/app.asar.unpacked/out/main/chunks/orcad-migration-source-retention-B_-OYaBD.js`; DEPTH=`/opt/Orca/resources/app.asar.unpacked/out/shared/nested-worker-depth.js`. R01-R08 mean current task's numbered research files/full JSON companions; complete absolute aliases and source lines remain in paired synthesis.

### 2.1 Contract and Role Model
[CODE-VERIFIED: source instructions]
| Boundary | Current rule and meaning | Evidence |
|---|---|---|
| Identity/eligibility | Live Task/Dispatch preamble defines worker; expressly user-started ordinary sessions not every launched nonworker. Coordinator person-opened. | WC:11,69 |
| Mode/command boundary | Explicit standalone unattended selector, no Orca/preamble/environment detection, not ban on other flags. Opening no-Orca-command sentence broader than WC-8's three named verbs. | WC:5,12-14,40 |
| Worker fan-out | Six routes: worker-start/dispatch/task-create/low-level dispatch/worktree create--agent/agent launch prohibited at any depth. Moving call/newRun/name does not amend rule. | WC:62 |
| Internal helpers/chains | Assigned command runs top-level, its own helpers retained, enclosing worker alone lifecycle. Fixed multiple Command lines supported, not autonomous child planning/dispatch. | WC:60,63-64,204-216 |
| Visible command guard | Worker checks actual project/global copies, mismatch/never-worker refusal before work. Source-tree conversion not deployed eligibility. | WC:16-23,216 |
| Task ownership/admission | Only self-created Tasks started; failed/blocked inputs not dependents, partial usability decided, reports read before admission/new dependents. | WC:239-246 |
| Human/Git boundaries | Exact Task quote/sole child occupancy/succeeded command for local commit, ends at completion; no transitive grant. Human Rulings only, ordinary PR placement, authorized outward owner, protected work/freeze/same-worktree resume. Fan-in admitted/settled, max10/min2 inputs. | WC:41-47,57,224-235,250-273 |

```text
Person-opened coordinator (owns Tasks, supervision and admission)
  +-- top-level worker (runs assigned commands, owns lifecycle)
        +-- command's existing internal Agent helpers
        +-- new external work reported upward, not launched by worker
```
Diagram represents source instructions, not automatic enforcement. CORE's creator-owner/middle-coordinator phrase coexists with explicit supervised-worker preservation; no subordinate brief/protocol/grant/exception follows. **Evidence:** CORE:52-59; WC anchors above; R01:31-150 and full§5.2-5.7 matrix. Compatibility cells not live passes.

### 2.2 Liveness and Reporting
[CODE-VERIFIED: source instructions]
| Signal/procedure | Current distinction | Evidence |
|---|---|---|
| Heartbeat/progress | Command index/on-disk counter/silence window; unchanged token is existence, substantive file/token/transcript change semantic progress. Arrival/reread not progress. | WC:65,110-114 |
| Long step/questions | Declared silence defers typed intervention not probes; helper gap not death. Eligible at mostone question/Task, timeout resumes sameID, no human Ruling. | WC:46,53-58,120 |
| Completion/admission | Own top worker_done exactlyonce, status/reply/handoff not completion; no coordinator synthesis. Contract/artifact read before admission. | WC:32-39,59-60,108,239-246 |
| Two acknowledgments | Whole FIFO Delivery handled/logged before ack, wake filters not permission to discard. applied/queued/refused different from batch receipt; current Task/Dispatch validation/quarantine. | WC:61,103-106,131-138 |
| Checkpoint/notes |40line command handoff includes lifecycle IDs/status/evidence/decisions/applied IDs/next; run notes record timing/lineage/admission/runtime split costs. | WC:64,97,104,146-179,242,246 |
| States | S0starting,S1progressing,S2long step,S3idle,S4person prompt,S5ask,S6context exhausted,S7unreachable,S8exited,S9finished unreported,S10settled,S11unknown; procedural distinctions, not executed state machine. | WC:118-129 |
| Response ladder | Observe/probe/nudge/idle-only typed question/proof-gated restart/human escalation; per-incident/lineage caps. Sweep at most every5min,10min no-progress probe, state/human by15min; starting values, not measured guarantees. pending_ack5/15min path and single conditional copy, not resend loop. | WC:97,110-159 |
| Never on silence | Deadlines/exhaustion/unverifiable alone not stop/retry/release/fail/person answer/Ruling/forged lifecycle. Settle prior attempt before new Task/report directory. | WC:73-79,157-192 |

[CODE-VERIFIED: development implementation] Delivery replay/generation fencing/FIFO batch selection/batch acknowledgment and harmless duplicate ack were traced in `/home/coder/workspaces/IronOrca/src/main/runtime/orchestration/db/messages/role-mailbox-delivery.ts:27-169`, not whole installed-build equivalence. Installed helper route separately traced below. R02 records eight incidents/#434 procedural response, not incident elimination. C1-C8/C15-C17 retained, C9 deleted, future C10-C14 not assumed delivered. Full paired synthesis preserves all12state rows, signals/ladder/ack/C-rule meanings. **Evidence:** WC:46-65,73-79,95-200,239-246; R02:26-136/full§3-8. Own/child progress/outcome/admission/checkpoint composition not defined by present worker-oriented instructions.

### 2.3 Orca Mechanics
[CODE-VERIFIED: installed implementation]
| Examined route/property | Traced result and limit | Evidence |
|---|---|---|
| worker-start | Depth resolved inside creation transaction before commit, rollback on refusal, caller identity/runtime maximum supplied | BUNDLE:640,2589-2597 |
| dispatch/inject/dry-run | Dispatch creation fenced; inject follows creation, dry-run explicitly resolves depth | BUNDLE:2698 |
| task-create | No nested-depth check, independent current coordinator/Run authority check remains | BUNDLE:388,2698 |
| ordinary worktree/agent launch | General launch/fallback, no automatic Run/Task/Dispatch or worker preamble on examined paths | ORCA/cli/handlers/worktree-create-agent-launch.js:13-61; ORCA/cli/handlers/agent-launch.js:11-33; ORCA/cli/agent-launch-request.js:79-103 |
| New Run/binding | Caller delegation depth not reset; ownership/takeover separate | BUNDLE:383-388 |
| Depth default | Historical default/fallback1 is superseded by the 2026-11-09 source observation: default/fallback2, root0, safe integer>=1 and guarded legacy1-to2 migration. Effective setting and migration execution remain UNVERIFIED. Transaction ordering remains a historical bundle trace, not a replacement-build finding. | DEPTH:10-42; historical BUNDLE:2589-2597; controlling snapshot correction |
| Native local helper identity | Same Run, creator Dispatch, parentTask default, same-host/new-agent; wrong Run/ordinary remote/terminal reuse rejected; helper preamble only below maximum | BUNDLE:640 |
| Creator mailbox | Active pending/dispatched same-Run creator selected, otherwise Run. Default ask/reports to creator; explicit Run address can target coordinator, reply recognizes creator | BUNDLE:640,2698; R03 installed send trace |
| Settlement handback | Selected unread worker_done/escalation/status and pendingquestions to Run, old deliveries fenced. Heartbeat excluded from selected unread list | BUNDLE:1267-1275 |
| Parentage | Workspace host/instance-validated lineage not merely cosmetic; Task parent/Run/creator, Dispatch creator/retry/depth/generation, Run owner/generation all different; no direct parentRun in inspected field set | ORCA/shared/resolved-worktree-lineage.js:10-22; R03:83-116 |
| Vocabulary/help | Nine supported message types, not all lifecycle settlement; arbitrary body label not new type. Blanket owning-Run recipient help omits local helper exception | ORCA/cli/specs/orchestration.js:73-80; R03:170-177 |

```text
Installed native local helper source (not IronClaude permission)
Run -> creator Dispatch -> helper Task/Dispatch
                   ^              |
                   +-- default reports/questions
inactive creator: new reports and selected unread mail -> Run
```
Selected handback not full supervision takeover. Supported types: status,dispatch,worker_done,merge_ready,escalation,handoff,decision_gate,question,heartbeat. [Source-record distinction] Version-matched guide lists coordinator/dispatched worker/handoff owner/compatibility operator/ordinary terminal agent; handoff-owner no-monitor instruction is guide policy, ordinary launch not supervised record. Remote/federated recipe separate. **Evidence:** R03:28-177 and complete return; installed anchors above. Live operation/effective setting/recovery excluded from factual diagram.

### 2.4 Hooks, Guards and Identity
[CODE-VERIFIED: implementation]
| Mechanism | Actual input/binding | Limit / evidence |
|---|---|---|
| Worktree-agent syntax | Bash positional/agent/help scanner; message printed after bare-create denial | Agent syntax not ownership permission. Ownership/no-self-use remain instructions. This hook's interpreter/subprocess/script/non-Bash/dependency ceilings not every hook's. WT-HOOK:6-61,94-103,342-357 |
| Launch-level guard | Validated top-level session/accepted launch-level record, not coordinator/parent/resource role model | Positively bound sessions only, unbound fail-open means absence of this enforcement not policy exception. GUARD:185-203,254-271,390-395 |
| Job adapter | Validated envelope/governed state and Bash rewrite, supported Linux same-user job identity | Not role inference/sandbox; whole-input ordering and persistent cwd not supplied by fresh-shell model. JOB:2-18,424-481 |

**Recognition ceiling (B1):** GUARD:450-478 takes basename and enters Orca branch for literal `orca`; observed `orca-ide` does not match. Other classifications can still deny, so neither universal coverage nor alternate-spelling permission/live bypass is proved. Recognized exceptions include status/help/version, worktree current/list/show, terminal list/show/read, orchestration check/inbox/run-current/task-list/worker-show and specified trailing help. Other pairs ESCAPE denied every governed level, agent flag does not override. GUARD:475-478,724-737.

**Required-probe mismatch (B2):** WC:107,110 requires worker-list enumeration; WC:151 worker-read transcript; WC:110 worktree ps prompt-wait. Those recognized pairs absent from exceptions and fall to ESCAPE. Listed worker-show is not equivalent. Even retained flat supervision cannot run these forms unchanged in bound session. Person-opened not automatically unbound. Launch/report/probes are separate policy surfaces, no expansion authorized.

Local/background Agent/Task branch not ESCAPE by itself; remote isolation is. SendMessage/Workflow/RemoteTrigger ESCAPE; actual child identity/live order not established by classification. GUARD:681-687. Registrations/install inclusion for three hooks source-visible, not successful live enforcement. **Evidence:** `src/superclaude/hooks/hooks.json:105-133`; CLI/install_hooks.py:86-93; R04:87-107 controlling addendum plus full return, dependent corrections R05/R07. Scope-limited syntax/session/job identity must not be conflated.

### 2.5 Session-Launcher Precedents
[CODE-VERIFIED: implementation or identified shipped instructions, not successful execution]
| Precedent | Established mechanism, not complete middle supervision | Evidence |
|---|---|---|
| L1 issue claim external agent | Intentional create/prepare/pending then ordinary launch; preflight claim environment not child, receipt not Task completion/authority | ISSUE-LAUNCH:666-681,1300-1355 |
| L2 issue lookup/draft helpers | Narrow Agent artifacts, missing-output retry, skill retains GitHub/ClickUp writes; not Orca Dispatch | `src/superclaude/skills/sc-issue-protocol/SKILL.md:54-76`; R05:44-61 |
| L3 issue-watch | Program's valid claim prompt/ordinary agent argv/outcome, not persistent upper coordinator | CLI/issue_watch/launch.py:84-116,352-370 |
| L4 ordinary PR session | D3 top-level ordinary carriage/attended monitor, not middle worker | WC:229-235; R05:44-61/full source register |
| L5 PM | Specialist/parallel-phase instructions, not implemented nested Orca authority | R05:44-61/full source register |
| L6 spawn | Explicit decomposition-only stopping boundary, not persistent execution | R05:44-61; source spawn command:176-210 in paired register |
| L7 agent | Current-session ownership/helper guidance, not external middle role | R05:44-61; source agent command:23-50 in paired register |
| L8 sprint phase | Configured child process polling/file-backed errors, program supervision not coordinator identity | CLI/pipeline/process.py:140-218 |
| L9 sprint task | Dependency waves/thread pool/subprocess/watchdog/results/atomic handoff; resume success requires task and gate | CLI/sprint/executor.py:1328-1335,1683-1723,2126-2146; scheduler.py:85-104; handoff.py:35-66 |
| L10 narrative helper | One-turn subprocess timeout/empty failure fallback, bypass invocation not safe-authority precedent | CLI/sprint/summarizer.py:310-367 |
| L11 checkpoint rerun | Scoped CLI recursion suppression/exit handling; shown subprocess has no timeout argument | CLI/sprint/rerun_tasks.py:1375-1387,1701-1719 |
| L12 sprint tmux | Foreground wrapper suppresses recursion/shares state, process packaging not agent upward reporting | CLI/sprint/tmux.py:176-202 |
| L13 swarm workers | Parallel model-text transport/retries/budgets/reduction; request payload not tool/worktree delegation | CLI/swarm/dispatch.py:241-276,409-475; transports/openai_compat.py:379-402; reduce.py:350-375 |
| L14 detached swarm | Saved-spec tmux CLI with missing-tool/empty/name-collision guards, durable job not lifecycle authority | CLI/swarm/commands.py:1297-1309; tmux.py:160-177 |

No inspected launcher implements the complete supervised-upper-assignment/external-children/aggregate-upward relationship. Source instruction and process/function capability remain distinct; issue skill labels not Orca layering, two-stage exception not worker permission, sprint environment/bypass not sandbox, governed L1 claims subject to recognition/probe corrections. **Evidence:** R05:40-75 and full fourteen-launcher/56-reuse-cell register; exact source references retained in paired synthesis. No launcher/path classified by an unexecuted outcome.

### 2.6 Decision History and Revisit Evidence
[CODE-VERIFIED: approved record/source instructions] D1 explicit mode/brief guard, D2 human Rulings/freeze, D3 ordinary PR carriage, D4 quoted narrow local commit, D5 depth1/person-opened coordinator/WC-13 retained; coordinator outward Git/merge/removal under human authority. **Evidence:** APPROVED:8-20; WC:60,62,69,229-246,250-269.

| Revisit condition | Applied SPEC:405 | REC:49 |
|---|---|---|
| Composite brief defined | required | required |
| Real runtime-only split with material extra coordinator round trip | required | required |
| Pre-raise AC-0.7 trace | required | required |
| Establish depth2 question/completion mailbox | not stated | required |

Short-record supersession at `.dev/orca-command-refactor/review/disposition-round4.md:48-58` does not explain omission intent. Source route established separately; no deliberate waiver inferred. R06 bounded search found no qualifying combined Task/split/timing record; follow-ups/runtimes/heartbeat gaps/copy refusals not that measurement, no global absence claim.

Final rejected alternative was session-layer depth2/scoped helper limit/no command changes, not original command-owned proposal. Five costs retained with corrections: composite authority not command chain; dual loop undefined; root-only prediction contradicted for current local route; worker rule still no exception; broader runtime/profile maximum not brief permission or all-machine scope. Recorded benefit fewer root wake/read/Task-creation round trips is rationale, not measured saving.

Historical P0 AC-0.7 acceptance not current-version/live refusal or depth2 success; current R03 independently traced call paths. P1 original FAIL not final accepted disposition and actual Skill invocation remains requirement. P2 static merge not live acceptance. **Evidence:** SPEC:396-407; REC:44-64; R06:52-157,175-201; R03:133-177; WC:204-216,246. Current source answers supersede slice-local routing/depth unknowns, not approved policy.

### 2.7 Issues, Pull Requests and Requirements
Recorded requirements/historical observations, not delivered architecture:
| Record | Scope and current relationship | Evidence |
|---|---|---|
|339supervision | Owner/routing/sweeps/recovery/attention/report/cleanup mostly flat-applicable; current worker procedure not whole all-session product | R08:19-85/full35requirement matrix |
|339security/hierarchy | Typed validation/scoped expiring attenuated grants/replay/destructive safeguards before later hierarchy, not permission changes now | R08:19-85,89-133 |
|423knowledge | Catalogue/relevance/shared lessons/overlap/course correction not child dispatch/depth/grant/upward acceptance | R08:89-106 |
|431/434liveness | Reported failures/new procedural response, not hierarchy authority or incident elimination | R02:100-136; R08:89-106 |
|409observer | Several coordinators not nested coordinators; excludes scheduler/session controls, synthetic scale not capacity | R08:106/full related-issue tables |
|326Git | Depth1/central Git relay not adopted; remaining commit/submodule work independent | R08:106-125; R06 approved outcomes |
|446lock | Requested bounded rechecks independent; current rule blocked with path, not implemented retry sequence | WC:45; R08:106-125 |
|422conversion | Observed merged static scope; historical open claim stale, not live rollout acceptance | R08:106-125 |
|449ownership | Creator-agent ownership/syntax hook/intentional claim exception, subordinate authority/aggregate protocol undefined, contract deferred | R08:117-125; INF record cited§1 |

All35 requirement dispositions retained in full pair: R01-R09 scale/routing/interaction/sweeps/recovery/closure/cleanup/push; R10-R17 retained evidence/conditional placement/registry/presentation/attention/display/server/skill integration; R18-R19 hierarchy/confirmation objective; R20-R24 modes/untrusted text/types/validation/inbound research; R25-R29 grants/session/expiry/replay/attenuation/destructive safeguards; R30-R35 sender/interception/research ordering/library selection/prerequisites/planning suggestion. Extraction is not delivery.

[CODE-VERIFIED: instructions] Absolute automation/disposal/worktree-per-prompt/time-based recovery/transitive consent conflict with WC:41-47,57,73-79,225,229-269. [CODE-VERIFIED: implementation] Actual coordinator-only claim code calls Orca, tension with universal no-primitives-Orca description, not worker exemption: ISSUE-LAUNCH:666-681,1351-1355. Existing optional Dispatch-capability forwarding not absent, but not proven proposed narrowing system: ORCA/cli/handlers/orchestration/message-send-handler.js:33-65. **Evidence:** R08:19-131 and complete records/URLs, WC and code anchors above. No web property imported into these current-state sections.

### 2.8 Current Wording and Change Surface
[CODE-VERIFIED: current source instructions/tests/distribution implementation]
| Surface | Established relation and limit | Evidence |
|---|---|---|
| Ownership prose/message | Root/core/README and source/plugin printed sentence not isolated; scanner agent-flag predicate separate | CORE:52-59; WT-HOOK:94-103,342-357; R07:11-41,65-153 |
| Exact vs roles test | Message expected exactly; role/paragraph parity not exact under-another phrase, so cannot assume two mandatory test edits | `tests/hooks/test_require_orca_worktree_agent.py:31-38`; `tests/core/test_orca_session_launch_guidance.py:44-59` |
| Contract inventory/tests | Static phrase/content/heading comparison, populated expectations and31 unattended headings (16P1+15P2), not31live runs | `tests/skills/test_worker_contract.py:746,755-758,831-886,907-909`; WC:303-304 |
| Plugin/source parity | Specified worktree-hook byte equality and routing-guide full-file tests, not universal copy freshness | `tests/cli/test_install_hooks.py:849-857`; `tests/commands/test_routing_plugin_parity.py:29-38` |
| Dev sync/build/install | Makefile copies distributables, not global core; builder packages plugin tree, not source synchronization; installers skip existing without force; install-test equality only test target | `Makefile:108-184`; `scripts/build_superclaude_plugin.py:15-18,69-76`; CLI/install_core.py:32-75; CLI/install_hooks.py:251-290; `tests/cli/test_how_we_work_install.py:23-33` |

Conditional topology effects: retained two tiers/wording touches prose/message/copies not new permission; independent peers need exclusive ownership, bound-probe issue persists; supervised helpers broaden eligibility/brief/outcome/admission/retry/ack/failure/grant/placement/governance, not necessarily command-side WC-8; ordinary launched owner needs role/upward contract, not inherited outward authority; internal helpers need no external policy change; deferral retains independent ambiguity/stale-description defects. **Evidence:** R07:65-145,188-198; R01:31-150.

Stale descriptions retained as discrepancies/history: developer guide's At-P0 empty inventory not current31; universal no-Orca-primitives description contradicted by narrow claim implementation; REC/CR-01 unapplied status historical; old P0-smoke trigger superseded; one-command premise corrected by chains; root-mailbox prediction corrected by local creator source;422open claim stale;446lock pointer nowWC:45; current setup skips without authorization and PRs remain ordinary; old Orca bundle/offsets historical, not current source. **Evidence:** `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:978-991`; WC:45,60-64,221,232,303-304; R01:162-172; R03:133-177; R06:52-157; R07:147-165; R08:106-125.

R07 approved current-source/tests/distributed inventory complete; older partial closing text not scope authority.867unread archival matching lines/274paths remain excluded background, no runtime/authority conclusion depends on classifying them. **Evidence:** R07:11-15,168-198; current gaps log:10-12.

### 2.N Current State Summary
| Evidence class | Current state established in this codebase-source synthesis | Boundary |
|---|---|---|
| A: repository rules/current implementation | Person-opened coordinator, explicit unattended/visible-copy guard, worker external fan-out ban, retained internal helpers, own lifecycle, human Rulings/narrow Task grants, authorized outward/admission/retry/protected cleanup; real coordinator-only issue launch | Verified instructions not automatic obedience. Claim helper not blanket worker/subordinate exception. Sources§2.1,2.5,2.7. |
| B: Orca source-enforced mechanisms/identified help | Worker/Dispatch depth paths including inject/dry-run, independent Task authority, caller depth not Run reset, native creator route/selected mail fallback, ordinary launches not automatic records, fixed message vocabulary | Source capability not project permission/live success or separate remote recipe certification. Sources§2.3. |
| C: prose-only authority/procedure boundaries | Creator owns agent/middle coordinator phrase, person-opened eligibility/human restrictions, liveness/acks/recovery procedures; syntax hook not role enforcer | Phrase tests preserve words, not implemented recursive authority or universal compliance. Additional bounded guard/probe integration defects. Sources§2.1-2.2,2.4,2.8. |
| D: explicitly UNVERIFIED or new decisions | Dedicated register below, not architecture assertions/diagrams | Source-answered routing/classification not reopened merely because live behavior unknown. |

#### Dedicated uncertainty register
| Category | Residual uncertainty / open-question family | Evidence boundary |
|---|---|---|
| UNVERIFIED live local lifecycle | Depth2 start/question/reply/completion/early creator settlement/restart/fence/recovery | G05-G06,G12,G17; source route already established |
| UNVERIFIED effective settings | Loaded maximum/storage/reload/safe lowering with descendants/questions | G14-G15; filtered stored1 not effective proof |
| UNVERIFIED concurrency/timing | Concurrent mailbox consumers/default wake/missed answers/attention delay/typing during tools | G05,G23; WC:194-200; source semantics not experiment |
| UNVERIFIED federation | Full separate-Run remote authority/depth/recovery | G13; not local-helper inference |
| UNVERIFIED live governance | Claim child environment/first-tool binding, real nested events, concurrent rewrite order/job/cwd | G28,G30-G31; claim preflight not child proof |
| UNVERIFIED measured outcomes | Eight incidents eliminated/procedure compliance/hierarchical detection bound | G01,G25; merged text/tests not measured outcome |
| Open policy, not live-test answer | Middle eligibility/composite scope/aggregate progress/result/question/retry/freeze/cancel/admission/cleanup/human relay | G02-G09,G19,G27,G34-G35; existing restrictions govern |
| UNVERIFIED bounded search | Qualifying unforeseen split/follow-up Task/material extra round trip | G10; not found in bounded search, not global absence |
| Open record interpretation | REC mailbox prerequisite omitted in short SPEC deliberately or summarization loss | G11; current source route does not explain history |
| Source-only slice's product/security limits | Sender/transport/deployed interception/validator/grants/replay/expiry/library/existing capability suitability not established as installed behavior here | G40-G43,G49; external findings belong§5 and may answer documented feature existence, not deployed security. Do not turn this slice's exclusions into an absolute no-feature claim. |
| UNVERIFIED bounded deployment assertions | Whole development/install equivalence/all-copy freshness/universal helper limits absence/full lineage persistence/full backend artifact validation | G18,G20,G22,G24,G32; specific source facts retain scope |
| UNVERIFIED independent proposed work |339scale/registry/server/report/closure,409remote package,326Git,446experiments,P2live acceptance,C10-C14 mechanisms | G26,G36-G39,G44-G48; proposals/targets/history not current architecture |
| UNVERIFIED excluded background |867unread archival lines/274paths | G53; excluded, not reopened/read/runtime evidence |

**Coverage/exclusions:** All eight numbered reports and full returns consumed. R01's exhaustive clause matrix retained as evidence, not all cells repeated; R02's state/signal/ack/ladder/C-rule detail retained in full pair, development not whole installed equivalence; R03 current installed source controls older source unknowns but no live/remote/setting/provider-limit proof; R04 correction overrides original universal guard/read claims; R05 all14launchers/56reuse cells preserved, instructions not execution; R06 approved history/trigger/P0/P1/P2 distinctions, current R03 answers slice-local source unknowns; R07 exact-v-role pins/distribution/31inventory/approved archival exclusion preserved; R08 all35requirements/related scope/conflicts/capability forwarding represented, estimates/interfaces/administrative release naming not architecture. Full paired synthesis has eight-row coverage register and every detail table. Strongest research conclusion retained as attributed research, not final comparative judgment: current two-tier/internal boundary remains, native helpers strongest existing supervised mechanism if reconsidered. Final option decision belongs§6-7.

No live run/test/model/API/permission/source change or external research performed for these sections. Main risk is confusing source capability or normative text with authorized and demonstrated nested operation.
