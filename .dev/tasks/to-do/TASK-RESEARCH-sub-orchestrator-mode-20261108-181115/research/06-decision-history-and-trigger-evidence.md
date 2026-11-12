# Research: Decision history and revisit evidence

**Investigation type:** Doc Analyst
**Scope:** Decisions D1-D5, applied spec, change records, P0-P2 evidence and run notes
**Status:** Complete (static and historical evidence; live uncertainties retained)
**Date:** 2026-11-09
**Delivery:** User-approved adaptation: researcher returns findings; coordinator writes this file. No model-tier change.

---

## Evidence conventions and source index

Coordinator transcription of the researcher's returned findings. [CODE-VERIFIED] for Markdown primitives confirms the current shipped instruction, NOT mechanical enforcement or universal compliance. [CODE-CONTRADICTED] marks conflict with current source; [UNVERIFIED] marks documentary evidence without established runtime behavior, authority or measurement. Researcher personally read cited spans and re-read load-bearing spans. No agents, GitHub or Orca operations, tests, installs or model changes were run.

| Key | Worktree-relative source (DEPTH is absolute) |
|---|---|
| SPEC | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` |
| REC | `.dev/orca-command-refactor/decisions/D5/RECOMMENDATION.md` |
| D5-A / D5-B | `.dev/orca-command-refactor/decisions/D5/option-a.md` / `option-b.md` |
| APPROVED | `.dev/orca-command-refactor/decisions/APPROVED.md` |
| DISPOSITION | `.dev/orca-command-refactor/review/disposition-round4.md` |
| CR01 | `.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md` |
| EVAL326 | `.dev/orca-command-refactor/review/issue-326-evaluation.md` |
| D2-PLAN / D3-PLAN / D4-PLAN / D5-PLAN | `.dev/orca-command-refactor/decisions/D2/debate/adversarial/refactor-plan.md` and corresponding D3, D4, D5 paths |
| CONTRACT | `src/superclaude/core/WORKER-CONTRACT.md` |
| CORE | `src/superclaude/core/CLAUDE.md` |
| QA | `src/superclaude/skills/sc-implement-protocol/refs/qa.md` |
| PR-SKILL | `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` |
| TEST | `tests/skills/test_worker_contract.py` |
| DEPTH | `/opt/Orca/resources/app.asar.unpacked/out/shared/nested-worker-depth.js` |
| P0 | `.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/p0-phase-report.md` |
| TRACE | `.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-0.7-depth-trace.md` |
| P1 | `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/p1-phase-report.md` |
| P2 / P2-FOLLOWUPS | `.dev/tasks/done/TASK-WF-writeTheP2Static-20261107-011441/artifacts/p2-static-report.md` / `follow-ups.md` |
| FOLLOWUP-SOURCE | `.dev/tasks/done/TASK-WF-workerContractFo-20261106-214402/source.md` |
| DEFERRAL | `.dev/reflect/pre-TASK-WF-enforceTheOwnerP-20261108-031809-20261108033529/REPORT.md` |

## 1. Decision from this slice

Retain O1 operationally with O6 evidence gates. Do not interpret creator ownership as permission for an O3 worker to start helpers.

| Finding | Evidence |
|---|---|
| Supervised middle layer not currently permitted | [CODE-VERIFIED] CONTRACT:62 bans six Orca routes at any depth; SPEC:81,405 agree |
| Two-part revisit trigger not established | [CODE-VERIFIED] No autonomous composite brief; fixed Command lines and WC-13 remain. [UNVERIFIED] No qualifying measured runtime-split record found |
| AC-0.7 completed historically | P0:18 PASS and TRACE:46-59 accepted historical trace; [UNVERIFIED] full current-version call coverage |
| Depth-2 mailbox unestablished | [UNVERIFIED] REC:49 requires it, REC:84 leaves it open; inspected evidence/contract do not establish it |
| Creator ownership does not repeal WC-13 | [CODE-VERIFIED] CORE:52-59 preserves supervised dispatch/worker ban; DEFERRAL:77-78 excludes supervised workers/WC-13 from ownership change |

**Key Takeaways:** potential benefit is not qualifying measured evidence; ordinary-session ownership, worktree ancestry and supervised dispatch depth are distinct; the contract remains the execution boundary.

## 2. Separate D5 texts and governing authority

### Applied spec row, SPEC:405 (verbatim)

```text
| D5 | Option (a): nesting depth stays 1, the coordinator is a session the person opened, and the worker session never starts Orca work (WC-13). Revisit only when a composite brief type is defined in this spec and the coordinator's run notes record a real run whose split was knowable only at run time and whose extra round trip was material; before any raise, AC-0.7's trace is done. | R1, WC-13, 2.3, non-goal 2, AC-C6, AC-0.7 |
```

### Recommendation, REC:49 (verbatim content)

> - Revisit only when both hold: a composite brief type is defined in this spec, and the coordinator's run notes (section 2.3) record a real run whose split was knowable only at run time and whose extra round trip was material. Before any raise: AC-0.7's trace is done, and the mailbox that receives a depth-2 worker's questions and `worker_done` is established.

| Condition | SPEC:405 | REC:49 |
|---|---|---|
| Defined composite brief | Required | Required |
| Real runtime-only split plus material extra round trip | Required | Required |
| AC-0.7 before raise | Required | Required |
| Establish depth-2 questions AND worker_done mailbox | Not stated | Required |

[CODE-VERIFIED] CONTRACT:62 governs current execution. SPEC:405 is the applied design record. DISPOSITION:48 explicitly marks the full D5 replacement "Superseded by the short record"; :103 explains short decision records. [UNVERIFIED] Whether losing the mailbox clause was deliberate or summarization loss: APPROVED:5,12 originally directs section-4 recommendation wording; DISPOSITION:48 says precondition/trigger kept but does not discuss omission. Omission proves neither working routing nor a conscious waiver. Either reading still prevents a raise because the two revisit conditions are not established.

**Key Takeaways:** separate citations matter; mailbox discrepancy is real; it is not a working upward channel.

## 3. Trigger evidence

| Trigger part / pre-raise item | Evidence searched | Result / decision |
|---|---|---|
| Composite brief defined in spec | Entire SPEC; CONTRACT terms/duties/layout/template; distributable-source search for Sub-workers, composite brief, depth-2 and sub-orchestrator | Not found. [CODE-VERIFIED] SPEC:86 and CONTRACT:204-216 allow prewritten Command chains; CONTRACT:60,63-64 govern execution/handoffs; :62 still bans creating Orca work. A chain is not autonomous delegation. Not met |
| Real unforeseen split with material round-trip cost in notes | P0/P1; P2 static/follow-ups; coordinator-named artifacts; completed TASK-WF Markdown/text/JSON searches for follow-up Tasks, notes, runtime splits, extra time/round trips | No qualifying combined record. [UNVERIFIED] Follow-ups exist but do not establish runtime-only decomposition AND measured material extra coordination latency. Not established |
| AC-0.7 done before raise | P0 report and underlying TRACE | Found historical completion: P0:18 PASS; TRACE:48-53 all six routes; :59 root depth. [UNVERIFIED] Current complete coverage |
| REC additional mailbox prerequisite | REC open items, D5-PLAN, phase reports, CONTRACT and depth-2/mailbox searches | [UNVERIFIED] Not established. D5-PLAN:105 requires; REC:84 open; CONTRACT:200 leaves two-consumer behavior unverified and prescribes one wait/Run. SPEC omits this prerequisite |

### Phase evidence: what does not establish the split trigger

| Artifact | Observed content | Why insufficient |
|---|---|---|
| P0:33-35,45-49 | [UNVERIFIED historical execution] Three successful single-command checks, command durations and heartbeat gaps | Long command/gap is not measured extra cost of runtime-only splitting |
| P1:8-12,117; APPROVED:79-83 | Original two FAIL checks and 11 workers without Skill calls; later approval reclassified checks and accepted P1 PASS; [CODE-VERIFIED] CONTRACT:60 now requires actual Skill invocation | Compliance acceptance, not decomposition-latency evidence; do not report original FAIL as final phase disposition |
| P2:3,19 | Static PASS; report explicitly delegates live checks/phase report to separate plan; no P2 live phase report found in searched done/to-do TASK-WF packages | Static conversions are not live split/cost measurement |
| P2-FOLLOWUPS:3-9 | Omitted wording/new nested calls and follow-ups; [UNVERIFIED] defects not independently reproduced | Does not record qualifying Task plus unknowability plus added time |
| FOLLOWUP-SOURCE:7 | Three PR #411 review follow-ups excluded from prior scope; [UNVERIFIED] GitHub history not re-established | Follow-up work not measured coordination penalty |
| P2:206 | Four brief-guard refusals from command-copy disagreement; ordinary subagent debates instead. [CODE-VERIFIED] Refusal consistent with CONTRACT:16-20; [UNVERIFIED] historical dispatches | Installation/copy drift, not evidence a depth-2 parent would avoid material splitting overhead |
| Coordinator-named files | Missing-summary retry and execution constraints | Neither contains qualifying timing record |

Coordinator-named files inspected: `.dev/tasks/done/TASK-WF-fixTheScIssueWor-20261104-162205/artifacts/coordinator-message.md:3-7` and `.dev/tasks/done/TASK-WF-scIssueCommand-20261104-064713/artifacts/coordinator-constraints.md:1-4`. No run-notes/coordinator-notes filename-pattern match found. This is bounded checkout-search negative evidence, not proof that notes do not exist elsewhere.

### Historical AC-0.7 versus current code

| Route | TRACE result |
|---|---|
| worker-start | Checked (:48) |
| dispatch | Checked (:49) |
| low-level dispatch --inject | Checked (:50) |
| task-create | Not checked (:51) |
| worktree create --agent | Not checked (:52) |
| agent launch | Not checked (:53) |
| Person-opened terminal without dispatch/remote attachment | Depth 0 (:59) |

[UNVERIFIED current complete coverage] The recorded minified bundle path no longer exists. [CODE-VERIFIED] Current DEPTH:7-10 still defines default max 1/root 0/error; `resolveNestedWorkerMaxDepth(settings)` :21-26 accepts safe positive integer, invalid falls back to 1; refusal formatting :11-14 uses supplied max. These functions do not establish which current entrypoints call them.

**Key Takeaways:** AC-0.7 historically complete; it found routes relying on contract/transcript protection; elapsed command runtime must not substitute for split-latency evidence.

## 4. Final D5 option (b): value and five costs

Final debated form: raise exactly to 2, only when brief says `Sub-workers: allowed, max N`; worker TOP-LEVEL session starts helpers, not command body (REC:48; D5-PLAN:81-91). [CODE-CONTRADICTED as current permission] CONTRACT:62 prohibits it.

| Cost in REC:48 | Current check |
|---|---|
| Undefined composite brief | [CODE-VERIFIED] Current layout is chains, not autonomous scope. [STALE DOC] Brief-is-one-command rationale contradicted by SPEC:86/CONTRACT:204-216 |
| Parent becomes second orchestrator running full coordinator loop | [CODE-VERIFIED rule distinction] CONTRACT:69 assigns coordination, :62 denies worker dispatch. [UNVERIFIED] No demonstrated nested loop |
| Questions probably reach root Run, not parent | [UNVERIFIED] REC hedges; REC:49 and D5-PLAN:105 demand routing evidence |
| WC-13 exception needed | [CODE-VERIFIED] CONTRACT:62 contains none |
| Brief scoped to IronClaude but depth raise affects profile runs | [UNVERIFIED full scope] DEPTH:21-26 reads setting; profile propagation/reload not independently traced; SPEC:276 also leaves reload open |

Potential value (REC:20,48): separately tracked child records/liveness/retry and one saved coordinator wake/read/Task creation per runtime split. [UNVERIFIED] No measured saving or successful nested run found. Original D5-B:3,22 proposed command calls/rewrites, but final REC:48 says no command-file changes. [CODE-CONTRADICTED] Original D5-B:13 "removes" fence: DEPTH:11-26 retains configurable positive max; accepting 2 does not disable it.

**Key Takeaways:** surviving benefit concerns unforeseen worker-session decomposition; a setting alone provides neither scope, routing nor authority; evaluate corrected option, not superseded command-calls-Orca version.

## 5. D1-D4 and git ownership

| Decision | Shipped/approved evidence | Middle-layer consequence |
|---|---|---|
| D1 explicit mode | [CODE-VERIFIED] APPROVED:8; SPEC:401; CONTRACT:12 no environment/preamble detection, :13 standalone-token parse, :16-24 guard vs nested propagation | Do not infer unattended mode from session hierarchy; preserve explicit flag and distinction between command and session |
| D2 person-only Rulings | [CODE-VERIFIED] APPROVED:9; SPEC:402; CONTRACT:57 and :250-268; QA:249,254-256 rejects invented approval/agent messages; D2-PLAN:40-58 freeze rationale | Middle coordinator cannot approve a halted child's work, relay a Ruling as authority or auto-retry frozen plan |
| D3 pr-submit never worker | [CODE-VERIFIED] APPROVED:10; SPEC:403; CONTRACT:23,232; PR-SKILL:43-49 top-level/in-session; D3-PLAN:14-26 ordinary vs worker carriage | Supervised middle layer gets no PR-worker permission; ordinary handoff is not supervised-helper authorization |
| D4 local commit grant | [CODE-VERIFIED] APPROVED:11; SPEC:404; CONTRACT:41-45 requires word-for-word Task-specific grant, sole child-worktree occupancy, succeeded status, post-command commit/no push; :233 expires at worker_done; D4-PLAN:28-46 | No invented transferable grant/general outward owner. Child grant inheritance undefined |
| Git ownership | [CODE-VERIFIED] SPEC:406-407; CONTRACT:229-235 outward/merge/cleanup belongs to coordinator under human authority; D4 wins conflicts; APPROVED:18 drops per-PR worker opt-in | One explicit outward owner; hierarchy does not authorize competing push/merge/cleanup/publication |

Current result flow [CODE-VERIFIED shipped instructions]: coordinator supplies exact commands/report/policy/grant; worker invokes command at top level; nested command contracts propagate (CONTRACT:24-25); top worker reports (:59); coordinator admits results before dependents (:239-246); further Orca work goes back to coordinator (:62). O3 changes brief authoring, reporting, admission and further-work ownership; O5 remains internal, not a new lifecycle owner.

[CODE-VERIFIED] CORE:55-59 names a middle role but also preserves worker-contract prohibition. DEFERRAL:78 explicitly excludes WC-13. [UNVERIFIED] Neither ordinary upward reporting nor supervised depth-2 routing follows from ownership text.

**Key Takeaways:** preserve explicit mode/human authority/PR carriage/Task-scoped grants; deferral is not an exception approval.

## 6. Six-option implications

| Option | Assessment |
|---|---|
| O1 two tiers | [CODE-VERIFIED] CONTRACT:62/SPEC:405; retains coordinator round trip; no material-cost measurement found |
| O2 person-opened peers | [CODE-VERIFIED] Fits coordinator requirement; [UNVERIFIED] peer reporting/ownership protocol; not supervised parent-child |
| O3 supervised helpers | [CODE-CONTRADICTED as allowed] WC-13/D5; potential saving, but brief, measured need and routing unestablished |
| O4 handoff owner | [CODE-VERIFIED] CORE recognizes creator ownership/middle-role words outside supervised exception; [UNVERIFIED] authority/upward channel; must not route around worker ban |
| O5 Agent-tool helpers | [CODE-VERIFIED] CONTRACT:60 preserves internal fan-out, but command stays top-level and lifecycle messages remain top-level worker; not separately supervised children |
| O6 defer with gates | Retain O1 pending defined composite brief, qualifying measurement and resolved routing; explicitly reconcile SPEC/REC mailbox discrepancy |

**Key Takeaways:** O3/O4 differ in authority/reporting; O5 is existing local fan-out; decision-history evidence supports deferral, not a new mode design.

## Gaps and Questions

| Gap | Status / consequence |
|---|---|
| Qualifying runtime split | [UNVERIFIED] No combined Task/unknowability/material-added-time evidence in bounded checkout search; notes may exist elsewhere |
| Composite brief | [CODE-CONTRADICTED if claimed current] Command chain is not dispatch permission |
| Omitted mailbox prerequisite | [UNVERIFIED intent] Summarization record does not explain omission |
| Depth-2 routing/fan-in/consumer ownership | [UNVERIFIED] No source-backed route/live demonstration in this slice |
| Current six-call depth coverage | [UNVERIFIED] Old bundle absent; constants read, full new call graph not retraced |
| Current profile/reload/safe lowering/per-run override | [UNVERIFIED] P2:14 historically 1; current config not read, no reload/active-depth probe; full profile propagation not traced |
| Markdown-rule universal compliance | [UNVERIFIED] TEST:155,907-909 phrase-pins WC-13; no tests run, no universal compliance proof |
| P2 live phase report | [UNVERIFIED/not found] P2:3 assigns separate live plan |
| Transitive grants/outward owner | [UNVERIFIED] No grant inheritance found; current grants Task-scoped |
| Ordinary handoff upward path | [UNVERIFIED] Ownership not a question/completion protocol |
| Historical contradicted statements | [CODE-CONTRADICTED] Listed below; not treated as current permission/runtime proof |

## Stale Documentation Found

| Historical statement | Current evidence |
|---|---|
| [STALE DOC] REC:3 spec not edited | [CODE-CONTRADICTED as current] SPEC:81,405 applied; CONTRACT:62 ships WC-13 |
| [STALE DOC] REC:64 none applied yet | [CODE-CONTRADICTED] SPEC:81,98,276,315,386; DISPOSITION:48-58 application record |
| [STALE DOC] CR01:3 not applied | [CODE-CONTRADICTED] SPEC:79,88; CONTRACT:47,220-225 |
| [STALE DOC] D5-A:19 smoke-run trigger | [CODE-CONTRADICTED current trigger] SPEC:405 two parts; D5-PLAN:95-105 replaces smoke wording |
| [STALE DOC] REC:20,48 one command per brief | [CODE-CONTRADICTED] SPEC:86, CONTRACT:204-216 multiple lines; DISPOSITION:105 D1 layout prevails; still not autonomous scope |
| [STALE DOC] Old SPEC:79/350-354 anchors | [CODE-CONTRADICTED locations] Current :79 WC-11, :84-86 layout, :405 D5 |
| [STALE DOC] REC:9 spec never states root-coordinator precondition | [CODE-CONTRADICTED] SPEC:386,405; CONTRACT:69 |
| [STALE DOC] REC:10 worker session has no rule | [CODE-CONTRADICTED] CONTRACT:62 explicit ban |
| [STALE DOC] D5-B:3,22 command rewrites | [CODE-CONTRADICTED final option] REC:48 worker-session fan-out/no command changes; CONTRACT:40 command ban |
| [STALE DOC] D5-B:13 raise removes fence | [CODE-CONTRADICTED] DEPTH:11-26 configurable positive max/invalid fallback |
| [STALE DOC] REC:67-72 unresolved D1-D4/git stub | [CODE-CONTRADICTED current outcome] APPROVED:8-13; SPEC:401-407; current CONTRACT |
| [STALE DOC] CR01:19 PR-worker trigger | [CODE-CONTRADICTED] CONTRACT:23,232; APPROVED:18 drops opt-in |
| [STALE DOC] CR01:15 unconditional issue/PR linking | [CODE-CONTRADICTED] CONTRACT:230 fork-only/no Orca links while upstream identity; DISPOSITION:102 drops wording |
| [STALE DOC] CR01:24/SPEC:88 default setup-run | [CODE-CONTRADICTED newer instruction] CONTRACT:221 skip default, setup only with specific authorization |
| [STALE DOC] EVAL326:80 depth 1 only stops workers starting workers | [UNVERIFIED blanket current claim] Historical TRACE:51-55 alternate routes not fenced; CONTRACT:62 broader; sentence cannot prove all child-session creation mechanically blocked |
| [STALE DOC if final disposition] P1:8 FAIL | APPROVED:79-83 later PASS/accepted exceptions; [CODE-VERIFIED] CONTRACT:60 actual Skill requirement now settled |
| [STALE DOC] Historical depth source lines/bundle | TRACE:25 old constants :11/:13, current DEPTH :7/:9; old minified bundle absent; full current coverage [UNVERIFIED] |

**Key Takeaways:** use historical reasoning, not stale status/single-command/undecided assertions; even applied spec lags on setup wording and mailbox clause.

## Summary

D5's revisit trigger is not established: no autonomous composite brief is defined and no qualifying measured runtime-only split record was found. AC-0.7 was completed historically, not a current six-route audit or depth-2 routing proof. SPEC omits REC's mailbox condition; CONTRACT still prohibits worker-session Orca fan-out. D1-D4 preserve explicit mode, human-only Rulings, ordinary PR sessions and local Task grants, not general middle-layer authority. Retain O1 with O6 evidence gates; reconsider only after brief, measured need and routing are established and the D5 texts reconciled.

Not checked: live nested workers, current settings changes, GitHub history, or full changed-bundle call graph. Risk: treating historical tracing/ownership wording as current permission or demonstrated nested supervision.

