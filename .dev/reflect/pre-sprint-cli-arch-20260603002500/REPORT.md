# /sc:reflect — UC-1 Pre-Execution Reflection Report

**Spec under review:** `.dev/releases/backlog/sprint-cli-architecture-brainstorm/SYNTHESIS.md`
(+ source docs `agent1-execution-model.md`, `agent2-handoff-mechanism.md`)
**Mode:** `pre` (UC-1, coverage-only — no `--tasklist` supplied)
**Depth:** `deep` → **Tier 2** (forced). 3 heterogeneous reviewers (gpt-5.5 / qwen3.6 / claude-opus-4-8), multi-vendor.
**Date:** 2026-06-03 · **Worktree:** `SprintCLIWireDead`
**Verdict:** Architecture **sound and code-verified**; spec is **NOT yet a complete basis for an implementation tasklist** — 16 gaps (6 HIGH), several attacking the headline "Stage 0 is decoupled / pure win."

---

## Headline

> The SYNTHESIS's central thesis — *"this is a wiring job, not a greenfield build"* — is **independently VERIFIED** (7/9 load-bearing code claims confirmed exactly; dead `setup_isolation`, dead `build_task_context`, missing main-path `task_complete`, hardcoded `turns_consumed=0`, heading-regex fork all real). The reasoning is rigorous and honestly flags its own inference.
>
> **But as a tasklist basis it is premature.** Reviewers + grounding found that the spec's most-repeated framing — *"Stage 0 is decoupled, a pure win, do it first in its own PR"* — does not survive contact with the code: wiring `setup_isolation` is a **behavior change** (Path A already sets a *conflicting* `CLAUDE_WORK_DIR`), its **gate doesn't test the failure it targets**, and two existing surfaces the spec never mentions (`write_task_rerun_complete`, `--start/--end` phase-granularity) force a tasklist author to **invent reconciliation decisions**.

**Readiness grade: 2 / 5** (reviewer grades 3, 2, 2). **Best-practice rigor of the spec itself: 4 / 5.** These are different axes — the spec is *well-reasoned* but *under-specified for execution*.

---

## Grounding verdict (Wave 1A — orchestrator-verified, then independently extended by reviewers)

| # | Spec claim | Verdict |
|---|---|---|
| 1 | `setup_isolation` dead (zero callers) | ✅ executor.py:151, no call site |
| 2 | `build_task_context` dead | ✅ proc:257, 0 ext callers (note: `compress_context_summary` has 1 caller — the dead `build_task_context:290` — so "zero callers" is imprecise but it is transitively dead) |
| 3 | "No `task_complete` writer at all" | ⚠️ **TRUE for main path; FALSE adjacent** — `write_task_rerun_complete` emits `task_rerun_complete` (logging_.py:205-211). The spec overlooked it. |
| 4 | Runtime fork on heading regex | ✅ config.py:380; executor.py:1264-1270 |
| 5 | `turns_consumed=0` hardcoded | ✅ executor.py:1118 — **+ code comment "wired separately in T02.06"** (an existing task the spec ignores) |
| 6 | "`CLAUDE_SETTINGS_DIR` never set anywhere" | ⚠️ **IMPRECISE** — set at executor.py:133 (in the dead `IsolationLayers`). True only as "never set in a live path." |
| 7 | "Stage 3 is the **first** consumer of `dependencies`" | ⚠️ **FALSE** — `rerun_tasks.py:438-449` already consumes it |
| 8 | `_jsonl` lock-free append | ✅ logging_.py:265-267 |
| 9 | checkpoints atomic temp+replace | ✅ checkpoints.py:208-210 |

**Cross-cutting:** every spec line-citation has **already drifted** in this worktree (+4 to **+55** lines) → a tasklist MUST anchor on symbol names, not line numbers.

---

## Merged findings (16) — ordered by severity, deduped across 3 reviewers + grounding

### 🔴 HIGH (must resolve before authoring a tasklist)

**H1 — "Stage 0 is decoupled / pure win" is false; wiring isolation is a behavior change.**
`R1-003, R3-003`. Path A today injects `CLAUDE_WORK_DIR = <phase-copy dir>` (executor.py:1327-1330); `setup_isolation` returns `CLAUDE_WORK_DIR = release_dir` (executor.py:178-183) — a *different value* that defeats per-phase file scoping. Isolation also changes `CLAUDE_SETTINGS_DIR`/`CLAUDE_PLUGIN_DIR`, affecting skills, MCP config, hooks, permissions inside the subprocess. Path A and Path B need **different** merge semantics; the spec treats both as one uniform additive change.
→ **Add a per-path merge-semantics table:** does Path A keep its phase-copy `CLAUDE_WORK_DIR` and only *add* `CLAUDE_SETTINGS_DIR`? Add a Stage-0 gate: "isolated subprocess can still invoke `/sc:task`, project hooks, allowed tools, configured MCPs."

**H2 — Stage 0 gate doesn't test the failure it targets.**
`R1-004, R2-001`. Gate "corruption reproduction no longer occurs in serial reruns" — but corruption is a *concurrent-writer* class; serial reruns can't exercise it. The gate is a tautology once a settings dir exists.
→ Split into (a) serial isolation smoke test (functionality), and (b) a controlled concurrent-`claude`-spawn repro proving isolated settings dirs prevent the known corruption.

