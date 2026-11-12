# Research: Hooks guards and identity

**Investigation type:** Integration Mapper
**Scope:** Worktree-agent and launch-level hooks, registrations, mirrors and related tests
**Status:** Complete (static investigation; runtime checks remain open)
**Date:** 2026-11-09
**Delivery:** User-approved adaptation: researcher returns findings; coordinator writes this file. No model-tier change.

---

## Evidence index and method

All paths below are relative to this worktree root. Citations use the identifier and the source line range read by the researcher.

| ID | Path |
|---|---|
| W | `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` |
| G | `src/superclaude/hooks/scripts/launch-level-guard.sh` |
| J | `src/superclaude/hooks/scripts/launch-job-identity.sh` |
| H | `src/superclaude/hooks/hooks.json` |
| I | `src/superclaude/cli/install_hooks.py` |
| D | `docs/designs/sc-issue-launch-level-hook.md` |
| TW | `tests/hooks/test_require_orca_worktree_agent.py` |
| TG | `tests/hooks/test_require_orca_worktree_agent_governed.py` |
| TL | `tests/hooks/test_launch_level_guard.py` |
| TC | `tests/core/test_orca_session_launch_guidance.py` |
| PH | `plugins/superclaude/hooks/hooks.json` |
| PW | `plugins/superclaude/hooks/scripts/require-orca-worktree-agent.sh` |
| PG | `plugins/superclaude/hooks/scripts/launch-level-guard.sh` |
| PJ | `plugins/superclaude/hooks/scripts/launch-job-identity.sh` |

The researcher read the five designated mandatory files in full, searched other files first and read targeted ranges, approximately 1,100 source lines total. This exceeds the prompt's approximately 1,000-line target; recorded as a delivery limitation, not concealed. No agents, tests, GitHub operations or Orca commands were run. The following is a coordinator transcription of returned findings; it is static source evidence, not runtime verification.

## 1. Identity signals available to each hook

| Hook | Inputs actually consumed | Binding authority | Role information and responsibility |
|---|---|---|---|
| W: worktree-agent requirement | `tool_name`, `tool_input.command`; jq selects Bash only, not session/agent/parent/role (W:345-347) | None; AWK `track(o,w)` records flags and `fin(o)` detects bare create (W:94-103) | No role-dependent decision. Ownership roles occur in the denial message (W:351-355). Blocks recognized bare worktree creation, not unauthorized callers |
| G: launch-level guard | Event name, validated `session_id`, tool name, Skill name, edit/notebook path, Agent/Task isolation, Bash/Monitor command; `agent_id` becomes presence flag on prompt events only (G:185-203) | Session launch-level record; accepted words `worktree`, `full`, `full-submit`; malformed/unreadable records become strictest level (G:254-270) | No role, parent-owner, depth or delegation scope. Classifies tools only for positively bound sessions; unbound/missing/invalid identity allows without enforcement claim (G:390-395) |
| J: job identity | Tool name, validated top-level `session_id`, event, optional `tool_use_id`, command; validates `agent_id`/`agent_type` shapes (J:424-455) | Existing session record followed by store/governed validation; existence alone is not rewrite authority (J:435-445) | Does not infer identity from agent ID, parent, cwd or environment (J:429-431). Shape checks are not role recognition. Replaces whole Bash input through `updatedInput` with execution-context guidance (J:478-481) |

Data flow:
1. W scans Bash command shell structure and allows or emits its agent-flag denial; no session lookup.
2. G parses top-level identity, checks binding and level, then classifies tools; cwd is not fallback identity (G:185-203,254-270,390-395).
3. J independently validates governed identity before rewriting Bash input. Other hooks' rewrite ordering is unspecified in its header (J:14-18,424-455).

**Key Takeaways:** a coordinator label is not a capability; session restrictions exist but hierarchy authorization does not appear in these inputs/records; process-job and orchestration-role identity are distinct.

## 2. What a role-aware guard would need

The following are inferred design requirements, not existing features.

