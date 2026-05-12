---
name: sc:recommend-protocol
description: "Full behavioral protocol for sc:recommend — ultra-intelligent command recommendation engine with multi-language support, context detection, and estimation"
allowed-tools: Read, Glob, Grep, Bash, TodoWrite, mcp__auggie-mcp__codebase-retrieval
---

# /sc:recommend — Command Recommendation Protocol

## Triggers

sc:recommend-protocol is invoked ONLY by the `sc:recommend` command via `Skill sc:recommend-protocol` in the `## Activation` section. It is never invoked directly by users.

Activation conditions:
- User runs `/sc:recommend [query]` in Claude Code
- Any `--estimate`, `--alternatives`, `--stream`, `--community` flags are passed through

Do NOT invoke this skill directly. Use the `sc:recommend` command.

## Multi-language Support

### Language Detection
- Turkish: Detect via Turkish-specific characters (ç, ğ, ı, ö, ş, ü)
- English: Detect via common English words (the, and, is, are, etc.)
- Default: English when uncertain
- Mixed language inputs handled with keyword mapping

## Keyword Extraction and Persona Matching

### Pattern Matching Categories

| Pattern | Category | Personas |
|---------|----------|----------|
| machine learning, ml, ai | ml_category | analyzer, architect |
| website, frontend, ui/ux, react, vue | web_category | frontend, qa |
| api, backend, server, microservice | api_category | backend, security |
| error, bug, issue, not working | debug_category | analyzer, security |
| slow, performance, optimization | performance_category | performance, analyzer |
| security, auth, vulnerability | security_category | security, analyzer |
| new, create, build, develop | create_category | frontend, backend, architect |
| test, qa, quality, validation | test_category | qa, performance |
| how, learn, explain, tutorial | learning_category | mentor, analyzer |
| refactor, cleanup, improve | improve_category | refactorer, mentor |

### Context Analysis
- beginner/starter → beginner_level + mentor persona
- expert/senior → expert_level + architect persona
- continue/resume → continuity_mode + sequential thinking
- next step → next_step_mode + thinking flags

## Context Retrieval & Verification

**Purpose**: Every candidate `/sc:*` command or project skill surfaced by the mapping table MUST be verified against its actual source before appearing in output. This phase runs AFTER candidate generation and BEFORE recommendation emission. It prevents flag fabrication, ghost-command recommendations, and inline protocol duplication.

### Scope

Verification applies to:
- Every `/sc:<name>` command the mapping table proposes for this query
- Every project skill (`sc:<name>-protocol` or similar) the mapping table proposes

Verification is **exempt** for:
- Built-in tools: `Read`, `Grep`, `Glob`, `Edit`, `Write`, `Bash`, `TodoWrite`, `WebFetch`, `WebSearch`
- MCP server names referenced abstractly (e.g., "use Sequential for reasoning")

### Retrieval Mechanism

Every shortlisted candidate MUST be resolved through **two complementary mechanisms**. Neither is optional when Auggie MCP is available:

1. **Direct read** (`Read`/`Grep`/`Glob`) — extracts the canonical interface from the command's source file: flag table, required inputs, activation block. Answers *"what is this command?"*.
2. **Auggie enrichment** (`mcp__auggie-mcp__codebase-retrieval`) — extracts context the command file alone does not carry: how the command is invoked elsewhere in the repo, related skills, known caveats, eval artifacts that demonstrate good/bad usage, recent behavioral changes. Answers *"how do you wield this command well in THIS codebase?"*.

A recommendation built from the file alone can cite the correct flag set and still produce a prompt that misuses the command — because it doesn't know which flag combinations are load-bearing, which edge cases the eval history has already surfaced, or which adjacent skills are conventionally paired. Auggie enrichment closes that gap. This is the failure mode the skill was refactored to prevent; do not reintroduce it by skipping Step 2.

### Retrieval Algorithm

For each shortlisted candidate, execute BOTH steps in order.

