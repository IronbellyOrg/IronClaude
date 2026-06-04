---
title: "Auto-Resume as Default for Sprint Pipeline"
feature_slug: sprint-auto-resume-default
domain: architecture
status: requirements
adversarial_status: consolidated-direct
convergence_score: null
created: 2026-06-02
source_brief: ./seed-brief.md
target_version: v4.3.5
---

# Merged Requirements: Auto-Resume as the Default for `sprint run` / `rerun-tasks`

> **Note on process:** the major design forks were resolved directly by the user during
> Socratic dialogue (granularity, default UX, staleness behavior, scope). Rather than fire
> a divergent 3-model adversarial debate to re-litigate settled decisions, this spec
> consolidates those decisions and applies an internal red-team lens (see §7 Risks). If the
> team later wants competing implementation strategies debated, run
> `/sc:adversarial --source .dev/brainstorms/20260602-sprint-auto-resume-default/merged-requirements.md --generate spec`.

## 1. Summary

Make resume the **default behavior** of the sprint pipeline. Running bare
`superclaude sprint run <index>` (or bare `superclaude sprint rerun-tasks <index>`) shall
auto-detect where the previous run was interrupted from on-disk state and execute as if the
operator had supplied the correct `--start/--end` (and, for the boundary phase, the correct
per-task) options. Explicit flags continue to work and disable auto-detection.

The defining difference from `/task` auto-resume: sprint phases are **not idempotent**, so
the resume **seam** (last completed task + next unfinished task) is treated as *suspect* and
must pass an integrity gate before new work is layered on top.

## 2. Goals / Non-Goals

**Goals**
- G1. Zero-flag resume as the default for `sprint run` and `sprint rerun-tasks`.
- G2. Reconstruct the resume plan `(start_phase, end_phase, boundary_task_disposition)` from
  existing artifacts — no new heavyweight state store.
- G3. A **resume-boundary integrity gate** that re-validates the last completed task and
  cleans/assesses the next (partially done) task before resuming.
- G4. A **semantic staleness assessment** (not a brittle byte-hash) that scores how safe it
  is to resume against a possibly-edited tasklist/source, ideally diffed vs. the git remote.
- G5. Visible-by-default UX: detect → print plan → proceed; with `--fresh` opt-out.
- G6. Reuse the v4.3.0 rerun engine (classifiers, per-task status, merge-back, SHA-guard).

**Non-Goals**
- NG1. Changing how phases themselves execute (executor loop semantics unchanged).
- NG2. Making phases idempotent or rewriting the checkpoint system.
- NG3. Auto-resuming across *different* tasklist files / release dirs without explicit input.
- NG4. Removing or deprecating `--start`/`--end`/`--phase`/`--tasks` (all retained).

## 3. Functional Requirements

### FR-1 — Resume Planner (new component)
A read-only planner that, given an `index_path` and resolved release dir, returns a
`ResumePlan`:
- FR-1.1 Enumerate completed phases by presence of `results/phase-N-result.json`.
- FR-1.2 Identify the **interrupted phase**: the highest `phase_start` in
  `execution-log.jsonl` with no matching `phase_complete`, OR the lowest phase whose
  `phase-N-result.json` carries a non-passing `PhaseStatus`/`fail_recoverable` tasks.
- FR-1.3 Compute `start_phase` = interrupted phase (or first incomplete phase);
  `end_phase` = existing auto-last behavior unless overridden.
- FR-1.4 For the boundary phase with per-task data, classify each task into
  `{completed, last_completed, next_unfinished, pending}` using `phase-N-result.json`
  `task_results[]` and, where result JSON is absent, the transcript classifiers
  `discover_failed_tasks_from_transcripts` / `_classify_transcript` (`rerun_tasks.py`).
- FR-1.5 Emit a `ResumePlan` that downstream code can execute via the **existing** code
  paths: phase-level → normal executor loop with computed `start/end`; task-level →
  `rerun-tasks` engine with computed phase + failed-task set.
- FR-1.6 **No prior run** ⇒ plan == fresh `--start 1`. **Fully complete sprint** ⇒ plan ==
  `nothing-to-resume` (print message; exit 0; suggest `--fresh` to redo).

### FR-2 — Resume-Boundary Integrity Gate (new component) — *the core safety mechanism*
Before any resumed work executes:
- FR-2.1 **Last completed task — deep suspicion validation.** Re-verify the last
  confirmed-completed task's declared deliverables/checkpoints actually exist and are
  coherent (checkpoint file existence per `checkpoints.py`, deliverable paths, and a
  targeted coherence read). Treat a "pass" status as a claim to be re-checked, not trusted.
- FR-2.2 **Next unfinished task — assume partial work.** Detect artifacts attributable to
  the next task that may be half-written; surface them for cleanup or assessment before
  re-execution layers new work on top.
