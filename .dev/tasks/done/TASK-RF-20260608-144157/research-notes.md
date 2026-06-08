# Research Notes: Remediate reflect follow-ups F2, F4, F5 (PRD pipeline)

**Date:** 2026-06-08
**Scenario:** A (explicit — findings + file:line evidence already produced and re-verified)
**Depth Tier:** Quick (3 small fixes, single concern, no discovery needed)
**Track Count:** 1

**Research basis:** These three findings were produced by a Tier-2 deep `/sc:reflect` audit
(`.dev/reflect/post-prd-halt-hard-failure-20260608121957/REPORT.md`) — 3 heterogeneous-model
reviewers + evidence-validator gate. All file:line citations below were RE-VERIFIED fresh against
the live source on 2026-06-08 (this build). They are optional, non-gating follow-ups left after
the F1 fix landed.

---

## EXISTING_FILES

- `src/superclaude/cli/prd/prompts.py`
  - `_load_json(path) -> dict` (lines **37-39**) — `return json.loads(path.read_text(...))`, UNGUARDED against malformed JSON.
  - `_read_file(path, max_bytes)` (42-47).
  - `MissingArtifactError(FileNotFoundError)` (50-64) — `__init__(self, path, producer_step)`; message "Required artifact {name} is missing — its producer step '{producer_step}' did not complete successfully."
  - `_read_required(path, producer_step, max_bytes) -> str` (67-71) — guards `path.is_file()`, raises `MissingArtifactError`.
  - `_load_json_required(path, producer_step) -> dict` (**74-78**) — guards `path.is_file()` only, then calls `_load_json(path)`. **No guard against a present-but-malformed file → uncaught `json.JSONDecodeError`.** (F2)
  - Five REQUIRED-read conversion sites with hardcoded producer strings: line **189** (`_load_json_required(... "parse-request")`), **290** (`_read_required(... "scope-discovery")`), **293** (`_load_json_required(... "parse-request")`), **377** (`_read_required(... "research-notes")`), **479** (`_read_required(... "research-notes")`). (F4)
- `src/superclaude/cli/prd/executor.py`
  - `_STEP_ARTIFACT_FILES: dict[str, str]` (lines **252-263**) — canonical step_id → artifact filename map: `parse-request → parsed-request.json`, `scope-discovery → scope-discovery-raw.md`, `research-notes → research-notes.md`, etc.
  - `_run_subprocess_step` call-site catch `except MissingArtifactError` (~688-700) — converts to a graceful HALT. Any subclass of `MissingArtifactError` is caught here automatically.
- `tests/cli/prd/test_e2e.py`
  - `test_e2e_standard_tier_validation_fail_does_not_halt` (line **765**) — asserts only `result.halt_step != "scope-discovery"` and `"research-notes" in executed_steps`; does NOT assert scope-discovery's recorded status is `VALIDATION_FAIL`. (F5)
  - `_mock_process_factory(step_overrides=...)` (~224) and `standard_e2e_config` fixture — the established harness.

## PATTERNS_AND_CONVENTIONS

- UV for all Python ops (`uv run pytest tests/cli/prd/ -v`, `uv run ruff check`). Never bare python/pytest.
- Source of truth is `src/superclaude/cli/prd/` (package code; no `.claude/` sync impact for these edits).
- Typed-error pattern already established by Atom 2: `MissingArtifactError(FileNotFoundError)` caught at the `_build_prompt` call site → `PrdStepResult(status=HALT, halt_reason=...)`. A NEW sibling subclass is caught by the SAME `except MissingArtifactError` (subclass catch), so no executor change is needed if F2 uses a subclass.
- Test idiom: e2e tests stub `_build_prompt` for full-pipeline runs (`executor._build_prompt = lambda ...`); the real-builder path is exercised by direct `_run_subprocess_step` calls or `resume_from` (no stub). Membership/property tests live in `test_models.py`.
- Step results: `PrdStepResult` exposes `.status`; the Stage-A loop appends each to `result.step_results`. To assert a specific step's status in an e2e test, locate it in `result.step_results` (the loop records them in execution order) — confirm how step_id is recoverable (PrdStepResult has no step_id field; the test may need a tracking factory OR to rely on the known execution order: with resume skipping, scope-discovery is the first executed step in the VALIDATION_FAIL scenario, OR use the existing `executed_steps` tracking list pattern).

