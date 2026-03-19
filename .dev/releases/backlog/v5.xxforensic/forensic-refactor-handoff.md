# Forensic Refactor Handoff

**Purpose**: Consolidate the relevant conclusions, architectural direction, constraints, and concrete refactor guidance from the recent discussion so a new agent can craft a proper refactoring plan for the original forensic spec.

**Primary source spec**: `/config/workspace/IronClaude/.dev/releases/backlog/v5.xxforensic/forensic-spec.md`

---

## 1. Executive Summary

The current planned `/sc:forensic` spec is a strong generic forensic pipeline, but for the specific task-unified failure-remediation use case it is too heavy to be embedded directly into `task-unified` and too heavy to be the only invocation shape.

### Key decision from this conversation

**Do not bake the full forensic workflow into `task-unified`.**

Instead:
- `task-unified` should own **failure detection, circuit-breaker policy, and strict resume semantics**.
- `/sc:forensic` should own **the forensic investigation and remediation-planning workflow**.
- The forensic command should gain a **lighter mode** suitable for automatic invocation from `task-unified`, with escalation to heavier modes based on complexity, ambiguity, or repeated failure.

### Core architectural sentence

> `task-unified` should own **when** forensic analysis is required; `/sc:forensic` should own **how** forensic analysis is performed.

---

## 2. Original problem driving this refactor

A major concern was identified around `sc:task-unified`: when tests fail at the end of a tasklist, the agent’s natural tendency is to immediately patch the bug and continue. This is dangerous because it invites:
- ad-hoc fixes
- shallow reasoning
- insufficient scrutiny
- weak traceability of why the fix was chosen

### Representative failure scenario from the discussion

A transcript was cited where:
- new tests passed
- broader existing tests then failed
- the agent immediately concluded the test assumptions needed updating and moved toward fixing them directly

This behavior was explicitly called out as a **huge risk**.

### User requirement that emerged

When failures or bugs are discovered mid-task, agents **must be prohibited from fixing anything ad-hoc**.

The desired structure originally proposed was:
1. Stop testing
2. Spawn 2 parallel `/sc:troubleshoot` agents for root-cause analysis
3. Run `/sc:adversarial --compare --depth quick` on their outputs
4. Spawn 2 parallel `/sc:brainstorm` agents for solution proposals
5. Run `/sc:adversarial --compare --depth quick` on those outputs
6. Save adjudicated plan into the tasklist before tests
7. Resume with `/sc:task-unified --compliance strict`
8. Retest

That requirement is the key integration driver for the forensic refactor.

---

## 3. What was learned about the current task-unified implementation

### Relevant files
- `src/superclaude/commands/task-unified.md`
- `src/superclaude/skills/sc-task-unified-protocol/SKILL.md`
- `src/superclaude/commands/troubleshoot.md`
- `src/superclaude/commands/brainstorm.md`
- `src/superclaude/skills/sc-adversarial-protocol/SKILL.md`

### Observed gaps in `task-unified`

From `src/superclaude/skills/sc-task-unified-protocol/SKILL.md`:
- STRICT flow includes running tests and answering adversarial questions.
- STANDARD flow includes direct test execution.
- There is **no explicit failure-analysis branch**.
- There is **no explicit “do not patch from failed test output” boundary**.
- There is **no required artifact contract for root-cause analysis and adjudicated remediation planning**.

### Existing command capabilities already available

#### `/sc:troubleshoot`
Source: `src/superclaude/commands/troubleshoot.md`

Important existing boundary:
- Diagnose first by default
- Without `--fix`, it must:
  - diagnose the issue
  - identify root cause
  - propose solution options
  - stop without applying fixes

This is already aligned with the desired “no ad-hoc fix” behavior.

#### `/sc:brainstorm`
Source: `src/superclaude/commands/brainstorm.md`

Important existing boundary:
- Requirements/specification oriented
- Explicitly stops after requirements discovery
- Does **not** implement

