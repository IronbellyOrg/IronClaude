# Codebase Context — `/sc:reflect` Rebuild

Wave 2A enrichment for the brainstorm titled *"Rebuild /sc:reflect as a tiered,
parallel multi-model protocol skill"*. All file:line citations re-verified
against on-disk content in worktree `feat-reflect-v2` immediately prior to
write. Paths are repo-root-relative unless prefixed with `/`.

---

## 1. Current `/sc:reflect` Implementation

### 1.1 Source-of-truth file

The canonical (and **only**) /sc:reflect surface in this repo is:

- `src/superclaude/commands/reflect.md` — 112 lines.

The `.claude/commands/sc/reflect.md` mirror is **absent** in this worktree
(checked at `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/.claude/commands/sc/reflect.md` — ENOENT).
That is consistent with the CLAUDE.md absolute rule that `.claude/{commands,skills,agents,…}`
is gitignored sync-dev output, regenerated from `src/superclaude/` via `make
sync-dev`. The mirror appears after install; absence in the worktree is
expected and **not** a bug.

There is **no companion skill** at `src/superclaude/skills/sc-reflect-protocol/`
(verified — directory does not exist). Every sibling Tier-3 command in this
repo (`sc:brainstorm`, `sc:troubleshoot`, `sc:adversarial`, `sc:roadmap`,
`sc:tasklist`, `sc:task`, `sc:validate-roadmap`, `sc:pm`,
`sc:cleanup-audit`, `sc:auggie-review`, `sc:cli-portify`, `sc:recommend`,
`sc:release-split`, `sc:review-translation`, `sc:validate-tests`) has a
matching `src/superclaude/skills/sc-<name>-protocol/SKILL.md`. `reflect`
is the lone exception. This is the structural gap the rebuild fills.

### 1.2 What the file declares

Frontmatter (`src/superclaude/commands/reflect.md:1-8`):

```yaml
name: reflect
description: "Task reflection and validation using Serena MCP analysis capabilities"
category: special
complexity: standard
mcp-servers: [serena, context7]
personas: []
```

Notable: `complexity: standard`, no personas, no `allowed-tools` list,
no `argument-hint`, no `Activation` section, no `Skill <name>` dispatch.

### 1.3 Behavioral Flow (lines 25-32)

Six numbered steps: Analyze → Validate → Reflect → Re-scrutinize → Document
→ Optimize. Step 4 ("Re-scrutinize") was added more recently — it deals
with executable-artifact verification against session facts and Context7
lookups for CLI verb preconditions (lines 30, 47, 65). This is the only
modern surface in an otherwise legacy spec.

### 1.4 Deprecated Serena surface (the load-bearing problem)

`reflect.md` is built almost entirely on the **legacy `think_about_*`
Serena tools**:

- `think_about_task_adherence` (lines 45, 52, 61)
- `think_about_collected_information` (lines 45, 53, 62)
- `think_about_whether_you_are_done` (lines 45, 54, 63)
- Plus the memory pair `read_memory` / `write_memory` / `list_memories` (line 46, 55)

These `think_about_*` tools are not in the modern Serena MCP surface used
anywhere else in this repo. A repo-wide search confirms zero other
`src/superclaude/` files reference them:

```bash
$ grep -rln "think_about_" src/superclaude/ | wc -l
0   # (only reflect.md mentions them)
```

By contrast, the **modern Serena surface** that every other protocol
skill is built on is structural / symbol-aware:

- `mcp__serena__find_symbol`
- `mcp__serena__find_referencing_symbols`
- `mcp__serena__get_symbols_overview`
- `mcp__serena__replace_symbol_body`
- `mcp__serena__write_memory` / `mcp__serena__read_memory`
- `mcp__serena__get_diagnostics_for_file`
- `mcp__serena__search_for_pattern`
- `mcp__serena__activate_project`

Healthy adopters (more in §5):

- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:4` — declares
  `find_symbol, find_referencing_symbols, get_symbols_overview` in `allowed-tools`.
- `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:4` — declares
  `read_memory, write_memory, find_symbol, get_symbols_overview, search_for_pattern, activate_project`.
- `src/superclaude/agents/auggie-reviewer.md:5` — agent tool list cites
  `mcp__serena__find_symbol, mcp__serena__find_referencing_symbols`.

The legacy `think_about_*` surface is essentially a thin self-prompt; it
does not give the protocol any handle on real code structure, real
symbols, or cross-file references. The rebuild should drop it entirely
and ground reflection in the modern symbol-aware + memory surface.

### 1.5 What is missing relative to siblings

Comparing `reflect.md` against any Tier-3 sibling SKILL.md (see §2):

| Surface | reflect.md | sibling Tier-3 |
|--------|------------|-----------------|
| Companion `*-protocol` skill | ❌ none | ✅ always |
| `allowed-tools` frontmatter | ❌ implicit | ✅ explicit MCP list |
| `argument-hint` | ❌ | ✅ |
| Wave/phase architecture | ❌ 6 prose steps | ✅ numbered waves w/ entry+exit |
| `refs/` directory | ❌ | ✅ 3-6 ref files per skill |
| Structured Output Contract / return contract | ❌ | ✅ tabled |
| STOP-on-empty / required-input gate | ❌ | ✅ |
| Multi-model orchestration (model rotation) | ❌ | ✅ (brainstorm: opus/sonnet/haiku) |
| Parallel sub-agent fan-out via `Task` | ❌ | ✅ |
| Adversarial debate hook | ❌ | ✅ (brainstorm, troubleshoot Wave 4) |
| Tiered escalation rubric | ❌ | ✅ (troubleshoot T1→T2→T3) |
| Independent calibration/validation agent | ❌ | ✅ (confidence-calibrator, evidence-validator) |
| Eval workspace under `.dev/eval-workspaces/` | ❌ | ✅ (brainstorm has it; troubleshoot has stub) |

The rebuild's job is to lift `/sc:reflect` from "prose checklist of legacy
Serena verbs" to "Tier-3 protocol skill with the same architectural
discipline as `sc:troubleshoot-protocol` and `sc:brainstorm-protocol`".

---

## 2. Sibling Tier-3 Protocol Skills to Model After

All three live at `src/superclaude/skills/sc-<name>-protocol/`. Each ships
a `SKILL.md` plus a `refs/` directory loaded on-demand per wave.

### 2.1 `sc-troubleshoot-protocol/` — Tiered T1→T2→T3 pattern

**SKILL.md size**: 456 lines. **refs/** contents:

```
refs/doc-discovery.md
refs/escalation-rubric.md
refs/hypothesis-card-template.md
refs/remediation-handoff.md
refs/report-template.md
refs/triage-checklist.md
```

**Architectural summary.** Tiered debugging protocol. T1 is "just look at
it" — single grounded hypothesis in 1-2 minutes. T2 fans out 2-4 parallel
hypothesis agents, runs them through independent calibration, then hands
≥2 competing fixes to `sc:adversarial` for debate, then runs a `self-review`
sanity check on the winning merge. T3 is opt-in remediation chain via
`task-builder`. Escalation is rubric-driven (`refs/escalation-rubric.md`),
never user-typed up front (`SKILL.md:18-22`).

**Structural patterns to steal for `/sc:reflect`:**

- **Tiered escalation gate (Wave 2 confidence gate)** at `SKILL.md:210-227`:
  `--depth quick | --no-escalate → stop at T1`; `--depth deep → always
  escalate`; otherwise `confidence ≥ 0.85 AND single-domain → stop, else
  escalate`. Same shape applies cleanly to reflection: trivial validation
  stops at T1, ambiguous-or-multi-domain reflection escalates.
- **Wave structure** at `SKILL.md:74-85`: Wave 0 parse → Wave 1 grounding
  → Wave 1.5 doc discovery → Wave 1.7 hypothesis form → Wave 2 confidence
  gate → Wave 3 parallel hypotheses (cond.) → Wave 4 adversarial fix
  debate (cond.) → Wave 5 synthesis → Wave 6 remediation chain (cond.).
  Each wave has explicit entry/exit criteria.
- **Refs loaded per-wave, never pre-loaded** (`SKILL.md:87`). Keeps the
  base SKILL.md small enough to load on demand; heavy templates only
  enter context when needed.
- **Output Contract as a frontmatter-style table** (`SKILL.md:38-58`)
  with fields like `status`, `tier_reached`, `report_path`, `confidence`,
  `escalation_reason`, asymmetric-cost flags (`test_is_wrong`,
  `behavior_is_documented`), `hypothesis_cards`, `adversarial_artifacts_dir`,
  `task_file_path`. The pattern of asymmetric-cost flags
  (`SKILL.md:49-71`) is directly transferrable: reflection should surface
  flags like `reflection_recommends_stop`, `deviation_requires_user_call`,
  `cannot_validate_without_user_input` so downstream automation can
  short-circuit without parsing prose.
- **Doc-context card injection into the adversarial channel** (`SKILL.md:291`):
  the Documentation Context Card from Wave 1.5 is appended verbatim into
  each `fix-<N>.md` so the debate is doc-aware without adding a new flag
  on `sc:adversarial`. Reflection can use the identical trick — embed
  the "what was promised" card into each candidate-deviation file so
  debate weighs intent vs implementation.
- **Independent calibration agent** (`SKILL.md:199-202`,
  `SKILL.md:263`): `confidence-calibrator` re-grades each hypothesis card
  against a 5-dim rubric without the formation context, reducing
  anchoring. The agent's calibrated confidence (not the agent's
  self-report) drives Wave 2. Reflection wants the same anchoring
  hygiene: a calibration pass on every reflection finding.
- **Independent evidence validator** (`evidence-validator` agent referenced
  by Wave 5): re-Reads every `file:line` citation in the draft report
  and drops unfounded items. This is the hallucination contract
  (`SKILL.md:24`) — every claim must cite a real file:line or command
  output; ungrounded findings are *dropped, not downgraded*.
- **Failure-handling table per wave** (e.g. `SKILL.md:178-186`,
  `SKILL.md:273-279`): every wave enumerates "scenario / behavior /
  fallback" rows. Reflection should do the same.
- **MCP enrichment in parallel with agent spawn** (`SKILL.md:251`):
  single-turn fan-out of context7 / tavily / auggie alongside the
  hypothesis agents. Reflection's analogous fan-out: tasklist diff +
  spec diff + commit log in parallel.
- **Fallbacks for missing MCPs and missing sub-agents** are documented
  inline (e.g. `SKILL.md:200` `calibration: inline-fallback`,
  `SKILL.md:204` `hypothesis_source: inline-fallback`). The protocol
  never assumes its sub-agents are available.

### 2.2 `sc-brainstorm-protocol/` — 6-wave architecture, return contract, model rotation

**SKILL.md size**: 421 lines. **refs/** contents:

```
refs/agent-spec-builder.md
refs/handoff-routing.md
refs/socratic-templates.md
```

**Architectural summary.** Orchestrator that turns an ambiguous topic
into unified requirements via: Socratic dialogue → optional enrichment →
agent-spec composition (N personas × 3 models, round-robin) → delegated
parallel proposal generation through `sc:adversarial` → flag-gated
handoff to `/sc:design | /sc:tasklist | /sc:task-builder`. v2 explicitly
does **not** re-implement debate, scoring, or merge logic — those belong
to `sc-adversarial-protocol`. v2's value is orchestration.

**Structural patterns to steal:**

- **6-wave architecture: 0, 1, 2A, 2B, 3, 4** (`SKILL.md:72-77`). Wave 2
  is split into 2A (context enrichment, partial-OK) and 2B (agent-spec
  composition, must-succeed). The A/B split lets enrichment failures
  degrade gracefully while spec composition is a hard gate.
- **Execution Vocabulary table** (`SKILL.md:78-88`) mapping `Verb → Tool
  → Scope`: `Invoke Skill → Skill`, `Dispatch Task agent → Task`, `Read
  / Load ref → Read`, `Compose → (inline)`. Standardises how the
  protocol talks about its own actions; eliminates ambiguity about
  whether a step is a tool call or pure reasoning.
- **Model rotation across 3 active aliases (opus/sonnet/haiku)**
  (`SKILL.md:217-219`): `Round-robin assign: (persona_i, model_(i mod
  len(models)))`. For `--depth deep`: prefer opus for first 2 personas
  (analyzer + architect). Reflection multi-model: rotate
  reviewer/validator/calibrator across opus/sonnet/haiku to surface
  per-model bias.
- **Persona selection priority order** (`SKILL.md:210-215`):
  `--personas flag → --strategy enterprise default → domain-aware
  default → pad/truncate to --proposals count`. The same priority
  ladder fits "reflection persona" selection (qa, analyzer, refactorer).
- **Custom instructions with template substitution** (`SKILL.md:221-230`):
  templates reference `{domain}` and `{strategy}` placeholders but
  **NEVER** the raw user topic (injection risk). All interpolated
  parameters are sanitised (strip `,`, `:`, `'`, `"`, control chars)
  and final spec string is validated by round-tripping through the
  adversarial parser. This is the safety pattern for any reflection
  prompt that takes user-provided strings.
