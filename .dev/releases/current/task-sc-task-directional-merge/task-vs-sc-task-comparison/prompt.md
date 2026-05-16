# Task-Command Deep Analysis Sprint — Bootstrapping Prompt

> **Usage**: Paste this entire prompt into a fresh Claude Code session opened at `/config/workspace/IronClaude`. It will generate a sprint-compatible tasklist that can be executed via `superclaude sprint run`.

---

## Context

You have access to **one repository** with **two overlapping task-execution surfaces** that share naming but diverge in behavior, scope, and intended workflow:

1. **`/sc:task` — Unified Task Command (orchestration / classification front door)**

   | Component | Location | Purpose |
   |-----------|----------|---------|
   | Command file | `.claude/commands/sc/task.md` | Slash-command entry point; declares MCP servers, personas, allowed tools |
   | Source-of-truth | `src/superclaude/commands/task.md` | Canonical command definition (synced into `.claude/`) |
   | Execution protocol | `.claude/skills/sc-task-protocol/SKILL.md` | Tier-classified execution (STRICT/STANDARD/LIGHT/EXEMPT) for new work |
   | Source-of-truth | `src/superclaude/skills/sc-task-protocol/` | Canonical skill package |
   | Tier classification table | inside `sc-task-protocol/SKILL.md` | Keyword/scope → tier mapping; emits classification header |
   | TFEP (Test Failure Escalation Protocol) | inside `sc-task-protocol/SKILL.md` | Forensic pipeline trigger on threshold breach |

2. **`/task` — MDTM Task File Executor (disciplined execution loop)**

   | Component | Location | Purpose |
   |-----------|----------|---------|
   | Skill package | `.claude/skills/task/SKILL.md` | F1 execution loop (READ → IDENTIFY → EXECUTE → UPDATE → REPEAT) over pre-written MDTM task files |
   | Source-of-truth | `src/superclaude/skills/task/` | Canonical skill package |
   | Companion builder | `.claude/skills/task-builder/SKILL.md` | Creates the MDTM task files that `/task` consumes |
   | Phase-gate QA mechanism | inside `task/SKILL.md` | Mandatory `rf-qa` subagent verification between phases |
   | Subagent vocabulary | inside `task/SKILL.md` | `rf-analyst`, `rf-qa`, `rf-qa-qualitative`, `rf-assembler`, `rf-task-builder`, `rf-task-researcher`, `Explore`, `general-purpose` |
   | MDTM file consumers | `.dev/tasks/to-do/TASK-*/TASK-*.md` | Concrete task files (real-world usage evidence) |

**Critical context**: These two surfaces were authored at different times, share lexical neighborhood (`task`, `task-protocol`, `task-builder`), have **identical marketing language** ("Unified task execution with intelligent workflow management, MCP compliance enforcement, and multi-agent delegation" appears verbatim in both `sc:task` command frontmatter AND `sc:task-protocol` skill frontmatter), yet operate at fundamentally different abstraction levels. The output of this sprint must determine whether their coexistence is **intentional and useful**, **redundant and confusing**, or **complementary but mis-documented**.

## Your Task

Generate a complete sprint tasklist (index + phase files) in the format used by SuperClaude's sprint CLI. Write the files to:

```
.dev/releases/current/task-vs-sc-task-comparison/
├── tasklist-index.md
├── phase-1-tasklist.md
├── phase-2-tasklist.md
├── phase-3-tasklist.md
├── phase-4-tasklist.md
├── phase-5-tasklist.md
├── phase-6-tasklist.md
├── phase-7-tasklist.md
└── phase-8-tasklist.md
```

### Sprint Format Requirements

**Index file** must contain a metadata table and phase file references in this pattern:
```markdown
| Phase N Tasklist | `TASKLIST_ROOT/phase-N-tasklist.md` |
```

**Phase files** must use this task format:
```markdown
### T{NN}.{NN} — {Task Title}
**Roadmap Item IDs**: {cross-refs}
**Tier**: {STRICT|STANDARD|LIGHT|EXEMPT}
**Effort**: {XS|S|M|L|XL}
**Steps**: numbered [VERB] steps
**Acceptance Criteria**: numbered list
**Validation**: numbered list
**Dependencies**: {task IDs or "None"}
```

Task IDs follow `T{phase}.{sequence}` pattern (e.g., T01.01, T03.05). Monitor regex: `T\d{2}\.\d{2}`.

### Sprint Structure (8 Phases)

