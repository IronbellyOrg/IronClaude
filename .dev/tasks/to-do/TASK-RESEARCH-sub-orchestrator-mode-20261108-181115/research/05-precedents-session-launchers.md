# Research: Session launcher precedents

**Investigation type:** Pattern Investigator
**Scope:** Issue claim, issue watcher, coordinator-only commands, sprint and swarm launchers
**Status:** Complete (static launcher inventory; detailed return retained)
**Date:** 2026-11-09
**Delivery:** User-approved adaptation: researcher returns findings; coordinator writes this file. No model-tier change.

---

## Complete evidence and method

Exact complete returned investigation is retained in `returned/05-returned-findings.json`, field `text`, including absolute source register, fourteen-launcher inventory, all 56 launcher/option reuse verdicts, references and limits. This indexed Markdown must be consumed with that text at synthesis/anti-omission. It does not replace the full matrix.

Six assigned mandatory files read fully, others Glob/Grep then <=150-line ranges; sprint/swarm globbed independently. No sessions/tests/state/GitHub/model changes; MCP retrieval unavailable. Markdown instructions [UNVERIFIED runtime]; actual launch code [CODE-VERIFIED static].

Aliases (paths relative root): I=`src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`; IS same skill SKILL.md; IT templates/launch-prompt.md; WL=`src/superclaude/cli/issue_watch/launch.py`; WCY same cycle.py; PR=`src/superclaude/commands/pr-submit.md`; PRS backing sc-pr-submit-protocol/SKILL.md; PM/PMS corresponding pm command/protocol; SPAWN/AGENT respective commands; DEC=`.dev/orca-command-refactor/decisions/APPROVED.md`; CONTRACT=`src/superclaude/core/WORKER-CONTRACT.md`; CORE same CLAUDE.md; GUARD=`src/superclaude/hooks/scripts/launch-level-guard.sh`; DP/DI=`docs/designs/sc-issue-claim-pipeline-flag.md` / `sc-issue-command.md`; SP/SE/SS/SH/SN/SR/ST=`src/superclaude/cli/sprint/{process,executor,scheduler,handoff,summarizer,rerun_tasks,tmux}.py`; PP=`src/superclaude/cli/pipeline/process.py`; SD/SC/SO/RED/SMT=`src/superclaude/cli/swarm/{dispatch,commands,transports/openai_compat,reduce,tmux}.py`.

## 1. Launch reporting authority and limits inventory

