# Diff Analysis: spec Comparison

## Metadata
- Generated: 2026-09-24T20:15:00Z
- Variants compared: 3 (V1 opus:architect, V2 sonnet:refactorer, V3 haiku:qa)
- Total differences found: 18
- Categories: structural (4), content (6), contradictions (4), unique (4), shared assumptions (4)

## Structural Differences

| # | Area | V1 architect | V2 refactorer | V3 qa | Severity |
|---|------|--------------|---------------|-------|----------|
| S-001 | Document organization | Numbered protocol sections + R-NNN in groups (invocation, architecture, enumeration, loop) | Flat R-001..R-020 + delete-table + loop sketch | Goal table + R-NNN each with AC-x.y Given/When/Then + E-* STOP catalog | Medium |
| S-002 | refs/ split | Three refs: task-enumeration, spec-compliance, ledger | At most one refs/spec-compliance.md; loop in SKILL.md | Three refs: intake, qa, ledger | Medium |
| S-003 | Command size / identity | Thin dispatcher ≤150; personas at most one per task | Rewrite in place; personas omitted; MCP frontmatter gone | Thin dispatcher; STOP codes as identity | Low |
| S-004 | Test seams | Falsify via grep + fixture run | Falsify via grep + protocol self-check | Explicit AC ids, ledger regex, halt-table tests, E-* codes | High |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|-------|----|----|----|----------|
| C-001 | Reviewer mode | `--reviewer auto\|inline\|subagent`; auto = inline if N≤3 else subagent | Inline if N≤3 AND source ≤400 lines; else one Task; no flag | Inline if N≤3 and not compacted; else one subagent; same schema; do not test executor identity | Medium |
| C-002 | Missing-AC handling | Fallback: whole body is AC; vague → cannot-verify; interactive wait one turn; non-interactive HALT | Item text is the AC; no E-NO-AC STOP | STOP E-NO-AC **before** any edit if no AC/Then/MUST/checkbox | High |
| C-003 | Extras order | Implement → extras → spec QA | Spec verdict first, extras after on same line | Extras after implement; never flip spec verdict | Medium |
| C-004 | Whole-list review | Skip when N=1; else optional | N=1 per-task IS the pass (do not run twice); optional if N>1 | Default ON; `--skip-final-review`; FINAL: lines do not rewrite per-task verdicts | Low |
| C-005 | Task cap | No hard cap in spec | No hard cap | Hard cap 20; E-TOO-MANY | Medium |
| C-006 | Verdict token | `spec-compliant` | `compliant` | `compliant` (forbids `spec compliant`) | Low |

## Contradictions

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|-------------------|----|----|----|--------|
| X-001 | MDTM input | STOP: "looks like MDTM, run /task" (redirect text, not auto-invoke) | Still execute via this protocol; do not hand off | Execute this protocol OR STOP E-WRONG-TOOL recommending /task — **no auto-handoff** | High |
| X-002 | Non-compliant proceed | One fix pass, then HALT; rulings for spec deviations | Fix **or** Ruling; no silent proceed | HALT unless three-field ruling (`what — why — cost-if-wrong`); complete only after ruling line; no `--force` without ruling | High |
| X-003 | Empty/vague AC | Fallback body as AC then cannot-verify/HALT | Requirement sentence is AC | Hard STOP E-NO-AC before implement | High |
| X-004 | MDTM vs phase-N tasklist | phase-N accepted; MDTM rejected | Both accepted as markdown; ignore MDTM ceremony | phase-N accepted; MDTM: this protocol or E-WRONG-TOOL | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V1 | `mcp__auggie__codebase-retrieval` once per task (warn, not STOP if down); task-start SHA on in-progress line | Medium |
| U-002 | V2 | Explicit delete-table for current implement.md (personas, MCP, pitch examples, "ready for /sc:test") | High |
| U-003 | V3 | Closed E-* STOP catalog; citation obligation (`path:line` or `Ti.ACk`); ledger corrupt STOP; `--force` invalid without ruling | High |
| U-004 | V3 | 20-task hard cap; `unrelated-red` extras vs touched-file-set | Medium |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | All variants | `/sc:implement` requires an existing spec/PRD/tasklist path; free-form pitch is invalid (hard cutover, no dual-mode) | STATED | no |
| A-002 | All variants | Primary per-task gate is spec compliance (Missing/Extra/Misunderstood vs AC+spec+instructions), not npm test | STATED | no |
| A-003 | All variants | Ledger is one markdown file at `.dev/implement/<slug>/progress.md`; resume = first non-complete; no `/task` 6-agent QA | STATED | no |
| A-004 | All variants | Thin command + `sc-implement-protocol`; `make lint-architecture` / `make sync-dev`; `.claude/` not SoT | STATED | no |
| A-005 | All variants | Spec is binding; silent extras in the diff are `extra`, not "nice to have" | STATED | no |
| A-006 | Implicit | Operator is present enough to write a three-field ruling or accept HALT — no fully unattended 20-task run without a human for non-compliant tasks | UNSTATED | yes |

Promoted [SHARED-ASSUMPTION]:

| # | Assumption | Impact | Status |
|---|------------|--------|--------|
| A-006 | Non-compliant tasks require a human (or a ledgered ruling written by the executor on the human's behalf). Unattended CI-style runs will HALT. | State/guard: loop cannot finish if AC is unmet and no ruling policy exists | [SHARED-ASSUMPTION] |

## Summary
- Total structural differences: 4
- Total content differences: 6
- Total contradictions: 4
- Total unique contributions: 4
- Total shared assumptions surfaced: 6 (UNSTATED: 1, STATED: 5, CONTRADICTED: 0)
- Highest-severity items: S-004, C-002, X-001, X-002, X-003, U-002, U-003, A-006