- FR-2.3 **Crash with no per-task data.** Phase re-run is permitted, but FR-2.2-style
  half-finished-work assessment/cleanup still runs first for the whole boundary phase.
- FR-2.4 **Gate condition (hard):** resume MUST NOT proceed until (a) boundary half-finished
  work is cleaned or explicitly assessed-and-accepted, AND (b) the last completed task is
  doubly validated. Failure ⇒ STOP with a report and require operator decision.
  **CG-4 ruling (YES, operator Ryan W 2026-06-02):** on the non-interactive (`--yes`/CI) path,
  "(a) explicitly assessed-and-accepted" is satisfied by **"`--yes` (or interactive assent) + a
  printed partial-paths report"** — the half-written paths are surfaced (F-2/CG-1) so the standing
  `--yes` is *informed* pre-consent, and the resume engine re-runs the boundary task (which
  overwrites that transient output). Quarantine remains the opt-in extra, not a precondition of
  `passed` (design §7). The interactive path is unchanged (the operator sees the prompt and assents).
- FR-2.5 Cleanup must be **non-destructive by default** (quarantine/stash with a recorded
  pointer, e.g. reuse the recovery `preserved/` + `recovery-audit.log` mechanism in
  `recovery.py`), never silent deletion.

### FR-3 — Semantic Staleness / Drift Assessment (refines rerun SHA-guard)
- FR-3.1 On auto-resume, rescan the tasklist and compare against the work already completed
  for alignment (phase/task identifiers, checkpoint declarations, deliverable paths).
- FR-3.2 Where a git remote is available, `git diff` the tasklist and relevant sources vs.
  the remote to characterize *what changed*, not merely *that* something changed.
- FR-3.3 Produce a **safety-confidence score ∈ [0,1]** that resuming is safe. Cosmetic edits
  (trailing whitespace, comment/formatting, the `<!-- SUPERCLAUDE-RERUN -->` block) MUST NOT
  reduce confidence — extend `_content_sha256_excluding_rerun_block` normalization rather
  than relying on raw bytes.
- FR-3.4 **Gate:** confidence ≥ 0.8 ⇒ print the drift summary + plan, **prompt the user**,
  then proceed on assent. Confidence < 0.8 ⇒ refuse silent resume; require explicit
  `--start N` or `--fresh`.