This makes it appropriate for solution proposal generation but not code changes.

#### `/sc:adversarial`
Source: `src/superclaude/skills/sc-adversarial-protocol/SKILL.md`

Already provides:
- compare mode
- structured debate
- scoring
- base selection
- merge/refactor plan generation
- failure handling
- artifact output conventions

This is already suitable as the adjudication mechanism for:
- competing root-cause analyses
- competing solution proposals

---

## 4. Original recommendation for task-unified before the forensic refactor decision

Before shifting toward the forensic-command solution, the recommended task-unified change was:

### Add a mandatory Failure Analysis Circuit Breaker
To `src/superclaude/skills/sc-task-unified-protocol/SKILL.md`:
- trigger on any failed test or discovered regression
- stop further testing immediately
- freeze implementation
- prohibit ad-hoc patching
- require structured diagnosis and solution planning before resuming

### Add hard prohibitions
- Never patch while diagnosing
- Never fix a failure directly from test output
- Never continue implementation until root-cause and solution artifacts exist

### Suggested artifact set
Root cause artifacts:
- `failure-root-cause-A.md`
- `failure-root-cause-B.md`
- `failure-root-cause-adjudicated.md`

Solution artifacts:
- `failure-solution-A.md`
- `failure-solution-B.md`
- `failure-solution-adjudicated.md`

Tasklist insertion:
- append adjudicated plan before tests section under a heading like:
  - `## Failure Remediation Plan (Adjudicated)`

### Prompt contracts proposed at the time
#### Root cause prompts
Must begin with `/sc:troubleshoot` and include:
- tasklist item
- failing test or step
- expected behavior
- actual behavior
- error output
- recent changes
- diagnosis only, no fixes
- required output file path

#### Solution prompts
Must begin with `/sc:brainstorm` and include:
- approved root cause
- desired behavior
- constraints
- affected files/components
- non-goals
- solution + implementation steps only
- required output file path

### Resume semantics proposed
After adjudication:
- resume with `/sc:task-unified --compliance strict`
- scope resume narrowly to the adjudicated fix plan
- consume the adjudicated root-cause and solution artifacts
- then retest

This remains highly relevant, but now should likely become a **cross-command integration contract** between `task-unified` and `forensic`, not something wholly embedded in `task-unified` itself.

---

## 5. Forensic-specific architectural debate and final decision

A dedicated adversarial-style analysis was done around two options:

### Option A — Keep failure-remediation logic inside `task-unified`
**Pros**
- single entrypoint
- strongest enforcement at the moment of failure
- simpler user mental model
- tighter local resume semantics

**Cons**
- bloats `task-unified`
- mixes routine task execution with forensic investigation
- creates a large embedded sub-protocol
- hard to reuse elsewhere
- likely to drift and become hard to maintain

### Option B — Move failure-remediation workflow into a separate `/sc:forensic` command and couple it to `task-unified`
**Pros**
- separation of concerns
- reusable for roadmap failures, QA failures, regression triage, release hardening, etc.
- naturally fits the existing forensic spec direction
- lets `task-unified` stay lean
- cleaner place for light/standard/deep forensic modes
- easier to evolve investigation logic independently

**Cons**
- requires a strong handoff contract
- more moving parts if poorly specified
- risk of unclear ownership if resume and artifact integration are underspecified

### Final decision from the discussion

**Winner: separate `/sc:forensic` command, coupled to `task-unified`.**

Rationale:
- The desired failure branch is no longer a small conditional branch.
- It is effectively its own pipeline:
  - root-cause discovery
  - adversarial comparison
  - solution generation
  - adversarial comparison
  - implementation planning
  - validation
  - reporting
- Pipelines should be promoted into first-class commands rather than buried as hidden branches inside other commands.

---

## 6. Implications for the forensic spec

The current forensic spec is valuable but currently optimized as a heavier generic pipeline.