**Step 1 — Direct read (canonical interface)**:
- `Glob src/superclaude/commands/<name>.md`
- If hit: `Read` the command file. Extract:
  - Flag table from the Options section
  - Required Input section (if present)
  - Activation block → extract the protocol skill name (pattern: `Skill sc:<name>-protocol`)
- If the command's activation points to a protocol skill, `Read` that skill's frontmatter (`allowed-tools`, `argument-hint`, `description`) for a richer interface record.
- If the literal path misses, `Grep -r "<name>" src/superclaude/commands/` to rule out a rename before concluding the candidate is a ghost.

**Step 2 — Auggie enrichment (contextual fit)** — **MANDATORY when Auggie MCP is available**:
- Issue one query per shortlisted candidate, shaped by the user's original request. Example phrasing:
  - `mcp__auggie-mcp__codebase-retrieval(query="How is /sc:<name> used across this codebase? Return invocation examples, common flag combinations, related skills, known caveats, and any eval artifacts demonstrating successful or failed usage — in the context of: <user's original request>.")`
- Use the returned context to populate the `usage_notes`, `related_skills`, `known_caveats`, and `invocation_examples` fields of the verified interface record (see below). If Auggie returns no matches for an otherwise-resolved command, note that gap — the command is new or rarely exercised, and the recommendation should say so rather than pretend to authority it lacks.
- Auggie enrichment is what lets the recommendation go beyond "correct flags" to "correct USE." Skipping it when Auggie is available is a **rule violation**, not a shortcut.
- Hard cap: **one Auggie query per shortlisted candidate, ≤3 shortlisted candidates per `/sc:recommend` invocation → ≤3 Auggie calls total**.

**Step 3 — Resolution**:
- Step 1 hit + Step 2 hit → full verified record; proceed.
- Step 1 hit + Auggie unavailable or empty → degraded record; emit a one-line degradation notice in the recommendation header ("Auggie enrichment unavailable — recommendation cites verified flags but omits repo-specific usage nuance").
- Step 1 miss + Step 2 miss → candidate is a ghost. **Drop it silently.** Do not emit. Do not warn.

### Verified Interface Record

Per resolved target, build:

```yaml
target: "sc:adversarial"
exists: true
source_path: "src/superclaude/commands/adversarial.md"
protocol_skill: "sc:adversarial-protocol"
flags:                  # only flags present in the command's Options table (from Step 1)
  - "--compare"
  - "--source"
  - "--generate"
  - "--agents"
  - "--pipeline"
  - "--depth"
  - "--convergence"
  - "--interactive"
  - "--output"
  - "--focus"
  - "--blind"
  - "--auto-stop-plateau"
activation_style: "skill-indirected"  # command file delegates to a protocol skill
# Fields below populated from Step 2 (Auggie enrichment):
usage_notes: |
  Summary of how the command is actually invoked in this repo (modes, typical
  flag combinations, cost/time characteristics). "unavailable" if Auggie skipped.
related_skills:         # commands/skills conventionally paired with this one
  - "sc:reflect"        # example — verify via Auggie, do not fabricate
known_caveats: |
  Pitfalls, recent changes, or eval-history lessons. "none surfaced" if Auggie
  found no relevant artifacts; "unavailable" if Auggie was skipped.
invocation_examples:    # concrete invocations mined from the repo
  - "verbatim example from eval or docs, or 'none found'"
```

### Session Cache

Cache verified interfaces within a single `/sc:recommend` invocation: `{target_name: verified_interface}`. Each entry holds BOTH the Step 1 canonical interface and the Step 2 Auggie enrichment. A single recommendation often surfaces overlapping primary and secondary commands; the cache ensures each target is read, parsed, and Auggie-queried at most once per run. The cache does not persist across invocations.

### Graceful Degradation

