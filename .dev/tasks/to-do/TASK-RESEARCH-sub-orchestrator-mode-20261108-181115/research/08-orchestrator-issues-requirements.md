# Research: Orchestrator issue requirements

**Investigation type:** Doc Analyst
**Scope:** Fork issues 339, 423, 431, 409, 326, 446; PRs 422 and 449; prior issue-444 analysis
**Status:** Complete (issue/source requirements; runtime claims qualified)
**Date:** 2026-11-09
**Delivery:** User-approved adaptation: researcher returns findings; coordinator writes this file. No model-tier change.

---

## Evidence conventions and complete result

Complete returned investigation, including every issue requirement R01-R35, exact comments/quotes, all conflicts, sources and bounded negatives, is preserved verbatim in `returned/08-returned-findings.json`, field `text`. Read that complete text with this index at synthesis/QA; no requirement should be omitted because this summary is shorter. [GH-OBSERVED] is observed record/text, not implementation. [CODE-VERIFIED] instruction source proves text, not compliance; [UNVERIFIED] proposal/runtime not established; [CODE-CONTRADICTED] current code differs.

Aliases: WC=`src/superclaude/core/WORKER-CONTRACT.md`; CORE same CLAUDE.md; HOOK=`src/superclaude/hooks/scripts/require-orca-worktree-agent.sh`; HOOK-REG same hooks.json; TEST=`tests/skills/test_worker_contract.py`; ISSUE-CODE=`src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`; CCSESSION=`src/superclaude/skills/ccsession-tag/ccsession`; D5=`.dev/orca-command-refactor/decisions/D5/RECOMMENDATION.md`; SPEC/APPROVED corresponding spec/approval; DEV-GUIDE=`docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`; STYLE=`src/superclaude/output-styles/pragmatic.md`; CR-01 change record; P0=`.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/p0-phase-report.md`; DEPTH-CODE=`/opt/Orca/resources/app.asar.unpacked/out/shared/nested-worker-depth.js`; SEND-CODE=`/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/orchestration/message-send-handler.js`.

All six assigned issues/comments, PR422/449, prior analyses and relevant source read with fork-explicit read-only calls. No files/external state/permissions/models changed. Filename search found no dedicated orchestrator primitive, not proof no design elsewhere.

## 1. Issue 339 requirement inventory

https://github.com/IronbellyOrg/IronClaude/issues/339 comments read:
- C1 #issuecomment-6659516712 polling/cleanup/hierarchy.
- C2 #issuecomment-6659559030 permission incident/typed protocol/grants.
- C3 #issuecomment-6703399956 research/adversarial choice.
- C4 #issuecomment-6703934716 historical accuracy.
- C5 #issuecomment-6703934983 claim/brainstorm estimate.

V1-independent means applicable without hierarchy, NOT shifting later security work into v1. C2 explicitly schedules typed messages/grants later.

