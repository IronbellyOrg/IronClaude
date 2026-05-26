---
proposal_id: 2
persona: qa
model: haiku
lens: test surface, edge cases, regression risk, acceptance criteria
---

# Proposal 2 — QA: Equivalence Gate Before Bridge Deletion

## Position

The migration plan is sound, but the *gate* between "vitest is running" and "delete the bridge" is the part where false confidence kills you. **Run both runners in parallel for at least one full sprint after the last batch flips,** with an explicit equivalence checker that compares pass/fail counts per directory between vitest and the pytest-shell bridge. Delete the bridge only after the equivalence checker is green for 5 consecutive CI runs.

## Failure modes to design against

1. **False pass via missing test discovery.** Vitest's default `include` glob is `['**/*.{test,spec}.?(c|m)[jt]s?(x)']`. If the existing tests use a filename pattern outside this (e.g., `__tests__/foo.spec.tsx`), vitest silently runs *zero* tests in that directory and reports green. **Mitigation**: explicit `include` glob matching the existing tree's actual file naming. CI assertion: `test count >= baseline count`.

2. **Different assertion semantics.** `expect(x).toBe(y)` in vitest and jest-style are similar but not identical at edge cases (NaN handling, Symbol equality, deep-vs-shallow comparison on Maps). The shell-pytest bridge invokes Jest underneath today; vitest's `expect` is Chai-flavored. **Mitigation**: surface this in the migration PR template — every batch PR must enumerate any test that changed assertion shape.

3. **Test isolation differences.** Vitest defaults to file-level parallelism with shared module cache by default; Jest defaults to file-level isolation. A test that mutates a shared module-level singleton can pass in Jest and fail in vitest (or vice versa). **Mitigation**: run vitest with `--isolate` in CI for the first month post-cutover to match Jest semantics, then evaluate switching off for the speed win.

4. **Coverage drift undetected.** Even if `merge-coverage.py` still produces an LCOV, the *contents* may shift (vitest-istanbul may instrument differently than nyc). A line that was 100% covered yesterday may show 95% today without anyone noticing. **Mitigation**: capture a baseline coverage report from the pre-migration `main` branch. After cutover, run a coverage diff. Any function that goes from "fully covered" to "partially covered" gets an issue filed.

5. **Snapshot tests break.** If any tests use jest-style snapshots (`toMatchSnapshot()`), the file format is identical but the *path* convention differs (`__snapshots__/Foo.test.tsx.snap` vs `__snapshots__/Foo.test.tsx.snap` — actually the same, but the comparison engine differs at multi-line whitespace). **Mitigation**: grep for snapshot usage before migration; if any exist, run a snapshot-update pass on the vitest side and diff the resulting `.snap` files. Zero diffs = pass.

6. **CI minutes regression instead of improvement.** The seed brief targets ≤2 min p95. Without a baseline measurement *captured before cutover*, you can't prove improvement. **Mitigation**: collect 20 CI runs of the legacy pytest-shell job before any vitest work; compute p95. Post-cutover, collect 20 vitest runs; verify p95 < 2 min.

## Acceptance criteria (concrete)

- **AC-Q1** — Equivalence gate: for every batch PR, vitest test count for the migrated directory equals the pytest-shell bridge's pass count (within ±0 tests). If different, PR is blocked.
- **AC-Q2** — Coverage parity: post-cutover combined LCOV total-line-coverage is within −1% of pre-cutover. Any single file dropping >5% gets an issue filed.
- **AC-Q3** — Wall-clock: vitest CI job p95 < 2 min over 20 consecutive runs. Captured by the existing CI metrics dashboard.
- **AC-Q4** — Parallel-run sprint: both runners run for ≥10 CI days after the last batch flips; equivalence checker green for ≥5 consecutive runs before bridge deletion.
- **AC-Q5** — Snapshot zero-diff: if snapshots exist, post-migration `__snapshots__/` directory diff against pre-migration baseline is empty.
- **AC-Q6** — Storybook smoke: post-cutover, Storybook build succeeds (proves fixtures alias still resolves).

## Risks the refactorer plan under-weights

- **R-Q1** — "5 days for batch migration" assumes batches don't surface assertion-shape diffs. Realistically, at least one batch (probably the `hooks/` one, which has more deep equality assertions) will hit a vitest/jest semantic diff. Budget +2 days.
- **R-Q2** — Deleting the bridge after one parallel run is too fast. Five consecutive CI runs is the minimum to filter out flake noise. **Insist on this.**
- **R-Q3** — Coverage provider choice (`istanbul` vs `v8`) is presented as a simple lever. It's not: `istanbul` instruments source, `v8` uses native coverage. They disagree on coverage of arrow functions and computed properties at the ~1-2% line. The refactorer is right to pick `istanbul` for compat — but if anyone later wants to switch to `v8` for speed, that needs its own change with its own equivalence gate.

## Test plan summary

- Unit (vitest itself): N/A — we're not building vitest, we're configuring it.
- Migration verification per batch: equivalence checker (script: `scripts/compare-test-counts.sh`) compares pytest-shell output to vitest `--reporter=json` output per directory.
- Coverage diff: `scripts/coverage-diff.py` (new, ~30 lines) reads pre-migration LCOV from a stored baseline and compares per-file line coverage.
- E2E: full CI run with both runners enabled; gate merge only when both green.
