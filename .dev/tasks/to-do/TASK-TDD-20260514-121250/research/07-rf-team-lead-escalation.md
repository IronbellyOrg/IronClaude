# Research: rf-team-lead Escalation + 3-Fix-Cycle Behavior

**Status:** Complete
**Date:** 2026-05-14
**Agent type:** Code Tracer
**Source:** src/superclaude/agents/rf-team-lead.md (431 lines)

---

## 1. Project-Mode Orchestrator Role

`rf-team-lead` is the top-level Rigorflow orchestrator. It runs either a single pipeline (`/rf:pipeline`) or, for multi-phase work, the **project mode** pipeline (`/rf:project`).

- **Front matter** (lines 1-30): defines the agent name, capabilities (Read, Write, Edit, Bash, Glob, Grep, WebFetch, Task, TaskCreate, TaskStop, Skill, AskUserQuestion, EnterPlanMode, etc.) with `permissionMode: bypassPermissions` and `memory: project`.
- **Team composition** (lines 36-46): spawns `rf-task-researcher` (context gathering), `rf-task-builder` (MDTM file creation), `rf-task-executor` (runs `automated_qa_workflow.sh`). Parallel tracks supported via track-suffixed names (`researcher-1`, `researcher-2`, ...).
- **Project Mode** (lines 398-420): For multi-phase / iterative work, `/rf:project` invokes `/rf:pipeline` directly via the Skill tool for each phase. The session itself becomes the team lead for each sequential pipeline invocation — there is no agent-nesting. Phase outputs flow between phases through files on disk.

This file is the orchestrator that, in the qualitative-research convergence pipeline (FR-CONV.6), would decide whether to surface a synthetic DNSP or trigger the all-agents-fail escalation when a phase exhausts its retry budget.

## 2. Verified Line-Number Drift

**Sed verbatim output** (`sed -n '410,420p' src/superclaude/agents/rf-team-lead.md`):

```
| Work requiring iterative fix cycles (build → test → fix → retest) | `/rf:project` |

### Project Mode Architecture

- **Direct pipeline invocation**: `/rf:project` invokes `/rf:pipeline` directly via the Skill tool for each phase — the session becomes the team lead for each pipeline run sequentially
- **Phase 0 (Planning)**: Pipeline produces feature brief, PRD, architecture proposal using template 02
- **Phase 1..N (Execution)**: Each phase gets its own pipeline invocation — fresh agents, full orchestration, automatic parallel track support
- **Fix Cycles**: If a phase pipeline returns issues, invoke another pipeline with a FIX request (max 3 cycles per phase). If max cycles exhausted, HALT and ask user — do NOT proceed with unresolved findings.
- **Project Plan**: Maintained using `.claude/templates/workflow/03_project_plan_template.md`
- **File-Based Context**: Context flows between phases via files on disk — no agent reuse needed
- **No subagent nesting**: The session runs each pipeline directly rather than spawning agents to run pipelines
```

**Exact line of "max 3 cycles per phase":** the phrase appears on **line 417** of the file (the `- **Fix Cycles**: ...` bullet is the 8th line of the sed window starting at 410, i.e. 410 + 7 = 417). The task brief speculated the current location had drifted to line 414; in fact **the PRD citation of line 417 is exactly correct** — no drift. Line 414 is a different bullet (`- **Direct pipeline invocation**:`).

**Drift: 0 lines.** PRD-cited 417 == current source 417.

## 3. "3 Fix Cycles per Phase" Rule (line 417 verbatim)

**Line 417, verbatim:**

> - **Fix Cycles**: If a phase pipeline returns issues, invoke another pipeline with a FIX request (max 3 cycles per phase). If max cycles exhausted, HALT and ask user — do NOT proceed with unresolved findings.

**Surrounding context (lines 412-420, `### Project Mode Architecture`):**

- L414: Direct pipeline invocation — `/rf:project` invokes `/rf:pipeline` via Skill tool per phase.
- L415: Phase 0 (Planning) — feature brief, PRD, architecture proposal.
- L416: Phase 1..N (Execution) — fresh agents per phase, parallel track support.
- **L417: Fix Cycles — max 3 cycles per phase, HALT and ask user on exhaust.**
- L418: Project Plan — `03_project_plan_template.md`.
- L419: File-Based Context — no agent reuse.
- L420: No subagent nesting.