**H3 — `task_complete` writer must reconcile with the existing `task_rerun_complete` event.**
`R3-001` (verified EV-1). `write_task_rerun_complete` (logging_.py:205-211) already journals a per-task completion event for the rerun path, with `event/phase/task_id/status/turns/duration_sec`. The proposed `write_task_complete` never says whether it shares that name/schema, whether rerun also emits the new event, or how consumers distinguish first-run vs rerun.
→ Freeze both event schemas side-by-side; define the exact `event` string and field set; decide unify-vs-supersede.

**H4 — `HandoffRecord` schema is never frozen, despite the Stage-1 gate asserting "schema frozen."**
`R1-008, R2-004, R3-010`. The fields appear only as loose prose (`status, gate_outcome, turns, output_path, produced_artifacts[], consumed_upstreams[], started/finished`); no types, optionality, `schema_version`, or mapping from the existing `TaskResult.to_dict()` (models.py:194). A round-trip-fidelity test (the gate) needs a frozen schema to assert against.
→ Ship a frozen typed `HandoffRecord` block (with `schema_version`) + its derivation from `TaskResult`, before tasklisting.

**H5 — Resume is unsafe-by-existence AND its on-disk key collides AND its CLI surface doesn't exist.**
`R1-002 + R3-002 + R3-004`.
- *Predicate:* Stage 2 "skip tasks with an existing handoff record" — but records are written for `FAIL_*`/`INCOMPLETE`/`SKIPPED` results too; existence ≠ success.
- *Key collision:* `handoff/<task_id>.json` uses bare `T<PP>.<TT>`, which is **not** sprint-unique — `task_output_file` already disambiguates with `phase-{N}-task-` (models.py:562). Two phases' tasks collide on one file.
- *Missing surface:* `--start/--end` are phase-granular ints (commands.py:75-83); there is **no `--resume` handler**, yet `resume_command()` emits `--resume {halt_task_id}` (models.py:877). "Task-granular resume" is net-new CLI+config surface, unassigned.
→ Skip predicate = "validated successful record"; key = `phase-{N}-task-{task_id}`; specify the new resume flag + reconcile the dangling `resume_command()`.

**H6 — Parallel shared-state is under-scoped to `TurnLedger` only; the test seam can't even verify isolation.**
`R1-005 + R2-003`. `execute_phase_tasks` mutates `results`, `remaining`, `gate_results`, TUI state, `shadow_metrics`, `remediation_log`, `sprint_result` — not just `TurnLedger` (executor.py:965-1072). Separately, the existing `_subprocess_factory` seam returns the result tuple directly (executor.py:1003-1004), **bypassing `env_vars`** — so the Stage-1 isolation wiring is untestable through it.
→ Add a Stage-3 "shared-state inventory" task; add an `_env_capture`/`_env_builder` seam so a test can assert per-worker `CLAUDE_SETTINGS_DIR`.

### 🟡 MEDIUM

**M1 — `dependencies` DAG: reuse `rerun_tasks.py`, don't re-derive.** `R1-007, R3-008` + grounding F-C. `rerun_tasks.py:438-449` already walks `entry.dependencies`/`tr.task.dependencies` (cross-phase, `ignore_deps`, transitive). Correct the Open-Item §5 line and add a Stage-3 prerequisite to extract/reuse that primitive rather than author a parallel scheduler.

**M2 — `_jsonl` concurrency ordering dependency is implicit.** `R1-006, R2-002, R3-007`. Stage 0/1 add a high-frequency writer (`write_task_complete`) through the lock-free `_jsonl` (logging_.py:265-267); the safety fix is deferred to Stage 3. State explicitly that Stages 0-2 rely on the sequential single-writer invariant and Stage 3's fix must cover all writers added earlier. Define the logger concurrency architecture (single-writer queue vs per-task event files) in Stage 1.

**M3 — "Per-task prompt narrowed to one task" is undefined.** `R3-006`. `build_prompt` is monolithic/phase-scoped (process.py:169-216): "Execute all tasks", phase Result File + EXIT_RECOMMENDATION, phase Checkpoint scan. Add a section-by-section disposition table (keep/drop/rewrite) and decide who writes the phase result file when tasks run per-process.

**M4 — New flag plumbing unassigned.** `R3-005`. `--task-parallelism K`, `--handoff=off`, and the `FileHandoffStore`↔`MailHandoffStore` switch are named only as behaviors; no `SprintConfig` field or `click.option` is specified — yet the "one config line" rollback depends on the switch. Enumerate the config fields + options and name the owning stage.

**M5 — Migration / back-compat for in-flight sprints unaddressed.** `R3-009`. Resume against a pre-Stage-1 `release_dir` (no `handoff/`, no `task_complete` events) is unspecified. Add a back-compat decision: degrade to today's phase-granular behavior; state whether `handoff/` is created lazily.

