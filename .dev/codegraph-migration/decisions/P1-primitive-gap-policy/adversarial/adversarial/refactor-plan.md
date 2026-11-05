# Refactoring Plan

## Overview
- Base variant: Variant 1 (option-a.md)
- Incorporated: Variant 3 (option-c.md) triage rule; Variant 2 (option-b.md) edit-once caution; debate corrections
- Planned changes: 9
- Overall risk: Medium (two High-impact items, C6 and C7, which touch the reflect CLI contract)
- Output: `../merged-recommendation.md` (the `--output` folder). Process artifacts stay in this folder.

## Planned Changes

### Change #1: Triage first, delete where a Serena-free native path is already named (V3 U-005)
- Source: option-c.md paragraph 1; debate C-001 and C-008 (unanimous merge).
- Target: base "Phase 1 edits each load-bearing SYM/REF/DIAG/ALLOW row" (opening paragraph).
- Approach: insert. Before rewriting, classify each LB row as **delete** (the same step already names a Serena-free Read/Grep/Glob/auggie path; examples: troubleshoot SKILL.md:193 with the :194 Glob + Grep fallback; troubleshoot command :89; auggie-reviewer :36 "Read (or serena)") or **rewrite** (no fallback, the fallback is "skip", or the fallback itself calls Serena).
- Risk: Medium.

### Change #2: Floor phrased as tools, bounded by roster (X-003, A-002)
- Source: debate X-003 and A-002 (all advocates).
- Target: base bullets "symbol lookup" and "references / callers".
- Approach: replace. Replace "`rg -n -w <symbol>`" with "the `Grep` tool with a word-boundary pattern". State that inside closed read-only rosters (reflect-reviewer, troubleshoot-analyst, reuse-auditor) the floor is Read/Grep/Glob/auggie only and Bash is never added.
- Risk: Low.

### Change #3: Diagnostics only where Bash already exists (X-002, C-005)
- Source: debate X-002 (the A advocate conceded); reflect-reviewer.md:38, :129; test_diagnostic_worker_contract.py:17-39.
- Target: base "diagnostics" bullet.
- Approach: replace. The project linter/type-checker runs through Bash only in orchestrators whose `allowed-tools` already include Bash (reflect orchestrator chain step 5/5.5; sc-troubleshoot-protocol). reflect §6.1.1's safety envelope (timeout, output cap, denylist) carries over to the Bash verify call. Closed rosters drop `get_diagnostics_for_file` and the step says the orchestrator's verification leg covers it.
- Risk: Medium.

### Change #4: Roster rule (A-001, C-007)
- Source: debate A-001 (all QUALIFY with the same rule); C-007.
- Target: base `tools:` / `allowed-tools:` bullet.
- Approach: append. Every `tools:` / `allowed-tools:` line naming `mcp__serena__*` is treated as load-bearing whatever its inventory label (R001 and R019 are labelled DEC). It changes in the same commit as the skill body that drives that agent and as its pinning test (`tests/troubleshoot/test_diagnostic_worker_contract.py` TOOLS set; sc-troubleshoot SKILL.md:31 prose roster).
- Risk: Low.

### Change #5: Rewrite the "fallbacks" that are not Serena-free (V3 advocate finding)
- Source: debate (C advocate); reuse-auditor.md:131; validate-roadmap SKILL.md:320-349.
- Target: new bullet after the implementations bullet.
- Approach: insert. reuse-auditor:131 auggie-unavailable fallback becomes "Grep by capability tokens + skeleton grep". F4 (line 57) uses a Grep reference search. validate-roadmap Step 0.5 gets a Grep-definition floor (same 30-lookup cap, same INFORMATIONAL ONLY artifact), not "skip".
- Risk: Low.

### Change #6: reflect degrade rule: floor is normal evidence (A-004, C-009)
- Source: debate A-004 and C-009; contract.py:32-34; reflect SKILL.md:636, :1492.
- Target: base reflect bullet.
- Approach: replace. After Phase 1, Grep/Glob/Read evidence is the normal path and emits no `serena` degraded token. `"serena"` and `"serena:context-excluded"` leave `_DEGRADED_COMPONENTS_HALT_SET` and the §6.5 / §10 fallback rows, in the same commit as the chain rewrite, with the CLI fixtures (for example `fixtures/degraded_serena.yaml`) updated together. Correct the base's "already decided" claim: context.md does not record this as decided. If no other decision owns it, this decision does.
- Risk: High (CLI code + tests).

### Change #7: reflect contract and telemetry fields keep names, get constants (A-003 + V2 caution)
- Source: debate A-003; orchestrator check `ensemble.py:824`, 26 files under `tests/cli/reflect/`.
- Target: new sub-bullet under reflect.
- Approach: insert. Field names stay stable in Phase 1. Producers: `find_declaration_no_match` from a zero-hit Grep. Constants: `type_hierarchy_invoked: false` (step 4.5 deleted, already gated off with no degrade), `summarize_changes_invoked: false`, `serena_summary_corroboration: unavailable` (matches the ensemble.py:824 default), `references_extended_info_used: false`. Step 7 `search_deps` is skipped and the claim is marked `[INFERRED]`. Renaming waits for Phase 3 or the contract decision.
- Risk: High.

### Change #8: Ledger keyed by file plus step heading, with the Phase 3 tier order (C-002, U-001, U-002)
- Source: debate C-002 (C conceded line drift); base ledger paragraph.
- Target: base ledger paragraph.
- Approach: restructure. Columns: file, step heading or anchor (not a line number), former Serena tool, action (deleted / floor), floor used, contract fields touched. Location: the Phase 3 handoff under `.dev/codegraph-migration/`. Phase 3 inserts codegraph as a tier above the floor; the floor stays.
- Risk: Low.

### Change #9: Release and acceptance statement (C-003, C-004, X-001)
- Source: debate (unanimous).
- Target: base "For" paragraph; new "Acceptance" lines.
- Approach: append. Phase 1 does not depend on Phase 3's merge timing. Its acceptance check is zero `mcp__serena__` / Serena-step hits in primitives and the plugin mirror outside `.dev/`, and no primitive step names a tool absent from its own roster.
- Risk: Low.

## Changes NOT Being Made
| Diff point | Non-base approach | Rationale |
|------------|-------------------|-----------|
| C-001 / U-004 | V2: keep LB Serena steps until Phase 3 | X-001: the merge shape is not planned (context.md:13); the V2 advocate conceded. |
| C-002 | V3: no ledger, re-derive from primitive-usage.md | Line numbers go stale after Phase 1 edits; V3 conceded. |
| C-006 | V3: validate-roadmap Step 0.5 becomes a no-op | Silent capability loss when a Grep floor is cheap; V3 conceded. |
| C-009 | V3: rely on reflect's named fallback as-is | It emits `degraded: ["serena"]`, which is in the halt set (contract.py:33), so every run would halt. |

## Risk Summary
| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| 1-5, 8, 9 | Low-Medium | Primitive text only | Revert the primitive edit |
| 6, 7 | High | reflect CLI halt set, ensemble defaults, fixtures, test_verdict_mapping | Same-commit revert of skill + CLI + fixtures |

## Review Status
- Approval: auto-approved (non-interactive)
- Timestamp: 2026-10-29T16:55:00Z
