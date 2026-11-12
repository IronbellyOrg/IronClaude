# Research: Orca nesting mechanics

**Investigation type:** Integration Mapper
**Scope:** Orca code, version-matched guides, depth configuration and P0 evidence
**Status:** Complete (installed-source inspection; no live nested run)
**Date:** 2026-11-09
**Delivery:** User-approved adaptation: researcher returns findings; coordinator writes this file. No model-tier change.

---

## Evidence key and method

Complete verbatim returned findings, including all evidence and limitations, are preserved in machine evidence `returned/03-returned-findings.json` (`text` field); this Markdown organizes their distinct findings for downstream research. All citations are the researcher's directly read source locations, not scope citations. Source reads establish implementation, not successful live execution.

| Key | Source |
|---|---|
| B | `/opt/Orca/resources/app.asar.unpacked/out/main/chunks/orcad-migration-source-retention-B_-OYaBD.js` |
| N | `/opt/Orca/resources/app.asar.unpacked/out/shared/nested-worker-depth.js` |
| D5 | `.dev/orca-command-refactor/decisions/D5/RECOMMENDATION.md` |
| CAPS | `.dev/orca-command-refactor/inventory/orca-capabilities.md` |
| P0-live | `.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/p0-phase-report.md` |
| P0-static / P0-trace | `.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/p0-static-report.md` / `ac-0.7-depth-trace.md` |
| Scope-02 / Scope-03 | `research/scope/scope-02-decision-history-d5.md` / `scope-03-enforcement-surface.md` in this package |
| WC | `src/superclaude/core/WORKER-CONTRACT.md` |

Observed executable `orca-ide`, version `1.4.245-aidev02.780594c521aa`; P0 was 1.4.237. Researcher read all three P0 reports, compact version-matched orchestration guide plus worker-contract/coordinator-loop references, relevant CLI help, bounded installed-bundle excerpts, and only the depth key/value from profile data. No sessions, tasks, dispatches, runs or worktrees created; no settings/messages/GitHub mutations. No credentials emitted.

## 1. Depth implementation and per-call table

| Component | [CODE-VERIFIED] source finding |
|---|---|
| Exports/defaults | N:3-10 exports helpers, default max 1, root 0, nested_worker_depth_exceeded |
| Validation | N:21-26 numeric safe integer >=1, invalid defaults to 1 |
| Creator depth | B:383 O4e/resolveCreatorDepth derives active Dispatch/remote attachment; absent delegation or system creator yields 0 |
| Self bookkeeping | B:383 mU/O4e exclude creator-is-own-assignee Dispatch from delegation |
| Child fence | B:388 A4e/j4e resolveChildDispatchDepth adds one; above max throws effectsApplied:false |
| Ambiguous remote identity | B:385-388 gU throws AmbiguousDispatchParentError for multiple live attachments |

[CODE-VERIFIED] New Run does not reset nesting: caller delegation identity determines depth (B:383-388), not a Run nesting field.

