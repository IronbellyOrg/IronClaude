# Diff Analysis: Task 11 token-gap proposals

## Metadata
- Variants: 3 (V1 opus:architect, V2 sonnet:analyzer, V3 haiku:scribe)
- Categories: structural (3), content (6), contradictions (3), unique (3), shared assumptions (2)

## Structural Differences
| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Verdict | REMEDIATE (seal) | HYBRID (3 fix + 7 accept) | ACCEPT all | High |
| S-002 | Organising principle | section hash + sealed/unsealed register | publish-path class | acceptance criteria met + compensating controls | Medium |
| S-003 | Ruling text | none | ruling for accepted 7 | ruling for all 10 | Low |

## Content Differences
| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | G2 consequence scope | seal | fix (High) | accept, neighbours hold | High |
| C-002 | G7 rubric cap | seal | fix (Med-High) | accept (concedes weak) | Medium |
| C-003 | G9 head-object fallback | seal | fix (Medium) | accept, grounding copy holds | Medium |
| C-004 | G3 jq-absent status | seal (Low) | accept | accept (concedes weak) | Medium |
| C-005 | G10 drop vs downgrade | seal (Medium) | accept (line 22 byte-identity) | accept | Low |
| C-006 | Stopping rule | UNSEALED register + move-to-SEALS | publish-path probe has zero survivors | 4-part done, synonyms recorded not needled | Medium |

## Contradictions
| # | Point | Positions | Impact |
|---|---|---|---|
| X-001 | G5 backstop | V3: J13 covers it. V2/V1: J13 is PR-mode only, explicit --diff not covered | High (V3 factually wrong) |
| X-002 | G4 backstop | V3: J17. V2: asserted Output Format and in_diff:false sentences. J17 only checks tag ids are unmerged defects | Medium |
| X-003 | G10 severity | V1: Medium (status flips). V2/V3: Low (line 22) | Medium |

## Unique Contributions
| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V1 | Heading register: every heading sealed or listed UNSEALED, test-enforced | Medium |
| U-002 | V2 | Publish-path class as a finite scope; G0 (A1-A7 Condition cells unasserted) | High |
| U-003 | V3 | Never-accept list; honest concessions per gap | Medium |

## Shared Assumptions
| A-NNN | Assumption | Classification |
|---|---|---|
| A-001 | Probed survivors approximate what the next reviewer will find | UNSTATED |
| A-002 | Task 12 oracle and Task 13 will actually run before merge | STATED (plan) but unenforced for this decision |

## Summary
Structural 3, content 6, contradictions 3, unique 3, shared assumptions 2. Highest severity: S-001, C-001, X-001.