### Current forensic spec strengths
From `forensic-spec.md`:
- Generic-first architecture
- Orchestrator bounded from reading raw source directly
- Parallel domain discovery
- Root-cause investigation
- Adversarial hypothesis validation
- Fix proposal generation
- Adversarial fix validation
- Specialist implementation
- Validation and reporting
- Resume/checkpoint support

### Current forensic spec issue for task-unified integration
For automatic invocation from `task-unified`, the current design is too heavy because it assumes a broad generic forensic run with:
- Phase 0 reconnaissance
- discovered domains
- multiple domain investigation agents
- heavier orchestration and reporting

That is valuable for larger QA/debug/regression use cases, but overkill for:
- one tasklist
- one failing test cluster
- one fresh regression likely caused by recent changes

### Key refactor direction
The forensic spec should be revised so it supports **multiple operating modes**, including a mode tailored for task-unified integration.

---

## 7. Critical refactor requirement: add a lighter forensic mode

This was a major conclusion.

### Required new concept
The forensic command should support a **lighter mode** appropriate for automatic invocation by `task-unified`, with escalation to broader modes as needed.

### Proposed mode family
- `light`
- `standard`
- `deep`

### Important note on naming conflict
The current forensic spec already uses `--mode debug|qa|regression|auto` to represent **investigation intent**.

This means the refactor plan must resolve a naming/design conflict:
- either repurpose `--mode`
- or introduce a second orthogonal dimension such as:
  - `--intention debug|qa|regression|auto`
  - `--tier light|standard|deep`
  - or similar

This is a major design item for the refactor plan.

### Recommended semantics from the conversation
#### Light mode
Intended for automatic task-unified failure handling.

Characteristics:
- fast failure triage
- scope limited to:
  - changed files
  - failing tests
  - direct importers/references
- exactly 2 root-cause analyses
- quick adversarial compare on root causes
- exactly 2 solution proposals
- quick adversarial compare on solutions
- compact artifacts
- likely no broad codebase reconnaissance
- should be optimized for re-entry into task-unified
- can be diagnosis/planning only if desired

#### Standard mode
Intended for more ambiguous or repeated failures.

Characteristics:
- broader than light mode
- some domain discovery or broader scope
- moderate adversarial rigor
- suitable when the first pass is not enough

#### Deep mode
Intended for severe, repeated, cross-domain, or non-obvious failures.

Characteristics:
- full forensic pipeline
- broad discovery and richer adversarial depth
- more complete reporting and orchestration

---

## 8. Recommended responsibility split after refactor

### `task-unified` should own
- detection of failure
- immediate circuit-breaker behavior
- stopping tests
- freezing implementation
- deciding to invoke forensic
- resume and retest semantics
- strict compliance on resumed implementation

### `/sc:forensic` should own
- forensic investigation workflow
- root-cause generation
- adversarial root-cause adjudication
- solution generation / remediation planning
- adversarial solution adjudication
- optional broader implementation/validation/reporting for standard/deep modes
- escalation logic recommendation

This split should be made explicit in the plan.

---

## 9. Proposed coupling contract between task-unified and forensic

This was an important concrete outcome and should likely appear in the refactor plan.

### Inputs `task-unified` should pass to forensic
At minimum:
- failing test command
- failing output / traceback / logs
- expected behavior
- actual behavior
- changed files
- target tasklist path
- current task/tasklist item
- test section location if relevant
- whether this is the first failure or a repeat failure
- possibly impacted test paths and recent edited files

### Outputs forensic should return
At minimum:
- `status`
- `root_cause_path`
- `solution_plan_path`
- `recommended_resume_mode` (expected to be `strict` for task-unified)
- `recommended_escalation` (`none|standard|deep` or equivalent)
- insertion-ready markdown for tasklist update, or a path to it
- `requires_user_review` boolean

### Important design point
The coupling contract should be explicit and machine-consumable enough that `task-unified` can safely:
- pause
- call forensic
- consume outputs
- update tasklist
- resume strict implementation
- retest