| Call | Fence / evidence |
|---|---|
| worker-start local | [CODE-VERIFIED] Fenced. B:642 workerStart -> B:640 itt supplies creator/max/helper -> B:2589-2597 Alt depth resolution before transaction |
| worker-start --on | [CODE-VERIFIED] Fenced at Run home, B:628 D5e starts depth-checked Dispatch before remote attach. Native worker-helper route separately rejects --on |
| dispatch | [CODE-VERIFIED] B:2698 -> createDispatchContext, B:697 prt depth check before creation |
| dispatch --inject | [CODE-VERIFIED] Same creation/fence at B:2698; inject occurs afterward |
| dispatch --dry-run | [CODE-VERIFIED] Explicit resolveChildDispatchDepth B:2698 around column 9151 before preview |
| task-create | [CODE-VERIFIED] NOT depth-fenced, B:2698 column 6317 CU authority -> createTask; B:2505-2520 Uct validates Run membership/parent/dependencies. Independent coordinator authority still required |
| worktree create --agent | [CODE-VERIFIED] NOT depth-fenced. Installed `out/cli/handlers/worktree-create-agent-launch.js:13-45` general launch (or older-host worktree.create fallback); B:2712 RPt -> B:349 SL creates no Dispatch |
| agent launch | [CODE-VERIFIED] NOT depth-fenced. Installed `out/cli/handlers/agent-launch.js:11-33` -> `out/cli/agent-launch-request.js:79-103` replay/launch -> B:2712 general machinery |
| run-create/run-use | Not child-Dispatch creation; B:388 handlers bind Runs with own/ancestor/takeover authority checks, not depth reset |
| send | Not creation fence; B:2677 sender/destination/lifecycle authority, creator-Dispatch routing |
| ask | B:2698 active Dispatch/Run validated; questions routed through iJ |
| check | B:2698 coordinator Run or Dispatch; B:2678 YX generation-fenced consumption |
| reply | B:2698 Kut/reply plus B:1288-1291 answerQuestion validates addressed Dispatch/generation |
| Legacy coordinator loop | [CODE-VERIFIED] B:2698 uses depth-checked createDispatchContext with system creator/runtime max; not normal helper workflow |
| Federation attach preamble | B:642 supplied depth + subWorkersInOwnRun:true, distinct recipe; full federation depth/authority not certified |
| skills/version/help | Read-only discovery, fence not applicable |

**Key Takeaways:** worker-start/dispatch fenced; general launches/task-create not depth-fenced is NOT unrestricted permission; fresh source strengthens historical classification but must not generalize all authority away.

## 2. Native local helper routing

[CODE-VERIFIED] Native helper questions/reports normally go to the creating worker's Dispatch mailbox, not directly to root Run. This is the critical correction to old D5 reasoning.

| Stage | Source and finding |
|---|---|
| Permission offered | B:640 $et passes depth < runtime max; B:460 includes SUB-DISPATCH only if true |
| Local recipe | B:493-505 Z3e uses worker-start --from worker-handle --spec subtask --worktree current --agent agent; questions/escalations/completion in worker's own check |
| Run identity | B:640 att uses coordinated Run or active creator Dispatch's existing Run; explicit different Run refused |
| Scope restrictions | B:640 ott rejects --on/--terminal, requires new same-host agent; existing Task last run by creator's helper |
| Parentage and fencing | B:640 itt defaults Task parent to helperCreator.task_id; B:2591-2594 creator Dispatch/depth; requiredCreatorDispatchId mismatch throws consumer_fenced |
| Default recipient | B:640 yet accepts same-Run pending/dispatched creator; iJ returns dispatch:creator-id else run:owning-run-id |
| Reports | B:2677 uses iJ for omitted recipient; worker_done/heartbeat use active-Dispatch routing even with explicit recipient |
| Questions | B:2698 ask uses iJ; explicit owning-Run question may instead reach root; manually sent question is not blocking ask |
| Receive/reply | B:2698 chooses Dispatch mailbox when not coordinator; B:2678 YX generation-fenced FIFO holds helper and coordinator mail. B:2698 Kut and B:1288-1291 validate helper answerer |
| Creator settles | yet/iJ sends new reports to Run; B:1267-1275 Jot hands unread selected reports/pending questions back to Run and fences old deliveries |

[CODE-CONTRADICTED] D5:48,69,84 predicted root-Run default, now wrong for native local helpers. Installed CLI specs `out/cli/specs/orchestration.js:78-80` owning-Run blanket default is also incomplete relative to B:640,2677,2698. B:640 vet report types are unspecified/default, worker_done, heartbeat, escalation, status, not every type. [UNVERIFIED] Live local start/reply/restart/completion/fencing/early-settlement not exercised. Remote recipe B:509-519 Q3e creates separate Run; B:642 selects subWorkersInOwnRun:true, so local conclusions do not certify federation.

**Key Takeaways:** existing native O3 upward channel can be reused; individual Task/Dispatch records coexist in one Run; source hand-back is not proven runtime recovery.

## 3. Parentage and ordinary launches

