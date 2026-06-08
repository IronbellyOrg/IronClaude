<!-- Provenance: produced by /sc:adversarial Mode B (inline), Step 2 Debate -->

# Adversarial Debate Transcript — Phase 10 (R1.5)

## Metadata
- Depth: standard (Round 1 parallel + Round 2 rebuttal + Round 2.5 invariant probe)
- Advocates: opus:architect (A), sonnet:analyzer (B), haiku:qa (C)
- Convergence threshold: 0.80
- Focus: necessity, correctness vs §MVR §4, CI-vs-runtime code_assertion distinction, step-budget honoring, fragility

## Round 1 — Advocate Statements

### Advocate A (opus:architect) — KEEP-leaning
- Steelman of B/C: the CI-vs-runtime hazard (X-001) is genuine and decisive; a source-tree FR scan cannot gate a pipx run.
- Position: The *intent* of §MVR §4 (a terminal Tasklist→AST verification killing the Flaw-1 fail-open chain) is correct and necessary. Step 10.1 (design-first, force the consolidation choice) and Step 10.3's budget/dispatch tests (U-001, U-002) are high-value and must be KEPT.
- Concession: Step 10.2 as written conflates two substrates. It must be REFACTORED to make the assertion operate on the **run's own artifacts** (tasklist/roadmap emitted by THIS run) + `envelope.accepted_deviations`, not the pipeline `src/` tree. The "AST" in "Tasklist→AST" should AST-parse the run's tasklist/roadmap for FR→named-binding claims, not rglob the pipeline source.

### Advocate B (sonnet:analyzer) — REFACTOR-leaning
- Steelman of A: the step is necessary; deleting verify-implementation outright would leave Flaw 1 only half-closed (R1.6 deletes the fail-open default but nothing replaces the positive resolution path).
- Position: Every Phase 10 item needs REFACTOR, not DISCARD, except the design step which is fine. Two concrete defects beyond the substrate issue:
  1. C-004/A-002: `envelope.spec_ids[FR]` is a type error — `spec_ids` is a `SpecIdRegistry` with `fr_ids: tuple`. Correct access is `envelope.spec_ids.fr_ids`.
  2. Step 10.2's `_run_verify_implementation(envelope, repo_path)` + `assert_all_frs_resolved(envelope, repo_path)` signatures keep `repo_path`/`repo_root` — that handle only resolves under a dev checkout (GT-4). If kept, it must be classified CI-only (dormant at runtime via the shim) and a *separate runtime-safe artifact assertion* must provide the live gate.
- Concession: if the assertion is reframed as runtime-artifact-only, `repo_root` may not even be needed — pushing it toward A's reframing.

### Advocate C (haiku:qa) — DISCARD/fragility-leaning
- Steelman of A/B: the design step and the budget-guard test are cheap and protective; killing them loses regression protection.
- Position (fragility hunt):
  1. X-002 is the killer: if verify-implementation's only assertion is source-tree, then at runtime EITHER the shim skips it (gate verifies nothing — a silent no-op, the very fail-open it claims to kill) OR it fires and fails-closed on every installed-package run (false halt on 100% of production runs, GT-4). Both are unacceptable. So Step 10.2 as written is DISCARD-as-written.
  2. The line-number citations are stale (GT-3: fail-open is L302/L320 not L287-303). A worker following the task verbatim edits wrong lines.
  3. `importlib.import_module` (X-003) to resolve an FR's name binding assumes the implementation is importable from the pipeline's namespace — false for a user project. Fragile.
  4. Step 10.3 `test_all_frs_resolve` "every FR maps to a real importable callable in the test fixtures" — this only ever passes under a dev test tree, confirming the assertion is intrinsically CI-only.
- Concession: the *test* items (10.3) and the design item (10.1) are KEEP/light-REFACTOR; only 10.2's resolution substrate is the deep problem.

## Round 2 — Rebuttals

- A → C: "silent no-op" overstates if we adopt the reframing. A runtime-safe verify-implementation reads the run's emitted tasklist/roadmap (always present as the run's own artifacts, GT-3 `_extract_fr_mappings` already reads a spec/artifact path) and asserts every `envelope.spec_ids.fr_ids` entry either appears with a named binding in the run's artifacts or is in `accepted_deviations`. That fires at runtime, is layout-independent, and kills Flaw 1's positive path. So the verdict is REFACTOR (rescue), not DISCARD.
- C → A: concedes. With the artifact-grounded reframing the step becomes runtime-meaningful. C upgrades 10.2 from "DISCARD-as-written" to "REFACTOR (mandatory substrate swap)".
- B → all: agreement converging. B adds: keep the source-tree `assert_step_reachable`-style check as a SEPARATE CI-only test (it already exists from R1.3 and Step 10.3 reuses it via `test_step_in_dispatch_map`) — do NOT fold a source-tree scan into the live gate.
- All → budget (S-003): consensus that Step 10.1/10.2's consolidation requirement is correct and load-bearing (GT-5: 14→15 without it). The wiring-verification absorption is the cleaner choice since verify-implementation AST-grounds the same property at the artifact level; certify-absorption is riskier (certify carries 3 runtime semantic_checks the R1.3 fix just wired). Recommend wiring-verification as the consolidation target, with certify preserved.

## Round 2.5 — Invariant Probe
See `invariant-probe.md`.

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| X-001 | B/C (substrate is CI-only) | 95% | GT-1/GT-2/GT-4; R1.3 INV-001 |
| X-002 | C (no-op-or-false-halt dilemma) | 92% | shim GT-2 + CWD fallback GT-4 |
| X-003 | C (importlib is dev-only) | 85% | user impl not in pipeline namespace |
| C-004/A-002 | B (type error) | 98% | SpecIdRegistry has no __getitem__ (GT-6) |
| A-003 | A (runtime-artifact reframing exists) | 90% | `_extract_fr_mappings` reads artifact path; envelope carries accepted_deviations (GT-7) |
| S-003 | consensus (consolidate wiring-verification) | 88% | GT-5 budget; certify carries runtime checks |
| U-001/U-002 | consensus KEEP | 95% | cheap regression guards |

## Convergence Assessment
- Points resolved: 7 of 7
- Convergence: ~0.91 (above 0.80 threshold)
- Status: CONVERGED (after Round 2 + invariant probe), with 1 HIGH invariant requiring mandatory REFACTOR (does not block the *verdict*, it IS the verdict).
- Unanimous outcome: Phase 10 is NECESSARY (kills Flaw 1 positive path) but 10.2 requires a mandatory substrate REFACTOR from source-tree scan → run-artifact + envelope grounding. 10.1, 10.3, PG10.1, PG10.2 are KEEP with minor REFACTORs.
