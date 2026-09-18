# Base Selection

## Decision

**Base:** `POLICY.md`
**Donor:** `RISK-REGISTER.md`

The artifacts are complementary. The policy is the correct base because the requested deliverable is an operating rule; the register supplies threats, mitigations, and residual-risk corrections.

## Qualitative Scoring

| Dimension | Policy | Risk register | Decision |
|---|---:|---:|---|
| Requested standing-rule coverage | 1.00 | 0.45 | Policy |
| Threshold specificity | 1.00 | 0.60 | Policy |
| Failure-contract specificity | 0.85 | 0.80 | Policy |
| Risk coverage | 0.70 | 1.00 | Risk register |
| Enforcement honesty | 0.55 initial / 0.90 merged | 0.95 | Donor corrections |
| Boundary/invariant coverage | 0.65 initial / 0.90 merged | 0.85 | Synthesis |

## Rationale

The base retained `N=4`, prospective triggering, read/write separation, state-dependency testing, and continue-and-report. The merge imported the register's strongest conclusions: prompt policy is not enforcement; unattended bypass execution needs stricter command grammar; resource limits must be mechanical; `/tmp` crash cleanup is incomplete; hook counts are proxies.

## Edge-Case Floor

The initial policy passed the edge-case floor but had 11 invariant findings. Ten were corrected in place. The remaining High residual is explicitly carried rather than hidden.
