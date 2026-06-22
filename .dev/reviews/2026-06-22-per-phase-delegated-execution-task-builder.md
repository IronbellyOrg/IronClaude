# Review: Per-Phase Delegated Execution for task-builder + /task

**Date:** 2026-06-22
**Status:** Review only — no code changes in this deliverable
**Scope (confirmed):** unit = each Phase · pipeline = task-builder + /task only · deliverable = review/plan

## Context

Today, a task built by the **task-builder** skill is a single MDTM file (`TASK-RF-*.md`)
made of **Phases → B2 self-contained checklist items**. The **/task** skill executes that
file **inline in the main session**: it runs the F1 loop (READ → IDENTIFY → EXECUTE →
UPDATE → REPEAT), spawning subagents only to *execute individual items*, and spawns a
lens-based QA team at each phase boundary.

The request is to change the execution model so that **each Phase is handed to its own
fresh-context executor agent**, which runs that phase end-to-end; a QA team then validates
that phase; only then does the orchestrator move to the next phase and spin up a **new**
executor + QA team. The "agent team" instructions are to be **baked into the generated
task file by the templates / task-builder**, so the file itself drives the per-phase
delegation.

This document identifies every modification required, the central architectural conflict,
a backward-compatibility strategy, risks, and a verification approach.

---

## The central conflict (must be resolved first)

The current model **explicitly prohibits** what is being asked. Both the executor skill and
the templates carry a load-bearing "non-delegable F1 loop" doctrine:

- `src/superclaude/skills/task/SKILL.md`
  - Critical Rule **#12**: *"The F1 loop is non-delegable. The executor MUST maintain the
    READ-IDENTIFY-EXECUTE-UPDATE-REPEAT loop itself... it must NOT spawn a subagent and
    instruct it to 'process items X through Y'."*
  - Prohibited Action (F2): *"Delegating across phase boundaries... Delegating the F1 loop
    itself to a subagent is prohibited."*
- `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (and `01_…`)
  - PART 1 **F2** (lines ~427): *"must not delegate the F1 loop itself; a subagent receives
    work from a SINGLE checklist item only."*

The new model **inverts this at the phase level**. The clean way to express it is a
**two-level loop** that preserves the "one phase = one unit, QA between phases" guarantee:

- **Orchestrator loop (P-loop)** — runs in the main `/task` session. Reads the task file,
  finds the **first incomplete phase**, spawns a **fresh phase-executor agent** for that
  phase, waits, then spawns the **phase QA team** (the existing M3 lens-based gate). On QA
  PASS it marks the phase complete and repeats; it never lets one executor span two phases.
- **Phase-executor loop (F1, scoped)** — runs in the spawned agent's **fresh context**. It
  runs the existing item-level F1 loop **scoped to its one assigned phase only**, spawning
  per-item subagents exactly as today, writing outputs incrementally to disk, then returns a
  structured completion report. It does **not** run the phase QA, touch other phases, or
  mark the task Done.

So Rule #12 / F2 are not deleted — they are **re-scoped**: the *phase boundary* remains
inviolable and the executor still cannot span phases; what changes is that the **whole
phase** (not just a single item) is now the delegated unit, and the F1 loop becomes
delegable *for one phase at a time*.

---

## Current-state findings (files reviewed)

- **task-builder skill** — `src/superclaude/skills/task-builder/SKILL.md` (~2.5k lines).
  Stage A pipeline (A.1–A.11): scope discovery → research → QA gates → spawn `rf-task-builder`
  → structural/alignment/qualitative validation (A.10/A.10.25/A.10.5) → present. The A.10
  validation checklist is where new structural requirements get enforced.
- **builder agent** — `src/superclaude/agents/rf-task-builder.md` (emits the MDTM file).
- **MDTM templates** — `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md`,
  `02_mdtm_template_complex_task.md`. PART 1 = build rules (Sections A–M); PART 2 = clean
  output structure. Phase-gate QA already standardized as **M3 lens-based gate** (≥6 agents:
  3 rf-qa + 3 rf-qa-qualitative; Steps `PG.1`–`PG.6`) and **M4 fidelity gate**; post-completion
  validation in `## Post-Completion Actions`. Per-phase QA already exists — only the
  **executor-delegation half is missing.**
- **executor skill** — `src/superclaude/skills/task/SKILL.md`. The F1 loop, phase-gate QA,
  post-completion validation, session resumption, agent-spawning conventions. This is where
  the P-loop and the rule re-scoping land.
- **existing executor agent** — `src/superclaude/agents/rf-task-executor.md` is **not a fit**:
  it shells out to `.gfdoc/scripts/automated_qa_workflow.sh` and is built for the rf agent-team
  / SendMessage model, not a generic fresh-context per-phase executor. A **new** agent is cleaner.
- **command** — `src/superclaude/commands/task.md` (thin router to the skill).
- **adjacent (out of scope, confirmed)** — `/sc:tasklist` + `sc-tasklist-protocol` build a
  separate multi-file Sprint bundle with its own phase files and `sprint run` executor. Not
  touched by this work.

---

## Required modifications

### 1. `/task` executor skill — add the orchestrator P-loop (PRIMARY)
File: `src/superclaude/skills/task/SKILL.md`
- Add a new top-level **"Phase Delegation Loop (P-loop)"** section above the F1 loop:
  READ task file → IDENTIFY first incomplete phase → SPAWN one fresh phase-executor →
  consume its report → SPAWN the phase QA team (existing gate) → on PASS mark phase done,
  update frontmatter `updated_date`, report progress → REPEAT.
