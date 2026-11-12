# Research: Liveness and reporting stack

**Investigation type:** Code Tracer
**Scope:** Worker-contract liveness, inbox and handoff rules; issue 431 and PR 434
**Status:** Complete (static source and policy trace; runtime limits retained)
**Date:** 2026-11-09
**Delivery:** User-approved adaptation: researcher returns findings; coordinator writes this file. No model-tier change.

---

## Evidence and complete-result reference

Complete returned findings (all signal/state/ladder/C-rule tables, sources, source ranges and caveats) are preserved verbatim in `returned/02-returned-findings.json`, field `text`. Downstream reviewers must read that text alongside this indexed view. No distinct detailed source evidence was discarded from the package.

| Alias | Path |
|---|---|
| K | `src/superclaude/core/WORKER-CONTRACT.md` |
| S | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` |
| D | `.dev/brainstorms/20261107-190223-orchestrator-v2-worker-liveness/merged-requirements.md` |
| T | `tests/skills/test_worker_contract.py` |
| A-* | `/home/coder/workspaces/IronOrca/src/main/runtime/` source checkout, explicitly NOT certified installed-build equivalence |
| I-DEPTH | `/opt/Orca/resources/app.asar.unpacked/out/shared/nested-worker-depth.js` |

No agents, mailbox consumption/acknowledgment, worker starts, settings changes or tests. Read-only fork-explicit GitHub calls for #431/#434; Auggie/Codegraph unavailable to researcher. Normative prose directly verified is [UNVERIFIED as runtime enforcement]; source capability is [CODE-VERIFIED] in named checkout, not deployed live proof.

## 1. Policy boundary and actual source trace

Current IronClaude forbids dual worker/supervisor: K:5 commands no Orca, :11 worker identity from preamble/Task/Dispatch, :40 command fan-out ban, :62 session fan-out at any depth, :69 coordinator person-opened. K:60 internal helpers cannot send lifecycle messages; :63 continuous chain exceptions; :64 <=40-line handoff lacks explicit helper roster/budgets/outstanding deliveries/admission state; :57,229-234 human/outward authority retained. S:405/K:246 D5 gate unchanged.

| Development-source function (under A-* root) | [CODE-VERIFIED] behavior |
|---|---|
| `rpc/methods/orchestration/worker/worker-start-authority.ts:11-47` resolveWorkerStartRun | Coordinated Run else active worker's same Run/helperCreator; foreign Run refused |
| Same :50-69 assertHelperStartScope | Reject remote/other terminal and existing Task outside creator-helper lineage |
| `orchestration/dispatch-report-mailbox.ts:4-36` | Report types default/done/heartbeat/escalation/status; live same-Run creator pending/dispatched; recipient creator Dispatch else Run |
| `rpc/methods/orchestration/messaging/send-methods.ts:143-153` | Default reports use creator route; done/heartbeat override explicit recipient with active identity |
| `messaging/check-worker.ts:175-207` | Dispatch mailbox/generation-fenced Delivery and ack |
| `orchestration/db/messages/role-mailbox-delivery.ts:27-104,111-169` | Replay outstanding Delivery, generation mismatch rejection, wake types separate from whole FIFO batch, whole-batch ack, duplicates harmless |
| `messaging/ask-methods.ts:91-137` | Resume only active Dispatch question; default creator mailbox, explicit root/coordinator permitted |
| `messaging/helper-question-answerer.ts:7-37` | Addressed parent Dispatch eligible answerer |
| `orchestration/db/runs/worker-run-binding.ts:44-72` | Worker cannot bind own/ancestor Run or take over coordinator role |
| `orchestration/db/messages/helper-mailbox-hand-back.ts:6-59` | On parent settlement selected unread reports/pending questions handed to Run; old Delivery fenced |
| `orchestration/preamble.ts:219-237` | Generated helper instructions: report to own check, wait helper_done before own_done (instruction, not behavioral enforcement) |
| `orchestration/db/dispatch-depth.ts:164-178` | Child depth=creator+1, above cap rejected |
| `orchestration/lifecycle-reconciliation.ts:119-162` | Inactive/unauthorized heartbeats suppressed, correct Dispatch timestamp recorded |

End-to-end: active worker recognized -> helper creator route -> send to Dispatch -> mixed parent/helper mailbox generation-fenced check -> helper ask/reply -> creator settlement selected mail handback/new reports Run fallback. [UNVERIFIED] Development checkout exact version equivalence and live behavior.

Installed CLI evidence, not backend equivalence: `/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/orchestration/message-check-handler.js:13-45` forwards caller/types/Run/ack/wait; `message-send-handler.js:23-65` resolves lifecycle sender/settlement; `worker-observation-handlers.js:8-50` independently exposes liveness, absent-vs-null agentWait and transcript/terminal reads. I-DEPTH:6-26 defaults max1, not proof active value.

**Key Takeaways:** transport already exists in source; new upward type not necessarily required; combined role policy and deployed behavior still open.

## 2. Signal trace (U upper, M middle, W child)

| Signal | Emitter -> consumer, evidence | Two-edge effect |
|---|---|---|
| Task/Dispatch identity | Runtime/preamble -> worker/supervisor K:11,16,106 | U tracks M; M tracks W; child result must not impersonate M |
| heartbeat | Worker -> supervisor K:46,65,108; development reconciliation :138-162 | Existence not progress; child's cannot substitute M's |
| progress token/semantic counter | Worker -> supervisor K:65,110-113 | Undefined aggregation; mail arrival/repeat not semantic progress |
| expect_silence_min | Worker -> supervisor K:46,65,112,120 | Defers typing not probing; child's window does not excuse M's other duties |
| status | Worker -> supervisor K:108 | Child completion-like status not M's S9 |
| application ack | Receiver -> sender K:61,131-138 | U->M applied and M->W applied are separate, not Delivery ack |
| ask/question and reply | K:53-58,65,108,123; A-ASK:113-137 | M blocked asking U may stop servicing W; authority/provenance of relay undefined |
| worker_done | Own top-level worker -> supervisor K:59-60,108 | Child completion and aggregate completion separate; no synthesis |
| escalation | K:106,108; A-ROUTE:4-36 | Native creator route exists; L5 says PERSON not just parent |
| decision_gate | K:108 | Human-only; not among creator-default report types |
| handoff message | K:59,106,108 | Not WC-15 file/completion; no implicit supervision transfer |
| merge_ready | K:106,108 | Receipt not merge authority |
| dispatch / unknown | K:101,105,108 | Unexpected logged, unknown S11 not automatic role assignment |
| Delivery / ack | K:103-104; A-DELIVERY:27-169 | Replay whole FIFO/mixed parent-helper batch, ack only after all handled; one loop cannot discard another's mail |
| consumer_fenced | K:61,63 | M stops, helpers may continue; takeover undefined |
| contract/stat/statuses | K:32-39,47,59,110,127,241-243 | Own aggregate vs each child durable report; no general child->aggregate outcome reduction |
| transcript/time | K:113,118-129,157 | M monitoring activity not child progress; U cannot infer child state |
| agentWait/screen | K:121-125,134-137 | Identify correct session; no proxy person approval |
| typed nudge/receipt | K:135-137,151-164 | Separate incident caps/proof; receipt not completion |
| <=40-line handoff | K:64,167-179 | Needs additional subtree checkpoint fields before supervisor recovery |
| run notes | K:97,104,146-159,242,246 | Local/upper correlated records, evidence not waking/delivery |
| exit/stall/cancellation | K:76-79,154-159 | M settled/exited does not prove children quiescent |

**Key Takeaways:** every supervision edge needs attribution; two ack kinds distinct; aggregate results/semantic progress undefined.

## 3. States timing ladder and acknowledgments

All classifications are procedural requirements, not observed automatic state machine.

| State K:118-129 | Trigger/action | Dual-role issue |
|---|---|---|
| S0 starting | No token/transcript 10min; probe/begin nudge, report by15 | Separate startup clock per edge |
| S1 progressing | Token within W plus semantic change10min; watch | M receiving repeated mail not own substantive progress |
| S2 long step | Declared silence or transcript<5min; probe10min even window; defer typing | Must still service parent and other children |
| S3 idle | Unchanged token W + old final turn/empty/no tool/no ask; bounded intervention, proof for restart | Healthy children can lack supervisor |
| S4 person prompt | agentWait; screenshot/report after5min+delay, every15; never answer | Relay must reach actual person |
| S5 ask | Open question; answer then ack timeline | M owes child answers while blocked upstream |
| S6 exhausted | Twice screen evidence5min apart; handoff interrupt; proof/budget restart | Need helper roster/pending mail/budgets preserved on replacement |
| S7 unreachable | unverifiable10min -> report, never restart solely | Child exit cannot be inferred |
| S8 exited | Positive exit; settle WC-6 then restart/report | Not subtree exit proof |
| S9 unreported | Final-command contract/no later line/no completion one sweep; read/nudge/escalate | Own command contract may precede child admission |
| S10 settled | Completion received, no liveness action | Child settlement not parent/subtree admission/cleanup |
| S11 unknown | Stale/unknown deciding evidence, probe/no typing | No guessed ownership/restart |

K:97,110-114 starting parameters: sweep wake/timeout <=once5min; fleet listing, prompt-wait listing, own contract stat per worker; W=max10min/twice observed median heartbeat (or declared silence), cap45; probe no semantic10; named state/human report15; unverifiable10. [UNVERIFIED] No measured cascading hierarchical detection bound.

| Ladder/ack | Evidence / duty | Middle-layer concern |
|---|---|---|
| L0 observe | K:150 | Separate edge health |
| L1 read probe | K:151 <=2 costly probes per triggered worker/sweep | Avoid independent stale duplicate interventions |
| L2 nudge | K:152 one/incident two/lineage, failed start counts | Budget persists supervisor replacement |
| L3 typed ask | K:153 one/incident after failed nudge | Not blocking Orca ask |
| L4 restart | K:154,157-159 proof or person cancel/quiescence; <=1/hour and2/lineage, failed-start rule stricter | WC-13 bars child retry now; future scope must explicitly authorize settlement/retry |
| L5 human report | K:155, S4 every15 | Parent agent not automatic person substitute |
| Silence never | K:182-192 stop/retry/release/fail/person answer/Ruling/lifecycle synthesis | Only L1-L3 authorized, all levels |
| A1 immediate | K:131-138 pending_ack | Distinct each edge |
| A2 five minutes | No ack/ask-return heartbeat -> prompt/transcript/screen | Child heartbeat not M return |
| A3 conditional | One copy/message to positively idle empty prompt | No busy/S11/S4/person-only; no terminal skips |
| A4 fifteen minutes | Report human with ID/answer/receipt/probes | Relay deadline/owner unspecified |
| Settlement | Duplicate ack harmless, unacked-at-settlement | Not child application proof |

C-rule map from D:547-557: C1 silence/probe K:46,182-192; C2 heartbeat K:65; C3 ack K:58,61,131-138; C4 done K:59; C5 WC14 K:63; C6 WC15 K:64; C7 coordinator stack K:95-200/T:199-252 phrase pins; C8 chain K:210-213; C15 person-cancel K:79; C16 actual Skill K:60; C17 own-path stat K:47,110. C9 deleted (exhaustion not proof) D:561. C10-C14 future monitor/hooks/dashboard/context/budget machinery D:563-571 [UNVERIFIED delivery], not #434. D:559 explicitly leaves WC-8/9/13 unchanged.

**Key Takeaways:** lineage budgets and acknowledgments must survive parent replacement; procedural improvements are not permission or measured runtime guarantees.

## 4. Upward channels and issue disposition

| Option | Existing channel / source | Missing boundary |
|---|---|---|
| O1 | Worker ask/check/ack/heartbeat/done + reports/handoffs/notes K:53-65,95-179 | No new hierarchy; further work goes root K:62 |
| O2 | Each Run inbox, explicit status to Run, shared read-only references/person | Peer status not worker_done; no peer control/admission ownership contract |
| O3 | Parent-facing M lifecycle plus child report/question to M Dispatch; A-START/ROUTE/CHECK/ASK/HANDBACK | Still prohibited; aggregate progress/outcome, mixed batch priority, L5 relay, retries and parent-failure ownership undefined; deployed match/live behavior unverified here |
| O4 | Generic non-lifecycle messages, durable result/handoff, upper observation | New protocol (not necessarily type/transport), IDs/completion/ack/deadlines/failure/owner, no lifecycle impersonation |
| O5 | Helper result->parent command; nested contracts K:24-25,46,60 | No per-helper Orca liveness promised; accepted heartbeat gaps; top-level lifecycle only |
| O6 | O1 plus runtime follow-up/time evidence K:246/S:405 | Preserve gates until role/routing/runtime evidence |

Channel suitability: mailbox durable but mixed ack requires single owner; contract durable not wake/subtree-settled proof; compact handoff not supervisor checkpoint yet; notes evidence not active delivery; new unknown type triggers S11, cannot replace protocol design.

Read-only https://github.com/IronbellyOrg/IronClaude/issues/431 and /pull/434: #431 still OPEN, eight historical incidents [UNVERIFIED reproduced]: timer heartbeat during compaction, idle turn, single-file mtime misclassification, closing status filtered out, missed answers35-40min, permission prompt, between-command stops, repeat context exhaustion. Present corresponding K rules respectively :65,113,124; :63,121,152-153; :47,110-113; :59,101-108,127; :61,131-138; :122; :63-64,210-213; :64,159,167-179. #434 merged text/phrase tests K:95-200/T:199-252. It shipped procedural response, not proof all failures eliminated or automatic monitoring. Topology remains person-opened K:69/workers no fanout K:62/D:559/S:405 depth1. New combined duties not defined.

**Key Takeaways:** #431 issues exist without hierarchy; #434 not proof solved; source helper path useful, but supervision/admission/human escalation need contracts.

## Gaps and Questions

[UNVERIFIED] (1) development/installed backend equivalence and active cap; (2) universal agent compliance with sweeps/tokens/ack/handoff/timing; (3) #431 elimination; (4) exact middle permissions including retry/cancel/worktree/merge/outward; (5) aggregate progress/final result; (6) mixed parent-child whole-batch handling; (7) child ownership when M blocked/fenced/exited/replaced (handback not full monitoring transfer, heartbeat not selected unread handback report); (8) L5 actual human relay; (9) handoff40-line adequacy; (10) D5 trigger evidence; (11-15) K:196-200 default waits/missed-answer cause/attention categories and delay/typing during tools/multi-consumer concurrency; (16) full backend report-file validation, so mandatory root read remains; (17) O4 ordinary completion contract; (20) v2 C10-C14 delivered elsewhere not audited. [CODE-CONTRADICTED] (18) older spec incomplete current liveness; (19) #446 old line44 now K:45.

## Stale Documentation Found

- [STALE DOC] S:78-84 lacks current WC14/15/liveness/pending_ack/S11, against K:58-65,95-200 and T:199-252; incomplete current description, not automatic enforcement proof.
- [STALE DOC] #446 lock anchor44 now K:45; proposal not current retry behavior.
- [STALE DOC] D:547-557 historical C-map anchors WC10:44/WC12:59/WC11:45 now K:46/61/47.
- Future-tense v2 is not stale solely unimplemented; D5 not stale merely because current other source supports helpers.

## Summary

Keep O1, O5 internal fanout and O6 for new external hierarchy. Development source offers same-Run helper delivery/reply/handback; main installed source equivalence/live nesting not proved in this slice. #434 adds progress/ack/states/bounded-intervention/handoff procedures but not dual-role authorization or aggregate/ownership policy. Reconsider O3 before inventing O4 if gates met, with own-vs-child outcomes, mixed mailbox, actual human escalation, parent replacement/lineage budgets and deployed runtime verification explicit. No live nested execution/active cap/timing guarantees/build equivalence checked.

