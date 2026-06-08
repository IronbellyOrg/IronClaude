# Research Notes: Reflect-V3-Serena audit remediation

**Date:** 2026-06-03
**Scenario:** A (Explicit — sites pinpointed by the reflect audit + remediation-context.md)
**Depth Tier:** Quick (4 small fixes across ~5 files, single cohesive concern)
**Track Count:** 1

## EXISTING_FILES
- src/superclaude/skills/sc-reflect-protocol/SKILL.md (F-1 @432, F-2 @230)
- src/superclaude/skills/sc-reflect-protocol/refs/report-template.md (G-1 @14)
- .dev/eval-workspaces/sc-reflect/cases/serena-memory-retention/expected.yaml (F-1 fixture @21)
- .dev/eval-workspaces/sc-reflect/cases/serena-wave0-config/expected.yaml (F-2 fixture @20)
- .dev/eval-workspaces/sc-reflect/evals/evals.json (F-2 @527; G-2 ids 22/24)
- .dev/eval-workspaces/sc-reflect/grader.py (G-2 semantics @177-188, read-only ref)

## PATTERNS_AND_CONVENTIONS
See research/01-fix-sites-and-design.md §Conventions. Key: src→sync-dev→verify-sync; never stage .claude/; eval-workspace not sync-dev'd; all-rule markdownlint; preserve corrected-form guards + C2–C5 + colon degrade tokens.

## GAPS_AND_QUESTIONS
None blocking. G-2 fix-option choice (recommend regex_present).

## RECOMMENDED_OUTPUTS
research/01-fix-sites-and-design.md (DONE — verified current-state + fix design for all 4 findings).

## SUGGESTED_PHASES
5 phases (F-1, F-2, G-1, G-2 each with a per-phase rf-qa task-integrity gate; Phase 5 = final rf-qa structural + rf-qa-qualitative pair). Template 02.

## TEMPLATE_NOTES
Template 02 (multi-phase, per-phase QA gates, conditional sync-dev per file class). QA_GATE_REQUIREMENTS=PER_PHASE. TESTING_REQUIREMENTS=NONE (protocol markdown + eval workspace; verify-sync + all-rule markdownlint + eval JSON-validity + static-grep re-checks replace a pytest suite). VALIDATION_REQUIREMENTS=make verify-sync PASS + all-rule markdownlint clean + evals.json valid JSON + corrected-form guards still 0.

## AMBIGUITIES_FOR_USER
None — intent is clear from the reflect audit + remediation-context.md.
