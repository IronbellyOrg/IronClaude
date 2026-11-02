# Refactor Plan

## Overview

- Base: Variant 2 (reviewer 2, qa) — adversarial/variant-2-original.md
- Incorporated: Variant 1 (reviewer 1, analyzer) — adversarial/variant-1-original.md; debate and invariant-probe outcomes
- Planned changes: 8; rejected: 2; overall risk: Low (classification and risk-register edits only; no AC verdict changes)
- Review status: auto-approved (2026-11-02T05:33Z)

## Planned Changes

1. **Reclassify R2-F1 (isatty guard) to necessary, LOW.** Source: V1 R1-F1, debate C-001/X-002/X-003 (both advocates and both calibrators). Target: base Deviations row R2-F1. Replace "drift / MEDIUM" and the claim "no artifact documents a discovered constraint" with: necessary, LOW; inline rationale at local-gateway-alias-proxy.py:859-862; the real forcing reason is a dead-pty stderr (proxy:126-127, :491 write stderr on every request; V1). Keep as notes: tty branch untested (test:598, ccsession:808); CHANGELOG.md:11 "the shim starts its own session" is unconditional while proxy:863 is not → soften to "when not started on a terminal" (documentation note, LOW). Risk: Low.
2. **Reclassify R2-F2 (T1 extra assertions) to necessary, LOW.** Source: V1 R1-F2, debate C-002. Evidence: getsid follows pre-execution F15 (pre-detach.../adversarial/merge-log.md:23) with an inline comment at test:1538; the thread wrapper records exceptions (an applied pre-execution finding); timeout=30 matches `streaming.join(30)`. Risk: Low.
3. **Split R2-F3 (CHANGELOG).** Heading suffix (CHANGELOG.md:9): drift, LOW, cosmetic (both variants). Last sentence (CHANGELOG.md:11 "A shim already running keeps the old behaviour…"): drift, LOW, accurate against ccsession:766 and :782-784; the only recorded rationale is an after-the-fact executor note (troubleshoot REPORT.md:135), and pre-execution F3 asked only for "shims stay up until stopped" (pre-detach REPORT.md:45, :76-77). Mark this point as the one unresolved debate point (C-004). Risk: Low.
4. **Keep R2-F4 (`make sync-dev`) as necessary, LOW.** No change.
5. **Add a Risks section (non-gating).** From V1 and the invariant probe:
   - INV-002 residual (MEDIUM, UNVERIFIED): other hosts (Orca on macOS, logind/sshd session teardown, environment-tag teardown). Addressed for this workspace by shared cgroup `0::/init.scope` and the detached 4013 shim surviving since Oct 31.
   - INV-001 (MEDIUM): under job control the shim becomes a group leader and setsid fails silently; the subshell still removes it from the ppid sweep; ccsession is a non-interactive `#!/bin/bash` script with no `set -m`.
   - macOS `os.getsid(<other pid>)` portability for test:1538 and :1562 (V1 R1-F6; CI runs ubuntu only).
   - Subreaper inside the terminal tree would keep the shim a descendant (V1 U-003; INV-004).
   - `sys.stderr` None (fd 2 closed) raises AttributeError at proxy:863 before bind; advisory — the old code already wrote stderr unguarded per request (proxy:126), so such a shim was already broken (V1 gap, calibrator correction; INV-005).
   - Stale shims accumulate after this change, each launch moving up a port, six tries before "no free shim port" (INV-006; ccsession:769, :793-796).
   - Tests do not send group/session signals and observe survival (INV-007); python3 wrappers (INV-003); pre-setsid window (INV-009); `pkill -f <copy path>` is a regex, slightly wider than exact-pid (V1 U-004).
6. **Correct the evidence notes.** Verification figure: verify-logs/pytest-ccsession.stdout.txt:17 "262 passed" (129 tiers + 133 tag) and package t5-checks.log:11 "457 passed" (7 files). Ledger pointer drift (progress.md T1 line cites t1-before.log:13/:19; outcome at :15-20, :22-23) is harmless.
7. **Update the adherence summary.** 13 AC audited, 13 adherent. Authorized 0; necessary 3 (R2-F1, R2-F2, R2-F4); drift 2 (heading suffix, last sentence; both LOW); regression 0.
8. **Add provenance and a "Not verified" list.** Not verified: Orca itself on other hosts; macOS; bash 3.2 runtime; `bash -n`, lint and the live check are implement-leg artifacts cross-corroborated by the reflect run's own 262-pass verification.

## Changes NOT Being Made

- **R1-F7** (no "262 passed" figure) — rejected: false premise (verify-logs:17); withdrawn by its own advocate.
- **R1-F4** (CHANGELOG sentence "authorized by reflection") — rejected: a pre-execution reflection is not an accepted authority source (taxonomy:28-36) and F3 did not ask for the sentence.

## Risk Summary

All changes are classification and annotation edits; none changes an AC verdict or the "no regression" conclusion. Rollback: use variant-2-original.md.
