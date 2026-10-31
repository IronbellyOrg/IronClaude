---
name: reflect
description: "Tiered reflection protocol — UC-1 pre-execution coverage/gap audit and UC-2 post-execution deviation audit with heterogeneous reviewer ensemble, blind calibration, and mandatory evidence-validator gate"
category: analysis
complexity: advanced
mcp-servers: [auggie, codegraph, context7, tavily]
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

# Offer the Tier 3 remediation chain after audit (plan route: sc:workflow -> /sc:implement .dev/tasks/to-do/<slug>/<slug>.md)
/sc:reflect --mode post --diff HEAD~1..HEAD --remediate

# Same, but via the MDTM route (task-builder -> /task); --depth deep alone does not remediate
/sc:reflect --mode post --diff HEAD~1..HEAD --depth deep --remediate

# Headless wrapper (superclaude reflect run --fix) follows the same depth rule:
#   default depth   -> plan route; contract field remediation_plan_path; the wrapper auto-runs /sc:implement <tasklist path>
#   --depth deep    -> MDTM route; contract field remediation_task_path; the wrapper auto-runs /task <path>
# Headless runs auto-accept (AUTO-FIXABLE registers only) and skip the plan-route refactor prompt and execution gate;
# sc:workflow's built-in advisory pre-review still runs but is not gated on; the wrapper's bounded re-audit is the verification.
```

### Detection-contract readiness bypass

Detection-contract readiness is not a UC-1/UC-2 reflection audit. Use the approved sibling CLI readiness surface instead of launching the normal `/sc:reflect` protocol:

```bash
superclaude reflect contract-status --repo <owner/repo> --pr <number>
superclaude reflect contract-status --validate --repo <owner/repo> --pr <number>
```

This path calls `superclaude.pr_submit.contract_setup`, prints readiness/blockers/checked paths/hashes/counts plus the next command to run, and does not write the local lock by default. It must not arm Monitor, mutate PR state, push, reply, resolve, retrigger, resume `/sc:pr-submit`, launch `ReflectRunner`, launch `ClaudeProcess`, or dump raw GitHub payload bodies.

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
| `--no-verify` | `false` (UC-2) | Disable the UC-2 verification run (Bash, scoped non-mutating linters/type-checkers/tests/build under the §6.1.1 envelope, §6.1 steps 5 and 5.5). Default-on; when set, degrades §10.4 Regression detection to the task-log claim with a Grounding Gap entry. Subsumes the deprecated `--rerun-tests` alias. |
| `--no-reachability` | `false` (UC-2) | Disable the §6.1 step-5.6 contracted-sink reachability & oracle-admissibility gate (the operator rollback path). Default-on; when set, records telemetry-only skip state (`reachability_gate_ran: false`, `reachability_skip_reason: --no-reachability`); it does NOT write a Grounding Gap, set needs_human_decision, or force status: partial. |
| `--remediate` | `false` | After the audit ships, offer the Tier 3 remediation chain. Default (plan route): `sc:workflow` builds the tasklist package `.dev/tasks/to-do/<slug>/<slug>.md` (its built-in `--mode pre` review is surfaced) → operator runs `/sc:implement <pkg>/<slug>.md` → `/sc:reflect --mode post` re-runs as the post-commit gate. With `--depth deep` (MDTM route): `task-builder` → operator runs `/task` → `/sc:reflect --mode post`. `--depth deep` alone does NOT remediate; the route follows the depth you requested, not the tier reached. |
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

For detection-contract readiness, do not enter the multi-wave skill path. The supported readiness command is `superclaude reflect contract-status [--validate] --repo <owner/repo> --pr <number>`; it is a diagnose/validate-first status surface that reports only status, paths, hashes, counts, and blockers and performs no default write or monitor/PR side effect.

The full multi-wave protocol lives in the skill. The command file performs only:

1. **Parse arguments** → resolve `--mode` (apply legacy mapping if `--type task` is present), validate input combinations, normalize paths.
2. **Validate environment** → MCP availability (or `--no-mcp` set); output dir is writable AND not under `.claude/skills,agents,commands/`.
3. **Hand off to the skill** via the Activation section below.
4. **On skill return**, surface: REPORT.md path, mode, tier reached, calibrated confidence, deviation counts per §10 class (UC-2), coverage_pct (UC-1), evidence-validator drop count, Wave 7 promotion verdict (UC-2), and (if `--remediate`) the route-specific Tier 3 remediation offer (plan route by default; MDTM route with `--depth deep`).

**Three tiers under the hood** (full details in `refs/reflection-rubric.md` and §5):

| Tier | When | What it does | Approx cost |
|------|------|--------------|------------|
| Tier 1 | Always (unless STOP) | Single grounded card from `root-cause-analyst` + `confidence-calibrator`, with auggie plus codegraph plus native Grep/Read grounding. | ~3-6k Claude tokens, 1-3 min |
| Tier 2 | Auto-escalate on calibrated confidence < threshold, multi-domain, or `--depth deep` / `--tier 2` | 2-3 heterogeneous reviewers (different model classes) fan out in parallel; each card is independently calibrated; competing verdicts merged via `sc:adversarial-protocol`; `evidence-validator` drops unfounded citations. | +15-60k tokens, +4-15 min |
| Tier 3 | Opt-in via `--remediate` AND user accepts | `--remediate`: `sc:workflow` produces the tasklist package `<slug>.md`; operator runs `/sc:implement <pkg>/<slug>.md` themselves; `/sc:reflect --mode post` re-runs as the post-commit gate. `--remediate --depth deep`: `task-builder` produces an MDTM remediation task file; operator runs `/task` themselves; `/sc:reflect --mode post` re-runs as the gate. | +20-40k tokens, +5-10 min |

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:reflect-protocol

Do NOT proceed with protocol execution using only this command file. The full behavioral specification — wave structure, mode-selection rubric, agent delegation map, heterogeneous reviewer ensemble, blind calibration, evidence-validator gate, deviation taxonomy, output contract, promotion mutation, error-handling matrix — is in the protocol skill at `~/.claude/skills/sc-reflect-protocol/SKILL.md`.

## MCP Integration

- **Auggie** (primary, free retrieval): Wave 0-2 codebase grounding via `mcp__auggie__codebase-retrieval`. Offloads heavy retrieval to the free tier, keeping Claude tokens tight.
- **codegraph**: Wave 0-6 symbol, caller and impact lookup above the native Grep/Read floor (guide `~/.claude/CODEGRAPH.md`); UC-2 Step 1B.3 calls `/sc:impact` and logs production and test caller counts only.
- **Context7**: Tier 2 only; consulted when the spec/diff references a framework or library by name.
- **Tavily**: Tier 2 only; rate-limited; used for external-symptom lookups when documentation grounding can't resolve a deviation.
- **Native reasoning**: Tier 2 synthesis when reconciling competing reviewer verdicts before the merge.

## Tool Coordination

- **`mcp__auggie__codebase-retrieval`**: in-repo grounding (all waves)
- **`mcp__codegraph__codegraph_status` / `_search` / `_node` / `_callers` / `_callees` / `_impact`**: one readiness check, then definitions, outlines, callers and impact above the floor (§6 Code-graph evidence chain); `Skill sc:impact-protocol` for the Step 1B.3 counts
- **`Grep` then `Read`**: symbol navigation floor — Grep for the definition (`def <name>|class <name>|function <name>`) then Read the range (§6.1 steps 2a/3, FR-2); Grep with a word-boundary pattern for references, then Read the call sites (step 4); best-effort Grep for `class .*\(<Base>\)` / `implements <Iface>` for the polymorphic implementor surface (step 3b, FR-1)
- **`Bash` (verification run)**: UC-2 §6.1 step 5 / 5.5 — the project's own linter or type-checker plus scoped non-mutating tests/build, run under the §6.1.1 safety envelope (timeout, output cap, verb allowlist, mutation denylist) and feeding §10.4 Regression detection; `--no-verify` disables
- **Read / Write / Edit on `docs/memory/reflect/deviation-patterns-<slug>.md`**: cross-session learning capture (§6.3 — 20-entry, 90-day retention); a tracked project file, no MCP server needed
- **`mcp__context7__resolve-library-id` / `query-docs`**: external library grounding (Tier 2)
- **`mcp__tavily__tavily_search`**: targeted web search (Tier 2, rate-limited)
- **`Task`**: spawn `root-cause-analyst`, `self-review`, `requirements-analyst`, `confidence-calibrator`, `rf-qa`, `rf-qa-qualitative`, `audit-validator`, `evidence-validator`, `socratic-mentor`
- **`Skill`**: invoke `sc:adversarial-protocol` (Wave 4 merge debate), `sc:workflow-protocol` (Wave 6 remediation, plan route — the default), `task-builder` (Wave 6 remediation, MDTM route — only with `--remediate --depth deep`), `confidence-check` / `tech-research` (auxiliary)
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

### Offer the remediation chain (plan route, the default)

```text
/sc:reflect --mode post --diff HEAD~1..HEAD --remediate
# - Runs the audit at the requested depth (standard), ships REPORT.md
# - After REPORT.md, the Tier 3 remediation offer is surfaced (Route: plan):
#   "Reflect identified N regression items. Proceed with sc:workflow? [yes / no]"
# - User accepts → sc:workflow builds the .dev/tasks/to-do/<slug>/ package and runs its own
#   advisory /sc:reflect --mode pre (reflect_status is shown);
#   the literal `/sc:implement <pkg>/<slug>.md` is shown and the operator runs it themselves;
#   /sc:reflect --mode post re-runs as the post-commit gate
```

### Force Tier 2 + MDTM remediation route (`--remediate --depth deep`)

```text
/sc:reflect --mode post --diff HEAD~1..HEAD --depth deep --remediate
# - --depth deep forces Tier 2 regardless of Tier 1 calibrated confidence
# - 3 heterogeneous reviewers fan out in parallel; sc:adversarial-protocol merges competing verdicts
# - evidence-validator runs as final gate
# - After REPORT.md, the Tier 3 remediation offer is surfaced (Route: mdtm):
#   "Reflect identified N regression items. Proceed with task-builder? [yes / no]"
# - User accepts → task file built; operator runs /task; /sc:reflect --mode post re-runs as post-commit gate
# - Without --remediate, --depth deep audits at Tier 2 and does NOT remediate
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
- Auto-execute the Tier 3 remediation chain on either route — `sc:workflow` produces a tasklist package and the operator runs `/sc:implement` themselves; `task-builder` (`--depth deep`) produces a task file and the operator runs `/task` themselves; the skill never runs `/sc:implement` or `/task`
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
- **With `--remediate` flag**: After REPORT.md, offer the Tier 3 remediation chain. By default (plan route) `sc:workflow` produces the tasklist package (running its own advisory `--mode pre` review), and the skill **stops and surfaces the literal `/sc:implement <pkg>/<slug>.md` command — the operator runs it, never the skill.** With `--depth deep` (MDTM route) `task-builder` produces the task file and the skill **stops and surfaces the literal `/task <path>` command — the operator runs it, never the skill.** `--depth deep` without `--remediate` never remediates.
- **After `/sc:implement` (or `/task`) completes**: The operator re-runs `/sc:reflect --mode post --diff <new-diff>` as the post-commit gate.

