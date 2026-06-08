---
artifact: option-b-rf-qa
qa_phase: task-integrity
target: "DEV-R13-001 / DEV-R13-006 simplified Option B fix"
task: TASK-RF-20260531-042405
created_date: 2026-06-02
verdict: PASS
confidence: 1.00
halt: false
note: "Could not be written at QA time due to ENOSPC; transcribed from the rf-qa agent's returned verdict after disk space was freed."
---

# rf-qa Adversarial Verdict — simplified Option B (DEV-R13-001 / DEV-R13-006)

## Overall: PASS — 1 MINOR scope-fidelity finding, no fix required, NO HALT

8/8 checks verified by reading files + running tests. All 6 new tests are
non-vacuous; focused suite green; ruff clean; only full-suite failures are the
3 pre-declared `test_default_agents*` (haiku-vs-sonnet drift), confirmed unrelated.

## Per-check findings

1. **No envelope passed — PASS.** `gate_passed(certify_step.output_file, CERTIFY_GATE)` called positionally; `envelope=None` hits the shim (`gates.py:93-98`), so `assert_step_reachable` (AST-over-`src/`) is correctly skipped while the 3 semantic_checks + frontmatter + min_lines still run.
2. **FAIL → certified-with-caveats, no exit — PASS (non-vacuous).** `dataclasses.replace(..., status=FAIL, gate_failure_reason=reason)` then append; no `sys.exit`/raise. `derive_pipeline_status` returns `"certified-with-caveats"`. The FAIL test genuinely flips `_certified_is_true`.
3. **Persistence — PASS.** certify appended then `_save_state(certify_metadata=...)`; lands in both `state["steps"]` and `state["certify"]`. No-progress + agent-mismatch guards pass on a fresh run.
4. **`_parse_certify_counts` — PASS.** OSError-guarded; line-anchored `^key:\s*(\d+)\s*$` regex, no YAML parser → malformed frontmatter can't crash; unmatched leaves default.
5. **DEV-R13-006 resume — PASS.** certify call is after the resumed-failure `sys.exit` and the success print (runs only on resumed success). No double-certify: spec-fidelity-fail path returns before the fresh-run certify (mutually exclusive).
6. **ADVERSARIAL — no new hard-fail path — PASS.** `gate_passed` on a missing report returns `(False, "File not found")`, does not raise; `assert_step_reachable` returns Finding/None, never raises (and is skipped anyway). Certify cannot hard-fail the pipeline — strictly safer than pre-fix.
7. **ADVERSARIAL — FAIL certify in `state["steps"]` is inert — PASS.** `derive_pipeline_status` reads `state["certify"]`, not `state["steps"]["certify"]`. `_apply_resume`/`_step_needs_rerun` iterate only `_build_steps` output, which excludes certify. On clean `--resume`, `_apply_resume` removes passing steps so certify already no-ops — no spurious re-run.
8. **Tests + ruff — PASS.** Focused set 64 passed (incl. 6 new); ruff clean on both changed files; full `tests/roadmap/` = 3 failed / 1846 passed / 12 skipped, the 3 being exactly the pre-existing `test_default_agents*`.

## The one finding (MINOR, no fix needed)

Merged-recommendation item 4 said the resume certify call should be "guarded by the
existing `check_certify_resume` skip." The implementation does NOT wire
`check_certify_resume` at either call site; that helper now has zero production callers
(tested only). Verified **functionally redundant, not a bug**: `_apply_resume` skips
passing steps by *removing* them from the run list, so on a clean resume remediate-PASS
is absent from `results` and `_run_certify_after_remediate` already no-ops — the guard
would change nothing. Not fixed (wiring it is a behavioral no-op and could obscure the
correct re-certify path). Recommend (non-blocking, R1.6): wire the guard for explicitness
OR add a one-line doc note that `_apply_resume`'s skip-by-removal already provides
idempotency.

## Informational (not a finding)
On `--resume` where remediate is re-run AND the user passes different `--agents` than
state, the agent-mismatch guard would skip the certify state-write — that's the guard's
documented anti-corruption job in a misuse case (agents are normally restored from state),
and it predates this change.

Verified 8/8 | 100% confidence | Tool engagement: Read 7, Grep 5, Bash 3.
Recommendation: PROCEED — closes DEV-R13-001 + DEV-R13-006 with installed-package-safe semantics.