---

## 10. Proposed task-unified failure policy after refactor

This is the recommended policy that should remain in task-unified even after forensic is split out.

On failure:
1. Stop testing immediately
2. Freeze implementation
3. Invoke `/sc:forensic` in its light mode with the task/failure context
4. Consume forensic outputs
5. Insert adjudicated remediation plan into the tasklist before tests
6. Resume with `/sc:task-unified --compliance strict`
7. Retest
8. If the light forensic run is inconclusive or the failure repeats, escalate to a broader forensic mode

### Escalation triggers suggested in the discussion
Escalate beyond light mode when there is:
- repeated failure
- multi-file blast radius
- low-confidence root cause
- unresolved adversarial outcome
- second failed retest
- cross-domain or non-obvious regression

---

## 11. Key constraints and observations from the existing forensic spec

From `forensic-spec.md` and related discussion:

### The current forensic spec already does many things right
- generic-first domain discovery
- bounded orchestrator token budgets
- adversarial reuse in Phases 2 and 3b
- specialist implementation delegation
- checkpoint/resume protocol
- clear phase artifacts

### Specific current command definitions that matter
From `forensic-spec.md:304-317`, current command flags include:
- `--mode debug|qa|regression|auto`
- `--depth quick|standard|deep`
- `--concurrency`
- `--focus`
- `--confidence-threshold`
- `--fix-tier minimal|moderate|robust`
- `--resume`
- `--dry-run`
- `--output`

### Important conflict to resolve
The current spec already uses `--depth quick|standard|deep` for adversarial debate depth, while the newly recommended lighter forensic execution concept also wants a light/standard/deep style dimension.

Therefore, the refactor plan must decide how to represent:
1. investigation intent (`debug|qa|regression|auto`)
2. forensic operating tier (`light|standard|deep` or similar)
3. adversarial depth (`quick|standard|deep`)

These three dimensions currently overlap semantically and will become confusing unless normalized.

---

## 12. Concrete design guidance for the new refactoring plan

The new planning agent should strongly consider the following refactor directions.

### A. Separate “intent” from “forensic operating tier” from “debate depth”
Possible shape:
- `--intent debug|qa|regression|auto`
- `--tier light|standard|deep`
- `--debate-depth quick|standard|deep`

Or similar.

This is probably the cleanest design.

### B. Introduce a task-unified integration mode or trigger
Potential options:
- `--trigger task-unified`
- `--caller task-unified`
- `--entrypoint task-unified`

This would let forensic alter defaults automatically for task-unified-originated invocations.

### C. Split forensic into profiles
The refactor plan should consider whether the current single 7-phase flow should be factored into reusable profiles such as:
- **triage profile** (light/task-unified integration)
- **investigation profile** (standard)
- **full forensic profile** (deep)

### D. Preserve genericity
The conversation strongly supported forensic remaining a generic command, not becoming a task-unified-only feature.

### E. Keep the circuit breaker in task-unified
Even if forensic becomes the main workflow engine, `task-unified` must still own the “stop, do not patch, invoke forensic” behavior.

---

## 13. Candidate artifact strategy for light forensic mode

While not finalized as spec text, the following artifact shapes were repeatedly useful in the discussion and may be worth preserving in the refactor plan.

### Root-cause artifacts
- `failure-root-cause-A.md`
- `failure-root-cause-B.md`
- `failure-root-cause-adjudicated.md`

### Solution/remediation artifacts
- `failure-solution-A.md`
- `failure-solution-B.md`
- `failure-solution-adjudicated.md`

### Tasklist integration artifact
- insertion-ready markdown block or dedicated file containing:
  - adjudicated remediation plan
  - implementation steps
  - maybe test expectations / retest criteria

### Return-contract idea
If `/sc:forensic` is going to be called by `task-unified`, it should likely return a structured contract similar in spirit to how `sc:adversarial` defines one.

---

## 14. High-value command/protocol boundaries to preserve

