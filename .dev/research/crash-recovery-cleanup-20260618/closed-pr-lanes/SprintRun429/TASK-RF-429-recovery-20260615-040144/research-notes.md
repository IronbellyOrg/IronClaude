# Research Notes: Sprint Run 429 / Account-Exhaustion Recovery

**Date:** 2026-06-15
**Scenario:** A (explicit — driving spec provides full module-level design)
**Depth Tier:** Deep
**Track Count:** 1 (single track — P1→P6 are strongly sequential; P2 depends on P1's detector, P3 on P1+P2, P4 reuses P3's loop, P5 wires P2/P3 outputs, P6 emits events for P3/P4. NOT independent work streams.)
**Spec:** .dev/brainstorms/sprint-429-recovery-spec.md (status: ready-for-mdtm; reflect-validated + remediated 2026-06-15)
**start_commit (O1 wrapper audit base):** 59b9e2a2b9f0
**executor_model_class:** sonnet

---

## EXISTING_FILES

All paths under `src/superclaude/cli/sprint/` unless noted. Source-of-truth is `src/superclaude/`; `.claude/` is sync-dev output (templates live at `src/superclaude/templates/workflow/`, NOT `.claude/templates/`).

### Files to MODIFY
- **monitor.py** (571 lines) — detection layer. Has `detect_error_max_turns` (`:37`), `detect_prompt_too_long` (`:64`), `ERROR_MAX_TURNS_PATTERN` (`:33`), `_TURN_INDICATOR_PATTERN` (`:112`), `count_turns_from_stream_json` (referenced by spec as the LAST-result-event parse mirror). All detectors take `output_path: Path`, read with `FileNotFoundError/OSError` tolerance, scan last / last-10 lines. **NEW** `detect_provider_failure` + `_provider_failure_from_text` core + `ProviderFailure` enum + `ProviderFailureSignal` + two regexes (`_RE_ALL_ACCOUNT`, `_RE_SINGLE_ACCOUNT`) go here (P1).
- **models.py** (1121 lines) — taxonomy + serialization.
  - `TaskStatus` enum (`:46-66`): PASS, PASS_RECOVERED, FAIL_TERMINAL, FAIL_RECOVERABLE, INCOMPLETE, SKIPPED. `is_success` = {PASS, PASS_RECOVERED} (`:57-58`). `is_failure` = {FAIL_TERMINAL, FAIL_RECOVERABLE, INCOMPLETE} (`:61-66`). **ADD** `FAIL_PROVIDER_EXHAUSTED = "fail_provider_exhausted"` and include in `is_failure` (P2).
  - `TaskResult` dataclass (`:171-240`): `to_dict` (`:190-216`) serializes flat fields; `from_dict` (`:218-240`) uses **HARD keys** for ALL result-level fields (`data["status"]`, `data["turns_consumed"]`, `data["exit_code"]`, `data["started_at"]`, `data["finished_at"]`, `data["output_bytes"]`, `data["gate_outcome"]`, `data["reimbursement_amount"]`, `data["output_path"]`). **ADD** `failure_class: str=""`, `session_resets: int=0`, `exhausted_model: str=""` with `.get(...)` defaults in from_dict so old `phase-N-result.json` round-trips (P2). VERIFIED: from_dict is hard-keyed (back-compat concern is real).
  - `PhaseStatus` enum (`:385+`): PENDING, RUNNING, PASS, PASS_NO_SIGNAL, PASS_NO_REPORT, PASS_RECOVERED, PREFLIGHT_PASS, …, HALT, TIMEOUT, ERROR, SKIPPED. `is_terminal` (`:410-423`), `is_success` (`:426+`). **ADD** `PROVIDER_EXHAUSTED` (P4).
  - **NEW** `build_account_exhaustion_halt(config, halt_task_id, exhausted_model, suggested_model, remaining_tasks, ledger)` (P5). Existing `build_resume_output` (`models.py:1017-1071`) / `:821-828` is the fall-through halt UX.
  - `HandoffRecord` (`:306-382`) already uses `.get()` forward-compat from_dict — pattern reference for back-compat.
