---
name: sc:reflect-protocol
description: "Tiered reflection and validation — pre-execution plan verification (UC-1) and post-execution adherence audit (UC-2). Grounded by Serena symbol navigation + auggie retrieval. Escalates to parallel multi-model review + adversarial merge via sc:adversarial. Delegates debate/scoring/merge; adds coverage-mapping, deviation-classification, and evidence-revalidation on top."
version: 1.0.0
mcp-servers: [serena, auggie-mcp, sequential]
complexity: advanced
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, TodoWrite, Task, Skill, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview, mcp__serena__get_diagnostics_for_file, mcp__serena__write_memory, mcp__serena__read_memory, mcp__serena__list_memories, mcp__serena__activate_project, mcp__sequential-thinking__sequentialthinking
argument-hint: "[--mode pre|post] [--scope path|symbol] [--depth quick|standard|deep] [--output dir]"
---

# /sc:reflect — Tiered Reflection & Validation Protocol

## Triggers

Invoked ONLY by the `/sc:reflect` command via `Skill sc:reflect-protocol`.
Never invoked directly by users.

Activation conditions:

- User runs `/sc:reflect` with a tasklist, spec, diff, or work artifact
- User runs `/sc:reflect --mode pre` for pre-execution validation (UC-1)
- User runs `/sc:reflect --mode post` for post-execution audit (UC-2)
- Auto-detection when input contains both a spec AND completed-work artifacts (defaults to `post`)

## 1. Purpose & Identity

Independent, grounded validation of proposed or completed work against a
source-of-truth specification. Two modes:

- **UC-1 (pre-execution)**: Does the plan/tasklist cover every spec
  requirement? Are there gaps, risks, or anti-patterns before token spend?
- **UC-2 (post-execution)**: Did the completed work actually deliver what
  the spec promised? What deviated, and is each deviation authorized?

**Core contract — independence.** The reviewer must be a *different model
class* than the executor for UC-2. Single-model self-review has structural
confirmation bias (Mehta 2026). UC-1 is less sensitive to this but still
benefits from independent calibration.

**What this skill is NOT** (delegated to siblings):

- Debate/scoring/merge → `sc:adversarial-protocol`
- Root-cause investigation → `root-cause-analyst` agent (owned by `sc:troubleshoot`)
- Brainstorming alternatives → `sc:brainstorm-protocol`
- Remediation task generation → `task-builder`
- Evidence re-validation → `evidence-validator` agent
- Confidence calibration → `confidence-calibrator` agent

This skill owns: coverage-mapping, deviation-classification,
spec-as-oracle adjudication, and the orchestration glue between these
delegated capabilities.

## 2. Required Input (STOP if missing)

**MANDATORY**: One of the following:

1. **A tasklist or strategy doc** (for UC-1) — path to `.md` file with
   enumerated items or sections
2. **Completed-work artifacts** (for UC-2) — one of:
   - A commit range or diff (`--scope <commit-ish>`)
   - An output directory of produced files
   - A task log / execution transcript

**AND** in both cases: a **source-of-truth spec/PRD/objectives doc**
referenced explicitly or detected from the tasklist frontmatter.

**STOP** if neither spec nor work-artifact is locatable:
`"reflect requires a spec and either a plan (UC-1) or completed work (UC-2). Provide --scope, @<spec-path>, or both."`

**Mode auto-detection** (when `--mode` is unset):

- Input contains only spec + plan/tasklist → `pre`
- Input contains diff, commit range, output-dir, or `--scope` pointing to changed files → `post`
- Ambiguous → STOP and ask user to set `--mode`

## 3. Output Contract

Versioned two-block contract written to `<output>/return-contract.yaml`
AND returned inline.

### Stable Contract (contract_version: 1.0)

```yaml
contract_version: "1.0"
status: success | partial | failed
mode: pre | post
tier_reached: 1 | 2 | 3
report_path: <path>
spec_path: <path>
work_input_path: <path | null>
coverage_pct: <float 0.0-1.0>
deviations_found: <int>
deviations_by_class:
  authorized_expansion: <int>
  necessary_deviation: <int>
  drift: <int>
  regression: <int>
gaps_found: <int>
recommendation: pass | proceed_with_caveats | escalate | block
escalation_reason: <string | null>
adversarial_artifacts_dir: <path | null>
remediation_task_path: <path | null>
```

