# Context: what Phase 1 does with load-bearing Serena references in primitives (issue #323)

Decision: between Phase 1 (removal of Serena and codebase-memory) and Phase 3 (adoption of codegraph in primitives), how are load-bearing Serena references in skills, commands, agents, refs and modes handled so that nothing is left dangling (a step that tells an agent to call a tool that no longer exists)?

## Verified facts

- Source: `.dev/codegraph-migration/inventory/primitive-usage.md` (W6). codebase-memory has zero references in primitives. Serena: 251 rows in 73 primitive files under `src/superclaude` + 19 plugin-mirror rows; 86 load-bearing (LB), 165 decorative.
- LB rows by job: MEM 40 (memory persistence), ACT 12 (activation/onboarding/config probe), SYM 10 (symbol lookup), NUDGE 7 (`think_about_*`, `summarize_changes`), ALLOW 4 (enforced `allowed-tools:`), CONTRACT 4 (reflect output-contract fields parsed by `src/superclaude/cli/reflect/contract.py`), REF 3 (callers), DIAG 3 (diagnostics/verification triangle), EDIT 2 (freshness hook matcher and `relative_path` branch), CFG 1.
- SYM/REF/DIAG LB rows live in: `commands/troubleshoot.md` (1), `skills/sc-reflect-protocol/SKILL.md` (11: symbol chain, references, diagnostics), `skills/sc-troubleshoot-protocol/SKILL.md` (1, Tier 1 grounding step), `skills/sc-validate-roadmap-protocol/SKILL.md` (2, deep-only fail-open symbol supplement), `agents/reuse-auditor.md` (1, F4 call-graph role; rg fallback named at line 131).
- Most Serena steps are already fail-open: validate-roadmap ("fail-open, skip entirely if Serena is unavailable"), reuse-auditor (rg skeleton fallback), troubleshoot (auggie + Read). reflect has fail-open branches for unavailable tools but its contract also emits Serena-specific degraded tokens (`serena`, `serena:context-excluded`) that the CLI halts on (`contract.py:32-34`).
- Memory (MEM) rows are already decided: Phase 1 replaces Serena memory with plain files in `.superclaude/memory/` (W2 decision D1, adversarial quick). ACT/NUDGE Serena-only calls are deleted, not ported (same decision, item 8). So this decision covers SYM, REF, DIAG, ALLOW and the reflect symbol chain.
- codegraph is installed only in Phase 2; Phase 3 maps every former Serena use to codegraph. codegraph tool names are known from `.dev/codegraph-migration/research/codegraph-evaluation.md` but must not appear in primitives before Phase 2 installs it.
- Planned merge shape (W5 research 5.3): Phase 1 and Phase 2 land on IronClaude `master` as one unit, because Coder auto-bumps its pin to every master commit. Phase 3 is planned as a later, separate change (UNVERIFIED whether it can be merged with Phases 1-2).
- Native tools always available to agents: Read, Grep, Glob, Bash (rg). Auggie (`mcp__auggie__codebase-retrieval`) is already named in most of these primitives as the semantic tier.
- Tests pin some of these: `tests/troubleshoot/test_diagnostic_worker_contract.py` (exact analyst tool roster), sc-troubleshoot SKILL.md line 31 declares the same roster in prose, reflect CLI fixtures and `test_verdict_mapping.py`.

## Options

- option-a.md: Phase 1 rewrites every load-bearing step to a named native floor.
- option-b.md: Phase 1 removes decorative mentions only; load-bearing steps wait for Phase 3.
- option-c.md: Phase 1 deletes the Serena tier and relies on the fallback each primitive already names; rewrites only steps with no fallback.
