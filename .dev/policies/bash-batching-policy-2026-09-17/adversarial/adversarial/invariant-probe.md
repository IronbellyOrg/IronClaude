# Invariant Probe Results

## Quick-Retry Fault-Finder Analysis

| ID | Category | Assumption | Initial status | Severity | Merge disposition |
|---|---|---|---|---|---|
| INV-001 | state/count | Mechanical hook streak equals semantic policy wave | UNADDRESSED | Medium | Hook relabeled proxy; dual metrics required |
| INV-002 | guard/state | Counter excludes writes and compliant batch calls | UNADDRESSED | Medium | Proxy limitations and separate batch-call recording added |
| INV-003 | count/evidence | Transcript elbow uses policy semantics | UNADDRESSED | Medium | Evidence provenance and metric mismatch disclosed |
| INV-004 | boundaries/interaction | Five parallel calls should be scripted | UNADDRESSED | Medium | Same-turn parallel calls exempted |
| INV-005 | boundaries | One script is compatible with 15-command chunks | UNADDRESSED | Low | One script per chunk plus checkpoint added |
| INV-006 | guard/failure | Footer alone propagates nonzero aggregate rc | UNADDRESSED | Medium | Explicit exit mapping and marker accounting added |
| INV-007 | interaction/security | Inline visibility is review under bypass | UNADDRESSED | High | Visibility downgraded to audit; simple-command subset added; residual remains |
| INV-008 | guard/lifecycle | Secure creation and crash cleanup are defined | UNADDRESSED | Low | `mktemp -d`, `umask 077`, cleanup failure, SIGKILL limitation added |
| INV-009 | measurement | Warning-rate denominator is defined | UNADDRESSED | Low | 15% of Bash calls specified |
| INV-010 | guard/eligibility | Network/recursive scope is consistent | UNADDRESSED | Low | Excluded from routine batches |
| INV-011 | boundaries/state | Judgment boundary requires plan change | UNADDRESSED | Low | Any interpret-before-next-action step now resets sequence |

## Summary

- Findings: 11
- Addressed by merge: 10
- Accepted residual: 1 High (`INV-007`)
- Convergence implication: policy can pass as an advisory latency rule, not as a mechanically enforced security policy.
