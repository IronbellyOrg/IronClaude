# Anti-Sycophancy Completeness Pass — Phase 2

**Task:** T02.04 — Anti-sycophancy completeness pass over all `feature-*.md`
**Roadmap Item:** R-007
**Side of Truth (R-RULE-10):** `src/superclaude/...` (canonical) — all files cited below live under `.dev/releases/current/task-sc-task-directional-merge/artifacts/` (audit artifacts, not framework source)
**Generated:** 2026-05-15

---

## Pass Criterion

For every `feature-*.md` file produced in T02.01-T02.03:

1. **R-RULE-04 (Anti-sycophancy on value claims):** every Standalone Value Claim (§6) carries at least one *concrete* (not boilerplate) condition under which the value does NOT hold.
2. **Coupling-cost concreteness:** every Coupling Cost Claim (§7) names a *concrete* recipient burden — `file:line` evidence, named extension point, or named integrity rule — rather than a generic "the recipient will need to do work."

A "concrete" non-value condition cites at least one of: a specific `file:line`, a specific dependency-absence verification (e.g. `grep -r ... finds no consumer`), a specific tier or branch case, or a specific verified-absent artifact (e.g. `config/tier-keywords.yaml` does not exist).

A "boilerplate" non-value condition would be generic phrasing like "the value does not hold in some cases" or "the claim depends on adoption" — none such appear in the nine files.

---

## File-by-File Verdict

| # | File | §6 Non-Value Conditions (count, concrete?) | §7 Recipient Burdens (count, named?) | Verdict | Correction Required |
|---|------|--------------------------------------------|---------------------------------------|---------|---------------------|
| 1 | `feature-tier-classification.md` | 2 conditions — (a) homogeneous-tier sessions with cost-but-no-routing-benefit at `task.md:87-89`, (b) LLM-estimated context boosters under text-only Critical Rule 1 at `task.md:53` | 5 burdens — lifecycle extension, schema extension, data-flow contract, configuration discipline, interactive-surface extension (all `file:line`-cited) | PASS | No |
| 2 | `feature-classification-header.md` | 3 conditions — (a) no downstream parser exists (`grep -r "SC:TASK-UNIFIED:CLASSIFICATION" src/` finds only producers), (b) sessions through `/task` never emit a header, (c) single-turn ad-hoc usage has no aggregation infrastructure | 4 burdens — first-output discipline, header-granularity decision, tier-source data path, non-emission guard contract (all `file:line`-cited) | PASS | No |
| 3 | `feature-tfep.md` | 4 conditions — (a) `/sc:forensic` callee does not exist in repo (verified absence of `src/superclaude/skills/sc-forensic/`), (b) LIGHT/EXEMPT sessions skip verification entirely, (c) sessions where all failures fall into the permitted-exception carve-out at `SKILL.md:137-140`, (d) `/task` F4 restrictions at `SKILL.md:144-158` forbid heading insertion outside DYNAMIC CONTENT MARKERS | 6 burdens — baseline-capture in First Item Protocol, test-failure interception in Error Handling, forensic skill must be authored, F4-compatible tasklist insertion, `output_dir` convention, FULL-STOP-and-resume-under-strict semantic (all `file:line`-cited) | PASS | No |
| 4 | `feature-per-tier-branching.md` | 5 conditions — (a) homogeneous-tier batches collapse the cost-gradient claim, (b) failsafe-path skill invocation bypasses Layer 1's command-internal shortcut, (c) `Skill` tool unavailable degrades silently, (d) STRICT-required MCP servers (Sequential/Serena) unavailable forces hard halt per `SKILL.md:253-263`, (e) `/task` invocations have no Layer 1 analog | 6 burdens — meta-dispatch surface, Tier frontmatter slot, four-workflow EXECUTE shape, tier-aware Phase-Gate QA, MCP-availability gate, skip-verification semantic vs always-run Phase-Gate QA invariant (all `file:line`-cited) | PASS | No |
| 5 | `feature-mcp-declarations.md` | 4 conditions — (a) Layer A is write-only (`grep -r "mcp-servers" src/superclaude/` finds only the declaration site), (b) Layer B's hard-prerequisite vs circuit-breaker conflation when Sequential/Serena are not installed by default, (c) "block task execution" specified without enforcement mechanism in repo, (d) two layers inconsistent — Layer A advertises `playwright/magic/morphllm` that Layer B never requires | 5 burdens — frontmatter slot on Skill (loader-recognition unverified), tier-source data path, runtime MCP-availability probe, block-vs-degrade enforcement, per-tier matrix location decision (all `file:line`-cited) | PASS | No |
| 6 | `feature-persona-activation.md` | 4 conditions — (a) activation layer unverifiable from this repo (rules live external to `task.md`), (b) no observability for auto-activations (no header, no sentinel), (c) persona-tier interaction unspecified at `task.md:8`, (d) two of the ten slugs (`python-expert`, `quality-engineer`) are subagent types per `~/.claude/agents/`, not personas | 4 burdens — frontmatter slot extension, prompt-text-input vs task-file-input layer, persona-vs-subagent disambiguation, Critical Rule 12 violation risk at `task SKILL.md:349` (all `file:line`-cited) | PASS | No |
| 7 | `feature-allowed-tools.md` | 4 conditions — (a) `Bash` on the list dilutes the boundary because Bash subsumes excluded tools (`curl` → `WebFetch`, etc.), (b) skill-side allowlist creates a Command→Skill reconciliation burden, (c) no documented override path (`task.md:44-48` lists 8 flags, none tool-related), (d) list is opaque about why each tool is included | 4 burdens — frontmatter slot + Skill-loader recognition, direct conflict with Critical Rule 6 at `task SKILL.md:337`, tool-list calibration, override/weakening path for heterogeneous items (all `file:line`-cited) | PASS | No |
| 8 | `feature-compliance-gating.md` | 4 conditions — (a) all five gates depend on the same upstream classification — single point of failure, (b) no gate has automated enforcement, all prose-discipline-only, (c) `--skip-compliance` / `--no-escalation` flags create legitimate bypasses for all guarantees, (d) two-track dispatch (command-inline vs skill) creates knowledge bifurcation with no consolidated reference | 6 burdens — Tier source extension, F1 loop bifurcation, Phase-Gate QA reconciliation, MCP circuit-breaker enforcement, TFEP integration with Error Handling, CLI-flag re-encoding into flagless skill (all `file:line`-cited) | PASS | No |
| 9 | `feature-triggering-surface.md` | 4 conditions — (a) donor heuristic matcher not implemented in repo (`grep -r "Complexity Score" src/superclaude/` finds the table but no executable rule), (b) recipient trigger phrases overlap with non-task conversational work — no telemetry to falsify, (c) cross-surface accidents — `/sc:task "execute this task"` vs `/task fix the bug` both fail gracelessly, (d) `/sc:task` low-friction value is gated by the whole donor stack (D08-D27) working | 4 burdens — free-text prompt-handling layer on a path-driven skill, heuristic-matcher implementation, reconciliation with existing skill-description trigger phrases, non-substitutability disambiguation rule at trigger boundary (all `file:line`-cited) | PASS | No |