Design the sprint with these 8 phases. Each phase should have 3–6 tasks. Every task must use the auggie MCP codebase-retrieval tool (`mcp__auggie-mcp__codebase-retrieval`) as the primary search mechanism, with `directory_path` set to `/config/workspace/IronClaude`.

---

#### Phase 1: Surface Inventory & Artifact Mapping
**Goal**: Build a complete inventory of every artifact tied to each task surface.

Tasks should:
- Use auggie MCP to enumerate every file that participates in `/sc:task`: the command file, the protocol skill, supporting templates/rules/scripts, declared MCP servers, declared personas, allowed tools, every agent named in the skill body
- Do the same enumeration for `/task`: skill file, companion `task-builder`, MDTM file format reference, every subagent type the F1 loop spawns, every "Prohibited actions" rule
- Trace dependency edges: which agents, MCP servers, hook scripts, settings keys, and skills each surface depends on at execution time
- Produce a structured `surface-inventory.md` artifact with one row per artifact, columns: surface (`/task` or `/sc:task`), artifact path, role (entry point | protocol | template | rule | agent | hook | setting), source-of-truth location, sync status with `.claude/`
- Identify any shared artifacts (e.g., both surfaces invoke `rf-qa`) — these become the seams where comparison sharpens

---

#### Phase 2: Strategy Extraction — `/sc:task` Deep Dive
**Goal**: Extract the design strategy, execution model, and enforcement mechanism of `/sc:task`.

Tasks should:
- Use auggie MCP + `/sc:analyze --focus architecture` patterns on the `/sc:task` command and `sc:task-protocol` skill
- Extract:
  - **Triggering surface**: how a user invokes it; what input shape is expected
  - **Classification model**: the tier decision tree (STRICT/STANDARD/LIGHT/EXEMPT), keyword/scope inputs, emitted classification header semantics
  - **Per-tier execution flow**: distinct step counts and gates per tier; which tier invokes which skills/subagents
  - **TFEP (Test Failure Escalation Protocol)**: thresholds, forensic pipeline integration, escalation outputs
  - **MCP and persona coupling**: declared servers (sequential, context7, serena, playwright, magic, morphllm) and personas (architect, analyzer, qa, refactorer, frontend, backend, security, devops, python-expert, quality-engineer) — and which actually get used per tier
  - **Boundary**: where `/sc:task` hands off to other skills (e.g., does it ever produce an MDTM file that `/task` consumes?)
- Document strengths AND weaknesses honestly (no sycophancy): where the tier model adds discipline, where it adds ceremony with no behavioral teeth
- Produce `strategy-sc-task.md`

---

#### Phase 3: Strategy Extraction — `/task` Deep Dive
**Goal**: Extract the design strategy, execution model, and enforcement mechanism of `/task`.

Tasks should:
- Use auggie MCP + `/sc:analyze --focus architecture` patterns on the `task` skill and `task-builder` companion
- Extract:
  - **Triggering surface**: F1 loop entry — how a task file is identified, parsed, and processed
  - **F1 loop semantics**: READ → IDENTIFY first unchecked `- [ ]` → EXECUTE exactly as written → UPDATE to `- [x]` → REPEAT; what "exactly as written" forbids and permits
  - **Prohibited actions catalog**: every "do not" rule (no working from memory, no skipping items, no modifying checklist items, no delegating the F1 loop itself) — and the failure mode each prevents
  - **Parallel subagent spawning rules**: when independent items within a phase are batched; the safety constraints
  - **Phase-gate QA**: mandatory `rf-qa` invocation between phases, post-completion `rf-qa` + `rf-qa-qualitative` invocation; what they check
  - **Resumability**: how progress is recovered from disk after context compression / session restart
  - **Boundary**: what the skill explicitly refuses to do (create task files, define what work to do, prescribe which agents) and why those refusals are load-bearing
- Document what makes `/task` rigorous AND what makes it inflexible / verbose / costly when applied to simple work
- Produce `strategy-task.md`

---

#### Phase 4: Cross-Surface Comparison & Debate
**Goal**: Systematically compare `/sc:task` and `/task` across multiple dimensions and debate where each wins.

