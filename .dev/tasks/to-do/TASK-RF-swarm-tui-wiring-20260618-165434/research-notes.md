# Research Notes: Wire `--tui` into `superclaude swarm run` (Approach A)

**Date:** 2026-06-18
**Scenario:** A (explicit — driving spec with 7 FRs as acceptance contract)
**Depth Tier:** Standard
**Track Count:** 1
**Spec:** `.dev/brainstorms/swarm-tui-wiring/merged-requirements.md`
**start_commit:** `300c06a6d53287893a446db8e859f5f1bc5434d8` (git merge-base HEAD master)
**Integration branch:** origin/master

---

## EXISTING_FILES

Primary change surface:
- `src/superclaude/cli/swarm/commands.py` (3538 lines) — owns `run_cmd` (def at **1471**, Click options 1300-1470). Key seams:
  - Resume branch + `--resume`/`--detached` reject at **1539-1567** (the detached reject the spec cites as "1547" is at **1547-1553**).
  - `--detached` branch (fresh) at **1589-1607** (calls `_launch_detached_run`, returns).
  - CLI-override block (target/output/transport/reviewers/...) at **1609-1694**.
  - Preflight + Logger + state setup at **1696-1792**. Logger built at **1728-1740**.
  - Inline prompt assembly at **1800-1805**.
  - **Fresh-run `dispatch_wave1(...)` blocking call at 1807-1813** (signature: `dispatch_wave1(preflight_result, transport_for_slot=, prompt=, worker_spec=, logger=)`).
  - Post-dispatch normalize_wave2/reduce_wave3 at 1815+ (must continue unchanged after the worker thread joins).
  - **Resume dispatch_wave1 at 2264** (`_run_resume_branch` / `raw_redispatched`) — **EXCLUDED from TUI in v1**.
  - Module constants: `EXECUTION_LOG_JSONL_FILENAME = "execution-log.jsonl"` (**99**), `SWARM_STATE_FILENAME = ".swarm-state.json"` (**85**), `EXIT_USAGE`/`EXIT_INVALID`.
  - `_write_swarm_state(output_dir, state, job_id)` at **692**.
- `src/superclaude/cli/swarm/tui.py` (315 lines) — **already built, likely no change**. `should_enable_tui(flag, stream=None)` (74), `TUI` class with `start()` (218), `stop()` idempotent (230), `update(state, events)` (236), pure `render()` (251), `_project_workers(events)` (145), `WorkerSnapshot`. `TUI.__init__` default `refresh_per_second=2`. `Live(... screen=False)` started at 221 with Rich's default `redirect_stdout/stderr` (the crash trap FR-1 polices).
- `src/superclaude/cli/swarm/logging_.py` (188 lines) — `Logger` dual-format writer. **`from_json` is NOT here** — see GAPS. Docstring references `event-log.jsonl` (generic, stale).
- `src/superclaude/cli/swarm/state.py` (196 lines) — `read_state(path) -> Optional[SwarmState]` (178, returns None when file missing), `write_state`, `confine_path`, `OutputConfinementError`.
- `src/superclaude/cli/swarm/models.py` — **`from_json(cls, payload)` defined at 1820** (NOT logging_.py). `EventRecord` dataclass at **1209** (fields: `event_type`, `timestamp`, `worker_index: Optional[int]`, `payload`). `SwarmState`, `to_json`, `from_dict`.

Test surface:
- `tests/swarm/test_inv012_tui_opt_in.py` (583 lines) — INV-012 guard. Pins gate from 3 angles (subprocess no-ANSI, gate helper, render contract). **The spec calls its grep/AST audit "vacuous" — FR-1 requires tightening it to assert `tui`/`Live`/`Console` reachable from ZERO dispatch/worker functions.**
- `tests/swarm/test_tui.py` (255 lines) — unit tests; `_FakeTTY` class with `isatty()->True` (44), gate tests, `TUI()` lifecycle tests. **Forced-TTY pattern reusable for FR-7 integration test.**
- `tests/swarm/test_commands_run.py` (21657 bytes) — `run_cmd` invocation patterns (CliRunner), reference for integration test scaffolding.
- `tests/swarm/conftest.py`, `tests/swarm/fixtures/` — shared fixtures.

