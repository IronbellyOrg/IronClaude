<!-- Provenance: produced by /sc:adversarial (merge-executor, Step 5) -->
<!-- Base: Variant 1 (option-a.md) -->
<!-- Merge date: 2026-10-29 -->
<!-- Inputs: adversarial/variant-1-original.md, adversarial/refactor-plan.md (9 changes, all applied) -->

# Decision P1: Phase 1 policy for load-bearing Serena steps in primitives (merged)

Read `../context.md` first. Terms used here: LB = load-bearing (a step an agent must actually execute), SYM = symbol lookup, REF = callers/references, DIAG = diagnostics, ALLOW = enforced `tools:` / `allowed-tools:` line.

## Decision
<!-- Source: Base (original, modified) — summary rewritten to reflect Changes #1-#9 -->

1. Phase 1 leaves no step that names a tool absent after Phase 1, at any commit.
2. Each LB SYM/REF/DIAG/ALLOW row is triaged first: **delete** the Serena half where the same step already names a Serena-free native path; **rewrite** it to a named native floor everywhere else.
3. The floor is phrased as tools (Read, Grep, Glob, auggie), never as shell commands, and never adds a tool to a closed read-only roster.
4. reflect treats floor evidence as normal: the `serena` degraded tokens leave the halt set, and contract/telemetry field names stay stable with constant values.
5. Phase 1 writes a codegraph slots ledger so Phase 3 can insert codegraph as a tier above the floor. The floor stays permanently.
6. Phase 1 is accepted on its own, independent of when Phase 3 merges.

## Scope
<!-- Source: Base (original, modified) — scope made explicit from context.md:11 -->

In scope: SYM, REF, DIAG, ALLOW rows and the reflect symbol chain (context.md:11). Out of scope: MEM rows (plain files in `.superclaude/memory/`) and ACT/NUDGE Serena-only calls (deleted), both already decided in W2 decision D1 (context.md:11).

## Per-step policy
<!-- Source: Base (original, modified) — triage rule merged per Change #1 (Variant 3); floor bullets modified per Changes #2, #3, #4, #5 -->

**Triage rule (applied first).** Classify each LB row:

- **delete**: the same step already names a Serena-free Read/Grep/Glob/auggie path. Examples: troubleshoot SKILL.md:193 (the :194 Glob + Grep fallback); troubleshoot command :89; auggie-reviewer :36 "Read (or serena)".
- **rewrite**: no fallback exists, the fallback is "skip", or the fallback itself calls Serena.

**Per-job floor for rewritten steps.**

- **Symbol lookup / outline**: the Grep tool for the definition (pattern such as `def name|class name|function name`), then Read the range. auggie first where the primitive already uses it.
- **References / callers**: the Grep tool with a word-boundary pattern for the symbol, then Read the call sites.
- **Implementations / type hierarchy**: the Grep tool for `class .*\(<Base>\)` or `implements <Iface>`; the step is marked "best effort".
- **Bound by roster**: inside closed read-only rosters (reflect-reviewer, troubleshoot-analyst, reuse-auditor) the floor is Read/Grep/Glob/auggie only. Bash is never added.
- **Diagnostics**: the project's own linter/type-checker runs through Bash only in orchestrators whose `allowed-tools` already include Bash (reflect orchestrator chain step 5/5.5; sc-troubleshoot-protocol). reflect §6.1.1's safety envelope (timeout, output cap, denylist) carries over to that Bash verify call. Closed rosters drop `get_diagnostics_for_file`, and the step says the orchestrator's verification leg covers it (reflect-reviewer.md:38, :129).
- **Rosters / allowlists**: every `tools:` / `allowed-tools:` line naming `mcp__serena__*` is treated as LB whatever its inventory label (R001 and R019 are labelled DEC). It changes in the same commit as the skill body that drives that agent and as its pinning test (`tests/troubleshoot/test_diagnostic_worker_contract.py` TOOLS set; sc-troubleshoot SKILL.md:31 prose roster).
- **Fallbacks that call Serena (rewrite, not delete)**:
  - reuse-auditor.md:131: the auggie-unavailable fallback becomes "Grep by capability tokens + skeleton grep". F4 (line 57) uses a Grep reference search.
  - validate-roadmap Step 0.5 (SKILL.md:320-349): gets a Grep-definition floor with the same 30-lookup cap and the same INFORMATIONAL ONLY artifact, not "skip".

## reflect
<!-- Source: Base (original, modified) — degrade rule replaced per Change #6; field constants inserted per Change #7 (Variant 2 edit-once caution) -->