## GAPS_AND_QUESTIONS

- **F2 implementation choice (resolve in task):** catch `json.JSONDecodeError` in `_load_json_required` and either (a) re-raise as `MissingArtifactError` (message would inaccurately say "is missing"), or **(b, RECOMMENDED)** add a sibling `MalformedArtifactError(MissingArtifactError)` with a "malformed/unparseable" message. Option (b) is caught by the existing call-site `except MissingArtifactError` automatically (subclass), keeps the halt_reason path working (`exc.path.name`, `exc.producer_step` both present), and gives an accurate message. The call-site `halt_reason` template currently says "missing required artifact {name}" — consider a small tweak so a malformed file doesn't read as "missing" (e.g., derive the verb from the exception type, or keep generic "unusable required artifact").
- **F4 implementation choice (resolve in task):** prefer a **consistency-guard test** over refactoring the 5 call sites — `_STEP_ARTIFACT_FILES` lives in `executor.py` and importing it into `prompts.py` risks a circular import (executor imports prompts locally for exactly this reason). A test that asserts, for each `(producer_step, artifact_filename)` pair used by the converted reads, `_STEP_ARTIFACT_FILES[producer_step]` resolves to the same filename, pins the two sources of truth in sync with zero runtime coupling. (If a clean no-cycle derivation is feasible, that is acceptable too — engineer's call, documented.)
- **F5:** confirm how to recover scope-discovery's status in the e2e harness (PrdStepResult has no step_id; use execution-order knowledge or a tracking wrapper). Lowest-risk: assert on `result.step_results` by position, or extend the existing pattern.

## RECOMMENDED_OUTPUTS

This is a remediation task, not a doc build. Outputs = code/test edits:
- F2: `prompts.py` (`MalformedArtifactError` + guarded `_load_json_required`; optional call-site message tweak in `executor.py`) + a unit/e2e test (malformed `parsed-request.json` → graceful HALT, no uncaught exception).
- F4: a consistency-guard test (`tests/cli/prd/test_prompts.py` or `test_models.py`) pinning producer-step strings to `_STEP_ARTIFACT_FILES`.
- F5: strengthen `test_e2e_standard_tier_validation_fail_does_not_halt` to assert scope-discovery status == `VALIDATION_FAIL`.
- Validation: `uv run ruff check` clean on edited files; `uv run pytest tests/cli/prd/ -v` green (currently 158 passed).

## SUGGESTED_PHASES

- Phase 1: F2 — typed malformed-artifact guard + test (highest value; same crash-class as the original bug).
- Phase 2: F4 — producer/artifact consistency-guard test.
- Phase 3: F5 — strengthen the VALIDATION_FAIL assertion.
- Phase 4: Validation — ruff + full prd suite green; final QA gate.

(Phases are independent edits; F2 is the only one touching `src/`. Each gets its own granular item.)

## TEMPLATE_NOTES

- Template **02** (complex): multiple phases with build + test + validation + a FINAL QA gate; conditional implementation choice in F2/F4.
- Tier **Quick**: 3 small fixes, evidence already complete. QA_GATE_REQUIREMENTS: FINAL_ONLY. TESTING_REQUIREMENTS: UNIT. VALIDATION_REQUIREMENTS: ruff + prd pytest suite must pass.
- Right-sizing note: the research-gate fan-out (A.7/A.8 parallel researchers + rf-analyst/rf-qa research gate) is intentionally skipped — there are no researcher outputs to gate; the "research" is the evidence-validator-confirmed deep-reflect audit, re-verified fresh this session. The mandatory A.10 task-integrity validation gate still runs on the produced task file.

## AMBIGUITIES_FOR_USER

None blocking. The two implementation choices (F2 option b; F4 guard-test vs derive) are documented with a recommended path and left as engineer's-call items with rationale — the executor decides at implementation time. F2/F4/F5 are all optional hardening (the reported crash is already fixed by Atoms 1+2 and F1).