| ID | Mechanism / placement | Report and authority | Limits / evidence |
|---|---|---|---|
| L1 issue governed agent | I cmd_worktree create no agent with repo/name/base/no-parent/comment/json :666-681; cmd_launch agent launch claude/path/terminal/nonce prompt :1351-1355 | JSON launch receipt (not completed work) :186-189,1397-1405; child template :21-26 shows plan/approval or final status locally, no upstream Task_done | Level worktree/full/full-submit :1332-1336; guard preflight :1300-1325; template planning/implementation/opt-in publication never merge :18-34 [UNVERIFIED behavior]; GUARD :455-478,681-687,724-737 all-level external ESCAPE. Local helpers permitted branch |
| L2 issue lookup/draft helpers | [UNVERIFIED runtime] Agent-tool tier-specific subagent_type, no model override, no worktree IS:54-68,84-88 | Paths read by skill, missing once retry then STOP IS:66-68; only skill GitHub/ClickUp writes IS:70-76 | Named narrow output/read-only roles/fixed tier assignments, not Orca Task/Dispatch identity |
| L3 issue-watch | WL launch_argv :84-116, launch :352-370 starts ordinary claim agent in configured cwd/worktree, does not create issue child itself | Outcome to cycle/audit state, not upper inbox WL:326-349; WCY:1080-1112,1180-1210; validated claim prompt :84-102 no coordinator role | Fork check WL:233-251; pending before launch, day/deadline/disabled caps, one outcome then stop WCY:812-834,1061-1112. Child authority inherited from claim not poller |
| L4 PR ordinary session | [UNVERIFIED practice] DEC:10,18 ordinary top-level per named PR in its child, never worker; PR:96-115 activates protocol not session-placement code | Attended main-session monitor/log/resume PRS:18-49, no parent coordinator channel | Monitor ordinal scope PR:111-121/PRS:36-41; main context/no nested-skill helper/daemon PRS:43-49 |
| L5 PM | [UNVERIFIED runtime] PM:49-55 -> PMS:56-84 specialist delegation/parallel phases, no concrete Orca launcher/worktree | Workflow aggregation, not Orca child contract; broad coordinator instructions | Roles/ordering not capability/depth/upward record; never-worker CONTRACT:23 |
| L6 spawn | [UNVERIFIED runtime] SPAWN:176-210 execution prose but final decomposition-only boundary | Returns hierarchy/dependencies/assignments, not persistent launched owner | No implementation/code/system changes; never-worker |
| L7 agent | [UNVERIFIED runtime] AGENT:23-50 helper instructions no concrete Orca launch | User progress/risk/escalation; own workflow | Confidence guidance not depth/report capability; never-worker |
| L8 sprint phase | SP:147-170,219-237 subclasses PP; PP:140-165 claude print verbose/permission/no persistence/tools/max turns/format/optional model; SE:2126-2146 starts; no Orca tree | stdout/stderr files, runner polls PP:199-218; whole phase tools, no coordinator credential | Turns/model/timeout=maxturns*120+300 + prompt checks; budgets not Orca depth |
| L9 sprint task | SE:1683-1699 task subprocess/files/isolation env; SE:1328-1334 bounded pool waves | Exit/turns/bytes SE:1708-1723; runner-built artifacts/deps :1312-1319; controller retains scheduler | SS:85-104 topo/cycle, concurrency k, watchdog/timeout; SH:35-66 atomic handoff/success AND gate for resume |
| L10 sprint narrative | SN invoke_sonnet :310-346 single-turn subprocess timeout/default alias, no worktree | Returns decoded text, empty missing binary/timeout/OS/nonzero :321-367 | One turn/timeout; permission-bypass flag in actual launcher not hard sandbox; no project ownership |
| L11 checkpoint rerun | SR:1375-1387,1701-1705 uv superclaude sprint rerun-tasks absolute index/phase/single checkpoint/no-verify-checkpoints | Wait exit/report mirror :1706-1719, not Orca session | Narrow rerun/no recursive verification; no timeout argument at shown subprocess |
| L12 sprint tmux | ST:81-107,176-202 tmux detached foreground sprint/no-tmux with state/limits/model | Outer launch + inner state/exit sentinel not upper Orca mail | no-tmux prevents recursive wrapper; budgets inner runner |
| L13 swarm HTTP workers | SD:409-475 ParallelExecutor per slot -> SO:379-402 endpoint model/user-message/token request; no agent session | WorkerResults -> SC:1946-1955; RED:350-375 atomic contract; controller retains artifacts | Timeout/retry policy SD:241-276 <=one extra attempt, worker count executor; max tokens, no tools/worktrees in shown payload |
| L14 swarm detached | SC:1297-1309 interpreter CLI from saved spec -> SMT:160-177 tmux optional cwd output | Returns tmux name, final RED contract not Orca lifecycle | Missing tmux/empty cmd/existing-name checks; child no detached flag; not delegated coordinator identity |

**Key Takeaways:** issue launch chain != supervised coordinator hierarchy; Python child/shell/model request/Agent helper/Orca worker are distinct. Sprint gives reusable deterministic scheduling/results; swarm gives bounded text fan-out, not repository/tool authority.

## 2. Reuse matrix for middle-layer options

R=reusable, P=partial, C=counter-example; detailed reasons retained verbatim in JSON section 2. Verdicts fit mechanisms, not working-mode proof.

| Launcher | O2 peers | O3 supervised middle | O4 handoff owner | O5 Agent helpers |
|---|---|---|---|---|
| L1 governed claim | P | C external ESCAPE | P launch/receipt, no upward contract and no fanout | P local helpers only |
| L2 issue helpers | P roles only | C no supervisor identity | P briefs/artifacts only | R explicit instructions |
| L3 watcher | P starts ordinary sessions | C poller not worker | P durable intent/unknown outcome/audit, no completion | P conceptual only |
| L4 PR session | R policy | C D3 | P distinct owner, no upper channel | C monitor must main context |
| L5 PM | P | C never-worker/no nested role | P broad owner only | P specialist prose/result vague |
| L6 spawn | P prepares assignments | C never-worker/decomposition | C not runtime launcher | P decomposition only |
| L7 agent | P | C never-worker/no role | P workflow only | P specialist prose |
| L8 sprint phase | P | C process != roles | P phase/result mechanics | P different mechanism |
| L9 sprint tasks | P | P mechanics only | P scheduler/handoff, no owner session | P subprocess not Agent |
| L10 narrative | C | C | C | P bounded helper concept |
| L11 checkpoint | C | C | P narrow operation/exit | P scoped retry concept |
| L12 sprint tmux | P packaging | C shell != supervisor | P durable CLI, not upward agent | C |
| L13 swarm | C HTTP not peer | C no tools/grandchild authority | P dispatch/contract only | P fanout shape, model requests |
| L14 swarm tmux | P job only | C no role | P durable launch/result | C |

**Key Takeaways:** no complete O3 precedent in these launcher paths; O4 reusable parts not end-to-end protocol; O5 clearest existing narrow helper pattern.

## 3. Launch ancestry versus supervision

