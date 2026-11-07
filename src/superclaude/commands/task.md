---
name: task
description: "Unified task execution with intelligent workflow management, MCP compliance enforcement, and multi-agent delegation"
category: special
complexity: advanced
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill
mcp-servers: [context7, playwright, morphllm]
personas: [architect, analyzer, qa, refactorer, frontend, backend, security, devops, python-expert, quality-engineer]
version: "2.0.0"
---

# /sc:task - Unified Task Command

## Purpose

A unified command with **orthogonal dimensions** that merges orchestration capabilities with MCP compliance enforcement:

```text
/sc:task [operation] --strategy [systematic|agile|enterprise] --compliance [strict|standard|light|exempt]
```

| Dimension | Purpose | Options |
|-----------|---------|---------|
| **Strategy** | HOW to coordinate work | systematic, agile, enterprise, auto |
| **Compliance** | HOW strictly to enforce quality | strict, standard, light, exempt, auto |

**Philosophy**: "Better false positives than false negatives" - when uncertain, escalate to higher compliance tier.

## Triggers

| Trigger Type | Condition | Confidence |
|--------------|-----------|------------|
| **Complexity Score** | Task complexity >0.6 with code modifications | 90% |
| **Multi-file Scope** | Estimated affected files >2 | 85% |
| **Security Domain** | Paths contain `auth/`, `security/`, `crypto/` | 95% |
| **Refactoring Scope** | Keywords: refactor, remediate, multi-file | 90% |

## Usage

```bash
/sc:task [operation] [target] [flags]
```

Key flags: `--strategy`, `--compliance`, `--verify`, `--skip-compliance`, `--force-strict`, `--parallel`, `--delegate`, `--no-escalation`. See protocol skill for full flag reference.

| Flag | Default | Description |
|------|---------|-------------|
| `--no-escalation` | `false` | Bypass TFEP (Test Failure Escalation Protocol) triggers. When set, agents may fix test failures directly without structured diagnostic escalation analysis. **WARNING**: Using `--no-escalation` voids TFEP protection against ad-hoc fixes. |
| `--unattended` | `false` | Worker mode for a coordinator; applies only as a standalone argument token. Behaviour is in `## Unattended mode`; without it nothing changes. |
| `--report-dir` | (none) | With `--unattended`: the directory that holds `return-contract.yaml` and `task-report.md`. |

## Classification (MANDATORY FIRST OUTPUT)

**CRITICAL RULES:**

1. **TEXT-ONLY**: Do NOT invoke ANY tools (Skill, Read, Grep, etc.) for classification. Tool invocation begins AFTER classification.
2. **EXACT FORMAT**: Use the HTML comment block below EXACTLY. Do NOT use `**CLASSIFICATION: ...**` or any other format.
3. **VALID TIERS ONLY**: The ONLY valid TIER values are: `STRICT`, `STANDARD`, `LIGHT`, `EXEMPT`. Values like "ITERATIVE", "SIMPLE", "IMPLEMENT", "COMPLEX" are INVALID and MUST NOT be used.
4. **FIRST OUTPUT**: This header MUST be your very first output, before any other text.

Emit this EXACT header format (replace bracketed values only):

```text
<!-- SC:TASK-UNIFIED:CLASSIFICATION -->
TIER: [STRICT|STANDARD|LIGHT|EXEMPT]
CONFIDENCE: [0.00-1.00]
KEYWORDS: [matched keywords or "none"]
OVERRIDE: [true|false]
RATIONALE: [one-line reason]
<!-- /SC:TASK-UNIFIED:CLASSIFICATION -->
```

**Tier rules** (check in priority order; first matching tier wins; check --compliance override first):

1. **STRICT** (Priority 1 — safety-critical):
   - Keywords: security, authentication, authorization, database, migration, refactor, breaking change, encrypt, token, session, oauth
   - Context boosters: >2 estimated files (+0.3), security paths like auth/, security/, crypto/ (+0.4)
   - Compound phrases: "fix security", "add authentication", "update database", "change api"
   - Note: "quick security" → still STRICT (security always wins); "minor auth change" → still STRICT

2. **EXEMPT** (Priority 2 — non-code operations):
   - Keywords: explain, search, commit, push, plan, discuss, brainstorm, what, how, why
   - Context boosters: is_read_only (+0.4), is_git_operation (+0.5), all doc files (+0.5)
   - Patterns: starts with "what/how/why/explain", docs-only paths (*.md, docs/)

3. **LIGHT** (Priority 3 — trivial changes):
   - Keywords: typo, comment, whitespace, lint, docstring, formatting, spacing, minor
   - Context boosters: single file (+0.1), <=50 lines estimated
   - Compound phrases: "quick fix", "minor change", "fix typo", "refactor comment"

4. **STANDARD** (Priority 4 — default development):
   - Keywords: implement, add, create, update, fix, build, modify, change
   - Default tier when no higher-priority tier matches

If confidence <0.70, prompt user: "Override with `--compliance [tier]`"