### From `/sc:troubleshoot`
Preserve diagnosis-first semantics:
- no code changes without explicit fix approval
- ideal for root-cause generation prompts

### From `/sc:brainstorm`
Preserve requirement/proposal-only semantics:
- use for solution design, not implementation

### From `/sc:adversarial`
Preserve compare/merge/adjudication role:
- use for selecting best root cause
- use for selecting best remediation plan

### From `/sc:task-unified`
Add explicit boundary text after refactor:
- on failure, task-unified will not permit ad-hoc mid-task fixing
- failure triggers formal forensic analysis before implementation resumes

---

## 15. Suggested planning questions for the next agent

The next agent crafting the refactoring plan should explicitly answer:

1. **What should the new flag model be?**
   - How should forensic represent intent, operating tier, and debate depth without confusion?

2. **How much of the current 7-phase pipeline remains universal?**
   - Is light mode a trimmed path through the same phases or a separate profile?

3. **What exactly does task-unified invoke?**
   - A light forensic profile?
   - A forensic protocol sub-mode?
   - A special caller-aware path?

4. **What is the machine-readable handoff contract?**
   - Inputs from task-unified to forensic
   - Outputs from forensic back to task-unified

5. **Where should resume responsibility live?**
   - Does forensic only produce plan artifacts?
   - Or does it optionally implement/validate in broader modes?
   - How does resumed task-unified consume forensic outputs?

6. **How should escalation work?**
   - First failure -> light
   - repeated or ambiguous failure -> standard
   - broad/severe repeated failure -> deep

7. **Should light forensic implement code or stay diagnosis/planning only?**
   - The discussion leaned toward keeping light mode optimized for diagnosis/adjudication/planning and letting task-unified resume strict implementation.

8. **How should artifacts be standardized?**
   - file names
   - output directory
   - insertion-ready tasklist block
   - return contract

---

## 16. Recommended direction for the eventual refactoring plan

If the next agent wants a concise direction statement to start from, use this:

### Recommended direction statement
Refactor the original forensic spec into a multi-profile forensic system where:
- the full generic pipeline remains available for broader QA/debug/regression use,
- a new light forensic profile supports fast failure triage and adjudicated remediation planning,
- `task-unified` invokes this light profile via a strict integration contract,
- and the command surface is redesigned to cleanly separate investigation intent, forensic operating tier, and debate depth.

---

## 17. Most important conclusions to preserve verbatim in spirit

- The current ad-hoc fix tendency after test failure is unacceptable.
- `task-unified` must stop, not patch.
- The desired failure branch has grown into a real pipeline and should be promoted into a first-class command.
- The full forensic workflow should not be buried inside `task-unified`.
- The forensic command needs a lighter mode suitable for automatic invocation.
- `task-unified` owns **when** forensic is needed.
- `/sc:forensic` owns **how** forensic is executed.
- Resume after forensic should return to `/sc:task-unified --compliance strict`.

---

## 18. File references discussed in this conversation

### Primary forensic documents
- `/config/workspace/IronClaude/.dev/releases/backlog/v5.xxforensic/forensic-spec.md`
- `/config/workspace/IronClaude/.dev/releases/backlog/v5.xxforensic/forensic-explore.md`

### Task-unified related files
- `/config/workspace/IronClaude/src/superclaude/commands/task-unified.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-task-unified-protocol/SKILL.md`

### Supporting command files
- `/config/workspace/IronClaude/src/superclaude/commands/troubleshoot.md`
- `/config/workspace/IronClaude/src/superclaude/commands/brainstorm.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-adversarial-protocol/SKILL.md`

---

## 19. Suggested next step for the next agent

The next agent should produce a **formal refactoring plan** for the forensic spec that includes:
- architectural target state
- CLI/flag redesign
- mode/profile model
- task-unified integration contract
- phase refactor strategy
- artifact contract
- migration plan from current spec text
- acceptance criteria
- risks and open decisions