- **Re-scope** Critical Rule #12 and the F2 "delegating across phase boundaries"
  prohibition to the new two-level model (phase boundary still inviolable; executor still
  may not span phases; one phase is now the delegated unit).
- Add **agent-spawning conventions** for the new executor type (subagent_type, embedded
  self-contained prompt passed verbatim, `mode: bypassPermissions`, foreground).
- Update **Session Resumption** and **Session Management**: resume = find first incomplete
  *phase* and re-delegate it; the executor must skip already-`[x]` items (idempotent).
- Keep Phase 1 (setup: status update, dir creation) **inline** in the orchestrator;
  delegate Phase 2+.
- **Backward compatibility:** if a phase carries no Phase Execution Directive (legacy task
  files), fall back to today's inline F1 loop. Directive present ⇒ delegate.

### 2. New phase-executor agent definition
File: `src/superclaude/agents/rf-phase-executor.md` (new)
- Role: given `{task file path, phase number, phase context}`, run the F1 item-loop **scoped
  to that one phase** in a fresh context; spawn per-item subagents as the items instruct;
  write outputs incrementally; return a structured report (items completed, output paths,
  blockers). Must **not** run phase QA, touch other phases, mark task Done, or spawn another
  phase-executor (recursion guard).
- Tools: Read, Write, Edit, Bash, Glob, Grep, Task/Agent, Skill (mirror rf-task-executor's
  set minus the team/script-specific pieces).

### 3. MDTM templates — bake in the per-phase executor-team directive
Files: `src/superclaude/templates/workflow/01_…` and `02_…`
- **PART 1 — new Section N "Per-Phase Delegated Execution"**: defines the executor-team
  model, the required contents of the embedded executor prompt (B2-style, self-contained:
  task path, phase number, phase goal, item scope, Execution Context references, output
  paths, "F1 scoped to this phase only" rule), and how it composes with the existing M3 QA
  gate. Update PART 1 **F2** prohibition text to match the re-scoped rule.
- **PART 2 — per executable phase**: add a builder-populated **"Phase N Execution
  Directive"** block (HTML-comment-guided, like the existing `PG.*`/Post-Completion
  placeholders) at the **start of each Phase 2+**. It encodes, as **orchestrator-level**
  checklist items: (a) "Spawn `rf-phase-executor` for Phase N with the embedded prompt
  below…", then (b) the existing M3 phase-gate QA team items (`PG.1`–`PG.6`). Use a clear
  marker (e.g., `[ORCHESTRATOR]`) to distinguish orchestrator-run items from executor-run
  items so the executor never tries to execute its own spawn directive (recursion guard).
- Reconcile with existing per-phase QA: the `PG.*` items become the **QA half** of each
  phase team; only the **executor-spawn half** is new.

### 4. task-builder skill — generate + validate the directives
File: `src/superclaude/skills/task-builder/SKILL.md`
- Add generation rules so the builder emits a Phase Execution Directive + embedded executor
  prompt for every executable phase.
- Extend the **A.10 structural validation checklist** with a new mandatory check: *every
  Phase 2+ has an orchestrator-level executor-spawn directive (fresh `rf-phase-executor`)
  plus its M3 QA team; reject files missing it.* Wire it into the A.10/A.10.5 lenses.

### 5. builder agent
File: `src/superclaude/agents/rf-task-builder.md` — update emission instructions to produce
the new per-phase directive blocks.

### 6. command (minor)
File: `src/superclaude/commands/task.md` — align wording with the orchestrator/executor model
if it describes execution behavior.

### 7. Sync + tests
- Run `make sync-dev` (mirror `src/superclaude/{skills,agents,templates}` → `.claude/`) and
  `make verify-sync`. **Never** stage `.claude/` mirrors (per CLAUDE.md).
- Extend `tests/skills/test_task_builder_merge.py` (and/or a new test) to assert generated
  task files contain a per-phase executor directive for each Phase 2+, the new agent file
  exists, and templates validate.

---

## Isolation contract (the "fresh context window")

Each phase-executor reads only: its phase section of the task file, the `## Execution
Context` section, `research/` artifacts, and `phase-outputs/` from prior phases — all on
disk. Nothing is carried in conversation context across phases, so every phase genuinely
starts in a fresh window. Both loops are disk-backed (checked items + frontmatter +
phase-outputs), preserving resumability and context-compression survival.

## Risks / things to flag

- **Doctrine reversal blast radius:** Rule #12 / F2 are framework-wide doctrine; re-scoping
  them touches the conceptual model other skills lean on. Backward-compat fallback (legacy
  files run inline) contains this.
- **Recursion:** executor must never spawn a phase-executor; orchestrator-only items must be
  fenced with an explicit marker.
- **Cost:** per phase now = 1 executor + 6–12 QA agents; multiplies by phase count. Worth
  calling out for token budgeting.
- **Phase 1 handling:** keep setup inline to avoid a pointless delegation.

## Verification (when implemented later)

1. `make sync-dev && make verify-sync` clean.
2. `uv run pytest tests/skills/ -v` incl. new assertions.
3. End-to-end: `/task-builder` a small 2-phase task, confirm generated file contains the
   per-phase executor directives + M3 QA teams; run `/task` on it and confirm each phase is
   executed by a distinct fresh `rf-phase-executor` followed by its QA team, with the next
   phase only starting on QA PASS.
4. Regression: run a legacy task file (no directives) and confirm inline-F1 fallback still works.
