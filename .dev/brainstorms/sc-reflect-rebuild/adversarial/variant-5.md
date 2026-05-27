---
name: sc:reflect-protocol
description: "Tiered reflection and validation protocol — fast Tier 1 single-agent re-grounding, Tier 2 parallel multi-model adversarial review via sc-adversarial, opt-in Tier 3 remediation handoff. Replaces legacy /sc:reflect command."
version: 2.0.0
complexity: tier-3
mcp-servers: [serena, auggie-mcp, sequential, context7, tavily]
allowed-tools: Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill,
  mcp__auggie__codebase-retrieval, mcp__serena__find_symbol,
  mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview,
  mcp__serena__read_memory, mcp__serena__write_memory,
  mcp__serena__list_memories, mcp__serena__get_diagnostics_for_file,
  mcp__serena__activate_project,
  mcp__context7__resolve-library-id, mcp__context7__query-docs,
  mcp__tavily__tavily-search, mcp__sequential-thinking__sequentialthinking
argument-hint: "[--mode pre|post|auto] [--depth quick|standard|deep] [--scope path|symbol] [--output dir] [--fix]"
---

<!-- markdownlint-disable MD013 MD040 -->

# /sc:reflect -- Tiered Reflection & Validation Protocol

## Triggers

`sc:reflect-protocol` is invoked ONLY by the `/sc:reflect` command via
`Skill sc:reflect-protocol` in its `## Activation` section. Never invoked
directly by users.

Activation conditions:
- User runs `/sc:reflect` in Claude Code
- `sc:troubleshoot` Wave 6 Phase B/C delegates a sub-reflection
- `sc:task` post-execution mode delegates a completion validation
- Pipeline composition: `/sc:tasklist | /sc:reflect --mode pre` for
  plan coverage analysis before sprint execution

## 1. Purpose & Identity

Validate agent work — before or after execution — with graduated depth:
Tier 1 is a fast single-agent grounding pass (~1-3 min). Tier 2 fans out
heterogeneous parallel reviewers and debates via `sc:adversarial` (~6-12 min).
Tier 3 is an opt-in remediation handoff to `task-builder` for gap closure.

**Why this works.** Single-model self-review is structurally biased — the
same representational biases that produced the work are present during
re-evaluation. Tier 2 uses heterogeneous model classes so each reviewer's
blind spots differ. The adversarial merge surface ensures the final verdict
has survived independent challenge, not echo-chamber consensus.

**Hallucination contract.** Every claim in the final reflection report must
cite a real `file:line`, a real spec section, or a real command output.
Ungrounded findings are dropped, not downgraded. The `evidence-validator`
agent re-Reads every citation before the report ships.

## 2. Required Input (STOP if missing)

The skill receives at least one of:

- **UC-1 (pre-execution)**: A tasklist OR proposed strategy file + its
  driving spec/PRD/objectives document.
- **UC-2 (post-execution)**: Completed work (commit diff, artifact files,
  task log) + the tasklist that drove it.

**Mode selection** (auto-detect when `--mode auto` or unset):

| Signal | Mode |
|--------|------|
| Input includes diff/commit artifacts, or `--scope` points to git commits | `post` |
| Input is a tasklist/strategy file without completed-work markers | `pre` |
| Both present | `post` (post-execution subsumes pre) |
| Neither present | STOP with usage hint |

**STOP** on empty input: `"Reflect requires input. Usage: /sc:reflect <tasklist-or-diff> [--mode pre|post] [--depth quick|standard|deep]"`

## 3. Tier-Decision Rubric

Tier selection uses five numeric signals scored at Wave 0. Each signal
contributes 0-2 points. Thresholds are explicit and machine-checkable.

### Signal Definitions

| Signal | 0 pts | 1 pt | 2 pts |
|--------|-------|------|-------|
| `scope_size` | < 5 files touched | 5-20 files | > 20 files |
| `task_count` | < 5 tasklist items | 5-15 items | > 15 items |
| `blast_radius` | single-module | cross-module, same package | cross-package or cross-system |
| `spec_density` | spec < 100 lines or absent | 100-500 lines | > 500 lines |
| `ambiguity_signals` | spec has explicit acceptance criteria for every item | some items lack criteria | many items lack criteria OR domain is unfamiliar |

### Tier Mapping

| Composite Score | Tier | Escalation |
|-----------------|------|------------|
| 0-2 | T1 | `--depth quick` only unless forced |
| 3-5 | T1 default, escalate to T2 if confidence < 0.80 after Wave 1 | Rubric-driven |
| 6-8 | T2 | Always escalate |
| 9-10 | T2 mandatory, `--depth deep` | Always escalate |

**Overrides**:
- `--depth quick` or `--no-escalate` forces T1 regardless of score.
- `--depth deep` forces T2 regardless of score.
- Multi-domain span detected (e.g., code + security, build + deployment)
  adds +3 to score (multi-domain risks exceed single-hypothesis coverage).

## 4. Wave/Tier Architecture

```
Wave 0:   Parse + Validate Input + Tier Scoring
Wave 1:   Tier 1 — Grounding + Coverage Map
Wave 1.5: Serena Memory Context Load (always, fail-open)
Wave 2:   Confidence Gate (tier decision)
Wave 3:   Tier 2 — Parallel Multi-Model Review (conditional)
Wave 4:   Tier 2 — Adversarial Merge via sc:adversarial (conditional)
Wave 5:   Synthesis + Report (always)
Wave 6:   Tier 3 — Remediation Handoff (conditional, --fix + user accept)
```

