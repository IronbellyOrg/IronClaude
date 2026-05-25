---
name: troubleshoot
description: "Tiered debugging — fast Tier 1 triage with auggie + serena grounding, auto-escalation to parallel hypothesis agents + adversarial fix debate, and an opt-in task-builder remediation chain"
category: analysis
complexity: advanced
mcp-servers: [auggie, serena, context7, tavily, sequential]
personas: [analyzer, performance, security, qa, refactorer, devops]
argument-hint: "[<issue description>] [--type bug|build|performance|deployment|security|test] [--depth quick|standard|deep] [--scope <path|symbol>] [--no-escalate] [--fix] [--models <tier:model,...>] [--output-dir <path>] [--no-doc-discovery] [--no-mcp]"
---

# /sc:troubleshoot - Tiered Issue Diagnosis

## Triggers

Auto-activates whenever the user reports a broken build, runtime error, performance regression, deployment problem, or failing test — even without saying "troubleshoot". Phrases that activate it:

1. **Direct invocation**: `/sc:troubleshoot ...`
2. **Symptom keywords**: "why is X broken", "this used to work", "something's off with", "regression", "flaky"
3. **Pasted evidence**: a stack trace, an exception name (`NameError`, `TypeError`, `ImportError`), a failing-command transcript, a CI log fragment, a profiler readout
4. **Programmatic call**: Another `/sc:*` command invokes the `sc:troubleshoot-protocol` skill directly

The trigger is intentionally pushy because the most common reason users skip a debugging tool is they don't know it would help.

## Required Input

**MANDATORY**: At least one of the following:

- **Issue description** — free text, error message, stack trace, log excerpt
- **`--scope`** — file, directory, or symbol paired with at least a brief description

**STOP** if neither is present — without a symptom and a scope the command has nothing to triage.

**STOP** if `--depth deep` is requested but the issue description is under 10 words and no `--scope` was given. Too vague for a deep pass to add value; ask the user to add detail first.

## Usage

```bash
/sc:troubleshoot "NameError: name 'Path' is not defined in eval_run.py"     # auto-detect type=bug
/sc:troubleshoot "API p99 jumped 10x after the widget refactor" --type performance
/sc:troubleshoot "flaky CI test, passes locally" --type test --depth deep
/sc:troubleshoot --type security --scope src/auth/ "SAST flagged IDOR"
/sc:troubleshoot "build broken" --type build --fix                          # diagnose + offer Tier 3 remediation
/sc:troubleshoot "test failing" --no-escalate                                # cap at Tier 1; do not fan out
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--type` | auto-detect | One of `bug`, `build`, `performance`, `deployment`, `security`, `test`. Auto-detected from keywords + structural cues in the issue description. |
| `--depth` | `standard` | `quick` (Tier 1 only, ~1-3 min, ~3-6k Claude tokens), `standard` (auto-escalate by rubric), `deep` (force Tier 2 with adversarial debate). |
| `--scope` | (none) | File, directory, or symbol to narrow auggie/serena queries against. |
| `--no-escalate` | `false` | Cap at Tier 1 regardless of confidence. Useful for quick second-opinion passes. |
| `--fix` | `false` | After diagnosis, offer the Tier 3 remediation chain (`task-builder` → `/sc:reflect --type task --analyze` → user runs `/task` → `/sc:reflect --type task --validate`). Code changes never auto-apply; the user runs `/task`. |
| `--models` | (agent defaults) | Per-tier model override, e.g. `tier1:sonnet,hypothesis:opus`. |
| `--output-dir` | `.dev/troubleshoot/<slug>-<timestamp>/` | Where REPORT.md, hypothesis cards, fix proposals, adversarial artifacts, and audit log are written. |
| `--no-doc-discovery` | `false` | Skip Wave 1.5 documentation grounding (release artifacts + architectural docs + semantic restrictions). Useful when the codebase has no formal docs or the user has already grounded the symptom externally; the resulting diagnosis is NOT weighted against documented behavior and the report records the skip in Grounding Gaps. |
| `--no-mcp` | `false` | Run in native-tools-only mode (skip auggie/serena/context7/tavily). Tier 1 quality degrades; surfaced in the report. |

## Behavioral Summary

The full multi-wave protocol lives in the skill. The command file performs only:

1. **Parse arguments** → resolve `--type` (auto-detect if absent), `--scope`, `--depth`, etc.
2. **Validate environment** → at least one of MCPs is available (or `--no-mcp` is set); output dir is writable.
3. **Hand off to the skill** via the Activation section below.
4. **On skill return**, surface: REPORT path, tier reached, confidence, chosen fix, and (if `--fix`) the Tier 3 remediation offer.

