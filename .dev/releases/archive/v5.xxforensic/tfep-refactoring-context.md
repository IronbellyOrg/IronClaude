# TFEP Refactoring Context: Forensic Spec Quick Mode + Task-Unified Integration

**Purpose**: Complete context brief for an agent tasked with crafting a refactoring plan to add a lightweight "quick/triage" mode to the forensic spec and integrate it as the test failure escalation mechanism in `sc:task-unified`.

**Date**: 2026-03-19
**Source**: Brainstorm + adversarial debate session on test failure handling in task-unified pipeline

---

## 1. The Problem Being Solved

### What's happening today

When `sc:task-unified` executes a tasklist and tests fail at the verification phase, the executing agent **immediately attempts ad-hoc fixes** without root cause analysis, scrutiny, or multi-perspective validation. This is dangerous:

1. **No root cause analysis** -- the agent patches symptoms, not causes
2. **No scrutiny** -- a single agent's "quick fix" bypasses the multi-perspective validation the protocol was designed to enforce
3. **Regression risk** -- ad-hoc fixes can introduce new bugs or mask the original issue
4. **Scope creep** -- the fix may touch code outside the original task scope without review

### Real-world example (transcript)

```
# Agent runs new tests -- 22 pass
# Agent then runs existing tests to check for regressions
# 10 existing tests fail with KeyError: None

"10 existing tests fail because they relied on RoadmapConfig having
hardcoded defaults and _build_steps being called with None agents/depth.
The fix: tests that construct RoadmapConfig directly without agents/depth
need to provide them explicitly now. Let me fix these:"

# Agent immediately starts editing tests -- NO investigation,
# NO alternatives considered, NO validation of root cause
```

### What we want instead

**Agents MUST BE prohibited from fixing anything ad-hoc mid-task.** When bugs are found or tests fail above a severity threshold, the agent must halt and enter a structured escalation protocol.

---

## 2. Decision: Forensic Command Integration (Not Baked In)

An adversarial debate evaluated two approaches:

| Approach | Score |
|----------|-------|
| A: Bake TFEP directly into task-unified protocol | 4.62/10 |
| B: Refactor forensic spec to have a quick mode, task-unified calls it | **7.85/10** |

### Why Artifact B won

| Criterion | A (Baked In) | B (Via Forensic) |
|-----------|-------------|-----------------|
| Single Responsibility | 4/10 -- task-unified becomes both orchestrator AND bug investigator | 9/10 -- each command does one thing |
| Protocol bloat | 3/10 -- adds 500+ lines to already complex skill | 8/10 -- adds ~50 lines to task-unified |
| Reusability | 2/10 -- TFEP locked inside task-unified only | 9/10 -- any command can call forensic |
| Escalation gradient | 3/10 -- all-or-nothing pipeline | 9/10 -- quick -> standard -> deep |
| Maintenance burden | 4/10 -- two divergent pipelines when forensic ships | 8/10 -- single source of truth |
| Checkpoint/resume | 2/10 -- not specified | 8/10 -- inherited from forensic |

### Key architectural argument

TFEP is literally a subset of the forensic pipeline. The mapping is 1:1:

| TFEP Step | Forensic Phase |
|-----------|---------------|
| Capture failure context | Phase 0 (Reconnaissance) |
| 2 parallel troubleshoot agents for RCA | Phase 1 (Root-Cause Discovery) |
| Adversarial debate on root causes | Phase 2 (Adversarial Debate - Hypotheses) |
| 2 parallel brainstorm agents for solutions | Phase 3 (Fix Proposals) |
| Adversarial debate on solutions | Phase 3b (Adversarial Debate - Fixes) |
| Implement fix and retest | Phase 4-5 (Implementation + Validation) |

Baking it into task-unified means writing a second, less-capable version of the same pipeline. When full forensic ships, you'd have two competing systems.

---

## 3. What the Refactoring Plan Must Produce

### 3.1 A new `--depth quick` mode in the forensic spec

The current forensic spec (`forensic-spec.md`) defines `--depth quick|standard|deep` but maps it **only** to adversarial debate depth (FR-038). The refactoring must expand `--depth` to affect the entire pipeline:

**Quick mode behavior (the TFEP equivalent):**

