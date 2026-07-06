# Diff Analysis: Delegate-to-reflect vs Keep-bespoke (single-proposition, 3 positions)

## Metadata
- Generated: 2026-06-04
- Variants: V1 (PRO delegate/consolidate) · V2 (ANTI keep bespoke) · V3 (CONDITIONAL rubric)
- Proposition: remove bespoke validators (auggie-reviewer, audit-validator), delegate to /sc:reflect, as a pattern for these two + all future protocols.
- Categories: content (4), contradictions (4), unique (3), shared assumptions (4)

## Content Differences
| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | Default stance for all future protocols | Always delegate | Never delegate | Delegate iff 4 gates pass | High |
| C-002 | Are bespoke validators subsets of reflect? | Yes (reflect is superset) | No (different jobs: blind recall, classification, dynamic-loading) | Sometimes (depends on protocol) | High |
| C-003 | Maintenance model | One shared contract (DRY) | N independent validators (fault isolation) | Per-protocol decision, recorded | Medium |
| C-004 | Treatment of the two named targets | Delegate both | Keep both | Keep both (G1/G2/G3 fail) | Medium |

## Contradictions
| # | Conflict | V1 | V2 | V3 | Impact |
|---|---|---|---|---|---|
| X-001 | Is consolidation a maintenance win or a coupling liability? | Win (one surface) | Liability (one reflect change breaks N protocols) | Both — net depends on protocol count passing the rubric | High |
| X-002 | Does delegating preserve the bespoke validator's value? | Yes (reflect reuses audit-validator) | No (loses blind recall; circular for audit) | Only if G3 passes | High |
| X-003 | Is "one universal validator" rigor or monoculture? | Rigor (superset mechanisms) | Monoculture (correlated framework-wide blind spots) | Risk to weigh in G-gates | High |
| X-004 | Is output-type cleanly classifiable per protocol? | Implied yes | Implied (review≠applied work, clear) | Explicit G1 test — assumes decidable | Medium |

## Unique Contributions
| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V2 | Framework-level *monoculture / correlated-failure* argument against a single universal validator | High |
| U-002 | V3 | The 4-gate rubric (G1 input-type · G2 no circular reuse · G3 property preservation · G4 cost-vs-stakes) as the decision procedure for "all future protocols" | High |
| U-003 | V2 | "Bespoke validators do *different jobs*" — blind recall ≠ deviation audit ≠ citation gate | High |

## Shared Assumptions
| A-NNN | Assumption | Classification | Promoted |
|---|---|---|---|
| A-001 | A protocol's output type ("applied work" vs "human-gated recommendation") is cleanly and stably decidable | UNSTATED | YES |
| A-002 | Reflect's contract/capabilities are stable enough to be a dependency for N protocols (it was modified *today*) | UNSTATED | YES |
| A-003 | Something validates reflect itself; delegating "all" verification to reflect does not create an unvalidated meta-validator (who watches the watcher?) | UNSTATED | YES |
| A-004 | The cost figures (reflect 35–70k; bespoke ~cheap) are accurate and stable across protocol types | STATED (V1/V2/V3 all cite `context.md` §4.1) | NO |

### Promoted [SHARED-ASSUMPTION] points
| # | Assumption | Impact | Status |
|---|---|---|---|
| A-001 | output-type cleanly decidable | If a protocol's output is *mixed* (sometimes applied, sometimes advisory), G1 is undecidable and the rubric (and both blanket rules) misfire | UNSTATED → probe |
| A-002 | reflect stable enough as universal dependency | A moving-target validator under N protocols = correlated breakage on every reflect change | UNSTATED → probe |
| A-003 | reflect-as-universal-validator is itself validated | Delegating *all* verification to one skill leaves that skill's own output unverified by anything independent — meta-monoculture | UNSTATED → probe (highest-value) |

## Summary
- content 4 · contradictions 4 · unique 3 · shared assumptions 4 (UNSTATED 3, STATED 1)
- Highest-severity: C-001, C-002, X-001, X-002, X-003, U-001, U-002, U-003, A-003
- **Live tension:** V1 vs V2 is a genuine blanket-policy clash; V3 claims to dissolve it with a rubric. The "all future protocols" scope makes the *meta* questions (monoculture A-003, decidability A-001, dependency-stability A-002) the load-bearing ones — not the per-target verdict (which all three roughly agree lands on "keep" for auggie-review and cleanup-audit).