| Relationship | [CODE-VERIFIED] representation and meaning |
|---|---|
| Worktree lineage | B:347 parentWorktreeId/worktreeInstanceId/parentWorktreeInstanceId; installed `out/cli/handlers/worktree-create-agent-launch.js:46-55` workspaceLineage |
| Lineage validity | Installed `out/shared/resolved-worktree-lineage.js:10-22` validates IDs, host boundary and instances; NOT mere cosmetic label, but no lifecycle authority |
| Task hierarchy | B:1875-1898 tasks.parent_id, run_id, creator terminal/pane/process/generation; B:2505 Uct same-Run parents/dependencies |
| Helper Task parent | B:640 itt uses creator's Task |
| Dispatch hierarchy | B:1901-1936 creator_dispatch_id, retry_of_dispatch_id, creator identity, run_id/task_id/depth/consumer_generation; B:532 hG exposes creatorDispatchId |
| Run ownership | B:1547-1562 coordinator handle/pane/session/generation, no parent_run_id column in inspected schema |
| Run ancestry | B:388 M4e/vU derive Dispatch creator ancestry to reject binding worker's own/ancestor Run |
| Placement | B:640 Aet/jet use workspace ancestry for new-child; depth still caller Dispatch identity |

[CODE-CONTRADICTED overstatement] Scope-03:109 "cosmetic grouping": host/instance validation exists. [UNVERIFIED] Full workspace backing persistence writer/table not located; schema/projection/validity verified only.

General agent launch and worktree-create-agent create NO Run/Task/Dispatch automatically on inspected paths. Agent launch yields terminal/chat and receipt/prompt (handlers agent-launch.js:11-33; B:2712 RPt -> B:349 SL); worktree launch yields workspace plus agent/setup/default tabs (worktree-create-agent-launch.js:13-61). B:2712 vPt/EPt and B:349 SL/mYe/TL create surfaces; EJe/UI delivers supplied prompt, not worker preamble GW. Conversely worker-start uses B:2589-2597 Alt transactional work/attempt records and B:640 $et preamble. New ordinary launch without active Dispatch/remote attachment resolves root depth 0 (B:383). [UNVERIFIED] Complete ordinary-launch -> Run -> workers -> upward report lifecycle untested.

**Key Takeaways:** operation ID is not Dispatch ID; workspace, Task, Dispatch and Run parentage differ; O4 uses a different ownership model, not equivalent supervised O3.

## 4. Fixed message vocabulary and guide roles

[CODE-VERIFIED] Exactly nine lifecycle types: status, dispatch, worker_done, merge_ready, escalation, handoff, decision_gate, question, heartbeat. CLI vocabulary `out/cli/specs/orchestration.js:73`; runtime B:642 WJ/Ont; federation Ftt/Ltt; SQL CHECK constraint B:1574-1578. Body/payload conventions do not add types or settlement semantics.

| Version-matched guide role | Source cross-check |
|---|---|
| Coordinator | Explicit supervision, Run binding/mailbox B:388,1547-1562,2688 |
| Dispatched worker | Live Task/Dispatch preamble GW B:393-462; $et B:640 |
| Handoff owner | Ordinary launches, no Run/Task/Dispatch, no monitoring instructed; absence of records source-verified, no-monitoring is policy not runtime prohibition |
| Compatibility operator | Legacy contract before mutation; B:382-388 authority distinctions |
| Ordinary terminal agent | No live preamble or explicit supervision; no lifecycle messages; label is guide wording, not stored role enum |

No sub-coordinator/sub-orchestrator row. Native helpers extend dispatched-worker flow. [CODE-VERIFIED instruction text] WC:62 forbids worker fan-out at any depth and WC:69 requires person-opened coordinator: native capability does NOT authorize IronClaude use.

**Key Takeaways:** no invented sub_coordinator_done type; transport custom fields need contract; capability and policy differ.

## 5. Depth setting scope

