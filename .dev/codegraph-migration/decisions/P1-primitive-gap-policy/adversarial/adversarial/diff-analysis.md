# Diff Analysis: decision-option Comparison (P1 primitive gap policy, issue #323)

## Metadata
- Generated: 2026-10-29T16:40:00Z
- Variants compared: 3
  - Variant 1 = option-a.md (Phase 1 rewrites every load-bearing step to a named native floor + slot ledger)
  - Variant 2 = option-b.md (Phase 1 removes decorative mentions only; load-bearing steps wait for Phase 3)
  - Variant 3 = option-c.md (Phase 1 deletes the Serena tier, relies on named fallbacks; rewrites only steps with no fallback)
- Shared fact base: `../context.md`; inventory `.dev/codegraph-migration/inventory/primitive-usage.md` (read-only)
- Total differences found: 18 (diff points counted for convergence)
- Categories: structural (2), content (9), contradictions (3), unique (5, not counted in convergence), shared assumptions (4 promoted)

Repo facts checked by the orchestrator while building this analysis (Read/Grep only):
- `src/superclaude/agents/reflect-reviewer.md:5,38,129` — closed read-only roster, "You have no write/Bash/Task tool".
- `src/superclaude/agents/troubleshoot-analyst.md:5` and `tests/troubleshoot/test_diagnostic_worker_contract.py:17-39` — exact closed roster `{Read, Grep, Glob, auggie, serena find_symbol, find_referencing_symbols, get_symbols_overview, get_diagnostics_for_file}`; no Bash.
- `src/superclaude/agents/reuse-auditor.md:5` — roster has no Bash.
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md:508-531` — §6.1 chain; `:634-636` §6.5 "Missing Serena → fall back to Grep/Glob with degraded: true"; `:1492` "Serena unavailable → Grep/Glob; skip get_diagnostics_for_file; mark degraded: ['serena']".
- `src/superclaude/cli/reflect/contract.py:33` — known degraded tokens include `"serena"` and `"serena:context-excluded"`.
- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:191-194` — Tier 1 step names auggie + Serena in parallel, with "fall back to Glob + Grep" on the next line.
- primitive-usage.md R141/R143 — validate-roadmap Step 0.5 fallback is "skip, no artifact".

## Structural Differences

| # | Area | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|------|---------------|---------------|---------------|----------|
| S-001 | Length / form | 6-bullet per-job mapping + ledger paragraph + For/Against | one paragraph + For/Against | one paragraph with per-primitive fallback list + For/Against | Low |
| S-002 | Granularity of the policy | per job type (SYM, REF, implementations, DIAG, ALLOW, reflect) with a named replacement for each | no per-row policy (all LB rows deferred as a block) | per primitive (which fallback already exists), with a residual "rewrite if no fallback" rule | Medium |

## Content Differences

| # | Topic | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|-------|---------------|---------------|---------------|----------|
| C-001 | What Phase 1 does with LB SYM/REF steps | rewrite each to a named native floor (Grep definition → Read; auggie first where already used) | leave `mcp__serena__*` in place until Phase 3 | delete where a fallback is already named; rewrite only where none is named | High |
| C-002 | Slot ledger for Phase 3 | written under `.dev/` (file, step, former tool, floor used) | not needed (one edit straight to codegraph) | not written; Phase 3 re-derives from primitive-usage.md | Medium |
| C-003 | Release / merge coupling (intermediate-commit state) | independent of Phase 3 timing; no dangling step at any commit | Phases 1+2+3 must merge together; feature-branch commits dangle | independent of Phase 3 timing; no dangling step at any commit | High |
| C-004 | Phase 1 acceptance search ("zero Serena hits outside `.dev/`") | can pass | cannot pass; needs large exception list | can pass | Medium |
| C-005 | Diagnostics (DIAG) | project linter/type-checker via Bash; drop `get_diagnostics_for_file` | unchanged until Phase 3 | not stated explicitly; implied by reflect's existing "skip get_diagnostics_for_file" fallback | Medium |
| C-006 | Steps whose only fallback is "skip" (validate-roadmap deep Step 0.5) | rewritten to Grep floor (capability kept) | kept on Serena (dangles) | deleted → no-op until Phase 3 (capability silently dropped) | Medium |
| C-007 | Allowlists / closed rosters + pinned test | `tools:`/`allowed-tools:` lose Serena names; troubleshoot-analyst roster and its pinning test change together | unchanged | "allowlists lose `mcp__serena__*`"; pinning test not mentioned | Medium |
| C-008 | Edit volume / touch-twice cost | most work (~20 LB rows + mirrors); some steps touched twice | least; each step edited once | middle (deletions for most rows) | Medium |
| C-009 | reflect Serena degraded tokens in the contract | removed (named as a separate, already-decided change) | not addressed | not addressed | Medium |

## Contradictions

