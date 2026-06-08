# QA Report — Phase-Gate (Phase 2: F2 typed malformed-artifact guard)

**Topic:** TASK-RF-20260608-144157 — F2 malformed-artifact guard (PRD pipeline hardening)
**Date:** 2026-06-08
**Phase:** phase-gate (Phase 2 / Steps 2.1, 2.2, 2.3)
**Fix cycle:** N/A
**Fix authorization:** true

---

## Overall Verdict: PASS

Zero issues found. Every acceptance criterion verified against live source with tool evidence, including an empirical falsification test (guard removed → test fails with uncaught JSONDecodeError → guard restored → green). No fixes required.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `MalformedArtifactError` subclasses `MissingArtifactError` EXACTLY | PASS | prompts.py:67 `class MalformedArtifactError(MissingArtifactError):` |
| 2 | Sets `self.path` + `self.producer_step` (parent attrs for `exc.path.name`/`exc.producer_step` HALT path) | PASS | prompts.py:81-82 sets both attrs in `__init__(self, path, producer_step)` |
| 3 | Message describes MALFORMED/UNPARSEABLE (not "is missing") | PASS | prompts.py:85-87 "is malformed/unparseable — its producer step '...' did not write valid JSON." Uses `FileNotFoundError.__init__` (bypasses parent "is missing" msg, prompts.py:83) |
| 4 | `_load_json_required` wraps `_load_json` in `try/except json.JSONDecodeError` raising `MalformedArtifactError(path, producer_step) from exc` | PASS | prompts.py:107-112 — guards `is_file()` then `try: return _load_json(path) except json.JSONDecodeError as exc: raise MalformedArtifactError(...) from exc` |
| 5 | `json` imported at module top | PASS | prompts.py:15 `import json` |
| 6 | No existing function signatures changed; `MissingArtifactError` message unchanged | PASS | prompts.py:58-64 parent `__init__`/message identical to discovery note; `_read_required`/`_load_json` signatures unchanged |
| 7 | No placeholder/TODO remains | PASS | grep for TODO/TBD/FIXME/PLACEHOLDER in the changed regions: none |
| 8 | Circular-import safety: no module-level import of `_STEP_ARTIFACT_FILES`/executor into prompts.py | PASS | prompts.py top imports only `json`, `datetime`, `pathlib`, `typing`, `._artifact_patterns`; executor import is LOCAL inside `_run_subprocess_step` (executor.py:692), not the reverse |
| 9 | F2 test does NOT stub `_build_prompt` on path under test | PASS | test_e2e.py:870-871 explicit comment + no `executor._build_prompt =` assignment in the test body (lines 845-886) |
| 10 | Test writes malformed `parsed-request.json`, invokes REAL required-read path | PASS | test_e2e.py:865-867 writes `"{not valid json"`; line 873-875 calls real `_run_subprocess_step("scope-discovery", ..., "build_scope_discovery_prompt")` whose first read is `_load_json_required(parsed-request.json, "parse-request")` (prompts.py:223-225) |
| 11 | Test asserts graceful HALT (status==HALT + halt_reason references malformed artifact) | PASS | test_e2e.py:878-886 asserts `status == PrdStepStatus.HALT`, `"parsed-request.json"`, `"parse-request"`, `"malformed"` in halt_reason, and `PrdClaudeProcess` not called |
| 12 | Executor tweak ONLY derives verb, does not alter HALT behavior | PASS | executor.py:699 `verb = "malformed" if isinstance(exc, MalformedArtifactError) else "missing"`; HALT structure (status/exit_code/halt_reason shape) unchanged from discovery note |
| 13 | `MalformedArtifactError` imported alongside `MissingArtifactError` in executor | PASS | executor.py:692 `from .prompts import MalformedArtifactError, MissingArtifactError` |
| 14 | Existing missing-artifact tests still assert on name+producer (not literal "missing") | PASS | test_e2e.py:838-839 + 982-983 assert artifact name + producer step only; grep confirms no halt_reason assertion on word "missing" |
| 15 | ruff clean on prompts.py + executor.py + test_e2e.py | PASS | `uv run ruff check` → "All checks passed!" |
| 16 | Full PRD suite green, 159 passed (baseline 158 + 1), zero regressions | PASS | `uv run pytest tests/cli/prd/` → 159 passed in 0.56s |
| 17 | New test PASSES and would FAIL without the guard | PASS | Empirical: reverted guard → `test_malformed_required_artifact_yields_graceful_halt` FAILED with uncaught `json.decoder.JSONDecodeError` escaping through `_build_prompt` (prompts.py:39); restored guard → green |
| 18 | Discovery note (f2-confirm.md) accurate vs live source | PASS | Note's recorded line ranges, `_load_json_required` body, and call-site catch verified verbatim against current prompts.py/executor.py |

## Summary
- Checks passed: 18 / 18
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (none required)

## Issues Found
None.

## Falsification Evidence (adversarial proof the test is real)
Removed only the `try/except json.JSONDecodeError` (reverting `_load_json_required` to its pre-F2 unguarded `return _load_json(path)`) and ran the new test in isolation:
- Result: FAILED — `json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes` propagated up through `build_scope_discovery_prompt` → `_build_prompt` → uncaught. This is precisely the crash-class (uncaught JSONDecodeError escaping `run()`) that F2 closes.
- Restored the guard (byte-identical); suite returns to 159 passed.
This proves the test genuinely exercises the guard and is not a tautology that would pass regardless.

## Actions Taken
No fixes applied — all 18 checks passed on first verification. Source files left unchanged (temporary revert was fully restored; `/tmp` backup removed).

## Confidence
- **Confidence:** Verified: 18/18 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 4 | Grep: 4 | Glob: 0 | Bash: 7
- No UNCHECKED items.
- No UNVERIFIABLE items.
- No web research performed (all claims are local/source-truth — no external lookup required).

## Recommendations
- Green light. Phase 2 (F2) is complete and correct. Proceed to Phase 3 (F4).

## QA Complete