Unchanged by design (C3 / AC-004 / NFR-001):
- `src/superclaude/cli/swarm/dispatch.py` — `dispatch_wave1` signature MUST NOT change.
- `src/superclaude/execution/parallel.py` — `ParallelExecutor` untouched.

## PATTERNS_AND_CONVENTIONS

- **Click options:** `@click.option("--flag", "dest", is_flag=True, default=False, help=...)` immediately above `run_cmd` decorators; `--detached` (1452-1469) and `--force-relens` (1434-1451) are the closest `is_flag` precedents. New `--tui` param appends to `run_cmd(...)` signature (currently ends `detached, auto_inject_guard`).
- **Usage rejects:** `click.echo("swarm run ...: <msg>", err=True)` then `raise click.exceptions.Exit(EXIT_USAGE)`. The resume+detached reject at 1547-1553 is the literal mirror FR-3 D1 asks for.
- **Deferred imports:** dispatch/preflight imported INSIDE `run_cmd` (1526-1527) to keep module load light + circular-import-free. The `tui` import (`TUI`, `should_enable_tui`) should follow the same deferred-import idiom inside the fresh-run path.
- **Threading precedent:** `threading.Lock` in logging_.py; `threading.Thread` in transports/stub.py. Non-daemon `Thread(target=, name="swarm-wave1", daemon=False)` + explicit `join()` per FR-5.
- **Test style:** pytest + `click.testing.CliRunner`; `_FakeTTY` shim for isatty; monkeypatch for gate shimming.

## GAPS_AND_QUESTIONS

1. **[CODE-CONTRADICTED] Event log filename.** Spec FR-4 says tail `event-log.jsonl`. The fresh-run path actually writes events to **`execution-log.jsonl`** (constant `EXECUTION_LOG_JSONL_FILENAME`, commands.py:99 → Logger at 1733). The `_tail_events` helper + FR-7 integration test MUST target `execution-log.jsonl` (resolved from the manifest dir / `EXECUTION_LOG_JSONL_FILENAME`) or the TUI tails a non-existent file and renders zero rows. Researchers: confirm definitively which file dispatch workers append worker_* events to, and whether `state_output_dir`/`manifest_dir` is the directory holding both `execution-log.jsonl` and `.swarm-state.json`.
2. **[CODE-CONTRADICTED] `from_json` import source.** Spec says `from_json` at logging_.py:46 — it's actually defined in **models.py:1820**. The poll loop import is `from superclaude.cli.swarm.models import from_json` (or reuse already-imported `_from_dict`). Confirm signature `from_json(cls, payload)`.
3. **Worker-event population on stub transport.** FR-7 needs ≥1 non-vacuous worker row. Confirm the stub transport path actually emits `worker_start`/`worker_done` EventRecords to the jsonl during a fresh `--lens bare-review --transport stub` run (so the integration test can assert a populated table without the live proxy). Researchers: trace dispatch._run_worker → logger.log_event for stub.
4. **state file read path.** `read_state` takes a path to `.swarm-state.json`. Confirm the poll loop computes `state_output_dir / SWARM_STATE_FILENAME` and that this is set on the fresh-run path (gated on `preflight_result.manifest_path`). What happens when `state_output_dir is None` (spec-only smoke path, no `--output`)? TUI gate likely should also require an output dir.
5. **Forced-TTY in CliRunner.** How does the FR-7 test force `should_enable_tui()->True`? Options: monkeypatch `commands.should_enable_tui` to return True, OR feed a `_FakeTTY`. Researchers: determine the cleanest seam given the helper is consulted inside `run_cmd` against `sys.stdout`.
6. **Iteration ceiling.** FR-4 mentions an optional iteration ceiling "mirroring `watch_max_iterations`". Locate that precedent (likely `swarm logs --follow` / status). Decide whether v1 needs it (anti-spin guard).
7. **KeyboardInterrupt path (FR-6).** Confirm `finally: tui.stop()` covers SIGINT and that the non-daemon join doesn't hang on Ctrl-C. Determine expected exit code on interruption.

