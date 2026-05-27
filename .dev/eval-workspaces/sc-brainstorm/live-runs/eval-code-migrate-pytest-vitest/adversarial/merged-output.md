<!-- Provenance: produced by sc:adversarial probe rerun for sc:brainstorm -->
<!-- Base: Variant 1 (architect, parallel-run), augmented with Variant 2 (refactorer) -->
<!-- Merge date: 2026-05-27 -->

---
case_id: code-migrate-pytest-vitest
topic: migrate from pytest to vitest
domain: code
status: success
convergence_score: 0.82
---

# Merged Output — pytest → vitest migration

(Normalized into the canonical brainstorm contract at `../merged-requirements.md`. This file is the raw adversarial merge output before Wave 3 step 5 normalization.)

## Strategy

Parallel-run base with bounded calendar and config-only cutover PR.

## Requirements (raw, pre-normalization)

1. Characterize pytest before any migration step.
2. Stand up vitest as a non-blocking CI job initially.
3. Commit a pytest → vitest concept-map doc.
4. Migrate suites per PR (leaf-most first); both runners green per PR.
5. Coverage non-regression check on every PR.
6. Parallel-run window has an explicit calendar end-date and a single accountable owner.
7. Flip vitest job to blocking when parity is reached.
8. Single config-only cutover PR removes pytest config + plugins + job.
9. Post-cutover dep-prune PR removes pytest-* deps from `pyproject.toml` or equivalent.

## Convergence

- Score: 0.82
- Status: PASS
