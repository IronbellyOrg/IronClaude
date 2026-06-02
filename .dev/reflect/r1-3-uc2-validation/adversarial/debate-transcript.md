# Adversarial Debate Transcript — Option A vs Option B

## Metadata
- Depth: standard (Round 1 + Round 2 + Round 2.5 invariant probe)
- Focus: correctness, blast-radius, spec-fidelity, maintainability, regression-risk
- Convergence: 0.88 (converged after the invariant probe reframed the question)

## Round 1 — Advocate statements

### Advocate A (route through execute_pipeline)
**Steelman of B:** B is local, closes DEV-001 + DEV-002 in one function, reuses build_certify_metadata.
**Position:** Architecturally, certify *should* be a normal gated step. Routing through execute_pipeline means one gate-eval path, no duplication, normal halt + state semantics. Avoids a bespoke second gate pathway that R1.6 must reconcile.
**Critique of B:** B creates a parallel gate-eval site; if R1.6 plumbs envelope into execute_pipeline, B's site is orphaned/duplicated.

### Advocate B (explicit gate_passed in the helper)
**Steelman of A:** A is the "clean" end-state — certify as a first-class gated step is conceptually right.
**Position:** R1.3's scope is explicitly "not a pipeline-executor refactor." A's A1 variant changes the SHARED `execute_pipeline` iteration semantics → risks sprint/cli_portify/cleanup_audit (PRESERVE-adjacent). A's A2 (second pass) double-invokes the pipeline (two _save_state, two "Pipeline complete" prints) for a single terminal step. B is local, reuses existing helpers, and lets the caller map a certify gate-fail to `certified-with-caveats` (matching derive_pipeline_status) rather than a hard exit.
**Critique of A:** A inherits retry/cosmetic-remediation/trailing-gate machinery certify doesn't need, and (to fire the code_assertion) forces the envelope-plumbing ripple that is explicitly R1.6 scope.

## Round 2 — Rebuttals

**A concedes:** the A1 shared-executor change is out of R1.3 scope; A2 is the only in-scope A variant, but its double-pipeline UX is awkward.
**B concedes:** the "second gate-eval pathway" is real duplication *if* one accepts the premise that certify's gate must eventually live in execute_pipeline.

Both advocates assumed (A-001) that making the **code_assertion** fire at runtime is the goal. Round 2.5 tests that premise.

## Round 2.5 — Invariant probe (fault-finder, sufficiency challenge)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | "Passing envelope makes the code_assertion correctly fire at runtime" | **UNADDRESSED** | **HIGH** | `assert_step_reachable` resolves `repo_root/"src"/"superclaude"/cli/roadmap/executor.py` (code_assertions.py:78) and is **fail-closed** (L80-81: missing file → HIGH CA-DISPATCH-001). Production install is **pipx** (CLAUDE.md memory `reference_superclaude_install_vector`) → site-packages layout, **no `src/` tree** → assertion would ALWAYS fail at runtime → certify spuriously FAILS. |
| INV-002 | guard_conditions | "repo_root is reliably the dev checkout at runtime" | UNADDRESSED | HIGH | `superclaude roadmap run` cwd is arbitrary; no config field carries repo_root. cwd-derived repo_root won't contain `src/superclaude` in production. |
| INV-003 | state_variables | "envelope.json exists when _run_certify_after_remediate runs" | ADDRESSED | MEDIUM | R1.2 dual-write writes the sidecar during the pipeline; but B must degrade gracefully if load fails (envelope=None → semantic_checks still run, only code_assertion skipped). |
| INV-004 | interaction_effects | "certify gate-FAIL should hard-halt" | ADDRESSED | MEDIUM | derive_pipeline_status already models `certified-with-caveats`; a gate-fail should map to that, not sys.exit. |
| INV-005 | sufficiency_challenge | "DEV-001 requires envelope to fix" | UNADDRESSED→resolved | HIGH | certify's 3 semantic_checks (certified_is_true / per_finding_table_present / frontmatter_values_non_empty) inspect the produced report — layout-independent. They run via `gate_passed(..., CERTIFY_GATE)` with **no** envelope; the shim skips ONLY the code_assertion. So DEV-001's real fix needs **no** envelope. |

**Convergence gate:** INV-001 is HIGH + UNADDRESSED by both naive options → blocks the naive framing. Resolution (below) addresses it by reframing.

## Reframed consensus (post-probe)

The probe dissolves the A-vs-B framing's shared premise:
1. `assert_step_reachable` is a **CI/source-tree check**, not a runtime check. The runtime shim that skips it is **correct**, not a deferred bug. Firing it at runtime (naive Option B-with-envelope, or Option A-with-envelope-plumbing) would break installed-package production.
2. DEV-001's real correctness gap is that certify's **semantic_checks** never run. Those are layout-independent and fixed by `gate_passed(certify_step.output_file, CERTIFY_GATE)` **without** envelope.
3. Therefore the winning fix is a **simplified Option B**: explicit no-envelope `gate_passed` in the helper + record result + resume-path call. Option A's machinery and envelope-plumbing are unnecessary and out of scope.

## Scoring matrix

| Diff point | Winner | Confidence | Evidence |
|------------|--------|------------|----------|
| C-002 blast radius | B | 90% | A touches shared executor / double-invokes; B is one function |
| C-004 installed-pkg safety | B (simplified, no-envelope) | 95% | INV-001: firing assert_step_reachable at runtime breaks pipx installs |
| C-005 R1.3 scope fit | B | 88% | "not a pipeline-executor refactor" |
| C-006 halt semantics | B | 80% | B can map FAIL→certified-with-caveats per derive_pipeline_status |
| C-001 gate-eval locus (purity) | A | 65% | A is conceptually cleaner *if* installed-pkg + scope weren't constraints |

Net: B wins 4/5 weighted points; A wins only the abstract-purity point, which the installed-package + scope constraints override.
