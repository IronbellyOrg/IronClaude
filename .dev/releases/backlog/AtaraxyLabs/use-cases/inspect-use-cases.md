# Inspect Use Cases for IronClaude/SuperClaude

## What inspect brings to the table

`inspect` gives IronClaude an entity-level, Rust/tree-sitter PR triage layer that sits between raw `git diff` and expensive LLM review. In this repo, that is most valuable where protocols already collect diffs, file lists, task logs, or roadmap artifacts and then spend model tokens deciding what matters: `/sc:auggie-review`, `/sc:reflect`, `/sc:cleanup-audit`, `/sc:troubleshoot`, `/sc:git`, and the roadmap pipeline. Its best role is an advisory pre-filter: risk-order files/entities, expose blast radius, and untangle mixed commits before Auggie/Claude/agents do deeper reasoning. It should never become a merge gate because the verified precision weakness (33.3%) and top-60 review ceiling make it a prioritizer, not an adjudicator.

## Ranked concrete use cases

### 1. `/sc:auggie-review` Wave 1/2 risk pre-filter for large PRs

- **Surface / files:** `/config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`; `/config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/refs/auggie-prompts.md`; `/config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubric.md`; `/config/workspace/IronClaude/src/superclaude/commands/auggie-review.md`.
- **Inspect command / MCP tool:** `inspect diff <base>...HEAD` or `inspect pr <number>` in Wave 1 after `diff.patch`/`files.txt`; MCP equivalent `inspect_triage` plus `inspect_risk_map`.
- **Status-quo pain removed:** The current protocol jumps from raw changed-file/diff collection into `auggie --print --output-format json --ask`. It chunks by directory when the diff crosses size thresholds and stops above very large diffs unless forced, but it does not know which changed entities are actually riskiest before spending Auggie turns.
- **Net value / QOL gain:** Feed Auggie a risk-ordered entity shortlist and heatmap before the deep pass. This can reduce prompt size on large PRs, make the first review pass focus on public APIs, high-blast-radius entities, and non-cosmetic changes, and make `--depth quick|standard|deep` decisions more evidence-backed. The top value is token pre-filter savings plus better reviewer attention: reviewers see “these are the riskiest entities and why” before reading a giant diff.
- **Advisory caveat:** Inspect must not filter out the rest of the diff invisibly. Because precision is only 33.3% and review only covers top-60 riskiest entities, the report should show a banner such as “inspect prioritized these entities; Auggie/human review remains authoritative; N entities were outside inspect's top-60.”

### 2. `/sc:reflect` UC-2 post-execution drift and regression triage

- **Surface / files:** `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/SKILL.md`; `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md`; `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md`.
- **Inspect command / MCP tool:** `inspect diff <ref>` for the UC-2 `--diff`/`--commit-range`; `inspect_group` to untangle logical change groups; `inspect_entity` for before/after plus dependents/dependencies on disputed entities.
- **Status-quo pain removed:** UC-2 compares completed work, tasklists, task logs, and diffs, then classifies deviations. It already has an expensive cross-task interaction scan using Serena and reviewer waves. What it lacks is a cheap first pass that says which changed symbols have real blast radius and which groups are mixed together.
- **Net value / QOL gain:** Inspect can front-load the UC-2 audit with “changed groups by risk” so reflect spends its deeper ensemble budget on high-blast-radius entities and likely drift/regression points. `inspect_group` is especially useful for tangled task completions: it can show that one commit contains unrelated rule changes, hook changes, and docs changes before reflect maps them to tasklist items.
- **Advisory caveat:** Reflect's evidence-validator and deviation taxonomy remain authoritative. Inspect can propose drift hotspots, but with 33.3% precision it must not auto-classify deviations or promote/withhold Wave 7 mutation.

### 3. `/sc:git` smart commit / PR hygiene assistant for rule-sensitive changes

- **Surface / files:** `/config/workspace/IronClaude/src/superclaude/commands/git.md`; `/config/workspace/IronClaude/CLAUDE.md`; `/config/workspace/IronClaude/scripts/precommit_block_claude_mirrors.sh`; `/config/workspace/IronClaude/Makefile`.
- **Inspect command / MCP tool:** `inspect diff --cached` or `inspect diff <base>...HEAD`; `inspect_risk_map`; `inspect_file <path>` for changed rule/hook/command files.
- **Status-quo pain removed:** `/sc:git` analyzes repo state and generates commits, while project rules separately warn about `.claude/` staging, fork-only PR target, UV-only Python operations, `make sync-dev`, and `make verify-sync`. Today those are mostly textual/process rules plus pre-commit checks; they are not risk-ranked against the actual changed entities.
- **Net value / QOL gain:** A pre-commit advisory pane could highlight rule-sensitive edits before commit-message generation: changes to `CLAUDE.md`, `scripts/precommit_block_claude_mirrors.sh`, `Makefile` sync targets, command/skill definitions, or PR workflow docs get a higher “human attention” score than cosmetic docs. This improves commit hygiene and reduces the chance of staging generated `.claude/` mirrors or making a PR-target/UV-only workflow regression.
- **Advisory caveat:** Inspect does not understand all project policy semantics. It can flag a high-risk entity or file, but it cannot decide whether a command violates “fork-only PR” or “UV-only”; existing hooks, `make verify-sync`, and human rule checks still decide.