| Forensic Phase | Quick Mode | Standard Mode | Deep Mode |
|----------------|-----------|---------------|-----------|
| Phase 0 (Recon) | **SKIP** -- caller provides context | 3 Haiku agents | 3 Haiku agents |
| Phase 1 (RCA) | **2 agents** (fixed), Sonnet, `/sc:troubleshoot` prompts | N agents (3-10), model-tiered | N agents (3-10), model-tiered |
| Phase 2 (Debate-H) | `/sc:adversarial --depth quick` | `/sc:adversarial --depth deep` | `/sc:adversarial --depth deep` |
| Phase 3 (Fix) | **2 agents** (fixed), `/sc:brainstorm` prompts | M agents (per cluster), Sonnet | M agents (per cluster), Sonnet |
| Phase 3b (Debate-F) | `/sc:adversarial --depth quick` | `/sc:adversarial --depth standard` | `/sc:adversarial --depth deep` |
| Phase 4 (Implement) | **SKIP** -- returns fix plan to caller | Specialist agents | Specialist agents |
| Phase 5 (Validate) | **SKIP** -- caller handles retesting | 3 validation agents | 3 validation agents |
| Phase 6 (Report) | **Abbreviated** `tfep-report.md` | Full `final-report.md` | Full `final-report.md` |

**Token budget for quick mode**: ~5-8K total (vs 50-80K for standard/deep).
**Agent count for quick mode**: 4 agents + 2 adversarial rounds = 6 invocations.

### 3.2 A new `--mode triage` option

The current spec defines `--mode debug|qa|regression|auto`. The refactoring should add:

- `--mode triage`: Optimized for "tests just failed, tell me why and how to fix it." Implies:
  - Caller provides failure context (no Phase 0 needed)
  - Focus is on the specific failure, not broad codebase investigation
  - Output is a fix plan, not a full report

### 3.3 Caller-provided context interface

Quick/triage mode needs an interface for the caller (task-unified) to pass in failure context instead of forensic running its own reconnaissance. This must include:

```yaml
# Context package passed from task-unified to forensic
failure_context:
  test_names: ["test_no_model_when_empty", "test_routing_with_agents", ...]
  test_files: ["tests/roadmap/test_cli_contract.py"]
  error_output: |
    E   KeyError: None
    tests/roadmap/test_cli_contract.py:85: in test_no_model_when_empty
    ...
  expected_behavior: "Tests should pass -- they were passing before this task"
  actual_behavior: "10 tests fail with KeyError: None"
  changes_made:
    - file: "src/superclaude/cli/roadmap/models.py"
      description: "Changed RoadmapConfig defaults"
    - file: "src/superclaude/cli/roadmap/executor.py"
      description: "Modified _build_steps to require explicit agents/depth"
  task_description: "Add resume/restore capability to roadmap CLI"
```

This may be a `--context <file>` flag or inline structured input. The refactoring plan must define this interface.

### 3.4 Integration point in task-unified

A small (~50-100 line) addition to `sc-task-unified-protocol/SKILL.md` that:

1. **Prohibits** ad-hoc fixes (CRITICAL/VIOLATION-level language)
2. **Detects** escalation triggers (threshold rules)
3. **Invokes** `/sc:forensic --depth quick --mode triage` with context
4. **Handles** escalation gradient (quick -> standard -> stop)
5. **Resumes** after fix with `--compliance strict`
6. **Reports** TFEP incidents in a standalone `tfep-report.md`

### 3.5 Artifact directory for quick mode

```
{output_dir}/                    # Specified by caller or default .forensic-qa/
  context.md                     # Caller-provided failure context
  phase-1/
    rca-alpha.md                 # Troubleshoot agent A findings
    rca-bravo.md                 # Troubleshoot agent B findings
  phase-2/
    adversarial/                 # Standard adversarial output
      debate-transcript.md
      base-selection.md
  rca-verdict.md                 # Synthesized root cause verdict
  phase-3/
    solution-alpha.md            # Brainstorm agent A proposal
    solution-bravo.md            # Brainstorm agent B proposal
  phase-3b/
    adversarial/                 # Standard adversarial output
      debate-transcript.md
      base-selection.md
  solution-verdict.md            # Synthesized solution verdict
  tfep-report.md                 # Abbreviated final report
  progress.json                  # Checkpoint (reuses existing schema)
```

**All artifacts MUST be committed to git** (user decision).

---

## 4. Escalation Threshold Rules

These are the rules for when task-unified triggers TFEP vs allowing the agent to fix directly.

### MUST escalate (trigger TFEP)

- **Any pre-existing test fails** -- tests that existed before this task and were not modified by the agent. This is the primary scenario (the transcript example).
- **3 or more new tests fail** -- indicates a systemic issue, not a simple typo.
- **Runtime exceptions in implementation code** -- TypeError, AttributeError, KeyError, etc. in the code being tested (not in the test scaffolding itself).

### MAY fix directly (no escalation)