**Degrade rule.** After Phase 1, Grep/Glob/Read evidence is the normal path and emits no `serena` degraded token. `"serena"` and `"serena:context-excluded"` leave `_DEGRADED_COMPONENTS_HALT_SET` (contract.py:32-34) and the §6.5 / §10 fallback rows (reflect SKILL.md:636, :1492). This lands in the same commit as the chain rewrite, with the CLI fixtures (for example `fixtures/degraded_serena.yaml`) updated together.

**Contract and telemetry fields.** Field names stay stable in Phase 1; each gets a producer or a constant:

- `find_declaration_no_match`: produced from a zero-hit Grep.
- `type_hierarchy_invoked: false` (step 4.5 deleted; it was already gated off with no degrade).
- `summarize_changes_invoked: false`.
- `serena_summary_corroboration: unavailable` (matches the `ensemble.py:824` default).
- `references_extended_info_used: false`.
- Step 7 `search_deps` is skipped and its claim is marked `[INFERRED]`.

Renaming these fields waits for Phase 3 or the contract decision. They are read by `ensemble.py:824` and 26 files under `tests/cli/reflect/`.

## Codegraph slots ledger
<!-- Source: Base (original, modified) — restructured per Change #8 -->

Phase 1 writes one row per touched step into the Phase 3 handoff under `.dev/codegraph-migration/`.

| Column | Content |
|--------|---------|
| file | primitive path |
| step | step heading or anchor (not a line number, because lines drift after Phase 1 edits) |
| former Serena tool | the `mcp__serena__*` tool removed |
| action | deleted / floor |
| floor used | the native floor that replaced it |
| contract fields touched | reflect fields affected, if any |

Phase 3 inserts codegraph as a tier above the floor. The floor stays, because codegraph can be absent in some projects.

## Release and acceptance
<!-- Source: Base (original, modified) — "For" paragraph extended per Change #9 -->

Phase 1 does not depend on Phase 3's merge timing. Phase 1 is accepted when:

1. A search for `mcp__serena__` and Serena steps finds zero hits in primitives and the plugin mirror outside `.dev/`.
2. No primitive step names a tool absent from its own roster.

Behaviour after Phase 1 is fully specified and testable step by step.

## Rejected alternatives
<!-- Source: refactor-plan.md "Changes NOT Being Made" -->

| Diff point | Rejected approach | Why |
|------------|-------------------|-----|
| C-001 / U-004 | Variant 2: keep LB Serena steps until Phase 3 | The merge shape is not planned (context.md:13); the Variant 2 advocate conceded (X-001). |
| C-002 | Variant 3: no ledger, re-derive from primitive-usage.md | Line numbers go stale after Phase 1 edits; Variant 3 conceded. |
| C-006 | Variant 3: validate-roadmap Step 0.5 becomes a no-op | Silent capability loss when a Grep floor is cheap; Variant 3 conceded. |
| C-009 | Variant 3: rely on reflect's named fallback as-is | It emits `degraded: ["serena"]`, which is in the halt set (contract.py:33), so every run would halt. |

## Risks
<!-- Source: Base (original, modified) — "Against" paragraph plus refactor-plan.md Risk Summary -->

| Risk | Impact | Mitigation / rollback |
|------|--------|-----------------------|
| Edit volume: about 20 LB rows plus mirrors | Primitive text only | Triage deletes where a native path exists; revert the primitive edit |
| Some steps are touched twice (Phase 1 floor, Phase 3 codegraph tier) | Extra Phase 3 work | Ledger gives Phase 3 exact targets; contract field names stay stable |
| Grep-based reference tracing is weaker than Serena's language server | reflect/troubleshoot quality dips until Phase 3 | "best effort" marking; auggie stays the semantic tier |
| reflect halt-set, ensemble defaults, fixtures and `test_verdict_mapping.py` change (Changes 6-7) | High: reflect CLI code and tests | Skill, CLI and fixtures change in one commit and revert together |

## Open items
<!-- Source: Base (original, modified) — base "already decided" claim corrected per Change #6 -->

- **Contract-token removal ownership.** context.md does not record removing the `serena` degraded tokens from the reflect contract as decided. This decision owns that change unless another decision does.
- **Merge shape.** Whether Phase 3 can merge with Phases 1-2 is UNVERIFIED (context.md:13). This decision does not depend on it.
- **Ledger file name.** The exact handoff file under `.dev/codegraph-migration/` is not named by the plan.