WL:84-116,352-370 -> IS:84-92 -> I:1351-1355 gives watcher -> claim -> helpers/governed agent, a real invocation chain. WCY:1080-1112,1180-1210 records launches, not continuous child completion. GUARD:455-478,681-687,724-737 restricts governed child fanout/messages. CONTRACT:60-69 still person-opened root/no worker fanout [UNVERIFIED universal enforcement]. CORE:55-59 owner-role words do not create upper Task/Dispatch/result contract; DEC:12 depth1 remains. Scoped negative finding: none of the inspected launchers receives supervised upper assignment, manages external children as lower coordinator and reports aggregate completion upward. Not a statement about all Orca internals/deployed sessions.

**Key Takeaways:** started-by != supervised-by; missing relation is authority/lifecycle/admission, not simply launch.

## 4. Issue design terminology and reusable patterns

[CODE-VERIFIED] DP:94-115 calls skill orchestrator, script creates/launches I:666-681,1351-1355; I:186-189 JSON result. DI:91-117 labels T1/T2/T3 Agent helpers workers, IS:54-76,84-88 prescribes delegation/write scope [UNVERIFIED compliance]. [CODE-CONTRADICTED interpretation] Neither diagram proves layered Orca coordinator design; external seam agent launch, not worker-start/Task. Lookup worker terminology is Agent assignments not Orca Dispatch. Base design narrower than later pipeline is not automatically defect.

Reusable evidence: watcher validated prompt/pending-before-launch/unknown outcome/audit (WCY:1080-1112; WL:326-349); governed explicit level/preflight/receipt (I:1300-1355); sprint runner-built atomic handoffs and success+gate resume (SE:1312-1319; SH:35-66), topo/bounded waves (SS:85-104; SE:1328-1334); swarm bounded fanout/reduce (SD:241-276,409-475; RED:350-375). None creates automatic upward coordinator identity. Internal helper constraints/results IS:56-68/CONTRACT:60-65 useful, not external supervisor credentials.

Researcher recommends O5 local specialist fanout, O2 person-opened persistent peers, defer O3/O4 under O6 pending authority/upward/cancel/aggregate/ownership contracts. Do not reuse permission-bypass subprocess launch as evidence of safe delegated authority.

## Gaps and Questions

[UNVERIFIED] Live dual-role Orca behavior absent (no Orca implementation audit in this slice); middle role CORE vs CONTRACT bridge undefined; D3 automatic/consistent placement not proved; PM/agent/issue helper role/output/tier compliance untested; PM always-active startup not verified; watcher launch-reply operation ID/error seams marked unverified in WL:39-48; claim preflight only verifies current process not child environment I:1314-1320 and IS:92 ship gates; no complete upward progress/decision/completion relation; no filesystem/authority sandbox proven by isolation env (SE:1683-1699,PP:140-183,199-218). Governed O3/O4 direct paths blocked by code, requiring separate policy. [CODE-CONTRADICTED] Diagram hierarchy interpretation, and universal atomic worktree-plus-agent guidance omits two-stage exception.

## Stale Documentation Found

- [STALE DOC][CODE-CONTRADICTED] CORE:55-59 universal create-with-agent language differs from I:666-681 then :1351-1355 two-stage claim exception; discrepancy does not authorize worker bypass.
- [STALE DOC candidate] SPAWN:176-182 execution prose vs :192-210 explicit decomposition-only stop; no runtime path established, classify by boundary.
- No verified layered coordinator design in DP/DI; misleading interpretation, not proof documents implement missing feature.

## Phase-2 correction addendum — B1/B2 dependency

Research04's B1/B2 correction supersedes categorical guard claims in L1, the L1 reuse-matrix row, §3, Gaps and Questions, and Summary. GUARD:450-478 recognizes literal basename `orca`, not research03's observed `orca-ide`; its all-level ESCAPE denial applies to recognized forms in bound sessions, not universally to all Orca executables. Other classifications may still deny a call; this mismatch grants no permission and proves no live success.

O2's fit is not blanket governed-session compatibility. For any O1-O4 supervisor operating in a bound session through recognized `orca`, worker-list, worker-read and worktree ps are unlisted despite their contract-required supervision uses (research04 addendum). Required probes therefore add a policy-design question distinct from launching/reporting; no allowlist expansion is authorized or automatically recommended. Current worker-role bans, launcher inventory, local-helper classification and absence of a complete inspected launcher-level O3 precedent remain unchanged. Immutable returned evidence is historical input subject to these corrections.

## Summary

Ordinary launchers, Agent helpers, subprocess supervisors and HTTP model fanout exist, but no inspected launcher implements full supervised coordinator-under-coordinator relation. Watcher/claim chain supplies receipt/audit, not upstream aggregate supervision, and governed child cannot further externally launch/message. Sprint/swarm offer reusable scheduling/budget/result/durability patterns without Orca role inheritance. O5 local and O2 persistent person-opened peers fit current boundaries; O3/O4 require explicit contracts. No live sessions/tests/tier resolution/deployment checks were run.

