# QA Source-Fidelity Report 2 — backtest_status contracts + NFR-1

**Topic:** Harness fidelity to RELEASE-SPEC §4.5 / §5.4 / §5.5 / NFR-1 (backtest_status)
**Date:** 2026-06-12
**Phase:** source-fidelity (report-only, fix_authorization: false — NO files modified)
**Assigned range:** RELEASE-SPEC §4.5 (line 316), §5.4 (lines 413-423), §5.5 (lines 425-439), NFR-1 (line 523)

**Spec:** `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-RELEASE-SPEC.md`
**Harness root:** `.../tests/troubleshoot/backtest/`

---

## Overall Verdict: PASS

No fidelity gap found across semantic coverage, detail preservation, or phantom-coverage detection.
The anti-vacuity tightening is a faithful stricter-but-compatible realization of §5.4, not a
contradicting deviation.

---

## Dimension 1 — SEMANTIC COVERAGE (PASS)

| # | Spec contract (file:line) | Harness analogue (file:line) | Result |
|---|---------------------------|------------------------------|--------|
| 1 | §5.4 derivation `not_run`/`partial`/`complete` (spec:417-421) | `_derive_backtest_status` empty→not_run / all-fully-caught→complete / else→partial (catch_rate.py:121-132) | FAITHFUL |
| 2 | Signoff stays advisory until complete (§4.5 invariant spec:316; §5.4 spec:419-421) | `production_signoff` returns "advisory" unless complete; only complete mirrors run-level verdict (catch_rate.py:209-219) | FAITHFUL |
| 3 | `partial` lists missing escape IDs (§5.4 spec:420) | `missing_escape_ids` (catch_rate.py:205-207) + markdown "**Partial** — escape ids missing…" (catch_rate_report.py:121-126) | FAITHFUL |
| 4 | Governing test `test_backtest_status_keeps_pipeline_health_advisory_until_complete` (spec named; cited in test docstring line 7) | `test_backtest_status_keeps_signoff_advisory_until_complete` asserts the REAL `production_signoff`, not a mock (test_backtest_status_separation.py:27-38), with partial (:41-53) + complete-mirror (:56-70) analogues | FAITHFUL ANALOGUE |
| 5 | §5.5 output-contract fields all present (spec:427-439) | `_CATCH_RATE_FIELDS` (catch_rate.py:59-70) + schema `required[10]` (schema:7-18) — contract_version, backtest_status, total_escapes, caught, missed, catch_rate, escapes, proxy_limitation all present | FAITHFUL |
| 6 | `backtest_status` enum + default not_run (§5.5 spec:433) | schema `$defs.backtestStatus` enum {not_run,partial,complete} (schema:71-79); STATUS_NOT_RUN default + empty→not_run (catch_rate.py:41-48,128-129) | FAITHFUL |

Test-level non-vacuity: every test asserts the actual derivation against real model methods —
`test_backtest_status_separation.py` (real `production_signoff`),
`test_catch_rate_aggregation.py:111-156` (derived status, EXACT-equality), and the hermetic
complete/partial arms (test_catch_rate_aggregation.py:159-276) that exercise the today-dead branches
on synthetic data. The spec-named test maps to a same-semantics harness test (name varies by a word;
the spec name is preserved verbatim in the docstring at line 7 — traceability intact).

## Dimension 2 — DETAIL PRESERVATION (PASS)

