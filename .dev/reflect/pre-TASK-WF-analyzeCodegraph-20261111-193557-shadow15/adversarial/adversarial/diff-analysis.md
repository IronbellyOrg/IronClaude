# Diff Analysis: reflect-pre findings cards (shadow15) — 3-variant comparison

## Metadata

- Generated: 2026-11-13T02:5x Z (session time)
- Variants compared: 3
  - V1 = variant-1-original.md — persona analyzer, model_class sonnet (claude-sonnet-5-5)
  - V2 = variant-2-original.md — persona qa, model_class haiku (claude-haiku-5-5, observed claude-gw-tier1b[1m])
  - V3 = variant-3-original.md — persona refactorer, model_class opus (claude-opus-5-5, observed claude-gw-tier1b[1m])
- Total differences found: 17
- Categories: structural (5), content (6), contradictions (4), unique (4), shared assumptions (2)
- Adjudication evidence beyond the cards: tasklist + spec (Read this session), `src/superclaude/commands/analyze.md` at HEAD and at execution commit 7764bb623 (`git show`), `src/superclaude/core/CODEGRAPH.md`, `t1-card.md`, reviewer briefs. Per the tasking note, analyze.md evolved after the package executed (PR #513 wording tightening = commit 930c5ebc8; PR #515 mcp grants — did not touch analyze.md), so findings are judged against the execution commit where attribution matters.

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|------|----|----|----|----------|
| S-001 | Frontmatter completeness | persona/model only | + `model_observed` | + `model_observed` | Low |
| S-002 | Findings count | 3 | 4 | 3 | Low |
| S-003 | Category spread | missing-requirement ×2, other ×1 | missing-requirement ×2, unpassable-check ×2 | other ×3 | Medium |
| S-004 | Refs anchoring style | spec R-IDs (R2, R7) | spec R-IDs (R2, R5, R7) | t1-card inference IDs (INF-005, INF-012) | Medium |
| S-005 | Citation stratum | spec + tasklist | spec + tasklist | shipped artifacts (analyze.md) + guide (CODEGRAPH.md) | Medium |

S-003/S-005 note: the three lenses are nearly disjoint on evidence stratum — V1/V2 audit the plan-vs-spec contract; V3 audits the shipped-artifact-vs-guide duplication. Only V2 audits AC falsifiability.

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|-------|----|----|----|----------|
| C-001 | R7 sub-ban AC coverage | F1: symbolsOnly ban has no AC (usage text only) | F2: verb ban AC'd, symbolsOnly + wildcard not; also 25-line cap + return-contract | (absent) | Medium |
| C-002 | Spec §2.4 items 3/6 coverage | (absent) | F1: "no tasklist AC and no visible matrix row" | (absent) | High |
| C-003 | Discover step conformance | F2: shipped Discover = unplanned elaboration | (absent) | (absent) | High |
| C-004 | AC falsifiability | (absent) | F3 + F4: escape-clause / unbounded-exception ACs | (absent) | Medium |
| C-005 | R2 access:mcp gate | F3: gate in R2 and shipped file, absent from all ACs | (absent) | (absent) | Medium |
| C-006 | Guide-vs-command duplication | (absent) | (absent) | F1 verb list, F2 60s wait, F3 dense bullet | Medium |

## Contradictions

| # | Point of Conflict | Position A | Position B | Impact |
|---|-------------------|-----------|-----------|--------|
| X-001 | What produced the Discover elaboration (`path` param, symbolsOnly on main files, search-only-when-symbol) | V1-F2: executor's "mild unplanned elaboration" vs tasklist | Git evidence: at 7764bb623 Discover matched the tasklist text verbatim; all three elaborations landed in 930c5ebc8 (PR #513, 2026-11-12, separate package) | High — misattribution |
| X-002 | "No visible matrix row" for §2.4 items 3/6 | V2-F1 claim vs its brief (summary row only) | t1-card.md INF-012 maps source.md:38-46 (items 3 and 6 included) to Task 1, containment, matched | High — factually false against the full matrix; vantage artifact |
| X-003 | Attribution of the 60s-wait restatement (analyze.md:30) | V3-F2: command restates guide rule, dropping the pgrep-allowlist condition | Git evidence: the 60s clause did not exist at 7764bb623; PR #513 added it. Also the current text says "(guide step 3)", pointing at the section that carries the condition | High — misattribution |
| X-004 | "return-contract.yaml unchanged (spec 2.5) has no AC" (V2-F2 clause) | No AC names it directly | Task 2 AC2 requires `## Unattended mode` byte-identical to HEAD, and the return-contract wording lives inside that section — transitively enforced | Medium — claim overstated |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | V2 | unpassable-check stratum: AC escape clauses (T3) and unbounded "intended additions" (T2) — the only falsifiability audit | High |
| U-002 | V1 | R2's `access: mcp` half-gate missing from every AC | Medium |
| U-003 | V3 | shipped-artifact ↔ guide duplication stratum (verb list, wait rule, dense bullet) | Medium (F1 stands; F2 falls on attribution; F3 weakened) |
| U-004 | V2 | 25-line soft cap has no AC (F2 residue) | Low |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|-----------|----------------|----------|
| A-001 | All three cards cite current-HEAD analyze.md as "the shipped" artifact with no temporal check | The audited package's output equals analyze.md at HEAD | UNSTATED (and CONTRADICTED for the clauses PR #513/#515 changed) | Yes — [SHARED-ASSUMPTION] |
| A-002 | No card escalates above MINOR/non-blocking; consistent with doc-only target | Doc-only command-file deviations cap at MINOR non-blocking | UNSTATED | Yes — [SHARED-ASSUMPTION] |

A-001 is the root cause of X-001 and X-003: every card assumed HEAD = execution output. A-002 is consistent with the t1-card kind-guard note (doc-only target, `implementation_coverage_pct: null`) and was not contested in debate.

## Summary

- Total structural differences: 5
- Total content differences: 6
- Total contradictions: 4 (three High: two misattributions X-001/X-003, one vantage artifact X-002; one Medium X-004)
- Total unique contributions: 4
- Total shared assumptions surfaced: 2 (UNSTATED: 2, STATED: 0, CONTRADICTED: 0 — A-001's contradiction is partial, affecting only post-PR-#513 clauses)
- Highest-severity items: X-001 (High), X-002 (High), X-003 (High), C-002/C-003 (High)
- Similarity check: differences far exceed 10% of comparable items — debate proceeds.
