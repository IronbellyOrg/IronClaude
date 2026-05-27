---
topic: "Rebuild /sc:reflect as a tiered, parallel multi-model protocol skill that replaces the current outdated implementation."
domain: code
strategy: systematic
depth: deep
proposals_target: 5
handoff_target: none
convergence_target: 0.75
blind: true
created: 2026-05-26T21:54:00Z
output_dir: .dev/brainstorms/sc-reflect-rebuild/
---

# Seed Brief: Rebuild /sc:reflect as Tiered Protocol Skill

## Problem Statement

The current `/sc:reflect` command (`src/superclaude/commands/reflect.md`) is an outdated thin wrapper:

- **Serena-only**, leaning on the **deprecated/under-leveraged** `think_about_*` surface (`think_about_task_adherence`, `think_about_collected_information`, `think_about_whether_you_are_done`).
- **No backing skill** — monolithic command file, no `sc-reflect-protocol` skill.
- **No tier escalation** — single execution path, no parallel sub-agents.
- **No multi-model verification** — single-model reflection, no adversarial pressure.
- **No integration with sibling protocol skills** (sc-troubleshoot, sc-adversarial, sc-brainstorm patterns).
- **Sycophancy/hallucination risk**: a single agent reflecting on its own work has structural bias; no independent re-grounding of citations or claims.

This must be rebuilt as a Tier 3 complex protocol skill that mirrors the architectural maturity of `sc-troubleshoot-protocol` and `sc-brainstorm-protocol`.

## Known Context

### Current implementation
- `src/superclaude/commands/reflect.md` (112 lines) — Serena MCP integration, TodoRead/TodoWrite bridging, "Recommendation Re-scrutiny" sub-feature.
- MCP servers declared: `serena, context7`. Personas: `[]`.
- Reflection tools used (all deprecated/redundant against modern Serena surface): `think_about_task_adherence`, `think_about_collected_information`, `think_about_whether_you_are_done`.

### Reference architecture (sibling protocol skills)
- **sc-troubleshoot-protocol** — tiered (T1 fast triage → T2 parallel hypothesis sub-agents + adversarial fix debate → opt-in T3 task-builder remediation chain), auggie + serena grounding, confidence-calibrator integration, evidence-validator gate.
- **sc-brainstorm-protocol** — 6-wave architecture (prereqs → Socratic → enrichment → agent-spec → adversarial → handoff), versioned return contract, model rotation across 3 active aliases.
- **sc-adversarial-protocol** — Mode A (compare existing artifacts) used for cross-agent merge with blind scoring and convergence gating.

### Modern Serena surface (replaces think_about_*)
- Symbol navigation: `find_symbol`, `find_referencing_symbols`, `get_symbols_overview`.
- Code mutation: `replace_symbol_body`, `insert_after_symbol`, `insert_before_symbol`, `replace_content`.
- Memory: `write_memory`, `read_memory`, `list_memories`, `rename_memory`, `edit_memory`, `delete_memory`.
- Diagnostics: `get_diagnostics_for_file`.
- Project state: `activate_project`, `get_current_config`.

### Reusable agents (already in repo, do not re-author)
- `confidence-calibrator` — rubric-based confidence re-grading, used by sc:troubleshoot in T1 calibration and T2 per-card calibration.
- `evidence-validator` — independent last-gate re-Read of every file:line citation; drops unfounded items.
- `rf-qa` / `rf-qa-qualitative` — intra-task QA with adversarial stance + `fix_authorization`.
- `root-cause-analyst` — hypothesis-driven investigation.
- `audit-validator` — spot-check accuracy of prior findings via independent re-test.

### Eval harness reference pattern
- `.dev/eval-workspaces/sc-brainstorm/` provides the model: `SPEC.md`, `evals/`, `iterations/iteration-N/`, `quality-grading.json` rubric, 2-3 measurable iteration cycles, `aggregate_iteration.py`, `grader.py`.