| Requirement | Current evidence | Decision implication |
|---|---|---|
| Authoritative role/capability binding | G parser has no role; record has three fixed level words (G:185-203,254-268) | Naming a session sub-orchestrator changes no policy |
| Parent/owner and delegated scope | G parses neither; J rejects inference from parent fields (G:185-203; J:429-431) | Depth-two/scoped-brief authority cannot currently be enforced from these signals |
| Trusted coordinator launch distinction | Level records distinguish launch levels, not worker/coordinator kinds (G:264-268) | Need validated capability or revised format; arbitrary new record word selects strict fallback today |
| Policy handoff to independently launched children | State-changing Orca becomes ESCAPE and is denied at every governed level (G:455-478,735-739) | Launch exception alone removes a restriction without binding the child |
| Constrained upward communication | SendMessage is ESCAPE; Orca exceptions are read-style, not send/dispatch (G:475-477,686-687) | Need parent-bound reporting, not unrestricted messaging |
| Verified context visibility | [UNVERIFIED] D:457 lists U7 Orca preamble | No established authoritative coordinator preamble visible to hooks |

[UNVERIFIED] U28 "Orca hooks" relates to O-22 structural pre-push installation (D:377,457), not proof of a role field or role-aware hook. U7 and U28 are separate unresolved questions.

**Key Takeaways:** trusted authorization is missing, not another name; neither prompt preamble nor arbitrary new launch-record value is established as a safe extension.

## 3. Governed claim sessions and sub-orchestration

[CODE-VERIFIED] D:175's documented Orca ESCAPE exceptions agree with G:455-478: status/help/version; worktree current/list/show; terminal list/show/read; orchestration check/inbox/run-current/task-list/worker-show. Other recognized Orca pairs are ESCAPE unless the segment ends with a help flag. ESCAPE is denied for W, WA, F, FS, including approved worktree and full-submit (G:737).

| Activity | Current classification | Implication |
|---|---|---|
| Worktree create with agent | Satisfies W syntax, but G still ESCAPE (W:94-103; G:475-478,737) | Need narrow launch authority and child-policy binding |
| Existing-worktree agent launch | Not in exceptions, ESCAPE (G:475-478,737) | Need who/scope/child-governance policy |
| Supervised worker start or task dispatch | Not in exceptions (G:475-478,737) | Need scoped authorization for state change |
| Upward Orca messages or SendMessage | Outside Orca exceptions; SendMessage explicitly ESCAPE (G:475-478,686-687,737) | Need authorized parent-bound upward channel |
| Explicitly listed inspections | For recognized `orca`: status/help/version; worktree current/list/show; terminal list/show/read; orchestration check/inbox/run-current/task-list/worker-show do not add ESCAPE in the Orca branch (G:475-476) | Branch-specific exception, not blanket approval of reads or combined commands |
| Required but unlisted supervision probes | For recognized `orca`, orchestration worker-list/worker-read and worktree ps fall through to ESCAPE unless the segment ends in --help/-h (G:475-478); ESCAPE is denied at all governed levels (G:737) | K:107,110,151 require these enumeration, prompt-wait and transcript probes; the existing supervision sweep/L1 cannot run unchanged through recognized `orca` in a bound session. Help is not execution of a probe |
| Local/background Agent or Task | Branch assigns ESCAPE only for remote isolation; does not scan prompt (G:681-683) | Existing classifier-compatible O5 shape; live identity inheritance remains open |
| Remote Agent/Task | ESCAPE (G:681-683,737) | Need remote-child policy |

External-session form cannot use direct state-changing Orca operations in a governed session. Agent-flag syntax does not override G. In-session delegation is allowed by its branch but does not establish independent Orca-session ownership or upward protocol. Unbound sessions allow because enforcement is absent (G:390-395), not because worker-contract restrictions are waived.

[UNVERIFIED] The claim launcher implementation was outside this slice's reads; no real claim launch or initial binding timing was observed. Conclusions apply to sessions already recognized as bound by G.

**Key Takeaways:** no launch level unlocks external sub-orchestration; both launching and upward communication need policy; satisfying W does not satisfy G.

## Phase-2 correction addendum — B1/B2

This addendum supersedes categorical guard-enforcement and read-compatibility claims in §§2-4, §7, Gaps and Questions, and Summary, including the policy-handoff row, “cannot use direct state-changing Orca operations”, “blocks external delegation for all governed sessions”, and the child-launch/upward-policy gap. Original returned evidence remains unchanged.

### B1 — executable recognition ceiling and gap

[CODE-VERIFIED] G:450 takes each normalized word's basename; G:455-458 enters the Orca branch only for literal `orca`. Research03 records the observed executable as `orca-ide`; that basename does not match this branch. Therefore the supported conclusion is: in positively bound sessions, recognized `orca` command forms outside the listed/help exceptions receive ESCAPE, denied at every governed launch level (G:475-478,737). This is not proof that every Orca invocation or executable is blocked.

