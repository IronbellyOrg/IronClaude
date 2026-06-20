# QA Report — Task-Integrity Gate (Stage 1)

**Topic:** Sprint CLI per-task wiring + runner-owned typed HandoffRecord — Stage 1 (Phase 3, Steps 3.1–3.18)
**Date:** 2026-06-03
**Phase:** task-integrity
**Fix cycle:** N/A (cycle 1)
**Mode:** adversarial, fix_authorization: true

---

## Overall Verdict: PASS

Zero-trust re-derivation: every criterion was checked against the real source on
disk (Read/Grep), tests were re-run independently, and lint was re-run. No issues
of any severity found; no fixes required.

---

## Per-Criterion Checklist (1–9)

### 1. H4 schema — PASS

`HandoffRecord` at `models.py:270-376`.

- Field NAME + ORDER match SYNTHESIS H4 verbatim: `schema_version, task_id, phase,
  status, gate_outcome, turns_consumed, exit_code, output_path, started_at,
  finished_at, produced_artifacts, consumed_upstreams` (`models.py:288-299`).
  Verified against the H4 code block at `SYNTHESIS.md:116-130`. Note: H4's source
  block lists `output_path` after `exit_code` and before `started_at` — the
  implementation matches this exactly (`models.py:295`).
- `schema_version: int = 1` default (`models.py:288`).
- List fields use `field(default_factory=list)` (`models.py:298-299`).
- `gate_outcome: str` is the GateOutcome `.value` string, NOT `dict|None`
  (`models.py:292`, docstring `models.py:282-285`). The H4 [CORRECTED v2] fix at
  `SYNTHESIS.md:122` is honored.
- `to_dict` is hand-written (explicit dict literal, NOT `dataclasses.asdict`)
  with `list(...)`-copied list fields (`models.py:301-320`).
- `from_dict` uses `data.get(key, default)` for every field, so an unknown key
  round-trips without raising (`models.py:322-344`). Confirmed by
  `test_handoff_record.py::test_from_dict_tolerates_unknown_future_field`.
- `from_task_result` derives `status` via `result.status.value`, `gate_outcome`
  via `result.gate_outcome.value`, timestamps via `.isoformat()`
  (`models.py:363-376`). Matches `TaskResult.to_dict` derivation at
  `models.py:201,204-205,207`.

### 2. FileHandoffStore atomicity — PASS

`FileHandoffStore` at `handoff.py:23-51`.

- `write` replicates the `checkpoints.write_manifest` idiom (`checkpoints.py:207-210`)
  verbatim: `path.parent.mkdir(parents=True, exist_ok=True)` →
  `tmp = path.with_suffix(path.suffix + ".tmp")` →
  `tmp.write_text(json.dumps(record.to_dict(), indent=2) + "\n")` →
  `tmp.replace(path)` (`handoff.py:36-40`). Trailing newline present.
- `read(missing)` returns `None` (does not raise) — `handoff.py:48-51` guards on
  `path.exists()`. Confirmed by `test_handoff_store.py::test_read_missing_returns_typed_none`.
- On-disk key is exactly `<results_dir>/handoff/phase-{N}-task-{task_id}.json` via
  `SprintConfig.handoff_file` (`models.py:683-689`):
  `self.results_dir / "handoff" / f"phase-{phase.number}-task-{task.task_id}.json"`.
  Confirmed by `test_handoff_store.py::test_on_disk_key_is_phase_qualified` and
  `::test_write_leaves_no_tmp_file`.

### 3. H3 reconciliation — PASS

`write_task_complete` at `logging_.py:221-244`.

- Emits `event: "task_complete"` (`logging_.py:236`).
- Field set/order mirrors `write_task_rerun_complete` (`logging_.py:205-219`)
  EXACTLY: `event, phase, task_id, status, turns, duration_sec, timestamp`
  (`logging_.py:236-243` vs `logging_.py:210-218`).
- Documented as the first-run discriminator (`logging_.py:224-233`): `task_complete`
  = first run, `task_rerun_complete` = rerun; both schemas frozen side-by-side.
- `status` typed `str` (`logging_.py:222`); caller passes `result.status.value`
  (`executor.py:1116`).
- Distinctness confirmed by `test_stage1_wiring.py::test_task_complete_event_emitted_and_distinct`
  (asserts exactly one `task_complete` and zero `task_rerun_complete`).

### 4. M3 context injection — PASS

- `build_task_context` exists (`process.py:306`) and produces a `## Prior Task
  Context` block (`process.py:335`).
- `_run_task_subprocess` gained `prior_context: str = ""` param (`executor.py:1160`)
  and appends it to the prompt when non-empty (`executor.py:1178-1179`); the
  single-task directive `Execute task {task.task_id}` is retained (`executor.py:1174`).
- `execute_phase_tasks` computes `prior_context = build_task_context(results,
  start_commit="")` in the parent (`executor.py:1040`) and passes it through
  (`executor.py:1050`). `start_commit=""` runs in-parent, no logger needed.
- Proven to REACH the prompt by `test_stage1_wiring.py::test_prior_context_reaches_per_task_prompt`
  (spy `ClaudeProcess.__init__` captures the prompt; asserts `## Prior Task Context`,
  the prior task id `T01.01`, and the single-task directive all appear) and
  `::test_execute_phase_tasks_threads_prior_context` (first task gets `""`, second
  task gets the context block).

### 5. M4 flag plumbing — PASS

Three-layer `--handoff` plumbing, all defaulting to `True`:

- `commands.py:190-194` — `@click.option("--handoff/--no-handoff", "handoff_enabled",
  default=True, ...)`; `run()` param `handoff_enabled: bool` (`commands.py:214`);
  passed into `load_sprint_config(..., handoff_enabled=handoff_enabled)`
  (`commands.py:251`).
- `config.py:295` — `load_sprint_config(..., handoff_enabled: bool = True)`;
  forwarded into `SprintConfig(..., handoff_enabled=handoff_enabled)` (`config.py:364`).
- `models.py:573` — `SprintConfig.handoff_enabled: bool = True`.
- `handoff_store` default `"file"` at `models.py:574`. Per SYNTHESIS M4
  (`SYNTHESIS.md:179`) store-select is "config/internal" for Stage 1, so the field
  default (not a CLI flag) is the correct surface — confirmed acceptable.

### 6. M5 legacy-exact — PASS

- The `execute_sprint` call site gates BOTH the store and the journal logger on
  `handoff_enabled` (`executor.py:1388-1393`): `_handoff_store = FileHandoffStore(config)
  if config.handoff_enabled and config.handoff_store == "file" else None`;
  `_handoff_logger = logger if config.handoff_enabled else None`. Both passed into
  `execute_phase_tasks` (`executor.py:1403-1404`).
- In the loop, the journal write is guarded `if logger is not None`
  (`executor.py:1112`) and the handoff write `if handoff_store is not None`
  (`executor.py:1120`) — so with `handoff_enabled=False` both are inert.
- `test_handoff_backward_compat.py::test_handoff_off_is_legacy_exact` asserts: no
  records under `<results_dir>/handoff/`, no `task_complete` events in the JSONL,
  and `post_threads <= baseline_threads + 1` (+0 daemon-thread parity).
- Positive control `::test_handoff_on_does_write_records_and_events` proves
  handoff=on writes exactly 2 records (`phase-1-task-*.json`) AND 2 `task_complete`
  events on the same sprint.

### 7. M6 warn-only router — PASS

- `_parse_phase_tasks` (`executor.py:1215-1247`) adds a SEPARATE near-miss probe
  using a NEW regex `_TASK_HEADING_NEAR_MISS_RE = re.compile(r"#{2,5}\s*T\d{1,2}[._]\d{1,2}",
  re.MULTILINE)` (`executor.py:61`). The probe runs only after `parse_tasklist`
  returns falsy (`executor.py:1229-1238`), emits `_routing_logger.warning(...)`
  (`executor.py:1239-1246`), and RETURNS `None` unchanged (`executor.py:1247`) — no
  reclassification.
- `config._TASK_HEADING_RE` (`config.py:382`) is NOT modified — it remains the
  strict extraction regex; the M6 probe is a wholly separate diagnostic regex in
  `executor.py`.
- Legitimately-freeform phases produce no warning (the loose probe finds no
  `T<PP>.<TT>`-like text) — confirmed by the corpus.
- `test_stage1_wiring.py::test_m6_heading_router_corpus` drives a 12-entry corpus
  (3 correct strict → tasks/no-warn; 7 near-miss → Path A/None + warn; 2 freeform →
  Path A/None/no-warn) asserting route AND warning expectation for each; nothing is
  reclassified (near-miss cases route to `None` exactly as freeform does).

### 8. M7 migration-safe — PASS

- `HandoffRecord` is versioned (`schema_version: int = 1`, `models.py:288`) and
  `from_dict` tolerates a newly-added unknown field via `.get` (`models.py:331-344`).
- `test_handoff_record.py::test_from_dict_tolerates_unknown_future_field` injects an
  extra key `a_field_from_the_future` and proves `from_dict` does not raise and the
  known fields survive; `::test_schema_version_present_and_defaults_to_one` proves
  default + missing-key degradation to 1.

### 9. No-regression — PASS

- Independently re-ran the Stage-1 suite: `144 passed, 5 failed` (matches
  `stage1-tests.md` exactly).
- The 5 failures are ALL on the pre-change baseline list
  (`pre-change-baseline.md:58-62`), all with the documented `.stdin` harness
  root cause (`_PassPopen`/`_HaltPopen`/etc. lack a `.stdin` attribute, hit via the
  Path A single-session fallback in `execute_sprint`). NONE are in the Path B
  per-task code this stage wires. Zero regressions.
- `make lint` re-run: `All checks passed!` (exit 0).

---

## Confidence

**Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 12 | Grep: 4 | Glob: 0 | Bash: 3

All 9 criteria marked [x] VERIFIED with cited file:line evidence and (where
applicable) independent test/lint re-runs. No web research was required (all
claims are local-source-bound).

---

## Summary

- Checks passed: 9 / 9
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0

## Issues Found

None. (Adversarial-stance note: I specifically probed the highest-risk spots —
the H4 field ORDER vs the spec block, the `gate_outcome` enum-`.value`-not-dict
fix, the M5 double-gating of store AND journal, the M6 separate-regex requirement
with `_TASK_HEADING_RE` left untouched, and the no-regression baseline match. All
held under scrutiny.)

## Actions Taken

None required — implementation is correct as-is.

## Recommendations

Green light to proceed to Phase 4 (Stage 2 — resume contract). One forward-looking
note for the Stage-2 reviewer (NOT a Stage-1 defect): Step 3.10/M4 deliberately
does NOT thread `handoff_store` through the CLI/config layers (it is a
config/internal field per `SYNTHESIS.md:179`); Stage 4 (out of scope) owns the
"mail" selector. This is correct for Stage 1.

## QA Complete
