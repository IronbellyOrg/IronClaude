# Phase 6 (P5) — Consolidated QA Findings (Cycle 1)

**Generated:** 2026-06-19 (Step 6.G8). Six lens reports consolidated (this phase the lens agents wrote
to de-collided `qa/qa-p6-*.md` paths, so no clobbering).

## Per-lens verdicts

| Lens | Agent | Verdict | Issues |
|------|-------|---------|--------|
| table-conformance vs spec.md:344-350 | rf-qa | PASS | 0 (table byte-identical to spec) |
| internal-consistency / mirror-sync | rf-qa | PASS | 6 MINOR (mirror abbreviations, non-contradictory) |
| evidence-quality / test-coverage | rf-qa | PASS | 2 IMPORTANT + 3 MINOR (test under-coverage) |
| non-mutation / advisory-only soundness | rf-qa-qualitative | PASS | 0 (provably read-only) |
| determinism / first-run robustness | rf-qa-qualitative | **FAIL** | 1 CRITICAL, 3 IMPORTANT, 1 MINOR |
| domain-accuracy vs spec + recorded decision | rf-qa-qualitative | PASS | 0 (4 MINOR non-defect observations) |

## CONSOLIDATED VERDICT: **FAIL**

The §5.3 pure-function fence (scored tiers roadmap-pure) and the non-mutation/advisory-only property are
SOUND (non-mutation lens PASS 11/11; table byte-identical to spec). The FAIL is in the *rendered advisory's*
determinism: the match logic references feedback-log fields that do not exist in the generator's actual
Feedback Collection Template schema, plus undefined tie-break/count/malformed-file semantics, plus 2 untested
determinism invariants.

## Deduplicated issue list

| ID | Severity | Lens | Location | Issue | Required fix |
|----|----------|------|----------|-------|--------------|
| C6-01 | CRITICAL | determinism I-2 | SKILL.md advisory match logic (~:873) | The advisory matches feedback rows on `roadmap_item_id` / `task_signature` / `suggested_tier`, but the actual Feedback Collection Template schema (~:851-862) has columns `Task ID | Original Tier | Override Tier | Override Reason | Completion Status | Quality Signal | Time Variance` — those three names do not exist there. "Matching overrides" is uncomputable → the ≥2 threshold (section present vs omitted) is non-deterministic. | Reconcile the advisory match logic to the EXISTING feedback-log columns: match a feedback row to a scored task when its `Task ID` equals the task's `T<PP>.<TT>`; a "matching override" = a matched row whose `Override Tier` is non-blank AND differs from the task's deterministically-scored tier; the advisory `Feedback-suggested tier` column ← the row's `Override Tier`. (Map the spec's abstract `roadmap_item_id\|task_signature`→`Task ID`, `suggested_tier`→`Override Tier`.) |
| C6-02 | IMPORTANT | determinism I-3 | SKILL.md advisory ordering (~:875) | Ascending `T<PP>.<TT>` is non-unique when a task has ≥2 matching feedback rows (different Override Tiers) → row order undefined, contradicting the "byte-identical" claim. | Define a deterministic emission: one advisory row per `(Task ID, Override Tier)` pair, ordered by Task ID ascending then Override Tier ascending (so the section is byte-deterministic). |
| C6-03 | IMPORTANT | determinism I-4 | SKILL.md advisory `Observed count` (~:880-882) | `Observed count` `<n>` has no defined counting semantics (the feedback-log has no count column). | Define `Observed count` = the number of feedback-log rows for that `(Task ID, Override Tier)` pair (counts repeated feedback across appended runs; 1 when a single row). |
| C6-04 | IMPORTANT | determinism I-1 | SKILL.md advisory read (~:870-871) | Best-effort read defined only for an ABSENT file; malformed/empty/partial feedback-log behavior undefined. | Add: rows missing any required field (`Task ID` / `Override Tier`) are ignored (cannot match); a malformed/empty/partial feedback-log simply yields fewer matches, and if <2 matching overrides the whole section is omitted (no error). |
| C6-05 | MINOR | determinism I-5 | SKILL.md advisory "emitted at Stage 4" (~:870) | Stage-attribution contradiction: the advisory is said to be "emitted at Stage 4 (Enrichment)" but Stage 4 is the scored-tier compute that the §5.3 fence forbids from reading feedback-log. | Clarify the advisory is RENDERED during index assembly — it reads the ALREADY-COMPUTED scored tiers + the feedback-log (read-only) AFTER the §5.3/§5.4 scored-tier compute; the fence holds because the scored-tier COMPUTE never reads feedback, only the advisory RENDER does (and it only reads, never writes, the scored tiers). |
| C6-06 | IMPORTANT | evidence-quality #1 | test (R-9 clause b) | R-9 clause (b) "same roadmap + same feedback-log → byte-identical advisory section" is documented but untested. | Add an assert that the source states the same-inputs→byte-identical-section determinism (the `same inputs → byte-identical section` clause). |
| C6-07 | IMPORTANT | evidence-quality #2 | test (first-run robustness) | First-run robustness (absent feedback-log → omit, no error) is untested. | Add an assert for the first-run omission clause (best-effort, absent → omitted, no error). |
| C6-08 | MINOR | evidence-quality #3 | test (R-14 mirror) | No P5 test reads `index_template_text` — mirror drift would pass. | Add an assert that the index-template mirror carries the `## Tier Calibration Advisory` placeholder (uses the existing `index_template_text` fixture). |

## Fix scope for Step 6.G9

- SKILL.md C6-01..C6-05: reconcile the advisory to the EXISTING feedback-log schema (match on `Task ID`,
  suggested tier ← `Override Tier`); define per-(Task ID, Override Tier) row + deterministic ordering;
  define `Observed count`; define malformed/empty/partial handling; clarify the render-at-index-assembly
  timing vs the §5.3 compute fence. All within P5 scope; the spec table columns + non-mutation property
  stay intact (table-conformance + non-mutation lenses PASSed — do NOT regress them). Mirror the reconciled
  match/count/ordering semantics into the index-template placeholder too (keep it abbreviated but consistent).
- Test hardening C6-06..C6-08 in `tests/tasklist/test_tasklist_cli.py` `TestP5TierCalibrationAdvisory`.
- After fixes: `make sync-dev` + `make verify-sync` + `uv run pytest tests/tasklist/ -v`.
- IMPORTANT: re-read post-fix SKILL.md; keep the existing PASS asserts green (the spec table, non-mutation,
  §5.3 fence); make new asserts byte-match the source.
