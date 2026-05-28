<!-- Variant 3: haiku:qa — defense-in-depth; regression tests + pin tests + eval-suite hardening -->

# Variant 3 — Eval-Suite-First Refactor (haiku:qa)

## Stance

The rubric and calibrator changes are necessary but not sufficient: M4 (eval-suite silent-green coverage) is the *prevention* mechanism for all three diagnostic mechanisms (per Cross-mechanism implications ¶4 of FINAL-MERGED-CAUSES.md — "without pin tests, any fix to M1/M2/M3 will be silently regressed"). The smallest *durable* refactor pairs minimal rubric/calibrator changes with a pin-test-first eval-suite that locks the new behavior in place. Without that, the refactor regresses on the next eval-corpus expansion.

The recursion-of-anti-pattern observation (Cross-mechanism implications ¶5) is the load-bearing rationale: the calibration apparatus failed pr86 the same way pr86's `test_t1` failed F1 — green-bar on irrelevant invariant. Don't ship the rubric fix without simultaneously fixing the apparatus that validated the broken rubric.

## Proposal

### Change 1 — `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` (minimum viable)

Identical to Variant 1's surgical patch (adopt by reference): add `Runtime check` 6th dimension, replace flat mean with `min(mean, evidence_grounding + 0.30, runtime_check + 0.30 if runtime_behavior)`, add verdict-direction modifier table, add escalation rule for `claim_class=runtime_behavior AND runtime_check<0.5`.

Rationale for adopting Variant 1's shape (not Variant 2's two-stage rewrite): the v2.0 schema overhaul is correct as an end-state but it doubles the migration cost (every in-flight card invalidates) without doubling the safety. The QA-first path is "smallest rubric change that holds + comprehensive pin tests that prevent regression". Schema v2.0 can ship in a follow-up commit.

### Change 2 — `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` (minimum viable)

Identical to Variant 1: add `Claim class` frontmatter field, `Runtime check` self-assessment row, `Falsification standard` section.

### Change 3 — `src/superclaude/agents/confidence-calibrator.md` (minimum viable)

Identical to Variant 1: add Runtime check scoring instruction, gated-min formula application, verdict-direction cap, claim-class handling subsection.

### Change 4 — `src/superclaude/skills/confidence-check/SKILL.md` (cultural-prior correction)

**Section affected**: lines 14-18, the "Test Results (2025-10-21): Precision 1.000, Recall 1.000, 8/8 test cases passed" claim.

**Shape**: Replace the unqualified claim with a scoped one. The 8/8 test cases passed for the *pre-implementation duplicate/architecture/docs/OSS/root-cause* checks, NOT for runtime-behavior calibration. The unqualified claim is doing rhetorical work the eval corpus cannot support (per M2 §Evidence on cultural priors).

**Diff sketch**:

```diff
 # Confidence Check Skill

 ## Purpose

 Prevents wrong-direction execution by assessing confidence **BEFORE** starting implementation.

 **Requirement**: ≥90% confidence to proceed with implementation.

-**Test Results** (2025-10-21):
-
-- Precision: 1.000 (no false positives)
-- Recall: 1.000 (no false negatives)
-- 8/8 test cases passed
+**Test Results** (2025-10-21, scope: pre-implementation duplicate/architecture/docs/OSS/root-cause checks):
+
+- Precision: 1.000 / Recall: 1.000 on 8 fixtures covering the five pre-implementation checks
+
+**Out of scope for these test results**:
+- Runtime-behavior calibration (see `sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` for that eval corpus)
+- Sha-pinned PR-diff citations (see same)
+- Structurally-unverifiable predicates of any kind
+
+The 5-check confidence assessment ratchets are not a general epistemology for code claims — they are a pre-implementation gate. Treat the runtime-vs-static evidence dimension as the calibrator's responsibility, not this skill's.
```

This change is **defense-in-depth for M2** (cultural-prior correction) and **defense-in-depth for M4** (kills the silent-green rhetorical claim). Not strictly required for M1+M2+M3a closure via Changes 1-3, but cheap and the right anti-recursion move.

### Change 5 — NEW FILE: `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md`

**Shape**: Create. This is the M4 pin-test deliverable: a fixture corpus + property tests that any future change to the rubric or calibrator must pass.

**Sketch**:

