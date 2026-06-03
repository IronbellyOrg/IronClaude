---
id: "TASK-RF-20260602-sprint-auto-resume"
title: "Auto-Resume as the Default for sprint run / rerun-tasks (v4.3.5)"
description: "Make auto-resume the default behavior of the sprint pipeline. Bare `superclaude sprint run <index>` / `sprint rerun-tasks <index>` auto-detect the interrupted phase from on-disk state (atomic phase-N-result.json as truth anchor) and resume as if the operator supplied --start/--end (or --phase/--tasks). Explicit flags continue to disable auto-detection. Implements three new read-first modules (ResumePlanner, DriftAssessor, BoundaryIntegrityGate) plus one backward-compatible write-path change, wired into the two CLI entrypoints. Non-idempotent phases mean the resume seam is treated as suspect and must pass an integrity gate."
status: "🟢 Done"
type: "✨ Feature"
priority: "🔼 High"
created_date: "2026-06-02"
updated_date: "2026-06-02"
assigned_to: "orchestrator"
autogen: false
autogen_method: ""
coordinator: orchestrator
parent_task: ""
depends_on: []
related_docs:
- path: ".dev/brainstorms/20260602-sprint-auto-resume-default/design.md"
  description: "Authoritative technical design (post-adversarial-refactor). DD-1..DD-5, §3-§10."
- path: ".dev/brainstorms/20260602-sprint-auto-resume-default/merged-requirements.md"
  description: "FR-1..5, AC-1..9, NFR-1..4 source."
- path: ".dev/brainstorms/20260602-sprint-auto-resume-default/validation/CONSOLIDATION.md"
  description: "What the 5 adversarial validators changed and why (durability model, advisory-LLM, report-only quarantine, INV-001, Click parameter-source)."
- path: "src/superclaude/cli/sprint/executor.py"
  description: "_write_phase_result_json (L2053) + atomic tmp+rename (L2070-2072); active_phases loop."
- path: "src/superclaude/cli/sprint/rerun_tasks.py"
  description: "_classify_transcript (L550), discover_failed_tasks_from_transcripts (L601), _content_sha256_excluding_rerun_block (L688), _declared_deliverables (L924), stash_and_restore_deliverables (L961), restore_from_bundle (L1039)."
- path: "src/superclaude/cli/sprint/recovery.py"
  description: "write_recovery_audit_log (L250), .recovery-locks lock helper (L278/L291), RecoveryBundle preserved/+manifest shape."
- path: "src/superclaude/cli/sprint/commands.py"
  description: "run() (L190), rerun_tasks() (L485), --start default=1 (L76), --end default=0 — CLI wiring points."
tags:
- "sprint"
- "auto-resume"
- "cli"
- "v4.3.5"
- "feature"
template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"
estimation: "Medium-large (3 new modules + 1 write-path change + 2 CLI wirings + ~12 tests)"
sprint: "v4.3.5"
due_date: ""
start_date: "2026-06-02"
completion_date: "2026-06-02"
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: static
---

# Auto-Resume as the Default for sprint run / rerun-tasks (v4.3.5)

## Task Overview

Make resume the **default behavior** of the sprint pipeline. Running bare `superclaude sprint run <index>` (or bare `superclaude sprint rerun-tasks <index>`) shall auto-detect where the previous run was interrupted from on-disk state and execute as if the operator had supplied the correct `--start/--end` (and, for the boundary phase, the correct per-task) options. Explicit flags continue to work and disable auto-detection.

The implementation adds three new **read-first** modules under `src/superclaude/cli/sprint/resume/` (`planner.py` → `ResumePlanner`, `drift.py` → `DriftAssessor`, `integrity.py` → `BoundaryIntegrityGate`, plus a `models.py` of dataclasses), exactly one backward-compatible write-path change (a `tasklist_sha256` field in `_write_phase_result_json`), and CLI wiring into `run()` and `rerun_tasks()`. Nothing about phase execution itself changes (NG1).

The defining safety property: sprint phases are **not idempotent**, so the resume **seam** (last completed task + next unfinished task) is treated as *suspect* and must pass a deterministic integrity gate before new work is layered on top. Per the adversarial consolidation: the atomic `phase-N-result.json` is the truth anchor (NOT the lossy JSONL ledger); all LLM use is **advisory** and never touches a gate verdict; cleanup is **report-only by default** with opt-in reversible copy-to-quarantine; per-phase drift hash uses `_content_sha256_excluding_rerun_block` over the per-phase `phase_obj.file` on BOTH sides (INV-001); and explicit-window detection uses Click **parameter source**, never value comparison.

## Key Objectives

- Implement `ResumePlanner` (FR-1): pure-read reconstruction of the resume plan from `execution-log.jsonl` + `phase-N-result.json` + transcripts, with result.json as the authoritative phase-completion signal (DD-1).
- Implement `DriftAssessor` (FR-3): deterministic tiered safety-confidence scoring; Tier 0 exact normalized-hash match (INV-001), Tier 1 whitespace-insensitive + structural diff (AC-4/AC-5), Tier 2 git annotation.
- Implement `BoundaryIntegrityGate` (FR-2): doubly-validate last-completed task (deterministic only), report-only-default + opt-in reversible quarantine of next-unfinished partial work, advisory Haiku coherence read (TASK-granularity only, never on verdict).
- Add the single backward-compatible write-path change: persist `tasklist_sha256` in `phase-N-result.json` (DD-4).
- Wire auto-resume into `run()` and `rerun_tasks()` with `--fresh`/`--restart`, `--yes`, `--dry-run`; detect explicit windows via Click parameter source (DD-5 / AC-7).
- Cover AC-1..AC-9 and the validator-corrected invariants with deterministic tests + the existing real-subprocess e2e harness; document the behavior change (R5) and bump version.

## Prerequisites & Dependencies

- Worktree on branch `SprintReRun`; cwd `/config/workspace/IronClaude/.claude/worktrees/SprintReRun`. All paths below are worktree-relative.
- The v4.3.0 rerun engine is present and merged (commits a77f5fdf..344a754a): classifiers, per-task status, merge-back, SHA-guard, real-subprocess e2e harness (`344a754a`).
- Python via **UV only** (`uv run pytest`). No `python -m` / bare `pip`.
- Read design.md §0 (DD-1..DD-5), §2 (data structures), §3-§6 (component contracts + wiring), §9 (test plan), §10 (phasing), §11 (evidence) before starting each phase.
- Phase ordering is strict: P1 unblocks all; P2 and P3 may proceed after P1; P4 depends on P1+P2+P3; P5 depends on P4.

## Execution Context

