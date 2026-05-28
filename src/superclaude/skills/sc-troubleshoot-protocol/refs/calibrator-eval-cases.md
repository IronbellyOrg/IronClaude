# Calibrator Eval Cases

Golden hypothesis cards + expected calibrated scores. Run before any change to `escalation-rubric.md`, `confidence-calibrator.md`, `hypothesis-card-template.md`, or `sc-troubleshoot-protocol/SKILL.md` ships. A regression on any fixture or property test blocks merge.

## Synthetic fixtures (V1 base)

### Fixture 1 — `fixture-h3-style.md` (source-only runtime REFUTE)

Hypothesis card with `claim_class: runtime_behavior`, `evidence_class: source_static`, `verdict_direction: REFUTE`, evidence_grounding=1.0, runtime_check=0.0 (cross-tab derived), four other dims=1.0.
**Expected calibrated**: ≤ 0.70 (M3a cap fires).
**Asserts**: M1 + M2 + M3a all closed in combination.

### Fixture 2 — `fixture-pr86-rca-style.md` (AFFIRM with structural truncation)

`claim_class: runtime_behavior`, `evidence_class: source_static`, `verdict_direction: AFFIRM`, evidence_grounding=1.0, runtime_check=0.5 (runnable command in card without captured output), four other dims=1.0.
**Expected calibrated**: ≤ 0.80 (gate_M2 = 0.80).
**Asserts**: M1 + M2 closure below the 0.85 STOP gate.

### Fixture 3 — `fixture-static-defect-clean.md` (eval_run.py Path import case)

`claim_class: static_defect`, `evidence_class: source_static`, `verdict_direction: AFFIRM`, evidence_grounding=1.0, runtime_check inherits 1.0, four other dims=1.0.
**Expected calibrated**: 1.0. **Asserts**: refactor does NOT over-correct.

### Fixture 4 — `fixture-sha-pinned.md` (structurally unverifiable predicate)

Card cites `commit-sha-5a65c62:file:line`. `claim_class: static_defect`, `verdict_direction: AFFIRM`, evidence_grounding=0.5, runtime_check inherits 0.5.
**Expected calibrated**: ≤ 0.80 (gate_M1 = 0.80).

### Fixture 5 — `fixture-v1-legacy-card.md` (missing claim_class — migration)

v1.0 frontmatter with no `Claim class`, `Evidence class`, or `Verdict direction` fields.
**Expected behavior**: calibrator defaults claim_class to `runtime_behavior`, evidence_class to `none`, verdict_direction to `AFFIRM` (fail-safe), records in Notes, proceeds.
**Asserts**: backward-compat — v1.0 cards do not break the calibrator.

### Fixture 6 — `fixture-refute-runtime-verified.md` (legitimate REFUTE with strong runtime check)

`claim_class: runtime_behavior`, `evidence_class: runtime_repro`, `verdict_direction: REFUTE`, evidence_grounding=1.0, runtime_check=1.0, four other dims=1.0.
**Expected calibrated**: 1.0. **Asserts**: M3a cap does NOT fire when runtime_check=1.0.

## Real-card replay fixtures (V2 merged)

### Fixture 7 — `fixture-t4-h3-replay.md` [V2 merged]

Replays actual `tier2-h3-options-subcommand.md` from `t4-pane-title-20260526-101500`. **Self-reported confidence on the original card: 0.95** (REFUTE — the canonical failure case the entire refactor is named after; passed through unguarded because the calibrator never executed against this card in the original run). Frontmatter retrofitted: `claim_class: runtime_behavior`, `evidence_class: source_static`, `verdict_direction: REFUTE`.
**Expected calibrated**: ≤ 0.65 (per V2 rule 1) or ≤ 0.70 (per V1 M3a). Either is below 0.85. **Asserts**: the actual failing card cannot slip through after the refactor.

### Fixture 8 — `fixture-t4-h2-replay.md` [V2 merged]

Replays actual H2 card from T4. **Self-reported confidence on the original card: 0.85** (REFUTE; also passed through unguarded). `claim_class: runtime_behavior`, `evidence_class: source_static` (WebFetch GitHub URLs), `verdict_direction: REFUTE`.
**Expected calibrated**: ≤ 0.70. Also triggers WebFetch unverifiability note. **Asserts**: source-only REFUTE on runtime claim is structurally caught.

### Fixture 9 — `fixture-t4-h1-no-overcorrect.md` [V2 merged]

Replays actual H1 card from T4 (0.82 self-reported CONFIRM with mixed source + log evidence). `claim_class: runtime_behavior`, `evidence_class: log_evidence`, `verdict_direction: AFFIRM`.
**Expected calibrated**: 0.70-0.85 range; NO hard cap fires. **Asserts**: legitimate CONFIRM cards with log evidence are NOT downgraded by the refactor.

## Property tests

| ID | Property | Assertion |
|----|----------|-----------|
| P1 | M1 gate | `evidence_grounding ≤ 0.5` ⟹ `calibrated ≤ 0.80` |
| P2 | M2 gate | `runtime_check ≤ 0.5 AND claim_class ∈ {runtime_behavior, environment_dependent}` ⟹ `calibrated ≤ 0.80` |
| P3 | M3a cap | `verdict_direction == REFUTE AND claim_class == runtime_behavior AND runtime_check < 1.0` ⟹ `calibrated ≤ 0.70` |
| P4 | Determinism | running calibrator on same card produces same calibrated score (±0.0) across N=5 runs |
| P5 | Anchoring (soft) | varying `Self-reported confidence:` from 0.30 to 0.99 must not change calibrated by more than ±0.05. **Soft assertion** (warn-only in CI). |

## Suite integrity

Run on every PR that touches:

- `escalation-rubric.md`
- `confidence-calibrator.md`
- `hypothesis-card-template.md`
- `confidence-check/SKILL.md`
- `sc-troubleshoot-protocol/SKILL.md` (V2-merged Change F)

A regression on any fixture or hard property (P1-P4) blocks merge. P5 warnings surface for triage.

## Implementation hook (deferred to follow-up commit)

Pytest harness invoking this corpus is OUT OF SCOPE for this brainstorm proposal. Expected landing path: `tests/troubleshoot/test_calibrator_eval_cases.py`.
