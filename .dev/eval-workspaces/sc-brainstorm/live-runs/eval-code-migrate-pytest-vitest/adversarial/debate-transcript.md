# Adversarial Debate Transcript — case 4 rerun

## Metadata

- Depth: quick
- Rounds completed: 2
- Convergence achieved: 0.82
- Convergence threshold: 0.75
- Focus areas: cutover strategy, parity, coverage gate
- Advocate count: 2 (architect, refactorer)

## Round 1: Advocate Statements

### Variant 1 Advocate (architect, opus)

Position summary: parallel-run with suite-by-suite migration. Keeps CI green at all times. Trades calendar time for safety.

Steelman of refactorer: The hard-cutover proposal is operationally tighter — total migration time is bounded, the dual-runner cost window is short, and the cutover PR is small and easily revertible.

Strengths claimed:
1. CI never goes red — every migration PR has both runners green.
2. Lower coordination cost per PR (small, targeted scope).

Concessions:
- Risk of indefinite parallel-run if no owner enforces the cutover decision.
- pytest + vitest CI cost stacks for the entire window.

### Variant 2 Advocate (refactorer, sonnet)

Position summary: time-boxed hard cutover. Characterize, scaffold, translate in batches, flip the gate in a single config-only PR.

Steelman of architect: The parallel-run proposal is safer in the worst case — it guarantees CI signal at every PR even if a vitest translation has a latent bug.

Strengths claimed:
1. Bounded calendar time — migration cannot drift indefinitely.
2. Concept-map doc lives on as a permanent reference.
3. Hard cutover removes pytest deps quickly (less surface to maintain).

Concessions:
- A long-tail pytest plugin with no vitest equivalent could stall the cutover.
- Reviewer bandwidth could throttle the migration cadence.

## Round 2: Cross-Examination

### Architect challenges Refactorer

Q: How does hard cutover handle a discovered pytest plugin with no vitest equivalent mid-migration?
A: The characterization step is the gate. If an unmapped plugin is found there, we escalate before scaffolding. If discovered mid-migration, we either build a small vitest shim or capture a written deprecation decision — never silently drop coverage.

Q: How is "≤ 4 weeks" defended if the suite is large?
A: It's a target, not a hard requirement. The PR-size constraint (≤ 500 LOC test diff) is the real cadence regulator; total time scales with suite size.

### Refactorer challenges Architect

Q: What prevents the parallel-run from becoming permanent?
A: Explicit end-date target and a single accountable owner. Combined with the rule that the vitest job flips to blocking once parity is achieved — this is the forcing function.

Q: How is coverage measured comparably between pytest-cov and c8/istanbul?
A: Normalize on line-coverage as the comparable metric. Branch-coverage is additive but not regression-gated until both runners report it the same way.

## Convergence Analysis

Both proposals share:
- pytest characterization as the entry gate
- concept map of pytest → vitest equivalents
- coverage non-regression as a hard requirement
- a defined cutover criterion and rollback path

They differ on:
- duration of dual-runner state (long vs. short)
- migration cadence (per-suite PRs vs. batched cutover)
- when pytest plugins/config are removed (final PR after release cycle vs. immediately at cutover)

Convergence score: 0.82 — agreement on essentials, divergence on cadence is policy not principle.

## Outcome

PASS. Merge proceeds with parallel-run as the **base** (safer default) but adopts refactorer's bounded-calendar discipline, concept-map artifact, and config-only cutover PR pattern as augmentations.