Tasks should:
- Use `/sc:adversarial` patterns — for each comparison dimension, structure a position-versus-position debate with citation evidence
- Use auggie MCP to pull specific file:line evidence for every claim
- For each dimension: identify what `/sc:task` does better, what `/task` does better, what is fundamentally different (not just tactically different), and what is compatible vs incompatible if they were merged
- Apply anti-sycophancy: every "strength" claim must have a corresponding "weakness" or trade-off documented (R-RULE-04 below)
- Produce one `comparison-{dimension}.md` artifact per dimension
- Required comparison dimensions (minimum):
  1. **Triggering surface**: command (`/sc:task ...`) vs skill-on-file (`/task .dev/tasks/...`) — UX, discoverability, error modes
  2. **Work definition locus**: classified-on-the-fly (`/sc:task`) vs pre-written checklist (`/task`) — flexibility, auditability, fidelity
  3. **Execution model**: tier-branched per-step protocol (`/sc:task`) vs F1 loop (`/task`) — determinism, resumability, drift resistance
  4. **Agent / persona orchestration**: declared personas + skill-routed subagents (`/sc:task`) vs MDTM-embedded subagent prompts (`/task`) — coupling, reusability
  5. **QA / validation gates**: TFEP + tier-defined acceptance (`/sc:task`) vs phase-gate `rf-qa` + post-completion `rf-qa-qualitative` (`/task`) — coverage, false-pass risk
  6. **MCP integration profile**: command-declared `mcp-servers` list (`/sc:task`) vs skill-allowed-tools list (`/task`) — runtime guarantees vs aspirations
  7. **Failure semantics**: classification-driven escalation (`/sc:task`) vs prohibited-actions list + dead-loop detection (`/task`) — recovery vs prevention

---

#### Phase 5: Synthesis — Coexistence Decision
**Goal**: Synthesize comparison results into a definitive answer: do `/task` and `/sc:task` **merge**, **coexist with clarified boundaries**, or does one **deprecate** the other?

Tasks should:
- Use `/sc:adversarial --depth deep` patterns to merge Phase 4 verdicts into one decision per dimension, then aggregate into a single recommendation
- For each comparison dimension, define: the merged or boundary-clarified position, what to adopt from each side, what to discard, the rationale, and the cost of getting it wrong
- Explicitly evaluate three end-states:
  - **(a) Merge**: collapse into a single surface — what is lost, what is gained, what backwards-compat path exists for existing MDTM task files and slash command invocations
  - **(b) Coexist with clarified boundaries**: keep both, but enforce a non-overlapping contract — e.g., "/sc:task always emits an MDTM file that /task then executes" — and codify the contract in documentation and a hook
  - **(c) Deprecate one**: pick a winner — which, why, and the migration path
- Apply the "adopt patterns not implementation mass" principle — extract the *control patterns* (classification header, F1 loop, phase-gate QA) and reject ceremony that has no behavioral teeth
- Produce `synthesis-decision.md` — the recommended end-state with explicit "rejected alternatives" subsection
- Produce a `boundary-contract.md` if end-state (b) is recommended

---

#### Phase 6: Refactoring Plan Generation
**Goal**: Convert the synthesis decision into concrete, actionable refactoring plans.

Tasks should:
- Use `/sc:roadmap` patterns to convert the decision into an implementation roadmap with dependency graph
- For every file change implied by the decision, produce a row with:
  - File path (must exist in repo — verify via auggie before writing the row)
  - What changes (rename, merge, delete, split, edit-in-place)
  - Why this change is required by the synthesis
  - Priority tier (P0/P1/P2/P3)
  - Effort estimate (XS/S/M/L/XL)
  - Dependencies on other changes in the plan
  - Acceptance criteria (observable post-condition)
  - Risk assessment (what breaks if applied incorrectly)
- Include refactors of the **distribution surface** if needed: `src/superclaude/commands/`, `src/superclaude/skills/`, the `superclaude install` CLI behavior, and `make sync-dev` semantics
- Include refactors of any **stale references**: `.dev/releases/backlog/*` artifacts that still call the surface `task-unified`, hook scripts, settings.json entries, README rows
- Produce per-area `refactor-{area}.md` artifacts (areas: command, skill, distribution, references, documentation)
- Produce `refactor-master.md` — the unified plan with dependency graph and recommended execution order

---

#### Phase 7: Validation & Adversarial Review
**Goal**: Validate the refactoring plan through adversarial challenge.