### Telemetry Block (non-stable)

```yaml
wave_durations_ms:
  wave_0: <ms>
  wave_1: <ms>
  wave_2: <ms>
  wave_3: <ms>
  wave_4: <ms>
token_usage:
  wave_1: <est>
  wave_3: <est>
agents_spawned: [<list>]
serena_tools_used: [<list>]
```

## 4. Tier-Decision Rubric

Tier is decided at Wave 2 (confidence gate) based on **four concrete signals**:

| Signal | Threshold | Tier triggered |
|--------|-----------|----------------|
| Coverage completeness (from Wave 1 scan) | < 70% of spec items mapped | T2 |
| Scope breadth | > 3 files changed OR > 150 lines touched | T2 |
| Spec complexity | > 10 enumerated requirements OR multi-domain spec | T2 |
| User override | `--depth deep` | T2 always |
| T2 produces competing deviation analyses | ≥ 2 substantively different deviation interpretations | T3 (adversarial) |
| User opts in to remediation | After report, user accepts T3 offer | T3 (task-builder) |

**Default path**: T1. Escalation is opt-in via rubric, never the starting
point. `--depth quick` forces T1 even if rubric says escalate (mirrors
sc-troubleshoot `--no-escalate`).

## 5. Wave Architecture

```
Wave 0: Parse + Validate Input + Mode Detection
Wave 1: T1 — Grounded Coverage Scan (always runs)
Wave 2: Confidence Gate (decides T1 stop vs T2 escalate)
Wave 3: T2 — Parallel Deviation Analysis (conditional)
Wave 4: Synthesis + Report (always finalizes)
Wave 5: T3 — Remediation Handoff (conditional, user opt-in)
```

Refs loaded per-wave, never pre-loaded.

### Wave 0 — Parse + Validate

**Purpose**: Validate inputs, detect mode, ensure Serena is active.

**Steps**:

1. Parse `$ARGUMENTS` into flags. Required: spec path + (plan OR work-artifact).
2. Auto-detect `--mode` if unset (see §2).
3. Resolve `--scope` to path/commit/symbol. If UC-2 with no scope given,
   attempt `git diff HEAD~1` as default scope; if no git history available,
   STOP: `"UC-2 requires --scope (commit range, diff file, or output dir)."`.
4. **Serena activation**: call `mcp__serena__activate_project` with current
   working directory. If fails, WARN and set `serena_available: false`;
   fall back to Grep/Glob for all subsequent Serena calls.
5. **Output-path policy guard**: if `--output` resolves under `.claude/skills/`,
   `.claude/agents/`, or `.claude/commands/`, STOP before any write.
6. Create output dir (default `.dev/reflect-<mode>-<slug>-<timestamp>/`).

**Exit criteria**: mode set, spec resolved, scope resolved (UC-2), output
dir created, Serena status known. Emit: `"Wave 0 complete: mode=<pre|post> serena=<ok|fallback>"`.

**STOP conditions**: missing spec, missing scope in UC-2, output dir
creation failure.

---

### Wave 1 — T1 Grounded Coverage Scan

**Purpose**: Build a coverage map between spec requirements and plan items
(UC-1) or diff/artifacts (UC-2). Single-agent, symbol-grounded.

**Refs loaded**: `refs/coverage-map-template.md` (coverage map schema).

**Steps**:

1. **Parse the spec** into enumerated requirements. Extract each numbered/
   bulleted item as a discrete requirement with an ID (`REQ-N`).
2. **Ground in real code** (parallel MCP calls):
   - `mcp__auggie__codebase-retrieval` with query: "Find code and structure
     related to: <spec topic summary>" scoped to `--scope` if set.
   - `mcp__serena__get_symbols_overview` on each file in scope to build a
     structural map of what exists.
