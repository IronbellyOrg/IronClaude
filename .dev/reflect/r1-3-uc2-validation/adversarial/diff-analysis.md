# Diff Analysis — Option A vs Option B (DEV-R13-001 fix)

## Metadata
- Variants: 2 (Option A = route certify through execute_pipeline; Option B = explicit gate_passed in _run_certify_after_remediate)
- Focus: correctness, blast-radius, spec-fidelity, maintainability, regression-risk
- Diversity source: heterogeneous reviewer input carried from the parent sc:reflect Wave 3 (sonnet BLOCK / haiku ship-with-notes) + orchestrator (opus) invariant probe.

## Variant summaries
- **Option A** — Make certify a normally-gated pipeline step by routing it through `execute_pipeline` (A1: dynamic append into the shared step loop; or A2: a second `execute_pipeline([certify_step])` pass). `gate_passed` runs via the canonical path. To also fire the code_assertion, envelope+repo_root must be plumbed into `execute_pipeline`'s gate call (ripples to all gated steps + consumers).
- **Option B** — After `roadmap_run_step` returns in `_run_certify_after_remediate`, add an explicit `gate_passed(certify_step.output_file, CERTIFY_GATE[, envelope, repo_root])`, act on the verdict, persist, and add the call to the resume path. Local blast radius.

## Diff points

| ID | Level | Topic | Option A | Option B | Severity |
|----|-------|-------|----------|----------|----------|
| C-001 | L2 | Where gate is evaluated | Canonical execute_pipeline path | New explicit call inside the certify helper | Medium |
| C-002 | L2 | Blast radius | Touches shared pipeline executor (A1) or double-invokes it (A2); risks sprint/cli_portify/cleanup_audit | One function + resume-path call | High |
| C-003 | L3 | Does the code_assertion fire at runtime? | Only if envelope plumbed (huge ripple) | Yes, if envelope passed | High |
| C-004 | L3 | **Installed-package safety of firing assert_step_reachable at runtime** | n/a unless envelope plumbed | **Naive B (pass envelope) spuriously FAILS in pipx install — no src/ tree** | High |
| C-005 | L2 | R1.3 scope fit ("not a pipeline-executor refactor") | Violates (executor control-flow change) | Fits (local) | Medium |
| C-006 | L3 | Halting semantics | Inherits execute_pipeline halt (hard exit on FAIL) | Caller chooses (can map FAIL→certified-with-caveats) | Medium |
| C-007 | L2 | State persistence | Via normal _save_state | Via build_certify_metadata + write_state (helpers exist) | Low |
| C-008 | L1 | UX / output | A2 emits a 2nd "Pipeline complete" | Single summary line | Low |

## Shared assumptions (UNSTATED, promoted)
- **A-001 [SHARED-ASSUMPTION] (CONTRADICTED):** Both options' framing assumes the code_assertion *should* fire at production runtime (that "runtime-dormant" is a bug to fix). The invariant probe contradicts this: `assert_step_reachable` AST-parses the `src/` source tree and is fail-closed; it is inherently a CI/source-tree check that would break installed-package production. → escalated to the debate's Category-6 sufficiency challenge.
- **A-002 [SHARED-ASSUMPTION] (UNSTATED):** Both assume DEV-001 requires *envelope* to be fixed. It does not — certify's semantic_checks are layout-independent and run via `gate_passed` with **no** envelope (the shim correctly skips only the code_assertion).
