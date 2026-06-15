# Research Notes: Differential backtest/eval harness for sc:troubleshoot Pipeline Hardening Closure (E1–E5 replay)

**Date:** 2026-06-11
**Scenario:** A (Explicit — GOAL, WHY, WHERE, REPLAY TARGETS, ORDER, DOD, CONSTRAINT, REFERENCES all supplied)
**Depth Tier:** Deep (mirrors a large existing framework, 5 differential scenarios, git-replay isolation, machine-readable report, pytest wiring; multi-subsystem: cli/eval + sprint git helpers + spec contract + impl tasklist)
**Track Count:** 1 (single cohesive deliverable: the backtest harness under tests/troubleshoot/backtest/)

**SPEC_PATH:** `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-RELEASE-SPEC.md`
**Impl tasklist (sibling, DO NOT collide):** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-hardening-20260611-023739/TASK-RF-troubleshoot-hardening-20260611-023739.md`
**Impl worktree (parallel /task owns it):** `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening` (branch `feat/troubleshoot-pipeline-hardening`)

> **Orchestrator note on task-folder location:** This task-builder run executes from the `ReflectGateWiring` worktree, but the build is cross-cutting and every reference path is a main-workspace absolute path; the sibling impl tasklist also lives at the main workspace. The task folder is therefore created at `/config/workspace/IronClaude/.dev/tasks/to-do/` (canonical shared location) so the executor — which the CONSTRAINT requires to build a fresh worktree off `origin/master` — can discover it. Researchers read tracked source via main-workspace absolute paths (`src/superclaude/cli/eval/`, `src/superclaude/cli/sprint/process.py`, `tests/...`), which exist in every checkout off origin/master.

---

## EXISTING_FILES

### Eval framework to MIRROR — `src/superclaude/cli/eval/` (all CONFIRMED present)
- `runner.py` — `EvalRunner` (class @ ~L712, `.run(spec)` @ L833, `_execute_once` @ L880, `_resolve_timeout`), `run_eval()` (L179), `ExecutorContext` (L86), `ObservedRun` (L110), `LifecycleExecutor` Protocol (L136: spawn/inject/observe), `_classify_outcome` (L400), `_finalize` (L425), `_JsonlLog` (L537, emit/write_to).
- `pty_driver.py` — `PtyDriver` (class @ L94): spawn (L167), context-manager (`__enter__`/`__exit__`), `expect_prompt_ready` (L224), `inject_prompt` (L270), `read_stdout` (L305), `wait_exit` (L334), `terminate` (L390), `exit_code` (L422). Errors: `PtyDriverError`/`PtyDriverTimeout`/`PtyDriverNotStarted`/`PtyDriverEOF`.
- `orchestrator.py`, `models.py`, `config.py` (`EvalConfig`), `loader.py`, `expect.py`, `reporter.py`, `run_report.py`, `exit_codes.py`, `isolation.py`, `coverage.py`, `disk_budget.py`, `retry.py`, `signal_handler.py`, `capabilities.py`, `hook_adapter.py`, `claude_process.py`, `artifact_layout.py`.
- `run_report.py` — machine-readable report writer (FR-RPT1 / DM-012 / D-0054): `render_summary_json` (L233, wraps `RunSummary.to_dict`), `render_summary_markdown` (L141), `render_summary_yaml` (L339), `render_junit_xml` (L259), `write_aggregated_report` (L47 in `__all__`), `ReporterContractViolation` (L67), `_check_invariant` (L96). **This is the model for the catch-rate report.**
- `schemas/summary.schema.json` — JSON Schema for the machine-readable summary (model for the catch-rate report schema).
- `suites/*.yaml` + `suites/suite.schema.json` — declarative suite spec pattern (e.g. `eval_smoke.yaml`, `task_classification_contract.yaml`, `tasklist_deterministic_shape.yaml`). Model for declaring the 5 E1–E5 scenarios.

### Git-replay helpers to MIRROR — `src/superclaude/cli/sprint/process.py` (CONFIRMED)
- `build_task_context(...)` @ L306 — builds executor context including a git-diff section.
- `get_git_diff_context(start_commit: str) -> str` @ L371 — runs `git diff` via `superclaude.cli.sprint.process._subprocess.run` (mockable seam; see tests). Returns a structured markdown section. **This is the git-via-subprocess pattern to mirror for the replay helper.**
- Tests at `tests/sprint/test_process.py` (23.5KB) demonstrate the subprocess-mock pattern: `test_git_diff_context_success` (L432), `test_git_diff_context_empty_diff` (L444), `test_context_injection_includes_git_diff` (L396) — all patch `superclaude.cli.sprint.process._subprocess.run`.

### Eval test patterns to MIRROR — `tests/cli/eval/` (CONFIRMED, ~75 test files)
- `conftest.py`, `fixtures/`, plus tests like `test_runner_class.py`, `test_pty_driver.py`, `test_run_report.py`, `test_reporter.py`, `test_reporter_contract.py`, `test_summary_schema.py`, `test_schema_validate.py`, `test_suite_loader.py`, `test_eval_lifecycle.py`. Model for pytest wiring, fixtures, and schema-validation tests.

### Target output (NEW — to be created by the executor)
- `tests/troubleshoot/backtest/` — does NOT exist yet (`tests/troubleshoot/` absent). The harness + runner + git-replay helper + per-escape differential scenarios + catch-rate report + pytest wiring all land here.
- Spec §4.7 EXPLICITLY sanctions test-only validators under `tests/troubleshoot/`; any reusable runtime logic promoted beyond tests must live under `src/superclaude/` and be referenced in §4.7 first.

---

## PATTERNS_AND_CONVENTIONS
- **UV only** — `uv run pytest tests/troubleshoot/backtest/`. Never `python -m`/bare pytest.
- **Subprocess mock seam** — git calls go through a module-level `_subprocess.run` so tests can patch them (sprint/process.py pattern). The replay helper should follow the same indirection so unit tests don't need real git.
- **Machine-readable report** — `run_report.py` renders a dataclass→`to_dict()`→`json.dumps(indent=2)` payload validated against a JSON Schema in `schemas/`. The catch-rate report should follow: a dataclass (per-escape MISS/CATCH verdicts + aggregate) → JSON, validated against a new schema, and a `backtest_status` derivation (not_run|partial|complete).
- **Declarative suite YAML** — scenarios can be declared in YAML + validated against a `suite.schema.json` (eval/suites pattern). Consider mirroring for the 5 E1–E5 scenarios, OR encode them as parametrized pytest cases — researcher 7 to recommend.
- **xfail/skip-guard** — DOD: the NEW=CATCH half may stay `xfail`/skip-guarded until the impl branch lands; OLD=MISS + harness wiring must run green now. Researcher 2 to document the project's xfail/skipif conventions (markers, reason strings, conditional import guards).
- **Throwaway worktree isolation** — replay must `git worktree add` a detached checkout at each escape's pre-fix parent, run the OLD-protocol assertion, then `git worktree remove --force`. Must be hermetic and self-cleaning (tmp_path or a dedicated scratch root), never mutate the live tree.

## GAPS_AND_QUESTIONS
- **What exactly does "OLD=MISS" assert per escape?** The pre-fix parent has the BUG but not the hardening gate. The OLD-protocol path must demonstrably FAIL to catch the escape (i.e., the un-hardened logic returns PASS/clean on input that the new gate would HALT). Researcher 5 must define, per escape, the concrete observable: the buggy code/logic at the pre-fix parent and the input that slips past it.
- **What is the "NEW H0-H5 gate" surface the harness calls?** The impl branch produces `refs/*.md` + `tests/troubleshoot/test_*.py` validators (per spec §4.7) + SKILL wiring. The harness must invoke the NEW gate logic (the H1/H2/H3/H4 validators) on the same escape input and assert CATCH. Researcher 6 maps which impl artifacts/validators expose the gate logic the eval can import/call, and how to xfail-guard until they exist.
- **Where does the gate logic live — markdown protocol or importable Python?** Spec §4.7 says protocol is markdown-first but every closure artifact affecting the verdict has an executable validation surface (`tests/troubleshoot/test_*.py`). The differential harness likely drives those validators (or a thin shared helper). Researcher 4 + 6 to resolve the executable seam.
- **backtest_status producer/consumer** — §4.5/§5.5: enum, default not_run, consumed by report+roadmap; NFR-1 replay gate is the producer. The catch-rate report sets it: all 5 pass→complete; some pass→partial (+missing IDs); none run→not_run. Researcher 4 to extract exact derivation + §5.4 "Backtest Status vs Run-Level Verdict" distinction (it is SEPARATE from `pipeline_hardening_verdict`).
- **PtyDriver vs direct call** — does the differential replay need a real Claude PTY run, or can it drive the validator logic directly (cheaper, deterministic)? Spec NFR-3 wants bounded cost / single-seam probe, no mandatory full E2E. Researcher 1 + 5 to recommend: prefer direct validator invocation over PTY where possible; PtyDriver mirrored only if an end-to-end seam is required.

## RECOMMENDED_OUTPUTS (researcher → file)
- `research/01-eval-framework-inventory.md` — EvalRunner/PtyDriver/orchestrator/reporter/run_report/schemas/suites API surface to mirror.
- `research/02-test-patterns-and-xfail.md` — tests/cli/eval pytest patterns, conftest/fixtures, xfail/skipif conventions, UV invocation, subprocess-mock seam.
- `research/03-git-replay-helpers.md` — sprint/process.py git-via-subprocess pattern + git worktree add/remove isolation pattern for pre-fix-parent checkout.
- `research/04-spec-contract-deepdive.md` — RELEASE-SPEC §1.1, §3.1 traceability matrix, §4.5/§4.7, §5.4/§5.5, §8.3 backtest scenarios, NFR-1, backtest_status derivation (DOC CROSS-VALIDATOR: tag CODE-VERIFIED/CONTRADICTED/UNVERIFIED).
- `research/05-replay-targets.md` — per-escape: fix commit, pre-fix parent SHA, what code/logic was buggy, the concrete OLD=MISS observable, the NEW=CATCH assertion target, mapped 1:1 to §8.3.
- `research/06-impl-tasklist-crossref.md` — which H0-H5 validator/test artifacts the impl branch produces, the importable/executable gate seam for NEW=CATCH, file-collision boundary (NEVER touch `src/superclaude/skills/sc-troubleshoot-protocol/**`), xfail-guard strategy.
- `research/07-mdtm-template-and-report-model.md` — MDTM template 02 PART 1 rules (A3/A4/B2/M3/M4/I19-I22/L1-L6); summary.schema.json + run_report.py as catch-rate-report model; suite.schema.json as scenario-declaration model.

## SUGGESTED_PHASES (researcher assignments — 7, Deep tier, single track)
All read tracked source via main-workspace absolute paths under `/config/workspace/IronClaude/`.

1. **R1 File Inventory** — `src/superclaude/cli/eval/{runner,pty_driver,orchestrator,models,config,reporter,run_report,exit_codes,isolation}.py` + `schemas/` + `suites/`. Catalog public classes/functions/signatures to mirror. Covers framework surface ONLY; not tests (R2), not git helpers (R3).
2. **R2 Patterns & Test Conventions** — `tests/cli/eval/conftest.py` + representative tests + project xfail/skipif/marker conventions + UV pytest invocation + the `_subprocess.run` mock seam usage in tests. Covers test scaffolding/conventions; not the framework API (R1).
3. **R3 Git-replay / Integration** — `src/superclaude/cli/sprint/process.py` (`get_git_diff_context` L371, `build_task_context` L306, `_subprocess` seam) + git `worktree add`/`remove`/`checkout` subprocess isolation pattern for checking out a pre-fix parent into a throwaway worktree. Covers git mechanics; not eval API (R1).
4. **R4 Spec Contract Deep-dive (Doc Cross-Validator)** — the RELEASE-SPEC sections above. Extract exact contracts; tag every doc claim CODE-VERIFIED/CONTRADICTED/UNVERIFIED against actual code. Covers the spec; not the impl tasklist (R6).
5. **R5 Replay-target verification** — git history for the 5 commits + parents (pre-verified: E1 7601ad25^=94d5baa0; E2 e97aa4fd^=10723863; E3 eb9a2633^=e97aa4fd; E4 b97c9960^=1b0264f1 UNMERGED; E5 10723863^=d878bc6d). For each: what changed (the fix), therefore what was buggy at the parent, the concrete OLD=MISS observable, the NEW=CATCH target, mapped 1:1 to §8.3 rows. Covers the commits; not the spec prose (R4).
6. **R6 Impl-tasklist cross-ref** — read the sibling impl tasklist; enumerate the H0-H5 validator artifacts/test files it will create (esp. `tests/troubleshoot/test_*.py`), identify the importable/callable gate seam the eval drives for NEW=CATCH, the xfail-guard strategy until that branch lands, and the hard file-collision boundary (`src/superclaude/skills/sc-troubleshoot-protocol/**` is OFF-LIMITS — impl /task owns it). Covers impl coordination; not the spec (R4).
7. **R7 MDTM template + report/schema model** — `.claude/templates/workflow/02_mdtm_template_complex_task.md` PART 1 (A3/A4/B2/M3/M4/I19-I22/L*); `src/superclaude/cli/eval/run_report.py` + `schemas/summary.schema.json` + `suites/suite.schema.json` as the model for the machine-readable catch-rate report + scenario declaration. Covers template + report model; not the eval runtime API (R1).

## TEMPLATE_NOTES
- **Template 02 (Complex)** — discovery→build→test→verify with phases, conditional flows (xfail-until-impl-lands), QA gates. Not 01.
- **Tier: Deep** — 7 researchers; framework-mirroring + 5 differential scenarios + machine-readable report + pytest wiring + git-worktree isolation.
- **POST_REFLECT_GATE: ENABLED** — spec-driven build; spec_path resolves; POST reflect item required as penultimate final-phase item.
- Generated tasklist must use per-phase QA gates (Template 02 default PER_PHASE), granular per-escape items (one item per E1..E5 scenario, not a batch), embedded agent prompts, incremental writing.
- **TESTING_REQUIREMENTS:** ALL (UNIT for helper/report logic + INTEGRATION for differential replay + the 5 E2E backtest scenarios). The deliverable IS tests.
- **VALIDATION_REQUIREMENTS:** `uv run pytest tests/troubleshoot/backtest/` green; OLD=MISS half green now; NEW=CATCH half xfail/skip-guarded until impl lands; lint/format (`uv run ruff check` + `uv run ruff format --check`) per project memory.

## AMBIGUITIES_FOR_USER
- **Branch/worktree creation timing:** CONSTRAINT says build on OWN branch+worktree `feat/troubleshoot-hardening-evals` off `origin/master`. This is an EXECUTION-time action (the `/task` executor creates it). The task-builder only produces the task file (no branch created now). The generated tasklist's Phase 1 will instruct the executor to create the worktree. Proceeding on this interpretation.
- Otherwise intent is clear from the richly-specified request.