| Failure mode | Response |
|---|---|
| Auggie MCP not configured | Proceed with Step 1 only. Emit header notice: "Auggie enrichment unavailable — recommendation cites verified flags but omits repo-specific usage nuance." Recommendation quality is reduced: flags are correct but usage guidance is thin. |
| Auggie call fails mid-run | Retry once. On second failure, degrade for that candidate only (same header notice). Do not stall the whole recommendation. |
| Auggie returns empty result for a resolved command | Emit the recommendation with `usage_notes: "none surfaced in codebase"`. This is an honest signal that the command is new or rarely exercised, not a failure. |
| Candidate not found via Step 1 AND Step 2 | Drop the candidate silently from the recommendation. |
| Command file found but has no flag table | Emit the bare command name with no flags. Valid and non-fabricated. |

## Output Constraints (Anti-Fabrication Rules)

These rules govern recommendation output after verification. They are **non-negotiable** and apply to every `/sc:recommend` invocation.

### Rule 1 — No unverified flags

A flag may appear in the recommendation **only if** it is present in the verified target's flag table (or argument-hint). Example: because `src/superclaude/commands/adversarial.md` defines `--compare`, `--depth`, `--convergence`, `--focus`, `--pipeline`, `--blind`, `--interactive`, `--output`, `--auto-stop-plateau` (and the Mode B flags `--source`/`--generate`/`--agents`), **no other flag may be attached to a `/sc:adversarial` recommendation**. Flags like `--rounds`, `--evidence-required`, `--verdict-per-claim`, `--measure-first` are fabricated and forbidden.

### Rule 2 — No unverified commands

A command may appear in the recommendation **only if** its source file was resolved (literal or Auggie). A candidate that cannot be located gets dropped silently. Example: `/sc:scan` does not exist in `src/superclaude/commands/` — the security_category mapping surfaces it, verification drops it.

### Rule 3 — No protocol reimplementation

When a verified target has `activation_style: skill-indirected` (meaning its command file delegates to a protocol skill via `Skill sc:<name>-protocol`), the generated prompt or command string MUST be a **hand-off**, not a **specification**.

- **Allowed**: `Run: /sc:adversarial --compare fileA.md,fileB.md --focus structure --depth standard`
- **Forbidden**: any inline content that restates what the target's protocol will do — debate rules, round counts, scoring formulas, "steelman strategy", phase breakdowns, artifact lists. The target's protocol skill owns that behavior; the recommendation must trust the hand-off and let the skill run.

Rule 3 enforces the principle: **invoke, don't reimplement**. Duplicating a target's protocol inline causes drift, wastes tokens, and produces recommendations that disagree with the actual command when the command is run.

### Rule 4 — Built-ins exempt

Verification is **not required** for built-in tools (`Read`, `Grep`, `Glob`, `Edit`, `Write`, `Bash`, `TodoWrite`, `WebFetch`, `WebSearch`). These are harness primitives with stable interfaces; reading their source adds overhead with no fabrication risk. Recommendations like "use `Grep` to find usages of `FooBar`" pass through without retrieval.

## Command Map by Category

### ml_category
- Primary: `/sc:analyze --seq --c7`, `/sc:design --seq --ultrathink`
- Secondary: `/sc:build --feature --tdd`, `/sc:improve --performance`
- MCP: --c7, --seq | Flags: --think-hard, --evidence

### web_category
- Primary: `/sc:build --feature --magic`, `/sc:design --api --seq`
- Secondary: `/sc:test --coverage --e2e --pup`, `/sc:analyze --code`
- MCP: --magic, --c7, --pup | Flags: --react, --tdd

### api_category
- Primary: `/sc:design --api --ddd --seq`, `/sc:build --feature --tdd`
- Secondary: `/sc:scan --security --owasp`, `/sc:analyze --performance`
- MCP: --seq, --c7, --pup | Flags: --microservices, --ultrathink