## Two Primary Use Cases (in scope)

### UC-1: Pre-execution validation
**Input**: A tasklist OR a proposed strategy + its driving spec/PRD/objectives document.
**Output**: A coverage + best-practice compliance verdict — does the proposed work cover every requirement in the spec, does the strategy follow established best practices for the domain, and what gaps/risks exist before execution begins.
**Stakes**: Catches bad plans before token spend. ROI similar to confidence-check (100-200 tokens to save 5,000-50,000).

### UC-2: Post-execution review
**Input**: Completed agent work (commit diff, artifact files, task log) + the tasklist that drove it.
**Output**: A 100%-completion verification, strict-adherence audit (every tasklist item resolved, no silent skips), explicit identification of validated deviations vs. unauthorized drift, and best-practice compliance grading for the deliverables.
**Stakes**: Independent re-grading prevents self-confirmation bias from the executing agent. This is the durable, high-value mode.

## Target Architecture

### Tier 3 complex protocol skill
- Location: `src/superclaude/skills/sc-reflect-protocol/SKILL.md`
- Size: ~400-700 lines per `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`.
- Structure: `SKILL.md` (main protocol) + `refs/` (on-demand loaded references) + `templates/` (if needed) + agent delegation.
- Multi-phase / multi-wave architecture mirroring sc-troubleshoot or sc-brainstorm.

### Tier escalation (mirrors sc-troubleshoot)
- **Tier 1** — fast single-agent reflection, grounded by serena + auggie. Used when scope is narrow and confidence-calibrator returns ≥0.85.
- **Tier 2** — auto-escalation. 2-3 parallel sub-agents on distinct smaller models (haiku, sonnet — plus optional qwen/kimi if available in the alias map) running the same reflection task in parallel. Opus merges T2 results via `Skill sc-adversarial-protocol` (Mode A) for the final adversarial verdict.
- **Tier 3** — opt-in remediation handoff. If post-execution review surfaces gaps/violations and the user opts in, hand off to `task-builder` for a corrective MDTM task file.

### Deep modern Serena integration
- Replace every `think_about_*` invocation with a concrete symbol/code-anchored equivalent:
  - "Task adherence" → `find_symbol` + `find_referencing_symbols` against the tasklist's named touch-points; diff against the actual git changes.
  - "Collected information" → `get_symbols_overview` on the touched files + `list_memories` for session context.
  - "Whether you are done" → `get_diagnostics_for_file` on every touched file + tasklist checkbox completion rate + spec-coverage map.
- Consult Serena's latest docs and community usage patterns via `Skill tech-research` before authoring.

### Cross-skill integration
- `sc-adversarial-protocol` (Mode A) — merges T2 parallel verdicts.
- `task-builder` — T3 remediation handoff.
- `confidence-check` — fires before any actionable recommendation per CLAUDE.md global rule 3.
- `evidence-validator` — re-grounds every file:line citation in the final verdict before emission.
- `tech-research` — Serena-docs lookup; best-practice external references when the spec references frameworks/libraries.

## Constraints (hard)

1. **CLAUDE.md ABSOLUTE RULES**:
   - `src/superclaude/` is source of truth → all authoring lands there first → `make sync-dev` → `.claude/` mirror.
   - NEVER stage `.claude/skills/`, `.claude/commands/`, `.claude/agents/` (gitignored sync-dev output).
   - `git add -f` on any `.claude/` path is forbidden.
2. **UV-only** Python execution.
3. **Confidence check** ≥90% gate before any actionable recommendation.
4. **Auggie-first** before significant edits (load codebase context).
5. **Temporal hygiene** — verify current date (2026-05-26) before any date/version reasoning.
6. **Architectural conformance** — must follow `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` Tier 3 contract.
7. **Sprint-CLI-compatible build path OR skill-creator eval-iteration path** must be specified for the build.
8. **No silent downgrades** — if a prerequisite skill is missing, STOP with explicit message (sc-brainstorm pattern).

