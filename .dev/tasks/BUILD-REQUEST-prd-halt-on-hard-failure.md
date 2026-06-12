# BUILD_REQUEST

## GOAL
Apply the defense-in-depth fix from the troubleshoot report so the `superclaude prd run` pipeline halts gracefully on any upstream hard step failure instead of crashing the CLI with an uncaught `FileNotFoundError` on a missing artifact (e.g. `scope-discovery-raw.md`).

## WHY
When `scope-discovery` hard-ERRORs (subprocess exits non-zero; no artifact written), the Stage-A loop does not halt because the halt decision keys off the downstream gate *enforcement tier* (`STANDARD`, not `STRICT`) rather than whether the step actually crashed. The pipeline then advances to `research-notes`, whose prompt builder unconditionally reads the missing `scope-discovery-raw.md` in `_build_prompt` — which runs *outside* any try/except — so the exception escapes `executor.run()` (try/finally, no except) and kills the CLI with a raw traceback.

Full diagnosis + evidence: `.dev/troubleshoot/prd-scope-discovery-missing-artifact-20260608020200/REPORT.md`

## SCOPE / WHERE (source of truth — edit src/, then `make sync-dev` + `make verify-sync`)
- `src/superclaude/cli/prd/models.py` — add `PrdStepStatus.is_hard_failure` property.
- `src/superclaude/cli/prd/executor.py` — Stage-A halt logic (~lines 567-575); catch `MissingArtifactError` at the `_build_prompt` call site (~line 672).
- `src/superclaude/cli/prd/prompts.py` — add `MissingArtifactError`, `_read_required`, `_load_json_required`; convert the 5 required Stage-A reads.
- `tests/` (prd pipeline tests, e.g. `tests/cli/prd/`) — regression tests.

## WHAT TO IMPLEMENT (two atoms — Atom 1 is the foundation and MUST land first; Atom 2 depends on it)

### Atom 1 — Executor: halt on any hard execution failure, independent of gate tier
1. In `models.py` `PrdStepStatus`, add:
   ```python
   @property
   def is_hard_failure(self) -> bool:
       return self in {ERROR, TIMEOUT, QA_FAIL_EXHAUSTED, HALT}
   ```
   (Use the real enum-member references.) Deliberately EXCLUDE `VALIDATION_FAIL` (intentional non-fatal STANDARD gate-quality path, exit 0, artifact written — `executor.py:736-741`) and `QA_FAIL` (has its own retry cycle).
2. In `executor.py:567-575`, change the halt condition to halt on `step_result.status.is_hard_failure OR (gate STRICT-gate-fail)`, setting `halt_reason` to distinguish "hard failure: <status>" vs "STRICT gate failure: <status>". Preserve existing STRICT behavior exactly.

### Atom 2 — Prompt builders: typed catchable error for missing REQUIRED artifacts (DEPENDS ON Atom 1)
1. In `prompts.py`, add `class MissingArtifactError(FileNotFoundError)` carrying `path` + `producer_step` with a clear message.
2. Add `_read_required(path, producer_step, max_bytes=50_000) -> str` (wraps `_read_file`) and `_load_json_required(path, producer_step) -> dict` (wraps `_load_json`). TWO helpers because the reads split across two return types.
3. Convert the 5 required Stage-A reads:
   - `_read_required`: `prompts.py:257` (`scope-discovery-raw.md`), `340` and `440` (`research-notes.md`).
   - `_load_json_required`: `prompts.py:158` and `258` (`parsed-request.json`).
   - Leave the 4 Stage-B `_derive_*` reads (`740/755/775/787`) UNCHANGED — they are correctly guarded/optional.
4. In `executor._build_prompt` (real call site `executor.py:672`), catch `MissingArtifactError` → return `PrdStepResult(status=PrdStepStatus.HALT, ...)` with `halt_reason` naming the missing artifact + its producer step. (Note: `MissingArtifactError ⊂ OSError`; the only nearby `except OSError` is `executor.py:701`, a different region — no collision.)

## TESTS (mandatory)
- Atom 1: a STANDARD-tier step returning `ERROR` MUST halt the pipeline; a STANDARD-tier step returning `VALIDATION_FAIL` (exit 0) MUST NOT halt. Confirm existing budget-exhaustion / STRICT-halt tests still pass.
- Atom 2: a missing required upstream artifact yields a graceful HALT (no uncaught `FileNotFoundError`, no raw traceback). The test MUST exercise the REAL `_build_prompt` (do NOT stub it — it is monkeypatched at `tests/.../test_e2e.py:549`, which would bypass the catch).
- End-to-end: simulate `scope-discovery` ERROR (non-zero exit, no artifact) → assert pipeline halts at `scope-discovery` with a clear reason and never reaches `research-notes`.

## CONSTRAINTS
- Edit `src/superclaude/cli/prd/` only; run `make sync-dev` then `make verify-sync`.
- UV for all Python ops. Feature/fix branch only — do NOT commit to master.
- Do NOT regress the intentional non-fatal STANDARD gate-quality degradation path.

## TEMPLATE
Template 02 (complex) — touches 4 files across executor/models/prompts + tests, with an ordering dependency between atoms.
