# QA Report — Task Integrity / Report Validation (PG-2, FINAL_ONLY)

**Topic:** PRD pipeline two-atom defense-in-depth fix (uncaught FileNotFoundError on missing `scope-discovery-raw.md`)
**Date:** 2026-06-08
**Phase:** report-validation (final code-fix gate, PG-2)
**Fix cycle:** N/A (zero issues found — no fixes required)
**Stance:** Adversarial, zero-trust. Every claim verified against real source; validation summaries distrusted and independently re-run.

---

## Overall Verdict: PASS

All 6 acceptance criteria verified true against the actual source files. Independent test run = 157 passed / 0 failed. Independent ruff = clean. The `make verify-sync` / `make lint` failures were verified to be caused EXCLUSIVELY by pre-existing orphaned `.claude/` skills unrelated to this task — proven, not taken on faith.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `is_hard_failure` exact membership (ERROR/TIMEOUT/QA_FAIL_EXHAUSTED/HALT; excludes VALIDATION_FAIL & QA_FAIL) | PASS | `models.py:155-163` — set is exactly `{ERROR, TIMEOUT, QA_FAIL_EXHAUSTED, HALT}`. Read full enum; VALIDATION_FAIL/QA_FAIL absent. |
| 2 | Halt fires on `is_hard_failure or strict_gate_fail`; STANDARD VALIDATION_FAIL preserved; STRICT preserved | PASS | `executor.py:572-585` — outer `if is_failure:` then inner `if is_hard_failure or strict_gate_fail:`. STANDARD VALIDATION_FAIL → is_failure=T, is_hard_failure=F, strict=F → no halt. |
| 3 | STRICT VALIDATION_FAIL cannot leak past the STANDARD path | PASS | `executor.py:759-762` — STRICT gate fail sets status=HALT (hard), STANDARD sets VALIDATION_FAIL. So VALIDATION_FAIL only ever arises STANDARD-tier. Internally consistent. |
| 4 | `MissingArtifactError(FileNotFoundError)` carrying `path`+`producer_step` | PASS | `prompts.py:50-64` — subclasses FileNotFoundError; `__init__` sets `self.path`, `self.producer_step`; message names artifact + producer. |
| 5 | BOTH helpers present with correct return types | PASS | `prompts.py:67-71` `_read_required`→`str`; `74-78` `_load_json_required`→`dict`. Both `.is_file()`-guard then delegate to base reader. |
| 6 | EXACTLY five REQUIRED Stage-A reads converted, correct helper per type | PASS | `prompts.py:189` (parsed-request.json,"parse-request",dict), `290` (scope-discovery-raw.md,"scope-discovery",str), `293` (parsed-request.json,"parse-request",dict), `377` (research-notes.md,"research-notes",str), `479` (research-notes.md,"research-notes",str). Enumerated via grep — exactly 5 call sites, no more. |
| 7 | dict sites use `_load_json_required` (NOT str helper) | PASS | Both parsed-request.json sites (189, 293) use `_load_json_required`. No JSON site wrapped by the str helper. |
| 8 | Four Stage-B `_derive_*` reads remain `.is_file()`-guarded, UNCHANGED | PASS | `prompts.py:779` (notes, `.is_file()`), `794` (parsed, `.is_file()`), `826` (scope, `.is_file()`), `848` (research_dir, `.is_dir()`). All guarded; none converted. |
| 9 | Adjacent `skill_refs_dir` reads remain `_read_file` | PASS | `prompts.py:480-484` — five skill_refs reads all `_read_file`; `579` task-file glob read also `_read_file`. Correctly NOT converted (not the 5 required artifacts). |
| 10 | `_build_prompt` catch at CALL SITE (executor ~682), catches `MissingArtifactError` specifically, returns HALT naming artifact+producer | PASS | `executor.py:688-700` — local import of MissingArtifactError, `try: self._build_prompt(...) except MissingArtifactError as exc:` → `PrdStepResult(status=HALT, halt_reason=f"missing required artifact {exc.path.name} (producer: {exc.producer_step})")`. |
| 11 | Catch does NOT live inside `_build_prompt` (tests monkeypatch it) | PASS | `_build_prompt` body read in full (`executor.py:1224-1260`) — contains NO MissingArtifactError handling. Catch is strictly at the caller. |
| 12 | No collision with the unrelated `except OSError` (raw_output read) | PASS | `executor.py:727-730` — the bare `except OSError` wraps `output_file.read_text` (raw_output), which is AFTER and OUTSIDE the `_build_prompt` try (690-700). The 690 try catches `MissingArtifactError` specifically, not bare OSError. No accidental swallow. |
| 13 | `halt_reason` field added to PrdStepResult | PASS | `models.py:245-248` — `halt_reason: Optional[str] = None` on PrdStepResult dataclass. |
| 14 | All required tests exist and PASS | PASS | `test_models.py:90-121` is_hard_failure membership; `test_e2e.py:720,765,814,846` four scenarios. Independent run: all 5 PASSED. |
| 15 | Atom 2 missing-artifact test uses the REAL `_build_prompt` (not monkeypatched stub) | PASS | `test_e2e.py:828-841` — comment "Intentionally do NOT stub _build_prompt"; calls `_run_subprocess_step("research-notes",...,"build_research_notes_prompt")` so the real builder raises MissingArtifactError; asserts HALT + halt_reason names both `scope-discovery-raw.md` and `scope-discovery`; `mock_process_cls.assert_not_called()`. |
| 16 | ruff clean on edited files | PASS | `uv run ruff check src/superclaude/cli/prd/ tests/cli/prd/` → "All checks passed!" |
| 17 | verify-sync/lint failures caused ONLY by pre-existing orphans, NOT task files | PASS | Proven below (see Independent Build Results). Orphans: `sc-persona-research-protocol`, `sc-recommend-protocol`, `recommend.md`. None are PRD files. |