- **executor.py** (2832 lines) — control flow.
  - `_run_one_task` (`:963-975`) — signature: `(task, config, phase, *, started_at, prior_context="", ledger=None, subprocess_factory=None, shadow_metrics=None, remediation_log=None, lock=None)`. Spawn at `:986-993` (runs **UNLOCKED** — docstring `:976-985` states spawn is the unlocked concurrency win; budget reconcile + post-task hooks run under `lock`). **ADD** `reset_policy`/latch as a new shared param (P3).
  - Status ladder (`:999-1015`): exit0→PASS (`:999`), 124→INCOMPLETE (`:1001`), `detect_error_max_turns`+`_task_completed_before_overrun`→PASS_RECOVERED (`:1003-1011`), `_is_transient_failure`→FAIL_RECOVERABLE (`:1012`), else→FAIL_TERMINAL (`:1014`). **INSERT** provider-failure branch ABOVE `:1012` and BELOW the `:1003` completion gate (P3). Detector order: success-envelope → error_max_turns(PASS_RECOVERED) → provider-failure → transient → terminal. Reuse `_task_completed_before_overrun(output_path)` as a guard before the provider-failure branch (covers clean-success+trailing-429).
  - K=1 sequential call site (`:1337-1348`, lock=None); K>1 parallel call site (`:1134-1145`, lock=<lock>). Atomic budget gate `ledger.try_launch()` (`:1120`).
  - `_is_transient_failure` (`:2267-2289`) — only `api_retry`/`ConnectionRefused`/(is_error+0 tokens).
  - Single-session phase path: `ClaudeProcess(config, phase, env_vars=…)` spawn (`:1815`) before `_determine_phase_status` (`:1993`). **WRAP** in re-spawn loop; ALL_ACCOUNT/cap-exhausted → `PhaseStatus.PROVIDER_EXHAUSTED` (P4).
  - `status.is_failure` consumer at `:2103-2132` = phase halt → `SprintOutcome.HALTED` + break (desired for exhaustion).
  - `_write_phase_result_json` (`:2657-2701`) — **ADD** top-level `halt_reason: "provider_exhaustion"` + `exhausted_model` (P3); emit `session_reset`/`account_exhaustion_halt` events to `execution-log.jsonl` (P6).
  - Test seams: `_run_one_task(subprocess_factory=…)` (`:986-993`), `_execute_phase_tasks_parallel(_subprocess_factory=…)` (`:1054`).
- **rerun_tasks.py** (1705 lines) — offline classifier.
  - `_classify_transcript(text: str) -> TaskStatus` (`:547-593`): parses events from a `text` string (NOT a path), keys on `is_error` + transient (`api_retry`/`ConnectionRefused`/0 tokens). 429 today → FAIL_TERMINAL (tokens>0) or FAIL_RECOVERABLE (tokens==0). **ADD** a `FAIL_PROVIDER_EXHAUSTED` branch ABOVE the `is_error`/transient branching (`:582-591`) keyed off the shared `_provider_failure_from_text` core (P2). NOTE signature mismatch: detector reads path, classifier has text → factor a text core.
  - `discover_failed_tasks_from_transcripts` (`:596+`) — hard-crash resume fallback; routes through `_classify_transcript`, so P2 alignment auto-covers the transcript-derived resume path.
  - `retry_count_for_task` (`:1482`) — cross-run content-rerun cap-3 (from recovery.py). The new reset budget is SEPARATE/in-memory (Q4).
- **recovery.py** (775 lines) — operator-invoked remediation. Nominators: `ManualNominator` (`:152`), `DriftNominator` (`:183`, nominates classification=="drift"), `ReflectReportNominator` (`:189+`). `retry_count_for_task`, `RecoveryBundle`, `merge_recovery_bundle`, `acquire_recovery_lock` (`:275`). **(G)** to honor UX contract #4, nominators SHOULD exclude `failure_class=="provider_exhaustion"` (P6) OR scope contract #4 to live-path.
- **resume/planner.py** — `plan.rerun_task_ids` (`:160-164`): re-runs tasks where `persisted_status is None or not persisted_status.is_success`. `_coerce_task_status(tr.get("status"))` (`:157`) → `TaskStatus(value)` auto-resolves the new member. Hard-crash fallback (`:166-171`) uses `discover_failed_tasks_from_transcripts`. NO separate planner edit needed (E).
- **process.py** (434 lines) — subprocess command builder. `claude --print --verbose --no-session-persistence --output-format stream-json [--model M]` (`:129-141`); `config.model`→`--model` (`:141`); `env_vars` merges into `os.environ.copy()`. `ClaudeProcess` extends `_PipelineClaudeProcess`; timeout `max_turns*120+300`.
- **commands.py** — CLI surface; **ADD** `--max-session-resets` flag (default 8) + CLI doc + doc⇆CLI parity (P5).