The executable mismatch is a concrete static enforcement ceiling and decision gap, not permission to use another spelling, proof a live call succeeds, or proof the whole hook permits it: other classifications may still deny a command. No alternate-executable experiment or hook change is authorized.

### B2 — supervision compatibility gap

K=`src/superclaude/core/WORKER-CONTRACT.md`. K:107 requires worker-list after three empty waits; K:110 requires worker-list and worktree ps --agent-wait in the sweep; K:151 includes worker-read --source transcript in L1. These pairs are absent from G:475-476 and fall through at G:477. Thus a governed ordinary supervisor cannot execute the existing sweep/L1 unchanged through recognized `orca`, despite worker-show being listed. This is an additional policy-design surface, not authorization or an automatic recommendation to expand the allowlist.

### Governed-context option qualifications

- O1 remains the current role policy, but “compatible” does not establish unchanged supervision inside a bound session: B2 applies.
- O2's unbound-session assessment applies only when actually unbound; person-opened alone does not establish binding status. A bound peer faces the same recognized-command restrictions.
- O3/O4's guard assessments concern bound sessions and recognized classifier forms, not every session or executable. Launch, reporting and required supervision probes are distinct policy questions. Research03's native local-helper capability remains source-established; classifier restrictions neither erase that capability nor authorize its use.

WC-13's worker fan-out ban and coordinator eligibility remain policy authority regardless of classifier coverage. Local Agent/Task classification and unverified live identity/rewrite behavior are unchanged. No live nesting or bypass success is claimed.

## 4. Declared enforcement ceilings and WC-13

| Hook | Declared ceiling | Hierarchy consequence |
|---|---|---|
| W | W:39-61 excludes shell/interpreter strings (`bash -c`, `sh -c`, `eval`, `env -S`, SSH), subprocess launchers (`xargs`, `find -exec`), shell-fed heredocs, partially assembled words, escaped nested backticks, some wrapper/global arguments, non-Bash tools, missing jq/awk, bare sessions skipping settings, human/other-tool creates and scripts invoking Orca. Quoted prompt equal to agent flag can satisfy lexical check | Bounded syntax check, not authorization. Ownership and no-self-use remain instructions (W:6-8) |
| G | Only positively bound sessions; missing/invalid/unbound identity explicitly fail-open, no cwd fallback (G:4-9,390-395). Header does not contain W's shell-ceiling list | Can reject recognized actions for bound sessions, but does not distinguish worker/coordinator; not complete WC-13 enforcement |
| J | Linux same-user job identity, not sandbox/controller-PID binding. Detachment/daemonization can escape selection; killing supervisor leaves unknown state; Monitor/pipelines unsupported; rewrite ordering, persistent cwd and live rewrite unresolved (J:2-18) | Process selection does not establish parent authority, delegation depth or role ownership |

[UNVERIFIED] Exact WC-13 text/exceptions were not inspected in this slice. For the assignment's proposed restriction, W supplies syntax checks regardless of role, G blocks external delegation for all governed sessions, and J supplies supported Bash-job identity only. W's coordinator wording does not itself relax WC-13; G's restriction is broader than worker-only.

**Key Takeaways:** do not transfer W's scanner ceilings to G; these are defensive checks, not full hierarchy enforcement; relaxing WC-13 needs a contract decision as well as hook-policy decision.

## 5. Registrations installer and mirrors

| Surface | Evidence |
|---|---|
| Source UserPromptSubmit | G registered with five-second timeout (H:63-70) |
| Source PreToolUse | W Bash/3 seconds; G Bash, Skill, Agent, Task, edits, Monitor, workflow, messaging, scheduling and selected MCP write names/5 seconds; J Bash/5 seconds (H:105-133) |
| Installer | All three in installer script list (I:86-93); inclusion is not installed-machine proof |
| Plugin registry | Same three PreToolUse registrations/timeouts (PH:76-102); prompt guard registration (PH:46-50) |
| W mirror | Coordinator-under-orchestrator message matches source (W:354; PW:354) |
| G mirror | All-level ESCAPE denial matches (G:737; PG:737) |
| J mirror | Whole-input rewrite warning matches (J:14-15; PJ:14-15) |

Plugin script directory enumerated before searching; matching tokens checked source/plugin. This is targeted parity, NOT byte-identical whole-file/registry proof. No sync command executed.

**Key Takeaways:** all three have source registration, installer entries and plugin counterparts; registry placement does not prove live rewrite ordering.

## 6. Tests and verification limits

