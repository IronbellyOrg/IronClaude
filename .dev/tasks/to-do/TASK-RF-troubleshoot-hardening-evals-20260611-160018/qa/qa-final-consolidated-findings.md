# Final Lens QA — Consolidated Findings

**Consolidated verdict: FAIL** (2 lenses FAIL + minor nits; FAIL if ANY agent reports ANY issue). One FAIL (consistency line-count) is a verified FALSE POSITIVE; the other (E4 heal-commit) is a REAL factual correction.

## Lens verdicts (7 final lens agents)

| Lens | Report | Verdict |
|------|--------|---------|
| Structural — template/structure | `qa-final-structural-template.md` | PASS (3 MINOR) |
| Structural — internal consistency | `qa-final-structural-consistency.md` | FAIL (1, FALSE POSITIVE — see F-4) |
| Structural — collision boundary | `qa-final-structural-collision.md` | PASS |
| Content — actionability/non-vacuity | `qa-final-content-actionability.md` | PASS (1 MINOR → F-2) |
| Content — numbers/metrics | `qa-final-content-metrics.md` | PASS |
| Content — crossref chain | `qa-final-content-crossref.md` | PASS |
| Content — NFR-1 fidelity + proxy honesty | `qa-final-content-nfr1-proxy.md` | FAIL (1 IMPORTANT → F-1, 2 MINOR) |

## Deduplicated issues

| # | Severity | File | Issue | Required fix | Lens |
|---|----------|------|-------|--------------|------|
| F-1 | IMPORTANT (REAL, git-verified) | `test_backtest_e4.py` (docstring L14, comments L43/L76, skip-reason) | The E4 HEAD-heal commit is cited as `20693bb8`, but git ground-truth shows `20693bb8` is NOT a HEAD ancestor (it's a sibling fix on another branch with the same intent). The actual HEAD-heal merged to this worktree is `acd5631f` (PR #158) — it adds the advisory branch to `_evaluate_gate` (HEAD executor.py:853-883). The task/research mis-cited `20693bb8`. Replay logic is UNAFFECTED (E4 still correctly pins to pre-fix parent `1b0264f1`). | Replace every `20693bb8` HEAD-heal citation in `test_backtest_e4.py` with `acd5631f` (#158), the actual commit that heals `_evaluate_gate` on this HEAD. Add a one-line note that the spec/research cited `20693bb8` (a same-intent sibling fix on another branch) but the verified HEAD-heal here is `acd5631f` (#158). Do NOT change the replay base (`1b0264f1` stays). | nfr1-proxy |
| F-2 | MINOR | `test_backtest_e5.py` assertion 1 | `assert "<BASE>..HEAD" in text` is non-discriminating: the POST-fix SKILL.md ALSO contains `<BASE>..HEAD` (inside the "NOT `<BASE>..HEAD`" prohibition), so this substring is present pre- AND post-fix. Only assertion 2 (prohibition absent pre-fix) is currently load-bearing. | Strengthen assertion 1 to the discriminating form `assert "--diff <BASE>..HEAD" in text` (the pre-fix reflect ACTION uses `--diff <BASE>..HEAD`; the post-fix action uses `--diff <BASE>` single-ref, so `--diff <BASE>..HEAD` appears ONLY pre-fix). Keep assertion 2. | actionability / negative-witness |
| F-3 | MINOR | `test_catch_rate_schema.py` (or aggregation test) | The `proxy_limitation` empty/whitespace `__post_init__` guard (catch_rate.py) has no NEGATIVE test. | Add a test asserting `CatchRateReport(... proxy_limitation="")` (or whitespace) raises `ValueError`. | nfr1-proxy |
| F-4 | MINOR (clarify; verified non-issue) | `final-harness-inventory.md` headline | Lens summed only the modules+tests table rows (2795) and flagged the "2869" headline as wrong. VERIFIED: 2869 = 2795 (modules+tests) + 74 (the 5 inline-listed fixtures). `find ... -exec cat {} + | wc -l` = 2869. The headline is CORRECT. | Clarify the inventory headline to "2869 (modules+tests 2795 + 5 fixtures 74)" to remove the ambiguity. Executor-handled doc edit (not harness code). | consistency |
| F-5 | MINOR | `git_replay.py` (ReplayEscape.wave doc "H0..H5") vs `catch_rate.py` (EscapeResult.wave doc "H1..H4") | Doc wording mismatch on the wave range. | Harmonize: note H0-H5 is the full wave taxonomy and H1-H4 are the waves the E1-E5 escapes map to. Tiny comment/docstring tweak. | template |
| D-x | MINOR (doc) | inventory symbol lists | `ReplayEscape` + `PrefixReplayError` omitted from the inventory's symbol columns. | Executor-handled: add them to the inventory. | template |

## Fix routing

- Harness code fixes (F-1, F-2, F-3, F-5): ONE serialized rf-qa fix agent (I20), touching ONLY `tests/troubleshoot/backtest/`, must keep the suite green-or-correctly-skips + ruff clean.
- Doc-only inventory edits (F-4, D-x): executor-handled directly on `phase-outputs/reviews/final-harness-inventory.md` (not harness code).
- The consistency FAIL (F-4) is a verified false positive (the harness is correct); it does not block.
