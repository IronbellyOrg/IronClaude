---
total_diff_points: 12
shared_assumptions_count: 14
---

## 1. Shared Assumptions and Agreements

Both variants agree on the following foundational points:

1. **Source spec**: Both reference `prd-refactor-spec-v2.md` with complexity score 0.45 and architect persona
2. **Core objective**: Decompose monolithic 1,369-line SKILL.md into three-tier architecture (command → skill → refs/)
3. **Zero behavioral change**: Both treat this as a structural refactor with no runtime behavior modifications
4. **Target file count**: Exactly 4 refs/ files + 1 command + 1 trimmed SKILL.md = 6 files total
5. **SKILL.md line budget**: 400-500 lines post-trim
6. **Command file line budget**: 100-170 lines
7. **Combined line count**: 1,380-1,520 across all 6 files
8. **BUILD_REQUEST constraint**: Exactly 6 path changes, no other modifications
9. **Risk inventory**: Both identify the same 9 risks at identical severity levels (3 HIGH, 5 MEDIUM, 1 LOW)
10. **Critical path**: Linear phase dependency with internal parallelism opportunities
11. **Sync gate**: Both require `make sync-dev` + `make verify-sync` before completion
12. **Activation pattern**: Both mandate `Skill prd` invocation + "Do NOT proceed" warning
13. **Template source**: Both use `adversarial.md` as the command file scaffold
14. **Fidelity verification**: Both require block-level diffs against original SKILL.md line ranges

---

## 2. Divergence Points

### D1: Phase Count and Granularity

- **Opus**: 4 phases (Foundation Verification → Create Artifacts → Decomposition → Fidelity/Sync)
- **Haiku**: 5 phases (Baseline Lock → Command Layer → SKILL Decomposition + Refs → Integration Wiring → Fidelity/Sync)
- **Impact**: Opus groups refs verification with a dedicated upfront phase; Haiku adds Phase 0 for governance setup and separates integration wiring (Phase 3) from decomposition (Phase 2). Haiku's Phase 0 adds explicit baseline freezing but also adds ceremony. Opus's approach is more streamlined for a solo implementer.

### D2: Ordering of Refs Verification vs Command Creation

- **Opus**: Verifies existing 3 refs/ files first (Phase 1), then creates command file and build-request ref (Phase 2)
- **Haiku**: Creates command file first (Phase 1), verifies/completes refs during SKILL decomposition (Phase 2)
- **Impact**: Opus's order is **safer** — it confirms the foundation before building on it. If existing refs have drifted, Opus catches this before any new work begins. Haiku risks building the command layer on assumptions about refs that haven't been verified yet.

### D3: Milestone Count and Naming

- **Opus**: 7 milestones (M1-M7) with specific gate conditions per milestone
- **Haiku**: 5 milestones (M0-M4) with broader scope per milestone
- **Impact**: Opus's finer granularity provides more checkpoints and earlier failure detection. Haiku's coarser milestones are simpler to track but offer fewer opportunities to catch issues mid-phase.

### D4: Effort Estimates

- **Opus**: Explicit time estimates per phase (30-45 min, 1-1.5 hrs, 1-1.5 hrs, 45-60 min) totaling 3.25-4.75 hours
- **Haiku**: Uses abstract "Sprint Slot" units (Slot 1, Slot 2, Slot 3) with no time conversion
- **Impact**: Opus gives actionable scheduling data. Haiku's Sprint Slot abstraction is framework-appropriate but leaves the implementer guessing at actual duration. For a solo task like this, Opus's approach is more practical.

### D5: Task Decomposition Granularity

- **Opus**: 47 explicitly numbered sub-steps across all phases with per-step verification criteria
- **Haiku**: ~20 numbered actions across phases, described at a higher level of abstraction
- **Impact**: Opus is directly executable as a task checklist — an implementer can follow it step-by-step with minimal interpretation. Haiku requires the implementer to decompose actions further during execution, which introduces ambiguity risk.

### D6: Governance/Baseline Phase

- **Opus**: No explicit baseline phase; assumes git provides rollback capability and jumps to verification
- **Haiku**: Includes Phase 0 for baseline freezing, acceptance matrix creation, and governance lock
- **Impact**: Haiku's Phase 0 is more methodologically rigorous for team settings. For a solo implementer with git, Opus's implicit baseline (git HEAD) is pragmatically equivalent with less overhead.

### D7: Team Role Assumptions