| Test | Inspected evidence | Limit |
|---|---|---|
| TW | Direct, compound, substitution create forms; per-command flag handling, help/agent allow cases, fail-open dependency/scanner errors; shell-string ceiling explicitly allowed (TW:57-125,144-194) | Read, not run; not all shell-form coverage |
| TG | Governed-shaped event with session/tool-use/cwd fields; W receives original bare-create command (TG:31-56) | Header explicitly excludes live rewritten-input/order proof (TG:1-9) |
| TL | Governed subagent/nested-subagent examples use bound session ID (TL:1585-1598) | Hand-written shapes pending OB-H1, not actual live envelope |
| TC | Pins launch/dispatch/internal-subagent/ownership/hook guidance (TC:12-34,44-59) | Text assertions do not prove coordinator protocol or role enforcement |

**Key Takeaways:** static tests support intended branches; no tests were executed; identity inheritance/rewrite ordering remain live questions.

## 7. Option implications (this slice, not the final decision)

| Option | Hook/identity implication | Assessment |
|---|---|---|
| O1 Keep two tiers | No new hierarchy authorization | Compatible with current restrictions, no external delegation added |
| O2 Person-opened peers | Unbound sessions outside G (G:390-395) | Avoids changing governed launch policy, no parent-child reporting established |
| O3 Worker with helpers | Direct launch/dispatch/upward messaging ESCAPE; no role distinction | Needs explicit capability, contract, child-governance and reporting decisions |
| O4 Handoff-owner sub-orchestrator | Agent flag satisfies W not G; independent children lack trusted upward relationship | Ownership wording insufficient |
| O5 In-session Agent delegation | Local/background branch not ESCAPE (G:681-683) | Closest existing permitted classifier shape, not independently owned Orca sessions |
| O6 Defer with gates | Retains external-launch restriction until authority/runtime verification | Appropriate for O3/O4 on this evidence |

Researcher's recommendation: do not add an unrestricted sub-mode exception to ESCAPE. O5 suits local decomposition; gate O3/O4 on trusted role binding, bounded delegation, governed child identity, authorized upward channel and live hook-order/event-shape evidence.

**Key Takeaways:** wording recognizes ownership, not complete authorization; blanket launch exception grants more than records can describe; O5 is supported at classifier level, external forms require further evidence.

## Gaps and Questions

| Gap | Evidence / clarification |
|---|---|
| [UNVERIFIED] U7 preamble visibility | D:457 unresolved; establish real authoritative hook-visible envelope |
| [UNVERIFIED] U28 Orca hooks/L2 installation | D:377,457 relates to O-22, not role field; runtime resolution not investigated |
| [UNVERIFIED] Actual subagent session identity | TL:1585-1598 hand-written shapes pending OB-H1 |
| [UNVERIFIED] Concurrent rewrite ordering | J:14-18 unspecified; TG:1-9 original command only |
| [UNVERIFIED] Complete claim-to-binding path | Claim launcher outside slice; no live launch/first-tool timing observed |
| [UNVERIFIED] Exact WC-13/D5 contract | Not read here; option labels are not contract permission evidence |
| Role model | No role/parent/depth/scope parsed or represented (G:185-203,264-268) |
| Child launch/upward destination policy | Existing direct paths ESCAPE (G:475-478,686-687,737) |
| [UNVERIFIED] Whole mirror parity/installed state | Scoped token parity only; no whole diff/install/sync verification |
| Runtime platform limits | Linux/process-selection limitations, live cwd/rewrite unresolved (J:2-18) |

## Stale Documentation Found

- No confirmed stale architectural claim in inspected design passages. [CODE-VERIFIED] D:175's ESCAPE exceptions agree with G:455-478.
- [UNVERIFIED] U7/U28 remain unresolved in D:377,457; no evidence collected resolves them, so do not mark them stale.
- "Orca preamble visible to hooks" is second-hand paraphrase; actual text is "U7 Orca preamble". No role field follows from it.
- Ownership wording exists in source/plugin (W:345-355; PW:354). Interpreting it as hierarchy-aware enforcement exceeds evidence; not grounds for a [STALE DOC] marker.

## Summary

The hooks inspect command syntax, launch-bound session identity and supported Bash-job identity, not an authoritative coordinator role or hierarchy. Governed sessions' recognized external launches and messaging are ESCAPE at every launch level, even with an agent flag. Local Agent/Task delegation is closest to an existing permitted shape, but live inherited identity and rewrite ordering remain unverified. Ownership wording is an instruction, not a runtime-ready sub-orchestrator capability. No files or external state were changed by the researcher; tests, live claims and whole mirror parity were not checked.