No silent code changes. No auto-execution of the remediation plan or task. No auto-commit.

## Related Commands

- **`superclaude reflect contract-status [--validate] --repo <owner/repo> --pr <number>`** — Approved detection-contract readiness surface. It diagnoses/validates existing file-based evidence without running UC-1/UC-2 audit machinery, writing a lock by default, arming Monitor, mutating PR state, or dumping raw payload bodies.
- **`/sc:troubleshoot`** — Its Tier 3 Wave 6 calls reflect twice. Plan route (`--fix`): the workflow tasklist is pre-reviewed with `--mode pre` (Phase B) and validated with `/sc:reflect --mode post ...` (Phase D). MDTM route (`--fix --depth deep`): the legacy `--type task --analyze` (Phase B) and `--type task --validate` (Phase D), preserved for this caller.
- **`/sc:adversarial`** — Invoked by reflect Wave 4 to debate competing reviewer verdicts in Tier 2. Reflect consumes the producer's `artifacts_dir` field and remaps it into its own `adversarial_artifacts_dir` contract field (mechanical resolution; not user-facing).
- **`/sc:workflow`** → **`/sc:implement`** — Default Tier 3 route with `--remediate`: reflect Wave 6 invokes `sc:workflow-protocol` (with `--handoff none`) to build the tasklist package `.dev/tasks/to-do/<slug>/<slug>.md`; the operator runs `/sc:implement <pkg>/<slug>.md`.
- **`task-builder` skill** — Only with `--remediate --depth deep`: invoked by reflect Wave 6 when the remediation offer is accepted; consumes the M1-frozen BUILD_REQUEST schema documented in `refs/remediation-handoff.md`.
- **`/sc:task`** — May auto-trigger `/sc:reflect` as an end-of-task hook when configured (deferred per Open Question 2 in the rebuild task file).
- **`/sc:analyze`** — Complementary; use for read-only quality/security/architecture analysis when there is no spec or diff to reflect against.
- **`/sc:brainstorm`** — Upstream of `/sc:reflect` when the spec or tasklist itself is genuinely ambiguous and the user wants to scope it first.