Tasks should:
- Use `/sc:adversarial` to debate the refactoring plan itself: is it complete? Is it over-engineered? Does it actually resolve the duplication / ambiguity it set out to resolve?
- Use auggie MCP to **re-verify every file reference** in the plan still exists and the proposed change is compatible with current code (catch drift between Phase 6 and Phase 7)
- Check for scope creep: does the plan stay within "patterns not mass"? Are there changes that would feel good but don't move the synthesis verdict forward?
- Check for missing connections: did any Phase 4 comparison dimension fail to produce a corresponding Phase 6 refactor (or an explicit "no change required" justification)?
- Check for compat hazards: does the plan break any in-flight MDTM task file under `.dev/tasks/to-do/`? Does it break any sprint already in progress under `.dev/releases/current/`?
- Produce `validation-report.md` with pass/fail per plan item and per comparison dimension
- Produce `final-refactor-plan.md` — the validated, corrected master plan

---

#### Phase 8: Sprint Checkpoint & Artifact Assembly
**Goal**: Assemble all artifacts into a navigable deliverable and validate sprint completeness.

Tasks should:
- Build `artifact-index.md` linking every artifact produced in Phases 1–7
- Verify traceability: every artifact in Phase 1 inventory → has strategy extraction in Phase 2 or 3 → has at least one comparison dimension touching it in Phase 4 → has a position in the Phase 5 synthesis → has a Phase 6 refactor row (or an explicit "no change required" justification) → has a Phase 7 validation verdict
- Verify no orphaned artifacts or dead references
- Produce `sprint-summary.md` with: findings count, comparison verdicts by dimension, synthesis end-state, plan items by priority, estimated total effort, recommended implementation order, and the explicit "rejected alternatives" carry-forward from Phase 5
- Final quality gate: all artifacts pass structural validation

---

### Deterministic Rules

Apply these rules in the generated tasklist:

- **R-RULE-01**: Every task that reads code must use `mcp__auggie-mcp__codebase-retrieval` as the primary search tool, with `directory_path` set to `/config/workspace/IronClaude`.
- **R-RULE-02**: Phase sequencing is strict: no phase begins until the prior phase's checkpoint passes.
- **R-RULE-03**: All comparison tasks must cite specific `file:line` evidence from the repo — no unsupported claims about either surface's behavior.
- **R-RULE-04**: Anti-sycophancy check: every "strength" claimed for `/sc:task` or `/task` must have a corresponding "weakness" or trade-off documented for the same surface.
- **R-RULE-05**: The "adopt patterns not mass" constraint must be verified in every Phase 6 refactoring plan item — patterns are extracted; ceremony with no behavioral teeth is rejected.
- **R-RULE-06**: Artifacts are written to `.dev/releases/current/task-vs-sc-task-comparison/artifacts/`.
- **R-RULE-07**: Each phase ends with a checkpoint table verifying all acceptance criteria.
- **R-RULE-08**: Both surfaces live in the same repo — never let an analysis task confuse `src/superclaude/` (source of truth) with `.claude/` (dev copy). Every file claim must specify which side it cites, and any drift between sides is itself a finding.

### Compliance Tiers

- **Phases 1–3**: EXEMPT (read-only analysis, no code changes)
- **Phase 4**: STANDARD (comparison and debate, produces artifacts but no code changes)
- **Phase 5**: STANDARD (synthesis, no code changes; produces a binding decision)
- **Phase 6**: STRICT (refactoring plans that will drive code changes; must verify file references)
- **Phase 7**: STRICT (adversarial validation of plans that will drive code changes)
- **Phase 8**: LIGHT (assembly and verification)

### MCP Requirements

Every task must specify MCP requirements. Recommended:
- **auggie MCP** (`mcp__auggie-mcp__codebase-retrieval`): Required for ALL code search tasks; `directory_path: /config/workspace/IronClaude`
- **Sequential**: Required for STRICT tier tasks (Phases 6, 7); recommended for comparison/debate tasks (Phase 4) and synthesis (Phase 5)
- **Serena**: Optional for symbol-level analysis when auggie results need deeper resolution (e.g., locating every reference to a renamed identifier)
- **Context7**: Not required (no external library docs involved in this comparison)

---

## Execution

After generating the tasklist files, the sprint can be executed with:

```bash
superclaude sprint run \
  .dev/releases/current/task-vs-sc-task-comparison/tasklist-index.md \
  --permission-flag "--dangerously-skip-permissions"
```

Or phase-by-phase:
```bash
superclaude sprint run \
  .dev/releases/current/task-vs-sc-task-comparison/tasklist-index.md \
  --start 1 --end 3 \
  --permission-flag "--dangerously-skip-permissions"
```

---

**Now generate the complete tasklist-index.md and all 8 phase files.**