- **Single ImportError/NameError in test scaffolding just written** -- agent just wrote a test and got the import path wrong. Affects <=2 tests. Error is in the test file itself, not the implementation.
- **Lint/formatting failures** -- trivially fixable, no ambiguity about root cause.
- **Deprecation warnings** -- not failures.

### Escalation gradient on repeated failures

```
1st TFEP trigger  -> /sc:forensic --depth quick --mode triage    (~5-8K tokens)
2nd TFEP trigger  -> /sc:forensic --depth standard               (~15-20K tokens)
3rd TFEP trigger  -> FULL STOP. Report to user. Do not attempt further.
```

---

## 5. TFEP Agent Prompting Requirements

### Phase 1: Root Cause Analysis agents

**CRITICAL**: Each agent's prompt MUST begin with `/sc:troubleshoot`.

The main agent provides each troubleshoot agent with:
- Full failure context (test names, errors, expected vs actual)
- What code was changed as part of the task
- What tests were passing before
- Ask: "Think through and propose a root cause"
- Output: Save to a unique `.md` file (e.g., `rca-alpha.md`, `rca-bravo.md`)

These 2 agents run **in parallel**.

### Phase 2: RCA Debate

Main agent invokes: `/sc:adversarial --compare rca-alpha.md,rca-bravo.md --depth quick`

The adversarial process:
- Debates both root causes
- Determines the best one
- Refactors/improves based on debate findings
- Saves to `rca-verdict.md`

### Phase 3: Solution Brainstorm agents

**CRITICAL**: Each agent's prompt MUST begin with `/sc:brainstorm`.

Each receives:
- Failure context
- The RCA verdict
- Ask: "Propose a solution with implementation steps"
- Output: Save to a unique `.md` file (e.g., `solution-alpha.md`, `solution-bravo.md`)

These 2 agents run **in parallel**.

### Phase 3b: Solution Debate

Main agent invokes: `/sc:adversarial --compare solution-alpha.md,solution-bravo.md --depth quick`

The adversarial process:
- Debates both solutions
- Determines the best one
- Improves based on debate findings
- Saves to `solution-verdict.md`

### Post-TFEP: Tasklist integration

The winning solution (with implementation steps) is:
1. **Appended to the current tasklist** as new task(s), inserted **before** the test/verification tasks
2. Formatted as proper tasklist entries compatible with `sc:task-unified`

### Resume

Agent resumes with `/sc:task-unified --compliance strict` to implement the fix tasks and then retest.

---

## 6. Existing Forensic Spec Structure (What Gets Refactored)

The current forensic spec is at: `.dev/releases/backlog/v5.xxforensic/forensic-spec.md`

### Current structure (unchanged sections)

These sections likely need no changes or minimal changes:
- Section 1: Purpose and Scope (add quick mode to scope)
- Section 2: Definitions and Glossary (add "triage" and "TFEP" definitions)
- Section 4: Architecture (add quick mode data flow diagram)
- Section 8: Agent Specifications (already covers all needed agents)
- Section 9: Data Schemas (may need a failure context schema)
- Section 11: MCP Routing Table (quick mode uses fewer MCP servers)
- Section 14: Error Handling (add TFEP-specific error cases)
- Section 15: Cross-References (update task-unified cross-reference)

### Sections requiring significant refactoring

**Section 3: Requirements**
- FR-038 (`--depth`) must be expanded from "maps to adversarial depth" to "controls entire pipeline profile"
- New FRs needed for: `--mode triage`, `--context <file>`, quick mode phase skipping, caller-provided context interface
- FR-037 (`--mode`) needs `triage` added to enum

**Section 5: Command Definition**
- Flag table needs `--context` flag
- `--mode` enum needs `triage`
- `--depth` description needs expansion
- New examples for quick/triage usage
- Boundaries need update (caller-provided context)

**Section 7: Phase Specifications**
- Each phase (0-6) needs a "Quick Mode Behavior" subsection or annotation
- Phase 0 needs "SKIP when --depth quick" logic
- Phase 1 needs "Fixed 2 agents with /sc:troubleshoot prompts when --depth quick"
- Phase 3 needs "Fixed 2 agents with /sc:brainstorm prompts when --depth quick"
- Phase 4-5 need "SKIP when --depth quick" logic
- Phase 6 needs abbreviated report template for quick mode

**Section 10: Model Tier Decision Matrix**
- Quick mode uses Sonnet for all 4 agents (no Haiku/Opus tiering)
- Add quick mode column to the matrix

**Section 12: Checkpoint and Resume**
- Quick mode artifact directory structure (simpler than full)
- Quick mode has fewer phases to checkpoint

**Section 13: Output Templates**
- New abbreviated `tfep-report.md` template for quick mode

