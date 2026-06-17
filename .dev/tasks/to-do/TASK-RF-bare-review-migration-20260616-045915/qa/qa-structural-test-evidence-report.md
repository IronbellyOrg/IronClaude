# QA Report — Structural / Test-Evidence Lens (WS-0 tests)

**Topic:** sc-bare-review M8/M9 migration — WS-0 e2e test coverage
**Date:** 2026-06-16
**Phase:** report-validation (structural test-evidence lens)
**Fix authorization:** false (REPORT ONLY)
**Adversarial stance:** assumed >=10 errors; verified every claim against source.

---

## Overall Verdict: PASS (with 1 MINOR documentation defect in the gate summary)

The five required verification axes all hold against real source + real runtime
output. No fabricated symbol, filename, or assertion was found. The single defect
is a misstatement in `ws0-gate-summary.md` about the *nature* of the second ruff
error — it does not affect the test correctness, the pass count, or the regression
conclusion, so the gate verdict stands.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Presence test asserts contract EXISTS + 3 normalized bodies w/ header + checksum | PASS | `test_e2e_user_guide.py:136` asserts `(out/RESULT_CONTRACT_FILENAME).exists()`; `:140-141` globs `bare-review-*.final.md` and asserts `len==3`; `:144` asserts `"T2-Bare Review" in body`; `:145` asserts `"target_checksum:" in body`. Header is REAL: `recipes/bare_review_v1.py:192` emits `f"# T2-Bare Review — {slug}"`. Checksum is REAL: `bare_review_v1.py:301` sets `"target_checksum": checksum` in the `fm` dict, rendered as `target_checksum: <val>` by `render_markdown` (`:184-190`). Contract assertions `status: success`/`workers_requested: 3`/`--suspect-source` at `:149-151` — `workers_requested` emitted by `reduce.py:651`; `--suspect-source` is the lens next-command at `bare_review.py:67`. Runtime: `ws0-presence-test.txt:12` shows this exact test PASSED. |
| 2 | Absent-test narrowed to match real WS-0 emission scope (only done.json absent) | PASS | `ws0-emission-scope.md:34-37` decided: contract + bodies + `merged.md` PRESENT, only `done.json` ABSENT. `test_quickstart_does_not_emit_done_sentinel` (`:107-120`) asserts ONLY `not (out/DONE_SENTINEL_FILENAME).exists()` — it does NOT assert merged.md or contract absent. `test_quickstart_lens_bare_review_emits_observability_artifacts` (`:80-104`) uses SUBSET `{...} <= names` (`:95-100`), NOT exact-set `==`, so WS-0's extra artifacts (contract/bodies/merged) cannot violate it. Both correctly conform to the scope decision. |
| 3 | No fabricated filename/symbol; every imported symbol real; glob matches CLI output | PASS | All imports verified real in `commands.py`: `RESULT_CONTRACT_FILENAME`=`return-contract.yaml` (`:86`), `DONE_SENTINEL_FILENAME`=`done.json` (`:113`), `EXIT_OK`=0 (`:188`), `EXIT_USAGE`=2 (`:190`), `SWARM_STATE_FILENAME` (`:85`), `EXECUTION_LOG_*` (`:99-100`), `TERMINAL_STATE_VALUE` (`:87`). `MANIFEST_FILENAME`/`MERGED_FILENAME` defined locally (`test:39-40`). Glob `bare-review-*.final.md` matches the real `<lens>-NN-<slug>.final.md` naming the normalizer writes to `final_path` (`normalize.py:482-483`). |
| 4 | Reviewers tests prove `--reviewers 4`→4 workers; out-of-range→EXIT_USAGE | PASS | `test_reviewers_flag_overrides_worker_count` (`:230-242`) asserts `"workers=4, results=4"` in stdout AND `manifest["preflight"]["workers_requested"] == 4`. Flag handling REAL: `commands.py:1637-1648` sets `workers_override["count"]=reviewers`. `test_reviewers_flag_rejects_out_of_range` (`:245-253`) with `--reviewers 5` asserts `EXIT_USAGE`; source `commands.py:1638-1644`: `if reviewers < 2 or reviewers > 4` → `raise click.exceptions.Exit(EXIT_USAGE)`. Range/exit faithful. |
| 5 | Gate summary baseline comparison: 2212→2215, 0 failed, derived from real output | PASS (with MINOR defect, see Issue 1) | `baseline-pytest-swarm.txt:135` = `2212 passed, 26 skipped`; `ws0-gate.txt` final line = `2215 passed, 26 skipped`; +3 delta = the 3 net-new WS-0 tests. 0 failed confirmed in both raw files. Numbers are real, not fabricated. |

## Summary
- Checks passed: 5 / 5
- Checks failed: 0
- Critical issues: 0
- Issues found: 1 (MINOR — documentation only)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | `ws0-gate-summary.md:37` | Summary claims the second pre-existing ruff error is `normalize.py:73 — same F821 Logger forward-ref pattern`. The raw `ws0-gate.txt` shows `normalize.py:73` is actually **`I001 Import block is un-sorted or un-formatted`**, NOT `F821 Logger`. Only `commands.py:1712` is the F821 Logger error. The summary mislabels the error class. | Correct `ws0-gate-summary.md:37` to read `normalize.py:73 — I001 import-block un-sorted (auto-fixable)`. Does NOT change the PASS verdict: both errors are still confirmed pre-existing/untouched-by-WS-0 and `normalize.py` import ordering is not a WS-0-introduced regression. |

## Adversarial probes that did NOT find issues (evidence of thoroughness)
- Probed for a fabricated `T2-Bare Review` header: initially absent in a dir-scoped grep, then confirmed REAL at `recipes/bare_review_v1.py:192` (recipe used by `normalize_wave2`). Not a fabrication.
- Probed whether `target_checksum:` is actually rendered into bodies: confirmed via the `fm` dict key (`bare_review_v1.py:301`) → `render_markdown` frontmatter loop (`:184-190`).
- Probed whether the absent-test still over-asserts (would break under WS-0's merged.md): confirmed it was narrowed to done.json-only and the observability test uses subset `<=`, not `==`. No stale over-assertion.
- Probed reviewers exit code: confirmed `EXIT_USAGE` (2) raised at source, matching test expectation (not a mismatched EXIT_INVALID).
- Cross-checked the +3 delta against the 3 named net-new tests; the 2 flipped/renamed tests correctly do not change the count.

## Confidence
**Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**
**Tool engagement:** Read: 8 | Grep: 9 | Glob: 0 | Bash: 6

Every check maps to direct source-or-runtime tool evidence (file:line anchored). No
external web lookup was required (all claims are local-source-bound).

## Recommendations
- Apply the MINOR fix to `ws0-gate-summary.md:37` (error-class mislabel). Non-blocking.
- Phase Gate 2 may proceed: tests are structurally sound, assert real symbols/files,
  prove the documented behavior, and show 0 regressions against the real baseline.

## QA Complete
