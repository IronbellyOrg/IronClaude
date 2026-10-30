# Merge Log

## Metadata
- Base: Variant 1 (`variant-1-original.md`, option-a.md)
- Executor: merge-executor (sc:adversarial Step 5)
- Plan: `refactor-plan.md` (9 planned changes, auto-approved 2026-10-29T16:55:00Z)
- Changes applied: 9 of 9
- Output: `../merged-recommendation.md`
- Status: COMPLETE
- Timestamp: 2026-10-29

## Changes

### Change #1: Triage first, delete where a Serena-free native path exists
- Status: applied
- Target section: Per-step policy (triage rule, placed before the floor mapping); Decision item 2
- Provenance tag: `Base (original, modified) — triage rule merged per Change #1 (Variant 3)`
- Before: base opened by rewriting every LB row. After: rows are classified delete / rewrite first, with the three examples from the plan (troubleshoot SKILL.md:193/:194, troubleshoot command :89, auggie-reviewer :36).

### Change #2: Floor phrased as tools, bounded by roster
- Status: applied
- Target section: Per-step policy (symbol lookup, references, "Bound by roster" bullet); Decision item 3
- Provenance tag: `... modified per Changes #2 ...`
- Before: `rg -n "def name|..."` and `rg -n -w <symbol>`. After: "the Grep tool" with a definition pattern and with a word-boundary pattern; closed rosters limited to Read/Grep/Glob/auggie, Bash never added.
- Note: the implementations bullet used the same shell `rg` phrasing; it was rephrased to "the Grep tool" for consistency with this change (X-003). No new strategy added.

### Change #3: Diagnostics only where Bash already exists
- Status: applied
- Target section: Per-step policy, Diagnostics bullet
- Provenance tag: `... modified per Changes #3 ...`
- Before: linter via Bash everywhere, drop `get_diagnostics_for_file`. After: Bash linter only in orchestrators that already have Bash (reflect step 5/5.5, sc-troubleshoot-protocol), §6.1.1 envelope carried over, closed rosters drop the tool and defer to the orchestrator's verification leg.

### Change #4: Roster rule
- Status: applied
- Target section: Per-step policy, Rosters / allowlists bullet
- Provenance tag: `... modified per Changes #4 ...`
- Appended: every roster naming `mcp__serena__*` is LB regardless of label (R001, R019 are DEC); same-commit change with the driving skill body and the pinning test (TOOLS set; SKILL.md:31).

### Change #5: Rewrite fallbacks that are not Serena-free
- Status: applied
- Target section: Per-step policy, "Fallbacks that call Serena" bullet (after implementations)
- Provenance tag: `... modified per Changes #5 ...`
- Inserted: reuse-auditor.md:131 fallback becomes Grep by capability tokens + skeleton grep; F4 (line 57) uses Grep reference search; validate-roadmap Step 0.5 gets a Grep-definition floor (30-lookup cap, INFORMATIONAL ONLY artifact).

### Change #6: reflect degrade rule
- Status: applied
- Target section: reflect (Degrade rule); Open items (ownership)
- Provenance tag: `Base (original, modified) — degrade rule replaced per Change #6`
- Before: "Serena degraded tokens are removed from the contract (separate, already decided)". After: floor evidence is normal; `"serena"` and `"serena:context-excluded"` leave the halt set and §6.5 / §10 rows in the same commit as the chain rewrite and fixtures. The "already decided" claim is removed; Open items states context.md does not record it as decided and this decision owns it unless another does.

### Change #7: Contract and telemetry fields keep names, get constants
- Status: applied
- Target section: reflect (Contract and telemetry fields)
- Provenance tag: `... field constants inserted per Change #7 (Variant 2 edit-once caution)`
- Inserted: the producer for `find_declaration_no_match`, four constants, step 7 `search_deps` skipped and marked `[INFERRED]`, renaming deferred; consumers named (`ensemble.py:824`, 26 files under `tests/cli/reflect/`).

### Change #8: Ledger keyed by file plus step heading
- Status: applied
- Target section: Codegraph slots ledger
- Provenance tag: `Base (original, modified) — restructured per Change #8`
- Before: columns file, step, former tool, floor; location "under `.dev/`". After: six columns (adds action, contract fields; step is heading/anchor, not line); location under `.dev/codegraph-migration/`; Phase 3 inserts codegraph above the floor, floor stays.

### Change #9: Release and acceptance statement
- Status: applied
- Target section: Release and acceptance; Decision item 6
- Provenance tag: `Base (original, modified) — "For" paragraph extended per Change #9`
- Appended: independence from Phase 3 merge timing; two acceptance checks (zero `mcp__serena__` / Serena-step hits outside `.dev/`; no step names a tool absent from its roster).

### Supporting sections (requested structure, no new strategy)
- Scope: from context.md:11. Rejected alternatives: copied from the plan's "Changes NOT Being Made". Risks: base "Against" paragraph plus the plan's Risk Summary. Open items: Change #6 correction, context.md:13 UNVERIFIED merge shape, and the unnamed ledger file (an observation, not a decision).

## Post-Merge Validation

| Check | Result | Detail |
|-------|--------|--------|
| Heading hierarchy | PASS | One H1; nine H2 sections (Decision, Scope, Per-step policy, reflect, Codegraph slots ledger, Release and acceptance, Rejected alternatives, Risks, Open items); no skipped levels. Each H2 has a `<!-- Source: ... -->` comment. |
| Provenance header | PASS | Lines 1-3: produced by /sc:adversarial; Base: Variant 1 (option-a.md); merge date 2026-10-29. |
| Internal references | PASS | Pointers to context.md:11 and :13 resolve (Read this session). Change IDs #1-#9 and diff IDs C-001, C-002, C-006, C-009, X-001 exist in the plan and transcript. Source file:line citations (contract.py, reflect SKILL.md, reflect-reviewer.md, reuse-auditor.md, validate-roadmap SKILL.md, ensemble.py) are copied verbatim from the plan and were not re-read in the source files. |
| Contradiction re-scan: Bash inside read-only agents | PASS | Grep for `Bash`: only lines 38-39, both stating Bash is never added to closed rosters and runs only in orchestrators that already have it. |
| Contradiction re-scan: shell `rg` | PASS | Grep for `` `rg ``/`ripgrep`: zero hits. Floor is phrased as the Grep tool throughout. |
| Contradiction re-scan: "already decided" contract-token claim | PASS | "already decided" appears only for MEM and ACT/NUDGE (line 23, matches context.md:11) and in a provenance comment (line 108). Open items states the token removal is not recorded as decided. |
| New contradictions vs variants | PASS | No merged statement conflicts with another; the conflicts X-002 and X-003 from Variant 1 are resolved, and the X-001 dependency from Variant 2 is rejected explicitly. |
| Length | PASS | About 112 lines (target under 140). |

## Summary
- Planned: 9
- Applied: 9
- Failed: 0
- Skipped: 0