- **Token-budget pre-flight with auto-downgrade** (`SKILL.md:232-238`):
  estimate = `proposals × depth_multiplier × persona_weight`. If
  estimate > 250k AND depth = deep → auto-downgrade proposals to 3 +
  WARN. If > 350k post-downgrade → STOP. Hard kill threshold at Wave 3:
  abort if cumulative tokens > 1.25 × estimate. Reflection needs the
  same envelope for its parallel calibration agents.
- **Dry-run gate** (`SKILL.md:246-251`): `--dry-run` prints composed
  agent-spec + token estimate + intended handoff, then exits with
  `status: dry-run`. Note from memory `feedback_dryrun_skips_subskills.md`:
  `--dry-run` skips sub-skill invocations entirely. For reflection,
  `--dry-run` should preview the validation matrix without running
  calibration agents.
- **Return-contract consumption with empty-response / partial-parse /
  missing-file guards** (`SKILL.md:280-285`): 3-tier guard sequence
  before any status routing — empty response → FAIL; partial parse
  without merged_output_path → FAIL; missing merged_output_path file
  → FAIL. Only after all guards pass does the 3-status routing
  (`SKILL.md:286-289`) kick in. Reflection's "did the adversarial
  reviewer return anything coherent" check should mirror this.
- **F1/F2/F3 fallback protocol** (`SKILL.md:291-294`): F1 retry once
  with reduced depth/proposals, F2 abort + emit error, F3 write
  `<output>/brainstorm-failed.md` with partial state for forensic
  review. Same three-tier fallback fits reflection's adversarial
  invocation.
- **Output artifacts enumerated up-front** (`SKILL.md:54-60`):
  `seed-brief.md`, `merged-requirements.md`, `enrichment/codebase-context.md`,
  `enrichment/research-light.md`, `adversarial/` (6 artifacts),
  `return-contract.yaml`. The reflection skill should declare its
  artifact set the same way: `reflection-brief.md`,
  `validation-report.md`, `enrichment/`, `adversarial/`, `return-contract.yaml`.
- **`Skill` invocation, not command**: brainstorm calls
  `Skill sc-adversarial-protocol` directly (`SKILL.md:278`) — per
  sc:roadmap pattern. Reflection should call sub-skills the same way.
- **Eval workspace bound in frontmatter**: `spec:
  .dev/eval-workspaces/sc-brainstorm/SPEC.md` (`SKILL.md:18`). Ties the
  skill to its versioned spec + eval harness.

### 2.3 `sc-adversarial-protocol/` — Mode A blind merge, convergence scoring

