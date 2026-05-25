---
debate_round: 1
proposals: [proposal-1-refactorer, proposal-2-qa]
convergence_score: 0.84
---

# Adversarial Debate Transcript

Two proposals against `seed-brief.md` (QUICK tier, 2 proposals as configured). Convergence is high because the proposals are largely **orthogonal**: refactorer covers the *how* (strangler-fig in 5 waves), QA covers the *gate* (equivalence checker, parallel-run sprint). The disagreements are around timing/budget rather than direction.

## Tension 1 — Bridge-deletion timing (Refactorer vs QA)

**Refactorer's position**: Wave 4 deletes the bridge ~0.5 day after Wave 3 (coverage cutover), assuming the equivalence has been proven during each batch PR.

**QA's pushback**: Per-batch equivalence is necessary but not sufficient. Flakes only surface in aggregate, over enough runs to filter noise. Demand 5 consecutive green CI days with both runners enabled before deletion.

**Resolution**: **QA wins.** Merged plan: Wave 4 is gated on `equivalence-checker green ≥5 consecutive CI runs over ≥10 calendar days`. Refactorer concedes the calendar cost (~1 additional sprint week) because the cost of false deletion (silent test-skip regression) dwarfs the cost of waiting.

## Tension 2 — Coverage provider (consensus)

Both proposals land on `@vitest/coverage-istanbul`. Refactorer for output compat with `merge-coverage.py`; QA for instrumentation-shape compat to avoid coverage drift. No tension. Adopted directly.

## Tension 3 — Test isolation default (QA flag)

QA raises that vitest's default file-level shared-cache parallelism differs from Jest's per-file isolation, and that a test that relies on Jest's isolation may silently fail post-migration.

**Refactorer's reply**: Plausible, but the seed brief's enrichment found no pytest-style fixtures; module-level mutation in tests is a code-smell that would already be a problem under the pytest-shell bridge (which runs Jest under the hood).

**Resolution**: **Adopt QA's mitigation prophylactically.** Run vitest with `--isolate` for the first month post-cutover. Capture metric: how many tests would change pass/fail status if `--isolate=false`. After the month, decide whether to disable for the speed win. Cheap to implement, surfaces the smell.

## Tension 4 — Co-location decision (carried forward as Open Question)

Refactorer explicitly defers co-location to a follow-up. QA does not address it. Merged plan carries this as an Open Question — not in scope for this work.

## Tension 5 — Snapshot tests (QA finding, refactorer silent)

QA raises snapshot tests as a potential subtle break. Refactorer's plan did not address snapshots specifically.

**Resolution**: Add a prerequisite check to Wave 0 — grep for `toMatchSnapshot` usage. If zero, drop AC-Q5 from acceptance criteria. If non-zero, AC-Q5 is mandatory and a snapshot-baseline must be captured pre-migration.

## Remaining disagreements

None substantive. The refactorer's plan + QA's gate compose cleanly. The main residual is timing: original "1 sprint" estimate becomes "2 sprints" once the parallel-run gate is honored.

## Convergence rationale

Two proposals, one tension (deletion timing) decisively resolved, two QA additions adopted (isolation flag, snapshot precheck), one carried-forward open question (co-location). Convergence **0.84** — high; the proposals were complementary rather than competing.
