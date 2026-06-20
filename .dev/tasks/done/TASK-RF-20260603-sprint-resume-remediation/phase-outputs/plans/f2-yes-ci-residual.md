# F-2 `--yes`/CI Residual (F-1 surface, gated by CG-4)

**Date:** 2026-06-03
**CG-4 ruling at time of writing:** `RULING: PENDING` (see `phase-outputs/plans/cg4-ruling.md`)

## What the F-2 fix covers

The F-2 remediation (Steps 3.3–3.5) surfaces the half-written partial-work paths via:
- `BoundaryReport.partial_paths` (populated unconditionally in `integrity.run()` when partial work exists), and
- a new print loop in `_print_resume_decision` (`commands.py`).

`_print_resume_decision` is called on exactly two paths, BOTH report-only:
- the `--dry-run` path, and
- the interactive-confirm path (`not assume_yes` AND stdin is a TTY).

So the partial paths are now shown to the operator on the dry-run and interactive paths.

## What the F-2 fix does NOT cover (the residual)

Per research `03-planner-commands-f4.md` §4, when `assume_yes` is True (`--yes`, or
`SUPERCLAUDE_SPRINT_ASSUME_YES`, or `CI`), `_auto_resume` returns `action="proceed"` directly
(`commands.py:469-471`) and **`_print_resume_decision` is NEVER called** on that path. Therefore on
the bare `--yes`/CI proceed path the partial paths are still neither printed nor prompted — the
operator's standing `--yes` is uninformed about the specific half-written artifacts.

This is precisely the **F-1 residual safety gap** identified in REPORT.md:37-39 (the F-1 × F-2
interaction). Its remediation is **CONDITIONAL on the CG-4 ruling**:

- **IF `RULING: NO`** (§4(c)/FR-2.4 govern, tighten the gate): F-1 requires tightening the
  `--yes`/CI gate — e.g. add `--accept-partial`, default STOP-on-partial under `--yes`, and/or
  surface the paths to stderr even on the `--yes` proceed path. This is a follow-up task (the
  decision record defers the `--accept-partial` code change to F-1).
- **IF `RULING: YES`** (§7 governs, F-1 as-designed): the `--yes` path intentionally proceeds; F-2
  path-surfacing on the dry-run/interactive paths is the agreed "informedness" fix and the `--yes`
  proceed path is accepted as a pre-authorized unattended path. No further `--yes`-path change.

## Scope statement

**This task does NOT implement any unconditional `--yes`-path change.** With CG-4 PENDING, neither
ruling is adopted, so no gate-tightening or `--yes`-path print was added. The F-2 fix is limited to
the report-only (dry-run + interactive) surfaces, exactly as scoped. No fabricated code change.