| Detail (spec:line) | Survives into harness (file:line) | Result |
|--------------------|-----------------------------------|--------|
| Enum default `not_run` (§4.5 spec:316; §5.5 spec:433) | STATUS_NOT_RUN + BACKTEST_STATUS_VALUES ordering (catch_rate.py:41-48); schema enum (schema:71-79); empty-escapes→not_run (catch_rate.py:128-129) | PRESERVED |
| Separation invariant (§5.4 spec:413-423) | `production_signoff` one-directional gating; test asserts a `blocked` run-level verdict is ALSO mirrored (gating-only, not a downgrade) (test_backtest_status_separation.py:69-70) | PRESERVED |
| Missing-escape-IDs on `partial` (§5.4 spec:420) | `_missing_escape_ids`/`missing_escape_ids` + aggregation asserts the exact missing set (catch_rate.py:135-137,205-207; test_catch_rate_aggregation.py:145-156) | PRESERVED |
| NFR-1 catch-rate-drives-signoff (spec:523) | catch_rate computed in `build_catch_rate_report` (catch_rate.py:246-261) → drives backtest_status → drives `production_signoff`. `proxy_limitation` honestly records NEW=CATCH is a documentation-presence proxy (catch_rate.py:160-168), faithful to NFR-1's "predicted until then" qualifier (spec:523) and Risk row "predicted coverage never validated post-G1" (spec:538) | PRESERVED |

NFR-1 "100% would-have-caught (post-build, predicted until then)" (spec:523): the harness does NOT
overclaim. `proxy_limitation` is a REQUIRED serialized + honesty-guarded field (schema minLength 1,
schema:64-68; whitespace-only raises, catch_rate.py:160-168, negative test
test_catch_rate_schema.py:268-286), so the artifact can never silently ship a "100% caught" claim
without the proxy caveat. This is a faithful encoding of the spec's "predicted until then" hedge.

## Dimension 3 — PHANTOM-COVERAGE DETECTION (PASS)

- No test merely names `backtest_status` without asserting its §5.4 derivation/separation. Every
  reference is load-bearing: separation tests hit `production_signoff`; aggregation tests assert the
  derived status with EXACT-equality (`==`, not substring); schema tests pin the enum tuple AND
  round-trip the REAL producer output through the validator (test_catch_rate_schema.py:73-95).
- **Anti-vacuity tightening is stricter-but-compatible, NOT a contradicting deviation.** §5.4 line 421
  defines `complete` as "E1-E5 replay scenarios all pass against the built gates." The harness requires,
  per escape, CATCH AND a truthy `negative_witness` AND a non-null `card_path` (catch_rate.py:109-115).
  Fidelity analysis:
  - A genuinely-passing scenario under §5.4's intent already carries all three: the negative witness is
    intrinsic to every H-wave differential proof (§5.3 `negative_witness: bool`, spec:380) and a proof
    surface (`card_path`) is mandated by §5.5 (spec:435-438). So the tightening reclassifies **no**
    genuinely-complete corpus as `partial` (no false-partial risk).
  - The tightening only rejects a VACUOUS `complete` (a bare CATCH count with no witness/proof). That is
    exactly the anti-inflation intent already present in the spec's sibling invariant
    `known_escapes_caught` "Membership requires a cited passing wave/card with status=PASS
    (anti-inflation)" (§4.5 spec:314). The tightening is the same anti-inflation principle applied to
    `complete`.
  - The code, schema, and docstrings explicitly cite §5.4 / research/07 as the basis
    (catch_rate.py:9-17,121-127; schema:5) — provenance is annotated, not silent.
  - The model is honestly scoped as a PRODUCER-ASSERTED bookkeeping contract (not an executed gate),
    with `card_path` enforced as NON-NULLNESS only and real on-disk existence delegated to the pure
    `unresolved_card_paths` helper (catch_rate.py:19-27,264-286). This does not overclaim executed
    coverage — consistent with NFR-1's "predicted until then."
- Negative-path coverage proves the tightening is real, not decorative: all-CATCH-missing-witness→partial
  (test_catch_rate_schema.py:201-214), all-CATCH-null-card→partial (:217-231), complete-claim+null-card
  RAISES (:234-252).

## Confidence

**Confidence:** Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 7 | Grep: 0 | Glob: 0 | Bash: 0

All 16 checkpoints (6 semantic + 4 detail + 6 phantom/anti-vacuity sub-checks) verified by direct Read
of the spec lines and the harness source. No web lookup required (claims are all local source-truth).

## Issues Found

None. Zero fidelity gaps.

## QA Complete
