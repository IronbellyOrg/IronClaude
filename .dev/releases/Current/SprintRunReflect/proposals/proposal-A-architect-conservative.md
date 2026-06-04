---
proposal_id: A
persona: architect
model: opus
stance: conservative-sidecar
---

# Proposal A — Background Subprocess, Sidecar-Only, Opt-in Flag

## T1 — Integration boundary

**Choice: Option B (background subprocess, never blocks).** Spawn `claude --print "/sc:reflect --mode post --depth deep ..."` via `subprocess.Popen` immediately after `notify_phase_complete()` returns at executor.py:1605. Capture stdout/stderr to a per-phase log under `<results_dir>/.reflect/phase-N.log`. The Popen handle is tracked in a `SprintReflectFleet` registry attached to `sprint_result`. The next phase starts immediately; reflect runs concurrently with phase N+1.

**Rejected alternatives:**
- Option A (subprocess that blocks until reflect finishes) — defeats the whole point of "parallel with the sprint continuing"; adds 30-120s wall-clock per phase at T2-deep.
- Option C (external watcher) — keep this as the *manual escape valve* but native integration is the goal.
- Option D (per-task reflect) — too granular for the per-phase audit grain that UC-2 is designed for; tasks lack the milestone-vs-roadmap framing that gives UC-2 its value.

## T2 — Gate semantics

**Choice: Option A (sidecar-only) for v1.** No gate effect. Reports written to `tasklist/validation/sc-reflect-post-phase-N-report.md` and `<results_dir>/.reflect/phase-N-report.md`. The Sprint pipeline continues regardless of reflect outcome.

**Rationale**: Asymmetric-cost argument cuts both ways. Halting on a false-positive regression is *also* costly (sprint stalls, operator must manually green-light). For v1, surface findings without acting; let the operator decide whether to halt manually. Gate semantics added in v2 once we have empirical regression-rate data from sidecar runs.

**Rejected**: Option B/C/D for v1; **planned for v2** once we have empirical false-positive rate from sidecar runs.

## T3 — Tier/depth selection

**Choice: Auto-tier via sc-reflect's own §5.3 rubric, with `--depth deep` forced.** Pass `--tier auto` so sc-reflect picks T1 vs T2 from its rubric (files-changed, error-budget, tier-tags). Pass `--depth deep` so the reviewers do thorough work when T2 fires. Pass `--budget-remaining <N>` from the sprint's tracked budget so reflect's Wave 0 pre-flight can self-downgrade if budget is tight.

**Cost envelope**: At 9 phases with rubric-mixed T1/T2, expect ~150-280k tokens total. Worth the safety floor.

## T4 — Parallelism details

- **Result surfacing**: file-on-disk poll. The pre-`notify_phase_complete()` hook at the next phase reads any completed `phase-N-report.md` for phase N-1 and surfaces a one-line summary in the TUI. No async event bus.
- **Race condition**: explicitly accept the race as a known limitation in v1. Document it in the report frontmatter: `audit_basis: git_HEAD_at_phase_end_<sha>`. The reflect agent reads files from that SHA via `git show` rather than working-tree, eliminating the race. Implementation: pass `--commit-range <prev_sha>..<phase_end_sha>` to sc:reflect.
- **Token budget envelope**: SprintConfig adds `reflect_budget_total: int = 250_000` and `reflect_budget_per_phase: int = 40_000`. The fleet registry tracks cumulative usage; when budget exhausted, remaining phases run with `--tier 1 --depth quick` (force-downgrade).
- **Cleanup**: signal_handler.shutdown_requested triggers SprintReflectFleet.terminate_all() which SIGTERMs all live Popen handles, waits 5s, then SIGKILLs.

## T5 — Sc-reflect features leveraged

- **§14.5 Wave 7 promotion mutation** — leave as-is (default-on UC-2 strict-gate); sidecar mode means it produces metrics without acting.
- **§4.1c auto-wire of tdd_file/prd_file from `.roadmap-state.json`** — auto-applies; no executor changes needed.
- **§15.1 metrics.json + `.dev/reflect/runs.jsonl`** — aggregator for end-of-sprint retrospective consumption (see T7).
- **§11.5 sampled citation budget** — auto-applies for large-diff phases.
- **§11.3 calibrator disjoint-set rule** — auto-applies.
- **§4 Wave 0 step 0.9 budget pre-flight** — executor passes `--budget-remaining <reflect_budget_per_phase>` for self-downgrade.

## T6 — Migration path

1. **v1 (this release)** — `--reflect post-phase` opt-in flag. Default off. Sidecar only. Released as feature flag.
2. **v1.1 (next minor)** — Collect 2-4 weeks of sidecar data. Compute false-positive/true-positive regression-detection rate from `.dev/reflect/runs.jsonl`. If FPR < 10%, recommend opt-out default.
3. **v2 (next major)** — Default on, with `--no-reflect` opt-out. Add gate flag `--reflect-mode {none|sidecar|halt-on-regression|strict}` per §T2.
4. **Compatibility**: in-flight sprints use `SprintConfig.reflect_mode` defaulted to `"none"` so resume() of a v1 sprint started before this flag works without surprise.

## T7 — Existing pipeline updates

- **`run_post_phase_wiring_hook`**: keep. Orthogonal — wiring is static (import graph, file references); reflect is content-driven (does the diff match the spec?). Co-exist as two independent gates.
- **`_verify_checkpoints`**: keep. Cp-file adherence is mechanical (artifacts exist + non-empty). Reflect's UC-2 verifies semantic adherence (do the artifacts *say* what the spec required?). Two-layer defense.
- **`retrospective.py`**: extend. Add a new helper `load_phase_reflect_reports()` that globs `tasklist/validation/sc-reflect-post-phase-*-report.md` and feeds them into the Haiku narrative as a "cross-phase reflection trend" section.
- **`monitor.py`/`tui.py`**: add a one-line "Reflect: queued | running | done | regression" status per phase in the TUI panel. Optional — non-blocking work.
- **`kpi.py`**: emit `reflect_calibrated_confidence_per_phase`, `reflect_regression_count`, `reflect_drift_count` as new KPI fields.

## Implementation cost

- **Files changed**: `executor.py` (+~80 LOC for spawn + fleet registry), `notify.py` (+~20 LOC for spawn hook), new `reflect_fleet.py` (~150 LOC), `retrospective.py` (+~40 LOC), `kpi.py` (+~30 LOC), `config.py`/SprintConfig schema (+~10 LOC), CLI entry (+~20 LOC for flag), tests (~300 LOC).
- **LOC delta**: ~650 LOC including tests.
- **Dependencies**: none new (uses stdlib `subprocess` + existing `claude` CLI).
- **Dev hours**: 12-16h including tests.

## Risks

- Subprocess error transparency — if the spawned `claude` crashes, only stderr capture saves us. Need careful logging.
- Budget runaway if sc-reflect ignores `--budget-remaining`. Mitigation: enforce hard `subprocess.kill` after 5min wall-clock per phase.
- Git-SHA audit basis assumes phases commit. If phases don't commit (very common), `--commit-range` is empty. Fallback: pass `--diff <results_dir>/.diffs/phase-N.patch` generated from `git diff` at phase-complete.