---

## Aggregate Summary

- **Files reviewed:** 9 of 9 (100% coverage).
- **R-RULE-04 violations found:** 0.
- **Files requiring correction:** 0.
- **Boilerplate non-value conditions detected:** 0.
- **Coupling-cost claims lacking concrete recipient burden:** 0.

**Total concrete non-value conditions across all files:** 34 (mean 3.8 per file, min 2, max 5).
**Total concrete coupling-cost burdens across all files:** 44 (mean 4.9 per file, min 4, max 6).

Every non-value condition cites either a `file:line` from the donor source, a verified absence (`grep -r ... finds only X`, or an artifact-existence check via `find`), or a tier-specific case bounded by the donor's own enumeration.

Every coupling-cost burden names either a specific recipient extension point (`task SKILL.md:64-73`, `task SKILL.md:89-96`, `task SKILL.md:170-179`, `task SKILL.md:182-211`, `task SKILL.md:291-299`, `task SKILL.md:337`, `task SKILL.md:349`) or a specific recipient invariant (frontmatter slot at `task SKILL.md:69`, F4 restrictions at `task SKILL.md:144-158`).

---

## Spot-Check Sample (validation aid for reviewer)

Three files selected for reviewer spot-check confirmation that the non-value conditions are *concrete and specific*, not boilerplate:

1. **`feature-tfep.md`** — the "`/sc:forensic` does not exist in the repo today" condition is concrete: it cites the directory absence (`src/superclaude/skills/sc-forensic/`) and the file absence (`src/superclaude/commands/forensic.md`). The downstream consequence — TFEP Steps 3-6 cannot complete — is named. This is the strongest concreteness in the set: a value claim is bounded by a verified missing dependency.

2. **`feature-mcp-declarations.md`** — the "Layer A is dead metadata when downstream tooling ignores it" condition cites a specific grep result (`grep -r "mcp-servers" src/superclaude/` finds only the declaration site, not a consumer). This is a *falsifiable* claim — a reviewer can re-run the grep and confirm.

3. **`feature-allowed-tools.md`** — the "`Bash` on the list dilutes the boundary" condition is concrete and *substantive*: it names specific excluded tools (`WebFetch`, `NotebookEdit`, `mcp__*`) and specific Bash substitutes (`curl`, `jupyter nbconvert`, `mcp_client`). This is not a generic "the boundary might be permeable" — it is a specific argument that the boundary *is* permeable via a named alternative path.

---

## Corrections Made During Pass

**None.** All nine files passed on first inspection. The Phase 2 characterization tasks (T02.01-T02.03) produced compliant artifacts; no in-place corrections were required.

---

## Cross-Reference

- T02.01 produced: `feature-tier-classification.md`, `feature-classification-header.md`.
- T02.02 produced: `feature-tfep.md`, `feature-per-tier-branching.md`.
- T02.03 produced: `feature-mcp-declarations.md`, `feature-persona-activation.md`, `feature-allowed-tools.md`, `feature-compliance-gating.md`, `feature-triggering-surface.md`.
- T02.05 (Phase 2 checkpoint) consumes this report to confirm the "Every value claim has a concrete non-value condition" row of the checkpoint table.
- R-RULE-04 is the source rule for anti-sycophancy on value claims; this pass operationalizes its acceptance criterion.
- R-RULE-10 (side-of-truth tagging) is honored across all nine files — every cited `file:line` carries an explicit `(src/)` side tag.