**SKILL.md size**: 3002 lines (the largest skill in the repo by far).
**refs/** contents:

```
refs/agent-specs.md
refs/artifact-templates.md
refs/debate-protocol.md
refs/scoring-protocol.md
```

**Architectural summary.** Generic, reusable adversarial debate +
comparison + merge pipeline. Accepts 2-10 artifacts (Mode A `--compare`
existing files, or Mode B `--source` + `--generate` + `--agents` to
generate variants). 5 sequential steps each producing a documented
artifact: (1) Diff Analysis, (2) Adversarial Debate, (3) Hybrid Scoring
+ Base Selection, (4) Refactoring Plan, (5) Merge Execution. Used as a
generic framework tool by brainstorm, roadmap, and (in this rebuild)
reflect.

**Structural patterns to steal:**

- **Output-path policy guard** (`SKILL.md:41`): refuses `--output` under
  `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` before
  any file is written. Directly enforces the CLAUDE.md ABSOLUTE RULE.
  Reflection's output dir must obey the same guard.
- **Mode A (blind compare) vs Mode B (generate)** (`SKILL.md:55-79`):
  the same skill backs both "I have two artifacts, debate them" and
  "I have a source, generate N variants in parallel, then debate".
  Reflection rebuild can invoke Mode A on candidate deviation reports
  or Mode B on a reflection seed-brief.
- **Three-level debate topic taxonomy (L1 surface / L2 structural / L3
  state-mechanics)** (`SKILL.md:134-177`): auto-tagging assigns each
  diff point exactly one level via signal-term scanning, with `L3 >
  L2 > L1` priority and L2 as fallback. Shared-assumption A-NNN points
  containing state/guard/boundary terms auto-tag L3. Reflection
  inherits this taxonomy automatically when it delegates.
- **Steelman requirement** (`SKILL.md:186`): "Advocates MUST construct
  strongest version of opposing positions before critiquing". The
  reflection skill's own self-review wave should impose the same
  requirement on any "I disagree with the implementation" finding —
  state the strongest case for the implementation first.
- **3-round debate with conditional escalation** (`SKILL.md:183-195`):
  Round 1 parallel (all advocates simultaneously), Round 2 sequential
  rebuttals (standard/deep depth), Round 3 final arguments (deep depth
  AND convergence < threshold). Per-point convergence tracking.
- **Hybrid scoring (50/50 quant + qual)** (`SKILL.md:216-249`):
  quantitative layer: requirement_coverage (0.30) + internal_consistency
  (0.25) + specificity_ratio (0.15) + dependency_completeness (0.15) +
  section_coverage (0.15). Qualitative layer: 30-criterion additive
  binary rubric across 6 dimensions (Completeness, Correctness,
  Structure, Clarity, Risk Coverage, Invariant & Edge Case Coverage)
  with Claim-Evidence-Verdict protocol per criterion. **Edge-case
  floor**: variants <1/5 on Invariant & Edge Case Coverage are
  ineligible as base; floor suspends when all variants score 0/5.
- **Position-bias mitigation** (`SKILL.md:255-259`): pass 1 evaluates
  in input order, pass 2 in reverse, agreement → use verdict,
  disagreement → re-evaluate with explicit comparison prompt citing
  both passes. Reflection should apply the same when comparing
  candidate findings.
- **Tiebreaker protocol** (`SKILL.md:264-268`): top two within 5% →
  level 1 debate performance → level 2 correctness criteria count →
  level 3 input order (deterministic).
- **5 artifacts every run** (`SKILL.md:122, 207, 271-272`):
  `diff-analysis.md`, `debate-transcript.md`, `base-selection.md`,
  `refactor-plan.md`, `merge-log.md`, plus `merged-output.md` — total
  6. Reflection consumes these directly when it delegates.

---

## 3. Reusable Agents Inventory

Source-of-truth directory: `src/superclaude/agents/` (NOT
`.claude/agents/`, which is gitignored sync-dev output per CLAUDE.md).
Enumerated via `ls src/superclaude/agents/`:

```
audit-analyzer.md         audit-comparator.md     audit-consolidator.md
audit-scanner.md          audit-validator.md      auggie-reviewer.md
backend-architect.md      business-panel-experts.md
confidence-calibrator.md  debate-orchestrator.md  deep-research-agent.md
deep-research.md          devops-architect.md     evidence-validator.md
frontend-architect.md     learning-guide.md       merge-executor.md
performance-engineer.md   pm-agent.md             python-expert.md
quality-engineer.md       refactoring-expert.md   repo-index.md
requirements-analyst.md   rf-analyst.md           rf-assembler.md
rf-qa.md                  rf-qa-qualitative.md    rf-task-builder.md
rf-task-executor.md       rf-task-researcher.md   rf-team-lead.md
root-cause-analyst.md     security-engineer.md    self-review.md
socratic-mentor.md        system-architect.md     technical-writer.md
```

Mapping requested agents to reflection lifecycle phases. UC-1 = pre-execution
reflect (am I aligned, am I ready?); UC-2 = post-execution reflect (did I do
what was promised, what deviated?). T1/T2/T3 mirrors the sc-troubleshoot
tier model.

### 3.1 `confidence-calibrator` — `src/superclaude/agents/confidence-calibrator.md`

**Purpose**: Independently re-grades a hypothesis card against a 5-dimension
rubric and returns calibrated confidence plus an escalation recommendation.
Designed to reduce — not eliminate — anchoring bias by stripping formation
context (frontmatter at lines 2-7; "Independence Instruction" section
reinforces it).

**Reflect slot**: **UC-1 T1 (confidence-first reflect)** — re-grade the
user's intended approach against the spec. **UC-2 T2** — re-grade each
parallel reviewer's deviation finding so the synthesis weights calibrated
scores, not self-reports. Direct port of sc:troubleshoot's Wave 1.7 +
Wave 3.5 pattern.

### 3.2 `evidence-validator` — `src/superclaude/agents/evidence-validator.md`

**Purpose**: Independent last-gate validator that re-Reads every `file:line`
citation in a draft report, drops unfounded items, and returns the verified
evidence set. "A pass that drops zero items is suspect" (frontmatter +
Behavioral Mindset). Tools: `Read, Grep, Glob` only — cannot modify files.

**Reflect slot**: **UC-2 T2/T3 final gate** before the reflection report
ships. Every cited `file:line` claim in the deviation report gets
independently re-verified. Hallucinated citations dropped, surfaced as
`status: partial` instead of `status: success`. This is the core
"reflection without hallucination" guarantee.

### 3.3 `rf-qa` — `src/superclaude/agents/rf-qa.md`

**Purpose**: Rigorflow QA Agent — intra-task quality assurance for RF
skill/command outputs. Handles research completeness gates, synthesis
verification, final report validation, task-file integrity checks.
Supports parallel partitioning (multiple QA instances each verify a
subset of files to prevent context rot). Fixes issues in-place when
authorized. Has the full Task / TaskOutput / TaskStop / TeamCreate
tool surface — heavy orchestrator-tier agent.

**Reflect slot**: **UC-2 T2** — partition the tasklist (or diff
hunks) across N rf-qa instances for parallel structural verification.
Per memory `feedback_rfqa_adversarial_pattern.md`: pair explicit
"ADVERSARIAL STANCE" framing with `fix_authorization: true` whenever
spawning rf-qa for MDTM gates.

### 3.4 `rf-qa-qualitative` — `src/superclaude/agents/rf-qa-qualitative.md`

**Purpose**: Content-level QA on assembled documents (PRDs, research
reports, tech references). Checks logical flow, realistic requirements,
no contradictions, no red flags, appropriate audience. Complements
`rf-qa` (structural) by checking whether the content actually makes
sense as a product document. Same heavy tool surface as rf-qa.

**Reflect slot**: **UC-2 T2** content-level pass. When `/sc:reflect`
reflects on documents produced by a wave (specs, PRDs, tech-refs),
this agent verifies the document reads correctly as a product artifact,
in parallel with rf-qa's structural pass. Same adversarial-stance +
fix_authorization discipline applies.

### 3.5 `root-cause-analyst` — `src/superclaude/agents/root-cause-analyst.md`

**Purpose**: Systematically investigate complex problems via
evidence-based analysis + hypothesis testing. Five focus areas:
Evidence Collection, Hypothesis Formation, Pattern Analysis,
Investigation Documentation, Problem Resolution. Behavioral mindset
(lines 14-15): "Follow evidence, not assumptions… Never jump to
conclusions without supporting evidence."

**Reflect slot**: **UC-2 T2** — when a deviation is detected between
tasklist and diff, this agent investigates the root cause (scope
creep? missed requirement? upstream spec change?). Already the
default Tier 1 hypothesis agent in sc:troubleshoot Wave 1.7.

### 3.6 `audit-validator` — `src/superclaude/agents/audit-validator.md`

**Purpose**: Spot-check validator verifying audit finding accuracy by
re-testing claims independently. Sample rate: 5 findings per 50 files
audited (10%). Tools: Read, Grep, Glob only, plan permission mode.
"Do NOT assume the prior agent was correct. Verify everything from
scratch."

**Reflect slot**: **UC-2 T3** — when the reflection produces a large
finding set (≥20 items, repo-scale audit), random 10% spot-check by
audit-validator becomes the cheap sanity gate before the report ships.
Lighter alternative to running evidence-validator over every citation.

### 3.7 `self-review` — `src/superclaude/agents/self-review.md`

**Purpose**: Post-implementation validation and reflexion partner.
Runs the four mandatory self-check questions: (1) Tests executed?
(2) Edge cases covered? (3) Requirements matched? (4) Follow-up or
rollback needed? Records reflexion patterns when defects appear.
Used in sc:troubleshoot Wave 4 step 4 as the sanity-check on the
adversarial-merged fix.

**Reflect slot**: **UC-2 T1 (default reflect)** — the cheapest
"did we finish?" pass. For low-complexity tasks the entire `/sc:reflect`
invocation may be a single self-review call. For T2/T3 it remains the
final sanity check after adversarial merge of competing deviation
analyses.

### 3.8 Other potentially-relevant agents

- `debate-orchestrator.md` — used internally by sc:adversarial; reflect
  doesn't invoke directly.
- `auggie-reviewer.md` — independent Claude-side review pass alongside
  Auggie's deep retrieval; could slot into UC-2 T2 for diff review.
  Note: `tools: [Read, Grep, Glob, Bash, mcp__auggie__codebase-retrieval,
  mcp__serena__find_symbol, mcp__serena__find_referencing_symbols]`
  (`auggie-reviewer.md:5`) — modern Serena surface, model `opus`,
  blinded (does not see Auggie's findings until after returning its own).
- `quality-engineer.md` — used by sc:troubleshoot for edge-case
  hypotheses; reusable for reflect.
- `socratic-mentor.md` (310 lines) — Socratic dialogue agent;
  could power UC-1 "are we sure about the approach?" dialogue
  if reflect wants brainstorm-style probing.

### 3.9 Gap-filling agents to author (NEW)

The agent inventory has no agent that's a natural fit for these
reflect-specific roles. Candidates for new agents:

- **`coverage-mapper`** — maps tasklist items / spec requirements to
  diff hunks and surfaces unmapped items (UC-2 T1/T2 default coverage
  pass). Pure analytical agent; tools: Read, Grep, Glob, optional
  `mcp__serena__find_symbol`.
- **`deviation-classifier`** — given a mapped coverage report, classifies
  each deviation as (scope-add, scope-cut, requirement-miss, requirement-
  misinterpretation, upstream-spec-change, refactor-side-effect). Feeds
  the adversarial debate input (UC-2 T2).
- **`tasklist-vs-diff-comparator`** — reads the tasklist, reads the diff
  (or N commits), produces a structured comparison report. The "diff
  half" of the coverage-mapper if you want them split (UC-2 T1).
- **`reflection-synthesizer`** — final-wave synthesizer that consumes
  all calibration reports + adversarial merge + evidence-validator
  output and writes the unified reflection-report.md. Mirrors what
  sc:troubleshoot Wave 5 does inline.

Whether to ship these as new agents vs. inline-orchestrator logic is a
brainstorm decision point. Pattern note: sc:troubleshoot uses dedicated
sub-agents specifically because each one's prompt context can stay
narrow + auditable. Inline logic in the SKILL.md tends to bloat to the
3000-line sc-adversarial size.

---

## 4. Eval-Harness Reference (`sc-brainstorm`)

Path: `.dev/eval-workspaces/sc-brainstorm/` — the only mature eval
workspace in the repo. The others under `.dev/eval-workspaces/` (e.g.
`__ac1_probe__`, `prd-*`, `sc-auggie-review`, `sc-release-split-protocol`,
`sc-troubleshoot`) are stubs or experiments.

### 4.1 Top-level layout

```
.dev/eval-workspaces/sc-brainstorm/
├── SPEC.md                       (44502 bytes — full v2 spec)
├── grader.py                     (10375 bytes — assertion runner)
├── aggregate_iteration.py        (6813 bytes)
├── evals/
│   └── evals.json                (12 cases, expanded from 3 pilot cases)
├── iterations/
│   ├── iteration-1/              (3 pilot cases — A1, B1, C1 in qual rubric)
│   └── iteration-2/              (12 cases — original 3 + deferred 4-12)
└── skill-snapshot/
    └── brainstorm-v1.md          (frozen v1 baseline for A/B comparison)
```

### 4.2 SPEC.md frontmatter

```yaml
spec_id: SC-BRAINSTORM-V2-SPEC
version: 2.0.0
status: draft
created: 2026-05-25
target_release: v4.3.0
spec_type: behavioral-protocol
component_type: command + skill (sc-brainstorm-protocol)
parent_command: /sc:brainstorm
supersedes: src/superclaude/commands/brainstorm.md (monolithic, no skill)
complexity_score: 0.78
complexity_class: high
target_audience: SuperClaude framework developers, brainstorm users
```

The "Key Differentiators vs v1" table at the top of SPEC.md is a clean
template for the reflect rebuild's own spec — every reflect-v1 limitation
gets a v2 column.

### 4.3 evals.json structure

Each eval is one JSON object: `id, name, prompt, topic, expected_domain,
expected_strategy, expected_proposal_count, handoff, special`. 12 cases
total in iteration-2 covering domains (code, incident, product,
architecture, process, research), depths (quick, standard, deep),
handoff targets (none/design/tasklist/task), and special modes (blind,
simulated interactive). For reflect, the analogous matrix would be
`use_case × depth × tier × scope_kind`.

### 4.4 Per-eval directory shape

```
iterations/iteration-1/eval-code-add-rate-limiting/
├── eval_metadata.json     (assertions list — see §4.5)
├── with_skill/            (v2 / new-skill runs)
│   ├── outputs/           (seed-brief.md, merged-requirements.md, etc.)
│   ├── run-1/             (raw run log)
│   └── grading.json       (written by grader.py)
└── old_skill/             (v1 / baseline runs)
    ├── outputs/
    ├── run-1/
    └── grading.json
```

The `with_skill` / `old_skill` partition is the A/B test rig.
`grader.py` runs the same assertions against both halves so deltas are
visible.

### 4.5 Assertion DSL (from `eval_metadata.json` + `grader.py`)

`grader.py` supports these assertion types (`grader.py:106-192`):

- `file_exists` — target exists and is a file.
- `frontmatter_field` — YAML frontmatter field equals expected.
- `section_present` — markdown section matching pattern exists.
- `section_enumerated` — section has ≥ N enumerated items (bullets or
  numbered).
- `yaml_field` — flat YAML field equals expected.
- `yaml_field_min` — flat YAML numeric field ≥ min_value.
- `yaml_substring` — flat YAML field contains any of N substrings.
- `dir_count` — directory has ≥ N files.

Example assertions from `iteration-1/eval-code-add-rate-limiting/eval_metadata.json`:

```json
{"text": "seed_brief.md exists in output dir", "type": "file_exists", "target": "with_skill/outputs/seed-brief.md"}
{"text": "seed-brief frontmatter declares domain: code", "type": "frontmatter_field", "target": "with_skill/outputs/seed-brief.md", "field": "domain", "expected": "code"}
{"text": "merged-requirements has Acceptance Criteria section with ≥4 enumerated items", "type": "section_enumerated", "target": "with_skill/outputs/merged-requirements.md", "section_pattern": "Acceptance Criteria", "min_items": 4}
{"text": "return-contract.yaml convergence_score ≥ 0.50", "type": "yaml_field_min", "target": "with_skill/outputs/return-contract.yaml", "field": "convergence_score", "min_value": 0.50}
{"text": "adversarial dir contains ≥2 proposal files + debate-transcript", "type": "dir_count", "target": "with_skill/outputs/adversarial/", "min_files": 3}
```

This DSL is **directly reusable** for `/sc:reflect`. Reflect-specific
assertions can extend the DSL with `grep_regex` (does the report
mention every tasklist item?) and `citation_resolves` (does every
`file:line` citation resolve to a real file?). The existing DSL is
syntactic; reflect needs at least one semantic assertion type.

### 4.6 grader.py at a high level

`grader.py:23-29` — `read_text(p)` swallows FileNotFoundError /
IsADirectoryError returning None; assertion checkers must handle
None.

`grader.py:31-45` — `parse_frontmatter(text)` parses leading `---` YAML
block into flat dict (string values only, no nesting).

`grader.py:48-61` — `parse_yaml_simple(text)` — flat YAML, no nested
keys, no lists. Sufficient for return-contract.yaml shapes.

`grader.py:64-85` — `find_section(text, section_pattern)` finds (start,
end) char offsets of a markdown section by regex on heading line, ends
at next heading of same-or-higher level. MULTILINE | IGNORECASE.

`grader.py:88-96` — `count_enumerated_items(text, section_pattern)`
counts bullet / numbered items within a section.

`grader.py:99-192` — `check_assertion(assertion, base_dir)` — single
switch on `a_type`, returns `(passed: bool, evidence: str)`.

`grader.py:195-244` — `grade_eval(eval_dir)` partitions assertions by
`with_skill/` vs `old_skill/` prefix, runs each through `check_assertion`,
writes `grading.json` to each side, returns aggregate stats. Output
schema: `{expectations: [{text, passed, evidence}], summary: {passed,
failed, total, pass_rate}}` — matches skill-creator's grading.json
schema (line 11 docstring).

`grader.py:247-269+` — `main()` iterates `iter_dir/eval-*` subdirs,
prints summary table.

The grader is **deterministic and side-effect-free** — perfect base
for a reflect grader. The qualitative `quality-grading.json` (lines
in iteration-1/quality-grading.json) is hand-graded by a "grader_model:
claude-opus-4-7[1m]" using 5 dimensions: concreteness, adversarial_diversity,
coverage, actionability, provenance (1-5 each, total /25). Reflect's
analogous qualitative rubric might be: completeness, faithfulness,
deviation-detection-recall, citation-validity, actionability.

### 4.7 Iteration cycle pattern

What changed between iteration-1 → iteration-2 (per
`evals/evals.json:1-6` and the directory listings):

- **iteration-1**: 3 pilot cases (code-add-rate-limiting,
  incident-staging-deploy-3am, product-ai-changelog), all `--depth
  standard`, `--proposals 3`, `handoff: none`.
- **iteration-2**: 12 cases — original 3 + deferred cases 4-12.
  Adds depth variation (quick, deep), strategy variation (agile,
  enterprise), handoff variation (none, design, tasklist, task),
  blind mode, simulated interactive mode. Adds 6 domains (was 3:
  code/incident/product → now 6: code/incident/product/architecture/process/research).

Pattern: **Iteration N+1 expands the matrix; the assertion DSL stays
stable.** Reflect should plan its eval matrix the same way: start
with 3 pilots covering UC-1 trivial / UC-2 small-diff / UC-2
large-diff, then expand.

### 4.8 Skill snapshot pattern

`skill-snapshot/brainstorm-v1.md` is the frozen v1 baseline used by
`old_skill/` runs. Same file the v2 supersedes. For reflect the
analogous snapshot would be `skill-snapshot/reflect-v1.md` =
`src/superclaude/commands/reflect.md` (current 112-line file) frozen
at start-of-rebuild.

---

## 5. Modern Serena Tool Usage in the Existing Codebase

Grepped `find_symbol | get_symbols_overview | find_referencing_symbols
| write_memory | read_memory` across `src/superclaude/skills/` and
`src/superclaude/agents/`. Healthy patterns to copy:

### 5.1 `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:4`

```
allowed-tools: Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill,
  mcp__auggie__codebase-retrieval, mcp__serena__find_symbol,
  mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview,
  mcp__context7__resolve-library-id, mcp__context7__query-docs,
  mcp__tavily__tavily-search, mcp__sequential-thinking__sequentialthinking
```

The reflect rebuild's `allowed-tools` line should match this shape:
explicit MCP names, no `think_about_*`.

### 5.2 `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:139`

```
- `mcp__serena__get_symbols_overview` on the target file or
  `mcp__serena__find_symbol` on a specific function if the issue names one.
```

Wave 1 step 1 pattern: parallel MCP fan-out — one auggie call for broad
context + one serena call for symbol-level precision. Reflect's
analogous fan-out: serena get_symbols_overview on the changed files to
build the structural map of what was actually modified.

### 5.3 `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:382`

```
| `mcp__serena__find_symbol` / `find_referencing_symbols` / `get_symbols_overview` | ✓ | ✓ | — |
```

(In a context-freshness refresh-tool selection table.) The skill
documents *which Serena verb to pick for which content type* — exactly
the table from CLAUDE.md "Refresh-tool selection". Reflect should ship
the same table to enforce freshness discipline on its own findings.

### 5.4 `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:4`

```
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill,
  mcp__auggie-mcp__codebase-retrieval, mcp__serena__read_memory,
  mcp__serena__write_memory, mcp__serena__find_symbol,
  mcp__serena__get_symbols_overview, mcp__serena__search_for_pattern,
  mcp__serena__activate_project
```

Note: uses `mcp__auggie-mcp__` (alternate namespace) — both
`mcp__auggie__` and `mcp__auggie-mcp__` exist in the wild; reflect
should pick one and stick.

### 5.5 `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:126-130`

Tool-purpose table (excerpt):

```
| Read session memory | `mcp__serena__read_memory` | Load validation ledger, terminology, patterns (Pre-Phase 0) — fail-open |
| Write session memory | `mcp__serena__write_memory` | Persist ledger, terminology, patterns (Post-Phase 6) — fail-open |
| Find symbol | `mcp__serena__find_symbol` | Symbol lookup for context supplement (Step 0.5, deep only) — fail-open |
| Get symbols overview | `mcp__serena__get_symbols_overview` | File-level symbol map (Step 0.5, deep only) — fail-open |
```

Pattern: every Serena call is **fail-open**. If Serena is unavailable,
the skill skips that step rather than aborting. Reflect should adopt
the same: missing Serena → fall back to Grep/Glob, log degraded mode,
keep going.

### 5.6 `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:147,155,165,1005,1007,1018,1039-1040,1070-1071`

Memory-keying convention: every memory key includes a project slug to
avoid cross-project contamination:

```
mcp__serena__read_memory key=validation-ledger-{project-slug}
mcp__serena__read_memory key=terminology-map-{project-slug}
mcp__serena__read_memory key=adversarial-patterns-{project-slug}
mcp__serena__read_memory key=pattern-log-{project-slug}
```

With retention rules: "Keep last 20 entries", "Retain top 20 patterns
by effectiveness score", "Expire entries older than 90 days". Reflect's
memory keys (e.g., `reflection-deviation-log-{project-slug}`) need the
same hygiene.

### 5.7 `src/superclaude/skills/sc-task-protocol/SKILL.md:89,101,291,297,307`

```
SKILL.md:89:  4. Check relevant memories (list_memories -> read_memory)
SKILL.md:101: 2. Search downstream impacts (find_referencing_symbols OR grep)
SKILL.md:291: 3. list_memories / read_memory: Check project state
SKILL.md:297: 3. find_referencing_symbols: Trace dependencies
SKILL.md:307: 1. write_memory: Save session state
```

Pattern: `find_referencing_symbols OR grep` — Serena preferred, grep
fallback. List memories first, then read targeted. Save state at end
of wave.

### 5.8 `src/superclaude/skills/sc-pm-protocol/SKILL.md:27-30, 43-44, 50-52, 113, 157, 166`

Heavy memory user — uses memory keys for cross-session continuity:
`pm_context`, `current_plan`, `last_session`, `next_actions`, `plan`,
`checkpoint`, `learning/patterns/[name]`, `learning/mistakes/[timestamp]`.
Slash-paths are conventional. The "learning/" prefix is a nice
namespacing pattern for reflection memories:
`reflection/deviation-patterns/{slug}`, `reflection/false-positives/{slug}`.

### 5.9 `src/superclaude/agents/pm-agent.md:32-35, 54, 67, 93, 109, 114, 133, 245-262`

Same memory pattern at agent level — agent-side reads/writes use the
same keys the skill expects. Pattern transfer: reflection's agents
should read the same keys the reflect skill writes (`reflection/
last-pass`, `reflection/deviation-log-{date}`).

### 5.10 `src/superclaude/agents/auggie-reviewer.md:5, 36, 81`

```
tools: [Read, Grep, Glob, Bash, mcp__auggie__codebase-retrieval,
        mcp__serena__find_symbol, mcp__serena__find_referencing_symbols]
```

Compact tool surface, modern Serena only, no `think_about_*`. Line 81
docstring: "precise symbol-level cross-reference when you need to
confirm who calls what". Line 36: "For each non-trivial change, pull
adjacent context with Read (or mcp__serena__find_symbol)". Direct
template for reflect's per-finding context-pull.

### 5.11 Anti-pattern note

The grep for `think_about_` returns **only** `reflect.md`:

```
$ grep -rln "think_about_" src/superclaude/
src/superclaude/commands/reflect.md
```

This is a single-file island of deprecated Serena surface. Removing it
is the single largest code-debt reduction the rebuild delivers.

---

## 6. Sprint-CLI Build Path vs Skill-Creator Build Path

Two distinct mechanisms exist for building/iterating a Tier-3 skill in
this repo. They serve different lifecycle stages.

### 6.1 Sprint CLI (`src/superclaude/cli/sprint/`)

Files in `src/superclaude/cli/sprint/`:

```
checkpoints.py    classifiers.py    commands.py       config.py
debug_logger.py   diagnostics.py    executor.py       __init__.py
kpi.py            logging_.py       models.py         monitor.py
notify.py         preflight.py      process.py        retrospective.py
summarizer.py     tmux.py           tui.py
```

Entry: `from .commands import sprint_group` (`__init__.py:3`).

`executor.py:1-12` declares it as the "core orchestration loop"
imported from `superclaude.cli.pipeline.models`. Heavy machinery:
multi-phase Claude Code sprint execution with phase results, gate
outcomes, monitor state, tmux pane updates, signal handling, debug
logging, checkpoint persistence. Runs Claude Code as a subprocess
(`process.ClaudeProcess`).

**Build path role**: Once a Tier-3 skill exists, `superclaude sprint
run <tasklist-index.md>` executes a tasklist of work against the
skill end-to-end with supervised phases, retries, anti-instinct hooks,
KPI tracking, and trailing-gate validation. This is the **production
execution path** for a built skill, not the build path itself.

### 6.2 Eval CLI (`src/superclaude/cli/eval/`)

Files: `artifact_layout.py, capabilities.py, claude_process.py,
commands.py, config.py, coverage.py, disk_budget.py, exit_codes.py,
expect.py, hook_adapter.py, isolation.py, loader.py, models.py,
orchestrator.py, pty/, pty_driver.py, pty_stream.py, reporter.py,
retry.py, runner.py, run_report.py, schemas/, signal_handler.py,
suites/`.

Entry (`__init__.py:1`): "IronClaude real-eval harness CLI package".
This is the real-process eval harness — runs Claude Code in a PTY
against suite manifests, captures coverage, enforces capability gates,
budgets disk usage, and produces machine-readable run reports.

**Build path role**: Production-grade eval execution. Same role as
`grader.py` in the sc-brainstorm workspace, but at infrastructure
scale (PTY isolation, hook adapters, signal handlers, disk-budget
quotas). Use when the simple `grader.py` rig outgrows its shoes.

### 6.3 Skill-Creator plugin (`/config/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/`)

The Anthropic skill-creator plugin (loaded from the marketplace, not
this repo). Layout:

```
plugins/skill-creator/
├── README.md
├── LICENSE
├── .claude-plugin/plugin.json
└── skills/skill-creator/
    ├── SKILL.md
    ├── eval-viewer/generate_review.py   (HTML review generator)
    ├── eval-viewer/viewer.html
    ├── agents/{comparator,grader,analyzer}.md
    ├── references/schemas.md
    └── scripts/{run_eval,generate_report,run_loop,quick_validate,
                 improve_description,aggregate_benchmark,
                 package_skill,utils}.py
```

SKILL.md lines 9-26 describe the lifecycle: "Decide what you want the
skill to do → Write a draft → Create test prompts → Run claude-with-
access-to-the-skill on them → Help the user evaluate qualitatively +
quantitatively → Rewrite based on feedback → Repeat → Expand the test
set → Try again at larger scale → Run description improver".

**Build path role**: This is the **early-stage iteration path** — draft
→ eval → rewrite loop with the user. `run_eval.py`, `run_loop.py`,
`quick_validate.py`, `generate_review.py`, `aggregate_benchmark.py`
power the iteration cycle. `package_skill.py` packages for distribution.

### 6.4 Practical difference for the reflect rebuild

| Stage | Tool | Reflect-rebuild use |
|-------|------|---------------------|
| Draft v2 SKILL.md + refs/ + agents | hand-authored under `src/superclaude/` | Start here |
| Initial 3-pilot eval (assertion DSL) | local `grader.py` mirroring `sc-brainstorm` | First eval gate |
| Multi-iteration draft→eval→rewrite loop with HTML review | **skill-creator plugin** (`run_loop.py`, `eval-viewer/generate_review.py`) | After v2 draft compiles |
| Production execution of built skill against tasklists | **sprint CLI** (`superclaude sprint run`) | After eval scores stabilise |
| Real-process eval at scale with PTY isolation + coverage | **eval CLI** (`superclaude eval ...`) | If scale outgrows grader.py |

**Per CLAUDE.md override** (Plugin Override — Skill-Creator Workspace
Destination): the skill-creator plugin's default sibling-workspace
location (`.claude/skills/<name>-workspace/`) is **forbidden** in this
project. Eval workspaces MUST go to `.dev/eval-workspaces/<skill-name>/`.
The PreToolUse hook in `.claude/settings.json` enforces this with a
redirect message; `.gitignore` matches `.claude/skills/*-workspace/`
to prevent commits. **The reflect eval workspace path is therefore
`.dev/eval-workspaces/sc-reflect/`**, mirroring `sc-brainstorm`.

**Natural fit for a multi-phase protocol skill with live-run eval
harness**: hybrid. Use `skill-creator` plugin for the draft/iterate
loop (it has `run_loop.py`, HTML reviewer, comparator/grader/analyzer
sub-agents already wired). Use the local `grader.py` pattern (copy
from `.dev/eval-workspaces/sc-brainstorm/grader.py`) for the
deterministic assertion gate. Use `sprint` CLI only after the skill
ships and is being executed against real tasklists. The eval CLI is
overkill for v1 of the rebuild — defer until pilot reflect runs are
producing reliable artifact shapes.

---

## 7. Anti-Patterns to Avoid

### 7.1 The deprecated `think_about_*` surface (in reflect.md itself)

Covered in §1.4. Repeated here because it's the headline anti-pattern
the rebuild eliminates. `src/superclaude/commands/reflect.md:45-46,
52-55, 61-63` is the only place in the entire `src/superclaude/` tree
that mentions `think_about_*`. This is *legacy Serena* surface — no
modern skill uses it. Rebuild MUST NOT carry it forward.

### 7.2 Implicit / missing `allowed-tools`

`reflect.md` declares `mcp-servers: [serena, context7]` in frontmatter
but no `allowed-tools` list. Compare to
`src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:4` which
enumerates all 11 MCP+native tools explicitly. The implicit-tools
pattern (a) hides the protocol's real dependencies from readers,
(b) prevents the skill loader from validating tool availability up
front, (c) silently regresses to "Claude picks whatever tools" rather
than enforcing the protocol's MCP discipline. Reflect rebuild must
declare `allowed-tools` explicitly.

### 7.3 Monolithic command without backing skill

The SPEC.md "Key Differentiators vs v1" table for brainstorm (read
§4.2) calls this out for brainstorm-v1: "Monolithic command file, no
backing skill". `reflect.md` shares the same anti-pattern. The fix is
the documented sibling pattern: thin command file (frontmatter +
trigger + `## Activation` block that calls `Skill sc:reflect-protocol`)
+ companion `src/superclaude/skills/sc-reflect-protocol/SKILL.md` with
the real behavior + `refs/` for templates.

### 7.4 Skipping the output-path policy guard

If reflect rebuild forgets the output-path policy guard pattern from
`sc-adversarial-protocol/SKILL.md:41`, users will eventually try
`/sc:reflect --output .claude/skills/foo/` and the protocol will
happily write distributable artifacts into a path that violates the
`.claude/`-source-of-truth rule. Always copy the guard.

### 7.5 Letting unbounded sub-skill recursion drain budget

The brainstorm-protocol guards against this with token-budget
pre-flight + auto-downgrade + hard kill threshold (`SKILL.md:232-238`).
A reflect protocol that calls sc:adversarial which calls sc:reflect-
recursively (e.g., user asks the protocol to reflect on its own
intermediate outputs) needs the same envelope. Without it, the
adversarial debate alone can burn 250k tokens before the calibration
agents even start.

### 7.6 Direct edit of `.claude/` mirrors

CLAUDE.md ABSOLUTE RULE forbids it (rule 6 in user-global CLAUDE.md,
plus repeated in project CLAUDE.md). Memory `feedback_hooks_source_of_truth.md`
reinforces it. Reflect rebuild must always edit `src/superclaude/` first,
then `make sync-dev`, then `make verify-sync`. The hook in
`.claude/settings.json` blocks edits to `.claude/` paths; **never pivot
to bypass the hook** (per memory `feedback_no_strategy_pivot_to_avoid_hooks.md`).

---

## 8. CLAUDE.md ABSOLUTE RULES Recap

These three rules are load-bearing for every variant the brainstorm
considers. Variants that violate any of them are inadmissible.

### 8.1 Source-of-truth: `src/superclaude/` + `make sync-dev`

`src/superclaude/` is the canonical location for skills, commands,
agents, and core files. Edit there first, run `make sync-dev` to copy
to `.claude/`, then `make verify-sync` to confirm match. If `.claude/`
was edited directly (e.g., iterating live), copy changes back to
`src/superclaude/` and verify-sync. The pre-commit hook runs
verify-sync to catch drift. **Reflect rebuild lives under
`src/superclaude/skills/sc-reflect-protocol/` and
`src/superclaude/commands/reflect.md`, never under `.claude/`.**

### 8.2 `.claude/` is gitignored except `settings.json`

`.claude/{skills,commands,agents,hooks,templates}/*` is gitignored
sync-dev output. The **only** tracked file under `.claude/` is
`.claude/settings.json`. Never `git add .claude/skills/...`, never
`git add -f` on any `.claude/` path. If `git add` requires `-f` for
`.claude/<not-settings.json>`, that `-f` is the violation siren — STOP,
move the change to `src/superclaude/`, run `make sync-dev`, stage only
the `src/` side. **The reflect rebuild's PR diff includes only
`src/superclaude/` paths plus `.dev/` artifacts; zero `.claude/` paths.**

### 8.3 PR target = fork (`IronbellyOrg/IronClaude`), NEVER upstream

This repo is a fork. `origin = IronbellyOrg/IronClaude`, `upstream =
SuperClaude-Org/SuperClaude_Framework`. **Mandatory command shape**:
`gh pr create --repo IronbellyOrg/IronClaude --base master --head
<branch> --title "..." --body "..."`. A bare `gh pr create` defaults to
the parent repo of a fork and silently lands the PR on public upstream.
Pre-PR: `git remote -v` to confirm origin, `git fetch origin && git log
master..origin/master` to detect divergence + rebase if needed, verify
returned URL points at `https://github.com/IronbellyOrg/IronClaude/pull/N`.
**The reflect-rebuild PR lands on IronbellyOrg/IronClaude; never on
upstream without explicit user authorization in the same session.**

---

## End of Codebase Context

All citations in this document re-verified against on-disk content in
worktree `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/`
immediately prior to write. Wave 2A enrichment artifact for the
`/sc:reflect` rebuild brainstorm; consumed by Wave 2B agent-spec
composition and Wave 3 adversarial proposal generation.
