# Troubleshoot Report — Run 2: PR #172 Sysx public-seed failure

**Target**: Sysx public arm (job 105657435166) seed-identity + rerun FAILs after successful create on df00c06
**Type**: deployment
**Tier reached**: 2
**Confidence**: 0.42 (calibrated, root-cause card; rubric penalizes unobserved enum)
**Status**: success_with_hardening_blocker (hardening witness = the retry run itself)
**Escalation reason**: forced_by_depth_deep
**Test is wrong**: partially — the rerun FAIL's label is wrong ("idempotency violated" for a rerun that never executed, test-startup-boot.sh:1960-1968 ordering); the seed assertion itself is CORRECT and must not be weakened
**Behavior is documented**: n/a
**Date**: 2026-09-18T18:40:00Z

---

## Summary

The layer mitigation is exonerated: the DinD-public arm passed the identical image, identical seed script, and identical octocat clone, and the Sysx-blank arm passed the same runtime — the failure is confined to the §8 outcome-derived checks of `seed_checkout_assert` (test-startup-boot.sh:380-401) under (sysbox-runc × outbound public clone). The probable recorded outcome is `clone-failed` — a fast, network-level git failure specific to the sysbox runtime's process environment (both cards converge; all other enums excluded by source logic plus the 13.9s startup duration vs the 120s clone budget anchored at §8 start). The second FAIL is collateral: `RERUN_SCRIPT` runs `seed_checkout_assert public cloned` under `set -euo pipefail` BEFORE the orchestrator rerun (test-startup-boot.sh:1962), so the rerun never executed and the NFR18 label is a misnomer. This step was never exercised before — no prior Sysx public run survived container create; the layer fix exposed the next latent failure in the chain.

## Diagnosis

**Root cause** (probable, pending enum): the in-workspace `git clone https://github.com/octocat/Hello-World.git` fails fast under sysbox-runc on the Coder host, so §8 records an outcome ≠ `cloned` and the correctly-written assertion rejects it.

**Cause class**: environment/runtime boundary (sysbox-runc internals — seccomp/proc-emulation/egress specifics unobservable from repo; host investigation is owner territory).

**Decomposition** (root-cause card): every runtime-independent check in the live seed ws_ssh (profile, DOCKER_HOST⇄RUNTIME, startup/askpass SHAs, modes, PAT guard) is proven passing under sysx by the sysx-blank control and under public-bytes by the DinD control; the only runtime-dependent inputs are the §8 outcome surfaces (seed-repo-outcome, section.8.*, and the tree checks contingent on a successful clone).

## Evidence

1. Job 105657435166 (Sysx public, df00c06): create OK; startup exit 0 `returned-success`, 13.9s (artifact startup-run.json, id 10559741513)
2. Coder Template CI 35360117622 matrix: dind-sidecar/public PASS, dind-sidecar/blank PASS, sysbox-runc/blank PASS — only sysbox-runc/public FAIL (gh run view)
3. `.github/contract-tests/test-startup-boot.sh:1941-1947` — live seed ws_ssh check order (all runtime-independent prefix checks controlled by the two passing arms)
4. `.github/contract-tests/test-startup-boot.sh:380-401` — seed_checkout_assert: outcome-derived checks are the discriminant
5. `.github/contract-tests/test-startup-boot.sh:1960-1968` — RERUN_SCRIPT ordering proof of rerun-collateral
6. `templates/VSCode-AIDev02/scripts/startup.sh:568-580` — 120s clone budget anchored at §8 start (cold boot cannot consume it); `:656-668` outcome mapping (fast git failure → clone-failed; auth-* unreachable for anonymous clone)
7. `templates/VSCode-AIDev02/main.tf:457-473` — both arms attach the same coder_coder_network; sole sysx delta is the OCI runtime (`:436`); DinD-public PASS is a positive egress control for the host/bridge
8. Artifact seed-checkout.txt: only `remote-assertion=fail` — pre-instrumentation runs emit no enum (the evidence gap atom B closes)

## Proposed Fix (owner-authorized experimental retry, one commit)

1. **Restore the layer mitigation**: revert-of-revert of c665c57 (exact inverse per self-review; restores df00c06: COPY consolidation 46→31, budget-73 gate). Create-clearing on Sysx is proven by this very run reaching post-create verification for the first time.
2. **Adopt the read-only seed projection** (Fable 6ced457 hunk, verbatim-safe per self-review): SEED_OUTCOME/SEED_DIAG allowlisted rows emitted BEFORE the assertion, plus its self-test rows. Assertions unchanged; sysx arm stays continue-on-error; nothing weakened. Decision rule: drop atom 2 if PR #170 merges or its queued run (job 105704643590) yields a non-absent enum before push — currently still queued, so both atoms ship.

## Alternative Fixes Considered

- **Weaken/skip the seed assertion for sysx** — rejected: gate weakening forbidden; the assertion is correct.
- **Guess a production network fix (proxy/DNS in template)** — rejected: cause unobserved; speculative template change violates minimal-diff discipline.
- **Do nothing (sysx is informational)** — rejected by owner directive (experimental retry on same PR) and leaves the enum gap open.

## Risk + Rollback

- Regression risk low (both atoms reviewed; revert is exact inverse; projection is read-only + allowlisted).
- If the retry run still fails Sysx public with `clone-failed`: honest terminal state for this PR is "Sysx public blocked on host-side sysbox egress — owner investigation required"; DinD arms + contracts + P-7 + cleanup remain the merge gates. Parent coordinates; no further blind iterations.
- Rollback: single `git revert` (precedent c665c57).

## Grounding Gaps

- The §8 outcome enum is UNOBSERVED in my run (pre-instrumentation artifact emits none) — `clone-failed` is source-logic-deduced, not read. Atom 2 (or Fable's run) resolves it.
- The underlying sysbox-internal break mechanism (seccomp vs proc-emulation vs egress specifics) is unobservable from the repo; host-side investigation is owner territory.
- Calibrated confidences (0.42/0.30) reflect exactly this gap; self-reports (0.87/0.78) were not used.

## Pipeline Hardening Closure

Applicable (evidence-boundary topology per run-1 correction precedent). **Verdict: blocked_pending_retry_run** — the required H1 runtime witness is the instrumented retry run itself; per owner directive this does NOT gate the push (CI is the validation venue). Waiver none; backtest not_run; off-path review performed (calibrators + self-review + cross-PR DinD control). NOT PROVEN — runtime proof deferred to run [pending ID].

## Next Steps

Push the two-atom retry to PR #172, record head/run IDs in publication.json, report to parent; on first CI result capture step/error/commit and report before any further iteration.

## Audit

- Cards: run2-tier1-hypothesis.md (cal 0.50), run2-tier2-root-cause-analyst-hypothesis.md (cal 0.42), run2-tier2-devops-architect-hypothesis.md (cal 0.30)
- Adversarial: not invoked — consensus
- Self-review: OK (run2-self-review.md)
- Audit log: audit.log (RUN 2 block)
