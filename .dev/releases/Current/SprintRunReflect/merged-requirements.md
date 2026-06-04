---
adversarial_status: pass
convergence_score: 0.85
proposals_synthesized: 3
created: 2026-06-01T00:00:00Z
---

# Merged Requirements — Sprint Run Reflect Integration

## Executive summary

Integrate `/sc:reflect --mode post --depth deep` as a native background hook in `superclaude sprint run`, fired after each phase's `notify_phase_complete()`. Reports land as sidecars by default; a `--reflect-mode` flag selects gate behavior. Phases run in parallel with reflect runs; a soft-join checkpoint at the next phase's first task surfaces any completed report. Migration is opt-in → opt-out → mandatory across three minor releases driven by empirical false-positive-rate data.

## T1 — Integration boundary (RESOLVED)

**Native in-executor spawn via a dedicated `reflect_fleet.py` helper module.** After `notify_phase_complete()` returns (executor.py line 1605), the executor calls `reflect_fleet.spawn(phase, phase_result, config)` which:

1. Computes audit basis: commit SHA via `git rev-parse HEAD`, or `git stash create` SHA if working tree is dirty.
2. Builds the `claude --print "/sc:reflect --mode post --depth deep --tasklist <path> --commit-range <prev_sha>..<curr_sha> --output <path> --budget-remaining <N>"` command line.
3. Spawns via `subprocess.Popen`, captures stdout/stderr to `<results_dir>/.reflect/phase-N.log`.
4. Registers Popen handle in a `SprintReflectFleet` registry attached to `sprint_result`.
5. Returns immediately. Phase N+1 starts without waiting.