3. **Build coverage map** (inline, not delegated):
   - UC-1: for each `REQ-N`, check if any plan/tasklist item addresses it.
     Tag: `covered`, `partially_covered`, `unmapped`.
   - UC-2: for each `REQ-N`, check if any changed symbol/file/artifact
     maps to it. Use `mcp__serena__find_referencing_symbols` on touched
     symbols to confirm traceability. Tag: `delivered`, `partially_delivered`,
     `not_delivered`, `changed_beyond_spec`.
4. **Compute coverage_pct** = `covered + delivered / total requirements`.
5. **Detect deviations** (UC-2 only): for items tagged `changed_beyond_spec`,
   classify each as:
   - `authorized_expansion` — tasklist was updated to include this work
   - `necessary_deviation` — technical blocker forced the change, documented in commit/task
   - `drift` — silent change with no documentation or authorization
   - `regression` — change contradicts the spec
   Classification uses commit messages, task-log entries, and PR descriptions
   as the authorization oracle. Items without a documented rationale default
   to `drift` (conservative).
6. Write coverage map to `<output>/coverage-map.md`.

**Exit criteria**: coverage map written, coverage_pct computed, deviations
classified (UC-2). Emit: `"Wave 1 complete: coverage=<X%> deviations=<N>"`.

**Fallback**: If Serena unavailable, use Grep/Glob for symbol discovery.
If auggie unavailable, use Serena `find_symbol` + `get_symbols_overview` only.

---

### Wave 2 — Confidence Gate

**Purpose**: Decide T1 stop vs T2 escalation using the rubric in §4.

**Decision logic** (from §4 thresholds):

- `--depth quick` → STOP at T1. Warn if coverage_pct < 70%.
- `--depth deep` → ALWAYS escalate to T2.
- Otherwise:
  - `coverage_pct >= 0.85` AND `deviations_found == 0` AND scope ≤ 3 files → STOP at T1.
  - `coverage_pct < 0.70` → escalate.
  - `deviations_found > 0` with any `regression` or `drift` → escalate.
  - Scope > 150 lines changed OR > 10 requirements → escalate.

**On STOP**: jump to Wave 4 (synthesis) with `tier_reached=1`.

**On escalate**: record `escalation_reason`, proceed to Wave 3.

---

### Wave 3 — T2 Parallel Deviation Analysis (conditional)

**Purpose**: Independent, multi-model review of deviations and gaps.

**Agent selection** — 2-3 agents, model-diverse:

| Agent | Model | Role |
|-------|-------|------|
| `confidence-calibrator` | sonnet | Re-grade Wave 1 coverage map against 5-dim rubric |
| `root-cause-analyst` | sonnet OR opus | Investigate each `drift`/`regression` deviation |
| (optional) `quality-engineer` | haiku | Edge-case and spec-ambiguity probe for UC-1 |

**Why these agents and no new ones**: `confidence-calibrator` already does
independent re-grading (proven in sc-troubleshoot Waves 1.7 + 3.5).
`root-cause-analyst` already does evidence-based investigation (proven in
sc-troubleshoot Wave 1.7). `quality-engineer` adds edge-case coverage for
UC-1 pre-execution checks. No new agents needed — the gap identified in
the enrichment (coverage-mapper, deviation-classifier) is handled inline
in Wave 1 steps 3-5, keeping the skill lean.

**Steps**:

1. **Spawn agents in parallel** via `Task`:
   - Each receives: spec path, coverage-map path, scope, mode.
   - `confidence-calibrator`: re-grade the coverage map. Output:
     `<output>/t2-calibration.md`.
   - `root-cause-analyst`: investigate each drift/regression. Output:
     `<output>/t2-root-cause.md`.
   - (optional) `quality-engineer`: spec-ambiguity probe. Output:
     `<output>/t2-edge-cases.md`.
2. **Calibrate each output independently** — spawn per-card `confidence-calibrator`
   instances if more than 2 agents ran. Use calibrated scores (not self-reports)
   for Wave 4 weighting.
