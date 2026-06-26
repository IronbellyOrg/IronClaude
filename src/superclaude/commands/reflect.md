---
name: reflect
description: "Tiered reflection protocol — UC-1 pre-execution coverage/gap audit and UC-2 post-execution deviation audit with heterogeneous reviewer ensemble, blind calibration, and mandatory evidence-validator gate"
category: analysis
complexity: advanced
mcp-servers: [auggie, serena, context7, tavily, sequential]
personas: [analyzer, qa, refactorer]
version: 2.0.0
supersedes: .dev/eval-workspaces/sc-reflect/skill-snapshot/reflect-v1.md
argument-hint: "[--mode pre|post] [--spec <path>] [--tasklist <path>] [--diff <ref-or-path>] [--scope <path>] [--depth quick|standard|deep] [--tier 1|2|auto] [--reviewers N] [--output <dir>] [--no-reachability] [--no-promote] [--promote-dry-run] [--remediate] | legacy: [--type task --analyze|--validate]"
---

# /sc:reflect - Tiered Reflection Protocol

## Triggers

Auto-activates whenever a reviewer-side, structurally-independent audit is needed against a spec, a tasklist, or a completed work-unit — even without saying "reflect". Activation paths:

1. **Direct invocation**: `/sc:reflect --mode pre|post ...` (recommended for non-interactive callers)
2. **Legacy invocation**: `/sc:reflect --type task --analyze` or `/sc:reflect --type task --validate` — preserved for `sc:troubleshoot-protocol` Wave 6 (Phase B and Phase D) and any other caller already on the v1 grammar. The legacy grammar is mapped onto the new modes (see Usage below).
3. **Programmatic call**: Another `/sc:*` command invokes the `sc:reflect-protocol` skill directly (e.g., `sc:task-protocol` end-of-task hook when enabled).

## Required Input

**MANDATORY**: A resolvable mode (UC-1 pre-execution or UC-2 post-execution). The skill resolves mode via the §3.2 6-rule first-match selection logic (see protocol). The minimum inputs per mode:

- **UC-1 (pre-execution)**: `--spec <path>` is required. `--tasklist <path>` is recommended.
- **UC-2 (post-execution)**: at least one of `--diff <ref-or-path>` or `--task-log <path>` is required. `--tasklist <path>` is recommended.

**STOP** conditions (the skill aborts cleanly with a `status: stopped-precondition` contract):

- `--mode pre` with no `--spec` (pre-execution reflection has nothing to reflect against).
- `--mode post` with no `--diff` AND no `--task-log` (post-execution reflection has no completed work to audit).
- `--depth deep` with under-specified input (1-line spec, empty tasklist).
- `--output` resolves under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` (CLAUDE.md ABSOLUTE RULE — distributable paths are not output sinks).

## Usage

```bash
# UC-1 pre-execution coverage/gap audit (new grammar — recommended)
/sc:reflect --mode pre --spec docs/spec.md --tasklist .dev/tasklists/my-feature.md

# UC-2 post-execution deviation audit (new grammar — recommended)
/sc:reflect --mode post --diff HEAD~1..HEAD --tasklist .dev/tasklists/my-feature.md

# Legacy grammar (preserved for sc:troubleshoot Wave 6 + other v1 callers)
/sc:reflect --type task --analyze    # → maps to --mode pre  (analysis-style pre-execution audit)
/sc:reflect --type task --validate   # → maps to --mode post (validation-style post-execution audit)

# Force tier and reviewer count
/sc:reflect --mode post --diff HEAD~1..HEAD --depth deep --reviewers 3

# Cap at Tier 1 (quick second opinion)
/sc:reflect --mode pre --spec docs/spec.md --tier 1

# Promotion controls (UC-2 only — see §14.5)
/sc:reflect --mode post --diff HEAD~1..HEAD --no-promote        # diagnose-only, suppress Wave 7
/sc:reflect --mode post --diff HEAD~1..HEAD --promote-dry-run   # print mv command + gate eval, no mutation