| ID | Requirement/source | Applicability | Present evidence / conflict |
|---|---|---|---|
| R01 | Manage10-20 sessions/body | V1 | [UNVERIFIED] target not measured capacity |
| R02 | Main orchestrator/routes child questions/updates/body | V1 | WC:53-61 supervised flow; persistent all-session mode [UNVERIFIED] |
| R03 | No manual child interaction/body | V1 | [CODE-CONTRADICTED absolute] Human Rulings/ordinary PR session WC:57,232 |
| R04 | Hour/two sweeps/body | V1 | WC:99-114 more frequent live procedure; named all-session sweep absent |
| R05 | Configurable recent-window default6h sweep last messages/progress/block/next/body | V1 | [UNVERIFIED] named command/interface; historical inventory != live worker sweep |
| R06 | Close finished/recover timeout/refusal/remind human/body | V1 | WC:73-79,118-159 recovery; timeout/refusal alone not authority |
| R07 | Poll until done/cleanup/closed/C1 | V1 | Wait/sweep WC:99-110, full invariant [UNVERIFIED] |
| R08 | Strict worktree/branch cleanup/body,C1 | V1 | WC:224-225 protections/admission WC:239-246 |
| R09 | Valuable files committed/all commits pushed before delete/body | V1 | WC:225 protected state; universal pushed predicate [UNVERIFIED] |
| R10 | Exclude logs/artifacts/reports/plans as valuable/body | V1 | [CODE-CONTRADICTED blanket] WC:234 task staging/:225 unread reports/ledgers |
| R11 | Prefer worktree/branch per possible prompt/body | V1 | [CODE-CONTRADICTED universal] Conditional isolation WC:47,218-225 |
| R12 | Permanent role flag/inform later sessions/body | V1 | [UNVERIFIED] registry absent; WC:11 preamble identity |
| R13 | Replace summary tables/static report/body | V1 | [CODE-CONTRADICTED] STYLE:22 DONE/NEXT no exceptions |
| R14 | Persistent attention until satisfied/body | V1 | WC:131-138 ack vs outcome; all-session persistent display [UNVERIFIED] |
| R15 | Report every3-5min/#409/body | V1 | [UNVERIFIED] implementation; #409 observer not controller |
| R16 | Management server relay/body | V1 | [UNVERIFIED] endpoint/owner unspecified |
| R17 | Incorporate orchestration skill/body | V1 | Stub read/WC:5-7,69 boundaries; future integration undefined |
| R18 | Orchestrator-of-orchestrators v2/C1 | SUB | [CODE-CONTRADICTED current permission] WC:62/69 if supervised |
| R19 | Hierarchical safeguards without repeated confirms/C1 | SUB as stated | [UNVERIFIED] delegated authority/confirmation-free path |
| R20 | Same permission-mode class/isolated workspace/C2 step1 | V1 immediate workaround proposed | CCSESSION:134-141 exposes flag overrides; behavior not reproduced, no permission-change authority from issue |
| R21 | Orchestrator avoids untrusted content/reports data/C2 | V1 safety | [UNVERIFIED] enforced separation/parser |
| R22 | Fixed six types status/question/done/request_sweep/request_close/resume/C2 step2 | V1 applicability, later release | WC:101 nine Orca types differ; mapping unimplemented |
| R23 | Typed IDs/worktree/branch, free text detail inert/C2 | V1 applicability later | WC:106 selected attempt identity checks not full data-only validator |
| R24 | Inbound hook enforcement else script-validated files/C2 | V1 prerequisite | [UNVERIFIED] inbound boundary; return contracts not automatically security parser |
| R25 | Signed expiring scoped per-child grants/C2 step3 | V1 applicability later | [UNVERIFIED] macaroon/Biscuit; WC:41-43 narrower local commit grant |
| R26 | Session binding/nonce/replay/offline verification/C2 | V1 applicability later | [UNVERIFIED] end-to-end verifier; existing nonce/capability not assumed equivalent |
| R27 | Root grants set of worktrees/sub attenuates only/C2 | SUB | [UNVERIFIED] format/enforcement; WC:62 currently bans worker children |
| R28 | Explicit destructive caveats + clean/merged PR/closed session/C2 step4 | V1 safeguards, sub delegation extends | WC:225,229-234 current checks; token/closed-session enforcement not established |
| R29 | Keep dangerous-removal safeguard/not cryptography-only/C2 | V1 | [UNVERIFIED] external safeguard untested; auth not poisoned-instruction prevention |
| R30 | How sender marks bypass for delivery/C2Q1,C3 | V1 transport | [UNVERIFIED] wrapper launch flag doesn't answer identity |
| R31 | Inbound hook inspect/refuse/C2Q2,C3 | V1 transport | [UNVERIFIED] interception mechanism |
| R32 | Research Q1/Q2 before layer/C2,C3 | V1 prerequisite | Completion not established |
| R33 | Maintained Python/Node macaroon vs Biscuit + adversarial/C2Q3,C3 | V1 grant choice, sub attenuation later | [UNVERIFIED] comparison/library decision/literature benchmark |
| R34 | Typed steps2/3 before hierarchy/C2 recommendation | SUB prerequisite | Proposed gates not completed features |
| R35 | Deep brainstorm first/C5 | V1 suggestion | Proposed step not executed/authority;40h estimate unverified |

C4 accuracy is not additional acceptance criteria. Detailed issue quotations/source evidence in exact JSON.

**Key Takeaways:** most supervision/cleanup requirements independent of sub mode; fixed messages/grants applicable flat but scheduled later; attenuation/delegated supervisor specifically hierarchical.

## 2. Requirement/contract conflicts