### 4. `/sc:cleanup-audit` cost-aware batch prioritization

- **Surface / files:** `/config/workspace/IronClaude/src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md`; `/config/workspace/IronClaude/src/superclaude/skills/sc-cleanup-audit-protocol/rules/verification-protocol.md`.
- **Inspect command / MCP tool:** `inspect_stats` for a lightweight timing/size summary; `inspect_risk_map` for file-level heatmap; `inspect_file <path>` for suspicious files before deeper Pass 2/3 analysis.
- **Status-quo pain removed:** Cleanup audit currently inventories many files, shards batches, runs waves of 7-8 subagents, and validates only a 10% spot-check sample. It is conservative, but it has to spread attention broadly and does not get a semantic risk heatmap before fan-out.
- **Net value / QOL gain:** Use inspect as a read-only pre-pass to rank batches: low-risk/cosmetic files stay in Haiku Pass 1; high-blast-radius files go straight to Sonnet structural analysis or validator spot-checks. The QOL gain is lower false-confidence in large audits and better use of limited validation sampling.
- **Advisory caveat:** Cleanup audit recommendations still require grep/import/dynamic-loading evidence. Inspect's low precision means a “hot” file is a review-priority signal, not a DELETE/KEEP/CONSOLIDATE decision.

### 5. `/sc:troubleshoot` regression-localization pre-pass

- **Surface / files:** `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`; `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/doc-discovery.md`; `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md`.
- **Inspect command / MCP tool:** `inspect diff <last-known-good>...HEAD`; `inspect_entity <entity-id>` for a changed failing component; `inspect_file <path>` when Wave 1 localizes the issue to a file.
- **Status-quo pain removed:** Troubleshoot Wave 1 grounds the symptom with Auggie/Serena and Wave 1.6 audits diagnosability, but regression reports often start with “this used to work” plus a broad scope. The protocol can spend time discovering the likely changed component before hypothesis formation.
- **Net value / QOL gain:** Inspect can narrow “what changed with blast radius near the failing component?” before Tier 2 parallel hypotheses. For flaky tests, build failures, or post-refactor regressions, this gives the root-cause analyst a ranked list of changed entities and dependents instead of a raw diff.
- **Advisory caveat:** Troubleshoot's reproducer/observation and file:line grounding remain mandatory. Inspect cannot replace running the failing command or validating the cited diagnostic path, and its top-60 limit can miss a low-scored but real root cause.

### 6. Roadmap pipeline and scanner risk context for generated plans

- **Surface / files:** `/config/workspace/IronClaude/src/superclaude/skills/sc-roadmap-protocol/SKILL.md`; `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py`; `/config/workspace/IronClaude/src/superclaude/cli/roadmap/obligation_scanner.py`; `/config/workspace/IronClaude/src/superclaude/cli/roadmap/validate_executor.py`; `/config/workspace/IronClaude/src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md`.
- **Inspect command / MCP tool:** `inspect_risk_map` over changed implementation files when validating a roadmap against a completed diff; `inspect_stats` for cheap scope/timing; `inspect_group` to map generated roadmap phases to logical change groups.
- **Status-quo pain removed:** The roadmap CLI already has deterministic anti-instinct modules, obligation scanning, validation, and generated artifacts, but those are mostly document-level. It can detect undischarged scaffolding and coverage problems, yet it does not have entity-level blast-radius data for the implementation changes a roadmap implies or later produces.
- **Net value / QOL gain:** Inspect can annotate roadmap validation with “these planned/changed entities carry high blast radius,” helping risk registers, milestone ordering, and validation focus. In post-roadmap execution, it can help compare whether the actual diff touched riskier entities than the roadmap anticipated.
- **Advisory caveat:** Inspect is weaker on Markdown-heavy planning artifacts and should not judge roadmap correctness. It is useful only when tied to actual code diffs or files, while roadmap validators and anti-instinct scanners remain the source of document-level truth.

## Where inspect does not help / where weaknesses bite

- **Not a gate or reviewer replacement:** 33.3% precision is too noisy for merge blocking, cleanup classifications, task promotion, or PR verdicts.
- **Top-60 ceiling matters on large PRs:** It can save tokens, but it can also hide long-tail entities. Any integration must disclose omitted entity counts and keep a raw-diff/Auggie/human fallback.
- **Weak for policy-only or Markdown-only reasoning:** IronClaude has many behavioral specs, skills, and roadmap docs. Inspect's entity model is most useful when there is real code structure or code-adjacent diffs; it is not a semantic judge for CLAUDE.md policy, roadmap obligations, or tasklist coverage.
- **Not a substitute for grounding:** Existing protocols deliberately re-Read file:line citations, run grep/import checks, validate command output, and use severity/deviation rubrics. Inspect can prioritize those checks, not perform them.
- **Installation/TCO risk remains:** A Rust/tree-sitter binary in a UV-only Python framework must justify install, latency, maintenance, and rollback cost. If the review provider is cheap, token savings alone may not cover that overhead.