Each wave has explicit entry/exit criteria. Refs loaded per-wave, never
pre-loaded.

### Execution Vocabulary

| Verb | Tool | Scope |
|------|------|-------|
| Invoke Skill | `Skill` | Cross-skill invocation (`sc-adversarial-protocol`) |
| Dispatch Task agent | `Task` | Parallel sub-agent work |
| Read / Load ref | `Read` | File reads, ref loading, artifact inspection |
| Write artifact | `Write` | Creating new files |
| Edit artifact | `Edit` | Modifying existing files |
| Validate | `Read` + `Bash` | File existence, prerequisite validation |
| Parse | (inline) | In-memory YAML/flag parsing — no tool |
| Compose | (inline) | Agent-spec composition — no tool |
| Serena symbol query | `mcp__serena__find_symbol` / `get_symbols_overview` | Structural grounding |
| Serena memory | `mcp__serena__read_memory` / `write_memory` | Cross-session context |

### Wave 0: Parse + Validate Input

**Purpose**: Validate inputs, compute tier score, prepare output directory.

**Steps**:

1. Parse `$ARGUMENTS` into input path(s) + flags.
2. Detect mode (pre/post) per auto-detect table above.
3. Validate input paths exist (Read tool). STOP on missing files.
4. Validate `sc-adversarial-protocol` exists at
   `src/superclaude/skills/sc-adversarial-protocol/SKILL.md`. STOP if
   missing: `"sc:adversarial skill not installed. Required by /sc:reflect v2."`
5. Compute tier score (5 signals). Apply overrides. Record composite in
   audit log.
6. Validate model aliases: check env vars `ANTHROPIC_DEFAULT_OPUS_MODEL`,
   `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL` are
   set. If missing, WARN and degrade gracefully (T2 uses available models
   only; do not abort on a missing alias — heterogeneous duo is better
   than nothing).
7. Create output directory. Default:
   `.dev/reflect/<mode>-<slug>-<YYYYMMDDHHMMSS>/`. If exists and
   non-empty, append `-N` suffix (cap at 99).
8. Open audit log with machine-readable header.

**Exit criteria**: Input validated, tier score computed, output dir ready.
Emit: `"Wave 0 complete: mode=<pre|post> tier-score=<N> tier=<T1|T2>."`

### Wave 1: Tier 1 — Grounding + Coverage Map

**Purpose**: Ground the reflection in real code/spec structure and produce
a coverage map showing what the tasklist covers vs what the spec requires.

**Steps**:

1. **Parallel grounding fan-out** (single message, parallel calls):
   - `mcp__auggie__codebase-retrieval` — query: "Find the structural
     surface area involved in: <spec summary, capped at 300 chars>.
     Include all functions, classes, and files referenced by the tasklist."
   - `mcp__serena__get_symbols_overview` on each file named in the
     tasklist or diff. For post-execution: on each file in the diff stat.
   - If `--scope` provided: narrow all queries to that scope.
   - Fallback (auggie/serena unavailable): `Grep` + `Glob` on tasklist
     keywords. Note degraded mode in audit log.
2. **Coverage map construction**:
   - UC-1 (pre): For each spec requirement/objective, map to tasklist
     items that address it. Surface unmapped spec items as coverage gaps.
   - UC-2 (post): For each tasklist item, map to diff hunks/artifacts
     that satisfy it. Surface unmapped tasklist items as completion gaps.
   - Write to `<output>/coverage-map.md`.
3. **Serena `think_about_collected_information` checkpoint** (mandatory,
   not optional): After step 2, invoke as a scripted protocol checkpoint.
   If the tool returns "concerns" or "incomplete" signals, log them and
   add a Coverage Gap entry. This is a lightweight intra-turn nudge, not
   the heavy reflection logic.
