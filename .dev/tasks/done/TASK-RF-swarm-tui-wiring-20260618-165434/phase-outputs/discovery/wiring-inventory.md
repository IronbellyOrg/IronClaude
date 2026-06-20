# Wiring-Site Inventory — `--tui` into `swarm run`

**Generated:** 2026-06-18 (Step 1.3)
**Production file (ONLY one modified):** `src/superclaude/cli/swarm/commands.py`
**Confirmation method:** Read each anchor against the CURRENT file contents.
**Drift verdict:** ZERO drift — every CURRENT line number matches `research/01-run-cmd-seam.md` exactly.

## Module-level constants (confirmed)

| Constant | Confirmed line | Value |
|---|---|---|
| `SWARM_STATE_FILENAME` | 85 | `".swarm-state.json"` |
| `EXECUTION_LOG_JSONL_FILENAME` | 99 | `"execution-log.jsonl"` |
| `EXECUTION_LOG_MD_FILENAME` | 100 | `"execution-log.md"` |
| `EXIT_OK` | 188 | `0` |
| `EXIT_INVALID` | 189 | `1` |
| `EXIT_USAGE` | 190 | `2` |

All module-scope, import-free. No deferred import needed for `EXIT_USAGE`.

## Insertion sites (in execution order)

| # | Site | Confirmed anchor | Edit to make (Step) |
|---|---|---|---|
| 1 | `--detached` option block | 1452–1469 (ends 1469) | Insert `@click.option("--tui", "tui", is_flag=True, default=False, help=(...))` AFTER 1469, BEFORE `@auto_inject_guard_option` @1470 (Step 2.1) |
| 2 | `@auto_inject_guard_option` (LAST decorator) | 1470 | Must remain last; `--tui` goes above it (Step 2.1) |
| 3 | `def run_cmd(` signature | 1471; `detached: bool,` @1484; `auto_inject_guard: bool,` @1485; `) -> None:` @1486 | Insert `tui: bool,` between 1484 and 1485 (Step 2.2) |
| 4 | Docstring flow narrative | 1487–1521 (narrative 1506–1520) | Add `--tui` mention near step 4 (Step 2.2) |
| 5 | Resume branch open | `if resume_job_id is not None:` @1539 | Context for Step 2.3b |
| 6 | Resume+detached reject (idiom to mirror) | 1547–1553 | Copy `click.echo(..., err=True)` + `raise click.exceptions.Exit(EXIT_USAGE)` shape (Steps 2.3/2.3b) |
| 7 | `--output` required reject | 1554–1560 | Boundary; `--resume --tui` reject goes after 1553, before `_run_resume_branch` @1561 (Step 2.3b) |
| 8 | `_run_resume_branch(...)` call | 1561–1566; resume `return` @1567 | `--resume --tui` reject must fire BEFORE this (Step 2.3b) |
| 9 | `force_relens` trap | 1573–1579 | Context only (not modified) |
| 10 | `mode, spec_dict = _resolve_input_mode(...)` | 1581 | `if tui and detached:` reject inserted right AFTER 1581, BEFORE `if detached:` @1589 (Step 2.3) |
| 11 | Fresh `if detached:` branch | 1589; `return` @1607 | Returns before dispatch → the `--tui --detached` guard MUST fire before it (Step 2.3) |
| 12 | `state_output_dir` init | `Optional[Path] = None` @1726; assigned `manifest_dir` @1731 inside `if preflight_result.manifest_path:` @1727 | Poll-loop read root; gate on `state_output_dir is not None` (Step 2.5) |
| 13 | Logger construction | 1732–1740 (`jsonl_path=manifest_dir/"execution-log.jsonl"` @1733) | Confirms log dir == `state_output_dir` (Step 2.5) |
| 14 | Fresh `dispatch_wave1(...)` call | 1807–1813; result name `worker_results` | Wrap in non-daemon thread closure; verbatim kwargs `transport_for_slot=run_transport_factory, prompt=assembled_prompt, worker_spec=inline_job.workers, logger=logger` (Step 2.5) |
| 15 | Post-dispatch continuation (first active line) | `recipe_name = inline_job.normalization.recipe` @1826; normalize/reduce 1827–1836+ | Must run only AFTER join + post-stop re-raise; consumes `worker_results` (Step 2.5) |
| 16 | New `_tail_events` helper | near private log helpers (precedent `_follow_log`/`_drain_appended` ~2737/~2834) | Add module-level `_tail_events(path, offset)` (Step 2.4) |
| 17 | Resume `dispatch_wave1` — DO NOT TOUCH | ~2264 (inside `_run_resume_branch` @2048) | LEFT UNTOUCHED in v1 |

## Notes

- `state_output_dir` is `None` on the no-`--output` spec-only smoke path → TUI gate must require `state_output_dir is not None` AND `should_enable_tui(...)`.
- Both `execution-log.jsonl` and `.swarm-state.json` are siblings of `manifest.json` in `state_output_dir` (== `manifest_dir` == `Path(preflight_result.manifest_path).parent`).
- The fresh `--detached` branch `return`s @1607 before dispatch, so the `--tui --detached` reject must precede it (placed after `_resolve_input_mode` @1581).
