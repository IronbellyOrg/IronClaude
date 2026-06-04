<!-- Provenance: produced by /sc:adversarial --compare (Option A vs Option B) -->
<!-- Base: Option B (simplified, no-envelope) -->
<!-- Incorporated from Option A: state-persistence + halt-semantics insights -->

# Merged Recommendation — DEV-R13-001 fix

## Verdict: adopt **simplified Option B** for R1.3 now. Convergence 0.88.

The adversarial debate + invariant probe overturned the question's shared premise. The
recommendation is NOT a straight "Option B as proposed" — the sufficiency challenge
(INV-001) showed that **passing envelope to make the code_assertion fire at runtime is
itself wrong**, so the winning fix is a *simplified* Option B that does NOT pass envelope.

### The decisive finding (INV-001, HIGH)
`assert_step_reachable` AST-parses `repo_root/"src"/"superclaude"/cli/roadmap/executor.py`
(`code_assertions.py:78`) and is **fail-closed** (`L80-81`: missing file → HIGH Finding →
gate FAIL). Production is a **pipx-installed package** (CLAUDE.md memory
`reference_superclaude_install_vector`) whose layout is `site-packages/superclaude/...`
with **no `src/` tree**. Therefore:
- `assert_step_reachable` is inherently a **CI / source-tree** check. It cannot run
  meaningfully at production runtime.
- The `gate_passed` envelope-None shim that keeps it dormant at runtime is **CORRECT for
  this assertion**, not a deferred bug. DEV-R13-002's framing ("plumb envelope so it fires
  at runtime") must be **corrected** — doing that would spuriously fail certify on every
  installed-package run.

### What DEV-R13-001 actually needs (the real gap)
certify's **3 semantic_checks** (`certified_is_true`, `per_finding_table_present`,
`frontmatter_values_non_empty`) inspect the produced `certification-report.md` — they are
layout-independent and runtime-meaningful, and today they never run. The fix is to evaluate
them via `gate_passed(certify_step.output_file, CERTIFY_GATE)` **with no envelope** — the
shim then skips ONLY the source-tree code_assertion, which is exactly what we want.

## Implementation (R1.3 NOW) — simplified Option B

In `_run_certify_after_remediate` (executor.py ~L2170), after `roadmap_run_step` returns:

1. `passed, reason = gate_passed(certify_step.output_file, CERTIFY_GATE)` — **no envelope/repo_root**.
2. If `not passed`: set `certify_result` to a non-PASS status with `gate_failure_reason = reason`,
   and derive the run outcome as **`certified-with-caveats`** (per `derive_pipeline_status`) rather
   than a hard `sys.exit` — certify runs after the main pipeline already succeeded; a late
   certification caveat should be recorded, not crash the run.
3. Persist the certify outcome: `build_certify_metadata(...)` → `write_state(...)` so certify is
   reflected in `.roadmap-state.json` (closes the "not persisted" compounding gap; `_save_state`
   at L3369 runs before certify, so certify needs its own targeted state write).
4. Resume path (executor.py ~L3593): add the `_run_certify_after_remediate` call, guarded by the
   existing `check_certify_resume` skip (closes DEV-R13-006).

Properties: local blast radius (one function + resume-path call), reuses existing helpers, no
shared-executor change, no envelope-plumbing ripple, no installed-package fragility. Fixes
DEV-R13-001 (semantic gate now evaluated) and DEV-R13-006 (resume parity).

## What changes about the audit's DEV-002 / R1.6 carry-forward (CORRECTION)
The earlier Follow-Up Item ("R1.6 must delete the shim AND plumb envelope into the live gate
path so the code_assertion fires at runtime") is **partly wrong** and must be re-scoped:
- **Do NOT** make source-tree/AST code_assertions (like `assert_step_reachable`) fire at
  production runtime — they depend on the `src/` checkout that installed packages lack.
- R1.6 should instead **split `code_assertions` into two kinds**: (a) **CI-only** static/source-tree
  checks (assert_step_reachable) — enforced exclusively by tests; and (b) **runtime** artifact
  checks (assert_envelope_artifacts_present, and the R1.5 verify-implementation FR→AST checks that
  operate on the run's own artifacts) — these may fire in the live gate path, and THOSE are what
  R1.6's envelope-plumbing should serve.
- The envelope-None shim should not be blanket-deleted; it should be replaced by an explicit
  per-assertion classification (CI-only vs runtime) so the live path runs only runtime-safe ones.

## Deferred to R1.6 (unchanged or newly-scoped)
- Canonical envelope plumbing into `execute_pipeline`'s gate call — but ONLY to serve runtime-safe
  code_assertions (per the split above), not source-tree ones.
- The CI-only-vs-runtime code_assertion classification mechanism.

## Net
Simplified Option B is a small, local, installed-package-safe change that closes the real
DEV-R13-001 correctness gap now, while the invariant probe corrects an architectural
misconception in the original R1.6 carry-forward (don't fire source-tree assertions at runtime).