**Why this rule is the all-agents-fail escalation:** When a phase pipeline returns issues (test failures, QA reject, agent abort), the lead loops back with a FIX request. After three FIX cycles still fail, the lead does **not** silently surface a partial result — it HALTs and requires user intervention. This is the unambiguous "stop the line" gate that FR-CONV.6 DNSP emission MUST NOT short-circuit.

## 4. Escalation Ladder Structure

The fix-cycle rule (line 417) plus the broader pipeline retry logic forms an implicit escalation ladder when applied per partition agent:

| Step | Trigger | Action |
|------|---------|--------|
| **initial** | Phase pipeline first run | Run normally; collect verdict |
| **retry-1** | Phase returned issues | Invoke `/rf:pipeline` with a FIX request (cycle 1) |
| **retry-2** | Cycle 1 still has issues | Invoke `/rf:pipeline` with a FIX request (cycle 2) |
| **retry-3 (final)** | Cycle 2 still has issues | Invoke `/rf:pipeline` with a FIX request (cycle 3) |
| **escalate (HALT)** | Cycle 3 still has issues | HALT, ask user — do NOT proceed with unresolved findings |

For convergence partition agents (per FR-CONV.6), the same ladder applies per partition. When a partition agent reaches the **escalate (HALT)** rung, that single partition is "exhausted." Whether the team-lead halts globally or emits a DNSP for that partition depends on the global state of other partitions — see §5.

## 5. All-Agents-Fail Guard Behavior Preserved by FR-CONV.6

**Critical invariant FR-CONV.6 must preserve:** the existing line-417 HALT is the all-agents-fail guard. DNSP emission must not replace it.

**Decision table for FR-CONV.6 DNSP emission:**

| Partition outcome state | At least one partition succeeded? | At least one partition exhausted? | Action |
|---|---|---|---|
| All partitions succeeded | yes | no | normal completion (no DNSP) |
| Some succeeded, some exhausted | **yes** | **yes** | **emit synthetic DNSP for exhausted partitions** (the "twice exhaust" condition) |
| All partitions exhausted (zero successful) | no | yes (every partition) | **fall through to existing rf-team-lead.md:417 HALT** — do NOT emit DNSP |

When zero partitions succeeded, surfacing DNSPs would mask a total-failure condition. The existing HALT is preserved: lead asks the user, does not synthesize a "best-effort" partial deliverable.

DNSP emission therefore only fires in the **mixed-outcome** regime: at least one success **AND** at least one exhaust. This is the "twice exhaust" gate — once at the partition's retry-3 (per §4), and once at the global "at least one other partition succeeded" check.

## 6. Interaction with Synthetic-DNSP Emission

The two failure paths are **mutually exclusive**:

1. **Per-partition exhaust → synthetic DNSP.** A single partition agent has burned its 3 fix cycles, but other partitions completed normally. The team-lead emits a synthetic DNSP for that partition only, preserving parallel-research outputs from the successful partitions. The successful partitions' research is not discarded; the convergence step proceeds with explicit `did_not_ship_partition=<id>` markers.

2. **All-partitions exhaust → existing rf-team-lead.md:417 escalation, NOT DNSP.** Every partition burned its 3 cycles. The team-lead executes the original HALT (`ask user — do NOT proceed with unresolved findings`). No DNSP is synthesized because there is no successful counterpart against which to scope it.

These two paths cannot fire simultaneously because the second one is gated on **zero** successes (no partition produced a non-DNSP outcome), and the first one is gated on **≥1** success. The two are logically disjoint.

**Practical implication for FR-CONV.6 design:** the synthesizer code path must check global partition success-count **before** emitting a DNSP. If success-count is 0, fall through to the existing HALT escalation; do not emit DNSPs in this branch.

## 7. Project Mode Cleanup

After line 420 (Project Mode Architecture), the file ends with a `## Cleanup` section (lines 422-431):

