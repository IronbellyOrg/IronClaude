# QA Input Manifest — Phase Gate A (Detection-Contract Gate)

**Generated:** 2026-06-11 11:24
**Step:** PGA.1 (L6 aggregation)
**Phase under review:** Phase 2 (Detection Contract Gate — the spec §3 build-DAG root)
**Contract-gate verdict:** PASS (6/6 tests; see `phase-outputs/plans/contract-verdict.md`)

## Phase 2 artifacts to verify

| # | Path | Lines | Description | Spec section |
|---|------|------:|-------------|--------------|
| 1 | `src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md` | 50 | DET ref: YAML-fronted probe-locked contract (`locked: false`) + 4 consequences + T-210 note | §7 (lines 473–500) |
| 2 | `src/superclaude/pr_submit/__init__.py` | 43 | Package docstring + top-level re-exports (classify, poll_augment_review, DetectionContract, models) | R04 §C |
| 3 | `src/superclaude/pr_submit/models.py` | 202 | `EventType` (33 members), `Severity` (5), `MonitorState` (19), `Finding`, `SkillResult`, `PushDecision` | §11.3 + §12.1 |
| 4 | `src/superclaude/pr_submit/detection.py` | 140 | `DetectionContract` loader (T-210 lock gate), `poll_augment_review` poll seam | §7, FR-2.1/2.2 |
| 5 | `src/superclaude/pr_submit/classifier.py` | 86 | Pure `classify(payload, contract)` three-state classifier keyed on `augment_bot_login` | §7, FR-2.2 |
| 6 | `tests/pr_submit/test_detection_contract.py` | 124 | T-201/202/203/210/211/212 (inline payloads; Phase 10 swaps for fixtures) | §6.3 |
| 7 | `phase-outputs/test-results/contract-gate-summary.md` | 32 | Structured test summary (6 passed) | — |
| 8 | `phase-outputs/plans/contract-verdict.md` | 10 | PASS verdict; DAG root established | §3 step 0 |

## Acceptance criteria the QA lenses verify (the Phase 2 "ensuring…" clauses)

- **detection-contract.md:** schema matches spec §7 EXACTLY (9 fields: `augment_bot_login`, `augment_author_association`, `augment_app_slug`, `emission_shape`, `findings_locus`, `severity_field_path`, `review_completeness_signal`, `probe_evidence`, `locked`); `locked` is `false`; NO hard-guessed bot login (`augment_bot_login` stays `<PROBE-LOCKED>`); notes T-210 enforces the lock gate.
- **models.py:** `EventType` has EXACTLY 33 members (32 from §11.3 + `push_aborted_or_not_landed` from §12.1); imports NO `anthropic`; zero `gh`/`git` tokens.
- **classifier.py / detection.py:** ZERO `gh`/`git` command tokens (NFR-6); classifier never embeds a literal bot-login; the `locked:false` HALT path present (T-210).
- **test_detection_contract.py:** T-210 asserts HALT when `locked:false`/absent; each test maps to its spec ID in a docstring; no fabricated Augment payload shapes beyond the documented three-state contract.
- **Evidence quality:** `contract-gate-summary.md` reflects the actual raw pytest output; the verdict matches; no hallucinated passing counts.