## Summary
- Checks passed: 17 / 17
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (none found)

## Independent Test Results

```
$ uv run pytest tests/cli/prd/ -v
============================= 157 passed in 0.59s ==============================
```

The four+1 required new tests, explicitly confirmed PASSED in my own run:
- `test_models.py::TestPrdStepStatusProperties::test_is_hard_failure_membership`
- `test_e2e.py::test_e2e_standard_tier_error_halts_pipeline`
- `test_e2e.py::test_e2e_standard_tier_validation_fail_does_not_halt`
- `test_e2e.py::test_missing_required_artifact_yields_graceful_halt` (real `_build_prompt`)
- `test_e2e.py::test_e2e_scope_discovery_error_halts_before_research_notes`

The validation summary's claimed count (157) matches my independent run exactly.

## Independent Build Results (`make verify-sync` / `make lint` claim verification)

Both fail, AS CLAIMED. I verified the cause is pre-existing orphans, NOT this task:

- `verify-sync` drift: `❌ MISSING in src/superclaude/skills/: sc-persona-research-protocol` and `sc-recommend-protocol` — these exist in `.claude/skills/` but NOT in `src/superclaude/skills/` (dev-copy orphans). Neither is a PRD pipeline component.
- `lint-architecture` error (the single error): `src/superclaude/commands/recommend.md has ## Activation but no matching skill directory: sc-recommend-protocol`. `recommend.md` was last touched by PR #127 (`feat(sc:recommend)`), unrelated to this fix.
- `git status --porcelain` of changed files shows EXACTLY the 5 expected task files modified: `executor.py`, `models.py`, `prompts.py`, `test_e2e.py`, `test_models.py`. None of the 5 appear in any drift/lint failure line.

Conclusion: AC #6's "fails ONLY on pre-existing orphans unrelated to this task" is TRUE and independently proven.

## Issues Found

None.

## Actions Taken

None — zero issues found. No in-place fixes were required. Per protocol, re-run of `uv run pytest tests/cli/prd/ -v` and `uv run ruff check` was still performed independently (results above).

## Adversarial Self-Audit

- Could a sixth required read have been missed? Grep for ALL `_read_required`/`_load_json_required` call sites returns exactly 5 (lines 189/290/293/377/479). Grep for remaining bare `_read_file(`/`_load_json(` returns only helper bodies (71/78), skill_refs reads (480-484), and the task-file glob read (579) — none of which are the five canonical Stage-A required artifacts. No over- or under-conversion.
- Could the OSError catch swallow MissingArtifactError? No — the 690 try/except is `except MissingArtifactError` (specific subclass), and it lexically precedes and is disjoint from the bare `except OSError` at 729 (raw_output read region). Verified by reading both blocks.
- Could the Atom 2 test be a false-green via the monkeypatch stub? No — it deliberately omits the stub and asserts `mock_process_cls.assert_not_called()`, proving the HALT short-circuited before subprocess creation through the real builder.
- Does Atom 1 break budget exhaustion? No — `_run_subprocess_step` returns `QA_FAIL_EXHAUSTED` on budget guard (executor.py:675-678), which IS in `is_hard_failure`; `test_e2e_budget_exhaustion` still PASSED.

## Confidence

**Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**

**Tool engagement:** Read: 7 | Grep: 5 | Glob: 0 | Bash: 8 (incl. 2 test/ruff runs, 3 build/lint runs, 3 grep-via-bash) — tool-call count exceeds the 17 checklist items; no padding. No web research performed (no external claims in scope); Tavily not invoked.

## Recommendations

- Proceed to mark the task Done. The two atoms are correctly implemented, internally consistent, fully tested, and ruff-clean.
- The `verify-sync` / `lint` failures are PRE-EXISTING and out of scope for this task; do NOT block the PRD fix on them. (Separate cleanup: either remove the orphaned `.claude/skills/sc-persona-research-protocol` + `sc-recommend-protocol` dev copies or restore their `src/` sources, and reconcile `recommend.md`'s `## Activation` reference — tracked independently of this fix.)

## QA Complete