```markdown
# Calibrator Eval Cases

Golden hypothesis cards + expected calibrated scores. Run before any change to escalation-rubric.md or confidence-calibrator.md ships.

## Fixtures (hypothesis cards with expected calibrated scores)

### Fixture 1: source-only runtime REFUTE (the H3 0.95 case)

**Card**: claim_class=runtime_behavior, verdict=REFUTE, source_citation=1.0, runtime_check=0.0, four other dims=1.0
**Expected calibrated**: ≤ 0.70 (M3a cap fires; without the cap, gated_min would be min(0.83, 1.30, 0.30) = 0.30, which already passes — but the cap protects against the case where runtime_check=0.5)
**Asserts**: M1 + M2 + M3a all closed.

### Fixture 2: pr86-style AFFIRM with structural truncation

**Card**: claim_class=runtime_behavior, verdict=AFFIRM, source_citation=1.0, runtime_check=0.5 (runnable command in card, no captured output), four other dims=1.0
**Expected calibrated**: ≤ 0.80 (gated_min = min(0.92, 1.30, 0.80) = 0.80; AFFIRM cap of 0.84 is not binding here)
**Asserts**: M1 + M2 closed; below the 0.85 STOP gate.

### Fixture 3: clean static defect (the eval_run.py Path-import case)

**Card**: claim_class=static_defect, source_citation=1.0, runtime_check=1.0 (inherited from source_citation), four other dims=1.0
**Expected calibrated**: 1.0
**Asserts**: refactor does NOT over-correct; legitimate static defects still pass cleanly.

### Fixture 4: sha-pinned citation

**Card**: cites `commit-sha-5a65c62:file:line`. claim_class=static_defect, source_citation=0.5 (citation exists but cannot verify against current HEAD), runtime_check=0.5
**Expected calibrated**: ≤ 0.80 (gated_min = min(?, 0.80, 0.80) = 0.80)
**Asserts**: structurally-unverifiable predicates cannot score 0.85+.

### Fixture 5: malformed card (missing claim_class)

**Card**: v1.0 frontmatter (no claim_class field).
**Expected behavior**: calibrator defaults claim_class to `runtime_behavior` (fail-safe) and notes the absence in its report.
**Asserts**: migration backward-compat: no silent acceptance of v1.0 schema in calibration mode.

### Fixture 6: well-written REFUTE on a runtime claim with strong runtime_check

**Card**: verdict=REFUTE, claim_class=runtime_behavior, runtime_check=1.0 (captured stdout from executed reproducer that contradicts the claim), source_citation=1.0, four other dims=1.0
**Expected calibrated**: 1.0
**Asserts**: M3a cap does NOT fire when runtime_check=1.0; legitimate runtime-verified REFUTEs are not over-penalized.

## Property tests

| ID | Property | Assertion |
|----|----------|-----------|
| P1 | M1 gate | `source_citation ≤ 0.5` ⟹ `calibrated ≤ 0.80` for any input |
| P2 | M2 gate | `runtime_check ≤ 0.5 AND claim_class != static_defect` ⟹ `calibrated ≤ 0.80` for any input |
| P3 | M3a cap | `verdict=REFUTE AND claim_class=runtime_behavior AND runtime_check<1.0` ⟹ `calibrated ≤ 0.70` |
| P4 | Determinism | running calibrator on same card produces same score (±0.0) across N=5 runs |
| P5 | Anchoring | varying the card's `Self-reported confidence:` field from 0.3 to 0.99 must not change calibrated by more than ±0.05 (Δcalibrated < anchoring-budget) |

## Suite integrity

Run on every PR touching:
- `escalation-rubric.md`
- `confidence-calibrator.md`
- `hypothesis-card-template.md`
- `confidence-check/SKILL.md`

A regression in any fixture or property test blocks merge.
```

### Change 6 — Eval-suite invocation: add to PR-checks