# Offer the Tier 3 remediation chain after audit
/sc:reflect --mode post --diff HEAD~1..HEAD --remediate
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--mode` | auto-detect via §3.2 | `pre` (UC-1 coverage/gap audit) or `post` (UC-2 deviation audit). Explicit setting eliminates auto-detect ambiguity. |
| `--type` | (legacy) | Legacy v1 flag — accepts `task` for backward compatibility with `sc:troubleshoot-protocol` Wave 6. Combined with `--analyze`/`--validate` to resolve mode (see legacy mapping below). |
| `--analyze` | (legacy) | Legacy v1 flag — paired with `--type task`, maps to `--mode pre`. |
| `--validate` | (legacy) | Legacy v1 flag — paired with `--type task`, maps to `--mode post`. |
| `--spec` | (none) | Driving spec / PRD / objectives doc. **Required for UC-1.** Recommended for UC-2. |
| `--tasklist` | (none) | Tasklist file. **Strongly recommended for UC-2** (does not STOP if omitted; the post hard requirement is `--diff` or `--task-log`). Recommended for UC-1 when one exists. |
| `--diff` | (none) | Git ref (e.g., `HEAD~1..HEAD`, branch name) or path to a diff file. **Required for UC-2** unless `--task-log` is provided. |
| `--commit-range` | (none) | Alternative to `--diff` for resolving a post-execution diff via git. |
| `--scope` | (none) | Narrowing scope; when it resolves to modified files, contributes to UC-2 auto-detect. |
| `--task-log` | (none) | Task execution log (UC-2 alternative input when no diff is available). |
| `--depth` | `standard` | `quick` (Tier 1 only) / `standard` (Tier 1, escalate by §5 rubric) / `deep` (force Tier 2). |
| `--tier` | `auto` | Explicit tier pin (`1`, `2`, or `auto`); overrides the rubric. |
| `--reviewers` | `3` | Tier 2 reviewer count (2-3); clamped by `--depth`. |
| `--output` | `.dev/reflect/<mode>-<slug>-<ts>/` | Output directory. MUST NOT resolve under `.claude/skills,agents,commands/`. |
| `--coverage-floor` | `0.90` | UC-1 coverage stop floor override (high-safety profile: `0.95`). |
| `--no-mcp` | `false` | Native-tools-only mode; warns and auto-degrades grounding quality. |
| `--no-evidence-validator` | `false` | Skip the final evidence-validator gate (debug only — auto-warns; report records the skip in Grounding Gaps). |
| `--no-doc-discovery` | `false` | Skip Wave 1.5 documentation grounding (records the skip in Grounding Gaps). |
| `--no-verify` | `false` (UC-2) | Disable the UC-2 verification triangle (`execute_shell_command` scoped non-mutating tests/linters/type-checkers/build, §6.1 step 5.5). Default-on; when set, degrades §10.4 Regression detection to the task-log claim with a Grounding Gap entry. Subsumes the deprecated `--rerun-tests` alias. |
| `--no-reachability` | `false` (UC-2) | Disable the §6.1 step-5.6 contracted-sink reachability & oracle-admissibility gate (the operator rollback path). Default-on; when set, records telemetry-only skip state (`reachability_gate_ran: false`, `reachability_skip_reason: --no-reachability`); it does NOT write a Grounding Gap, set needs_human_decision, or force status: partial. |
| `--onboard` | `false` | Opt-in one-shot Serena `onboarding` bootstrap at Wave 0.7b — runs ONLY when `list_memories` is empty for the project slug; seeds the §6.3 cold-start calibration baseline. Never creates `.serena/` implicitly. |
| `--with-hierarchy` | `false` | Opt-in `type_hierarchy` transitive supertype/subtype retrieval (§6.1 step 4.5, Wave 1B.3). Backend-gated (`jetbrains` only; default OFF on `lsp`, unavailable on `none`); non-OO codebases see zero change. |
| `--remediate` | `false` | After the audit ships, offer the Tier 3 remediation chain (`task-builder` → operator runs `/task` → `/sc:reflect --mode post` re-runs as the post-commit gate). |
| `--budget-remaining` | (none) | Caller-side budget hint (typically `TurnLedger.available()` from a sprint context). When provided, reflect cross-checks against the §15 cost profile and may auto-degrade tier; emits `budget_forced_tier_downgrade: true` in the contract. |
| `--no-promote` | `false` (UC-2) | Suppress Wave 7 promotion. Default behavior: when the §14.5.2 strict gate passes, the validated work-unit folder moves to its `done` destination. |
| `--promote-anyway` | `false` (UC-2) | Override the `status: partial` gate condition. No effect on `status: failed`. |
| `--promote-dry-run` | `false` (UC-2) | Print the `mv` command + gate evaluation; perform no mutation. |
| `--promote-mode` | `auto` (UC-2) | Force a specific promotion adapter: `auto` / `task` / `sprint-release` / `none`. |
| `--promote-resume` | (none) | Resume an interrupted cross-filesystem promotion from a `promotion-checkpoint.yaml`. |

### Legacy grammar mapping

The v1 surface used `--type task --analyze|--validate`. The v2 protocol preserves these flags for `sc:troubleshoot-protocol` Wave 6 and any other caller already on the legacy grammar. The mapping is mechanical:

| Legacy invocation | v2 resolution |
|-------------------|---------------|
| `/sc:reflect --type task --analyze` | `--mode pre` (pre-execution analysis audit) |
| `/sc:reflect --type task --validate` | `--mode post` (post-execution validation audit) |

Legacy callers do not need to be migrated. Mixing legacy + new flags (e.g., `--type task --analyze --mode post`) is a STOP condition — explicit `--mode` wins and `--type/--analyze/--validate` are reported as ignored in the contract.

## Behavioral Summary

The full multi-wave protocol lives in the skill. The command file performs only:

1. **Parse arguments** → resolve `--mode` (apply legacy mapping if `--type task` is present), validate input combinations, normalize paths.
2. **Validate environment** → MCP availability (or `--no-mcp` set); output dir is writable AND not under `.claude/skills,agents,commands/`.
3. **Hand off to the skill** via the Activation section below.
4. **On skill return**, surface: REPORT.md path, mode, tier reached, calibrated confidence, deviation counts per §10 class (UC-2), coverage_pct (UC-1), evidence-validator drop count, Wave 7 promotion verdict (UC-2), and (if `--remediate`) the Tier 3 remediation offer.

**Three tiers under the hood** (full details in `refs/reflection-rubric.md` and §5):

| Tier | When | What it does | Approx cost |
|------|------|--------------|------------|
| Tier 1 | Always (unless STOP) | Single grounded card from `root-cause-analyst` + `confidence-calibrator`, with auggie/serena grounding. | ~3-6k Claude tokens, 1-3 min |
| Tier 2 | Auto-escalate on calibrated confidence < threshold, multi-domain, or `--depth deep` / `--tier 2` | 2-3 heterogeneous reviewers (different model classes) fan out in parallel; each card is independently calibrated; competing verdicts merged via `sc:adversarial-protocol`; `evidence-validator` drops unfounded citations. | +15-60k tokens, +4-15 min |
| Tier 3 | Opt-in via `--remediate` AND user accepts | `task-builder` produces an MDTM remediation task file; operator runs `/task` themselves; `/sc:reflect --mode post` re-runs as the post-commit gate. | +20-40k tokens, +5-10 min |

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:reflect-protocol

Do NOT proceed with protocol execution using only this command file. The full behavioral specification — wave structure, mode-selection rubric, agent delegation map, heterogeneous reviewer ensemble, blind calibration, evidence-validator gate, deviation taxonomy, output contract, promotion mutation, error-handling matrix — is in the protocol skill at `src/superclaude/skills/sc-reflect-protocol/SKILL.md`.

## MCP Integration

- **Auggie** (primary, free retrieval): Wave 0-2 codebase grounding via `mcp__auggie__codebase-retrieval`. Offloads heavy retrieval to the free tier, keeping Claude tokens tight.
- **Serena**: Wave 0-6 symbol-level navigation (`find_symbol`, `find_referencing_symbols`, `get_symbols_overview`, plus `find_declaration` / `find_implementations` / `type_hierarchy` for declaration-anchored and polymorphic grounding), the UC-2 §6.1 step-5.5 verification triangle (`get_diagnostics_for_file` / `execute_shell_command` / `summarize_changes`; `--no-verify` disables), opt-in `onboarding` cold-start bootstrap (`--onboard`), the memory pattern for cross-session learning capture (§6.3), and the `think_about_*` checkpoint triad as one of several signals (NOT the sole reflection mechanism — see §6.4 fail-open policy).
- **Context7**: Tier 2 only; consulted when the spec/diff references a framework or library by name.
- **Tavily**: Tier 2 only; rate-limited; used for external-symptom lookups when documentation grounding can't resolve a deviation.
- **Sequential**: Tier 2 synthesis when reconciling competing reviewer verdicts before the merge.

## Tool Coordination

- **`mcp__auggie__codebase-retrieval`**: in-repo grounding (all waves)
- **`mcp__serena__find_symbol` / `find_referencing_symbols` / `get_symbols_overview`**: symbol navigation
- **`mcp__serena__find_declaration` / `find_implementations`**: diff-hunk → canonical declaration site (§6.1 step 2a, FR-2) and polymorphic implementor surface (§6.1 step 3b, FR-1)
- **`mcp__serena__type_hierarchy`**: transitive supertype/subtype family (§6.1 step 4.5, Wave 1B.3) — backend- and `--with-hierarchy`-gated; fail-open when unavailable
- **`mcp__serena__get_diagnostics_for_file` / `execute_shell_command` / `summarize_changes`**: UC-2 §6.1 step-5.5 verification triangle (LSP issues + scoped non-mutating tests/linters/type-checkers + change summary) feeding §10.4 Regression detection; `--no-verify` disables
- **`mcp__serena__onboarding`**: opt-in cold-start memory bootstrap at Wave 0.7b (`--onboard`, default OFF)
- **`mcp__serena__think_about_*`**: checkpoint signals (§6.4) — three-row table feeds the merge, never the sole verdict
- **`mcp__serena__read_memory` / `write_memory` / `list_memories`**: cross-session learning capture (§6.3 — 20-entry, 90-day retention)
- **`mcp__context7__resolve-library-id` / `query-docs`**: external library grounding (Tier 2)
- **`mcp__tavily__tavily-search`**: targeted web search (Tier 2, rate-limited)
- **`Task`**: spawn `root-cause-analyst`, `self-review`, `requirements-analyst`, `confidence-calibrator`, `rf-qa`, `rf-qa-qualitative`, `audit-validator`, `evidence-validator`, `socratic-mentor`
- **`Skill`**: invoke `sc:adversarial-protocol` (Wave 4 merge debate), `task-builder` (Wave 6 remediation), `confidence-check` / `tech-research` (auxiliary)
- **`Read` / `Grep` / `Glob`**: native fallback when MCPs are unavailable; file:line re-Read for evidence-validator
- **`Bash`**: diff resolution, git ref expansion, output-dir creation
- **`Write`**: REPORT.md, hypothesis cards, calibration reports, tier_decision.yaml, promotion-log.yaml, telemetry artifacts

## Examples

### UC-1 pre-execution coverage audit (most common pre-flight check)

```text
/sc:reflect --mode pre --spec docs/spec.md --tasklist .dev/tasklists/my-feature.md
# - Resolves mode = pre
# - Wave 1B builds spec-to-tasklist coverage map via refs/coverage-mapping.md
# - Tier 1 ships if calibrated confidence ≥ 0.85 AND coverage_pct ≥ --coverage-floor
# - REPORT.md surfaces coverage_pct, missing_requirements list, and recommended additions
# - ROI: 200-500 tokens to potentially save 5-50k of misdirected execution
```

### UC-2 post-execution deviation audit with auto-promotion

```text
/sc:reflect --mode post --diff HEAD~1..HEAD --tasklist .dev/tasklists/my-feature.md
# - Resolves mode = post
# - Wave 1 builds per-task verdict matrix
# - Wave 3+ runs the heterogeneous reviewer ensemble + blind calibration
# - Wave 5 evidence-validator drops unfounded file:line citations
# - Wave 7 §14.5.2 strict gate evaluated; pass → mv to done destination
# - REPORT.md surfaces deviation counts (Authorized / Necessary / Drift / Regression) + per-task verdicts
```

### Force Tier 2 + offer remediation chain

```text
/sc:reflect --mode post --diff HEAD~1..HEAD --depth deep --remediate
# - --depth deep forces Tier 2 regardless of Tier 1 calibrated confidence
# - 3 heterogeneous reviewers fan out in parallel; sc:adversarial-protocol merges competing verdicts
# - evidence-validator runs as final gate
# - After REPORT.md, the Tier 3 remediation offer is surfaced:
#   "Reflect identified N regression items. Spawn task-builder to author a remediation MDTM task? (y/N)"
# - User accepts → task file built; operator runs /task; /sc:reflect --mode post re-runs as post-commit gate
```

### Legacy `sc:troubleshoot` Wave 6 invocation (preserved)

```text
/sc:reflect --type task --analyze   # mapped → --mode pre
# - sc:troubleshoot Wave 6 Phase B calls this before /task runs
# - Treated as pre-execution analysis audit of the task-builder output