- FR-3.5 The assessment must explain its score (what changed, why it does/doesn't matter).

### FR-4 — Default UX & Flags
- FR-4.1 Bare `sprint run <index>` (no `--start/--end`) ⇒ auto-resume path. Bare
  `sprint rerun-tasks <index>` (no `--phase/--tasks/--from-reflect-report`) ⇒ auto-detect
  the most recent phase with recoverable failures + its failed-task set, then run as if
  specified.
- FR-4.2 Default behavior = **detect → print inferred plan → proceed** (per S2). Plan output
  names: completed phases, interrupted phase, granularity chosen, boundary tasks being
  re-validated/cleaned, and drift confidence.
- FR-4.3 New `--fresh` / `--no-resume` flag forces a clean run from `--start 1` (alias
  decision deferred to design; provide one canonical name + one alias).
- FR-4.4 Explicit `--start`/`--end` (run) or `--phase`/`--tasks` (rerun-tasks) **disable
  auto-detect** and preserve today's exact semantics (backward compatibility).
- FR-4.5 `--dry-run` prints the full `ResumePlan` + integrity-gate findings + drift score
  without executing.

### FR-5 — Disambiguation (from `/task`)
- FR-5.1 If multiple plausible resume points / release dirs / conflicting state are found,
  print the candidates and STOP requesting an explicit flag — never auto-pick on an
  expensive run (mirrors `skills/task/SKILL.md:50-56`).

## 4. Non-Functional Requirements
- NFR-1 Planner + integrity gate are **read-only** w.r.t. canonical results until the gate
  passes; all mutations are non-destructive and audit-logged (`recovery-audit.log`).
- NFR-2 Reuse existing modules; net-new surface limited to a `resume_planner` + integrity
  gate + drift assessor, wired into `commands.py run`/`rerun_tasks`.
- NFR-3 Deterministic core (phase/task enumeration); any LLM-judgment step (coherence,
  drift) must be isolated, explainable, and overridable by flags.
- NFR-4 CI/unattended safety: the prompt in FR-3.4 must have a documented non-interactive
  behavior (e.g. `--yes`/env) so automation can opt into proceed-on-≥0.8.

## 5. Acceptance Criteria
- AC-1 Interrupt a sprint at phase 3 of 5; bare `sprint run <index>` resumes at phase 3,
  prints the plan, completes phases 3–5; phases 1–2 are not re-run.
- AC-2 Phase 3 had a `fail_recoverable` task; auto-resume re-runs only that task via the
  rerun engine (task-level), merges back, refreshes canonical per-task status.
- AC-3 Hard crash mid-phase 3 (no `phase-3-result.json`): auto-resume assesses/cleans
  half-finished phase-3 artifacts, then re-runs phase 3; last completed task (phase 2 tail)
  is double-validated first.
- AC-4 Add only trailing whitespace to the tasklist between runs ⇒ drift confidence stays
  high (≥0.8) ⇒ resume proceeds after prompt; **no full-phase redo** is forced.
- AC-5 Materially edit a completed phase's task in the tasklist ⇒ confidence < 0.8 ⇒ silent
  resume refused; operator guided to `--start`/`--fresh`.
- AC-6 Fully completed sprint ⇒ `nothing-to-resume` message, exit 0.
- AC-7 Explicit `--start 4` ⇒ auto-detect bypassed; behaves exactly as today.
- AC-8 Ambiguous state (two candidate release dirs) ⇒ candidates listed, STOP, no execution.
- AC-9 Bare `sprint rerun-tasks <index>` ⇒ auto-detects latest phase with recoverable
  failures + failed tasks; identical result to the equivalent explicit invocation.

## 6. Architecture Sketch (reuse-first)
```
commands.py run() / rerun_tasks()
  └─ if no explicit position flags:
       ResumePlanner.plan(index_path, release_dir)        # NEW (reads jsonl + result.json + transcripts)
         ├─ uses rerun_tasks._classify_transcript / discover_failed_tasks_from_transcripts
         └─ returns ResumePlan{start, end, boundary_tasks, granularity}
       DriftAssessor.assess(tasklist, completed_work, git_remote)  # NEW (refines SHA-guard)
         └─ confidence∈[0,1] + explanation ; gate ≥0.8 → prompt
       BoundaryIntegrityGate.run(plan)                    # NEW (validate-last + clean-next)
         └─ uses checkpoints.py verification + recovery.py preserve/audit
       → dispatch:
            phase-level  → existing executor.active_phases loop (start/end set)
            task-level   → existing rerun-tasks engine (phase + failed tasks)
```

## 7. Risks & Red-Team Findings (internal adversarial lens)
- R1 **False "completed" trust.** A task marked `pass` whose deliverables were never written
  (agent over-claimed) is exactly the seam FR-2.1 targets — but coherence validation is
  fuzzy. *Mitigation:* prefer deterministic checkpoint/deliverable existence checks first;
  reserve LLM coherence for ambiguous cases; always print what was validated.
- R2 **Crash-before-`phase_start` blind spot.** If the process dies before emitting
  `phase_start`, the planner can't see the intended phase. *Mitigation:* emit/confirm a
  pre-spawn breadcrumb (OQ1) so the interrupted phase is always inferable; otherwise fall
  back to "first phase without result.json."
- R3 **Drift scoring is the trust anchor and the attack surface.** A wrong "high confidence"
  silently resumes against a changed plan. *Mitigation:* conservative scoring (bias toward
  <0.8 on uncertainty), mandatory explanation, and the user prompt at the ≥0.8 boundary —
  it is prompt-then-go, never silent-go, even above threshold.
- R4 **Non-destructive cleanup that loses work.** Quarantining half-finished artifacts could
  strand partial progress. *Mitigation:* reuse `recovery.py` `preserved/` + audit log;
  never delete; record restore pointers (parallels `rerun-tasks --restore`).
- R5 **Backward-compat regressions / CI.** Teams scripting `sprint run` without flags now
  get auto-resume + a prompt. *Mitigation:* FR-4.4 explicit-flag bypass + FR-NFR-4
  non-interactive opt-in; document the behavior change loudly in the v4.3.5 changelog.
- R6 **Two commands, doubled test surface.** `rerun-tasks` auto-detect (FR-4.1) shares the
  planner but has its own edge cases. *Mitigation:* single `ResumePlanner` with two thin
  adapters; shared test fixtures over the real-subprocess e2e harness added in `344a754a`.

## 8. Open Questions (for design phase)
- OQ1 Resume cursor: derive-only vs. add pre-phase breadcrumb (R2).
- OQ2 Precise definition of "doubly validated" (checkpoint + deliverable existence vs. LLM).
- OQ3 Cleanup mechanism: git stash vs. `preserved/` quarantine vs. report-only default.
- OQ4 Drift assessment: deterministic heuristic vs. LLM vs. hybrid; remote-diff when offline.
- OQ5 Canonical opt-out flag name (`--fresh` vs `--no-resume` vs `--restart`).

## 9. Suggested Next Step
This is design-heavy (the integrity gate + drift scoring are the hard parts). Recommended:
`/sc:design @.dev/brainstorms/20260602-sprint-auto-resume-default/merged-requirements.md`
to settle OQ1–OQ5, then `/sc:tasklist` for a v4.3.5 sprint bundle.