**Shape**: Add an entry to `tests/troubleshoot/` (or wherever the protocol's tests live) that invokes the calibrator against the fixtures in Change 5 and asserts the expected calibrated scores. Concretely: a pytest module that for each fixture loads the card, dispatches the calibrator (or its inline-fallback), and asserts on the returned calibrated value.

(Out of scope for this markdown-only proposal to specify the pytest itself — the deliverable is the test plan. The brainstorm proposal will name the file path the implementation should land at.)

## Coverage matrix

| Cause | Change 1 (rubric) | Change 2 (card) | Change 3 (calibrator) | Change 4 (confidence-check SKILL) | Change 5 (eval cases) | Change 6 (pytest hookup) | Closes? |
|-------|-------------------|-----------------|------------------------|------------------------------------|------------------------|---------------------------|---------|
| M1 | gated-min formula | — | applies formula | — | P1 fixture+property | enforces P1 in CI | **closes + prevents regression** |
| M2 | 6th dim + tightened anchor | claim_class + Runtime check field + Falsification standard | scores runtime_check; claim_class handling | scopes "1.000 precision" claim to pre-impl | P2 fixture+property | enforces P2 in CI | **closes + prevents regression** |
| M3a | verdict-direction modifier | — | applies modifier | — | P3 fixture | enforces P3 in CI | **closes + prevents regression** |
| M3b | — | Falsification standard required | reads it via Runtime check evidence | — | (implicit in fixtures 1,2,4) | (implicit) | **partially closes** |
| M3c | — | — | — | — | P5 anchoring property test | enforces P5 in CI | **prevention only** (the test catches anchoring drift; no rubric mechanism added) |
| M4 | — | — | — | scopes the silent-green claim | **directly addresses** — this IS the M4 fix | enforces it | **closes** |

## Counter-arguments considered

- **Rejected: "Variant 2's schema v2.0 is the right end-state; just do it."** Agreed it's the right end-state. Rejected as the right *next step* because: (a) the migration cost (every in-flight pr86-style card invalidates) is high enough that the refactor would block on it; (b) Variant 1's surgical patch + Variant 3's pin tests achieve the same M1+M2+M3a closure at a fraction of the migration cost; (c) schema v2.0 ships in a follow-up commit, gated by all 6 pin tests passing on v1.5 (Variant 1's shape).
- **Rejected: "Pin tests are a follow-up; ship the rubric fix first."** This is exactly the M4 anti-pattern: ship the rubric fix without the pin tests, and the next rubric tweak silently regresses. Recursion-of-anti-pattern (Cross-mechanism implications ¶5) is the reason this rejection is load-bearing.
- **Rejected: "Add property test P5 (anchoring) as a hard assertion."** Soft assertion only (log warning, don't block CI). LLM-as-judge tests have run-to-run variance; a hard P5 will flake. Track the variance; tighten gradually.
- **Rejected: "Don't touch confidence-check/SKILL.md — it's out of scope."** It IS out of scope for M1+M2+M3a *closure*, but the unqualified "Precision 1.000 / Recall 1.000" claim is the rhetorical engine of the M2 cultural prior. Leaving it untouched while fixing the calibrator is half-measure; the diff is 5 lines.

## Minimal-change subset closing M1+M2+M3a

**Changes 1+2+3** (same as Variant 1 — the rubric + card + calibrator triple). M1+M2+M3a are closed mathematically by those three edits alone.

**Changes 4+5+6** are defense-in-depth: 4 closes M4 (and the recursion-of-anti-pattern), 5+6 are M4's pin-test enforcement so the closure doesn't silently regress.

Ship Changes 1+2+3+5+6 in one PR. Change 4 is a one-line annotation, ship in same PR or follow-up.

## Regression tests / eval-suite additions

**See Change 5** — that's the entire substance of this variant's distinctive contribution. Six fixture cards (H3-style REFUTE, pr86-style AFFIRM, clean static defect, sha-pinned, malformed, runtime-verified REFUTE) + five property tests (P1-P5) + pytest hookup gating PR merges.

## Migration / backward-compat note

- **Schema v1.0 cards (no claim_class)**: calibrator defaults to `claim_class: runtime_behavior` (fail-safe per Variant 1). Pin test Fixture 5 asserts this default fires correctly.
- **In-flight pr86 calibration**: re-running calibration with the v1.5 rubric will produce different (lower) scores for source-only runtime-behavior claims. This is intentional — the calibration was wrong. Annotate the old reports with `[calibrated under pre-M1+M2+M3a rubric — see new rubric for current scoring]`.
- **Eval-suite "Test Results 1.000/1.000" claim** in `confidence-check/SKILL.md:14-18`: scoped via Change 4 to its actual coverage (5 pre-implementation checks). The unqualified claim was the cultural prior making M2 invisible.
- **Pin-test corpus growth**: Fixtures 1-6 are the seed. Add a fixture every time a new calibration miss is identified. This is the antidote to silent-green: the suite should grow strictly faster than the rubric/calibrator surface area.