**Three tiers under the hood**:

| Tier | When | What it does | Cost |
|------|------|--------------|------|
| Tier 1 | Always (unless STOP) | Single grounded hypothesis from `root-cause-analyst` + `confidence-calibrator`, with auggie/serena grounding | ~3-6k Claude tokens, 1-3 min |
| Tier 2 | Auto-escalate on `confidence < 0.85`, multi-domain, intermittent, security < 0.95, or `--depth deep` | 2-4 specialist agents fan out in parallel; each produces a hypothesis card; competing fixes debated via `sc:adversarial-protocol`; `self-review` sanity-checks the merge | +15-60k tokens, +4-15 min |
| Tier 3 | Opt-in via `--fix` AND user accepts | `task-builder` produces an MDTM task file; user runs `/task`; `/sc:reflect --type task --validate` gates the commit | +20-40k tokens, +5-10 min |

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:troubleshoot-protocol

Do NOT proceed with protocol execution using only this command file. The full behavioral specification — wave structure, escalation rubric, agent selection, file:line validation, hallucination contract, remediation chain — is in the protocol skill.

## MCP Integration

- **Auggie** (primary, free retrieval): Tier 1, Wave 1.5 (documentation grounding fan-out across release artifacts + architectural docs + semantic restrictions), and Tier 2 codebase grounding via `mcp__auggie__codebase-retrieval`. Offloads heavy retrieval to a free / low-cost tier, keeping the Claude token budget tight.
- **Serena**: Tier 1 + Tier 2 symbol-level navigation via `find_symbol`, `find_referencing_symbols`, `get_symbols_overview`. Critical when the issue names a specific function or class.
- **Context7**: Tier 2 only, when the symptom mentions a framework or library by name or the stack trace ends in third-party code.
- **Tavily**: Tier 2 only, rate-limited to ≤ 2 queries per invocation. Used for `<exact error string> github issue` and `<library> <version> <symptom>` lookups.
- **Sequential**: Tier 2 synthesis when reconciling competing hypotheses.

## Tool Coordination

- **`mcp__auggie__codebase-retrieval`**: in-repo grounding (Tier 1 + Tier 2)
- **`mcp__serena__find_symbol` / `find_referencing_symbols` / `get_symbols_overview`**: symbol navigation
- **`mcp__context7__resolve-library-id` / `query-docs`**: external library docs (Tier 2)
- **`mcp__tavily__tavily-search`**: targeted web search (Tier 2, rate-limited)
- **`Task`**: spawn `root-cause-analyst`, Tier 2 specialist agents, `confidence-calibrator`, `evidence-validator`, `self-review`
- **`Skill`**: invoke `sc:adversarial-protocol` (Wave 4), `task-builder` (Wave 6), `/sc:reflect` (Wave 6)
- **`Read` / `Grep` / `Glob`**: native fallback when MCPs are unavailable; file:line validation
- **`Bash`**: cheap reproducer commands (Tier 1) and diagnostic commands (Tier 2)
- **`Write`**: hypothesis cards, REPORT.md, audit log, calibration reports, validation reports

## Examples

### Quick Tier 1 diagnosis (most common)

```
/sc:troubleshoot "NameError: name 'Path' is not defined at eval_run.py:142"
# - Auto-detects --type bug
# - Spawns root-cause-analyst with auggie + serena grounding
# - confidence-calibrator re-grades the hypothesis card
# - If confidence ≥ 0.85 and single-domain → STOP at Tier 1
# - REPORT.md with the chosen fix written to --output-dir
```

### Tier 2 auto-escalation on intermittent symptom

```
/sc:troubleshoot "flaky CI test, passes locally, fails ~1/5 runs since session-pool refactor"
# - Tier 1 produces a hypothesis but the "intermittent" keyword forces escalation
# - 3 specialist agents (quality-engineer, root-cause-analyst, refactoring-expert) fan out in parallel
# - confidence-calibrator scores each card independently
# - sc:adversarial-protocol debates competing fix proposals
# - evidence-validator drops any unfounded file:line citations before REPORT.md ships
```

### Force deep pass + remediation offer

