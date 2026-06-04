<!-- Provenance: produced by /sc:adversarial Mode B (inline), merge step -->

# Merged Recommendation — Phase 10 (R1.5 verify-implementation)

## Verdict: Phase 10 is NECESSARY but Step 10.2 requires a MANDATORY substrate REFACTOR. Convergence 0.91.

verify-implementation is the positive half of the Flaw-1 fix: R1.6 (Step 11.4) deletes the fail-open `found=True` default, and verify-implementation must supply the fail-closed FR-resolution path that replaces it. Discarding it would leave Flaw 1 only half-closed. **But the task encodes FR-resolution against the pipeline `src/` tree** (`fidelity_checker._scan_codebase` rglob + `importlib`), which is a CI-only substrate that cannot gate a pipx-installed production run (R1.3 INV-001). At runtime this yields either a silent no-op (shim-skipped) or a 100%-false-halt (fails-closed because no `src/`). The fix is to ground the assertion in the **run's own artifacts** (the tasklist/roadmap THIS run emits) + `envelope.accepted_deviations` + `envelope.spec_ids.fr_ids`, which is layout-independent and runtime-meaningful.

## The decisive correction (INV-001 + INV-002, HIGH)
- `assert_all_frs_resolved(envelope, repo_path)` as specified inspects `repo_path/src/...` via `_scan_codebase`. That is a **CI-only** check (R1.3 split: source-tree/AST = CI-only; run-artifact = runtime-safe).
- A runtime CodeAssertion-only gate that depends on a source-tree scan is self-defeating: the `gate_passed` envelope-None shim (pipeline/gates.py:93-98) skips it unless envelope+repo_root are plumbed, and even if plumbed, `repo_root` resolves to the user's CWD on an installed package, so the scan target is wrong.
- **Sufficiency (INV-002):** verify-implementation closes Flaw 1 ONLY IF (a) its assertion reads the run's emitted artifacts (not src/), AND (b) the live gate path actually plumbs envelope so the assertion is not shim-skipped. Phase 10 as written guarantees neither.

## Required substrate for Step 10.2 (the REFACTOR)
`assert_all_frs_resolved(envelope, repo_path=None)` must, for each `fr_id in envelope.spec_ids.fr_ids`:
1. Check whether the FR's name binding appears in the **run's own emitted artifacts** (the tasklist/roadmap files produced by this run — already on disk as `envelope.artifacts[...]`/the run output dir), AST-or-text-scanned. This is the "Tasklist→AST" link §MVR §4 names. OR
2. Match `fr_id` against `envelope.accepted_deviations` (or `envelope.spec_ids.accepted_deviation_ids`).
3. If neither → HIGH Finding (fail-closed). Explicit empty-`fr_ids` guard → also a Finding (Contract #4: no silent PASS on empty target, closes INV-004).
The source-tree `_scan_codebase`/`importlib` path stays a CI-only test concern (Step 10.3's `test_step_in_dispatch_map` already uses the R1.3 `assert_step_reachable` walker for that) — it does NOT belong in the live gate.

## Budget (S-003, INV-006): KEEP as-is
Consolidate **wiring-verification** (executor.py:2588), not certify. verify-implementation AST-grounds the same wiring property at the artifact level; certify carries the 3 runtime semantic_checks the R1.3 fix just wired and must be preserved. This holds the count at 14 (Acceptance Gate #6).

## Net
The phase's existence, position, gate shape, budget-consolidation, and test scaffold are correct. The single deep defect is the FR-resolution substrate in 10.2 — swap source-tree scan for run-artifact + envelope grounding, fix the `spec_ids[FR]` subscript, and decide plumb-vs-CI-only per the R1.3 split. With those three changes the step becomes runtime-safe and actually kills Flaw 1's positive path.
