# Diff Analysis: Bash Batching Policy and Risk Register

## Metadata

- Mode: compare existing artifacts
- Depth: quick fallback after standard orchestration failed validation
- Focus: policy-soundness, risk-coverage
- Variants: `POLICY.md`, `RISK-REGISTER.md`
- Relationship: complementary artifacts, not competing specifications

## Structural Differences

| ID | Area | Policy | Risk register | Severity |
|---|---|---|---|---|
| S-001 | Purpose | Normative operating rule | Adversarial failure catalogue | Low |
| S-002 | Enforcement | Prompt/tasklist guidance plus optional hook | Evaluates whether controls are enforceable | High |
| S-003 | Runtime contract | Defines script lifecycle, markers, bounds | Tests lifecycle, markers, bounds | High |

## Content Differences

| ID | Topic | Policy position | Risk-register position | Severity |
|---|---|---|---|---|
| C-001 | Threshold | `N=4`, trigger on fifth eligible serial call | Threshold is gameable and must remain advisory | Medium |
| C-002 | Interactivity | Batch only pre-known independent reads | Frozen plans remain a high-likelihood risk | High |
| C-003 | Failure behavior | Continue-and-report, setup fail-fast | Supports this choice but requires explicit aggregate exit | High |
| C-004 | `bypassPermissions` | Inline visibility and command classification | Visibility is audit evidence, not a gate | High |
| C-005 | Hook | Optional advisory counter | False positives and semantic blindness dominate CPU cost | High |
| C-006 | `/tmp` | Private same-call lifecycle | Forced-kill cleanup and wrapper bypass remain | High |
| C-007 | Resource bounds | Count/runtime/output caps | Predicted caps are insufficient unless enforced | High |

## Contradictions

| ID | Conflict | Initial policy | Risk/adversarial position | Resolution |
|---|---|---|---|---|
| X-001 | Mechanical versus semantic streak | Hook reset on non-Bash; policy ignored cosmetic splits | One metric cannot prove the other | Policy now labels hook as proxy and measures both populations |
| X-002 | Parallel calls | Preferred parallelism but standing rule could include it | Same-turn parallel calls already avoid RTT | Explicit exemption added |
| X-003 | Aggregate rc | Footer specified without explicit `exit` mapping | `echo BATCH_FAIL` can still exit 0 | Explicit exit 0/1 and marker accounting added |
| X-004 | One script versus 15-command cap | Exactly one script, but long wave needs chunks | Contract ambiguous | One script per chunk plus checkpoint added |
| X-005 | Network/recursive scope | Bounded examples conflicted with split rule | Eligibility unclear | Routine batches now exclude network/remote/recursive/streaming work |
| X-006 | Enforcement wording | Called prompt guidance enforceable | No runtime Bash gate exists | Status and enforcement wording downgraded to normative guidance |

## Unique Contributions

| ID | Source | Contribution | Value |
|---|---|---|---|
| U-001 | Policy | Empirical `N=4` threshold and prospective trigger | High |
| U-002 | Policy | Three-question state-dependency test | High |
| U-003 | Policy | Per-command marker and lifecycle contract | High |
| U-004 | Risk register | R7→R4→R10 wrapper-bypass failure chain | High |
| U-005 | Risk register | Multiple alternative mitigations per risk | High |
| U-006 | Invariant probe | Aggregate-exit, parallel-call, and chunk-boundary defects | High |

## Shared Assumptions

| ID | Assumption | Classification | Outcome |
|---|---|---|---|
| A-001 | Agent round trips dominate local read execution | STATED | Supported by incident data |
| A-002 | Read-only effect can be recognized reliably from prompt text | UNSTATED | Rejected as a security guarantee; restricted subset and residual risk documented |
| A-003 | Human approval is absent for some agents | STATED | Policy treats visibility as audit only |
| A-004 | Hook counters can only approximate semantic intent | STATED | Advisory proxy only |

## Summary

The documents agree on the optimization opportunity, `N=4`, read/write separation, continue-and-report semantics, and rejection of a hard counter. High-severity differences concern whether prompt policy is enforcement, whether resource limits are real, and whether unattended `bypassPermissions` execution can safely accept free-form shell. Those findings drove the merged changes.