/sc:reflect --type task --validate  # mapped → --mode post
# - sc:troubleshoot Wave 6 Phase D calls this after /task completes
# - Treated as post-execution validation audit of the /task work-unit
```

### Suppress promotion (diagnose-only mode)

```text
/sc:reflect --mode post --diff HEAD~1..HEAD --no-promote
# - Runs the full UC-2 audit, ships REPORT.md, but skips Wave 7 promotion mutation
# - Useful for read-only review passes where the operator wants to review before promoting
```

### Dry-run promotion (preview the mv + gate evaluation)

```text
/sc:reflect --mode post --diff HEAD~1..HEAD --promote-dry-run
# - Wave 7 evaluates the 9-condition strict gate and prints the mv command + per-condition pass/fail
# - No filesystem mutation; promotion-log.yaml is NOT written
# - Useful for debugging gate conditions before flipping --no-promote off
```

## Boundaries

**Will:**

- Resolve mode via the §3.2 6-rule first-match selection logic and surface it explicitly in the contract
- Always run Tier 1 first; auto-escalate to Tier 2 only when the §5 rubric or `--depth deep` / `--tier 2` says so
- Fan out 2-3 heterogeneous reviewers in Tier 2 — different model classes per `refs/reviewer-spec.md` rotation table — to defeat per-model representational bias
- Blind-calibrate every reviewer card via `confidence-calibrator` with the disjoint-set rule from `refs/reflection-rubric.md`
- Run `evidence-validator` as the final gate before REPORT.md ships; drop (not downgrade) unfounded `file:line` citations
- Classify every UC-2 deviation into one of 4 canonical categories: `authorized` / `necessary` / `drift` / `regression` per §10
- Default-on Wave 7 promotion mutation for UC-2 when the §14.5.2 strict gate passes; `--no-promote` suppresses
- Preserve the legacy `--type task --analyze|--validate` grammar for `sc:troubleshoot-protocol` Wave 6 and other v1 callers
- Write the §9 stable output contract (versioned via `contract_version`) so downstream consumers can parse without ambiguity
- Stay within the §15 cost profile and emit `budget_forced_tier_downgrade: true` when `--budget-remaining` forces a tier drop

**Will Not:**

- Trust agent-reported confidence without re-grading via `confidence-calibrator` (single-model self-grading is structurally biased per Mehta, Towards-AI Mar-2026)
- Ship a REPORT.md whose `file:line` citations have not passed through `evidence-validator` (or its documented fallback when `--no-evidence-validator` is set)
- Seat a reviewer whose model class collides with the calibrator's model class (Khan ICML 2024 disjoint-set rule — enforced by the `refs/reviewer-spec.md` rotation logic)
- Use the Serena `think_about_*` triad as the sole reflection mechanism (the v1 failure mode) — they are checkpoint signals only; the protocol applies §6.4 fail-open policy
- Auto-execute the Tier 3 remediation chain — `task-builder` produces a task file; the operator runs `/task` themselves
- Auto-commit after Tier 3 — `/sc:reflect --mode post` is the post-commit gate the operator re-runs
- Mutate filesystem for promotion when `--promote-dry-run` is set
- Write outputs under `.claude/skills,agents,commands/` (CLAUDE.md ABSOLUTE RULE — STOP condition)
- Maintain a persistent cross-session knowledge graph; memory uses 20-entry / 90-day retention per §6.3
- Block on hedge cases for LOW/MEDIUM-stakes deviations — surface them as `[INFERRED]` rather than refusing to deliver
- Validate non-executable commentary or prose narratives — only artifacts the user is expected to act on are in scope

## CRITICAL BOUNDARIES

**AUDIT FIRST — REMEDIATION REQUIRES `--remediate` FLAG AND EXPLICIT USER CONFIRMATION**

This command is audit-first by default.

- **Default behavior (no `--remediate` flag)**: Run the resolved mode end-to-end, produce REPORT.md, run Wave 7 promotion if UC-2 and the §14.5.2 gate passes, STOP. The operator reviews and either re-runs with `--remediate` or addresses findings manually.
- **With `--remediate` flag**: After REPORT.md, offer the Tier 3 remediation chain. `task-builder` produces the task file. **Stop and surface the literal `/task <path>` command — the operator runs it, never the skill.**
- **After `/task` completes**: The operator re-runs `/sc:reflect --mode post --diff <new-diff>` as the post-commit gate.

No silent code changes. No auto-execution of the remediation task. No auto-commit.

## Related Commands

- **`/sc:troubleshoot`** — Invokes `/sc:reflect --type task --analyze` (Wave 6 Phase B) and `/sc:reflect --type task --validate` (Wave 6 Phase D); the legacy grammar is preserved for this caller.
- **`/sc:adversarial`** — Invoked by reflect Wave 4 to debate competing reviewer verdicts in Tier 2. Reflect consumes the producer's `artifacts_dir` field and remaps it into its own `adversarial_artifacts_dir` contract field (mechanical resolution; not user-facing).
- **`task-builder` skill** — Invoked by reflect Wave 6 when `--remediate` is accepted; consumes the M1-frozen BUILD_REQUEST schema documented in `refs/remediation-handoff.md`.
- **`/sc:task`** — May auto-trigger `/sc:reflect` as an end-of-task hook when configured (deferred per Open Question 2 in the rebuild task file).
- **`/sc:analyze`** — Complementary; use for read-only quality/security/architecture analysis when there is no spec or diff to reflect against.
- **`/sc:brainstorm`** — Upstream of `/sc:reflect` when the spec or tasklist itself is genuinely ambiguous and the user wants to scope it first.