```
## Cleanup

When the pipeline completes:

Ask rf-task-executor to shut down
Ask rf-task-builder to shut down
Ask rf-task-researcher to shut down
Clean up the team
```

**Behavior:** When the pipeline completes — either via normal success or via HALT (line 417 escalation) — the team-lead shuts down each teammate in reverse-launch order (executor → builder → researcher) and then dissolves the team. This applies equally to:

- Normal completion (all phases pass, no fix cycles needed beyond budget).
- All-agents-fail HALT (zero partitions succeeded, line 417 escalation fires, user must intervene).
- Per-partition DNSP emission (FR-CONV.6 case: partial success surfaced, then teardown).

Cleanup is unconditional: regardless of which termination path fired, the teammates are dismissed. This means FR-CONV.6 DNSP emission must finalize all DNSP artifacts **before** the cleanup phase runs — otherwise an exhausted partition's DNSP could be lost when its corresponding partition agent is shut down.

## 8. Gaps and Questions

1. **Where is "per-partition fix cycle count" stored?** The rf-team-lead spec describes "max 3 cycles per phase" but does not show how the cycle counter is persisted across pipeline invocations. For FR-CONV.6 partition-level granularity, we need a per-partition counter — confirm whether `03_project_plan_template.md` or `phase-outputs/` carries this state.
2. **DNSP artifact location:** spec is silent on where the synthetic DNSP should be written. Candidate locations: `.dev/tasks/to-do/TASK-RF-.../qa/dnsp/<partition-id>.md` or `.../synthesis/dnsp/`. Needs decision from FR-CONV.6 TDD.
3. **Mixed-outcome regression:** the existing line-417 HALT is binary (HALT vs proceed). Once we add DNSP emission for mixed outcomes, the team-lead spec itself will need amending so the "proceed" branch includes "...with DNSP markers for exhausted partitions." This is a documentation update item for the FR-CONV.6 implementation.
4. **Ordering of cleanup vs DNSP write:** §7 above raises a race — needs explicit ordering constraint in the FR-CONV.6 TDD.
5. **Does HALT bubble up in project mode?** Line 417 says HALT on cycle exhaust, but project mode runs multiple phase pipelines sequentially. If phase N HALTs, do later phases run? Reading the spec strictly: "HALT and ask user" implies global HALT, not phase-only. FR-CONV.6 must inherit this semantic — DNSP per partition does **not** advance the phase counter.

## 9. Stale Documentation Found

**Drift verification result: NO DRIFT.**

The task brief speculated the "3 fix cycles per phase" anchor had drifted from PRD-cited line 417 to current line 414. Verbatim `sed -n '410,420p'` output shows:

- Line 414 is `- **Direct pipeline invocation**: /rf:project invokes /rf:pipeline directly via the Skill tool for each phase — the session becomes the team lead for each pipeline run sequentially`
- Line 417 is `- **Fix Cycles**: If a phase pipeline returns issues, invoke another pipeline with a FIX request (max 3 cycles per phase). If max cycles exhausted, HALT and ask user — do NOT proceed with unresolved findings.`

PRD citation of **line 417 is accurate as of 2026-05-14**, against `src/superclaude/agents/rf-team-lead.md` (431 lines total). No remediation needed for this anchor. Drift is **0 lines**.

(Sed verbatim output reproduced in §2 above is the source-of-truth artifact.)

## 10. Summary

`rf-team-lead.md` line 417 defines the all-agents-fail escalation: a phase pipeline that returns issues triggers up to 3 FIX-request retry cycles, and if all three exhaust, the team-lead HALTs and requires user intervention rather than proceeding with unresolved findings. PRD-cited line 417 is accurate against current source (zero drift); the sed-verbatim verification reproduces the rule unchanged. FR-CONV.6 DNSP emission must preserve this guard: synthetic DNSPs only fire when at least one partition succeeded AND at least one partition exhausted ("twice exhaust"), while all-partitions-exhaust falls through to the existing line-417 HALT. These two failure paths are logically disjoint by success-count, and the project-mode cleanup section (lines 422-431) requires DNSP artifacts to be persisted before teammate teardown.

---

**Status:** Complete