```
/sc:troubleshoot "scratch-root allowlist accepts /etc/foo" --type security --depth deep --fix
# - --depth deep forces Tier 2 regardless of Tier 1 confidence
# - --type security raises the escalation threshold (security_caution rule)
# - After REPORT.md, the Tier 3 remediation chain offers task-builder
# - User accepts → MDTM task file built; /sc:reflect --type task --analyze runs
# - User runs /task themselves (never auto-executed); /sc:reflect --type task --validate gates commit
```

### Suppress escalation (quick second opinion)

```
/sc:troubleshoot "off-by-one in pagination" --no-escalate
# - Caps at Tier 1; never fans out to Tier 2 even if rubric would have escalated
# - Useful when the user is confident the bug is small and wants a fast read
```

### Native-tools-only mode

```
/sc:troubleshoot "something's wrong with the worker" --no-mcp
# - Skip auggie/serena/context7/tavily; use Read/Grep/Glob/Bash only
# - Tier 1 quality degrades; flagged in REPORT.md's Grounding Gaps
# - Useful when MCPs are unavailable or the user wants pure local execution
```

## Boundaries

**Will:**

- Always run Tier 1 first (respect the "quick first option" contract)
- Auto-escalate to Tier 2 only when the rubric in `refs/escalation-rubric.md` says so, or when `--depth deep` is set
- Fan out 2-4 specialist agents in parallel in Tier 2 (capped at 4 by signal mix)
- Use auggie + serena every tier for in-repo grounding; use context7 + tavily only in Tier 2 and only when the symptom suggests external knowledge
- Run Wave 1.5 documentation grounding (release artifacts + architectural docs + semantic restrictions) before any fix is proposed, unless `--no-doc-discovery` is set
- Invoke `sc:adversarial-protocol` only when Tier 2 produces 2-3 competing strong fixes (skip on consensus — that wastes the debate)
- Run `evidence-validator` in Wave 5 to drop any unfounded `file:line` citations before REPORT.md ships
- Run `confidence-calibrator` after every hypothesis card to defeat self-grading anchoring bias
- Offer the Tier 3 remediation chain only when `--fix` is set AND REPORT.md status is `success`

**Will Not:**

- Apply code changes without `--fix` AND explicit user confirmation
- Recommend a code change for a symptom whose observed behavior matches the documented behavior (the documented contract is the source of truth — fix the docs or open a stakeholder discussion, never silently regress the contract)
- Skip Tier 1 and jump straight to Tier 2 (even with `--depth deep`, Tier 1 still runs first and its output feeds Tier 2)
- Spawn Tier 2 hypothesis agents on consensus single-domain Tier 1 results
- Spawn more than 4 hypothesis agents in Tier 2 (token waste; signal already saturated)
- Trust agent-reported confidence without independent re-grading via `confidence-calibrator`
- Ship a REPORT.md whose `file:line` citations have not passed through `evidence-validator` (or its inline fallback)
- Auto-execute the Tier 3 task file — that is always a separate user-initiated `/task` invocation
- Auto-commit after Tier 3 — `/sc:reflect --type task --validate` is the final gate the user runs before committing

## CRITICAL BOUNDARIES

**DIAGNOSE FIRST — FIXES REQUIRE `--fix` FLAG AND EXPLICIT USER CONFIRMATION**

This command is diagnosis-first by default.

- **Default behavior (no `--fix` flag)**: Run Tiers 1-2, produce REPORT.md, STOP. The user reviews and either re-runs with `--fix` or applies the fix manually.
- **With `--fix` flag**: After REPORT.md, offer the Tier 3 remediation chain. Build the task file. **Stop and surface the literal `/task <path>` command — the user runs it, never the skill.**
- **After `/task` completes**: The user runs `/sc:reflect --type task --validate` as the pre-commit gate.

No silent code changes. No auto-execution. No auto-commit.

## Related Commands

- **`/sc:adversarial`** — Invoked in Wave 4 of Tier 2 when 2-3 competing strong fixes need to be debated. Complementary; use directly when you need multi-model debate on artifacts that aren't fix proposals.
- **`/sc:analyze`** — Complementary; use for read-only quality/security/architecture analysis when you don't have a specific symptom yet.
- **`/sc:reflect --type task`** — Used twice in Tier 3 (analyze + validate gates).
- **`task-builder` skill** — Invoked between REPORT.md and execution to produce an MDTM task file.
- **`/sc:brainstorm`** — Complementary; use upstream of `/sc:troubleshoot` when the symptom is genuinely ambiguous and the user wants to scope it first.
- **`/sc:auggie-review`** — Complementary; use for whole-PR review vs this command's symptom-driven diagnosis.
