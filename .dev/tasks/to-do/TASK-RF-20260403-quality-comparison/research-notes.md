# Research Notes: Pipeline Quality Comparison — PRD/TDD vs Spec-Only Baseline

**Date:** 2026-04-03
**Scenario:** A (Explicit — build request has 8 dimensions, exact paths, phases)
**Depth Tier:** Standard (comparison task reading existing artifacts, 3 result directories)
**Track Count:** 1

---

## EXISTING_FILES

### Result Directories (ALL EXIST — DO NOT REGENERATE)
- `.dev/test-fixtures/results/test3-spec-baseline/` — 18 .md files, extraction (302 lines), roadmap (380 lines), tasklist-index (66 lines) + 5 phase files
- `.dev/test-fixtures/results/test2-spec-prd-v2/` — 9 .md files, extraction (247 lines), roadmap (558 lines), NO tasklist yet
- `.dev/test-fixtures/results/test1-tdd-prd-v2/` — 13 .md files, extraction (660 lines), roadmap (746 lines), tasklist-index (219 lines) + 3 phase files

### Key Artifacts Per Run

| Artifact | Run A (Baseline) | Run B (Spec+PRD) | Run C (TDD+PRD) |
|----------|-----------------|------------------|-----------------|
| extraction.md | 302 lines | 247 lines | 660 lines |
| roadmap.md | 380 lines | 558 lines | 746 lines |
| anti-instinct-audit.md | EXISTS | EXISTS | EXISTS |
| tasklist-index.md | EXISTS (66 lines) | MISSING | EXISTS (219 lines) |
| phase-*-tasklist.md | 5 files | MISSING | 3 files |
| tasklist-fidelity.md | EXISTS | MISSING | NOT YET (validation hasn't run on v2 yet) |
| spec-fidelity.md | CHECK | MISSING (anti-instinct halt) | MISSING (anti-instinct halt) |
| test-strategy.md | CHECK | MISSING (anti-instinct halt) | MISSING (anti-instinct halt) |

## PATTERNS_AND_CONVENTIONS

- This is a READ-ONLY comparison task — no code modifications, no pipeline runs
- All metrics use grep -c, wc -l, and YAML field reads against existing .md files
- QA should verify metric accuracy against actual files, not report prose

## GAPS_AND_QUESTIONS

1. Run B (Spec+PRD) has no tasklist — Dimension 7 (Tasklist Generation) will have N/A for Run B
2. spec-fidelity.md and test-strategy.md may not exist in any run (anti-instinct halts all pipelines) — Dimensions 4 and 5 may be entirely N/A
3. tasklist-fidelity.md may not exist in the v2 directories (validation hasn't run with real tasklists in the latest runs yet)

## RECOMMENDED_OUTPUTS

| # | Researcher Topic | Output File |
|---|-----------------|-------------|
| 01 | Run A Artifact Inventory | research/01-run-a-inventory.md |
| 02 | Run B Artifact Inventory | research/02-run-b-inventory.md |
| 03 | Run C Artifact Inventory | research/03-run-c-inventory.md |
| 04 | Template & Comparison Patterns | research/04-template-patterns.md |

## SUGGESTED_PHASES

- Researcher 1: Inventory Run A (baseline) — all artifacts, frontmatter values, line counts, key content
- Researcher 2: Inventory Run B (spec+PRD) — same
- Researcher 3: Inventory Run C (TDD+PRD) — same
- Researcher 4: Template patterns — MDTM template 02, prior comparison report examples

## TEMPLATE_NOTES

Template 02. Task reads existing artifacts and produces comparison reports.

## AMBIGUITIES_FOR_USER

None — the build request specifies all 8 dimensions with exact metrics and grep patterns.

**Status:** Complete
