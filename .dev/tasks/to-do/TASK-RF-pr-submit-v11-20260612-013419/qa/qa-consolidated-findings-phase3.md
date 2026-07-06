# Phase 3 — Consolidated QA Findings (M3 lens gate)

8 lens agents ran (3 structural + 3 content + 2 domain), all report-only. Reports:
qa-structural-conformance-report.md (PASS), qa-structural-consistency-report.md (FAIL),
qa-structural-evidence-report.md (PASS w/ minor), qa-content-actionability-report.md (FAIL),
qa-content-domain-accuracy-report.md (FAIL), qa-content-crossref-report.md (FAIL),
qa-domain-core-purity-report.md (PASS), qa-domain-closed-enum-report.md (PASS).

## TOP-LINE VERDICT: FAIL → fixes required (see ACTIONABLE below)

## Deduplicated findings + disposition

| # | Finding (lenses) | Severity | Disposition |
|---|---|---|---|
| F1 | **decline_retrigger_regex misses backtick-wrapped trigger.** Real Augment declines render `` Comment `augment review` `` with markdown backticks; char class `["']?` excludes backtick, so the most common real decline shape is MISSED (domain-accuracy, verified vs real PRs). | **CRITICAL** | **FIX** — widen char class to `["'`+"`"+`]?` in detection.py (2 sites) + ref YAML; add backtick fixture+test. In-scope (FR-9.1 real-world fidelity). Documented as Necessary Deviation from spec §6.2 literal default. |
| F2 | **Decline-first ordering is unguarded by any test.** Mutation test proved moving the decline check AFTER findings leaves all tests green; no fixture has BOTH a findings-review and a decline-comment (actionability). | **CRITICAL** | **FIX** — add `test_t1110c_decline_wins_over_cooccurring_findings` asserting a findings-bearing Augment review + decline comment → "declined". |
| F3 | **`poll_augment_review` docstring still says 3-state** ("polling/clean/findings") but now can return "declined" via `classify` delegation (evidence + domain). | MINOR | **FIX** — update detection.py docstring to 4-state. |
| F4 | **EC-23 watermark test filed as `ec23`, matrix maps it to T-1118** — unresolvable by T-ID token (crossref). | MINOR | **FIX** — add `T-1118` traceability token to the watermark test docstring. |
| F5 | **Fixtures/AUGMENT use `augment-code[bot]` (hyphen); real login is `augmentcode[bot]`** (internal-consistency HIGH, domain CRITICAL-1). | HIGH (test-fidelity) | **DEFER (no-fix, documented)** — Step 3.6 EXPLICITLY instructed "use the fixture bot login `augment-code[bot]` to match existing fixtures". The shipped V1.0 fixtures (review-clean.json etc.) + the global `AUGMENT` constant all use the hyphenated form; the synthetic `contract` fixture sets `augment_bot_login=AUGMENT`, so tests are self-consistent and exercise the classifier LOGIC correctly. classify() keys on `contract.augment_bot_login` (no runtime literal), and the operator's REAL locked override already uses `augmentcode[bot]` — so there is NO runtime bug. Normalizing the synthetic test login is a pre-existing V1.0 test-fidelity concern orthogonal to V1.1; logged as a Follow-Up Item. The pre-existing intra-file `augment-code[bot]` (L28) vs `augmentcode[bot]` (L107/119) contradiction is V1.0, not introduced here. |
| F6 | **17 of 21 §9-matrix T-IDs have no test** (T-1101-1106, T-1113-1118, T-1120-1125, T-PUSH-WITHOUT-REREVIEW-NO-TICK, T-AUGGIE-AT-MOST-ONCE) (crossref). | (scope artifact) | **DEFER — out of Phase-3 scope.** Those T-IDs belong to Phases 4 (run_log) and 5 (fsm/retrigger/fallback), not yet built. The crossref agent compared the WHOLE-feature §9 matrix against only the Phase-3-landed slice. They will be satisfied by Steps 4.4/4.5/5.8/5.9. Not a Phase 3 defect. |
| F7 | phrase regex narrow (misses "too large"/"exceeds size limit"); benign both-phrase clean review → false declined (domain IMPORTANT) | LOW | **NO-FIX (documented)** — spec §6.2 specifies `abnormally\s+large` literally; the App's real decline uses exactly that phrasing (memory). Both-AND already minimizes false positives; a clean review containing both markers is implausible. Keeping spec-literal phrase. |
| F8 | t1110 `expected.state` self-assert is tautological (actionability MINOR) | LOW | **NO-FIX** — harmless fixture sanity check; the real assertion `classify(...) == "declined"` immediately follows. |

## ACTIONABLE FIXES (applied serially by the executor as the single I20 writer, Step 3.G6)
- F1: backtick in retrigger regex (detection.py field default + from_yaml default + detection-contract.md YAML) + `decline-backtick.json` fixture + a backtick test.
- F2: co-occurrence decline-wins test.
- F3: poll_augment_review docstring → 4-state.
- F4: T-1118 token in watermark test.