**M6 — Heading-regex fallback is a global-routing change, untested.** `R1-010, R2-006, R3-013`. The B→A demotion fix touches the shared router (`_TASK_HEADING_RE`, config.py:380; fork at executor.py:1264), affecting *every* phase's path selection. Specify warn-only vs re-route; add a ≥10-entry heading-variant corpus with expected routing + diagnostics; the happy-path "3-phase sprint" gate does not exercise near-miss headings.

**M7 — Stage-1 schema freeze is premature relative to Stage-2 needs.** `R1-008`. M2 (resume skip-list + declared-upstream fan-in) is exactly what determines schema adequacy. Change the Stage-1 gate to "schema versioned + migration-safe" and freeze after Stage-2 tests, or pre-include `schema_version`/`upstreams`/`attempt_id`/`resume_eligible`.

### 🟢 LOW

**L1 — T02.06 reconciliation.** `R2-007, R3-012` + grounding F-B. executor.py:1117 references an existing turn-counting task; Stage 0's "fix `turns_consumed=0`" may duplicate it. Acceptance test must assert the *correct* turn value, not merely `!= 0`. Reconcile scope.

**L2 — Stage-4 rollback overstated.** `R1-009`. "Flip one line, free rollback" ignores sidecar/token/MCP-injection/mailbox cleanup. Reword to "*data* rollback is lossless (file remains source of truth)" + add an operational teardown checklist.

**L3 — Crash-consistency asymmetry untested.** `R2-005`. Handoff file = atomic temp+replace; journal = bare `_jsonl`. A crash between the two yields a completed task with no journal event. Add a test asserting resume uses handoff files (not the JSONL) as source of truth.

**L4 — DAG + resume interaction + benchmark baseline missing.** `R2-009, R2-010, R2-011`. Stage-3 "wall-clock win" has no defined baseline/harness; resume-under-parallel-DAG (in-flight task at kill time → no handoff file, dependents must not launch) is untested; Stage-4 mail-server mid-sprint failover lacks an acceptance criterion.

**L5 — Documentation work unassigned.** `R3-011`. New CLI flags, the `handoff/` artifact, and the new ledger event are user-visible surface with no docs/changelog task.

---

## What the spec gets right (so the tasklist preserves it)

- Evidence-grounded throughout; explicitly flags `INFERENTIAL`/`UNVERIFIED` (agent2 §8, SYNTHESIS §5).
- The **one-file-per-task, atomic temp+replace, runner-owned** handoff is genuinely immune-by-construction to the corruption class — and reusing the `checkpoints.py:208-210` idiom is the right call.
- Correct risk gate: **config-corruption blocks concurrency**; sequential-first (Proposal A / K=1) is the right ordering.
- agent-mail deferral to a shadow, reversible, concurrency-gated pilot is well-justified (shared-store + global `.commit.lock` echoes the original bug).
- Every stage has a flag-based escape hatch.

---

## Recommended next action

**Do not author the tasklist from the SYNTHESIS as-is.** Resolve at least the 6 HIGH findings into the spec first — they are concentrated in exactly the "do Stage 0 first" path the spec calls safest. Concretely:

1. Patch SYNTHESIS §3-§4 with the **per-path isolation merge table** (H1) + corrected Stage-0 gate (H2).
2. Add a **frozen `HandoffRecord` + ledger-event reconciliation** block (H3, H4) covering `task_rerun_complete`.
3. Add the **resume contract** (H5): success-predicate, `phase-N`-scoped key, new flag + `resume_command()` reconciliation.
4. Add the **Stage-3 shared-state inventory + `_env_capture` test seam** note (H6).
5. Correct the **Open-Item §5** "first consumer" line and point Stage 3 at `rerun_tasks.py` (M1).

Then re-run `/sc:reflect --mode pre --spec <patched> --tasklist <draft>` to get a real coverage_pct against an actual tasklist.

**Paste-ready follow-up (after patching the spec + drafting a tasklist):**
```
/sc:reflect --mode pre --depth deep --spec .dev/releases/backlog/sprint-cli-architecture-brainstorm/SYNTHESIS.md --tasklist <draft-tasklist-path>
```

---

## Grounding gaps / caveats (honest limitations)

- **No `--tasklist` supplied** → `coverage_pct` is undefined (UC-1 coverage-only). This report assesses *spec readiness*, not coverage of a concrete tasklist.
- **Calibrator-class collision:** reviewer R3 ran on the `opus` alias (claude-opus-4-8) — the same class as this orchestrator/merge — so calibration of R3's card is `degraded` per the disjoint-set rule. R1 (gpt-5.5) and R2 (qwen) are cleanly disjoint.
- **Merge method:** inline orchestrator synthesis of 3 reviewer cards (the `sc-adversarial-protocol` skill was not spawned in this run); `merge_method: inline-orchestrator`.
- **Zero citations dropped** by evidence-validation. Per protocol, a zero-drop pass is a *flag, not a clean signal* — mitigated here because the 4 highest-load-bearing reviewer citations were independently re-Read against current source (EV-1..EV-4 all confirmed).
- Spec line-numbers are stale in this worktree; all citations above were re-anchored to current symbol locations.
