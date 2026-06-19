# A.10 Structural Validation — Consolidated Findings (for single fix agent)

Source reports: `qa-task-validation-b2-report.md` (B2 self-containment), `qa-task-validation-structure-report.md` (phase structure).
Both verdicts: FAIL. Consolidated fix list below. Apply ALL.

## FIX-1 (IMPORTANT) — Add the missing FR-3 resume+`--tui` reject
The driving spec FR-3 has TWO non-negotiable acceptance criteria:
1. `--tui --detached` MUST raise UsageError before dispatch (IMPLEMENTED — Step 2.3).
2. `--tui` on a resume / non-fresh invocation MUST be rejected — "both invocations exit with UsageError naming the incompatibility; the resume path with --tui does not spawn the TUI loop." (MISSING.)

The task currently implements only criterion 1 and lets `--tui` on a resume run silently no-op. That drops half of FR-3 while the frontmatter/overview claim "Implements FR-1..FR-7".

FIX: Add a new implementation item in Phase 2 (e.g. **2.3b**) that rejects `--tui` when `resume_job_id is not None`. Place it inside / adjacent to the resume branch guard block in `src/superclaude/cli/swarm/commands.py` (the resume branch begins `if resume_job_id is not None:` ~line 1539; the resume+detached reject is ~1547-1553). The new reject mirrors that idiom:
`click.echo("swarm run --tui: --tui is not supported with --resume (v1 scope = fresh-run only; resume does not enter the TUI loop)", err=True)` then `raise click.exceptions.Exit(EXIT_USAGE)`, placed BEFORE `_run_resume_branch(...)` is called so the resume path never spawns the TUI loop. Self-contained item (context+action+output+verification+completion gate). Add a matching test assertion (extend the FR-3 reject test or the FR-7 file) that `swarm run --resume <id> --tui --output <dir>` exits EXIT_USAGE (2) naming the incompatibility. Update any "resume excluded" wording so it reads "resume + --tui is REJECTED (UsageError)", not "silently ignored".

## FIX-2 (IMPORTANT) — POST reflect gate must be penultimate
Current Post-Completion order: POST reflect gate (L279) → Task Summary write (L281) → status→Done (L283). The Task Summary write is interposed between the reflect gate and the Done flag, violating the "reflect gate immediately before status→Done" rule.

FIX: Reorder the Post-Completion items so the sequence ends: `… → Task Summary write → POST reflect gate → status→Done`. Move the Task Summary item to BEFORE the POST reflect gate item. The reflect gate stays exit-0-only and the status→Done item stays last (anti-orphaning preserved). Do not alter the reflect wrapper command itself.

## FIX-3 (MINOR) — Pin test-file destinations
Steps 3.2/3.4/3.5/3.6/3.8 leave the destination as `<chosen file>`. Pin concrete paths so each item is self-contained:
- FR-1 audit tightening → `tests/swarm/test_inv012_tui_opt_in.py` (existing file, tighten in place).
- FR-1 runtime main-thread probe → `tests/swarm/test_inv012_tui_opt_in.py` or `tests/swarm/test_run_tui_integration.py` (pick one, pin it).
- FR-2 no-regression, FR-5 exception-not-masked, FR-6 teardown, FR-7 integration, no-signature-change → consolidate into a NEW file `tests/swarm/test_run_tui_integration.py` (FR-2/FR-5/FR-6/FR-7/no-sig), and FR-4 `_tail_events` unit test → `tests/swarm/test_run_tui_integration.py` or a focused `tests/swarm/test_tail_events.py`. Pin each item's destination explicitly (no `<chosen file>` placeholders remain). Ensure no two items silently target the same undefined file.

## FIX-4 (MINOR) — Justify the dense item 2.5
Item 2.5 (threaded-dispatch + poll + finally + re-raise glue) is a ~3400-char single item with 5 sub-edits. It IS semantically atomic (one coherent refactor of one function in one file, `commands.py`), so it need not be split. Add a one-line TB-Add-5 justification comment to the item, e.g. `<!-- TB-Add-5: single atomic refactor of run_cmd's fresh-run dispatch block in commands.py; the 5 sub-edits (import, thread wrapper, gate, poll loop, finally/re-raise) are interdependent and must land together to keep the function compiling -->`.

## NON-ISSUES (no action)
- Key Constraints file:line citations inside `## Execution Context` — out of TB-Add-7 scope (which validates Source Areas only; that sub-block is clean and contains no file:line). Observational only.
- Frozen `dispatch_wave1` kwargs, no stale-spec propagation (execution-log.jsonl + models.py from_json), DAG deps, frontmatter completeness, reflect wrapper NFR-7-clean form — ALL verified clean by both agents.

After applying FIX-1..FIX-4, re-verify: item count grows by 1-2 (the 2.3b reject + possibly a resume-reject test), POST reflect gate is penultimate, no `<chosen file>` placeholders remain, frontmatter "Implements FR-1..FR-7" is now true for all of FR-3.