## Success Criteria

- ✅ A complete `sc-reflect-protocol` skill at `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (~400-700 lines).
- ✅ Supports both UC-1 (pre-execution) and UC-2 (post-execution) modes via explicit flag or auto-detection.
- ✅ Three-tier escalation: T1 fast → T2 parallel multi-model + adversarial merge → opt-in T3 remediation handoff.
- ✅ Zero references to deprecated `think_about_*` Serena tools; full modern-Serena tool surface.
- ✅ Reuses confidence-calibrator, evidence-validator, rf-qa, root-cause-analyst — does NOT duplicate them.
- ✅ Defines tier-decision rubric (scope/complexity signals → tier mapping) BEFORE build begins.
- ✅ Defines eval rubric dimensions + acceptance thresholds BEFORE build begins.
- ✅ Live-run eval harness at `.dev/eval-workspaces/sc-reflect/` modeled on sc-brainstorm — real prompts against real codebase, 2-3 iteration cycles measuring improvement.
- ✅ Versioned return contract (stable + telemetry blocks).
- ✅ Architectural conformance to Tier 3 complex-skill spec.

## Open Questions (for variants to answer)

1. **Tier-decision rubric specifics** — exact scope/complexity signals that route T1 vs T2; thresholds (line-count touched? cyclomatic complexity? blast radius? task count?).
2. **Multi-model topology** — fixed 2 sub-agents (haiku+sonnet) or 3 (haiku+sonnet+qwen-if-present)? How to handle missing optional aliases?
3. **Pre- vs post-execution mode selection** — explicit flag (`--mode pre|post`) or auto-detect from input shape (presence of completed-work artifacts)?
4. **Adversarial merge contract** — what convergence threshold for T2 PASS (0.75? 0.65?)? What's the fallback when sub-agents diverge irreconcilably?
5. **Deviation taxonomy** — what counts as a "validated deviation" vs. unauthorized drift? Where does the gold-standard reference for "validated" come from (PR description? commit message? task-builder approval log?)?
6. **Evidence-validator integration depth** — re-Read every citation in the verdict, or only HIGH-stakes claims? What's the budget?
7. **New agents needed** — does any variant identify a gap that requires a new custom agent (e.g., a `coverage-mapper` or `deviation-classifier`)?
8. **Build path** — Sprint CLI (tasklist-driven, multi-file bundle) vs. skill-creator eval-iteration (single-skill iterative refinement)? What's the right pick for this skill given its eval-driven nature?
9. **Eval rubric dimensions** — what are the 4-7 grading axes (e.g., citation accuracy, coverage completeness, deviation-classification precision, best-practice compliance, recommendation actionability)?
10. **Pipeline composability** — should `/sc:reflect` accept piped input from `/sc:task` (post-execution mode) and `/sc:tasklist` (pre-execution mode) directly via a shared return-contract format?

## Variant Mandate

Each of the 5 parallel variants MUST:
- Propose a concrete tier-decision rubric (answer Q1, Q2, Q4).
- Specify pre-vs-post mode selection (Q3).
- Define an eval rubric with ≥4 dimensions and acceptance thresholds (Q9).
- Map every reusable agent (confidence-calibrator, evidence-validator, rf-qa, root-cause-analyst) to a phase, OR justify omission.
- Pick a build path (Sprint CLI vs skill-creator) with rationale (Q8).
- Honor every constraint in §Constraints — variants that violate ABSOLUTE RULES are auto-failed in adversarial debate.

Persona overlays (assigned in Wave 2B):
- **architect** — systems design, tier topology, skill-boundary surface.
- **analyzer** — root-cause framing, deviation taxonomy, hallucination/sycophancy guardrails.
- **refactorer** — code health, eliminating deprecated surfaces, minimizing duplication with sibling skills.
- **quality-engineer** — eval rubric, acceptance thresholds, iteration harness design, test strategy.
- (5th persona padded in Wave 2B per persona-matrix default.)

## Enrichment Context

### Codebase context (enrichment/codebase-context.md — 1074 lines)
Key findings:
- **/sc:reflect is the only Tier-3 command in this repo with no companion `*-protocol` skill** — every other sc:* command has one (sc-troubleshoot, sc-brainstorm, sc-adversarial, sc-roadmap, sc-tasklist, etc.). This is a structural anomaly the rebuild closes.
- **`think_about_*` Serena verbs are a single-file island** — grep against `src/superclaude/` returns zero hits outside `commands/reflect.md`. No prior art in the rest of the codebase to inherit from.
- **Target size for the SKILL.md: ~421-456 lines** (sc-troubleshoot = 421, sc-brainstorm = 456). `sc-adversarial-protocol/SKILL.md` is an outlier at 3002 lines and is NOT a model.
- **Eval workspace location is project-overridden**: per CLAUDE.md, eval workspaces must land at `.dev/eval-workspaces/sc-reflect/`, NOT the skill-creator default sibling path under `.claude/skills/`. The PreToolUse hook + .gitignore enforce this.
- **`grader.py` assertion DSL has 8 reusable types** (`file_exists`, `frontmatter_field`, `section_present`, `section_enumerated`, `yaml_field`, `yaml_field_min`, `yaml_substring`, `dir_count`). At least one new semantic type — `citation_resolves` — is needed for reflection-specific re-grounding checks.

### Deep research (enrichment/research-deep.md — ~7400 words)
Key recommendations:
- **`think_about_*` are CURRENT, not deprecated** (verified via oraios/serena docs + Dec 2025 community guides). They are under-leveraged meta-cognition checkpoints (18-tool default MCP surface). The right move is to wire them as **mandatory scripted protocol checkpoints**, not optional self-nudges. The heavy reflection logic should still live in the modern symbolic surface (`get_symbols_overview` → `find_symbol` → `find_referencing_symbols` + `write_memory`/`read_memory`).
- **Khan et al. ICML 2024 Oral + Kenton NeurIPS 2024**: weak judges + strong persuasive debaters outperform strong-judge + weak-debaters. This validates "Sonnet-as-merge-judge between Opus debaters" OR keeps the spec's "Opus-merges-T2-via-sc-adversarial" path defensible only if the T2 sub-agents are genuinely independent (heterogeneous models).
- **Heterogeneous models beat homogeneous-cheap stacks** (HDEE, LLM-TOPLA, DeePEen, Wisdom of Silicon Crowd). A haiku+sonnet+(qwen|kimi|deepseek) trio is empirically better than 3× haiku.
- **Single-model self-review is structurally biased** (Mehta 2026 — "the same representational biases that produced the error are present when it re-evaluates"). The reviewer MUST be a different model class than the executor for UC-2 to be valid.
- **0–5 grading scale** has highest human-LLM ICC alignment (arxiv 2601.03444). Target 70-90% assertion pass rate, not 100%. Convergence: stop iterating when N+1 vs N is <5% absolute improvement on held-out test set.
- **Anthropic Skill Creator 2.0** ships parallel sub-agents (grader/comparator/analyzer) — directly applicable patterns.
- **Microsoft Azure Task Adherence (preview, Dec 2025)** is the closest commercial precedent for UC-1 — explicitly validates agent plans BEFORE tool execution. NASA MBSE+LLM reports 35%→67% coverage and 76.7%→92% accuracy gains for plan-vs-spec traceability.
- **Validated-deviation taxonomy is a literature gap** — variants are encouraged to propose a concrete 4-category taxonomy (Authorized expansion / Necessary deviation / Drift / Regression).

Enrichment sources used:
- `codebase` — quality_tier: primary (general-purpose agent, Read + Grep + Glob + auggie)
- `research-deep` — quality_tier: primary (deep-research agent, tavily-search across 5 topics)