## RECOMMENDED_OUTPUTS

5 research files in `research/`:
- `01-run-cmd-seam.md` (File Inventory + insertion points)
- `02-reader-contracts.md` (Integration: read_state, from_json, EventRecord, EXECUTION_LOG_JSONL_FILENAME, _project_workers, should_enable_tui, dispatch_wave1 signature)
- `03-patterns-conventions.md` (Click/UsageError/threading/deferred-import patterns)
- `04-template-examples.md` (MDTM template 02 + prior task examples)
- `05-test-verification.md` (test_inv012 vacuity analysis, test_tui forced-TTY pattern, test_commands_run scaffolding, stub-transport event emission, AST/grep audit approach for FR-1)

## SUGGESTED_PHASES

- R1 File Inventory → `01-run-cmd-seam.md`: enumerate exact line anchors in commands.py for the option block, run_cmd signature, resume+detached guard, fresh detached branch, override block, Logger/state setup, **fresh dispatch_wave1 call (1807)**, post-dispatch continuation, resume dispatch (2264, excluded). Other researchers cover reader contracts + tests.
- R2 Integration Points → `02-reader-contracts.md`: verify read_state/from_json/EventRecord/_project_workers/should_enable_tui/TUI lifecycle signatures + the **execution-log.jsonl vs event-log.jsonl** filename truth + dispatch_wave1 exact signature (C3 no-change proof). Covers reader/consumer contracts only.
- R3 Patterns & Conventions → `03-patterns-conventions.md`: Click is_flag option idiom, UsageError reject idiom (mirror 1547), deferred-import idiom, threading.Thread non-daemon precedent, byte-offset tail idioms in repo. Covers code style only.
- R4 Template & Examples → `04-template-examples.md`: read `.claude/templates/workflow/02_mdtm_template_complex_task.md` PART 1 (A3/A4/B2), survey `.dev/tasks/to-do/` examples. Covers template only.
- R5 Test & Verification → `05-test-verification.md`: dissect test_inv012 vacuity, extract test_tui `_FakeTTY` + lifecycle patterns, test_commands_run CliRunner scaffolding, trace stub-transport worker-event emission to jsonl, AST/grep approach for FR-1 reachability audit, partial-line truncation fixture for FR-4. Covers tests only.

## TEMPLATE_NOTES

- **Template 02** (complex): work has discovery + build + test + verify phases; multiple coupled FRs with non-negotiable gates (FR-1 single-writer, FR-5 exception-not-masked). Not a direct transformation → not Template 01.
- **Tier Standard:** 4 source files + test files, moderate complexity, single subsystem (swarm CLI). Not Deep (no multi-subsystem / multi-track). Not Quick (>5 files when tests counted, coupled invariants, gate tests).
- Generated tasklist should carry: granular per-FR items (FR-1..FR-7 each → its own implementation + verification item), the `--tui` option add, the `_tail_events` helper, the two scope guards, the FR-1 audit tightening, the FR-7 integration test. POST reflect gate ENABLED. PRE reflect gate consumes `--spec`.

## AMBIGUITIES_FOR_USER

None blocking — intent is clear from the spec's 7 FRs and the recommended Approach A code sketch. The two `[CODE-CONTRADICTED]` items (event-log vs execution-log filename; `from_json` location) are codebase-resolvable, not user-intent questions — researchers resolve them and the builder uses the CODE-VERIFIED filename/import, NOT the spec's stale references.