**Section 16: Quality Attributes**
- Token budget for quick mode (~5-8K)
- Quality metrics for quick mode

### New sections needed

**Section 18: Task-Unified Integration**
- TFEP trigger detection rules (threshold from Section 4 above)
- Failure context package schema
- Invocation pattern from task-unified
- Escalation gradient (quick -> standard -> stop)
- Tasklist integration format
- Resume behavior
- `--no-escalation` escape hatch

**Section 19: Quick Mode Specification**
- Consolidated quick mode behavior across all phases
- Differences from standard/deep modes
- Token budget breakdown
- Agent prompting requirements (troubleshoot/brainstorm prefixes)

---

## 7. Files That Need Changes

### Primary target (refactoring)

| File | Change Type | Scope |
|------|------------|-------|
| `.dev/releases/backlog/v5.xxforensic/forensic-spec.md` | **Major refactor** | Add quick mode, triage mode, caller context interface, task-unified integration section |

### Secondary targets (new or modified)

| File | Change Type | Scope |
|------|------------|-------|
| `src/superclaude/skills/sc-task-unified-protocol/SKILL.md` | **Add section** | ~50-100 lines: TFEP prohibition, trigger detection, forensic invocation, escalation gradient |
| `src/superclaude/commands/task-unified.md` | **Minor update** | Add `--no-escalation` flag docs, mention TFEP in boundaries |
| `src/superclaude/skills/sc-task-unified-protocol/refs/tfep.md` | **New file** | Detailed TFEP behavioral reference (optional -- may keep inline in SKILL.md given small size) |

### Sync targets (after source changes)

After editing `src/superclaude/`, run `make sync-dev` to propagate to:
- `.claude/skills/sc-task-unified-protocol/SKILL.md`
- `.claude/commands/sc/task-unified.md`

---

## 8. Implementation Phasing (from adversarial verdict)

The adversarial debate recommended a two-phase approach:

### Phase 1: Immediate guard (this sprint)

Add the TFEP **prohibition rule** and **trigger detection** to task-unified NOW, even before forensic quick mode exists. When triggered, the agent STOPS and tells the user to run `/sc:forensic --depth quick` manually or use `--no-escalation`. This is ~30 lines in SKILL.md.

**Value**: Immediately blocks ad-hoc fixes. Zero dependency on forensic being built.

### Phase 2: Full integration (forensic quick mode)

Build the forensic quick mode. Once available, update the Phase 1 rule so task-unified **automatically invokes** forensic instead of prompting the user.

**Value**: Fully automated TFEP pipeline. No user intervention needed.

---

## 9. Key Constraints and Decisions

| Decision | Resolution | Rationale |
|----------|-----------|-----------|
| Artifacts committed to git | **Yes** | User requirement |
| User notification during TFEP | **Autonomous** -- proceed through all phases, report at end | User requirement |
| CLI code changes needed | **None** -- purely protocol-level | User requirement |
| Naming | **TFEP** (Test Failure Escalation Protocol) | User approved |
| Threshold: every failure triggers? | **No** -- only actual code bugs above threshold | User requirement |
| Report format | **Standalone** `tfep-report.md` per escalation | User approved |
| Max escalation iterations | **3** then full stop | Adversarial recommendation |
| "Test is wrong" as valid outcome | **Yes** -- adversarial debate can conclude test expectations are outdated | Brainstorm decision |

---

## 10. Cross-References

| Document | Path | Relevance |
|----------|------|-----------|
| Forensic spec (target) | `.dev/releases/backlog/v5.xxforensic/forensic-spec.md` | Primary refactoring target |
| Forensic exploration | `.dev/releases/backlog/v5.xxforensic/forensic-explore.md` | Original exploratory analysis |
| Task-unified command | `src/superclaude/commands/task-unified.md` | Secondary change target |
| Task-unified protocol | `src/superclaude/skills/sc-task-unified-protocol/SKILL.md` | Secondary change target |
| Adversarial command | `src/superclaude/commands/adversarial.md` | Dependency (invoked by TFEP) |
| Adversarial protocol | `src/superclaude/skills/sc-adversarial-protocol/SKILL.md` | Dependency (invoked by TFEP) |
| Troubleshoot command | `src/superclaude/commands/troubleshoot.md` | Dependency (RCA agents use this) |
| Brainstorm command | `.claude/commands/sc/brainstorm.md` | Dependency (solution agents use this) |
| Proposal verdicts | `.dev/releases/backlog/v5.xxforensic/proposal-verdicts.md` | Prior expert panel review |
| Spec review proposals | `.dev/releases/backlog/v5.xxforensic/spec-review-proposals.md` | Prior spec review |