4. **Tier 1 hypothesis** (single-agent): Produce a preliminary
   reflection card at `<output>/tier1-reflection.md` containing:
   - Coverage assessment (% of spec/tasklist items mapped)
   - Deviation inventory (any tasklist item that appears unmapped,
     partially mapped, or mapped to unexpected artifacts)
   - Confidence estimate (0.0-1.0, self-reported, will be calibrated)
   - Best-practice flags (for each mapped item, does the implementation
     follow the domain's established patterns?)
   - `consistency_with_spec`: `aligned | partial | conflicts | no_spec`

**Exit criteria**: Coverage map written, tier 1 reflection card written,
grounding artifacts in audit log. Emit:
`"Wave 1 complete: coverage=<X%> confidence=<Y>."`

### Wave 1.5: Serena Memory Context Load

**Purpose**: Load any prior reflection context from Serena memory to
avoid repeating work and enable cross-session learning.

**Steps**:

1. `mcp__serena__list_memories` — search for keys matching
   `reflect-*` or `reflection-*`.
2. If found, `mcp__serena__read_memory` for the most recent matching
   key. Extract prior deviation patterns, false-positive logs, and
   project-specific reflection history.
3. **Fail-open**: If Serena memory is unavailable, skip this wave and
   add a Grounding Gap entry in the final report. Never abort on memory
   failure — reflection must proceed on current evidence alone.
4. Memory key convention: `reflection/<project-slug>/last-pass` and
   `reflection/<project-slug>/deviation-log-<date>`.

**Exit criteria**: Prior context loaded (or skip recorded). Emit:
`"Wave 1.5 complete: memory=<loaded|skipped>."`

### Wave 2: Confidence Gate

**Purpose**: Decide whether Tier 1 is sufficient or escalation to Tier 2
is warranted.

**Steps**:

1. **Independent calibration** — spawn `confidence-calibrator` agent via
   `Task` with `card_path=<output>/tier1-reflection.md`,
   `rubric_path=<skill-dir>/refs/calibration-rubric.md`,
   `card_tier=1`. The agent re-grades against the 5-dimension rubric
   without formation context (anchoring reduction).
   - **Fallback**: If agent fails, inline-calibrate using the tier-score
     composite as a proxy. Mark `calibration: inline-fallback` in audit.
2. **Decision logic**:
   - `--depth quick` or `--no-escalate` -> STOP at T1.
   - `--depth deep` -> ALWAYS escalate.
   - Tier score >= 6 -> ALWAYS escalate.
   - Calibrated confidence >= 0.85 AND single-domain AND coverage >= 90%
     -> STOP at T1.
   - Otherwise -> escalate to T2. Record `escalation_reason` in audit.

**On STOP**: jump to Wave 5 with `tier_reached=1`.
**On escalate**: proceed to Wave 3.

### Wave 3: Tier 2 — Parallel Multi-Model Review

**Purpose**: Fan out 2-3 heterogeneous reviewers to independently assess
the work, surfacing blind spots that a single reviewer would miss.

**Agent selection**: Spawn 2-3 agents based on available model aliases.
Heterogeneous model assignment is mandatory — never use 3x the same model.

| Available aliases | Agents spawned |
|-------------------|---------------|
| opus + sonnet + haiku | 3 agents: one per model |
| opus + sonnet | 2 agents: one per model |
| sonnet + haiku | 2 agents: one per model |
| opus only | 1 agent (degraded — WARN that T2 is partially effective) |

**Agent persona assignment** (per reviewer):

| Reviewer slot | Persona | Focus |
|---------------|---------|-------|
| Reviewer 1 (strongest model) | analyzer | Root-cause depth, deviation taxonomy precision |
| Reviewer 2 | qa | Coverage completeness, boundary cases, test adequacy |
| Reviewer 3 (if available) | refactorer | Code health, structural adherence, tech debt flags |

**Steps**:

1. **MCP enrichment in parallel with agent spawn**:
   - `mcp__context7__resolve-library-id` + `mcp__context7__query-docs`
     when the spec references specific frameworks/libraries.
   - `mcp__tavily__tavily-search` for best-practice patterns in the
     domain (rate-limited: max 2 queries).
2. **Spawn reviewers** via `Task` (single message, parallel). Each agent
   receives:
   - The input artifacts (spec + tasklist for UC-1; spec + tasklist +
     diff + artifacts for UC-2)
   - The Tier 1 reflection card from `<output>/tier1-reflection.md`
   - The coverage map from `<output>/coverage-map.md`
   - The enrichment results
   - Output path: `<output>/tier2-<reviewer-name>-review.md`
   - Instruction: produce a structured review with sections:
     Coverage Assessment, Deviation Inventory (each deviation classified
     per the taxonomy below), Citation Evidence (every claim cites
     `file:line` or spec section), Confidence (0.0-1.0), Risks.
   - **Steelman requirement**: For every "I disagree with the
     implementation" finding, the reviewer must first state the strongest
     case FOR the implementation before critiquing it.
3. **Wait for all agents**. Read each review.
4. **Per-reviewer calibration** — spawn N `confidence-calibrator`
   instances in parallel (one per review). Use calibrated scores, not
   self-reports, for merge weighting.

**Deviation taxonomy** (4 categories, applied by each reviewer):

| Category | Definition | Example |
|----------|-----------|---------|
| Authorized expansion | Scope addition with explicit prompt or tasklist update | User asked for X+Y in a follow-up; tasklist updated |
| Necessary deviation | Blocked by technical constraint, documented in code/PR | API changed upstream; adapted but spec not yet updated |
| Drift | Silent change not in original spec/tasklist, no documentation | Extra logging added that wasn't requested or discussed |
| Regression | Change that contradicts the spec | Spec says "reject invalid" but code now accepts invalid |

**Exit criteria**: >= 1 review written to disk. A `candidate-reviews.md`
index written listing each review, calibrated confidence, and deviation
count by category. Emit:
`"Wave 3 complete: <N> reviews received."`

**Failure handling**:
- Agent subprocess fails -> continue with remaining; if < 2 complete,
  downgrade to T1 and add a warning.
- MCP fails -> continue without that enrichment; note in audit.
- All agents converge with high confidence -> skip Wave 4; proceed to
  Wave 5 with consensus verdict.

### Wave 4: Tier 2 — Adversarial Merge via sc:adversarial

**Purpose**: When Tier 2 produced competing reviews (disagreement on
deviation classification, different coverage assessments, or conflicting
recommendations), delegate to `sc:adversarial` for structured debate.

**Preconditions**: Wave 3 produced >= 2 reviews with meaningful
disagreement (divergence in any deviation classification, or confidence
spread > 0.15 across reviewers).

**Steps**:

1. **Materialize each review as a standalone artifact** — ensure each
   `<output>/tier2-<name>-review.md` is self-contained.
2. **Invoke `Skill sc-adversarial-protocol`** in compare mode:

   ```
   Skill sc-adversarial-protocol with
     --compare tier2-<r1>-review.md,tier2-<r2>-review.md[,tier2-<r3>-review.md]
     --depth standard
     --focus correctness,coverage,deviation-accuracy
     --output <output>/adversarial/
   ```

3. **Consume return contract** (3-tier guard sequence, per brainstorm
   pattern):
   - Empty response -> FAIL Wave 4.
   - Partial parse without merged_output_path -> FAIL.
   - Missing merged_output_path file -> FAIL.
   - All guards pass -> route by convergence:
     - convergence >= 0.65 -> PASS
     - convergence >= 0.50 -> PARTIAL (surface warning)
     - convergence < 0.50 -> FAIL (report divergence, skip to Wave 5
       with best single review as fallback)
4. **Sanity-check**: spawn `self-review` agent via `Task` against the
   merged reflection. If blocker flagged, surface and downgrade to
   best single calibrated review.

**Fallback protocol** (F1-F3):
- **F1**: Skill tool error -> retry once with `--depth quick`.
- **F2**: Retry fails -> use highest-calibrated single review. Emit error.
- **F3**: All fail -> write `<output>/reflect-failed.md` with partial
  state. Exit.

**Exit criteria**: Merged reflection available (PASS/PARTIAL) or best
single review selected (FAIL). Adversarial artifacts archived under
`<output>/adversarial/`. Emit:
`"Wave 4 complete: adversarial merge (convergence: X.XX, status: <PASS|PARTIAL|FAIL>)."`

### Wave 5: Synthesis + Report

**Purpose**: Produce one reflection report at `<output>/REPORT.md`
regardless of tier reached.

**Refs Loaded**: `refs/report-template.md` (lazy load, not before now).

**Steps**:

1. Load report template.
2. Compose `REPORT.md` filling in:
   - Header (mode, tier reached, confidence, escalation reason)
   - Summary (2-4 sentence executive summary)
   - Coverage Assessment (per the coverage map, with % mapped and gap list)
   - Deviation Inventory (each deviation with classification, evidence
     citation, and severity)
   - Validated vs Unauthorized breakdown (summary counts per taxonomy
     category)
   - Best-Practice Compliance (per-domain assessment)
   - Risks (what could go wrong if current state ships)
   - Recommendations (concrete, actionable next steps)
   - Grounding Gaps (anywhere evidence was unavailable or degraded)
3. **Evidence validation pass** (non-negotiable):
   - Spawn `evidence-validator` agent via `Task` with
     `report_draft_path=<output>/REPORT.md.draft`.
   - Agent re-Reads every `file:line` citation, drops unfounded items.
   - Apply verdict: remove dropped citations; if any dropped, set
     `status: partial` and add Grounding Gap entries.
   - **Fallback**: If agent fails, inline-validate citations in the
     orchestrator context. Mark `status: partial`. Never ship without
     validation.
4. **Serena `think_about_whether_you_are_done` checkpoint** (mandatory):
   After validation pass, invoke as a scripted completion gate. If it
   surfaces "not done" signals, log them and add to Grounding Gaps.
5. **Serena memory write**: Write reflection summary to Serena memory:
   `reflection/<project-slug>/last-pass` with key findings, deviation
   patterns, and false-positive notes. Fail-open (never abort on write
   failure).
6. Write final `REPORT.md`.
7. Append machine-readable footer to audit log.
8. Surface to user: one-paragraph summary + report path + tier reached +
  confidence + next-step recommendation.

**Exit criteria**: `REPORT.md` written, audit log finalized, user
notified, memory persisted (or skip recorded). If `--fix` not set,
return output contract and STOP.

### Wave 6: Tier 3 — Remediation Handoff

**Preconditions**: `--fix` set AND `REPORT.md` is `success` (not
`partial`) AND user explicitly accepts.

**Steps**:

1. Present remediation offer. Ask yes/no. Wait.
2. On accept:
   - Invoke `task-builder` via `Skill` with BUILD_REQUEST whose GOAL is
     "Close the gaps and deviations identified in `<REPORT.md path>`",
     WHY is the summary, WHERE is the cited files, TEMPLATE is generic.
   - Surface task file path + literal command (`/task <path>`).
   - Do NOT auto-execute.
3. On decline: return success; report is final deliverable.

**Exit criteria**: Task file path returned (or decline recorded).

## 5. Modern Serena Tool Usage

The legacy `think_about_*` triad from reflect-v1 is retained but
repositioned as **mandatory scripted checkpoints** (not optional
self-nudges). They fire at defined protocol moments:

| Tool | When invoked | Purpose |
|------|-------------|---------|
| `think_about_collected_information` | End of Wave 1 (after coverage map) | Is evidence complete enough for a verdict? |
| `think_about_task_adherence` | Wave 5 step 2 (after report composition) | Does the report address the original input scope? |
| `think_about_whether_you_are_done` | Wave 5 step 4 (after evidence validation) | Are there unresolved items that need surfacing? |

The **heavy reflection logic** uses the modern symbolic surface:

| Tool | Phase | Purpose |
|------|-------|---------|
| `get_symbols_overview` | Wave 1 | Structural map of touched files |
| `find_symbol` + `find_referencing_symbols` | Wave 3 per-reviewer | Verify that referenced symbols exist and match claims |
| `get_diagnostics_for_file` | Wave 5 pre-report | Catch any LSP errors in touched files |
| `read_memory` / `write_memory` | Wave 1.5 / Wave 5 | Cross-session context persistence |
| `list_memories` | Wave 1.5 | Discover prior reflection history |
| `activate_project` | Wave 0 | Ensure project activation before any symbol queries |

All Serena calls are **fail-open**. If Serena is unavailable, fall back
to `Grep`/`Glob`, log degraded mode, keep going. Never abort the
protocol on an MCP failure.

**Context-freshness refresh-tool selection** (per CLAUDE.md):

| Content type | Tool |
|--------------|------|
| Exact line numbers / file content | `Read` |
| Symbolic queries (which function, where defined) | `mcp__serena__find_symbol` |
| Cross-cutting ("is there an X anywhere") | `mcp__auggie__codebase-retrieval` |
| Runtime state (permissions, diagnostics) | `Bash` (read-only) |

## 6. Cross-Skill Integration

| Skill | Integration point | Mode |
|-------|------------------|------|
| `sc-adversarial-protocol` | Wave 4: merge competing Tier 2 reviews | Mode A `--compare` |
| `confidence-calibrator` (agent) | Wave 2 calibration, Wave 3 per-reviewer | Task spawn |
| `evidence-validator` (agent) | Wave 5 evidence pass | Task spawn |
| `self-review` (agent) | Wave 4 sanity check, T1 fallback | Task spawn |
| `root-cause-analyst` (agent) | UC-2 deviation investigation in Wave 3 | Task spawn |
| `task-builder` | Wave 6 remediation handoff | Skill invocation |
| `sc:troubleshoot` | Wave 6 Phase B/C sub-delegation | Skill invocation |
| `rf-qa` / `rf-qa-qualitative` | UC-2 T2 structural + content verification | Task spawn (with ADVERSARIAL STANCE + fix_authorization) |
| `tech-research` | Wave 3 best-practice enrichment for unfamiliar domains | Skill invocation |

**No duplicate implementation.** This skill delegates debate, scoring,
and merge to `sc-adversarial`. It delegates confidence calibration to the
`confidence-calibrator` agent. It delegates evidence validation to the
`evidence-validator` agent. The skill itself is pure orchestration.

## 7. Agent Delegation Map

| Wave | Agent | Model | Purpose |
|------|-------|-------|---------|
| Wave 1 | (orchestrator inline) | opus | Coverage map + T1 reflection |
| Wave 1.5 | (serena memory) | n/a | Context load |
| Wave 2 | `confidence-calibrator` | opus | Independent re-grading |
| Wave 3 | `root-cause-analyst` | strongest available | UC-2 deviation investigation |
| Wave 3 | `rf-qa` (ADVERSARIAL STANCE) | varies | UC-2 structural verification |
| Wave 3 | `rf-qa-qualitative` | varies | UC-2 content verification |
| Wave 3 | `confidence-calibrator` (xN) | opus | Per-reviewer calibration |
| Wave 4 | `self-review` | sonnet | Post-merge sanity check |
| Wave 5 | `evidence-validator` | opus | Citation re-verification |
| Wave 6 | `task-builder` | opus | Remediation task file |

**Reviewer model heterogeneity**: Tier 2 reviewers MUST run on different
model classes. If only one model alias is available, WARN that T2 is
degraded (single-model self-review has structural bias per Mehta 2026).

## 8. Build Path Decision

### 8.1 Sprint CLI path

The Sprint CLI (`superclaude sprint run <tasklist-index.md>`) executes a
tasklist of work through supervised phases with retry, checkpointing,
anti-instinct hooks, KPI tracking, and trailing-gate validation. It
orchestrates Claude Code as a subprocess via PTY.

**For this skill build, Sprint CLI would look like**:
1. Author a `tasklist-index.md` with phases: Phase 1 scaffold (SKILL.md
   + refs/ + frontmatter), Phase 2 eval harness (SPEC.md + evals.json +
   grader.py), Phase 3 pilot runs, Phase 4 iteration.
2. `superclaude sprint run .dev/tasks/reflect-rebuild-index.md` to
   execute each phase as a supervised Claude Code session.

**Pros**: Production-grade execution, checkpoint persistence, automatic
phase gating, anti-instinct hooks prevent shortcuts, KPI tracking gives
quantitative sprint metrics.

**Cons**: Sprint CLI is designed for multi-file *feature* work spanning
many phases. A single-skill build is fundamentally an eval-driven
iteration loop (draft -> eval -> rewrite -> eval -> ...), which Sprint
treats as N sequential phases rather than a tight loop. Sprint also
requires the tasklist to exist before execution begins — but the eval
harness design IS part of the build. Bootstrapping problem: you need the
eval to judge the skill, but you need the skill to run the eval.
Additionally, Sprint runs Claude Code as a subprocess — it cannot
directly invoke `Skill sc-adversarial-protocol` or `Skill sc-reflect-protocol`
mid-sprint because the skill being built does not yet exist as an
installable artifact.

### 8.2 Skill-creator path

The Anthropic skill-creator plugin (`/skill-creator`) provides an
explicit draft -> eval -> rewrite loop with `run_eval.py`, `run_loop.py`,
`quick_validate.py`, an HTML review viewer, and parallel sub-agents
(grader, comparator, analyzer).

**For this skill build, skill-creator would look like**:
1. `/skill-creator Create sc-reflect-protocol` to draft the initial
   SKILL.md + refs/.
2. Define test cases in `benchmark.json` (each case = a reflect prompt +
   verifiable assertions on the output).
3. `/skill-creator Eval` to run test cases with the draft skill loaded.
4. Review results in HTML viewer. Identify failing assertions.
5. `/skill-creator Improve` to iterate on the SKILL.md.
6. Repeat steps 3-5 until assertion pass rate stabilizes.

**Pros**: Purpose-built for the exact task (skill authoring +
eval-driven iteration). The grader/comparator/analyzer sub-agents are
already wired. The HTML review viewer gives immediate visual feedback.
The `benchmark.json` format matches the eval harness pattern in
`.dev/eval-workspaces/sc-brainstorm/`. Skill-creator understands that
the skill under test is the artifact being built — no bootstrap problem.

**Cons**: Skill-creator's default eval workspace is a sibling directory
under `.claude/skills/<name>-workspace/` — forbidden by CLAUDE.md
ABSOLUTE RULE (Plugin Override). Must redirect to
`.dev/eval-workspaces/sc-reflect/` (enforced by the PreToolUse hook in
`.claude/settings.json`). Skill-creator also produces skills in its own
format, which may need adjustment to match this repo's conventions
(frontmatter schema, refs/ layout, allowed-tools format).

### 8.3 Hybrid path (RECOMMENDED)

Combine both mechanisms at their strongest lifecycle stage:

**Stage 1: Skill-creator for draft + eval iteration (stages 1-3)**.
Use `/skill-creator Create` for the initial SKILL.md + refs/ scaffold,
then `/skill-creator Eval` + `/skill-creator Improve` for the tight
eval-driven loop. The eval workspace is at
`.dev/eval-workspaces/sc-reflect/` (PreToolUse hook enforces this).

Why: The eval-driven nature of this skill (Tier-3 protocol with
multi-agent delegation, return-contract requirements, deviation taxonomy
precision) demands many rapid draft-eval-rewrite cycles. Skill-creator's
`run_loop.py` and HTML viewer are purpose-built for exactly this.

**Stage 2: Hand-author the command file + sync**.
Edit `src/superclaude/commands/reflect.md` to be a thin dispatch wrapper
(frontmatter + `## Activation` calling `Skill sc:reflect-protocol`),
replacing the current 112-line monolith. Edit `src/superclaude/skills/
sc-reflect-protocol/SKILL.md` (the skill-creator output, adjusted to
repo conventions). Run `make sync-dev` to mirror to `.claude/`.

Why: The command file and any repo-convention adjustments (frontmatter
schema, allowed-tools format, memory key naming) belong under
`src/superclaude/` as source of truth per CLAUDE.md ABSOLUTE RULE 1.

**Stage 3: Sprint CLI for integration testing (stage 4)**.
After eval scores stabilize, create a tasklist that runs the completed
skill against real work (e.g., reflect on a completed sc:troubleshoot
run, reflect on a sc:brainstorm output). Execute via
`superclaude sprint run` to validate end-to-end under production
conditions.

Why: Sprint CLI is the right tool for validating that the built skill
works correctly when invoked by other skills and commands in the
production pipeline. It tests the integration surface, not the skill's
internal logic.

**Concrete pick: Hybrid — skill-creator for draft/eval loop (stages
1-3), hand-author + sync-dev for repo integration (stage 3 boundary),
Sprint CLI for production validation (stage 4).**

Rationale: This skill's Tier-3 complexity and multi-agent delegation
mean the eval-driven iteration phase is the longest and most uncertain
part of the build. Skill-creator is purpose-built for that phase. But
the repo's source-of-truth discipline (CLAUDE.md ABSOLUTE RULE 1),
the sync-dev/verify-sync pipeline, and the lint-architecture checks
require hand-authoring under `src/superclaude/` and flowing through
`make sync-dev`. Neither mechanism alone covers the full lifecycle.

## 9. Ops Integration

### 9.1 Makefile targets

Existing targets used by this skill's build:

| Target | Purpose | Frequency |
|--------|---------|-----------|
| `make sync-dev` | Mirror `src/superclaude/` edits to `.claude/` | After every edit to src/ |
| `make verify-sync` | Confirm src/ and .claude/ match | Before every commit |
| `make lint` | Ruff linter | Before every commit |
| `make lint-architecture` | Bidirectional command<->skill link, size limits | Before every commit |
| `make test` | Pytest suite | Before every commit |

New targets proposed for this skill:

| Target | Purpose | When run |
|--------|---------|----------|
| `make reflect-eval` | Run the reflect eval harness (`grader.py` against current SKILL.md) | During eval iteration, before release |
| `make reflect-eval-quick` | Run only the 3 pilot eval cases (fast smoke test) | During rapid iteration |
| `make eval-skill SKILL=sc-reflect-protocol` | Create `.dev/eval-workspaces/sc-reflect-protocol/` | Once (setup) |

Total: 3 new targets (2 eval runners + 1 existing generic).

### 9.2 File-layout discipline

```
src/superclaude/                          # SOURCE OF TRUTH (edit here)
  commands/reflect.md                     # Thin dispatch wrapper
  skills/sc-reflect-protocol/
    SKILL.md                              # Protocol (~500 lines)
    refs/
      calibration-rubric.md               # 5-dimension calibration rubric
      report-template.md                  # REPORT.md template
      deviation-taxonomy.md               # 4-category deviation definitions
      review-checklist.md                 # Per-reviewer checklist

.claude/                                  # SYNC-DEV OUTPUT (never edit directly)
  commands/sc/reflect.md                  # Mirror of src/.../reflect.md
  skills/sc-reflect-protocol/             # Mirror of src/.../sc-reflect-protocol/

.dev/                                     # BUILD + EVAL ARTEFACTS
  eval-workspaces/sc-reflect-protocol/    # Eval workspace (NEVER .claude/skills/*-workspace/)
    SPEC.md                               # Full v2 spec
    grader.py                             # Copied + extended from sc-brainstorm
    evals/evals.json                      # Test cases
    iterations/
      iteration-1/                        # 3 pilot cases
      iteration-2/                        # Full matrix
    skill-snapshot/
      reflect-v1.md                       # Frozen v1 baseline (current 112-line file)
```

**The `-f` rule**: If `git add` requires `-f` on any `.claude/` path
(except `.claude/settings.json`), that `-f` is the violation siren.
STOP. Move the change to `src/superclaude/`, run `make sync-dev`, stage
only the `src/` side.

### 9.3 PreToolUse hook awareness

The `.claude/settings.json` PreToolUse hook rejects writes to
`.claude/skills/*-workspace/**` with a redirect to
`.dev/eval-workspaces/<skill-name>/`. This skill's eval workspace MUST
land at `.dev/eval-workspaces/sc-reflect-protocol/` to pass the hook.
The `.gitignore` also matches `.claude/skills/*-workspace/` so any
misplaced workspace cannot be committed.

### 9.4 sync-dev / verify-sync pre-commit hook compliance

The pre-commit hook runs `make verify-sync` to catch drift between
`src/superclaude/` and `.claude/`. The build workflow:

1. Edit `src/superclaude/skills/sc-reflect-protocol/SKILL.md`.
2. Edit `src/superclaude/commands/reflect.md`.
3. Run `make sync-dev`.
4. Run `make verify-sync` (must exit 0).
5. Run `make lint-architecture` (must confirm bidirectional link +
   frontmatter completeness).
6. Stage ONLY `src/` and `.dev/` paths. NEVER stage `.claude/` paths.

### 9.5 CI compatibility

**Eval harness in CI**: Yes, the `make reflect-eval` target is
CI-compatible. The grader.py is deterministic and side-effect-free (same
pattern as `.dev/eval-workspaces/sc-brainstorm/grader.py`). It reads
files, checks assertions, writes grading.json. No network calls. No
model inference (assertions are structural).

**Cadence**: Run on every PR that touches `src/superclaude/skills/sc-reflect-protocol/`
or `src/superclaude/commands/reflect.md`. The `reflect-eval-quick` target
(3 pilot cases) runs in < 30s. The full `reflect-eval` runs in < 2 min.

**Assertion DSL extensions needed**: The existing grader.py supports 8
assertion types. For reflect-specific checks, add:
- `citation_resolves` — verify every `file:line` citation in the report
  resolves to a real file (requires a small Read-based checker).
- `deviation_classified` — verify every deviation in the report has a
  taxonomy tag matching one of the 4 categories.

## 10. Versioned Return Contract

### Stable Contract (contract_version: 1.0)

```yaml
contract_version: "1.0"
status: success | partial | failed | dry-run
mode: pre | post
tier_reached: 1 | 2 | 3
report_path: <path>
audit_log_path: <path>
confidence: <float 0.0-1.0>
escalation_reason: <string | none>
coverage_pct: <float 0.0-1.0>
deviations:
  authorized_expansion: <int>
  necessary_deviation: <int>
  drift: <int>
  regression: <int>
adversarial_artifacts_dir: <path | null>
task_file_path: <path | null>
remediation_offered: <bool>
remediation_accepted: <bool>
grounding_gaps: [<list of strings>]
```

### Telemetry Block (non-stable)

```yaml
wave_durations_ms:
  wave_0: <ms>
  wave_1: <ms>
  wave_1_5: <ms>
  wave_2: <ms>
  wave_3: <ms>
  wave_4: <ms>
  wave_5: <ms>
  wave_6: <ms>
tier_score:
  scope_size: <0-2>
  task_count: <0-2>
  blast_radius: <0-2>
  spec_density: <0-2>
  ambiguity_signals: <0-2>
  composite: <0-10>
reviewer_models: [<list of model aliases used>]
calibration_method: agent | inline-fallback
evidence_validator_used: <bool>
serena_memory_loaded: <bool>
```

## 11. Eval Rubric

### Dimensions (5 axes, 0-5 scale each)

| Dimension | Weight | 1 (poor) | 3 (acceptable) | 5 (excellent) |
|-----------|--------|-----------|-----------------|----------------|
| **Citation accuracy** | 0.25 | < 50% of citations resolve | 70-85% resolve | > 95% resolve, all grounded |
| **Coverage completeness** | 0.25 | < 60% of spec/tasklist items addressed | 80-90% addressed | 100% addressed with gap analysis |
| **Deviation-classification precision** | 0.20 | Frequent misclassification | Mostly correct, edge-case errors | Correct classification for every deviation |
| **Recommendation actionability** | 0.15 | Vague advice ("improve code quality") | Concrete but lacks file paths | Specific file:line + code-level guidance |
| **Best-practice compliance** | 0.15 | No domain-specific assessment | Identifies obvious violations | Assesses against framework-specific standards |

### Acceptance Thresholds

| Tier | Assertion pass rate | Weighted dimension score | Latency |
|------|-------------------|-------------------------|---------|
| T1 | >= 80% | >= 3.0/5.0 | < 3 min |
| T2 | >= 90% | >= 3.5/5.0 | < 12 min |
| Ship gate (final) | >= 85% (held-out) | >= 3.5/5.0 | Per-tier |

### Iteration Harness

Location: `.dev/eval-workspaces/sc-reflect-protocol/`

**Iteration 1**: 3 pilot cases:
- `eval-pre-trivial` — single-file pre-execution validation (T1 expected)
- `eval-post-small` — 5-file diff post-execution review (T1/T2 boundary)
- `eval-post-large` — 25-file cross-package post-execution review (T2 mandatory)

**Iteration 2**: Expand to 12 cases covering:
- Mode: pre x 4, post x 8
- Depth: quick x 4, standard x 5, deep x 3
- Domain: code, architecture, product, security
- Special: blind mode, multi-domain, no-spec (coverage-only)

**Iteration 3** (if needed): Add edge cases:
- Empty tasklist, conflicting spec, git merge conflict artifacts,
  non-code artifacts (docs, configs).

**Convergence criterion**: Ship at iteration N if iteration N+1 shows
< 5% absolute improvement on held-out test set (60/40 train/test split).

## 12. Error Handling Matrix

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| Empty input | STOP with usage hint | None |
| `sc-adversarial-protocol` missing | STOP with install instruction | None |
| Input files missing | STOP with file-not-found | None |
| Mode auto-detect ambiguous | Default to `post`; WARN | User can pass `--mode pre` |
| Tier score computation fails | Default to T2 (safe escalation) | Manual `--depth` override |
| Serena unavailable (all calls) | Run in degraded mode (Grep/Glob grounding); WARN; add Grounding Gap | None |
| Auggie unavailable | Fall back to Serena `get_symbols_overview`; then Grep/Glob | quality_tier=fallback_1 then fallback_2 |
| `confidence-calibrator` agent fails | Inline-calibrate using tier-score composite; mark `calibration: inline-fallback` | Do not block escalation |
| All T2 agents fail | Downgrade to T1 result; report `partial`; recommend rerun | None |
| `sc-adversarial` returns convergence < 0.50 | Use highest-calibrated single review; surface divergence warning | None |
| `sc-adversarial` empty/unparseable response | FAIL Wave 4; fall back to best single review | None |
| `evidence-validator` agent fails | Inline-validate citations; mark `status: partial` | Never ship without validation |
| `self-review` flags blocker | Surface blocker; do not proceed to Wave 5 with broken merge | None |
| `task-builder` unavailable in Wave 6 | Surface fix recommendations as text; suggest manual task creation | None |
| User declines remediation | Return success; report is final deliverable | None |
| `--depth deep` on under-specified input | STOP at Wave 0; ask user for more detail | None |
| Output dir collision | Append `-N` suffix; cap at 99; STOP at 100 | None |
| Model alias missing (e.g., no HAIKU) | WARN; spawn reviewers on available models; T2 degraded | Do not abort on missing alias |
| PreToolUse hook blocks write to `.claude/skills/*-workspace/` | Redirect to `.dev/eval-workspaces/sc-reflect-protocol/` | Never bypass the hook |
| `make verify-sync` detects drift after edit | Re-edit `src/superclaude/`, re-run `make sync-dev`, re-verify | Never stage `.claude/` paths |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` unset | WARN; T2 uses available models; do not abort | Heterogeneous duo is acceptable |

## 13. Boundaries

**Will:**

- Orchestrate tiered reflection with graduated depth (T1 -> T2 -> T3)
- Auto-detect mode (pre/post) from input shape
- Use heterogeneous multi-model review in Tier 2
- Delegate debate/scoring/merge to `sc:adversarial-protocol`
- Validate every citation via `evidence-validator` before report ships
- Persist reflection summaries to Serena memory for cross-session learning
- Produce versioned, two-block return contract for composability
- FAIL fast on empty/malformed adversarial responses
- Honor `--depth quick` and `--no-escalate` to keep T1 cheap

**Will Not:**

- Re-implement adversarial debate, scoring, or merge logic
- Apply code changes (reflection produces reports, not edits)
- Auto-execute Tier 3 task files (user-initiated `/task` invocation only)
- Silently downgrade missing sub-skills or agents (STOP and surface)
- Activate `ANTHROPIC_DEFAULT_*` env var swapping for unavailable models
- Inject raw user input strings into agent-spec custom instructions
- Stage or commit `.claude/` paths (source of truth is `src/superclaude/`)
- Place eval workspaces under `.claude/skills/*-workspace/`
- Bypass PreToolUse hooks or `make verify-sync` failures
- Ship a `REPORT.md` whose `file:line` citations have not been validated