3. **If ≥ 2 agents produce competing deviation interpretations** (e.g.,
   one says "drift", another says "necessary_deviation" for the same item):
   delegate to `sc:adversarial-protocol` Mode A:
   ```
   Skill sc:adversarial-protocol --compare t2-calibration.md,t2-root-cause.md \
       --depth quick --focus correctness,coverage \
       --output <output>/adversarial/
   ```
   Consume the adversarial return contract. If `convergence_score >= 0.65`,
   use the merged output as the authoritative deviation classification.
   If `< 0.65`, surface both interpretations in the report flagged as
   `unresolved_conflict`.

**Exit criteria**: calibration + root-cause outputs written. Adversarial
invoked if competing interpretations exist. Emit:
`"Wave 3 complete: agents=<N> adversarial=<yes|no>"`.

**Failure handling**:

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| Agent subprocess crash | Continue with remaining agents | If < 2 agents complete, downgrade to T1-only |
| sc:adversarial fails | Use highest-confidence agent's deviation classification | Flag as `adversarial_unavailable` in report |
| All agents converge | Skip adversarial; use consensus | None |

---

### Wave 4 — Synthesis + Report

**Purpose**: Produce the reflection report regardless of tier reached.

**Refs loaded**: `refs/report-template.md`.

**Steps**:

1. Load report template.
2. Compose `REPORT.md` filling in:
   - Header (mode, tier, coverage_pct, recommendation)
   - Summary (2-4 sentences)
   - Coverage Map (tabular: `REQ-N | status | evidence`)
   - Deviations (UC-2 only: classification, root cause, authorization status)
   - Gaps (unmapped requirements with severity)
   - Recommendation (`pass | proceed_with_caveats | escalate | block`)
   - Next Steps (T1: `--depth deep` for more; T2 without remediation:
     re-invoke with `--fix`; T2 with `--fix`: confirm for Wave 5)
3. **Evidence re-validation** — spawn `evidence-validator` via `Task` with
   `report_draft_path=<output>/REPORT.md.draft`. The agent re-Reads every
   `file:line` citation. Drop mismatches. If any dropped, set
   `status: partial` and add "Grounding Gaps" section.
   - **Fallback**: if `evidence-validator` unavailable, inline-validate
     citations. Mark `status: partial` with Grounding Gap entry.
4. **Serena memory write** — `mcp__serena__write_memory` with key
   `reflection-last-pass-{project-slug}` containing: mode, coverage_pct,
   deviation counts, recommendation, timestamp. Supports cross-session
   continuity.
5. Write `<output>/return-contract.yaml`.
6. Surface to user: summary paragraph, report path, recommendation.

**Exit criteria**: `REPORT.md` written, return contract finalized, user
notified. If `--fix` not set, return contract and STOP.

---

### Wave 5 — T3 Remediation Handoff (conditional)

**Preconditions**: `--fix` is set AND `REPORT.md` recommendation is
`proceed_with_caveats`, `escalate`, or `block` AND user accepts.

**Steps**:

1. Present remediation offer — one yes/no question. Wait.
2. On accept: invoke `task-builder` via `Skill` with `BUILD_REQUEST` whose
   GOAL is "Address the gaps/deviations described in `<REPORT.md>`".
3. Capture task file path. Surface to user with `/task <path>` command.
   Do NOT auto-execute.
4. On decline: return success; report is the final deliverable.

**Exit criteria**: task file path returned (or decline recorded).

## 6. Modern Serena Tool Usage

**Zero references to deprecated `think_about_*` tools.** The rebuild
eliminates the legacy surface entirely (it is a single-file island in
`commands/reflect.md`; no other skill in the repo uses it).

Serena tool selection per wave:

| Tool | Wave | Purpose |
|------|------|---------|
| `activate_project` | W0 | Ensure LSP-backed symbol resolution |
| `get_symbols_overview` | W1 | Structural map of touched files |
| `find_symbol` | W1 | Targeted symbol lookup when spec names specific functions |
| `find_referencing_symbols` | W1 | Trace which spec requirements map to which changed symbols |
| `get_diagnostics_for_file` | W4 | Post-review diagnostic check on touched files |
| `write_memory` | W4 | Persist reflection results for cross-session continuity |
| `read_memory` | W0 | Load prior reflection pass context |
| `list_memories` | W0 | Discover existing reflection-related memories |

