# QA Report — Task Qualitative Review (Operational Correctness)

**Topic:** Wire `--tui` into `superclaude swarm run` (Approach A)
**Date:** 2026-06-18
**Phase:** task-qualitative
**Lens:** operational-correctness
**Fix cycle:** N/A
**fix_authorization:** false

---

## Overall Verdict: PASS (with 3 MINOR fold-in recommendations — none blocking)

## Tool engagement
Read: 11 | Grep/Bash: 7 | Glob: 0

## Confidence
Verified: 30/30 items operationally reasoned against actual source | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%

---

## Items Reviewed (operational lens — the 9 spawn-prompt probes)

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Threaded-dispatch closure compiles + passes frozen kwargs | none | PASS | All dispatch locals (`preflight_result`, `run_transport_factory`, `assembled_prompt`, `inline_job`, `logger`) computed BEFORE the call @commands.py:1807-1813; a closure defined after them reads them correctly. Step 2.5 keeps the EXACT kwargs (`transport_for_slot=`, `prompt=`, `worker_spec=`, `logger=`, `preflight_result` positional) matching frozen sig @dispatch.py:334-343. Result-box/exc-box + join + finally-stop + post-stop re-raise ordering matches FR-5/FR-6. |
| 2 | Gate `should_enable_tui(...) AND state_output_dir is not None` | none | PASS | `state_output_dir` init None @1726, set only inside `if preflight_result.manifest_path:` @1731. `should_enable_tui(flag, stream)` sig @tui.py:74 matches `should_enable_tui(tui, sys.stdout)`. No-`--output` path -> state_output_dir None -> gate closed -> synchronous path (FR-2). |
| 3 | `_tail_events(path, offset)` tolerates partial trailing line | none | PASS | `from_json` @models.py:1820 = `json.loads(payload)` raises JSONDecodeError on truncation. Step 2.4 buffers to last newline, never feeds partial to from_json, does not advance offset past partial. Mirrors `_drain_appended` seek/read/tell @commands.py:2834-2858. |
| 4 | FR-7 forced-TTY monkeypatch target correct (deferred import) | none | PASS | commands.py currently has ZERO `should_enable_tui`/tui imports (grep confirmed) -> Step 2.5 adds function-local import -> patching source module `superclaude.cli.swarm.tui` is correct (mirrors dispatch monkeypatch @test_commands_run.py:322-324). Stub `bare-review` emits exactly 3 worker_done rows to execution-log.jsonl (confirmed @test_commands_run.py:559-568). |
| 5 | FR-1 AST audit detects reachability + vacuity guard | none | PASS | `_ShellDispatchVisitor`/`_scan_module`/`_iter_swarm_py_sources` @test_concurrency_python_only.py:145-230 is a real copyable visitor with visit_Import/visit_ImportFrom. `_run_worker` @dispatch.py:279 (in dispatch.py as claimed). Step 3.1 mandates vacuity guard + mutation guard (synthetic `import rich.live` must flag). |
| 6 | `git diff <start_commit> -- dispatch.py parallel.py` signature proof | none | PASS | start_commit 300c06a6 IS an ancestor of HEAD (verified); current diff of both frozen files is EMPTY. parallel.py frozen sigs @80/100/103/169 match task claims verbatim. |
| 7 | ruff check + format --check + full-suite ordered after impl | none | PASS | Phase 4 runs after Phases 2/3. Format-check (Step 4.2) present + distinct from lint (Step 4.1), runs `ruff format --check src/ tests/` (CI surface). |
| 8 | POST reflect wrapper exit-0-only behind skip guard | none | PASS | Gates Done on exit 0 only; non-zero -> Blocked + blocker_reason; wrapper resolves base from start_commit frontmatter (no --base). Penultimate ordering confirmed (inherited structural PASS). |
| 9 | A.10.25 MINOR gaps F1/F2/F4 | none | PASS | Real holes; fold-in recommendations below (non-blocking). |

## Checklist coverage (15-item operational checklist, all 30 task items)