| Conflict | Evidence / implication |
|---|---|
| New Orca-calling slash command vs no-Orca command boundary | WC:5,40 rule; [CODE-CONTRADICTED universal implementation description] actual ISSUE-CODE:666-682/1351-1355 creates/launches. Need deliberate coordinator-only boundary, not accidental blanket exception |
| Supervised child supervisor | WC:62 all six calls any depth; :69 person-opened; CORE:55-59 preserves contract. Flag/depth alone insufficient |
| All-session automation vs human authority | WC:57,232,250-269 Ruling/PR/freeze cannot be delegated |
| Token grant vs outward ownership | WC:41 no brief authorizes outward, :229 human instruction, :233 unseen-commit review; signature not permission policy |
| Cleanup/artifact disposal vs evidence | WC:225 unread reports/unfinished ledgers/frozen state; :234 task packages retained/staged |
| Universal worktrees | WC:47,220-225 conditional placement, not supervision hierarchy |
| Proposed six message protocol | WC:101,105-108 current types/identity; SEND-CODE:33-65 lifecycle sender/capability; don't synthesize completion/indiscriminate ack |
| Timeout recovery | WC:46,73-79,157-192 positive settlement, no duplicated restart authority |
| Cross-workspace correction | WC:61 pulled followups/:246 self-created Tasks; [UNVERIFIED] peer correction admission |
| Summary replacement | STYLE:22 explicit policy exception needed |

HOOK:94-103 track/fin checks words/flags; :342-357 Bash extraction/exit, HOOK-REG:105-113 registers. [CODE-VERIFIED] Syntactic flag check, not worker-role authority guard.

## 3. Distinct v2 scopes

#339 C1: "Version 2 should include an orchestrator of orchestrators."
#339 C2: "For the orchestrator-of-orchestrators in version 2, the top Orchestrator grants a sub-orchestrator a token for its set of worktrees; the sub-orchestrator can only narrow it further for its children."
#339 C2: "Build Steps 2 and 3 as part of version 2, before any orchestrator-of-orchestrators work."
#423: "Orchestrator v2 - Proactive Holistic", a catalogue/working knowledge of all agents/workspaces; explicitly separate release after v1 #339, not v1 scope expansion.

[GH-OBSERVED proposals] #423 acceptance is catalogue refresh/relevance/shared research/lessons/duplicates/course corrections, NOT child supervisor/depth/attenuation/upward/cleanup authority. Thus v1 supervision (#339), knowledge sharing (#423), hierarchy (#339 comments +444) are separate objectives. [UNVERIFIED] No administrative release-number resolution established.

**Key Takeaways:** plural orchestrators doesn't imply parentage; #423 completion would not satisfy hierarchy sketch.

## 4. Related issues and merged work

| Source | Evidence and boundary |
|---|---|
| #431 OPEN | Eight reported six-worker incidents: compaction timer heartbeat, idle turn, single-file mtime, filtered final status, unread answers, permission wait, chain stop, repeated exhaustion. [UNVERIFIED] Reproduction. WC:95-200 now progress/timing/ack/screen/all-type/chain/handoff procedures. Human prompt/unknown recovery and multi-consumer (WC:200) still uncertain. Middle doubles failure boundaries, not a prerequisite to solve flat problems |
| #446 | Retry lock after1/2/3/4s ~10total, never delete/move/edit; persistent lock block path/age; no long-hook wait/environment assumptions. [CODE-CONTRADICTED current change] WC:45 still immediate block; stale old anchor44. Tests same shared source; experiments unrerun, no delegated Git authority |
| #409 | "One human supervising 5-10 orchestrators and 50-100 sessions/worktrees" observer, "not ... a scheduler, or a session manager"; out-of-scope approve/retry/terminate/spawn/merge/rebase/delete/instruct. Synthetic data/schema proposed, prototype absent here, remote package/tests/version/API unverified. Compatible with O2 peers, not proof hierarchy needed |
| #326 approved follow-up | Comment https://github.com/IronbellyOrg/IronClaude/issues/326#issuecomment-6590983517 says depth1 retained and central git relay not adopted because commands can't call another session. WC:42 implement per-task commit depends on #326; :47/:224-234 single owner. Remaining Git/submodules not established |
| PR422 | [GH-OBSERVED] merged2026-11-07T14:15:58Z. WC:24-25 nested result propagation/:304 fifteen P2 commands, TEST phrase checks. Static conversion not P2 live acceptance, no later rollout readiness implied |
| PR449 | [GH-OBSERVED] merged2026-11-08T07:05:30Z. CORE wording/HOOK registered syntactic guard; ISSUE-CODE two-stage create-without-agent then launch intentional exception. No upward/grant/supervision protocol; successful reported tests not rerun |

**Key Takeaways:** flat liveness/locks/observer/Git work mostly independent; merge/static claims not runtime proof.

## 5. Prior F1-F7 checked and narrowed

