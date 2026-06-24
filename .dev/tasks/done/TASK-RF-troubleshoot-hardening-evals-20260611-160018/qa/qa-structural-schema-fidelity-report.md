# QA Report — Structural Schema + Fidelity (catch_rate)

**Topic:** catch_rate.schema.json + test_catch_rate_schema.py fidelity (sc:troubleshoot pipeline-hardening backtest)
**Date:** 2026-06-12
**Phase:** task-integrity / structural-schema-fidelity (report-only)
**Fix cycle:** N/A
**Fix authorization:** false (modified NO source file)

---

## Overall Verdict: PASS

Adversarial stance applied: assumed >=5 errors, attempted to break the schema (metaschema, pattern enforcement, fixture pass/fail paths, real-producer routing, enum verbatim match, $def provenance). Every one of the 5 verification criteria holds up under independent tool-verified execution. No CRITICAL/IMPORTANT/MINOR issues found.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Valid draft-2020-12 (`Draft202012Validator.check_schema`) | PASS | Bash `uv run python` ran `check_schema` on `catch_rate.schema.json` → `check_schema: PASS`. `$schema` declares `.../draft/2020-12/schema` (schema:2). |
| 2 | `$defs` enums match model verbatim | PASS | Schema `backtestStatus.enum` = `[not_run, partial, complete]` (catch_rate.schema.json:72-76) == `BACKTEST_STATUS_VALUES` (catch_rate.py:33-37, runtime print `('not_run','partial','complete')`). `verdict.enum` = `[CATCH, MISS]` (schema:103-106) == `VERDICT_CATCH/VERDICT_MISS` (catch_rate.py:26-27). |
| 3 | Loader is wheel-safe `importlib.resources`, mirrors summary `__init__.py` | PASS | `__init__.py:28-32` uses `resources.files(__name__).joinpath(...).read_text(...)` — no `Path(__file__)` relative tricks; returns freshly decoded mapping per call (:33). Mirrors the summary schemas pattern as the module docstring claims (:7). |
| 4 | Fidelity test validates REAL `render_catch_rate_json` output (not hand-built dict) | PASS | test (b) `test_backtest_render_output_validates_against_schema` (test:72-94) builds via `build_catch_rate_report(...)` then `json.loads(render_catch_rate_json(report))` and `validator.validate(payload)` — routes through the production producer+writer. Independently replicated: status=partial, caught=3, missed=2, key order == required order. |
| 5 | Both pass + `pytest.raises(ValidationError)` paths exercised; escapeId `^E[0-9]+$` is this schema's OWN $def (not claimed-reused) | PASS | Valid path: test:268-270 validates `valid_minimal.json`+`valid_full.json`. Invalid path: test:273-278 `pytest.raises(ValidationError)` over `invalid_bad_status.json`+`invalid_bad_verdict.json`. Independently confirmed both raise (`'BOGUS' is not one of...`, `'WRONG' is not one of...`). `escapeId` declared fresh at schema:79-82 with self-documenting note; verified NOT present in summary.schema.json (no escape-id/eval-id pattern $def — confirmed by full read of summary.schema.json:72-251). Pattern is actually enforced (mutated `X9` → ValidationError `'X9' does not match '^E[0-9]+$'`), not a dead $def. |

## Summary
- Checks passed: 5 / 5
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

## Adversarial probes that did NOT find a defect (negative results, for audit honesty)
| Probe | Hypothesis | Result |
|-------|-----------|--------|
| Mutate `escape_id` to `X9` in a valid payload | escapeId $def is decorative / not $ref'd on a live path | REJECTED — `escapeResult.properties.escape_id` `$ref`s `#/$defs/escapeId` (schema:96); mutation raises ValidationError. |
| Run full suite | Tests assert but don't actually exercise schema | REJECTED — 14/14 pass in 0.05s. |
| Check `additionalProperties: true` (schema:19, :94) | Loose top-level allows junk to pass silently | NOT A DEFECT — intentional + documented; required-set + enum + pattern $refs still gate the load-bearing fields. Mirrors summary.schema.json:18 idiom. Count-balance (`caught+missed==total`) is explicitly delegated outside the schema to `__post_init__`/`_check` (schema:5, catch_rate.py:142-148, catch_rate_report.py:45-61) and IS tested (test:127-160). |
| Compare required order vs test pin vs producer key order | Order drift between schema/test/producer | REJECTED — all three identical: schema:7-18 == test:99-110 == runtime `to_dict()` key order (walks `_CATCH_RATE_FIELDS`, catch_rate.py:48-59,198). |

## Issues Found
None.

## Actions Taken
None (report-only; fix_authorization: false). No source file modified.

## Recommendations
- None blocking. Optional (MINOR, not a gate failure): the schema intentionally does not enforce `caught+missed==total_escapes` or the anti-vacuity derivation (both delegated to `__post_init__`/`_check` and covered by tests b/d/f). This is correctly documented at schema:5 and is the same separation-of-concerns the summary schema uses — no change needed.

## Confidence
- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 0 | Glob: 0 | Bash: 5
- Tavily/web: not required (no external/URL/standards-bound claim; all verification was source-truth-local).
- Every VERIFIED item cites specific file:line + a tool-call output (check_schema run, fixture validation run, pattern-mutation run, real-producer replication run, full pytest run). Tool calls (13 Read+Bash) >= 5 checklist items → engagement minimum satisfied.

## QA Complete