| # | Point of Conflict | Variant positions / evidence | Impact |
|---|-------------------|------------------------------|--------|
| X-001 | B's release guarantee vs the planned merge shape | B: "Release constraint: Phases 1, 2 and 3 merge to `master` together (one unit), so no released build contains a dangling step." context.md: "Phase 3 is planned as a later, separate change (UNVERIFIED whether it can be merged with Phases 1-2)." B's guarantee rests on a merge shape the plan does not have. | High |
| X-002 | A's DIAG floor vs read-only agent rosters | A: "diagnostics -> the project's own linter/type-checker via Bash". reflect-reviewer.md:38 "You have no write/Bash/Task tool"; troubleshoot-analyst roster (pinned by test_diagnostic_worker_contract.py:17-39) has no Bash. Inside those agents the Bash floor is impossible without breaking their read-only design. | High |
| X-003 | A's reference floor phrased as shell `rg` vs agents without Bash | A: "references / callers -> `rg -n -w <symbol>` over the repo". reuse-auditor, troubleshoot-analyst, reflect-reviewer rosters have the `Grep` tool but no Bash. The floor must be phrased as the Grep tool, not a shell command. | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | A | "codegraph slots" ledger so Phase 3 inserts codegraph above the floor without re-searching (immune to line drift) | High |
| U-002 | A | Floor stays useful permanently because codegraph can be absent in some projects, so Phase 3 needs a floor anyway | High |
| U-003 | A | Mark implementations / type-hierarchy floor as "best effort" | Medium |
| U-004 | B | Each LB step edited once, straight to its final form; Phase 3 designs reflect chain with full freedom | Medium |
| U-005 | C | Delete instead of rewrite where a native alternative is already named in the same step (smaller diff) | Medium |

## Shared Assumptions

Agreement points scanned: all three (1) delete decorative rows in Phase 1, (2) treat MEM/ACT/NUDGE as already decided, (3) keep codegraph names out of primitives until Phase 2, (4) treat the inventory's LB/DEC split as the work list.

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| — | (2) | MEM/ACT/NUDGE handled by W2 D1 | STATED (context.md) | No |
| — | (3) | Phases 1 and 2 land together; codegraph names wait for Phase 2 | STATED (context.md) | No |
| — | (A only) | Plugin mirror edited in lockstep | STATED (A: "plus their mirrors") | No |
| A-001 | (4) | The LB/DEC classification in primitive-usage.md is correct for allowlist rows (e.g. R019 reflect-reviewer `tools:` marked DEC with "UNVERIFIED whether the reviewer calls them"; R001 auggie-reviewer `tools:` DEC). If a DEC allowlist is deleted while the skill body that drives that agent still names Serena (B), the boundary breaks. | UNSTATED | Yes |
| A-002 | (1)+(4) | The native floor available inside a subagent is bounded by that agent's closed roster: reflect-reviewer, troubleshoot-analyst and reuse-auditor have Read/Grep/Glob/auggie only — no Bash. | UNSTATED | Yes |
| A-003 | (4) | Removing/rewriting reflect chain steps keeps every contract/telemetry field that those steps produce (`find_declaration_no_match`, `references_extended_info_used`, `type_hierarchy_invoked`, `summarize_changes_invoked`, `serena_summary_corroboration`) supplied with a producer or a defined constant value. | UNSTATED | Yes |
| A-004 | (1)+(4) | Whether native-floor evidence is reported as normal or as degraded: today's fail-open marks Grep/Glob fallback as `degraded: ["serena"]` (reflect SKILL.md:636,1492; contract.py:33). After removal, a run that always uses the floor either always reports degraded or the degrade rule must be redefined. | UNSTATED | Yes |

### Promoted [SHARED-ASSUMPTION] points

| # | Assumption | Impact | Status |
|---|------------|--------|--------|
| A-001 | LB/DEC split correct for allowlist rows | Medium | Open for debate |
| A-002 | Subagent floor bounded by closed roster (no Bash) | High | Open for debate |
| A-003 | reflect contract fields keep a producer | High | Open for debate |
| A-004 | Floor evidence normal vs degraded | High | Open for debate |

## Debate taxonomy pre-tagging

| Point | Level |
|-------|-------|
| S-001 | L1 |
| S-002, C-001, C-002, C-005, C-008 | L2 |
| C-003, C-004, C-006, C-007, C-009, X-001, X-002, X-003, A-001, A-002, A-003, A-004 | L3 |

## Summary
- Total structural differences: 2
- Total content differences: 9
- Total contradictions: 3
- Total unique contributions: 5
- Total shared assumptions surfaced: 7 (UNSTATED: 4, STATED: 3, CONTRADICTED: 0)
- Highest-severity items: C-001, C-003, X-001, X-002, A-002, A-003, A-004
- Similarity check: differences well above 10%; debate proceeds.