### Files to CREATE
- **recovery_policy.py** (NEW) — `Action` enum (RETRY_NEW_SESSION, HALT_MODEL_SWITCH, FAIL_TASK, CONTINUE); `SessionResetPolicy` dataclass (`max_session_resets=8`, `_exhaustion_attempts`, `_latch_tripped`) with `decide(signal, attempt) -> Action` (P3).
- **aienv.py** (NEW) — parse `~/.aienv` for `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` + `T*Model0N`/`IC_ALIASES`; `suggest_alternate_model(failed_model_or_alias)` returns next distinct alias. Reuse resolution convention from `src/superclaude/scripts/ic` (P5).

### TESTS (to CREATE)
- `tests/.../fixtures/exhaustion/`: `single_account_429.jsonl`, `all_account_cooldown.jsonl`, `operation_timeout.jsonl`, `api_retry_maxed.jsonl`, `task_failure_real.jsonl`, `clean_pass.jsonl` (authored from verbatim ground-truth JSON; §2/§6). Find the existing sprint test dir + fixture conventions.
- Unit (detector), policy (decide truth table), executor (subprocess_factory seam scenarios), resume-safety, UX golden-string + doc⇆CLI parity, aienv, back-compat round-trip.

---

## PATTERNS_AND_CONVENTIONS

- **Detector family pattern** (monitor.py): pure function `(output_path: Path) -> bool|signal`; `try: read_text(errors="replace") except (FileNotFoundError, OSError): return <neutral>`; scan last / last-N non-empty lines; module-level compiled regex constants. `detect_provider_failure` must mirror this (OSError/parse-tolerant → NONE).
- **Stream-json parsing**: iterate `text.splitlines()`, `line.strip()`, skip non-`{`, `json.loads` in try/except, accumulate `usage.output_tokens`, capture last `{"type":"result"}` event (see `_classify_transcript:555-574`). Reuse for the LAST-result-event parse. **Do NOT key on `subtype`** (it is `"success"` even when `is_error` is true).
- **Enum + property pattern** (models.py): string-valued Enum members; `is_success`/`is_failure`/`is_terminal` as `@property` returning `self in (…)` tuples. Add members to the relevant tuples.
- **Serialization back-compat**: `to_dict` flat; `from_dict` — old code hard-keyed (TaskResult) vs forward-compat `.get()` (HandoffRecord). New fields MUST use `.get(default)`.
- **Concurrency**: `_run_one_task` shares `ledger`/`shadow_metrics`/`remediation_log` via params, guarded by `lock` (K>1) or `lock=None` (K=1). Spawn UNLOCKED; reconcile/hooks LOCKED. New latch follows this exact pattern.
- **SoT discipline** (spec §7): edit `src/superclaude/cli/sprint/` → `make sync-dev` → `make verify-sync`; `uv run ruff format --check src/ tests/` before push; `uv run pytest` for tests; feature branch; PR to `IronbellyOrg/IronClaude` with `--repo`.
- **CLI test conventions**: UV only (`uv run pytest`); fixtures under `tests/`.

## GAPS_AND_QUESTIONS

(For researchers to close — the core executor/models/monitor/rerun/planner surface is already verified; these are the un-verified edges.)
1. **process.py:129-141** exact subprocess cmd assembly + how `env_vars`/`config.model` flow (confirm the `--model` injection point for the resume command and the env inheritance for the alias suggester).
2. **executor.py:1815 / :1993** — exact single-session `ClaudeProcess` spawn + `_determine_phase_status` shape (P4 wrap point).
3. **executor.py:2657-2701** `_write_phase_result_json` structure + `execution-log.jsonl` event-emission helper (`monitor.py:37,64` detect_* are templates; find the event emitter).
4. `src/superclaude/scripts/ic` alias-resolution convention + `~/.aienv` format (`T*Model0N`, `IC_ALIASES`) for aienv.py.
5. Existing sprint **test layout + fixture conventions** (where do detector/executor/resume tests live; subprocess_factory usage examples; how transcripts are authored as fixtures).
6. `recovery.py` nominator interfaces (exact `nominate(context)` contract) for the (G) `failure_class` exclusion.
7. `count_turns_from_stream_json` exact location/signature in monitor.py (LAST-result-event parse mirror).
8. `commands.py` flag-registration pattern + `sprint run --help` surface for `--max-session-resets` + doc⇆CLI parity test location.