| Question | Finding |
|---|---|
| Default | [CODE-VERIFIED] N:7 and `out/shared/default-global-settings.js:160` = 1 |
| Stored profile | Filtered `/home/coder/.config/orca/profiles/local-default/orca-data.json:1` yielded only nestedWorkerMaxDepth:1; no other requested profile-glob matches |
| Range | [CODE-VERIFIED] Safe numeric integer >=1 N:21-26; zero not unlimited; no smaller application max there |
| Desktop control | [CODE-VERIFIED] `out/renderer/assets/Settings-D8mQKKOP.js:4` OC/control validates min 1/integer and updateSettings; no explicit max in control |
| Per-Run override | [CODE-VERIFIED bounded surface] No relevant CLI depth option or Run max-depth column; handlers use runtime getter |
| CLI settings | [CODE-VERIFIED bounded registered surface] No depth settings verb/flag in out/cli/specs; registration index.js:32-60 |
| Scope | [CODE-VERIFIED] Global-settings/runtime-profile field, not Task/Run setting; every Run under SAME runtime/profile is supported. Every profile on machine is too broad |
| Effective current value/reload | [UNVERIFIED] Stored JSON=1 is not proof of active storage authority, complete getter backing or external-edit reload |

**Key Takeaways:** stored value and defaults verified; no supported per-Run switch found; active effective/reload behavior remains untested.

## 6. Reconciliation: task-create and P0

[CODE-VERIFIED] task-create lacks nested-depth check. Scope-02's narrow claim is correct; Scope-03 depth question resolved by code, without mutation. But lack of depth checking is not worker permission.

| Evidence | Establishes / does not establish |
|---|---|
| P0-trace:51 | Historical not-depth-checked; not current worker authority |
| P0-static:12 | AC-0.7 PASS/classification, not live task-create experiment |
| P0-live:18,27 | Carries static trace; no forbidden-call transcript matches; cannot prove rejection of never-attempted calls |
| P0-live:33-35 | Troubleshoot/workflow/adversarial workers, not nested helper/refusal/routing tests |
| B:2698 taskCreate | CU requireCurrentConsumer -> createTask, no depth resolution |
| B:2505-2520 Uct | Run, parent/dependency membership, insert; no creator-depth check |
| B:388 CU/P4e/vU | Current coordinator ownership; unbound worker cannot appropriate owning Run |
| N:21-26 / B:388 A4e | Validation/depth function exists but not called on this path |

[CODE-CONTRADICTED broad wording] Scope-02:83 "only WC-13" fence for task creation in Run ignores coordinator-authority protection. [UNVERIFIED] Raw three P0 session transcripts not replayed; documentary live compliance not forbidden-call-path proof.

**Key Takeaways:** settle source question by inspection; keep permission/depth distinct; P0 did not attempt forbidden calls.

## 7. D5 open facts: source versus live

| D5 item | Source result | Remaining uncertainty |
|---|---|---|
| 1 depth calls/task-create | [CODE-VERIFIED] Per-call table | Live error receipts untested |
| 2 person-opened depth | [CODE-VERIFIED] No delegation=0 B:383-388 | Particular session identity must be observed |
| 3 low-level/ordinary launches | [CODE-VERIFIED] Inject fenced; launches no Dispatch | Ordinary-owner end-to-end lifecycle |
| 4 reread setting | [UNVERIFIED] Getter per operation visible | Full storage/reload trace/authorized probe |
| 5 per-Run override absence | [CODE-VERIFIED bounded CLI/schema] None supported found | Not universal internal/private absence |
| 6 safe lowering | [UNVERIFIED] | Existing helpers/new starts/questions/settlement need authorized test |
| 7 question/completion mailbox | [CODE-VERIFIED] Creator Dispatch with Run fallback | Local live reply/restart/fence/early-settlement; remote separate |
| 8 Agent-tool limits | [UNVERIFIED universal never] Fence counts Dispatches | Adapter/provider analysis/live evidence |
| 9 final D1-D4/git decisions | [UNVERIFIED in mechanics slice] Separate policy records | Read decisions, no live test needed just for decision status |

