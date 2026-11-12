# Research: Contract authority and role model

**Investigation type:** Architecture Analyst
**Scope:** Worker contract, applied spec, D5 decision, ownership guidance and test pins
**Status:** Complete (static source and policy analysis; full matrix in linked returned evidence)
**Date:** 2026-11-09
**Delivery:** User-approved adaptation: researcher returns findings; coordinator writes this file. No model-tier change.

---

## Evidence and delivery convention

**Full evidence-bearing investigation:** `returned/01-returned-findings.json`, field `text`, preserves the researcher's complete final return verbatim, including the exhaustive seven-part rule-by-option matrix (all WC-2 through WC-15 and section-4 duties), exact quotations, evidence register, proposed authority definition and limitations. This file is an indexed research view, not a replacement for that complete result. Downstream agents must read the JSON text for the complete matrix; the source file was too long to transcribe without duplicate loss. Both files are retained for the anti-omission gate.

Policy quotations establish what current source says, not runtime enforcement. The researcher uses [CODE-VERIFIED] only for actual implementations, [UNVERIFIED] for policy enforcement/proposals, and marks option consequences as inferred. "Holds" is compatibility, not observed execution.

| Alias | Source |
|---|---|
| W / WI | `src/superclaude/core/WORKER-CONTRACT.md` / `/home/coder/.claude/WORKER-CONTRACT.md` (both 328 lines read) |
| S / A | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` / `decisions/APPROVED.md` |
| D5 / D5B / D5M | `.dev/orca-command-refactor/decisions/D5/RECOMMENDATION.md`, `option-b.md`, `debate/adversarial/merged-output.md` |
| C / R | `src/superclaude/core/CLAUDE.md` / root `CLAUDE.md` |
| T | `tests/skills/test_worker_contract.py` (narrow Grep only) |
| H / I | `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` / `src/superclaude/cli/install_core.py` |
| Q / F | `src/superclaude/skills/sc-implement-protocol/refs/qa.md` / `src/superclaude/commands/workflow.md` |
| N | `/opt/Orca/resources/app.asar.unpacked/out/shared/nested-worker-depth.js` |
| P0 | `.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-0.7-depth-trace.md` |

D5 directory enumerated; options/recommendation/merge/invariant probe/contract/log/refactor-plan structure examined. No agents, tests, GitHub calls, Orca mutations/settings/model changes. Auggie/codegraph unavailable to this agent; direct Read/Glob/Grep used.

## 1. Exact role and command boundaries

W:62 and WI:62:
> **WC-13. No Orca fan-out from the worker session.** The worker's top-level session never calls `worker-start`, `dispatch` or `task-create`, Orca's low-level dispatch, or `orca-cli` `worktree create --agent` or `agent launch`, at any depth setting. Work it finds that needs another worker is stated in its `worker_done` body; the coordinator decides (section 4).

W:69 and WI:69:
> These bind the coordinator: an Orca coordinator session the person opened. It plans, creates Tasks, starts workers, reads their reports and performs every outward action.

W:11:
> **Worker run**: a session that received an Orca preamble carrying a Task ID and a Dispatch ID. Only such a session may send lifecycle messages; a session the user started, inside or outside Orca, is an ordinary session.

W:5:
> A coordinator plans the work, creates Tasks, starts one worker per Task and reads each worker's report. Each `/sc:` command stays a self-contained unit of work: one worker (a top-level Claude session in its own Orca terminal) runs one command and reports it with `worker_done`. Commands themselves contain no Orca calls.

W:12:
> **Unattended mode**: the behaviour a command switches to when its caller passes `--unattended`. It is the only command-side change the contract asks for besides report files and resume. It names no Orca command, so the same mode serves any caller that has no person at the keyboard. The mode is selected only by the flag (decision D1). No command detects Orca, its preamble or its environment. The worker session separately applies the brief guard (below).

W:40:
> **WC-8. No Orca fan-out from inside a command.** A command never calls `worker-start`, `dispatch` or `task-create`. Fan-out that needs Orca records is split into separate Tasks by the coordinator.

All quotations directly read; runtime enforcement [UNVERIFIED]. Grep `orchestrator` in W found zero matches. C:57-59/R:312 say creator becomes orchestrator or coordinator under another orchestrator, but C:52-57 preserves supervised dispatch/worker prohibition. This is general ownership language, not implied WC-13 amendment.

| Session | Classification / analytical consequence |
|---|---|
| Live Task/Dispatch preamble | Worker duties/WC-13 apply |
| User-started inside/outside Orca | Ordinary; unattended flag not worker identity |
| Agent-launched, no worker preamble | Not expressly a person-opened coordinator; no-worker does not prove coordinator authority |
| Agent-tool internal helper | W:60 permits internal fan-out but not helper lifecycle messages/top-level worker replacement |

**Key Takeaways:** worktree ownership, command boundaries and session authority are different. Raising depth/new Run/new name does not amend WC-13. Lexical absence of orchestrator is not authority loophole.

## 2. D1 and the two verb lists

A:8/S:401 approve explicit unattended flag plus worker-side guard. D1 does not ban every other option (depth/output flags exist); it bans replacing the worker/person mode selector with environment/preamble detection. A sub flag granting fan-out changes authority/topology, not just configuration.

| Rule | Actor | Calls | Additional boundary |
|---|---|---|---|
| WC-8 W:40 | Command | worker-start, dispatch, task-create | W:5 broader no-Orca-calls instruction |
| WC-13 W:62 | Worker top-level session | Same three plus low-level dispatch, worktree create --agent, agent launch | Any depth setting |

| Option | Mode/command implication (inferred) |
|---|---|
| O1 | No sub switch needed; coordinator session can operate outside commands. Orca-calling slash entry still needs W:5 exception |
| O2 | No second mode switch needed; independent peers require ownership division; Orca-calling command still exception |
| O3 | Scoped D5 alternative is session brief, not command flag; must reopen D5/WC-13 and resolve D1/topology. Session-only calls can preserve WC-8; command calls additionally change W:5/WC-8 |
| O4 | Role may be established outside command; new eligibility/upward authority required; supervised creator still prohibited |
| O5 | Existing internal helper boundary, no sub mode/Orca calls required; preserve WC-7 top-level command/lifecycle |
| O6 | No switch/calls needed now; record future gates |

**Key Takeaways:** WC-8 shorter list is not a loophole; moving calls outside command still hits WC-13; even non-sub orchestrator entrypoint needs deliberate command-boundary decision.

## 3. Rule-by-option compatibility matrix

Assumptions: O1 current root coordinator/workers; O2 independent person-opened peers, each owns Tasks; O3 dispatched worker supervises Orca helpers at session layer; O4 non-dispatched launched owner with unspecified upward protocol (if launched by a worker, violates WC-13); O5 command-owned internal helpers only; O6 defer retaining current rules. All cells inferred, not live results. Full per-clause quotations/matrix are in the preserved JSON sections 5.2-5.7 and must be consumed with this index.

| Rule (W line) | O1 | O2 | O3 | O4 | O5 | O6 |
|---|---|---|---|---|---|---|
| WC-2 no blocking person step (:31) | holds | holds | holds | holds | holds | holds |
| WC-3 questions to coordinator (:53-58) | holds | holds | undefined | undefined | holds | holds |
| WC-4 known report every outcome (:32-39) | holds | holds | undefined | undefined | holds | holds |
| WC-5 own top-level worker_done once (:59) | holds | holds | undefined | undefined | holds | holds |
| WC-6 retry new Task (:71-79) | holds | holds | undefined | undefined | holds | holds |
| WC-7 top-level command (:60) | holds | holds | holds | holds | holds | holds |
| WC-8 command no fan-out (:40) | holds | holds | holds | holds | holds | holds |
| WC-9 outward/local grants (:41-45) | holds | holds | holds | undefined | holds | holds |
| WC-10 long-wait liveness (:46) | holds | holds | undefined | undefined | holds | holds |
| WC-11 distinct writers (:47) | holds | holds | holds | holds | holds | holds |
| WC-12 pulled follow-ups (:61) | holds | holds | undefined | undefined | holds | holds |
| WC-13 no worker Orca fan-out (:62) | holds | holds | breaks | holds | holds | holds |
| WC-14 continuous chains (:63) | holds | holds | undefined | undefined | holds | holds |
| WC-15 context handoffs (:64) | holds | holds | undefined | undefined | holds | holds |
| Person-opened coordinator (:69) | holds | holds | breaks | breaks | holds | holds |
| Root merge-back duty (:224) | holds | holds | breaks if assumed by worker | undefined | holds | holds |
| Root outward action (:229) | holds | holds | breaks if assumed by worker | undefined | holds | holds |
| Root git only quiescent/no frozen plan (:234) | holds | holds | breaks if assumed by worker | undefined | holds | holds |

### Section-4 clause coverage index

The complete JSON matrix has a row for each of the following clauses; these are required downstream inputs, not silently deduplicated omissions.

| W span | Clauses individually covered in complete matrix | Middle-layer findings |
|---|---|---|
| :69,73-79 | eligibility, no retry-of, new retry Task/directory/old ID, three-start cap, no unsettled/unverifiable retry, positive proof + cancellation settlement, no brief update via task-update/send, person-only cancellation/quiescence, ignore late replaced-attempt message | Eligibility breaks O3/O4; retry lineage/settlement authority mostly undefined; safety prohibitions can remain |
| :85-93 | exact unattended command, unique report, blocked policy, quoted grant, historical P0 report conditional, no other outward grant, placement/setup, admission before reuse/release | Composite command identity/grants/placement/admission undefined; uniqueness/no outward defaults compatible |
| :97-114 | run-note timing overrides only coordinator, all message types, whole FIFO replay/ack, write-before-ack/fail-notes-no-ack, unknown S11, attempt quarantine, three-empty-waits inventory, heartbeat not progress, status-S9, actual completion/no synthesis, question/ack clock, escalation L1/L5, decision human, handoff new-work owner, merge human, unexpected dispatch, sweeps/probe budget, W formula, semantic-change definition/deadlines | Mail ownership, status scope, deadlines, parent progress and child progress undefined; non-destructive/human boundaries retained |
| :118-129 | all states S0-S11 with their distinct triggers/actions | Parent/child startup/ask/context/exit/finality/settlement undefined; S1 observable progress, S2 silence-only typed deferral, S11 no typed input compatible |
| :131-143 | no mailbox resend, A1 pending_ack, A2 5-min probe, A3 one positively-idle typed copy, A4 15-min human report, no busy/S11/S4/person prompt typing, no-terminal skips A3, duplicate ack harmless/not truth proof, settlement unacked, one-line typed-message format | Two ack relationships and final disposition undefined; safety constraints unchanged |
| :146-179 | lineage budgets, L0-L5, costly-probe cap, nudge/ask/restart caps, no silence/probe/context as stall proof, repeated cause no plain restart, reduce-load successor, no redo completed steps, resume-note position/new directory/implement priority, resume fields | Subtree lineage, restart ownership, human escalation and child state in handoff undefined; protected proof requirements retained |
| :182-200 | silence never authorizes stop/retry/release/fail/person answer/Ruling/lifecycle synthesis; only L1-L3; wait/answer/attention/typing/multi-consumer uncertainty register | All protections retainable; runtime unknowns not facts |
| :204-216 | guard before labelled commands, Task not starts slash, refusal runs nothing, chain before commands, worker-visible copies, exact token-preserving rerun | Child aggregation chain behavior undefined; source-copy/guard discipline retained |
| :220-225 | Orca/default paths, one feature coordinator, authorized setup skip default, setup success before dispatch, placement map, absolute reports, distinct implement slugs, resume same child, admitted merge/remove/discard/conflict stops, protected deletion/no duplicate managed package | One-root placement/cleanup ownership undefined or worker conflict; safety guards retained |
| :229-235 | named user outward authorization, fork/no upstream links, evidence-backed posts, ordinary PR owner, unseen commits review, one-Task expiring grants, quiescent git/explicit staging/commit-only/hook no bypass, PR owner recorded | Broad ownership not inherited; human/fork/freeze constraints retainable |
| :239-246 | read/admit outcomes; failed/blocked no dependents; guard-refusal bounded new Tasks; dependencies only after admitted actual inputs; start only self-created Tasks; unknown Task to person; runtime split/time evidence | Upper/lower admission/retry/splitting responsibility undefined |
| :250-269 | frozen plan/worktree, no writing/shared git/merge/removal, narrow E-RESUME exception, person handback plus ledger checks, all Ruling eligibility/format/baseline/settlement checks, no force, same halted path/worktree | Freeze protections retainable, authority lifting remains person-owned, worker cannot invent resume consent |
| :273,275-281 | all fan-in inputs settled/admitted; failed/blocked new Task or recorded drop; <=10 inputs; replacements not extra; >=2 admitted inputs required; example restates rules | Aggregate admission undefined, input-count safeguards compatible |

**Key Takeaways:** O3 conflicts directly; O4 no-worker is not coordinator eligibility; most hard safety rules survive but routing/aggregation/recovery lack a defined owner.

## 4. Required authority definition and allocations

Proposed consistency definition (NOT current authorization): subordinate coordinator is separately identified, has bounded planning/supervision scope, named upward owner, exclusive self-created Task ownership and reporting channel. Role name grants no launch/outward/user-approval/transferable-grant authority. Dispatched workers remain WC-13-bound until approved replacement.

| Duty | Existing boundary | Required allocation |
|---|---|---|
| Suggest split/proposed briefs | W:62,83-91 | Can advise/prepare text, not create/start Task by implication |
| Create/start children | W:62,69,246 | Not worker today; need eligibility, exception, scope/count/ownership |
| Start foreign Task | W:246 | No; preserve exclusive creator/start or explicitly replace |
| Local commit grant | W:42-43,88,233 | Task-specific user's exact words; parent grant not child consent |
| Push/publish/post/install/paid run/shared merge | W:41,90,229-234 | Never worker under current D4; O4 no automatic inheritance |
| Child placement/setup/merge/removal | W:47,62,91,220-225 | Explicit creator/isolation/setup/report/admission/freeze/conflict/removal owner |
| Ruling | W:57; A:9; Q:254 | Agent message cannot substitute human acceptance |
| Clarification | W:53-58 | Eligible brief-fixed ordinary questions only; budgets/escalation/late answers per edge |
| Liveness/check/ack | W:95-192 | One consumer/intervention owner per worker; own vs child progress separated |
| Completion | W:59,108 | Own lifecycle only; no synthetic child_done; aggregate admitted outcomes explicit |
| Retry/release subtree | W:73-79,146-159 | Lineage caps, orphans, ordering, parent-failure takeover |
| Frozen implement | W:250-269 | Human-only resumption, writers frozen, same halted path and baseline |

Never infer user consent/Ruling/grant widening, worker external fan-out/outward acts, helper lifecycle impersonation, destructive silence recovery, or owner-name override of freezes/deletion checks.

**Key Takeaways:** planning text easier to delegate than operational authority; both directions need contracts; current human/lifecycle authority cannot be manufactured.

## 5. Verified implementations and test limits

[CODE-VERIFIED] I:32-75 install_core_files lists known core docs, enumerates Markdown, skips existing without force, copies with shutil.copy2. Does not prove all machines fresh. H:94-102 scanner tracks words/flags only; H:342-357 Bash parser/message not hierarchy permission. N:7-10 constants root0/max1; :21-26 validates configurable max; :11-15 formats refusal, not proof all handlers call it.

T (Grep-only): WC-8/WC-13 headings :123/:155; _check_rule :755-758 phrase presence; parametrized test :907-909, not nested worker exercise. _ORCA_NAME_RE :843-845 literal executable/subcommand matcher, not universal process detector; unattended scan :885-886 rejects source-tree refs/Orca text, not new coordinator exception. F:68-76 is actual command instruction for explicit unattended/report/propagation/no outward; Q:254-256 excludes other-agent approval and invented acceptance, but compliance runtime [UNVERIFIED]. No orchestrator-named command/skill found by bounded source filename search.

## Gaps and Questions

All policy behavior enforcement universally [UNVERIFIED]; holds cells are compatibility only. Unresolved: agent-launched O4 eligibility; O3 composite aggregate contract/question budget/completion/admission; current all-six launch fences (N helper not call graph); historical bundle not current; helper mailbox/ack/fence/Run isolation; W:196-199 wake/missed-answer/attention-delay/typed-input unknowns; active settings/profile reload/safe lowering/per-Run override; qualifying runtime-split evidence; subtree retry/pending-ack/freeze/removal transfer; grants not inheritable; generalized owner vs person-opened coordinator; S:88 setup-run vs W:221 skip; S:61 never-worker list omits issue while W:23 includes; Q generic genuine confirmation vs worker-specific Ruling restriction; W:5 exception for new Orca-calling command. [CODE-CONTRADICTED citation only] historical P0 constants :11/13/30-35 now N:7/9/21-26.

## Stale Documentation Found

| Source | Disposition |
|---|---|
| D5B:3,22 vs D5M:76 | [STALE DOC] Original command-fan-out proposal replaced by session-only/no command edits |
| D5B:13 | [STALE DOC] Raise does not prove removal of every fence; N retains valid integer max |
| D5:64,67 | [STALE DOC] Unapplied/undecided drafting status superseded A:8-13,S:401-406,W |
| S:88 vs W:221 | [STALE DOC] Old setup-run vs authorization-sensitive skip default |
| S:61 vs W:23 | [STALE DOC] Old never-worker list lacks issue |
| P0:7,20,25 | [STALE DOC] Bundle/line anchors changed, full current call coverage not proven here |
| C:52-59/R:312 | Not proven stale; broad owner role incomplete, surrounding worker restrictions persist |

## Summary

Current policy denies a supervised middle tier: WC-13 covers six routes at any depth, section 4 requires person-opened coordinator. Ownership wording does not define subordinate authority/upward reporting/exemption. Session-layer O3 needs D5/WC-13 reopened; an Orca-calling orchestrator command separately needs no-Orca-command boundary decision even without sub mode. Recommend O6 on proposed mode with O1 current and O5 internal helpers; require composite brief, material measured runtime split, current trace, routing/ack/fencing, exclusive ownership/retry/freeze rules, and preserved human authority. All detailed per-clause matrix/evidence remains in the linked exact returned JSON. No live behavior/tests/full handler tracing checked.

