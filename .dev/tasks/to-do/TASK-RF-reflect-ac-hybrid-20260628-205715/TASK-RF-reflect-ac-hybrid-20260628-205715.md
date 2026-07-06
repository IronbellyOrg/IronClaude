---
id: "TASK-RF-reflect-ac-hybrid-20260628-205715"
title: "Implement sc-reflect A→C Anti-Self-Confirmation Fast-Follow (5 subtractive/narrowing edits + telemetry de-risk)"
description: "Harden the reflect wrapper's graded executor-class-exclusion machinery with the 5 Option C edits (C1 non-collapsing Tier-2, C2 narrow exclusion trigger to reliable identity, C3 reflect-side reader for executor_model_class, C4 gate the graded invariant on identity reliability, C5 evals) plus an executor_class_source telemetry emission and a sampled human-decision urgency checkpoint. Funded, scheduled, NON-BLOCKING fast-follow to the PR #197 Decision A (executor-class exclusion) merge."
version: ""
status: "🟡 To Do"
type: "🐛 BugFix"
priority: "🔼 High"
created_date: "2026-06-28"
updated_date: "2026-06-28"
assigned_to: "rf-task-executor"
autogen: false
autogen_method: ""
coordinator: orchestrator
parent_doc: ""
parent_task: ""
depends_on:
- "PR-197-Decision-A-executor-class-exclusion-merge"
spec_path: "/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/.dev/brainstorms/pr197-final-merge-strategy/adversarial-decisionA/merged-decisionA-recommendation.md"
reflect_pre:
  verdict: ""
  coverage_pct: null
  depth: ""
  tcs: 0
  run_id: ""
  report: ""
  reviewed_at: ""
reflect_post: ""   # reflect_post: room — populated by the executor after the final-phase POST reflect wrapper subagent runs. DO NOT hand-author or lock.
related_docs:
- path: "/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/.dev/brainstorms/pr197-final-merge-strategy/adversarial-decisionA/merged-decisionA-recommendation.md"
  description: "Driving spec — Option C 5-point fast-follow list (lines ~33-40) + open item X-004 / telemetry de-risk (lines ~42-47)"
- path: "/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/research-notes.md"
  description: "Consolidated research notes (authoritative) — EXISTING_FILES inventory with file:line anchors, patterns, gaps, recommended outputs"
related_prd: ""
related_tdd: ""
tags:
- "reflect"
- "anti-self-confirmation"
- "executor-class-exclusion"
- "pr197"
- "fast-follow"
template_schema_doc: ""
estimation: ""
sprint: ""
due_date: ""
start_date: ""
completion_date: ""
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: static
start_commit: "cda6e2d4526c73a3d2739a3bf6efb500c4402f60"   # git merge-base HEAD origin/master at build time
executor_model_class: "sonnet"   # placeholder executor-class alias — the operator MUST confirm the real executing model-class at run time before relying on the executor-class-exclusion invariant
---

# Implement sc-reflect A→C Anti-Self-Confirmation Fast-Follow (5 subtractive/narrowing edits + telemetry de-risk)

## Task Overview

This task implements the **Option C "Edit A → C" fast-follow** to the PR #197 "Decision A" merge (executor-class exclusion in the `sc-reflect` wrapper). Decision A's day-1 anti-self-confirmation guarantee is only as strong as executor-class *resolution*; on a bare-CLI/heuristic path it can fail open (driving-spec open item X-004). This task applies five *subtractive/narrowing* edits to the existing graded executor-class-exclusion machinery, plus a telemetry de-risk that sizes the urgency of the heuristic-drop:

- **C1** — Remove the destructive tier-collapse: on an executor-class collision that cannot reach a disjoint N=2 reviewer panel, STAY Tier-2, fill best-available distinct model classes, and emit contract fields `executor_exclusion_unsatisfiable: true` + `t2_model_class_diversity: degraded` (loud, non-collapsing) instead of collapsing to Tier-1.
- **C2** — Narrow the exclusion trigger to reliable identity: only fire executor-class exclusion when `executor_class_source ∈ {flag, env, frontmatter}`; DROP the commit-author `log-heuristic` source from the trigger (the live fail-open footgun).
- **C3** — Add the reflect-side reader for `executor_model_class` (today written by task-builder frontmatter but UNREAD by the reflect wrapper — INV-202).
- **C4** — Gate the graded invariant `executor_model_class NOT IN reviewer_model_classes` on identity reliability: ASSERTED when reliable, WAIVED-NOT-FAILED otherwise.
- **C5** — Eval: prove (a) a same-class reviewer panel is actually avoided when identity is reliable, and (b) the unsatisfiable branch stays Tier-2 (does not collapse).
- **Telemetry de-risk** — Emit `executor_class_source` to telemetry, SAMPLE a handful of real reflect runs to measure how often the source is `flag|env|frontmatter` vs `log-heuristic|unknown`, then write a PENDING human-decision checkpoint and HALT the dependent urgency/priority decision.