### debug_category
- Primary: `/sc:troubleshoot --investigate --seq`, `/sc:analyze --code --seq`
- Secondary: `/sc:scan --security`, `/sc:improve --quality`
- MCP: --seq, --all-mcp | Flags: --evidence, --think-hard

### performance_category
- Primary: `/sc:analyze --performance --pup --profile`, `/sc:troubleshoot --seq`
- Secondary: `/sc:improve --performance --iterate`, `/sc:build --optimize`
- MCP: --pup, --seq | Flags: --profile, --benchmark

### security_category
- Primary: `/sc:scan --security --owasp --deps`, `/sc:analyze --security --seq`
- Secondary: `/sc:improve --security --harden`
- MCP: --seq | Flags: --strict, --validate, --owasp

### create_category
- Primary: `/sc:build --feature --tdd`, `/sc:design --seq --ultrathink`
- Secondary: `/sc:analyze --code --c7`, `/sc:test --coverage --e2e`
- MCP: --magic, --c7, --pup | Flags: --interactive, --plan

### test_category
- Primary: `/sc:test --coverage --e2e --pup`, `/sc:scan --validate`
- Secondary: `/sc:improve --quality`
- MCP: --pup | Flags: --validate, --coverage

### improve_category
- Primary: `/sc:improve --quality --iterate`, `/sc:cleanup --code --all`
- Secondary: `/sc:analyze --code --seq`
- MCP: --seq | Flags: --threshold, --iterate

### learning_category
- Primary: `/sc:document --user --examples`, `/sc:analyze --code --c7`
- Secondary: `/sc:brainstorm --interactive`
- MCP: --c7 | Flags: --examples, --interactive

## Expertise Level Customization

| Level | Style | Extra Explanations |
|-------|-------|--------------------|
| Beginner | Detailed, step-by-step | Yes |
| Intermediate | Balanced, technical | Some |
| Expert | Fast, direct | Minimal |

## Project Context Detection

### File System Analysis
- React: package.json with react, src/App.jsx → frontend commands + magic
- Vue: package.json with vue, src/App.vue → frontend commands + magic
- Node API: express in package.json, routes/, controllers/ → backend + security
- Python: requirements.txt, setup.py → analyzer + architect
- Database: schema.sql, migrations/ → backend + security

### Project Size
- Small (<50 files): Direct implementation
- Medium (50-200): Plan → analyze → implement
- Large (>200): Comprehensive analysis → design → implement

## Streaming Mode

Continuous recommendation throughout project lifecycle:
1. Analysis & Planning → 2. Implementation → 3. Testing → 4. Deployment

## Alternative Recommendation Engine

When `--alternatives` flag:
- Present primary recommendation
- 2-3 alternative approaches with pros/cons
- Comparison matrix
- Community preference percentages

## Time and Budget Estimation

When `--estimate` flag:

### Complexity Factors
- Project type: simple component (1-3d) to enterprise (3-6mo)
- Experience multiplier: beginner 2.0x, intermediate 1.5x, expert 1.0x
- Scope: small 1.0x, medium 1.5x, large 2.5x, enterprise 4.0x

### Time Distribution
- ML: data 20-30%, preprocessing 15-25%, training 10-20%, eval 10-15%, deploy 15-25%
- Web: design 15-25%, frontend 30-40%, backend 25-35%, testing 10-20%, deploy 5-15%

## Smart Flag Recommendations

### Context-Based
- Small project: --quick --simple
- Medium: --plan --validate --profile
- Large: --plan --validate --seq --ultrathink

### Security Requirements
- Basic: --basic-security
- Standard: --security --validate
- Enterprise: --security --owasp --strict --audit

### History-Based
- Previous errors: --validate --dry-run --backup
- Security issues: --security --scan --strict
- Performance issues: --profile --optimize --monitor

## Response Format

Standard output structure:
1. Header: Project analysis, language detection, level, persona
2. Main: 3 primary commands, additional recommendations, quick start
3. Enhanced: Smart flags, time estimate, alternatives, community data