## RECOMMENDED_OUTPUTS

Research files in `${TASK_DIR}research/`:
- `01-file-inventory.md` — exhaustive inventory of the 9 modify/create targets w/ exports, line counts, exact insertion points.
- `02-patterns-conventions.md` — detector pattern, enum/property pattern, serialization back-compat, concurrency lock model, SoT discipline.
- `03-integration-points.md` — executor wiring (both per-task & single-session), planner resume routing, recovery nominators, process.py subprocess+env flow.
- `04-data-flow-tracer.md` — 429 signature flow: subprocess stdout stream-json → detector → policy → status → persistence → resume; the four-way discrimination.
- `05-test-verification.md` — sprint test layout, subprocess_factory seam usage, fixture authoring conventions, doc⇆CLI parity test pattern, ground-truth JSON shapes for the 6 fixtures.
- `06-template-examples.md` — read template 02 (src/superclaude/templates/workflow/02_…) PART 1 rules (A3 granularity, B2 self-containment, M3/M4/I19-I22 QA encoding); scan .dev/tasks/to-do/ for prior task examples.

## SUGGESTED_PHASES

6 researchers (Deep), all spawned in ONE message, no overlapping file assignments:
- **R1 File Inventory** → monitor.py, models.py, recovery_policy.py(new), aienv.py(new) targets — exports, line counts, exact insertion points. Other researchers cover executor/rerun/planner/recovery (R3) and tests (R5).
- **R2 Patterns & Conventions** → detector pattern, enum/property, serialization, concurrency lock model from monitor.py/models.py/executor.py. R3 covers wiring; R2 covers idioms.
- **R3 Integration Points** → executor.py (per-task :963-1015, single-session :1815/:1993, persistence :2657-2701), planner.py, recovery.py nominators, process.py subprocess+env. R1 covers file-level inventory; R3 covers cross-module contracts.
- **R4 Data Flow Tracer** → end-to-end 429 flow + four-way discrimination + edge cases (#1-#10 in spec §5). R3 covers static wiring; R4 covers runtime data movement.
- **R5 Test & Verification** → tests/ layout, subprocess_factory seam, fixture conventions, the 6 ground-truth fixtures, doc⇆CLI parity, back-compat round-trip. Exclusive on tests.
- **R6 Template & Examples** → template 02 PART 1 + prior task examples. Exclusive on template.

## TEMPLATE_NOTES

- **Template 02 (complex)** — multi-phase discovery+build+test+review; matches the 6-phase plan. Path: `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (NOT `.claude/`).
- **Tier Deep** — 9 files across detection/taxonomy/policy/executor/UX/telemetry; P3 is High-risk live concurrency.
- **Granularity (A3)**: one item per file-edit / per-test / per-fixture. NOT "implement P3" batch items — P3 alone = recovery_policy.py + executor per-task loop + latch threading + persistence + ~6 factory tests, each its own item.
- **QA encoding**: PER_PHASE gates (Template 02). Each phase-gate ≥6 agents (3 rf-qa + 3 rf-qa-qualitative) per I19/I22-full; test-bearing phases get a verification gate. TESTING_REQUIREMENTS = UNIT + INTEGRATION (executor factory scenarios are integration-shaped). VALIDATION = ruff format check + make verify-sync + uv run pytest.
- **POST_REFLECT_GATE: ENABLED** — penultimate final-phase item = flat `superclaude reflect run {TASK_FILE} --depth deep --fix --promote` wrapper shell-out behind the SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE skip guard.
- **Phase ordering = P1→P6** with explicit `after Phase N` dependencies (P2 needs P1 detector; P3 needs P1+P2; P4 reuses P3 loop; P5 wires P2/P3; P6 emits events for P3/P4).

## AMBIGUITIES_FOR_USER

None blocking — intent is clear from the reflect-validated spec. Two design choices the spec already resolved (Q1-Q5) and one deferred decision the builder must encode as written, not auto-resolve:
- **(G) UX contract #4 scope**: the spec now offers two options (exclude `failure_class=="provider_exhaustion"` at recovery.py nominators in P6, OR scope contract #4 to the live auto-path). The builder should encode the P6 nominator-exclusion as the implementation and note the scoping fallback in the item Context — NOT silently pick. This is a `needs_human_decision`-adjacent item per `feedback_human_decision_items_must_halt`: if the nominator-exclusion proves non-trivial, the item writes the finding and proceeds with the documented default rather than shipping an unreviewed behavior change.
