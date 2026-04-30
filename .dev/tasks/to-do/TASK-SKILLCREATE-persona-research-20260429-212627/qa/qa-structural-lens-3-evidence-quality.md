# QA Report — Skillcreate Evidence Quality (Lens 3 of 6)

**Topic:** sc-persona-research-protocol SKILL.md
**Date:** 2026-04-30
**Phase:** skillcreate-evidence-quality
**Lens:** evidence-quality
**Fix authorization:** false (REPORT ONLY)

## Overall Verdict: FAIL

## Items Reviewed

| # | Check | Result |
|---|-------|--------|
| 1 | Evidence citation validity (cited paths exist) | FAIL — 2 cited research files do not exist (wrong filenames). |
| 2 | No hallucinated file paths (parents exist) | FAIL — folder naming inconsistency (archetypes/ vs archetype-proposals/) — at least one set of references will fail at runtime. |
| 3 | Claim substantiation | PASS — spec citations trace correctly with at most ±1 line drift. |
| 4 | Documentation staleness tags | FAIL — only 11 occurrences of any verification tag across 1861 lines; spec-sourced claims appear as bare parentheticals not [SPEC-FR-N] tags. |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | CRITICAL | SKILL.md:1352 | References non-existent file `09-spec-part3-ethics-archetype-schema.md`. Actual file is `09-spec-part3-ethics-acceptance-archetype-schema.md`. | Rename citation to match actual filename. |
| 2 | IMPORTANT | SKILL.md:1498-1499 | References non-existent `02-tech-research-analysis.md`. Actual file is `02-reference-tech-research.md`. | Replace with `02-reference-tech-research.md`. |
| 3 | CRITICAL | Lines 46/176/335 vs 606/865/964/982/1805 | Folder naming inconsistency: Variable Reference + Output Locations + folder-creation use `archetypes/`, but Discovery Worker output (line 865) and Aggregator input (line 964) reference `archetype-proposals/`. Runtime task folder will be one of these names; the other set will dangle. | Pick one canonical name (recommend `archetype-proposals/` since used in worker output paths) and replace all instances uniformly across S4/S9/S20/S28. |
| 4 | IMPORTANT | Body throughout | Documentation-staleness tagging defined in S23 #12 / S26 Rule 5 but not applied. Hundreds of spec-sourced claims appear as bare "(FR-8)" rather than [SPEC-FR-8]. | Apply [SPEC-FR-N] inline OR add explicit S26 exception that "(FR-N)" parenthetical citation subsumes the tag. |
| 5 | MINOR | SKILL.md:56 | "spec §3, lines 80-156" — actual schema content runs L80-114. | Tighten to "lines 80-114" or "§3 Inputs". |

## Confidence: 100% | Tool engagement: Read=4, Grep=9, Bash=9

## QA Complete