**CRITICAL PRECONDITION:** This task assumes **Option A (executor-class EXCLUSION) has ALREADY LANDED** on the execution branch (master's §7.1 exclusion + §11.3 three-way partition + grader assertion + the 3 telemetry fields, contract_version 1.7.0). The current worktree branch (`feat/rf-harness-sync`, PR #197) still carries #197's INSTANCE-LEVEL / no-executor-removal prose. Phase 0 MUST verify on-disk that Option A is present and HALT with a labeled precondition-failure note if it is ABSENT — the A→C edits would otherwise be built on the wrong base. Source of truth is `src/superclaude/` (then `make sync-dev`); the reflect wrapper code is intentionally thin and under a strict no-nesting guard.

## Key Objectives

The following objectives MUST be achieved by this task:

1. **Precondition gate:** Verify on-disk that Option A (executor-class exclusion) has landed on the execution branch; HALT and write a labeled precondition-failure note if it is absent (do NOT begin the A→C edits on the wrong base).
2. **Telemetry de-risk (C2 groundwork):** Emit `executor_class_source` to reflect telemetry, sample real reflect runs, and write a PENDING `needs_human_decision` checkpoint recording the measured `flag|env|frontmatter` vs `log-heuristic|unknown` distribution — HALTING the dependent urgency decision until the operator confirms.
3. **C3 reflect-side reader:** Add the reflect wrapper reader for `executor_model_class` (INV-202) so the frontmatter value written by task-builder is actually consumed.
4. **C2 narrowed trigger:** Narrow the executor-class exclusion trigger to `executor_class_source ∈ {flag, env, frontmatter}` and drop the commit-author `log-heuristic` source from the trigger.
5. **C1 non-collapsing Tier-2:** On an unsatisfiable disjoint-N=2 collision, stay Tier-2 with best-available distinct classes and emit `executor_exclusion_unsatisfiable: true` + `t2_model_class_diversity: degraded` (loud, non-collapsing) — preserving reflect exit-code semantics (degraded ≠ content failure).
6. **C4 identity-gated invariant:** Gate the graded invariant `executor_model_class NOT IN reviewer_model_classes` on identity reliability — ASSERTED when reliable, WAIVED-NOT-FAILED otherwise.
7. **C5 evals + extended tests:** Prove (a) reliable same-class exclusion avoids a same-class panel, (b) unreliable-source case WAIVES (not FAILS) the invariant, (c) the unsatisfiable branch stays Tier-2; extend `test_ensemble_unit.py` and `test_ensemble_stub_integration.py` and keep the no-nesting guard green after every `runner.py`/`ensemble.py` edit.
8. **Doc-prose alignment:** Update `SKILL.md`, `refs/reviewer-spec.md`, `refs/reflection-rubric.md` only where C2/C3/C4 add new prose (the Option-A-owned exclusion surfaces).
9. **Validation + sync + POST reflect:** Run the per-edit and final validation gates, `make sync-dev`/`make verify-sync`, and the final-phase POST reflect wrapper shell-out before marking the task Done.

## Prerequisites & Dependencies

### Parent Task & Dependencies
- **Parent Task:** PR #197 "Decision A" merge (executor-class exclusion) — this task is its funded, scheduled, NON-BLOCKING fast-follow.
- **Blocking Dependencies:**
  - PR-197-Decision-A-executor-class-exclusion-merge: Option A (executor-class exclusion: §7.1 exclusion + §11.3 three-way partition + grader assertion + 3 telemetry fields, contract_version 1.7.0) MUST be present on the execution branch before any A→C edit begins. Phase 0 verifies this and HALTS if absent.
- **This task blocks:** None (non-blocking fast-follow). The telemetry-sampling result feeds a human-decision urgency checkpoint, not a downstream task.

### Previous Stage Outputs (MANDATORY INPUTS)

**INFORMATIONAL ONLY - NO CHECKLIST ITEMS HERE**

The actual checklist items for reading these inputs are embedded directly into the Phase 0+ checklist items below (per the self-contained item rule).

**Required Previous Stage Outputs:**
- **Driving spec:** `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/.dev/brainstorms/pr197-final-merge-strategy/adversarial-decisionA/merged-decisionA-recommendation.md` — Purpose: Option C 5-point list (lines ~33-40) is the authoritative edit list; open item X-004 + telemetry de-risk (lines ~42-47) governs the telemetry-emission + sampling + urgency checkpoint.
- **Research notes:** `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/research-notes.md` — Purpose: EXISTING_FILES inventory (file:line anchors VERIFIED-AS-OF-RESEARCH, require re-location at execution time since Option A landing shifts line numbers), patterns/conventions, gaps, recommended outputs, suggested phases.

## Execution Context

### References
- R-001 [Driving spec — merged-decisionA-recommendation.md](/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/.dev/brainstorms/pr197-final-merge-strategy/adversarial-decisionA/merged-decisionA-recommendation.md): Option C 5-point "Edit A → C" list (lines ~33-40) and open item X-004 + telemetry de-risk (lines ~42-47).
- R-002 [Research notes — research-notes.md](/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/research-notes.md): authoritative EXISTING_FILES inventory, patterns, gaps, recommended outputs (re-verify all file:line at execution time).
- R-003 The 5 A→C edits (C1 non-collapsing Tier-2; C2 narrow trigger drop log-heuristic; C3 reflect-side reader INV-202; C4 identity-gated graded invariant assert-vs-waive; C5 evals) + the `executor_class_source` telemetry emission and sampled human-decision urgency checkpoint.

### Source Areas
- `config.py` (reflect wrapper input-resolution): `src/superclaude/cli/reflect/config.py` — executor-model-class constants and resolver; C2/C3 reader + `executor_class_source` provenance tracking surface.
- `contract.py` (reflect contract/verdict derivation): `src/superclaude/cli/reflect/contract.py` — verdict map + degraded semantics; C1 loud-degraded alignment.
- `ensemble.py` (Tier-2 ensemble driver): `src/superclaude/cli/reflect/ensemble.py` — contract builder, diversity function, reviewer-count/tier logic; C1 non-collapsing Tier-2 + unsatisfiable telemetry, C4 graded invariant. Under no-nesting guard.
- `models.py` (reflect config/result dataclasses): `src/superclaude/cli/reflect/models.py` — `ReflectConfig`/result fields; new `executor_class_source` / `executor_exclusion_unsatisfiable` fields if needed.
- `runner.py` (reflect orchestration): `src/superclaude/cli/reflect/runner.py` — wrapper orchestration; `--executor-model` forwarding. Under no-nesting guard.
- sc-reflect-protocol skill + refs: `src/superclaude/skills/sc-reflect-protocol/SKILL.md`, `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md`, `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md` — prose updates only where C2/C3/C4 add new prose.
- reflect unit + stub-integration tests: `tests/cli/reflect/test_ensemble_unit.py`, `tests/cli/reflect/test_ensemble_stub_integration.py` — extend for diversity/reviewer-count/degradation + positive/negative Tier-2 witnesses.
- no-nesting guard test: `tests/cli/reflect/test_no_nesting_guard.py` — run after every `runner.py`/`ensemble.py` edit.

### Key Constraints
- Source-of-truth = `src/superclaude/`; after any change run `make sync-dev` then `make verify-sync`. NEVER edit or stage `.claude/{skills,cli,...}` mirrors (only `.claude/settings.json` is tracked).
- Strict no-nesting guard on `runner.py`/`ensemble.py`: they may NOT gain `import anthropic` / `from anthropic` / `subagent_type` / `Agent(` / `Task(` tokens, may NOT add async/await, and may NOT import sprint/roadmap packages. Run `tests/cli/reflect/test_no_nesting_guard.py` after every edit to either file.
- UV-only Python (`uv run pytest`, `uv run ruff ...`); never bare `python -m` / `pip`.
- Preserve reflect exit-code semantics: `degraded` is a LOUD non-collapsing Tier-2 signal, NOT a content failure (degraded ≠ content failure). C1 must stay Tier-2.
- Per-edit gate (MANDATORY): after EVERY item that edits a `src/superclaude/cli/reflect/*.py` file, run `uv run pytest tests/cli/reflect -q`; after any `runner.py`/`ensemble.py` edit ALSO run `tests/cli/reflect/test_no_nesting_guard.py`.
- QA intensity: **full** — per-phase QA gates after each code-editing phase (min 5 agents per intermediate gate; serialized fix authorization; adversarial framing) plus a final-document/final-validation gate.
- `needs_human_decision` items HALT and write PENDING — they NEVER ship a default.
- Precondition HALT (Phase 0) is FIRST and MUST gate every subsequent edit.

### Handoff File Convention

This task uses intra-task handoff patterns. Items write intermediate outputs to:
**`.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/`**

Subdirectories:
- `discovery/` - Code-reading probe results and on-disk precondition evidence
- `test-results/` - pytest / no-nesting-guard output and summaries
- `reviews/` - Quality review verdicts
- `plans/` - Conditional action outputs (precondition verdict, fix plans) and the PENDING human-decision checkpoint
- `reports/` - Aggregated reports and summaries

QA agent reports are written to the `qa/` subdirectory of the task directory:
**`.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/`**

These files persist across all batches and session rollovers. Later items read them by path.

### Frontmatter Update Protocol

YOU MUST update the frontmatter at these MANDATORY checkpoints:
- **Upon Task Start:** Update `status` to "🟠 Doing" and `start_date` to current date
- **Upon Completion:** Update `status` to "🟢 Done" and `completion_date` to current date
- **If Blocked:** Update `status` to "⚪ Blocked" and populate `blocker_reason`
- **After Each Work Session:** Update `updated_date` to current date

DO NOT modify any other frontmatter fields unless explicitly directed by the user.

## Detailed Task Instructions

**CRITICAL: SELF-CONTAINED CHECKLIST ITEMS.** Due to session rollovers between batches, context loaded in early batches is NOT available in later batches. Therefore EVERY checklist item below is a complete, self-contained prompt embedding all context references, actions, and outputs in ONE PARAGRAPH. Execute items strictly top-to-bottom, ONE at a time, marking each complete before the next. NEVER skip ahead. NEVER mark an item above the current position.

### Phase 1: Preparation and Setup

YOU MUST complete EVERY item in this checklist IN ORDER. DO NOT skip ahead. Mark each item as complete before proceeding to the next.

**Step 1.1:** Update task status

- [ ] Update `status` to "🟠 Doing" and `start_date` to current date in the frontmatter of this file, then add a timestamped entry to the ### Execution Log in the ## Task Log / Notes section at the bottom of this task file using the format: `**[YYYY-MM-DD HH:MM]** - Task started: Updated status to "🟠 Doing" and start_date.` This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 1.2:** Create handoff directories

- [ ] Create the phase-outputs directory structure at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/` with subdirectories `discovery/`, `test-results/`, `reviews/`, `plans/`, and `reports/`, and create the QA report directory `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/`, to enable intra-task handoff between items and QA gates, ensuring all six directories are created successfully. If the parent directory does not exist, create it first. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

### Phase 2: Precondition Verification (HALT-if-Option-A-absent) and Code-Reading Probe

**CRITICAL:** This phase is the precondition gate for the ENTIRE task. The A→C edits assume **Option A (executor-class EXCLUSION) has ALREADY LANDED** on the execution branch. The current worktree (`feat/rf-harness-sync`, PR #197) is documented to still carry INSTANCE-LEVEL / no-executor-removal prose. If Option A is ABSENT, Step 2.1 HALTS the task — DO NOT proceed to any A→C edit on the wrong base. DO NOT assume any specific current line number for these surfaces; re-locate them on the live tree (Option A landing shifts line numbers).

**Step 2.1:** Verify Option A precondition on-disk (HALT gate)

- [ ] Verify on-disk, on the CURRENT execution branch, that **Option A (executor-class EXCLUSION) has landed** by reading `src/superclaude/skills/sc-reflect-protocol/SKILL.md` and using Grep to confirm ALL of: (a) §7.1 describes executor-class EXCLUSION (the executor's model class IS removed from the reviewer pool when reliably identified) — NOT the instance-level "executor's model class is never removed" / "`--executor-model <class>` is ACCEPTED and IGNORED" prose; (b) a §11.3 (or equivalent) three-way partition is documented; (c) a grader assertion `executor_model_class NOT IN reviewer_model_classes` exists; (d) the 3 telemetry fields tied to executor-class exclusion are documented; and (e) the contract/`contract_version` is `1.7.0` (Grep `src/superclaude/cli/reflect/` for the contract version constant), THEN write the file `precondition-verdict.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/plans/precondition-verdict.md` containing: overall verdict (`OPTION-A-PRESENT` or `OPTION-A-ABSENT`), a checklist of the five sub-checks (a-e) each marked present/absent with the exact file path + located line range as evidence, and the contract_version found; ensuring every sub-check is backed by an actual Grep/Read result with no assumption, and the line numbers are the ones found live (not copied from research). IF the verdict is `OPTION-A-ABSENT`, YOU MUST set `status` to "⚪ Blocked" and populate `blocker_reason` with "PRECONDITION FAILURE: Option A (executor-class exclusion) not present on execution branch; A→C edits would be built on the wrong base", write a labeled `### Phase 2 Findings` PRECONDITION-FAILURE entry describing exactly which sub-checks failed, and HALT the task (do NOT execute any subsequent item). IF the verdict is `OPTION-A-PRESENT`, proceed normally. If unable to complete due to file access issues, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 2.2:** Probe the reflect input-resolution surface (`config.py`)

- [ ] Read the file `config.py` at `src/superclaude/cli/reflect/config.py` to locate (re-locating live, not from research) the executor-model-class resolution surface — the constants `_FRONTMATTER_EXECUTOR_MODEL_KEY = "executor_model_class"` and `_EXECUTOR_MODEL_ENV = "EXECUTOR_MODEL_CLASS"`, the resolver order (env → tasklist frontmatter), and how/whether any source-provenance (`flag`/`env`/`frontmatter`/`log-heuristic`/`unknown`) is currently tracked — and read the research notes at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/research-notes.md` EXISTING_FILES section for context, THEN write a probe report `probe-config.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/discovery/probe-config.md` documenting: the exact functions/constants and their live line ranges that resolve `executor_model_class`, whether `executor_class_source` provenance already exists or must be added (C2/telemetry groundwork), and where the reflect-side reader (C3/INV-202) must be wired; ensuring every claim cites the live file:line found by reading config.py with no fabrication, and the report explicitly states the resolver order observed. If unable to complete due to file access issues, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 2.3:** Probe the Tier-2 ensemble driver (`ensemble.py`)

- [ ] Read the file `ensemble.py` at `src/superclaude/cli/reflect/ensemble.py` to locate (re-locating live) the contract builder that sets `tier_reached`, `merge_method`, `reviewer_count`, and `t2_model_class_diversity`, and the model-class diversity helper (currently returns `full` when ≥2 succeeded `model_id` values are distinct, else `insufficient`), and the executor-class collision / disjoint-N=2 logic if present, THEN write a probe report `probe-ensemble.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/discovery/probe-ensemble.md` documenting: the live line ranges of the contract builder and diversity helper, exactly where the C1 non-collapsing Tier-2 + `executor_exclusion_unsatisfiable`/`degraded` logic must be inserted, where the C4 graded invariant (`executor_model_class NOT IN reviewer_model_classes`) is evaluated, and any tokens already present that the no-nesting guard bans (there must be none); ensuring every claim cites live file:line with no fabrication. If unable to complete due to file access issues, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 2.4:** Probe the verdict-derivation and dataclass surfaces (`contract.py`, `models.py`)

- [ ] Read the file `contract.py` at `src/superclaude/cli/reflect/contract.py` to locate (re-locating live) the verdict-derivation logic that degrades expected-T2 runs reaching Tier-1 and degrades when `t2_model_class_diversity` is present and not `full`, AND read the file `models.py` at `src/superclaude/cli/reflect/models.py` to confirm the EXACT current dataclass fields on `ReflectConfig` and the contract/result dataclass (the build research could NOT pin every field — this probe MUST resolve them before any edit), THEN write a probe report `probe-contract-models.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/discovery/probe-contract-models.md` documenting: the live verdict-map/degrade conditions and their line ranges, the full enumerated field list of `ReflectConfig` and the contract/result dataclass, whether new fields `executor_class_source` and `executor_exclusion_unsatisfiable` must be added (and to which dataclass), and how to keep loud-degraded semantics aligned with the existing verdict map WITHOUT changing exit-code semantics (degraded ≠ content failure); ensuring every field and condition cites live file:line with no fabrication. If unable to complete due to file access issues, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 2.5:** Probe the orchestration surface and reflect tests (`runner.py`, test files)

- [ ] Read the file `runner.py` at `src/superclaude/cli/reflect/runner.py` to locate (re-locating live) where `config.executor_model` is forwarded into `/sc:reflect --executor-model` and confirm it carries NO no-nesting-guard-banned tokens, AND read `tests/cli/reflect/test_ensemble_unit.py`, `tests/cli/reflect/test_ensemble_stub_integration.py`, and `tests/cli/reflect/test_no_nesting_guard.py` to catalogue the exact existing test names, fixtures/stub-transport patterns, and the banned-token / async / sprint-roadmap-import guards, THEN write a probe report `probe-runner-tests.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/discovery/probe-runner-tests.md` documenting: the live line range of the `--executor-model` forwarding in runner.py, the existing diversity/reviewer-count/source-order unit tests to EXTEND, the existing positive/negative Tier-2 stub witnesses to EXTEND, and the exact banned tokens the no-nesting guard enforces on `runner.py`/`ensemble.py`; ensuring every claim cites live file:line with no fabrication. If unable to complete due to file access issues, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

### Phase 3: Telemetry Emission of `executor_class_source` (C2 groundwork) + Sampling + Human-Decision PENDING Checkpoint

This phase lands the telemetry de-risk from driving-spec X-004 (lines ~42-47): emit `executor_class_source` to telemetry, sample real reflect runs, and write a PENDING `needs_human_decision` checkpoint that HALTS the dependent urgency/priority decision. The telemetry edit is C2 groundwork (the source enum the C2 trigger will narrow on).

**Step 3.1:** Emit `executor_class_source` to reflect telemetry

- [ ] Read the probe report `probe-config.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/discovery/probe-config.md` and the probe report `probe-contract-models.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/discovery/probe-contract-models.md` to determine the live resolver surface and which dataclass holds telemetry fields, then read the live `src/superclaude/cli/reflect/config.py` (and `src/superclaude/cli/reflect/models.py` if the probe determined the field lives there) to confirm the insertion point, THEN edit the appropriate `src/superclaude/cli/reflect/*.py` file(s) to RESOLVE and EMIT `executor_class_source` as one of `flag | env | frontmatter | log-heuristic | unknown` based on where the executor model class was actually resolved from (flag/env/frontmatter when reliably present, `log-heuristic` for the commit-author-derived path, `unknown` when none), wiring it into the reflect telemetry/contract output WITHOUT yet changing any exclusion/trigger behavior (telemetry-only at this step), ensuring the new field is derived strictly from the live resolver path with no fabricated source value, the change touches only the file(s) the probe identified, and (if `ensemble.py`/`runner.py` were edited) NO no-nesting-guard-banned token (`import anthropic`, `from anthropic`, `subagent_type`, `Agent(`, `Task(`, async/await, sprint/roadmap imports) is introduced. If unable to complete due to unclear resolver structure or file access issues, log the specific blocker using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 3.2:** Per-edit gate after the telemetry emission

- [ ] Use the Bash tool to run `uv run pytest tests/cli/reflect -q` and capture the complete output, AND (because Step 3.1 may have edited `runner.py`/`ensemble.py`) ALSO run `uv run pytest tests/cli/reflect/test_no_nesting_guard.py -q`, then write the raw output to `pytest-phase3-telemetry.txt` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/test-results/pytest-phase3-telemetry.txt` and a structured summary `pytest-phase3-telemetry-summary.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/test-results/pytest-phase3-telemetry-summary.md` containing overall result (PASSED/FAILED), counts (passed/failed/skipped), the no-nesting-guard result, and a table of any failures (Test Name, Error Type, Brief Message), ensuring the summary matches the raw output with no fabricated results. IF any test FAILS, read the failure output, fix the cause in the `src/superclaude/cli/reflect/*.py` file edited in Step 3.1 (NOT by weakening the no-nesting guard), and re-run until green before marking complete. If the test command itself fails to execute, log the specific blocker using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 3.3:** Sample real reflect runs and measure the source distribution

- [ ] Sample a handful (target: 5 or more, or the most recent available) of real reflect runs to measure the `executor_class_source` distribution by using Glob/Grep over existing reflect run artifacts under `.dev/reflect/` (and any `return-contract.yaml` / telemetry outputs that record `executor_class_source` now that Step 3.1 emits it), counting how many resolved to `flag|env|frontmatter` (reliable) vs `log-heuristic|unknown` (unreliable), THEN write a sampling artifact `executor-class-source-distribution.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/reports/executor-class-source-distribution.md` (NOT in `docs/generated/`) containing: the number of runs sampled, a per-run table (run id/path, resolved `executor_class_source`), and the aggregate counts + percentages for reliable vs unreliable sources, ensuring every row is backed by an actual sampled artifact with no fabricated counts, and the totals add up to the number sampled. If fewer than the target runs are available (e.g., telemetry only just started emitting), record exactly how many were found and note the limitation rather than fabricating runs. If unable to complete due to no available run artifacts, log the specific blocker using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 3.4:** Write the PENDING human-decision checkpoint and HALT the dependent urgency decision

- [ ] Read the sampling artifact `executor-class-source-distribution.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/reports/executor-class-source-distribution.md` to obtain the measured reliable-vs-unreliable distribution, THEN write a PENDING decision record `human-decision-urgency-checkpoint.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/plans/human-decision-urgency-checkpoint.md` containing: a `DECISION_STATUS: PENDING` header, the measured distribution (counts + percentages for `flag|env|frontmatter` vs `log-heuristic|unknown`), the decision required ("Does the measured `log-heuristic`/`unknown` share raise the urgency/priority of the C2 heuristic-drop such that day-1 behavior should change?"), the named decider (operator RyanW), and an explicit statement that NO default has been applied, ensuring the record reflects the actual sampled distribution with no fabricated numbers and applies NO default outcome. This is a `needs_human_decision` item: YOU MUST NOT auto-apply any default; write the PENDING record, add a `### Phase 3 Findings` entry stating the urgency decision is PENDING operator confirmation, and DO NOT let this checkpoint silently change the C2 day-1 behavior implemented later (C2 narrows the trigger to reliable identity regardless; this checkpoint governs only the *priority/urgency* framing, not whether C2 ships). The downstream C2 edit (Phase 5) proceeds as specified, but any change to day-1 *default behavior* beyond C2's defined narrowing remains blocked until the operator confirms. If unable to complete, log the specific blocker using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

### Phase Gate 3: Code-Review QA (M3 Lens-Based, serialized fix per I20, full intensity ≥5 agents)

This intermediate code-review gate verifies the Step 3.1 telemetry edit before later phases build on it. Minimum 5 agents (3 rf-qa structural/correctness lenses + 2 rf-qa-qualitative semantic lenses). All report-only (`fix_authorization: false`); a SINGLE serialized fix agent applies consolidated findings; a 2-agent verification round confirms. Gate type: code-review (treat as task-integrity for cycle limits — 2 max, then unresolved issues become Open Questions). Each agent spawn is its own `- [ ]` item with an embedded lens-specific adversarial prompt.

**Step PG3.1:** Aggregate Phase 3 outputs

- [ ] Use Glob to find all Phase 3 outputs (the edited `src/superclaude/cli/reflect/*.py` file(s), `phase-outputs/test-results/pytest-phase3-telemetry-summary.md`, `phase-outputs/reports/executor-class-source-distribution.md`, `phase-outputs/plans/human-decision-urgency-checkpoint.md`) and read each, then write an aggregation summary `phase-3-output-summary.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/reports/phase-3-output-summary.md` listing every file changed/created with a one-line description and the exact diff hunks touched in `*.py`, ensuring the summary lists all discovered outputs with no omission. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step PG3.2:** Spawn structural/correctness lens agents (PARALLEL, report-only)

- [ ] Spawn an **rf-qa** agent with the **correctness lens** and adversarial framing "Assume the Phase 3 `executor_class_source` telemetry edit has at least 5 correctness errors. Find them.": it MUST read `phase-outputs/reports/phase-3-output-summary.md` and the edited `src/superclaude/cli/reflect/*.py` file(s) and verify the `executor_class_source` value is correctly derived for each of the five enum cases (`flag|env|frontmatter|log-heuristic|unknown`), that no exclusion/trigger behavior was changed at this step (telemetry-only), and that exit-code semantics are untouched, writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-structural-correctness-report.md` with `fix_authorization: false` (report-only). If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
- [ ] Spawn an **rf-qa** agent with the **no-nesting-guard lens** and adversarial framing "Assume the Phase 3 edit introduced at least 1 banned nesting token. Find it.": it MUST read the edited `src/superclaude/cli/reflect/*.py` file(s) and `tests/cli/reflect/test_no_nesting_guard.py` and verify that `runner.py`/`ensemble.py` (if edited) gained NONE of `import anthropic`, `from anthropic`, `subagent_type`, `Agent(`, `Task(`, no async/await, and no sprint/roadmap imports, writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-structural-no-nesting-report.md` with `fix_authorization: false`. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
- [ ] Spawn an **rf-qa** agent with the **test-evidence lens** and adversarial framing "Assume the Phase 3 per-edit gate result is misreported. Find the discrepancy.": it MUST read `phase-outputs/test-results/pytest-phase3-telemetry-summary.md` and `phase-outputs/test-results/pytest-phase3-telemetry.txt` and verify the summary's PASS/FAIL counts exactly match the raw pytest output and that the no-nesting-guard test was actually run and passed, writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-structural-test-evidence-report.md` with `fix_authorization: false`. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step PG3.3:** Spawn semantic lens agents (PARALLEL with PG3.2, report-only)

- [ ] Spawn an **rf-qa-qualitative** agent with the **spec-fidelity lens** and adversarial framing "Assume the Phase 3 telemetry edit deviates from driving-spec X-004 in at least 3 ways. Find them.": it MUST read the driving spec at `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/.dev/brainstorms/pr197-final-merge-strategy/adversarial-decisionA/merged-decisionA-recommendation.md` (lines ~42-47) and the edited `*.py` file(s) and verify the `executor_class_source` telemetry emission matches the spec's de-risk intent (the five-source enum and the reliable-vs-unreliable distinction), writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-content-spec-fidelity-report.md` with `fix_authorization: false`. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
- [ ] Spawn an **rf-qa-qualitative** agent with the **human-decision-integrity lens** and adversarial framing "Assume the PENDING checkpoint silently applied a default. Find where.": it MUST read `phase-outputs/plans/human-decision-urgency-checkpoint.md` and `phase-outputs/reports/executor-class-source-distribution.md` and verify the checkpoint is genuinely PENDING (no default outcome applied), records the actual sampled distribution with no fabricated numbers, names the operator decider, and does not let the urgency framing pre-empt the C2 day-1 narrowing, writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-content-human-decision-report.md` with `fix_authorization: false`. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step PG3.4:** Consolidate findings and apply fixes (serialized per I20)

- [ ] Read ALL five QA reports from Steps PG3.2-PG3.3 in `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/` and consolidate them into `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-consolidated-findings-phase3.md`, deduplicating issues (same issue from multiple lenses listed once with all originating lenses noted) with severity (CRITICAL/IMPORTANT/MINOR), ensuring every issue from every report is captured with no omission. The consolidated verdict is FAIL if ANY agent reported ANY issue of any severity. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
- [ ] Spawn ONE **rf-qa** fix agent with `fix_authorization: true` and the consolidated findings file `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-consolidated-findings-phase3.md` as input: it MUST apply ALL consolidated fixes to the affected `src/superclaude/cli/reflect/*.py` file(s) and handoff artifacts WITHOUT introducing any no-nesting-guard-banned token and WITHOUT changing exit-code semantics, ensuring every consolidated finding is addressed. If the consolidated verdict is PASS (no findings), record "No findings — fix phase skipped" and mark complete. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step PG3.5:** Verification round (PARALLEL) and conditional proceed

- [ ] Spawn an **rf-qa** verification agent (`fix_authorization: false`) to confirm the Step PG3.4 fixes were applied correctly to the `*.py` file(s) and that no new structural/correctness issue or banned nesting token was introduced, writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-verification-structural-phase3.md`. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
- [ ] Spawn an **rf-qa-qualitative** verification agent (`fix_authorization: false`) to confirm spec-fidelity and human-decision-integrity were maintained after the fixes, writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-verification-content-phase3.md`. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
- [ ] Read both verification reports (`qa-verification-structural-phase3.md`, `qa-verification-content-phase3.md`): IF both report PASS, write a `gate3-verdict.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/plans/gate3-verdict.md` recording PASS and proceed to Phase 4; IF either reports FAIL, repeat Steps PG3.4-PG3.5 (consolidate new + remaining findings, fix, verify) up to a maximum of 2 fix cycles (task-integrity / code-review gate limit), after which the remaining unresolved issues become Open Questions recorded in the ### Follow-Up Items section and the gate proceeds with those documented; record the cycle count in `gate3-verdict.md`, ensuring the verdict reflects the actual verification reports. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 4: C3 — Reflect-Side Reader for `executor_model_class` (INV-202)

C3 wires the reflect wrapper to actually READ the `executor_model_class` value that task-builder writes to tasklist frontmatter but which the wrapper currently leaves unread (INV-202). This is the reader that C2/C4 will gate on.

**Step 4.1:** Add the reflect-side reader for `executor_model_class`

- [ ] Read the probe report `probe-config.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/discovery/probe-config.md` and the probe report `probe-contract-models.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/discovery/probe-contract-models.md` to confirm the live resolver surface and dataclass fields, then read the live `src/superclaude/cli/reflect/config.py` (and `src/superclaude/cli/reflect/models.py` if the probe shows the field belongs there) to confirm the insertion point, THEN edit the relevant `src/superclaude/cli/reflect/*.py` file(s) so the reflect wrapper READS the `executor_model_class` value from tasklist frontmatter (via the existing `_FRONTMATTER_EXECUTOR_MODEL_KEY = "executor_model_class"` constant) and makes it available to the ensemble/contract path together with its `executor_class_source` provenance (set `frontmatter` when read from frontmatter), closing INV-202, ensuring the reader uses the existing constant with no new magic strings, the resolver precedence (env vs frontmatter) observed in the probe is preserved, the value flows to where C4's invariant will consume it, and (if `config.py` is the only edit, no nesting concern; if `ensemble.py`/`runner.py` were touched) NO no-nesting-guard-banned token is introduced. If unable to complete due to unclear resolver wiring or file access issues, log the specific blocker using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 4.2:** Per-edit gate after the C3 reader

- [ ] Use the Bash tool to run `uv run pytest tests/cli/reflect -q` and capture the complete output, AND (if Step 4.1 edited `runner.py`/`ensemble.py`) ALSO run `uv run pytest tests/cli/reflect/test_no_nesting_guard.py -q`, then write the raw output to `pytest-phase4-c3.txt` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/test-results/pytest-phase4-c3.txt` and a structured summary `pytest-phase4-c3-summary.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/test-results/pytest-phase4-c3-summary.md` (overall result, counts, no-nesting-guard result, failure table), ensuring the summary matches the raw output with no fabrication. IF any test FAILS, fix the cause in the edited `*.py` file (NOT by weakening the guard) and re-run until green before marking complete. If the command fails to execute, log the specific blocker using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

### Phase 5: C2 — Narrow the Exclusion Trigger to Reliable Identity (drop `log-heuristic`)

C2 narrows the executor-class exclusion trigger to fire ONLY when `executor_class_source ∈ {flag, env, frontmatter}`, dropping the commit-author `log-heuristic` source from the trigger (the live fail-open footgun). This is a *narrowing* edit on the existing graded machinery — it does NOT change exit-code semantics.

**Step 5.1:** Narrow the exclusion trigger to `{flag, env, frontmatter}`

- [ ] Read the probe report `probe-config.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/discovery/probe-config.md` and the probe report `probe-ensemble.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/discovery/probe-ensemble.md` to confirm where the executor-class exclusion trigger is evaluated and where `executor_class_source` is now emitted (Phase 3), then read the live `src/superclaude/cli/reflect/*.py` file(s) that own the trigger, THEN edit the relevant file(s) so the executor-class exclusion FIRES ONLY when `executor_class_source` is one of `flag`, `env`, or `frontmatter` (reliable identity), and does NOT fire when the source is `log-heuristic` or `unknown` (the fail-open footgun is dropped from the trigger — the heuristic source is still emitted to telemetry from Phase 3, just not used to TRIGGER exclusion), ensuring the narrowing is expressed against the `executor_class_source` enum with no new magic strings, exit-code semantics are unchanged, and (if `ensemble.py`/`runner.py` were edited) NO no-nesting-guard-banned token is introduced. If unable to complete due to unclear trigger location or file access issues, log the specific blocker using the templated format in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 5.2:** Per-edit gate after the C2 narrowing

- [ ] Use the Bash tool to run `uv run pytest tests/cli/reflect -q` and capture the complete output, AND (if Step 5.1 edited `runner.py`/`ensemble.py`) ALSO run `uv run pytest tests/cli/reflect/test_no_nesting_guard.py -q`, then write the raw output to `pytest-phase5-c2.txt` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/test-results/pytest-phase5-c2.txt` and a structured summary `pytest-phase5-c2-summary.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/test-results/pytest-phase5-c2-summary.md` (overall result, counts, no-nesting-guard result, failure table), ensuring the summary matches the raw output with no fabrication. IF any test FAILS, fix the cause in the edited `*.py` file (NOT by weakening the guard) and re-run until green before marking complete. If the command fails to execute, log the specific blocker using the templated format in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

### Phase 6: C1 — Non-Collapsing Tier-2 + `executor_exclusion_unsatisfiable`/`degraded` Contract Fields

C1 removes the destructive tier-collapse: on an executor-class collision that cannot reach a disjoint N=2 reviewer panel, the wrapper STAYS Tier-2, fills best-available distinct model classes, and emits `executor_exclusion_unsatisfiable: true` + `t2_model_class_diversity: degraded` (loud, non-collapsing) instead of collapsing to Tier-1. Preserves exit-code semantics: `degraded` is a LOUD non-collapsing signal, NOT a content failure.

**Step 6.1:** Implement non-collapsing Tier-2 with best-available distinct-class fill

- [ ] Read the probe report `probe-ensemble.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/discovery/probe-ensemble.md` and the probe report `probe-contract-models.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/discovery/probe-contract-models.md` to confirm the live contract builder, the diversity helper, and which dataclass holds contract fields, then read the live `src/superclaude/cli/reflect/ensemble.py` (and `src/superclaude/cli/reflect/models.py` if a new field must be declared there), THEN edit the relevant file(s) so that when an executor-class collision means a disjoint N=2 reviewer panel CANNOT be reached, the ensemble STAYS Tier-2 (does NOT collapse `tier_reached` to 1), fills the panel with the best-available distinct model classes, and emits `executor_exclusion_unsatisfiable: true` plus `t2_model_class_diversity: degraded` into the contract, ensuring `tier_reached` remains 2 on this branch, the `degraded` value is set instead of collapsing, the new `executor_exclusion_unsatisfiable` field is declared on the correct dataclass (per the probe), no exit-code semantics change (degraded ≠ content failure), and NO no-nesting-guard-banned token is introduced into `ensemble.py`. If unable to complete due to unclear contract-builder structure or file access issues, log the specific blocker using the templated format in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 6.2:** Align verdict-derivation for loud non-collapsing degraded (if required)

- [ ] Read the probe report `probe-contract-models.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/discovery/probe-contract-models.md` to confirm the live verdict map and degrade conditions in `contract.py`, then read the live `src/superclaude/cli/reflect/contract.py`, THEN — ONLY IF the probe shows the existing verdict map would incorrectly treat the new `executor_exclusion_unsatisfiable: true` + `degraded` Tier-2 branch as a content failure or would wrongly degrade the expected-T2-reaching-T1 path — edit `contract.py` so the loud non-collapsing degraded Tier-2 signal maps to the SAME exit-code semantics as the existing `degraded` diversity case (degraded ≠ content failure, Tier-2 preserved), ensuring the verdict map change is minimal and aligned with the existing degraded handling, no exit-code regression is introduced, and if no change is required record "No contract.py change required — existing verdict map already handles the degraded Tier-2 branch correctly" in the ### Phase 6 Findings. If unable to complete, log the specific blocker using the templated format in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 6.3:** Per-edit gate after the C1 edits

- [ ] Use the Bash tool to run `uv run pytest tests/cli/reflect -q` and capture the complete output, AND (because Step 6.1 edited `ensemble.py`) ALSO run `uv run pytest tests/cli/reflect/test_no_nesting_guard.py -q`, then write the raw output to `pytest-phase6-c1.txt` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/test-results/pytest-phase6-c1.txt` and a structured summary `pytest-phase6-c1-summary.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/test-results/pytest-phase6-c1-summary.md` (overall result, counts, no-nesting-guard result, failure table), ensuring the summary matches the raw output with no fabrication. IF any test FAILS, fix the cause in the edited `*.py` file (NOT by weakening the guard) and re-run until green before marking complete. If the command fails to execute, log the specific blocker using the templated format in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

### Phase 7: C4 — Gate the Graded Invariant on Identity Reliability (assert vs waive-not-fail)

C4 gates the graded invariant `executor_model_class NOT IN reviewer_model_classes` on identity reliability: ASSERTED when `executor_class_source` is reliable (`flag|env|frontmatter`), WAIVED-NOT-FAILED otherwise (`log-heuristic|unknown`). A waive is NOT a failure — it must not change exit-code semantics.

**Step 7.1:** Gate the graded invariant on identity reliability

- [ ] Read the probe report `probe-ensemble.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/discovery/probe-ensemble.md` to confirm where the graded invariant `executor_model_class NOT IN reviewer_model_classes` is evaluated, then read the live `src/superclaude/cli/reflect/ensemble.py` (and any dataclass file the probe indicates holds the invariant result), THEN edit the relevant file(s) so the graded invariant is ASSERTED (evaluated and enforced as a real check) when `executor_class_source ∈ {flag, env, frontmatter}` and is WAIVED-NOT-FAILED when the source is `log-heuristic` or `unknown` — a waive records the invariant as not-applicable/waived rather than failed, and does NOT mark the run as a content failure or collapse the tier, ensuring the assert path and the waive path are clearly distinguished in the contract output, a waive carries no exit-code penalty (waive ≠ fail ≠ collapse), the C3 reader value (Phase 4) feeds the invariant, and NO no-nesting-guard-banned token is introduced into `ensemble.py`. If unable to complete due to unclear invariant location or file access issues, log the specific blocker using the templated format in the ### Phase 7 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 7.2:** Per-edit gate after the C4 edit

- [ ] Use the Bash tool to run `uv run pytest tests/cli/reflect -q` and capture the complete output, AND (because Step 7.1 edited `ensemble.py`) ALSO run `uv run pytest tests/cli/reflect/test_no_nesting_guard.py -q`, then write the raw output to `pytest-phase7-c4.txt` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/test-results/pytest-phase7-c4.txt` and a structured summary `pytest-phase7-c4-summary.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/test-results/pytest-phase7-c4-summary.md` (overall result, counts, no-nesting-guard result, failure table), ensuring the summary matches the raw output with no fabrication. IF any test FAILS, fix the cause in the edited `*.py` file (NOT by weakening the guard) and re-run until green before marking complete. If the command fails to execute, log the specific blocker using the templated format in the ### Phase 7 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

### Phase Gate 7: Code-Review QA for C3/C2/C1/C4 (M3 Lens-Based, serialized fix per I20, full intensity ≥5 agents)

This intermediate code-review gate verifies the combined C3 (Phase 4), C2 (Phase 5), C1 (Phase 6), and C4 (Phase 7) edits before the eval/test phase builds witnesses on them. Minimum 5 agents (3 rf-qa structural/correctness lenses + 2 rf-qa-qualitative semantic lenses), all report-only; a single serialized fix agent; a 2-agent verification round. Gate type: code-review (2 max fix cycles, then Open Questions). Each agent spawn is its own `- [ ]` item with an embedded lens-specific adversarial prompt.

**Step PG7.1:** Aggregate the C3/C2/C1/C4 edits

- [ ] Use Glob to find all `src/superclaude/cli/reflect/*.py` files modified across Phases 4-7 and the per-edit test summaries (`pytest-phase4-c3-summary.md`, `pytest-phase5-c2-summary.md`, `pytest-phase6-c1-summary.md`, `pytest-phase7-c4-summary.md`), read each, then use Bash `git diff --stat` (read-only) over the reflect package to enumerate the changed hunks, and write an aggregation summary `phase-4-7-output-summary.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/reports/phase-4-7-output-summary.md` listing every file changed with the specific lines/functions touched per edit (C3 reader, C2 trigger narrowing, C1 non-collapsing Tier-2, C4 invariant gating) and the per-edit gate result, ensuring all four edits and all four gate summaries are represented with no omission. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step PG7.2:** Spawn structural/correctness lens agents (PARALLEL, report-only)

- [ ] Spawn an **rf-qa** agent with the **trigger-and-reader correctness lens** and adversarial framing "Assume C3/C2 have at least 5 correctness errors. Find them.": it MUST read `phase-outputs/reports/phase-4-7-output-summary.md` and the edited `src/superclaude/cli/reflect/*.py` file(s) and verify (a) the C3 reader reads `executor_model_class` via the existing constant and sets `executor_class_source=frontmatter`, and (b) the C2 trigger fires ONLY for `{flag,env,frontmatter}` and never for `log-heuristic`/`unknown`, writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-structural-trigger-reader-report.md` with `fix_authorization: false`. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
- [ ] Spawn an **rf-qa** agent with the **tier-and-contract correctness lens** and adversarial framing "Assume C1 collapses the tier or mis-emits a contract field. Find it.": it MUST read the edited `ensemble.py`/`contract.py`/`models.py` and verify (a) the unsatisfiable disjoint-N=2 branch keeps `tier_reached == 2` (no collapse to 1), (b) it emits `executor_exclusion_unsatisfiable: true` + `t2_model_class_diversity: degraded`, and (c) exit-code semantics are unchanged (degraded ≠ content failure), writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-structural-tier-contract-report.md` with `fix_authorization: false`. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
- [ ] Spawn an **rf-qa** agent with the **no-nesting-guard + invariant-gating lens** and adversarial framing "Assume an edit added a banned token or mis-gated the invariant. Find it.": it MUST read the edited `ensemble.py`/`runner.py` and `tests/cli/reflect/test_no_nesting_guard.py` and verify (a) NO banned token (`import anthropic`, `from anthropic`, `subagent_type`, `Agent(`, `Task(`, async/await, sprint/roadmap imports) was introduced, and (b) the C4 invariant is ASSERTED for reliable sources and WAIVED-NOT-FAILED (not failed, not tier-collapsing) for `log-heuristic`/`unknown`, writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-structural-guard-invariant-report.md` with `fix_authorization: false`. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step PG7.3:** Spawn semantic lens agents (PARALLEL with PG7.2, report-only)

- [ ] Spawn an **rf-qa-qualitative** agent with the **Option-C spec-fidelity lens** and adversarial framing "Assume C1-C4 deviate from the Option C 5-point list in at least 3 ways. Find them.": it MUST read the driving spec at `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/.dev/brainstorms/pr197-final-merge-strategy/adversarial-decisionA/merged-decisionA-recommendation.md` (lines ~33-40) and the edited `*.py` file(s) and verify each of C1/C2/C3/C4 matches its spec bullet (non-collapsing degraded Tier-2; trigger narrowed to reliable identity with log-heuristic dropped; reflect-side reader INV-202; invariant asserted-when-reliable / waived-not-failed otherwise), writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-content-option-c-fidelity-report.md` with `fix_authorization: false`. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
- [ ] Spawn an **rf-qa-qualitative** agent with the **exit-code-semantics preservation lens** and adversarial framing "Assume an edit silently changed reflect exit-code semantics. Find it.": it MUST read the edited `contract.py`/`ensemble.py` and `tests/cli/reflect/test_verdict_mapping.py` and verify that NONE of C1/C2/C4 turned a `degraded` or `waived` outcome into a content failure or changed the verdict→exit-code mapping (degraded ≠ content failure; waive ≠ fail), writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-content-exit-code-semantics-report.md` with `fix_authorization: false`. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step PG7.4:** Consolidate findings and apply fixes (serialized per I20)

- [ ] Read ALL five QA reports from Steps PG7.2-PG7.3 in `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/` and consolidate them into `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-consolidated-findings-phase7.md`, deduplicating issues (same issue from multiple lenses listed once with originating lenses noted) with severity, ensuring every issue from every report is captured. Consolidated verdict is FAIL if ANY agent reported ANY issue of any severity. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
- [ ] Spawn ONE **rf-qa** fix agent with `fix_authorization: true` and the consolidated findings file `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-consolidated-findings-phase7.md` as input: it MUST apply ALL consolidated fixes to the affected `src/superclaude/cli/reflect/*.py` file(s) WITHOUT introducing any no-nesting-guard-banned token, WITHOUT collapsing the tier, and WITHOUT changing exit-code semantics, ensuring every consolidated finding is addressed. If the consolidated verdict is PASS, record "No findings — fix phase skipped" and mark complete. After applying fixes, re-run `uv run pytest tests/cli/reflect tests/cli/reflect/test_no_nesting_guard.py -q` to confirm green. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step PG7.5:** Verification round (PARALLEL) and conditional proceed

- [ ] Spawn an **rf-qa** verification agent (`fix_authorization: false`) to confirm the Step PG7.4 fixes were applied correctly across C3/C2/C1/C4 and that no new correctness issue, banned token, tier-collapse, or exit-code regression was introduced, writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-verification-structural-phase7.md`. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
- [ ] Spawn an **rf-qa-qualitative** verification agent (`fix_authorization: false`) to confirm Option-C spec-fidelity and exit-code-semantics preservation were maintained after the fixes, writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-verification-content-phase7.md`. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
- [ ] Read both verification reports (`qa-verification-structural-phase7.md`, `qa-verification-content-phase7.md`): IF both report PASS, write `gate7-verdict.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/plans/gate7-verdict.md` recording PASS and proceed to Phase 8; IF either reports FAIL, repeat Steps PG7.4-PG7.5 up to a maximum of 2 fix cycles (code-review / task-integrity limit), after which remaining unresolved issues become Open Questions in the ### Follow-Up Items section and the gate proceeds with those documented; record the cycle count in `gate7-verdict.md`, ensuring the verdict reflects the actual verification reports. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 8: C5 — Evals / Tests (extend existing reflect tests + add new unit witnesses)

C5 proves the behavior: (a) a same-class reviewer panel is actually avoided when identity is reliable, (b) the unreliable-source case WAIVES (not FAILS) the invariant, (c) the unsatisfiable branch stays Tier-2 with `executor_exclusion_unsatisfiable: true` + `t2_model_class_diversity: degraded`. EXTEND the existing tests rather than replacing them, and keep the no-nesting guard green. Each test addition is its own item, and the per-edit reflect gate runs after each test edit.

**Step 8.1:** Extend `test_ensemble_unit.py` — reliable same-class exclusion avoids a same-class panel (C5a)

- [ ] Read the probe report `probe-runner-tests.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/discovery/probe-runner-tests.md` to identify the existing diversity/reviewer-count unit tests and the fixture/stub-transport pattern, then read the live `tests/cli/reflect/test_ensemble_unit.py` to match its style, THEN add a new unit test that, with `executor_class_source` set to a reliable value (`flag`/`env`/`frontmatter`) and an executor model class that collides with a candidate reviewer class, ASSERTS that the resulting reviewer panel does NOT contain the executor's model class (the same-class panel is avoided), ensuring the test uses the existing fixture/stub-transport pattern, names the test descriptively (e.g., `test_reliable_same_class_exclusion_avoids_same_class_panel`), asserts on the actual panel/`reviewer_model_classes` output with no fabricated assertion, and does not modify unrelated tests. If unable to complete, log the specific blocker using the templated format in the ### Phase 8 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 8.2:** Extend `test_ensemble_unit.py` — unreliable source WAIVES (not FAILS) the invariant (C5 / C4 witness)

- [ ] Read the live `tests/cli/reflect/test_ensemble_unit.py` (matching the style confirmed in `probe-runner-tests.md`), THEN add a new unit test that, with `executor_class_source` set to `log-heuristic` (or `unknown`) and an executor model class that would collide with a reviewer class, ASSERTS that the graded invariant `executor_model_class NOT IN reviewer_model_classes` is recorded as WAIVED (not-applicable/waived) rather than FAILED, that the run is NOT marked a content failure, and that the tier is NOT collapsed, ensuring the test names itself descriptively (e.g., `test_unreliable_source_waives_invariant_not_fail`), asserts on the actual waive/fail status field with no fabricated assertion, and does not modify unrelated tests. If unable to complete, log the specific blocker using the templated format in the ### Phase 8 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 8.3:** Extend `test_ensemble_unit.py` — unsatisfiable branch stays Tier-2 with degraded contract fields (C5b unit)

- [ ] Read the live `tests/cli/reflect/test_ensemble_unit.py` and the existing source-order / contract-degradation coverage identified in `probe-runner-tests.md`, THEN add a new unit test that, when a disjoint N=2 reviewer panel cannot be reached (executor-class collision exhausts distinct classes), ASSERTS that the contract reports `tier_reached == 2` (NOT collapsed to 1), `executor_exclusion_unsatisfiable is True`, and `t2_model_class_diversity == "degraded"`, ensuring the test names itself descriptively (e.g., `test_unsatisfiable_disjoint_panel_stays_tier2_degraded`), asserts on the actual contract fields with no fabricated assertion, and does not modify unrelated tests. If unable to complete, log the specific blocker using the templated format in the ### Phase 8 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 8.4:** Extend `test_ensemble_stub_integration.py` — positive/negative Tier-2 stub witness for the unsatisfiable branch (C5b integration)

- [ ] Read the probe report `probe-runner-tests.md` to identify the existing positive/negative Tier-2 stub-integration witnesses, then read the live `tests/cli/reflect/test_ensemble_stub_integration.py` to match its stub-transport pattern, THEN add a stub-integration test that drives the ensemble through the unsatisfiable-disjoint-panel path end-to-end (via the existing stub transport) and witnesses that the run STAYS Tier-2 (does not collapse to Tier-1) and surfaces `executor_exclusion_unsatisfiable: true` + `t2_model_class_diversity: degraded` in the contract, plus a complementary negative witness confirming that a satisfiable reliable-identity path produces a non-degraded disjoint Tier-2 panel, ensuring both witnesses use the existing stub pattern, name themselves descriptively, assert on actual contract output with no fabricated assertion, and do not modify unrelated tests. If unable to complete, log the specific blocker using the templated format in the ### Phase 8 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 8.5:** Per-edit gate after the test additions (includes no-nesting guard)

- [ ] Use the Bash tool to run `uv run pytest tests/cli/reflect -q` and `uv run pytest tests/cli/reflect/test_no_nesting_guard.py -q` and capture the complete output, then write the raw output to `pytest-phase8-c5.txt` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/test-results/pytest-phase8-c5.txt` and a structured summary `pytest-phase8-c5-summary.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/test-results/pytest-phase8-c5-summary.md` (overall result, counts, no-nesting-guard result, and explicit confirmation that the four new tests from Steps 8.1-8.4 ran and PASSED, listed by name), ensuring the summary matches the raw output with no fabrication and the four new test names appear as passed. IF any test FAILS, fix the cause (in the test if the assertion is wrong, or in the `src/superclaude/cli/reflect/*.py` source if the behavior is wrong — NOT by weakening the guard) and re-run until green. If the command fails to execute, log the specific blocker using the templated format in the ### Phase 8 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

### Phase 9: Doc-Prose Alignment (only where C2/C3/C4 add new prose)

Update the sc-reflect-protocol prose surfaces ONLY where C2/C3/C4 add NEW behavior prose. These are Option-A-owned surfaces (exclusion model already documented by Option A); A→C touches them only to document the reliable-identity gating (C2), the reflect-side reader (C3/INV-202), and the non-collapsing degraded/waive behavior (C1/C4). Do NOT re-author the Option-A exclusion prose.

**Step 9.1:** Update `SKILL.md` prose for reliable-identity gating + non-collapsing degraded

- [ ] Read the driving spec at `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/.dev/brainstorms/pr197-final-merge-strategy/adversarial-decisionA/merged-decisionA-recommendation.md` (Option C lines ~33-40) and the precondition verdict `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/plans/precondition-verdict.md` to confirm the Option-A exclusion prose already present, then read the live `src/superclaude/skills/sc-reflect-protocol/SKILL.md` to locate the §7.1 exclusion section and any §11.3 partition / telemetry-field prose, THEN edit `SKILL.md` to ADD prose (without re-authoring the Option-A exclusion text) describing: (a) the exclusion trigger fires ONLY for reliable identity `executor_class_source ∈ {flag, env, frontmatter}` and the commit-author `log-heuristic` source is dropped from the trigger (C2); (b) the reflect wrapper now READS `executor_model_class` from frontmatter (C3/INV-202); (c) on an unsatisfiable disjoint-N=2 collision the wrapper STAYS Tier-2 and emits `executor_exclusion_unsatisfiable: true` + `t2_model_class_diversity: degraded` (loud, non-collapsing, degraded ≠ content failure) (C1); and (d) the graded invariant is asserted-when-reliable / waived-not-failed otherwise (C4), ensuring the new prose is consistent with the actual implemented behavior, no contradicting instance-level / no-removal sentences remain adjacent to the new prose, and `executor_class_source` and `executor_exclusion_unsatisfiable` are spelled exactly as in the code. If unable to complete, log the specific blocker using the templated format in the ### Phase 9 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 9.2:** Update `refs/reviewer-spec.md` prose for reliable-identity gating + waive semantics

- [ ] Read the live `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md` to locate the class-diversity / executor-vs-reviewer disjointness prose (the research notes flag an internal inconsistency here between "no removal" text and a later "disjointness is enforced" sentence), THEN edit `reviewer-spec.md` to ADD/RECONCILE prose so it consistently states that executor-vs-reviewer disjointness is enforced ONLY when identity is reliable (`flag|env|frontmatter`), is WAIVED-NOT-FAILED when the source is `log-heuristic`/`unknown`, and that an unsatisfiable disjoint panel degrades (non-collapsing Tier-2) rather than failing, ensuring any pre-existing internal contradiction between "never removed" and "disjointness enforced" is resolved in favor of the implemented reliable-identity-gated behavior, the prose matches the code, and the `executor_class_source` enum values are named exactly. If unable to complete, log the specific blocker using the templated format in the ### Phase 9 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 9.3:** Update `refs/reflection-rubric.md` prose for the gated invariant

- [ ] Read the live `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md` to locate the prose that (per research) says executor class is deliberately not separated from the reviewer pool, THEN edit `reflection-rubric.md` to ADD/UPDATE prose so the rubric reflects the implemented C4 behavior — the graded invariant `executor_model_class NOT IN reviewer_model_classes` is ASSERTED when identity is reliable and WAIVED-NOT-FAILED otherwise — and remove or correct any sentence stating the executor class is never separated, ensuring the rubric prose matches the implemented gating, no stale "not separated" claim remains, and the enum values are named exactly as in the code. If unable to complete, log the specific blocker using the templated format in the ### Phase 9 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

### Phase 10: Final Validation, Source-of-Truth Sync, Final QA Gate, and POST Reflect

This phase runs the mandated final validation command sequence VERBATIM in order, runs the final-document lens-based QA gate on the changed surfaces, then (penultimate) runs the POST reflect wrapper shell-out, then (last) sets status to Done. Run the validation commands in the EXACT order given.

**Step 10.1:** Sync source-of-truth to `.claude/`

- [ ] Use the Bash tool to run the single-line command `make sync-dev` (because the source of truth is `src/superclaude/` and the `.claude/` mirrors must be regenerated after the skill/ref prose edits in Phase 9 and any code changes), capturing the output, then record PASS/FAIL and the command output in `validation-final.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/test-results/validation-final.md` (create the file with a `## make sync-dev` section), ensuring the command completed without error. DO NOT stage or commit any `.claude/` path (only `.claude/settings.json` is tracked). If the command fails, log the specific blocker using the templated format in the ### Phase 10 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 10.2:** Verify source-of-truth sync

- [ ] Use the Bash tool to run the single-line command `make verify-sync` (to confirm `src/superclaude/` and `.claude/` are in sync after Step 10.1), capturing the output, then append a `## make verify-sync` section with PASS/FAIL and the output to `validation-final.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/test-results/validation-final.md`, ensuring verify-sync reports in-sync. IF it reports out-of-sync, re-run `make sync-dev` and re-verify before marking complete. If the command fails, log the specific blocker using the templated format in the ### Phase 10 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 10.3:** Run the full reflect + swarm test suite

- [ ] Use the Bash tool to run the single-line command `uv run pytest tests/cli/reflect tests/swarm -q` (the full reflect + swarm gate; swarm is included because reflect shares the no-nesting/transport surface), capturing the output, then append a `## uv run pytest tests/cli/reflect tests/swarm -q` section with overall result, pass/fail counts, and any failure table to `validation-final.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/test-results/validation-final.md`, ensuring the recorded counts match the raw output with no fabrication and overall result is PASSED. IF any test FAILS, fix the cause in the relevant `src/superclaude/cli/reflect/*.py` source or test (NOT by weakening the no-nesting guard) and re-run until green before marking complete. If the command fails to execute, log the specific blocker using the templated format in the ### Phase 10 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 10.4:** Run ruff format check

- [ ] Use the Bash tool to run the single-line command `uv run ruff format --check src/ tests/` (CI runs `ruff format --check` separately from `make lint`, so green lint does NOT imply green format), capturing the output, then append a `## uv run ruff format --check src/ tests/` section with PASS/FAIL and the output to `validation-final.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/test-results/validation-final.md`, ensuring the check passes. IF the check reports files needing formatting, run `uv run ruff format` SCOPED ONLY to the files this task changed (the reflect `*.py` and any changed tests — NOT a broad repo-wide format, which would reformat unrelated files due to a possible worktree ruff version mismatch), then re-run the check before marking complete. If the command fails to execute, log the specific blocker using the templated format in the ### Phase 10 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 10.5:** Run lint

- [ ] Use the Bash tool to run the single-line command `make lint` (ruff check), capturing the output, then append a `## make lint` section with PASS/FAIL and the output to `validation-final.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/test-results/validation-final.md`, ensuring lint passes with no errors. IF lint reports errors in this task's changed files, fix them and re-run until clean before marking complete. If the command fails to execute, log the specific blocker using the templated format in the ### Phase 10 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

### Phase Gate 10: Final-Document QA (M3 Lens-Based, full intensity, serialized fix per I20)

Final-state lens-based QA on the cumulative changed surface (the reflect `*.py` edits, the extended/new tests, and the skill/ref prose). Per I19 final-gate floor: 6 agents (3 rf-qa structural + 3 rf-qa-qualitative content), all report-only; single serialized fix agent; 2-agent verification round. Gate type: report-validation (3 max fix cycles, then HALT and escalate). This task does NOT produce a >500-line document and does NOT transform source material into a different format, so NO M4 source-fidelity gate is required. Each agent spawn is its own `- [ ]` item with an embedded lens-specific adversarial prompt.

**Step PG10.1:** Aggregate the full change set

- [ ] Use Bash `git diff --stat` (read-only) over the worktree plus Glob over `phase-outputs/test-results/*-summary.md` to enumerate every file changed by this task (reflect `*.py`, `tests/cli/reflect/*.py`, skill/ref prose) and the final validation results, then write `final-change-summary.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/reports/final-change-summary.md` listing every changed file, the A→C edit it implements (C1/C2/C3/C4/telemetry/test/doc), and the final validation command results (sync-dev, verify-sync, full pytest, ruff format, lint), ensuring every changed file and validation command is represented with no omission. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step PG10.2:** Spawn structural lens agents (PARALLEL, report-only)

- [ ] Spawn an **rf-qa** agent with the **completeness lens** and adversarial framing "Assume at least 5 of the A→C edits, telemetry, tests, or doc updates are missing or incomplete. Find them.": it MUST read `phase-outputs/reports/final-change-summary.md` and the driving spec Option C list and verify ALL of C1, C2, C3, C4, the `executor_class_source` telemetry emission, the four C5 tests, and the three doc-prose updates are present and complete, writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-final-structural-completeness-report.md` with `fix_authorization: false`. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
- [ ] Spawn an **rf-qa** agent with the **internal-consistency lens** and adversarial framing "Assume at least 5 inconsistencies exist across code, tests, and docs. Find them.": it MUST read the changed reflect `*.py`, the extended tests, and the three skill/ref prose surfaces and verify the `executor_class_source` enum values, `executor_exclusion_unsatisfiable`, and `t2_model_class_diversity: degraded` are spelled and used consistently across code, tests, and prose with no contradictions, writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-final-structural-consistency-report.md` with `fix_authorization: false`. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
- [ ] Spawn an **rf-qa** agent with the **guard-and-evidence lens** and adversarial framing "Assume a banned nesting token slipped in or a validation result is misreported. Find it.": it MUST read the changed `runner.py`/`ensemble.py`, `tests/cli/reflect/test_no_nesting_guard.py`, and `phase-outputs/test-results/validation-final.md` and verify NO banned token was introduced and that the recorded validation results (sync-dev, verify-sync, full pytest, ruff format, lint) all actually PASSED with outputs matching the captured raw results, writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-final-structural-guard-evidence-report.md` with `fix_authorization: false`. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step PG10.3:** Spawn content lens agents (PARALLEL with PG10.2, report-only)

- [ ] Spawn an **rf-qa-qualitative** agent with the **spec-fidelity lens** and adversarial framing "Assume the final change set deviates from Option C / X-004 in at least 5 ways. Find them.": it MUST read the driving spec (lines ~33-47) and the final change summary and verify the implemented behavior faithfully realizes the Option C 5-point list AND the telemetry de-risk (emission + sampling + PENDING urgency checkpoint), writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-final-content-spec-fidelity-report.md` with `fix_authorization: false`. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
- [ ] Spawn an **rf-qa-qualitative** agent with the **exit-code / degraded-semantics lens** and adversarial framing "Assume an edit changed reflect exit-code semantics or made degraded/waive a failure. Find it.": it MUST read the changed `contract.py`/`ensemble.py`, `tests/cli/reflect/test_verdict_mapping.py`, and the C5 tests and verify that `degraded` (C1) and `waived` (C4) outcomes carry NO exit-code penalty and that Tier-2 is never collapsed on the unsatisfiable branch, writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-final-content-exit-code-report.md` with `fix_authorization: false`. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
- [ ] Spawn an **rf-qa-qualitative** agent with the **doc-code parity lens** and adversarial framing "Assume the skill/ref prose contradicts the implemented code in at least 3 places. Find them.": it MUST read the three updated prose surfaces (`SKILL.md`, `refs/reviewer-spec.md`, `refs/reflection-rubric.md`) and the changed reflect `*.py` and verify the prose accurately describes the implemented reliable-identity gating, the C3 reader, the non-collapsing degraded behavior, and the assert-vs-waive invariant — with NO stale instance-level / "never removed" / "not separated" claims left contradicting the code, writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-final-content-doc-parity-report.md` with `fix_authorization: false`. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step PG10.4:** Consolidate findings and apply fixes (serialized per I20)

- [ ] Read ALL six QA reports from Steps PG10.2-PG10.3 in `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/` and consolidate into `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-consolidated-findings-final.md`, deduplicating issues with severity and originating lens, ensuring every issue from every report is captured. Consolidated verdict is FAIL if ANY agent reported ANY issue of any severity. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
- [ ] Spawn ONE **rf-qa** fix agent with `fix_authorization: true` and the consolidated findings file `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-consolidated-findings-final.md`: it MUST apply ALL consolidated fixes to the affected code/tests/prose WITHOUT introducing any banned nesting token, collapsing the tier, or changing exit-code semantics, then re-run `make sync-dev`, `uv run pytest tests/cli/reflect tests/swarm -q`, `uv run ruff format --check src/ tests/`, and `make lint` to confirm the validation gates remain green after the fixes, ensuring every consolidated finding is addressed. If the consolidated verdict is PASS, record "No findings — fix phase skipped" and mark complete. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step PG10.5:** Verification round (PARALLEL) and conditional proceed

- [ ] Spawn an **rf-qa** verification agent (`fix_authorization: false`) to confirm the Step PG10.4 fixes were applied correctly across code/tests, no banned token / tier-collapse / exit-code regression was introduced, and the validation gates are green, writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-final-verification-structural.md`. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
- [ ] Spawn an **rf-qa-qualitative** verification agent (`fix_authorization: false`) to confirm spec-fidelity, degraded/waive semantics, and doc-code parity were maintained after the fixes, writing its report to `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/qa/qa-final-verification-content.md`. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
- [ ] Read both final verification reports: IF both report PASS, write `gate10-verdict.md` at `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/plans/gate10-verdict.md` recording PASS and proceed to Post-Completion Actions; IF either reports FAIL, repeat Steps PG10.4-PG10.5 up to a maximum of 3 fix cycles (report-validation gate limit), after which YOU MUST HALT and escalate to the user (set `status` to "⚪ Blocked", populate `blocker_reason`, and write a ### Phase Gate Findings escalation entry) rather than marking the task Done; record the cycle count in `gate10-verdict.md`, ensuring the verdict reflects the actual verification reports. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

## Post-Completion Actions

- [ ] Verify all task outputs by using Glob to confirm every output file specified in the checklist items exists on disk — the edited `src/superclaude/cli/reflect/*.py` files, the extended `tests/cli/reflect/test_ensemble_unit.py` and `test_ensemble_stub_integration.py`, the three updated skill/ref prose files, the discovery probe reports, the per-edit pytest summaries, the sampling artifact, the PENDING human-decision checkpoint, the QA reports, and `validation-final.md` — ensuring no expected deliverable is missing. If any file is missing, check the Task Log for a documented blocker explaining its absence; if missing without reason, log the gap in the ### Follow-Up Items section below, then mark this item complete. Once done, mark this item as complete.

- [ ] Confirm the source-code test state is clean by verifying (from `phase-outputs/test-results/validation-final.md`) that the final `uv run pytest tests/cli/reflect tests/swarm -q` run passed with no regressions and the no-nesting guard is green; if the validation was already recorded as passing in Step 10.3 / Step PG10.4 and no subsequent source change was made, note "Tests verified green in Phase 10 / Phase Gate 10" in the ### Execution Log and mark this item complete. If a source change was made after the last green run, re-run `uv run pytest tests/cli/reflect tests/swarm -q` and confirm green before marking complete. Once done, mark this item as complete.

- [ ] Confirm the `needs_human_decision` checkpoint is still correctly PENDING by reading `.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/phase-outputs/plans/human-decision-urgency-checkpoint.md` and verifying it still reads `DECISION_STATUS: PENDING` with NO default applied, ensuring the urgency/priority decision remains routed to the operator (RyanW) and was not silently auto-resolved during execution; record in the ### Execution Log that the urgency decision remains PENDING operator confirmation. If the checkpoint was somehow auto-resolved, revert it to PENDING and log the deviation in the ### Deviations from Process section, then mark this item complete. Once done, mark this item as complete.

- [ ] Create a ### Task Summary section at the top of the ## Task Log / Notes section at the bottom of this task file using the templated format provided there, documenting: work completed (the precondition verdict, the `executor_class_source` telemetry emission, C3 reader, C2 narrowed trigger, C1 non-collapsing Tier-2, C4 gated invariant, the four C5 tests, the three doc-prose updates), the PENDING human-decision urgency checkpoint and its status, challenges encountered, any deviations from the planned process and their rationale, and all blockers logged during execution with their resolution status, ensuring the summary accurately reflects the execution log with no fabrication. Once the summary is complete, mark this item as complete.

- [ ] Run the POST reflect-gate validation by using the Bash tool to execute the FLAT wrapper shell-out `superclaude reflect run /config/workspace/IronClaude/.dev/worktrees/pr197-remediation/.dev/tasks/to-do/TASK-RF-reflect-ac-hybrid-20260628-205715/TASK-RF-reflect-ac-hybrid-20260628-205715.md --depth deep --fix --promote`, BUT FIRST guard against recursive invocation: IF the environment variable `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` is already set (truthy), SKIP this item entirely and record "POST reflect skipped — SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE already set (recursion guard)" in the ### Execution Log, then mark complete; OTHERWISE run the command and CONSUME its exit code — IF the exit code is `0`, record the reflect verdict and proceed to the final status-update item; IF the exit code is NON-ZERO, record the reflect output and exit code, set `status` to "⚪ Blocked" with `blocker_reason` naming the POST reflect failure, and HALT (do NOT mark the task Done). DO NOT add `--base` or `--spec` to this POST invocation, and DO NOT spawn any agent or use any agent-spawn token — this is a flat CLI shell-out only. The executor records the resulting verdict into the `reflect_post:` frontmatter room per the wrapper's contract. If the command fails to execute (binary missing), log the specific blocker using the templated format in the ### Phase 10 Findings section of the ## Task Log / Notes, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

- [ ] Update `completion_date` and `updated_date` to today's date and update task `status` to "🟢 Done" in the frontmatter (ONLY if the POST reflect gate above returned exit code 0 and the final QA gate passed — otherwise the task remains "⚪ Blocked"), then add an entry to the ### Execution Log in the ## Task Log / Notes section using the format: `**[YYYY-MM-DD HH:MM]** - Task completed: Updated status to "🟢 Done" and completion_date.` This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

## Task Log / Notes 📋

### Task Summary
<!-- Fill this section in Post-Completion Actions -->

**Completion Date:** [YYYY-MM-DD]

**Work Completed:**
- [Precondition verdict]: [OPTION-A-PRESENT/ABSENT + evidence]
- [Files created]: [List with paths]
- [Files modified]: [List with paths — reflect *.py, tests, skill/ref prose]
- [Handoff files created]: [List phase-outputs/ and qa/ files]

**Challenges Encountered:**
- [Challenge]: [How addressed] OR None

**Deviations from Process:**
- [Deviation]: [Rationale] OR None

**Human-Decision Checkpoint Status:**
- Urgency/priority of C2 heuristic-drop: **PENDING** operator (RyanW) confirmation — see `phase-outputs/plans/human-decision-urgency-checkpoint.md`. OR [Resolved: ...]

**Blockers Logged:**
- [Step X.Y]: [Description] - **Status:** [Resolved/Unresolved] OR None

**Follow-Up Required:** [Yes/No] - [Description if yes]

### Execution Log

<!-- TEMPLATE FOR EXECUTION LOG ENTRIES:
**[YYYY-MM-DD HH:MM]** - [Action taken]: [Brief description of what was done and outcome]
-->

**[YYYY-MM-DD HH:MM]** - Task started: Updated status to "🟠 Doing" and start_date.

**[YYYY-MM-DD HH:MM]** - Task completed: Updated status to "🟢 Done" and completion_date.

### Phase 1 - Preparation and Setup Findings

<!-- TEMPLATE FOR PHASE FINDINGS:
**[YYYY-MM-DD HH:MM]** - [Step X.Y]: [Finding or blocker description]
- **Status:** [Completed | Blocked]
- **Details:** [Specific information about what was found, created, or what blocked completion]
- **Blocker Reason (if blocked):** [Specific reason why this could not be completed]
- **Files Affected:** [List of files read, created, or modified]
-->

### Phase 2 - Precondition Verification and Code-Reading Probe Findings

<!-- PRECONDITION-FAILURE entries (Step 2.1 HALT) go here. Template:
**[YYYY-MM-DD HH:MM]** - Step 2.1 PRECONDITION-FAILURE:
- **Verdict:** OPTION-A-ABSENT
- **Failed sub-checks:** [which of (a)-(e) were absent, with file:line evidence]
- **Action taken:** Set status to "⚪ Blocked"; HALTED task — A→C edits NOT begun (would build on wrong base)
- **Required to Unblock:** Land Option A (executor-class exclusion) on the execution branch, then re-run this task.
-->

### Phase 3 - Telemetry Emission + Sampling + Human-Decision Checkpoint Findings

### Phase 4 - C3 Reflect-Side Reader Findings

### Phase 5 - C2 Narrow Exclusion Trigger Findings

### Phase 6 - C1 Non-Collapsing Tier-2 Findings

### Phase 7 - C4 Identity-Gated Invariant Findings

### Phase 8 - C5 Evals / Tests Findings

### Phase 9 - Doc-Prose Alignment Findings

### Phase 10 - Final Validation, Sync, and POST Reflect Findings

### Phase Gate Findings

_QA gate verdicts, fix cycle counts, and unresolved issues are recorded here (Gates 3, 7, 10)._

### Follow-Up Items Identified

<!-- TEMPLATE FOR FOLLOW-UP ITEMS:
- **[Priority: High/Medium/Low]** [Description of follow-up needed] - Identified in Step [X.Y]
-->

### Deviations from Process

<!-- TEMPLATE FOR DEVIATIONS:
**[YYYY-MM-DD HH:MM]** - Deviation from [Step X.Y]:
- **Expected:** [What the process specified]
- **Actual:** [What was done instead]
- **Rationale:** [Why this deviation was necessary]
-->