| Hypothesis | Disposition |
|---|---|
| F1 undefined role | Verified wording gap, but WC:11 ordinary clause explicitly says USER-started. Agent-launched nonworker not automatically expressly ordinary/coordinator; classification gap |
| F2 no upper channel for allowed lower supervision | Worker has channel but prohibition; proposed handoff-owner channel unestablished. Not a claim native helpers absent everywhere |
| F3 alternate launches unfenced | Historical P0:27 documentary; not freshly retraced here, mechanics slice owns current proof |
| F4 machine-wide/one-way depth | DEPTH-CODE:7-26 default/root/validation verified; effective profile/reload/reversal/per-Run absence not established. One-way overstates unknown-safe-lowering |
| F5 authority undefined | Current Ruling/grants/cleanup/outward rooted, no new transfer rule found |
| F6 hook role blind | Source scanner words/flags not coordinator/worker |
| F7 unbuilt orchestrator | Bounded filename search no dedicated primitive, not universal no-design claim |

[CODE-VERIFIED] SEND-CODE:59-60 accepts optional Dispatch capability forwarded as orchestration capability. No macaroon/Biscuit found must NOT be generalized to no capability mechanism. [UNVERIFIED] Attenuation/semantics/suitability need investigation before separate grant system.

## 6. Hidden dependencies and options

Decision dependencies (not plan): explicit coordinator-only no-Orca-command exception; genuine-human approval/PR/freeze authority; liveness/admission before treating heartbeat as supervision; transport spike Q1/Q2; typed/grant enforcement and library comparison before hierarchy; D5 composite+material runtime split trace/routing gates; worktree placement distinct; one owner per Task/mailbox/child/cleanup; settled retry/freeze propagation; coordinate #446 shared source; don't smuggle #326 commits/submodules into sub mode; #423 knowledge release separate; #409 remains observer not enforcement layer.

Options: O1 current default policy; O2 independent human-opened peers compatible without implicit cross-control; O3 currently banned and D5-gated; O4 code ownership phrase not full route/authority, historical unfenced launch not safe contract; O5 internal helper fanout WC:60 no lifecycle replacement; O6 recommended on new sub mode, retain O1 and independently evaluate v1. No measured benefit outweighing supervisor/authority boundary shown here. Reopen O3/O4 only after need/transport/authority/routing/liveness/freeze-cleanup evidence, not simply release label.

**Key Takeaways:** don't add sub flag then discover security; down authority AND up evidence required; deferral not rejection of local parallelism.

## Gaps and Questions

[UNVERIFIED] R01-R35 unimplemented parts (scale/registry/sweep/attention/server/push+closed predicates/validation/grants); transport sender bypass/held message/inbound interception/fallback; maintained grant choice/verification/attenuation/expiry/session/nonces, existing capability compatibility; launched-middle classification; depth2 mailbox/ack/consumer replacement; live #431 resolution and cross-level orphan recovery; active cap/all entrypoints/profile/reload/rollback; D5 qualifying notes (not exhaustively searched in this slice); P2 live admission; #409 remote source/test/schema; #446 experiments and remaining #326 work; C2 benchmark/literature; no actual permission/model change. [CODE-CONTRADICTED] Absolute automation/disposable evidence/worktree-per-prompt/table replacement/worker fanout conflict with policy; universal no-Orca-command description contradicted by coordinator-only claim helper implementation.

## Stale Documentation Found

- [STALE DOC] #339 C4 PR422 open -> merged timestamp above [GH-OBSERVED].
- [STALE DOC] #446 old line44 -> WC:45; requested retry remains absent.
- [STALE DOC] #339 old liveness baseline vs WC:95-200 and TEST:199-253 additions; not full runtime/cleanup guarantee.
- [STALE DOC][CODE-CONTRADICTED] DEV-GUIDE:980 universal no-Orca-calls implementation description vs ISSUE-CODE actual subprocesses; worker ban still current.
- [STALE DOC if current] DEV-GUIDE:985 historical P0 inventory vs WC:303-304/current converted set; preserve history not current readiness.
- [STALE DOC] CR01:19,24 PR-worker/default setup-run vs WC:23,232,221.
- P0:27 historical trace only, not fresh current handlers.
- [STALE INTERPRETATION] Prior F1 infers every agent launch ordinary; WC explicitly describes user-started sessions.

## Summary

Most #339 needs apply without hierarchy. Its later hierarchy sketch requires transport research/typed messages/scoped grants, while #423 v2 is knowledge sharing, not nested supervision. Current contract worker ban/human authority remains despite ownership phrase, and hook checks flag syntax not grant. Recommend O6 new sub mode with O1 current; independent v1/knowledge objectives need not wait on hierarchy. Preserve all 35 requirement dispositions and precise source/uncertainty distinctions from exact returned JSON. No live messaging/current effective depth/remote observer/test execution checked.

