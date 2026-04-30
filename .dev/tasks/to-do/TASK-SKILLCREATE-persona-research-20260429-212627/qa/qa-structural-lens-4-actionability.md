# QA Report — Actionability Lens (Lens 4 of 6)

**Topic:** sc-persona-research-protocol SKILL.md
**Date:** 2026-04-30
**Phase:** skillcreate-actionability
**Fix authorization:** false (REPORT ONLY)

## Overall Verdict: FAIL

The SKILL.md is substantially actionable — 15 agent prompts each have inlined inputs, named subagent_types, output paths, and verbatim protocol blocks — but 2 IMPORTANT actionability requirements are not met.

## Items Reviewed

| # | Check | Result |
|---|-------|--------|
| 1 | Agent prompt actionability (15 prompts: 6 domain + 6 lens + 3 fidelity) | PASS — all prompts have inlined inputs, sequencing, model, output paths; all 4 protocol blocks embedded. Discovery Worker (lines 858-948) is exemplary with inline grep targets. |
| 2 | Validation criteria testability (S25) | FAIL — see issues 1, 2, 3. |
| 3 | Content rules specificity (S26 ≥4 domain rows) | PARTIAL PASS — 4 unambiguous domain rows (rows 7-10), exactly meets floor. |
| 4 | Critical Rules 23-28 relevance | PASS — all 6 expected failure modes mapped (FR-6 disclaimer, FR-2 identity gate, FR-7 quotes, FR-22 generic-purity, FR-25 Tavily, FR-24/26 Opus cap). |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | S25.3 line 1655 (NO_FIRST_PERSON_ATTRIBUTION) | Says "regex for `<Name> said` / `<Name>:` patterns" but `<Name>` is a meta-placeholder, not runnable regex. | Replace with concrete regex: `grep -nE '\b[A-Z][a-z]+ (said\|stated\|wrote\|tweeted)\s+["“]'` and `grep -nE '\b[A-Z][a-z]+:\s+["“]'`. |
| 2 | IMPORTANT | S25.3 line 1656 (ARCHETYPE_GENERIC_PURITY) | Linter check described in prose but not encoded as runnable rule list. Discovery Worker prompt (L916-921) has it; S25 does not. | Add sub-checklist of grep rules under §25.3, mirroring L916-921. Cross-reference Discovery Worker prompt as authoritative implementation. |
| 3 | MINOR | S25.2 FR-7 line 1628 | Same `<Name>` meta-placeholder issue as Issue #1. | Use same concrete regex. |
| 4 | MINOR | S26 row 6 ("Don't fabricate") | Borderline boilerplate-vs-domain. Strict count of unambiguous domain rows is 4 — meets floor with no margin. | Add 11th row covering FR-25 Tavily routing or FR-8 no-auto-write. |

## Confidence: 100% | Tool engagement: Read=3, Grep=1, Bash=1

## QA Complete
