# BUILD-REQUEST — MultiModelSwarm post-reflect remediation

## Goal
Build an MDTM remediation tasklist that closes the deviations found by the deep per-phase
`/sc:reflect` audit of the Multi-Model Swarm feature.

## Authoritative input
`/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/validation/deep/AMALGAMATED-REMEDIATION.md`
(consolidated, de-duplicated fix set; per-phase evidence in the sibling `1..9` + `8-rerun` REPORT.md files).

## CRITICAL execution context
- **cwd MUST be the SwarmPost worktree:** `/config/workspace/IronClaude/.claude/worktrees/SwarmPost`
  (branch `feat/multimodel-swarm`). The swarm code (`src/superclaude/cli/swarm`, `tests/swarm`) exists
  ONLY there. Researching from `main` produces false negatives — that is exactly what invalidated the
  original Phase-8 reflect. Do not research or cite from `/config/workspace/IronClaude/` main.
- Reports/tasklist live in `main`'s `.dev/releases/current/MultiModelSwarm/...` (read via absolute paths).

## Scope — build tasks for these (priority order from §4 of the amalgamation)
1. **F-P3-1 (CRITICAL):** `swarm run --transport stub` dispatches 0 workers (transport=None). Wire resolved Transport before `dispatch_wave1`.
2. **RW-4, RW-5, RW-1 (commit gates):** detect-secrets (6 fixtures + release-notes), markdownlint (28×MD024 / MD040 / MD013), `make verify-sync` mirror drift.
3. **RW-2, RW-3:** INV-002 tmux-subprocess test scoping (OQ-7.1); UV-enforcement `python -m` in commands.py (OQ-7.2).
4. **F-P1-3, F-P2-1, F-P2-2:** frozen dataclasses decision; wire `custom_prompt_dir`; Manifest `caller_metadata`.
5. **F-P3-3..7:** state persistence, retry matrix, model-identity-on-error, logger confinement, confinement test hardening.
6. **F-P7-1:** `test_detached_mode.py` decision.
7. **F-P8-1, F-P8-2:** TEST-005 `test_subprocess_caller.py`, TEST-008 `integration/conftest.py`. For F-P8-1, **inspect T08.14/T08.02 and the existing `tests/swarm/test_non_claude_caller.py` first; author the new test by default. Do NOT auto-rename/reconcile** the existing test (that branch mutates the tasklist → treat as a decision, not a mechanical fix).
8. **RW-6:** regenerate missing/stale checkpoints (P1 cp5, P2 cp5, P5 cp1/cp2/cp3, P8 cp3/cp4) — LAST, after gates pass.
9. **F-P9-1..5:** Phase 9 PLAN edits (do before any `sprint run --start 9`).

## Exclusions
- **Phase 6** — clean, no fixes.
- **Original `8/REPORT.md`** — INVALID/superseded; use `8-rerun/REPORT.md` only.

## Mandatory task-construction constraints
- The following are `needs_human_decision` items — emit them as **HALT** tasks that write PENDING and stop
  the dependent mutation (per `feedback_human_decision_items_must_halt`); do NOT auto-pick a default:
  - **F-P1-3:** freeze all 20 DM dataclasses *vs* amend spec to drop the frozen requirement.
  - **RW-3 (= F-P1-1, OQ-7.2):** UV-safe detached re-entry (`uv run superclaude ...`) *vs* documented AC-001 exception.
  - **F-P3-4:** remove 4xx/timeout retry *vs* authorize configurable overrides in the spec.
  - **F-P7-1:** backfill `test_detached_mode.py` *vs* authorize the current test distribution.
  - **F-P9-1:** which path wins for the duplicate docs (`runbook.md` vs `operator-runbook.md`; `docs/dev` vs `docs/swarm` lens-policy).
  - **F-P9-2:** the human-gated Phase-9 sign-offs — T09.01 (ops-reviewer exercise), T09.04/T09.08 (sign-off capture), T09.05 (tabletop rehearsal + sign-off) — MUST each be emitted as HALT tasks that write PENDING; never auto-fill a date or sign-off line (amalgamation §3 F-P9-2).
  - **F-P9-3:** OPS-003 *vs* OPS-001 ownership of the `return-contract.yaml` troubleshooting recipe (reconcile the roadmap AC 4-vs-5 surfaces) — HALT before mutating the roadmap AC; do not auto-assign ownership (amalgamation §3 F-P9-3).
- Each fix task carries its amalgamation ID, the `file:line` evidence (re-confirm at build time — line numbers are as-of 2026-06-04), and the verifier command from the amalgamation.
- Respect repo rules: edit `src/superclaude/`, never stage `.claude/`; UV only; feature-branch commits only.

## Definition of done for the tasklist
All non-HALT fixes have concrete deliverables + verifier commands; HALT items block their dependents; the
final checkpoint re-runs the per-phase reflects (and `8-rerun`) to confirm regressions cleared.

The re-validation matrix (amalgamation §5) covers P1/P2/P3 (after fixes), P5 (after RW-6), P7 (after F-P7-1),
and P9 (after F-P9-*). The final checkpoint MUST emit one `/sc:reflect --mode post --depth deep` re-run task per
phase (mode `pre` for P9 plan edits), each from cwd=SwarmPost with `--tasklist`/`--spec` pointing at the
absolute release paths and `--output` under `.../validation/deep/<phase>-rerun` — mirroring the Phase-8 re-run
command already given at amalgamation §5 (lines 194-197). Do not rely on the bare "re-run the per-phase reflects"
phrasing to imply commands; emit them explicitly.