## Execution

After emitting the classification header as text, proceed based on tier:

- **EXEMPT**: Execute immediately — answer the question or perform the read-only operation. No Skill invocation needed.
- **LIGHT**: Execute the change directly. No Skill invocation needed for trivial changes.
- **STANDARD / STRICT**: Invoke the full protocol for tier-appropriate workflow:
  > Skill sc:task-protocol

## Classification Output Examples

**The ONLY valid tier values are: STRICT, STANDARD, LIGHT, EXEMPT. Do NOT invent other labels (e.g., "ITERATIVE", "IMPLEMENT", "SIMPLE" are INVALID).**

For `/sc:task "fix security vulnerability in auth module"`:

```text
<!-- SC:TASK-UNIFIED:CLASSIFICATION -->
TIER: STRICT
CONFIDENCE: 0.95
KEYWORDS: security, vulnerability, auth
OVERRIDE: false
RATIONALE: Security-critical change in authentication module
<!-- /SC:TASK-UNIFIED:CLASSIFICATION -->
```

For `/sc:task "explain how the routing middleware works"`:

```text
<!-- SC:TASK-UNIFIED:CLASSIFICATION -->
TIER: EXEMPT
CONFIDENCE: 0.92
KEYWORDS: explain, how
OVERRIDE: false
RATIONALE: Read-only explanation request, no code changes
<!-- /SC:TASK-UNIFIED:CLASSIFICATION -->
```

For `/sc:task "fix typo in error message"`:

```text
<!-- SC:TASK-UNIFIED:CLASSIFICATION -->
TIER: LIGHT
CONFIDENCE: 0.95
KEYWORDS: typo, fix
OVERRIDE: false
RATIONALE: Trivial single-string correction
<!-- /SC:TASK-UNIFIED:CLASSIFICATION -->
```

For `/sc:task "add pagination to user list endpoint"`:

```text
<!-- SC:TASK-UNIFIED:CLASSIFICATION -->
TIER: STANDARD
CONFIDENCE: 0.85
KEYWORDS: add, endpoint
OVERRIDE: false
RATIONALE: Typical feature addition, moderate scope
<!-- /SC:TASK-UNIFIED:CLASSIFICATION -->
```

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:task-protocol

Do NOT proceed with protocol execution using only this command file. The full behavioral specification — classification rubric, tier logic, TFEP escalation protocol, sub-agent delegation, MCP compliance enforcement — is defined in the protocol skill at `~/.claude/skills/sc-task-protocol/SKILL.md`.

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:task` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
- **Report directory.** `--report-dir <dir>` only. Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome, and on every tier, not only on TFEP. `report_path` is `<report-dir>/task-report.md` for every run, a short summary the run writes (tier, verification result, files changed). `artifacts` lists every changed file, `tfep-incident-report.md` when TFEP ran, and the nested contracts; paths git ignores are left out (WC-4).
- **Person-mode flags.** None is refused.
- **Gates.** Under `--unattended` confidence below 0.70 resolves as blocked, with the `--compliance [tier]` override question in `blocked_question`. The TFEP "present to user" points resolve as blocked, with the review question in `blocked_question`, and every FULL STOP resolves as blocked, with the report to the user in `blocked_question`. The TFEP report `tfep-incident-report.md` is written and listed in `artifacts` and is not committed. There is no other gate.
- **Nested invocations.** The STRICT `sc:impact-protocol` call receives `--unattended --output-dir <report-dir>/nested/impact-<n>/` in place of `.dev/impact/task-<slug>`, and the TFEP `/sc:troubleshoot` call receives `--unattended --output-dir <report-dir>/nested/troubleshoot-<n>/` in place of `{output_dir}`, each `<n>` counting from 1 per nested command and never reused (a retry or an escalated re-invocation takes the next number); each contract is listed in `artifacts`, also when the call failed. A nested contract is read by the nested-result rule of `~/.claude/WORKER-CONTRACT.md`.
- **Outward actions.** It pushes, commits and stages nothing: EXEMPT `commit` and `push` are refused (contract `worker_status: failed`, the operation in `reason`).

## Boundaries

**Will:**

- Classify tasks into appropriate compliance tiers with confidence scoring
- Enforce tier-appropriate verification requirements
- Spawn verification agents for STRICT tier tasks
- Support user overrides with documented justification
- Coordinate MCP servers based on tier requirements

**Will:**

- Enforce TFEP (Test Failure Escalation Protocol) when test failures meet escalation thresholds
- Block ad-hoc fixes when pre-existing tests fail during task execution

**Will Not:**

- Skip safety-critical verification for STRICT tasks
- Apply STRICT overhead to genuinely trivial changes
- Override user's explicit compliance choice
- Proceed with <70% confidence without user confirmation
- Execute unbounded batches (max 15 changes per batch)
- Use deprecated `/sc:task-mcp` (use `--compliance [tier]` instead)
- Allow ad-hoc code fixes in response to test failures without TFEP workflow (unless `--no-escalation` is set)