All Serena calls are **fail-open**: if Serena is unavailable, fall back
to Grep/Glob, log degraded mode in audit, continue. No abort on Serena
failure.

## 7. Cross-Skill Integration

This is the load-bearing section. For every phase, the table below states
which sibling skill/agent does the heavy lifting and what sc:reflect adds.

| Phase | Heavy lifting by | What sc:reflect adds |
|-------|-------------------|----------------------|
| Coverage mapping (W1) | Inline orchestrator using Serena symbol tools | Spec-to-code traceability matrix (no sibling does this) |
| Deviation classification (W1) | Inline orchestrator with commit/task-log oracle | 4-class taxonomy with authorization grounding (no sibling does this) |
| Confidence calibration (W1, W3) | `confidence-calibrator` agent (owned by sc:troubleshoot) | Reuses agent without change; adds coverage-specific rubric dimensions |
| Root-cause investigation (W3) | `root-cause-analyst` agent (owned by sc:troubleshoot) | Reuses agent; scopes its input to deviation items only |
| Adversarial debate (W3) | `sc:adversarial-protocol` Mode A | Passes competing deviation analyses as compare inputs |
| Evidence re-validation (W4) | `evidence-validator` agent (owned by sc:troubleshoot) | Reuses agent; scopes to reflection report citations |
| Remediation task gen (W5) | `task-builder` skill | Reuses skill; provides reflection-specific BUILD_REQUEST |
| Edge-case probing (W3 opt) | `quality-engineer` agent | Reuses agent for UC-1 spec-ambiguity detection |
| Memory persistence (W4) | Serena `write_memory`/`read_memory` | Adds `reflection-last-pass-{slug}` key convention |

**Sibling delegation count: 7** (confidence-calibrator, root-cause-analyst,
sc:adversarial-protocol, evidence-validator, task-builder, quality-engineer,
Serena memory). **New agents authored: 0.**

## 8. Agent Delegation

| Agent | Phase | Reuse rationale |
|-------|-------|-----------------|
| `confidence-calibrator` | W1.5 (inline), W3 (Task) | Proven in sc:troubleshoot W1.7 + W3.5. Independent re-grading reduces anchoring. No modification needed. |
| `root-cause-analyst` | W3 (Task) | Proven in sc:troubleshoot W1.7. Evidence-based investigation. Scoped to deviation items only. |
| `evidence-validator` | W4 (Task) | Proven in sc:troubleshoot W5. Re-Reads every file:line. Drops hallucinated citations. |
| `quality-engineer` | W3 optional (Task) | Proven in sc:troubleshoot W3 (edge-case hypothesis). Adds spec-ambiguity probe for UC-1. |
| `self-review` | W4 (after adversarial merge) | Proven in sc:troubleshoot W4. Four-question sanity check on merged output. |

**No new agents.** The coverage-mapper and deviation-classifier gaps from
the enrichment are handled inline in Wave 1 — they are narrow enough that
dedicated agents would add coordination overhead without sufficient
complexity reduction. If Wave 1 inline logic proves fragile in eval, a
future iteration can extract them.

## 9. Eval Rubric

Harness at `.dev/eval-workspaces/sc-reflect/` (CLAUDE.md override:
never `.claude/skills/reflect-workspace/`).

**Dimensions (5)**:

| Dimension | Weight | Measurement | Acceptance threshold |
|-----------|--------|-------------|---------------------|
| Coverage completeness | 0.25 | % of spec items correctly mapped in coverage-map.md | ≥ 85% |
| Deviation classification precision | 0.25 | % of classified deviations matching human gold label | ≥ 75% |
| Citation accuracy | 0.20 | % of file:line citations in REPORT.md that resolve correctly | ≥ 90% |
| Recommendation actionability | 0.15 | % of recommendations with concrete next-step (file path, command, or boolean gate) | ≥ 80% |
| False-positive rate | 0.15 | % of "drift"/"regression" flags that human review overturns | ≤ 20% |

