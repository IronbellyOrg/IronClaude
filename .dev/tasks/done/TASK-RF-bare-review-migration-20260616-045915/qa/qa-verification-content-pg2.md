# QA Verification Report — Phase Gate 2 content-fidelity re-check (PG2.5)

**Topic:** WS-0 inline-path Wave 1→2→3 migration for `swarm run --lens bare-review`
**Date:** 2026-06-16
**Phase:** task-qualitative (PG2 fix verification — behavioral fidelity)
**Fix cycle:** verification of PG2 fixes (`fix_authorization: false` — REPORT ONLY)
**Mandate:** Confirm the PG2 fixes (C1 FIXED, C2 DEFERRED, C3 FIXED, C4 FIXED) preserve LEGACY behavioral fidelity and introduce no behavioral drift.
**Legacy reference:** `src/superclaude/skills/sc-bare-review/scripts/t2_normalize.py:292-295`

---

## Overall Verdict: PASS

The headline IMPORTANT defect (C1 — unsubstituted `recommended_next_command` placeholders) is
**genuinely fixed and reproduces the legacy comma-join behavior byte-for-byte** under a live
`--transport stub` run. The C2 deferral to Phase 4 (WS-B byte-parity) is a **sound engineering
judgment, not a hidden defect**: the empty body `reviewer_model_id` is recoverable (the contract
`output_files[].model_id`, the filename, and the verdict line all carry the model) and is genuinely
cosmetic under the single-model stub, and the attempted fix demonstrably broke a real cross-cutting
shared-helper contract (`test_recipe_args_forwarded`). C3 (doc label) is corrected and matches the
raw gate evidence. No behavioral drift was introduced in the reviewers/label/line-cap/timeout flags;
full swarm suite is green (2218 passed / 0 failed).

---

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | C1 reproduces legacy `recommended_next_command` | none | PASS | Live contract `recommended_next_command` whitespace-normalized-EXACT-matches the legacy `t2_normalize.py:293-295` comma-join shape (compare leads with `<existing-review>` then 3 success `final_path`s; suspect = same 3 paths). No `{suspect_files}`/`{compare_files}` placeholders remain. |
| 2 | C1 suspect:true + IMM-5 success-first still correct | none | PASS | Live contract `caller_metadata.suspect: true`; `status: success` with `workers_succeeded: 3 == workers_requested: 3` (M==N→success, legacy IMM-5 at t2_normalize.py:284-290). |
| 3 | C2 deferral is cosmetic-under-stub, not a defect | none | PASS | Contract `output_files[].model_id: lens-default-model-0` carries per-worker model; body frontmatter `reviewer_model_id: ""` is the only empty surface. Under single-model stub all 3 workers ARE `lens-default-model-0` (recoverable from contract + filename + `Verdict: stub:lens-default-model-0:…`). Loss only materializes under real multi-model `openai_compat`. |
| 4 | C2 deferral rationale (broke shared contract) is true | none | PASS | `tests/swarm/test_normalize.py:215-216` pins `normalize_wave2` VERBATIM recipe_args forwarding (`captured["args"] == {"cap":4000,"lens":"bare-review"}`). Injecting per-worker `model_id` keys breaks this; the contract is cross-cutting (all recipes + resume), broader than WS-0's "wire the inline path" mandate. |
| 5 | C3 doc label corrected | none | PASS | `ws0-gate-summary.md:37` now reads `normalize.py:73 — I001`; raw `ws0-gate.txt:149-150` confirms `I001 Import block un-sorted` at `cli/swarm/normalize.py:73`. Both ruff items still pre-existing, not WS-0-introduced. |
| 6 | No drift: --reviewers / --label flags | none | PASS | Live `--reviewers 4 --label pg2-caller-ctx` → `workers_requested:4`/`workers_succeeded:4`, body `caller_label: "pg2-caller-ctx"`, next_cmd populated with 4 success paths, 0 placeholders. `--reviewers 5` → exit=2 (EXIT_USAGE). |
| 7 | No drift: --target-line-cap / --timeout-sec | none | PASS | Live `--target-line-cap 2000 --timeout-sec 90` → exit=0, job dispatched. (Truncation field stays 4000 because the 8-line target is under any cap — effect not stub-observable, matches original report note; flag acceptance + spec-threading is the verifiable surface.) |
| 8 | C1 presence test no longer AX-4-weak | none | PASS | `test_e2e_user_guide.py:156,158` now asserts `"{suspect_files}" not in contract` AND `".final.md" in contract` — guards the actual defect, not just the `--suspect-source` substring. |
| 9 | C4 new tests exist + pass | none | PASS | `test_label_flag_stamps_caller_label_frontmatter`, `test_reviewers_flag_rejects_below_range`, `test_target_line_cap_and_timeout_flags_accepted` present + 4/4 targeted pass. |
| 10 | No regression: full swarm suite | none | PASS | `uv run pytest tests/swarm/` = **2218 passed / 26 skipped / 0 failed** (matches consolidated claim exactly). |

## Summary
- Checks passed: 10 / 10
- Checks failed: 0
- Issues found: 0 (the prior IMPORTANT C1 is resolved; C2 is an accepted, well-reasoned deferral)
- Issues fixed in-place: 0 (report-only)
- drift-axis baseline: BUILD_REQUEST.GOAL not supplied verbatim; legacy `t2_normalize.py:292-295`
  served as the parity baseline (same baseline as the original FAIL report). AX-1 lens applied
  against legacy source.