**Soft-join checkpoint** is added at the start of phase N+1's task loop: before phase N+1's first task launches, executor calls `reflect_fleet.poll(phase_n.number, timeout=0)` — if reflect-N has finished, consume the report; if not, proceed (it'll land mid-phase-N+1 as a sidecar). Cost ≈ 0s when reflect is still running, ≤ 1s when it just finished.

## T2 — Gate semantics (RESOLVED)

New CLI flag `--reflect-mode {none|sidecar|halt-on-regression|strict}`. SprintConfig field `reflect_mode: str = "sidecar"`.

| Mode | Behavior |
|---|---|
| `none` | Disable reflect entirely. Back-compat. |
| `sidecar` | **v1 default.** Spawn and consume reports but never gate. |
| `halt-on-regression` | Halt sprint when reflect-N produces `regression_present=true`. Operator prompted (continue/abort/view). Default action in non-interactive mode (CI): abort. |
| `strict` | Halt on regression OR drift OR status=partial. Reserved for release pipelines. |

Halt point is **between tasks of phase N+1**, never mid-task. If reflect-N's report arrives during phase N+1's mid-task, the halt is queued for the next task boundary. This avoids killing in-flight work.

## T3 — Tier/depth (RESOLVED)

- **Depth**: always `deep` (user spec).
- **Tier**: new flag `--reflect-tier {auto|t1|t2}`, SprintConfig field `reflect_tier: str = "auto"`. Default `auto` delegates to sc-reflect's §5.3 rubric. `t2` pins for cross-phase signal consistency in release sprints. `t1` is the fast-cheap option for high-frequency development sprints.

Budget envelope:
- T1-deep ≈ 8-15k tokens/phase
- T2-deep ≈ 35-70k tokens/phase
- 9-phase sprint at auto-mix ≈ 150-280k; at pinned t2 ≈ 315-630k.

## T4 — Parallelism details (RESOLVED)

- **Result surfacing**: file-on-disk poll. `SprintReflectFleet` maintains an in-process registry of `{phase_num: PopenHandle, report_path, status}`. Polling thread checks every 2s for Popen.poll() completion; on completion, parses the report frontmatter for `status`, `regression_present`, `calibrated_confidence`. Surfaces via:
  - TUI cell update (monitor.py / tui.py).
  - `reflect_complete` event written to `execution-log.jsonl` (backward-compatible with existing log consumers).
  - `sprint_result.reflect_reports[phase_num]` accessor.
- **Race condition handling**: commit-pinning via `git rev-parse HEAD` or `git stash create` SHA. Reflect reads files via `git show <sha>:<path>` not working-tree. Race eliminated.
- **Token budget envelope**: SprintConfig adds:
  - `reflect_budget_total: int = 300_000` (envelope for entire sprint).
  - `reflect_budget_per_phase: int = 50_000` (passed as `--budget-remaining`).
  - Fleet tracks cumulative consumption from sc-reflect's `metrics.json`. When 80% consumed: WARN. When 100%: force-downgrade remaining phases to `t1`. When 150% (runaway): kill all live Popens, stop spawning.
- **Cleanup**: `signal_handler.shutdown_requested` triggers `SprintReflectFleet.terminate_all(grace=5s, then_kill=True)`. `atexit` handler as belt-and-suspenders.
- **Wall-clock timeout per reflect**: 5min hard kill (configurable via `reflect_timeout_seconds: int = 300`).

## T5 — Sc-reflect features leveraged (RESOLVED — unanimous)

| Feature | Use |
|---|---|
| §14.5 Wave 7 promotion mutation | Honor `promotion_decision: blocked` in gate modes |
| §4.1c auto-wire of tdd_file/prd_file | Auto-applies via `.roadmap-state.json` in results_dir |
| §15.1 metrics.json + .dev/reflect/runs.jsonl | Cross-phase aggregator consumed by retrospective.py + kpi.py |
| §11.5 sampled citation budget | Auto for large diffs |
| §11.3 calibrator disjoint-set rule | Auto |
| §4 Wave 0 step 0.9 budget pre-flight | Pass `--budget-remaining <per_phase_cap>` |

## T6 — Migration path (RESOLVED)

| Release | Default | Flags | Notes |
|---|---|---|---|
| v1.0 (this) | `--reflect-mode none` (off) | `--reflect-mode`, `--reflect-tier`, `--reflect-budget-total`, `--reflect-budget-per-phase` | Opt-in. Document `sidecar` and `halt-on-regression` as recommended. |
| v1.1 (next minor, ~2-4 wk telemetry) | `--reflect-mode sidecar` | same | Passive — reports flow, no gates. |
| v1.2 (after FPR < 10%) | `--reflect-mode halt-on-regression` | same | Conservative gate becomes default. |
| v2.0 (release pipelines) | `--reflect-mode strict` for release pipelines only | same | Dev sprints stay at `halt-on-regression`. |

**Resume compatibility**: SprintConfig.reflect_mode, reflect_tier, budgets are persisted to `.roadmap-state.json` at sprint start. `resume()` honors original values; new flags ignored on resume.

**In-flight sprint compat**: any sprint started before v1.0 lacks these config fields. `SprintConfig.__post_init__` defaults missing fields to `none`/`auto`/300_000/50_000 — zero behavior change.

## T7 — Existing pipeline updates (RESOLVED)

### `run_post_phase_wiring_hook` — KEEP unchanged

Orthogonal to reflect. Wiring is static (import graph, file references); reflect is content-driven (does the diff match the spec?). Both evaluate independently; either can halt independently (analogous to anti-instinct + wiring independence per NFR-010).

### `_verify_checkpoints` — KEEP unchanged, document the two-layer model

The cp-file existence + non-emptiness check remains a fast sanity gate (sub-second). Reflect's UC-2 verifies semantic adherence (do the artifacts *say* what the spec required?). Two-layer defense — fast mechanical + slow semantic.

### `retrospective.py` — EXTEND

Add `load_phase_reflect_reports()` and `aggregate_reflect_runs_jsonl()`. New sections in the Haiku narrative:
- "Calibrated confidence trend (per-phase)"
- "Deviation taxonomy distribution"
- "Regression count by phase"

The Haiku consumes the structured fields, not raw report markdown. Lightweight extension (~50 LOC).

### `monitor.py` / `tui.py` — EXTEND

New TUI cell per phase: `[Reflect: queued | running | ok | drift | regression]` with color coding (green/yellow/red). Updates every 2s from `SprintReflectFleet` state. Non-blocking.

### `kpi.py` — EXTEND

New fields:
- `reflect_per_phase_status: dict[int, str]`
- `reflect_calibrated_confidence_per_phase: dict[int, float]`
- `reflect_regression_count: int`
- `reflect_drift_count: int`
- `reflect_authorized_expansion_count: int`
- `reflect_budget_consumed: int`
- `reflect_budget_remaining: int`

### `notify.py` — MINOR

`notify_phase_complete()` returns; right after, executor calls `reflect_fleet.spawn(...)`. No change to `notify_phase_complete()` itself.

## Implementation cost (consolidated)

| File | LOC | Notes |
|---|---|---|
| New `reflect_fleet.py` | ~250 | Fleet registry, Popen mgmt, budget tracking, commit-pinning, polling thread |
| `executor.py` | +~80 | Fleet init, spawn after notify, soft-join checkpoint, signal_handler integration |
| `notify.py` | +~5 | (Minimal — fleet hooked in executor, not notify.) |
| `config.py` SprintConfig | +~30 | New fields with safe defaults |
| `cli/main.py` (sprint subcommand) | +~40 | New CLI flags wiring to SprintConfig |
| `retrospective.py` | +~50 | Reflect report aggregation + new narrative sections |
| `kpi.py` | +~50 | New KPI fields |
| `monitor.py` / `tui.py` | +~40 | Reflect status cell |
| Tests | ~600 | Unit (fleet, budget, commit-pin) + integration (gate semantics, race) |
| **Total LOC delta** | **~1145** | Including tests |

**Dependencies**: none new. Uses stdlib `subprocess`, `threading`, `os`, `signal`.

**Dev hours**: 20-26h including tests and docs.

## Risks (consolidated)

1. **Subprocess error transparency** — if spawned `claude` crashes silently, only stderr capture catches it. Mitigation: stderr → log + `phase-N.error` sentinel file → TUI surfaces "reflect errored, check log".
2. **Budget runaway if sc-reflect ignores `--budget-remaining`** — hard kill at 150% cumulative; per-reflect 5min wall-clock kill.
3. **Race condition if phases don't commit** — git-stash fallback covers this. If even stash fails (rare), reflect reads working-tree with the known race; report frontmatter flags `audit_basis: working_tree_race_accepted`.
4. **Reflect mode persistence across resume** — must be in `.roadmap-state.json` schema. Add field with safe default for back-compat.
5. **TUI flicker if many reflect cells update concurrently** — debounce TUI redraws to every 250ms.
6. **Operator confusion about which gates failed** — TUI must distinguish wiring vs checkpoint vs reflect gate failures with distinct labels.

## Open questions (for user resolution before coding)

1. **Should reflect runs be allowed for sprints without a roadmap?** Today some sprints run without `.roadmap-state.json` (e.g., one-off tasklists). sc-reflect §4.1c auto-wire fails in that case. Options: (a) skip reflect for roadmap-less sprints with INFO log; (b) require `--tdd-file`/`--prd-file` CLI flags as fallback; (c) hard-error. **Recommendation: option (a) with INFO log.**
2. **Should the soft-join checkpoint be configurable to a full block?** Some operators may want phase N+1 to *wait* for reflect-N before starting. Add `--reflect-join {none|soft|block}` (default `soft`)? Or punt to v1.1?
3. **Should `--reflect-mode strict` halt on `authorized_expansion` (sc-reflect §10.1)?** strict is documented as "halt on regression OR drift OR status=partial" but `authorized_expansion` is a *successful* deviation. Confirm strict does NOT halt on authorized expansion.
4. **Multi-sprint scenarios** — if the operator launches two sprints in parallel (different worktrees), do their reflect fleets share a budget envelope or each get their own? **Recommendation: per-sprint envelope, no cross-sprint coordination.**

## Acceptance criteria

- [ ] Existing sprints with `--reflect-mode none` (or no flag) behave identically to today.
- [ ] `--reflect-mode sidecar` produces a `phase-N-report.md` for every phase, never halts.
- [ ] `--reflect-mode halt-on-regression` halts at the next task boundary when a report has `regression_present=true`.
- [ ] `--reflect-tier auto` produces a mix of T1 and T2 reports per sc-reflect's §5.3 rubric.
- [ ] `--reflect-budget-total` is honored; runaway is killed at 150%.
- [ ] Ctrl-C during a phase cleanly terminates all in-flight reflect Popens.
- [ ] `retrospective.py` summary includes per-phase reflect trend section.
- [ ] `kpi.py` outputs all new reflect_* fields.
- [ ] Resume of a v1.0 sprint started without `--reflect-mode` works.
- [ ] Sprint with no `.roadmap-state.json` skips reflect with INFO log (per open question 1).
- [ ] Test coverage ≥ 85% for `reflect_fleet.py`.

## Next-step handoff suggestions

- **Direct to tasklist generation**: `Skill sc-tasklist-protocol` with `--source @.dev/releases/backlog/SprintRunReflect/merged-requirements.md` — produce a deterministic phased tasklist.
- **Or TDD first**: `Skill tdd` to produce a `SprintRunReflect_TDD.md` formalizing the `reflect_fleet.py` module surface, fleet state model, race-handling proofs, and budget enforcement state-machine before coding.
- **Or pre-coding confidence check**: `Skill confidence-check` to validate ≥90% readiness against the open questions list.