**Grading scale**: 0-5 per dimension (highest human-LLM ICC per Anthropic
arxiv 2601.03444). Total weighted score / 5.0.

**Ship acceptance**: aggregate score ≥ 3.5 (70%) on held-out test set.
Target: iteration N ships when iteration N+1 shows < 5% absolute improvement.

**Iteration cycle** (modeled on sc-brainstorm):

- Iteration 1: 3 pilot cases (UC-1 trivial, UC-2 small-diff, UC-2 large-diff)
- Iteration 2: expand to 8-12 cases adding depth variation, multi-domain specs,
  edge cases (empty diff, all-drift, all-covered)

**Assertion DSL extensions** (extend sc-brainstorm grader.py):

- `coverage_pct_min` — coverage_pct in return-contract.yaml ≥ threshold
- `deviation_class_count` — count of `drift` + `regression` in return-contract.yaml
- `citation_resolves` — every `file:line` citation in REPORT.md resolves to
  a real file on disk (new semantic assertion type)
- `section_present` — reuse from brainstorm
- `yaml_field_min` — reuse from brainstorm

**Grader model**: Opus grading Sonnet/Haiku outputs (different + more capable
model per Arize/Evidentiary guidance). Never self-grade.

## 10. Build Path Decision

**Pick: Skill-creator eval-iteration loop for initial build, then Sprint CLI
for production execution.**

**Rationale**: sc:reflect is a workflow skill whose value is in the protocol
steps and deviation taxonomy — exactly the kind of thing that needs
draft-eval-rewrite cycles against real prompts. The skill-creator plugin
provides `run_loop.py`, comparator/grader/analyzer sub-agents, and HTML
review generation out of the box. Sprint CLI is the execution harness for
*running* the built skill against tasklists, not for iterating on its
design. Eval CLI (PTY isolation) is deferred until pilot runs outgrow
the lightweight grader.py.

**Eval workspace path**: `.dev/eval-workspaces/sc-reflect/` per CLAUDE.md
override. Skill-creator's default sibling workspace (`.claude/skills/reflect-workspace/`)
is blocked by the PreToolUse hook and .gitignore.

## 11. Error Handling Matrix

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| Missing spec file | STOP with clear message | None |
| Missing scope in UC-2 | STOP unless git history available | Auto-try `git diff HEAD~1` |
| Serena unavailable | WARN, set `serena_available: false` | Grep/Glob for all symbol queries |
| Auggie unavailable | WARN, fall back to Serena-only grounding | `get_symbols_overview` + `find_symbol` |
| `confidence-calibrator` agent fails | Inline orchestrator calibration | Mark `calibration: inline-fallback` |
| `root-cause-analyst` agent fails | Continue with coverage map only | Flag as `root_cause_unavailable` |
| `sc:adversarial-protocol` fails | Use highest-confidence agent output | Flag as `adversarial_unavailable` |
| `evidence-validator` agent fails | Inline citation validation | Mark `status: partial` |
| `task-builder` unavailable | Surface report; recommend manual task creation | None |
| All Wave 3 agents fail | Downgrade to T1 report | Report `partial` with T2 failure note |
| User declines remediation | Return success; report stands | None |
| Output path under `.claude/` | STOP before any write | None |
| `--depth deep` on empty spec | STOP; ask for spec | None |
| Token budget exceeded mid-Wave-3 | Hard abort with partial state | `--resume` support |

## 12. Boundaries

### Will

- Build a spec-to-code coverage map using Serena symbol tools
- Classify deviations using a 4-class taxonomy with documented authorization oracle
- Delegate calibration to `confidence-calibrator`, investigation to `root-cause-analyst`
- Delegate competing-resolution to `sc:adversarial-protocol` Mode A
- Re-validate every citation via `evidence-validator` before report ships
- Persist reflection results to Serena memory for cross-session continuity
- Offer remediation handoff to `task-builder` when user opts in
- Produce versioned return contract for composability with `/sc:task`, `/sc:tasklist`

