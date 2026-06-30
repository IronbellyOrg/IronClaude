# Diff Analysis: Family-B Prose Decision

## Metadata

- Variants compared: 3
- Focus: correctness, scope discipline, risk of over-editing, task executability
- Evidence inputs:
  - `research/03-taskbuilder-clause-flip.md`
  - `qa/analyst-cross-validation-report.md`

## Structural Differences

| ID | Area | Variant A | Variant B | Variant C | Severity |
|----|------|-----------|-----------|-----------|----------|
| S-001 | Decision treatment | Resolves stale prose by edit | Defers to Open Question / operator acceptance | Ignores after CLI edit | High |
| S-002 | Scope | Family A + minimal descriptive Family-B claims | Family A only, explicit documentation | Family A only, no documentation | Medium |

## Content Differences

| ID | Topic | Variant A Approach | Variant B Approach | Variant C Approach | Severity |
|----|-------|--------------------|--------------------|--------------------|----------|
| C-001 | Correctness of task-builder prose after Step 3 | Removes claims known false after exclusion restore | Leaves false claims but documents residual risk | Leaves false claims silently | High |
| C-002 | Scope discipline | Slightly widens scope to avoid contradiction, with narrow guardrails | Strictly follows original R3 A-narrow + human acceptance | Strict literalism | High |
| C-003 | Task executability | Executor gets actionable edit and validation | Executor must halt/ask before Step 4 | Executor may ship contradiction | High |

## Contradictions

| ID | Conflict | Variant A | Variant B | Variant C | Impact |
|----|----------|-----------|-----------|-----------|--------|
| X-001 | Family-B prose says reflect skill no longer class-excludes, but Step 3 restores class exclusion | Eliminates contradiction by rewording blanket prose only | Keeps contradiction as accepted/documented risk | Keeps contradiction silently | High |
| X-002 | R3 clause-7 says A.10.7 byte-for-byte untouched, but cross-validation says Family-B prose is false post-R2 | Reconciles by preserving action, editing stale justification | Chooses clause-7 literalism and documents conflict | Chooses clause-7 literalism without documentation | High |

## Unique Contributions

| ID | Variant | Contribution | Value |
|----|---------|--------------|-------|
| U-001 | A | Separates PRE action from stale descriptive prose, preserving behavior while fixing truthfulness | High |
| U-002 | B | Respects human-decision/anti-auto-default discipline by requiring acceptance if not editing | Medium |
| U-003 | C | Fastest, narrowest implementation | Low |

## Shared Assumptions

| ID | Assumption | Classification | Promoted |
|----|------------|----------------|----------|
| A-001 | Step 3 will restore `sc-reflect-protocol` to executor-class exclusion | STATED | no |
| A-002 | PRE action remains orthogonal because no executor exists at PRE | STATED | no |
| A-003 | Silent false prose in task-builder is unacceptable for a high-confidence reduce task | UNSTATED | yes |

## Summary

- Highest-severity items: S-001, C-001, C-002, C-003, X-001, X-002
- Core tension: correctness vs scope discipline.
- Variant C is dominated because it neither fixes nor documents the contradiction.