- **Opus**: Written for a solo implementer; no role assignments
- **Haiku**: Defines 3 team roles (Architect/Tech Lead, Docs/Skill Engineer, QA/Validation Engineer)
- **Impact**: Haiku's role separation is good practice for team execution but overspecifies for what both variants score as a 0.45 complexity solo task. Opus matches the expected execution context.

### D8: Integration Points Documentation

- **Opus**: Provides a wiring table embedded in Phase 3 with mechanism types, owning phases, and consuming phases
- **Haiku**: Provides integration points as a standalone section at the end with cross-reference pointers
- **Impact**: Opus's approach ties wiring to the phase that owns it, making it actionable during implementation. Haiku's standalone section is better for architectural review but disconnected from execution flow.

### D9: Parallelism Documentation

- **Opus**: Explicitly marks which steps can run in parallel within each phase (e.g., "Steps 2.1 and 2.2 are independent")
- **Haiku**: Notes parallelism at phase level ("refs fidelity checks can run in parallel with SKILL trimming") but doesn't mark individual steps
- **Impact**: Opus's per-step parallelism annotations enable a tool or agent to maximize concurrent execution. Haiku's phase-level notes require the implementer to determine step-level parallelism.

### D10: Success Criteria Presentation

- **Opus**: 12-row validation table with specific test commands and pass/fail definitions
- **Haiku**: 8-item validation matrix referencing FR/NFR requirement IDs + a separate measurable checks list
- **Impact**: Opus's table is directly executable as a test script. Haiku's approach requires dereferencing requirement IDs to understand what's being tested, adding an indirection step.

### D11: Developer Guide Reference

- **Opus**: Does not explicitly reference the Developer Guide as a dependency
- **Haiku**: Includes `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` as a governance authority dependency
- **Impact**: Haiku's explicit governance reference is more traceable for auditing compliance. Minor practical difference since both variants implement the same constraints.

### D12: Rollback Strategy

- **Opus**: Explicit rollback plan in validation section: `git checkout -- .claude/skills/prd/ .claude/commands/sc/prd.md`
- **Haiku**: Implicit rollback via baseline phase; no explicit rollback command documented
- **Impact**: Opus provides a copy-pasteable recovery command. Haiku assumes the implementer knows how to use git for recovery.

---

## 3. Areas Where One Variant Is Clearly Stronger

### Opus is stronger in:

- **Executability**: 47 numbered sub-steps with per-step verification make it directly usable as a task checklist without further decomposition
- **Time estimates**: Concrete hour ranges vs abstract Sprint Slots
- **Parallelism annotations**: Per-step concurrency markers enable automated execution
- **Rollback plan**: Explicit recovery command documented
- **Success criteria**: Executable test table with specific commands
- **Line-range precision**: Maps every extraction to specific SKILL.md line numbers throughout

### Haiku is stronger in:

- **Governance rigor**: Phase 0 baseline lock and explicit Developer Guide dependency
- **Team scalability**: Role definitions enable delegation if scope grows
- **Requirement traceability**: Every action maps to FR/NFR IDs, making compliance auditing straightforward
- **Architectural priority ordering**: Explicitly states priority hierarchy (governance → fidelity → wiring → budgets → sync)

---

## 4. Areas Requiring Debate to Resolve

1. **Phase 0 necessity**: Is an explicit baseline/governance phase worth the overhead for a solo 0.45-complexity task, or is git HEAD sufficient? Opus says no; Haiku says yes. Resolution depends on whether this roadmap will be executed by a single agent or reviewed by a team.

2. **Refs verification ordering**: Should refs be verified before (Opus) or during (Haiku) the main decomposition work? Opus's approach is safer but adds a blocking phase. Haiku's approach is faster if refs are correct but riskier if they've drifted. The answer depends on confidence in the existing refs — if drift is likely, Opus wins; if drift is unlikely, Haiku's integration is more efficient.

3. **Granularity level**: Opus's 47-step checklist vs Haiku's 20-action plan. Over-specification risks rigidity if the implementer encounters unexpected structure. Under-specification risks ambiguity and missed steps. The right level depends on the executor's familiarity with the codebase.

4. **Sprint Slot vs hours**: Should effort be expressed in abstract slots (portable across teams) or concrete hours (actionable for this task)? For roadmap-to-tasklist pipeline consumption, Sprint Slots may integrate better with existing tooling; for human planning, hours are more useful.