### Will Not

- **Implement debate/scoring/merge logic** — delegated to `sc:adversarial-protocol` (§7)
- **Investigate root causes of bugs** — delegated to `root-cause-analyst` via `sc:troubleshoot` (§7)
- **Brainstorm alternative approaches** — delegated to `sc:brainstorm-protocol` (§7)
- **Generate or apply code fixes** — only `task-builder` produces remediation tasks; sc:reflect never edits source files
- **Run tests or build commands** — sc:reflect is a review skill, not an execution skill; test execution belongs to `/sc:test` or `/sc:validate-tests`
- **Perform SAST/security analysis** — delegated to `sc:analyze` or `security-engineer` agent
- **Maintain a cross-session deviation knowledge graph** — Serena memory stores the last pass summary only; persistent entity tracking is out of scope
- **Auto-execute remediation tasks** — always user-initiated via `/task <path>`
- **Validate non-executable prose or commentary** — only spec-traceable deliverables are in scope
- **Support streaming/interactive reflection** — batch mode only; interactive Socratic dialogue belongs to `sc:brainstorm`
- **Accept `.claude/` output paths** — blocked by policy guard (Wave 0 step 5)
- **Re-implement confidence calibration** — reuses `confidence-calibrator` agent from sc:troubleshoot (§8)
- **Re-implement evidence re-validation** — reuses `evidence-validator` agent from sc:troubleshoot (§8)
- **Re-implement task file generation** — reuses `task-builder` skill (§8)

## 13. Kill List

Features deliberately excluded (with justification):

1. **New `coverage-mapper` agent** — the coverage mapping logic is narrow
   enough to handle inline in Wave 1; a dedicated agent adds coordination
   overhead without sufficient complexity reduction. Extract only if eval
   shows Wave 1 inline logic is fragile.

2. **New `deviation-classifier` agent** — same reasoning as coverage-mapper.
   The 4-class taxonomy is a classification rule over commit messages and
   task logs, not a deep investigation. Inline is cheaper and more auditable.

3. **Streaming / interactive reflection dialogue** — interactive Socratic
   probing is `sc:brainstorm`'s core value. sc:reflect is a batch review
   skill. Adding interactive dialogue would duplicate brainstorm's Wave 1
   and dilute reflect's identity as a validation tool.

4. **Persistent deviation knowledge graph** — Serena memory stores the
   last-pass summary. A full deviation graph with deduplication, temporal
   trending, and cross-project aggregation is a separate product, not a
   skill feature. Start with the minimal `write_memory` key.

5. **Multi-model fan-out in T1** — T1 is intentionally single-agent and
   cheap. Heterogeneous multi-model review is a T2/T3 feature. Running
   parallel models at T1 would violate the "quick first" contract that
   makes sc:troubleshoot's T1 effective.

## 14. Refs

| File | When loaded |
|------|-------------|
| `refs/coverage-map-template.md` | Wave 1 (coverage map schema + deviation taxonomy) |
| `refs/report-template.md` | Wave 4 (report structure) |

Two refs total. Intentionally minimal — the protocol logic lives in this
SKILL.md; refs contain only schema templates. Compare: sc-troubleshoot
has 6 refs, sc-brainstorm has 3. The lean ref count reflects the refactorer's
discipline: every piece of logic that could be inline IS inline; only
structural templates that would bloat the SKILL.md are externalized.

## 15. Token Cost Profile

| Tier reached | Serena/Auggie tokens (offloaded) | Claude tokens (orchestration + agents) | Wall clock |
|--------------|----------------------------------|----------------------------------------|------------|
| T1 only | ~2-4k | ~3-5k | 1-2 min |
| T2 (no adversarial) | ~5-10k | ~10-20k | 3-5 min |
| T2 (with adversarial) | ~10-15k | ~20-40k | 6-10 min |
| T3 added | +0 | +15-25k (task-builder) | +3-5 min |

T1 target: 3-9k Claude tokens. The escalation gate keeps T1 inside this
band for the common case.
