# Reviewer Card 2 — QA Persona (Review #178 / FR-028)

## Findings

### F-1: Shared-args path is correctly exercised by the 3 new tests
**Claim:** The three new tests in `test_recipe_bare_review.py` deliberately OMIT `status` from `recipe_args`, which is the exact production shared-args shape. The dispatcher injects `worker.status` per-worker via the dict-copy on line 448.
**Evidence:**
- `test_dispatcher_threads_per_worker_status_for_salvage` (line 275-300): no `"status"` key in recipe_args, parse_error worker promoted to success. PASS.
- `test_dispatcher_unrecoverable_parse_error_stays_failed_shared_args` (line 303-330): no `"status"` key, parse_error stays parse_error, no final file written. PASS.
- `test_dispatcher_shared_args_mixed_statuses` (line 333-361): ONE shared dict drives 3 workers; asserts `[success, success, parse_error]` + `"status" not in shared_args` (immutability guard). PASS.
**Severity:** INFO (confirming correctness)
**Classification:** Grounded
**All 3 tests pass** (`uv run pytest tests/swarm/test_recipe_bare_review.py -v` → 14/14 passed).

### F-2: `test_recipe_args_forwarded` correctly updated (not loosened)
**Claim:** The dispatcher-level test in `test_normalize.py:198` (`test_recipe_args_forwarded`) was updated to assert that `status` is injected per-worker while the REST of recipe_args forwards verbatim.
**Evidence:** Read `tests/swarm/test_normalize.py:198-224`. The test passes `recipe_args={"cap": 4000, "lens": "bare-review"}`, uses a `_CapturingRecipe` to capture what the recipe received, and asserts `captured["args"] == {"cap": 4000, "lens": "bare-review", "status": "success"}`. The comment on lines 216-219 explicitly documents the FR-028 behavior. The assertion is tighter (more specific), not looser.
**Severity:** INFO (confirming correctness)
**Classification:** Grounded

