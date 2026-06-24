# QA Verification — Phase 4 Fix Content (report-only, fix_authorization: false)

**Verdict: PASS**

**Phase:** doc-qualitative (fix-verification of Phase 4 aggregation fixes)
**Date:** 2026-06-12
**Scope:** Confirm P4-1 (hermetic complete/partial test) and P4-2 (exact-tmp_path guard) fixes are genuine; confirm the fix did NOT weaken §8.3 mapping / E4 pin / skip-guard / not_run behavior; confirm no new vacuity in Phase 4.
**Files modified by this agent:** NONE.

---

## Top-line: PASS

Both IMPORTANT fixes are genuine and semantically load-bearing. The §8.3 per-escape mapping, the E4 `1b0264f1` pin, the skip-guard discipline, and the `not_run`-today behavior are all intact. No new vacuity introduced.

---

## VERIFY-1 — Hermetic test exercises the today-dead complete + partial arms (PASS)

**Today-dead premise confirmed.** All 6 hardening refs are ABSENT under
`src/superclaude/skills/sc-troubleshoot-protocol/refs/` (verified by directory listing — only
calibrator-eval-cases.md, diagnosability-audit.md, doc-discovery.md, escalation-rubric.md,
hypothesis-card-template.md, remediation-handoff.md, report-template.md, triage-checklist.md
present). So `_collect_escape_results()` (test_catch_rate_aggregation.py:61-65) hits
`if not any(present.values()): return []` and only the `not_run` arm runs live. The
complete/partial else-branch of `test_backtest_catch_rate_report_drives_status` (lines 134-156) is
genuinely dead today — P4-1's premise holds.

**Complete arm is non-tautological — requires all-3 conjuncts.** The new test
`test_backtest_aggregation_complete_and_partial_derivations` (lines 159-276) runs UNCONDITIONALLY
(no `@requires_impl_ref`, no `skipif`, no skip inside) — confirmed PASSED (not skipped) at
line-level pytest output. The complete arm (lines 167-216) builds 5 synthetic CATCH escapes each
with `negative_witness=True` AND a real `card_path` written under `tmp_path`, then asserts
`backtest_status == "complete"`, `caught == 5`, `missed == 0`, `catch_rate == 1.0`,
`missing_escape_ids() == ()`.

This is NOT a tautology because the assertion is checked against the model's real derivation:
`_derive_backtest_status` (catch_rate.py:119-130) returns `complete` ONLY when
`all(e.is_fully_caught() for e in escapes)`, and `is_fully_caught` (catch_rate.py:107-113) requires
the conjunction `verdict == CATCH AND bool(negative_witness) AND card_path is not None`. The
`__post_init__` invariant (catch_rate.py:189-201) independently re-derives and raises `ValueError`
on any escape claimed toward `complete` with a null card_path or a broken conjunct. The synthetic
escapes satisfy all three, so `complete` is the genuine derived outcome — a single dropped conjunct
would flip it to `partial` and fail the test.

**Unresolved-card wiring (real existence gate) is exercised genuinely** (lines 201-237):
- correct `base_dir=tmp_path` → `unresolved_card_paths() == ()` (cards exist);
- `base_dir=other_dir` → every card surfaces as unresolved (lines 205-207);
- a fabricated never-created card surfaces as unresolved even with correct base_dir (lines 219-237).
This drives the real on-disk check in `unresolved_card_paths` (catch_rate.py:262-284), which is the
filesystem gate the frozen model deliberately does not perform — not asserted anywhere else.

**Partial arm surfaces the RIGHT missing id** (lines 239-276): one MISS with `card_path=None` (E1)
+ four CATCH → `backtest_status == "partial"`, `caught == 4`, `missed == 1`, and the precise-set
assertion `set(partial_report.missing_escape_ids()) == {"E1"}` (line 276). This is exact-set
equality, not a weak membership check — it proves the missing-id derivation
(`_missing_escape_ids`, catch_rate.py:133-135) surfaces exactly the right escape, not a superset.

**md headline coverage** (line 216): `assert "5/5" in md_text` exercises
`render_catch_rate_markdown` (catch_rate_report.py:107-110), covering the P4-3 MINOR
(caught/total in the md) inside the hermetic test as the consolidation routed it.

## VERIFY-2 — Exact-tmp_path guard is a real protection, not vacuous (PASS)

The P4-2 fix replaced the vacuous `"docs" not in str(written[...].parent)` substring check with
`assert written["catch-rate.json"].parent == tmp_path` (lines 124-126). This is a genuine
protection: `write_catch_rate_report` (catch_rate_report.py:156-162) builds `out = Path(output_dir)`
and writes `out / "catch-rate.json"`, so the written parent is exactly `output_dir`. Asserting
equality against pytest's `tmp_path` fixture proves the artifact is tmp_path-rooted (never under
`docs/`, which the autouse `_pollution_snapshot` guard fails on). Unlike the old substring check —
which any `/tmp/...` path trivially satisfied — exact-equality would FAIL if the writer ever rooted
the artifact anywhere other than the passed dir. Non-vacuous.

