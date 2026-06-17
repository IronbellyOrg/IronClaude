# Reflect REPORT — sc:pr-submit default changes (UC-2 post-execution)

- **Mode:** post (UC-2) · **Tier reached:** 2 (escalated by §5.3 rule 4 — `S_domains ≥ 3`: code + tests + docs)
- **Status:** `success` · **Calibrated confidence:** 0.92
- **Diff:** `HEAD` (working tree vs `0f9c8d36`), 5 files · **Tasklist:** `TASK-pr-submit-defaults-20260616/task.md`
- **Promotion:** skipped (`--no-promote`)
- **Ensemble:** 2 heterogeneous reviewers — analyzer (gpt-5.5) + qa (qwen3.6-plus), multi-vendor, converged

## Verdict

The change is **correct, complete, and regression-free.** It flips two `sc:pr-submit` defaults — `--monitor` 0→1 and `--timeout` 1800→600 — across source, tests, command doc, protocol doc, and the augment-poll reference, with the explicit `--monitor 0` open-only path preserved and tested end-to-end.

## Coverage map (tasklist → diff)

| # | Checklist item | Diff evidence | Verified |
|---|----------------|---------------|----------|
| 1 | fsm.py defaults + parser wiring | `DEFAULT_MONITOR=1` (fsm.py:30), `DEFAULT_TIMEOUT=600` (fsm.py:33), `SkillArgs.monitor` (fsm.py:52), parser `default=DEFAULT_MONITOR` (fsm.py:74), `RunConfig.monitor_ordinal` (fsm.py:721) | ✅ |
| 2 | test defaults + preserve explicit `--monitor 0` | `test_t103_default_monitor_one_armed` (test_skill_parse.py:57-61), `test_explicit_monitor_zero_not_armed` (:64-68), timeout assert (:81-84) | ✅ |
| 3 | command doc | pr-submit.md:8 argument-hint, :26 + :45 table rows | ✅ |
| 4 | protocol doc | SKILL.md:45, :90 (Wave 1 timeout text) | ✅ |
| 5 | augment-poll ref | augment-poll.md:51 (1800→600, ~30→~10 min) | ✅ |
| 6 | sync-dev / verify-sync | `make verify-sync` → "All components in sync" | ✅ (re-run clean) |
| 7 | pytest pr_submit | **191 passed** | ✅ (re-run clean) |
| 8 | reflect gate | THIS run | ▶ |
| 9 | commit / push / PR | not started | ☐ (post-gate) |

`tasklist_completion_pct (implementation) = 1.0`.

## Correctness (Grounded)

- **`armed` semantics hold.** fsm.py:64-67 `armed` = `self.monitor >= 1`; with `DEFAULT_MONITOR=1`, runtime-confirmed `parse_args([]).armed == True`, `parse_args(["--monitor","0"]).armed == False`, `parse_args([]).timeout == 600`.
- **Explicit-0 escape hatch tested end-to-end** — not just the parse: `test_t110_monitor_never_armed_at_l0` (test_monitor_arm.py:35-43) asserts `run_skill(RunConfig(monitor_ordinal=0))` → arm-recorder `calls == 0` and final state `S0_IDLE`.
- **No stale references survive.** Repo-wide greps (`1800`, `~30 min`, monitor `default 0`, `omit/without --monitor`) found zero surviving pr_submit default references. The 5 `tests/pr_submit/*` `1800` literals are explicit `timeout=` args (arithmetic tests), not the default — and all pass, proving no stale *default* assertion.
- **Verification triangle clean:** 191 tests pass, `ruff format --check` + `ruff check` green, `make verify-sync` confirms `.claude` mirror matches `src/`.

## Deviation classification (§10)

| Class | Count |
|-------|-------|
| Authorized expansion | 0 |
| Necessary deviation | 1 |
| Drift | 0 |
| Regression | 0 |

**The one necessary deviation:** `RunConfig.monitor_ordinal` default `0 → DEFAULT_MONITOR` (fsm.py:721). Not separately enumerated as a checklist sub-item, but required for the default-behavior change to be coherent across the pure-core seam — without it, a bare `RunConfig()` would run at L0, half-implementing the goal. Contradicts no criterion; no caller relied on the old 0 default.

### Divergence from the prior `prbranch` run
The prior reflect (Tier 2, **degraded** model diversity) recorded **1 drift**. This run (Tier 2, **full** multi-vendor diversity + independent orchestrator re-grounding) **reclassifies that hunk from drift → necessary.** Both heterogeneous reviewers independently rejected the drift call with the same coherence rationale. The net code verdict is unchanged (clean, ship-ready); only the deviation *label* on the contested hunk changed.

## [INFERRED]

- fsm.py:608 `ctx.get("monitor_ordinal", 0)` is a **safe defensive floor** in the pure `transition()` function, intentionally decoupled from the parser default — topology tests call `transition()` with no context to assert edge structure under the most-restrictive ceiling. Argued structurally (not a cited contradiction), so tagged inferred; both reviewers concur it must stay 0.

## Recommendations (actionable)

1. **(Non-blocking, cosmetic)** Update `tests/pr_submit/test_monitor_arm.py` module docstring (lines 3-4) and the `test_skill_parse.py` T-110/T-103 cross-reference to note that `--monitor 0` is now an **explicit opt-out**, not the default. Assertions are correct; only the narrative lags. *Verify:* re-read the docstrings.
2. **Proceed to commit/PR (item 9).** The gate is clean. Open the PR against `IronbellyOrg/IronClaude` per CLAUDE.md (`gh pr create --repo IronbellyOrg/IronClaude --base master --head fix/pr-submit-defaults-monitor-timeout ...`).

## Grounding / structural notes

- `evidence-validator`: inline (agent not spawned); orchestrator re-Read all load-bearing citations → **0 dropped**. Zero-drop is flagged per §11.2; corroborated by 2 independent reviewers + re-Read on a small, fully-verified surface.
- `calibrator`: inline 5-dim calibration (`calibrator-inline-fallback`) → `calibrator_diversity: degraded`. Reviewer diversity itself is **full** (multi-vendor), the primary anti-confirmation gate.
- `sc-adversarial` not invoked: the two cards converged (no competing verdict to debate).
- Promotion not evaluated (`--no-promote`); independently, the tasklist frontmatter still records the prior `prbranch` run and `status: in-progress` with items 8-9 open — the wrapper/operator owns the frontmatter stamp for this run.