### F-3: No regression — full swarm suite 2215/0
**Claim:** `normalize_wave2` is shared across all lenses. Threading per-worker `status` via dict-copy (`{**args, "status": worker.status}` at normalize.py:448) cannot mutate the original shared dict. All existing tests still pass.
**Evidence:** `uv run pytest tests/swarm/ -q` → **2215 passed, 27 skipped, 0 failed**. Four recipes read `args.get("status", "success")`: `bare_review_v1.py:249`, `findings_table_v1.py:296`, `verdict_only_v1.py:406`, `hypothesis_table_v1.py:362`. All use `.get()` with a default so the injection is additive, not overriding. Even if an old test explicitly passes `"status": "parse_error"` in recipe_args, the per-worker copy overwrites it with `worker.status` which is correct (the worker's status is the real upstream status).
**Severity:** INFO (confirming no blast-radius)
**Classification:** Grounded

### F-4: Edge case — proxy_error and timeout workers are correctly short-circuited
**Claim:** `normalize.py:424` checks `if worker.status in {"timeout", "proxy_error"}` BEFORE the status injection at line 448. The injection never fires for hard-failure workers. The existing `test_hard_failure_skips_normalize_but_emits_meta` in `test_normalize.py:254-269` covers both.
**Evidence:** Read normalize.py:424 — the short-circuit returns before line 448. The `@pytest.mark.parametrize` test covers both `timeout` and `proxy_error`.
**Severity:** INFO (confirming correctness)
**Classification:** Grounded

### F-5: MISSING TEST — empty-body success worker with injection
**Claim:** No test exercises a worker with `status="success"` + empty body through the new injection path. `_read_raw` (normalize.py:334-342) returns `""` when neither `worker.body` nor `worker.raw_path` yields content. The recipe at bare_review_v1.py:267 sees empty raw and returns `NormalizedResult(text="", salvaged=False, error="empty raw body")`. This is functionally equivalent to the parse_error branch (no final file, error on sidecar) even though the worker came in as `success`.
**Evidence:** Read normalize.py:493 — `if worker.final_path and result.text:` — empty text means no atomic write fires. No test in `test_normalize.py` or `test_recipe_bare_review.py` explicitly creates a success worker with empty body and verifies the injection path handles it.
**Severity:** MINOR — the code path is safe (empty text → no write, error on sidecar) but untested with the new injection line. The `_PassthroughFallback` test at line 117 sends `body="hello\n"` which is non-empty.
**Classification:** Inferred

### F-6: MISSING TEST — WorkerResult with `status=None` (None attribute)
**Claim:** `WorkerResult.status` is typed as `WorkerStatus = Literal["success", "timeout", "parse_error", "proxy_error"]` with a default of `"success"` (models.py:1125). The `__post_init__` validates against `typing.get_args(WorkerStatus)`. If someone bypasses the constructor and sets `worker.status = None` after construction, the injection at line 448 does `{**args, "status": None}`. The recipe then does `str(args.get("status", "success"))` which yields `"None"` (string), not `"parse_error"`. The salvage gate at `normalize.py:163` checks `worker_result.status != "parse_error"` — this compares the WorkerResult's `status` (None), NOT the injected args value. So salvage is correctly rejected (None != "parse_error"), but the recipe sees `"None"` as its status string, which doesn't match any branch.
**Evidence:** Read models.py:1125 (status default `"success"`), normalize.py:448 (injection), normalize.py:163 (salvage gate reads `worker_result.status`, not args).
**Severity:** MINOR — requires post-construction mutation of a dataclass field. The dataclass-level validation (models.py:1131-1133) would catch this at construction time. No test exercises this pathological case, which is acceptable.
**Classification:** Inferred

### F-7: Other recipe tests still use OLD pattern (explicit status in recipe_args)
**Claim:** The three other lens recipe test files (`test_recipe_findings_table.py`, `test_recipe_hypothesis_table.py`, `test_recipe_verdict_only.py`) ALL still pass `"status"` explicitly in every `recipe_args` dict. This means their tests don't exercise the shared-args path that FR-028 was designed for.
**Evidence:** Read `test_recipe_findings_table.py:233-246` — includes `"status": "success"`. Read `test_recipe_hypothesis_table.py:248-261` — includes `"status": "success"`. Read `test_recipe_verdict_only.py:275-288` — includes `"status": "success"`. All three pass status explicitly. Since the injection overwrites whatever is in recipe_args, the tests still pass correctly, but they don't exercise the actual production shape (omitted status).
**Severity:** MINOR — tests still pass and cover the correct behavior, but they test the pass-through case (status in recipe_args → overwritten by injection) rather than the shared-args case (status omitted → injected). A future PR should add shared-args variants to these test files for parity with `test_recipe_bare_review.py`.
**Classification:** Grounded

## Deviation Classification

| Finding | Type |
|---------|------|
| F-1 | NO_DEVIATION (tests correct) |
| F-2 | NO_DEVIATION (test correctly tightened) |
| F-3 | NO_DEVIATION (no regression) |
| F-4 | NO_DEVIATION (short-circuit correct) |
| F-5 | MISSING_TEST_COVERAGE |
| F-6 | MISSING_TEST_COVERAGE (pathological) |
| F-7 | INCOMPLETE_TEST_COVERAGE (other lenses) |

## Calibrated Confidence (5 dimensions)

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Test adequacy | 0.75 | 3 new tests cover the critical shared-args path; other lenses lack shared-args variants (F-7); empty-body edge case untested (F-5) |
| Regression safety | 0.95 | 2215/0 full suite pass; dict-copy injection is additive-safe; all 4 recipes use `.get()` with defaults |
| Code correctness | 0.90 | Injection is on line 448, after short-circuit (line 424), before recipe call (line 451). Salvage gate reads worker_result.status (line 163), not args — correct separation. |
| Edge case coverage | 0.65 | proxy_error/timeout short-circuit tested; empty-body success NOT tested; None-status pathological NOT tested (acceptable) |
| Blast radius | 0.90 | All lenses use `.get("status", "success")` default so injection is additive. `normalize_wave2` feeds resume path + all lenses — injection is per-worker copy, safe. |

**Overall confidence: 0.83**

## Verdict: PASS

The change is well-tested for its primary purpose (threading per-worker status into the shared recipe_args path). The 3 new tests correctly exercise the shared-args shape by omitting `status` from recipe_args. The full swarm suite (2215/0) confirms no regression. The injection is safe (dict-copy, additive, after hard-failure short-circuit). Minor findings are gaps in secondary test coverage, not correctness issues with the change itself.

**Top finding (F-7):** Other lens recipe tests (findings_table, hypothesis_table, verdict_only) still pass `status` explicitly in recipe_args, so they test the overwrite path rather than the actual production shared-args shape. These should get shared-args variants for parity with `test_recipe_bare_review.py`. Evidence: `test_recipe_findings_table.py:233` `"status": "success"` in recipe_args.