## VERIFY-3 — §8.3 mapping / E4 pin / skip-guard / not_run all intact (PASS)

**§8.3 per-escape mapping UNCHANGED.** The escape→wave mapping lives in `REPLAY_ESCAPES`
(git_replay.py:48-56): E1→H1, E2→H3, E3→H3, E4→H2, E5→H4. The runners assert these waves verbatim
(e1:wave="H1", e2:"H3", e3:"H3", e4:"H2", e5:"H4") and the aggregation's collected records inherit
`wave=e.wave` (test_catch_rate_aggregation.py:73, 86). The fix touched neither `REPLAY_ESCAPES` nor
any runner's wave/ref/SHA. The `_ESCAPE_REFS` proof-surface map
(test_catch_rate_aggregation.py:39-45) is unchanged. P4-5 (the §8.3-vs-§3.1 wave note) was advisory
and correctly not applied.

**E4 `1b0264f1` pin INTACT.** `REPLAY_ESCAPES` pins E4 to `prefix_parent_sha="1b0264f1"`
(git_replay.py:52-54, with the `fix UNMERGED; replay against parent` note). test_backtest_e4.py:34-45
consumes that bare parent and documents the HEAD-drift rationale (bug healed on HEAD via 20693bb8;
spec fix b97c9960 unmerged → pin to pre-fix parent). Verified `1b0264f1` exists in local history
(`git cat-file -e 1b0264f1^{commit}` → 0; `fix(pipeline): robust large-prompt stdin delivery ... (#156)`).
The fix did not touch the E4 runner or the pin.

**Skip-guard discipline INTACT.** `requires_impl_ref` (=_impl_guard.py:43-57) remains a
file-existence `skipif` (never importorskip / xfail). The OLD=MISS halves run unconditionally; the
NEW=CATCH halves skip until refs land. The aggregation's own ref-gated parametrized test
(test_backtest_escape_collected_into_catch_rate) still skips at not_run — confirmed 5×SKIPPED in
verbose output. The fix added an UNGUARDED hermetic test that uses purely synthetic escapes (no
impl-ref dependency), so it neither weakens nor bypasses the skip-guard — it tests the model
directly, which is the correct separation.

**not_run-today behavior PRESERVED.** The original
`test_backtest_catch_rate_report_drives_status` (lines 111-156) still asserts the not_run arm:
`if not results: payload["backtest_status"] == "not_run"; total_escapes == 0; caught == 0`
(lines 129-133). Confirmed PASSED today (the live `_collect_escape_results()` returns `[]`). The
fix did NOT alter this test's not_run assertions — it only swapped the vacuous docs-guard for the
exact-tmp_path guard (lines 124-126) and left the not_run/else logic intact.

## VERIFY-4 — No new vacuity introduced anywhere in Phase 4 (PASS)

- New hermetic assertions are all substantive: exact-equality on counts/rate, exact-set equality on
  missing ids (`== {"E1"}`, line 276), real filesystem existence checks via `unresolved_card_paths`
  with both a matching and a non-matching base_dir, and a substring check on the md headline that
  the writer actually emits (`"5/5"`).
- The exact-tmp_path guard (VERIFY-2) is the OPPOSITE of vacuous — it replaced the one vacuous check
  that existed.
- No new substring-only / always-true guards were added. The waiver test
  (test_waiver_regreen.py) is untouched and remains a correctly-shaped single skip-guarded NFR-4
  test, EXCLUDED from the E1-E5 catch_rate arithmetic (total_escapes==5 invariant intact).
- Full backtest suite: 32 passed, 11 skipped, 0 failed; ruff clean on the modified file.

---

## Self-Audit

**(a) Reliance list — structural items relied on (verified independently below):**
- Relied on prior structural PASS for §8.3 mapping presence / ruff / collection counts.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Dead-arm premise: independently listed `refs/` dir and probed all 6 hardening refs ABSENT
  (Bash) → confirmed the live path yields `[]` / not_run, proving P4-1's dead-arm claim.
- Complete-arm non-tautology: read `is_fully_caught` + `_derive_backtest_status` + `__post_init__`
  (catch_rate.py:107-201) and traced that the synthetic escapes earn `complete` only via the real
  3-conjunct derivation, not a hardcoded literal.
- tmp_path guard reality: read `write_catch_rate_report` (catch_rate_report.py:156-162) and confirmed
  the written parent == passed dir, so the exact-equality guard is enforceable, not vacuous.
- E4 pin: `git cat-file -e 1b0264f1^{commit}` (Bash) → exists; matched the runner's documented pin.
- Behavior preservation: ran the suite at line-level verbosity — confirmed the original
  not_run-driver test PASSES and the new hermetic test PASSES unconditionally (not skipped).

**Confidence:** Verified: 4/4 verify-axes | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 9 | Grep: 0 | Glob: 0 | Bash: 4 (refs-presence, suite run, pin+suite, verbose+ruff)
**Web research:** none performed (all checks local-file / git-bound).

## QA Complete