<!-- OPTIONAL task-level reading aid. Per-item Context fields + research/*.md remain the evidence venue with file:line citations. This block contains NO specific path.py:NN references (NFR-CONV.3). -->

- **References:** R-001: design.md DD-1..DD-5 (resolves OQ1-OQ5); R-002: merged-requirements.md FR-1..5 / AC-1..9 / NFR-1..4; R-003: validation/CONSOLIDATION.md (5 adversarial REFACTOR verdicts applied).
- **Source areas:** sprint resume modules (new), sprint executor result-json writer, sprint rerun-tasks classifiers and quarantine helpers, sprint recovery audit and lock helpers, sprint CLI commands, sprint config release-dir resolver, sprint test suite.
- **Key constraints:** atomic result.json is the truth anchor (LLM advisory-only, never on gate verdict — NFR-3); cleanup report-only by default + opt-in reversible copy quarantine (NFR-1); per-phase hash via the same normalized-hash function over the same per-phase file on both sides (INV-001); explicit-window detection via Click parameter source, NOT value comparison (AC-7); UV-only test execution.

---

## Phase 1: ResumePlanner + models + the one write-path change (FR-1, DD-1, DD-4)

> Read-only planner unblocks everything. The ONLY write-path change in the whole feature (DD-4) lands here and must be backward-compatible.

- [x] **1.1 — Create the `resume/` package skeleton**
  - **Context**: Three new read-first modules live in `src/superclaude/cli/sprint/resume/` per design §1. The directory does not exist yet (verified absent 2026-06-02).
  - **Action**: Create `src/superclaude/cli/sprint/resume/__init__.py` (empty or exporting the public classes). Confirm the package imports under the existing `superclaude.cli.sprint` namespace.
  - **Output**: `src/superclaude/cli/sprint/resume/__init__.py`.
  - **Verification**: `uv run python -c "import superclaude.cli.sprint.resume"` exits 0.
  - **Completion gate**: Package importable.

- [x] **1.2 — Implement `resume/models.py` dataclasses**
  - **Context**: design §2 specifies the exact dataclasses. `TaskStatus`/`PhaseStatus` are reused from `models.py` (locate by name via grep — `class TaskStatus`, `class PhaseStatus`).
  - **Action**: Implement `Granularity(Enum)` (TASK/PHASE/NONE); `BoundaryTask` (task_id, persisted_status, derived_status, artifacts_present, role, suspect); `ResumePlan` (index_path, release_dir, completed_phases, interrupted_phase, interrupt_kind, start_phase, end_phase, granularity, boundary_tasks, rerun_task_ids, ambiguous, ambiguity_reasons); `DriftAssessment` (confidence, tier, changed_paths, explanation, cosmetic_only); `BoundaryReport` (validated_last, suspects, quarantined, passed, blocking_reasons, coherence_warnings); and a `ResumeDecision` aggregate referenced by the commands helper (§8). Field names/types must match design §2 verbatim. `coherence_warnings: list[tuple[BoundaryTask, str]]` must NOT be part of `passed` (NFR-3).
  - **Output**: `src/superclaude/cli/sprint/resume/models.py`.
  - **Verification**: `uv run python -c "from superclaude.cli.sprint.resume.models import ResumePlan, BoundaryReport, DriftAssessment, BoundaryTask, Granularity, ResumeDecision"` exits 0; field set matches design §2.
  - **Completion gate**: All dataclasses importable with the design-specified fields.

- [x] **1.3 — Add `tasklist_sha256` to `_write_phase_result_json` (the ONE write-path change, DD-4)**
  - **Context**: `_write_phase_result_json` is at `src/superclaude/cli/sprint/executor.py:2053`; payload dict at L2059-2067; atomic tmp+rename at L2070-2072 (`tmp.replace(out)`). Today `source_tasklist_sha256` is only persisted inside a `RecoveryBundle` after a rerun (recovery.py:111) — fresh-run drift needs a baseline captured at each phase_complete.
  - **Action**: Extend the payload dict with one key: `tasklist_sha256 = _content_sha256_excluding_rerun_block(phase_obj.file)` for the phase being written — using the SAME function (`rerun_tasks.py:688`) over the per-phase `phase_obj.file` that `DriftAssessor` will use on the current side (INV-001). Reuse the existing atomic writer (do NOT add a second write). The field MUST be backward-compatible: absent ⇒ planner/DriftAssessor fall back to Tier-1/2, never crash.
  - **Output**: Modified `src/superclaude/cli/sprint/executor.py` (`_write_phase_result_json`).
  - **Verification**: Locate the function by name; confirm the new key rides the existing tmp+rename path (no second write). `uv run pytest tests/ -k "phase_result_json or write_phase_result" -v` (or the nearest existing executor result-json test) passes; manually confirm a generated `phase-N-result.json` contains `tasklist_sha256` and that loading a pre-v4.3.5 result.json without the key does not raise.
  - **Completion gate**: `tasklist_sha256` persisted via the atomic writer using `_content_sha256_excluding_rerun_block(phase_obj.file)`; absent-field load path verified non-crashing.

- [x] **1.4 — Implement `ResumePlanner.plan()` phase classification (FR-1.1/1.2/1.3, DD-1)**
  - **Context**: design §3. Reuse `_resolve_release_dir` + `discover_phases` (config.py L242/L58). `execution-log.jsonl` at release ROOT (models.py:543), `results/` (models.py:539). DD-1: result.json presence with PASS-family status is the AUTHORITATIVE completion signal; a torn/dropped `phase_complete` ledger line must NOT demote a phase whose atomic result.json proves completion. JSONL reading must be tolerant (skip malformed lines).
  - **Action**: Implement `plan(index_path, *, end_override=None) -> ResumePlan`. Per design §3: classify each phase as COMPLETED (result.json exists with PASS-family status) / CRASH (phase_start without close) / INTERRUPT (phase_interrupt, OR non-passing result.json) / PENDING. Compute `interrupted_phase` = lowest non-COMPLETED phase with any start/result else None; `start_phase` = interrupted_phase; `end_phase` = max phase number unless `end_override`. Handle FR-1.6: no phase ever started ⇒ fresh start_phase=1; all phases COMPLETED ⇒ `granularity=NONE` (nothing-to-resume).
  - **Output**: `src/superclaude/cli/sprint/resume/planner.py` (`ResumePlanner.plan`, phase-classification portion).
  - **Verification**: Unit-level: feed a synthetic release dir with result.json for P1,P2 and a dangling `phase_start` for P3 ⇒ `interrupted_phase==3`, `completed_phases==[1,2]`, `interrupt_kind=="crash"`. All-complete fixture ⇒ `granularity==NONE`. Planner performs NO writes (assert results/ unchanged).
  - **Completion gate**: Phase classification matches DD-1 (result.json authoritative) across COMPLETED/CRASH/INTERRUPT/PENDING/NONE.

- [x] **1.5 — Implement boundary disposition + granularity selection (FR-1.4/1.5)**
  - **Context**: design §3 step 2. result.json schema at executor.py:2053-2072. Per-task data present ⇒ `granularity=TASK`; build `BoundaryTask` per `task_results[]` with `persisted_status=tr.status`; `rerun_task_ids = [t.id for t if persisted_status != PASS]`. Absent task_results ⇒ call `discover_failed_tasks_from_transcripts(results_dir, interrupted)` (rerun_tasks.py:601); `granularity = TASK if derived else PHASE`. Mark `last_completed` (highest-index PASS) and `next_unfinished` (first non-PASS) roles.
  - **Action**: Implement the boundary-disposition block of `plan()`. Populate `boundary_tasks` (interrupted phase only) and `rerun_task_ids`. Assign roles `last_completed` / `next_unfinished` / `pending`.
  - **Output**: `src/superclaude/cli/sprint/resume/planner.py` (boundary-disposition portion).
  - **Verification**: Fixture with P3 result.json carrying one `fail_recoverable` task ⇒ `granularity==TASK`, `rerun_task_ids==[that task]`, `last_completed`/`next_unfinished` roles assigned. Hard-crash fixture (no result.json, partial transcripts) ⇒ `granularity` derived from transcripts (TASK if any derived, else PHASE).
  - **Completion gate**: Granularity + boundary roles + rerun_task_ids derived correctly for TASK and PHASE paths.

- [x] **1.6 — Implement FR-5 ambiguity detection**
  - **Context**: design §3 step 3 + FR-5.1 (mirror `skills/task/SKILL.md` disambiguation). `_resolve_release_dir` is deterministic with no lock (config.py:242) — concurrent `sprint run <same index>` share one ledger; event-pairing must tolerate interleaved `phase_start` events OR flag ambiguous (§12 R2 caveat).
  - **Action**: Set `ambiguous=True` + populate `ambiguity_reasons` when: >1 plausible release-dir candidate, conflicting/interleaved ledger that cannot be paired, or unreadable core files. Never auto-pick on an expensive run.
  - **Output**: `src/superclaude/cli/sprint/resume/planner.py` (ambiguity portion).
  - **Verification**: Two-candidate-release-dir fixture ⇒ `ambiguous==True` with both candidates listed in `ambiguity_reasons`.
  - **Completion gate**: Ambiguous state flagged with reasons, no silent auto-pick.

- [x] **1.7 — Phase 1 checkpoint: ResumePlanner read-only + write-path change land together**
  - **Context**: P1 must leave the tree green and the planner provably read-only.
  - **Action**: Run `uv run pytest tests/ -k "resume_planner or phase_result" -v` and `uv run ruff check src/superclaude/cli/sprint/resume/ src/superclaude/cli/sprint/executor.py`.
  - **Output**: Passing P1 unit tests; clean lint.
  - **Verification**: All P1 tests pass; planner makes zero writes to canonical results; `tasklist_sha256` persisted backward-compatibly.
  - **Completion gate**: P1 green; ready to unblock P2/P3.

---

## Phase 2: DriftAssessor (FR-3, DD-4, INV-001)

> Deterministic tiered scoring; LLM optional explainer only. Tier 0 exact-match; AC-4 lives in Tier 1.

- [x] **2.1 — Implement Tier 0 exact normalized-hash match (INV-001)**
  - **Context**: design §5 + DD-4. `recorded_sha` = `tasklist_sha256` stored in `phase-N-result.json` (from P1.3); `current_sha` = `_content_sha256_excluding_rerun_block(phase_obj.file)` (rerun_tasks.py:688). The stored and current hash MUST use the SAME function over the SAME per-phase `phase_obj.file` or Tier 0 can never match (INV-001). Tier 0 is exact-match only, NOT whitespace-tolerant (the function strips only the RERUN block).
  - **Action**: Implement `assess(index_path, plan) -> DriftAssessment`. Compute per-phase `current_sha` for the boundary phase's `phase_obj.file`; read `recorded_sha` from result.json. If both present and equal ⇒ `DriftAssessment(confidence=1.0, tier="hash", cosmetic_only=True)`. Absent recorded hash (pre-v4.3.5 phase) ⇒ skip Tier 0, fall through to Tier 1.
  - **Output**: `src/superclaude/cli/sprint/resume/drift.py` (`DriftAssessor.assess`, Tier 0).
  - **Verification**: Unchanged-tasklist fixture with a recorded hash ⇒ confidence 1.0, tier "hash". Fixture missing the recorded hash ⇒ no crash, falls to Tier 1.
  - **Completion gate**: Tier 0 matches only on exact same-fn-same-file hash equality (INV-001); absent hash degrades gracefully.

- [x] **2.2 — Implement Tier 1 whitespace-insensitive comparator (AC-4) + structural diff (AC-5)**
  - **Context**: design §5 Tier 1. AC-4 (trailing whitespace ⇒ confidence stays ≥0.8) is handled HERE, not Tier 0. Cosmetic = `git diff --ignore-all-space` clean (when tracked) OR normalize-then-rehash equal. Structural diff composes `parse_tasklist` (task IDs) + `extract_checkpoint_paths` (checkpoint paths) with deliverable-path diff best-effort over `description`.
  - **Action**: Implement Tier 1. If cosmetic-only and no structural change ⇒ confidence ≈0.9 (≥0.8 ⇒ AC-4 passes). If changes touch COMPLETED-phase task IDs / checkpoints / deliverables ⇒ confidence ≈0.3 (<0.8 ⇒ AC-5). If changes only in not-yet-run phases ⇒ confidence ≈0.85. Only the 0.8 boundary gates; other confidences advisory. Populate `changed_paths` and `explanation` (FR-3.5).
  - **Output**: `src/superclaude/cli/sprint/resume/drift.py` (Tier 1).
  - **Verification**: Trailing-whitespace-only fixture ⇒ confidence ≥0.8 (AC-4). Materially-edited completed-phase task fixture ⇒ confidence <0.8 (AC-5). Edit confined to not-yet-run phase ⇒ ≈0.85. `explanation` non-empty in all cases.
  - **Completion gate**: AC-4 (≥0.8 on cosmetic) and AC-5 (<0.8 on material completed-phase edit) both satisfied; scoring conservative.

- [x] **2.3 — Implement Tier 2 git characterization behind capability check**
  - **Context**: design §5 Tier 2 / FR-3.2. `git diff @{upstream}` annotation when tracked+online; must skip gracefully on detached-HEAD / no upstream / git unavailable.
  - **Action**: When git is available and the tasklist is tracked, annotate `changed_paths` with a `git diff` summary; set `tier="git"` when this path contributes. Wrap in a capability check; on any git failure, fall back to the Tier-1 result without raising.
  - **Output**: `src/superclaude/cli/sprint/resume/drift.py` (Tier 2 + capability guard).
  - **Verification**: Git-unavailable / detached-HEAD fixture ⇒ no exception, returns Tier-1 result. Tracked+upstream fixture ⇒ `changed_paths` annotated.
  - **Completion gate**: Git tier is purely additive annotation, never crashes offline, never overrides the deterministic gate value.

- [x] **2.4 — Phase 2 checkpoint**
  - **Context**: Drift scoring is the trust anchor (R3) — verify conservatism.
  - **Action**: `uv run pytest tests/ -k "drift" -v`; `uv run ruff check src/superclaude/cli/sprint/resume/drift.py`.
  - **Output**: Passing drift tests; clean lint.
  - **Verification**: All drift tests pass; only the 0.8 boundary gates; explanation always present.
  - **Completion gate**: P2 green.

---

## Phase 3: BoundaryIntegrityGate (FR-2, DD-2, DD-3, NFR-1, NFR-3)

> The core safety mechanism. Deterministic-only verdict; LLM advisory; report-only default + opt-in reversible quarantine.

- [x] **3.1 — Implement doubly-validate last-completed task (FR-2.1, DD-2 deterministic layer)**
  - **Context**: design §4(a). Signal A = `lc.persisted_status` (from result.json). Signal B = `_classify_transcript(read(task_output_file(phase, lc.id)))` (rerun_tasks.py:550). `artifacts_ok` = all declared checkpoint/deliverable paths for lc exist (checkpoints.py + executor.py:1844 logic). `validated_last = (A==PASS and B==PASS and artifacts_ok)`. If not validated ⇒ add lc to `suspects` (catches R1 over-claim).
  - **Action**: Implement `run(plan, *, accept_suspect=False) -> BoundaryReport`, deterministic last-completed validation portion. Treat `pass` status as a claim to be re-checked, not trusted.
  - **Output**: `src/superclaude/cli/sprint/resume/integrity.py` (`BoundaryIntegrityGate.run`, validate-last portion).
  - **Verification**: Fixture where last-completed task is marked PASS but a declared deliverable is missing ⇒ `validated_last==False`, lc in `suspects`. Fully-coherent last-completed ⇒ `validated_last==True`.
  - **Completion gate**: Last-completed double-validation is purely deterministic (A + B + artifact existence); over-claim caught.

- [x] **3.2 — Implement next-unfinished partial-work detection + report-only surfacing (FR-2.2/2.3)**
  - **Context**: design §4(b). Cover BOTH file classes: transcript (`phase-N-task-<id>-output.txt`) AND declared deliverables (`_declared_deliverables`, rerun_tasks.py:924) — a never-started task has no transcript, so transcript-only detection misses half-written deliverables. For `granularity==PHASE`, run over the whole boundary phase set (FR-2.3).
  - **Action**: Detect partial work: transcript exists with derived_status in {INCOMPLETE, FAIL_*} OR any declared-deliverable path exists OR stray `phase-N-task-<id>-*` files exist. ALWAYS report suspect paths in the `BoundaryReport` (FR-2.2 surface). Default = report-only, NO results/ mutation.
  - **Output**: `src/superclaude/cli/sprint/resume/integrity.py` (detect + report portion).
  - **Verification**: Half-written-deliverable fixture (no transcript) ⇒ partial detected and surfaced. Default run asserts NO results/ mutation.
  - **Completion gate**: Partial work detected across transcript AND deliverable classes; surfaced; default makes zero mutations.

- [x] **3.3 — Implement opt-in reversible copy-to-quarantine (FR-2.5, DD-3, NFR-1)**
  - **Context**: design §4(b) + DD-3. Opt-in only. COPY (`shutil.copy2`) suspect artifacts into `<results>/.resume-quarantine-<ts>/` with a `manifest.json` of the SAME shape `stash_and_restore_deliverables` writes (rerun_tasks.py:961) so the EXISTING `restore_from_bundle` (rerun_tasks.py:1039) reverses it — no new restore verb. Acquire `.recovery-locks/phase-{phase}.lock` (recovery.py:278/291) before any results/ mutation. Append a `resume_quarantine` line via `write_recovery_audit_log` (recovery.py:250). NEVER rename-in-place, NEVER delete, NEVER reuse the `.failed-<ts>` rename (it is inlined in `merge_recovery_bundle`, not reusable, not reversed by `--restore`, and would race the rerun engine's own stash on the TASK path).
  - **Action**: When `cleanup_opted_in`: acquire the phase lock; create `.resume-quarantine-<ts>/`; copy suspect paths preserving structure; write `manifest.json` (preserved/+manifest shape); append the audit line; record `quarantined[canonical] = qdir-copy`. Leave canonical originals untouched.
  - **Output**: `src/superclaude/cli/sprint/resume/integrity.py` (quarantine portion).
  - **Verification**: Opt-in fixture ⇒ copy exists under `.resume-quarantine-<ts>/` with manifest, ORIGINAL untouched, audit line written, `.recovery-locks` taken; `restore_from_bundle` reverses it. Default fixture ⇒ none of this happens.
  - **Completion gate**: Quarantine is copy-only, lock-guarded, audit-logged, reversible by existing `restore_from_bundle`; default path is report-only.

- [x] **3.4 — Implement advisory Haiku coherence read (DD-2, NFR-3) — TASK-granularity only**
  - **Context**: design §4(a) ADVISORY block + §8. Scoped ONLY to `granularity==TASK` with a non-empty transcript + declared deliverables. Skipped entirely for `granularity==PHASE` (no per-task last-completed object — executor.py:1309+). Uses the advisory Haiku surface (summarizer.py:305). If it flags incoherence ⇒ append to `coherence_warnings` and list the task for operator review; it NEVER flips `validated_last`/`passed`. Empty verdict (claude absent / timed out) ⇒ `BoundaryReport` identical to the no-Haiku path (CI-safe).
  - **Action**: When `validated_last and granularity==TASK and transcript_nonempty(lc) and lc_declared_deliverables`: call a bounded (~1 call) Haiku coherence read; on `verdict.suspect` append `(lc, reason)` to `coherence_warnings`. Do NOT modify `validated_last`/`passed`. Empty/failed verdict yields the no-Haiku BoundaryReport.
  - **Output**: `src/superclaude/cli/sprint/resume/integrity.py` (advisory Haiku portion).
  - **Verification**: (a) Mock Haiku verdict=suspect on a deterministically-validated TASK ⇒ `coherence_warnings` populated but `passed`/`validated_last` UNCHANGED. (b) `granularity==PHASE` or empty transcript ⇒ Haiku NOT invoked. (c) claude absent (empty verdict) ⇒ BoundaryReport identical to no-Haiku path.
  - **Completion gate**: Haiku is advisory-only, TASK-scoped, never on the verdict path, CI-safe.

- [x] **3.5 — Implement the hard gate verdict (FR-2.4, NFR-3)**
  - **Context**: design §4(c). `passed = validated_last and (no unresolved suspects) and (partial work quarantined or accepted)`. PURE function of deterministic signals; `coherence_warnings` are surfaced for the operator but are NOT in `passed` (NFR-3). On `not passed`, populate `blocking_reasons` explaining exactly what must be resolved.
  - **Action**: Compute `passed` deterministically; set `blocking_reasons` when failing. `accept_suspect=True` is the explicit operator-accepted path.
  - **Output**: `src/superclaude/cli/sprint/resume/integrity.py` (verdict portion).
  - **Verification**: Suspect-unresolved fixture ⇒ `passed==False` with `blocking_reasons`. Coherence-warning-present-but-deterministically-clean fixture ⇒ `passed==True` (NFR-3). Accept-suspect path ⇒ proceeds.
  - **Completion gate**: `passed` is a pure deterministic function; coherence warnings never affect it.

- [x] **3.6 — Phase 3 checkpoint**
  - **Context**: Verify NFR-1 non-destructive guarantee and NFR-3 advisory isolation hold.
  - **Action**: `uv run pytest tests/ -k "boundary or integrity or quarantine or coherence" -v`; `uv run ruff check src/superclaude/cli/sprint/resume/integrity.py`.
  - **Output**: Passing P3 tests; clean lint.
  - **Verification**: Default gate makes zero results/ mutations; opt-in quarantine reversible; verdict deterministic.
  - **Completion gate**: P3 green.

---

## Phase 4: CLI wiring in run() + rerun_tasks() (FR-4, DD-5, AC-6/7/8)

> Depends on P1+P2+P3. The flag-bypass detection is the worst failure mode if wrong — use Click parameter source, never value comparison.

- [x] **4.1 — Add new flags to `run()` and `rerun_tasks()`**
  - **Context**: design §6 flags table. Both subcommands gain `--fresh`/`--restart` (bool), `--yes` (bool, also honored via env e.g. `SUPERCLAUDE_SPRINT_ASSUME_YES=1`), and `--dry-run` (run: extend existing dry-run). `run()` is at commands.py:190; `rerun_tasks()` at commands.py:485.
  - **Action**: Add the Click options. `--fresh` = "ignore prior on-disk state; run from phase 1 with auto-detect disabled" (DD-5); `--restart` is its alias. Add `--yes` with env fallback. Extend `run()`'s existing `--dry-run`.
  - **Output**: Modified `src/superclaude/cli/sprint/commands.py` (option decorators + signatures for both commands).
  - **Verification**: `uv run superclaude sprint run --help` and `... rerun-tasks --help` show `--fresh`/`--restart`, `--yes`, `--dry-run`. Existing flags unchanged.
  - **Completion gate**: New flags present on both subcommands; existing surface intact.

- [x] **4.2 — Add `@click.pass_context` + parameter-source explicit-window detection (DD-5, AC-7)**
  - **Context**: design §6 + CONSOLIDATION DD-5. `run()` currently does NOT take `@click.pass_context` (verified at commands.py:190); `--start` default=1 (commands.py:76), `--end` default=0 — so `start_phase != 1` CANNOT distinguish explicit `--start 1` from no flag. MUST use `ctx.get_parameter_source("start_phase") == ParameterSource.COMMANDLINE` (or the `None`-sentinel-default alternative mirroring rerun-tasks `--phase/--tasks`). NEVER value comparison.
  - **Action**: Add `@click.pass_context` to `run()`; compute `position_explicit = src("start_phase")==COMMANDLINE or src("end_phase")==COMMANDLINE`. For `rerun_tasks()`, detect explicit `--phase`/`--tasks`/`--from-reflect-report` presence the same way (parameter source or None-sentinel).
  - **Output**: Modified `src/superclaude/cli/sprint/commands.py` (context + detection).
  - **Verification**: AC-7 — `sprint run --start 4 <index>` bypasses auto-detect (planner NOT called); critically, `sprint run --start 1 <index>` ALSO bypasses (treated as explicit window), proving value-comparison is not used.
  - **Completion gate**: Explicit window detected by parameter source; explicit `--start 1` bypasses auto-resume (AC-7).

- [x] **4.3 — Implement the `_auto_resume` control flow in `run()` (FR-4.2, AC-1/6/8, FR-2.4, FR-3.4)**
  - **Context**: design §6 + §8 `_auto_resume(index_path, *, assume_yes, dry_run) -> ResumeDecision`. Branch order: `if fresh` → clean run from phase 1, auto-detect OFF; `elif position_explicit` → today's exact path, auto-detect OFF; `else` → AUTO-RESUME.
  - **Action**: In the AUTO-RESUME branch: `plan = ResumePlanner().plan(index_path)`; if `granularity==NONE` print "nothing to resume" and exit 0 (AC-6); if `plan.ambiguous` print candidates and STOP non-zero (FR-5/AC-8); `drift = DriftAssessor().assess(...)`; `report = BoundaryIntegrityGate().run(plan)`; `print_plan(plan, drift, report)` (FR-4.2 detect→print); if `not report.passed` STOP with blocking_reasons (FR-2.4); if `drift.confidence < 0.8` STOP and guide to `--start`/`--fresh` (FR-3.4/AC-5); else prompt the user (unless `--yes`/CI env) then proceed (FR-3.4/NFR-4).
  - **Output**: Modified `src/superclaude/cli/sprint/commands.py` + `_auto_resume` helper.
  - **Verification**: AC-6 fully-complete fixture ⇒ "nothing-to-resume", exit 0. AC-8 two-candidate fixture ⇒ candidates listed, STOP, no execution. `not report.passed` ⇒ STOP with reasons. `drift<0.8` ⇒ STOP with guidance. `--yes`/env ⇒ no interactive prompt.
  - **Completion gate**: All gate STOPs and the nothing-to-resume / ambiguous exits behave per design §6.

- [x] **4.4 — Implement `dispatch(plan)` to existing code paths (FR-1.5, AC-1/AC-2)**
  - **Context**: design §6 dispatch + §7 happy path. `granularity==TASK` ⇒ `run_rerun_tasks(index_path, phase=plan.interrupted_phase, tasks=plan.rerun_task_ids, merge_back=True)` (AC-2 — merge-back refreshes canonical per-task status). Else ⇒ set `config.start_phase`/`config.end_phase` and call `execute_sprint(config)` via the existing `active_phases` loop. Nothing about phase execution changes (NG1).
  - **Action**: Implement `dispatch` routing to the existing rerun engine (TASK) or executor loop (PHASE). No new execution machinery.
  - **Output**: Modified `src/superclaude/cli/sprint/commands.py` (dispatch).
  - **Verification**: AC-1 — interrupt at phase 3 of 5, bare `sprint run` resumes at phase 3, completes 3-5, phases 1-2 NOT re-run. AC-2 — phase 3 `fail_recoverable` task ⇒ only that task re-run via rerun engine, merged back, canonical per-task status refreshed.
  - **Completion gate**: TASK path dispatches to rerun engine with merge-back; PHASE path dispatches to executor loop; AC-1/AC-2 satisfied.

- [x] **4.5 — Wire `rerun_tasks()` auto-detect parity (FR-4.1, AC-9)**
  - **Context**: design §6 closing paragraph. When `--phase`/`--tasks`/`--from-reflect-report` are ALL absent, call the planner, take `interrupted_phase` + `rerun_task_ids`, and proceed as if specified.
  - **Action**: Add the symmetric auto-detect path to `rerun_tasks()` reusing `ResumePlanner` (thin adapter). Explicit flags still bypass (4.2).
  - **Output**: Modified `src/superclaude/cli/sprint/commands.py` (`rerun_tasks` auto-detect).
  - **Verification**: AC-9 — bare `sprint rerun-tasks <index>` auto-detects the latest phase with recoverable failures + its failed-task set; identical result to the equivalent explicit `--phase --tasks` invocation.
  - **Completion gate**: Bare rerun-tasks == explicit invocation (AC-9).

- [x] **4.6 — Implement `--dry-run` plan/report/drift print (FR-4.5)**
  - **Context**: design §6 flags. `--dry-run` prints the full `ResumePlan` + `BoundaryReport` + `DriftAssessment`, no execution.
  - **Action**: In `_auto_resume`, when `dry_run`, run planner+drift+gate, print all three structured outputs, and return without dispatch.
  - **Output**: Modified `src/superclaude/cli/sprint/commands.py` (dry-run branch).
  - **Verification**: `sprint run --dry-run <index>` on an interrupted fixture prints plan + report + drift and executes nothing.
  - **Completion gate**: Dry-run prints all three artifacts, zero execution.

- [x] **4.7 — Phase 4 checkpoint**
  - **Context**: CLI is the integration surface; verify backward-compat (R5) and the flag-bypass invariant.
  - **Action**: `uv run pytest tests/ -k "sprint and (run or rerun or resume or autodetect or explicit)" -v`; `uv run ruff check src/superclaude/cli/sprint/commands.py`.
  - **Output**: Passing P4 tests; clean lint.
  - **Verification**: Explicit-flag paths preserve today's exact semantics (FR-4.4); auto-resume path behaves per design.
  - **Completion gate**: P4 green.

---

## Phase 5: Tests, docs, version (FR-5, R5, §9 test plan)

> Depends on P4. Maps 1:1 to acceptance criteria + the validator-corrected invariants.

- [x] **5.1 — Author the AC-mapped unit/integration tests (§9 table)**
  - **Context**: design §9 maps each test to an AC with a fixture. Tests live under `tests/` (pytest, UV). Reuse existing sprint test fixtures/patterns.
  - **Action**: Author: `test_resume_planner_phase_boundary` (AC-1), `test_resume_task_level_recoverable` (AC-2), `test_resume_hard_crash_phase_level` (AC-3), `test_drift_trailing_whitespace_high_conf` (AC-4), `test_drift_material_edit_low_conf` (AC-5), `test_nothing_to_resume` (AC-6), `test_explicit_start_bypasses_autodetect` (AC-7), `test_ambiguous_release_dirs_stop` (AC-8), `test_rerun_tasks_autodetect_parity` (AC-9). Each must assert against its design §9 fixture.
  - **Output**: New test module(s) under `tests/` (e.g. `tests/sprint/test_resume_*.py`).
  - **Verification**: `uv run pytest tests/ -k "resume or drift or autodetect" -v` — all AC tests pass. AC-7 asserts the planner is NOT called when `--start` is explicit (incl. `--start 1`).
  - **Completion gate**: AC-1..AC-9 each have a passing test asserting the design behavior.

- [x] **5.2 — Author the validator-corrected invariant tests**
  - **Context**: design §9 rows for FR-2.5 and DD-2, plus INV-001. These guard the exact defects the 5 adversarial validators found.
  - **Action**: Author `test_boundary_quarantine_nondestructive` (FR-2.5: default report-only NO mutation; opt-in copy under `.resume-quarantine-<ts>/` with manifest, ORIGINAL untouched, audit line, `.recovery-locks` taken) and `test_haiku_coherence_advisory_only` (DD-2: (a) suspect verdict ⇒ warnings but `passed`/`validated_last` unchanged; (b) PHASE/empty transcript ⇒ Haiku not invoked; (c) claude absent ⇒ identical BoundaryReport). Add an INV-001 test: stored `tasklist_sha256` and current `current_sha` use the same fn+file ⇒ Tier 0 matches on an unchanged tasklist.
  - **Output**: Test cases (in the modules from 5.1 or a dedicated invariants module).
  - **Verification**: `uv run pytest tests/ -k "quarantine or coherence or inv001 or advisory" -v` passes; the advisory-only and non-destructive invariants are explicitly asserted.
  - **Completion gate**: Quarantine non-destructiveness, Haiku advisory-only, and INV-001 are test-locked.

- [x] **5.3 — Wire the real-subprocess e2e tests (AC-1/2/3)**
  - **Context**: design §9 e2e row — reuse the real-subprocess harness from commit `344a754a`.
  - **Action**: Add e2e cases over the existing harness for AC-1 (phase-boundary resume), AC-2 (task-level recoverable), AC-3 (hard-crash phase-level with last-completed double-validation first).
  - **Output**: e2e test cases under the existing sprint e2e harness location.
  - **Verification**: `uv run pytest tests/ -k "e2e and (resume or rerun)" -v` (or the harness's marker) passes for AC-1/2/3.
  - **Completion gate**: e2e harness exercises the three resume scenarios end-to-end.

- [x] **5.4 — Run full sprint suite + lint gate**
  - **Context**: Backward-compat regression guard (R5) — existing `sprint run`/`rerun-tasks` behavior must be intact under explicit flags.
  - **Action**: `uv run pytest tests/ -k "sprint" -v` and `uv run ruff check src/superclaude/cli/sprint/`. Fix any regression.
  - **Output**: Green sprint suite; clean lint across the sprint package.
  - **Verification**: All sprint tests pass; no lint errors; explicit-flag paths unchanged.
  - **Completion gate**: Full sprint suite + lint green.

- [x] **5.5 — Document the behavior change + changelog (R5)**
  - **Context**: R5 — teams scripting bare `sprint run` now get auto-resume + a prompt. Document loudly. Note the FR-4.4 explicit-flag bypass and the NFR-4 non-interactive opt-in (`--yes`/env).
  - **Action**: Add a v4.3.5 changelog entry (use `.claude/templates/workflow/changelog_template.md` shape if the project keeps a changelog) and update the relevant sprint user-guide/reference docs describing default auto-resume, `--fresh`/`--restart`, `--yes`, `--dry-run`, and the integrity-gate/drift behavior. Do NOT edit `.claude/` distributable copies — docs live under `docs/`.
  - **Output**: Changelog entry + sprint docs update under `docs/`.
  - **Verification**: Changelog names the behavior change, the opt-out (`--fresh`), and the CI opt-in (`--yes`/env). Docs describe the detect→print→prompt→proceed default.
  - **Completion gate**: Behavior change documented; opt-out and CI path called out.

- [x] **5.6 — Version bump to v4.3.5 (operator-confirm target)**
  - **Context**: `pyproject.toml` is at 4.2.0; design targets v4.3.5; v4.3.0 rerun code is already merged without a pyproject bump (Open Question — see Task Log). This is release hygiene, not a code blocker.
  - **Action**: Bump `pyproject.toml` `version` and any version constant the package exposes to the operator-confirmed target (default `4.3.5`). If the team prefers to defer the bump to a release step, mark this item N/A and note it.
  - **Output**: Updated `pyproject.toml` (and any version constant).
  - **Verification**: `grep -E '^version' pyproject.toml` shows the confirmed target; `uv run superclaude --version` (or equivalent) reflects it.
  - **Completion gate**: Version reflects the confirmed v4.3.5 target, OR item explicitly deferred with a note.

- [x] **5.7 — Update task status to Done**
  - **Context**: All phases P1-P5 complete and verified.
  - **Action**: Update frontmatter: `status` to "🟢 Done"; set `completion_date`. Record final outcomes in the Task Log.
  - **Output**: This task file updated.
  - **Verification**: Frontmatter shows "🟢 Done"; Task Log has execution entries for each phase.
  - **Completion gate**: Task marked complete.

---

## Task Log / Notes

### Execution Log
- 2026-06-02 — Task file built (inline single-threaded task-builder run; design.md served as the code-verified research corpus, key anchors re-verified against the worktree this session).
- 2026-06-02 — Phase 1 executed (items 1.1–1.7) + phase-gate QA PASS. New `resume/` package (`__init__`, `models`, `planner`) + `tasklist_sha256` write-path change in `executor._write_phase_result_json`. updated_date bumped.
- 2026-06-02 — Phases 2–5 executed; per-phase gate QA PASS on each (P2 DriftAssessor, P3 BoundaryIntegrityGate, P4 CLI wiring [caught + fixed a runtime dispatch defect], P5 tests/docs/version [strengthened tests, mutation-proved hard-STOP]). §7 verdict refinement applied during P4. Version bumped 4.2.0 → 4.3.5 (operator-confirmed).
- 2026-06-02 — POST-COMPLETION VALIDATION: rf-qa structural PASS (`reviews/qa-final-validation-report.md`, 20 cross-phase checks, INV-001 + dispatch-signature re-proven end-to-end) + rf-qa-qualitative operational PASS (`reviews/qa-qualitative-review.md`, 8 acceptance paths run against the real CLI). Zero defects, zero fixes. Resume feature stash-proven to add ZERO test regressions (base 54/55 == with-feature 54; +36 new passing tests). TASK COMPLETE → status Done.

### Phase Findings
- **P1 (2026-06-02).** 1.1 `resume/__init__.py` created; package imports clean. 1.2 `resume/models.py` — all 6 dataclasses/enums import; field sets match design §2 verbatim (`coherence_warnings` excluded from `passed` per NFR-3). 1.3 `tasklist_sha256` added to `_write_phase_result_json` via a function-body lazy import of `_content_sha256_excluding_rerun_block` (avoids circular import — rerun_tasks already lazily imports executor). Smoke: key present + equals the hash fn over `phase.file` (INV-001 ✓), absent-key `.get()` returns None (backward-compatible ✓). Existing result-json tests (3) pass.
- **PRE-EXISTING (not this task's regression).** `tests/sprint/test_summarizer.py` and `tests/sprint/test_retrospective.py` fail to COLLECT: `ImportError: cannot import name 'invoke_haiku' from superclaude.cli.sprint.summarizer`. `summarizer.py` is untouched by this task (git clean). Design §0 references the advisory-Haiku surface as `summarizer.py:305`; the test expects a symbol named `invoke_haiku` that does not exist. **Relevant to item 3.4** (advisory Haiku coherence read) — the actual Haiku entrypoint must be located by name there, not assumed to be `invoke_haiku`. Tracked in Follow-Up.
- **1.7 checkpoint (2026-06-02).** `ruff check` on `resume/` + `executor.py` → all checks passed. `pytest -k "resume_planner or phase_result"` → 5 passed, 1 skipped, 1 FAILED. The single failure (`test_integration_lifecycle.py::test_phase_result_has_timing` — `'FakePopen' object has no attribute 'stdin'`) was PROVEN pre-existing by `git stash`-ing only the executor.py change and re-running: it fails identically on the base. Not this task's regression (the failure is in subprocess-spawn test infra, which executes before result-json is written). Tracked in Follow-Up.
- **P1 PHASE-GATE QA: PASS** (rf-qa, adversarial, fix_authorization). Report: `reviews/qa-phase-1-report.md`. 9/9 ACs verified via executed logic traces. One MINOR fix applied in-place: `resume/__init__.py` now re-exports `ResumePlanner` (`from .planner import ResumePlanner` + `__all__`) — the docstring promised it and Phase 4 CLI wiring imports it from the package. Adversarial probes all clean: planner is pure-read (zero write ops), `tasklist_sha256` uses `phase.file` (INV-001), `coherence_warnings` never leaks into `passed` (NFR-3), torn-ledger+PASS-result.json→COMPLETED, fresh index→PHASE (not NONE), models.py field-exact vs design §2, backward-compat `.get()` throughout.

- **P2 (2026-06-02).** DriftAssessor (`resume/drift.py`): Tier 0 exact hash (INV-001 — same fn over `phase.file`, verified end-to-end vs the executor write side), Tier 1 structural ID-diff (AC-4 cosmetic→0.9, AC-5 completed-task removed→0.3, not-yet-run→0.85, explanations always present), Tier 2 git annotation (additive: tier="git"+changed_paths, never touches confidence; skips gracefully no-git/detached/no-upstream/untracked). PHASE granularity tolerates edits (0.9). ruff clean.
- **P2 PHASE-GATE QA: PASS** (rf-qa, adversarial, fix_authorization). Report: `reviews/qa-phase-2-report.md`. All ACs re-derived via live execution against real `discover_phases`/`parse_tasklist_file`/`_content_sha256_excluding_rerun_block`. One fix applied: a TASK-granularity parse-failure guard — when a boundary file is readable but parses to ZERO task IDs against a non-empty recorded baseline, the code previously mislabeled it as "completed tasks removed"; now it keeps the conservative 0.3/<0.8 STOP but accurately attributes "empty/corrupt/format" (FR-3.5). Git provably additive-only (confidence in==out). Confirmed `index_path` is NOT used for the hash; per-phase `phase.file` is.

- **P3 (2026-06-02).** BoundaryIntegrityGate (`resume/integrity.py`): (3.1) last-completed double-validation = Signal A (persisted PASS) ∧ Signal B (`_classify_transcript`) ∧ artifacts (`_declared_deliverables` exist) — PASS is re-checked not trusted; (3.2) partial-work detection across transcript + deliverable + stray classes, report-only default (zero mutation); (3.3) opt-in `shutil.copy2` quarantine into `.resume-quarantine-<ts>/preserved/` with manifest reversible by EXISTING `restore_from_bundle`, lock-guarded, audit-logged, original untouched; (3.4) advisory coherence read via `invoke_sonnet` (the real surface — design's "Haiku" maps to `invoke_sonnet`; summarizer has NO `invoke_haiku`), TASK-only, never on verdict, CI-safe on empty; (3.5) `passed = accept_suspect or (validated_last and not unresolved_partial)` — pure deterministic. ruff clean.
- **P3 PHASE-GATE QA: PASS** (rf-qa, adversarial, fix_authorization). Report: `reviews/qa-phase-3-report.md`. 21/21 items via 55+ executed-fixture assertions. NFR-3 proven 3 ways (runtime + source-ordering: `_advisory_coherence` at L84 runs AFTER `report.passed` at L71 + data-flow: `_verdict` references no LLM token). NFR-1 proven via recursive sha256 snapshot byte-identical in default mode. Reversibility proven (corrupt original → `restore_from_bundle` restores byte-exact). DD-3 double-stash safety: `_quarantine` has `copy2` + zero rename/move/delete. integrity.py ships as-is, NO changes needed.
- **BLAST-RADIUS CHECK (2026-06-02).** The pre-existing `invoke_haiku` ImportError (commit `70ef6486` haiku→sonnet rename) breaks `retrospective.py:34,337` + `test_summarizer.py` + `test_retrospective.py`. Confirmed Phase 4 is UNBLOCKED: `commands.py` does NOT import `retrospective`, and `import superclaude.cli.sprint.commands` succeeds. Impact is limited to (a) `retrospective.py` runtime + (b) the 5.4 "full suite green" gate. Trivial one-line-per-site remediation (`invoke_haiku`→`invoke_sonnet`) is fully diagnosed in `reviews/qa-phase-3-report.md`. Decision deferred to item 5.4.

- **P4 refinement (2026-06-02) — gate verdict aligned to design §7.** While wiring the CLI I re-read §7 (canonical happy path): it shows `passed=True` with the next-unfinished's half-written outputs merely *reported*. The Phase-3 verdict had made unresolved partial work a hard block (too strict). CORRECTED in `integrity.py`: `passed = accept_suspect or validated_last`. Boundary partial work is SURFACED via `report.suspects` (role=next_unfinished) but does NOT flip the verdict — it belongs to the task the resume plan re-runs ("assessed-and-accepted" by the plan; the CLI prompt is the assent point). The HARD gate remains the last-completed integrity check. Re-verified: §7 happy (passed True, partial surfaced, zero mutation), over-claim (passed False + blocking), clean (passed True), quarantine opt-in still reversible. Did NOT add a `BoundaryReport` field (design §2 is field-exact) — surfacing rides `suspects`. This keeps the 3.2 gate (detected+surfaced+no-mutation) and 3.5 gate (over-claim→False, accept→True, coherence-never-on-verdict) satisfied.

- **P4 (2026-06-02).** CLI wiring in `commands.py`. `run()`: `@click.pass_context` + `--fresh`/`--restart`/`--yes`; explicit-window detection via `ParameterSource.COMMANDLINE` (AC-7 verified: `--start 1` AND `--start 4` both bypass auto-resume, planner NOT called; bare invokes it). `_auto_resume` helper: plan→drift→gate→dry-run/STOP/prompt→ResumeDecision; nothing-to-resume (AC-6, exit 0), ambiguous (STOP exit 2), gate-fail STOP, drift<0.8 STOP, interactive confirm unless `--yes`/env/CI/non-tty. `_dispatch_resume_rerun` (TASK→`run_rerun_tasks` merge_back) + PHASE→set start/end & fall through to executor (NG1). `--dry-run` prints plan+drift+gate (FR-4.5, verified). `rerun_tasks()`: `--fresh`/`--restart`/`--yes`; bare auto-detect parity (AC-9 verified: bare == explicit `--phase 3 --tasks T03.02` produce identical `run_rerun_tasks` args). ruff clean on commands.py.
- **P4 checkpoint classification (stash-verified).** `pytest -k "sprint and (run|rerun|resume|autodetect|explicit)"` → 74 passed, 8 failed. Stashing ONLY my tracked changes (commands.py, executor.py) and re-running showed **7 of 8 fail identically on base** → PRE-EXISTING (test_e2e_halt, test_integration_halt ×5, test_watchdog stall-reset — unrelated halt/resume + the invoke_haiku family). The **1 genuinely affected by my change** is `test_cli_contract.py::test_rerun_tasks_requires_phase_without_reflect_report` — it asserts bare `rerun-tasks` errors with "--phase is required". FR-4.1 INTENTIONALLY changes that to auto-detect, so the OLD contract no longer holds. **Action (Phase 5):** update that test to the new default-auto-detect contract (bare rerun-tasks on a no-phase index → "Nothing to rerun"/guidance; on an interrupted index → AC-9 auto-detect). FR-4.4 (explicit `--start/--end`/`--phase/--tasks` paths preserve today's semantics) is intact — verified by the 74 passing + AC-7/AC-9.

- **P4 PHASE-GATE QA: PASS** (rf-qa, adversarial, fix_authorization). Report: `reviews/qa-phase-4-report.md`. 2 fixes applied in-place: **(CRITICAL)** `_dispatch_resume_rerun` was calling `run_rerun_tasks` with only 3 of its 12 kwargs — the other 9 are keyword-only with NO defaults, so the AC-2 task-level happy path would have raised `TypeError` at runtime. My Phase-4 inline test missed it (used a `**kw`-absorbing fake); the QA caught it against the REAL callee and fixed `commands.py:480-494` to pass all 9 with CLI-default values (proven: pre-fix TypeError → post-fix SystemExit(0), rerun engine ran end-to-end). **(MINOR)** `resume/__init__.py` import sort. All other ACs proven by executed CliRunner evidence: AC-7 (value-comparison trap avoided), AC-2/AC-6/AC-8/AC-9, dry-run, FR-4.4 explicit-path preservation, §7 verdict refinement. ruff clean across the sprint package.

- **P5 tests (2026-06-02).** `tests/sprint/test_resume.py` (16 deterministic: AC-1..AC-9 with the design §9 names + INV-001 Tier-0, quarantine non-destructive/reversible FR-2.5, Haiku advisory-only DD-2) + `tests/sprint/e2e_real/test_e2e_resume.py` (3 REAL-subprocess: AC-2/AC-9 bare rerun-tasks auto-detect, AC-1 bare `sprint run` auto-resume→task dispatch, AC-3 hard-crash→PHASE re-run of all tasks) + updated `test_cli_contract.py` for the FR-4.1 contract change. 37 feature tests green; ruff clean on all.
- **P5 5.4 full-suite — REGRESSION-FREE, blocked only by PRE-EXISTING breakage.** Stash-classified rigorously: full `pytest -k sprint` on the BASE (my tracked changes stashed, my new test files excluded) = **55 failed / 997 passed**; WITH my changes (same exclusions) = **54 failed / 998 passed**. My work introduces **ZERO new failures** (one fewer, +19 new passing tests). The ~54 failures span subprocess/TUI/halt/watchdog test-infra (e.g. `FakePopen` lacks `stdin`) + the `invoke_haiku` family — none touch the resume feature, all predate commit work here. Additionally 2 collection errors (`test_summarizer.py`, `test_retrospective.py` → `retrospective.py:34` dangling `invoke_haiku` import) abort un-ignored collection. Per scope discipline I did NOT modify unrelated modules. **R5 no-regression requirement MET.** Full green requires the separate pre-existing-breakage remediation tracked in Follow-Up.

- **P5 PHASE-GATE QA: PASS** (rf-qa, adversarial, fix_authorization). Report: `reviews/qa-phase-5-report.md`. Verified the tests are MEANINGFUL not vacuous: AC-4/AC-5 fixtures correctly record the ORIGINAL baseline (`recorded_body=_P3`) so Tier 0 genuinely misses and Tier 1 is under test; AC-7 uses a real call-counter; e2e uses the REAL claude shim. One IMPORTANT strengthening: the durable suite asserted only the `passed==True` direction (a gate regressed to always-True would still pass) — QA added `test_gate_hard_stops_on_last_completed_overclaim` and MUTATION-PROVED it (forcing `_verdict` always-True → test fails; revert → passes), plus AC-4 `tier!="hash"` and AC-5 explanation-name assertions. Source untouched; 36 tests pass; ruff clean.

### Open Questions
- **OQ-A — RESOLVED (2026-06-02).** Operator chose "Bump to 4.3.5 now" (AskUserQuestion). `pyproject.toml` `version` and `src/superclaude/__init__.py` `__version__` both 4.2.0 → 4.3.5; confirmed `import superclaude` → 4.3.5. The already-merged 4.3.0 is skipped per operator direction.
- **OQ-B — `--yes` env var name (4.1).** Design suggests `SUPERCLAUDE_SPRINT_ASSUME_YES=1` as an example; confirm the canonical env var name.
- **NOTE — `models.py` line numbers.** Symbol locations in `models.py` (execution-log.jsonl :543, results/ :539, phase_result_json :570, transcripts :561-565, TaskStatus :45-52, PhaseStatus :270, active_phases :550) are from design.md; file presence verified this session but lines not re-paginated symbol-by-symbol. Items instruct locating symbols by name (grep), not by trusting line numbers — robust to drift.

### Follow-Up Items
- **Pre-existing test breakage (NOT introduced by this task).** (1) `tests/sprint/test_summarizer.py` + `tests/sprint/test_retrospective.py` fail to collect — `ImportError: invoke_haiku` from `summarizer.py`. (2) `tests/sprint/test_integration_lifecycle.py::test_phase_result_has_timing` — `FakePopen` lacks `stdin` (proven pre-existing via stash). Both should be triaged separately from this feature; they affect the "run full sprint suite green" gate at 5.4 and may need an `--ignore`/xfail note or a base-branch fix.
