# Diff Analysis: reviewer-card comparison (sc:reflect Wave 4, UC-1 pre)

## Metadata

- Generated: 2026-11-03T00:05:00Z
- Variants compared: 3 (variant-1 = reviewer 1 analyzer/sonnet, variant-2 = reviewer 2 qa/glm-5.3, variant-3 = reviewer 3 refactorer/opus)
- Plan under review: `.dev/tasks/to-do/TASK-WF-workflowSource-20261102-233731/TASK-WF-workflowSource-20261102-233731.md` (spec `source.md` in the same folder)
- Focus: correctness, coverage, deviation-classification
- Total differences found: 13 debate points (structural 2, content 7, contradictions 2, shared assumptions 2) plus 13 unique contributions
- Note: inputs are YAML cards copied as `.md` (non-markdown warning logged; proceeding)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 | Granularity | 11 findings, broad sweep incl. guide-template and sub-item audits | 6 findings, coverage-focused | 10 findings, ordering/sequencing-focused | Low |
| S-002 | "No-change" findings | R1-F11 records verified-consistent ground facts (authorized) | none | R3-F8 (necessary) and R3-F10 (authorized) record non-deviations | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| C-001 | Missing closing verification (smoke pytest + `make test`, source.md:47-50) | R1-F1 drift, blocking; add final task or Constraint | R2-F1 drift, blocking; adds evidence executor will not run tests (`src/superclaude/commands/implement.md:11`) | R3-F1 drift, blocking; add Task 67 + smoke run in Task 26 AC | Low (same verdict; different remedy) |
| C-002 | A-W22 #9 codegraph.md backlink targets (Task 17) | R1-F3 drift, minor | R2-F2 drift, minor | R3-F2 drift, minor | Low |
| C-003 | B-W22 #6 git-standards section-6 pointer | listed inside R1-F9 as a grounding-gap sub-item | R2-F3 drift, minor | R3-F3 drift, minor | Medium (classification differs) |
| C-004 | B-W12 #6 four-note links / Task 37 runs before Tasks 43-46 | R1-F8 grounding-gap (dependency) | R2-F4 drift | R3-F4 drift | Medium (classification differs) |
| C-005 | Dependency declarations / forward links (Tasks 4, 13, 47, 66) | R1-F8 grounding-gap | (only via R2-F4) | R3-F5 drift | Medium (classification differs) |
| C-006 | Out-of-scope rules not restated (report/manifest, no issue filing) | R1-F10 grounding-gap | R2-F6 drift; CONSOLIDATED-PLAN.md:636 tells executor to file issues | not raised | Medium |
| C-007 | Markdownlint constraint | R1-F5 drift: "record pre-existing violations" relaxation conflicts with pre-commit `--fix`; pin itself correct | no finding (pin matches pre-commit) | R3-F8 necessary: pin matches pre-commit | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|---|---|---|---|---|
| X-001 | Taxonomy class for plan ordering/omission defects (C-003..C-005) | grounding-gap ("risk, not a contradiction", R1-F8/F9) | drift (R2-F3, R2-F4) | drift (R3-F3, R3-F4, R3-F5) | Medium |
| X-002 | Whether the plan's markdownlint constraint deviates from the spec | drift (R1-F5) | no deviation (self-audit: authorized under "per repo config") | necessary deviation (R3-F8) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | 1 | R1-F2: Task 39 AC (grep for `--custom-prompt-dir` returns nothing) contradicts item B-W15.3, which tells the writer to say the flag is planned | High |
| U-002 | 1 | R1-F4: removal-grep ACs (Tasks 13, 27, 28, 29) conflict with docs that truthfully say "X does not exist" | Medium |
| U-003 | 1 | R1-F5: pre-commit markdownlint `--fix` rewrites whole staged files | Medium |
| U-004 | 1 | R1-F6: plan drops the Tier A/B/C grouping and template header fields for guides | Medium |
| U-005 | 1 | R1-F7: Task 65 hardcodes `python3 -m http.server` (UV-only rule); `_fetch` likely accepts `file://` | Low |
| U-006 | 1 | R1-F9: numbered sub-items of items not pinned in task text/AC | Medium |
| U-007 | 2 | R2-F1: `/sc:implement` treats tests as extras (implement.md:11), so the final `make test` belongs to nothing | High |
| U-008 | 2 | R2-F5: "53/53" count is wrong; 66 deliverables | Low |
| U-009 | 2 | R2-F6: CONSOLIDATED-PLAN.md:636 instructs issue filing, which the executor reads | Medium |
| U-010 | 3 | R3-F6: Task 42 paraphrases B-W18 (worktree vs `git stash push`) | Medium |
| U-011 | 3 | R3-F7: Task 47 adds index links not requested by B-W13 | Low |
| U-012 | 3 | R3-F9: sync-dev does not cover `core/` or `rules/` (verify-sync half uncited) | Medium |
| U-013 | 3 | R3-F10: Tasks 3 and 4 both add a README upgrading link | Low |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | C-001 (all three recommend adding a verification task or Constraint) | A workflow plan may contain a verification-only task | CONTRADICTED: `~/.claude/skills/sc-workflow-protocol/refs/quality-gates.md:22` "Final verification belongs to the executor: no status field, no checkbox, no verification-only task" | yes (flag) |
| A-002 | All recommendations are phrased as plan edits | The plan may be edited after this advisory review | UNSTATED; `/sc:workflow` Wave 4 says reflect is advisory and "never edit, delete, or regenerate `<id>.md` from findings" | yes |
| A-003 | V1 and V3 note sequential safety | `/sc:implement` executes tasks in listed order | STATED (R1-F8, R3-F5) | no |
| A-004 | All accept CONSOLIDATED-PLAN items as ground truth | Item evidence is correct | STATED in self-audits (not re-verified) | no |

Promoted:

| # | Assumption | Impact | Status |
|---|---|---|---|
| A-001 | Verification-only task is allowed | Recommendation "add Task 67" would fail the workflow gate; remedy must be an AC addition or executor/orchestrator action | CONTRADICTED, debate |
| A-002 | Plan is editable post-review | All remedies must route to the executor run or the post-release orchestrator, not to `<id>.md` | UNSTATED, debate |

## Summary

- Structural differences: 2; content differences: 7; contradictions: 2; unique contributions: 13; shared assumptions: 4 (UNSTATED 1, STATED 2, CONTRADICTED 1)
- Highest-severity items: C-001 (blocking in all variants), U-001, U-007, A-001
- Taxonomy tags: L1 = S-001, S-002; L2 = C-002, C-003, C-004, C-005, C-006, X-001; L3 = C-001 (verification gate), C-007 (validation rule), X-002, A-001, A-002 (guard/invariant)
- Similarity check: differences exceed 10% of comparable items; debate proceeds