## C1 — live evidence (the resolved IMPORTANT)
Legacy (`t2_normalize.py:293-295`):
```
compare = ",".join(["<existing-review>", *success_paths])
suspect = ",".join(success_paths) if success_paths else "<no-bare-files>"
next_cmd = f"/sc:adversarial --compare {compare} --suspect-source {suspect}"
```
Live emitted contract (`/tmp/pg2cverif/return-contract.yaml`), whitespace-normalized:
```
/sc:adversarial --compare <existing-review>,/tmp/pg2cverif/bare-review-00-lens-default-model-0.final.md,…01….final.md,…02….final.md --suspect-source /tmp/pg2cverif/bare-review-00….final.md,…01….final.md,…02….final.md
```
Programmatic assertion (repo venv): `' '.join(nc.split()) == ' '.join(expected.split())` → **True**;
`'{suspect_files}' in nc` → **False**; `'{compare_files}' in nc` → **False**. Compare leads with
`<existing-review>`; suspect = the 3 succeeded `final_path`s. Exact legacy comma-join shape reproduced.

## C2 — why the deferral is sound, not a hidden defect
1. **Information is not lost under the tested path.** The contract `output_files[].model_id` carries
   `lens-default-model-0` for every worker; the on-disk filename carries it
   (`bare-review-00-lens-default-model-0.final.md`); and each body's `## Verdict` line carries it
   (`stub:lens-default-model-0:…`). The only empty surface is the body frontmatter
   `reviewer_model_id`/`reviewer_model_label`. Under the single-model stub all reviewers are the
   *same* model, so the empty field distinguishes nothing.
2. **The fix would break a real contract.** `test_normalize.py::test_recipe_args_forwarded` pins
   `normalize_wave2`'s documented VERBATIM recipe_args forwarding. Threading per-worker `model_id`
   into that shared helper changes a contract shared by all recipes + the resume branch — strictly
   broader than WS-0's "wire the inline path" mandate.
3. **The deferral target is correct.** WS-B (Phase 4) byte-parity against the real legacy golden is
   exactly where a multi-model `openai_compat` diff would force (and validate) the shared-helper
   change. The empty `reviewer_model_id` under stub does NOT block WS-0. Accepted deferral.

## Actions Taken
None — `fix_authorization: false`. All verification was independent tool engagement.

## Self-Audit
No `## Inherited Structural Verdict` block in the spawn prompt → standalone behavior; reliance audit N/A.

**(a) Reliance list — items taken on faith from the consolidated findings:** none. Every fix-outcome
claim was independently re-verified: C1 via a fresh live run (not by trusting the recorded contract
snippet); C2's "broke test_recipe_args_forwarded" by reading the test's verbatim-forwarding assertion;
C3 against the raw `ws0-gate.txt` evidence (not the summary); regression by re-running the full suite.

**(b) Independent semantic checks (tool evidence):**
- Legacy shape — Read `t2_normalize.py:270-312` (compare/suspect comma-join, IMM-5 284-290).
- C1 live — fresh `swarm run --lens bare-review --target /tmp/pg2c_target.py (151B) --output /tmp/pg2cverif --transport stub`; parsed contract via repo-venv PyYAML; whitespace-normalized exact-match vs reconstructed legacy expected string; placeholder-absence asserted.
- C2 — Read `test_normalize.py:198-216` (verbatim recipe_args contract); grep `reviewer_model_id`/`caller_label` across all 3 body frontmatters (empty); contract `output_files[].model_id` populated.
- C3 — `sed` `ws0-gate-summary.md:36-37` (corrected to I001) vs raw `ws0-gate.txt:148-150` (I001 confirmed); live `ruff check cli/swarm/normalize.py` reproduces I001 at :73.
- Drift — live `--reviewers 4 --label`, `--reviewers 5` (exit 2), `--target-line-cap 2000 --timeout-sec 90` (exit 0); inspected contracts + body frontmatter.
- Regression — `uv run pytest tests/swarm/` (2218 passed/0 failed) + targeted 4-test run (4 passed).

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 4 | Grep: 6 | Glob: 0 | Bash: 8

If I claimed PASS without evidence, the user should NOT believe it — so the PASS rests on a *fresh*
live run whose emitted contract exact-matches the legacy comma-join shape (the precise thing that was
broken in the original FAIL), plus a re-run of the full 2218-test swarm suite. The original FAIL was
caught by runtime inspection, not static reading; this verification used the same runtime method and
confirms the fix holds.

## Recommendations
1. **C1/C3/C4 fixes are sound — proceed past Phase Gate 2.** No further action on these.
2. **Carry C2 forward as a Phase-4 (WS-B) acceptance item**, not a blocker: the WS-B byte-parity gate
   against the real legacy golden must decide whether to thread per-worker `model_id` through
   `normalize_wave2` (with `test_recipe_args_forwarded` updated in lockstep). Document the empty
   stub `reviewer_model_id` as an intentional stub-path property in the migrated SKILL.md contract.
3. **Document narrowings N1–N3** (64-hex checksum, removed env-driven model-count ceiling, IMM-4
   no-contract-on-inline-path) in the migrated SKILL.md contract section, as already recommended.

## QA Complete