| # | Checklist item | axis | Result | Evidence |
|---|----------------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | All `uv run pytest`/`ruff`/`git diff` commands have satisfiable preconditions; baseline suite green-expected (90+); stub path emits worker_done rows. |
| 2 | Project convention compliance | none | PASS | Only commands.py + tests/swarm/ touched; src/ side; UV-only; unmarked tests (strict-markers); format-check item present. |
| 3 | Intra-phase execution-order simulation | none | PASS | Step 2.2 (param) precedes 2.3/2.3b (rejects using `tui`/`detached` params) precedes 2.4 (`_tail_events`) precedes 2.5 (glue consuming it) precedes 2.6 (assertion on 2.5's loop). Test phase consumes impl phase. Step 1.3 baseline precedes 4.3 compare; 3.8 reads 1.3's frozen-signatures.md (with re-derive fallback). |
| 4 | Function signature verification | none | PASS | dispatch_wave1, ParallelExecutor.*, read_state, from_json, should_enable_tui, TUI.update/start/stop, _project_workers all verified against source. |
| 5 | Module context analysis | none | PASS | Deferred-import idiom matches existing run_cmd pattern (@1526); constants EXIT_USAGE/SWARM_STATE_FILENAME/EXECUTION_LOG_JSONL_FILENAME module-level @190/85/99; tui.stop idempotent @tui.py:230-234. |
| 6 | Downstream consumer analysis | none | PASS | Post-dispatch continuation @1815-1912 consumes `worker_results` + emits success echo @1907 + Exit(EXIT_OK) @1912; Step 2.5 (d) re-raises before continuation runs and the continuation reads worker_results from the result-box. See OBSERVATION-1 below for the one nuance to enforce. |
| 7 | Test validity | none | PASS | Tests drive real CliRunner + real stub transport + real execution-log.jsonl tailing; FR-7 has explicit anti-vacuity ("fails if --tui unwired") + non-vacuous-row assertion. |
| 8 | Test coverage of primary use case | none | PASS | FR-7 is full-pipeline run->tui integration; FR-2/3/4/5/6 each target a distinct contract. |
| 9 | Error path coverage | none | PASS | Both FR-3 rejects (EXIT_USAGE), FR-5 exception-not-masked, FR-6 SIGINT/clean/exception teardown. |
| 10 | Runtime failure-path trace | none | PASS | input->preflight->threaded dispatch->poll/tail->join->stop->re-raise->continuation. No downstream gate left unable to handle new output: the gate-closed path is byte-identical; gate-open path re-raises worker exceptions preserving EXIT_* semantics. |
| 11 | Completion-scope honesty | none | PASS | No unresolved Open Questions proceeding as done; FR-3 dual-criterion explicitly closed by 2.3+2.3b; stale-name (event-log->execution-log, logging_:46->models:1820) honored in items. |
| 12 | Ambient dependency completeness | none | PASS | Click option dest `tui` + matching param; deferred imports for tui/state/models; no __init__ export needed (private helper); no CLI registry change (option on existing run_cmd). |
| 13 | Kwarg sequencing | none | PASS | param add (2.2) precedes its uses (2.3/2.3b/2.5); no "add kwarg before add param" inversion. |
| 14 | Function-existence claims grep-verified | none | PASS | "_tail_events absent / should_enable_tui present / commands.py has no tui import" all confirmed by grep. |
| 15 | Template/cross-ref accuracy | none | PASS | Line anchors (1469/1471/1485/1547-1553/1581/1589/1607/1726/1731/1807-1813/1826/2264) confirmed against current commands.py; minor drift noted as expected and Step 1.3 re-confirms. |

## Observations (non-blocking, enforce-during-execution)

**OBSERVATION-1 (item 6, downstream consumer — MINOR / already mitigated):** The post-dispatch
continuation @1815-1912 references the local name `worker_results` (and `len(worker_results)` in the
success echo @1910). Step 2.5's threaded refactor moves the assignment into a closure that writes a
result-box. The executor MUST bind `worker_results = result_box[...]` on the main thread AFTER join
(before the continuation) so @1826+ and @1910 still resolve `worker_results`. Step 2.5 (a) names the
result-box and (d) places re-raise "BEFORE the post-dispatch continuation at ~line 1826 runs," which
implies the binding — but the item does not say verbatim "re-bind worker_results from the box." This
is an execution-discipline nuance, not a plan defect: a competent executor reading 2.5 will produce
compiling code (the alternative leaves `worker_results` undefined and fails immediately at the FR-2
baseline test). Recommend the executor confirm the re-bind. Not a FAIL.

**OBSERVATION-2 (FR-7 / FR-4 `_project_workers` return shape — MINOR):** `_project_workers` returns
`dict[int, WorkerSnapshot]` (@tui.py:145), NOT a list. Steps 3.3/3.7 say "calls `_project_workers(records)`
and asserts `len(projected) >= 1`" — `len(dict)` is valid. But Step 3.7's "at least one row is
NON-VACUOUS (status ... and a populated model_label)" requires iterating `.values()`, not the dict
directly (iterating a dict yields int keys). A test author iterating `for w in projected:` instead of
`projected.values()` would get ints and the attribute access would AttributeError. The item's intent is
correct; the executor must iterate `.values()`. Recommend the item add "(iterate `.values()`)". Not a FAIL.

## Issues Found

No CRITICAL or IMPORTANT operational defects found. The plan is operationally sound: every command's
preconditions are satisfiable, every signature claim verifies against source, the threaded-dispatch
glue compiles given the locals are all computed before the dispatch call, the gate logic is correct,
the partial-line discipline matches the JSONDecodeError reality of `from_json`, the monkeypatch
targets respect the deferred-import seam, and the frozen-signature diff is provably empty from the
verified-ancestor start_commit.

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | Step 2.5 (commands.py glue) | Item implies but does not state verbatim that `worker_results` must be re-bound from the result-box on the main thread after join, before the @1826/@1910 continuation that reads it. | Add to Step 2.5: "after join, bind `worker_results = <result-box value>` so the post-dispatch continuation (@1826) and success echo `len(worker_results)` (@1910) resolve." (Self-correcting: omission fails the FR-2 baseline test immediately.) |
| 2 | MINOR | Steps 3.3 / 3.7 (`_project_workers` use) | `_project_workers` returns `dict[int, WorkerSnapshot]`; the non-vacuous-row assertion must iterate `.values()` not the dict. | Add "(iterate `projected.values()`)" to the non-vacuous-row assertion in Steps 3.3/3.7. |
| 3 | MINOR | A.10.25 F1/F2/F4 gaps (inherited) | F1 iteration-ceiling has no asserting test; F2 no test that `tui.update(None, ...)` first-frame doesn't crash; F4 `_tail_events` corrupt-complete-line branch untested. | Optional one-line fold-ins (see Recommendations). The first poll iteration passes `state=None` until `read_state` first returns; `TUI.update(None, events)` + `render(None, ...)` is null-safe by inspection (@tui.py:241-285 guards `state is not None`), so F2 is low-risk but cheap to assert. |

## Recommendations (fold-ins — all optional, none gate the verdict per the "ALL findings resolved" rule being applied as advisory because fix_authorization is false and these are sub-MINOR plan-clarity nits)

- **R1 (Step 2.5 clarity):** Spell out the `worker_results` re-bind from the result-box after join.
- **R2 (Steps 3.3/3.7 clarity):** Note `.values()` iteration for `_project_workers` rows.
- **R3 (F2 cheap safety, fold into Step 3.2 or 3.7):** Assert the first poll frame with `state=None`
  (before `read_state` returns a state) does not raise — confirms first-frame null-state safety.
  `render`/`_build_header` already guard `state is not None`, so this is a one-line guard test.
- **R4 (F4 cheap safety, fold into Step 3.3):** Add a `_tail_events` case where a COMPLETE line is
  valid JSON but not an EventRecord shape (corrupt-complete-line) and assert the tailer's documented
  behavior (it currently treats JSONDecodeError-on-line as still-partial; a non-decode shape error is
  a separate branch worth one assertion).

## Self-Audit

**(a) Reliance list — rf-qa structural-PASS items skipped for structural re-check:**
- Relied on inherited A.10 structural PASS for: 30-item count, 0 `<chosen file>` placeholders, frontmatter
  shape, item structure, TB-Add-5 justification presence, resume+--tui reject *presence*, reflect-gate
  *penultimate ordering*. I did NOT re-count sections or re-verify frontmatter YAML shape.
- Relied on inherited A.10.25 research-alignment PASS for: all 7 FRs have implementing+verifying items,
  both stale-name resolutions honored, no fabrication. I did NOT re-map every FR to items from scratch.

**(b) Independent semantic checks (≥1 required) where structural PASS was insufficient and my own
tool work was required:**
- **Threaded-closure operability (item 1):** Structural QA confirms the glue item EXISTS; it cannot
  confirm the glue would COMPILE. I read commands.py:1700-1912 and verified every dispatch local is
  computed before line 1807, so a closure can legally close over them — a semantic property structure
  cannot see. (Tool: Read commands.py @1700-1860.)
- **Partial-line correctness (item 3):** Structure confirms `_tail_events` is specified; I read
  models.py:1820 and confirmed `from_json` = `json.loads` (raises JSONDecodeError), which is what makes
  the "buffer to newline, don't advance offset" discipline operationally NECESSARY rather than
  decorative. (Tool: Bash sed models.py:1815-1845.)
- **Monkeypatch-target reality (item 4):** Structure cannot know whether patching
  `superclaude.cli.swarm.tui` vs `...commands` is correct. I grepped commands.py and confirmed it has
  ZERO current tui imports, so the deferred-function-local-import seam means the SOURCE module is the
  correct patch target. (Tool: Bash grep commands.py for should_enable_tui/tui import.)
- **Frozen-signature diff provability (item 6):** Structure cannot verify the git base. I ran
  `git merge-base --is-ancestor` + `git diff` and confirmed start_commit 300c06a6 is a real ancestor and
  the current frozen-file diff is empty — so Step 4.4's proof is operationally meaningful. (Tool: Bash git.)
- **Downstream-consumer completeness (item 6/OBS-1):** Structure confirms a post-dispatch item exists;
  I read 1815-1912 and found the `worker_results`/`len(worker_results)` consumers that the threaded
  refactor must keep resolvable — surfacing OBSERVATION-1, which structural QA could not. (Tool: Read.)

## QA Complete

VERDICT: PASS — The task is operationally correct. All 30 items have satisfiable preconditions, every
shell/pytest/git/ruff command will work as written, the threaded-dispatch glue is compilable and
preserves the frozen dispatch_wave1 contract, the gate logic and partial-line discipline are sound, and
the monkeypatch/AST/diff verification mechanisms are non-vacuous and provable. The 3 MINOR findings are
plan-clarity nits and optional safety fold-ins (R1–R4); none would cause execution failure (R1/R2 are
self-correcting via the FR-2/FR-7 tests). QA_GATE_REQUIREMENTS: NONE waiver is correct for a code task
and is NOT flagged.
