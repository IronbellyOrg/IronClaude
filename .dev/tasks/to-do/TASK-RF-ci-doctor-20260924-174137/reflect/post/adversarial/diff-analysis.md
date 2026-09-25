# Diff Analysis: POST reviewer cards

## Metadata
- Generated: 2026-09-24T19:52:00Z
- Variants compared: 3
- Total differences found: 4
- Categories: structural (1), content (1), contradictions (1), unique (1), shared assumptions (1)

## Structural Differences

| # | Area | Variant 1 grok | Variant 2 deepseek | Variant 3 T1 | Severity |
|---|------|----------------|--------------------|--------------|----------|
| S-001 | Card shape | YAML findings list | YAML + suspected_hallucination | Markdown T1 card | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|-------|----|----|----|----------|
| C-001 | YAML hunk class | none / authorized insert | drift: install missing --no-promote | none + 3 Necessary protocol adaptations | High |

## Contradictions

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|-----------|----|----|----|--------|
| X-001 | Does `superclaude install` need `--no-promote`? | no finding | yes, Medium drift at test.yml:219 | no; --no-promote is reflect Wave 7 | High — V2 is suspect:true and contradicts install CLI |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | V3 T1 | Classifies diff-file POST, --no-promote, uncommitted tree as Necessary | High |

## Shared Assumptions

| # | Assumption | Classification | Promoted |
|---|------------|----------------|----------|
| A-001 | Doctor command remains `superclaude doctor --verbose` | STATED | no |

## Summary
- Highest-severity: X-001 (V2 hallucination vs install CLI)
