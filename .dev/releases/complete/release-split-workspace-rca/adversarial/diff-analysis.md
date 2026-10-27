# Diff Analysis — RCA Comparison

## Metadata
- Generated: 2026-05-08
- Variants compared: 3 (RCA #1 skill-spec, RCA #2 eval-harness, RCA #3 governance)
- Total differences found: 17 (S: 0, C: 5, X: 2, U: 7, A: 3)

## Structural Differences

All three RCAs followed the assigned section template (Method / Findings / Root Cause / Confidence / Refactor / Acceptance / Limitations). No structural divergence. (S-NNN: 0 entries.)

## Content Differences

| # | Topic | RCA #1 | RCA #2 | RCA #3 | Severity |
|---|---|---|---|---|---|
| C-001 | Cause attribution | Skill spec NOT the cause (negative claim) | Anthropic skill-creator plugin SKILL.md L167 | Governance gap (no documented rule + dormant detection) | High |
| C-002 | Layer of action | SuperClaude skill spec | Anthropic plugin (vendored) | Project governance / CI / docs | High |
| C-003 | Nature of finding | Self-declared dead-end | Smoking gun with file/line citation | Multi-symptom governance audit | Medium |
| C-004 | Refactor target | Defensive guards in skill | PreToolUse hook + CLAUDE.md addendum | 5-pronged governance fix (R1–R5) | High |
| C-005 | Recommended next pivot | "Defer to RCA #2" | "RCA #3 should investigate why commit was accepted" | "RCA #1 / #2 may carry more causal weight" | Low |

## Contradictions

| # | Point | RCA Position A | RCA Position B | Impact |
|---|---|---|---|---|
| X-001 | "Dominant cause" claim | RCA #2: plugin is dominant cause | RCA #3: governance is dominant cause | Medium — resolved by layered framing (proximate vs systemic) |
| X-002 | Whether `.dev/eval-workspaces/` is the right destination | RCA #1, RCA #2 assume yes | RCA #3 notes it diverges from prior art at `.dev/releases/complete/v2.15-cli-portify/` | Low — flagged for documentation decision in L2.4 |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | RCA #1 | Output-path safety gate at skill Prerequisites (refuse `.claude/skills/...` outputs) | Medium (defense in depth) |
| U-002 | RCA #2 | Smoking-gun citation: skill-creator SKILL.md L167 mechanically requires `<skill-name>-workspace/` sibling | **High** |
| U-003 | RCA #2 | PreToolUse hook proposal — only enforcement that doesn't rely on Claude obedience | **High** |
| U-004 | RCA #2 | argparse audit proving no flag/env-var override exists in upstream harness | High |
| U-005 | RCA #3 | Identification that `verify-sync`'s error message misleads ("not distributable!" → wrong fix) | **High** |
| U-006 | RCA #3 | CI gap: no workflow runs `verify-sync` or `lint-architecture` | **High** |
| U-007 | RCA #3 | Broken CLAUDE.md pointers to PLANNING.md/TASK.md/KNOWLEDGE.md | Medium (governance corrosion) |

## Shared Assumptions

| # | Assumption | Source Agreement | Classification | Promoted |
|---|---|---|---|---|
| A-001 | `.dev/eval-workspaces/<skill-name>/` is the correct destination | All three | UNSTATED — but RCA #3 noted divergence from prior art | YES (informs L2.4 in merged plan) |
| A-002 | The fix should target the IronClaude project, not the upstream Anthropic plugin | All three (plugin is "vendored", outside project's modification scope per RCA #2 §Refactor proposal) | UNSTATED but reasonable | NO — adopted as constraint |
| A-003 | This eval-workspace pattern will recur for other skills | RCA #2 (Option D explicitly generalizes), RCA #3 (R4 blocklist generalizes) | STATED | NO — already addressed in L1.1 + L2.3 |

## Summary

- Total content differences: 5
- Total contradictions: 2 (one resolved by layering, one flagged for documentation)
- Total unique contributions: 7 (5 of high value)
- Total shared assumptions: 3 (1 promoted to action item)
- Highest-severity items: U-002, U-003, U-005, U-006 (all four foundation pieces of the merged fix)