## 8. Option implications and recommendation

| Option | Assessment |
|---|---|
| O1 two tiers | Current contract-compatible, centralized lifecycle, no depth-setting change |
| O2 person-opened peers | Root identities need no extra Dispatch depth; no automatic upward supervisor; sharing boundaries contractual |
| O3 worker helpers | Strongest native supervised fit: ancestry/mailboxes exist; effective max must permit 2 and IronClaude permission must change. Native ordinary helper same-host/new-agent only |
| O4 handoff owner | Unfenced general launches lack preamble/records; needs new reporting/liveness/completion/ownership contract, not worktree-parent substitute |
| O5 internal subagents | Existing boundary; no per-helper Orca Task/Dispatch provenance; universal no-limit claim unverified |
| O6 defer gates | Present recommendation; preserve contract, evaluate O3 against actual need/lifecycle evidence; O4 not equivalent shortcut |

Researcher recommends O6 now, O3 if reconsideration justified. Current code removes the old root-inbox-overload premise, not authority/scope/retry/write-safety/rollback questions. Gates: runtime-discovered need; explicit session/command permission; helper/retry/write/outward budgets; authorized live depth-2 start/question/reply/completion/creator-settlement/recovery; effective setting and rollback verification.

**Key Takeaways:** O3 better supported than old mailbox hypothesis; current ban still applies; O4 changes supervision model.

## Gaps and Questions

1. [UNVERIFIED] Effective active maximum/external JSON reload, only stored field read.
2. [UNVERIFIED] Safe lowering with depth-2 work.
3. [UNVERIFIED] Live local start/question/reply/completion/restart/fencing/parent settlement; source routing verified only.
4. [UNVERIFIED] Complete remote/federated separate-Run helper workflow.
5. [UNVERIFIED] Universal absence of Agent-tool adapter/provider limits.
6. [UNVERIFIED] Ordinary-owner lifecycle/upward protocol.
7. [UNVERIFIED in this slice] Final D1-D4/git decisions require record reads, not live probes.
8. [UNVERIFIED] P0 raw transcript observations not independently replayed.
9. [UNVERIFIED] Workspace-lineage backing writer/table; schema/projection/validation known.
10. [CODE-CONTRADICTED] D5 root-Run helper default prediction; actual creator Dispatch route.
11. [CODE-CONTRADICTED] Blanket CLI send/ask owning-Run defaults omit helper exception.
12. [CODE-CONTRADICTED broad wording] Scope-02 task-create permission ignores coordinator authority.
13. [CODE-CONTRADICTED overstatement] Scope-03 lineage is not merely cosmetic; still not lifecycle authority.

## Stale Documentation Found

| Document | Disposition |
|---|---|
| [STALE DOC] D5:48,69,84 | [CODE-CONTRADICTED] Local default routing superseded by B:640,2677,2698 |
| CAPS:103 | Depth uncertainty closed by current source; worker-start/dispatch checked, task-create not depth-checked |
| Scope-03:108,121 | task-create depth gap resolved without mutation |
| Scope-02:83 | [CODE-CONTRADICTED as broad permission] Coordinator authority still required |
| P0-trace:5-7,48-59 | Historical version/bundle/symbols/anchors, not current citations; broad classification independently reverified |
| [STALE DOC] CLI specs orchestration.js:78-80 / ask help | [CODE-CONTRADICTED blanket default] Local helper exception missing |
| EVAL326:80 | Correct only narrowed to Dispatch generations; not all ordinary child-agent launches |

## Summary

Current installed Orca implements native local helpers with Task/Dispatch ancestry and creator-worker mailbox delivery. worker-start/dispatch including inject/dry-run are depth-fenced; task-create/ordinary launches are not, while task-create still requires coordinator authority. P0's three live checks recorded compliance, not forbidden-call refusals or depth-2 success; current routing contradicts the old root-mailbox prediction. Defer new sub-mode permission pending policy and live gates, with native O3 the strongest candidate if justified. No live workers, settings mutations or GitHub writes were tested.

